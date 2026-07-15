#!/usr/bin/env python3
"""msp_apply.py — Mandala Surface Protocol contract applicator.

Syncs the canonical MSP-TOKENS block (the shared apparatus contract) to
every in-pipeline site. The canonical source of truth is a single file,
`msp-tokens-canonical.css`, colocated with this script. Editing the
contract means editing that one file; re-running this script propagates
the change everywhere.

Pipeline membership:
  A site is in-pipeline iff its repo root contains `msp.json`. Sites
  without `msp.json` (e.g. platform-erosion-observatory, the original
  test-case surface) are ignored entirely.

Scope per site:
  By default, only files listed in `msp.json["index_files"]` are touched,
  matching the original applicator's contract. Pass `--recurse` to walk
  every HTML file under the site (useful when subpages carry the MSP block
  via a build script or hand-authored copy).

What is touched:
  1. The `/* MSP-TOKENS-START */ ... /* MSP-TOKENS-END */` block inside
     each targeted HTML file. Only the body between the markers is
     replaced with the canonical body; the markers themselves are kept.
  2. `assets/msp-tokens.css` (if present) is overwritten with the
     canonical body verbatim (no markers — the vendored file IS the body).

What is preserved:
  - Everything outside the MSP-TOKENS block, including any adjacent
    `/* MSP-SKIN-START */ ... /* MSP-SKIN-END */` block (which lives
    outside the applicator's overwrite region by design, so per-site
    skin tuning survives every re-sync).
  - Other stages' work: `.msp_state.json` is MERGED, not overwritten;
    keys like `idstrip`, `apparatus`, `link_typing`, `lemmas`, `helix`
    stay intact.

CLI:
  msp_apply.py [--sites-root PATH] [--recurse] [--dry-run] [SITE ...]

  --sites-root PATH  Directory containing site repo subdirs. Default:
                     $PWD, then the parent of this script if that fails.
  --recurse          Walk every HTML under each site, not just index_files.
  --dry-run          Report planned changes; write nothing.
  SITE               Optional site basenames to restrict to (repeatable).
                     Default: every in-pipeline site.

Exit code: nonzero iff any site failed (missing canonical, unparseable
msp.json, IO error). Skipped sites (no msp.json, no markers found) are
not failures.

The `tokens` stage this script owns is stage 1 of the full applicator.
The other stages (idstrip, apparatus, link_typing, lemmas, helix) are
not yet re-implemented in this reconstruction — they must be added
before a full editorial pass can be reproduced. This script marks
`editorial_changes[file]["tokens"] = True` in the state file so a
downstream orchestrator can see which stage last touched each file.
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

TOKENS_START = "/* MSP-TOKENS-START */"
TOKENS_END = "/* MSP-TOKENS-END */"
SKIN_START = "/* MSP-SKIN-START"
SKIN_END = "/* MSP-SKIN-END */"

# Regex that matches the full MSP-TOKENS block including markers. Anchored
# on the literal markers to avoid pulling in adjacent regions by accident.
TOKENS_BLOCK_RE = re.compile(
    re.escape(TOKENS_START) + r".*?" + re.escape(TOKENS_END),
    re.DOTALL,
)

STATE_FILENAME = ".msp_state.json"
VENDORED_CSS_PATH = "assets/msp-tokens.css"
CANONICAL_FILENAME = "msp-tokens-canonical.css"

SKIP_DIR_PARTS = (".git", "node_modules", "dist", ".next", ".vercel", "build")


# ─── helpers ────────────────────────────────────────────────────────────────


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def _load_canonical(script_dir: Path) -> str:
    """Read the canonical MSP-TOKENS body from the sibling file."""
    canonical = script_dir / CANONICAL_FILENAME
    if not canonical.exists():
        raise FileNotFoundError(
            f"canonical body not found at {canonical}. This file is the source "
            "of truth for the MSP-TOKENS contract; the applicator refuses to "
            "run without it."
        )
    body = canonical.read_text(encoding="utf-8")
    # Sanity: canonical must not contain the START/END markers — those are
    # applied by this script when it wraps the body for HTML injection.
    if TOKENS_START in body or TOKENS_END in body:
        raise ValueError(
            f"{canonical} must contain body only, not the START/END markers"
        )
    return body


def _discover_sites(sites_root: Path) -> list[Path]:
    """Return in-pipeline site dirs (those with an msp.json at their root)."""
    return sorted(
        d
        for d in sites_root.iterdir()
        if d.is_dir() and (d / "msp.json").exists()
    )


def _resolve_targets(
    site_dir: Path, msp_config: dict, recurse: bool
) -> list[Path]:
    """Return the HTML files this site's `tokens` stage should touch."""
    if recurse:
        found: list[Path] = []
        for html in site_dir.rglob("*.html"):
            if any(part in html.parts for part in SKIP_DIR_PARTS):
                continue
            try:
                text = html.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if TOKENS_START in text:
                found.append(html)
        return sorted(found)
    # Default: msp.json["index_files"], resolved relative to site root.
    files = msp_config.get("index_files") or []
    return [site_dir / f for f in files if (site_dir / f).exists()]


