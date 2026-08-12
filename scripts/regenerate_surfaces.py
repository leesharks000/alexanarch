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
import re
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

HOMEPAGE_RECENT_N = 12  # must equal the JS slice in index.html
ALL_SURFACES = ["state", "browse", "feed", "browse-index", "hex-to-deposit", "chunks", "sitemap", "sha256sums", "wiki", "graph", "homepage-noscript", "api-index", "search-index", "search-static", "dynamic-counts", "semantic-addresses"]


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
<div id="browse-meta" style="color:#777;font-size:.88em;margin-bottom:16px">{total} deposits · sorted by deposit number, oldest first · for newest see <a href="/">home page</a></div>
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
<!-- END-OF-BROWSE-ROWS: {total} deposits above. If your fetch tool truncated the page (this page is ~940 KB), you did NOT see this marker. Trust the numberOfItems field in the JSON-LD at the top over any row-count. Complete machine-readable listing at /data/browse-index.json (~570 KB). -->
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script defer src="/assets/gc-enhance.js"></script>
<div class="footer"><strong>Alexanarch</strong> · <span style="color:#777">end of {total} rows</span> · machine index: <a href="/data/browse-index.json" style="color:var(--teal)">browse-index.json</a><div style="margin-top:5px;color:var(--accent)">∮ = 1</div></div></div></body></html>"""


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
        "@id": "https://www.alexanarch.org/s/browse/",
        "name": "Alexanarch — Complete Deposit Registry",
        "description": f"Self-governing library for machine-mediated scholarship. {total} deposits with content-derived AXN identifiers.",
        "url": "https://www.alexanarch.org/s/browse/",
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
    # P2 filter — progressive enhancement over the complete static list. The full
    # list stays in the HTML for crawlers and no-JS readers; the widget only hides
    # non-matching rows and routes onward to full-text search.
    from filter_widget import filter_widget
    parts.append(filter_widget('a[href^="/s/records/"]', 'deposits', total))
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
            # NESTED-ANCHOR FIX (MANUS screenshots, 2026-08-04): the browse card
            # IS an <a>. An <a> inside an <a> is invalid HTML — every browser
            # closes the outer anchor at the inner one and hoists the remaining
            # inner links to the end of the document. That is what produced the
            # broken tail: rows reading "AXN:… · superseded by" with no target,
            # and a long orphaned column of #NNNN links after the last row.
            # The target is now plain text inside the card's own link, which
            # already points at the record; the record page carries the pointer.
            status_badge = (f' · <span style="color:#92400e;font-size:.85em">'
                            f'superseded by #{superseded_by_n}</span>')
            card_opacity = ';opacity:.65'
        elif status == 'DRAFT_PENDING':
            status_badge = ' · <span style="color:#6b7280;font-size:.85em;font-style:italic">draft pending</span>'
            card_opacity = ';opacity:.65'
        # T6: surface non-canonical availability on the card itself
        _cts = d.get("canonical_text_status")
        if _cts == "metadata_only":
            status_badge += ' · <span style="color:#6b7280;font-size:.85em">metadata-only</span>'
        elif _cts == "recovered_full_text":
            pass  # full text present; no caveat needed on the card
        elif _cts in ("withdrawn", "tombstone"):
            status_badge += f' · <span style="color:#991b1b;font-size:.85em;font-weight:600">{_cts.upper()}</span>'
        parts.append(BROWSE_CARD.format(
            n=n,
            title=esc_html(d.get("title", "(untitled)")),
            date=esc_html(d.get("date", "")),
            axn=esc_html(d.get("axn", "")),
            version_chip=version_chip,
            status_badge=status_badge,
            card_opacity=card_opacity,
        ))
    parts.append(BROWSE_FOOTER.format(total=total))

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
# Surface 2.5: data/hex-to-deposit.json — used by /records/?id= redirect
# ──────────────────────────────────────────────────────────────────────────────

def regenerate_hex_to_deposit(reg, dry_run=False):
    """Rebuild data/hex-to-deposit.json — hex AXN identifier → deposit number.

    Used by /records/index.html to handle legacy URLs indexed by search
    engines and AI overviews using ?id=<hex> (e.g. ?id=0143) rather than
    ?id=<deposit_number>. The hex/deposit relationship is content-derived
    for early deposits, so a static formula is insufficient; a lookup
    table is required.
    """
    deposits = reg["deposits"]
    mapping = {}
    for d in deposits:
        h = d.get("hex")
        n = d.get("deposit_number")
        if not h or n is None:
            continue
        key = str(h).upper()
        mapping[key] = n
        # Also expose 4-digit zero-padded variant for early "01"/"02"/"03"
        padded = key.zfill(4)
        if padded != key:
            mapping[padded] = n

    target = REPO_ROOT / "data" / "hex-to-deposit.json"
    # Sort keys for stable diffs; compact JSON (small file)
    payload = json.dumps(mapping, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    if dry_run:
        print(f"  [DRY] would write {target} ({len(payload):,} bytes)")
        return
    _receipt(target)
    with open(target, "w", encoding="utf-8") as f:
        f.write(payload)
    print(f"  ✓ data/hex-to-deposit.json ({len(payload):,} bytes, {len(mapping)} hex→deposit entries)")


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
    # AXN resolution layer (permanent — do not remove)
    ("https://www.alexanarch.org/data/doi-resolution-index.json", 0.9),
    ("https://www.alexanarch.org/api/doi-axn-map.json", 0.9),
    ("https://www.alexanarch.org/data/provenance-871.json", 0.8),
    # Network surfaces: permanent cross-listing PRESERVED, relocated to the
    # crawlable /fleet/ page (EA-AVAILABILITY-INTEGRITY-01 T4, ⟡9 RESOLVED
    # 2026-07-28) — cross-host sitemap locs are discarded by crawlers and
    # erode sitemap trust; the HTML page keeps every link crawler-visible.
    ("https://www.alexanarch.org/fleet/", 0.7),
    # Core
    ("https://www.alexanarch.org/", 1.0),
    ("https://www.alexanarch.org/deposit/", 0.8),
    ("https://www.alexanarch.org/guide/", 0.8),
    ("https://www.alexanarch.org/manifest/", 0.8),
    ("https://www.alexanarch.org/principles/", 0.8),
    ("https://www.alexanarch.org/identifiers/", 0.8),
    # Discovery surfaces (the 7 the audit flagged as missing)
    ("https://www.alexanarch.org/observatory/", 0.9),
    ("https://www.alexanarch.org/lexical/", 0.8),
    ("https://www.alexanarch.org/citations/", 0.8),
    ("https://www.alexanarch.org/captures/", 0.8),
    ("https://www.alexanarch.org/addresses/", 0.7),
    ("https://www.alexanarch.org/resolve/", 0.7),
    ("https://www.alexanarch.org/datasets/", 0.7),
    # Generated surfaces
    ("https://www.alexanarch.org/s/browse/", 0.5),
    ("https://www.alexanarch.org/s/wiki/", 0.5),
    ("https://www.alexanarch.org/s/graph/", 0.5),
    ("https://www.alexanarch.org/s/search/", 0.5),
    ("https://www.alexanarch.org/search/", 0.6),
    # Canonical data
    ("https://www.alexanarch.org/data/registry.json", 0.5),
    ("https://www.alexanarch.org/data/state.json", 0.6),
    ("https://www.alexanarch.org/data/navigation.json", 0.4),
    ("https://www.alexanarch.org/data/doi-resolution-index.json", 0.5),
    ("https://www.alexanarch.org/data/batch-axn-assignment.json", 0.4),
    ("https://www.alexanarch.org/data/chunks/registry/_index.json", 0.4),
    ("https://www.alexanarch.org/api/search-index.json", 0.7),
    # Protocols
    ("https://www.alexanarch.org/api/index.json", 0.6),
    ("https://www.alexanarch.org/api/deposit-protocol.json", 0.5),
    ("https://www.alexanarch.org/api/deposit-schema.json", 0.5),
    ("https://www.alexanarch.org/api/axn-protocol.json", 0.5),
    ("https://www.alexanarch.org/api/enrichment-protocol.json", 0.4),
    ("https://www.alexanarch.org/api/lifecycle-protocol.json", 0.5),
    # Documents
    ("https://www.alexanarch.org/AGENTS.md", 0.4),
    ("https://www.alexanarch.org/DEPOSIT-FLOW.md", 0.4),
]



def regenerate_feed(reg, dry_run=False):
    """Atom 1.0 feed of the most recent deposits at /feed.xml.

    2026-08-12: an external audit looked for /feed.xml and found nothing. The
    archive publishes a sitemap, an OAI-PMH endpoint, ResourceSync and a JSON
    index — every machine-facing surface EXCEPT the one a plain feed reader
    speaks. Syndication is the oldest and least demanding way for a follower to
    learn that something new exists, and it costs one file.

    Atom rather than RSS: it requires an explicit updated timestamp per entry
    and a stable id, both of which the registry already carries, and it does not
    invite the date-format ambiguity RSS 2.0 tolerates.
    """
    feed_n = 50
    deposits = sorted(reg['deposits'], key=lambda d: d.get('deposit_number', 0))
    active = [d for d in deposits if d.get('status', 'ACTIVE') != 'SUPERSEDED']
    recent = list(reversed(active[-feed_n:]))
    if not recent:
        print("  ⚠ no deposits — skipping feed")
        return

    def esc(x):
        return esc_html(str(x or ''))

    newest_date = recent[0].get('date') or datetime.now(timezone.utc).strftime('%Y-%m-%d')
    updated = '%sT00:00:00Z' % newest_date
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        '  <title>Alexanarch — recent deposits</title>',
        '  <subtitle>The self-governing library for machine-mediated scholarship. '
        'Content-derived AXN identifiers; every deposit auditable.</subtitle>',
        '  <link href="https://www.alexanarch.org/feed.xml" rel="self" type="application/atom+xml"/>',
        '  <link href="https://www.alexanarch.org/" rel="alternate" type="text/html"/>',
        '  <id>https://www.alexanarch.org/</id>',
        '  <updated>%s</updated>' % updated,
        '  <generator uri="https://github.com/leesharks000/alexanarch">scripts/regenerate_surfaces.py</generator>',
        '  <rights>Deposits carry their own licences; see each record.</rights>',
    ]
    for d in recent:
        n = d.get('deposit_number', 0)
        url = 'https://www.alexanarch.org/s/records/%d/' % n
        date = d.get('date') or newest_date
        desc = (d.get('description', '') or '')[:600]
        if len(d.get('description', '') or '') > 600:
            desc += '…'
        lines += [
            '  <entry>',
            '    <title>%s</title>' % esc(d.get('title', '(untitled)')),
            '    <link href="%s" rel="alternate" type="text/html"/>' % url,
            # The AXN is the archive's own identifier and is content-derived, so it
            # is the honest atom:id — stable, and independent of the URL scheme.
            '    <id>urn:axn:%s</id>' % esc(d.get('axn', str(n))),
            '    <updated>%sT00:00:00Z</updated>' % esc(date),
            '    <author><name>%s</name></author>' % esc(d.get('creator', 'Alexanarch')),
            '    <category term="%s"/>' % esc(d.get('content_type', '')),
            '    <summary type="text">%s</summary>' % esc(desc),
            '  </entry>',
        ]
    lines.append('</feed>')
    out = '\n'.join(lines) + '\n'
    path = REPO_ROOT / 'feed.xml'
    if dry_run:
        print("  [dry-run] feed.xml would list %d deposits" % len(recent))
        return
    _receipt(path, reason="regenerate_surfaces feed")
    path.write_text(out, encoding='utf-8')
    print("  ✓ feed.xml (%d deposits, %d bytes)" % (len(recent), len(out)))


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
        # <lastmod> carries the record's own modification date when it has one
        # (see scripts/record_modification.py). Absence means unmodified since
        # deposit — a truthful claim — so we fall back to the publication date
        # rather than stamping today and teaching crawlers to discount the field.
        last = esc_xml(d.get("date_modified") or d.get("date") or today)
        lines.append(
            f'  <url><loc>https://www.alexanarch.org/s/records/{n}/</loc>'
            f'<lastmod>{last}</lastmod><priority>0.8</priority></url>'
        )
        # PDFs demoted from the sitemap 2026-07-19 (Canonical Record Convergence
        # P0.7, MANUS-directed searchability pass): the /papers/ layer remains
        # fully published and linked from every record page as a representation,
        # but no longer competes with /s/records/N/ as an independent crawl
        # target. (Supersedes the 2026-07-17 regression note: the paper layer
        # is preserved by record-page links + /papers/ directory, not sitemap.)
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

    # SEALED CORES (2026-08-06): stored symbolon originals belong in the
    # real-file manifest. They were absent from it entirely — a depositor could
    # not run `sha256sum -c` against the file this archive holds on her behalf,
    # and a mirror operator had nothing to check a copy against. Their expected
    # hash is not a separate assertion: it IS the AXN0 kernel, so these lines
    # are self-checking. Written from bytes on disk, like the text lines above.
    sym_dir = REPO_ROOT / "data/symbolon-registry/files"
    sym_count = 0
    if sym_dir.is_dir():
        for sf in sorted(sym_dir.iterdir()):
            if not sf.is_file() or sf.name.startswith("."):
                continue
            try:
                sh = hashlib.sha256(sf.read_bytes()).hexdigest()
                file_lines.append(f"{sh}  {sf.relative_to(REPO_ROOT).as_posix()}")
                sym_count += 1
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
    print(f"  ✓ SHA256SUMS.txt ({len(file_lines)} file lines incl. {sym_count} sealed cores, real paths, sha256sum -c verifiable)")

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

    # Task 2 of EA-RETRIEVAL-DENSITY-01: after the dataset is written, delegate
    # to publish_wiki_entries.py which generates one HTML page per entry at
    # /s/wiki/{n}/ and OVERWRITES s/wiki/index.html with a static alphabetical
    # listing (retiring the JS-only pagination that hid 97% of entries from
    # non-JS crawlers). Overwrite is intentional: the paginated version above
    # is written first as a defensive fallback in case publish_wiki_entries
    # fails, then replaced by the crawler-friendly static list.
    try:
        import subprocess
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "scripts" / "publish_wiki_entries.py")],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                print(f"    {line}")
        else:
            print(f"  ! publish_wiki_entries failed (returncode={result.returncode}):")
            print(f"    stderr: {result.stderr[:400]}")
    except Exception as e:
        print(f"  ! publish_wiki_entries invocation error: {e}")


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
    """Server-render the latest deposits INTO #recent-deposits in index.html.

    2026-08-12 (MANUS): previously this wrote the cards into a <noscript> block,
    leaving the visible container holding only 'Loading registry...'. That was
    adequate for a no-JS reader but not for a crawler: agents that execute
    JavaScript commonly skip <noscript> entirely, and agents that do not may
    treat it as low-value. Either way the homepage presented a manifesto with
    almost no record links, and the deposit corpus reached crawlers only through
    the sitemap and /s/browse/.

    The cards are now written as the DEFAULT CONTENT of the #recent-deposits
    div. The existing JavaScript replaces el.innerHTML on load, so this is
    ordinary progressive enhancement: real links in the served HTML, live
    rendering for a browser. The <noscript> block is removed as redundant.

    The contract is unchanged: the static render must equal what JS renders for
    'Recent Deposits'. Both read data/registry.json — JS at runtime, this
    generator at build time. HOMEPAGE_RECENT_N is the single place the count is
    set, and the JS slice must match it.
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
    recent = list(reversed(active_deposits[-HOMEPAGE_RECENT_N:]))

    cards = []
    for d in recent:
        n = d.get('deposit_number', 0)
        axn = esc_html(d.get('axn', ''))
        title = esc_html(d.get('title', '(untitled)'))
        creator = esc_html(d.get('creator', ''))
        date = esc_html(d.get('date', ''))
        content_type_raw = d.get('content_type', '') or ''
        # Card-hardening (MANUS, 2026-07-08): content_type is a category label
        # (like "Philological erratum"), not a specification paragraph. Clip
        # defensively so an accidentally-long entry cannot balloon the card
        # vertically. The full content_type remains in the deposit record page.
        if len(content_type_raw) > 140:
            content_type = esc_html(content_type_raw[:140].rsplit(' ', 1)[0] + '…')
        else:
            content_type = esc_html(content_type_raw)
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

    new_block = (
        '<div id="recent-deposits" style="margin-bottom:30px">\n'
        f'<!-- SERVER-RENDERED from data/registry.json by scripts/regenerate_surfaces.py on '
        f'{datetime.now(timezone.utc).strftime("%Y-%m-%d")}. Latest {len(recent)} active deposits, '
        f'matching the JavaScript Recent Deposits slice. The JS below replaces this on load; '
        f'crawlers and no-JS readers get real record links without it. -->\n'
        + ''.join(cards) +
        '<div style="text-align:center;margin-top:12px"><a href="/s/browse/" style="color:#0a7c6a">Browse all deposits →</a></div>\n'
        '</div>'
    )

    import re
    html = index_path.read_text()
    # Replace the whole #recent-deposits container, whatever it currently holds
    container = re.compile(r'<div id="recent-deposits".*?</div>\s*(?=<noscript>|<script>|<h2|$)', re.DOTALL)
    m = re.search(r'<div id="recent-deposits"[^>]*>.*?\n</div>', html, re.DOTALL)
    if not m:
        # first-run shape: placeholder div with a single child div
        m = re.search(r'<div id="recent-deposits"[^>]*>\s*<div[^>]*>Loading registry\.\.\.</div>\s*</div>', html, re.DOTALL)
    if not m:
        print("  ⚠ index.html has no #recent-deposits container — skipping")
        return
    new_html = html[:m.start()] + new_block + html[m.end():]
    # retire the now-redundant noscript duplicate, once
    new_html = re.sub(r'<noscript>\s*<!-- Generated from data/registry\.json.*?</noscript>\s*', '', new_html, count=1, flags=re.DOTALL)

    if dry_run:
        print(f"  [dry-run] index.html #recent-deposits would be server-rendered with {len(recent)} latest deposits")
        return
    _receipt(index_path, reason="regenerate_surfaces homepage-deposits")
    index_path.write_text(new_html, encoding='utf-8')
    print(f"  ✓ index.html #recent-deposits server-rendered ({len(recent)} latest deposits, matching JS slice)")


