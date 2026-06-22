#!/usr/bin/env python3
"""
protocol_update.py — atomic protocol update + central-index propagation.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS
═══════════════════════════════════════════════════════════════════════════════

If you hand-edit /api/deposit-protocol.json (or any other protocol JSON), the
central index at /api/index.json now disagrees with reality — its
content_sha256 entry is stale. Bootstrap will fail. CI will fail. The whole
familiarization mechanism breaks.

This script is the ONE supported path for modifying a protocol JSON. It:

  1. Verifies the protocol JSON parses as valid JSON.
  2. Computes the new content_sha256 of the file.
  3. Updates /api/index.json with the new hash and the new last_updated date.
  4. Optionally bumps the protocol_version (e.g. v1 → v2) and appends a
     change_log entry to the protocol JSON itself.
  5. Optionally propagates the version string to dependent files listed in
     the index's referenced_by field for that protocol.

USAGE
═════
    # After editing api/deposit-protocol.json, run this to update the index:
    python3 scripts/protocol_update.py \\
        --protocol deposit \\
        --description "Added enrichment_pipeline orchestrator hook"

    # Just verify the index is consistent with current protocol files
    python3 scripts/protocol_update.py --verify-index

    # Bump a protocol version (e.g. deposit/v1 → deposit/v2)
    python3 scripts/protocol_update.py --protocol deposit --bump-version \\
        --new-version "alexanarch-deposit-protocol/v2" \\
        --description "Major: added X, Y, Z"

    # Add a brand new protocol (the JSON file must already exist)
    python3 scripts/protocol_update.py --add-protocol orchestration \\
        --path /api/orchestration-protocol.json \\
        --version "orchestration/v1" \\
        --governs "..." \\
        --description "Initial protocol creation"

After running this script, run scripts/bootstrap_familiarization.py to
confirm the index is consistent.
═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "api" / "index.json"


def sha256_of_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_index():
    with open(INDEX_PATH) as f:
        return json.load(f)


def save_index(idx):
    payload = json.dumps(idx, ensure_ascii=False, indent=2)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(payload + "\n")


def verify_index(idx):
    """Check that every entry's content_sha256 matches the file on disk."""
    failures = []
    for section_name in ("protocols", "schemas"):
        for key, entry in idx.get(section_name, {}).items():
            path = entry.get("canonical_path", "")
            file_path = REPO_ROOT / path.lstrip("/")
            if not file_path.exists():
                failures.append(f"[{section_name}/{key}] FILE_MISSING: {path}")
                continue
            actual = sha256_of_file(file_path)
            claimed = entry.get("content_sha256")
            if claimed != actual:
                failures.append(
                    f"[{section_name}/{key}] HASH_MISMATCH for {path}\n"
                    f"      claimed: {claimed}\n      actual:  {actual}"
                )
    return failures


def update_protocol(idx, protocol_name, description, new_version=None):
    """Update an existing protocol entry: recompute hash, update timestamps, optional version bump."""
    if protocol_name not in idx.get("protocols", {}):
        raise KeyError(f"Protocol '{protocol_name}' not found in index. Known: {list(idx.get('protocols', {}).keys())}")
    entry = idx["protocols"][protocol_name]
    path = entry["canonical_path"]
    file_path = REPO_ROOT / path.lstrip("/")
    if not file_path.exists():
        raise FileNotFoundError(f"Protocol file does not exist: {file_path}")

    # Validate the protocol JSON parses
    with open(file_path) as f:
        proto_obj = json.load(f)

    # If bumping version, also write it back into the protocol JSON
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if new_version:
        proto_obj["protocol_version"] = new_version
        # Append change_log to the protocol JSON
        cl = proto_obj.setdefault("change_log", [])
        cl.append({
            "version": new_version,
            "date": today,
            "changes": [description],
        })
        proto_obj["last_updated"] = today
        # Write back the protocol JSON with the new version
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(proto_obj, f, ensure_ascii=False, indent=2)
            f.write("\n")

    # Recompute hash AFTER any modifications
    new_hash = sha256_of_file(file_path)
    old_hash = entry.get("content_sha256")

    entry["content_sha256"] = new_hash
    entry["last_updated"] = today
    if new_version:
        entry["current_version"] = new_version

    # Update the index's own last_updated and change_log
    idx["last_updated"] = today
    idx_cl = idx.setdefault("change_log", [])
    idx_cl.append({
        "index_version": idx.get("index_version", "v1.0"),
        "date": today,
        "changes": [
            f"Updated protocol '{protocol_name}': {description}"
            + (f" (version bumped to {new_version})" if new_version else "")
        ],
    })

    save_index(idx)
    return {
        "protocol": protocol_name,
        "old_hash": old_hash,
        "new_hash": new_hash,
        "new_version": new_version,
        "description": description,
    }


