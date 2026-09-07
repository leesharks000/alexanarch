#!/usr/bin/env python3
"""build_pressure_index.py — the inverse historical projection (2026-09-07).

For every record, what later records declared toward it: backward edges (by kind) and reciprocal
pressure, each dated by the LATER record's deposit date. Written to data/pressure-index.json and
rendered at each record's forward socket as "later growth". These lines are the archive's
present-tense reconstruction of what occupied the empty place — not the earlier record's statement.
The earlier record's bytes and pressure field are untouched.
"""
import json
reg = json.load(open("data/registry.json"))
by = {d.get("deposit_number"): d for d in reg["deposits"]}
idx = {}
for d in reg["deposits"]:
    p = d.get("pressure")
    if not p: continue
    n = d.get("deposit_number"); date = d.get("date")
    for e in p.get("backward") or []:
        if isinstance(e.get("to"), int): idx.setdefault(str(e["to"]), []).append({"from": n, "k": e["k"], "date": date, "note": e.get("note")})
    for e in p.get("reciprocal") or []:
        idx.setdefault(str(e["to"]), []).append({"from": n, "k": "reciprocal", "date": date, "note": e.get("note")})
for k in idx: idx[k].sort(key=lambda x: (x["date"] or "", x["from"]))
out = {"_rule": "forward pressure is derived, never stored in the record it presses from; these entries are readings of what subsequently happened", "generated_from": "data/registry.json", "sockets_filled": len(idx), "index": idx}
json.dump(out, open("data/pressure-index.json", "w"), ensure_ascii=False, indent=1)
print(f"pressure index: {len(idx)} sockets carry later growth")
