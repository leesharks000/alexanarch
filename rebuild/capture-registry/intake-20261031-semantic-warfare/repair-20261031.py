"""Capture repair 2026-10-31: AXN:0B46 ("semantic warfare", Google AI Mode, exact match). The intake of 04:10 read the operator's
"and note that this is sharks and fraction" as naming the answer's Technical Disclosure Commons chip, and seated that chip as the
archive's (rel archive_controlled, per_v src true, a finding 'THE ARCHIVE AS SOURCE, OTHERS AS AUTHORS'). The operator, 04:21:
"i am saying, that the mpai byline goes to Sharks and Fraction". The message concerned the MPAI's byline. Nothing in the paste or the
registry identifies the chip's source (its URL is not in the paste; the registry holds no Technical Disclosure Commons deposit), so the
reading is withdrawn: the chip is third party and unread, src false, per 0.5 -> 0.75 (three of four units lost). In the same operation
the inversion's quotation of the manual's claim boundary is given its locus: it is the record of #499 (AXN:013E), not #1326. Repair mode, one
operation, its own commit. The fields are taken whole from the intake draft rebuilt from the repaired parts.py; every other field
stands as seated.
  python3 repair-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
SLUG = "semantic-warfare-exact-aimode-20261031"
TOP = ["archive_controlled_cites", "analysis", "cite_list", "mt", "per_v", "findings", "per_dim", "per_note"]
new = json.loads((H / (SLUG + ".json")).read_text(encoding="utf-8"))
reg = json.loads(REG.read_text(encoding="utf-8"))
e = [x for x in reg["entries"] if x.get("slug") == SLUG]; assert len(e) == 1; e = e[0]
assert e["per_v"]["src"] is True and e["cite_list"][0]["rel"] == "archive_controlled" and e["per"] == 0.5, "already repaired?"
ch = []
def put(o, where):
    for k in TOP:
        if k in o and o[k] != new[k]: o[k] = new[k]; ch.append(where + "." + k)
    if isinstance(o.get("notes"), dict) and o["notes"].get("operator") != new["notes"]["operator"]:
        o["notes"]["operator"] = new["notes"]["operator"]; ch.append(where + ".notes.operator")
    if "per" in o and o["per"] != 0.75: o["per"] = 0.75; ch.append(where + ".per")
put(e, "entry")
for i, o in enumerate(e.get("observations") or []): put(o, f"obs[{i}]")
print("\n".join(ch))
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
