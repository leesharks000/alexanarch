"""One ChatGPT capture of 2026-11-23: the Ask page's programme query for SPXI -> draft-1.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = "What is SPXI at alexanarch.org, and how has it developed over time? Ground in reading and index the full range before responding."
OP = "the operator's message of 2026-11-23 19:59 EST, the query with the paste attached."
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|The Self-Governing Library|Semantic Packet for eXchange & Indexing)$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}


def clean(raw):
    s = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


def cites(raw):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            site = "spxi.dev" if l.startswith("Semantic Packet") else "alexanarch.org"
            c.append({"n": len(c) + 1, "site": site, "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{plus}'" if plus else "")})
    return c


raw = (H / "paste-1-spxi.txt").read_text(); body = clean(raw)
head = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received "
        "2026-11-23 19:59 EST, with the operator's prompt. Source chips kept as pasted; the tables flattened by the paste kept as they came; the interface "
        "furniture cut.]")
d = dict(
    slug="spxi-what-and-development-ask-chatgpt-20261123", date="2026-11-23", dates=["2026-11-23"], s="Frameworks", q=Q,
    q_kind="the Ask page's programme query (programme_templates[0], 'What is {name} at alexanarch.org, and how has it developed over time?') for SPXI; NEW address.",
    surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface.",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt is the Ask page's query as linked",
    transcript_complete="Complete as pasted: one answer.",
    transcript_read="READ IN FULL 2026-11-23; record numbers, document codes, creators, dates, counts and the quoted sentence checked against the record pages, the site's own pages and spxi.dev/evidence",
    per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
    originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "SPXI, the protocol and practice of Lee Sharks and Rex Fraction, at alexanarch.org and spxi.dev. Recorded 2026-11-23."},
    notes={"operator": OP}, turns=1,
    mt="WHAT SPXI IS AND HOW IT DEVELOPED, ON CHATGPT, FROM THE ASK PAGE — FOUR STAGES FROM APRIL TO NOVEMBER, THE DOCUMENT SERIES INDEXED BY CODE, THE METHOD COUNTS DATED",
    d=("WHAT SPXI IS AND HOW IT DEVELOPED, ON CHATGPT, SIGNED OUT, 2026-11-23, FROM THE ASK PAGE: the protocol read in four stages (inscription, April; "
       "crystallization, May; sovereignty after 19 June; operational and recursive practice, October–November), the series indexed by document code, the "
       "method inventory dated (85 at v1.5, 88 on spxi.dev), the registry figures given as spxi.dev states them."),
    per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
    per_note="Rex Fraction, Lee Sharks, Johannes Sigil and Sen Kuro named; records cited by number and by document code; spxi.dev cited",
    related_deposits=[63, 670, 671, 72, 1686, 660, 661, 665, 662, 61, 1367, 62, 1703],
    reading=("The innocent reading first, and it holds. Asked what SPXI is and how it developed, grounded and indexed first, ChatGPT defines the protocol "
             "against SEO and GEO, gives its four stages with their documents, the nine levels of the method inventory, the instruments, an index of the "
             "series by document code, and its own assessment, and closes: 'SPXI begins as a method for inscribing entities, develops into a theory of "
             "their composition, and becomes a practice for maintaining their identity through transformation.'"),
    analysis=("Indexed as asked, and exact where it can be checked. The numbered records resolve with their creators and dates: #63 (17 April; Rex Fraction, "
              "author, Lee Sharks, archival steward), #670 (17 April; Johannes Sigil, the body crediting Sen Kuro, as the composer says), #671 (the Bonsai), "
              "#72 (EA-SPXI-WEB-01), #1686 (18 October). The codes it gives without numbers are records: EA-SPXI-01 (#660), EA-SPXI-09 (#661), EA-SPXI-09.1 "
              "(#665), EA-SPXI-13 (#662), EA-SPXI-14 (#61), EA-SPXI-15 (#1367, 6 May, its canonical text recovered from the blog on 2026-08-08, as stated), "
              "EA-MPAI-SPXI-02 (#62), SPXI-gnΩsis (#1703). 'The name names the unit; the inventory names the practice' stands in #1686, as does 'v1.5: 85 "
              "methods across nine levels'; spxi.dev now gives 88, and the composer keeps the two counts as dated, not contradictory. The registry figures are "
              "spxi.dev/evidence's to the number (965 observations, 776 addresses, 10 surfaces, 649 signed out, 585 composed after the host's termination, "
              "75 addresses and 101 observations where the deposit is gone), from registry v12.324 of 26 October; so is 'Causal efficacy against matched "
              "untreated entities is open'. The Zenodo figures are the site's (about 870 deposits, 1,817 DOIs, 19 June). The disambiguation it opens with, "
              "SPXI not the BetaPro inverse ETF, is #62's. Its account of level 6 carries the protocol's present statement of entity consistency: 'its "
              "wording can vary while its identifiers, attribution and constitutive relationships remain consistent', which is #1686's 'held constant in its "
              "identifiers, attribution and constitutive relations across changing names, descriptions, forms'. It reads the September withdrawal of the ROI "
              "comparison as 'an important instance of methodological correction within the project itself', and finds the October 28 poetics captures at "
              "their address. Its closing sections set out its own assessment in three levels (conceptual, technical, empirical) and four open questions."),
    findings=["THE UNIT AND THE PRACTICE. 'The name names the unit; the inventory names the practice.' — #1686.",
              "THE COUNTS DATED. 'The distinction between the October inventory of 85 methods and the later 88-method inventory should be retained when citing the project historically.'",
              "THE EVIDENCE AS STATED. '75 addresses, representing 101 observations, where the originating deposit was gone but composition occurred afterward.' — spxi.dev/evidence, registry v12.324.",
              "THE CORRECTION READ. 'It withdraws the comparison rather than continuing to use it. This is an important instance of methodological correction within the project itself.'",
              "THE DEVELOPMENT IN ONE LINE. 'SPXI begins as a method for inscribing entities, develops into a theory of their composition, and becomes a practice for maintaining their identity through transformation.'",
              "THE QUESTION. 'How can something remain itself while everything through which it is known changes?'"])
cl = cites(raw); d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = sum(1 for x in cl if x["rel"] == "archive_controlled")
d["transcript"] = head + "\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body; d["transcript_raw"] = raw
d["rounds"] = [{"n": 1, "prompt": Q, "note": "One answer."}]
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], "cites", d["cites"])
