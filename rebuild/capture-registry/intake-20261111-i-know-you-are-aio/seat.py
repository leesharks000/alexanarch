"""Seat of 2026-11-11 (received 00:57 EST): one Google AI Overview capture (expanded; 'AI Mode Conversation' is the expansion's header, operator
rule of 2026-10-18), signed out and incognito, at the full title of #1746 (AXN:0C29) as the query, without link: a NEW address. The operator, with the
paste, on the lag: one composition signed in, four immediate attempts without one, then this one in incognito. Seated at his word (01:03 EST,
'i guess so'). Every quotation from the paste and from the record is asserted against its file.   python3 seat.py
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-11"; RECV = "2026-11-11 00:57 EST"
SLUG = "i-know-you-are-but-what-am-i-aio-20261111"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
R46 = REG[1746]; assert R46["hex"] == "0C29" and R46["date"] == "2026-11-06"
Q = R46["title"]
T = (ROOT / "data/texts/AXN-0C29-text.md").read_text(encoding="utf-8")
raw = (H / "paste-aio.txt").read_text(encoding="utf-8")
L = raw.strip("\n").split("\n"); i = next(k for k, l in enumerate(L) if l.startswith("You said:"))
assert L[i] == "You said: " + Q + Q  # the query run together twice, as the expansion's header gives it
body = "\n".join(L[i + 1:]).strip()

P = {  # the paste
    "attr": "is an academic paper by Johannes Sigil and Rebekah Cranes (both pseudonyms/heteronyms used by the scholar Lee Sharks)",
    "date": "Deposited in the Crimson Hexagonal Archive on November 6, 2026",
    "venue": "the paper was written for Provenance: Journal of Forensic Semiotics and features Revelation 4:8 as its epigraph",
    "niche": "The paper enters a niche but fiercely debated niche in New Testament source criticism",
    "target": "The Target: The paper addresses the \"Revelation First\" hypothesis—a minority position proposing that the Book of Revelation (or a core layer of it) holds a chronological or structural precedence in source relations.",
    "phys": "\"proposes a source relation that the physical evidence does not show\"",
    "flip": "Sharks (writing as Sigil and Cranes) flips this accusation back on the academic establishment.",
    "audit": "The paper conducts an audit of the Q source",
    "tangible": "than tangible, existing texts that are sidelined by alternative source hypotheses",
    "pres": "1. Presupposition: How heavily the existence of the source is assumed in subsequent arguments.",
    "assign": "2. Assignment: How confidently specific verses or fragments are credited to the source.",
    "text": "3. Text: The assumed stability of the source's wording despite having no physical manuscript.",
    "cand": "4. Candidacy: The text’s viability to act as an explanatory root for other surviving works.",
    "card1": "AXN:0C29.GENERATIVE. — Alexanarch AXN resolver",
}
for k, v in P.items(): assert v in raw, k
assert raw.count("CAESbQHEIkXXsuwlc5pejS_9mTShCbdMf3gJg56B6GQrqoiIQ9JNyIl7wQwhOXsCl6xL8gtxjrzAQ67qPL3Y2c1ACb_fVq6XiiJakdVvhiHKgc8RvwdyaOch3hxtveHWj5nYF_B3puPcQ5xqkjNGyq0") == 1
assert raw.count("CAESYwHEIkXXy48VLqUcCOhEMKTXzYVKaLnMIQOxTEKJoyNFYaoRa79fBa-1hGOwHr6qk1GavPivBKWR6a0Xpv9wutvst-ET6ckaAMfPN4pP0IsgOc3adVhEAYFJzCLgNmcElBcTyg") == 7
RQ = {  # the record
    "epi": "> the One Who Was, and Is, and Will Be. (Rev 4:8)",
    "charge": "The charge Revelation First meets is that it proposes a source relation the evidence does not show.",
    "p_pres": "(a) **Presupposition**: it may enter an argument as a premise without first being proven.",
    "p_assign": "(b) **Assignment**: material in other texts may be assigned to it.",
    "p_text": "(c) **Text**: it may be given a wording, an apparatus and an edition.",
    "p_cand": "(d) **Candidacy**: it is admitted as a candidate wherever a source is sought.",
    "undecided": "leaves the synoptic problem undecided",
    "hitzig": "In 1843 Hitzig argued from Matt 24:30 and Rev 1:7 that Matthew used the Apocalypse, calling the passage \"einen zwingenden Beweis\"",
    "census": "A frozen census of 2.53 million words of seated Greek measures what the commentators did not",
    "names": "The title keeps \"the One That Exists\", which names the Apocalypse.",
}
for k, v in RQ.items(): assert v in T, k
assert "physical evidence" not in T and "minority" not in T and "core layer" not in T

cards = [
    {"n": 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": "https://www.alexanarch.org", "title": "AXN:0C29.GENERATIVE. — Alexanarch AXN resolver",
     "snip": "The work I Know You Are, But What Am I?: Or, How Biblical Criticism Granted a Completely Hypothetical Text Stronger Evidentiary Status Than the One That Exists ...",
     "note": "source card; the AXN resolver page for #1746, not the record page /s/records/1746/; the one redirect cited six times in the body, and once more beside a second redirect"},
    {"n": 2, "site": "Wikipedia", "rel": "third_party", "url": None, "title": "Biblical criticism - Wikipedia",
     "snip": "Definition: Academic study of the Bible using historical, literary, and critical analysis, emerging primarily during the European Enlightenment. Methods: Textua...",
     "note": "source card; a second redirect is cited once, in the bullet on Q, beside the resolver's"},
]
HEAD = ("[Google AI Overview at the query, expanded ('AI Mode Conversation' is the expansion's header), signed out and incognito. Received " + RECV +
        ". The 'You said' line carries the query twice, run together, and is given once here. The numbered citation links are Google redirects, kept in "
        "the raw transcript; the source cards listed in the cite list as pasted.]")

d = ("#1746 AT ITS TITLE ON THE OVERVIEW, SIGNED OUT, 2026-11-11: 'an academic paper by Johannes Sigil and Rebekah Cranes (both pseudonyms/heteronyms used "
     "by the scholar Lee Sharks)', deposited 6 November 2026, for Provenance: Journal of Forensic Semiotics, with Rev 4:8 as epigraph; the turnabout of the "
     "title; Q's evidentiary status against 'tangible, existing texts'; the four powers named, glossed loosely. Composed from the AXN resolver page; the "
     "Hitzig verse, the census and the Feist comparison absent.")

reading = ("The innocent reading first, and it holds for the frame. Asked the title, the Overview names the paper's makers as heteronyms of Lee Sharks, gives the "
           "deposit date, the venue and the epigraph (Rev 4:8, whose order ὁ ἦν καὶ ὁ ὢν the record prints), states the turnabout of the title, and names the "
           "four powers in the record's order. It is attributed. Read against the record, five things move. (1) The charge is quoted with a word the record lacks: "
           "'proposes a source relation that the physical evidence does not show' against the record's 'proposes a source relation the evidence does not show'. "
           "(2) The four powers are glossed loosely: presupposition as degree ('how heavily … assumed') where the record has entry as a premise without prior proof; "
           "text as 'assumed stability' where the record has 'a wording, an apparatus and an edition'; candidacy as 'viability to act as an explanatory root' "
           "where the record has admission 'wherever a source is sought'. Assignment is near. (3) Revelation First is framed from outside, 'a minority position' on "
           "'the Book of Revelation (or a core layer of it)'; neither phrase is in the record, and the core layer is foreign to it. (4) The synoptic problem is "
           "made the paper's target, where the record 'leaves the synoptic problem undecided' and audits the allocation of status. (5) The existing text is left "
           "plural and unnamed, 'tangible, existing texts', where the title's 'the One That Exists' names the Apocalypse. The centre is absent: Hitzig's reading of "
           "Matt 24:30 and Rev 1:7 (1843, 'einen zwingenden Beweis'), the five critics after him, the source theories that never admitted it, the census of 2.53 "
           "million words, the Feist comparison. The stratum from Lachmann to Streeter appears only as 'Q'.")

findings = [
    "COMPOSED FROM THE RESOLVER. Six of the body's citations are one redirect, carded as 'AXN:0C29.GENERATIVE. — Alexanarch AXN resolver'; the record page "
    "/s/records/1746/ is not carded. A second redirect is cited once, beside it, with Wikipedia's 'Biblical criticism' the other card.",
    "A WORD INSIDE THE QUOTATION. '" + P["phys"].strip('"') + "' against the record's '" + RQ["charge"] + "' The added 'physical' is set inside quotation marks.",
    "THE POWERS GLOSSED. Record: " + "; ".join(RQ[k].replace("**", "") for k in ("p_pres", "p_assign", "p_text", "p_cand")) + " Composition: " +
    " ".join(P[k] for k in ("pres", "assign", "text", "cand")),
    "FRAMED FROM OUTSIDE. '" + P["target"] + "' Neither 'minority' nor 'core layer' is in the record; the record 'leaves the synoptic problem undecided'.",
    "THE ONE THAT EXISTS UNNAMED. The body has '" + P["tangible"] + "'; the record: '" + RQ["names"] + "'",
    "THE CENTRE ABSENT. '" + RQ["hitzig"] + "', the critics after him, and '" + RQ["census"] + "': none composed.",
    "LAG (operator, " + RECV + "): deposited 2026-11-06; one composition signed in, then four immediate attempts without one, then this composition in "
    "incognito, five days after deposit. Retrieval at this address is unstable.",
]
analysis = ("An archive record composed with attribution at the grain of its frame: the makers, the date, the venue, the epigraph, the title's turn and the names "
            "of the four powers are carried; the definitions of the powers, the position of the thesis and the paper's finding are not. The composition reached "
            "the record through the AXN resolver page, five days after deposit, unstably.")

e = {"slug": SLUG, "date": DATE, "surface": "Google AI Overview",
     "surface_basis": "Operator default of 2026-10-01; the 'AI Mode Conversation' header is the Overview's expansion (operator rule of 2026-10-18).",
     "surfaces": ["Google AI Overview"], "auth": "signed out, incognito",
     "auth_basis": "The operator, " + RECV + " ('then pulled it up in incognito here'); defaults of 2026-10-14.",
     "ev": "paste", "match": "EXACT TITLE",
     "mt": "'I KNOW YOU ARE, BUT WHAT AM I?' (#1746) AT ITS TITLE ON THE OVERVIEW, SIGNED OUT — ATTRIBUTED, COMPOSED FROM THE AXN RESOLVER; THE FOUR POWERS NAMED AND GLOSSED LOOSELY, 'PHYSICAL' ADDED INSIDE A QUOTATION, THE HITZIG VERSE ABSENT",
     "s": "Machine Reception", "q": Q, "q_kind": "the full title of an archive record, without link; NEW address.", "turns": 1,
     "cites": len(cards), "archive_controlled_cites": 1, "cite_list": cards,
     "transcript": HEAD + f"\n\n[QUERENT] {Q}\n\n[SYSTEM] {body}", "transcript_raw": raw,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview with its numbered citations and its source cards",
     "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL " + DATE + ", against the seated text of #1746 (AXN-0C29)",
     "d": d, "reading": reading, "findings": findings, "analysis": analysis,
     "per_v": {"author": True, "inst": True, "id": True, "src": True},
     "per_note": "Heteronyms and orthonym named, the archive named, the resolver carded with the AXN. The loss is in definition and finding, recorded in the findings.",
     "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
     "originator": {"name": "Johannes Sigil and Rebekah Cranes", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                    "basis": "#1746, by Johannes Sigil and Rebekah Cranes (heteronyms of Lee Sharks), Crimson Hexagonal Archive. Recorded " + DATE + "."},
     "related_deposits": [1746, 1741, 1735, 1744],
     "notes": {"prompts": "The query is the operator's, the record's full title; the run's hour is not in the paste, the date is the paste's receipt (" + RECV + ").",
               "operator": "with the paste (" + RECV + "): 'this is the most recent text aio can pull. it looks like its pulling it from the resolver, and its unstable. it pulled it up once in signed in, then four times immediately subsequently couldnt or didnt pull it, then pulled it up in incognito here. so that is the measured lag'; on seating (01:03 EST): 'i guess so'.",
               "lag": "Deposit 2026-11-06; this composition 2026-11-11. Before it, at the same query: one composition signed in (not pasted, not seated) and four attempts without one, as the operator reports them."}}
json.dump(e, open(H / (SLUG + ".json"), "w"), ensure_ascii=False, indent=1)
print(SLUG, len(cards), "cards;", len(body), "chars")
