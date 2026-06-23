#!/usr/bin/env python3
"""
regenerate_surfaces.py — bring every derived surface into agreement with data/registry.json.

═══════════════════════════════════════════════════════════════════════════════
THE PROBLEM THIS SCRIPT SOLVES
═══════════════════════════════════════════════════════════════════════════════

data/registry.json is the canonical source of truth for all deposits.
But Alexanarch serves the archive through MANY derived surfaces, and if any
of them goes stale relative to registry.json the archive is internally
inconsistent — a deposit can exist in the registry but be invisible to anyone
browsing the site.

The derived surfaces are:

  1. s/browse/index.html           — static browse page (every deposit, no JS)
  2. data/browse-index.json        — compact JSON of all deposits (used by tools)
  3. data/chunks/registry/*.json   — 1MB-targeted chunks for streaming
  4. data/chunks/registry/_index.json — chunk catalog metadata
  5. sitemap.xml                   — XML sitemap for crawlers
  6. SHA256SUMS.txt                — content-addressable checksums

The mint-axn.yml workflow handles registry + record pages + deposits/*.md,
but does NOT touch ANY of the six derived surfaces above. The result is
that any deposit minted through the auto-flow leaves the archive in an
inconsistent state until someone runs this script.

THE FIX: run this script after EVERY change to data/registry.json.

═══════════════════════════════════════════════════════════════════════════════
USAGE
═══════════════════════════════════════════════════════════════════════════════

    python3 scripts/regenerate_surfaces.py                # regenerate all surfaces
    python3 scripts/regenerate_surfaces.py --dry-run      # show what would change
    python3 scripts/regenerate_surfaces.py --only browse  # only browse page
    python3 scripts/regenerate_surfaces.py --only browse,chunks  # subset

Available surfaces: browse, browse-index, chunks, sitemap, sha256sums

After running this script the archive is internally consistent.
The script is idempotent — running it twice produces the same result.

═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "data" / "registry.json"

# Pre-overwrite receipt mechanism (workplan item 8.13).
# Each regenerator write logs an auto-receipt to data/pre-overwrite-receipts.log
# so the audit trail captures EVERY surface-overwrite event, regardless of
# whether the write came from an instance or from the regenerator. The
# receipt log is the structural complement to the discipline of running
# scripts/pre_overwrite.py before any ad-hoc edit.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from overwrite_guard import issue_auto_receipt
    _OVERWRITE_GUARD_AVAILABLE = True
except ImportError:
    _OVERWRITE_GUARD_AVAILABLE = False

ALL_SURFACES = ["browse", "browse-index", "chunks", "sitemap", "sha256sums", "wiki", "graph"]


def _receipt(path, reason: str = "regenerate_surfaces write"):
    """Issue an auto-receipt for a regenerator write. No-op if guard module
    isn't importable (defensive — the script should still work even if the
    guard module is missing or temporarily broken)."""
    if not _OVERWRITE_GUARD_AVAILABLE:
        return
    try:
        issue_auto_receipt(path, actor="regenerate_surfaces", reason=reason,
                           instance_id=os.environ.get("ALEXANARCH_INSTANCE_ID", "regenerator"))
    except Exception as e:
        # Don't let receipt failure block a regenerator run; log and continue.
        print(f"[regenerate_surfaces] warning: receipt failed for {path}: {e}", file=sys.stderr)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def esc_html(s):
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def esc_xml(s):
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("'", "&apos;")
            .replace('"', "&quot;"))


# ──────────────────────────────────────────────────────────────────────────────
# Surface 1: s/browse/index.html
# ──────────────────────────────────────────────────────────────────────────────

BROWSE_HEADER = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Browse — Alexanarch ({total} deposits)</title>
<meta name="description" content="Complete registry of {total} deposits in the Alexanarch self-governing library.">
<script type="application/ld+json">{jsonld}</script>
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--teal:#0a7c6a;--border:#e0e0e0;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.6;font-size:15px}}.wrap{{max-width:720px;margin:0 auto;padding:60px 24px}}a:hover{{background:#f8f8ff}}.nav{{display:flex;gap:12px;margin-bottom:20px;font-size:.85em;overflow-x:auto;white-space:nowrap}}.nav a{{color:#777;font-weight:500;text-decoration:none}}.nav a:hover{{color:var(--accent);background:none}}.footer{{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:#777}}</style>
</head><body><div class="wrap">
<nav class="nav"><a href="/">Alexanarch</a> <a href="/deposit/">Deposit</a> <a href="/s/wiki/">Wiki</a> <a href="/s/graph/">Graph</a> <a href="/guide/">Guide</a> <a href="/manifest/">Manifest</a></nav>
<h1 style="font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:4px">Complete Deposit Registry</h1>
<div style="color:#777;font-size:.88em;margin-bottom:16px">{total} deposits · sorted by deposit number, oldest first · for newest see <a href="/">home page</a></div>
"""

