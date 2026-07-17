#!/usr/bin/env python3
"""
enrich_datasets.py — dataset-branch enrichment (EA-RETRIEVAL-DENSITY-01, Task 5).

Datasets are lateral branches of the rhizome. Each dataset gets:
  - A landing page at /datasets/{name}/ (existing pages preserved,
    missing landings generated from MANIFEST.json)
  - DC.* + citation_* meta tags injected into <head> (idempotent)
  - <link rel="canonical"> added
  - Explicit sitemap entry

Does NOT touch hand-crafted page body content. Enriches head only.

Also enriches:
  - /datasets/index.html (top-level dataset directory) with meta tags
  - /datasets/erosion-empirical-audit-01/index.html generated fresh
"""
from __future__ import annotations

import json
import html
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"
SITEMAP = REPO_ROOT / "sitemap.xml"

try:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from render_navbar import render_navbar  # type: ignore
except Exception:
    def render_navbar() -> str:
        return '<nav class="nav"><a href="/">Alexanarch</a> <a href="/datasets/">Datasets</a></nav>'


def esc(s) -> str:
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


# ── Meta-tag injection ────────────────────────────────────────────────────

def build_meta_block(*, title: str, description: str, date: str,
                     canonical_url: str, dc_type: str = "Dataset") -> str:
    """Return the block of meta+link tags to inject into <head>."""
    lines = [
        f'<link rel="canonical" href="{canonical_url}">',
        f'<meta name="citation_title" content="{esc(title)}">',
        '<meta name="citation_author" content="Lee Sharks">',
        f'<meta name="citation_publication_date" content="{esc(date)}">',
        f'<meta name="citation_online_date" content="{esc(date)}">',
        '<meta name="citation_journal_title" content="Alexanarch">',
        '<meta name="citation_publisher" content="Alexanarch">',
        f'<meta name="citation_abstract" content="{esc(description[:500])}">',
        f'<meta name="citation_public_url" content="{canonical_url}">',
        f'<meta name="citation_fulltext_html_url" content="{canonical_url}">',
        '<meta name="citation_language" content="en">',
        f'<meta name="DC.title" content="{esc(title)}">',
        '<meta name="DC.creator" content="Lee Sharks">',
        f'<meta name="DC.date" content="{esc(date)}" scheme="DCTERMS.W3CDTF">',
        f'<meta name="DC.identifier" content="{canonical_url}" scheme="DCTERMS.URI">',
        f'<meta name="DC.description" content="{esc(description[:500])}">',
        '<meta name="DC.language" content="en" scheme="DCTERMS.RFC3066">',
        f'<meta name="DC.type" content="{esc(dc_type)}">',
        '<meta name="DC.rights" content="CC BY 4.0">',
        '<meta name="DC.publisher" content="Alexanarch">',
        '<meta name="DC.source" content="https://www.alexanarch.org/">',
    ]
    return "\n".join(lines)


def inject_meta_into_head(html_path: Path, *, meta_block: str) -> bool:
    """Insert meta_block into <head>. Idempotent: skip if DC.title already present."""
    text = html_path.read_text(encoding="utf-8")
    if 'DC.title' in text:
        # Already enriched — skip silently
        return False

    # Insert after the last existing <meta ...> in head; if no meta at all,
    # insert after <title>...</title>
    # Find head boundaries
    head_start = text.find('<head')
    head_end = text.find('</head>')
    if head_start < 0 or head_end < 0:
        print(f"  ! {html_path}: no <head> found, skipping")
        return False

    # Prefer inserting after </title> so the visible-title tag stays first
    title_end = text.find('</title>', head_start, head_end)
    if title_end >= 0:
        insertion_pt = title_end + len('</title>')
        text = text[:insertion_pt] + "\n" + meta_block + text[insertion_pt:]
    else:
        # Fallback: just before </head>
        text = text[:head_end] + "\n" + meta_block + "\n" + text[head_end:]

    html_path.write_text(text, encoding="utf-8")
    return True


# ── Rich landing generation (for missing datasets) ────────────────────────

