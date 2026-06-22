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

ALL_SURFACES = ["browse", "browse-index", "chunks", "sitemap", "sha256sums"]


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
    with open(target, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"  ✓ SHA256SUMS.txt ({len(lines)} lines, {len(out):,} bytes)")


# ──────────────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────────────

SURFACE_FNS = {
    "browse": regenerate_browse,
    "browse-index": regenerate_browse_index,
    "chunks": regenerate_chunks,
    "sitemap": regenerate_sitemap,
    "sha256sums": regenerate_sha256sums,
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
