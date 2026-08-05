#!/usr/bin/env python3
"""
publish_wiki_entries.py — generate one crawlable HTML page per wiki entry at
/s/wiki/{deposit_number}/, plus rebuild /s/wiki/index.html with a full static
alphabetical list (retiring the JS-only pagination that hid 97% of entries
from non-JS crawlers).

Task 2 of EA-RETRIEVAL-DENSITY-01.

URL scheme: /s/wiki/{n}/ where n is deposit_number. Matches /s/records/{n}/
for direct navigation. Each wiki entry corresponds 1:1 with a deposit.

Per-entry page:
  - Title (H1) — deposit title
  - Wiki article body from the `wiki` field
  - Defines list (terms this deposit defines)
  - Referenced-by count
  - Canonical link back to /s/records/{n}/
  - JSON-LD Article + DefinedTermSet mention
  - Full DC.* + citation_* meta tags (matching Task 3a record pattern)

Index page: alphabetical (by title) static list of all 865 entries with
their AXN, date, defined-terms count, and refby-total. JS pagination
retired (crawler-hostile); static list is crawler-friendly and readable.
"""
from __future__ import annotations

import json
import html
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_JSON = REPO_ROOT / "data" / "wiki-entries.json"
WIKI_DIR = REPO_ROOT / "s" / "wiki"
SITEMAP = REPO_ROOT / "sitemap.xml"

try:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from render_navbar import render_navbar  # type: ignore
except Exception:
    def render_navbar() -> str:
        return '<nav class="nav"><a href="/">Alexanarch</a> <a href="/s/wiki/">Wiki</a></nav>'


def render_article(text: str) -> str:
    """Render a wiki article's markdown to HTML.

    Added 2026-08-05: the article body was being HTML-escaped and emitted raw,
    so authored emphasis appeared on the page as literal asterisks —
    '**Provenance preemption** interrupts...' rather than bold. Wiki articles
    are written in markdown like every other authored field in the archive;
    the page must parse it. Escaping happens first, so no markup in the source
    can inject HTML.
    """
    import re as _re
    out = []
    for para in _re.split(r'\n\s*\n', (text or '').strip()):
        p = esc(para.strip())
        if not p:
            continue
        p = _re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p)
        p = _re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', p)
        p = _re.sub(r'`([^`]+)`', r'<code>\1</code>', p)
        p = _re.sub(r'\[([^\]]+)\]\((https?://[^\s\)]+|/[^\s\)]+)\)',
                    r'<a href="\2">\1</a>', p)
        # bullet blocks
        if _re.match(r'^\s*[-*]\s', para.strip()):
            items = ''.join(f'<li>{_re.sub(r"^\s*[-*]\s*", "", l)}</li>'
                            for l in p.split('\n') if l.strip())
            out.append(f'<ul>{items}</ul>')
        else:
            out.append('<p>' + p.replace('\n', ' ') + '</p>')
    return ''.join(out)


def esc(s) -> str:
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


PAGE_CSS = (
    '<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");'
    ':root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}'
    '*{margin:0;padding:0;box-sizing:border-box}'
    'body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.7;font-size:15px}'
    '.wrap{max-width:720px;margin:0 auto;padding:60px 24px}'
    'a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}'
    'a:hover{border-bottom-color:var(--accent);background:#f8f8ff}'
    '.nav{display:flex;gap:12px;margin-bottom:20px;font-size:.85em;overflow-x:auto;white-space:nowrap}'
    '.nav a{color:#777;font-weight:500;border:none}.nav a:hover{color:var(--accent);background:none}'
    'h1{font-size:1.35em;font-weight:600;color:var(--accent);margin-bottom:8px;line-height:1.35}'
    'h2{font-size:1em;font-weight:600;color:var(--accent);margin:22px 0 6px}'
    'p{margin:8px 0}code{font-family:var(--mono);font-size:.92em;background:#f0f4f8;padding:1px 6px;border-radius:3px}'
    '.wiki-body{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:16px 20px;line-height:1.8;margin:12px 0;color:#333}'
    '.axn{font-family:var(--mono);font-size:.9em;color:var(--teal);background:var(--surface);padding:10px 14px;border-radius:6px;border-left:4px solid var(--teal);margin:10px 0}'
    '.meta-row{margin:6px 0;font-size:.9em}.meta-row strong{color:var(--accent);display:inline-block;min-width:130px}'
    '.tag{display:inline-block;background:#f0f4f8;color:var(--accent);padding:2px 8px;border-radius:10px;font-size:.78em;margin:2px}'
    '.footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}'
    '.entry-row{padding:8px 0;border-bottom:1px solid #eee;font-size:.9em}'
    '.entry-row a{border:none}.entry-row a:hover{border-bottom:1px solid var(--accent)}'
    '.entry-meta{color:#777;font-size:.85em;margin-top:2px}'
    '</style>'
)


