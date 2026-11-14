#!/usr/bin/env python3
"""build_forward_sidecars.py — the forward pointers of every deposit, as data (2026-11-13).

Lee Sharks, 2026-11-13: "it can be added as metadata, in the same way as the errata. this needs to be a flexible
rhizomatic corpus. the content identity does not need to change to point and maintain its developing relations";
"we have hologram frames. this is now about building forward to holograms before consolidation. it should be a
forward pointing metadata category"; "the socrates as orthonym holographic frame is the place for the metadata note -
its the router".

A forward pointer records a developing relation that a record carries without changing its bytes: a later or
pending piece that stands as a section of an earlier one, develops it, or is to be consolidated into it. A framework
hologram is the router: it holds the pointers for its line, and its next build consolidates them. The deposited
bytes and the AXN are never touched by a forward entry.

Source of truth: the registry's `forward` field on each deposit. Entry shape (writer strict, reader generous):
    {date, kind, from_deposit, from_locus, to_deposit | to_pending, note, raised_by, ruling, status}
This script projects it to
    data/forward/<deposit_number>.json   for EVERY deposit (an empty list is a statement: none recorded)
    data/forward/index.json              the deposits whose sidecar holds entries, and every routed pair
The record page renders the same entries below the errata (wire_deposit._forward_html).

Usage: python3 scripts/build_forward_sidecars.py [--dry-run]
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "forward"
BASE = "https://www.alexanarch.org"
SCOPE = ("developing relations carried as metadata: a piece that stands as a section of a record, develops it, or is to be "
         "consolidated into a framework hologram's next build; the deposited bytes and AXN are unchanged")


def main():
    dry = "--dry-run" in sys.argv
    reg = json.loads((ROOT / "data" / "registry.json").read_text())
    by_n = {d["deposit_number"]: d for d in reg["deposits"]}
    OUT.mkdir(parents=True, exist_ok=True)
    held, routes, written = [], [], 0
    for d in reg["deposits"]:
        n = d["deposit_number"]
        entries = d.get("forward") or []
        doc = {"deposit_number": n, "axn": d.get("axn"), "record": f"{BASE}/s/records/{n}/",
               "forward": entries, "count": len(entries), "scope": SCOPE}
        if entries:
            held.append({"deposit_number": n, "axn": d.get("axn"), "title": d.get("title"), "count": len(entries),
                         "sidecar": f"{BASE}/data/forward/{n}.json"})
            for e in entries:
                if not isinstance(e, dict):
                    continue
                t = e.get("to_deposit")
                routes.append({"router": n, "from_deposit": e.get("from_deposit"), "from_locus": e.get("from_locus"),
                               "to_deposit": t, "to_pending": e.get("to_pending"),
                               "to_title": by_n[t]["title"] if t in by_n else None, "kind": e.get("kind")})
        p = OUT / f"{n}.json"
        new = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
        if not p.exists() or p.read_text() != new:
            written += 1
            if not dry:
                p.write_text(new)
    idx = {"name": "Alexanarch forward pointers", "scope": SCOPE,
           "rule": "every deposit has a sidecar at /data/forward/<deposit_number>.json; this index lists those holding entries "
                   "and every routed pair; a framework hologram is the router for its line",
           "deposits_with_entries": len(held), "entries": sum(h["count"] for h in held), "deposits": held, "routes": routes}
    if not dry:
        (OUT / "index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n")
    print(f"forward sidecars: {len(reg['deposits'])} deposits, {len(held)} with entries, {len(routes)} routes, "
          f"{written} files changed" + (" (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
