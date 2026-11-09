"""Repair of 2026-11-08 (22:35 EST), the seven captures of the entity Enli Lucente. Operator: "it might need the notice moved to the body of
those captures, with targeted correction"; "yes, lets repair those seven captures." The 23 October notice stays as written; each record takes a
lead sentence, placed at the head of its page, its description and its JSON-LD, stating the entity's origin as the registry holds it (originator:
external, "Operator ruling 2026-09-25: originated outside the archive") and what a capture records. The captured compositions are untouched.
    python3 repair.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/EA-WG-CAPTURES-01.json"
LEAD = ("Enli Lucente is an independent researcher who originated outside this archive. This page records what an AI system composed about her "
        "on the date given; it does not record how she came to exist. SPXI treatment of her entity was partial, within limits she set, and ended "
        "after her notice of 22 October 2026.")
d = json.loads(P.read_text(encoding="utf-8")); n = 0
for e in d["entries"]:
    q = (e.get("q") or "").lower()
    if "enli" in q or "lucente" in q:
        nt = e["notice"]; assert nt["date"] == "2026-10-23" and (e.get("originator") or {}).get("relation") == "external"
        nt["placement"] = "lead"; nt["lead"] = LEAD
        nt["lead_basis"] = "Operator ruling, 2026-11-08 22:35 EST: 'yes, lets repair those seven captures'"
        n += 1
assert n == 7, n
P.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("repaired", n)