def render_entry_page(entry: dict) -> str:
    n = entry.get("n")
    axn = entry.get("axn", "")
    title = entry.get("title", "")
    creator = entry.get("creator", "")
    date = entry.get("date", "")
    wiki_body = entry.get("wiki", "")
    defines = entry.get("defines", []) or []
    refby_total = entry.get("refby_total", 0)

    page_url = f"https://www.alexanarch.org/s/wiki/{n}/"
    record_url = f"https://www.alexanarch.org/s/records/{n}/"

    jsonld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": record_url,
        "name": f"Wiki entry: {title}",
        "headline": title,
        "author": {"@type": "Person", "name": creator or "Lee Sharks"},
        "datePublished": date,
        "url": record_url,
        "mainEntityOfPage": record_url,
        "about": {"@type": "ScholarlyArticle", "url": record_url, "identifier": axn},
        "articleBody": wiki_body,
    }
    if defines:
        jsonld["mentions"] = [{"@type": "DefinedTerm", "name": t} for t in defines[:20]]

    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
        f'<title>Wiki: {esc(title)} — Alexanarch</title>'
        f'<meta name="description" content="{esc(wiki_body[:160])}">'
        f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
        f'<link rel="canonical" href="{record_url}">'
        '<meta name="robots" content="noindex,follow">'
        f'<meta name="citation_title" content="Wiki entry: {esc(title)}">'
        f'<meta name="citation_author" content="{esc(creator or "Lee Sharks")}">'
        f'<meta name="citation_publication_date" content="{esc(date)}">'
        '<meta name="citation_journal_title" content="Alexanarch">'
        '<meta name="citation_publisher" content="Alexanarch">'
        f'<meta name="citation_abstract" content="{esc(wiki_body[:500])}">'
        f'<meta name="citation_public_url" content="{page_url}">'
        f'<meta name="citation_fulltext_html_url" content="{page_url}">'
        '<meta name="citation_language" content="en">'
        f'<meta name="DC.title" content="Wiki: {esc(title)}">'
        f'<meta name="DC.creator" content="{esc(creator or "Lee Sharks")}">'
        f'<meta name="DC.date" content="{esc(date)}" scheme="DCTERMS.W3CDTF">'
        f'<meta name="DC.identifier" content="{page_url}" scheme="DCTERMS.URI">'
        f'<meta name="DC.description" content="{esc(wiki_body[:500])}">'
        '<meta name="DC.language" content="en" scheme="DCTERMS.RFC3066">'
        '<meta name="DC.type" content="Wiki article (encyclopedic entry for a deposit)">'
        '<meta name="DC.rights" content="CC BY 4.0">'
        '<meta name="DC.publisher" content="Alexanarch">'
        f'<meta name="DC.relation" content="{record_url}" scheme="DCTERMS.URI">'
        f'{PAGE_CSS}</head>'
    )

    parts = ['<body><div class="wrap">', render_navbar()]
    parts.append(
        f'<div style="font-size:.8em;color:#777;margin-bottom:6px">'
        f'<a href="/s/wiki/">Wiki</a> › <a href="/s/records/{n}/">#{n}</a>'
        f'</div>'
    )
    parts.append(f'<h1>{esc(title)}</h1>')
    parts.append(
        f'<div style="font-size:.85em;color:#777;margin-bottom:10px">'
        f'{esc(creator)} · {esc(date)} · deposit #{n}'
        f'</div>'
    )
    parts.append(f'<div class="axn">{esc(axn)}</div>')

    parts.append('<h2>Article</h2>')
    parts.append(f'<div class="wiki-body">{render_article(wiki_body)}</div>')

    if defines:
        parts.append(f'<h2>Defines ({len(defines)})</h2>')
        parts.append('<div>')
        for t in defines:
            parts.append(f'<span class="tag">{esc(t)}</span>')
        parts.append('</div>')

    if refby_total:
        parts.append('<h2>Reference network</h2>')
        parts.append(
            f'<p style="font-size:.9em;color:#555">Referenced by {refby_total} other '
            f'entities in the archive. See the full <a href="/s/graph/">Knowledge Graph</a> '
            f'for reference paths, or the <a href="/s/records/{n}/">primary record</a> for '
            f'the full deposit with reference details.</p>'
        )

    parts.append(
        f'<div class="footer">'
        f'Primary record: <a href="/s/records/{n}/">/s/records/{n}/</a> · '
        f'AXN resolver: <a href="/s/axn/{axn.split(":")[1].split(".")[0] if ":" in axn else n}/">/s/axn/{axn.split(":")[1].split(".")[0] if ":" in axn else n}/</a> · '
        f'<a href="/s/wiki/">All wiki entries →</a>'
        f'</div>'
    )
    parts.append('</div></body></html>')

    return head + '\n'.join(parts)


