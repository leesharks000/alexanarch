#!/usr/bin/env python3
"""REVERT 2026-10-12 — the two repairs of ontological-laundering-alexanarch-aio-20260922 made earlier today
(repair-20261012-absence-claims, repair-20261012-pseudonym-heteronym) rewrote an analysis that was accurate as written.

Timeline (registry and git): the term first appears in EA-ONTOLOGICAL-ECONOMY-01 v0.12, a working draft dated
2026-09-21; the capture was supplied 2026-09-22 and seated 21:27 EDT; the paper was staged 21:57 and minted as #1634 at
23:15 EDT. At seating no deposited text carried 'ontological laundering' or 'ontology laundering', and the issued string
carried an unpublished term. 'Coinage by composition' is the right reading: the layer presented the term as an
established Alexanarch concept and composed its definition, as a unit, out of #79 and #1627. The repairs treated a
later deposit as evidence against a record written before it.

This script restores every field the repairs changed to its value before the first repair (taken from that repair's
notes.errata 'was'), keeps both errata entries and adds a third marking them reverted, and adds one dated note:
#1634 deposits the term after seating — a later fact, not a correction.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
D = json.loads(REG.read_text(encoding="utf-8"))
E = {e["slug"]: e for e in (D.get("entries") or D.get("captures"))}
e = E["ontological-laundering-alexanarch-aio-20260922"]
errata = list(e["notes"]["errata"])
first = next(x for x in errata if x["by"] == "repair-20261012-absence-claims")
second = next(x for x in errata if x["by"] == "repair-20261012-pseudonym-heteronym")
orig = dict(second["was"]); orig.update(first["was"])      # first repair's 'was' is the pre-repair state
notes0 = orig.pop("notes")
for k, v in orig.items():
    e[k] = v
n = dict(notes0 or {})
n["errata"] = errata + [{"date": "2026-10-12", "kind": "repairs reverted",
    "basis": "The analysis was accurate as written: at seating (21:27 EDT 2026-09-22) no deposited text carried the term; the issued string carried an unpublished term from the 2026-09-21 working draft, minted as #1634 at 23:15 EDT. The two repairs used a later deposit against an earlier record.",
    "reverts": ["repair-20261012-absence-claims", "repair-20261012-pseudonym-heteronym"], "by": "repair-20261012-revert-laundering"}]
n["subsequent_deposit"] = ("2026-09-22, 23:15 EDT, after seating: #1634, Ontological Economy: Entity Power, Ontology Laundering, and Who Pays for the "
    "Wrong World (EA-ONTOLOGICAL-ECONOMY-01 v0.12, working draft dated 2026-09-21), deposits the term — 'Ontology Laundering' in the title, "
    "'ontology laundering' defined (defines_concepts, §8), 'failed ontological laundering' in §24.3. The issued string carried the term "
    "from that draft before it was published. Recorded 2026-10-12.")
e["notes"] = n
e["related_deposits"] = sorted(set(e["related_deposits"] + [1634]))
REG.write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
print("reverted; fields restored:", sorted(orig))
