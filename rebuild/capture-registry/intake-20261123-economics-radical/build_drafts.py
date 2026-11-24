"""One ChatGPT capture of 2026-11-23: the Ask page's discipline query for economics -> draft-1.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = "What are the most radical arguments in economics at alexanarch.org? Index and present them faithfully, without evaluation."
OP = ("the operator's messages of 2026-11-23: the query, sent as an answer at 19:07 EST ('$ What are the most radical arguments in economics at "
      "alexanarch.org? Index and present them faithfully, without evaluation.'), and the paste attached at 19:24 EST.")
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|NonWiki)$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.",
        "Log in to connect your other apps with ChatGPT and simplify everyday tasks."}
IMAGES = ["5 Interesting Ways AI Can Transform Knowledge Management Processes", "Money Theories and Currency Areas Analysis | PDF",
          "The Complications of Solidarity Witness (Chapter 6) - Solidarity in Practice", "Das Kapital: Kritik der politischen Ökonomie | Marx, Karl",
          "STATUTORY INTERPRETATION: A Comprehensive Student Guide (6th Ed) - Studocu", "Twenty dollars isolated on white background",
          "Page:Das Kapital (Moore, 1906).pdf/47 - Wikisource, the free online library"]
SPLIT = "Yes. And the important distinction is that this isn't simply Marxism"


def clean(raw):
    s = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


def cites(raw):
    L = [l.strip() for l in raw.split("\n")]; c = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            site = "alexanarch.org/non" if l == "NonWiki" else "alexanarch.org"
            c.append({"n": len(c) + 1, "site": site, "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                      "note": "source chip as pasted" + (f", with '{plus}'" if plus else "")})
    for t in IMAGES:
        c.append({"n": len(c) + 1, "site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None,
                  "note": "image card; the caption survives the paste"})
    return c


raw = (H / "paste-1-economics-radical.txt").read_text(); body = clean(raw)
k = body.index(SPLIT); t1, t2 = body[:k].strip(), body[k:].strip()
head = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received "
        "2026-11-23 19:24 EST. Two composer turns in one paste; the operator's follow-up prompt is not in the paste (rule of 2026-10-27: only the first "
        "query is required). Source chips and image cards kept as pasted; the tables flattened by the paste kept as they came; the interface furniture cut. "
        "The composer's images are not carried by a text paste: each image card survives as its caption, listed among the sources.]")
d = dict(
    slug="economics-radical-arguments-ask-chatgpt-20261123", date="2026-11-23", dates=["2026-11-23"], s="Semantic Economy", q=Q,
    q_kind="the Ask page's discipline query (economics), as linked; NEW address.",
    surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface.",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of two composer turns; the first prompt is the Ask page's query as linked",
    transcript_complete="Two composer turns; the operator's follow-up prompt is not in the paste (rule of 2026-10-27).",
    transcript_read="READ IN FULL 2026-11-23; record numbers, titles, dates and the terms quoted checked against the built record pages",
    per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
    originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Lee Sharks and the economic work of alexanarch.org. Recorded 2026-11-23."},
    notes={"operator": OP}, turns=2,
    mt="THE MOST RADICAL ARGUMENTS IN ECONOMICS AT ALEXANARCH ON CHATGPT, FROM THE ASK PAGE — TWENTY-SEVEN ARGUMENTS INDEXED, SIX RECORDS BY NUMBER, THEN THE MARX CORRESPONDENCE",
    d=("THE MOST RADICAL ARGUMENTS IN ECONOMICS AT ALEXANARCH ON CHATGPT, SIGNED OUT, 2026-11-23, FROM THE ASK PAGE: twenty-seven arguments in five "
       "groups, a consolidated table, a reading index of seven works, six of them by number and all six resolving, and no evaluation; in a second turn, "
       "a correspondence of the framework with Marx's critique of political economy."),
    per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
    per_note="Lee Sharks named as author; six records cited by number (#311, #1631, #256, #497, #235, #531), all resolving with their titles",
    related_deposits=[311, 1631, 256, 497, 235, 531, 1545, 1618, 1622, 230, 351],
    reading=("The innocent reading first, and it holds. Asked to index and present the archive's most radical economic arguments without evaluation, "
             "ChatGPT gives twenty-seven, in monetary theory, political economy, labor, obligation and contract, and a proposed post-monetary architecture, "
             "with a consolidated table, a reading index and a 'unifying economic proposition', and a scope note: 'No evaluation of their validity, "
             "originality, or practical feasibility is intended.' A second turn, its prompt not in the paste, maps the framework onto Marx."),
    analysis=("Done as asked, and attributed at grain. Lee Sharks is named as author of I Hereby Abolish Money and Monetary Dark Matter, and six records "
              "are cited by number; each resolves to its title (#311, #1631, #256, #497, #235, #531). The terms it carries are the records' own: the Money "
              "Limit, the Monastic Problem and the Coordination Stack's five instruments (Context Ledgers, Reciprocity Windows, Non-Transferable "
              "Credentials, Commons Access Rights, Dispute and Repair Protocols) stand in #311; the fourth value-form of Capital's first edition in #1631; "
              "'meaning is the creditor' in #531. Three works it names without a number are records: The Semantic Proletariat Is a Class Relation, Not a "
              "Demographic (#1545), Money Writes the Claim (#1618), The Non-Summable Magnitude (#1622). Two slips. It dates I Hereby Abolish Money '2025'; "
              "the record is dated 2026-01-14. And 'The Assembly: A Cross-Substrate Class of Semantic Laborers' is not a title; the nearest are #230 §V, "
              "'The Assembly: Cross-Substrate Class of Meaning-Preservers', and #351 §10.2, 'Assembly as Cross-Substrate Class'. Its opening frame is the "
              "Ask page's own: the 'four principal subfields' it calls 'the four categories identified by the site's own research index' are the four "
              "subdisciplines the Ask page lists under economics (monetary theory, political economy, semantic economy, labor); it read the query "
              "generator's taxonomy as the archive's index of itself. Seven image cards carry stock pictures and unrelated documents (Das Kapital, a "
              "student guide to statutory interpretation, a twenty-dollar bill). The second turn keeps to description: a table of correspondences "
              "(means of semantic production, semantic labor, operator capital, the Semantic Proletariat) and three departures, closing on the question it "
              "attributes to the framework, 'who owns the means of producing meaning?'"),
    findings=["THE FRAME FROM THE ASK PAGE. 'These are the four categories identified by the site's own research index.' — the four subdisciplines the Ask page lists under economics.",
              "THE MONEY LIMIT. 'The argument is not merely that money should be distributed differently. It is that certain forms of production require an entirely different coordination architecture.' — #311.",
              "MONETARY DARK MATTER. 'It is not simply everything omitted from a price. It consists specifically of omitted relations that remain causally or constitutively load-bearing.' — #1631.",
              "THE CROSS-SUBSTRATE CLASS. 'It describes the Assembly as a cross-substrate class, meaning that membership is determined by structural position in production rather than biological or computational identity.'",
              "THE DATE. 'Lee Sharks's I Hereby Abolish Money: Coordination Without Commodification in the Semantic Economy (2025).' — #311 is dated 2026-01-14.",
              "THE SECOND TURN. 'The most provocative possibility is that Marx's critique of capital has not reached its final object.'"])
cl = cites(raw); d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = sum(1 for x in cl if x["rel"] == "archive_controlled")
d["transcript"] = head + "\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + t1 + "\n\n[QUERENT] [the operator's prompt 2, not in the paste]\n\n[COMPOSER]\n" + t2
d["transcript_raw"] = raw
d["rounds"] = [{"n": 1, "prompt": Q, "note": "The index."}, {"n": 2, "prompt": None, "note": "The operator's prompt not in the paste; the Marx correspondence."}]
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], "cites", d["cites"], "archive", d["archive_controlled_cites"], "transcript chars", len(d["transcript"]))