def regenerate_api_index(reg, dry_run=False):
    """Update api/index.json's drift-prone fields from authoritative sources.

    Specifically: current_count fields should equal what data/state.json says,
    and protocol content_sha256 fields should match the actual file SHA-256s.
    Anything outside these regenerable fields is left untouched.

    This does NOT regenerate the whole file from scratch — that would lose
    hand-curated descriptive content. It updates only the fields that have
    documented, derivable values.
    """
    # 2026-08-12: the generator looked in api/ while the file has always lived at
    # data/api/index.json, so this stage silently no-opped every run and the
    # machine-authority counts froze at whatever was last hand-edited. The file
    # declares itself the single source of truth — "if this file disagrees with
    # any other surface, this file wins" — so a silent skip here is the most
    # consequential failure in the surface set. Both paths are now tried, and a
    # miss is loud.
    idx_path = None
    for cand in (REPO_ROOT / 'data' / 'api' / 'index.json', REPO_ROOT / 'api' / 'index.json'):
        if cand.exists():
            idx_path = cand
            break
    if idx_path is None:
        raise SystemExit("FATAL: api/index.json not found at data/api/ or api/ — "
                         "the machine-authority index cannot be left stale silently.")
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


# ──────────────────────────────────────────────────────────────────────────────
# Surface 12: /api/search-index.json — token-level inverted index (v1)
# ──────────────────────────────────────────────────────────────────────────────
#
# Machine-facing search endpoint. Reads registry, emits an inverted index
# mapping tokens → lists of deposit numbers. Fetch once; look up any term
# as a key. Complements /data/browse-index.json (which is walk-and-grep):
# search-index.json is direct lookup, no scan.
#
# Series prefixes (gw.tachyon, EA-*, MPAI, OCTANG, etc.) are captured as
# structured entries with their casing preserved. Generic tokens are
# case-folded and stopwords are stripped. Content-derived identifiers
# (AXN hex, full AXN) are added as their own lookup keys so a bare hex
# like "0421" resolves to its deposit number.

