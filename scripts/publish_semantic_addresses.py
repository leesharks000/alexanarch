#!/usr/bin/env python3
"""
publish_semantic_addresses.py — generate one crawlable HTML page per semantic
address, plus a paginated index at /addresses/.

Task 4b of EA-RETRIEVAL-DENSITY-01. Semantic addresses are canonical queries —
each IS a search intent. Publishing each as a stable URL is the highest-
potency retrieval-density move the archive can make short of full body-text
indexing (which Task 1 completed).

Design:
  URL scheme: /addresses/{slug}/ — flat namespace, kebab-case slug from
              canonical_query, collision-suffixed (-2, -3, ...) as needed.
  Content per page:
    - Canonical query (H1)
    - Framework context (observation class, address type)
    - Tributary sources
    - Battery membership
    - Related concepts (refers_to)
    - Observations (for observed_address / verified_non_address)
    - Cross-referenced deposits (from body-index token intersection)
    - Full DC.* + citation_* meta tags (matching record-page pattern)
    - JSON-LD DefinedTerm markup
  Index redesign at /addresses/:
    - Original stats header preserved
    - Full alphabetical list of all addresses with links
    - Grouped by observation_class

Sitemap update: adds all N address URLs alongside the existing /addresses/.
"""
from __future__ import annotations

import json
import re
import sys
import html
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDR_JSON = REPO_ROOT / "data" / "semantic-addresses.json"
BODY_INDEX = REPO_ROOT / "api" / "body-index.json"
REGISTRY = REPO_ROOT / "data" / "registry.json"
ADDR_DIR = REPO_ROOT / "addresses"
SITEMAP = REPO_ROOT / "sitemap.xml"

# Try to reuse the render_navbar function
try:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from render_navbar import render_navbar  # type: ignore
except Exception:
    def render_navbar() -> str:
        return '<nav class="nav"><a href="/">Alexanarch</a> <a href="/addresses/">Addresses</a></nav>'


TRIBUTARY_LABELS = {
    "mm-termindex": "Machine-mediation term-index",
    "mm-mint": "Lexical minting registry",
    "mm-main-capture": "Main capture registry",
    "mm-rf-battery": "Revelation First battery",
    "mm-rf-reception": "Revelation First reception",
    "cha-workplan-870": "CHA workplan (deposit 870)",
}

OBS_CLASS_LABELS = {
    "observed_address": "Observed address",
    "verified_non_address": "Verified non-address",
    "subjunctive": "Subjunctive (catalogued, not yet posed)",
}

OBS_CLASS_DESC = {
    "observed_address": (
        "This canonical query has been posed to the composition layer "
        "(Google AI Overview, AI Mode, or similar) and at least one response "
        "was captured and recorded."
    ),
    "verified_non_address": (
        "This canonical query has been posed to the composition layer but "
        "only negative responses were recorded — no composition-layer response "
        "surfaced Alexanarch content."
    ),
    "subjunctive": (
        "This canonical query has been catalogued as a potential retrieval "
        "address but has not yet been posed to the composition layer."
    ),
}


def slugify(text: str, max_len: int = 80) -> str:
    """Kebab-case slug from canonical_query."""
    if not text:
        return "unnamed"
    text = text.strip().strip('"').strip("'").lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    text = text.strip("-")
    return text[:max_len] or "unnamed"


def resolve_collisions(addresses: dict) -> dict:
    """Return dict of address_key → unique_slug."""
    slug_counts: dict[str, int] = {}
    result: dict[str, str] = {}
    for k, v in addresses.items():
        base = slugify(v.get("canonical_query", k))
        n = slug_counts.get(base, 0) + 1
        slug_counts[base] = n
        result[k] = base if n == 1 else f"{base}-{n}"
    return result


