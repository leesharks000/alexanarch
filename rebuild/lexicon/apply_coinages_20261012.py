#!/usr/bin/env python3
"""Lexicon pass 5 (2026-10-12): the archive's coinages, read by hand and marked positively.

Passes 3–4 marked what is NOT a minted term. This pass marks what IS: entry_class 'coinage' for every entry that
names a concept, mechanism, instrument, protocol, metric, operator, role or room in the archive's own theory —
'Semantic Liquidation', 'Beige Threshold (β)', 'Airlock Verification Swarm', 'adjacency is not affiliation',
'Huskification', 'Retrocausal Canon Formation'.
Read: the 4,040 unflagged entries of three or more words; the 1,052 two-word and 495 one-word entries passes 3–4 kept;
and the two-word entries pass 4 flagged, of which 219 (plus four document-structure entries) were archive coinages
flagged in error ('Cognitive rent', 'Classification Violence', 'Assembly witness'). Those are reclaimed:
'not-a-term' leaves entry_class_all and is recorded under entry_class_superseded with the pass that set it.
Not marked: headings, section and figure labels, status codes, notation, people's names, borrowed
scholarly terms (Ergodic literature, Speech Act Theory), ordinary words the archive uses as operator names.
NOTHING IS DELETED (_CLEANING principle, 2026-08-14). Lists: read-20261012-coinage-{1word,2word,3plus}.txt.
"""
import json, pathlib
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parents[1]
LEX = ROOT / "data/lexical-minting-registry.json"
lex = json.loads(LEX.read_text(encoding="utf-8")); T = lex["terms"]
BASIS = "read 2026-10-12 (pass 5): a coinage of the archive"
stats = {}
for name in ("1word", "2word", "3plus"):
    ids = [int(x) for x in (HERE / f"read-20261012-coinage-{name}.txt").read_text().split()]
    rec = 0
    for i in ids:
        t = T[i]
        allc = list(t.get("entry_class_all") or ([t["entry_class"]] if t.get("entry_class") else []))
        if "not-a-term" in allc:
            allc.remove("not-a-term"); rec += 1
            sup = list(t.get("entry_class_superseded") or [])
            sup.append({"entry_class": "not-a-term", "basis": t.get("entry_class_basis"), "superseded_by": "pass 5"})
            t["entry_class_superseded"] = sup
        if "coinage" not in allc:
            allc.insert(0, "coinage")
        t["entry_class_all"] = allc
        t["entry_class"] = "coinage"
        t["entry_class_basis"] = BASIS
    stats[name] = {"marked": len(ids), "reclaimed_from_not_a_term": rec}
c = lex.setdefault("_CLEANING", {}); c.setdefault("passes", [])
c["passes"].append({"date": "2026-10-12", "pass": 5, "script": "rebuild/lexicon/apply_coinages_20261012.py",
                    "read": "all unflagged 3+ word entries, all kept 1- and 2-word entries, and the pass-4 two-word flags, by hand",
                    "marked_coinage": sum(s["marked"] for s in stats.values()), "by_length": stats,
                    "principle": "positive class 'coinage'; reclaimed not-a-term flags recorded in entry_class_superseded, nothing deleted"})
LEX.write_text(json.dumps(lex, ensure_ascii=False, indent=1), encoding="utf-8")
print(stats)
