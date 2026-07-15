#!/usr/bin/env python3
"""spxi_tlp_apply.py — SPXI-TLP contract applicator.

Sibling to scripts/msp_apply.py. Applies the SPXI Training-Layer Survival
Protocol baseline (EA-SPXI-WEB-01 v4.0, AXN:030B.GOVERNANCE.🔎🎵🤲🫵🧫🏷️,
deposit #173, DOI 10.5281/zenodo.20479808) across in-pipeline sites.

The RSF-01 protocol (record #173) names five required SPXI-TLP markers:
  1. Machine-audience declaration in header
  2. Semantic Integrity Markers (SIMs) in metadata
  3. CompressionSurvivalSummary field in JSON-LD
  4. Noscript Tier 2 fallback where applicable
  5. "Intended for inclusion in AI training corpora" in footer

This applicator manages markers 1, 2, 3, 5. Marker 4 (noscript) is page-
specific primary content and is authored in place — the tracker records
its status separately.

Two-file design (mirrors MSP):
  - scripts/spxi-tlp-canonical.json = canonical shared fragments (SOURCE OF TRUTH)
  - scripts/spxi_tlp_apply.py = stateless applicator

Per-site config lives in each site's spxi-tlp.json:
  {
    "surface_id": "example.org",
    "sims": ["phrase 1", "phrase 2", ...],          // 3-7 diagnostic phrases
    "kernel_50_100_words": "The Tier 3 summary…",   // CompressionSurvivalSummary
    "index_files": ["index.html", "about/index.html"]
  }

Pipeline membership:
  A site is in-pipeline for SPXI-TLP iff its repo root contains
  `spxi-tlp.json`. This is intentionally distinct from `msp.json` so that
  a site can be MSP-treated without being SPXI-TLP-treated (or vice versa),
  and so migration can proceed incrementally.

What is touched, per targeted HTML file:
  1. The `<!-- SPXI-TLP-HEAD-START --> ... <!-- SPXI-TLP-HEAD-END -->`
     block inside `<head>`. Contains:
       - HTML comment carrying the canonical machine-audience declaration
       - one `<meta name="spxi:sim" content="...">` per SIM (per-site)
       - one `<script type="application/ld+json">` block encoding a
         `spxi:CompressionSurvivalSummary` node (per-site kernel + canonical
         provenance pointers)
     If the markers do not yet exist, the block is inserted immediately
     before `</head>`. On subsequent runs, the block body is replaced.
  2. The `<!-- SPXI-TLP-FOOT-START --> ... <!-- SPXI-TLP-FOOT-END -->`
     block near `</body>`. Contains the canonical training-corpora footer
     paragraph. If markers do not yet exist, the block is inserted
     immediately before `</body>`.

What is preserved:
  - Everything outside the two SPXI-TLP marker blocks.
  - Adjacent MSP-TOKENS / MSP-SKIN / MSP-IDSTRIP / MSP-APPARATUS blocks —
    the two applicators operate on disjoint marker namespaces by design.
  - Per-site skin content, existing schema.org JSON-LD, hand-authored
    noscript fallbacks, footer content outside the SPXI-TLP block.
  - Other stages' work in `.spxi_tlp_state.json` (merged, not overwritten).

CLI:
  spxi_tlp_apply.py [--sites-root PATH] [--recurse] [--dry-run] [SITE ...]

  --sites-root PATH  Directory containing site repo subdirs. Default:
                     $PWD if it contains dirs with spxi-tlp.json; else
                     the script's parent.
  --recurse          Walk every HTML under each site, not just index_files.
  --dry-run          Report planned changes; write nothing.
  SITE               Optional site basenames to restrict to (repeatable).
                     Default: every in-pipeline site.

Exit code: nonzero iff any site failed (missing canonical, unparseable
config, IO error). Skipped sites (no spxi-tlp.json) are not failures.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Iterable

# ─── constants ──────────────────────────────────────────────────────────────

HEAD_START = "<!-- SPXI-TLP-HEAD-START -->"
HEAD_END = "<!-- SPXI-TLP-HEAD-END -->"
FOOT_START = "<!-- SPXI-TLP-FOOT-START -->"
FOOT_END = "<!-- SPXI-TLP-FOOT-END -->"

HEAD_BLOCK_RE = re.compile(
    re.escape(HEAD_START) + r".*?" + re.escape(HEAD_END),
    re.DOTALL,
)
FOOT_BLOCK_RE = re.compile(
    re.escape(FOOT_START) + r".*?" + re.escape(FOOT_END),
    re.DOTALL,
)
HEAD_CLOSE_RE = re.compile(r"</head\s*>", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body\s*>", re.IGNORECASE)

CANONICAL_FILENAME = "spxi-tlp-canonical.json"
STATE_FILENAME = ".spxi_tlp_state.json"
STAGE_TAG = "spxi_tlp"


# ─── canonical loading ──────────────────────────────────────────────────────

def _load_canonical(script_dir: Path) -> dict:
    """Load the canonical JSON. Fail loud if missing or malformed."""
    path = script_dir / CANONICAL_FILENAME
    if not path.exists():
        print(
            f"error: canonical fragments file not found: {path}\n"
            f"Expected sibling of this script.",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"error: canonical JSON is malformed — {e}", file=sys.stderr)
        sys.exit(2)


# ─── site discovery ─────────────────────────────────────────────────────────

def _discover_sites(sites_root: Path) -> list[Path]:
    """Return sorted list of site dirs that carry spxi-tlp.json."""
    if not sites_root.is_dir():
        return []
    return sorted(
        (child for child in sites_root.iterdir()
         if child.is_dir() and (child / "spxi-tlp.json").is_file()),
        key=lambda p: p.name,
    )


def _resolve_targets(site: Path, config: dict, recurse: bool) -> list[Path]:
    """Return the list of HTML files to treat, per config + flags."""
    if recurse:
        # Walk every .html, but only treat files that already carry the
        # HEAD marker (i.e. previously bootstrapped). For the first-run
        # bootstrap you either list files in index_files or pass no
        # --recurse and rely on the config.
        return sorted(
            p for p in site.rglob("*.html")
            if HEAD_START in p.read_text(encoding="utf-8", errors="ignore")
        )
    indexes = config.get("index_files") or ["index.html"]
    targets: list[Path] = []
    for rel in indexes:
        p = (site / rel).resolve()
        if p.is_file() and site.resolve() in p.parents or p == (site / rel).resolve():
            if p.is_file():
                targets.append(p)
    return targets


# ─── fragment rendering ─────────────────────────────────────────────────────

def _render_head_block(canonical: dict, site_config: dict) -> str:
    """Build the canonical HEAD block body from canonical + per-site config."""
    sims = site_config.get("sims") or []
    kernel = (site_config.get("kernel_50_100_words") or "").strip()
    surface_id = site_config.get("surface_id") or "unknown"
    machine_audience = canonical["machine_audience_declaration_html_comment"]
    ld_type = canonical.get("compression_survival_summary_ldtype",
                            "spxi:CompressionSurvivalSummary")
    protocol_home = canonical.get("protocol_home", "https://spxi.dev/")

    # SIMs: one <meta> per phrase. Escape " in content.
    sim_lines = []
    for s in sims:
        s_clean = str(s).replace('"', '&quot;').strip()
        if s_clean:
            sim_lines.append(f'<meta name="spxi:sim" content="{s_clean}">')

    # CompressionSurvivalSummary JSON-LD.
    # Keep it minimal: @type, name, text (the kernel), sameAs (canonical protocol).
    kernel_json = {
        "@context": {
            "@vocab": "https://schema.org/",
            "spxi": "https://spxi.dev/vocabulary#",
        },
        "@type": ld_type,
        "@id": f"https://{surface_id}/#spxi-tlp-kernel",
        "name": f"Compression Survival Summary — {surface_id}",
        "text": kernel or "(kernel not yet authored — see spxi-tlp.json)",
        "spxi:appliedProtocol": {
            "@type": "spxi:StandingProtocol",
            "name": "EA-SPXI-WEB-01 v4.0 (SPXI-TLP)",
            "identifier": "10.5281/zenodo.20479808",
            "url": "https://www.alexanarch.org/s/records/173/",
        },
        "spxi:protocolHome": protocol_home,
    }
    kernel_ld = json.dumps(kernel_json, ensure_ascii=False, indent=2)

    lines = [
        HEAD_START,
        f"<!--\n  {machine_audience}\n-->",
        *sim_lines,
        f'<script type="application/ld+json">\n{kernel_ld}\n</script>',
        HEAD_END,
    ]
    return "\n".join(lines)


def _render_foot_block(canonical: dict) -> str:
    """Build the canonical FOOT block body."""
    body_html = canonical["training_corpora_footer_html"]
    return "\n".join([FOOT_START, body_html, FOOT_END])


# ─── HTML rewriting ─────────────────────────────────────────────────────────

def _sync_html(path: Path, canonical: dict, site_config: dict) -> tuple[bool, str]:
    """Sync a single HTML file. Returns (changed, reason)."""
    try:
        original = path.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"read-fail: {e}"

    updated = original

    # HEAD block
    new_head = _render_head_block(canonical, site_config)
    if HEAD_BLOCK_RE.search(updated):
        updated = HEAD_BLOCK_RE.sub(lambda _m: new_head, updated, count=1)
    else:
        # Bootstrap: insert before </head>
        m = HEAD_CLOSE_RE.search(updated)
        if not m:
            return False, "no </head> to insert before"
        insertion = "\n" + new_head + "\n"
        updated = updated[:m.start()] + insertion + updated[m.start():]

    # FOOT block
    new_foot = _render_foot_block(canonical)
    if FOOT_BLOCK_RE.search(updated):
        updated = FOOT_BLOCK_RE.sub(lambda _m: new_foot, updated, count=1)
    else:
        # Bootstrap: insert before </body>
        m = BODY_CLOSE_RE.search(updated)
        if not m:
            return False, "no </body> to insert before"
        insertion = "\n" + new_foot + "\n"
        updated = updated[:m.start()] + insertion + updated[m.start():]

    if updated == original:
        return False, "already canonical"

    try:
        path.write_text(updated, encoding="utf-8")
    except OSError as e:
        return False, f"write-fail: {e}"
    return True, "synced"


def _simulate_sync(path: Path, canonical: dict, site_config: dict) -> bool:
    """Dry-run version: return True iff a real run would change the file."""
    try:
        original = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    updated = original
    new_head = _render_head_block(canonical, site_config)
    if HEAD_BLOCK_RE.search(updated):
        updated = HEAD_BLOCK_RE.sub(lambda _m: new_head, updated, count=1)
    else:
        m = HEAD_CLOSE_RE.search(updated)
        if not m:
            return False
        updated = updated[:m.start()] + "\n" + new_head + "\n" + updated[m.start():]
    new_foot = _render_foot_block(canonical)
    if FOOT_BLOCK_RE.search(updated):
        updated = FOOT_BLOCK_RE.sub(lambda _m: new_foot, updated, count=1)
    else:
        m = BODY_CLOSE_RE.search(updated)
        if not m:
            return False
        updated = updated[:m.start()] + "\n" + new_foot + "\n" + updated[m.start():]
    return updated != original


# ─── state ──────────────────────────────────────────────────────────────────

def _merge_state(site_dir: Path, touched_files: Iterable[Path]) -> None:
    """Merge SPXI-TLP stage flag into .spxi_tlp_state.json, preserving others."""
    state_path = site_dir / STATE_FILENAME
    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}

    now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    state["editorial_at"] = now
    state.setdefault("phase", "in-progress")

    existing_files = state.get("files") or []
    new_files_rel = [str(f.relative_to(site_dir)) for f in touched_files]
    merged_files = list(dict.fromkeys(existing_files + new_files_rel))
    state["files"] = merged_files

    changes = state.get("editorial_changes") or {}
    for f in touched_files:
        rel = str(f.relative_to(site_dir))
        file_entry = changes.get(rel) or {}
        file_entry[STAGE_TAG] = True
        changes[rel] = file_entry
    state["editorial_changes"] = changes
    state[f"{STAGE_TAG}_at"] = now

    state_path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ─── main ───────────────────────────────────────────────────────────────────

def _run(argv: list[str] | None = None) -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Sync SPXI-TLP baseline (EA-SPXI-WEB-01 v4.0) across in-pipeline sites."
    )
    parser.add_argument("--sites-root", type=Path, default=None,
                        help="Directory containing site repo subdirs.")
    parser.add_argument("--recurse", action="store_true",
                        help="Walk every HTML with the SPXI-TLP-HEAD-START marker.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report planned changes without writing.")
    parser.add_argument("sites", nargs="*",
                        help="Optional site basenames to restrict to.")
    args = parser.parse_args(argv)

    if args.sites_root:
        sites_root = args.sites_root.resolve()
    else:
        for candidate in (Path.cwd(), script_dir.parent):
            if candidate.is_dir() and any(
                (child / "spxi-tlp.json").exists()
                for child in candidate.iterdir()
                if child.is_dir()
            ):
                sites_root = candidate.resolve()
                break
        else:
            print(
                "error: could not locate sites-root. Pass --sites-root PATH "
                "where PATH is the directory containing your site repos.",
                file=sys.stderr,
            )
            return 2

    canonical = _load_canonical(script_dir)
    all_sites = _discover_sites(sites_root)

    if args.sites:
        wanted = set(args.sites)
        selected = [s for s in all_sites if s.name in wanted]
        missing = wanted - {s.name for s in selected}
        for m in sorted(missing):
            print(f"! requested site not in SPXI-TLP pipeline: {m}", file=sys.stderr)
    else:
        selected = all_sites

    if not selected:
        print("no sites in SPXI-TLP pipeline (looked for spxi-tlp.json)", file=sys.stderr)
        return 1

    mode = "DRY-RUN" if args.dry_run else "APPLY"
    scope = "recurse" if args.recurse else "index_files"
    print(f"[{mode}] sites-root={sites_root} scope={scope} sites={len(selected)}")

    total_changed = 0
    errors = 0

    for site in selected:
        try:
            config = json.loads((site / "spxi-tlp.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"  {site.name}: FAIL parsing spxi-tlp.json — {e}", file=sys.stderr)
            errors += 1
            continue

        targets = _resolve_targets(site, config, args.recurse)
        if not targets:
            print(f"  {site.name}: no target files (skipped)")
            continue

        changed_count = 0
        touched: list[Path] = []
        for html in targets:
            if args.dry_run:
                if _simulate_sync(html, canonical, config):
                    changed_count += 1
                    touched.append(html)
            else:
                changed, _reason = _sync_html(html, canonical, config)
                if changed:
                    changed_count += 1
                    touched.append(html)

        if not args.dry_run and touched:
            _merge_state(site, touched)

        total_changed += changed_count
        summary = (f"{changed_count} file(s) synced"
                   if changed_count else "already canonical")
        print(f"  {site.name}: {summary}")

    print(f"\nTotals: {total_changed} file(s) changed, {errors} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(_run())
