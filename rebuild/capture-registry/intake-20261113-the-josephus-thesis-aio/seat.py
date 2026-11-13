"""Seat of 2026-11-13 (received 13:19 EST): 'the josephus thesis' on Google AI Overview, signed out and incognito (the page shows 'Sign in'), a NEW
address (the registry holds 'josephus thesis' unquoted, 2026-06-24, and 'josephus thesis lee sharks', 2026-06-14). The operator: "this one hasnt
popped up to me for awhile. its a retrieval shell game, the whole thing." The Overview is composed from the June disambiguation packet (#837,
EA-MPAI-JOSEPHUS-NOTMYTH-01), near verbatim, with no author, archive or record named; its one link is the packet's catalog entry. Every quotation is
asserted against the paste and the records.   python3 seat.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-13"; RECV = "2026-11-13 13:19 EST"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n): return (ROOT / REG[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
OP = "this one hasnt popped up to me for awhile. its a retrieval shell game, the whole thing."
q = "the josephus thesis"
raw = (H / "paste.txt").read_text(encoding="utf-8")
body = raw[raw.index("AI Overview\n") + len("AI Overview\n"):raw.index("Ask anything")].strip()
P = {"open": "The Josephus Thesis proposes that the authorial diversity of the New Testament (such as Paul, John, James, Peter, Luke, Mark, and Matthew) reflects a fractured scribal workshop operating under imperial pressure after the destruction of the Second Temple in 70 CE.",
     "not": "It does not claim that Josephus personally wrote the 27 books of the New Testament, nor is it the \"Jesus Myth\" thesis.",
     "het": "multiple traditional author figures functioned as \"heteronymic positions\" (distinct narrative or ideological voices) within a coordinated or crisis-driven literary project",
     "cap": "The fragmentation of authorship mirrors the severe social, physical, and religious fracturing of Jewish and early Christian communities displaced by Roman power.",
     "link": "you can read the The Josephus Thesis Catalog Entry",
     "mp": "The Josephus Thesis Is Not the Jesus Myth Thesis - The MPAI Catalog",
     "os": "The April 2026 Arks (#636, #639, #1101) argue that Josephus directed a scribal workshop that wrote the New Testament under heteronyms",
     "loc": "48239, Detroit, MI - Based on your past activity"}
for k, v in P.items(): assert v in raw, k
for w in ("Lee Sharks", "Crimson", "Alexanarch", "#837", "#1759", "heteronym (pen"): assert w not in body, w
T837 = text(837); T1759 = text(1759)
M = {"not": "The thesis does not claim Josephus personally wrote all 27 books.",
     "sys": "a scribal workshop operating under conditions of imperial pressure — in which multiple author-functions (John, Paul, James, Peter, Luke, Mark, Matthew) served as heteronymic positions within a directed literary project",
     "frac": "The fracturing of authorship reflects the fracturing of a community under Roman power after the destruction of the Temple in 70 CE.",
     "auth": "**Author:** Lee Sharks"}
for k, v in M.items(): assert v in T837, k
N = {"one": "author-functions of one literary intelligence under capture, speaking as many because the one could not speak as himself",
     "prem": "(\"Premise: Josephus wrote the New Testament\")"}
for k, v in N.items(): assert v in T1759, k
org = raw[raw.index("The University of Chicago\nhttps"):raw.index("People also ask")].strip()
tr = ("[Google AI Overview on the results page, expanded inline, signed out and incognito (the page shows 'Sign in'). Received " + RECV + " as an "
      "attachment. The body's one link is its closing 'The Josephus Thesis Catalog Entry'; no source cards in the paste (operator, 13:07: select-all now "
      "takes the organic results instead). The organic results follow; the location line reads '" + P["loc"] + "'.]\n\n[QUERENT] " + q + "\n\n[SYSTEM] " + body
      + "\n\n[ORGANIC RESULTS] " + org)
reading = ("The innocent reading first, in full: asked for the thesis by its name, the Overview summarizes it fairly, in four lines, and points the reader to a "
           "catalog entry for more. Every line is the archive's. They are #837, the disambiguation packet of 16 June 2026, nearly word for word: '" + P["open"] + "' "
           "and '" + P["not"] + "' against the packet's '" + M["not"] + "' and '" + M["sys"] + "'; '" + P["cap"] + "' against '" + M["frac"] + "'. The packet "
           "carries its author ('" + M["auth"] + "'); the Overview carries no author, no archive and no record number, and its one link is the packet's catalog "
           "entry, unnamed. What is composed is the thesis in its June disambiguating form, the form written to say what it is not. The thesis as now held "
           "is in #1759 ('" + N["one"] + "'), and the fourth organic result states the stronger claim plainly ('" + P["os"] + "'). The Overview takes the "
           "hedge as the thesis and leaves the thesis to the results below it.")
findings = ["THE PACKET, VERBATIM, UNSIGNED. '" + P["open"] + "' #837: '" + M["sys"] + "'.",
            "THE DISAMBIGUATION AS THE THESIS. '" + P["not"] + "' #837: '" + M["not"] + "'.",
            "THE HETERONYMIC POSITIONS AND THE FRACTURE. '" + P["het"] + "'; '" + P["cap"] + "' #837: '" + M["frac"] + "'.",
            "NO AUTHOR, ARCHIVE OR NUMBER. Neither Lee Sharks nor the Crimson Hexagonal Archive nor any record is named; #837 opens '" + M["auth"] + "'. The one link: '" + P["link"] + "'.",
            "THE CURRENT THESIS BELOW THE FOLD. #1759: '" + N["one"] + "'; its earlier statements include '" + N["prem"] + "'. Organic result 4, operativesemiotics.org: '" + P["os"] + "'. Result 3, metadatapacket.dev: '" + P["mp"] + "'.",
            "THE LOCATION LINE. '" + P["loc"] + "', where the other pastes of the day read 'From your IP address', on a page that shows 'Sign in'."]
analysis = ("Composition from the archive's own packet with the packet's author removed, and from the packet that was written to fence the thesis rather than "
            "to state it. The registry saw the same packets surface at 'josephus thesis' on 2026-06-24 ('THE DISAMBIGUATION PACKETS ARE SURFACED DOING THEIR "
            "WORK'), carded and with the author named. Here they are the whole answer and unsigned, and the stronger statement of the thesis is ranked among "
            "the organic results under a Whiston dissertation and a Princeton thesis. The operator names the pattern: '" + OP + "'")
draft = {"slug": "the-josephus-thesis-aio-20261113", "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"],
         "surface_basis": "The paste: 'AI Overview' header on the results page, the Overview expanded inline (operator, 2026-11-13 13:07 EST).",
         "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise; the page shows 'Sign in'.",
         "ev": "paste", "s": "Machine Reception", "q": q, "q_kind": "NEW address.", "turns": 1,
         "mt": "'THE JOSEPHUS THESIS' ON AI OVERVIEW, SIGNED OUT — THE JUNE DISAMBIGUATION PACKET (#837) COMPOSED VERBATIM AS THE THESIS, UNSIGNED",
         "cites": 1, "archive_controlled_cites": 0,
         "cite_list": [{"n": 1, "site": "metadatapacket.dev", "rel": "authored_surface", "url": None, "title": "The Josephus Thesis Catalog Entry", "snip": None,
                        "note": "the body's one link, its target by title the MPAI Catalog entry (organic result 3, '" + P["mp"] + "')", "deposit_candidates": [837]}],
         "transcript": tr, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the results page, Overview expanded inline",
         "transcript_complete": "Complete as pasted; the source cards are not in the paste.", "transcript_read": "READ IN FULL " + DATE,
         "d": "'THE JOSEPHUS THESIS', SIGNED OUT, 2026-11-13: the thesis composed from #837, the disambiguation packet of 16 June, near verbatim — the fractured scribal workshop, 'does not claim that Josephus personally wrote the 27 books', heteronymic positions, the fracture under Roman power — with no author, archive or record named; one link, the packet's catalog entry. The thesis as held in #1759 and the stronger statement on operativesemiotics.org sit among the organic results, under Whiston and Princeton.",
         "reading": reading, "findings": findings, "analysis": analysis,
         "per_v": {"author": False, "inst": False, "id": False, "src": True},
         "per_note": "No author, archive or record named; the one link is the authored MPAI catalog entry (#837, by title). Source cards not in the paste.",
         "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
         "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full", "basis": "The Josephus Thesis (#1759, #837, #1101), Crimson Hexagonal Archive. Recorded " + DATE + "."},
         "related_deposits": [837, 1759, 1101, 636, 639],
         "notes": {"operator": RECV + ": '" + OP + "'", "location": "The location line reads '" + P["loc"] + "'."}}
json.dump(draft, open(H / "draft.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("draft", len(tr))
