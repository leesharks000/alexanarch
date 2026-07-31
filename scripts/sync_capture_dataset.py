#!/usr/bin/env python3
"""sync_capture_dataset.py — publish the capture registry as a dataset from source.

THE DEFECT THIS CLOSES
----------------------
`datasets/capture-registry/` held a manifest and nothing else. The manifest
declared three files with sizes and hashes; none was on disk. It was pinned at
v9.19 while the source of truth on machinemediation had advanced to v9.29 — ten
versions of drift behind a manifest asserting files that did not exist.

This is PATHOLOGY-26/28 in the Atlas register: a copied value with no refresh
path becomes a claim about the past, presented identically to a claim about the
present. Here the copied value was an entire file list.

SOURCE OF TRUTH
---------------
The capture registry is authored on machinemediation.org and published here.
`--source` points at that working copy. The two other dataset members are
produced inside this repository and are copied from their canonical locations.

The manifest is regenerated from what is actually on disk — never hand-edited —
so it cannot again declare a file the dataset does not hold.

    python3 scripts/sync_capture_dataset.py --source /tmp/mm
"""
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "datasets" / "capture-registry"

# member name → where it comes from ("mm" = the source-of-truth working copy)
MEMBERS = {
    "EA-WG-CAPTURES-01.json": ("mm", "data/registry.json"),
    "capture-deposit-links.json": ("local", "data/capture-deposit-links.json"),
    "semantic-addresses.json": ("local", "data/semantic-addresses.json"),
}


def human(n):
    return f"{n/1e6:.2f} MB" if n >= 1e6 else f"{n/1024:.1f} KB"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="/tmp/mm",
                    help="working copy of the machinemediation repository")
    a = ap.parse_args()
    src_root = Path(a.source)
    DEST.mkdir(parents=True, exist_ok=True)

    records, missing = [], []
    reg_version = reg_date = None
    total_captures = None

    for name, (origin, rel) in MEMBERS.items():
        src = (src_root / rel) if origin == "mm" else (ROOT / rel)
        dst = DEST / name
        if not src.is_file():
            missing.append((name, str(src)))
            if dst.exists():
                dst.unlink()          # never leave a stale copy standing in for a live one
            continue
        shutil.copy2(src, dst)
        b = dst.read_bytes()
        if name == "EA-WG-CAPTURES-01.json":
            reg = json.loads(b)
            reg_version = reg.get("version")
            reg_date = reg.get("date")
            total_captures = reg.get("total_captures") or len(reg.get("entries", []))
        records.append({
            "name": name,
            "path": f"/datasets/capture-registry/{name}",
            "size_bytes": len(b),
            "size_human": human(len(b)),
            "sha256": hashlib.sha256(b).hexdigest(),
            "source": ("machinemediation (source of truth)" if origin == "mm"
                       else f"this repository, {rel}"),
        })

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "dataset": "capture-registry",
        "title": "AI Overview Capture Registry — machine-composition reception events",
        "version": reg_version,
        "date": reg_date,
        "description": (
            "Dated captures of machine-composition reception events against the Crimson "
            "Hexagonal Archive's entities and frameworks. Authored on machinemediation.org "
            "and published here; this copy is generated, never hand-edited. The manifest is "
            "rebuilt from the files actually present, so it cannot declare a member the "
            "dataset does not hold."),
        "canonical_home": "https://www.machinemediation.org/captures/",
        "source_of_truth": "machinemediation.org — data/registry.json",
        "total_captures": total_captures,
        "generated_by": "scripts/sync_capture_dataset.py",
        "generated_at": now,
        "total_files": len(records),
        "total_bytes": sum(r["size_bytes"] for r in records),
        "records": records,
    }
    if missing:
        manifest["missing_members"] = [
            {"name": n, "expected_source": s,
             "note": "declared member not found at source; not published, and not "
                     "left as a stale copy"} for n, s in missing]
    (DEST / "manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"capture-registry dataset → v{reg_version} ({reg_date}), "
          f"{total_captures} captures")
    for r in records:
        print(f"    {r['name']:34s} {r['size_human']:>10s}  {r['source']}")
    for n, s in missing:
        print(f"    MISSING {n} (expected {s})")


if __name__ == "__main__":
    main()
