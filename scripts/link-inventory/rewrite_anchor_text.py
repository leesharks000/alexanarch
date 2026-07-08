#!/usr/bin/env python3
"""rewrite_anchor_text.py — semantic link rewriter.

For every anchor (`<a href="X">TEXT</a>` in HTML or `[TEXT](X)` in markdown) where
TEXT contains a DOI reference (`10.5281/zenodo.N`) or an AXN reference (`AXN:HEX...`),
rewrite the URL X to the alexanarch resolver endpoint:

  DOI in anchor text → href=https://www.alexanarch.org/go/?doi=10.5281/zenodo.N
  AXN in anchor text → href=https://www.alexanarch.org/axn/<hex>/

Rewrites happen regardless of what the current href is. Rationale:
  - The resolver map is the source of truth
  - /go/ reads the map at request time — any future map update propagates instantly
  - Even links that currently point at correct alexanarch records benefit from
    auto-update behavior for zero cost (one client-side redirect hop)

This complements rewrite_links.py which handles bare URL rewrites. Together they
cover both:
  URL-based:      href="https://doi.org/10.5281/zenodo.N"    → /go/?doi=N
  Text-based:     <a href="/s/records/0/">DOI 10.5281/zenodo.N</a>  → /go/?doi=N

Usage:
  python3 rewrite_anchor_text.py --check /path/to/repo
  python3 rewrite_anchor_text.py --apply /path/to/repo
"""
import re, argparse, sys
from pathlib import Path
from collections import Counter, defaultdict

GO_BASE = 'https://www.alexanarch.org/go/'
AXN_BASE = 'https://www.alexanarch.org/axn/'

# Match <a>-tags with DOI or AXN in visible text
# We capture: (open-tag, href, close-of-open, inner, closing-tag)
# Anchor may span multiple lines
A_TAG_RE = re.compile(
    r'(<a\s+[^>]*?href\s*=\s*)(["\'])([^"\']*)(\2)([^>]*>)([^<]*?)(</a>)',
    re.IGNORECASE | re.DOTALL
)
# Markdown link with anchor text
MD_LINK_RE = re.compile(r'\[([^\]\n]{1,300})\]\(([^)\s]{1,600})(\s+"[^"]*")?\)')

# Anchor text patterns to extract DOI or AXN
DOI_IN_TEXT_RE = re.compile(r'10\.5281/zenodo\.(\d+)')
# AXN full form (hex[.family[.glyphs]])
AXN_IN_TEXT_RE = re.compile(r'AXN:([0-9A-Fa-f]{4})(?:\.[A-Z]+)?(?:\.\S+?)?(?=[\s\)\]\}\|,;:!?"\'<]|$)', re.UNICODE)

def rewrite_href_for_text(text, current_href):
    """Return (new_href, kind) if we should rewrite based on anchor text; else (current, None)."""
    m = DOI_IN_TEXT_RE.search(text or '')
    if m:
        new = f'{GO_BASE}?doi=10.5281/zenodo.{m.group(1)}'
        # Skip if already exactly this
        if current_href == new:
            return current_href, None
        return new, 'doi_from_text'
    m = AXN_IN_TEXT_RE.search(text or '')
    if m:
        hex_id = m.group(1).lower()
        new = f'{AXN_BASE}{hex_id}/'
        if current_href.rstrip('/') == new.rstrip('/'):
            return current_href, None
        return new, 'axn_from_text'
    return current_href, None

