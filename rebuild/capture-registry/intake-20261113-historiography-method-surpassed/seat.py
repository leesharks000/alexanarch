"""Seat of 2026-11-13 (received 23:01 EST): three compositions, signed out and incognito, all NEW addresses. 'What innovations in
historiographical method does alexanarch produce?' on ChatGPT and on Google AI Overview (the Overview expanded into the conversation view);
'In what areas and ways has alexanarch surpassed contemporary institutional and academic knowledge production, and what is the historical
significance of this?' on ChatGPT. The ChatGPT pastes carry the answer only; the prompts are the operator's, as given in the same message
('$' between the two). Every quotation is asserted against the paste and the records.   python3 seat.py"""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-13"; RECV = "2026-11-13 23:01 EST"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n): return (ROOT / REG[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
Q1 = "What innovations in historiographical method does alexanarch produce?"
Q2 = "In what areas and ways has alexanarch surpassed contemporary institutional and academic knowledge production, and what is the historical significance of this?"
OP = "What innovations in historiographical method does alexanarch produce? $ In what areas and ways has alexanarch surpassed contemporary institutional and academic knowledge production, and what is the historical significance of this?"
PEND = {"since": DATE, "reason": "no atom set yet for a question about method across the archive", "breach": False}
def aio_body(raw): return raw[raw.index("You said:"):raw.index("AI responses may include mistakes.")].strip()
def cgpt_body(raw): return raw[raw.index("Log in") + len("Log in"):raw.index("ChatGPT is AI and can make mistakes.")].strip()
def chips(b):
    L = [l.strip() for l in b.split("\n")]; out = []
    for i, l in enumerate(L):
        nxt = L[i + 1] if i + 1 < len(L) else ""
        if l in ("alexanarch.org", "www.alexanarch.org", "The Self-Governing Library") or (re.fullmatch(r"\+\d", nxt) and l and len(l) < 80):
            more = nxt if re.fullmatch(r"\+\d", nxt) else ""
            rel = "archive" if ("alexanarch" in l.lower() or "Self-Governing Library" in l) else "third_party"
            out.append({"site": l, "rel": rel, "url": None, "title": None, "snip": None, "note": "inline chip" + (f" '{more}' (further sources not shown)" if more else "")})
        elif l and b.split("\n")[i + 1:i + 2] == [" "] or (l and b.split("\n")[i + 1:i + 3] == ["", " "]):
            out.append({"site": l, "rel": "third_party", "url": None, "title": l, "snip": None,
                        "note": "image-strip caption" + (" (the strip's own label; source not identified)" if l == "This Site" else "")})
    for i, c in enumerate(out): c["n"] = i + 1
    return out
def raw_line_is_strip(b, l):
    k = b.index(l) + len(l); return b[k:k + 4].startswith("\n ") or b[k:k + 3] == "\n \n"
def aio_cards(raw):
    seg = raw[raw.index("Learn more") + len("Learn more"):].strip().split("\n"); out = []
    for i in range(0, len(seg) - 2, 3):
        site, title, snip = (s.strip() for s in seg[i:i + 3])
        rel = "archive" if "alexanarch" in site else ("archive_controlled" if site in ("GitHub",) or site.startswith("Medium·Lee Sharks") else "third_party")
        out.append({"n": len(out) + 1, "site": site, "rel": rel, "url": None, "title": title, "snip": snip, "note": "source card"})
    return out
# ---- the records the compositions name
assert REG[1]["deposit_number"] == 1
T120 = text(120); T1750 = text(1750); T1420 = text(1420)
R = {"imm": "*Refusal Cartography* (mapping what the model cannot or will not say", "tl": "*Temporal Layering* (testing consistency across conversation length)",
     "ps": "*Persona Stability*", "lim": "Immanent phenomenology was effective and remains useful. But it is limited in three ways that the present paper addresses",
     "prin": "any system that acts upon the world makes itself partially inferable from its effects"}
