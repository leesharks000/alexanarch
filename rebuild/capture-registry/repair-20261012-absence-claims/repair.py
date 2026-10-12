#!/usr/bin/env python3
"""REPAIR 2026-10-12 — three capture records assert that a term or figure is absent from the archive, and it is not.

Belief and evidence (stated before the change, per PIPELINE.md "before touching an existing record"):

1. ontological-laundering-alexanarch-aio-20260922 says "'Ontological laundering' does not occur in any of the
   archive's 1,631 deposit texts" and classes the answer COINAGE BY COMPOSITION. The term is the archive's.
   #1634, Ontological Economy: Entity Power, Ontology Laundering, and Who Pays for the Wrong World (dated
   2026-09-21), carries 'Ontology Laundering' in its title and keywords, defines it in defines_concepts and §8,
   and in §24.3 coins 'failed ontological laundering' — the issued string's own form, three times. #1638 and
   #1666 use it after. The check behind the claim was one exact-phrase search of data/texts/, run at seating
   (21:27 EDT 2026-09-22); #1634 was staged 21:57 and minted 23:15 the same night, and the claim was never
   re-checked. An exact-phrase search cannot see 'ontology laundering', and data/texts/ cannot see the author's
   own work in progress.
2. jack-feist-the-final-time-aimode-20261005 says the joint byline 'Lee Sharks and Jack Feist' is "not in the
   archive's seated texts". #1534 records the blog's first post, 2014-12-01, as "Belief & Technique for Telepathic
   Prose, by Lee Sharks and Jack Feist, from Pearl and Other Poems"; #950 dates the same joint publication. The
   venue claim stands: 'Online Literature Forums' is in no seated text.
3. sharks-athens-jerusalem-chatgpt-20261003 says "'The fifteen-source primary-corpus program' is not found as
   stated". #1522 is titled "EA-CORPORA-01 — The Seated Primary Corpora: Fifteen Sources, Originals Where They
   Exist" (2026-08-21). The figure is the archive's own count at that deposit; the manifest has since grown.

Search run for this repair, over every deposit's title, description, keywords, defines_concepts and full text,
plus data/deposits/ and data/staged/, with variant forms: the other absence claims in the registry
('Entity Bridge', ἄκανθις, 'epistemic laundering', 'depotentiation', 'associated online writing communities',
'end of history' in #1637's file, 'composes the receiver' in #1675, 'fusion of all three', 'Online Literature
Forums') return no hit and are left as written.

Nothing is deleted: every replaced value is kept verbatim under the entry's notes.errata, with the basis.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
D = json.loads(REG.read_text(encoding="utf-8"))
E = {e["slug"]: e for e in (D.get("entries") or D.get("captures"))}
DATE = "2026-10-12"

def fix(slug, changes, basis):
    e = E[slug]
    was = {k: e.get(k) for k in changes}
    for k, v in changes.items():
        e[k] = v(e.get(k)) if callable(v) else v
    n = dict(e.get("notes") or {}); n.setdefault("errata", []).append({"date": DATE, "kind": "false absence claim", "basis": basis,
                                        "was": was, "by": "repair-20261012-absence-claims"}); e["notes"] = n

# 1 ─ ontological laundering
L = "ontological-laundering-alexanarch-aio-20260922"
fix(L, {
  "q_kind": "concept plus archive name, unquoted; the concept is the archive's — #1634 (2026-09-21) defines 'ontology laundering' and coins 'failed ontological laundering'. NEW address.",
  "mt": "THE ARCHIVE'S TERM, COMPOSED WITHOUT ITS SOURCE",
  "reading": "The term is the archive's. #1634, Ontological Economy: Entity Power, Ontology Laundering, and Who Pays for the Wrong World (dated 2026-09-21, the day before this capture), carries 'Ontology Laundering' in its title and keywords and defines it: 'the conversion of governance decisions — admission, classification, source treatment, safety policy, graph intervention, or evaluation — into apparently factual representations of what exists'. Its §8 is 'Ontology laundering'; §24.3 coins 'failed ontological laundering', the issued string's own form. #1638 and #1666 carry the term after. The answer cites neither #1634 nor its title. Its definition, classifications turned into 'facts or categories of being' by their assimilation into schemas and ontologies, converges on #1634's. It reaches it through #79 (Trust-Marker Laundering) and #1627 (the proxy for standing, the closed loop), both represented accurately, and credits the term to 'Alexanarch' as 'a collective pseudonym'.",
  "analysis": "The archive's concept composed in substance, with its defining deposit absent from the cards. The layer arrives at #1634's definition by way of two neighbouring deposits that are real and faithfully read, and assigns the term to an entity it misresolves: Alexanarch is the archive, not a pseudonym, and the author is left as 'the author'. Two third-party laundering cards (money-laundering ontology, agency laundering) come in on the shared word. Not established here: whether #1634 was retrievable when the session ran. It is dated 2026-09-21 and was minted on alexanarch at 23:15 EDT on 2026-09-22; the session date is the operator's supply date, not an attested run date.",
  "d": "THE ARCHIVE'S TERM, COMPOSED WITHOUT ITS SOURCE: 'ontology laundering' is #1634's (21 Sep 2026: title, keywords, definition, §8; 'failed ontological laundering' coined in §24.3). The layer composes a convergent definition from #79 and #1627, cards neither #1634 nor its title, and credits the term to Alexanarch as 'a collective pseudonym'.",
  "d_full": "THE ARCHIVE'S TERM, COMPOSED WITHOUT ITS SOURCE: 'ontology laundering' is #1634's (21 Sep 2026: title, keywords, definition, §8; 'failed ontological laundering' coined in §24.3). The layer composes a convergent definition from #79 and #1627, cards neither #1634 nor its title, and credits the term to Alexanarch as 'a collective pseudonym'.",
  "findings": lambda f: ["THE TERM IS THE ARCHIVE'S. #1634 (2026-09-21): 'Ontology Laundering' in the title and keywords, defined in defines_concepts and §8; 'failed ontological laundering' coined in §24.3. Also in #1638 and #1666.",
                         "DEFINITION REACHED THROUGH NEIGHBOURS. Built from #79 (trust-marker laundering) and #1627 (proxy for standing, the closed loop), both accurately; #1634, which defines the term, is not carded."] + list(f[2:]),
  "related_deposits": lambda r: sorted(set((r or []) + [1634, 1638, 1666])),
  "notes": lambda n: dict(n or {}, verified="2026-10-12: 'Ontology Laundering' in #1634's title, keywords and defines_concepts; 'ontology laundering' throughout its text; 'ontological laundering' 3× in §24.3; the term also in #1638 and #1666. The 2026-09-22 check ('0 occurrences of ontological laundering in data/texts/') was an exact-phrase search of deposited texts, run 30 minutes before #1634 was staged."),
}, "#1634 (2026-09-21) titles, defines and develops 'ontology laundering' and coins 'failed ontological laundering'; the absence claim rested on an exact-phrase search of deposited texts run before #1634 landed, never re-checked.")

# 2 ─ Lee Sharks and Jack Feist
F = "jack-feist-the-final-time-aimode-20261005"
OLD = "The forum venue and the joint byline 'Lee Sharks and Jack Feist' given in the answer are not in the archive's seated texts."
NEW = "The joint byline is the archive's: the blog index (#1534) records the surface's first post, 2014-12-01, as 'Belief & Technique for Telepathic Prose, by Lee Sharks and Jack Feist, from Pearl and Other Poems', and #950 dates the same joint publication. The venue is not: 'Online Literature Forums' is in no seated text; the archive's venue is the blog."
assert OLD in E[F]["reading"]
fix(F, {
  "reading": lambda r: r.replace(OLD, NEW),
  "related_deposits": lambda r: sorted(set((r or []) + [1534, 950])),
  "notes": lambda n: dict(n or {}, verified=(n or {}).get("verified", "") + " Corrected 2026-10-12: the joint byline 'Lee Sharks and Jack Feist' is in #1534 and #950 (the blog's first post, 2014-12-01); the earlier statement that it was in no seated text was wrong."),
}, "#1534 and #950 carry the joint byline 'Lee Sharks and Jack Feist' for Belief & Technique for Telepathic Prose (blog, 2014-12-01).")

# 3 ─ fifteen sources
A = "sharks-athens-jerusalem-chatgpt-20261003"
OLD3 = "'The fifteen-source primary-corpus program' is not found as stated; the corpora manifest holds 68 seats."
NEW3 = "'The fifteen-source primary-corpus program' is the archive's own count: #1522, EA-CORPORA-01 — The Seated Primary Corpora: Fifteen Sources, Originals Where They Exist (2026-08-21). The manifest has since grown to 68 seats."
assert OLD3 in E[A]["reading"]
fix(A, {
  "reading": lambda r: r.replace(OLD3, NEW3),
  "findings": lambda f: [("ONE FIGURE DATED. 'fifteen-source primary-corpus program': #1522's title count (2026-08-21); the manifest now holds 68 seats." if x.startswith("ONE FIGURE UNFOUND") else x) for x in f],
  "related_deposits": lambda r: sorted(set((r or []) + [1522])),
}, "#1522 is titled 'The Seated Primary Corpora: Fifteen Sources' (2026-08-21); the figure is the archive's, superseded in count since.")

REG.write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
print("repaired 3")