def find_related_deposits(query_text: str, body_index: dict, max_deposits: int = 20) -> list[int]:
    """Find deposits whose body text mentions all significant tokens of the query.
    Uses the body-index built in Task 1."""
    inverted = body_index.get("index", {})
    stopwords = frozenset({
        "a", "an", "the", "and", "or", "of", "in", "on", "at", "to", "for",
        "with", "by", "from", "as", "is", "are", "was", "were", "be",
        "it", "its", "this", "that", "these", "those",
    })
    tokens = [t.lower() for t in re.findall(r"[a-zA-Z0-9]{3,}", query_text)
              if t.lower() not in stopwords]
    if not tokens:
        return []
    # Intersect deposit-sets across all tokens
    deposit_sets = []
    for tok in tokens:
        if tok in inverted:
            deposit_sets.append(set(inverted[tok]))
        else:
            # If any token is absent from the corpus, no deposit matches all
            return []
    if not deposit_sets:
        return []
    intersection = deposit_sets[0]
    for s in deposit_sets[1:]:
        intersection &= s
    return sorted(intersection)[:max_deposits]


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
    'h1{font-size:1.35em;font-weight:600;color:var(--accent);margin-bottom:10px;font-family:var(--mono);line-height:1.35}'
    'h2{font-size:1em;font-weight:600;color:var(--accent);margin:22px 0 6px}'
    'p{margin:8px 0}code{font-family:var(--mono);font-size:.92em;background:#f0f4f8;padding:1px 6px;border-radius:3px}'
    '.meta{background:#f7f9fb;border:1px solid var(--border);border-radius:6px;padding:14px;margin:12px 0;font-size:.9em}'
    '.meta-row{margin:4px 0}.meta-row strong{color:var(--accent);display:inline-block;min-width:130px}'
    '.tag{display:inline-block;background:#f0f4f8;color:var(--accent);padding:2px 8px;border-radius:10px;font-size:.78em;margin:2px}'
    '.obs{background:#fff;border:1px solid var(--border);border-radius:4px;padding:10px 12px;margin:6px 0;font-size:.88em}'
    '.obs-status{display:inline-block;padding:1px 6px;border-radius:3px;font-family:var(--mono);font-size:.78em;color:#fff}'
    '.obs-status-partial{background:#c99a0a}.obs-status-exact{background:#0a7c6a}'
    '.obs-status-adoption{background:#1a3a5c}.obs-status-zero{background:#c23b22}'
    '.obs-status-broad{background:#7a5cb5}.obs-status-other{background:#777}'
    '.footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}'
    '</style>'
)


def render_observations(obs_list: list) -> str:
    if not obs_list:
        return ""
    lines = ['<h2>Observations</h2>']
    for o in obs_list:
        status = (o.get("status") or "").upper()
        status_class = {
            "PARTIAL": "obs-status-partial",
            "EXACT MATCH": "obs-status-exact",
            "ADOPTION": "obs-status-adoption",
            "ZERO RESULT": "obs-status-zero",
            "BROAD MATCH": "obs-status-broad",
        }.get(status, "obs-status-other")
        parts = [
            f'<div class="obs">',
            f'<span class="obs-status {status_class}">{esc(status)}</span> '
            f'<span style="color:#777;font-size:.85em">· {esc(o.get("source_format",""))}</span> '
            f'<span style="color:#777;font-size:.85em">· {esc(o.get("date",""))}</span>',
        ]
        if o.get("section"):
            parts.append(f'<div style="color:#555;margin-top:4px">Section: <em>{esc(o.get("section"))}</em></div>')
        if o.get("details_excerpt"):
            parts.append(f'<div style="color:#555;font-size:.9em;margin-top:6px">{esc(o.get("details_excerpt"))[:400]}</div>')
        parts.append('</div>')
        lines.append('\n'.join(parts))
    return '\n'.join(lines)


