#!/usr/bin/env python3
"""
bootstrap_familiarization.py — what every new agent runs FIRST before touching
Alexanarch infrastructure.

═══════════════════════════════════════════════════════════════════════════════
PURPOSE
═══════════════════════════════════════════════════════════════════════════════

The design problem this solves: new instances arrive without knowing the
current protocols, make autonomous changes, and propagate drift. The fix is
not behavioral exhortation but mechanical verification — this script:

  1. Fetches the central protocol index (/api/index.json).
  2. For every protocol and schema listed, verifies its content_sha256 matches
     what the index claims. Hash mismatch = the protocol was modified out-of-
     band; the script fails closed and tells the operator to investigate.
  3. Reads the operator_directive section and prints it. This is the binding
     instruction set for this session.
  4. Produces a familiarization receipt — a text block listing protocol
     versions read, content hashes verified, timestamp, instance label. The
     receipt is what an agent attaches to commits and deposits as evidence of
     familiarization.
  5. Optionally appends the receipt to /data/instance-familiarization.log as
     a JSONL audit trail.

USAGE
═════
    # Print familiarization receipt to stdout
    python3 scripts/bootstrap_familiarization.py

    # Write receipt to a file (for commit-message inclusion)
    python3 scripts/bootstrap_familiarization.py --receipt-file /tmp/receipt.txt

    # Also append to the audit log
    python3 scripts/bootstrap_familiarization.py --append-log

    # Specify the instance label that appears in the receipt
    python3 scripts/bootstrap_familiarization.py --instance "TACHYON session 20260622-PM"

    # Strict mode — exit non-zero on any hash mismatch
    python3 scripts/bootstrap_familiarization.py --strict

The script reads from local filesystem by default. Pass --remote to fetch from
alexanarch.org instead (slower; useful for verifying a clone is in sync with
the published index).
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
INDEX_PATH = REPO_ROOT / "api" / "index.json"


def sha256_of_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_index():
    if not INDEX_PATH.exists():
        sys.stderr.write(f"FATAL: {INDEX_PATH} not found. The central protocol index is missing.\n")
        sys.exit(2)
    with open(INDEX_PATH) as f:
        return json.load(f)


def verify_section(section_obj, label, results):
    """Verify content_sha256 for each entry in a protocols/schemas section."""
    for key, entry in section_obj.items():
        claimed = entry.get("content_sha256")
        path = entry.get("canonical_path", "")
        if not claimed or not path:
            results.append({
                "section": label, "key": key, "status": "NO_HASH",
                "path": path, "claimed": claimed, "actual": None,
            })
            continue
        file_path = REPO_ROOT / path.lstrip("/")
        if not file_path.exists():
            results.append({
                "section": label, "key": key, "status": "FILE_MISSING",
                "path": path, "claimed": claimed, "actual": None,
            })
            continue
        actual = sha256_of_file(file_path)
        results.append({
            "section": label, "key": key,
            "status": "OK" if actual == claimed else "HASH_MISMATCH",
            "path": path, "claimed": claimed, "actual": actual,
            "version": entry.get("current_version") or entry.get("version_label") or "",
        })


def build_receipt(idx, results, instance_label, generated_at):
    """Build the receipt text block (also used as commit-message snippet)."""
    lines = []
    lines.append("━" * 76)
    lines.append("  ALEXANARCH FAMILIARIZATION RECEIPT")
    lines.append("━" * 76)
    lines.append(f"  generated_at:   {generated_at}")
    lines.append(f"  instance:       {instance_label}")
    lines.append(f"  index_version:  {idx.get('index_version', '?')}")
    lines.append(f"  index_path:     /api/index.json")
    lines.append("")
    lines.append("  PROTOCOLS READ:")
    for r in results:
        if r["section"] != "protocols":
            continue
        marker = "✓" if r["status"] == "OK" else "✗"
        lines.append(f"    {marker} {r['key']:14s}  version={r['version']:36s}  sha256={r['actual'][:16]}…")
        if r["status"] != "OK":
            lines.append(f"        STATUS: {r['status']}")
            if r["claimed"]:
                lines.append(f"        claimed: {r['claimed']}")
            if r["actual"]:
                lines.append(f"        actual:  {r['actual']}")
    lines.append("")
    lines.append("  SCHEMAS VERIFIED:")
    for r in results:
        if r["section"] != "schemas":
            continue
        marker = "✓" if r["status"] == "OK" else "✗"
        lines.append(f"    {marker} {r['key']:20s}  sha256={r['actual'][:16] if r['actual'] else '?':16}…")
    lines.append("")
    overall = "OK" if all(r["status"] == "OK" for r in results) else "DRIFT"
    lines.append(f"  OVERALL STATUS: {overall}")
    if overall != "OK":
        lines.append("")
        lines.append("  ⚠  One or more protocols/schemas have drifted from the index.")
        lines.append("  ⚠  Do not proceed with protocol-modifying actions until this is reconciled.")
        lines.append("  ⚠  To reconcile: review the change, then run scripts/protocol_update.py")
        lines.append("  ⚠  to recompute hashes and update /api/index.json.")
    lines.append("━" * 76)
    return "\n".join(lines)


def build_log_entry(idx, results, instance_label, generated_at, action_summary):
    """Build a JSONL log line for the audit trail."""
    return {
        "timestamp": generated_at,
        "instance_label": instance_label,
        "index_version": idx.get("index_version"),
        "protocol_versions_read": {
            r["key"]: r["version"] for r in results if r["section"] == "protocols"
        },
        "content_sha256_verified": {
            r["key"]: r["actual"] for r in results if r["status"] == "OK"
        },
        "hash_mismatches": [
            {"key": r["key"], "section": r["section"],
             "claimed": r["claimed"], "actual": r["actual"]}
            for r in results if r["status"] == "HASH_MISMATCH"
        ],
        "action_summary": action_summary,
    }


def print_operator_directive(idx):
    """Print the operator_directive section so the operator sees the binding instructions."""
    od = idx.get("operator_directive", {})
    print()
    print("─" * 76)
    print("  OPERATOR DIRECTIVE  (from /api/index.json)")
    print("─" * 76)
    for line in od.get("for_new_instances", []):
        print(f"  {line}")
    if "for_workflows" in od:
        print()
        print(f"  For workflows: {od['for_workflows']}")
    print("─" * 76)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--receipt-file", type=Path,
                        help="write the receipt to this file (also prints to stdout)")
    parser.add_argument("--append-log", action="store_true",
                        help="append a JSONL entry to /data/instance-familiarization.log")
    parser.add_argument("--instance", default=os.environ.get("ALEXANARCH_INSTANCE_LABEL", "(unspecified)"),
                        help="instance label included in the receipt and log entry")
    parser.add_argument("--action-summary", default="",
                        help="brief description of what this session intends to do "
                             "(included in the log entry, not in the receipt)")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero on any hash mismatch")
    parser.add_argument("--silent-directive", action="store_true",
                        help="don't print the operator directive (just produce receipt)")
    args = parser.parse_args()

    idx = load_index()
    generated_at = datetime.now(timezone.utc).isoformat()

    results = []
    verify_section(idx.get("protocols", {}), "protocols", results)
    verify_section(idx.get("schemas", {}), "schemas", results)

    receipt = build_receipt(idx, results, args.instance, generated_at)
    print(receipt)

    if args.receipt_file:
        args.receipt_file.write_text(receipt + "\n")
        print(f"\nReceipt written to {args.receipt_file}")

    if args.append_log:
        log_path = REPO_ROOT / "data" / "instance-familiarization.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = build_log_entry(idx, results, args.instance, generated_at,
                                args.action_summary)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"Logged to {log_path}")

    if not args.silent_directive:
        print_operator_directive(idx)

    overall_ok = all(r["status"] == "OK" for r in results)
    if not overall_ok and args.strict:
        print()
        print("STRICT mode: exiting non-zero due to hash mismatch(es).", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
