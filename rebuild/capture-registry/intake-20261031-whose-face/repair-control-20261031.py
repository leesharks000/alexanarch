"""Capture repair 2026-10-31 (second): AXN:0B4F (whose-face-is-on-the-twenty-chatgpt-20261031). The intake's fifth finding read the composition as
turning the control (#508) against the argument and reversing its conclusion. Read again under the displacement test (does the response preserve the
claim and address its evidence; does it assign the paper an unsupported causal claim), the composition reads the control for an objection and proposes
a controlled experiment, a fair use of a control; the weight it removes lies in the clause assigning the paper 'deliberate institutional choices involving
Epstein', which #509 keeps in Tier D. The finding is restated; every other field stands. Operator: "lets do the one line repair" (16:59 EDT).
  python3 repair-control-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
SLUG = "whose-face-is-on-the-twenty-chatgpt-20261031"
new = json.loads((H / (SLUG + ".json")).read_text(encoding="utf-8"))
reg = json.loads(REG.read_text(encoding="utf-8"))
e = [x for x in reg["entries"] if x.get("slug") == SLUG]; assert len(e) == 1; e = e[0]
assert "THE CONTROL TURNED AGAINST THE ARGUMENT" in json.dumps(e["findings"]), "already repaired?"
e["findings"] = new["findings"]
print(["findings"])
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
