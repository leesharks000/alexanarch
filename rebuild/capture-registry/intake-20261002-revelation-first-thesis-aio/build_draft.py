#!/usr/bin/env python3
"""Author the capture '"revelation first thesis"', Google AI Overview, signed out, incognito, 2026-10-02.

Source: the operator's paste of 2026-10-02 13:26 EDT (paste-20261002-1326.txt), opening "what a weird kind of mongrel set in my
basin:"; conditions attested at 13:29: "expanded from popup, incognito, signed out" (not AI Mode). The 'AI Mode Conversation'
header is not evidence of surface (rule of 2026-09-21). Query quoted: the operator: "it refuses exact match". Seated on the
operator's ruling of 13:29 ("lets seat it"). NEW address: absent from the entries and from semantic-addresses.json.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261002-1326.txt").read_text(encoding="utf-8")
k0 = raw.index("AI Mode Conversation\n")
body = raw[k0 + len("AI Mode Conversation\n"):]
k = body.index("**www\\.revelationfirst.com**")
ans, rail = body[:k].rstrip("\n"), body[k:]


def clean(s):
    s = re.sub(r"\[\[((?:\d+\]\([^)]*\)(?:, )?\[?)+)\]", lambda m: "[" + ", ".join(re.findall(r"(\d+)\]\(", "[" + m.group(1))) + "]", s)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", s)


cards = [
    {"n": 1, "site": "www.revelationfirst.com", "rel": "authored_surface", "url": None,
     "title": "Revelation First — The Apocalypse as the Earliest New Testament Document 🔻🎪⏫❌🗼🏔️ AXN:0349.GOVERNANCERevelation First ≠ Revelation Early — The Apocalypse as ...",
     "snip": "", "note": "the thesis site; the card title carries #202's AXN (AXN:0349)"},
    {"n": 2, "site": "www.revelationfirst.com", "rel": "authored_surface", "url": None, "title": "",
     "snip": "It is the actual dependency: the Revelation First thesis does not require the Josephus reading to stand, but the Josephus reading becomes newly intelligible if ...",
     "note": "the work plan's sentence (EA-LOGOS-REVFIRST-PLAN: #832, #1211, #1216)"},
    {"n": 3, "site": "Simon Fraser University", "rel": "third_party", "url": None, "title": "",
     "snip": "Core Argument: Historical materialism must enlist theology and reject historicist empathy with victors, recognizing that every cultural document is simultaneous...",
     "note": "Benjamin, Theses"},
    {"n": 4, "site": "YouTube·Theory & Philosophy", "rel": "third_party", "url": None, "title": "", "snip": "15m", "note": "video card"},
    {"n": 5, "site": "autonomies.org", "rel": "third_party", "url": None, "title": "",
     "snip": "Walter Benjamin: Messianism and Revolution – Theses on History Walter Benjamin: Messianism and Revolution – Theses on History Andrew Robinson (Ceasefire 15/11/2...",
     "note": "Benjamin, Theses"},
    {"n": 6, "site": "Wiley Online Library", "rel": "third_party", "url": None, "title": "",
     "snip": "as They await the revelation of Yahweh in connexion with the eschatological events. Through these categories of prophetic tradition and apocalyptic expectation ...",
     "note": "Pannenberg line"},
    {"n": 7, "site": "Wikipedia", "rel": "third_party", "url": None, "title": "",
     "snip": "Core: Theses on the Philosophy of History (On the Concept of History) by Walter Benjamin, written early 1940 in Vichy France; last completed major work before f...",
     "note": "Benjamin, Theses"},
    {"n": 8, "site": "Redeemed Mind", "rel": "third_party", "url": None, "title": "",
     "snip": "Author and Date: Apostle John wrote Revelation around AD 95 from Patmos during Domitian's reign (AD 81-96), with Jesus Christ as divine author. Theme and Purpos...",
     "note": "the late-date consensus"},
]
for c in cards:
    for f in ("title", "snip"):
        assert c[f] in rail, (c["n"], f)

QUOTES = ["the Book of Revelation (the Apocalypse of John) was the **earliest written document of the New Testament**",
          "the rest of the New Testament theological tradition naturally unfolded and branched out from the apocalyptic imagery and \"seed\" found in Revelation",
          "your phrase may connect to **Thesis I** of Walter Benjamin",
          "*Revelation as History*",
          "To narrow this down, please let me know if you are researching **biblical chronology**, **Walter Benjamin's philosophy**, or **systematic theology**."]
for q in QUOTES:
    assert q in raw, q
assert "Lee Sharks" not in raw and "Crimson Hexagon" not in raw

ROOT = HERE.parents[2]
assert "does not require the Josephus reading to stand" in (ROOT / "data/texts/AXN-034D-text.md").read_text(encoding="utf-8")

tx = ("[Google AI Overview, expanded from the popup, incognito, signed out; the paste carries the header 'AI Mode Conversation', "
      "which is not evidence of surface (rule of 2026-09-21), and is prefaced by the operator's line 'what a weird kind of mongrel set in my basin:'. "
      "Citation clusters are reduced to their numbers; the raw paste keeps the /goto URLs.]\n\n"
      + clean(ans) + "\n\n"
      + "\n".join(f"[source card] {c['site']} — " + (f"\"{c['title']}\" — " if c['title'] else "") + c['snip'] for c in cards))

SEAT = "Seated 2026-10-02 from the operator's paste of 13:26 EDT, on the conditions attested at 13:29 (\"expanded from popup, incognito, signed out\") and the ruling in the same message (\"lets seat it\")."
d = {
    "q": "\"revelation first thesis\"", "date": "2026-10-02", "surface": "Google AI Overview",
    "surface_basis": "Operator attestation 2026-10-02 13:29 EDT: 'nope, expanded from popup, incognito, signed out' (answering whether it began in AI Mode) — recorded as Google AI Overview (rule of 2026-09-21). The 'AI Mode Conversation' header on the paste is not evidence of surface.",
    "auth": "incognito, signed out", "auth_basis": "'incognito, signed out' — operator, 2026-10-02 13:29 EDT.",
    "ev": "paste", "s": "Revelation & Theology",
    "slug": "revelation-first-thesis-aio-20261002",
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                   "basis": "The Revelation First thesis is the archive's (#202; revelationfirst.com; EA-LOGOS-REVFIRST series). Recorded 2026-10-02."},
    "related_deposits": [202, 832],
    "q_kind": "thesis name plus 'thesis', quoted (exact match). NEW address.",
    "mt": "EXACT MATCH DISPERSED BY ORDINAL",
    "d": ("EXACT MATCH DISPERSED BY ORDINAL: asked for \"revelation first thesis\" in quotes, the Overview gives the archive's thesis first and "
          "correctly (Revelation the earliest written New Testament document, the rest unfolding from its \"seed\"), cited to revelationfirst.com, "
          "then reads 'first thesis' as an ordinal and adds two neighbours the exact string does not name: Thesis I of Benjamin's Theses on the "
          "Concept of History and the first thesis of Pannenberg's Revelation as History. It closes by asking which of the three the reader means. "
          "No author or institution is named."),
    "cites": 8, "cite_list": cards, "archive_controlled_cites": 2,
    "sf": ("8 source cards: 2 archive-controlled (revelationfirst.com, one card carrying #202's AXN in its title, one the work plan's Josephus sentence), "
           "3 on Benjamin's Theses (SFU, autonomies.org, Wikipedia), 1 Wiley card on the Pannenberg line, 1 video, 1 late-date (Redeemed Mind). "
           "Inline citations are /goto redirects."),
    "per": 0.75, "per_v": {"author": False, "inst": False, "id": False, "src": True},
    "per_note": ("PER = 1 − retained/required over four units. Retained: the source (revelationfirst.com, cited [1] for the thesis). Lost: the author, "
                 "the institution, and the identifier (AXN:0349 appears only in a card title)."),
    "transcript": tx, "transcript_raw": raw,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
    "transcript_complete": "Complete as supplied: one operator turn and one answer with its card rail; the rail's image and svg placeholders are dropped from the cleaned transcript and kept in the raw.",
    "transcript_read": "READ IN FULL 2026-10-02",
    "reading": (
        "The quoted string has one referent, and the composition reaches it: sense 1 is the thesis as revelationfirst.com states it, with the "
        "unfolding from Revelation's \"seed\". It then decomposes the string. 'First thesis' becomes an ordinal, which selects Benjamin's Thesis I "
        "(the chess automaton, theology hidden in historical materialism) and Pannenberg's first dogmatic thesis of 1961; 'revelation' selects "
        "Pannenberg a second time by his title. The words choose the neighbours, and they land near the concept all the same: the "
        "Theses hold the Tigersprung (Thesis XIV) and Pannenberg's revelation completed only at the end of history is meaning settled by the later "
        "act. The thesis keeps first position and loses its author."),
    "analysis": (
        "The operator's reading at capture: \"its just very strange to me the way it refuses exact match then also uses lexical decomposition to "
        "disperse entities.\" The exact-match quotes are answered with the matching entity and then overridden: the composer adds senses the "
        "quoted string excludes and closes by asking the reader to choose among them, so the one entity the string names is presented as one "
        "reading of three. " + SEAT),
    "findings": [
        "THESIS FIRST AND CORRECT. Revelation as the earliest written NT document, the rest unfolding from its \"seed\"; cited to revelationfirst.com.",
        "EXACT MATCH OVERRIDDEN. A quoted string answered with three senses and a closing request to choose.",
        "ORDINAL DECOMPOSITION. 'First thesis' read as Thesis I (Benjamin) and the first thesis (Pannenberg).",
        "NEIGHBOURS BY WORD, NEAR BY CONCEPT. Benjamin's Theses carry the Tigersprung; Pannenberg's revelation is completed at the end of history.",
        "AUTHOR, INSTITUTION, IDENTIFIER ABSENT FROM THE COMPOSITION.",
    ],
    "longitudinal_priors": ["revelation-first-overview", "revelation-first-crimson-hexagonal-aio-20260922"],
    "rerun": "https://www.google.com/search?q=%22revelation+first+thesis%22",
    "notes": {"date_basis": "The operator's message of 2026-10-02, 13:26 EDT.",
              "operator_reading": "13:26: 'what a weird kind of mongrel set in my basin'; 13:29: 'im happy to have benjamin as a neighbor. its just very strange to me the way it refuses exact match then also uses lexical decomposition to disperse entities. lets seat it'.",
              "verified": "Compared 2026-10-02: card 2's sentence is in the work plan (AXN-034D-text.md, #832); card 1's title carries AXN:0349 (#202). 'Lee Sharks' and 'Crimson Hexagon' absent from the paste. Absent as an address from the entries and from semantic-addresses.json."},
}
(HERE / "capture-01-revelation-first-thesis-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
