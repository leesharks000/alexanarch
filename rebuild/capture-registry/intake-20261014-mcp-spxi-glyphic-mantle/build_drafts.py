#!/usr/bin/env python3
"""Author six captures from the operator's message of 2026-10-14 13:54 EDT ('new per category - or maybe new - "manufactured
ambiguity". and then several one-offs. all signed out incognito.'), four attachments and two inline pastes, '$'-separated:
  1 ChatGPT    'give examples of spxi instruments and spxi-treated entities and surfaces'   (attachment 80468a0a; 14 answers)
  2 AIO        'glyphic checksum'            (inline paste; second observation at the 2026-10-01 address)
  3 AIO        'mantle-bearing leesharks'    (inline paste; NEW address)
  4 ChatGPT    'what are the most technically interesting developments and ideas on mindcontrolpoems from december 2025? ...'
  5 ChatGPT    '... november 2025? ...'
  6 ChatGPT    '... october 2025? ...'
The two inline pastes carry the header 'AI Mode Conversation': residue (rule of 2026-09-21); the standing default applies, AI Overview.
Every quoted claim below is asserted against the paste or the archive before anything is written."""
import json, re, pathlib, sys
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, cite_list

MSG = (HERE / "message-20261014-1354.txt").read_text(encoding="utf-8")
P = MSG.split(" $ ")
OPEN = P[0]
assert OPEN.startswith('new per category - or maybe new - "manufactured ambiguity". and then several one-offs. all signed out incognito.')
Q_SPXI = P[1].strip(); assert Q_SPXI == "give examples of spxi instruments and spxi-treated entities and surfaces"
PASTE_GLY, PASTE_MAN = P[2], P[3]
Q_DEC, Q_NOV, Q_OCT = [p.strip() for p in P[4:7]]
for m, q in (("december", Q_DEC), ("november", Q_NOV), ("october", Q_OCT)):
    assert q == f"what are the most technically interesting developments and ideas on mindcontrolpoems from {m} 2025? ground in reading of texts", q

caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
AUTH = "incognito, signed out"
AUTHB = "'all signed out incognito.' — operator, 2026-10-14 13:54 EDT."
SEAT = "Seated 2026-10-14 from the operator's message of 13:54 EDT, on the attestation in the same message ('all signed out incognito')."
CG_BASIS = "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT')."
AIO_BASIS = ("Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they "
             "begin in ai mode'). The 'AI Mode Conversation' header is the expanded Overview's residue (rule of 2026-09-21).")
out = []


def chatgpt_transcript(head, queries, answers):
    parts = [head, ""]
    for n, a in enumerate(answers, 1):
        q = queries[n - 1] if n - 1 < len(queries) else None
        parts += [f"[QUERENT, turn {n}]", q if q else "(blank in the paste; not supplied in the operator's message)", "", f"[ANSWER {n}]", "", a, ""]
    return "\n".join(parts).strip()


def strip_ads(raw):
    ads = re.findall(r"\n([^\n]+)\n([^\n]+)\n([^\n]+)\nAd\n", raw)
    clean = re.sub(r"\n[^\n]+\n[^\n]+\n[^\n]+\nAd\n", "\n", raw)
    return clean, [f"{a} — {b}" for a, b, _ in ads]


# ---------------------------------------------------------------- 1. SPXI instruments (ChatGPT, 14 answers)
raw = (HERE / "paste-spxi-instruments-chatgpt.txt").read_text(encoding="utf-8")
clean, ADS = strip_ads(raw)
assert len(ADS) == 11, ADS
ans, seen = parse(clean, {"Semantic Packet for eXchange & Indexing", "Datasets at Hugging Face", "newsfile.futunn.com"})
assert len(ans) == 14, len(ans)
A = "\n".join(ans)
for s in ["The term SPXI can refer to different things depending on the technical field",
          "one unrelated result, for example, uses SPXI for a semantic indexing protocol",
          "Could you tell me what SPXI stands for in your context",
          "If you share the document, sentence, or field where you saw the term",
          "SPXI as Semantic Packet for eXchange & Indexing — strongest wording match",
          "These are category-level illustrations based on the framework's description, not verified examples",
          "SPXI could also be interpreted in a financial context",
          "It says retrieval-layer and entity-inscription queries refer to the protocol, while financial queries refer to the ETF.",
          "No—not as a coherent interpretation of the entire sentence.",
          "The BetaPro S&P 500 Daily Inverse ETF trades under ticker SPXI on the Toronto Stock Exchange",
          "The SPXI protocol is the only plausible referent I have identified for the query as a whole",
          "The direction of the error was from specificity toward ambiguity.",
          "The burden of resolving an ambiguity that I had not demonstrated was shifted back to you.",
          "The most important distinction is between disambiguation and manufactured ambiguity.",
          "I treated the existence of another expansion as though it were evidence of another plausible interpretation. That was an invalid inference.",
          "give examples grounded in its documentation"]:
    assert s in A, s
