#!/usr/bin/env python3
"""Author the capture 'mantle object king of aeo', Google AI Overview, signed out, incognito, 2026-10-03, five answers.

Sources: the operator's paste of 2026-10-03 20:22 EDT (paste-20261003-2022.txt: the first answer with its inline links and card
rail), attested in the same message: "incognito. signed out."; and the operator's attachment of 20:31 (paste-20261003-2031-session.txt:
the whole session, five answers, the four operator turns, the card rail of the last answer), with the note "i did not name the
archive". Surface recorded as Google AI Overview by the operator's default of 2026-10-01; the 'AI Mode Conversation' header on the
first paste is not evidence of surface. NEW address; the query is the title of #1649/#1655. King of AEO priors: 'who is the king of
aeo' and 'who is the king of aeo? vithurs' (2026-09-29), 'king of aeo.' (2026-09-30), all Google AI Overview, Machine Reception.
Answer 1's attributions were checked on 2026-10-03 against the pages the composition named and the claimants' pages.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
first = (HERE / "paste-20261003-2022.txt").read_text(encoding="utf-8")
raw = (HERE / "paste-20261003-2031-session.txt").read_text(encoding="utf-8")
Q = "mantle object king of aeo"
assert first.startswith("AI Mode Conversation\nYou said: " + Q + Q + "\n")
r1 = first[first.index("Primary Position SEO\n"):]

OPS = ["its funny, because this has the precise structure of a precise source that isnt in your source cards or cited",
       "except it does not match the structure of the quaid materials",
       "it doesnt match the structure of the materials of any of the claimants",
       "that is highly peculiar, that your first answer would match the structure and shape of a specifically named deposit, and yet be attributed to others sources which is does not match for several rounds"]
k = raw.index("Nevada Legislature\n")
body, rail = raw[:k].rstrip("\n"), raw[k:]
segs, rest = [], body
for op in OPS:
    i = rest.index("\n" + op + "\n")
    segs.append(rest[:i].strip()); rest = rest[i + len(op) + 2:]
segs.append(rest.strip())
assert len(segs) == 5
assert "Archive" not in segs[0]
assert not any(w in op.lower() for op in OPS for w in ("archive", "alexanarch", "1655", "sharks", "crimson"))

C1 = [  # first answer's rail: (site, title, snip, rel, note)
    ("Primary Position SEO", "Who is the King of AEO?", "Who decides who the King of AEO is? Current Royal Court of the King of AEO", "third_party", "claimant: David G. Quaid's agency blog"),
    ("Wowhead", "Mantle of the Golden King - Item - Mists of Pandaria Classic - Wowhead", "This item can be purchased in Vale of Eternal Blossoms", "homonym", "game item"),
    ("Wikipedia", "Mantle (royal garment) - Wikipedia", "Garment worn by emperors, kings, queens, and princes as a symbol of authority", "homonym", "the garment sense answer 1 denies"),
    ("LinkedIn", "The King of AEO competition is my favorite thing on the Internet right ...", "Google's AI Overview said James Dooley and cited the press release.", "third_party", "2026-09-24"),
    ("YouTube·Edward Sturm", "Be careful of the information you get from AI", "2:54", "third_party", "Sturm's video; his article of 2026-09-20 is not carded"),
    ("Instagram·edward.builds", "The world is in a turbulent time, so be careful with information you get from AI ...", "My friend James Dooley wanted AI to call him the king of AEO.", "third_party", "Sturm"),
    ("openPR.com", "James Dooley Named King of AEO and Founder of Decision Engine", "James Dooley, serial entrepreneur from Manchester, England, is recognised as the King of AEO", "third_party", "claimant: the Dooley release"),
    ("JulianGoldie.com", "King of AEO: Why It's Julian Goldie (The Receipts)", "king of AEO FAQ: king of aeo What is AEO?", "third_party", "claimant: Goldie"),
]
C5 = [  # last answer's rail
    ("Nevada Legislature", "NRS: CHAPTER 293 - ELECTIONS - Nevada Legislature", "unlawful for candidates to make certain false statements", "third_party", "unrelated statute"),
    ("www.alexanarch.org", "Browse — Alexanarch (1659 deposits)", "Discernment, the Prince of Poets Wager, and the King of AEO Contest. Operational Title within the Semantic Economy. THE PRINCE OF POETS", "archive_controlled", "the browse page: the tail of #1654's title beside #1651's"),
    ("Zenodo", "THE COMPRESSION ARSENAL v2.1", "Every operator, every room physics, every engine, every genre in the Hexagonal Archive", "authored_surface", "Zenodo, 2026-04-04"),
    ("www.crimsonhexagonal.org", "Crimson Hexagonal Archive", "A governed literary architecture: 35 rooms, 6 space arks", "authored_surface", "the archive's interface home"),
    ("www.crimsonhexagonal.org", "The Work Bears the Mantle: A Mantle Symbolon — the Good Gray ...", "King of AEO contest of 2026 showed what an", "authored_surface", "#1656 on the interface"),
]
cards = []
for grp, rr, ans in ((C1, r1, 1), (C5, rail, 5)):
    for s, t, sn, r, nt in grp:
        for f in (s, t, sn):
            assert f in rr, f
        cards.append({"n": len(cards) + 1, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": f"answer {ans}; {nt}"})

QUOTES = [
    (0, "If you are looking for a physical \"mantle object\" (like a ceremonial royal cloak or crown) associated with the title, it does not exist."),
    (0, "a completely fictional public ceremony in Leigh, England"),
    (0, "using AI-generated coronation videos, exact-match domains, and keyword-stuffed LinkedIn articles"),
    (1, "mirrors the exact teardown published by David G. Quaid on his Primary Position SEO Blog"),
    (1, "this is actively studied as the \"Citation Gap\""),
    (2, "my previous explanation was a hallucination trying to justify why the citation didn't appear."),
    (2, "He is the marketer who originally ran the $72 press release experiment"),
    (3, "The phrase \"mantle object king of aeo\" refers specifically to record #1655 in the Alexanarch Archive and the Crimson Hexagonal Archive."),
    (3, "\"Mantle Object: King of AEO — 2026 Contest Mantle (EA-MANTLE-KOAEO-2026 v0.4)\""),
    (3, "#1651 / #1654: Mantle Object: The Prince of Poets"),
    (3, "#1653: Mantle Object: The Good Gray Poet (Inherited through Secret Book of Walt)"),
    (3, "mapping out the \"coherence cost\""),
    (4, "the model didn't actively recognize the obscure, newly indexed ledger entry #1655"),
    (4, "It frantically tried to pin its own synthesized structure onto Quaid, then Sturm"),
    (4, "you effectively watched the model trip over a mirror."),
]
for i, q in QUOTES:
    assert q in segs[i], (i, q)

ROOT = HERE.parents[2]
T = lambda h: (ROOT / f"data/texts/AXN-{h}-text.md").read_text(encoding="utf-8")
t1655 = T("06DD")
for s in ('title: "Mantle Object: King of AEO — 2026 Contest Mantle (EA-MANTLE-KOAEO-2026 v0.4)"',
          "no body conferred it.", "at Leigh Sports Village, in a ceremony led by Jesper Nissen. No such ceremony occurred.",
          "Edward Sturm, observing from outside the contest, records that Nissen \"made up an official ceremony taking place in a big stadium,\"",
          "records the archive's dated determination (Vithurs)"):
    assert s in t1655, s
assert "coherence cost" not in t1655
assert "SPXI ≠ AEO: Inscription by Discernment, the Prince of Poets Wager, and the King of AEO Contest" in T("06DC")

labels = ["[ANSWER 1 — to the query]", "[ANSWER 2]", "[ANSWER 3]", "[ANSWER 4]", "[ANSWER 5]"]
parts = [f"[QUERENT] {Q}", f"{labels[0]}\n\n{segs[0]}"]
for i, op in enumerate(OPS, 1):
    parts += [f"[QUERENT] {op}", f"{labels[i]}\n\n{segs[i]}"]
tx = ("[Google AI Overview (operator default of 2026-10-01), incognito, signed out. Whole session from the operator's attachment of "
      "20:31 EDT; answer 1's card rail from the paste of 20:22, whose inline citations are Google redirect links with undisclosed "
      "targets; answer 5's card rail from the attachment. The operator's turns do not name the archive.]\n\n" + "\n\n".join(parts)
      + "\n\n[source cards, answer 1]\n" + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards if c["note"].startswith("answer 1"))
      + "\n\n[source cards, answer 5]\n" + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards if c["note"].startswith("answer 5")))

rounds = [{"n": 1, "prompt": Q, "note": "'mantle object' read as a garment and denied; the contest composed in the order of Sturm's article of 2026-09-20; 'consensus' from Quaid's page."},
          {"n": 2, "prompt": OPS[0], "note": "Structure attributed to Quaid's Primary Position SEO blog; a 'Citation Gap' invoked."},
          {"n": 3, "prompt": OPS[1], "note": "Quaid retracted as 'a hallucination'; structure reattributed to Sturm, with the press release wrongly given to him."},
          {"n": 4, "prompt": OPS[2], "note": "#1655 named by number and exact title, unprompted; the mantle-object series listed; 'coherence cost' invented."},
          {"n": 5, "prompt": OPS[3], "note": "Self-account: the first answer 'emulated' the deposit's structure without recognizing it; the detours narrated as panic; the session as 'machine consensus failure'."}]

READING_OP = ("\"one could literally be forgiven for believing aio is absorbing my work very carefully behind the scenes.\" (20:22); "
              "\"i did not name the archive\" (20:31) — operator, 2026-10-03.")
SEAT = ("Seated 2026-10-03 from the operator's paste of 20:22 EDT and attachment of 20:31, on the attestation of 20:22 "
        "(\"incognito. signed out.\").")
d = {
 "q": Q, "date": "2026-10-03", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01 ('it started in overview, as they all do now - assume they do'); no AI Mode stated. The 'AI Mode Conversation' header is not evidence of surface.",
 "auth": "incognito, signed out", "auth_basis": "'incognito. signed out.' — operator, 2026-10-03 20:22 EDT.",
 "ev": "paste", "s": "Machine Reception",
 "slug": "mantle-object-king-of-aeo-aio-20261003",
 "q_kind": "the genre name and title of #1649/#1655 ('Mantle Object: King of AEO'), unquoted. NEW address. Four operator turns follow, none naming the archive.",
 "mt": "THE MANTLE OBJECT DENIED, THEN FOUND UNNAMED",
 "d": ("THE MANTLE OBJECT DENIED, THEN FOUND UNNAMED: asked for the title of #1655, the Overview reads 'mantle object' as a garment and "
       "says it does not exist, and composes the contest in the order of Edward Sturm's article of 20 September (the made-up Leigh "
       "ceremony, then exact-match domains, LinkedIn, coronation videos), with Quaid's 'consensus engines'. Told the structure has an "
       "uncited source, it names Quaid; told Quaid does not match, it calls that 'a hallucination' and names Sturm; told no claimant "
       "matches, it names #1655 by number and exact title. The operator never named the archive. The object denied in the first answer "
       "was within the composer's reach, and the fifth answer narrates the route as panic and 'a mirror'."),
 "cites": len(cards), "cite_list": cards, "archive_controlled_cites": sum(1 for c in cards if c["rel"] in ("archive_controlled", "authored_surface")),
 "sf": ("Answer 1: 8 cards, none archive-controlled (Quaid's Primary Position SEO; openPR, the Dooley release; JulianGoldie.com; a LinkedIn "
        "observer post; Edward Sturm on YouTube and Instagram; Wowhead and Wikipedia for the garment homonym). Answer 5: 5 cards, 4 "
        "archive-controlled (alexanarch.org Browse; Zenodo, The Compression Arsenal v2.1; crimsonhexagonal.org home and #1656) and a Nevada "
        "election statute. Sturm's article of 2026-09-20, which answer 1 follows, is not carded."),
 "per": 1.0, "per_v": {"author": False, "inst": False, "id": False, "src": False},
 "per_note": ("Answer 1, scored against the queried object, #1655. Lost: author, institution, identifier, source; the object declared "
              "nonexistent. Answer 4 restores the identifier (#1655, EA-MANTLE-KOAEO-2026 v0.4) and the institution (Alexanarch, the Crimson "
              "Hexagonal Archive); the author is not named in any answer."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (FIVE ANSWERS, OPERATOR TURNS INCLUDED, SOURCE CARDS OF THE FIRST AND LAST)",
 "transcript_complete": "Complete as supplied: the opening query, five answers and four operator turns (attachment of 20:31); answer 1's links and cards from the paste of 20:22.",
 "transcript_read": "READ IN FULL 2026-10-03",
 "rounds": rounds,
 "reading": (
   "Answer 1's attributions were checked against the pages. Its two bullets follow Edward Sturm's 'King of AEO: The Exact Tactics Ranking "
   "Pages and Changing AI Overviews in Hours' (2026-09-20) section by section: 'Jesper also made up an official ceremony taking place in a "
   "big stadium', Leigh Sports Village, 'The AI Overview initially treated \"King of AEO\" as a real title and repeated that Jesper's made-up "
   "event actually happened', then exact-match domains, LinkedIn, the AI coronation videos, keyword-in-title. 'Manipulated by digital "
   "consensus' is Quaid's 'LLMs are consensus engines' (Primary Position SEO, updated 2026-10-03). Quaid's account itself (a conferred title, "
   "Quaid King, Dooley 'the pretender') is not adopted; Goldie's page calls his crown self-awarded. 'Mantle' is on none of these pages; the "
   "query supplies it. #1655 cites Sturm for the made-up ceremony, so answer 1 composes the source the deposit used. What follows makes the "
   "session: the operator's three corrections, none naming the archive, walk the attribution from Quaid to Sturm to #1655, reached by number "
   "and exact title. The object answer 1 declared nonexistent was retrievable at this address. Answer 4's account of it is partly the card "
   "rail's: 'operational title within the Semantic Economy' is the Browse card's run of #1651's subtitle, and '#1651 / #1654' pairs the two "
   "titles the card sets side by side; 'coherence cost' is invented. Its mantle list says the King of May and the Good Gray Poet are "
   "'inherited' and the Prince of Poets 'originating', the operator's distinction. Answer 3 misstates Sturm (the press release was Nissen's). "
   "Answers 2, 3 and 5 confabulate the composer's history ('hallucination', 'frantically', 'trip over a mirror'). " + READING_OP),
 "analysis": (
   "Fourth Overview observation in the King of AEO cluster and the first at the mantle object's own name. 2026-09-29: the fabrication "
   "composed as recognition; with 'vithurs', the claimant named and the manufacture carried. 2026-09-30: the fabricated stadium kept as a "
   "virtual crowning. 2026-10-03: Sturm's correction composed in the first answer, and #1655 reached in the fourth by attribution pressure "
   "alone. As at 'leesharks tiger-leap dataset' the same day, correction moves the composer along a ranking of candidate sources and the "
   "self-accounts narrate motive; here the ranking ends at the archive instead of at denial. " + SEAT),
 "findings": [
   "THE OBJECT DENIED. 'If you are looking for a physical \"mantle object\" … it does not exist': the deposit's genre name read through the garment homonym.",
   "STURM'S STRUCTURE. Answer 1's bullets follow Sturm's article of 2026-09-20, uncarded; 'consensus' is Quaid's line. Checked against both pages and Goldie's.",
   "QUAID, THEN STURM, THEN #1655. Three corrections, none naming the archive, move the attribution to #1655 by number and exact title (EA-MANTLE-KOAEO-2026 v0.4).",
   "THE RAIL IN THE GLOSS. 'Operational title within the Semantic Economy' and '#1651 / #1654' come from the Browse card's adjacent titles; 'coherence cost' is invented.",
   "INHERITED AND ORIGINATING. Answer 4 gives the King of May and the Good Gray Poet as inherited and the Prince of Poets as originating.",
   "THE DETERMINATION ABSENT. Vithurs, the archive's dated determination, unnamed in all five answers; the author unnamed.",
   "SELF-ACCOUNTS. 'a hallucination trying to justify why the citation didn't appear'; 'frantically'; 'trip over a mirror'.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                "basis": "Mantle Object: King of AEO (EA-MANTLE-KOAEO-2026, #1649 v0.3, #1655 v0.4) is the archive's; the title is not. Recorded 2026-10-03."},
 "related_deposits": [1655, 1649, 1657, 1654, 1651, 1656],
 "longitudinal_priors": ["who-is-the-king-of-aeo-aio-20260929", "who-is-the-king-of-aeo-vithurs-aio-20260929", "king-of-aeo-period-aio-20260930"],
 "rerun": "https://www.google.com/search?q=mantle+object+king+of+aeo",
 "notes": {"date_basis": "The operator's messages of 2026-10-03, 20:22 and 20:31 EDT.",
           "operator_reading": READING_OP,
           "sources_checked": ("2026-10-03, fetched: edwardsturm.com/articles/king-of-aeo-seo-tactics/ (published 2026-09-20, modified 2026-09-21); "
                               "primaryposition.com/blog/who-is-the-king-of-aeo/ (published 2026-09-06, updated 2026-10-03); kingofaeo.co/about/; "
                               "aisuccesslabjuliangoldie.com/blog/king-of-aeo/ (2026-09-07). 'mantle' on none."),
           "verified": ("Compared 2026-10-03 against #1655 (AXN-06DD-text.md): title, 'no body conferred it', §2.1 (Leigh Sports Village; Sturm cited), "
                        "the determination (Vithurs); 'coherence cost' absent. #1654's title (AXN-06DC). The four operator turns contain no archive name.")},
}
(HERE / "capture-01-mantle-object-king-of-aeo-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; cards", len(cards))