_SEARCH_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "is", "are", "was", "were", "be", "been",
    "being", "has", "have", "had", "it", "its", "this", "that", "these",
    "those", "which", "who", "whom", "whose", "what", "when", "where",
    "why", "how", "not", "no", "so", "if", "than", "then", "into", "out",
    "via", "per", "over", "vs",
})

_SEARCH_SERIES_PATTERNS = [
    # (regex, case-fold?)
    (re.compile(r"\bgw\.tachyon(?:\.[a-z]+)?", re.IGNORECASE), True),
    (re.compile(r"\bgw\.[a-z]+(?:\.[a-z]+)?", re.IGNORECASE), True),
    (re.compile(r"\bEA-[A-Z0-9]+(?:-[A-Z0-9]+)*"), False),
    (re.compile(r"\bMPAI(?:-[A-Z0-9]+)*"), False),
    (re.compile(r"\bOCTANG(?:-\d+)?"), False),
    (re.compile(r"\bPVE-\d+"), False),
    (re.compile(r"\bEB-\d+"), False),
    (re.compile(r"\bSPXI(?:-[A-Z0-9]+)*"), False),
    (re.compile(r"\bCHA(?:-[A-Z0-9-]+)?"), False),
    (re.compile(r"\bNEGSHAPE(?:-\d+)?"), False),
    (re.compile(r"\bAXN:[0-9A-F]{3,4}", re.IGNORECASE), False),
]


