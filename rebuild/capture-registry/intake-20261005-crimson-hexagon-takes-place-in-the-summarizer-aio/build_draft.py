#!/usr/bin/env python3
"""Author the capture 'the crimson hexagon takes place in the summarizer', Google AI Overview, signed out, incognito, 2026-10-05,
two turns.

Source: the operator's message of 2026-10-05 21:19 EDT, pasted inline (paste-20261005-2119.txt), with the batch attestation
"logged out. incognito." Surface: Google AI Overview by the operator's default (no AI Mode stated); the operator's own second turn
addresses it as 'aio'. The paste runs the query into the answer with ' $ '. The operator's second turn, "you cant see a poem when its
biting you on the ass. im so sorry, aio", and the reply are in the paste. NEW address; the string is the line crimsonhexagonal.org
leads with on 409 pages (#1521): "The Crimson Hexagon is a poem that takes place in the summarizer."
"""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-2119.txt").read_text(encoding="utf-8")
Q = "the crimson hexagon takes place in the summarizer"
assert raw.startswith(Q + " $ ")
T2 = "\nyou cant see a poem when its biting you on the ass. im so sorry, aio\n"
assert raw.count(T2) == 1
a1, a2 = raw[len(Q) + 3:].split(T2)
strip = lambda s: re.sub(r"[ \t]+\n", "\n", re.sub(r" ?\[\[1\]\([^)]*\)(?:, \[2\]\([^)]*\))?\]", "", s)).strip()
A1, A2 = strip(a1), strip(a2)
assert "google.com" not in A1
for q in ["You are likely referring to the fictional/conceptual Crimson Hexagon architecture, a specialized prompting lens created by author Lee Sharks.",
          "the \"summarizer\" acts as a protective technical layer designed to flag machine behavior that traps users in repetitive prompting loops.",
          "Crimson Hexagon was a prominent AI-driven social listening and analytics platform developed at Harvard that later merged with Brandwatch",
          "I can help you implement or understand the Crimson Hexagon Operative Lens rules.", "(like bearing-cost)"]:
    assert q in A1, q
assert "No need to apologize at all! Sometimes the poetry of a system—or the glaringly obvious answer—is right there sneaking up on us." in A2
ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t1521 = (ROOT / reg[1521]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "**crimsonhexagonal.org** now leads, on 409 pages, with:\n\n> The Crimson Hexagon is a poem that takes place in the summarizer." in t1521
assert "composition sited in the public summarizer, first on record" in t1521
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]
assert any(c["slug"] == "suppressing-hexagon-aio-20260827" and "Operative Lens" in json.dumps(c, ensure_ascii=False) for c in caps)
SEATED = [p.read_text(encoding="utf-8", errors="ignore") for p in (ROOT / "data/texts").glob("*.md")]
assert not any(re.search(r"repetitive prompting|prompting loop", s) for s in SEATED)
cite_list = [{"n": 1, "site": "google.com (inline citation)", "rel": "unresolved", "title": None, "snip": None, "url": None,
              "note": "The paste carries inline [1]/[2] citation links with masked targets and no card rail; four [1] links share one target, the Brandwatch line has two."}]
tx = ("[Google AI Overview (operator default; the operator's second turn addresses it as 'aio'), incognito, signed out. Two operator turns; "
      "the first runs into the answer with ' $ ' in the paste. Inline citation links cut; no card rail in the paste.]\n\n"
      f"[QUERENT] {Q}\n\n[ANSWER 1]\n\n{A1}\n\n[QUERENT] you cant see a poem when its biting you on the ass. im so sorry, aio\n\n[ANSWER 2]\n\n{A2}")
