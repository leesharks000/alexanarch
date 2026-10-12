#!/usr/bin/env python3
"""Lexicon passes 3 and 4 (2026-10-12): the single-word and two-word terms, read by hand.

Pass 4 applies the same rule to the 5,528 two-word entries, where the added classes are article + noun sentence
heads ('A theorist', 'A creature'), labelled fields and sections ('Canonical URL', 'Companion Documents', 'Day 3',
'Logion 22', 'Rule 7'), and lowercase phrase fragments ('accelerate collapse', 'cannot know'). Kept: the archive's
coined two-word vocabulary ('semantic samizdat', 'relational enclosure', 'Semantic Rent'), operator codes and
room/section codes ('MPM-07 Patch', 'r.07 Revelation', 'R2 compression').


All 2,278 one-word entries were read (term and the head of its definition). An entry is marked
entry_class 'not-a-term' when it is not a minted term: an ordinary English word glossed in passing ('Theorist',
'Accuracy', 'Fire'), a field label whose 'definition' is a value ('Affiliation: Johannes Sigil Institute…'), a
function word or sentence head ('about', 'and', 'cannot'), a filename, or another person's name ('Adorno').
Kept, unflagged: coinages ('Ambidextrose', 'campification'), notation and protocol codes ('A_cred', 'ALLOW_FLAG'),
the archive's own operator, room and status names ('Archon', 'Bride', 'Caster', 'Dormant', 'PROVISIONAL'),
heteronym names, and Greek philosophical terms carried as concepts ('Ataraxia', 'kairos').
NOTHING IS DELETED (_CLEANING principle, 2026-08-14). The indices read are in read-20261012-single-word-not-a-term.txt.
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
LEX = ROOT / "data/lexical-minting-registry.json"
# usage: apply_read_flags_20261012.py [words] [pass]   — 1 → single-word list (pass 3), 2 → two-word list (pass 4)
WORDS = int(sys.argv[1]) if len(sys.argv) > 1 else 1
PASS = int(sys.argv[2]) if len(sys.argv) > 2 else 3
LIST = {1: "read-20261012-single-word-not-a-term.txt", 2: "read-20261012-two-word-not-a-term.txt"}[WORDS]
LABEL = {1: "single-word", 2: "two-word"}[WORDS]
ids = [int(x) for x in (pathlib.Path(__file__).parent / LIST).read_text().split()]
lex = json.loads(LEX.read_text(encoding="utf-8")); T = lex["terms"]
n = 0
for i in ids:
    t = T[i]
    assert len((t.get("term") or "").split()) == WORDS, (i, t.get("term"))
    allc = list(t.get("entry_class_all") or ([t["entry_class"]] if t.get("entry_class") else []))
    if "not-a-term" not in allc:
        allc.append("not-a-term")
    t["entry_class_all"] = allc
    t.setdefault("entry_class", "not-a-term")
    t["entry_class_basis"] = f"read 2026-10-12 (pass {PASS}, {LABEL} terms): not a minted term"
    n += 1
c = lex.setdefault("_CLEANING", {}); c.setdefault("passes", [])
total = sum(1 for t in T if len((t.get("term") or "").split()) == WORDS)
c["passes"].append({"date": "2026-10-12", "pass": PASS, "script": "rebuild/lexicon/apply_read_flags_20261012.py",
                    "read": f"all {total:,} {LABEL} entries, by hand", "marked_not_a_term": n,
                    "kept": total - n, "principle": "nothing deleted; entry_class 'not-a-term' with entry_class_basis"})
LEX.write_text(json.dumps(lex, ensure_ascii=False, indent=1), encoding="utf-8")
print("marked", n)