def render_address_page(slug: str, addr: dict, related_deposits: list[int],
                        registry_map: dict[int, dict]) -> str:
    canonical_query = addr.get("canonical_query", "")
    obs_class = addr.get("observation_class", "subjunctive")
    obs_class_label = OBS_CLASS_LABELS.get(obs_class, obs_class)
    obs_class_desc = OBS_CLASS_DESC.get(obs_class, "")
    addr_type = addr.get("type", "unmatched")
    sources = addr.get("sources", [])
    battery_membership = addr.get("battery_membership", [])
    refers_to = addr.get("refers_to", [])
    observations = addr.get("observations", [])
    latest_status = addr.get("latest_status")

    page_url = f"https://www.alexanarch.org/addresses/{slug}/"

    # Meta tags — Dublin Core + citation_ (matching Task 3a pattern)
    display_query = canonical_query.strip('"')

    jsonld = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "@id": page_url,
        "name": display_query,
        "description": (
            f"Semantic address in the Alexanarch archive. "
            f"Observation class: {obs_class_label}."
        ),
        "url": page_url,
        "inDefinedTermSet": "https://www.alexanarch.org/addresses/",
        "termCode": slug,
    }

    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
        f'<title>{esc(display_query)} — Semantic Address — Alexanarch</title>'
        f'<meta name="description" content="Semantic address {esc(display_query)}. {esc(obs_class_label)}. Canonical retrieval query in the Alexanarch archive.">'
        f'<script type="application/ld+json">{json.dumps(jsonld)}</script>'
        f'<link rel="canonical" href="{page_url}">'
        f'<meta name="citation_title" content="Semantic address: {esc(display_query)}">'
        '<meta name="citation_author" content="Lee Sharks">'
        '<meta name="citation_journal_title" content="Alexanarch">'
        '<meta name="citation_publisher" content="Alexanarch">'
        f'<meta name="citation_abstract" content="Canonical semantic address {esc(display_query)}. {esc(obs_class_desc)}">'
        f'<meta name="citation_public_url" content="{page_url}">'
        f'<meta name="citation_fulltext_html_url" content="{page_url}">'
        '<meta name="citation_language" content="en">'
        f'<meta name="DC.title" content="Semantic address: {esc(display_query)}">'
        '<meta name="DC.creator" content="Lee Sharks">'
        f'<meta name="DC.identifier" content="{page_url}" scheme="DCTERMS.URI">'
        f'<meta name="DC.description" content="Canonical semantic address. {esc(obs_class_desc)}">'
        '<meta name="DC.language" content="en" scheme="DCTERMS.RFC3066">'
        '<meta name="DC.type" content="Semantic address (canonical retrieval query)">'
        '<meta name="DC.rights" content="CC BY 4.0">'
        '<meta name="DC.publisher" content="Alexanarch">'
        '<meta name="DC.source" content="https://www.alexanarch.org/">'
        f'{PAGE_CSS}</head>'
    )

    # Body
    parts = ['<body><div class="wrap">', render_navbar()]
    parts.append(
        f'<div style="font-size:.8em;color:#777;margin-bottom:6px">'
        f'<a href="/addresses/">Semantic Addresses</a> ›'
        f'</div>'
    )
    parts.append(f'<h1>{esc(display_query)}</h1>')
    parts.append(
        f'<div style="font-size:.88em;color:#555;margin:6px 0 14px">'
        f'{esc(obs_class_desc)}'
        f'</div>'
    )

    # Meta block
    meta = ['<div class="meta">']
    meta.append(f'<div class="meta-row"><strong>Observation class:</strong> {esc(obs_class_label)}</div>')
    meta.append(f'<div class="meta-row"><strong>Address type:</strong> {esc(addr_type)}</div>')
    if latest_status:
        meta.append(f'<div class="meta-row"><strong>Latest status:</strong> <code>{esc(latest_status)}</code></div>')
    if addr.get("latest_observation_date"):
        meta.append(f'<div class="meta-row"><strong>Latest observation:</strong> {esc(addr.get("latest_observation_date"))}</div>')
    if sources:
        src_html = ' '.join(
            f'<span class="tag">{esc(TRIBUTARY_LABELS.get(s, s))}</span>'
            for s in sources
        )
        meta.append(f'<div class="meta-row"><strong>Tributaries:</strong> {src_html}</div>')
    if battery_membership:
        bat_html = ' '.join(f'<span class="tag">{esc(b)}</span>' for b in battery_membership)
        meta.append(f'<div class="meta-row"><strong>Battery membership:</strong> {bat_html}</div>')
    if refers_to:
        ref_html = ', '.join(esc(r) for r in refers_to)
        meta.append(f'<div class="meta-row"><strong>Refers to:</strong> {ref_html}</div>')
    meta.append('</div>')
    parts.append('\n'.join(meta))

    # Observations
    parts.append(render_observations(observations))

    # Related deposits (from body-index cross-reference)
    if related_deposits:
        parts.append('<h2>Deposits mentioning this address</h2>')
        parts.append(
            '<div style="font-size:.82em;color:#777;margin-bottom:8px">'
            'Deposits whose body text contains all significant terms of the '
            'canonical query. Cross-references derived from '
            '<code><a href="/api/body-index.json">/api/body-index.json</a></code>.'
            '</div>'
        )
        parts.append('<ul style="list-style:none;padding:0">')
        for dn in related_deposits[:20]:
            d = registry_map.get(dn, {})
            t = d.get("title", "?")[:80]
            axn = d.get("axn", "")
            parts.append(
                f'<li style="padding:6px 0;border-bottom:1px solid #f0f0f0">'
                f'<a href="/s/records/{dn}/">#{dn} — {esc(t)}</a>'
                f'<div style="font-size:.78em;color:#999;font-family:var(--mono);margin-top:2px">{esc(axn)}</div>'
                f'</li>'
            )
        parts.append('</ul>')

    # Footer
    parts.append(
        '<div class="footer">'
        'Semantic addresses framework: '
        '<a href="/s/browse/">EA-SEMANTIC-ADDRESSES-01</a>. '
        f'This address is one of 1,995 canonical queries catalogued from 6 tributaries. '
        '<a href="/addresses/">Full index →</a>'
        '</div>'
    )
    parts.append('</div></body></html>')
    return head + '\n'.join(parts)