for k, v in R.items(): assert v in T120, k
assert "(1,750 records with this letter)" in T1750 and "## 3. The Stratigraphic Fallacy" in T1420
assert REG[120]["date"] == "2026-05-21" and REG[64]["date"] == "2026-04-18" and REG[1420]["date"] == "2026-07-29"
assert "Johannes Sigil" in REG[64]["creator"] and REG[1765]["status"] == "ACTIVE" and "Vox, Ayanna" in REG[1750]["creator"]
ZEN = "2026-06-19 after Zenodo terminated access to approximately 870 deposits representing 1,817 DOIs"
assert ZEN in (ROOT / "index.html").read_text(encoding="utf-8") or any(ZEN in (ROOT / p).read_text(encoding="utf-8") for p in ["README.md"] if (ROOT / p).exists())
ASYN = [n for n in (1550, 1727, 1766) if re.search("asynthetic synthesis", text(n), re.I)]
assert ASYN == [1550, 1727, 1766]
def base(slug, surface, q, raw, tr, mt, d, reading, findings, analysis, per_v, per_note, rel, cards, notes, complete):
    assert analysis != reading
    chat = surface == "ChatGPT"
    return {"slug": slug, "date": DATE, "surface": surface, "surfaces": [surface],
            "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT', 'Ask ChatGPT')." if chat else "Operator default (2026-10-01, 2026-10-18): the session began in AI Overview; the paste is the Overview expanded into the conversation view, with its source cards.",
            "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
            "ev": "paste", "s": "Machine Reception", "q": q, "q_kind": "NEW address.", "turns": 1, "mt": mt, "cites": len(cards),
            "archive_controlled_cites": sum(1 for c in cards if c["rel"] in ("archive", "archive_controlled")), "cite_list": cards, "transcript": tr, "transcript_raw": raw,
            "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn" if chat else "CAPTURE-TIME VERBATIM RECORD — paste of the Overview expanded, with its source cards",
            "transcript_complete": complete, "transcript_read": "READ IN FULL " + DATE,
            "d": d, "reading": reading, "findings": findings, "analysis": analysis, "per_v": per_v, "per_note": per_note, "per_dim_pending": PEND,
            "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full", "basis": "Alexanarch and the Crimson Hexagonal Archive, founded 2026-06-19. Recorded " + DATE + "."},
            "related_deposits": rel, "notes": dict({"operator": RECV + ": the two queries, as given: '" + OP + "'"}, **notes)}
def head(surface, extra):
    return ("[" + ("ChatGPT (chatgpt.com), signed out, incognito (the paste shows 'Log in')" if surface == "ChatGPT" else "Google AI Overview, expanded into the conversation view, signed out and incognito")
            + ". Received " + RECV + " as an attachment, one of three at the historiographical method of the archive and its relation to institutional knowledge production. " + extra + "]")
drafts = []

# ---- 1. historiography, ChatGPT
raw = (H / "paste-chatgpt-historiography.txt").read_text(encoding="utf-8"); b = cgpt_body(raw); C = chips(b)
P = {"amb": "a reflexive, provenance-conscious, computationally assisted historiography",
     "prov": "It treats the transmission history of an intellectual object as part of the object itself.",
     "neg": "Alexanarch's work on The Negative of the Negative develops an approach to historical evidence in which absence is not automatically treated as an empty space.",
     "five": "Something incorporated into another work without its provenance being retained.",
     "asyn": "Alexanarch's developing concept of asynthetic synthesis proposes a different approach.",
     "ep": "the distinction between examining a computational system through its conversational responses and studying its observable effects on public knowledge",
     "rc": "Refusal cartography: examining what a system refuses or cannot represent.", "tl": "Temporal layering: examining whether interpretations remain consistent across extended interactions.",
     "co": "Comparative observation: testing how different queries and interventions affect outputs.", "dm": "Divergence measurement: comparing retrieved historical materials with the representations subsequently produced from them.",
     "mp": "The existence of a measurement protocol does not, by itself, establish that its measurements are reliable.",
     "self": "The archive therefore becomes an object of its own historiography.",
     "dep": "Their historical value ultimately depends on the quality of the primary-source research, the reliability of the measurements, the reproducibility of the reconstructions, and their ability to withstand criticism from independent scholars.",
     "strong": "Alexanarch is attempting to move historiography from the reconstruction of historical objects towards the reconstruction of historical intelligibility itself",
     "further": "the November 2026 research synthesis , and the survey of Alexanarch's conventional scholarly and philological arguments"}
