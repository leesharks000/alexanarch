#!/usr/bin/env python3
"""repair_per_from_vector_20261015.py — re-derive the PER scalar from its four-unit vector (ruling, 2026-10-15).

capture_intake.per_vector: "PER is a FOUR-UNIT VECTOR. The scalar is a projection of it, never the record." The entity
layer found 69 observations whose stored scalar disagrees with their vector (per_v; True = retained): 49 store the
retained share (most seated 2026-08-13), 20 match neither. Operator, 2026-10-15 03:39 EDT: "lets correct the scores".
Each corrected observation carries per_corrected {from, to, on, basis}; the registry version moves and the correction
log records the pass. Observations without a four-boolean vector are untouched.
"""
import json, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(P.read_text(encoding="utf-8"))
fixed, seen = [], set()
for e in reg["entries"]:
    for o in [e] + (e.get("observations") or []):
        pv = o.get("per_v") if isinstance(o.get("per_v"), dict) else None
        vals = [v for v in (pv or {}).values() if isinstance(v, bool)]
        p = o.get("per")
        if not vals or p is None:
            continue
        lost = round(1 - sum(vals) / len(vals), 2)
        if abs(p - lost) > 0.01:
            o["per_corrected"] = {"from": p, "to": lost, "on": "2026-10-15",
                                  "basis": "re-derived from per_v, the four-unit vector that is the record (capture_intake.per_vector)"}
            o["per"] = lost
            key = o.get("obs_id") or e["slug"]
            if key not in seen:
                seen.add(key); fixed.append((key, e["slug"], p, lost))
old = reg["version"]
maj, mn = old.split(".")
reg["version"] = f"{maj}.{int(mn) + 1}"
reg["date"] = "2026-10-15"
reg.setdefault("correction_log", []).append({"date": "2026-10-15", "change": f"version {old} → {reg['version']}; PER re-derived from its vector on {len(fixed)} observations",
    "detail": "The entity layer (data/entity-relations.json) computed PER from per_v and found the stored scalar disagreeing on these observations: most stored the retained share, the rest matched neither. The vector is the record (capture_intake.per_vector); the scalar is re-derived and each observation carries per_corrected {from, to}. Ruling: operator, 2026-10-15 03:39 EDT, 'lets correct the scores'.",
    "observations": [k for k, _, _, _ in fixed]})
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"PER re-derived on {len(fixed)} observations; version {old} -> {reg['version']}")
for k, s, a, b in fixed[:6]:
    print(" ", k, s, a, "->", b)
