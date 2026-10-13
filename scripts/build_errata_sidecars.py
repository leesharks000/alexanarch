#!/usr/bin/env python3
"""build_errata_sidecars.py — the errata sidecar of every deposit, as data.

MPAI Formal Specification v2.0 (#1677) §10; MANUS 2026-10-13: "a wrong reference doesnt require a full
erratum deposit - it can go in an errata sidecar on each deposit, which we should have anyways - below
the deposit, not first thing."

Source of truth: the registry's `errata` field on each deposit. This script projects it to

    data/errata/<deposit_number>.json   for EVERY deposit (an empty list is a statement: none recorded)
    data/errata/index.json              the deposits whose sidecar holds entries

The record page renders the same entries below the full text (wire_deposit._errata_html). The deposited
bytes and the AXN are never touched by an errata entry. Corrections of argument or evidence are erratum
deposits, collected at /errata/ by build_errata_surface.py; this sidecar is for reference, citation,
source and count defects.

New entries are written in the shape {date, kind, locus, was, now, reason, raised_by, status}.

Usage: python3 scripts/build_errata_sidecars.py [--dry-run]
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "errata"
BASE = "https://www.alexanarch.org"


def main():
    dry = "--dry-run" in sys.argv
    reg = json.loads((ROOT / "data" / "registry.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    held, written = [], 0
    for d in reg["deposits"]:
        n = d["deposit_number"]
        entries = d.get("errata") or []
        doc = {"deposit_number": n, "axn": d.get("axn"), "record": f"{BASE}/s/records/{n}/",
               "errata": entries, "count": len(entries),
               "scope": "reference, citation, source and count corrections; the deposited bytes and AXN are unchanged",
               "erratum_deposits": f"{BASE}/errata/", "specification": f"{BASE}/s/records/1677/"}
        if entries:
            held.append({"deposit_number": n, "axn": d.get("axn"), "title": d.get("title"), "count": len(entries),
                         "sidecar": f"{BASE}/data/errata/{n}.json"})
        p = OUT / f"{n}.json"
        new = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
        if not p.exists() or p.read_text() != new:
            written += 1
            if not dry:
                p.write_text(new)
    idx = {"name": "Alexanarch errata sidecars", "specification": f"{BASE}/s/records/1677/",
           "rule": "every deposit has a sidecar at /data/errata/<deposit_number>.json; this index lists those holding entries",
           "deposits_with_entries": len(held), "entries": sum(h["count"] for h in held), "deposits": held}
    if not dry:
        (OUT / "index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n")
    print(f"errata sidecars: {len(reg['deposits'])} deposits, {len(held)} with entries, {written} files changed"
          + (" (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