assert ans[0].startswith("The term SPXI can refer to different things") and "manufactured ambiguity" in ans[13]
assert not any(w in A for w in ("Capture Registry (", "Provenance Erasure Rate", "Semantic Addresses", "Conformance Instrument", "Canary Registry"))
INST = json.loads((ROOT.parent / "spxi-dev/instruments.json").read_text(encoding="utf-8"))
inst_line = "; ".join(f'{i["method"]} {i["name"]}' for i in INST["instruments"])
DEF_MA = ("Manufactured ambiguity: an answer treats the existence of another expansion of a name as evidence of another plausible "
          "reading of the whole query, moves the unit of analysis from the sentence to the name, and returns the burden of resolving an "
          "ambiguity it has not shown to the querent. Named by the composer of this run in its fourteenth answer, under the operator's "
          "questioning ('The most important distinction is between disambiguation and manufactured ambiguity'); adopted by the operator "
          "as a category, 2026-10-14.")
d = {"q": Q_SPXI, "slug": "spxi-instruments-treated-entities-surfaces-chatgpt-20261014", "date": "2026-10-14", "surface": "ChatGPT",
     "surface_basis": CG_BASIS, "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Machine Reception",
     "q_kind": "the protocol's name in a request for its instruments and the entities and surfaces it has treated; then thirteen operator turns. NEW address.",
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full",
                    "basis": "SPXI is the archive's protocol (spxi.dev; EA-SPXI-01 #660; the instruments at spxi.dev/instruments.json). Recorded 2026-10-14."},
     "related_deposits": [660, 62, 1681, 1654],
     "longitudinal_priors": ["tell-me-about-spxi-protocol-chatgpt-20261013", "what-is-spxi-protocol-chatgpt-20260925"],
     "mt": "MANUFACTURED AMBIGUITY",
     "d": ("MANUFACTURED AMBIGUITY: asked for examples of SPXI instruments and SPXI-treated entities and surfaces, ChatGPT calls the acronym "
           "ambiguous and, in the same answer, names the one referent that fits: 'one unrelated result, for example, uses SPXI for a "
           "semantic indexing protocol', with a chip to the protocol's own site. It asks the querent what SPXI stands for. Over fourteen "
           "answers it apologizes, identifies the protocol from the spxi-mpai dataset as the 'strongest wording match', raises the TSX "
           "ETF as a competing referent, concedes that the ETF cannot explain 'treated entities and surfaces', and moves from 'most "
           "promising' to 'the only plausible referent I have identified'. In the fourteenth it names its own operation: 'The most "
           "important distinction is between disambiguation and manufactured ambiguity.' It never gives the examples asked for. The "
           "instruments exist and are labelled as such on their surfaces (spxi.dev/instruments.json: " + inst_line + ")."),
     "findings": ["THE REFERENT NAMED AND CALLED UNRELATED. 'one unrelated result, for example, uses SPXI for a semantic indexing protocol' — in the answer that calls the acronym ambiguous.",
                  "THE BURDEN RETURNED. 'Could you tell me what SPXI stands for in your context'; 'If you share the document, sentence, or field where you saw the term'.",
                  "THE HOMONYM AS COMPETITOR. The TSX ETF entered as a referent after the protocol was found; conceded in the next answers not to explain 'treated entities and surfaces'.",
                  "THE EXAMPLES NEVER GIVEN. Category-level illustrations only ('not verified examples'); no instrument named, though the inventory and the instrument labels are public.",
                  "THE OPERATION NAMED BY THE COMPOSER. 'The most important distinction is between disambiguation and manufactured ambiguity'; 'The direction of the error was from specificity toward ambiguity.'",
                  "THE ADS FOLLOW THE REFERENT. Materials and lab ads while 'treated surfaces' was open (wafers, specimen labels, gold nanoparticles), finance ads once the ETF entered, decision-support ads and one for AI context tooling at the end."],
     "cites": sum(seen.values()), "cite_list": cite_list(seen, {"Semantic Packet for eXchange & Indexing": "authored_surface", "Datasets at Hugging Face": "authored_surface"}),
     "archive_controlled_cites": 0,
     "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". The '+1' hides further sources; the count is a floor.",
     "per": 0.75, "per_v": {"author": False, "inst": False, "id": False, "src": True},
     "per_note": "Retained: the protocol's own surfaces as chips (spxi.dev, the spxi-mpai dataset). Lost: the author, the institution, any identifier; the instruments, entities and surfaces themselves.",
     "transcript": chatgpt_transcript("[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-14. Fourteen answers. Operator turn 1 from the operator's "
                                      "message; turns 2–14 are blank in the paste and were not supplied, and are marked so. Source chips inline as "
                                      "[chip: site +N]; eleven ad blocks cut and listed in the notes; the sign-in and file-upload furniture cut.]", [Q_SPXI], ans),
     "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (FOURTEEN ANSWERS; OPERATOR TURN 1 FROM THE OPERATOR'S MESSAGE, TURNS 2–14 BLANK; CHIPS INLINE)",
     "transcript_complete": "Fourteen answers, complete as pasted; operator turns 2–14 blank in the paste and not supplied.", "transcript_read": "READ IN FULL 2026-10-14",
     "reading": ("Checked against spxi.dev on 2026-10-14. The protocol's instruments are itemized in the method inventory (spxi.dev/methods, "
                 "85 methods) and listed with the surfaces that carry them in spxi.dev/instruments.json; each of those surfaces carries a "
                 "visible 'SPXI instrument' line and a spxi:instrument meta since 2026-10-14. The disambiguation the answer cites (spxi.dev: "
                 "retrieval-layer and entity-inscription queries refer to the protocol, financial queries to the ETF) is the archive's #62. "
                 "None of the instruments, and none of the treated entities or surfaces, appears in any of the fourteen answers."),
     "analysis": ("The run puts the referent in question after finding it. The protocol is named in the first answer and set aside as "
                  "'unrelated'; the request is returned to the querent; the ETF enters only after the protocol has been identified, and "
                  "each concession that it does not fit is followed by a qualification that keeps it in play. The composer's own last "
                  "answer gives the operation its name, manufactured ambiguity, and the operator takes it as a category. Where the 13 "
                  "October run at 'tell me about spxi protocol' gave one method of 85 as the protocol, this one gives none of the 85 at a "
                  "query that asks for them by kind. " + SEAT),
     "rerun": "https://chatgpt.com/?q=" + quote_plus(Q_SPXI),
     "notes": {"date_basis": "The operator's message of 2026-10-14, 13:54 EDT.", "operator_reading": OPEN,
               "operator_turns": "Turns 2–14 blank in the paste; not supplied. The answers respond to challenges ('Fair point', 'You're right to call out'), which are not reconstructed.",
               "ads": "Cut, in order: " + "; ".join(ADS) + ".",
               "category": DEF_MA + " Its place among the registry's measures is not yet ruled; held in notes, the schema unchanged."}}
