"""Capture repair 2026-10-31: the fifteen census captures (AXN:0B5A-0B68), on the reports of the fifteen NonWiki composers, each item checked by the
session against the saved sources before it was applied (REPAIRS-PENDING.md lists the reports). Restated: readings attributed to #1725 that #1725 does
not make (MIA, BannedThought, EROL, IISH, Reuther), now the census record's or quoted from #1725 with its line; MIA's count headline (180,000 against
over 400,000 is not a fifth); the Reuther appointment line (the library offers one; the composition gives the offer as a rule); the holders the Irish
Left Archive and libcom name on their own pages; the New Reasoner origin on a page no card carries; the IISH custody (RGASPI); the CCC 'nonviolent'
(on card 3), 'strikes' (on no card) and count; the GNAD range (both figures on cards) and the excluded movement; the Labor Action Tracker scope and the
China Labour Bulletin thanks; the unionstats figure without a readable source; BannedThought's grain; MEGAdigital's d. Added: the source-panel titles
the cite lists left out (MIA, IISH, Labor Notes). Fields are taken whole from the rebuilt drafts (parts.py; the intake's version kept as parts-intake.py).
  python3 repair-20261031.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
FIELDS = ("mt", "d", "findings", "analysis", "cite_list", "cites", "per_dim")
reg = json.loads(REG.read_text(encoding="utf-8"))
by = {x.get("slug"): x for x in reg["entries"]}
for f in sorted(H.glob("*-2026103[1].json")):
    new = json.loads(f.read_text(encoding="utf-8")); e = by[new["slug"]]
    before = {k: json.loads(json.dumps(e.get(k))) for k in FIELDS}
    ch = [k for k in FIELDS if k in new and json.dumps(e.get(k), sort_keys=True) != json.dumps(new[k], sort_keys=True)]
    for k in ch:
        if k == "cite_list":   # seat-time enrichment (deposit links) is kept; the repair only appends the titles the list left out
            have = {c["title"] for c in e["cite_list"]}
            e["cite_list"] = e["cite_list"] + [c for c in new["cite_list"] if c["title"] not in have]
        elif k == "per_dim":   # the reading's own stamp is kept
            pd = dict(new["per_dim"]); pd["read"] = e["per_dim"].get("read"); e["per_dim"] = pd
        else:
            e[k] = new[k]
    ch = [k for k in ch if json.dumps(e.get(k), sort_keys=True) != json.dumps(before[k], sort_keys=True)]
    print(new["slug"], ch)
if "--check" not in sys.argv:
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
