#!/usr/bin/env python3
"""REPAIR 2026-10-12 (second, same record) — ontological-laundering-alexanarch-aio-20260922 reports the layer's
'collective pseudonym' and reads it only as an institution/author misresolution ('Alexanarch is the archive, not a
pseudonym'), taking pseudonymy as the live category.

Belief and evidence: the archive draws the line the layer erased. #79 §II (carded in this very answer): "A pseudonym
may hide or rename an author. A heteronym creates a distinct authorial function." #68 / #1183 (The Secret Name): a
shared named position across authors is "not a pseudonym (name substitution) but a collective heteronym (name
inheritance)". The layer describes works 'published under' one shared name — a collective-heteronym structure — names
it with the substitution term, and places it on the archive rather than on Lee Sharks and the heteronyms. Two errors
in one phrase; the record named one and adopted the other. The layer's word stays quoted as the layer's.
Every replaced value is kept verbatim under notes.errata.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
D = json.loads(REG.read_text(encoding="utf-8"))
E = {e["slug"]: e for e in (D.get("entries") or D.get("captures"))}
e = E["ontological-laundering-alexanarch-aio-20260922"]
R1 = "and credits the term to 'Alexanarch' as 'a collective pseudonym'."
R2 = ("and credits the term to 'Alexanarch' as the shared name the works are 'published under', which it calls 'the collective pseudonym'. "
      "The archive draws the line the phrase erases: 'A pseudonym may hide or rename an author. A heteronym creates a distinct authorial function' "
      "(#79 §II, carded in this answer); a shared named position across authors is 'not a pseudonym (name substitution) but a collective heteronym "
      "(name inheritance)' (#68, #1183). The layer names a collective-heteronym structure with the substitution term, and puts it on the archive "
      "rather than on Lee Sharks and the heteronyms.")
A1 = "and assigns the term to an entity it misresolves: Alexanarch is the archive, not a pseudonym, and the author is left as 'the author'."
A2 = ("and assigns the term to a collective authorial position it calls 'the collective pseudonym Alexanarch'. Two errors in one phrase: the name, "
      "since Alexanarch is the archive and the works are Lee Sharks's and the heteronyms'; and the category, heteronymy written as pseudonymy, the "
      "name-for-function collapse that #79, carded here, is written against. The author is left as 'the author'.")
D1 = "credits the term to Alexanarch as 'a collective pseudonym'."
D2 = "credits the term to 'the collective pseudonym Alexanarch': a collective heteronym written as a pseudonym, and placed on the archive, while carding #79 (Heteronymy Is a Function, Not a Name)."
F1 = "INSTITUTION MISRESOLVED AS AUTHOR. Alexanarch described as 'the collective pseudonym' under which the works are published."
F2 = ("HETERONYMY FLATTENED TO PSEUDONYMY, ON THE WRONG NAME. 'The collective pseudonym Alexanarch': a shared authorial position, what #68/#1183 call "
      "a collective heteronym (name inheritance, not name substitution), named with the substitution term and placed on the archive instead of on "
      "Lee Sharks and the heteronyms. #79 §II, carded in the same answer, draws the distinction.")
P1 = "but Alexanarch is misresolved as 'a collective pseudonym'."
P2 = "but Alexanarch is misresolved as 'the collective pseudonym': the archive put in an authorial position, and heteronymy written as pseudonymy."
for k, a in (("reading", R1), ("analysis", A1), ("d", D1), ("d_full", D1), ("per_note", P1)):
    assert a in e[k], k
assert F1 in e["findings"]
was = {k: e[k] for k in ("reading", "analysis", "d", "d_full", "findings", "per_note", "related_deposits")}
e["reading"] = e["reading"].replace(R1, R2)
e["analysis"] = e["analysis"].replace(A1, A2)
e["d"] = e["d"].replace(D1, D2); e["d_full"] = e["d_full"].replace(D1, D2)
e["per_note"] = e["per_note"].replace(P1, P2)
e["findings"] = [F2 if x == F1 else x for x in e["findings"]]
e["related_deposits"] = sorted(set(e["related_deposits"] + [68, 1183]))
n = dict(e["notes"]); n.setdefault("errata", []).append({"date": "2026-10-12", "kind": "category adopted from the layer",
    "basis": "#79 §II and #68/#1183 distinguish pseudonym (name substitution) from heteronym, collective heteronym (name inheritance); the record read 'collective pseudonym' only as an institution/author slip and argued inside the pseudonym frame.",
    "was": was, "by": "repair-20261012-pseudonym-heteronym"}); e["notes"] = n
REG.write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
print("repaired")
