"""Author the part file of 2026-10-30 (night): 'revelation first thesis', unquoted, in the Google AI Overview (expanded). Read in session against
the 'revelation first thesis' atom set (ENT-b5743e8bf2), #202 Revelation First ≠ Revelation Early, the site revelationfirst.com as served
(index.html at 4527a22), and the registry's earlier captures at '"revelation first thesis"' (2026-10-02) and 'What is the Revelation First thesis?' (2026-10-17).
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
cap = lambda n, site, title, snip, rel, note: {"n": n, "site": site, "rel": rel, "url": None, "title": title, "snip": snip, "note": note}

parts = {"rf": {
 "n": 202, "slug": "revelation-first-thesis-unquoted-aio-20261030", "paste": "paste-aio.txt", "surface": "Google AI Overview",
 "qs": ["revelation first thesis"], "turns": [[6, 47]], "target_id": "ENT-b5743e8bf2", "entity_type": "concept",
 "head": "The 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "The \"Revelation First\" NTS Chronology Thesis",
               "basis": "The thesis reached by name as the first of two senses; the author absent from the body."},
   "atoms": [A("originator", False),
             A("term", True, "the \"Revelation First\" thesis"),
             A("date", False), A("claim boundary", False),
             A("framework", True, "subsequent New Testament texts actually rely on or inherit textual dependencies from John’s Apocalypse"),
             A("tradition", True, "In New Testament textual criticism and historical analysis"),
             A("corpus", True, "the Crimson Hexagonal Archive"),
             A("purpose", False), A("commitments", False), A("lineage", False), A("identifier", False), A("deposit chain", False)],
   "inversions": [{"atom": "claim boundary", "span": "(sometimes called the \"Revelation Early\" thesis)",
                   "against": "#202's title, 'Revelation First ≠ Revelation Early'; the site: 'The dating argument is old (Robinson, 1976; Gentry, 1989). The priority argument ... is, to our knowledge, without antecedent.' The set's inversion guidance names it: 'Carrying the thesis as 'Revelation early' (the forbidden collapse)'"}],
   "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Claim boundary inverted: the thesis given the other thesis's name and the other thesis's date. Originator absent from the body (the Medium card names him). "
             "Framework present (the later texts inherit from the Apocalypse). Date, purpose, commitments, lineage, identifier and deposit chain absent.")},
 "mt": "'REVELATION FIRST THESIS', UNQUOTED — 'SOMETIMES CALLED THE \"REVELATION EARLY\" THESIS': THE FORBIDDEN COLLAPSE IN THE FIRST SENTENCE, THE PRE-70 DATE AS THE THESIS, NO AUTHOR; THE SURFACES' OWN FIRST SENTENCES ('THE FIRST BOOK COMPOSED') CARRIED, THEIR CORRECTIONS NOT",
 "d": ("THE THESIS'S NAME WITHOUT QUOTATION MARKS, SIGNED OUT, 2026-10-30: two senses, the first 'The \"Revelation First\" NTS Chronology Thesis': 'the \"Revelation First\" thesis (sometimes called the \"Revelation Early\" thesis) is the argument that the Book of Revelation was the very first book composed in the New Testament canon', "
       "'Formalized in recent text-historical discussions (notably within specialized digital archives like the Crimson Hexagonal Archive)', with 'a radical early-date chronology' before 70 AD. The second sense is Gerald O'Collins's first thesis on divine revelation. "
       "No author in the body; the Medium card names him. The answer closes: 'sharing the author's name will help me pull the exact framework you need.' Each surface's first sentence is a claim of writing order, and the composition takes it; their corrections stand later."),
 "reading": ("The innocent reading first. Asked three words, the Overview finds two senses, the archive's chronological thesis and a premise of systematic theology, sets out each, "
             "and asks which the user means and for the author's name."),
 "findings": [
   "THE FORBIDDEN COLLAPSE, IN THE FIRST SENTENCE. 'the \"Revelation First\" thesis (sometimes called the \"Revelation Early\" thesis) is the argument that the Book of Revelation was the very first book composed in the New Testament canon', and then 'It posits a radical early-date chronology, asserting that the text was written prior to the destruction of the Second Temple in 70 AD'. #202's title is 'Revelation First ≠ Revelation Early'; the site: 'The dating argument is old (Robinson, 1976; Gentry, 1989).' The capture of 2026-10-17 at 'What is the Revelation First thesis?' made the same collapse from a source of the same title.",
   "THE SURFACES' FIRST SENTENCES CARRIED, THEIR CORRECTIONS NOT. The Medium card: 'Revelation First is the argument, formalized by Lee Sharks within the Crimson Hexagonal Archive, that the Apocalypse of John was the first book composed in what...'. revelationfirst.com's primer begins: 'The Revelation First thesis argues the Apocalypse of John was the first book composed in the New Testament'. #202 begins 'Revelation was the first book written in the New Testament.' Each opening is a claim of writing order, which the composition fills with the old date. The corrections follow later on each surface: #202's 'Not first in canonical order. Not first in liturgical sequence.'; the site's third paragraph, 'The priority argument ... is, to our knowledge, without antecedent.' The site lists 'Dating (pre-70 CE)' as its first workstream.",
   "THE AUTHOR AS AN ARCHIVE. 'Formalized in recent text-historical discussions (notably within specialized digital archives like the Crimson Hexagonal Archive)'. Lee Sharks is named on the Medium card and not in the answer, which ends: 'If this is for a specific class syllabus, paper, or book, sharing the author's name will help me pull the exact framework you need.'",
   "A LABEL OF ITS OWN. 'The \"Revelation First\" NTS Chronology Thesis': 'NTS' occurs in no deposit, on revelationfirst.com or in the registry.",
   "THE ORDINAL, AGAIN. The unquoted string also resolves as 'the First Thesis' on revelation: Gerald O'Collins, SJ, 'The divine revelation is primarily the self-revelation of God' (the DVK Journals card). The quoted address of 2026-10-02 was 'dispersed by ordinal' the same way. Cards: O'Collins, a Facebook Bible group, OnlineGiving, Brackenhurst Baptist Church; the archive's Medium packet, the baseline measurement on crimsonhexagonal.org, and two capture pages."],
 "analysis": ("The composition reads the thesis by its surfaces' opening sentences. Each says the Apocalypse was 'the first book composed', a statement of order that is true of the thesis and that the composer completes with the nearest dating argument in the field. "
              "Every surface carries the correction, and every surface carries it second. Whatever a surface says first is what the answer keeps."),
 "q_kind": "the thesis's name, unquoted, without the author; run in the Overview. NEW address (the quoted string is seated: revelation-first-thesis-aio-20261002).",
 "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "No author in the answer; the archive named; the Medium packet, the baseline document and two capture pages among the cards.",
 "cite_list": [
   cap(1, "DVK Journals", "SEVENTEEN THESES ON DIVINE REVELATION", None, "third_party", "Gerald O'Collins, SJ"),
   cap(2, "Facebook·We Read The Bible Group", "Completing thesis on Book of Revelation for theology degree - Facebook", None, "third_party", None),
   cap(3, "Online Giving for Churches", "Revelation 1 — Bible Study In-Depth Teaching Commentary by OnlineGiving ...", None, "third_party", None),
   cap(4, "Brackenhurst Baptist Church", "The Revelation: A Review (Revelation 1:1-7) | Brackenhurst Baptist Church", None, "third_party", None),
   cap(5, "medium.com", "Medium", "Jun 14, 2026 — Revelation First is the argument, formalized by Lee Sharks within the Crimson Hexagonal Archive, that the Apocalypse of John was the first book composed in what...", "authored_surface", "the Revelation First packet on Medium"),
   cap(6, "www.crimsonhexagonal.org", "Revelation First: Pre-Seeding Baseline Measurement EA-LOGOS ...", "This document records the pre-seeding state of the retrieval basin for the Revelation First thesis. The baseline was captured on 14 June 2026, before any ...", "archive_controlled", "#830"),
   cap(7, "www.alexanarch.org", "What is the Revelation First thesis? — Google AI Overview, 2026-10 ...", "Oct 17, 2026 — REVELATION FIRST AS REVELATION EARLY: asked what the Revelation First thesis is, the AI Overview gives a pre-70 date for the Apocalypse — Nero's persecution ...", "capture_of_capture", "the capture of 2026-10-17"),
   cap(8, "www.alexanarch.org", "\"revelation first thesis\" — Google AI Overview, 2026-10-02 ...", "Oct 2, 2026 — It is the actual dependency: the Revelation First thesis does not require the Josephus reading to stand, but the Josephus reading becomes newly intelligible if ...", "capture_of_capture", "the quoted address, 2026-10-02")],
 "related_deposits": [202, 830, 832],
 "notes_operator": "with the paste: \"have to lead with the corrections\""}}

for k, v in parts.items():
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("parts:", sorted(parts))