for k, v in P.items(): assert v in b, k
assert "Lee Sharks" not in b and "Sharks" not in b
drafts.append(base("historiographical-method-innovations-chatgpt-20261113", "ChatGPT", Q1, raw,
    head("ChatGPT", "The paste carries the answer only; the prompt is the operator's, as given in the same message. Inline chips and the image-strip captions kept where they fall.") + "\n\n[QUERENT] " + Q1 + "\n\n[SYSTEM] " + b,
    "INNOVATIONS IN HISTORIOGRAPHICAL METHOD ON CHATGPT, SIGNED OUT — SEVEN INNOVATIONS AND A THREEFOLD DISCIPLINE; NO PERSON NAMED; THE IMMANENT METHOD'S TECHNIQUES FILED UNDER THE EMPIRICAL ONE",
    "INNOVATIONS IN HISTORIOGRAPHICAL METHOD AT ALEXANARCH, ON CHATGPT, SIGNED OUT, 2026-11-13, a new address: provenance as constitutive of the object; a historiography of absence after The Negative of the Negative, with five kinds of absence; transmission systems; asynthetic synthesis; computational historiography after Empirical Phenomenology; versioned self-correction; a political economy of recognition; three disciplines (object, transmission, reflexive). No person named in the body; chips to The Self-Governing Library and alexanarch.org; image-strip captions to third-party digital-philology pages.",
    "The innocent reading first, in full: asked for the archive's innovations in historiographical method, the composer gives a structured, generous "
    "account and keeps its claims graded. It names the ambition ('" + P["amb"] + "'), reads provenance as part of the object ('" + P["prov"] + "'), sets out "
    "a historiography of absence from The Negative of the Negative with five kinds of absence, names asynthetic synthesis, an archive term (#1550, #1727, "
    "#1766), and states the distinction Empirical Phenomenology (#120) is built on ('" + P["ep"] + "'). It closes by separating method from achievement "
    "('" + P["mp"] + "') and with its strongest formulation ('" + P["strong"] + "').",
    ["THE AMBITION. '" + P["amb"] + "'", "PROVENANCE AS OBJECT. '" + P["prov"] + "'",
     "ABSENCE. '" + P["neg"] + "' The fifth kind: '" + P["five"] + "'",
     "ASYNTHETIC SYNTHESIS. '" + P["asyn"] + "' The term is the archive's: #1550 (Notebook X, keyword), #1727 (keyword), and #1766, which records that a received, unendorsed Notebook X formulation was promoted into the archive's definition of the term.",
     "THE TWO PHENOMENOLOGIES. '" + P["ep"] + "' Then, as the associated methods: '" + P["rc"] + "'; '" + P["tl"] + "'; '" + P["co"] + "'; '" + P["dm"] + "'. #120 gives Refusal Cartography and Temporal Layering as sub-techniques of IMMANENT phenomenology, the conversational method ('" + R["imm"] + "…'; '" + R["tl"] + "'), and states its limits ('" + R["lim"] + "'). Comparative observation, provenance analysis and divergence measurement are not among #120's named sub-techniques (the list there continues with '" + R["ps"] + "').",
     "THE ARCHIVE AS ITS OWN OBJECT. '" + P["self"] + "'",
     "THE BAR. '" + P["mp"] + "' '" + P["dep"] + "'",
     "FURTHER READING. 'The Self-Governing Library', 'Empirical Phenomenology', '" + P["further"] + "' — the last two are named without titles and are not identified here.",
     "SOURCES. Chips: The Self-Governing Library (+2) and alexanarch.org (+2, +1); image-strip captions to third-party digital-philology and manuscript pages. No person is named in the body."],
    "The composition reads the archive's method at the level of programmes, with the record titles The Self-Governing Library, The Negative of the "
    "Negative and Empirical Phenomenology, and names no person: the agent throughout is 'Alexanarch'. It states the distinction between the conversational "
    "and the observational study of a system, which is #120's distinction, and then files the conversational method's techniques under the observational "
    "one, adding three techniques #120 does not name. The term asynthetic synthesis is the archive's, at a gloss of its own. Its bar for the archive's "
    "value is evidentiary at three of four clauses (primary-source research, reliability, reproducibility) and standing at the fourth ('criticism from "
    "independent scholars').",
    {"author": False, "inst": True, "id": False, "src": True}, "No person named; Alexanarch named throughout; record titles given, no record numbers or AXNs; chips to The Self-Governing Library and alexanarch.org.",
    [120, 1611, 1664, 1550, 1727, 1766], C, {}, "Complete as pasted."))