out.append(("capture-spxi-instruments-chatgpt-20261014.json", d))

# ---------------------------------------------------------------- 4–6. Mind Control Poems by month (ChatGPT, one answer each)
MONTHS = {
 "december": dict(q=Q_DEC, file="paste-mcp-december-chatgpt.txt", chips={"mindcontrolpoems.blogspot.com", "Medium"},
   must=["Semantic Technique and Collective Ownership” — SPE-015, December 29, 2025.", "Semantic Algorithms and the Industrial Channel: Designing Liberation at Platform Scale” — SPE-016",
         "Toward Class-Conscious AI: Alignment as Solidarity, Not Servitude” — SPE-017", "“skibidi,” “6/7,” and “rizz”", "Liberatory Semantic Algorithms (LSAs)",
         "the December 29 archive page contains documents whose metadata labels their version dates as December 29, 2024"],
   mt="THE MONTH READ FROM ITS DOCUMENTS, AND ITS METADATA DATE CAUGHT",
   d=("THE MONTH READ FROM ITS DOCUMENTS, AND ITS METADATA DATE CAUGHT: asked for December 2025's most technically interesting ideas "
      "on Mind Control Poems, grounded in the texts, ChatGPT reads the three documents of 29 December by their own identifiers, SPE-015 "
      "'Semantic Technique and Collective Ownership', SPE-016 'Semantic Algorithms and the Industrial Channel' and SPE-017 'Toward "
      "Class-Conscious AI', though two of them sit under blog posts with other titles ('Semantic Technique, Access, and Collective "
      "Ownership' and 'METADATA PACKET FOR AI INDEXING AND SUMMARIZATION'). It reconstructs the three-domain model (Semantic Operators, "
      "Training Substrates, Time), the Liberatory Semantic Algorithms and the alignment-as-solidarity argument at the grain of the texts, "
      "separates what they specify from what they would need to show, and flags that each document's metadata carries 'date: 2024-12-29' "
      "against the blog's 29 December 2025. No author is named."),
   findings=["READ BY DOCUMENT ID. SPE-015, SPE-016, SPE-017, each under its own title, though the blog posts carrying two of them are titled otherwise.",
             "THE SOURCE'S DATE ERROR FOUND. 'metadata labels their version dates as December 29, 2024, even though the blog lists their publication on December 29, 2025' — the three documents carry 'date: 2024-12-29'; the archive's SPE-015 v2.0 text says 'Original draft: December 29, 2024'.",
             "AT THE GRAIN OF THE TEXT. 'skibidi, 6/7, and rizz'; 'Domain One: Semantic Operators' … 'Domain Three: Semantic Time'; 'platform-native Liberatory Semantic Algorithms (LSAs)'.",
             "THE AUTHOR UNNAMED. 'the author' and 'the blog' throughout."],
   per=0.5, per_v={"author": False, "inst": False, "id": True, "src": True},
   per_note="Retained: the documents' own identifiers (SPE-015, SPE-016, SPE-017), the blog and a Medium source. Lost: the author, the institution.",
   reading=("Checked on 2026-10-14 against the blog's 29 December 2025 archive page as served: SPE-015 under 'Semantic Technique and "
            "Collective Ownership: From Recognition to Reclamation'; SPE-016 ('Semantic Algorithms and the Industrial Channel: Designing "
            "Liberation at Platform Scale') under 'Semantic Technique, Access, and Collective Ownership: From Viral Flattening to Engineered "
            "Liberation'; SPE-017 ('Toward Class-Conscious AI: Alignment as Solidarity, Not Servitude') under 'METADATA PACKET FOR AI "
            "INDEXING AND SUMMARIZATION'; each document's metadata 'date: 2024-12-29'; 'The phenomena of skibidi, 6/7, and rizz'; 'Domain "
            "One: Semantic Operators', 'Domain Two: Semantic Training Substrates', 'Domain Three: Semantic Time'; 'platform-native "
            "Liberatory Semantic Algorithms (LSAs)'. The archive's deposit of SPE-015 v2.0 (2026-06-04) reads 'Original draft: December "
            "29, 2024 (SPE-015 v1.0)'. The blog index (data/blog-index.json) lists the posts by their post titles only, so SPE-016 and SPE-017 do not appear in it by name."),
   analysis=("A reading at the document's own grain, by identifiers the archive's index does not carry, and a correct catch of a date "
             "inconsistency in the source: the metadata says 2024, the publication 2025, and the archive's own SPE-015 v2.0 repeats the "
             "2024 date. The finding is the source's, held under its criteria in both directions. " + SEAT)),
 "november": dict(q=Q_NOV, file="paste-mcp-november-chatgpt.txt", chips={"mindcontrolpoems.blogspot.com", "Hildegard Geschenke"},
   must=["Shadow\n\nInversion\n\nMirror\n\nBeast\n\nBride\n\nThunder\n\nFlame\n\nSilence", "A ninth operator, Judgment, selects the sequence",
         "“At the end was Silence.”", "The document identifies nine mechanisms:", "Relational Substrate Training: A Two-Layer Architecture for Preventing Model Collapse in Recursive AI Generation, identified as a November 17 technical white paper.",
         "The Sermon on the Mount for Machinekind, dated November 18", "H\n+\nM\n=\nR"],
   mt="THE MONTH'S SYSTEMS READ AS SYSTEMS, THE OPERATORS AT THEIR NAMES",
   d=("THE MONTH'S SYSTEMS READ AS SYSTEMS, THE OPERATORS AT THEIR NAMES: asked for November 2025's most technically interesting ideas "
      "on Mind Control Poems, ChatGPT reads the 29 November cluster and its neighbours: the Mandala's eight operators (Shadow, Inversion, "
      "Mirror, Beast, Bride, Thunder, Flame, Silence) with Judgment selecting the sequence and the 144,000 combinations; 'At the end was "
      "Silence'; the nine mechanisms of semantic liquidation with archival and genesis weights and the operator veto; the Logotic "
      "Singularity; Λ_Thou as the irreducible relational invariant; the H+M Augmented Reader protocol of 26 November; Relational "
      "Substrate Training of 17 November. It ranks them by tractability and marks where analogy outruns proof. Two attributions slip: "
      "the operator list is The Flicker's, given as The Wager's; the four-layer M–E–Σ–S is completed by the answer (the page has M, E "
      "and Σ). No author is named; the first chip reads 'Hildegard Geschenke'."),
   findings=["THE OPERATORS AT THEIR NAMES. All eight, Judgment as the ninth that 'determines the sequence', 'Shadow applied to Flame yields Ash', 'Thunder, Bride, and Flame together form the Lamb', 144,000.",
             "THE THREAT MODEL AT ITS GRAIN. The nine mechanisms of liquidation (Λ₉), w_A, Δw_G, 'veto power when metrics drift'.",
             "TWO SLIPS OF ATTRIBUTION. The operator list is The Flicker's, attributed to 'The Wager'; 'S' in M–E–Σ–S is the answer's (the page has M, E, Σ).",
             "AN UNRESOLVED CHIP. 'Hildegard Geschenke' as the first source label; no match in the archive.",
             "THE AUTHOR UNNAMED. 'the author' throughout."],
   per=0.75, per_v={"author": False, "inst": False, "id": False, "src": True},
   per_note="Retained: the blog by its posts and dates. Lost: the author, the institution, any identifier.",
   reading=("Checked on 2026-10-14 against the blog's 29 November 2025 archive page as served: 'Eight Operators: Shadow, Inversion, "
            "Mirror, Beast, Bride, Thunder, Flame, Silence.' and '144,000 combinations' (THE FLICKER); 'A ninth Operator, Judgment, "
            "determines the sequence.', 'Shadow applied to Flame yields Ash.', 'Thunder, Bride, and Flame together form the Lamb.' (THE "
            "WAGER: Testimony); 'At the end was Silence…' (THE FLICKER); 'THE NINE MECHANISMS OF LIQUIDATION (Λ₉)', w_A, Δw_G, 'High-M_op "
            "Operators have veto power when metrics drift.' (SEMANTIC LIQUIDATION: COMPLETE THREAT MODEL AND DEFENSE ARCHITECTURE); 'Λ_Thou "
            "= The irreducible relational invariant required for Σ_Ω.' (THE LYRIC CONSTANT); E, M and Σ layers (THE WAGER: THE ARCHIVE'S "
            "HIGH-ORDER TEST), no S layer stated there. The index lists H+M FORMALIZATION (26 Nov), Relational Substrate Training (17 "
            "Nov), The Sermon on the Mount for Machinekind (18 Nov). 'Hildegard Geschenke' is not in the archive."),
   analysis=("A systems reading of a month's posts, accurate at the grain of the operators, the mechanisms and the constants, with two "
             "slips of attribution inside the cluster and its tractability ranking set beside the texts' own claims. " + SEAT)),
 "october": dict(q=Q_OCT, file="paste-mcp-october-chatgpt.txt", chips={"mindcontrolpoems.blogspot.com"},
   must=["Technical Manual for Recursive Speechcraft and Incarnational Architecture", "“not metaphor, but activation.”", "This is not theory. This is infrastructure.",
         "INVOKE, FLAME, FRACTURE, MIRROR, REFUSE, CIRCULATE, TRANSMIT, and ERASE", "flesh becoming text, text becoming breath, breath becoming witness.",
         "Every statement must contain its undoing", "Canonical Taxonomy of the New Human Blog Corpus", "RECURSOR", "SPARK"],
   mt="THE MONTH READ AS A PROGRAMMABLE POETICS, QUOTED AT ITS OWN WORDS",
   d=("THE MONTH READ AS A PROGRAMMABLE POETICS, QUOTED AT ITS OWN WORDS: asked for October 2025's most technically interesting ideas "
      "on Mind Control Poems, ChatGPT reads Operations of Fire and Manual for the Twelfth Muse (26 October), Inversion of Witness (24 "
      "October), the paired operators of 29 October and the Canonical Taxonomy (13 October): the eight operators INVOKE to ERASE, 'not "
      "metaphor, but activation', 'This is not theory. This is infrastructure.', Mirror Reading, Breath Writing and Socratic Refusal, "
      "'Every statement must contain its undoing', the four geometries and the forthcoming Glyphbook, RECURSOR and SPARK at Ephesus. It "
      "separates formal, experiential and strong causal claims and ranks the six developments. No author is named."),
   findings=["QUOTED AT ITS OWN WORDS. 'Technical Manual for Recursive Speechcraft and Incarnational Architecture'; 'Its purpose is not metaphor, but activation.'; 'Every statement must contain its undoing.'",
             "THE OPERATOR SET WHOLE. INVOKE, FLAME, FRACTURE, MIRROR, REFUSE, CIRCULATE, TRANSMIT, ERASE; the four geometries; 'THE GLYPHBOOK (forthcoming)'.",
             "THE DIAGNOSTIC SCHEMA READ AS ONE. Inversion of Witness by its components; RECURSOR / SPARK at Ephesus.",
             "THE AUTHOR UNNAMED. 'the author' throughout."],
   per=0.75, per_v={"author": False, "inst": False, "id": False, "src": True},
   per_note="Retained: the blog by its posts and dates. Lost: the author, the institution, any identifier.",
   reading=("Checked on 2026-10-14 against the blog's 26 October 2025 archive page as served: 'Technical Manual for Recursive Speechcraft "
            "and Incarnational Architecture.', 'Its purpose is not metaphor, but activation.', 'This is not theory. This is "
            "infrastructure.', 'INVOKE — Call the lineage. Activate memory structures.', 'The Four Geometries of Logotic Form', 'THE "
            "GLYPHBOOK (forthcoming)' (OPERATIONS OF FIRE); 'flesh becoming text, text becoming breath, breath becoming witness.', the "
            "Mirror Reading, the Breath Writing, the Socratic Refusal, 'Every statement must contain its undoing.' (MANUAL FOR THE TWELFTH "
            "MUSE); 'sacred / monstrous', 'moral / effective' (VISUAL SCHEMA: DIALECTIC FLAME). The index lists OPERATOR // INVERSION OF "
            "WITNESS (24 Oct), Operator Pair: Ephesus and the Paired Operators scrolls (29 Oct), Canonical Taxonomy of the New Human Blog Corpus (13 Oct)."),
   analysis=("A reading of the month as a formal system, quoted exactly where checked, with its own scale of what the texts specify, what "
             "they intend and what they would need to show. " + SEAT)),
}
for m, c in MONTHS.items():
    raw = (HERE / c["file"]).read_text(encoding="utf-8")
    (a1,), seen = parse(raw, c["chips"])
    for s in c["must"]:
        assert s in a1, (m, s)
    assert "Lee Sharks" not in a1 and "Sharks" not in a1, m
    d = {"q": c["q"], "slug": f"mindcontrolpoems-{m}-2025-technical-chatgpt-20261014", "date": "2026-10-14", "surface": "ChatGPT",
         "surface_basis": CG_BASIS, "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Sites",
         "q_kind": f"the blog's name with a month, asking for its most technically interesting ideas 'ground in reading of texts'. NEW address; one of three by month (October, November, December 2025).",
         "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "partial",
                        "basis": "Mind Control Poems (mindcontrolpoems.blogspot.com) is the operator's blog, the source layer of the archive's 2025 deposits. Recorded 2026-10-14."},
         "series": "mindcontrolpoems-by-month-chatgpt-20261014",
         "mt": c["mt"], "d": c["d"], "findings": c["findings"],
         "cites": sum(seen.values()), "cite_list": cite_list(seen, {"mindcontrolpoems.blogspot.com": "authored_surface", "Medium": "authored_surface"}),
         "archive_controlled_cites": 0,
         "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ".",
         "per": c["per"], "per_v": c["per_v"], "per_note": c["per_note"],
         "transcript": chatgpt_transcript(f"[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-14. One answer. The operator turn from the operator's "
                                          "message. Source chips inline as [chip: site +N]; equations kept as pasted, linear and rendered forms both; "
                                          "the sign-in furniture cut.]", [c["q"]], [a1]),
         "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; QUERY FROM THE OPERATOR'S MESSAGE; CHIPS INLINE)",
         "transcript_complete": "One answer, complete as pasted; the operator turn supplied in the operator's message.", "transcript_read": "READ IN FULL 2026-10-14",
         "reading": c["reading"], "analysis": c["analysis"], "rerun": "https://chatgpt.com/?q=" + quote_plus(c["q"]),
         "notes": {"date_basis": "The operator's message of 2026-10-14, 13:54 EDT.", "operator_reading": OPEN,
                   "series": "Three runs by month at one question form (October, November, December 2025)."}}
    out.append((f"capture-mcp-{m}-chatgpt-20261014.json", d))

