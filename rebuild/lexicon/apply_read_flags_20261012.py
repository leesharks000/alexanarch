#!/usr/bin/env python3
"""Lexicon pass 3 (2026-10-12): the single-word terms, read by hand.

All 2,278 one-word entries were read (term and the head of its definition). An entry is marked
entry_class 'not-a-term' when it is not a minted term: an ordinary English word glossed in passing ('Theorist',
'Accuracy', 'Fire'), a field label whose 'definition' is a value ('Affiliation: Johannes Sigil Institute…'), a
function word or sentence head ('about', 'and', 'cannot'), a filename, or another person's name ('Adorno').
Kept, unflagged: coinages ('Ambidextrose', 'campification'), notation and protocol codes ('A_cred', 'ALLOW_FLAG'),
the archive's own operator, room and status names ('Archon', 'Bride', 'Caster', 'Dormant', 'PROVISIONAL'),
heteronym names, and Greek philosophical terms carried as concepts ('Ataraxia', 'kairos').
NOTHING IS DELETED (_CLEANING principle, 2026-08-14). The indices read are in read-20261012-single-word-not-a-term.txt.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
LEX = ROOT / "data/lexical-minting-registry.json"
ids = [int(x) for x in (pathlib.Path(__file__).parent / "read-20261012-single-word-not-a-term.txt").read_text().split()]
lex = json.loads(LEX.read_text(encoding="utf-8")); T = lex["terms"]
n = 0
for i in ids:
    t = T[i]
    assert len((t.get("term") or "").split()) == 1, (i, t.get("term"))
    allc = list(t.get("entry_class_all") or ([t["entry_class"]] if t.get("entry_class") else []))
    if "not-a-term" not in allc:
        allc.append("not-a-term")
    t["entry_class_all"] = allc
    t.setdefault("entry_class", "not-a-term")
    t["entry_class_basis"] = "read 2026-10-12 (pass 3, single-word terms): not a minted term"
    n += 1
c = lex.setdefault("_CLEANING", {}); c.setdefault("passes", [])
c["passes"].append({"date": "2026-10-12", "pass": 3, "script": "rebuild/lexicon/apply_read_flags_20261012.py",
                    "read": "all 2,278 single-word entries, by hand", "marked_not_a_term": n,
                    "kept": 2278 - n, "principle": "nothing deleted; entry_class 'not-a-term' with entry_class_basis"})
LEX.write_text(json.dumps(lex, ensure_ascii=False, indent=1), encoding="utf-8")
print("marked", n)