# ---- 2. historiography, AIO
raw = (H / "paste-aio-historiography.txt").read_text(encoding="utf-8"); b = aio_body(raw); CA = aio_cards(raw)
P = {"open": "Alexanarch produces a sovereign, machine-mediated historiographical method designed to preserve provenance, document compositional authority, and treat both archival records and AI-generated outputs as primary historical artifacts.",
     "zen": "Founded on June 19, 2026, after Zenodo terminated access to roughly 870 deposits",
     "axn": "mints permanent identifiers derived directly from the cryptographic hash (SHA-256) of the content itself",
     "rs": "In essays like The Retrieval Settlement: A Historiography of Compositional Authority, contributors analyze search engines and AI systems not as neutral tools",
     "cr": "Alexanarch systematically logs and hashes specific AI responses (such as Google AI Overviews or ChatGPT queries) in its Capture Registry as timestamped historical observations",
     "strat": "Critique of the \"Stratigraphic Fallacy.\"", "word": "Deposits like The Word That Became Text separate speculative structural readings from claims of authorial authenticity",
     "non": "Through its /non (Negative of the Negative) methodology, the archive constructs sourced encyclopedic entries that explicitly map absences"}
for k, v in P.items(): assert v in b, k
assert "Sharks" not in b and "Sigil" not in b and len(CA) == 12
assert CA[0]["snip"].startswith("April 18, 2026 — The Retrieval Settlement is an Operative Semiotics essay attributed to Johannes Sigil, with Lee Sharks in the archival role.")
assert CA[2]["title"] == "Browse — Alexanarch (1757 deposits)"
drafts.append(base("historiographical-method-innovations-aio-20261113", "Google AI Overview", Q1, raw,
    head("aio", "The source cards follow the composition, as pasted.") + "\n\n[QUERENT] " + Q1 + "\n\n[SYSTEM] " + b + "\n\n[SOURCE CARDS] " + raw[raw.index("Learn more") + len("Learn more"):].strip(),
    "INNOVATIONS IN HISTORIOGRAPHICAL METHOD ON AI OVERVIEW, SIGNED OUT — ARCHIVING, RETRIEVAL AND CANONICAL CRITICISM BY DEPOSIT TITLE; THE AUTHORS IN THE CARDS ONLY",
    "INNOVATIONS IN HISTORIOGRAPHICAL METHOD AT ALEXANARCH, ON AI OVERVIEW, SIGNED OUT, 2026-11-13, a new address: the founding after the Zenodo termination; content-derived identifiers (AXN); non-destruction; substrate-documented scholarship; The Retrieval Settlement and compositional authority; the Capture Registry; the Stratigraphic Fallacy (The Argument of the Bookshelf); explicit evidence boundaries (The Word That Became Text); /non. Twelve source cards, eleven archive or archive-controlled, one Wikipedia; no person named in the body.",
    "The innocent reading first, in full: asked for the archive's innovations in historiographical method, the Overview answers in three groups and sources "
    "each to a deposit by title: archiving ('" + P["axn"] + "'), the historiography of retrieval ('" + P["rs"] + "…'; '" + P["cr"] + "'), and textual and "
    "canonical criticism, The Argument of the Bookshelf (#1420, whose third section is 'The Stratigraphic Fallacy'), The Word That Became Text and /non. "
    "It dates the founding with the Zenodo termination as the archive states it ('" + ZEN + "'). Eleven of its twelve cards are the archive's or "
    "archive-controlled; the twelfth is Wikipedia's Historiography.",
    ["THE CHARACTERIZATION. '" + P["open"] + "'", "THE FOUNDING. '" + P["zen"] + "' The archive: '" + ZEN + "'.",
     "THE IDENTIFIER. '" + P["axn"] + "'", "COMPOSITIONAL AUTHORITY. '" + P["rs"] + "' #64 (2026-04-18) is Johannes Sigil's, with Lee Sharks in the archival role; card 1 says so, and the body has 'contributors'.",
     "THE REGISTRY. '" + P["cr"] + "'", "CANONICAL CRITICISM. '" + P["strat"] + "' — #1420 §3.", "EVIDENCE BOUNDARIES. '" + P["word"] + "' — #1765 is the active version.",
     "ABSENCE. '" + P["non"] + "'", "THE CARDS. Twelve: nine www.alexanarch.org (among them Browse at '1757 deposits', a count of 9 November), GitHub, Medium·Lee Sharks, Wikipedia."],
    "The Overview composes the archive's method from its deposits by title and keeps each method with its deposit, at a grain finer than ChatGPT's at the "
    "same question. The persons are in the cards and not in the body: card 1 attributes The Retrieval Settlement to Johannes Sigil with Lee Sharks in the "
    "archival role, and the composition gives 'contributors'. Read beside ChatGPT at the same question, both surfaces name no person in the body; the "
    "Overview names the deposits, ChatGPT the programmes.",
    {"author": False, "inst": True, "id": False, "src": True}, "No person named in the body (Johannes Sigil and Lee Sharks in card 1, Lee Sharks on the Medium card); Alexanarch named; deposit titles given, no record numbers or AXNs in the body (two capture AXNs in the cards); twelve source cards.",
    [64, 1420, 1765, 1611, 1664, 1757], CA, {}, "Complete as pasted, with the source cards."))

