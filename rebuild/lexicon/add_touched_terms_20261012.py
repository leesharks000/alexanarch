#!/usr/bin/env python3
"""LEXICON PASS 6 — 2026-10-12. Terms the archive substantially defines, redefines or reworks, not yet in the lexicon.

Criterion (the operator's, 2026-10-12): the lexicon is not only for coinages but for terms the archive has
substantially touched or modified — not every passing term. A term is added here only when a deposit does
definitional work on it: a bolded definition, an 'X is / names / denotes' sentence, a 'what we call' clause,
a declared concept (defines_concepts), or a titled or sectioned treatment.

Sources read: (1) a scan of every deposit text for definitional signals (bolded heads, headings, 'what we call',
'the term', 'X is the', title segments), 1,836 candidates read by hand; (2) the registry's declared concepts
missing from the lexicon, 614 read by hand. Each kept term's definition is taken from the archive's own
defining sentence, chosen and read term by term (read-20261012-touched-terms.tsv).

Classes:
  coinage                 — the term is the archive's.
  archive-reworked term   — an established word or term the archive gives its own fixed sense
                            (meter, enjambment, aura, negative capability ...); the definition is the archive's sense.
definition_status 'context' marks an entry whose definition is the defining context rather than a clean
definitional sentence.

Nothing is deleted; entries are appended.
"""
import json, pathlib, csv
ROOT = pathlib.Path(__file__).resolve().parents[2]
LEX = ROOT / "data/lexical-minting-registry.json"
TSV = pathlib.Path(__file__).with_name("read-20261012-touched-terms.tsv")
L = json.loads(LEX.read_text(encoding="utf-8"))
R = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
have = {t["term"].strip().lower() for t in L["terms"]}
added = {"coinage": 0, "archive-reworked term": 0}; ctx = 0
for row in csv.DictReader(TSV.open(encoding="utf-8"), delimiter="\t"):
    term, cls, dep, dfn, st = row["term"], row["class"], int(row["deposit"]), row["definition"], row["status"]
    assert cls in added, cls
    if term.lower() in have: continue
    e = {"term": term, "definition": dfn, "defined_in_deposit": dep,
         "defined_in_title": (R.get(dep, {}).get("title") or "")[:80], "type": "read",
         "mint_batch_size": 1, "mint_mode": "lexicon pass 6 (read)",
         "entry_class_all": [cls], "entry_class": cls,
         "entry_class_basis": "read 2026-10-12 (pass 6): " + ("a coinage of the archive" if cls == "coinage"
                               else "an established term the archive gives its own sense")}
    if st: e["definition_status"] = st; ctx += 1
    L["terms"].append(e); have.add(term.lower()); added[cls] += 1
L["total_terms"] = len(L["terms"])
L["_CLEANING"]["passes"].append({"date": "2026-10-12", "pass": 6, "script": "rebuild/lexicon/add_touched_terms_20261012.py",
    "read": "definitional-signal scan of all deposit texts (1,836 candidates) and the registry's undeposited declared concepts (614), by hand",
    "added": added, "definition_status_context": ctx,
    "principle": "terms the archive substantially defines or reworks, not every passing term; definitions are the archive's own sentences; nothing deleted"})
LEX.write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
print(added, "context:", ctx, "total:", L["total_terms"])