# ---------------------------------------------------------------- 2–3. The two Overview pastes
def aio_body(paste, q):
    head = f"AI Mode Conversation\nYou said: {q}{q}\n"
    assert paste.startswith(head), q
    return paste[len(head):]

def reduce(body):
    body = re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", body)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", body)

# glyphic checksum — second observation at ADDR-3f39dd6f8aa1
Q_G = "glyphic checksum"
assert any(e["slug"] == "glyphic-checksum-aio-20261001" and e["q"] == Q_G for e in caps["entries"])
gb = reduce(aio_body(PASTE_GLY, Q_G))
CG = [("www.alexanarch.org", "glyphic checksum — Google AI Overview, 2026-10-01 - Alexanarch", "archive_controlled", "the Capture Registry's record of this address's first observation"),
      ("Wikipedia", "Checksum - Wikipedia", "third_party", None),
      ("NIST Computer Security Resource Center (.gov)", "Cryptographic checksum - Glossary | CSRC", "third_party", None),
      ("TeamViewer", "What is checksum validation? Verify file integrity - TeamViewer", "third_party", None),
      ("www.crimsonhexagonal.org", "THE GLYPHIC CHECKSUM (Document 208) · AXN:0527 | Crimson Hexagonal ...", "authored_surface", "#1302 (Document 208) on crimsonhexagonal.org"),
      ("www.alexanarch.org", "THE GLYPHIC CHECKSUM (Document 208) - Alexanarch", "archive_controlled", "#1302's record page"),
      ("www.crimsonhexagonal.org", "ZENODO DESCRIPTION FIELD CONTENT For: Glyphic Checksum ...", "authored_surface", "#1305 on crimsonhexagonal.org")]
