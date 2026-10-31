"""Capture repair 2026-10-31 (third): AXN:0B46 ("semantic warfare", Google AI Mode, exact match). The intake recorded an inversion of
the claim boundary at the span "forcing complex human thoughts into flat, binary, and algorithmic \"meaning-systems\" designed to
generate engagement through friction", on the belief that the Field Manual's meaning-systems are the communities' own ontologies and the
composition made them the platform's product. Read against the Field Manual's chapter 8 (#499, §8.3: "Platforms are financially
optimized for friction. Conflict generates engagement; engagement generates revenue; therefore conflict generates revenue"; the field
"has effectively captured the creators' coherence algorithms without explicit coercion"), the sentence gives the manual's field role
at its grain. The inversion is withdrawn; the reached basis, the third and fifth findings and the analysis restated; every other field
stands. Repair mode, one operation, its own commit. Fields taken whole from the intake draft rebuilt from the repaired parts.py.
  python3 repair-inversion-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
SLUG = "semantic-warfare-exact-aimode-20261031"
new = json.loads((H / (SLUG + ".json")).read_text(encoding="utf-8"))
reg = json.loads(REG.read_text(encoding="utf-8"))
e = [x for x in reg["entries"] if x.get("slug") == SLUG]; assert len(e) == 1; e = e[0]
assert e["per_dim"].get("inversions") or "meaning-systems" in json.dumps(e["per_dim"]), "already repaired?"
ch = []
for k in ("findings", "analysis", "per_dim"):
    if e.get(k) != new[k]: e[k] = new[k]; ch.append(k)
for o in e.get("observations") or []:
    for k in ("findings", "analysis", "per_dim"):
        if k in o and o[k] != new[k]: o[k] = new[k]; ch.append("obs." + k)
print(ch)
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
