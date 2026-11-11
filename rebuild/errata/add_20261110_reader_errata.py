#!/usr/bin/env python3
"""Errata entries in the registry's `errata` field (the sidecar below each deposit; the deposited bytes and the AXN untouched), at the author's
word of 2026-11-10 22:36-22:38: "lets just add errata notes at the bottom of those records, i dont want to reversion everything ... in the metadata
i mean". The defects were noted by the eight readers who read these records in full for the argument layer of EA-HK-ORTHONYM-01 v1.3 (#1754), and
each was checked against the seated text before entry: every `was` below is asserted to occur in the record as it stands. Reference, citation,
source, count and consistency defects only (#1677 §10; the author, 2026-10-13). Markup defects (doubled headings, flattened lists) are not entered.
   python3 rebuild/errata/add_20261110_reader_errata.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
BY = "reader of 2026-11-10 (the argument-layer reading for #1754 v1.3), checked against the seated text"
REASON = 'Lee Sharks, 2026-11-10: "lets just add errata notes at the bottom of those records, i dont want to reversion everything"; "in the metadata i mean"'
E = [
 (938, "reference", "header, Reserved AXN", "**Reserved AXN:** #939 / hex 03B7", "The record is deposit #938, hex 03B6."),
 (136, "reference", "the kernel's stripProtection note", "(XII Coda)", "The body and the Abstract place the performative enactment at §X and the seal at §XI; the record has no §XII."),
 (136, "citation", "Suggested Citation", "Heteronymy, Authorial Law, and the Unbounded Configuration", "The deposit's title is: The Chaerephon Problem: Heteronymy as Symbolon — Authorial Law, the Unbounded Configuration, and Propagation by Cascading Philological Failure."),
 (136, "source", "the closing heading", "## Deposit Information\n\nThis paper is part of", "No defect: the heading has a body. The reader's report of an empty final heading did not hold on checking, and no entry is made."),
 (1603, "reference", "Appendix A, A2 and E.5", "§3 of the note", "The peirastic identification is made in §4 of this paper; '§3 of the note' points into the earlier version."),
 (1603, "count", "Appendix A §E, the numbered list", "8. **The fork's second horn", "The list runs 1–5, then 7–8; there is no item 6."),
 (1574, "count", "Abstract", "across four commercial language models", "Two models: §2, §3.3 and B5 state 'Twenty rounds, two models, eleven configurations'."),
 (1574, "reference", "§3.4", "reports 16 and 17 in B5", "B5 lists the v1.9 pair as R17/R18 and the v2.0 pair as R19/R20; §3.4's 'reports 16 and 17' and 'reports 18 and 19' are each one lower."),
 (1574, "count", "checklist, item 1", "v0.9 adds five first-person-verb locations", "Four locations are listed (προειλόμεθα 183a37, ὑπεθέμεθα 183b3, εἰρήκαμεν 183b6, διεληλύθαμεν 183b13)."),
 (1574, "reference", "A7, entry 10", "(SE 18, 177a?–)", "The locus is unresolved in the text; to be supplied."),
 (1582, "consistency", "§5", "voted by a polis", "§0 corrects the granting body to the Delphic Amphictyony, 'not simply the polis of Delphi'; §5 still says 'voted by a polis' and 'the polis's stone'."),
 (1583, "quotation", "Abstract", "μέχρι μὲν δὴ τούτων ἄρτιος ὁ λόγος …", "The seated hinge, as §2 quotes it, reads 'μέχρι μὲν δὴ τούτων οἷον ἄρτιος ὁ λόγος'; the Abstract drops οἷον inside the quotation."),
 (1588, "count", "evidence table", "agree with the data at 74–76%", "The JSON block gives 25/34, 24/34 and 26/34, which are 73.5%, 70.6% and 76.5%: a range of 71–76%."),
 (1588, "count", "evidence table", "fourteen held-out texts with labels fixed in advance project onto the axis at 11/12", "The count of texts (fourteen) and the denominator (12) differ; to be reconciled."),
 (1593, "count", "Abstract and the matched-removal paragraph", "Name recovery falls to 0.564 when the botanical and zoological works are removed", "The rebuilt §5c table and the conditional claim give 0.547 (p = 0.273) for the same removal; the two figures are not reconciled in the text."),
 (1593, "code", "Appendix R, report()", "'attribution_accuracy': S['accuracy'], 'baseline': S['baseline']", "The repaired attribute() returns block_accuracy and majority_baseline; report() as delivered raises a KeyError."),
 (1593, "reference", "Appendix R, the elision comment", "(Paper §4.2.)", "The elision material is in §2."),
 (1597, "source", "THE WORK, RENDERED, unit 42 (w1134–1192)", "But how one ought to posit the principles, and of what sort, one might well raise as a difficulty", "This sentence closes unit 42's rendering and is the opening of unit 7 (w1192–1227), which renders it again; the Greek of unit 42 does not contain it."),
 (1597, "source", "THE WORK, RENDERED, units 24 and 34", "For the necessary is spoken of in these many ways", "Rendered as the close of unit 24; in the Greek it opens unit 34, whose rendering then repeats the end of unit 24. Units 6 and 8 end on '…' and unit 19 opens on '…'; whether the rendering omits Greek at those points is to be checked."),
 (1597, "source", "the Greek of the Theophrastan lines", "Κύριπίδην", "OCR damage in the seated Greek: Κύριπίδην, ἀπαιτοῦνμέχρι, ἰόνκ, τοιαύ1η, ἀρίστοῦ, ζώυις, ἀρ χῶν, φνσιν, μέγνστον, λαμνβάνειν, σύμιπαντος."),
 (1563, "source", "the seat table, both rows", "underlying edition public  |", "A word is missing: 'underlying edition public domain'."),
 (1570, "source", "after M52", "∮ = 1 on Pessoa.** Pooling", "A stray copy of the M17 paragraph, with its comparator and limits lines, follows M52."),
 (1570, "reference", "§27 and §33.2", "(see M39, M40b, M40c, all corrected)", "The register has no entries labelled M40b or M40c; it also has no §29 (§28 M39 is followed by §30 M41), and §36 runs 36.7, 36.9–36.11, 36.8."),
 (1580, "source", "Seat 12/01, the wills", "Ἀστυἀνακτι", "Read Ἀστυάνακτι. The Aristotle will also carries '. , ὡς καὶ πατὴρ ὢν' and 'ἐξάγειν αὐτά .', remainders of the apparatus removal."),
 (1569, "count", "Rounds 41 and 42", "## 165. THE ANCIENT BRANCH", "§165 and §166 each occur twice: in Round 41 (THE ANECDOTE IS A TRANSFER; AND THIS IS THE SECOND INSTANCE) and in Round 42 (THE ANCIENT BRANCH; THE MODERN BRANCH)."),
 (1569, "source", "Part II §0", "σύμBOΛΟΝ", "Read σύμΒΟΛΟΝ: the B and O are Latin capitals in place of Greek Β and Ο."),
 (1575, "reference", "§VIII and §IX notes", "[VIII.1] ⭑ VLASTOS AND THE DEVELOPMENTAL", "The §IX notes are keyed [VIII.1]–[VIII.6], the keys of the §VIII notes, so 'papyrology [VIII.4]' (§IX.52) and 'The CPF [VIII.4]' ([F.5]) are ambiguous."),
 (1575, "count", "§I", "## 4. THE SHAPE", "§I's subsections run 1, 2, 4; there is no 3."),
 (1667, "count", "after the concordance", "the method refused (2)", "The per-join counts sum to 12 against the eleven Α insertions the sentence names; the '(2)' at the method refused counts units, and 'the account totalled (1)' holds two units (A581, A614)."),
 (1584, "count", "§4", "puts that vocabulary at 16.08 per thousand in *EN* II–IV and at 0.45 in the *Characters*", "The §6 table gives 12.76 (EN II–IV) and 0.15 (Characters); the inference from the §4 figures is withdrawn in the record, and the two sets of figures are not reconciled."),
 (167, "consistency", "§1.2 and §5.2", "it included Xenophon alongside Plato", "§5.2 says the response 'substituted Xenophon for Aristotle'; the two accounts of the same response differ."),
 (167, "reference", "Assembly Substrate Cross-Check", "(manual action, algorithmic adjustment, knowledge-panel enclosure, composition amnesia)", "§7 lists stabilization, softening, provenance erasure and source replacement."),
 (167, "source", "Figures 1–4", "lee-sharks-unquoted-2026-06-05.png", "The figures are named by filename and not embedded."),
 (1734, "reference", "matrix and FAQ", "keeps the four biographies apart (§0.1)", "§0.1, §0.4, §1.6, §8.8 and §4.5 are sections of Legitimately Many (#1733); this packet's §0 is the Executive symbolon."),
 (1732, "reference", "32/12, Normalization", "reduced to one block per fragment by build31.py", "'How the seats were made' names build32.py as the builder; to be confirmed whether build31.py's reducer was reused."),
]
added = 0
for n, kind, locus, was, now in E:
    if "No defect" in now: continue
    t = (ROOT / D[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    assert was in t, (n, was[:60])
    ent = {"date": "2026-11-10", "kind": kind, "locus": locus, "was": was, "now": now, "reason": REASON, "raised_by": BY, "status": "open"}
    ex = D[n].setdefault("errata", [])
    if any(e.get("was") == was and e.get("date") == "2026-11-10" for e in ex if isinstance(e, dict)): continue
    ex.append(ent); added += 1
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
print("errata added:", added, "records:", len({e[0] for e in E if 'No defect' not in e[4]}))