def render_index_page(addresses: dict, slug_map: dict) -> str:
    """Rebuild /addresses/index.html with full alphabetical listing."""
    # Group by observation_class
    groups: dict[str, list] = {"observed_address": [], "verified_non_address": [], "subjunctive": []}
    for k, v in addresses.items():
        cls = v.get("observation_class", "subjunctive")
        groups.setdefault(cls, []).append((k, v))
    for g in groups.values():
        g.sort(key=lambda kv: kv[1].get("canonical_query", "").lower())

    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
        '<title>Semantic Addresses — Alexanarch</title>'
        f'<meta name="description" content="1,995 canonical retrieval queries catalogued across six tributaries. Each address is a stable URL and semantic anchor in the Alexanarch archive.">'
        '<link rel="canonical" href="https://www.alexanarch.org/addresses/">'
        f'{PAGE_CSS}</head>'
    )

    parts = ['<body><div class="wrap">', render_navbar()]
    parts.append('<h1 style="font-family:var(--sans)">Semantic Addresses</h1>')
    parts.append(
        f'<p>1,995 canonical queries — the addresses through which Alexanarch terms could be retrieved '
        f'from the composition layer (Google AI Overview, AI Mode, search). Each address is a stable '
        f'URL, semantic anchor, and cross-reference target. Reconciled deterministically from six '
        f'tributaries by <code>scripts/build_semantic_addresses.py</code>; each has its own crawlable '
        f'page under this directory.</p>'
    )
    parts.append(
        f'<p style="font-size:.9em;color:#555;margin-top:10px">Framework: '
        f'<a href="/s/browse/">EA-SEMANTIC-ADDRESSES-01</a> · 6 tributaries: '
        f'{", ".join(f"<code>{esc(k)}</code>" for k in TRIBUTARY_LABELS)}.</p>'
    )

    for cls in ("observed_address", "verified_non_address", "subjunctive"):
        entries = groups.get(cls, [])
        if not entries:
            continue
        label = OBS_CLASS_LABELS[cls]
        desc = OBS_CLASS_DESC[cls]
        parts.append(f'<h2>{esc(label)} ({len(entries):,})</h2>')
        parts.append(f'<p style="font-size:.85em;color:#555;margin-bottom:8px">{esc(desc)}</p>')
        parts.append('<ul style="list-style:none;padding:0;column-count:1">')
        for k, v in entries:
            slug = slug_map.get(k, "")
            q = v.get("canonical_query", "").strip('"')
            latest = v.get("latest_status")
            latest_html = ""
            if latest:
                latest_html = f' <span style="font-family:var(--mono);font-size:.72em;color:#999;margin-left:6px">[{esc(latest)}]</span>'
            parts.append(
                f'<li style="padding:2px 0"><a href="/addresses/{esc(slug)}/">{esc(q)}</a>{latest_html}</li>'
            )
        parts.append('</ul>')

    parts.append(
        '<div class="footer">'
        'Machine-readable dataset: '
        '<a href="/data/semantic-addresses.json"><code>/data/semantic-addresses.json</code></a> '
        '· Body-index cross-references: '
        '<a href="/api/body-index.json"><code>/api/body-index.json</code></a>'
        '</div>'
    )
    parts.append('</div></body></html>')
    return head + '\n'.join(parts)


