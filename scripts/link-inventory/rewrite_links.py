#!/usr/bin/env python3
"""rewrite_links.py — rewrite broken/legacy links across every repo in the
leesharks000 network to use the alexanarch resolver's /go/ endpoint.

Once links are rewritten to `www.alexanarch.org/go/?doi=X`, any future resolver
map update propagates instantly to those clicks — no re-rewriting needed.

Rewrite rules (only inside HTML href attributes and markdown link forms):

  A. DOI URL rewrites (goal: automatic-update via /go/)
     https://doi.org/10.5281/zenodo.N        → https://www.alexanarch.org/go/?doi=10.5281/zenodo.N
     http://doi.org/10.5281/zenodo.N         → same
     https://dx.doi.org/10.5281/zenodo.N     → same
     https://zenodo.org/record[s]/N          → same
     https://www.zenodo.org/record[s]/N      → same

  B. Alexanarch apex → www normalization
     https://alexanarch.org/*                → https://www.alexanarch.org/*

  C. Alexanarch old-URL-form correction
     alexanarch.org/records/?id=N            → alexanarch.org/s/records/N/

Never touched:
  - Bare DOI text (`10.5281/zenodo.N`) outside any link — those are prose citations
  - Alexanarch's own data/api/audit/datasets directories (data storage)
  - Files named RECORD-SHA256-MANIFEST.txt etc. (hash manifests)
  - JSON files that are the resolver's own data (`doi-resolution-index.json`, `doi-axn-map.json`)
  - .git, node_modules, dist, build, __pycache__, .venv

Usage:
  python3 rewrite_links.py --check /path/to/repo   # dry-run, show planned changes
  python3 rewrite_links.py --apply /path/to/repo   # actually write
"""
import re, sys, argparse
from pathlib import Path
from collections import Counter, defaultdict

# --- URL rewrite patterns ---
# We rewrite URLs ONLY inside HTML href="..." / href='...' and markdown [title](url)
# The value/URL part is what gets rewritten.

DOI_URL_RE = re.compile(
    r'https?://(?:dx\.)?doi\.org/(10\.5281/zenodo\.\d+)',
    re.IGNORECASE
)
ZENODO_URL_RE = re.compile(
    r'https?://(?:www\.)?zenodo\.org/records?/(\d+)(?:[/?#][^\s\'"\)\]]*)?',
    re.IGNORECASE
)
ALEX_APEX_RE = re.compile(
    r'https?://alexanarch\.org(?![./\w-])',    # ends after 'org' (not followed by more of a subdomain)
    re.IGNORECASE
)
# match apex form followed by path/end
ALEX_APEX_WITH_PATH_RE = re.compile(
    r'https?://alexanarch\.org(/[^\s\'"\)\]]*)?',
    re.IGNORECASE
)
# old query-string form on alexanarch
ALEX_OLD_QS_RE = re.compile(
    r'(https?://(?:www\.)?alexanarch\.org)/records/\?id=(\d+)',
    re.IGNORECASE
)

def rewrite_url(url):
    """Return (new_url, kind) or (url, None) if no change."""
    # DOI → /go/
    m = DOI_URL_RE.match(url)
    if m:
        return f'https://www.alexanarch.org/go/?doi={m.group(1)}', 'doi_url'
    m = ZENODO_URL_RE.match(url)
    if m:
        return f'https://www.alexanarch.org/go/?doi=10.5281/zenodo.{m.group(1)}', 'zenodo_url'
    # Old records/?id=N form
    m = ALEX_OLD_QS_RE.match(url)
    if m:
        return f'{m.group(1)}/s/records/{m.group(2)}/', 'alex_old_qs'
    # Apex → www (must come after old_qs since that also matches apex)
    m = re.match(r'https?://alexanarch\.org(/[^\s\'"\)\]]*)?', url, re.IGNORECASE)
    if m:
        path = m.group(1) or '/'
        return f'https://www.alexanarch.org{path}', 'alex_apex_to_www'
    return url, None

# --- Locate URLs to rewrite in a text buffer ---

# HTML href — captures group 1 = surrounding attribute prefix, group 2 = quote, group 3 = URL
HREF_RE = re.compile(r'(href\s*=\s*)(["\'])([^"\']+)(\2)', re.IGNORECASE)
# Markdown link [text](url) — captures group 1 = URL. Also handles [text](url "title") form.
MD_LINK_RE = re.compile(r'\[([^\]\n]*?)\]\(([^)\s]+)(\s+"[^"]*")?\)')

