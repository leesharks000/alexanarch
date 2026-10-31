"""Capture repair 2026-10-31 (fourth): AXN:0B44 ("semantic warfare", Google AI Mode) and the October observation of AXN:079D
("autonomous semantic warfare", Google AI Overview, OBS-db53ff649054). The intake read the agentic sense (AI agents generating and
manipulating narratives) as another sense of the archive's term, and at 079D recorded an inversion of the claim boundary on that belief.
The operator: "its not - thats also a layer processing meaning." The Field Manual gives AI three roles in semantic warfare, "as combatant
when making local ranking or generation decisions, as tool when deployed by human operators to amplify operations, and as field when its
platform-wide optimization criteria shape the entire ecology of semantic interaction" (#499, ch. 8). The agentic sense is the term's tool
and combatant roles; what the compositions drop is the field role and the author. The 079D inversion is withdrawn and restated as a
narrowing; 0B44's "another sense" restated as the term in its tool role. The June observation of 079D stands. Repair mode, its own commit.
Fields taken whole from the intake drafts rebuilt from the repaired parts.py.
  python3 repair-agentic-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(REG.read_text(encoding="utf-8"))
E = {x.get("slug"): x for x in reg["entries"]}
ch = []
a = json.loads((H / "semantic-warfare-aimode-20261031.json").read_text(encoding="utf-8"))
e = E["semantic-warfare-aimode-20261031"]
assert "ANOTHER SENSE" in json.dumps(e["findings"]), "0B44 already repaired?"
for k in ("findings", "analysis", "per_dim"):
    if e[k] != a[k]: e[k] = a[k]; ch.append("0B44." + k)
b = json.loads((H / "autonomous-semantic-warfare-aio-20261031.json").read_text(encoding="utf-8"))
o = [x for x in E["autonomous-semantic-warfare-expanded"]["observations"] if x.get("obs_id") == "OBS-db53ff649054"]; assert len(o) == 1; o = o[0]
assert o["per_dim"].get("inversions"), "079D October observation already repaired?"
for k in ("findings", "analysis", "per_dim"):
    if o[k] != b[k]: o[k] = b[k]; ch.append("079D.OBS-db53ff649054." + k)
print(ch)
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