PAGE_CSS = (
    '<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");'
    ':root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}'
    '*{margin:0;padding:0;box-sizing:border-box}'
    'body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.7;font-size:15px}'
    '.wrap{max-width:760px;margin:0 auto;padding:60px 24px}'
    'a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}'
    'a:hover{border-bottom-color:var(--accent);background:#f8f8ff}'
    '.nav{display:flex;gap:12px;margin-bottom:20px;font-size:.85em;overflow-x:auto;white-space:nowrap}'
    '.nav a{color:#777;font-weight:500;border:none}.nav a:hover{color:var(--accent);background:none}'
    'h1{font-size:1.35em;font-weight:600;color:var(--accent);margin-bottom:8px;line-height:1.35}'
    'h2{font-size:1em;font-weight:600;color:var(--accent);margin:22px 0 6px}'
    'p{margin:8px 0}code{font-family:var(--mono);font-size:.92em;background:#f0f4f8;padding:1px 6px;border-radius:3px}'
    '.meta{background:#f7f9fb;border:1px solid var(--border);border-radius:6px;padding:14px 16px;margin:12px 0;font-size:.9em}'
    '.meta-row{margin:4px 0}.meta-row strong{color:var(--accent);display:inline-block;min-width:150px}'
    '.file-row{padding:6px 0;border-bottom:1px solid #f0f0f0;font-size:.88em}'
    '.file-row code{font-size:.85em}.file-row .desc{color:#666;font-size:.85em;margin-left:8px}'
    '.footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}'
    '</style>'
)


