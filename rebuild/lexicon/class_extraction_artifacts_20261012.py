#!/usr/bin/env python3
"""Lexicon pass 7 (2026-10-12): the entries no pass kept are classed, and /lexical/ shows only the lexicon.
On the operator's ruling of 16:42: 'a hispanic studies scholar is a product of a bad automated pass ... why would i want it
on the page?' The 3,463 entries with no entry_class are the remainder pass 5 read by hand and did not mark a coinage
(headings, phrases, people's descriptions, labels the automated extractions recorded as terms). They are classed
'extraction artifact' — a product of the automated extraction, not a term and not an archival coding. NOTHING IS DELETED
(_CLEANING principle, 2026-08-14): the entries stay addressable in the JSON; /lexical/ presents entries classed coinage or
archive-reworked term (3,194) and nothing else."""
import json, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]; LEX = ROOT / "data/lexical-minting-registry.json"
lex = json.loads(LEX.read_text(encoding="utf-8")); T = lex["terms"]
BASIS = "automated extraction; read 2026-10-12 (pass 5), not kept as a term (pass 7)"
n = 0
for t in T:
    if t.get("entry_class") is None:
        t["entry_class"] = "extraction artifact"; t["entry_class_all"] = ["extraction artifact"]; t["entry_class_basis"] = BASIS; n += 1
c = collections.Counter(t.get("entry_class") for t in T)
lex["_CLEANING"]["passes"].append({"date": "2026-10-12", "pass": 7, "script": "rebuild/lexicon/class_extraction_artifacts_20261012.py",
    "classed_extraction_artifact": n, "lexicon": c["coinage"] + c["archive-reworked term"],
    "presentation": "/lexical/ shows entries classed coinage or archive-reworked term only; all other classes stay in this file",
    "principle": "nothing deleted; every entry now carries a class"})
LEX.write_text(json.dumps(lex, ensure_ascii=False, indent=1), encoding="utf-8")
print(n, dict(c))