def _sync_html(path: Path, canonical_body: str) -> tuple[bool, str]:
    """Replace the MSP-TOKENS block body in `path`. Returns (changed, reason)."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"read error: {e}"

    match = TOKENS_BLOCK_RE.search(text)
    if not match:
        return False, "no MSP-TOKENS block (skipped)"

    new_block = f"{TOKENS_START}\n{canonical_body.rstrip()}\n{TOKENS_END}"
    new_text = text[: match.start()] + new_block + text[match.end():]

    if new_text == text:
        return False, "already canonical"

    path.write_text(new_text, encoding="utf-8")
    return True, "tokens block synced"


def _sync_vendored_css(site_dir: Path, canonical_body: str) -> tuple[bool, str]:
    """Overwrite site's vendored assets/msp-tokens.css with the canonical body."""
    css_path = site_dir / VENDORED_CSS_PATH
    if not css_path.exists():
        return False, "no vendored css (skipped)"
    current = css_path.read_text(encoding="utf-8")
    if current == canonical_body:
        return False, "already canonical"
    css_path.write_text(canonical_body, encoding="utf-8")
    return True, "vendored css synced"


def _merge_state(
    site_dir: Path,
    touched_files: list[Path],
    stage_tag: str = "tokens",
) -> None:
    """Merge tokens-stage output into the site's .msp_state.json.

    Preserves fields written by other stages. Never truncates or removes
    keys we didn't set here — this stage is one of many.
    """
    state_path = site_dir / STATE_FILENAME
    state: dict = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # Corrupt state — better to warn and rebuild than silently pave over
            print(f"    ! {state_path} unreadable; rewriting", file=sys.stderr)
            state = {}

    now = _now_iso()
    state["editorial_at"] = now
    state.setdefault("phase", "in-progress")

    # `files`: union of prior scope and this run's scope, string-relative
    existing_files = state.get("files") or []
    new_files_rel = [str(f.relative_to(site_dir)) for f in touched_files]
    merged_files = list(dict.fromkeys(existing_files + new_files_rel))
    state["files"] = merged_files

    # editorial_changes: merge per-file, only setting our stage's flag.
    changes = state.get("editorial_changes") or {}
    for f in touched_files:
        rel = str(f.relative_to(site_dir))
        file_entry = changes.get(rel) or {}
        file_entry[stage_tag] = True
        changes[rel] = file_entry
    state["editorial_changes"] = changes

    state[f"{stage_tag}_at"] = now
    state_path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ─── main ───────────────────────────────────────────────────────────────────


def _run(argv: list[str] | None = None) -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Sync canonical MSP-TOKENS contract across in-pipeline sites."
    )
    parser.add_argument(
        "--sites-root",
        type=Path,
        default=None,
        help="Directory containing site repo subdirs. Default: $PWD if it "
             "contains site dirs with msp.json; otherwise the script's parent.",
    )
    parser.add_argument(
        "--recurse",
        action="store_true",
        help="Walk every HTML file under each site (not just index_files).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report planned changes without writing.",
    )
    parser.add_argument(
        "sites",
        nargs="*",
        help="Optional site basenames to restrict to. Default: all in-pipeline.",
    )
    args = parser.parse_args(argv)

    # Locate sites_root: explicit > cwd > script-parent
    if args.sites_root:
        sites_root = args.sites_root.resolve()
    else:
        for candidate in (Path.cwd(), script_dir.parent):
            if any(
                (child / "msp.json").exists()
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

    canonical_body = _load_canonical(script_dir)

    all_sites = _discover_sites(sites_root)
    if args.sites:
        wanted = set(args.sites)
        selected = [s for s in all_sites if s.name in wanted]
        missing = wanted - {s.name for s in selected}
        for m in sorted(missing):
            print(f"! requested site not in pipeline: {m}", file=sys.stderr)
    else:
        selected = all_sites

    if not selected:
        print("no sites to process", file=sys.stderr)
        return 1

    mode = "DRY-RUN" if args.dry_run else "APPLY"
    scope = "recurse" if args.recurse else "index_files"
    print(f"[{mode}] sites-root={sites_root} scope={scope} sites={len(selected)}")

    total_html_changed = 0
    total_css_changed = 0
    errors = 0

    for site in selected:
        try:
            msp_config = json.loads((site / "msp.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"  {site.name}: FAIL parsing msp.json — {e}", file=sys.stderr)
            errors += 1
            continue

        targets = _resolve_targets(site, msp_config, args.recurse)
        if not targets:
            print(f"  {site.name}: no target files (skipped)")
            continue

        html_changed = 0
        touched: list[Path] = []
        for html in targets:
            if args.dry_run:
                # Simulate to see if a real run would change the file
                current = html.read_text(encoding="utf-8", errors="replace")
                match = TOKENS_BLOCK_RE.search(current)
                if not match:
                    continue
                simulated = (
                    current[: match.start()]
                    + f"{TOKENS_START}\n{canonical_body.rstrip()}\n{TOKENS_END}"
                    + current[match.end():]
                )
                if simulated != current:
                    html_changed += 1
                    touched.append(html)
            else:
                changed, _reason = _sync_html(html, canonical_body)
                if changed:
                    html_changed += 1
                    touched.append(html)

        # Vendored CSS
        css_changed = False
        if args.dry_run:
            css_path = site / VENDORED_CSS_PATH
            if css_path.exists():
                css_changed = css_path.read_text(encoding="utf-8") != canonical_body
        else:
            css_changed, _ = _sync_vendored_css(site, canonical_body)

        if not args.dry_run and touched:
            _merge_state(site, touched)

        total_html_changed += html_changed
        total_css_changed += 1 if css_changed else 0

        parts = []
        if html_changed:
            parts.append(f"{html_changed} html")
        if css_changed:
            parts.append("+ vendored css")
        summary = ", ".join(parts) if parts else "already canonical"
        print(f"  {site.name}: {summary}")

    print(
        f"\nTotals: {total_html_changed} html changed, "
        f"{total_css_changed} vendored css changed, {errors} error(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(_run())
