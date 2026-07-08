#!/usr/bin/env python3
"""build_link_review_db.py — the link inventory Lee asked for at the start.

Every link across every repo, recorded with:
  - anchor_text  (what the user sees)
  - href         (where the link goes)
  - context_before / context_after / context_prose  (surrounding prose so we can
    tell what work the link is about, not just what the link text says)
  - DOI and AXN references extracted from anchor text, href, and context
  - resolver lookup for the DOI (title, target, mapping_type)
  - mismatch analysis (prose vs resolver title jaccard; best-alternative-record)
  - verdict flag for review

Output: /tmp/linkscan/links_review.db (SQLite)

Companion report generators run against this DB (build_review_md.py etc).
"""
import re, sqlite3, sys, time, json
from pathlib import Path
from collections import Counter

REPOS_DIR = Path('/tmp/linkscan/repos')
ALEX_LIVE = Path('/home/claude/alexanarch')
DB = Path('/tmp/linkscan/links_review.db')
DB.unlink(missing_ok=True)

# --- Regexes -------------------------------------------------------------

# HTML <a href="X">TEXT</a>  (multi-line OK)
A_TAG_RE = re.compile(
    r'<a\s+([^>]*?)>([^<]{0,500})</a>',
    re.IGNORECASE | re.DOTALL
)
HREF_ATTR_RE = re.compile(r'href\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)

# Markdown [text](url)
MD_LINK_RE = re.compile(r'\[([^\]\n]{0,300})\]\(([^)\s]{1,600})(\s+"[^"]*")?\)')

# Identifiers
DOI_RE = re.compile(r'10\.5281/zenodo\.(\d+)')
AXN_RE = re.compile(
    r'AXN:([0-9A-Fa-f]{4})(?:\.[A-Z]+)?(?:\.\S+?)?(?=[\s\)\]\}\|,;:!?"\'<]|$)',
    re.UNICODE
)
# Also for hrefs pointing at alexanarch records
ALEX_RECORD_RE = re.compile(r'alexanarch\.org/s?/records/(\d+)', re.IGNORECASE)
GO_DOI_RE = re.compile(r'/go/\?doi=(10\.5281/zenodo\.\d+)', re.IGNORECASE)
DOI_URL_RE = re.compile(r'https?://(?:dx\.)?doi\.org/(10\.5281/zenodo\.\d+)', re.IGNORECASE)
ZENODO_URL_RE = re.compile(r'https?://(?:www\.)?zenodo\.org/records?/(\d+)', re.IGNORECASE)

# --- File selection ------------------------------------------------------

TEXT_EXTS = {'.md', '.markdown', '.html', '.htm', '.txt', '.py', '.js', '.jsx',
             '.ts', '.tsx', '.mjs', '.rst', '.svg', '.vue', '.rb', '.astro'}
SKIP_DIRS = {'.git', 'node_modules', 'dist', 'build', '__pycache__',
             '.venv', '.next', '.cache', 'vendor'}
MAX_BYTES = 15 * 1024 * 1024

def is_skip_path(repo, rel):
    if repo == 'alexanarch':
        for p in ('data/', 'api/', 'audit/', 'datasets/', 'chunks/'):
            if rel.startswith(p): return True
        if 'MANIFEST' in rel or 'SHA256' in rel: return True
    if any(w in rel.lower() for w in ('backup', 'manifest')):
        return True
    return False

def iter_files(repo_path, repo_name):
    for path in repo_path.rglob('*'):
        if not path.is_file(): continue
        if any(p in SKIP_DIRS for p in path.parts): continue
        if path.suffix.lower() not in TEXT_EXTS: continue
        try:
            if path.stat().st_size > MAX_BYTES: continue
        except Exception:
            continue
        rel = str(path.relative_to(repo_path))
        if is_skip_path(repo_name, rel): continue
        yield path, rel

# --- Extractors ----------------------------------------------------------

def extract_href(attrs):
    m = HREF_ATTR_RE.search(attrs)
    return m.group(1).strip() if m else ''

def strip_html_tags(s):
    return re.sub(r'<[^>]+>', ' ', s or '')

def normalize_space(s):
    return re.sub(r'\s+', ' ', s or '').strip()

def first_doi(s):
    m = DOI_RE.search(s or '')
    return f'10.5281/zenodo.{m.group(1)}' if m else None

def first_axn_hex(s):
    m = AXN_RE.search(s or '')
    return m.group(1).lower() if m else None

def alex_record_from_href(href):
    m = ALEX_RECORD_RE.search(href or '')
    return int(m.group(1)) if m else None

def doi_from_href(href):
    """Extract DOI implied by an href: doi.org, zenodo.org, or /go/?doi= forms."""
    m = GO_DOI_RE.search(href or '')
    if m: return m.group(1)
    m = DOI_URL_RE.match(href or '')
    if m: return m.group(1)
    m = ZENODO_URL_RE.match(href or '')
    if m: return f'10.5281/zenodo.{m.group(1)}'
    return None

# --- Context extraction --------------------------------------------------

def context_slices(text, pos, pos_end, before=200, after=200):
    """Return (before_text, after_text) — plain-text slices around a match."""
    b = text[max(0, pos - before):pos]
    a = text[pos_end:pos_end + after]
    return normalize_space(strip_html_tags(b))[-before:], normalize_space(strip_html_tags(a))[:after]

def enclosing_prose(text, pos, pos_end, max_before=800, max_after=800):
    """Broader prose context: try to find enclosing paragraph or heading region."""
    # Find previous paragraph/heading break
    b_start = max(0, pos - max_before)
    a_end = min(len(text), pos_end + max_after)
    slab = text[b_start:a_end]
    slab = normalize_space(strip_html_tags(slab))
    return slab[:1600]

# --- Setup DB ------------------------------------------------------------

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executescript('''
CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo TEXT NOT NULL,
    file_path TEXT NOT NULL,
    line_no INTEGER NOT NULL,
    link_form TEXT NOT NULL,
    anchor_text TEXT,
    href TEXT,
    context_before TEXT,
    context_after TEXT,
    context_prose TEXT,
    doi_in_text TEXT,
    doi_in_href TEXT,
    doi_in_context TEXT,
    axn_in_text TEXT,
    axn_in_href TEXT,
    href_record_num INTEGER,
    resolver_doi TEXT,
    resolver_target TEXT,
    resolver_title TEXT,
    resolver_record INTEGER,
    resolver_mapping_type TEXT,
    prose_vs_resolver_jaccard REAL,
    best_alt_record INTEGER,
    best_alt_title TEXT,
    best_alt_jaccard REAL,
    verdict TEXT,
    verdict_confidence TEXT
);
CREATE INDEX ix_repo ON links(repo);
CREATE INDEX ix_doi_text ON links(doi_in_text);
CREATE INDEX ix_verdict ON links(verdict);
CREATE INDEX ix_resolver_record ON links(resolver_record);

CREATE TABLE repos_meta (
    repo TEXT PRIMARY KEY,
    files_scanned INTEGER,
    links_stored INTEGER,
    scanned_at TEXT
);
''')
conn.commit()

# --- Scan pass -----------------------------------------------------------

def scan_file(path, rel, repo_name):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return []
    rows = []

    def line_of(p): return text.count('\n', 0, p) + 1

    # HTML anchors
    for m in A_TAG_RE.finditer(text):
        attrs, inner_raw = m.group(1), m.group(2)
        href = extract_href(attrs)
        if not href:
            continue
        anchor_text = normalize_space(strip_html_tags(inner_raw))
        # Skip empty or trivial (favicon links, style icons)
        if not anchor_text or len(anchor_text) < 2:
            continue
        cb, ca = context_slices(text, m.start(), m.end(), 200, 200)
        prose = enclosing_prose(text, m.start(), m.end(), 800, 800)
        rows.append((
            repo_name, rel, line_of(m.start()), 'html_a',
            anchor_text, href, cb, ca, prose,
            first_doi(anchor_text), doi_from_href(href), first_doi(prose),
            first_axn_hex(anchor_text), first_axn_hex(href),
            alex_record_from_href(href),
        ))

    # Markdown links
    for m in MD_LINK_RE.finditer(text):
        anchor_text = normalize_space(m.group(1))
        href = m.group(2).strip()
        if not anchor_text or len(anchor_text) < 2:
            continue
        cb, ca = context_slices(text, m.start(), m.end(), 200, 200)
        prose = enclosing_prose(text, m.start(), m.end(), 800, 800)
        rows.append((
            repo_name, rel, line_of(m.start()), 'md',
            anchor_text, href, cb, ca, prose,
            first_doi(anchor_text), doi_from_href(href), first_doi(prose),
            first_axn_hex(anchor_text), first_axn_hex(href),
            alex_record_from_href(href),
        ))

    return rows

start = time.time()
total_rows = 0
for repo_dir in sorted(REPOS_DIR.iterdir()):
    if not repo_dir.is_dir(): continue
    repo_name = repo_dir.name
    target = ALEX_LIVE if repo_name == 'alexanarch' else (
        repo_dir.resolve() if repo_dir.is_symlink() else repo_dir
    )
    files = 0
    rows = []
    for path, rel in iter_files(target, repo_name):
        files += 1
        rows.extend(scan_file(path, rel, repo_name))
    if rows:
        cur.executemany('''
            INSERT INTO links(repo, file_path, line_no, link_form,
                              anchor_text, href, context_before, context_after, context_prose,
                              doi_in_text, doi_in_href, doi_in_context,
                              axn_in_text, axn_in_href,
                              href_record_num)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', rows)
    cur.execute('INSERT INTO repos_meta(repo, files_scanned, links_stored, scanned_at) VALUES (?,?,?,?)',
                (repo_name, files, len(rows), time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())))
    conn.commit()
    total_rows += len(rows)
    print(f'  {repo_name:35}  files={files:>5}  links={len(rows):>6}')

print(f'\nSCAN COMPLETE: {total_rows:,} links across {sum(1 for _ in cur.execute("SELECT DISTINCT repo FROM links"))} repos')
print(f'  {time.time()-start:.1f}s')
print(f'  DB: {DB}  size: {DB.stat().st_size / 1024 / 1024:.1f} MB')
