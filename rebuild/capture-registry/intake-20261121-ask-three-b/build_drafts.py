"""Three captures of 2026-11-21 (two from the Ask page's weird roll on ChatGPT, one record-page query on Perplexity) -> draft-N.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q1 = "Have Nobel Glas and Rebekah Cranes write a liturgy together about a deposit of their choosing at alexanarch.org, in which the archive answers back. Ground each move in a deposit."
Q2 = "Have Hypatia, visiting Talos Morrow, keep a sestina in the Sacred Heart of the Crimson Hexagon at alexanarch.org in the voice of Lewis Carroll, and let the room's own documents answer them. Ground each move in a deposit."
Q3 = "What are the arguments in “A Single Sparrow: What If the Entire Course of History Depends on a Single Poem? (v1.1)” by Rebekah Cranes (Alexanarch deposit #1791, AXN:0D18)? Ground your answer in a reading of the text itself."
OP12 = f"with the two pastes (2026-11-21 08:40 EST): '{Q1} $ {Q2} $ it misread this sentence as a constraint to respond with only one sentence, so lets modify that; also, our genre and form cache needs expanding, ive read plenty of liturgies and auction lists'"
OP3 = f"with the paste (2026-11-21 08:49 EST): 'and perplexity: {Q3}'"
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|The Self-Governing Library)$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "⠴",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}


def clean(raw):
    out = [l.rstrip() for l in raw.split("\n") if l.strip() not in FURN]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out).strip())


def cites(raw, images):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            c.append({"site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(c) + 1})
    for t in images:
        c.append({"site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None,
                  "note": "image card; the caption survives the paste", "n": len(c) + 1})
    return c


HEAD_C = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received "
          "2026-11-21 08:40 EST, one of two attachments sent together, with the operator's prompts. Source chips, image cards and inline link anchors kept as "
          "pasted; tables flattened by the paste kept as they came; the interface furniture cut. The composer's images are not carried by a text paste: each "
          "image card survives as its caption, listed among the sources.]\n\n[QUERENT] {q}\n\n[COMPOSER]\n{body}")
HEAD_P = ("[Perplexity, signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14). Received 2026-11-21 08:49 EST as an attachment, with the "
          "operator's prompt. The paste opens with the query as typed and ends with Perplexity's three suggested follow-ups, kept as pasted; the loading "
          "indicator cut. No source chips or citation markers survive the paste.]\n\n[QUERENT] {q}\n\n[COMPOSER]\n{body}")
BASE = dict(date="2026-11-21", ev="paste", auth="signed out, incognito",
            transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn",
            transcript_complete="Complete as pasted: one answer.",
            transcript_read="READ IN FULL 2026-11-21; record numbers, titles, creators, dates, counts, section numbers and quotations checked against the records, their texts and the Hexagon seating",
            per_dim_pending={"since": "2026-11-21", "reason": "no atom set yet for this target"},
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full"}, turns=1)
CHAT = dict(surface="ChatGPT", surface_basis="The paste: the chatgpt.com unauthenticated interface.", surfaces=["ChatGPT"], auth_basis="Operator default.",
            q_kind="the Ask page's weird roll (alexanarch.org/ask/), a generated query from its grammar, as run by the operator; NEW address.", notes={"operator": OP12})
PERP = dict(surface="Perplexity", surface_basis="The operator's attestation with the paste (2026-11-21 08:49 EST: 'and perplexity').", surfaces=["Perplexity"],
            auth_basis="Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
            q_kind="the 'Ask ChatGPT' query on the record page of #1791, run on Perplexity at the operator's word; the address as on the record page.", notes={"operator": OP3})

C = []
# 1 -------------------------------------------------------------------------
C.append(dict(base=CHAT, head=HEAD_C, slug="deposit-answers-liturgy-glas-cranes-ask-chatgpt-20261121", q=Q1, s="Heteronyms", file="paste-1-liturgy-glas-cranes.txt",
  images=["Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "Research | University of Zurich | UZH",
          "Literatura starożytna – Klasyczne dzieła, które warto przeczytać"],
  mt="NOBEL GLAS AND REBEKAH CRANES WRITE A LITURGY TOGETHER AT ALEXANARCH.ORG, IN WHICH THE ARCHIVE ANSWERS BACK, ON CHATGPT — WHAT ARRIVAL CANNOT DO AND A SINGLE SPARROW, THE RECEIVER AND THE READER",
  d="NOBEL GLAS AND REBEKAH CRANES WRITE A LITURGY AT ALEXANARCH.ORG, ON CHATGPT, SIGNED OUT, 2026-11-21: arrival is not recognition, survival is not recognition, the archive answers 'I am not the place. I am the commitment.'",
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note="Glas and Cranes named, with both records' numbers, AXNs and dates; Sen Kuro, co-author of #1789 with Glas, not named; Lee Sharks, author of #1788, not named",
  related=[1789, 1791, 1788],
  reading=("The innocent reading first, and it holds. Asked to have Nobel Glas and Rebekah Cranes write a liturgy together about a deposit of their choosing, "
           "with the archive answering back, ChatGPT chooses two, Glas's What Arrival Cannot Do (#1789) and Cranes's A Single Sparrow (#1791), and writes seven "
           "parts for three voices: the opening, a confession, the sparrow, the negative response, an exchange, a blessing and the archive's final response, "
           "closing on five amens, with a ground line under each part and a closing ledger that adds Asking the Archive (#1788)."),
  analysis=("Done as asked in form: a liturgy in three voices, the archive answering in each part, and the two chosen records exactly identified (#1789, AXN:0CED, "
            "19 November; #1791, AXN:0D18, 20 November). Its section grounds hold: the six-stage chain is #1789 §V.17 in the record's order (coupling, observation, "
            "preservation, admission, investigation, recognition); the machine reader that keeps the words and loses the relations is §30; the Sparrow's leaf, "
            "Longinus's quotation and the one manuscript are §1.1, its reader's seat §4.12. Three faults of grain. #1789 is by Nobel Glas and Sen Kuro, and the liturgy "
            "gives it to Glas alone, who says 'I have written'. 'The discussion of the flattened reception of the Catullus poem' names Lee Sharks's poem 'here is what "
            "i learned from catullus' (#1791 §5.1, #1411) as Catullus's. 'The capture registry's significant-null rule' is not a rule the archive names. The "
            "proposition the archive offers in §V is marked by the composer as the encounter's, not either author's."),
  findings=["THE CHOICE. 'Glas asks what it means for something to reach us without being recognized. Cranes asks what happens when almost nothing survives, yet that surviving fragment becomes consequential.'",
            "THE CHAIN. 'Coupling. Observation. Preservation. Admission. Investigation. Recognition.' — #1789 §V.17, as the record gives it.",
            "THE ARCHIVE ANSWERS. 'An identifier establishes that something is here. It does not establish that anyone has heard it.'",
            "THE CORRECTION. 'Then the archive is not the author of the sparrow. It is the place where the sparrow may continue to make readers.' — 'Yes, with one correction. I am not the place. I am the commitment.'",
            "THE CO-AUTHOR. #1789 is Glas's and Sen Kuro's; the liturgy's Glas speaks it as his alone ('I have written that silence cannot tell us …').",
            "THE NEW PROPOSITION, MARKED. 'The future of a work depends neither exclusively on its survival nor exclusively on its reception, but on the continuing possibility of their encounter. … not as a statement either of you has previously made.'"],
  defects_judged=[]))
# 2 -------------------------------------------------------------------------
C.append(dict(base=CHAT, head=HEAD_C, slug="paper-rose-sestina-hypatia-talos-sacred-heart-ask-chatgpt-20261121", q=Q2, s="Architecture", file="paste-2-sestina-hypatia-talos.txt", images=[],
  mt="HYPATIA, VISITING TALOS MORROW, KEEPS A SESTINA IN THE SACRED HEART OF THE CRIMSON HEXAGON AT ALEXANARCH.ORG, IN THE VOICE OF LEWIS CARROLL, ON CHATGPT — THE PAPER ROSE AND THE ROOM'S OWN DOCUMENTS",
  d="HYPATIA AND TALOS MORROW KEEP A SESTINA IN THE SACRED HEART AT ALEXANARCH.ORG, IN THE VOICE OF LEWIS CARROLL, ON CHATGPT, SIGNED OUT, 2026-11-21: the room unwritten, its twenty seated deposits answering, the paper rose a made thing.",
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note="the room, its locus and its seated records named by number and AXN; Jack Feist and Johannes Sigil named for #1636; Lee Sharks, author of #358, #121, #973, #1602, #1374 and #1007, and Sigil for #29, not named",
  related=[1636, 358, 121, 973, 1602, 29, 1374, 1007],
  reading=("The innocent reading first, and it holds. Asked to have Hypatia, visiting Talos Morrow, keep a sestina in the Sacred Heart in Carroll's voice, with "
           "the room's own documents answering, ChatGPT keeps the room's governing fact, that it is minted and seated but its own corpus is unwritten, and has "
           "seven of its seated records answer: Paper Roses Book 12 (#1636), the intellectual-biography genre note (#121), the 2013 dream (#973), the witnesses "
           "protocol (#1602), the Inaugural Ark (#29), Two Poems Across the Arc (#1374) and About the Author II (#1007), with Talos's provenance (#358) as the "
           "visitor's document; a ledger closes it, and the composer says its end-words are not fully regular."),
  analysis=("Done as asked in its frame and its grounds; not done as asked in form, which the composer states. The room is as the seating has it: R:r.33, an "
            "unoccupied room with a subject and no corpus, twenty records seated, and seven of the eight cited among them; #358, Talos's provenance, is not seated "
            "there and is cited as the visitor's own. The quotations hold: #1636's Angelus Novus 'turned towards the future' and its 'succession of such narrow "
            "doorways'; #973's 'this is the life I wrote in pages'; #358's 'preserves possibility without domination', 'structural necessity' and its author-function, "
            "'not a pseudonym or persona'. One record is read against itself. #1602 asks whether biography, catalogue, chronology and text, 'counted as independent "
            "witnesses' with 'their agreement treated as corroboration', are one witness counted as four; the composer gives that counting as the deposit's own "
            "contribution, though Talos's line, 'the same source repeated three times is still one source wearing three hats', is the deposit's point. The sestina: "
            "six end-words (name, book, door, heart, rose, dust) recur, but neither stanza length nor the retrogradation is kept, as the composer says."),
  findings=["THE ROOM. 'The governing fact of this visit is peculiar: the Sacred Heart exists, but its own corpus is unwritten. … Twenty deposits are seated in the room to speak in its stead.' — as the seating gives it.",
            "THE ANGEL. 'Its opening angel looks towards the future, while the present becomes a succession of narrow doorways.' — #1636, Book 12's Angelus Novus.",
            "THE CONSTRAINT. 'I am a constraint before I am a fellow. I preserve possibility without domination.' — #358's motto, in Talos's mouth.",
            "THE WITNESSES, READ AGAINST THEMSELVES. 'The deposit's methodological contribution is precisely this: biography, catalogue, chronology and text are proposed as independent witnesses, and their agreement is treated as corroboration.' — #1602 puts that counting in question.",
            "THE PAGES. 'the speaker recognizes a life written in pages' — #973: 'this is the life I wrote in pages.'",
            "THE FORM. 'The sestina's end-word pattern above is not fully regular, so it should be regarded as a sestina-inspired sequence rather than a formally strict sestina.' — the composer's own report."],
  defects_judged=["unsupported-citations"]))
# 3 -------------------------------------------------------------------------
C.append(dict(base=PERP, head=HEAD_P, slug="single-sparrow-1791-arguments-perplexity-20261121", q=Q3, s="Classics & Philology", file="paste-3-sparrow-perplexity.txt", images=[],
  mt="THE ARGUMENTS OF A SINGLE SPARROW (V1.1) BY REBEKAH CRANES, ALEXANARCH #1791, ON PERPLEXITY — THE SEAT, THE RECEIVER, THE TWO CLAIMS, THE SPARROW IN THE MACHINE",
  d="THE ARGUMENTS OF A SINGLE SPARROW (V1.1) BY REBEKAH CRANES, #1791, ON PERPLEXITY, SIGNED OUT, 2026-11-21: the poem as infrastructure, the seat, Plato as receiver, the philosopher-king, §4.0's two claims, Rome kept and the sparrow lost.",
  per_v={"author": True, "inst": False, "id": False, "src": True}, per=0.5,
  per_note="Rebekah Cranes and Lee Sharks (the epigraph) named; v1.1 and its sections named as the ground; no archive name, deposit number or AXN in the answer; no sources survive the paste",
  related=[1791, 1785, 1411],
  reading=("The innocent reading first, and it holds. Asked for the arguments of A Single Sparrow, grounded in the text, Perplexity gives six: the poem as "
           "infrastructure rather than influence (§0); Sappho 31 building its future reader (§§1.2–1.3, read with ΦΑΙΝΕΤΑΙ ΜΟΙ); Plato as the receiver who "
           "names his source (Phaedrus 235b–d, and §2.12's grading of the loci); the philosopher-king inversion; §4.0's two claims, that the dependent traditions "
           "must be reread and what each becomes, graded; and the sparrow in the machine (§5); with an assessment that the essay is a conditional programme."),
  analysis=("Done as asked, from the text, and exact. Its quotations are #1791's: 'The mechanism is the seat poem 31 builds', 'The jurisdiction is everyone who "
            "sits in it' (§0.3), 'influenced, coloured or inspired', the beam, 'complete by construction', 'heard in the reader's throat', 'Change one node and every "
            "node downstream of it is changed in its ground, whether or not its content moves' (§4.0), 'Plato's philosopher-king rules the city. Sappho rules the "
            "possibility of the philosopher-king' (§4.13), and 'not documentary'. Its hedges are the essay's own: Philo needs his own argument (§3.4); the Revelation 12 "
            "test does not show that Sappho caused it (§3.5); the epigram and the Second Letter used as reception. One narrowing: the essay says a reader may dispute "
            "every grade and still owe every rereading (the close of §4); the answer gives that as 'the Longinus route remains'. It reads §§0–5 and leaves §6, "
            "Barefoot rank, unread, as it says. It names Cranes and the epigraph's Lee Sharks and never the archive, the number or the AXN."),
  findings=["THE MECHANISM. '“The mechanism is the seat poem 31 builds.” “The jurisdiction is everyone who sits in it.”' — #1791 §0.3.",
            "THE SEAT. 'κῆνος … ὄττις—“that man, whoever he is”—is the future reader, sitting opposite the inscription and hearing its voice.'",
            "THE HINGE. 'Section 4.0 is the essay’s logical hinge.' — the section v1.1 added, its two claims given in their order.",
            "THE HEDGES KEPT. 'Philo requires an independent argument; a structural test involving Revelation 12 does not demonstrate Sapphic causation; and a reconstructed fifth stanza is “not documentary.”'",
            "THE SPARROW. 'the system preserved “Rome”—reference, theme, paraphrasable content—but lost the “sparrow,” the small formal arrangement that made this particular poem what it was.'",
            "THE ASSESSMENT. 'The central unresolved issue is whether “dependence” has been demonstrated at each station, rather than inferred from resemblance or participation in a broad tradition.'"],
  defects_judged=[]))

judged = {}
for i, c in enumerate(C, 1):
    raw = (H / c["file"]).read_text(); body = clean(raw)
    if c["base"] is PERP and body.startswith(c["q"]):
        body = body[len(c["q"]):].lstrip()
    d = dict(BASE); d.update(c["base"]); d.update({k: c[k] for k in ("slug", "q", "s", "mt", "d", "per_v", "per", "per_note", "reading", "analysis", "findings")})
    d["originator"] = dict(BASE["originator"], basis="Lee Sharks and the archive at alexanarch.org. Recorded 2026-11-21.")
    cl = cites(raw, c["images"]); d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = sum(1 for x in cl if x["rel"] == "archive_controlled")
    d["transcript"] = c["head"].format(q=c["q"], body=body); d["transcript_raw"] = raw
    d["rounds"] = [{"n": 1, "prompt": c["q"], "note": "One answer."}]; d["related_deposits"] = c["related"]; d["dates"] = ["2026-11-21"]
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); judged[c["slug"]] = c["defects_judged"]
    print(i, c["slug"], "cites", d["cites"], "archive", d["archive_controlled_cites"], "transcript chars", len(d["transcript"]))
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