BROWSE_CARD = """<a href="/s/records/{n}/" itemscope itemtype="https://schema.org/CreativeWork" style="display:block;padding:6px 0;border-bottom:1px solid #f0f0f0;text-decoration:none;color:var(--fg)">
<div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">
<span style="font-family:var(--mono);font-size:.72em;color:var(--teal);min-width:40px">#{n}</span>
<span itemprop="name" style="font-weight:500;color:var(--accent);font-size:.9em;flex:1">{title}</span>
<time itemprop="datePublished" datetime="{date}" style="font-size:.72em;color:#999;white-space:nowrap">{date}</time>
</div>
<div style="font-size:.7em;color:#aaa;margin-top:1px;padding-left:48px"><code itemprop="identifier">{axn}</code></div>
</a>
"""

BROWSE_FOOTER = """
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<div class="footer"><strong>Alexanarch</strong><div style="margin-top:5px;color:var(--accent)">∮ = 1</div></div></div></body></html>"""


def regenerate_browse(reg, dry_run=False):
    """Rebuild s/browse/index.html — the canonical static browse surface.

    Sort order: ascending by deposit_number (#1 first). This matches the
    existing convention. Most-recent deposits appear at the bottom of the page;
    use the home page Recent Deposits section to see newest-first.
    """
    deposits = reg["deposits"]
    total = len(deposits)
    sorted_deps = sorted(
        deposits,
        key=lambda d: d.get("deposit_number") or d.get("issue_number") or 0,
    )

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "@id": "https://alexanarch.org/s/browse/",
        "name": "Alexanarch — Complete Deposit Registry",
        "description": f"Self-governing library for machine-mediated scholarship. {total} deposits with content-derived AXN identifiers.",
        "url": "https://alexanarch.org/s/browse/",
        "creator": {
            "@type": "Person",
            "name": "Lee Sharks",
            "identifier": "https://orcid.org/0009-0000-1599-0703",
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "numberOfItems": total,
    })

    parts = [BROWSE_HEADER.format(total=total, jsonld=jsonld)]
    for d in sorted_deps:
        n = d.get("deposit_number") or d.get("issue_number") or 0
        if n == 0:
            continue
        parts.append(BROWSE_CARD.format(
            n=n,
            title=esc_html(d.get("title", "(untitled)")),
            date=esc_html(d.get("date", "")),
            axn=esc_html(d.get("axn", "")),
        ))
    parts.append(BROWSE_FOOTER)

    out = "".join(parts)
    target = REPO_ROOT / "s" / "browse" / "index.html"
    if dry_run:
        print(f"  [DRY] would write {target} ({len(out):,} bytes, {total} deposits)")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    _receipt(target)
    with open(target, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ s/browse/index.html ({len(out):,} bytes, {total} deposits)")


# ──────────────────────────────────────────────────────────────────────────────
# Surface 2: data/browse-index.json
# ──────────────────────────────────────────────────────────────────────────────

def regenerate_browse_index(reg, dry_run=False):
    """Rebuild data/browse-index.json — compact deposit list for tools."""
    deposits = reg["deposits"]
    out = {
        "total": len(deposits),
        "deposits": [],
    }
    for d in sorted(deposits, key=lambda x: x.get("deposit_number") or x.get("issue_number") or 0):
        n = d.get("deposit_number") or d.get("issue_number") or 0
        if n == 0:
            continue
        # Compact schema preserves existing format: n/a/t/c/d/f/s/y
        desc = d.get("description", "") or ""
        snippet = desc[:200]
        if len(desc) > 200:
            snippet += "..."
        out["deposits"].append({
            "n": n,
            "a": d.get("axn", ""),
            "t": d.get("title", ""),
            "c": d.get("creator", ""),
            "d": d.get("date", ""),
            "f": d.get("download_md") or d.get("full_text_path") or f"/data/texts/AXN-{d.get('hex','')}-text.md",
            "s": snippet,
            "y": d.get("content_type", ""),
        })

    target = REPO_ROOT / "data" / "browse-index.json"
    payload = json.dumps(out, ensure_ascii=False, indent=2)
    if dry_run:
        print(f"  [DRY] would write {target} ({len(payload):,} bytes)")
        return
    _receipt(target)
    with open(target, "w", encoding="utf-8") as f:
        f.write(payload)
    print(f"  ✓ data/browse-index.json ({len(payload):,} bytes, {len(out['deposits'])} deposits)")


# ──────────────────────────────────────────────────────────────────────────────
# Surface 3 + 4: data/chunks/registry/*.json + _index.json
# ──────────────────────────────────────────────────────────────────────────────

def regenerate_chunks(reg, dry_run=False, chunk_target_bytes=1_000_000):
    """
    Rebuild data/chunks/registry/chunk-NNN-deposits-X-to-Y.json + _index.json.

    The chunking strategy: walk deposits in deposit_number order; greedily fill
    each chunk until adding the next deposit would exceed chunk_target_bytes;
    then close the chunk and start a new one. Existing chunk file names use
    the actual first/last deposit numbers they contain.
    """
    deposits = sorted(
        reg["deposits"],
        key=lambda d: d.get("deposit_number") or d.get("issue_number") or 0,
    )
    deposits = [d for d in deposits if (d.get("deposit_number") or d.get("issue_number"))]

    chunks_dir = REPO_ROOT / "data" / "chunks" / "registry"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    chunks = []
    current = []
    chunk_num = 1

    def serialize_chunk(deps_in_chunk, num):
        """Return (chunk_obj, serialized_bytes) for a candidate chunk."""
        first = deps_in_chunk[0].get("deposit_number") or deps_in_chunk[0].get("issue_number")
        last = deps_in_chunk[-1].get("deposit_number") or deps_in_chunk[-1].get("issue_number")
        obj = {
            "chunk_number": num,
            "first_deposit": first,
            "last_deposit": last,
            "count": len(deps_in_chunk),
            "deposits": deps_in_chunk,
        }
        payload = json.dumps(obj, ensure_ascii=False, indent=2)
        return obj, payload

    def flush(deps_in_chunk, num):
        obj, payload = serialize_chunk(deps_in_chunk, num)
        first, last = obj["first_deposit"], obj["last_deposit"]
        path = chunks_dir / f"chunk-{num:03d}-deposits-{first}-to-{last}.json"
        if dry_run:
            print(f"  [DRY] would write {path.name} (#{first}-#{last}, {len(payload):,} bytes)")
        else:
            _receipt(path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(payload)
        return {
            "chunk_number": num,
            "path": str(path.relative_to(REPO_ROOT)),
            "first_deposit": first,
            "last_deposit": last,
            "count": len(deps_in_chunk),
            "size_bytes": len(payload.encode("utf-8")),
        }

    # Remove existing chunk files (recreate fresh from current registry)
    if not dry_run:
        for f in chunks_dir.glob("chunk-*.json"):
            f.unlink()

    for d in deposits:
        # Measure exact size of chunk if we added this deposit
        _, candidate_payload = serialize_chunk(current + [d], chunk_num)
        if current and len(candidate_payload.encode("utf-8")) > chunk_target_bytes:
            chunks.append(flush(current, chunk_num))
            chunk_num += 1
            current = []
        current.append(d)

    if current:
        chunks.append(flush(current, chunk_num))

    index_obj = {
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "name": "Alexanarch Registry — Chunked",
        "chunk_target_bytes": chunk_target_bytes,
        "total_chunks": len(chunks),
        "total_deposits": len(deposits),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "chunks": chunks,
    }
    index_path = chunks_dir / "_index.json"
    payload = json.dumps(index_obj, indent=4)
    if dry_run:
        print(f"  [DRY] would write {index_path} ({len(chunks)} chunks, {len(deposits)} deposits)")
    else:
        _receipt(index_path)
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"  ✓ data/chunks/registry/ ({len(chunks)} chunks, {len(deposits)} deposits)")


# ──────────────────────────────────────────────────────────────────────────────
# Surface 5: sitemap.xml
# ──────────────────────────────────────────────────────────────────────────────

# Static (non-deposit) URLs the sitemap must always include
STATIC_URLS = [
    ("https://alexanarch.org/", 1.0),
    ("https://alexanarch.org/deposit/", 0.8),
    ("https://alexanarch.org/browse/", 0.8),
    ("https://alexanarch.org/principles/", 0.8),
    ("https://alexanarch.org/identifiers/", 0.8),
    ("https://alexanarch.org/wiki/", 0.8),
    ("https://alexanarch.org/graph/", 0.8),
    ("https://alexanarch.org/guide/", 0.8),
    ("https://alexanarch.org/manifest/", 0.8),
    ("https://alexanarch.org/s/browse/", 0.7),
    ("https://alexanarch.org/s/wiki/", 0.6),
    ("https://alexanarch.org/s/graph/", 0.6),
    ("https://alexanarch.org/data/registry.json", 0.5),
    ("https://alexanarch.org/data/doi-resolution-index.json", 0.5),
    ("https://alexanarch.org/data/batch-axn-assignment.json", 0.5),
    ("https://alexanarch.org/api/deposit-schema.json", 0.5),
    ("https://alexanarch.org/AGENTS.md", 0.5),
    ("https://alexanarch.org/DEPOSIT-FLOW.md", 0.5),
]


def regenerate_sitemap(reg, dry_run=False):
    """Rebuild sitemap.xml — every static URL + every deposit record page."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, priority in STATIC_URLS:
        lines.append(f'  <url><loc>{esc_xml(url)}</loc><lastmod>{today}</lastmod><priority>{priority}</priority></url>')

    deposits = sorted(
        reg["deposits"],
        key=lambda d: d.get("deposit_number") or d.get("issue_number") or 0,
    )
    for d in deposits:
        n = d.get("deposit_number") or d.get("issue_number")
        if not n:
            continue
        last = esc_xml(d.get("date") or today)
        lines.append(
            f'  <url><loc>https://alexanarch.org/s/records/{n}/</loc>'
            f'<lastmod>{last}</lastmod><priority>0.6</priority></url>'
        )
    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"

    target = REPO_ROOT / "sitemap.xml"
    if dry_run:
        print(f"  [DRY] would write {target} ({len(out):,} bytes, {len(deposits)} deposit URLs)")
        return
    _receipt(target)
    with open(target, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ sitemap.xml ({len(out):,} bytes, {len(deposits)} deposit URLs)")


# ──────────────────────────────────────────────────────────────────────────────
# Surface 6: SHA256SUMS.txt
# ──────────────────────────────────────────────────────────────────────────────

def regenerate_sha256sums(reg, dry_run=False):
    """Rebuild SHA256SUMS.txt — one line per deposit with hash + AXN-hex + title."""
    deposits = reg["deposits"]
    lines = []
    for d in deposits:
        h = d.get("hash") or d.get("content_sha256")
        if not h:
            continue
        hex_id = d.get("hex", "")
        title = (d.get("title") or "").strip()
        # The conventional format is: <sha>  AXN-<hex> <title>
        lines.append(f"{h}  AXN-{hex_id} {title}")

    lines.sort()
    out = "\n".join(lines) + "\n"

    target = REPO_ROOT / "SHA256SUMS.txt"
    if dry_run:
        print(f"  [DRY] would write {target} ({len(lines)} lines, {len(out):,} bytes)")
        return
    _receipt(target)
    with open(target, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ SHA256SUMS.txt ({len(lines)} lines, {len(out):,} bytes)")


# ──────────────────────────────────────────────────────────────────────────────
# Wiki tab — project /s/wiki/index.html from registry wiki_article + entity-index
# ──────────────────────────────────────────────────────────────────────────────

WIKI_PATH = REPO_ROOT / "s" / "wiki" / "index.html"
ENTITY_INDEX_PATH = REPO_ROOT / "data" / "entity-index.json"


def _load_entity_index():
    """Load entity-index.json if present, else return None."""
    if not ENTITY_INDEX_PATH.exists():
        return None
    with open(ENTITY_INDEX_PATH) as f:
        return json.load(f)


def regenerate_wiki(reg, dry_run=False):
    """Project the wiki tab from registry wiki_article fields + entity-index backlinks.

    Each deposit with a non-empty wiki_article becomes a wiki entry. Entries
    show: canonical v2 AXN, title, creator, date, wiki_article body,
    "Defines:" (from defines_concepts or registry-listed entities), and
    "Referenced by N deposits" link to the deposit's record page.
    """
    eidx = _load_entity_index()
    concepts = (eidx or {}).get("concepts", {}) if eidx else {}

    # Entries to render: deposits that have wiki_article populated.
    # Sort by deposit_number ascending so the wiki reads in canonical order.
    entries = []
    for d in sorted(reg["deposits"], key=lambda x: x.get("deposit_number", 0)):
        wiki_article = d.get("wiki_article") or ""
        if not wiki_article.strip():
            continue
        entries.append(d)

    # Concepts defined per deposit (collected from entity-index, since registry
    # may not always carry defines_concepts).
    defines_by_deposit = {}
    for term, c in concepts.items():
        di = c.get("defined_in")
        if di is None:
            continue
        defines_by_deposit.setdefault(di, []).append(term)

    parts = []
    parts.append(_WIKI_HTML_HEAD)

    parts.append(f'<p style="font-size:0.86em;color:var(--dim);margin-bottom:18px">'
                 f'Wiki entries auto-projected from <code>data/registry.json</code> '
                 f'<code>wiki_article</code> fields and back-linked to '
                 f'<code>data/entity-index.json</code>. '
                 f'<strong>{len(entries):,}</strong> entries from a corpus of '
                 f'<strong>{len(reg["deposits"]):,}</strong> deposits.</p>\n')

    for d in entries:
        dn = d["deposit_number"]
        axn = d.get("axn", "")
        title = esc_html(d.get("title", "(untitled)"))
        creator = esc_html(d.get("creator") or d.get("author") or "")
        date = esc_html(d.get("date", ""))
        article = esc_html((d.get("wiki_article") or "").strip())

        defines = defines_by_deposit.get(dn, []) or d.get("defines_concepts") or []
        defines_html = ""
        if defines:
            shown = sorted(defines)[:12]
            tail = f' <span style="color:var(--dim)">+{len(defines)-12} more</span>' if len(defines) > 12 else ""
            defines_html = ('<div style="margin-top:6px;font-size:.82em">'
                            '<strong style="color:var(--teal)">Defines:</strong> '
                            + ", ".join(esc_html(t) for t in shown) + tail + '</div>')

        # "Referenced by N other deposits" — count concepts defined by THIS deposit
        # that appear in other deposits' references_concepts.
        # Cheap version: count = sum of reference_counts across defines.
        refby_total = 0
        for t in defines:
            c = concepts.get(t)
            if c:
                refby_total += c.get("reference_count", 0)
        refby_html = ""
        if refby_total:
            refby_html = ('<div style="margin-top:4px;font-size:.78em;color:var(--dim)">'
                          f'Concepts defined here referenced across {refby_total} other-deposit citations.'
                          '</div>')

        parts.append(
            '<div style="margin-bottom:24px">'
            f'<div style="font-family:var(--mono);font-size:.82em;color:var(--teal);'
            f'background:#f0f8f6;display:inline-block;padding:3px 8px;border-radius:4px">'
            f'{esc_html(axn)}</div>'
            f'<h1 style="font-size:1.2em;margin-bottom:4px">'
            f'<a href="/s/records/{dn}/">{title}</a></h1>'
            f'<div style="font-size:.82em;color:var(--dim);margin-bottom:8px">'
            f'{creator}{" · " + date if creator and date else date}</div>'
            f'<div class="art">{article}</div>'
            f'{defines_html}'
            f'{refby_html}'
            f'<div style="margin-top:4px;font-size:.82em">'
            f'<a href="/s/records/{dn}/">Full record →</a></div>'
            '</div>\n'
        )

    parts.append(_WIKI_HTML_TAIL)

    html = "".join(parts)
    size = len(html.encode("utf-8"))
    if dry_run:
        print(f"  [dry-run] {WIKI_PATH} would be {size:,} bytes, {len(entries)} entries")
        return
    WIKI_PATH.parent.mkdir(parents=True, exist_ok=True)
    _receipt(WIKI_PATH)
    WIKI_PATH.write_text(html, encoding="utf-8")
    print(f"  ✓ s/wiki/index.html ({size:,} bytes, {len(entries)} wiki entries)")


# ──────────────────────────────────────────────────────────────────────────────
# Graph tab — project /s/graph/index.html from entity_triples + citation_graph
# ──────────────────────────────────────────────────────────────────────────────

GRAPH_PATH = REPO_ROOT / "s" / "graph" / "index.html"
CITATION_GRAPH_PATH = REPO_ROOT / "data" / "citation-graph.json"


def _load_citation_graph():
    if not CITATION_GRAPH_PATH.exists():
        return None
    with open(CITATION_GRAPH_PATH) as f:
        return json.load(f)


def regenerate_graph(reg, dry_run=False):
    """Project the graph tab from entity_triples + citation_graph.

    Renders subject→predicate→object triples in the same visual format the
    hand-curated graph used to use ([observed]/[inferred]/[performative]).
    Sourced from:
      - entity-index.json: each concept's entity_triples[] array
      - citation-graph.json: deposit→deposit edges become (deposit,
        cites, deposit) triples
    """
    eidx = _load_entity_index()
    citation_graph = _load_citation_graph()

    # Gather triples from entity_triples first
    concept_triples = []
    if eidx:
        for term, c in eidx.get("concepts", {}).items():
            for tr in (c.get("entity_triples") or [])[:3]:  # top 3 per concept to avoid explosion
                s = tr.get("subject") or term
                p = tr.get("predicate")
                o = tr.get("object")
                ev = tr.get("evidence_status") or "observed"
                if s and p and o:
                    concept_triples.append((s, p, o, ev))

    # Cap concept triples to keep page size reasonable
    concept_triples = concept_triples[:1500]

    # Gather deposit-to-deposit citation edges (cap to 500 for page size)
    deposit_triples = []
    if citation_graph:
        for e in (citation_graph.get("edges") or [])[:500]:
            src = e.get("source_axn") or f"#{e.get('source_deposit')}"
            tgt = e.get("target_axn") or f"#{e.get('target_deposit')}"
            via = e.get("via") or "cites"
            deposit_triples.append((src, via, tgt, "observed"))

    total_concept_edges = sum(len((c.get("entity_triples") or [])) for c in (eidx or {}).get("concepts", {}).values()) if eidx else 0
    total_citation_edges = len((citation_graph or {}).get("edges") or [])

    parts = []
    parts.append(_GRAPH_HTML_HEAD)

    parts.append(
        f'<p style="color:var(--dim);margin-bottom:8px">'
        f'<strong>{total_concept_edges + total_citation_edges:,}</strong> total edges '
        f'projected from <code>data/entity-index.json</code> '
        f'and <code>data/citation-graph.json</code>. '
        f'<span class="ev evo">[observed]</span> '
        f'<span class="ev evi">[inferred]</span> '
        f'<span class="ev evp">[performative]</span></p>\n'
    )

    if concept_triples:
        parts.append('<h2 style="font-size:1em;margin-top:18px;border-bottom:1px solid var(--border);padding-bottom:4px">'
                     f'Concept Relations <span style="color:var(--dim);font-weight:400;font-size:0.85em">'
                     f'(showing first {len(concept_triples):,} of {total_concept_edges:,})</span></h2>\n')
        for s, p, o, ev in concept_triples:
            cls = "evo" if ev == "observed" else "evi" if ev == "inferred" else "evp"
            parts.append(
                f'<div class="er">'
                f'<span class="es">{esc_html(s)}</span>'
                f'<span class="ep">{esc_html(p)}</span>'
                f'<span class="eo">{esc_html(o)} <span class="ev {cls}">[{esc_html(ev)}]</span></span>'
                f'</div>\n'
            )

    if deposit_triples:
        parts.append('<h2 style="font-size:1em;margin-top:24px;border-bottom:1px solid var(--border);padding-bottom:4px">'
                     f'Deposit Citation Edges <span style="color:var(--dim);font-weight:400;font-size:0.85em">'
                     f'(showing first {len(deposit_triples):,} of {total_citation_edges:,})</span></h2>\n')
        for s, p, o, ev in deposit_triples:
            parts.append(
                f'<div class="er">'
                f'<span class="es">{esc_html(s)}</span>'
                f'<span class="ep">{esc_html(p)}</span>'
                f'<span class="eo">{esc_html(o)} <span class="ev evo">[observed]</span></span>'
                f'</div>\n'
            )

    parts.append(_GRAPH_HTML_TAIL)

    html = "".join(parts)
    size = len(html.encode("utf-8"))
    if dry_run:
        print(f"  [dry-run] {GRAPH_PATH} would be {size:,} bytes, {len(concept_triples)+len(deposit_triples)} edges shown")
        return
    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    _receipt(GRAPH_PATH)
    GRAPH_PATH.write_text(html, encoding="utf-8")
    print(f"  ✓ s/graph/index.html ({size:,} bytes, {len(concept_triples)+len(deposit_triples)} edges)")


# HTML templates for wiki and graph — keep the existing visual style/classes
_WIKI_STYLE = """<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}*{margin:0;padding:0;box-sizing:border-box}body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}.wrap{max-width:720px;margin:0 auto;padding:60px 24px}a{color:var(--accent);text-decoration:none}a:hover{color:var(--accent2)}h1{font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:8px}h2{font-size:1em;font-weight:500;color:var(--accent);margin-top:20px;margin-bottom:6px;border-bottom:1px solid var(--border);padding-bottom:3px}h3{font-size:.9em;color:var(--teal);margin-top:14px}p{margin-bottom:10px;color:#333}.nav{display:flex;gap:16px;margin-bottom:24px;font-size:.85em;flex-wrap:wrap}.nav a{color:var(--dim);font-weight:500}.art{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px;line-height:1.9;color:#333;font-size:.93em;margin:8px 0;white-space:pre-wrap}.footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}.glyph{margin-top:5px;color:var(--accent)}</style>"""

_WIKI_HTML_HEAD = (
    '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
    '<title>Wiki — Alexanarch</title>'
    + _WIKI_STYLE +
    '</head><body><div class="wrap">'
    '<nav class="nav"><a href="/">Alexanarch</a> <a href="/s/browse/">Browse</a> '
    '<a href="/s/wiki/">Wiki</a> <a href="/s/graph/">Graph</a> '
    '<a href="/deposit/">Deposit</a> <a href="/manifest/">Manifest</a></nav>'
    '<h1>Alexanarch Wiki</h1>'
)

_WIKI_HTML_TAIL = (
    '<div class="footer"><strong>Alexanarch</strong> · '
    '<a href="https://orcid.org/0009-0000-1599-0703">ORCID</a>'
    '<div class="glyph">∮ = 1</div></div>'
    '</div>'
    '<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    '</body></html>\n'
)

_GRAPH_STYLE = """<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}*{margin:0;padding:0;box-sizing:border-box}body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}.wrap{max-width:720px;margin:0 auto;padding:60px 24px}a{color:var(--accent);text-decoration:none}a:hover{color:var(--accent2)}h1{font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:8px}.nav{display:flex;gap:16px;margin-bottom:24px;font-size:.85em;flex-wrap:wrap}.nav a{color:var(--dim);font-weight:500}.er{display:flex;gap:6px;padding:2px 0;font-size:.82em;border-bottom:1px solid #f8f8f8;flex-wrap:wrap}.es{font-weight:500;color:var(--accent);min-width:140px}.ep{color:var(--teal);font-family:var(--mono);font-size:.8em;min-width:80px}.eo{color:#444}.ev{font-size:.65em;font-family:var(--mono);margin-left:3px}.evo{color:var(--teal)}.evi{color:#d4a537}.evp{color:#9966cc}.footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}.glyph{margin-top:5px;color:var(--accent)}</style>"""

_GRAPH_HTML_HEAD = (
    '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
    '<title>Knowledge Graph — Alexanarch</title>'
    + _GRAPH_STYLE +
    '</head><body><div class="wrap">'
    '<nav class="nav"><a href="/">Alexanarch</a> <a href="/s/browse/">Browse</a> '
    '<a href="/s/wiki/">Wiki</a> <a href="/s/graph/">Graph</a> '
    '<a href="/deposit/">Deposit</a> <a href="/manifest/">Manifest</a></nav>'
    '<h1>Knowledge Graph</h1>'
)

_GRAPH_HTML_TAIL = (
    '<div class="footer"><strong>Alexanarch</strong> · '
    '<a href="https://orcid.org/0009-0000-1599-0703">ORCID</a>'
    '<div class="glyph">∮ = 1</div></div>'
    '</div>'
    '<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    '</body></html>\n'
)


# ──────────────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────────────

SURFACE_FNS = {
    "browse": regenerate_browse,
    "browse-index": regenerate_browse_index,
    "chunks": regenerate_chunks,
    "sitemap": regenerate_sitemap,
    "sha256sums": regenerate_sha256sums,
    "wiki": regenerate_wiki,
    "graph": regenerate_graph,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="show what would change without writing")
    parser.add_argument("--only", default=None,
                        help=f"comma-separated subset of surfaces to regenerate. options: {','.join(ALL_SURFACES)}")
    args = parser.parse_args()

    if args.only:
        surfaces = [s.strip() for s in args.only.split(",")]
        for s in surfaces:
            if s not in SURFACE_FNS:
                print(f"unknown surface: {s}", file=sys.stderr)
                sys.exit(2)
    else:
        surfaces = ALL_SURFACES

    reg = load_registry()
    n_deposits = len(reg["deposits"])
    print(f"Registry: {n_deposits} deposits (total_deposits field: {reg.get('total_deposits')})")
    if n_deposits != reg.get("total_deposits"):
        print(f"  ⚠ total_deposits field mismatch — will be corrected indirectly by chunks index")

    print(f"Regenerating {len(surfaces)} surface(s){' [DRY RUN]' if args.dry_run else ''}:")
    for s in surfaces:
        SURFACE_FNS[s](reg, dry_run=args.dry_run)

    print("Done." if not args.dry_run else "Dry run complete — no files written.")


if __name__ == "__main__":
    main()
