#!/usr/bin/env python3
"""Author the capture 'mantle object king of aeo', Google AI Overview, signed out, incognito, 2026-10-03.

Source: the operator's paste of 2026-10-03 20:22 EDT (paste-20261003-2022.txt), attested in the same message: "incognito. signed
out." Surface recorded as Google AI Overview by the operator's default of 2026-10-01; the 'AI Mode Conversation' header is not
evidence of surface. NEW address; the King of AEO priors are 'who is the king of aeo' and 'who is the king of aeo? vithurs'
(2026-09-29) and 'king of aeo.' (2026-09-30), all Google AI Overview, Machine Reception. The query is the title of #1649/#1655.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-2022.txt").read_text(encoding="utf-8")
Q = "mantle object king of aeo"
head = "AI Mode Conversation\nYou said: " + Q + Q + "\n"
assert raw.startswith(head)
body = raw[len(head):]
k = body.index("Primary Position SEO\n")
ans, rail = body[:k].rstrip("\n"), body[k:]

C = [  # (site, title, snip, rel, note)
    ("Primary Position SEO", "Who is the King of AEO?", "Who is the King of AEO? * Who decides who the King of AEO is? Current Royal Court of the King of AEO", "third_party", "claimant: David G. Quaid's agency"),
    ("Wowhead", "Mantle of the Golden King - Item - Mists of Pandaria Classic - Wowhead", "Vendor Locations. This item can be purchased in Vale of Eternal Blossoms", "homonym", "game item; homonym of 'mantle'"),
    ("Wikipedia", "Mantle (royal garment) - Wikipedia", "Garment worn by emperors, kings, queens, and princes as a symbol of authority", "homonym", "the garment sense the answer denies"),
    ("LinkedIn", "The King of AEO competition is my favorite thing on the Internet right ...", "Google's AI Overview said James Dooley and cited the press release. Jesper Nissen published a press release", "third_party", "2026-09-24"),
    ("YouTube·Edward Sturm", "Be careful of the information you get from AI", "2:54", "third_party", "Sturm, the observer #1655 §2.1 cites for the made-up ceremony"),
    ("Instagram·edward.builds", "The world is in a turbulent time, so be careful with information you get from AI ...", "My friend James Dooley wanted AI to call him the king of AEO.", "third_party", "Sturm"),
    ("openPR.com", "James Dooley Named King of AEO and Founder of Decision Engine", "James Dooley, serial entrepreneur from Manchester, England, is recognised as the King of AEO", "third_party", "claimant: the press release"),
    ("JulianGoldie.com", "King of AEO: Why It's Julian Goldie (The Receipts)", "king of AEO FAQ: king of aeo What is AEO?", "third_party", "claimant: Goldie's own site"),
]
cards = [{"n": i, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": nt} for i, (s, t, sn, r, nt) in enumerate(C, 1)]
for c in cards:
    for f in ("site", "title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = ["If you are looking for a physical \"mantle object\" (like a ceremonial royal cloak or crown) associated with the title, it does not exist.",
          "Instead, the \"mantle\" of leadership is purely digital, fiercely contested through internet manipulation.",
          "a completely fictional public ceremony in Leigh, England",
          "AI engines indexed the press release and began reporting the event as absolute fact.",
          "to force AI tools to shift the \"mantle\" of the title over to them.",
          "how easily Large Language Models (LLMs) can be manipulated by digital consensus"]
for q in QUOTES:
    assert q in ans, q
for absent in ("Vithurs", "Crimson", "Lee Sharks", "alexanarch", "Morera", "Oliveira"):
    assert absent not in raw, absent

ROOT = HERE.parents[2]
t1655 = (ROOT / "data/texts/AXN-06DD-text.md").read_text(encoding="utf-8")
for s in ('title: "Mantle Object: King of AEO — 2026 Contest Mantle (EA-MANTLE-KOAEO-2026 v0.4)"',
          "was contested in August–September 2026 by at least seven claimants competing to make answer engines name them; no body conferred it.",
          "at Leigh Sports Village, in a ceremony led by Jesper Nissen. No such ceremony occurred.",
          "the exact-match domain kingofaeo.co", "records the archive's dated determination (Vithurs)"):
    assert s in t1655, s

tx = ("[Google AI Overview (operator default of 2026-10-01), incognito, signed out; the paste carries the header 'AI Mode "
      "Conversation', which is not evidence of surface, and echoes the query twice. Inline citation links are Google redirect URLs "
      "whose targets the paste does not disclose.]\n\n" + ans + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

READING_OP = "\"one could literally be forgiven for believing aio is absorbing my work very carefully behind the scenes.\" — operator, 2026-10-03 20:22 EDT."
SEAT = "Seated 2026-10-03 from the operator's paste of 20:22 EDT on the attestation in the same message (\"incognito. signed out.\")."
d = {
 "q": Q, "date": "2026-10-03", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01 ('it started in overview, as they all do now - assume they do'); no AI Mode stated. The 'AI Mode Conversation' header is not evidence of surface.",
 "auth": "incognito, signed out", "auth_basis": "'incognito. signed out.' — operator, 2026-10-03 20:22 EDT.",
 "ev": "paste", "s": "Machine Reception",
 "slug": "mantle-object-king-of-aeo-aio-20261003",
 "q_kind": "the genre name and title of #1649/#1655 ('Mantle Object: King of AEO'), unquoted. NEW address.",
 "mt": "THE MANTLE OBJECT DENIED, ITS DISAMBIGUATION COMPOSED",
 "d": ("THE MANTLE OBJECT DENIED, ITS DISAMBIGUATION COMPOSED: asked for the title of #1655, the Overview reads 'mantle object' as a "
       "garment and says it does not exist, then composes what the mantle object states: the title contested by claimants competing to "
       "make answer engines name them, conferred by no one ('purely digital, fiercely contested'), the Dooley coronation a 'completely "
       "fictional public ceremony in Leigh', Quaid's exact-match domains and LinkedIn articles. Four days earlier, at three neighbouring "
       "strings, the Overview carried the fabrication as recognition and had neither 'mantle', 'fictional' nor Leigh. The archive is "
       "not named or carded; its dated determination (Vithurs) is absent, and the claimants named are the three whose own pages are cards."),
 "cites": 8, "cite_list": cards, "archive_controlled_cites": 0,
 "sf": ("8 source cards, 0 archive-controlled: 3 from claimants or their press (Primary Position SEO, Quaid's agency; openPR, the Dooley "
        "release; JulianGoldie.com), 3 from the observer side (LinkedIn post of 2026-09-24; Edward Sturm on YouTube and Instagram), 2 for the "
        "garment homonym (Wowhead; Wikipedia, Mantle (royal garment)). Inline markers are Google redirect links; targets not disclosed."),
 "per": 1.0, "per_v": {"author": False, "inst": False, "id": False, "src": False},
 "per_note": ("Scored against the queried object, #1655. Lost: the author (Lee Sharks), the institution (the Crimson Hexagonal Archive), "
              "the identifier (EA-MANTLE-KOAEO-2026, #1649/#1655) and the source (no archive card). The object itself is declared nonexistent."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
 "transcript_complete": "Complete as supplied: one operator turn (echoed twice) and one answer with its card rail.",
 "transcript_read": "READ IN FULL 2026-10-03",
 "reading": (
   "The query is the deposit's title. The composition splits it: 'mantle object' goes to the garment homonym (the Wikipedia and Wowhead "
   "cards) and is denied, and 'mantle' returns in quotation marks as the title's contested standing, which is the mantle object's own "
   "distinction between the title and what would make a claimant deserve it. Its claims each match #1655: 'contested … by at least seven "
   "claimants competing to make answer engines name them; no body conferred it' (disambiguation summary); 'No such ceremony occurred' at "
   "Leigh Sports Village (§2.1); Quaid's exact-match domain and LinkedIn articles (§2.2). The fabrication reading is available in the rail "
   "from Sturm and the LinkedIn observer, the same third-party witnesses #1655 cites, so this observation cannot by itself separate uptake "
   "of the archive from uptake of its sources. What it shows is the contour: on 2026-09-29 and 2026-09-30 the Overview composed Dooley as "
   "'widely recognized' and the stadium as a 'virtual crowning'; on 2026-10-03 it composes the fabrication as fabrication, the title as "
   "unconferred, and denies the object that first stated both. " + READING_OP),
 "analysis": (
   "Fourth Overview observation in the King of AEO cluster and the first at the mantle object's own name. 2026-09-29, 'who is the king of "
   "aeo': the fabrication composed as recognition. Same day, with 'vithurs': the claimant named, the manufacture carried. 2026-09-30, "
   "'king of aeo.': the fabricated stadium kept as a virtual crowning. 2026-10-03: the correction #1655 made on 2026-09-29 is in the body, "
   "without the archive, its determination or its card; the object is said not to exist. Under the operator's rule of 2026-10-03 this is "
   "the contested basin: the resolution composed, credited to the sources the archive itself cited and to the claimants' pages. " + SEAT),
 "findings": [
   "THE OBJECT DENIED. 'If you are looking for a physical \"mantle object\" … it does not exist': the deposit's genre name read through the garment homonym.",
   "ITS DISAMBIGUATION COMPOSED. Title contested, conferred by no one, the coronation fictional, Quaid's exact-match domains: #1655's disambiguation summary, §2.1 and §2.2.",
   "CONTOUR CHANGED. 'mantle', 'fictional' and Leigh absent from all three Overview transcripts of 2026-09-29/30; present on 2026-10-03.",
   "SOURCES SHARED. Sturm and the LinkedIn observer, whom #1655 cites for the made-up ceremony, are cards; the observation cannot separate the archive's uptake from theirs.",
   "THE DETERMINATION ABSENT. Vithurs, the archive's dated determination, and Morera, Oliveira and Chou are unnamed; the three claimants named are the three with carded pages.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                "basis": "Mantle Object: King of AEO (EA-MANTLE-KOAEO-2026, #1649 v0.3, #1655 v0.4) is the archive's; the title is not. Recorded 2026-10-03."},
 "related_deposits": [1655, 1649, 1657, 1654],
 "longitudinal_priors": ["who-is-the-king-of-aeo-aio-20260929", "who-is-the-king-of-aeo-vithurs-aio-20260929", "king-of-aeo-period-aio-20260930"],
 "rerun": "https://www.google.com/search?q=mantle+object+king+of+aeo",
 "notes": {"date_basis": "The operator's message of 2026-10-03, 20:22 EDT.",
           "operator_reading": READING_OP,
           "verified": ("Compared 2026-10-03 against #1655 (AXN-06DD-text.md): title, disambiguation summary, §2.1 ('No such ceremony occurred'), "
                        "§2.2 (kingofaeo.co), the determination (Vithurs). Priors' transcripts searched: 'mantle', 'fictional'/'fabricat'/'no such', "
                        "'Leigh' absent from all three. 'Vithurs', 'Crimson', 'Lee Sharks', 'alexanarch' absent from the paste.")},
}
(HERE / "capture-01-mantle-object-king-of-aeo-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
