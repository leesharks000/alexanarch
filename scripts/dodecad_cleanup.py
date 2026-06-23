#!/usr/bin/env python3
"""
Dodecad site cleanup engine.

For each leesharks000/<repo>, apply uniform post-Zenodo language cleanup:
  - Stale deposit counts (866/532/455/870, present tense) -> 879
  - "CERN's Zenodo" / "on Zenodo" present-tense -> sovereign-successor framing
  - doi.org/10.5281/zenodo.* links -> repointed via override table + resolution-index
  - "Zenodo" link text when URL points to alexanarch -> "Alexanarch"
  - Optional contact line in footer

Preserves historical/event narrative ("On June 19, 2026, Zenodo terminated...").
Logs every change for human audit. Pushes via Trees API as single commit per repo.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

PAT = os.environ.get('GITHUB_TOKEN')
if not PAT:
    print("ERROR: set GITHUB_TOKEN environment variable to a PAT with repo scope.", file=sys.stderr)
    sys.exit(2)
OWNER = 'leesharks000'

# ============================================================
# OVERRIDE TABLE — hand-verified DOI -> alexanarch record mappings
# These take priority over the doi-resolution-index (which has bad entries
# for the most-cited works).
# ============================================================
DOI_OVERRIDES = {
    # From leesharks.com audit
    '10.5281/zenodo.19474724': ('/s/records/637/', 'The Encyclotron'),
    '10.5281/zenodo.19763346': ('/s/records/695/', 'Writable Retrieval Basins'),
    '10.5281/zenodo.19202711': ('/s/records/579/', 'The Three Compressions'),
    '10.5281/zenodo.19739494': ('/s/records/683/', 'The Secret Book of Walt'),
    '10.5281/zenodo.19709024': ('/s/records/71/',  'The Gospel of Antioch'),
    '10.5281/zenodo.19390843': ('/s/records/38/',  'Operative Semiotics: A Grundrisse'),
    '10.5281/zenodo.19734726': ('/s/records/660/', 'SPXI'),
    '10.5281/zenodo.19864158': ('/s/records/705/', 'SPXI-Sitemap Protocol'),
    '10.5281/zenodo.19578086': ('/s/records/103/', 'Metadata Packet for AI Indexing'),
    '10.5281/zenodo.19412081': ('/s/records/76/',  'Holographic Kernel'),
    '10.5281/zenodo.18811939': ('/s/records/526/', 'Provenance Gravity Markers'),
    '10.5281/zenodo.19923120': ('/s/records/88/',  'Constitution of the Semantic Economy'),
    '10.5281/zenodo.19923143': ('/s/records/87/',  'Companion Guide (PH-03)'),
    '10.5281/zenodo.18946111': ('/s/records/547/', 'UKTP'),
    '10.5281/zenodo.19013315': ('/s/records/549/', 'Space Ark v4.2.7'),
    # From revelationfirst audit
    '10.5281/zenodo.20722689': ('/s/records/832/', 'Revelation First Work Plan'),
    # From watergiraffe audit
    '10.5281/zenodo.20634184': ('/s/records/177/', "Water Giraffes Aren't Real"),
    '10.5281/zenodo.20632525': ('/s/records/803/', 'The Water Giraffe Cycle'),
    '10.5281/zenodo.18319455': ('/s/records/352/', 'CTI Wound Vault'),
    '10.5281/zenodo.18319653': ('/s/records/353/', 'Water Giraffe Room Anchor'),
    '10.5281/zenodo.18323376': ('/s/records/365/', 'Water Giraffe Sighting Protocol'),
    '10.5281/zenodo.18323465': ('/s/records/366/', 'Water Giraffe as Semantic Being'),
    '10.5281/zenodo.19442262': ('/s/records/633/', 'Gravity Well: Suffusion Map'),
    # From secret-book-of-walt audit
    '10.5281/zenodo.19779493': ('/s/records/78/',  'TANG of Secret Book of Walt'),
    '10.5281/zenodo.19703009': ('/s/records/683/', 'Secret Book of Walt (alt DOI)'),
}

# Load the doi-resolution-index for non-override lookups
RESOLUTION_INDEX = None
def load_resolution_index():
    global RESOLUTION_INDEX
    if RESOLUTION_INDEX is None:
        try:
            idx = json.load(open('/home/claude/alexanarch/data/doi-resolution-index.json'))
            RESOLUTION_INDEX = {m['dead_doi']: m for m in idx['mappings']}
            print(f"  Loaded {len(RESOLUTION_INDEX)} entries from doi-resolution-index", file=sys.stderr)
        except Exception as e:
            RESOLUTION_INDEX = {}
            print(f"  WARNING: could not load resolution-index: {e}", file=sys.stderr)
    return RESOLUTION_INDEX

def resolve_doi(doi):
    """Return (alexanarch_url, title, confidence) for a dead Zenodo DOI.
    Falls back to /resolve/?doi=... when no specific alexanarch record is known —
    this routes any link through alexanarch's resolution surface rather than
    leaving the link pointing at a dead doi.org URL."""
    if doi in DOI_OVERRIDES:
        rec, title = DOI_OVERRIDES[doi]
        return (f'https://alexanarch.org{rec}', title, 'override')
    idx = load_resolution_index()
    m = idx.get(doi)
    if m and m.get('alexanarch_record') and m['alexanarch_record'] != '/s/records/0/':
        return (f'https://alexanarch.org{m["alexanarch_record"]}', m.get('title', '')[:60], 'index')
    # Fallback: route through /resolve/?doi=... so the link still lands on alexanarch.
    return (f'https://alexanarch.org/resolve/?doi={doi}', None, 'resolve-fallback')

# ============================================================
# PER-REPO RECIPES — wrong-target /s/records/N/ link fixes
# Sourced from earlier audits (see audit/<site>-homepage.json).
# Format: repo_name -> list of (old_substring, new_substring) tuples.
# Applied BEFORE the broad cleanup rules.
# ============================================================
PER_REPO_RECIPES = {
    'revelationfirst-com': [
        # Workstream 1 (Dating Question / Work Plan) — wrong target
        ('"https://alexanarch.org/s/records/842/"', '"https://alexanarch.org/s/records/832/"'),
        # Workstream 2 (Heteronymic Reading) — wrong target
        ('"https://alexanarch.org/s/records/835/"', '"https://alexanarch.org/s/records/837/"'),  # Josephus≠Myth uses 835 too
        # Workstream 3 (Inscription Chain)
        ('"https://alexanarch.org/s/records/826/"', '"https://alexanarch.org/s/records/828/"'),
        # Workstream 4 (Slavonic Josephus) — off by one
        ('"https://alexanarch.org/s/records/625/"', '"https://alexanarch.org/s/records/626/"'),
        # Number of Superscription
        ('"https://alexanarch.org/s/records/636/"', '"https://alexanarch.org/s/records/642/"'),
        # /s/records/847/ used for both Josephus≠Piso and Baseline Captures — point to Josephus≠Piso (203)
        ('"https://alexanarch.org/s/records/847/"', '"https://alexanarch.org/s/records/203/"'),
        # MMRS Charter — point to system manifest as best available
        ('"https://alexanarch.org/s/records/834/"', '"https://alexanarch.org/s/records/848/"'),
    ],
    'crimson-hexagonal-interface': [
        # Space Ark — current target /s/records/561/ ("THE SPLICE") is wrong
        ('"https://alexanarch.org/s/records/561/"', '"https://alexanarch.org/s/records/549/"'),
        # Dead Zenodo community link
        ('href="https://zenodo.org/communities/leesharks000"',
         'href="https://alexanarch.org/s/browse/"'),
    ],
    'watergiraffe-org': [
        # WG-04 wrong target (was Assembly Room Anchor, should be Water Giraffe Room Anchor)
        ('"https://alexanarch.org/s/records/349/"', '"https://alexanarch.org/s/records/353/"'),
    ],
    'secret-book-of-walt': [
        # Gospel of Antioch — wrong target was /s/records/689/ (EA-GEO-01)
        ('"https://alexanarch.org/s/records/689/"', '"https://alexanarch.org/s/records/71/"'),
        # TANG of Secret Book of Walt — wrong target was /s/records/696/
        ('"https://alexanarch.org/s/records/696/"', '"https://alexanarch.org/s/records/78/"'),
    ],
}

# Heuristic: skip lines that look like historical-event narrative.
HISTORICAL_MARKERS = re.compile(
    r'(June\s+19,?\s+2026|terminat\w+|6/19/2026|2026-06-19|book[\s-]+burning|'
    r'erasure|removed.{0,40}from.{0,40}zenodo|loud exclusion|'
    r'zenodotus|deleted.{0,40}from.{0,40}zenodo|former zenodo|previously)',
    re.IGNORECASE
)

# Stale deposit-count patterns
COUNT_PATTERNS = [
    # Match the count in clear hosting/scale contexts only
    (re.compile(r'\b(455\+?|532\+?|866|870)\s*(DOI-anchored\s+)?deposits?\b', re.IGNORECASE),
     lambda m: '879 deposits'),
    (re.compile(r'\b(455\+?|532\+?|866|870)\s+(\w+\s+){0,2}AXN', re.IGNORECASE),
     lambda m: re.sub(r'^\d+\+?', '879', m.group(0))),
]

# "CERN's Zenodo" prose — the big one
PROSE_REWRITES = [
    # "<count> DOI-anchored deposits on CERN's Zenodo"
    (re.compile(
        r"(\b\d+\+?)\s*DOI-anchored\s+deposits?\s+on\s+CERN['\u2019]s\s+Zenodo",
        re.IGNORECASE),
     "879 deposits in Alexanarch, the AXN-minting sovereign successor to the Crimson Hexagonal Archive on Zenodo"),
    # "<count> deposits on CERN's Zenodo"
    (re.compile(
        r"(\b\d+\+?)\s+deposits?\s+on\s+CERN['\u2019]s\s+Zenodo",
        re.IGNORECASE),
     "879 deposits in Alexanarch, the AXN-minting sovereign successor to the Crimson Hexagonal Archive on Zenodo"),
    # "hosted on CERN's Zenodo"
    (re.compile(r"hosted\s+on\s+CERN['\u2019]s\s+Zenodo", re.IGNORECASE),
     "hosted in Alexanarch, the AXN-minting sovereign successor to the Crimson Hexagonal Archive on Zenodo"),
    # "hosted on Zenodo" (more general)
    (re.compile(r"hosted\s+on\s+Zenodo(?!\w)", re.IGNORECASE),
     "hosted in Alexanarch (the sovereign successor to the Crimson Hexagonal Archive on Zenodo)"),
    # "deposits on Zenodo" (present tense, after count)
    (re.compile(r"(\b\d+\+?)\s+(DOI-anchored\s+)?deposits?\s+on\s+Zenodo(?!\w)", re.IGNORECASE),
     "879 deposits in Alexanarch (the AXN-minting sovereign successor to the Crimson Hexagonal Archive on Zenodo)"),
]

# Link text fixes when URL points to alexanarch but text is still Zenodo-era
LINK_TEXT_FIXES = [
    # <a href="https://alexanarch.org/s/browse/">Zenodo community</a>
    (re.compile(r'(<a[^>]+href="https://alexanarch\.org/s/browse/?"[^>]*>)Zenodo community(</a>)', re.IGNORECASE),
     r'\1Alexanarch (sovereign archive)\2'),
    # <a href="https://alexanarch.org/s/browse/">Zenodo</a>
    (re.compile(r'(<a[^>]+href="https://alexanarch\.org/s/browse/?"[^>]*>)Zenodo(</a>)', re.IGNORECASE),
     r'\1Alexanarch\2'),
]

# DOI link repointer — replaces inline href="https://doi.org/10.5281/zenodo.XXXX" with the alexanarch record
DOI_LINK_PATTERN = re.compile(
    r'<a([^>]*?)href="https://doi\.org/(10\.5281/zenodo\.\d+)"([^>]*)>([^<]+)</a>',
    re.IGNORECASE
)

def repoint_doi_links(text):
    """For each <a href='doi.org/10.5281/zenodo.X'>TEXT</a>, find the right alexanarch target and rewrite.
    Returns (new_text, count_changed, list_of_changes)."""
    changes = []
    def replace(m):
        attrs_before, doi, attrs_after, link_text = m.group(1), m.group(2), m.group(3), m.group(4)
        new_url, title, confidence = resolve_doi(doi)
        if not new_url:
            return m.group(0)  # leave as-is
        # Decide what link text to show:
        if confidence == 'resolve-fallback':
            # No specific record identified; route through /resolve/ but keep link text as-is.
            # No need to add an AXN # since we don't have one. Add a small grey hint.
            if doi in link_text or 'zenodo.' in link_text.lower():
                new_link_text = f'{doi} <span style="color:#999;font-size:.88em">(via Alexanarch)</span>'
                new_html = f'<a{attrs_before}href="{new_url}"{attrs_after}>{new_link_text}</a>'
            else:
                new_html = f'<a{attrs_before}href="{new_url}"{attrs_after}>{link_text}</a>'
        elif doi in link_text or 'zenodo.' in link_text.lower():
            # link text was the DOI string — show AXN # with legacy DOI in grey
            axn_num = new_url.rsplit('/', 2)[-2]
            new_link_text = f'AXN #{axn_num}'
            new_html = (f'<a{attrs_before}href="{new_url}"{attrs_after}>{new_link_text}</a> '
                       f'<span style="color:#999;font-size:.88em">(legacy: {doi})</span>')
        else:
            # link text is descriptive (work title) — just swap the URL
            new_html = f'<a{attrs_before}href="{new_url}"{attrs_after}>{link_text}</a>'
        changes.append({'doi': doi, 'old_text': link_text[:50], 'new_url': new_url, 'confidence': confidence})
        return new_html
    new_text, n = DOI_LINK_PATTERN.subn(replace, text)
    return new_text, n, changes

def apply_cleanup(filename, text, repo=None):
    """Apply all cleanup rules to a single file's text.
    Returns (new_text, change_log)."""
    log = {'file': filename, 'recipe_fixes': 0, 'prose_rewrites': 0, 'count_updates': 0,
           'link_text_fixes': 0, 'doi_links_repointed': 0, 'doi_changes': [], 'skipped_lines': 0}
    original = text  # remember the ORIGINAL text for change detection
    
    # FIRST: per-repo recipe fixes (wrong-target /s/records/N/ links)
    if repo and repo in PER_REPO_RECIPES:
        for old, new in PER_REPO_RECIPES[repo]:
            count = text.count(old)
            if count > 0:
                text = text.replace(old, new)
                log['recipe_fixes'] += count
    
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        # Skip lines that are historical narrative
        if HISTORICAL_MARKERS.search(line):
            new_lines.append(line)
            log['skipped_lines'] += 1
            continue
        
        original = line
        
        # Prose rewrites
        for pat, replacement in PROSE_REWRITES:
            if isinstance(replacement, str):
                line, n = pat.subn(replacement, line)
            else:
                line, n = pat.subn(replacement, line)
            log['prose_rewrites'] += n
        
        # Count updates (apply AFTER prose rewrites so we don't double-process)
        for pat, repl in COUNT_PATTERNS:
            line, n = pat.subn(repl, line)
            log['count_updates'] += n
        
        # Link text fixes
        for pat, replacement in LINK_TEXT_FIXES:
            line, n = pat.subn(replacement, line)
            log['link_text_fixes'] += n
        
        new_lines.append(line)
    
    new_text = '\n'.join(new_lines)
    
    # DOI link repoints — needs full-text context because some span lines
    new_text, n_doi, doi_changes = repoint_doi_links(new_text)
    log['doi_links_repointed'] = n_doi
    log['doi_changes'] = doi_changes
    
    log['changed'] = (new_text != original)
    return new_text, log

# ============================================================
# GITHUB API HELPERS
# ============================================================

def gh(method, path, body=None, retries=3):
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                f'https://api.github.com{path}',
                method=method,
                headers={'Authorization': f'Bearer {PAT}', 'Accept': 'application/vnd.github+json'}
            )
            if body is not None:
                req.data = json.dumps(body).encode()
                req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (403, 502, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    raise last_err

def list_html_files(repo):
    """Get all HTML files in the repo root + one level deep."""
    try:
        tree = gh('GET', f'/repos/{OWNER}/{repo}/git/trees/main?recursive=1')
    except urllib.error.HTTPError as e:
        if e.code == 409:  # empty repo
            return []
        raise
    files = []
    for item in tree.get('tree', []):
        if item['type'] != 'blob': continue
        path = item['path']
        if not path.endswith('.html'): continue
        # Skip deeply nested files — only get root + 1-level subdirs (keep audit scope tight)
        depth = path.count('/')
        if depth > 1: continue
        files.append(path)
    return files

def fetch_file(repo, path):
    """Get raw file content."""
    url = f'https://raw.githubusercontent.com/{OWNER}/{repo}/main/{path}'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {PAT}'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', errors='replace')

def push_files(repo, file_contents, commit_message):
    """Push multiple files via Trees API as one commit."""
    ref = gh('GET', f'/repos/{OWNER}/{repo}/git/ref/heads/main')
    parent_sha = ref['object']['sha']
    parent_commit = gh('GET', f'/repos/{OWNER}/{repo}/git/commits/{parent_sha}')
    base_tree_sha = parent_commit['tree']['sha']
    
    tree_entries = []
    for path, content in file_contents.items():
        blob = gh('POST', f'/repos/{OWNER}/{repo}/git/blobs', {
            'content': content, 'encoding': 'utf-8'
        })
        tree_entries.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
    
    new_tree = gh('POST', f'/repos/{OWNER}/{repo}/git/trees', {
        'base_tree': base_tree_sha, 'tree': tree_entries
    })
    new_commit = gh('POST', f'/repos/{OWNER}/{repo}/git/commits', {
        'message': commit_message, 'tree': new_tree['sha'], 'parents': [parent_sha]
    })
    gh('PATCH', f'/repos/{OWNER}/{repo}/git/refs/heads/main', {'sha': new_commit['sha']})
    return new_commit['sha']

# ============================================================
# PER-REPO CLEANUP
# ============================================================

def cleanup_repo(repo, dry_run=False):
    """Apply cleanup to all HTML files in a repo. Returns summary dict."""
    summary = {'repo': repo, 'files_examined': 0, 'files_changed': 0, 
               'total_prose_rewrites': 0, 'total_count_updates': 0,
               'total_link_text_fixes': 0, 'total_doi_repoints': 0,
               'file_logs': [], 'commit_sha': None, 'error': None}
    
    try:
        html_files = list_html_files(repo)
        summary['files_examined'] = len(html_files)
        if not html_files:
            return summary
        
        changed_files = {}
        for path in html_files:
            try:
                original = fetch_file(repo, path)
            except Exception as e:
                summary['file_logs'].append({'file': path, 'error': str(e)})
                continue
            
            new_text, log = apply_cleanup(path, original, repo=repo)
            summary['file_logs'].append(log)
            
            if log['changed']:
                changed_files[path] = new_text
                summary['files_changed'] += 1
                summary['total_recipe_fixes'] = summary.get('total_recipe_fixes', 0) + log.get('recipe_fixes', 0)
                summary['total_prose_rewrites'] += log['prose_rewrites']
                summary['total_count_updates'] += log['count_updates']
                summary['total_link_text_fixes'] += log['link_text_fixes']
                summary['total_doi_repoints'] += log['doi_links_repointed']
        
        if changed_files and not dry_run:
            msg = build_commit_message(repo, summary)
            sha = push_files(repo, changed_files, msg)
            summary['commit_sha'] = sha
    except Exception as e:
        summary['error'] = f'{type(e).__name__}: {e}'
    
    return summary

def build_commit_message(repo, summary):
    """Tailored commit message for each repo's cleanup."""
    msg = f"Post-Zenodo language cleanup: prose, DOI link repoints, counts\n\n"
    msg += f"Uniform pass aligning {repo} with the current state: alexanarch.org "
    msg += f"is the AXN-minting sovereign successor to the Crimson Hexagonal Archive "
    msg += f"on Zenodo (terminated 2026-06-19; 879 deposits now live in Alexanarch).\n\n"
    msg += "CHANGES IN THIS COMMIT\n" + "=" * 22 + "\n\n"
    msg += f"  Files examined:        {summary['files_examined']}\n"
    msg += f"  Files modified:        {summary['files_changed']}\n"
    if summary.get('total_recipe_fixes', 0):
        msg += f"  Wrong-target /s/records/N/ fixes: {summary['total_recipe_fixes']}  (per audit recipe)\n"
    msg += f"  Prose rewrites:        {summary['total_prose_rewrites']}  (\"CERN's Zenodo\" / \"hosted on Zenodo\" -> sovereign-successor framing)\n"
    msg += f"  Stale count updates:   {summary['total_count_updates']}  (866 / 532 / 455 / 870 -> 879)\n"
    msg += f"  Link text fixes:       {summary['total_link_text_fixes']}  (\"Zenodo\" link text when URL points to alexanarch -> \"Alexanarch\")\n"
    msg += f"  DOI links repointed:   {summary['total_doi_repoints']}  (doi.org/10.5281/zenodo.* -> alexanarch.org/s/records/N/)\n\n"
    
    all_doi_changes = []
    for log in summary['file_logs']:
        if log.get('doi_changes'):
            all_doi_changes.extend(log['doi_changes'])
    if all_doi_changes:
        msg += "DOI REPOINTS BY DOI\n" + "=" * 19 + "\n\n"
        seen = set()
        for ch in all_doi_changes:
            key = ch['doi']
            if key in seen: continue
            seen.add(key)
            msg += f"  {ch['doi']:28s} -> {ch['new_url']}\n"
        msg += "\n"
    
    msg += "Lines containing historical-event narrative (\"On June 19, 2026, Zenodo "
    msg += "terminated...\", \"Zenodotus' Book-Burning\", etc.) were detected and "
    msg += "preserved — those references are factually correct and historically "
    msg += "load-bearing.\n\n"
    msg += "Scope: HTML files at repo root + one level deep. Deeper subpages can be "
    msg += "audited in a follow-up pass.\n\n"
    msg += "Related: leesharks000/leesharks.com@c5f001f (homepage + about), "
    msg += "leesharks000/alexanarch@3097abf (contact line)."
    return msg

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    repos = sys.argv[1:]
    if not repos:
        print("Usage: dodecad_cleanup.py REPO1 [REPO2 ...]", file=sys.stderr)
        sys.exit(1)
    
    all_summaries = []
    for repo in repos:
        print(f"\n=== {repo} ===", flush=True)
        s = cleanup_repo(repo)
        all_summaries.append(s)
        if s.get('error'):
            print(f"  ERROR: {s['error']}", flush=True)
            continue
        print(f"  examined {s['files_examined']} files; "
              f"{s['files_changed']} changed; "
              f"recipe:{s.get('total_recipe_fixes', 0)} "
              f"prose:{s['total_prose_rewrites']} count:{s['total_count_updates']} "
              f"linktext:{s['total_link_text_fixes']} doi:{s['total_doi_repoints']}",
              flush=True)
        if s['commit_sha']:
            print(f"  pushed: {s['commit_sha'][:10]}", flush=True)
        else:
            print(f"  no changes needed", flush=True)
    
    # Final summary
    print(f"\n{'=' * 60}")
    print(f"DONE — {len(all_summaries)} repos processed")
    total_changed = sum(s['files_changed'] for s in all_summaries)
    total_prose = sum(s['total_prose_rewrites'] for s in all_summaries)
    total_count = sum(s['total_count_updates'] for s in all_summaries)
    total_lt = sum(s['total_link_text_fixes'] for s in all_summaries)
    total_doi = sum(s['total_doi_repoints'] for s in all_summaries)
    print(f"  files changed:       {total_changed}")
    print(f"  prose rewrites:      {total_prose}")
    print(f"  count updates:       {total_count}")
    print(f"  link text fixes:     {total_lt}")
    print(f"  DOI links repointed: {total_doi}")
    
    # Save the full per-file logs to disk for audit
    log_path = Path('/home/claude/alexanarch/audit/dodecad-cleanup-log.json')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(all_summaries, indent=2, ensure_ascii=False))
    print(f"  audit log:           {log_path}")