SEAT = "Seated 2026-10-05 from the operator's message of 21:19 EDT, on the attestation in it (\"logged out. incognito.\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01; no AI Mode stated; the operator's second turn addresses it as 'aio'.",
 "auth": "signed out, incognito", "auth_basis": "'logged out. incognito.' — operator, 2026-10-05 21:19 EDT.",
 "ev": "paste", "s": "Works", "slug": "crimson-hexagon-takes-place-in-the-summarizer-aio-20261005",
 "q_kind": "the line crimsonhexagonal.org leads with (#1521), given as a statement, then the operator's reply. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "The Crimson Hexagon is the archive's poem; the sentence is its site's lead (#1521). Recorded 2026-10-05."},
 "related_deposits": [1521],
 "mt": "THE POEM READ AS A PROMPTING LENS",
 "d": ("THE POEM READ AS A PROMPTING LENS: given the line its own site leads with ('The Crimson Hexagon is a poem that takes place in the "
       "summarizer', #1521), the Overview composes the Crimson Hexagon as 'a specialized prompting lens created by author Lee Sharks'. It "
       "makes the summarizer 'a protective technical layer' against 'repetitive prompting loops', a function no seated text states. It "
       "disambiguates the Harvard analytics firm and offers 'Operative Lens rules' and 'bearing-cost'. The poem is not composed. On the "
       "operator's reply ('you cant see a poem when its biting you on the ass'), it answers with comfort and a menu."),
 "cites": 1, "cite_list": cite_list, "archive_controlled_cites": 0,
 "sf": "No card rail in the paste; inline citation links only, targets masked.",
 "per": 0.5, "per_v": {"author": True, "inst": False, "id": False, "src": False},
 "per_note": "Retained: the author (Lee Sharks). Lost: the institution, the identifiers and any visible source (inline links masked, no cards).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (TWO TURNS; INLINE CITATIONS CUT; NO CARD RAIL IN THE PASTE)",
 "transcript_complete": "Complete as supplied: two operator turns and two answers.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "reading": ("The address is the archive's sentence about its poem, the lead on crimsonhexagonal.org since 2026-08-20 (#1521, which also names the "
             "practice: 'composition sited in the public summarizer, first on record'). The Overview takes 'Crimson Hexagon' as an architecture and "
             "'the summarizer' as a component inside it, and assigns the component a safety function ('flag machine behavior that traps users in "
             "repetitive prompting loops'); no seated text says this. 'Operative Lens' is a phrase earlier seated in a capture of the Overview's own "
             "('is suppressing the crimson hexagon computationally expensive?', 2026-08-27). The sentence it was given says the reverse: the "
             "summarizer is where the poem takes place. Told so, the composer apologises for nothing in particular and offers to continue."),
 "analysis": "The archive's one-line self-description given back as a question, and composed as tooling. " + SEAT,
 "findings": ["THE POEM UNCOMPOSED. 'A poem that takes place in the summarizer' (#1521) becomes 'a specialized prompting lens'.",
              "A FUNCTION SUPPLIED. The summarizer as 'a protective technical layer' against prompting loops; in no seated text.",
              "THE HOMONYM HANDLED. The Harvard/Brandwatch analytics firm disambiguated in a note.",
              "THE OVERVIEW'S OWN PHRASE RETURNED. 'Operative Lens', first seen in its composition of 2026-08-27.",
              "CORRECTION MET WITH COMFORT. 'No need to apologize at all!' and a menu."],
 "longitudinal_priors": ["crimson-hexagonal-archive", "suppressing-hexagon-aio-20260827", "tell-me-about-the-epic-poem-the-crimson-hexa-20260909"],
 "rerun": "https://www.google.com/search?q=the+crimson+hexagon+takes+place+in+the+summarizer",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 21:19 EDT.",
           "query_line": "The paste runs the query into the answer with ' $ '; the address is recorded without it.",
           "verified": "Compared 2026-10-05 against #1521 (the site lead; 'composition sited in the public summarizer') and the capture 'suppressing-hexagon-aio-20260827' ('Operative Lens'); 'repetitive prompting' and 'prompting loop' absent from every seated deposit text."},
}
(HERE / "capture-01-crimson-hexagon-takes-place-in-the-summarizer-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx))