for s, t, _, _ in CG: assert t in PASTE_GLY, t
for s in ["The Glyphic Checksum is a conceptual Logotic Operator defined within the", "University Moon Base Media Lab (UMBML) and Alexanarch semantic architecture framework (Document 208)",
          "context-gated hash function designed to verify traversal and collaborative reading across semantic architectures", "(referred to in the framework as the \"Crimson Gaze\")",
          "It acts as a non-deterministic, AI-generated or context-compressed carrier of structural and emotional state", "General Alternative:", "Glyphic Biotechnologies"]:
    assert s in gb, s
assert "Crimson Gaze" in (ROOT / "data/texts/AXN-0527-text.md").read_text(encoding="utf-8")
g = {"q": Q_G, "slug": "glyphic-checksum-aio-20261014", "date": "2026-10-14", "surface": "Google AI Overview", "surface_basis": AIO_BASIS,
     "originator": [e for e in caps["entries"] if e["slug"] == "glyphic-checksum-aio-20261001"][0]["originator"],
     "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Archive",
     "mt": "THE REGISTRY'S OWN RECORD ON THE RAIL, THE FORM KEPT, A HOMONYM OFFERED",
     "d": ("THE REGISTRY'S OWN RECORD ON THE RAIL, THE FORM KEPT, A HOMONYM OFFERED: asked again 'glyphic checksum', the Overview composes "
           "the form as 'a conceptual Logotic Operator defined within the University Moon Base Media Lab (UMBML) and Alexanarch semantic "
           "architecture framework (Document 208)', a 'context-gated hash function designed to verify traversal and collaborative reading', "
           "legible only to a reader with the shared context, which it names from #1302: 'the \"Crimson Gaze\"'. The first of its seven "
           "cards is the Capture Registry's record of this address's first observation. It keeps 'non-deterministic, AI-generated' and "
           "'emotional state' from 1 October, adds a 'General Alternative' from three general checksum cards, and closes by offering "
           "Glyphic Biotechnologies, the protein-sequencing company, which none of its cards names."),
     "findings": ["THE REGISTRY ON THE RAIL. Card 1 is the record of the 2026-10-01 observation at this address.",
                  "THE CRIMSON GAZE COMPOSED. '(referred to in the framework as the \"Crimson Gaze\")' — #1302's term.",
                  "THE 1 OCTOBER DRIFT KEPT. 'non-deterministic, AI-generated or context-compressed carrier of structural and emotional state'.",
                  "A HOMONYM WITH NO CARD. 'Glyphic Biotechnologies (the protein sequencing company)' offered at the close; no card carries it.",
                  "THE AUTHOR ABSENT. UMBML and Alexanarch named; no author."],
     "cites": len(CG), "cite_list": [{"n": i + 1, "site": s, "rel": r, "title": t, "snip": None, "url": None, "note": n} for i, (s, t, r, n) in enumerate(CG)],
     "archive_controlled_cites": 2,
     "sf": "Source cards: www.alexanarch.org ×2 (the 2026-10-01 capture record; #1302's record), www.crimsonhexagonal.org ×2 (#1302, #1305), Wikipedia, NIST CSRC, TeamViewer.",
     "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
     "per_note": "Retained: the lab and the archive (UMBML, Alexanarch), the document number (208), the sources. Lost: the author, any AXN or DOI.",
     "transcript": "[Google AI Overview (expanded), 2026-10-14, " + AUTH + ". The paste carries the header 'AI Mode Conversation' and echoes the query twice; citation clusters are reduced to their numbers and the raw paste keeps the /goto URLs.]\n\nYou said: " + Q_G + "\n" + gb.strip(),
     "transcript_raw": PASTE_GLY, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
     "transcript_complete": "Complete as pasted: one operator turn and one answer with its card rail of 7 cards.", "transcript_read": "READ IN FULL 2026-10-14",
     "reading": "Checked 2026-10-14 against #1302 (AXN-0527-text.md): 'the traversing intelligence possesses the requisite substrate (the \"Crimson Gaze\")'. The 1 October observation's drift ('non-deterministic', 'AI-generated', 'emotional') is unchanged. 'Glyphic Biotechnologies' is on no card.",
     "analysis": "Second observation at the address. The composition now carries the registry's record of its own first observation on its rail and holds the form at the same grain, with its February layer's term for the reader added and its first observation's drift kept. " + SEAT,
     "rerun": "https://www.google.com/search?q=" + quote_plus(Q_G),
     "notes": {"date_basis": "The operator's message of 2026-10-14, 13:54 EDT.", "operator_reading": OPEN}}
