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

# Import canonical navbar renderer
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.render_navbar import render_navbar

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

ALL_SURFACES = ["state", "browse", "browse-index", "chunks", "sitemap", "sha256sums", "wiki", "graph", "homepage-noscript", "api-index"]


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
<nav class="nav">__NAVBAR_TOKEN__</nav>
<h1 style="font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:4px">Complete Deposit Registry</h1>
<div style="color:#777;font-size:.88em;margin-bottom:16px">{total} deposits · sorted by deposit number, oldest first · for newest see <a href="/">home page</a></div>
"""

BROWSE_CARD = """<a href="/s/records/{n}/" itemscope itemtype="https://schema.org/CreativeWork" style="display:block;padding:6px 0;border-bottom:1px solid #f0f0f0;text-decoration:none;color:var(--fg){card_opacity}">
<div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap">
<span style="font-family:var(--mono);font-size:.72em;color:var(--teal);min-width:40px">#{n}</span>
<span itemprop="name" style="font-weight:500;color:var(--accent);font-size:.9em;flex:1">{title}{version_chip}</span>
<time itemprop="datePublished" datetime="{date}" style="font-size:.72em;color:#999;white-space:nowrap">{date}</time>
</div>
<div style="font-size:.7em;color:#aaa;margin-top:1px;padding-left:48px"><code itemprop="identifier">{axn}</code>{status_badge}</div>
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

    parts = [BROWSE_HEADER.format(total=total, jsonld=jsonld).replace('__NAVBAR_TOKEN__', render_navbar()[len('<nav class="nav">'):-len('</nav>')])]
    for d in sorted_deps:
        n = d.get("deposit_number") or d.get("issue_number") or 0
        if n == 0:
            continue
        # Version / status chips
        version = d.get("version", "")
        status = d.get("status", "ACTIVE")
        superseded_by_n = d.get("superseded_by_deposit_number")
        in_real_series = bool(d.get("version_series_id"))
        version_chip = ''
        if version and (version != 'v1.0' or in_real_series):
            version_chip = f' <span style="font-family:var(--mono);font-size:.78em;color:var(--teal);font-weight:500;background:#f0f4f8;padding:1px 6px;border-radius:8px;margin-left:4px">{esc_html(version)}</span>'
        status_badge = ''
        card_opacity = ''
        if status == 'SUPERSEDED' and superseded_by_n:
            status_badge = f' · <span style="color:#92400e;font-size:.85em">superseded by <a href="/s/records/{superseded_by_n}/" style="color:#92400e;text-decoration:underline">#{superseded_by_n}</a></span>'
            card_opacity = ';opacity:.65'
        elif status == 'DRAFT_PENDING':
            status_badge = ' · <span style="color:#6b7280;font-size:.85em;font-style:italic">draft pending</span>'
            card_opacity = ';opacity:.65'
        parts.append(BROWSE_CARD.format(
            n=n,
            title=esc_html(d.get("title", "(untitled)")),
            date=esc_html(d.get("date", "")),
            axn=esc_html(d.get("axn", "")),
            version_chip=version_chip,
            status_badge=status_badge,
            card_opacity=card_opacity,
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
        payload_bytes = payload.encode("utf-8")
        chunk_sha = hashlib.sha256(payload_bytes).hexdigest()
        if dry_run:
            print(f"  [DRY] would write {path.name} (#{first}-#{last}, {len(payload):,} bytes, sha256 {chunk_sha[:16]}…)")
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
            "size_bytes": len(payload_bytes),
            "sha256": chunk_sha,
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
    # Core
    ("https://alexanarch.org/", 1.0),
    ("https://alexanarch.org/deposit/", 0.8),
    ("https://alexanarch.org/guide/", 0.8),
    ("https://alexanarch.org/manifest/", 0.8),
    ("https://alexanarch.org/principles/", 0.8),
    ("https://alexanarch.org/identifiers/", 0.8),
    # Discovery surfaces (the 7 the audit flagged as missing)
    ("https://alexanarch.org/observatory/", 0.9),
    ("https://alexanarch.org/lexical/", 0.8),
    ("https://alexanarch.org/citations/", 0.8),
    ("https://alexanarch.org/captures/", 0.8),
    ("https://alexanarch.org/addresses/", 0.7),
    ("https://alexanarch.org/resolve/", 0.7),
    ("https://alexanarch.org/datasets/", 0.7),
    # Generated surfaces
    ("https://alexanarch.org/s/browse/", 0.7),
    ("https://alexanarch.org/s/wiki/", 0.6),
    ("https://alexanarch.org/s/graph/", 0.6),
    # Canonical data
    ("https://alexanarch.org/data/registry.json", 0.5),
    ("https://alexanarch.org/data/state.json", 0.6),
    ("https://alexanarch.org/data/navigation.json", 0.4),
    ("https://alexanarch.org/data/doi-resolution-index.json", 0.5),
    ("https://alexanarch.org/data/batch-axn-assignment.json", 0.4),
    ("https://alexanarch.org/data/chunks/registry/_index.json", 0.4),
    # Protocols
    ("https://alexanarch.org/api/index.json", 0.6),
    ("https://alexanarch.org/api/deposit-protocol.json", 0.5),
    ("https://alexanarch.org/api/deposit-schema.json", 0.5),
    ("https://alexanarch.org/api/axn-protocol.json", 0.5),
    ("https://alexanarch.org/api/enrichment-protocol.json", 0.4),
    ("https://alexanarch.org/api/lifecycle-protocol.json", 0.5),
    # Documents
    ("https://alexanarch.org/AGENTS.md", 0.4),
    ("https://alexanarch.org/DEPOSIT-FLOW.md", 0.4),
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
    """Rebuild two complementary integrity manifests.

    The audit (§16) correctly noted that the historical SHA256SUMS.txt used
    semantic labels rather than file paths, which standard verification tools
    can't use. Fix: emit two files.

    1. SHA256SUMS.txt — real-file-path manifest in `sha256sum -c` format.
       Lists data/texts/AXN-NNNN-text.md paths with the actual sha256 of the
       file bytes. Standard tools verify byte integrity directly.

    2. RECORD-SHA256-MANIFEST.txt — semantic-label manifest (the old format,
       kept under a clearer name). Lists registry-declared content hashes
       against AXN identities. Useful for verifying that a deposit's
       registry-declared hash matches what was minted.

    Both regenerate together; the audit's complaint is closed by having
    real-file checksums alongside the semantic ones.
    """
    deposits = reg["deposits"]

    # SHA256SUMS.txt — real file paths, hashes computed from disk
    file_lines = []
    semantic_lines = []
    for d in deposits:
        hex_id = d.get("hex", "")
        title = (d.get("title") or "").strip()

        # Semantic manifest
        h = d.get("hash") or d.get("content_sha256")
        if h:
            semantic_lines.append(f"{h}  AXN-{hex_id} {title}")

        # Real-file manifest — only for deposits that have an on-disk text file
        text_rel = f"data/texts/AXN-{hex_id}-text.md"
        text_path = REPO_ROOT / text_rel
        if text_path.exists():
            try:
                file_h = hashlib.sha256(text_path.read_bytes()).hexdigest()
                file_lines.append(f"{file_h}  {text_rel}")
            except Exception:
                pass

    file_lines.sort()
    semantic_lines.sort()
    file_out = "\n".join(file_lines) + "\n"
    semantic_out = "\n".join(semantic_lines) + "\n"

    sha_target = REPO_ROOT / "SHA256SUMS.txt"
    rec_target = REPO_ROOT / "RECORD-SHA256-MANIFEST.txt"

    if dry_run:
        print(f"  [DRY] would write {sha_target} ({len(file_lines)} file lines, {len(file_out):,} bytes)")
        print(f"  [DRY] would write {rec_target} ({len(semantic_lines)} record lines, {len(semantic_out):,} bytes)")
        return

    _receipt(sha_target)
    with open(sha_target, "w", encoding="utf-8") as f:
        f.write(file_out)
    print(f"  ✓ SHA256SUMS.txt ({len(file_lines)} file lines, real paths, sha256sum -c verifiable)")

    _receipt(rec_target)
    with open(rec_target, "w", encoding="utf-8") as f:
        f.write(semantic_out)
    print(f"  ✓ RECORD-SHA256-MANIFEST.txt ({len(semantic_lines)} record lines, semantic AXN→hash mapping)")


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
    """Regenerate the wiki surface as a paginated single page.

    Architecture mirrors /addresses/: one HTML file, fetches a flat JSON,
    JS paginates 25 entries per page with search. The previous chunked URL
    layout (/s/wiki/chunk-NNN-deposits-X-to-Y/) is removed -- those URLs
    exposed repository internals to readers who only want to see wikis.

    Outputs:
      data/wiki-entries.json  -- flat array consumed by JS; also a
                                 machine-readable wiki dataset
      s/wiki/index.html       -- single-page paginated view
    """
    eidx = _load_entity_index()
    concepts = (eidx or {}).get("concepts", {}) if eidx else {}

    entries = []
    for d in sorted(reg["deposits"], key=lambda x: x.get("deposit_number", 0)):
        wiki_article = (d.get("wiki_article") or "").strip()
        if not wiki_article:
            continue
        entries.append(d)

    defines_by_deposit = {}
    for term, c in concepts.items():
        di = c.get("defined_in")
        if di is None:
            continue
        defines_by_deposit.setdefault(di, []).append(term)

    flat = []
    for d in entries:
        dn = d["deposit_number"]
        defines = sorted(defines_by_deposit.get(dn, []) or d.get("defines_concepts") or [])
        refby_total = sum(concepts.get(t, {}).get("reference_count", 0) for t in defines)
        flat.append({
            "n": dn,
            "axn": d.get("axn", ""),
            "title": d.get("title") or "(untitled)",
            "creator": d.get("creator") or d.get("author") or "",
            "date": d.get("date", ""),
            "wiki": (d.get("wiki_article") or "").strip(),
            "defines": defines,
            "refby_total": refby_total,
        })

    json_payload = {
        "schema_version": "v1.0",
        "purpose": "Flat wiki-entries dataset projected from data/registry.json wiki_article fields and back-linked to data/entity-index.json. Source for /s/wiki/ paginated view; also a machine-readable wiki dataset.",
        "count": len(flat),
        "corpus_size": len(reg["deposits"]),
        "entries": flat,
    }
    json_str = json.dumps(json_payload, ensure_ascii=False, indent=None, separators=(",", ":"))

    # Static header + page-content prefix
    body_pre = (
        f'<p style="font-size:0.86em;color:var(--dim);margin-bottom:18px">'
        f'Wiki entries auto-projected from <code>data/registry.json</code> '
        f'<code>wiki_article</code> fields and back-linked to '
        f'<code>data/entity-index.json</code>. '
        f'<strong>{len(flat):,}</strong> entries from a corpus of '
        f'<strong>{len(reg["deposits"]):,}</strong> deposits. '
        f'Read from <a href="/data/wiki-entries.json"><code>data/wiki-entries.json</code></a>.'
        f'</p>\n'
        f'<input type="search" id="search" placeholder="Search title, creator, or wiki text..." '
        f'style="width:100%;padding:10px 12px;font-size:.95em;border:1px solid var(--border);'
        f'border-radius:6px;font-family:var(--sans);background:var(--surface);margin-bottom:16px">\n'
        f'<div class="pager" id="pager-top"></div>\n'
        f'<div id="entries">Loading...</div>\n'
        f'<div class="pager" id="pager-bot"></div>\n'
    )

    # JS pagination — clean raw triple-string, no Python-string escape gymnastics
    js = r"""<script>
fetch("/data/wiki-entries.json").then(function(r){return r.json()}).then(function(data){
  var pageSize = 25;
  var page = 0;
  var query = "";
  var pool = data.entries || [];
  var ESC_MAP = {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"};
  function esc(s){ return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){ return ESC_MAP[c]; }); }
  function nl2br(s){ return esc(s).replace(/\n/g, "<br>"); }

  function filtered(){
    if(!query) return pool;
    var q = query.toLowerCase();
    return pool.filter(function(e){
      return (e.title || "").toLowerCase().indexOf(q) >= 0
          || (e.creator || "").toLowerCase().indexOf(q) >= 0
          || (e.wiki || "").toLowerCase().indexOf(q) >= 0
          || (e.defines || []).join(" ").toLowerCase().indexOf(q) >= 0;
    });
  }

  function renderEntry(e){
    var definesHtml = "";
    if(e.defines && e.defines.length){
      var shown = e.defines.slice(0, 12).map(esc).join(", ");
      var tail = e.defines.length > 12
        ? ' <span style="color:var(--dim)">+' + (e.defines.length - 12) + ' more</span>'
        : "";
      definesHtml = '<div style="margin-top:6px;font-size:.82em"><strong style="color:var(--teal)">Defines:</strong> ' + shown + tail + '</div>';
    }
    var refbyHtml = "";
    if(e.refby_total){
      refbyHtml = '<div style="margin-top:4px;font-size:.78em;color:var(--dim)">Concepts defined here referenced across ' + e.refby_total + ' other-deposit citations.</div>';
    }
    var creatorLine = esc(e.creator) + ((e.creator && e.date) ? " &middot; " : "") + esc(e.date);
    return '<div style="margin-bottom:24px" id="d' + e.n + '">' +
      '<div style="font-family:var(--mono);font-size:.82em;color:var(--teal);background:#f0f8f6;display:inline-block;padding:3px 8px;border-radius:4px">' + esc(e.axn) + '</div>' +
      '<h1 style="font-size:1.2em;margin-bottom:4px"><a href="/s/records/' + e.n + '/">' + esc(e.title) + '</a></h1>' +
      '<div style="font-size:.82em;color:var(--dim);margin-bottom:8px">' + creatorLine + '</div>' +
      '<div class="art">' + nl2br(e.wiki) + '</div>' +
      definesHtml + refbyHtml +
      '<div style="margin-top:4px;font-size:.82em"><a href="/s/records/' + e.n + '/">Full record &rarr;</a></div>' +
      '</div>';
  }

  function pagerHtml(suffix, total){
    var totalPages = Math.max(1, Math.ceil(total / pageSize));
    var label = "Page " + (page + 1) + " of " + totalPages + " &middot; " + total.toLocaleString() + " wiki entr" + (total === 1 ? "y" : "ies");
    var prev = page <= 0
      ? '<span class="disabled">&larr; Previous</span>'
      : '<a href="#" id="prev-' + suffix + '">&larr; Previous</a>';
    var next = page >= totalPages - 1
      ? '<span class="disabled">Next &rarr;</span>'
      : '<a href="#" id="next-' + suffix + '">Next &rarr;</a>';
    return prev + '<span class="center">' + label + '</span>' + next;
  }

  function bindPager(suffix, totalPages){
    var p = document.getElementById('prev-' + suffix);
    var n = document.getElementById('next-' + suffix);
    if(p) p.onclick = function(ev){ ev.preventDefault(); if(page > 0){ page--; render(); window.scrollTo(0, 0); } };
    if(n) n.onclick = function(ev){ ev.preventDefault(); if(page < totalPages - 1){ page++; render(); window.scrollTo(0, 0); } };
  }

  function render(){
    var pool2 = filtered();
    var totalPages = Math.max(1, Math.ceil(pool2.length / pageSize));
    if(page >= totalPages) page = totalPages - 1;
    if(page < 0) page = 0;
    var slice = pool2.slice(page * pageSize, (page + 1) * pageSize);
    document.getElementById('entries').innerHTML = slice.map(renderEntry).join('') ||
      '<p style="color:var(--dim);padding:20px 0">No matches.</p>';
    document.getElementById('pager-top').innerHTML = pagerHtml('t', pool2.length);
    document.getElementById('pager-bot').innerHTML = pagerHtml('b', pool2.length);
    bindPager('t', totalPages);
    bindPager('b', totalPages);
  }

  document.getElementById('search').addEventListener('input', function(ev){
    query = ev.target.value;
    page = 0;
    render();
  });

  render();
});
</script>"""

    html = _WIKI_HTML_HEAD + body_pre + js + _WIKI_HTML_TAIL

    json_path = REPO_ROOT / "data" / "wiki-entries.json"
    html_path = WIKI_PATH

    if dry_run:
        print(f"  [dry-run] data/wiki-entries.json would be {len(json_str):,} bytes ({len(flat)} entries)")
        print(f"  [dry-run] s/wiki/index.html would be {len(html):,} bytes (JS-paginated, 25 per page)")
        chunk_dirs = list((REPO_ROOT / "s" / "wiki").glob("chunk-*"))
        if chunk_dirs:
            print(f"  [dry-run] would delete {len(chunk_dirs)} chunk dir(s)")
        return

    json_path.parent.mkdir(parents=True, exist_ok=True)
    _receipt(json_path)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(json_str + "\n")

    html_path.parent.mkdir(parents=True, exist_ok=True)
    _receipt(html_path)
    html_path.write_text(html, encoding="utf-8")

    # Remove obsolete chunk directories
    import shutil
    chunk_dirs = list((REPO_ROOT / "s" / "wiki").glob("chunk-*"))
    for cdir in chunk_dirs:
        if cdir.is_dir():
            shutil.rmtree(cdir)

    print(f"  ✓ data/wiki-entries.json ({len(json_str):,} bytes, {len(flat)} entries)")
    print(f"  ✓ s/wiki/index.html ({len(html):,} bytes, JS-paginated 25 per page)")
    if chunk_dirs:
        print(f"  ✓ removed {len(chunk_dirs)} obsolete chunk director{'y' if len(chunk_dirs)==1 else 'ies'}")


CITATION_GRAPH_PATH = REPO_ROOT / "data" / "citation-graph.json"
GRAPH_PATH = REPO_ROOT / "s" / "graph" / "index.html"


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
_WIKI_STYLE = """<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}*{margin:0;padding:0;box-sizing:border-box}body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}.wrap{max-width:720px;margin:0 auto;padding:60px 24px}a{color:var(--accent);text-decoration:none}a:hover{color:var(--accent2)}h1{font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:8px}h2{font-size:1em;font-weight:500;color:var(--accent);margin-top:20px;margin-bottom:6px;border-bottom:1px solid var(--border);padding-bottom:3px}h3{font-size:.9em;color:var(--teal);margin-top:14px}p{margin-bottom:10px;color:#333}.nav{display:flex;gap:16px;margin-bottom:24px;font-size:.85em;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch;padding-bottom:6px}.nav a{color:var(--dim);font-weight:500}.nav a:hover{color:var(--accent)}.pager{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:18px 0;padding:12px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);font-size:.88em;flex-wrap:wrap}.pager a{color:var(--accent);font-weight:500;padding:6px 12px;border:1px solid var(--border);border-radius:4px;background:var(--surface);text-decoration:none}.pager a:hover{background:#f8f8ff}.pager .disabled{color:var(--dim);padding:6px 12px;border:1px solid var(--border);border-radius:4px;opacity:.4;background:transparent}.pager .center{color:var(--dim);font-size:.88em;text-align:center;flex:1}.art{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px;line-height:1.9;color:#333;font-size:.93em;margin:8px 0;white-space:pre-wrap}.footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}.glyph{margin-top:5px;color:var(--accent)}</style>"""

_WIKI_HTML_HEAD = (
    '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
    '<title>Wiki — Alexanarch</title>'
    + _WIKI_STYLE +
    '</head><body><div class="wrap">'
    + render_navbar(active='/s/wiki/') +
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

_GRAPH_STYLE = """<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}*{margin:0;padding:0;box-sizing:border-box}body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}.wrap{max-width:720px;margin:0 auto;padding:60px 24px}a{color:var(--accent);text-decoration:none}a:hover{color:var(--accent2)}h1{font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:8px}.nav{display:flex;gap:16px;margin-bottom:24px;font-size:.85em;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch;padding-bottom:6px}.nav a{color:var(--dim);font-weight:500}.nav a:hover{color:var(--accent)}.er{display:flex;gap:6px;padding:2px 0;font-size:.82em;border-bottom:1px solid #f8f8f8;flex-wrap:wrap}.es{font-weight:500;color:var(--accent);min-width:140px}.ep{color:var(--teal);font-family:var(--mono);font-size:.8em;min-width:80px}.eo{color:#444}.ev{font-size:.65em;font-family:var(--mono);margin-left:3px}.evo{color:var(--teal)}.evi{color:#d4a537}.evp{color:#9966cc}.footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}.glyph{margin-top:5px;color:var(--accent)}</style>"""

_GRAPH_HTML_HEAD = (
    '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
    '<title>Knowledge Graph — Alexanarch</title>'
    + _GRAPH_STYLE +
    '</head><body><div class="wrap">'
    + render_navbar(active='/s/graph/') +
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

# ──────────────────────────────────────────────────────────────────────────────
# state.json + homepage noscript fallback + api/index.json — single-source-of-truth
# ──────────────────────────────────────────────────────────────────────────────

def regenerate_state(reg, dry_run=False):
    """Wraps scripts/generate_state.py — produces data/state.json as the
    canonical generated source for all displayed counts.
    """
    # Defer to the standalone module so it can also be run directly
    sys.path.insert(0, str(REPO_ROOT / 'scripts'))
    import generate_state as _gs
    if dry_run:
        st = _gs.build_state()
        print(f"  [dry-run] data/state.json would be regenerated "
              f"(deposits={st['deposits']['total']}, captures={st['corpus']['captures']})")
        return
    _gs.main()


def regenerate_homepage_noscript(reg, dry_run=False):
    """Rewrite the <noscript>...</noscript> block in index.html so it shows
    the same N latest deposits the JavaScript renders. Previously hand-maintained
    with 4 hardcoded records; now generated from registry on every regen so
    no-JS readers and crawlers see actual current state.

    The contract: the static fallback must equal what JS would render for the
    'Recent Deposits' section. Both pull from data/registry.json — JS at
    runtime, this generator at build time.
    """
    index_path = REPO_ROOT / 'index.html'
    if not index_path.exists():
        print(f"  ⚠ {index_path} not found — skipping")
        return

    # Match the JS slice: filter SUPERSEDED out (canonical reference for an
    # older version is the Version history on the current version's page,
    # not a separate card here), then take the last 5 by deposit_number,
    # reverse for newest-first. Keeps the static fallback in parity with
    # the runtime JS view.
    deposits = sorted(reg['deposits'], key=lambda d: d.get('deposit_number', 0))
    active_deposits = [d for d in deposits if d.get('status', 'ACTIVE') != 'SUPERSEDED']
    recent = list(reversed(active_deposits[-5:]))

    cards = []
    for d in recent:
        n = d.get('deposit_number', 0)
        axn = esc_html(d.get('axn', ''))
        title = esc_html(d.get('title', '(untitled)'))
        creator = esc_html(d.get('creator', ''))
        date = esc_html(d.get('date', ''))
        content_type = esc_html(d.get('content_type', ''))
        desc = esc_html((d.get('description', '') or '')[:250])
        if len(d.get('description', '') or '') > 250:
            desc = desc + '...'
        # Version chip + status badge (mirrors browse-card logic)
        version = d.get('version', '')
        status = d.get('status', 'ACTIVE')
        superseded_by_n = d.get('superseded_by_deposit_number')
        in_real_series = bool(d.get('version_series_id'))
        version_chip = ''
        if version and (version != 'v1.0' or in_real_series):
            version_chip = (f' <span style="font-family:monospace;font-size:.8em;color:#0a7c6a;'
                            f'background:#f0f4f8;padding:1px 6px;border-radius:8px;margin-left:4px;'
                            f'font-weight:500">{esc_html(version)}</span>')
        status_banner = ''
        opacity = '1'
        if status == 'SUPERSEDED' and superseded_by_n:
            opacity = '0.65'
            status_banner = (f'<div style="font-size:0.78em;color:#92400e;background:#fef3c7;'
                             f'padding:4px 10px;border-radius:4px;margin:6px 0;display:inline-block">'
                             f'⚠ Superseded by <strong>#{superseded_by_n}</strong></div>')
        elif status == 'DRAFT_PENDING':
            opacity = '0.65'
            status_banner = ('<div style="font-size:0.78em;color:#6b7280;background:#f3f4f6;'
                             'padding:4px 10px;border-radius:4px;margin:6px 0;display:inline-block;'
                             'font-style:italic">⏳ Draft — body not yet written</div>')

        card = (
            f'<a href="/s/records/{n}/" style="display:block;background:#fff;border:1px solid #e0e0e0;'
            f'border-radius:6px;padding:20px;margin-bottom:12px;text-decoration:none;color:inherit;opacity:{opacity}">'
            f'<div style="font-family:monospace;font-size:0.88em;color:#0a7c6a;font-weight:500">{axn}</div>'
            f'{status_banner}'
            f'<div style="font-weight:500;font-size:0.95em;margin:4px 0">{title}{version_chip}</div>'
            f'<div style="font-size:0.82em;color:#777">{creator} · {date} · {content_type}</div>'
            f'<div style="font-size:0.82em;color:#999;margin-top:6px;line-height:1.5">{desc}</div>'
            f'</a>'
        )
        cards.append(card)

    new_noscript = (
        '<noscript>\n'
        f'<!-- Generated from data/registry.json by scripts/regenerate_surfaces.py on '
        f'{datetime.now(timezone.utc).strftime("%Y-%m-%d")}. Latest {len(recent)} deposits, '
        f'matching the JavaScript Recent Deposits slice. -->\n'
        + ''.join(cards) +
        '<div style="text-align:center;margin-top:12px"><a href="/s/browse/" style="color:#0a7c6a">Browse all deposits →</a></div>\n'
        '</noscript>'
    )

    html = index_path.read_text()
    # Replace the existing noscript block
    import re
    noscript_pattern = re.compile(r'<noscript>.*?</noscript>', re.DOTALL)
    if not noscript_pattern.search(html):
        print(f"  ⚠ index.html has no <noscript> block — skipping")
        return
    new_html = noscript_pattern.sub(new_noscript, html, count=1)

    if dry_run:
        print(f"  [dry-run] index.html <noscript> would be updated to {len(recent)} latest deposits")
        return
    _receipt(index_path, reason="regenerate_surfaces homepage-noscript")
    index_path.write_text(new_html, encoding='utf-8')
    print(f"  ✓ index.html <noscript> updated ({len(recent)} latest deposits, matching JS slice)")


def regenerate_api_index(reg, dry_run=False):
    """Update api/index.json's drift-prone fields from authoritative sources.

    Specifically: current_count fields should equal what data/state.json says,
    and protocol content_sha256 fields should match the actual file SHA-256s.
    Anything outside these regenerable fields is left untouched.

    This does NOT regenerate the whole file from scratch — that would lose
    hand-curated descriptive content. It updates only the fields that have
    documented, derivable values.
    """
    idx_path = REPO_ROOT / 'api' / 'index.json'
    if not idx_path.exists():
        print(f"  ⚠ {idx_path} not found — skipping")
        return
    with open(idx_path) as f:
        idx = json.load(f)

    changes = []

    # Update deposit count
    if 'registries' in idx and 'deposits' in idx['registries']:
        old = idx['registries']['deposits'].get('current_count')
        new = len(reg['deposits'])
        if old != new:
            idx['registries']['deposits']['current_count'] = new
            changes.append(f"registries.deposits.current_count: {old} → {new}")

    # Update protocol content_sha256 fields
    for proto_key in ('deposit', 'axn', 'enrichment', 'lifecycle'):
        if 'protocols' not in idx or proto_key not in idx['protocols']:
            continue
        canonical = idx['protocols'][proto_key].get('canonical_path', '')
        if not canonical:
            continue
        file_path = REPO_ROOT / canonical.lstrip('/')
        if not file_path.exists():
            continue
        actual_sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
        old_sha = idx['protocols'][proto_key].get('content_sha256')
        if old_sha != actual_sha:
            idx['protocols'][proto_key]['content_sha256'] = actual_sha
            changes.append(f"protocols.{proto_key}.content_sha256: {(old_sha or 'none')[:16]}… → {actual_sha[:16]}…")

    # Remove stale 'javascript_embedded' claim (workflow no longer embeds JS;
    # it invokes Python via axn_lib.py)
    axn_proto = idx.get('protocols', {}).get('axn', {})
    canonical_impls = axn_proto.get('canonical_implementations', {})
    if canonical_impls.get('javascript_embedded'):
        del canonical_impls['javascript_embedded']
        changes.append("protocols.axn.canonical_implementations.javascript_embedded: REMOVED (stale claim — workflow uses scripts/axn_lib.py)")

    # Add or update state_reference
    state_path = REPO_ROOT / 'data' / 'state.json'
    if state_path.exists():
        state_sha = hashlib.sha256(state_path.read_bytes()).hexdigest()
        if 'state' not in idx:
            idx['state'] = {
                'canonical_path': '/data/state.json',
                'description': 'Canonical generated source for all displayed counts. Read this rather than hand-maintaining counts here.',
                'content_sha256': state_sha,
            }
            changes.append("Added 'state' reference pointing to /data/state.json")
        elif idx['state'].get('content_sha256') != state_sha:
            idx['state']['content_sha256'] = state_sha
            changes.append(f"state.content_sha256 updated to {state_sha[:16]}…")

    if dry_run:
        if changes:
            print(f"  [dry-run] api/index.json: {len(changes)} field(s) would update")
            for c in changes:
                print(f"      {c}")
        else:
            print(f"  [dry-run] api/index.json: in sync with data sources")
        return

    if changes:
        _receipt(idx_path, reason="regenerate_surfaces api-index")
        with open(idx_path, 'w') as f:
            json.dump(idx, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f"  ✓ api/index.json updated ({len(changes)} drift correction(s))")
        for c in changes:
            print(f"      {c}")
    else:
        print(f"  ✓ api/index.json (already in sync)")


SURFACE_FNS = {
    "state": regenerate_state,
    "browse": regenerate_browse,
    "browse-index": regenerate_browse_index,
    "chunks": regenerate_chunks,
    "sitemap": regenerate_sitemap,
    "sha256sums": regenerate_sha256sums,
    "wiki": regenerate_wiki,
    "graph": regenerate_graph,
    "homepage-noscript": regenerate_homepage_noscript,
    "api-index": regenerate_api_index,
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
