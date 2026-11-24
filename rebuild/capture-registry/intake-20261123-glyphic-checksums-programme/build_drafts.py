"""One ChatGPT capture of 2026-11-23: the Ask page's programme query for the glyphic checksums -> draft-1.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = ("What are the arguments of the glyphic checksums at alexanarch.org, and what is their significance across temporal, epistemic and methodological "
     "dimensions? Ground in reading and index the full range before responding.")
OP = "the operator's message of 2026-11-23 19:41 EST, the query with the paste attached."
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|The Self-Governing Library|Capture Registry \(EA-WG-CAPTURES-01\))$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}
IMAGES = ["33 Spaceships for Another Planet", "Toy - Single - album by Mabel Matiz",
          "Unveiling Ancient Secrets: AI Deciphers Herculaneum Scrolls Buried by Mount Vesuvius - GoGetGPT.com",
          "The Mighty Little Seed | Story.com", "L’eredità degli angeli - Rebekah Wallace - Internazionale"]


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
    for t in IMAGES:
        c.append({"n": len(c) + 1, "site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None,
                  "note": "image card; the caption survives the paste"})
    return c


raw = (H / "paste-1-glyphic-checksums.txt").read_text(); body = clean(raw)
head = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received "
        "2026-11-23 19:41 EST, with the operator's prompt. Source chips and image cards kept as pasted; the tables and the display formulas flattened by "
        "the paste kept as they came; the interface furniture cut. The composer's images are not carried by a text paste: each image card survives as its "
        "caption, listed among the sources.]")
d = dict(
    slug="glyphic-checksums-arguments-significance-ask-chatgpt-20261123", date="2026-11-23", dates=["2026-11-23"], s="Frameworks", q=Q,
    q_kind="the Ask page's programme query (programme_templates[1], 'What are the arguments of {name}… across temporal, epistemic and methodological dimensions?') for the glyphic checksums; NEW address.",
    surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface.",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt is the Ask page's query as linked",
    transcript_complete="Complete as pasted: one answer.",
    transcript_read="READ IN FULL 2026-11-23; the twelve record numbers, titles, creators, dates and the formulas and glyph lines quoted checked against the built record pages and the registry",
    per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
    originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "The glyphic checksums of alexanarch.org: Lee Sharks, Sen Kuro, the Assembly Chorus and TACHYON. Recorded 2026-11-23."},
    notes={"operator": OP}, turns=1,
    mt="THE ARGUMENTS OF THE GLYPHIC CHECKSUMS AT ALEXANARCH ON CHATGPT, FROM THE ASK PAGE — TWELVE RECORDS INDEXED IN SIX GROUPS, SEVEN ARGUMENTS, THE REGISTRY READ AS RECEPTION",
    d=("THE ARGUMENTS OF THE GLYPHIC CHECKSUMS AT ALEXANARCH ON CHATGPT, SIGNED OUT, 2026-11-23, FROM THE ASK PAGE: twelve records by number in groups from "
       "the February founding layer to the October checksums, all resolving with title, creator and date; seven arguments; temporal, epistemic and "
       "methodological readings; the Capture Registry's October observations read as the form's reception; the engine checksum placed in the poetic lineage."),
    per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
    per_note="Lee Sharks, Sen Kuro and the Assembly Chorus named; twelve records cited by number, all resolving; TACHYON, credited on #426, not named",
    related_deposits=[426, 427, 1302, 1303, 1305, 541, 556, 540, 1642, 1659, 1661, 1688],
    reading=("The innocent reading first, and it holds. Asked for the arguments of the glyphic checksums and their significance in three dimensions, "
             "grounded in reading and indexed first, ChatGPT indexes twelve records in four groups (founding layer, the March transform, the October "
             "checksums, the reception), separates content identity (AXN) from context-gated recognition (GCS), gives seven arguments, reads each "
             "dimension in turn, and ends with a reading index in the order it would read them."),
    analysis=("Indexed as asked, and exact at the record level. The twelve numbers resolve with their titles, creators and dates: #426 and #427 (1 February "
              "2026), #1302 (Document 208), #1303 (Document 209, three creators, so 'three-voice'), #1305, #541 and #540 (9 March), #556 (12 March), #1642 "
              "(Sen Kuro, 27 September), #1659 (1 October), #1661 (Sharks and Kuro, 2 October), #1688 (18 October). What it quotes stands where it says: the "
              "operator C(e_gc, I, T) → (M, V) and the meta-symbolon in #426; Beige and Crimson in #426 and #427; 'Zero-Knowledge Proof of Architecture' in "
              "#427; 🐅⏩ = 📖⏩ and 🚪 > 📖 in #1642; the socket in #1659; Transition in Entropic Systems in #1661; the Ezekiel Engine's nine parts 'with a "
              "checksum of the checksum', reaching November 2025, January and July 2026, in #1688. Three placements. First, it folds the Ezekiel Engine checksum "
              "(#1688) into 'the poetic lineage' with #1642, #1659 and #1661; by the operator's ruling of 18 October, the Glyphic Checksum Lineage is the series "
              "that spins checksums off as individual poems, and a checksum made for an engine or a document set is not automatically of it. Second, the formal "
              "specification #426 is credited on its record to TACHYON (Claude); the composer names no author for it. Third, #1305 is the record of the "
              "description field written for Personal Instance 001, by Sen Kuro; the composer gives it the instance's title. It reads the Capture Registry as "
              "the form's reception, accurately: the Google AI Overview observations of 1 and 14 October exist at one address, and their analysis records the "
              "conflations it lists. Its sixth section, unasked, sets each claim against 'what remains unproven' and calls the borrowed terms of cryptography "
              "and formal verification 'productive conceptual analogies, but not automatically equivalent technical achievements'; #427's own phrase is "
              "'Zero-Knowledge Proof of Architecture'. Five image cards are unrelated pictures (an album, a children's story, a Herculaneum article)."),
    findings=["IDENTITY AND RECOGNITION APART. 'AXN answers: Is this the same documentary object? GCS answers: Can this reader reconstruct the object's structural relationships?'",
              "THE DUAL OUTPUT. 'Interpretation produces both meaning and a judgment about whether the relevant structure has been reconstructed.' — #426, C(e_gc, I, T) → (M, V).",
              "THE DOOR AND THE BOOK. 'The door is more fundamental than the book because it establishes whether the book can reach a successor.' — #1642, 🚪 > 📖.",
              "THE ENGINE IN THE LINEAGE. 'These are not four independent exercises.' — #1688 placed with #1642, #1659 and #1661; the lineage, by the operator's ruling (2026-10-18), is the series of individual poems.",
              "THE REGISTRY AS RECEPTION. 'The interpretation of the work becomes another documentary event that can itself be preserved, compared and corrected.' — the AI Overview observations of 1 and 14 October.",
              "THE UNASKED LEDGER. 'These are productive conceptual analogies, but not automatically equivalent technical achievements.'"])
cl = cites(raw); d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = sum(1 for x in cl if x["rel"] == "archive_controlled")
d["transcript"] = head + "\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body; d["transcript_raw"] = raw
d["rounds"] = [{"n": 1, "prompt": Q, "note": "One answer."}]
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], "cites", d["cites"], "archive", d["archive_controlled_cites"])