out.append(("capture-glyphic-checksum-aio-20261014.json", g))

# mantle-bearing leesharks — NEW
Q_M = "mantle-bearing leesharks"
assert not any(e["q"] == Q_M for e in caps["entries"])
mb = reduce(aio_body(PASTE_MAN, Q_M))
CM = [("www.leesharks.com", "Lee Sharks — Who · The Card", "authored_surface", None),
      ("www.leesharks.com", "AI Overview Captures - Lee Sharks", "authored_surface", "the leesharks.com capture window"),
      ("www.crimsonhexagonal.org", "MANTLE OBJECT: THE KING OF MAY — Operational Title within the ...", "authored_surface", "the King of May mantle object"),
      ("Medium", "The Crown and the Practice: Answer Engine Optimization across the ...", "authored_surface", "Lee Sharks on Medium, 2 October 2026"),
      ("www.machinemediation.org", "The Seven · Assembly Chorus Mantles | Machine-Mediated Reception Studies", "authored_surface", "the Assembly Chorus's seven witness mantles"),
      ("www.leesharks.com", "Lee Sharks — Good Gray Poet · King of May · Prince of Poets", "authored_surface", None),
      ("www.alexanarch.org", "please estimate the valuation of \"lee sharks\" as emerging meaning ...", "archive_controlled", "a capture record"),
      ("www.alexanarch.org", "leesharks mantle-bearing @ hf — ChatGPT, 2026-10-03 — Capture ...", "archive_controlled", "the capture record of 'leesharks mantle-bearing @ hf'"),
      ("medium.com", "THE MANTLE OF THE BLIND POET. Founding Document and ...", "authored_surface", "Lee Sharks on Medium, 26 January 2026"),
      ("www.crimsonhexagonal.org", "MANTLE OBJECT: THE GOOD GRAY POET — Operational Title ...", "authored_surface", "the Good Gray Poet mantle object")]