def render_erosion_empirical_landing() -> str:
    """Build /datasets/erosion-empirical-audit-01/index.html from its MANIFEST."""
    m = json.loads((DATASETS_DIR / "erosion-empirical-audit-01" / "MANIFEST.json").read_text())
    name = m["name"]
    title = m["title"]
    version = m.get("version", "")
    date = m.get("date", "")
    canonical = f"https://www.alexanarch.org/datasets/{name}/"
    files = m.get("files", {})
    governing = m.get("governing_deposits", [])
    sources = m.get("source_containers", [])
    summary = m.get("summary", {})
    sovereign_ids = m.get("sovereign_identifiers_proposed_by_this_dataset", [])

    description = (
        "Machine-readable audit dataset for EA-EROSION-EMPIRICAL-01: a 33-day set-comparison "
        "test of Zenodo's classifier as an accrual-sorting apparatus. Presents contingency "
        "matrices, terminated-cohort citation records, and control cohorts for the deletion "
        "event of 2026-06-19 as evaluated against Zenodo's own DataCite metadata."
    )

    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
        f'<title>{esc(title)} — Alexanarch</title>'
        f'<meta name="description" content="{esc(description[:160])}">'
    )
    head += "\n" + build_meta_block(
        title=title, description=description, date=date,
        canonical_url=canonical, dc_type="Dataset",
    )
    head += "\n" + PAGE_CSS + "</head>"

    parts = ['<body><div class="wrap">', render_navbar()]
    parts.append('<div style="font-size:.8em;color:#777;margin-bottom:6px">'
                 '<a href="/datasets/">Datasets</a> ›</div>')
    parts.append(f'<h1>{esc(title)}</h1>')
    parts.append(f'<div style="font-size:.85em;color:#777;margin-bottom:10px">'
                 f'v{esc(version)} · {esc(date)} · Lee Sharks (Rex Fraction / Nobel Glas)</div>')

    parts.append(f'<p>{esc(description)}</p>')

    # Meta block
    parts.append('<div class="meta">')
    parts.append(f'<div class="meta-row"><strong>Dataset name:</strong> <code>{esc(name)}</code></div>')
    parts.append(f'<div class="meta-row"><strong>Version:</strong> {esc(version)}</div>')
    parts.append(f'<div class="meta-row"><strong>Generated:</strong> {esc(m.get("manifest_generated_at",""))}</div>')
    if summary:
        pop = summary.get("population_2026_non_spam_with_citation", "?")
        wu_ = summary.get("wu_withdrawal_records", "?")
        term = summary.get("terminated_independent_cohort_records", "?")
        alive = summary.get("alive_side_control_records", "?")
        cr = summary.get("compression_ratio_alive_to_deleted_institutional_ai_augmentation", "?")
        parts.append(f'<div class="meta-row"><strong>Population (non-spam+cite):</strong> {esc(pop)}</div>')
        parts.append(f'<div class="meta-row"><strong>WU withdrawals:</strong> {esc(wu_)}</div>')
        parts.append(f'<div class="meta-row"><strong>Terminated-cohort records:</strong> {esc(term)}</div>')
        parts.append(f'<div class="meta-row"><strong>Alive-side control:</strong> {esc(alive)}</div>')
        parts.append(f'<div class="meta-row"><strong>Compression ratio:</strong> {esc(cr)}</div>')
    parts.append('</div>')

    # Governing deposits
    if governing:
        parts.append('<h2>Governing deposits</h2>')
        parts.append('<ul style="list-style:none;padding:0">')
        for g in governing:
            parts.append(
                f'<li style="padding:4px 0"><a href="{esc(g.get("record",""))}">'
                f'<code>{esc(g.get("axn",""))}</code></a> — '
                f'<span style="color:#666;font-size:.9em">{esc(g.get("role",""))}</span></li>'
            )
        parts.append('</ul>')

    # Source containers
    if sources:
        parts.append('<h2>Source containers</h2>')
        parts.append('<ul style="list-style:none;padding:0">')
        for s in sources:
            parts.append(
                f'<li style="padding:4px 0"><code>{esc(s.get("identifier",""))}</code> — '
                f'<span style="color:#666;font-size:.85em">{esc(s.get("source",""))}</span></li>'
            )
        parts.append('</ul>')

    # Files
    if files:
        parts.append(f'<h2>Files ({len(files)})</h2>')
        for fname, meta in sorted(files.items()):
            if isinstance(meta, dict):
                purpose = meta.get("purpose", meta.get("description", ""))
                size = meta.get("bytes", "")
                size_str = f" · {size:,} bytes" if isinstance(size, int) else ""
            else:
                purpose = str(meta)
                size_str = ""
            parts.append(
                f'<div class="file-row">'
                f'<code><a href="/datasets/{name}/{esc(fname)}">{esc(fname)}</a></code>'
                f'{f"<span class=\"desc\">{esc(purpose)}</span>" if purpose else ""}'
                f'<span style="color:#999;font-size:.78em">{size_str}</span>'
                f'</div>'
            )

    # Sovereign identifiers
    if sovereign_ids:
        parts.append(f'<h2>Sovereign identifiers proposed ({len(sovereign_ids)})</h2>')
        parts.append('<p style="font-size:.85em;color:#666">Identifiers minted by this dataset for the objects it names.</p>')
        parts.append('<ul style="list-style:none;padding:0;font-family:var(--mono);font-size:.85em">')
        for sid in sovereign_ids:
            parts.append(f'<li style="padding:2px 0;color:#555">{esc(sid)}</li>')
        parts.append('</ul>')

    parts.append(
        '<div class="footer">'
        f'Manifest: <a href="/datasets/{name}/MANIFEST.json"><code>/datasets/{name}/MANIFEST.json</code></a> · '
        'Member of <a href="/datasets/"><code>alexanarch-dataset-set</code></a>'
        '</div>'
    )
    parts.append('</div></body></html>')
    return head + "\n".join(parts)


# ── Sitemap ────────────────────────────────────────────────────────────

