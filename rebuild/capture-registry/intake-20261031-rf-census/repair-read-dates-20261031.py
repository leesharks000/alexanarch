"""Capture repair 2026-10-31 (second): the PER-dim read date. scripts/per_backlog.py stamped every reading with its constant
TODAY = "2026-10-29" (pd_of, read.on), and the intake builders since then called pd_of without overriding it, so observations read at
intake on 2026-10-30 and 2026-10-31 carry a read date before their capture. Each such read.on is set to its observation's own date (the
reading was done at intake, the day the capture was seated). Only observations dated after 2026-10-29 whose read.on is "2026-10-29" are
touched. Applied to the registry and to the intake drafts of 2026-10-30 and 2026-10-31. pd_of now takes the reading's date (on=...).
  python3 repair-read-dates-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"


def fix(o, date):
    pd = o.get("per_dim") or {}
    rd = pd.get("read") or {}
    if rd.get("on") == "2026-10-29" and str(date) > "2026-10-29":
        rd["on"] = str(date); return 1
    return 0


reg = json.loads(REG.read_text(encoding="utf-8"))
n = 0
for e in reg["entries"]:
    n += fix(e, e.get("date"))
    for o in e.get("observations", []):
        n += fix(o, o.get("date") or e.get("date"))
drafts = 0
for d in sorted((ROOT / "rebuild/capture-registry").glob("intake-2026103*/*.json")):
    try: x = json.loads(d.read_text(encoding="utf-8"))
    except Exception: continue
    if not isinstance(x, dict) or "per_dim" not in x: continue
    if fix(x, x.get("date")):
        drafts += 1
        if "--check" not in sys.argv: d.write_text(json.dumps(x, ensure_ascii=False, indent=1), encoding="utf-8")
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print("read dates set:", n, "in the registry,", drafts, "intake drafts", "(check only)" if "--check" in sys.argv else "")