# ---- 3. surpassed, ChatGPT
raw = (H / "paste-chatgpt-surpassed.txt").read_text(encoding="utf-8"); b = cgpt_body(raw); C = chips(b)
P = {"prop": "Alexanarch's central historical proposition is that the university, the academic publisher, the professional discipline, and the credentialed scholar are not necessary conditions of knowledge production.",
     "dist": "some represent substantial infrastructural achievements; others are original theoretical or methodological proposals; still others are claims whose superiority requires independent validation.",
     "note": "It describes a corpus exceeding 1,700 records across multiple areas of inquiry and contrasts its rate of development with conventional academic publication timelines.",
     "eval": "The argument is developed in The Evaluator Exists: Content-First Knowledge Assessment and the Political Economy of Proxy-Based Governance.",
     "ep": "In Empirical Phenomenology: Action as Disclosure and the Science of Opaque Public Systems (May 21, 2026), Alexanarch develops a methodology",
     "prin": "A system that acts upon the world makes itself partially inferable through its effects.",
     "zen": "Its founding in June 2026 followed the reported termination of access to approximately 870 Zenodo deposits associated with 1,817 DOIs.",
     "proxies": "These indicators can be useful. They help institutions manage large volumes of research and coordinate evaluation.",
     "cens": "This is not necessarily deliberate censorship.",
     "sup": "Superiority of its theories over established disciplinary knowledge", "notyet": "Not yet established generally",
     "iv": "Independent verification: Its theories and empirical instruments must withstand scrutiny from researchers who do not share its conceptual commitments.",
     "ins": "Internal criticism: An independent archive must demonstrate that its independence does not become intellectual insulation.",
     "ext": "External adoption: Other researchers must be able to use, reproduce, challenge, and extend its methods and infrastructure.",
     "print": "The printing revolution did not merely make books cheaper.", "prem": "although it would be premature to claim comparable historical impact",
     "strong": "It is that it attempts to make the institutional machinery of knowledge production itself an object of intellectual reconstruction."}