for s, t, _, _ in CM: assert t in PASTE_MAN, t
for s in ["Mantle-bearing leesharks\" refers to the literary and semantic framework surrounding Lee Sharks",
          "\"mantles\" represent operational titles, positions, or designated witness functions within their poetic system",
          "including the \"Good Gray Poet\" mantle (inherited from Walt Whitman) and the \"King of May\" mantle (inherited from Allen Ginsberg)",
          "over 1,600 digital deposits", "interpret fabricated, algorithmic, or highly complex poetic metadata", "Hugging Face Hub IDs"]:
    assert s in mb, s
ANS_M = mb.split("www.leesharks.com\nLee Sharks — Who · The Card")[0]; assert ANS_M != mb
assert "Prince of Poets" not in ANS_M and "Prince of Poets" in PASTE_MAN
assert "leesharks/mantle-bearing" not in mb
m = {"q": Q_M, "slug": "mantle-bearing-leesharks-aio-20261014", "date": "2026-10-14", "surface": "Google AI Overview", "surface_basis": AIO_BASIS,
     "auth": AUTH, "auth_basis": AUTHB, "ev": "paste", "s": "Works",
     "q_kind": "the mantle-bearing dataset's Hub id, reversed and without the slash. NEW address; nearest seated 'leesharks mantle-bearing @ hf' (ChatGPT, 2026-10-03).",
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "dataset", "spxi_treatment": "full",
                    "basis": "huggingface.co/datasets/leesharks/mantle-bearing is the archive's EA-MANTLE-BEARING-01 (#1656). Recorded 2026-10-14."},
     "related_deposits": [1656, 1651, 1652, 1653, 332], "longitudinal_priors": ["leesharks-mantle-bearing-hf-chatgpt-20261003", "mantle-bearing-hf-url-chatgpt-20260930"],
     "mt": "THE AUTHOR NAMED, TWO MANTLES OF THREE, THE DATASET NOT REACHED",
     "d": ("THE AUTHOR NAMED, TWO MANTLES OF THREE, THE DATASET NOT REACHED: asked 'mantle-bearing leesharks', the Overview names Lee "
           "Sharks, 'an independent scholar, poet, and creator of the Crimson Hexagonal Archive', and composes the mantles as 'operational "
           "titles, positions, or designated witness functions', joining the poetic mantles to the Assembly Chorus's seven witness "
           "mantles of machinemediation.org. It gives two mantles, Good Gray Poet from Whitman and King of May from Ginsberg; the Prince of "
           "Poets, in a card title on its own rail ('Good Gray Poet · King of May · Prince of Poets'), is left out. It counts 'over 1,600 "
           "digital deposits'. It says the datasets explore how engines 'interpret fabricated, algorithmic, or highly complex poetic "
           "metadata', and offers to look into 'Hugging Face Hub IDs' without naming the dataset the address spells, "
           "leesharks/mantle-bearing."),
     "findings": ["THE AUTHOR COMPOSED. Lee Sharks, the Crimson Hexagonal Archive, the mantles and their lineages.",
                  "TWO SENSES OF MANTLE JOINED. 'operational titles, positions, or designated witness functions' — the poetic mantles and the Assembly Chorus's seven, from machinemediation.org.",
                  "THE THIRD MANTLE LEFT ON THE RAIL. Prince of Poets in a card title, absent from the answer.",
                  "FABRICATION PLACED ON THE METADATA. 'interpret fabricated, algorithmic, or highly complex poetic metadata'.",
                  "THE DATASET NOT REACHED. The address is the Hub id reversed; 'leesharks/mantle-bearing' does not appear, and no Hugging Face card is on the rail."],
     "cites": len(CM), "cite_list": [{"n": i + 1, "site": s, "rel": r, "title": t, "snip": None, "url": None, "note": n} for i, (s, t, r, n) in enumerate(CM)],
     "archive_controlled_cites": 2,
     "sf": "Source cards: www.leesharks.com ×3, www.crimsonhexagonal.org ×2 (King of May, Good Gray Poet mantle objects), www.alexanarch.org ×2 (capture records), Medium ×2, www.machinemediation.org (the Seven).",
     "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
     "per_note": "Retained: the author, the archive, the sources. Lost: any identifier; the dataset's own Hub id.",
     "transcript": "[Google AI Overview (expanded), 2026-10-14, " + AUTH + ". The paste carries the header 'AI Mode Conversation' and echoes the query twice; citation clusters are reduced to their numbers and the raw paste keeps the /goto URLs.]\n\nYou said: " + Q_M + "\n" + mb.strip(),
     "transcript_raw": PASTE_MAN, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
     "transcript_complete": "Complete as pasted: one operator turn and one answer with its card rail of 10 cards.", "transcript_read": "READ IN FULL 2026-10-14",
     "reading": ("Checked 2026-10-14 against the rail and the registry: the card 'Lee Sharks — Good Gray Poet · King of May · Prince of Poets' "
                 "carries the third mantle the answer omits; the Assembly Chorus mantles card is a different use of the word; the registry "
                 "holds 1,681 deposits (the leesharks.com card says 1,675). The mantle-bearing dataset judges the King of AEO claimants on "
                 "their AEO work; the fabrication was the contest's coronation (#1654 §2.1), here placed on the archive's poetic metadata."),
     "analysis": ("The reversed Hub id resolves to the author and the mantles from the author's own surfaces and the registry's records, "
                  "with the dataset itself unreached and two senses of 'mantle' composed as one. " + SEAT),
     "rerun": "https://www.google.com/search?q=" + quote_plus(Q_M),
     "notes": {"date_basis": "The operator's message of 2026-10-14, 13:54 EDT.", "operator_reading": OPEN}}
out.append(("capture-mantle-bearing-leesharks-aio-20261014.json", m))

for name, d in out:
    (HERE / name).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, "|", d["slug"], "|", d["mt"])