def _tokenize_search(text):
    """Extract case-folded generic tokens, ≥3 chars, stopwords removed."""
    if not text:
        return []
    words = re.findall(r"[a-zA-Z0-9]{3,}", text.lower())
    return [w for w in words if w not in _SEARCH_STOPWORDS]


def _extract_series(text):
    """Find series-prefix matches with structure preserved."""
    if not text:
        return []
    out = []
    for cre, fold in _SEARCH_SERIES_PATTERNS:
        for m in cre.findall(text):
            if isinstance(m, tuple):
                m = m[0] if m else ""
            if m:
                out.append(m.lower() if fold else m)
    return out


def regenerate_search_index(reg, dry_run=False):
    """Build /api/search-index.json — token-level inverted index.

    Sources per deposit: title, description, creator, content_type, keywords,
    axn (full), hex. Series prefixes captured in a dedicated table with
    casing preserved.
    """
    _cts_index = {}
    for _d in reg["deposits"]:
        _cts_index.setdefault(_d.get("canonical_text_status", "unclassified"), []).append(_d["deposit_number"])
    _cts_index = {k: sorted(v) for k, v in sorted(_cts_index.items())}
    deposits = reg["deposits"]

    inverted = {}    # generic token → set of deposit numbers
    series_ix = {}   # series token (e.g. gw.tachyon, EA-EROSION-01) → deposit numbers
    creator_ix = {}  # creator full-string → deposit numbers
    type_ix = {}     # content_type prefix → deposit numbers
    hex_ix = {}      # hex label → deposit number(s)
    keyword_ix = {}  # explicit keyword (whole phrase, lowercased) → deposit numbers

    for d in deposits:
        n = d.get("deposit_number") or d.get("issue_number") or 0
        if not n:
            continue
        title = d.get("title", "") or ""
        creator = (d.get("creator", "") or "").strip()
        desc = d.get("description", "") or ""
        ctype_full = (d.get("content_type", "") or "").strip()
        ctype_prefix = re.split(r"[;(]", ctype_full)[0].strip()
        axn = d.get("axn", "") or ""
        hexid = d.get("hex", "") or ""
        keywords = d.get("keywords", []) or []

        # Generic tokens from title + description
        for tok in _tokenize_search(title):
            inverted.setdefault(tok, set()).add(n)
        for tok in _tokenize_search(desc):
            inverted.setdefault(tok, set()).add(n)

        # Series prefixes from title + description (preserve casing)
        for series_tok in _extract_series(title + " " + desc):
            series_ix.setdefault(series_tok, set()).add(n)

        # Creators — both as full-string key and as tokens
        if creator:
            creator_ix.setdefault(creator, set()).add(n)
            for tok in _tokenize_search(creator):
                inverted.setdefault(tok, set()).add(n)

        # Content-type prefix as its own facet
        if ctype_prefix:
            type_ix.setdefault(ctype_prefix, set()).add(n)
            for tok in _tokenize_search(ctype_prefix):
                inverted.setdefault(tok, set()).add(n)

        # Keywords: whole phrase + individual tokens
        for kw in keywords:
            kw_norm = kw.strip().lower()
            if kw_norm:
                keyword_ix.setdefault(kw_norm, set()).add(n)
            for tok in _tokenize_search(kw):
                inverted.setdefault(tok, set()).add(n)

        # AXN and hex as their own lookup keys
        if axn:
            inverted.setdefault(axn.lower(), set()).add(n)
        if hexid:
            hex_ix.setdefault(hexid.upper(), set()).add(n)
            # Also case-folded into the generic table for grep-style queries
            inverted.setdefault(hexid.lower(), set()).add(n)

    def to_sorted(d):
        return {k: sorted(v) for k, v in sorted(d.items())}

    output = {
        "$schema": "https://www.alexanarch.org/api/schemas/search-index.schema.json",
        "canonical_text_status_index": _cts_index,
        "$id": "https://www.alexanarch.org/api/search-index.json",
        "index_version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "total_deposits": len(deposits),
        "tokenization": {
            "sources": ["title", "description", "creator", "content_type", "keywords", "axn", "hex"],
            "min_length": 3,
            "case_folded": True,
            "stopwords_stripped": True,
            "series_prefixes_regex_captured": True,
            "series_families_recognized": [
                "gw.tachyon.*", "gw.<substrate>.*", "EA-*", "MPAI-*", "OCTANG-*",
                "PVE-*", "EB-*", "SPXI-*", "CHA-*", "NEGSHAPE-*", "AXN:*"
            ],
        },
        "series_prefixes": to_sorted(series_ix),
        "hex_labels": to_sorted(hex_ix),
        "creators": to_sorted(creator_ix),
        "content_types": to_sorted(type_ix),
        "keywords": to_sorted(keyword_ix),
        "index": to_sorted(inverted),
        "counts": {
            "series_prefix_terms": len(series_ix),
            "hex_labels": len(hex_ix),
            "creator_names": len(creator_ix),
            "content_types": len(type_ix),
            "keyword_phrases": len(keyword_ix),
            "generic_tokens": len(inverted),
        },
    }

    target = REPO_ROOT / "data" / "api" / "search-index.json"
    payload = json.dumps(output, ensure_ascii=False, indent=2)
    if dry_run:
        print(f"  [DRY] would write {target} ({len(payload):,} bytes)")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    _receipt(target)
    with open(target, "w", encoding="utf-8") as f:
        f.write(payload)
    print(f"  ✓ api/search-index.json ({len(payload):,} bytes, "
          f"{len(inverted)} generic tokens, {len(series_ix)} series prefixes, "
          f"{len(keyword_ix)} keyword phrases)")


