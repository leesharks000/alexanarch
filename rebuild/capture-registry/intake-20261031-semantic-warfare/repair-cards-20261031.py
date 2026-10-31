"""Capture repair 2026-10-31: the October observation of autonomous-semantic-warfare-expanded (AXN:079D, OBS-db53ff649054) says
"Eight cards" and lists seven; its cites is 7 and the paste shows seven. Found by the /non composer of the autonomous-semantic-warfare
row (reported, not fixed) and checked against the paste (paste-asw-aio.txt). Repair mode, one operation, its own commit: the count word
only, wherever this entry carries it (root and observation), and in the intake's parts.py. Every other field stands as seated.
  python3 repair-cards-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
OLD, NEW = "strategic and military integration. Eight cards:", "strategic and military integration. Seven cards:"
reg = json.loads(REG.read_text(encoding="utf-8"))
e = [x for x in reg["entries"] if x.get("slug") == "autonomous-semantic-warfare-expanded"]; assert len(e) == 1; e = e[0]
s = json.dumps(e, ensure_ascii=False); n = s.count(OLD); assert n >= 1, "already repaired?"
reg["entries"][reg["entries"].index(e)] = json.loads(s.replace(OLD, NEW))
pp = H / "parts.py"; t = pp.read_text(encoding="utf-8"); assert t.count(OLD) == 1
print("entry occurrences:", n)
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    pp.write_text(t.replace(OLD, NEW), encoding="utf-8")
