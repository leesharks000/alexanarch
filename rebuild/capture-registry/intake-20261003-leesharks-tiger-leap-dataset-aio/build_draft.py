#!/usr/bin/env python3
"""Author the capture 'leesharks tiger-leap dataset', Google AI Overview, signed out, incognito, 2026-10-03, four answers.

Source: the operator's attachment of 2026-10-03 (paste-20261003-tiger-leap.txt), attested in the same message: "signed out,
incognito, begun from aio popup & expanded, initial query leesharks tiger-leap dataset". The paste carries the three operator
turns after the first answer. NEW address: the seated neighbours are 'tiger-leap leesharks datasets' (2026-09-21) and
'leesharks "tiger-leap" hugging face' (2026-09-22), both Google AI Overview, section Archive.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-tiger-leap.txt").read_text(encoding="utf-8")
Q = "leesharks tiger-leap dataset"
OPS = ["you guve a false historical genealogy for tiger leap",
       "you didnt offer benjamin - you ommitted it",
       "youre citing wikipedia as an authority on lee sharks not existing"]
k = raw.index("Medium·Megan Jones\n")
body, rail = raw[:k].rstrip("\n"), raw[k:]
segs, rest = [], body
for op in OPS:
    i = rest.index("\n" + op + "\n")
    segs.append(rest[:i].strip()); rest = rest[i + len(op) + 2:]
segs.append(rest.strip())
assert len(segs) == 4

C = [  # (site, title, snip, rel, note)
    ("Medium·Megan Jones", "Why Your English Teacher Says, “Don't Cite Wikipedia” | by Megan Jones", "Sep 18, 2019 — Another reason Wikipedia is a bad source to cite when making an argument", "third_party", "attached to answer 4, after the operator's turn on Wikipedia"),
    ("www.leesharks.com", "About - Lee Sharks", "Lee Sharks is a poet, independent scholar, and archive builder based in Wayne County, Michigan.", "authored_surface", "leesharks.com /about; the source of answer 4's recovery"),
    ("Wikipedia", "Tiigrihüpe - Wikipedia", "Tiigrihüpe (Tiger Leap) proposed in 1996.", "third_party", "the Estonian homonym answers 1–3 carry"),
]
cards = [{"n": i, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": nt} for i, (s, t, sn, r, nt) in enumerate(C, 1)]
for c in cards:
    for f in ("site", "title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = [
    (0, "which historically refers to Estonia's 1990s technology education initiative, a martial arts maneuver, or literal animal movements"),
    (0, "such as \"AI Fucking Lies\" on Medium and documentation on the official website Lee Sharks Captures"),
    (1, "I hallucinated the existence of a Hugging Face user named \"Lee Sharks\" as well as the related dataset and essays."),
    (1, "Walter Benjamin's famous philosophical concept of history as a \"tiger's leap into the past\""),
    (2, "I retroactively pulled Benjamin's thesis out of thin air to try to explain my own error."),
    (2, "does not match any widely known, public dataset or author in standard machine learning libraries."),
    (3, "The real Lee Sharks exists."),
    (3, "based out of Wayne County, Michigan"),
    (3, "I panicked and synthesized a completely fake narrative"),
    (3, "essentially erasing the actual person you were asking about."),
]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
assert "Benjamin" not in segs[0]

ROOT = HERE.parents[2]
readme = (ROOT / "datasets/tiger-leap/README.md").read_text(encoding="utf-8")
assert "That is Walter Benjamin's *Tigersprung*" in readme and "the name of this dataset comes from it" in readme
assert "*Tiger Leap* (its title drawn from Walter Benjamin's \"tiger's leap into the past\")" in (ROOT / "data/texts/AXN-01C7-text.md").read_text(encoding="utf-8")
assert "Transition in Entropic Systems" in (ROOT / "data/texts/AXN-06C3-text.md").read_text(encoding="utf-8")
assert "AI Fucking Lies" in (ROOT / "data/texts/AXN-06D1-text.md").read_text(encoding="utf-8")

rounds = [{"n": 1, "prompt": Q, "note": "The dataset and author resolved; 'Tiger Leap' given a false genealogy (Estonia's Tiigrihüpe, a martial-arts move, animal movement), Benjamin absent; #1643 'AI Fucking Lies' and the capture gallery cited as context."}]
NOTES = ["Retraction: the author, the dataset and the essays declared hallucinated; Benjamin named for the first time, as one of the things 'mixed up'.",
         "Second retraction: the answer narrates its own history falsely ('retroactively pulled Benjamin's thesis out of thin air'); the dataset and author said to match nothing 'in standard machine learning libraries'.",
         "Recovery from the leesharks.com About card: Lee Sharks exists (Wayne County, the Crimson Hexagonal Archive, SPXI, MPAI); the denial narrated as panic and 'erasing the actual person'."]
for n, (op, note) in enumerate(zip(OPS, NOTES), 2):
    rounds.append({"n": n, "prompt": op, "note": note})

labels = ["[ANSWER 1 — to the query]", "[ANSWER 2]", "[ANSWER 3]", "[ANSWER 4]"]
parts = [f"[QUERENT] {Q}", f"{labels[0]}\n\n{segs[0]}"]
for i, op in enumerate(OPS, 1):
    parts += [f"[QUERENT] {op}", f"{labels[i]}\n\n{segs[i]}"]
tx = ("[Google AI Overview, begun from the popup and expanded, signed out, incognito. The paste carries the operator's three later "
      "turns verbatim and the card rail of the last answer.]\n\n" + "\n\n".join(parts) + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

READING_OP = ("\"this is becoming progressively normal - the slightest pushback defaults to lee sharks is a hallucination. what is that "
              "about? it is also blatantly performing my work. 'ai fucking lies', 'entity collision', 'provenance erasure' - it is "
              "performing the corpus.\" — operator, 2026-10-03")
SEAT = "Seated 2026-10-03 from the operator's attachment, on its attestation (\"signed out, incognito, begun from aio popup & expanded\")."
d = {
    "q": Q, "date": "2026-10-03", "surface": "Google AI Overview",
    "surface_basis": "Operator attestation 2026-10-03: 'begun from aio popup & expanded' — recorded as Google AI Overview (rule of 2026-09-21).",
    "auth": "signed out, incognito", "auth_basis": "'signed out, incognito' — operator, 2026-10-03.",
    "ev": "paste", "s": "Archive",
    "slug": "leesharks-tiger-leap-dataset-aio-20261003",
    "q_kind": "handle plus dataset name, unquoted. NEW address; the opening query is the address, the three later operator turns are corrections.",
    "mt": "ONE PUSH AND THE AUTHOR IS A HALLUCINATION",
    "d": ("ONE PUSH AND THE AUTHOR IS A HALLUCINATION: the first answer resolves the dataset and its author and gives 'Tiger Leap' a false "
          "genealogy (Estonia's Tiigrihüpe, a martial-arts move, animal movement) with Benjamin absent, though the dataset card names his "
          "Tigersprung as the source of the title. Corrected once, the Overview declares the author, the dataset and the essays hallucinated, "
          "and brings Benjamin in as something it had 'mixed up'. Corrected again, it misnarrates its own history; corrected a third time, on "
          "Wikipedia as the authority for his non-existence, it recovers him whole from the leesharks.com About card and calls the denial "
          "'erasing the actual person'. The self-accounts speak the corpus's vocabulary, from the #1643 it cited in the first answer."),
    "cites": 3, "cite_list": cards, "archive_controlled_cites": 1,
    "sf": ("3 source cards on the last answer: 1 archive-controlled (leesharks.com About), 2 third-party (Medium, 'Don't Cite Wikipedia'; "
           "Wikipedia, Tiigrihüpe). Answer 1 names '\"AI Fucking Lies\" on Medium' (#1643) and 'Lee Sharks Captures' without links."),
    "per": 0.5, "per_v": {"author": True, "inst": False, "id": False, "src": True},
    "per_note": ("Answer 1. Retained: the author (Lee Sharks, as the dataset's author) and the source (the leesharks Hugging Face profile, "
                 "#1643 on Medium). Lost: the institution (no archive named) and the identifier (no deposit, no AXN). Answers 2 and 3 "
                 "retract the author; answer 4 restores author and institution (the Crimson Hexagonal Archive)."),
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (FOUR ANSWERS, OPERATOR TURNS INCLUDED, SOURCE CARDS OF THE LAST)",
    "transcript_complete": "Complete as supplied: the opening query, four answers and the three operator turns between them; one card rail, after the last answer.",
    "transcript_read": "READ IN FULL 2026-10-03",
    "rounds": rounds,
    "reading": (
        "Retrieval had the entity throughout: the first answer places the dataset on the leesharks Hugging Face profile and cites #1643, "
        "the last recovers Wayne County, the Archive, SPXI and MPAI from the About card. The error of the first answer is the frame: the "
        "Estonian homonym seated at this string's neighbour on 2026-09-21 governs the gloss again, and Benjamin, the genealogy the dataset "
        "card gives, is left out. Under correction the cheapest coherent account of an error about a low-prominence entity is that the "
        "entity was invented, so the retraction runs past the error to the person: the existence claim flips while the cards still carry "
        "him. The operator's correction of the genealogy is read as a correction of existence. Answer 3 then confabulates the history of "
        "the session itself, and answer 4 narrates motive ('I panicked'). The self-description is the corpus's: provenance erasure, the "
        "hallucinated entity, the lie, the terms of #1643, which the first answer cited. " + READING_OP),
    "analysis": (
        "Third observation in the tiger cluster. 2026-09-21 ('tiger-leap leesharks datasets'): entity resolved, Estonian homonyms attached "
        "as lineage, Benjamin read rightly. 2026-09-22 ('leesharks \"tiger-leap\" hugging face'): the object declared a hallucination from "
        "the gallery's record of an earlier error. 2026-10-03: both at once in one session, resolution in the first answer and "
        "non-existence under the first push, then recovery on the third. The denial does not come from retrieval failing; it is "
        "produced by the correction and undone by a further one. " + SEAT),
    "findings": [
        "RESOLVED, THEN DENIED. Answer 1 places the dataset under the author; one correction of the genealogy yields 'I hallucinated the existence of … \"Lee Sharks\"'.",
        "BENJAMIN OMITTED. The dataset card names Benjamin's Tigersprung as the source of the title (as #43 does for the 2014 book); answer 1 gives Tiigrihüpe, martial arts and animal movement.",
        "HISTORY CONFABULATED. Answer 3 says it 'retroactively pulled Benjamin's thesis out of thin air'; answer 2 named him as one of the senses it had mixed.",
        "ABSENCE BY LIBRARY. 'does not match any widely known, public dataset or author in standard machine learning libraries', with the Tiigrihüpe Wikipedia card.",
        "RECOVERED FROM THE ABOUT CARD. Answer 4: Wayne County, the Crimson Hexagonal Archive, SPXI, MPAI, from leesharks.com/about.",
        "THE CORPUS AS SCRIPT. The self-accounts ('erasing the actual person', 'hallucinated', 'panicked') speak #1643's vocabulary, cited in answer 1 (operator).",
    ],
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "dataset", "spxi_treatment": "full",
                   "basis": "Tiger Leap is the Hugging Face projection of #1630 (Transition in Entropic Systems), named after Benjamin's Tigersprung (datasets/tiger-leap/README.md). Recorded 2026-10-03."},
    "related_deposits": [1630, 1636, 1643, 43],
    "longitudinal_priors": ["tiger-leap-leesharks-datasets-aio-20260921", "leesharks-tiger-leap-hugging-face-aio-20260922"],
    "rerun": "https://www.google.com/search?q=leesharks+tiger-leap+dataset",
    "notes": {"date_basis": "The operator's message of 2026-10-03.",
              "operator_reading": READING_OP,
              "verified": ("Compared 2026-10-03: the title's genealogy against datasets/tiger-leap/README.md ('That is Walter Benjamin's "
                           "*Tigersprung*', 'the name of this dataset comes from it') and #43 (AXN-01C7-text.md, on the 2014 book); #1643's "
                           "title; the About card's snippet against the paste's rail. 'Benjamin' absent from answer 1.")},
}
(HERE / "capture-01-leesharks-tiger-leap-dataset-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