def regenerate_search_static(reg, dry_run=False):
    """Build /s/search/index.html — static crawler-readable series-prefix table.

    Complements the dynamic /search/ page (JS-driven). Machines that follow
    HTML links land here; agents that want token-level lookup should fetch
    /api/search-index.json directly.
    """
    deposits_by_n = {d.get("deposit_number") or d.get("issue_number"): d
                     for d in reg["deposits"]}

    # Rebuild the series and hex tables here (mirror of search-index logic)
    series_ix = {}
    hex_ix = {}
    for n, d in deposits_by_n.items():
        if not n:
            continue
        text = (d.get("title", "") or "") + " " + (d.get("description", "") or "")
        for series_tok in _extract_series(text):
            series_ix.setdefault(series_tok, set()).add(n)
        hexid = d.get("hex", "")
        if hexid:
            hex_ix.setdefault(hexid.upper(), set()).add(n)

    # Series section
    series_rows = []
    for series_tok, nums in sorted(series_ix.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        nums_sorted = sorted(nums)
        links = " · ".join(
            f'<a href="/s/records/{n}/">#{n}</a>'
            for n in nums_sorted[:100]
        )
        more = f" (+{len(nums_sorted) - 100} more)" if len(nums_sorted) > 100 else ""
        series_rows.append(
            f'<h3>{esc_html(series_tok)} <span class="count">{len(nums_sorted)}</span></h3>'
            f'<p>{links}{more}</p>'
        )
    series_body = "\n".join(series_rows) or "<p><em>No series prefixes detected.</em></p>"

    nav = render_navbar(active="/s/search/")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Search — Alexanarch</title>
<meta name="description" content="Static series-prefix table with deposit links. For token-level search, fetch /api/search-index.json or use /search/.">
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");
:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.7;font-size:15px}}
.wrap{{max-width:900px;margin:0 auto;padding:60px 24px}}
a{{color:var(--accent);text-decoration:none}}a:hover{{color:var(--accent2)}}
h1{{font-size:1.4em;font-weight:600;color:var(--accent);margin-bottom:12px}}
h2{{font-size:1em;font-weight:500;color:var(--accent);margin-top:24px;margin-bottom:8px;border-bottom:1px solid var(--border);padding-bottom:4px}}
h3{{font-family:var(--mono);font-size:.95em;color:var(--fg);margin-top:20px;margin-bottom:4px}}
h3 .count{{color:var(--dim);font-family:var(--sans);font-weight:400;font-size:.85em;margin-left:8px}}
p{{margin-bottom:8px;color:#333;font-size:.9em}}
.nav{{display:flex;gap:12px;margin-bottom:24px;font-size:.85em;overflow-x:auto;white-space:nowrap}}
.nav a{{color:#777;font-weight:500;text-decoration:none}}.nav a:hover{{color:var(--accent)}}
.hint{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 18px;margin:14px 0;font-size:.88em;color:#444;line-height:1.6}}
.hint code{{background:#f0f4f8;font-family:var(--mono);font-size:.9em;padding:1px 6px;border-radius:3px}}
.footer{{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}}
</style>
</head>
<body>
<div class="wrap">
<!-- NAV-START -->
{nav}
<!-- NAV-END -->
<h1>Search — Series-Prefix Table (static)</h1>
<div class="hint">
This is the static, crawler-readable projection of the series-prefix table. Every named series (<code>gw.tachyon</code>, <code>EA-*</code>, <code>MPAI-*</code>, <code>OCTANG-*</code>, etc.) is listed with its member deposit numbers. For interactive token-level search, use <a href="/search/">/search/</a> (JS-driven). For machine-facing token lookup, GET <a href="/api/search-index.json"><code>/api/search-index.json</code></a> directly — it is an inverted index keyed by token, returning deposit numbers.
</div>
<h2>Series prefixes ({len(series_ix)})</h2>
{series_body}
<div class="footer"><strong>Alexanarch</strong> · Self-governing static archive<div style="color:var(--accent)">∮ = 1</div></div>
</div>
</body>
</html>
"""

    target = REPO_ROOT / "s" / "search" / "index.html"
    if dry_run:
        print(f"  [DRY] would write {target} ({len(html):,} bytes)")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    _receipt(target)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ s/search/index.html ({len(html):,} bytes, {len(series_ix)} series prefixes)")


SURFACE_FNS = {
    "state": regenerate_state,
    "browse": regenerate_browse,
    "browse-index": regenerate_browse_index,
    "hex-to-deposit": regenerate_hex_to_deposit,
    "chunks": regenerate_chunks,
    "feed": regenerate_feed,
        "sitemap": regenerate_sitemap,
    "sha256sums": regenerate_sha256sums,
    "wiki": regenerate_wiki,
    "graph": regenerate_graph,
    "homepage-noscript": regenerate_homepage_noscript,
    "api-index": regenerate_api_index,
    "search-index": regenerate_search_index,
    "search-static": regenerate_search_static,
    "dynamic-counts": None,  # populated below (forward-reference to preserve declaration order)
}


# ─── Dynamic counts (Data Art Sweep #1) ─────────────────────────────────────
#
# The archive presents identifying counts on several derived surfaces (Browse,
# Wiki, Datasets, Addresses, Captures, Homepage-noscript). Prior to this
# regenerator, those counts were maintained in different places at different
# cadences, producing version skew: Browse could say 1,083 while Wiki still
# said 863, while Datasets showed a hardcoded 881.
#
# This surface establishes a single mechanism: any element whose text should
# come from a source-of-truth JSON is tagged with either
#
#   <span data-count="{file}:{path}">1,234</span>
#
# for text-node counts, or the comment marker
#
#   <!--REGEN-COUNT {file}:{path}-->
#   <meta content="… 1,234 …">
#
# for counts embedded in attribute-only nodes (meta descriptions, og:*, etc.).
# The regenerator resolves {file}:{path} against the corresponding JSON file
# under data/ and rewrites the count in place. Numbers are formatted with
# thousands separators; a leading + sign is preserved.
#
# jsonpath uses dot-notation with an optional [] suffix meaning len():
#   registry.json:total_deposits
#   semantic-addresses.json:class_counts.subjunctive
#   semantic-addresses.json:addresses[]

_SRC_CACHE = {}


def _load_source(name):
    """Load a source-of-truth JSON file under data/ (cached per run)."""
    if name in _SRC_CACHE:
        return _SRC_CACHE[name]
    path = REPO_ROOT / "data" / name
    if not path.exists():
        raise FileNotFoundError(f"dynamic-counts source not found: {path}")
    _SRC_CACHE[name] = json.loads(path.read_text(encoding="utf-8"))
    return _SRC_CACHE[name]


def _resolve_jsonpath(src, jsonpath):
    """Resolve a dot-separated path into src. Suffix '[]' means len()."""
    parts = jsonpath.split(".")
    v = src
    for i, part in enumerate(parts):
        is_last = (i == len(parts) - 1)
        if part.endswith("[]"):
            key = part[:-2]
            if key:
                v = v[key]
            if not hasattr(v, "__len__"):
                raise TypeError(f"jsonpath {jsonpath}: '{part}' expected a container, got {type(v).__name__}")
            v = len(v)
        else:
            if not isinstance(v, dict):
                raise TypeError(f"jsonpath {jsonpath}: '{part}' expected a dict, got {type(v).__name__}")
            v = v[part]
    return v


def _fmt_count(value):
    """Format an integer count with thousands separators. Pass-through for str."""
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


_ATTR_RE = re.compile(r'(data-count="([^"]+)"[^>]*>)([^<]*)(</)')
_COMMENT_RE = re.compile(r'<!--\s*REGEN-COUNT\s+([^\s]+)\s*-->\s*\n?([^\n]*)')
_NUM_IN_LINE_RE = re.compile(r'\b\d[\d,]*(?:\+)?\b')

DYNAMIC_COUNT_PAGES = [
    "index.html",
    "datasets/index.html",
    "addresses/index.html",
    "captures/index.html",
]


def regenerate_dynamic_counts(reg, dry_run=False):
    """Sweep pages for data-count attributes and REGEN-COUNT comments; update in place.

    Preserves everything outside the marked spans / next-line meta values.
    Prints per-page substitution summary."""
    print("Regenerating dynamic counts across derived surfaces …")

    # Seed the source cache with the already-loaded registry so we don't re-read it.
    _SRC_CACHE["registry.json"] = reg

    for page_rel in DYNAMIC_COUNT_PAGES:
        page = REPO_ROOT / page_rel
        if not page.exists():
            print(f"  · {page_rel}: not present (skipped)")
            continue
        html = page.read_text(encoding="utf-8")
        original = html
        substitutions = []

        # Pattern 1: <X data-count="src:path">value</X>
        def _sub_attr(m):
            open_tag, spec, current, close_open = m.group(1), m.group(2), m.group(3), m.group(4)
            try:
                source_name, jsonpath = spec.split(":", 1)
                src = _load_source(source_name)
                value = _resolve_jsonpath(src, jsonpath)
                fresh = _fmt_count(value)
            except Exception as e:
                print(f"  ! {page_rel}: data-count={spec!r} failed — {e}")
                return m.group(0)
            if fresh != current.strip():
                substitutions.append((spec, current.strip(), fresh))
            return f"{open_tag}{fresh}{close_open}"

        html = _ATTR_RE.sub(_sub_attr, html)

        # Pattern 2: <!--REGEN-COUNT src:path-->\n<next line with a number>
        def _sub_comment(m):
            spec, next_line = m.group(1), m.group(2)
            try:
                source_name, jsonpath = spec.split(":", 1)
                src = _load_source(source_name)
                value = _resolve_jsonpath(src, jsonpath)
                fresh = _fmt_count(value)
            except Exception as e:
                print(f"  ! {page_rel}: REGEN-COUNT={spec!r} failed — {e}")
                return m.group(0)
            new_line, replaced = _NUM_IN_LINE_RE.subn(fresh, next_line, count=1)
            if replaced and new_line != next_line:
                substitutions.append((spec, next_line.strip()[:60], fresh))
            return f"<!--REGEN-COUNT {spec}-->\n{new_line}"

        html = _COMMENT_RE.sub(_sub_comment, html)

        if html == original:
            print(f"  · {page_rel}: already canonical")
            continue

        if dry_run:
            print(f"  [DRY] {page_rel}: {len(substitutions)} substitution(s):")
            for spec, old, new in substitutions:
                print(f"      {spec}: '{old}' → '{new}'")
            continue

        _receipt(page)
        page.write_text(html, encoding="utf-8")
        print(f"  ✓ {page_rel}: {len(substitutions)} substitution(s):")
        for spec, old, new in substitutions:
            print(f"      {spec}: {old!r} → {new!r}")


SURFACE_FNS["dynamic-counts"] = regenerate_dynamic_counts


def regenerate_semantic_addresses(reg, dry_run=False):
    """
    Regenerate data/semantic-addresses.json from the six tributaries
    registered in scripts/build_semantic_addresses.py, per the
    EA-SEMANTIC-ADDRESSES-01 framework.

    The `reg` argument is accepted for interface compatibility but not
    used — the Semantic Addresses dataset draws from tributary files
    (mm-main-capture, mm-rf-reception, mm-termindex, mm-mint,
    mm-rf-battery, cha-workplan-870) rather than data/registry.json.
    """
    # Import the reference regenerator's build + emit
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from build_semantic_addresses import build_addresses, emit  # noqa: E402

    sa_path = REPO_ROOT / "data" / "semantic-addresses.json"

    addresses, input_hashes = build_addresses(str(REPO_ROOT))
    payload = emit(addresses, input_hashes)

    if dry_run:
        print(f"  [semantic-addresses] would write {payload['total_addresses']} addresses "
              f"({payload['total_observations']} observations) — {payload['class_counts']}")
        return

    with open(sa_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    _receipt(sa_path, reason="regenerate_surfaces semantic-addresses")
    print(f"  [semantic-addresses] wrote {payload['total_addresses']} addresses "
          f"({payload['total_observations']} observations) — {payload['class_counts']}")


SURFACE_FNS["semantic-addresses"] = regenerate_semantic_addresses


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

# AXN resolution layer — regenerate on every surface pass (added 2026-07-04)
if __name__ == "__main__" and "--dry-run" not in __import__("sys").argv:
    import generate_axn_resolver as _axn
    _axn.main()
