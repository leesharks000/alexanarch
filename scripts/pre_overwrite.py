#!/usr/bin/env python3
"""
pre_overwrite.py — produce a structural inventory receipt before overwriting an existing file.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS
═══════════════════════════════════════════════════════════════════════════════

Commit `729dfd9` overwrote /s/wiki/index.html and /s/graph/index.html with
static replacements, having mistaken them for stubs without inspecting the
DYNAMIC canonical primaries at /wiki/ and /graph/. The recovery commit
`49864f4` had to re-derive the lost work.

The post-mortem standing directive: make the failure pattern impossible at
the file-system level, not as a discipline that has to be maintained across
instances.

This script is the structural pause. An instance about to overwrite a file
MUST first run:

    python3 scripts/pre_overwrite.py <path>

It does three things:

  1. Reads the current file. Computes sha256, size, line count, type-infer.
  2. Looks up the path in api/index.json. If the path or its parent surface
     has role metadata (primary / static_fallback / derived_enrichment / ...)
     the script SURFACES that role and any companion_to relationship LOUDLY
     in stdout. This is where the 729dfd9 failure would have been caught —
     the instance would have been told "this is the static_fallback for
     /wiki/; the canonical primary is at /wiki/index.html" before writing.
  3. Appends a receipt to data/pre-overwrite-receipts.log (JSONL, append-only).

The receipt entry pins {timestamp, actor, path, sha256, size, role,
companion_to, instance_id} so subsequent guards (overwrite_guard.require_receipt)
can verify a fresh receipt exists with matching sha256 before the actual write.

═══════════════════════════════════════════════════════════════════════════════
USAGE
═══════════════════════════════════════════════════════════════════════════════

    # Standard: print inventory + warnings, append receipt, exit 0
    python3 scripts/pre_overwrite.py /home/claude/alexanarch/wiki/index.html

    # JSON-only output (for tooling)
    python3 scripts/pre_overwrite.py wiki/index.html --json

    # Specify the actor (default: 'instance')
    python3 scripts/pre_overwrite.py file --actor regenerate_surfaces

    # Set the instance label that will appear in the receipt
    python3 scripts/pre_overwrite.py file --instance "TACHYON 20260622-PM"

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
RECEIPT_LOG = REPO_ROOT / "data" / "pre-overwrite-receipts.log"
INDEX_PATH = REPO_ROOT / "api" / "index.json"

# ANSI color codes for stdout warnings
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BOLD = "\033[1m"
RESET = "\033[0m"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def infer_role(canonical_path: str, index: dict) -> dict:
    """Walk api/index.json looking for any entry whose canonical_path matches.
    Returns dict with role, companion_to, section, and any other metadata found."""
    result = {"role": None, "companion_to": None, "section": None, "shows": None}
    if not index:
        return result
    # The canonical_path we look for is relative to the repo root, web-rooted
    # (e.g. /wiki/index.html or /data/registry.json).
    targets_to_try = [canonical_path]
    # If absolute path passed, also try the web-rooted form
    if canonical_path.startswith("/"):
        pass  # already web-rooted
    sections_to_walk = ["protocols", "schemas", "registries", "derived_surfaces", "scripts"]
    for section in sections_to_walk:
        block = index.get(section, {})
        if not isinstance(block, dict):
            continue
        for entry_name, entry in block.items():
            if not isinstance(entry, dict):
                continue
            entry_path = entry.get("canonical_path", "")
            if entry_path in targets_to_try or entry_path.lstrip("/") in [t.lstrip("/") for t in targets_to_try]:
                result["section"] = section
                result["entry_name"] = entry_name
                result["role"] = entry.get("role")
                result["companion_to"] = entry.get("companion_to")
                result["shows"] = entry.get("shows") or entry.get("purpose") or entry.get("description")
                return result
    return result


def find_companion_primary(canonical_path: str, index: dict) -> dict:
    """If the target is a static_fallback, find the role=primary companion that
    shares the same conceptual surface. The 729dfd9 failure pattern.
    Returns dict with the primary's canonical_path if a sibling exists, else empty."""
    result = {}
    if not index:
        return result
    derived = index.get("derived_surfaces", {})
    if not isinstance(derived, dict):
        return result
    # Find the target entry
    target_role = None
    target_concept = None  # e.g. 'wiki' from '/s/wiki/' or '/wiki/'
    for entry_name, entry in derived.items():
        if not isinstance(entry, dict):
            continue
        if entry.get("canonical_path") == canonical_path:
            target_role = entry.get("role")
            # Try to extract conceptual name: 'wiki_html' → 'wiki', 'wiki_dynamic' → 'wiki'
            target_concept = entry_name.split("_")[0]
            break
    if not target_concept or target_role != "static_fallback":
        return result
    # Look for a sibling with same concept but role=primary
    for entry_name, entry in derived.items():
        if not isinstance(entry, dict):
            continue
        sibling_concept = entry_name.split("_")[0]
        if sibling_concept == target_concept and entry.get("role") == "primary" and entry.get("canonical_path") != canonical_path:
            result["primary_path"] = entry.get("canonical_path")
            result["primary_entry"] = entry_name
            result["primary_shows"] = entry.get("shows")
            return result
    return result