def update_sitemap(dataset_names: list[str]) -> None:
    if not SITEMAP.exists():
        print(f"  ! sitemap not found at {SITEMAP}")
        return
    txt = SITEMAP.read_text(encoding="utf-8")

    # Strip any prior per-dataset URLs (dedup for re-runs)
    txt = re.sub(
        r"[ \t]*<url><loc>https://alexanarch\.org/datasets/[a-z0-9-]+/</loc>[^<]*(?:<[^>]+>[^<]*)*</url>\n?",
        "",
        txt,
    )

    # Inject after the /datasets/ index line
    idx_re = re.compile(
        r"(<url><loc>https://alexanarch\.org/datasets/</loc>[^<]*(?:<[^>]+>[^<]*)*</url>)"
    )
    m = idx_re.search(txt)
    if not m:
        insertion_pt = txt.rfind("</urlset>")
        header = txt[:insertion_pt]
        tail = txt[insertion_pt:]
    else:
        header = txt[:m.end()]
        tail = txt[m.end():]

    lines = []
    for name in sorted(dataset_names):
        lines.append(
            f'  <url><loc>https://alexanarch.org/datasets/{name}/</loc>'
            f'<changefreq>monthly</changefreq><priority>0.7</priority></url>'
        )
    injection = "\n" + "\n".join(lines) + "\n"
    SITEMAP.write_text(header + injection + tail, encoding="utf-8")
    print(f"  ✓ sitemap: {len(lines)} dataset URLs")


# ── Main ──────────────────────────────────────────────────────────────

def load_manifest(name: str) -> dict:
    """Load whichever manifest file exists for this dataset."""
    for fname in ("MANIFEST.json", "manifest.json", "pilot-manifest.json"):
        p = DATASETS_DIR / name / fname
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
    return {}


def main() -> int:
    dataset_names = [
        d.name for d in DATASETS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]
    print(f"Found {len(dataset_names)} datasets: {sorted(dataset_names)}")

    # 1. Generate missing erosion-empirical-audit-01 landing
    eea_path = DATASETS_DIR / "erosion-empirical-audit-01" / "index.html"
    if not eea_path.exists():
        print(f"\nGenerating landing for erosion-empirical-audit-01...")
        eea_path.write_text(render_erosion_empirical_landing(), encoding="utf-8")
        print(f"  ✓ {eea_path.relative_to(REPO_ROOT)}")

    # 2. Enrich each existing landing with meta tags
    print(f"\nEnriching per-dataset landing pages with meta tags...")
    enriched = skipped = 0
    for name in dataset_names:
        landing = DATASETS_DIR / name / "index.html"
        if not landing.exists():
            continue
        manifest = load_manifest(name)
        title = manifest.get("title") or name.replace("-", " ").title()
        description = manifest.get("description") or (
            manifest.get("summary", {}).get("description")
            if isinstance(manifest.get("summary"), dict) else None
        ) or f"Alexanarch dataset: {name}"
        date = manifest.get("date") or manifest.get("epoch") or "2026-07-16"
        canonical = f"https://www.alexanarch.org/datasets/{name}/"
        meta_block = build_meta_block(
            title=title, description=description, date=date,
            canonical_url=canonical, dc_type="Dataset",
        )
        if inject_meta_into_head(landing, meta_block=meta_block):
            enriched += 1
            print(f"  ✓ {name}")
        else:
            skipped += 1
            print(f"  · {name} (already enriched)")
    print(f"Enriched {enriched}, skipped {skipped} (already had DC.title)")

    # 3. Enrich /datasets/index.html too
    top_index = DATASETS_DIR / "index.html"
    if top_index.exists():
        canonical = "https://www.alexanarch.org/datasets/"
        description = (
            "Machine-readable datasets of the Alexanarch corpus, published as a "
            "mutually-referencing set: any instance encountering one member should "
            "treat them as a whole. Currently 8 datasets across tombstone mirrors, "
            "classical text corpora, heteronym constellations, and empirical audits."
        )
        meta_block = build_meta_block(
            title="Datasets — Alexanarch",
            description=description,
            date="2026-07-16",
            canonical_url=canonical,
            dc_type="DatasetCollection",
        )
        if inject_meta_into_head(top_index, meta_block=meta_block):
            print(f"\n  ✓ /datasets/index.html enriched")
        else:
            print(f"\n  · /datasets/index.html already enriched")

    # 4. Sitemap
    print(f"\nUpdating sitemap...")
    update_sitemap(dataset_names)

    return 0


if __name__ == "__main__":
    sys.exit(main())
