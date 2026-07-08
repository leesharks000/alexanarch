import os
#!/usr/bin/env python3
"""apply_sentinel0_fixes.py — replace `href="alexanarch.org/s/records/0/"` with
the correct record target for each of the 69 auto-fixable cases identified by
unique-substring anchor-text matching.

For each fix, the anchor text uniquely matches one registry record via title
substring, so we set href to `https://www.alexanarch.org/s/records/<N>/` directly
(bypassing /go/ since these have no DOI and the record number is stable).

Post-application, commits and pushes each affected repo.
"""
import json, subprocess, sys, re
from pathlib import Path
from collections import defaultdict

fixes = json.load(open('/tmp/linkscan/sentinel0_fixes.json'))
TOK = os.environ.get('GH_TOKEN', '')  # set via env var, do not commit
REPOS_DIR = Path('/tmp/linkscan/repos')
ALEX_LIVE = Path('/home/claude/alexanarch')

# Group by repo
by_repo = defaultdict(list)
for fix in fixes:
    by_repo[fix['repo']].append(fix)

def run(cmd, cwd, quiet=False):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if r.returncode != 0 and not quiet:
        print(f'  ! {" ".join(cmd)} → {r.stderr[:200]}', file=sys.stderr)
    return r

def apply_repo(repo_name, repo_fixes):
    """Apply fixes to one repo. Returns (files_changed, applied_count, missed_count)."""
    repo_path = ALEX_LIVE if repo_name == 'alexanarch' else REPOS_DIR / repo_name
    if not repo_path.exists():
        print(f'  ! {repo_name}: path not found')
        return 0, 0, 0

    # Group fixes by file
    fixes_by_file = defaultdict(list)
    for fix in repo_fixes:
        fixes_by_file[fix['file']].append(fix)

    files_changed = 0
    applied = 0
    missed = 0

    for rel_file, file_fixes in fixes_by_file.items():
        p = repo_path / rel_file
        if not p.exists():
            print(f'  ! {repo_name}/{rel_file}: file not found')
            missed += len(file_fixes)
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except Exception as e:
            print(f'  ! {repo_name}/{rel_file}: {e}')
            missed += len(file_fixes)
            continue

        original = text
        for fix in file_fixes:
            # We need to find the specific anchor's sentinel href and rewrite it
            anchor = fix['anchor']
            target_rec = fix['target_record']
            new_href = f'https://www.alexanarch.org/s/records/{target_rec}/'

            # Escape anchor for regex; use a bounded match so we only affect THIS anchor
            anchor_re = re.escape(anchor[:80])
            # HTML pattern: href="...s/records/0/..." ... > <anchor text>
            # We look for either apex or www variant and either exact 0/ or with trailing extra
            patterns = [
                # HTML <a href="alexanarch.org/s/records/0/">…anchor…</a>
                (rf'(<a\s+[^>]*?href\s*=\s*["\'])(https?://(?:www\.)?alexanarch\.org/s/records/0/[^"\']*)(["\'][^>]*>[^<]*?{anchor_re}[^<]*?</a>)', True),
                # Markdown [anchor](alexanarch.org/s/records/0/...)
                (rf'(\[[^\]\n]*?{anchor_re}[^\]\n]*?\]\()(https?://(?:www\.)?alexanarch\.org/s/records/0/[^)\s]*)(\))', True),
            ]
            replaced = False
            for pat, _ in patterns:
                new_text, n = re.subn(pat, lambda m, nh=new_href: m.group(1) + nh + m.group(3), text, count=1)
                if n > 0:
                    text = new_text
                    applied += 1
                    replaced = True
                    break
            if not replaced:
                missed += 1
                # Only print for first few missed
                if missed <= 3:
                    print(f'    - no match for anchor "{anchor[:40]}..." in {rel_file}')

        if text != original:
            p.write_text(text, encoding='utf-8')
            files_changed += 1

    return files_changed, applied, missed

def commit_and_push(repo_path, repo_name, applied, files_changed):
    run(['git','config','user.email','tachyon@alexanarch.org'], repo_path, quiet=True)
    run(['git','config','user.name','TACHYON'], repo_path, quiet=True)
    r = run(['git','add','-A'], repo_path)
    if r.returncode != 0: return None, False

    msg = (f'link-inventory fixes: {applied} sentinel-0 hrefs corrected to specific record targets '
           f'across {files_changed} files.\n\n'
           f'For each fix, the anchor text uniquely matches one alexanarch record title as a\n'
           f'substring (or the record title contains the anchor text as a substring, unique across\n'
           f'the registry). Old href was https://www.alexanarch.org/s/records/0/ (the sentinel\n'
           f'"no target known" placeholder); new href is the matching record page.\n\n'
           f'Fixes derived from the link inventory deposit #1056 v1.0\n'
           f'(AXN:0431.ARCHIVAL.🔗🕸️🗺️🔍📋⚖️) at /data/link-inventory/link-review-actionable.csv.\n'
           f'These records have no known dead DOI to route through /go/, so href goes directly\n'
           f'to the stable /s/records/<N>/ path.')

    r = run(['git','commit','-m',msg], repo_path)
    if r.returncode != 0:
        if 'nothing to commit' in r.stdout or 'nothing to commit' in r.stderr:
            return None, True
        return None, False
    run(['git','fetch','origin','main'], repo_path, quiet=True)
    run(['git','pull','--rebase','origin','main'], repo_path, quiet=True)
    sha = run(['git','rev-parse','HEAD'], repo_path).stdout.strip()[:12]
    push_url = f'https://x-access-token:{TOK}@github.com/leesharks000/{repo_name}.git'
    push_r = run(['git','push', push_url,'HEAD:main'], repo_path)
    return sha, push_r.returncode == 0

results = []
for repo, repo_fixes in sorted(by_repo.items()):
    files_changed, applied, missed = apply_repo(repo, repo_fixes)
    print(f'  {repo:35} planned={len(repo_fixes):>3}  applied={applied:>3}  missed={missed:>3}  files={files_changed}')
    if applied > 0:
        repo_path = ALEX_LIVE if repo == 'alexanarch' else REPOS_DIR / repo
        sha, ok = commit_and_push(repo_path, repo, applied, files_changed)
        status = 'PUSHED' if ok else 'FAIL'
        print(f'    → {status} sha={sha}')
        results.append({'repo': repo, 'applied': applied, 'files': files_changed, 'sha': sha, 'pushed': ok})

print(f'\n=== SUMMARY ===')
print(f'  total repos touched: {len(results)}')
print(f'  total fixes applied: {sum(r["applied"] for r in results)}')
print(f'\n=== SHAs ===')
for r in results:
    print(f'  {r["sha"]}   {r["repo"]:35}  ({r["applied"]} fixes)')

with open('/tmp/linkscan/sentinel0_apply_results.json','w') as f:
    json.dump(results, f, indent=1)