def web_root_path(abs_or_rel: str) -> str:
    """Normalize an arbitrary path to a web-rooted form like /wiki/index.html."""
    p = Path(abs_or_rel)
    try:
        rel = p.resolve().relative_to(REPO_ROOT)
        return "/" + str(rel)
    except (ValueError, FileNotFoundError):
        # Path doesn't resolve under REPO_ROOT (or doesn't exist); return as-is
        s = str(p)
        if s.startswith("/"):
            return s
        return "/" + s.lstrip("./")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="Path to the file about to be overwritten")
    parser.add_argument("--actor", default="instance", help="Who is issuing the receipt (default: instance)")
    parser.add_argument("--instance", default=os.environ.get("ALEXANARCH_INSTANCE_ID", "unspecified"),
                        help="Instance identifier (e.g. 'TACHYON 20260622-PM')")
    parser.add_argument("--json", action="store_true", help="Print inventory as JSON only (suppress narrative output)")
    parser.add_argument("--reason", default=None, help="Brief reason for the planned overwrite")
    parser.add_argument("--silent-on-missing", action="store_true",
                        help="If target file does not exist, exit 0 silently (this is a CREATE, not an overwrite)")
    args = parser.parse_args()

    abs_path = Path(args.path).resolve() if not Path(args.path).is_absolute() else Path(args.path)
    web_path = web_root_path(args.path)

    if not abs_path.exists():
        if args.silent_on_missing:
            sys.exit(0)
        if args.json:
            print(json.dumps({"status": "file_does_not_exist", "path": str(abs_path)}))
        else:
            print(f"{GREEN}[pre_overwrite]{RESET} File does not exist: {abs_path}")
            print(f"  → No overwrite to inventory. This is a CREATE operation, which is safe by default.")
        sys.exit(0)

    if not abs_path.is_file():
        print(f"{RED}[pre_overwrite] ERROR{RESET}: {abs_path} is not a regular file.", file=sys.stderr)
        sys.exit(2)

    # --- Inventory ---
    size = abs_path.stat().st_size
    sha = file_sha256(abs_path)
    try:
        text = abs_path.read_text(encoding="utf-8")
        line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
        head_excerpt = "\n".join(text.splitlines()[:5])
        is_binary = False
    except UnicodeDecodeError:
        line_count = None
        head_excerpt = "(binary file)"
        is_binary = True

    # --- Lookup role in api/index.json ---
    index = {}
    if INDEX_PATH.exists():
        try:
            index = json.loads(INDEX_PATH.read_text())
        except json.JSONDecodeError:
            pass

    role_info = infer_role(web_path, index)
    companion_primary = find_companion_primary(web_path, index)

    # --- Build receipt ---
    receipt = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "actor": args.actor,
        "instance_id": args.instance,
        "path": str(abs_path),
        "web_path": web_path,
        "sha256": sha,
        "size_bytes": size,
        "line_count": line_count,
        "is_binary": is_binary,
        "role": role_info.get("role"),
        "section": role_info.get("section"),
        "entry_name": role_info.get("entry_name"),
        "companion_to": role_info.get("companion_to"),
        "primary_companion": companion_primary.get("primary_path"),
        "reason": args.reason,
    }

    # --- Append to log ---
    RECEIPT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(RECEIPT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(receipt, ensure_ascii=False) + "\n")

    # --- Output ---
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False))
        return

    print(f"{BOLD}[pre_overwrite]{RESET} Receipt issued.")
    print(f"  Path:        {abs_path}")
    print(f"  Web path:    {web_path}")
    print(f"  Size:        {size:,} bytes" + (f", {line_count:,} lines" if line_count is not None else ", binary"))
    print(f"  SHA-256:     {sha[:24]}…")
    print(f"  Actor:       {args.actor}  ({args.instance})")

    # The visible pause moment — surface role + companion warnings
    print()
    print(f"{BOLD}=== STRUCTURAL CONTEXT ==={RESET}")

    if role_info.get("role"):
        print(f"  Role:        {BOLD}{role_info['role']}{RESET}")
        print(f"  Section:     {role_info.get('section')}")
        print(f"  Entry:       {role_info.get('entry_name')}")
        if role_info.get("companion_to"):
            print(f"  Companion:   {role_info.get('companion_to')}")
        if role_info.get("shows"):
            shows = role_info["shows"]
            shows_short = shows[:200] + "…" if len(shows) > 200 else shows
            print(f"  Description: {shows_short}")
    else:
        print(f"  Not registered in api/index.json. Treat with extra caution if this is")
        print(f"  a load-bearing path (top-level pages, /api/*, /scripts/*).")

    # The 729dfd9 alarm — if this is a static_fallback, scream about the primary
    if role_info.get("role") == "static_fallback" and companion_primary.get("primary_path"):
        print()
        print(f"{RED}{BOLD}╔══════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{RED}{BOLD}║  WARNING — STATIC FALLBACK                                           ║{RESET}")
        print(f"{RED}{BOLD}╠══════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{RED}║  You are about to overwrite a STATIC FALLBACK surface.               {RESET}")
        print(f"{RED}║  The CANONICAL PRIMARY for this concept lives at:                    {RESET}")
        print(f"{RED}║    {BOLD}{companion_primary['primary_path']}{RESET}{RED}                                                   {RESET}")
        print(f"{RED}║                                                                      {RESET}")
        print(f"{RED}║  This is the 729dfd9 failure pattern. If your intent is to extend    {RESET}")
        print(f"{RED}║  the surface, EDIT THE PRIMARY, not the fallback. The fallback is    {RESET}")
        print(f"{RED}║  REGENERATED FROM SOURCE and your changes here will be overwritten   {RESET}")
        print(f"{RED}║  on next regenerate_surfaces.py run.                                 {RESET}")
        print(f"{RED}{BOLD}╚══════════════════════════════════════════════════════════════════════╝{RESET}")

    print()
    print(f"{GREEN}Receipt logged to data/pre-overwrite-receipts.log{RESET}")
    print(f"  → Subsequent write-path scripts (regenerate_surfaces, etc.) can now verify")
    print(f"    a fresh receipt exists with matching sha256 before allowing the write.")


if __name__ == "__main__":
    main()
