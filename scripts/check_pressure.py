#!/usr/bin/env python3
"""check_pressure.py — the pressure gate (MANUS ruling 2026-09-07, provenance gravity as sockets).

A deposited record may declare only pressures available at its moment of deposit:
  pressure.backward   — declared: [{k, to, note}], k in the six backward kinds; `to` a deposit number
                        LOWER than the record's own, or a locus string.
  pressure.reciprocal — declared by the LATER side about an EARLIER record: [{to, note}], to < own number.
  pressure.forward    — a socket: ALWAYS the string "∅". Never a list, never a target. What grew from the
                        record is derived by build_pressure_index.py and rendered at the socket; it is a
                        reading of what subsequently happened, not provenance, and never enters the record.
Any other shape fails the build.
"""
import json, sys
KINDS = {"inherits", "problem", "preserves", "transforms", "rejects", "consequence"}
reg = json.load(open("data/registry.json"))
fails = []
for d in reg["deposits"]:
    p = d.get("pressure")
    if p is None: continue
    n = d.get("deposit_number") or 0
    if not isinstance(p, dict): fails.append(f"#{n}: pressure must be an object"); continue
    if p.get("forward") != "∅": fails.append(f"#{n}: pressure.forward must be the socket '∅' (got {p.get('forward')!r})")
    for e in p.get("backward") or []:
        if e.get("k") not in KINDS: fails.append(f"#{n}: backward kind {e.get('k')!r} not in {sorted(KINDS)}")
        t = e.get("to")
        if isinstance(t, int) and t >= n: fails.append(f"#{n}: backward edge to #{t} is not earlier than the record")
        if not e.get("note"): fails.append(f"#{n}: backward edge to {t!r} carries no note")
    for e in p.get("reciprocal") or []:
        t = e.get("to")
        if not (isinstance(t, int) and t < n): fails.append(f"#{n}: reciprocal must name an EARLIER deposit number (got {t!r})")
    extra = set(p) - {"backward", "reciprocal", "forward"}
    if extra: fails.append(f"#{n}: unknown pressure keys {sorted(extra)}")
for f in fails: print("  FAIL", f)
print(f"check_pressure: {sum(1 for d in reg['deposits'] if d.get('pressure'))} records carry pressure · {len(fails)} failure(s)")
sys.exit(1 if fails else 0)