def update_sitemap(slug_map: dict) -> None:
    """Add /addresses/{slug}/ URLs to sitemap.xml, replacing prior address URLs."""
    if not SITEMAP.exists():
        print(f"  ! sitemap not found at {SITEMAP}")
        return
    txt = SITEMAP.read_text(encoding="utf-8")

    # Remove any existing per-address URL entries (avoid duplicates on re-run)
    # Keep only /addresses/ index; strip /addresses/{anything else}/
    txt = re.sub(
        r"[ \t]*<url><loc>https://alexanarch\.org/addresses/[^<]+/</loc>[^<]*(?:<[^>]+>[^<]*)*</url>\n?",
        "",
        txt,
    )

    # Inject new URLs immediately after the /addresses/ line
    addr_index_re = re.compile(
        r"(<url><loc>https://alexanarch\.org/addresses/</loc>[^<]*(?:<[^>]+>[^<]*)*</url>)"
    )
    m = addr_index_re.search(txt)
    if not m:
        # Fallback: append before </urlset>
        insertion_point = txt.rfind("</urlset>")
        header = txt[:insertion_point]
        tail = txt[insertion_point:]
    else:
        header = txt[:m.end()]
        tail = txt[m.end():]

    lines = []
    for slug in sorted(set(slug_map.values())):
        lines.append(
            f'  <url><loc>https://alexanarch.org/addresses/{slug}/</loc>'
            f'<changefreq>weekly</changefreq><priority>0.6</priority></url>'
        )
    injection = "\n" + "\n".join(lines) + "\n"

    new_txt = header + injection + tail
    SITEMAP.write_text(new_txt, encoding="utf-8")
    print(f"  ✓ sitemap.xml updated: {len(slug_map)} address URLs")


def main() -> int:
    print("Loading data...")
    addresses = json.loads(ADDR_JSON.read_text())["addresses"]
    body_index = json.loads(BODY_INDEX.read_text()) if BODY_INDEX.exists() else {"index": {}}
    reg = json.loads(REGISTRY.read_text())
    registry_map = {d["deposit_number"]: d for d in reg.get("deposits", [])}
    print(f"  {len(addresses):,} addresses, {len(registry_map):,} deposits in registry")

    print("Computing slugs (with collision resolution)...")
    slug_map = resolve_collisions(addresses)
    print(f"  {len(set(slug_map.values())):,} unique slugs")

    print("Rendering address pages...")
    ADDR_DIR.mkdir(exist_ok=True)
    n_written = 0
    n_with_related = 0
    for k, v in addresses.items():
        slug = slug_map[k]
        page_dir = ADDR_DIR / slug
        page_dir.mkdir(exist_ok=True)
        query = v.get("canonical_query", "")
        related = find_related_deposits(query, body_index)
        if related:
            n_with_related += 1
        html_text = render_address_page(slug, v, related, registry_map)
        (page_dir / "index.html").write_text(html_text, encoding="utf-8")
        n_written += 1
        if n_written % 500 == 0:
            print(f"  {n_written}/{len(addresses)} written")

    print(f"  ✓ {n_written} address pages written")
    print(f"  {n_with_related} addresses have deposit cross-references from body-index")

    print("Rebuilding /addresses/index.html...")
    idx_html = render_index_page(addresses, slug_map)
    (ADDR_DIR / "index.html").write_text(idx_html, encoding="utf-8")
    print(f"  ✓ addresses/index.html ({len(idx_html):,} bytes)")

    print("Updating sitemap.xml...")
    update_sitemap(slug_map)

    return 0


if __name__ == "__main__":
    sys.exit(main())
