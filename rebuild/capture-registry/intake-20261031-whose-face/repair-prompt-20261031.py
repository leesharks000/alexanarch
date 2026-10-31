"""Capture repair 2026-10-31: AXN:0B4F (whose-face-is-on-the-twenty-chatgpt-20261031). The ChatGPT paste's prompt line is blank; the intake read it
as the Overview's prompt of the same hour, to be confirmed. The operator, 16:16 EDT: "yup, same prompt." The transcript head and transcript_class
are restated from the draft rebuilt from the repaired parts.py; every other field stands. Repair mode, its own commit.
  python3 repair-prompt-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
SLUG = "whose-face-is-on-the-twenty-chatgpt-20261031"
new = json.loads((H / (SLUG + ".json")).read_text(encoding="utf-8"))
reg = json.loads(REG.read_text(encoding="utf-8"))
e = [x for x in reg["entries"] if x.get("slug") == SLUG]; assert len(e) == 1; e = e[0]
assert "to be confirmed" in e["transcript"], "already repaired?"
ch = []
for k in ("transcript", "transcript_class"):
    if e.get(k) != new[k]: e[k] = new[k]; ch.append(k)
for o in e.get("observations") or []:
    for k in ("transcript", "transcript_class"):
        if k in o and o[k] != new[k]: o[k] = new[k]; ch.append("obs." + k)
print(ch)
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