def render_index_page(entries: list) -> str:
    """Full alphabetical static list — no JS pagination hiding entries from crawlers."""
    sorted_entries = sorted(entries, key=lambda e: (e.get("title", "") or "").lower())

    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
        f'<title>Wiki — Alexanarch ({len(entries)} entries)</title>'
        f'<meta name="description" content="Alexanarch Wiki. {len(entries)} encyclopedic entries — one per deposit — with definitions, references, and links to primary records.">'
        '<link rel="canonical" href="https://www.alexanarch.org/s/wiki/">'
        f'{PAGE_CSS}</head>'
    )
    parts = ['<body><div class="wrap">', render_navbar()]
    parts.append('<h1>Alexanarch Wiki</h1>')
    parts.append(
        f'<p style="color:#555;font-size:.92em;margin-bottom:16px">'
        f'{len(entries):,} encyclopedic entries auto-projected from '
        f'<code>data/registry.json</code>. Each entry summarizes a deposit '
        f'and lists the concepts it defines. Alphabetical by title. '
        f'Machine-readable dataset: <a href="/data/wiki-entries.json"><code>/data/wiki-entries.json</code></a>.'
        f'</p>'
    )

    parts.append('<div style="font-size:.85em;color:#777;margin:16px 0 8px">'
                 f'{len(entries)} entries · sorted alphabetically</div>')

    for e in sorted_entries:
        n = e.get("n")
        title = e.get("title", "")
        axn = e.get("axn", "")
        date = e.get("date", "")
        defines = e.get("defines", []) or []
        refby = e.get("refby_total", 0)
        defines_count = len(defines)

        parts.append(
            f'<div class="entry-row">'
            f'<div><a href="/s/wiki/{n}/">{esc(title)}</a></div>'
            f'<div class="entry-meta">'
            f'<span style="font-family:var(--mono);color:var(--teal)">{esc(axn)}</span>'
            f' · {esc(date)} · #{n}'
            f' · defines {defines_count}'
            f' · refby {refby}'
            f'</div>'
            f'</div>'
        )

    parts.append(
        f'<div class="footer">'
        f'{len(entries):,} entries total. Full dataset: '
        f'<a href="/data/wiki-entries.json"><code>/data/wiki-entries.json</code></a> · '
        f'Body-text search: <a href="/api/body-index.json"><code>/api/body-index.json</code></a>'
        f'</div>'
    )
    parts.append('</div></body></html>')

    return head + '\n'.join(parts)


def update_sitemap(entries: list) -> None:
    """Per-entry wiki URLs NO LONGER enter the sitemap (Canonical Record
    Convergence P0.7, 2026-07-19): wiki pages canonicalize to their records
    and carry noindex,follow, so listing them as crawl targets would be
    contradictory. This function now REMOVES any legacy /s/wiki/{n}/ URLs
    from sitemap.xml (idempotent)."""
    if not SITEMAP.exists():
        return
    import re as _re
    xml = SITEMAP.read_text(encoding="utf-8")
    cleaned = _re.sub(r'\s*<url><loc>https://alexanarch\.org/s/wiki/\d+/</loc>.*?</url>', '', xml)
    if cleaned != xml:
        SITEMAP.write_text(cleaned, encoding="utf-8")
        print("  ✓ sitemap purged of per-entry wiki URLs (canonical lives at the record)")

def main() -> int:
    print("Loading wiki-entries.json...")
    data = json.loads(WIKI_JSON.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    print(f"  {len(entries):,} entries")

    print("Rendering per-entry pages...")
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    n_written = 0
    for e in entries:
        n = e.get("n")
        if n is None:
            continue
        page_dir = WIKI_DIR / str(n)
        page_dir.mkdir(exist_ok=True)
        html_text = render_entry_page(e)
        (page_dir / "index.html").write_text(html_text, encoding="utf-8")
        n_written += 1
        if n_written % 200 == 0:
            print(f"  {n_written}/{len(entries)} written")
    print(f"  ✓ {n_written} wiki entry pages")

    print("Rebuilding /s/wiki/index.html (static alphabetical list)...")
    idx_html = render_index_page(entries)
    (WIKI_DIR / "index.html").write_text(idx_html, encoding="utf-8")
    print(f"  ✓ s/wiki/index.html ({len(idx_html):,} bytes)")

    print("Updating sitemap.xml...")
    update_sitemap(entries)

    return 0


if __name__ == "__main__":
    sys.exit(main())