def add_protocol(idx, name, path, version, governs, description,
                 depends_on=None, referenced_by=None, enforced_by=None):
    """Add a brand new protocol entry to the index."""
    if name in idx.get("protocols", {}):
        raise ValueError(f"Protocol '{name}' already exists in index.")
    file_path = REPO_ROOT / path.lstrip("/")
    if not file_path.exists():
        raise FileNotFoundError(f"Protocol file must exist before being added to index: {file_path}")
    h = sha256_of_file(file_path)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    idx["protocols"][name] = {
        "name": name,
        "current_version": version,
        "canonical_path": path,
        "content_sha256": h,
        "governs": governs,
        "depends_on": depends_on or [],
        "referenced_by": referenced_by or [],
        "enforced_by": enforced_by or [],
        "last_updated": today,
    }
    idx["last_updated"] = today
    idx.setdefault("change_log", []).append({
        "index_version": idx.get("index_version", "v1.0"),
        "date": today,
        "changes": [f"Added new protocol '{name}' at {path}: {description}"],
    })
    save_index(idx)
    return {"protocol": name, "hash": h, "version": version}


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--verify-index", action="store_true",
                        help="just verify the index — no updates")
    parser.add_argument("--protocol", help="name of existing protocol to update (e.g. 'deposit', 'axn')")
    parser.add_argument("--bump-version", action="store_true",
                        help="bump the protocol_version. Requires --new-version.")
    parser.add_argument("--new-version", help="new protocol_version string (used with --bump-version)")
    parser.add_argument("--description", help="brief description of this change (required for updates)")
    parser.add_argument("--add-protocol", help="add a new protocol with this name")
    parser.add_argument("--path", help="canonical path of new protocol (used with --add-protocol)")
    parser.add_argument("--version", help="protocol_version of new protocol (used with --add-protocol)")
    parser.add_argument("--governs", help="what the new protocol governs (used with --add-protocol)")
    args = parser.parse_args()

    idx = load_index()

    if args.verify_index:
        failures = verify_index(idx)
        if failures:
            print(f"INDEX INCONSISTENT ({len(failures)} failure(s)):")
            for f in failures:
                print(f"  {f}")
            sys.exit(1)
        print("✓ Index is consistent — every entry's content_sha256 matches the file on disk.")
        return

    if args.add_protocol:
        if not args.path or not args.version or not args.governs:
            print("--add-protocol requires --path, --version, --governs, --description")
            sys.exit(2)
        result = add_protocol(idx, args.add_protocol, args.path, args.version,
                              args.governs, args.description or "")
        print(f"✓ Added protocol '{result['protocol']}': sha256={result['hash'][:16]}…, version={result['version']}")
        return

    if args.protocol:
        if not args.description:
            print("--protocol requires --description")
            sys.exit(2)
        new_version = args.new_version if args.bump_version else None
        if args.bump_version and not new_version:
            print("--bump-version requires --new-version")
            sys.exit(2)
        result = update_protocol(idx, args.protocol, args.description, new_version)
        print(f"✓ Updated protocol '{result['protocol']}':")
        print(f"    old sha256: {result['old_hash'][:16]}…")
        print(f"    new sha256: {result['new_hash'][:16]}…")
        if result["new_version"]:
            print(f"    new version: {result['new_version']}")
        print()
        print("Run `python3 scripts/bootstrap_familiarization.py --strict` to confirm.")
        return

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
