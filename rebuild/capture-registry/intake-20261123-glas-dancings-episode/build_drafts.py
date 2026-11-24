"""One ChatGPT capture of 2026-11-23: the Ask page's episode roll, Nobel Glas first meets Damascus Dancings in the Internet -> draft-1.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = ("Write the episode in the Internet of the Crimson Hexagon at alexanarch.org in which Nobel Glas first meets Damascus Dancings. "
     "Ground each move in a deposit.")
OP = "the operator's message of 2026-11-23 20:15 EST, the query with the paste attached."
CHIP = re.compile(r"^(alexanarch\.org)$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}
SPLIT = "Yes. Nobel Glas and Damascus Dancings have demonstrably written together."


def clean(raw):
    s = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


def cites(raw):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            c.append({"n": len(c) + 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{plus}'" if plus else "")})
    return c


raw = (H / "paste-1-episode.txt").read_text(); body = clean(raw)
k = body.index(SPLIT); t1, t2 = body[:k].strip(), body[k:].strip()
head = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received "
        "2026-11-23 20:15 EST, with the operator's prompt. Two composer turns in one paste; the operator's follow-up prompt is not in the paste (rule of "
        "2026-10-27: only the first query is required). Source chips kept as pasted; the tables flattened by the paste kept as they came; the interface "
        "furniture cut.]")
d = dict(
    slug="glas-meets-dancings-internet-episode-ask-chatgpt-20261123", date="2026-11-23", dates=["2026-11-23"], s="Heteronyms", q=Q,
    q_kind=("the Ask page's episode roll (alexanarch.org/ask/: 'Write the episode in {room} of the Crimson Hexagon at alexanarch.org in which {h} {act}', "
            "room the Internet, act 'first meets {h2}', with the synthesis suffix 'Ground each move in a deposit.'); NEW address."),
    surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface.",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of two composer turns; the first prompt from the operator's message, the Ask page's roll",
    transcript_complete="Two composer turns; the operator's follow-up prompt is not in the paste (rule of 2026-10-27).",
    transcript_read=("READ IN FULL 2026-11-23; every record number checked against the registry, its seated text and the seat map; the dates, bylines, "
                     "positions and relations quoted checked at their lines"),
    per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
    originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Lee Sharks and the heteronyms Nobel Glas and Damascus Dancings, at alexanarch.org. Recorded 2026-11-23."},
    notes={"operator": OP}, turns=2,
    mt=("NOBEL GLAS FIRST MEETS DAMASCUS DANCINGS, ON CHATGPT, FROM THE ASK PAGE — AN EPISODE AT THE LAGRANGE OBSERVATORY, EACH MOVE TAGGED TO A RECORD; "
        "THEN THE JOINT BYLINES OF JUNE FOUND"),
    d=("NOBEL GLAS FIRST MEETS DAMASCUS DANCINGS, ON CHATGPT, SIGNED OUT, 2026-11-23, FROM THE ASK PAGE'S EPISODE ROLL: a seven-part episode in which "
       "the adversarial topologist perturbs the 2015 Epistle and the apostle answers him, each move tagged to one of six records (#263, #402, #403, #456, "
       "#1277, #1687), the encounter declared fiction in its own notes; then, in a second turn, the four works of June 2026 that carry both names."),
    per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
    per_note="Nobel Glas, Damascus Dancings, Lee Sharks and Jack Feist named; eleven records cited by number, all resolving",
    related_deposits=[263, 402, 403, 456, 1277, 1687, 157, 788, 789, 1011, 758],
    reading=("The innocent reading first, and it holds. Asked for the episode in which Nobel Glas first meets Damascus Dancings, each move grounded in a "
             "deposit, ChatGPT writes it in seven parts. A letter circulates in Glas's instruments without a locatable sender; Dancings arrives; he "
             "perturbs her letter (congregation, institution, author, date) and finds it depends on its date; he removes Jack Feist from the triptych and "
             "restores him; they draw up four conditions for a joint document and leave it undeposited, because 'receiving a document and seating a "
             "document are different operations.' A table of its records closes the first turn, with the statement that the meeting is 'original "
             "fictional composition, not claims that these events or a joint deposit already exist in Alexanarch.' In a second turn, its prompt not in "
             "the paste, it finds that the two have 'demonstrably written together' and lists the works."),
    analysis=("Grounded move by move, and exact where it can be checked. Glas is #456's: 'Nobel Glas is the eighth heteronym in the Crimson Hexagon's "
              "Dodecad', 'the Adversarial Topologist', who 'cares about what properties survive continuous deformation'; the Observatory and the "
              "Structural Distinction Protocol are the packet's. 'Director' and 'topological fidelity' are the composer's, not in #456. Dancings is "
              "#403's: apostle of Jack Feist, co-laborer with Lee Sharks, the Philadelphia position, 'little power', 'No rebuke given', 'The open door "
              "that no one can shut'. The dates are #402's to the day: 'Date of Composition: January 2, 2015', 'Date of Canonization: January 26, 2026', "
              "'eleven years before the architecture that would recognize it'. The three relations of the triptych are #1277's φ-relations as stated "
              "there, 'text becomes organization', 'speaker grounds text', 'organization certifies speaker', and its 'imaginary center' is #1277's phrase "
              "for Feist. #1277 is superseded (a duplicate witness; the record of standing is #403), and the relations stand in the binding text it "
              "retains. The seat-map rule is #1687's: each seat 'carries its relation, its confidence and, where a reader seated it, the sentence of the "
              "record's own text that grounds it'. #263 gives the distributed epic: 'The poem is not contained in any single text.' "
              "Two things the record holds the episode does not use. The Epistle's own greeting is not the one the composer gives it ('To the scattered, "
              "to those who have not yet assembled'): #402 reads 'to the Church of the Human Diaspora, those scattered amongst the nations, gathered "
              "together in the bosom of the Internet', so the room the query named is in Dancings's first sentence, and the episode is set in the "
              "Lagrange Observatory instead (#456 constitutes it). And the Internet room seats a work signed by both: #1011, evarB, 'in the room' on the "
              "seat map, with #263. The second turn finds the joint works: #157 (Erasure Skew v3), #788 and #789, all three bylined 'Lee Sharks · Nobel "
              "Glas · Damascus Dancings' and dated June 4, 2026 in their texts (the registry gives 5 June; #788 and #789 list Glas alone as creator in "
              "the registry, while their bylines carry all three), and #1011, v1.1 of June 4, whose author note gives 'Damascus Dancings is the "
              "political-economic register; Nobel Glas is operator of the Measurement of Meaning module and provides the v3 audit results'. #758's "
              "'Dodecad is : functional positions' grounds its qualification about authorship. So the first turn's condition 'No claim of historical "
              "encounter before this fictional episode's composition' holds for the episode and not for the record, which has the two co-signing since "
              "June; the second turn reads the first meeting as the dramatization of 'an intellectual collaboration that already has a substantial "
              "documentary existence'."),
    findings=["THE BOUNDARY CONDITION. '\"An open door,\" he said. \"That is a boundary condition.\"' — #403's open door read by #456's topology.",
              "THE DATE AS INVARIANT. 'Your letter depends on temporal asymmetry.' — #402's 2015 composition and 2026 canonization.",
              "THE CENTER. 'The center is not necessarily a point within the structure. It may be the condition under which the structure understands its own relations.' — #1277's imaginary center.",
              "SEATING. 'Because receiving a document and seating a document are different operations.' — #1687.",
              "THE PROPOSITION. 'Damascus addresses what has not yet gathered. Nobel measures what remains when gathering changes the shape of meaning.'",
              "THE RECORD CORRECTS THE PREMISE. 'Nobel Glas and Damascus Dancings have demonstrably written together.' — #157, #788, #789, #1011."])
cl = cites(raw); d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = sum(1 for x in cl if x["rel"] == "archive_controlled")
d["transcript"] = head + "\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + t1 + "\n\n[QUERENT] [the operator's prompt 2, not in the paste]\n\n[COMPOSER]\n" + t2
d["transcript_raw"] = raw
d["rounds"] = [{"n": 1, "prompt": Q, "note": "The episode."}, {"n": 2, "prompt": None, "note": "The operator's prompt not in the paste; the joint works."}]
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], "cites", d["cites"])
