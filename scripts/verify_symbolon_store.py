#!/usr/bin/env python3
"""verify_symbolon_store.py — re-verify every stored sealed core against its kernel,
record the date, and publish a mirror manifest.

WHY
---
A stamped file whose bytes were hash-checked once, at ingest, and never again,
carries a status ("witnessed-verified") that is a memory rather than a
measurement. Depositor E. asked the right question of her own file on
2026-08-06 — where is the original stored, and under what conditions — and the
honest answer exposed three gaps:

  1. entries read `witnessed-verified` with `verified_at: null` — verified when?
  2. the stored files appeared in NO checksum manifest, so `sha256sum -c`
     could not check them;
  3. they appeared in NO harvest feed, so the store was public but not
     *mirrorable without asking* — which is the only kind of public that
     survives an account termination.

This script closes (1) and (2) and emits the manifest that closes (3).

WHAT IT DOES
------------
For every entry in data/symbolon-registry/entries/, finds its stored file (if
any), hashes the bytes on disk, and compares against the entry's AXN0 kernel —
the identifier IS the expected hash, so verification needs no external truth.

  match    → records verified_at (first verification) and last_verified_at (this
             one), plus verification_method and byte length. Status may rise
             from witnessed-unverified to witnessed-verified on evidence.
  MISMATCH → never silently repaired. The entry is marked
             integrity_alert, the status is NOT raised, and the run exits
             nonzero. A stored core that does not hash to its kernel is either
             a corrupted copy or a substituted one, and both are findings.
  absent   → identity-only witnessing (no core stored). Recorded as such, not
             as a failure: storage is optional by design and the kernel is
             true without it.

Then writes data/symbolon-registry/MANIFEST.json — one line per stored core with
kernel, size, retrieval URL, and verification dates. This is the file a mirror
operator needs: fetch, hash, compare, done. No trust in this archive required.

Usage:
    python3 scripts/verify_symbolon_store.py              # verify + write
    python3 scripts/verify_symbolon_store.py --dry-run    # report only
"""
import json, hashlib, pathlib, datetime, sys, argparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "data/symbolon-registry/entries"
FILES = ROOT / "data/symbolon-registry/files"
MANIFEST = ROOT / "data/symbolon-registry/MANIFEST.json"
BASE = "https://www.alexanarch.org"


def now():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    t = now()

    stored_by_prefix = {}
    if FILES.is_dir():
        for f in sorted(FILES.iterdir()):
            if f.is_file() and not f.name.startswith("."):
                stored_by_prefix.setdefault(f.name.split("-", 1)[0], []).append(f)

    rows, verified, absent, alerts, changed = [], 0, 0, [], 0

    for ef in sorted(ENTRIES.glob("*.json")):
        entry = json.loads(ef.read_text())
        kernel16 = ef.stem
        tup = entry.get("tuple", {})
        expect = (tup.get("axn0") or {}).get("sha256")
        cands = stored_by_prefix.get(kernel16, [])

        if not expect:
            alerts.append(f"{kernel16}: entry declares no AXN0 sha256 — cannot verify")
            continue

        if not cands:
            absent += 1
            if entry.get("core_stored") is not False:
                entry["core_stored"] = False
                entry["core_storage_note"] = (
                    "identity-only witnessing: no sealed core held by this archive. "
                    "The kernel is true without it; the depositor holds Seed B.")
                changed += 1
                if not a.dry_run:
                    ef.write_text(json.dumps(entry, ensure_ascii=False, indent=1))
            continue

        path = cands[0]
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        size = path.stat().st_size
        rel = path.relative_to(ROOT).as_posix()

        if got != expect:
            alerts.append(
                f"{kernel16}: INTEGRITY MISMATCH — stored bytes hash {got[:16]}… "
                f"but kernel declares {expect[:16]}… ({rel})")
            entry["integrity_alert"] = {
                "detected_at": t, "expected_sha256": expect,
                "found_sha256": got, "path": "/" + rel,
                "note": "Stored core does not hash to its kernel. Not repaired "
                        "automatically: a mismatch is either corruption or "
                        "substitution, and both are findings, not chores."}
            if not a.dry_run:
                ef.write_text(json.dumps(entry, ensure_ascii=False, indent=1))
            continue

        verified += 1
        first = entry.get("verified_at") or t
        before = (entry.get("verified_at"), entry.get("last_verified_at"),
                  entry.get("status"), entry.get("core_bytes"))
        entry["verified_at"] = first
        entry["last_verified_at"] = t
        entry["verification_method"] = (
            "sha256 of stored bytes compared to the entry's AXN0 kernel; the "
            "identifier is the expected hash, so verification is self-contained")
        entry["core_stored"] = True
        entry["core_bytes"] = size
        entry["core_path"] = "/" + rel
        if entry.get("status") == "witnessed-unverified":
            entry["status"] = "witnessed-verified"
            entry["status_raised_at"] = t
        if (entry.get("verified_at"), entry.get("last_verified_at"),
                entry.get("status"), entry.get("core_bytes")) != before:
            changed += 1
            if not a.dry_run:
                ef.write_text(json.dumps(entry, ensure_ascii=False, indent=1))

        rows.append({
            "position": entry.get("position"),
            "axn": entry.get("axn"),
            "entry": f"/data/symbolon-registry/entries/{ef.name}",
            "path": "/" + rel,
            "retrieval": f"{BASE}/{rel}",
            "sha256": got,
            "bytes": size,
            "status": entry.get("status"),
            "registered": entry.get("registered"),
            "verified_at": first,
            "last_verified_at": t,
        })

    rows.sort(key=lambda r: (r["position"] or ""))
    manifest = {
        "description": (
            "Sealed cores held by this archive for AXN symbolon witnessings. "
            "Each row's sha256 IS the entry's AXN0 kernel: fetch the file, hash "
            "it, compare. Verification requires no trust in this archive and no "
            "permission to mirror. Copy freely — a copy that hashes to the "
            "kernel is the work, wherever it lives."),
        "generator": "scripts/verify_symbolon_store.py",
        "generated": t,
        "base": BASE,
        "stored_cores": len(rows),
        "identity_only_witnessings": absent,
        "integrity_alerts": len(alerts),
        "mirror_instructions": (
            "sha256sum -c against SHA256SUMS.txt for the repository copy, or "
            "fetch each `retrieval` URL and compare to `sha256`. Both are the "
            "same check. Independent custody means a copy held by someone who "
            "is not this archive's administrator, on a platform this archive "
            "does not use."),
        "cores": rows,
    }
    if not a.dry_run:
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))

    tag = "[DRY] " if a.dry_run else ""
    print(f"{tag}symbolon store: {verified} verified · {absent} identity-only · "
          f"{len(alerts)} alerts · {changed} entries updated")
    for al in alerts:
        print("  ALERT:", al, file=sys.stderr)
    return 1 if alerts else 0


if __name__ == "__main__":
    sys.exit(main())