def rewrite_buffer(text):
    """Return (new_text, counts_by_kind, changes)."""
    counts = Counter()
    changes = []  # list of (old_url, new_url, kind, line_no)

    def line_of(pos):
        return text.count('\n', 0, pos) + 1

    def href_sub(m):
        prefix, quote, url, _ = m.group(1), m.group(2), m.group(3), m.group(4)
        new, kind = rewrite_url(url)
        if kind:
            counts[kind] += 1
            changes.append((url, new, kind, line_of(m.start())))
            return f'{prefix}{quote}{new}{quote}'
        return m.group(0)

    def md_sub(m):
        label, url, title = m.group(1), m.group(2), m.group(3) or ''
        new, kind = rewrite_url(url)
        if kind:
            counts[kind] += 1
            changes.append((url, new, kind, line_of(m.start())))
            return f'[{label}]({new}{title})'
        return m.group(0)

    text = HREF_RE.sub(href_sub, text)
    text = MD_LINK_RE.sub(md_sub, text)
    return text, counts, changes

# --- File selection ---

TEXT_EXTS = {'.md', '.markdown', '.html', '.htm', '.txt', '.py', '.js', '.jsx',
             '.ts', '.tsx', '.mjs', '.rst', '.svg', '.vue', '.rb', '.astro',
             '.jsx', '.css'}
MAX_FILE_BYTES = 15 * 1024 * 1024  # 15MB cap

SKIP_DIR_NAMES = {'.git', 'node_modules', 'dist', 'build', '__pycache__',
                  '.venv', '.next', '.cache', 'vendor'}

# Repo-specific skip paths (relative to repo root)
def is_skip_path(repo_name, rel):
    # Skip alexanarch's own data storage
    if repo_name == 'alexanarch':
        for p in ('data/', 'api/', 'audit/', 'datasets/', 'chunks/'):
            if rel.startswith(p): return True
        # Skip hash manifests
        for name in ('RECORD-SHA256-MANIFEST', 'SHA256SUMS'):
            if name in rel: return True
    # Anywhere: skip anything named for backups
    if 'backup' in rel.lower() or 'manifest' in rel.lower():
        return True
    return False

def iter_files(repo_path: Path, repo_name: str):
    for path in repo_path.rglob('*'):
        if not path.is_file(): continue
        parts = path.parts
        if any(p in SKIP_DIR_NAMES for p in parts): continue
        ext = path.suffix.lower()
        if ext not in TEXT_EXTS: continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES: continue
        except Exception:
            continue
        rel = str(path.relative_to(repo_path))
        if is_skip_path(repo_name, rel): continue
        yield path, rel

def process_repo(repo_path: Path, apply=False, verbose=False):
    repo_name = repo_path.name
    total_counts = Counter()
    all_changes = defaultdict(list)  # file → list of changes
    files_touched = 0
    files_changed = 0

    for path, rel in iter_files(repo_path, repo_name):
        files_touched += 1
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        except Exception:
            continue

        new_text, counts, changes = rewrite_buffer(text)
        if counts:
            files_changed += 1
            total_counts.update(counts)
            all_changes[rel] = changes
            if apply and new_text != text:
                path.write_text(new_text, encoding='utf-8')

    return {'repo': repo_name, 'files_touched': files_touched,
            'files_changed': files_changed,
            'counts': dict(total_counts),
            'changes': dict(all_changes)}

# --- CLI ---

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true', help='dry-run (default)')
    p.add_argument('--apply', action='store_true', help='write changes')
    p.add_argument('--verbose', '-v', action='store_true')
    p.add_argument('paths', nargs='+', help='repo root path(s)')
    args = p.parse_args()
    if not args.check and not args.apply:
        args.check = True   # default

    grand_counts = Counter()
    grand_files = 0

    for path_str in args.paths:
        repo = Path(path_str)
        if not repo.is_dir():
            print(f'SKIP {path_str} (not a directory)', file=sys.stderr)
            continue
        r = process_repo(repo, apply=args.apply, verbose=args.verbose)
        grand_counts.update(r['counts'])
        grand_files += r['files_changed']
        total = sum(r['counts'].values())
        if total == 0:
            print(f'  {r["repo"]:35}  files_scanned={r["files_touched"]:>5}  no rewrites')
            continue
        print(f'\n  {r["repo"]:35}  files_scanned={r["files_touched"]:>5}  files_changed={r["files_changed"]:>4}  total_rewrites={total:>6}')
        for kind, n in sorted(r['counts'].items(), key=lambda x: -x[1]):
            print(f'    {kind:20}  {n:>6}')
        if args.verbose:
            for rel, changes in list(r['changes'].items())[:5]:
                print(f'    {rel}:')
                for old, new, kind, ln in changes[:3]:
                    print(f'      L{ln} [{kind}]')
                    print(f'         old: {old[:100]}')
                    print(f'         new: {new[:100]}')

    print(f'\n=== TOTAL ===')
    for kind, n in sorted(grand_counts.items(), key=lambda x: -x[1]):
        print(f'  {kind:20}  {n:>6,}')
    print(f'\n  {sum(grand_counts.values()):,} rewrites across {grand_files:,} files')
    if not args.apply:
        print(f'\n  DRY RUN — no writes. Re-run with --apply to write.')

if __name__ == '__main__':
    main()