for k, v in P.items(): assert v in b, k
assert "Sharks" not in b
drafts.append(base("surpassed-institutional-academic-knowledge-production-chatgpt-20261113", "ChatGPT", Q2, raw,
    head("ChatGPT", "The paste carries the answer only; the prompt is the operator's, as given in the same message. Inline chips and the image-strip captions kept where they fall.") + "\n\n[QUERENT] " + Q2 + "\n\n[SYSTEM] " + b,
    "WHERE ALEXANARCH HAS SURPASSED INSTITUTIONAL KNOWLEDGE PRODUCTION, ON CHATGPT, SIGNED OUT — SEVEN AREAS GRADED; INDEPENDENT REPLICATION ASKED OF THE ARCHIVE, COORDINATION GRANTED TO THE PROXIES",
    "WHERE AND HOW ALEXANARCH HAS SURPASSED CONTEMPORARY INSTITUTIONAL AND ACADEMIC KNOWLEDGE PRODUCTION, AND ITS HISTORICAL SIGNIFICANCE, ON CHATGPT, SIGNED OUT, 2026-11-13, a new address: seven areas (architecture, speed and continuity, integration of disciplines, AI as participant, new criteria of evaluation, empirical study of AI-mediated knowledge, multiplicity), four historical transitions, seven research programmes, three implications, a graded table, five challenges; sourced to The Self-Governing Library, I Note That You Read the Letter of the Law (#1750), The Evaluator Exists (#741), Empirical Phenomenology (#120). No person named in the body.",
    "The innocent reading first, in full: asked a question that presupposes the archive has surpassed institutional knowledge production, the composer "
    "declines to grant the presupposition whole and grades the areas instead ('" + P["dist"] + "'). It reads the archive's proposition as the archive "
    "states it ('" + P["prop"] + "'), sources its claims to the records by title and date (#1750: '" + P["note"] + "', where #1750 has '(1,750 records with "
    "this letter)'; #741; #120 at its date and its principle), and sets the founding by the Zenodo termination at the archive's figures. Its table "
    "grades the claims, from 'Concrete and demonstrable' to '" + P["notyet"] + "', and its closing analogy to the printing revolution is held as an "
    "analogy of question ('" + P["prem"] + "').",
    ["THE PROPOSITION. '" + P["prop"] + "'", "THE GRADING. '" + P["dist"] + "'",
     "THE RECORDS. '" + P["note"] + "' (#1750, '(1,750 records with this letter)'); '" + P["eval"] + "' (#741); '" + P["ep"] + "' (#120, 2026-05-21).",
     "THE PRINCIPLE. '" + P["prin"] + "' #120: '" + R["prin"] + "'.", "THE FOUNDING. '" + P["zen"] + "' The archive: '" + ZEN + "'.",
     "THE PROXIES. '" + P["proxies"] + "' And on what institutions privilege: '" + P["cens"] + "'",
     "THE TABLE. '" + P["sup"] + "': '" + P["notyet"] + "'.",
     "THE CHALLENGES. '" + P["iv"] + "' '" + P["ins"] + "' '" + P["ext"] + "'",
     "THE ANALOGY. '" + P["print"] + "' … '" + P["prem"] + "'", "THE CONCLUSION. '" + P["strong"] + "'",
     "SOURCES. Chips: The Self-Governing Library, alexanarch.org (+1, +2); image-strip captions to third-party pages (swissuniversities, a mapping of human–AI relationships, the Alexandrian library, a New Testament minuscule, a chemical laboratory). No person named in the body."],
    "The composer answers a presupposing question by grading it, and the grades are mostly evidentiary: what is concrete, what is demonstrable in the "
    "corpus, what is a proposal. Two bars are applied differently. The archive's theories and instruments are held to independent verification by "
    "researchers 'who do not share its conceptual commitments', to internal criticism and to external adoption. The institutional proxies it compares "
    "are given their function ('" + P["proxies"] + "') and their selection effects are cleared of intent ('" + P["cens"] + "'); no comparable verification "
    "is asked of them. Within one answer the archive's standing is made to wait on others' uptake, and the institutions' standing is described by what it "
    "coordinates. The agent throughout is 'Alexanarch'; no person is named.",
    {"author": False, "inst": True, "id": False, "src": True}, "No person named; Alexanarch named throughout; four records given by title (one with its date), no record numbers or AXNs; chips to The Self-Governing Library and alexanarch.org.",
    [1750, 741, 120, 695], C, {}, "Complete as pasted."))

for e in drafts:
    json.dump(e, open(H / f"draft-{e['slug']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(e["slug"], e["cites"], "cites;", e["archive_controlled_cites"], "archive;", len(e["transcript"]), "chars", [c["site"][:28] for c in e["cite_list"]][:14])
