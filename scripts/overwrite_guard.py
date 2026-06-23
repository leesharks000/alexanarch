"""
overwrite_guard.py — importable helpers for the pre-overwrite mechanism.

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS MODULE PROVIDES
═══════════════════════════════════════════════════════════════════════════════

For instance-issued receipts (the human-in-the-loop case), see pre_overwrite.py.

This module is for AUTO-FLOW write paths — scripts like regenerate_surfaces.py
that legitimately overwrite many files in deterministic, repeatable ways.
Such scripts call `issue_auto_receipt(path, actor='regenerate_surfaces')`
before each write, which:

  1. Appends an audit entry to data/pre-overwrite-receipts.log
  2. Returns the receipt dict so the caller can include it in change logs

And `require_receipt(path, max_age_seconds=600)` for paths where you want to
HARD-FAIL if no fresh receipt exists. (Use sparingly; primarily for ad-hoc
script paths that aren't part of the canonical regenerator.)

═══════════════════════════════════════════════════════════════════════════════
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RECEIPT_LOG = REPO_ROOT / "data" / "pre-overwrite-receipts.log"


class StaleReceiptError(Exception):
    """No fresh receipt found, or receipt sha256 does not match current file."""


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _web_root_path(abs_or_rel) -> str:
    p = Path(abs_or_rel)
    try:
        rel = p.resolve().relative_to(REPO_ROOT)
        return "/" + str(rel)
    except (ValueError, FileNotFoundError):
        s = str(p)
        if s.startswith("/"):
            return s
        return "/" + s.lstrip("./")


def issue_auto_receipt(path, actor: str, reason: str = "", instance_id: str = "") -> dict:
    """Append a receipt for an automated write path. Returns the receipt dict.

    For paths that don't yet exist (a CREATE), the receipt records sha256=None
    and size=0 with a `created=True` marker — still a useful audit signal.
    """
    abs_path = Path(path).resolve() if not Path(path).is_absolute() else Path(path)
    web_path = _web_root_path(path)
    if abs_path.exists() and abs_path.is_file():
        sha = _file_sha256(abs_path)
        size = abs_path.stat().st_size
        created = False
    else:
        sha = None
        size = 0
        created = True
    receipt = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "instance_id": instance_id or os.environ.get("ALEXANARCH_INSTANCE_ID", "auto"),
        "path": str(abs_path),
        "web_path": web_path,
        "sha256": sha,
        "size_bytes": size,
        "created": created,
        "reason": reason,
    }
    RECEIPT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(RECEIPT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(receipt, ensure_ascii=False) + "\n")
    return receipt


def find_recent_receipts(path, max_age_seconds: int = 600) -> list:
    """Return all receipts for the path within max_age_seconds, newest first.

    Reads the entire log; this is O(n) in receipt count. For Alexanarch's
    scale (small-K receipts) this is fine. If/when receipts hit 100K+ scale,
    rotate the log by month and binary-search the tail.
    """
    if not RECEIPT_LOG.exists():
        return []
    abs_path = str(Path(path).resolve() if not Path(path).is_absolute() else Path(path))
    web_path = _web_root_path(path)
    cutoff = datetime.now(timezone.utc).timestamp() - max_age_seconds
    results = []
    with open(RECEIPT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("path") != abs_path and r.get("web_path") != web_path:
                continue
            try:
                ts = datetime.fromisoformat(r.get("ts", ""))
                if ts.timestamp() < cutoff:
                    continue
            except (ValueError, TypeError):
                continue
            results.append(r)
    results.sort(key=lambda r: r.get("ts", ""), reverse=True)
    return results


def require_receipt(path, max_age_seconds: int = 600, allow_actors=None) -> dict:
    """Verify a fresh receipt exists for the path with matching sha256.

    Raises StaleReceiptError if:
      - No receipt found within max_age_seconds
      - Receipt sha256 does not match the file's current sha256
        (meaning the file was modified after the receipt was issued)

    Returns the verifying receipt. By default accepts any actor; pass
    `allow_actors=['instance']` to require human-issued receipts only.
    """
    abs_path = Path(path).resolve() if not Path(path).is_absolute() else Path(path)
    receipts = find_recent_receipts(path, max_age_seconds=max_age_seconds)
    if not receipts:
        raise StaleReceiptError(
            f"No receipt found for {abs_path} within last {max_age_seconds} seconds. "
            f"Run `python3 scripts/pre_overwrite.py {abs_path}` first."
        )
    if allow_actors:
        receipts = [r for r in receipts if r.get("actor") in allow_actors]
        if not receipts:
            raise StaleReceiptError(
                f"No receipt found for {abs_path} from accepted actors {allow_actors}. "
                f"Run `python3 scripts/pre_overwrite.py {abs_path} --actor instance` first."
            )
    most_recent = receipts[0]
    # Verify sha256 matches current file (if file exists)
    if abs_path.exists():
        current_sha = _file_sha256(abs_path)
        if most_recent.get("sha256") and most_recent["sha256"] != current_sha:
            raise StaleReceiptError(
                f"Receipt sha256 mismatch for {abs_path}.\n"
                f"  Receipt sha256: {most_recent['sha256']}\n"
                f"  Current sha256: {current_sha}\n"
                f"  The file changed after the receipt was issued. Re-run "
                f"pre_overwrite.py to refresh."
            )
    return most_recent


# ─── Tail helper for diagnostics ──────────────────────────────────────────

def tail_receipts(n: int = 20) -> list:
    """Return the last N receipts from the log, newest first."""
    if not RECEIPT_LOG.exists():
        return []
    lines = RECEIPT_LOG.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines[-n:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    out.reverse()
    return out


if __name__ == "__main__":
    # Diagnostic: print recent receipts
    import argparse
    parser = argparse.ArgumentParser(description="Inspect the pre-overwrite receipts log")
    parser.add_argument("--tail", type=int, default=20, help="Show last N receipts")
    parser.add_argument("--path", help="Filter to receipts for a specific path")
    parser.add_argument("--max-age", type=int, default=86400, help="Max age in seconds (default 1 day)")
    args = parser.parse_args()
    if args.path:
        rs = find_recent_receipts(args.path, max_age_seconds=args.max_age)
        print(f"Receipts for {args.path} within last {args.max_age} seconds: {len(rs)}")
        for r in rs:
            print(f"  {r['ts']}  actor={r['actor']:<20s}  sha={(r.get('sha256') or '')[:16]}…  size={r.get('size_bytes', 0):,}")
    else:
        rs = tail_receipts(args.tail)
        print(f"Last {len(rs)} receipts:")
        for r in rs:
            actor = r.get("actor", "?")[:18]
            path_short = r.get("web_path", r.get("path", ""))[:50]
            sha_short = (r.get("sha256") or "—")[:12]
            print(f"  {r['ts']}  {actor:<18s}  {path_short:<50s}  sha={sha_short}")