def rewrite_buffer(text):
    counts = Counter()
    changes = []

    def line_of(pos):
        return text.count('\n', 0, pos) + 1

    def a_sub(m):
        pre, quote, href, _, close_open, inner, close = (
            m.group(1), m.group(2), m.group(3), m.group(4),
            m.group(5), m.group(6), m.group(7)
        )
        new_href, kind = rewrite_href_for_text(inner, href)
        if kind:
            counts[kind] += 1
            changes.append((href, new_href, kind, inner.strip()[:80], line_of(m.start())))
            return f'{pre}{quote}{new_href}{quote}{close_open}{inner}{close}'
        return m.group(0)

    def md_sub(m):
        inner, url, title = m.group(1), m.group(2), m.group(3) or ''
        new_url, kind = rewrite_href_for_text(inner, url)
        if kind:
            counts[kind] += 1
            changes.append((url, new_url, kind, inner.strip()[:80], line_of(m.start())))
            return f'[{inner}]({new_url}{title})'
        return m.group(0)

    text = A_TAG_RE.sub(a_sub, text)
    text = MD_LINK_RE.sub(md_sub, text)
    return text, counts, changes

TEXT_EXTS = {'.md', '.markdown', '.html', '.htm', '.txt', '.py', '.js', '.jsx',
             '.ts', '.tsx', '.mjs', '.rst', '.svg', '.vue', '.rb', '.astro', '.css'}
MAX_FILE_BYTES = 15 * 1024 * 1024
SKIP_DIR_NAMES = {'.git', 'node_modules', 'dist', 'build', '__pycache__',
                  '.venv', '.next', '.cache', 'vendor'}

def is_skip_path(repo_name, rel):
    # For alexanarch, skip data-storage dirs but ALLOW s/ (record pages)
    if repo_name == 'alexanarch':
        for p in ('data/', 'api/', 'audit/', 'datasets/', 'chunks/'):
            if rel.startswith(p): return True
        if 'RECORD-SHA256-MANIFEST' in rel or 'SHA256SUMS' in rel: return True
    if 'backup' in rel.lower() or 'manifest' in rel.lower():
        return True
    return False

def iter_files(repo_path: Path, repo_name: str):
    for path in repo_path.rglob('*'):
        if not path.is_file(): continue
        if any(p in SKIP_DIR_NAMES for p in path.parts): continue
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
    changes_by_file = defaultdict(list)
    files_touched = files_changed = 0

    for path, rel in iter_files(repo_path, repo_name):
        files_touched += 1
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
        new, counts, changes = rewrite_buffer(text)
        if counts:
            files_changed += 1
            total_counts.update(counts)
            changes_by_file[rel] = changes
            if apply and new != text:
                path.write_text(new, encoding='utf-8')

    return {'repo': repo_name, 'files_touched': files_touched,
            'files_changed': files_changed,
            'counts': dict(total_counts),
            'changes': dict(changes_by_file)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--verbose', '-v', action='store_true')
    p.add_argument('paths', nargs='+')
    args = p.parse_args()
    if not args.check and not args.apply: args.check = True

    grand = Counter()
    grand_files = 0

    for path_str in args.paths:
        repo = Path(path_str)
        if not repo.is_dir():
            print(f'SKIP {path_str}', file=sys.stderr); continue
        r = process_repo(repo, apply=args.apply)
        grand.update(r['counts'])
        grand_files += r['files_changed']
        total = sum(r['counts'].values())
        if total == 0:
            print(f'  {r["repo"]:35}  no changes')
            continue
        print(f'\n  {r["repo"]:35}  files_changed={r["files_changed"]:>4}  total_rewrites={total:>5}')
        for kind, n in sorted(r['counts'].items(), key=lambda x: -x[1]):
            print(f'    {kind:22}  {n:>5}')
        if args.verbose:
            for rel, changes in list(r['changes'].items())[:3]:
                print(f'    {rel}:')
                for old, new, kind, text, ln in changes[:2]:
                    print(f'      L{ln} text="{text[:50]}"')
                    print(f'         was: {old[:80]}')
                    print(f'         now: {new[:80]}')

    print(f'\n=== TOTAL ===')
    for kind, n in sorted(grand.items(), key=lambda x: -x[1]):
        print(f'  {kind:22}  {n:>6,}')
    print(f'\n  {sum(grand.values()):,} rewrites across {grand_files:,} files')
    if not args.apply:
        print('\n  DRY RUN — re-run with --apply to write.')

if __name__ == '__main__':
    main()
