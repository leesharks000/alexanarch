#!/usr/bin/env python3
"""Backfill the address match type on every capture (2026-10-11), on the operator's rulings: "exact is quoted. broad is unquoted."
and "we can leave the 15 indeterminate - there may have been some question early in the data whether the distinction was being
recorded at each point". match is derived from q by capture_intake.match_of; where the mt as recorded says EXACT MATCH or BROAD
MATCH and the address says the other, match is INDETERMINATE and match_note carries the mt as recorded. mt is not touched."""
import json, pathlib, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts")); from capture_intake import match_of
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(REG.read_text(encoding="utf-8"))
c = collections.Counter(); ind = []
for e in reg["entries"]:
    m = match_of(e["q"]); rec = str(e.get("mt") or "")
    rec = "EXACT MATCH" if rec.startswith("EXACT MATCH") else "BROAD MATCH" if rec.startswith("BROAD MATCH") else None
    if rec and rec != m:
        e["match"] = "INDETERMINATE"
        e["match_note"] = (f"mt recorded '{e['mt']}'; the address as stored is {'quoted' if m == 'EXACT MATCH' else 'unquoted'} "
                           f"('{e['q']}'). Left indeterminate (operator, 2026-10-11): the early record may not have recorded the "
                           "distinction at each point.")
        ind.append(e["slug"])
    else:
        e["match"] = m; e["match_note"] = None
    c[e["match"]] += 1
assert c["INDETERMINATE"] == 15, c
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print(dict(c)); print("indeterminate:", ind)
