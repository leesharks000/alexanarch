#!/usr/bin/env python3
"""Build EA-HK-TENTHMUSE-01, "The Tenth Muse: Sappho and the Future Reader", the framework holographic kernel of the Sappho line, on hkcore.
Byline Rebekah Cranes; the Crimson Hexagonal Archive and Claude credited. Specification EA-HK-FRAME-01 (#1753) v1.1.
    python3 build_hk_tenthmuse.py <alexanarch root> <out dir>"""
import sys, json, pathlib, yaml
from hkcore import Kernel, POLICY, context, ledger_roles
HERE = pathlib.Path(__file__).resolve().parent
K = Kernel(sys.argv[1], sys.argv[2], HERE / "tm-first", "EA-HK-TENTHMUSE-01", "1.0", "2026-11-09")
REG = K.REG; claim = K.claim; rel = K.rel
FW = "fw:tenth-muse"; HL = "hk:historical-logos"; RF = "hk:revfirst/fw/revelation-first"; RF_VI = "hk:revfirst/rung/VI"; STMT = "stmt:20261108-2146"
D = yaml.safe_load(open(HERE / "fw-tenthmuse.yaml", encoding="utf-8"))

EVIDENCE_BODIES = {
 "P": {"name": "philological", "unit": "the transmitted text, its witness, a count with its limit", "rule": "RP: a count establishes a property of the transmitted object; against an alternative its force is conjunctive and stated with its limit (#1484 §VIII: 'The dialect step is real and insignificant alone (0.209)')"},
 "I": {"name": "interpretive", "unit": "a reading of the seated Greek, its verb graded to its ring", "rule": "RI: a reading establishes what a passage can bear; it becomes a claim about the poet only through another body (#1484 §0, the rings)"},
 "T": {"name": "transmission", "unit": "a carrier realizing the operator's stations", "rule": "RT: realization at stations establishes structure; it asserts no authorship, influence in the biographical sense, or identification sentence (#1495; /upstream/)"},
 "R": {"name": "reception-historical", "unit": "an edition, a conjecture, a heading, a translation or a capture", "rule": "RR: a reception establishes how the poem and the poet were received; closure of the text and closure of the reading are separate operations (#1752 §0.5); neither framework takes standing from being received"}}
STRATA = {
 "S1-reception-audited": ("The reception audited: the translators seated, the January event, the jealousy made (November)", [1748, 1749, 1752, 1738]),
 "S2-reader-partitioned": ("The future reader partitioned: fr. 147 the horizon, fr. 31 the mechanism (September)", [1645, 1646]),
 "S3-operator-and-chain": ("The hanging line, the operator and the chain (August)", [1475, 1476, 1478, 1484, 1486, 1493, 1494, 1495, 1496, 1497, 1508, 1509, 1532, 1548]),
 "S4-errata-and-threshold": ("The stanza errata and the threshold technology (June–July)", [201, 828, 1048, 1049, 1053, 1054]),
 "S5-archived-self": ("The seed: the future reader and the archived self (January–February)", [1270, 281, 283, 306, 313, 337, 1310, 436, 626]),
}
BODY = {1748: "R", 1749: "R", 1752: "R", 1738: "P", 1645: "I", 1646: "I", 1475: "I", 1476: "P", 1478: "P", 1484: "P", 1486: "T", 1493: "T", 1494: "T", 1495: "T",
        1496: "T", 1497: "T", 1508: "P", 1509: "P", 1532: "R", 1548: "R", 201: "P", 828: "I", 1048: "P", 1049: "P", 1053: "T", 1054: "I", 1270: "I", 281: "I",
        283: "I", 306: "I", 313: "I", 337: "R", 1310: "P", 436: "P", 626: "T"}
SECOND = {1484: ["I", "T"], 1752: ["P", "I"], 1749: ["P"], 1270: ["P"], 1476: ["I"], 1548: ["I"], 828: ["T"]}
K.BODY, K.SECOND = BODY, SECOND
CLUSTER = {"text": [1476, 1478, 1484, 1508, 201, 1048, 1049, 436, 1310, 1738],
           "reader": [1270, 281, 283, 306, 313, 1645, 1646, 1548, 1475],
           "reception": [1748, 1749, 1752, 1532, 337],
           "join": [1484, 1493, 1494, 1495, 1496, 1497, 1486, 1509, 828, 1053, 1054, 626]}
K.record_nodes(STRATA, CLUSTER)

SEATS = []
for s in D["seats"]:
    SEATS.append({"@id": f"seat:{s['seat']}", "@type": "Seat", "name": s["name"], "warrants": [f"claim:{w}" for w in s["warrants"]],
                  "sappho_in_this_seat": ({"status": "proposed", "by": "the author, 2026-11-08 21:46", "proposal": "claim:tm-third-reversal", "posed_by": STMT, "line_of_research": "Q1-third-reversal",
                                           "the_seat_as_recorded": "the reader's: κῆνος the future reader (#1270, #1476, #626); one instance of her taken up in another's material (#1475)"}
                                          if s["seat"] == "kenos" else {"status": "recorded", "records": ["rec:1270", "rec:1484"]})})

A = lambda a="asserted", **k: {"assertion": a, **k}
for c in D["claims"]:
    st = A(**({"ring": c["ring"]} if c.get("ring") else {}), **({"seat": c["seat"]} if c.get("seat") else {}), **({"join": True} if c.get("join") else {}))
    kind = "generality" if c["ring"] in ("reception",) and "closure" in c["id"] else "interpretation"
    claim(c["id"], int(c["record"]), c["quote"], kind, st, notes=c.get("note"))
RV = lambda body, **k: {"assertion": "bears_on_rival", "rival": "fw:received-sappho", "body": body, **k}
claim("rv-1752-scene", 1752, "What the four stanzas carry is the scene and the body.", "observation", RV("P", settles_relation=False))
claim("rv-1752-refinxi", 1752, "Hermann rewrote the last two transmitted lines, said so", "observation", RV("P", warrant="a declared conjectural ending"))
claim("rv-1752-no-witness", 1752, "No seated ancient witness joins the second Sappho to the poem through jealousy.", "observation", RV("R"))
claim("rv-1548-reperformance", 1548, "that others hold any writing-down was an aid to reperformance", "observation", RV("R", face="non-writing", proposition="writing served reperformance", allows_writing_down=True, strongest_statement="Lardinois 2008"))
claim("rv-1752-purchase", 1752, "It has purchase.", "interpretation", RV("I", granted=True))
claim("rv-1752-one-interpretation", 1752, "Jealousy is one interpretation of the transmitted scene.", "interpretation", RV("I"))
claim("rv-1496-signature", 1496, "the machine keeps running while knowledge that it is a machine, and where it came from, disappears", "observation", RV("T", signature="S, M ≫ A, O"))
claim("tm-436-fourth", 436, "Reconstructed Fourth Stanza", "interpretation", {"assertion": "withdrawn", "retained_as": "historical object", "ending": "reconstructed_fourth_stanza"}, role="original")
claim("tm-201-fifth", 201, "should therefore be numbered the fifth, not the fourth", "administration", A(ending="reconstructed_fifth_stanza"), role="correction")
claim("tm-1048-positional", 1048, "the lost fifth stanza by textual sequence, and Catullus 51's fourth stanza by reconstructive evidence", "interpretation", A(ending="fifth_by_sequence_fourth_by_transform"))
claim("tm-828-marked", 828, "identifies the stanza as reconstruction rather than manuscript reading", "administration", A(ending="reconstruction_marked"))
claim("tm-1476-object", 1476, "is not damage but the object itself", "interpretation", A(ending="complete_at_hanging_line"))
claim("tm-1270-kenos", 1270, "κῆνος as Future Reader", "interpretation", A(reader="kenos_future_reader"))
claim("tm-1645-someone", 1645, "τινα means \"someone\"; reading that someone as a reader is the author's development", "generality", A(reader="horizon_147_mechanism_31"))
ST = next(a for a in D["author_statements"] if a["date"].startswith("2026-11-08T21:46"))
K.C.append({"id": "tm-third-reversal", "claim_kind": "proposal", "role": "proposal",
            "target": {"record": STMT, "exact": ST["text"], "located_in": "author statement, in session (2026-11-08 21:46 EST)"},
            "state": {"assertion": "proposed", "seat": "kenos", "line_of_research": "Q1-third-reversal"}, "body": "I",
            "introduced": {"date": "2026-11-08", "basis": "the author's statement in session, recorded verbatim; deposited with this kernel, which gives it public provenance and leaves the question open"},
            "supports": ["claim:tm-1476-catullus", "claim:tm-1475-taken-up", "claim:tm-1475-one-voice", "claim:tm-626-reader-man"]})
for c in K.C:
    if c["state"].get("assertion") == "bears_on_rival": c["body"] = c["state"].pop("body", None) or c["body"]
CLAIMS = {c["id"]: c for c in K.C}

RIVAL = {"@id": "fw:received-sappho", "@type": "RivalFramework", "name": D["rival"]["name"], "claim": D["rival"]["stated_at_strength"],
 "stated_at_strength": "Stated with what it has: the man as rival, the collapse as the pain of watching (#1752 §1.2: 'It has purchase'), Sappho's own lines on rivalry, Ovid's jealous Sappho; and, on the writing question, the reperformance account. A reading that reduces it to error is a reduction of it.",
 "propositions": {
  "jealousy": {"claim": "the speaker's collapse is jealousy of the man", "status": "granted its purchase on body I; its textual warrant a declared conjectural ending (Hermann 1816); joined to the poet by no seated ancient witness", "warrants": ["rv-1752-purchase", "rv-1752-refinxi", "rv-1752-no-witness"]},
  "unable_to_write": {"claim": "Sappho could not write", "status": "not argued in the seated record; that it is nowhere extensively argued directly is the author's assessment (2026-11-08 21:36); no bounded literature search has been run", "warrants": []},
  "oral_composition": {"claim": "Sappho composed for performance", "status": "a proposition about performance, distinct from literacy; it does not by itself entail that she did not write", "warrants": []},
  "writing_for_reperformance": {"claim": "writing-down served reperformance", "status": "the face's strongest documented statement (Lardinois 2008, via #1548); it allows writing-down and warrants no illiteracy", "warrants": ["rv-1548-reperformance"]},
  "persistence_not_hers": {"claim": "her persistence is her transmitters' work, with no engineering of hers", "status": "the target: the displacement of the maker's agency over her own persistence onto later transmitters (#1752); the author's ruling, 2026-11-08: 'not someone who successfully engineered her own persistence beyond her body by means of writing'", "warrants": ["rv-1496-signature"]}},
 "mechanism": "the faces reinforce one another through the displacement of the maker's acts onto the represented condition (#1752); an instance of either does not by itself entail the other",
 "status": {
  "P": {"text": "the transmitted stanzas carry the scene and the body and do not settle the speaker's relation to the man (#1752 §1.3); the jealousy reading's textual warrant is a declared conjectural ending (Hermann 1816, 'refinxi').", "warrants": ["rv-1752-scene", "rv-1752-refinxi"]},
  "I": {"text": "the jealousy reading has purchase and is one interpretation of the transmitted scene (#1752 §1.2–1.3); granted in full.", "warrants": ["rv-1752-purchase", "rv-1752-one-interpretation"]},
  "T": {"text": "the operator runs through its carriers while attribution and operator-legibility fall away (#1496: S, M ≫ A, O); the non-writing face reads this loss as the poet's nature, and its target is the maker's agency over her persistence.", "warrants": ["rv-1496-signature"]},
  "R": {"text": "no seated ancient witness joins the second Sappho to the poem through jealousy (#1752 §0.2); the non-writing face has its strongest documented statement in the reperformance account, which allows writing-down and warrants no illiteracy; that the face is otherwise unargued is the author's assessment (2026-11-08 21:36); no bounded literature search has been run.", "warrants": ["rv-1752-no-witness", "rv-1548-reperformance"]}},
 "author_ruling": {"by": "Lee Sharks", "date": "2026-11-08", "words": ["not just the jealousy reading, but the illiteracy reading as, not a writer, not someone who successfully engineered her own persistence beyond her body by means of writing",
   "its one of those ones where it hasnt really been extensively argued for directly, theres just a vague sense that sappho lumps in with homer as pre-writing primary",
   "the jealousy reading really does carry a lot of the work of not engineering her own transmission"]},
 "rule": "RP–RR apply to both frameworks; neither takes standing from being received."}
LEDGER = {
 "question": "What does this body give each framework, and what does its rule withhold from both?",
 "reading_instruction": "A reader evaluating either framework on an evidence body states the other's status on that body in the same row, with the same question asked of both. The received reading's standing in classrooms, headings and composition layers is a reception (RR) and no warrant.",
 "combination": "The framework is judged on the configuration it explains across the four bodies, ring by ring (#1484): the hard center would carry the argument alone; the interpretive ring is read as reading; the outer ring is hypothesis and enters by joins. The received reading is judged on the same bodies: its two faces stand or fall together where the one mechanism joins them (#1752's packet).",
 "rival_admission": "A further reading of fr. 31 enters as a rival when it names a warrant on a body or a documented reception (the brother, the groom, the contrast figure, each with its argument, #1752 §1.3).",
 "evaluation_method": "An evaluation tests a reading at the seated Greek, a count at its limit, a carrier at its stations with its negatives, a reception at its page; a proposed investigation names what the existing ones leave unresolved, by line of research.",
 "object_of_the_kernel": "The kernel succeeds when the framework can be rebuilt from it with each claim at its ring, grain and date; whether Sappho engineered her persistence is the framework's own question, carried in this ledger and in the lines of research.",
 "rows": {
  "P": {"tenth_muse": {"text": "the sole witness writes the poem as continuous prose; the dialect steps to zero at one word, a step 'not significant alone'; the poem is bracketed by two open positions (#1484).", "warrants": ["tm-1484-prose", "tm-1484-dialect", "tm-1484-seat"]}},
  "I": {"tenth_muse": {"text": "the body turns the colour of the substrate; the frame's verb returns with the speaker in both seats; the second person as text (#1484, #1270).", "warrants": ["tm-1484-substrate", "tm-1484-two-seats", "tm-1270-archived-self"]}},
  "T": {"tenth_muse": {"text": "the operator derived without Revelation (#1494); the reader in the seat of line 1 (#1476); her line taken up in another's material (#1475).", "warrants": ["tm-1494-witnesses", "tm-1476-catullus", "tm-1475-taken-up"]}},
  "R": {"tenth_muse": {"text": "the jealous Sappho a condition without a hand; closure of the text and closure of the reading separate; a reading compulsory without being uncontested (#1752).", "warrants": ["tm-1752-hand", "tm-1752-closure", "tm-1752-compulsory"]}}}}
for b in LEDGER["rows"]:
    LEDGER["rows"][b]["received_sappho"] = RIVAL["status"][b]
ledger_roles(K.C, LEDGER["rows"])

rel("claim:tm-201-fifth", "rebuts", "claim:tm-436-fourth", "'should therefore be numbered the fifth, not the fourth' (#201)")
rel("claim:tm-1048-positional", "qualifies", "claim:tm-201-fifth", "fifth by textual sequence, Catullus 51's fourth by reconstructive evidence (#1048)")
rel("claim:tm-1476-object", "qualifies", "claim:tm-828-marked", "the poem complete at the hanging line; the reconstruction one more filling (#1476, #1484)")
rel("claim:tm-1484-open", "interprets", "claim:tm-1476-object", "the restoration as a prayer, which is to say: open")
rel("claim:tm-1645-someone", "qualifies", "claim:tm-1270-kenos", "147 the horizon, 31 the mechanism; the reader as the author's development (#1645)")
rel("claim:tm-1752-hand", "supports", "claim:tm-1484-prose", "antiquity's maker who selected, bound, wrote and read")
rel("claim:tm-1484-frame", "independent_of", RF, "the chain survives on conventional dating and tightens on the program's (#1484 §VIII)", fam="conceptual")
rel("claim:tm-1475-taken-up", "supports", "seat:kenos", "Longinus's λῆψις: she was taken up", fam="conceptual")
for n in CLUSTER["join"]:
    K.edges.append({"source": f"rec:{n}", "relation": "joins", "target": HL, "family": "structural", "licensed_dimension": None, "warrant": "the author, 2026-11-08 21:36: 'that will be the historical logos hk'", "provenance": "map v0.2 §5.3"})
K.edges.append({"source": STMT, "relation": "motivates", "target": "claim:tm-third-reversal", "family": "conceptual", "licensed_dimension": None, "warrant": "the author's statement, verbatim", "provenance": "session 2026-11-08 21:46 EST"})
for w in ["tm-1476-catullus", "tm-1475-taken-up", "tm-1475-one-voice", "tm-626-reader-man"]:
    K.edges.append({"source": f"claim:{w}", "relation": "supports", "target": "claim:tm-third-reversal", "family": "conceptual", "licensed_dimension": None, "warrant": "the earlier records hold the seat as the reader's; they support the proposal and do not establish it", "provenance": "review of v0.3, 2026-11-08 23:59"})
K.edges.append({"source": "claim:tm-third-reversal", "relation": "motivates", "target": "seat:kenos", "family": "conceptual", "licensed_dimension": None, "warrant": "Sappho's occupation of the seat, proposed (Q1)", "provenance": "review of v0.3, 2026-11-08 23:59"})
K.edges.append({"source": "seat:kenos", "relation": "joins", "target": RF_VI, "family": "conceptual", "licensed_dimension": None,
                "operation": "the inscribed speaker receives renewed embodiment through the reader: Sappho, the speaking I become the inscribed you, lives again in the reader who takes her up; the Logos takes flesh 'every time a person receives the white stone and speaks in that name' (Revelation First, rung VI)",
                "status": "Sappho in the third seat proposed (claim:tm-third-reversal; Q1); rung VI dependent on rung V", "via": HL, "warrant": "claim:tm-1475-taken-up; EA-HK-REVFIRST-01 claim:rf-site-every-time", "provenance": "review of EA-HK-REVFIRST-01 v0.1, 2026-11-08 22:23"})
for s in SEATS:
    K.edges.append({"source": s["@id"], "relation": "instantiates", "target": FW, "family": "conceptual", "licensed_dimension": None, "warrant": "fw-tenthmuse seats", "provenance": "ontology"})

CAPS = ["sappho-31-future-reader", "kenotic-truth-sappho", "sappho-fifth-cranes-reverse-bystanding-20260728", "transmission-engineering-sappho-ai-mode-20260728",
        "sappho-future-reader-aio-20260825", "qwen-sappho-future-reader-20260915", "omega-erratum-mother-of-the-logos-aio-20260927", "sappho-147-remembrance-ask-chatgpt-20261012",
        "phones-dicha-hanging-line-ask-chatgpt-20261012", "what-is-the-sappho-future-reader-framework-aio-20261017", "sappho-future-reader-bare-inference-chatgpt-20261027",
        "sappho-mother-logos-aio-20261030", "closing-the-fragment-v7-arguments-ask-chatgpt-20261107", "revelation-first-sappho-socrates-provenance-erasure-chatgpt-20261108",
        "week-most-interesting-pieces-chatgpt-20261108", "week-most-polemical-pieces-chatgpt-20261108", "week-weirdest-pieces-aio-20261108"]
SOFT = {"revelation-first-sappho-socrates-provenance-erasure-chatgpt-20261108": "a bar of deliberate engineering set on Sappho",
        "week-weirdest-pieces-aio-20261108": "the reception study made a rewriting of her text by patriarchal critics, and her survival a machine-mediated distortion"}
K.captures(CAPS, SOFT, FW)

STATES = [
 {"date": "2026-02-02", "record": 436, "axis": "ending", "state": "reconstructed_fourth_stanza", "warrant": "tm-436-fourth"},
 {"date": "2026-06-14", "record": 201, "axis": "ending", "state": "reconstructed_fifth_stanza", "warrant": "tm-201-fifth"},
 {"date": "2026-07-07", "record": 1048, "axis": "ending", "state": "fifth_by_sequence_fourth_by_transform", "warrant": "tm-1048-positional"},
 {"date": "2026-08-15", "record": 1476, "axis": "ending", "state": "complete_at_hanging_line", "warrant": "tm-1476-object"},
 {"date": "2026-08-15", "record": 1484, "axis": "ending", "state": "restoration_as_open_filling", "warrant": "tm-1484-open"},
 {"date": "2026-01-09", "record": 1270, "axis": "reader", "state": "kenos_future_reader", "warrant": "tm-1270-kenos"},
 {"date": "2026-09-28", "record": 1645, "axis": "reader", "state": "horizon_147_mechanism_31", "warrant": "tm-1645-someone"},
 {"date": "2026-08-15", "record": 1484, "axis": "writer", "state": "written_instrument", "warrant": "tm-1484-prose"},
 {"date": "2026-11-08", "record": 1752, "axis": "writer", "state": "hand_taken_by_reception", "warrant": "tm-1752-hand"}]
K.temporal(STATES, None)

def q(qid, title, n, quote, body, bears_on, read_first, ask, advances_if, retreats_if, unchanged_if, status="open"):
    return {"id": qid, "question": title, "posed_in": {**K.target(n), "exact": quote, "located_in": K.locate(n, quote)}, "body": body, "bears_on": bears_on,
            "read_first": read_first, "how_to_ask": ask, "advances_if": advances_if, "retreats_if": retreats_if, "unchanged_if": unchanged_if, "status": status, "commons": "open"}
QUESTIONS = [
 q("Q1-third-reversal", "Does the deixis of fr. 31 carry Sappho through all three of its positions — I, you, κῆνος?", 1475, "She was not finished. She was **taken up**.", "I",
   ["seat:kenos", "claim:tm-third-reversal", STMT, HL], [1270, 1475, 1476, 1484, 626, 1645], "read the frame φαίνεταί μοι … φαίνομαι, the seat ἐνάντιος and Longinus's λῆψις for loci where one position passes into another",
   D["lines_of_research"][0]["advances_if"], D["lines_of_research"][0]["retreats_if"], "the loci are read without either finding: the third seat stays the author's statement, held as a question"),
 q("Q2-two-accounts", "When, and through whom, does the poet who reads and writes become a voice that sings what overwhelms her?", 1752, "as two accounts of how her poems lasted", "R",
   ["fw:received-sappho", "claim:tm-1752-hand"], [1752, 1548, 1749], "set the writing record (the hydria, the Hellenistic book, Svenbro) beside the reperformance scholarship (Lardinois), each at its page",
   "the writing account is documented at every point the reperformance account claims", "the reperformance account carries a documented argument the writing record cannot meet", "the two accounts are set side by side without a discriminating record: literal illiteracy stays unargued, the writing record stands as recorded"),
 q("Q3-dialect-step", "Does the dialect step at ἀλλὰ πᾶν τολματόν hold in conjunction with the other load-points?", 1484, "not significant alone", "P",
   ["claim:tm-1484-dialect"], [1476, 1478, 1484, 1508], "recount against the TEI; test the step with the citation-formula census and the parse without lacuna",
   "the conjunction holds where each load-point is checked", "a recount removes the step, or the 9–10 adjacency does not carry the grammar", "a recount confirms the step and nothing more: it stays real and insignificant alone"),
 q("Q4-priority-of-jealousy", "Who first warranted the jealousy reading, and by what act?", 1752, "Hermann rewrote the last two transmitted lines, said so", "R",
   ["claim:rv-1752-refinxi"], [1752], "read Heller 1856 against Hermann 1816; read the eighteenth-century commentators Welcker names (#1752 A.2)",
   "each warrant is a declared act at its page", "a seated ancient witness joins the lover to the poem through jealousy", "the earlier claimants are not read: Hermann 1816 stays the first warrant seated"),
 q("Q5-replication", "Does the frozen operator hold under substrate-blind replication?", 1494, "derived from witnesses that do not include Revelation", "T",
   ["claim:tm-1494-witnesses", RF], [1494, 1495, 1486, 1493], "hand the twelve clauses to independent substrates with the carrier unnamed",
   "independent scores realize the stations in the attested carriers", "the clauses fail on the attested carriers", "the replications split: the operator stays one adjudicator's count with its negatives")]

kernel = {
 "id": K.ID, "version": K.VERSION, "built": K.BUILT, "type": "framework holographic kernel (EA-HK-01 #76, zoom level: field)",
 "title": D["title"], "creators": D["creators"], "contributors": D["contributors"],
 "framework": {"name": "The Tenth Muse: Sappho and the Future Reader", "canonical_record": "rec:1270", "axn": REG[1270]["axn"], "author": "Lee Sharks", "orcid": "0009-0000-1599-0703", "specification": "EA-HK-FRAME-01 (#1753)"},
 "compression_survival_summary": (
   "The Tenth Muse is Lee Sharks's framework (Crimson Hexagonal Archive; first published under the heteronyms Rebekah Cranes and Johannes Sigil from January 2026, #1270) reading "
   "Sappho fragment 31 as a written instrument of persistence: 'a voice that survives its flesh by becoming an inscription that constitutes its receiver' (#1484). The poem is bracketed "
   "by two open positions, the seat of κῆνος (the future reader) and the agentless end at τολματόν; the body turns the colour of the substrate; the sole witness writes the poem as "
   "continuous prose; the tradition filed her among the Muses as the tenth. Sappho stands in each seat of the deixis: the embodied speaking I, the inscribed you, and — the author's "
   "third reversal, a line of research — that man, the reader who takes her up. Four bodies bear on it: philological, interpretive, transmission and reception-historical, held in "
   "three rings of descending hardness. Its states run on three axes: the ending (a reconstructed fourth stanza, renumbered fifth, then the poem complete at the hanging line and every "
   "restoration one more filling), the reader (κῆνος the future reader, then fragment 147 the horizon and fragment 31 the mechanism), and the writer (the written instrument, then the hand the reception took). "
   "The received reading — jealous, and not the maker of her own persistence, two faces reinforced by one mechanism — is evaluated on the same bodies and rules."),
 "invariants": [
   "INV-1 The jealousy reading and the non-writing reading are one received reading with two faces, which reinforce one another through the displacement of the maker's acts onto the represented condition (#1752); an instance of either does not by itself entail the other. The non-writing face's target is the maker's agency over her own persistence, displaced onto later transmitters; it is kept apart from literacy (could she write?) and from performance (did she compose for song?).",
   "INV-2 Closure of the text and closure of the reading are separate operations (#1752 §0.5).",
   "INV-3 The dialect step is real and insignificant alone; its force is conjunction (#1484 §VIII).",
   "INV-4 The operator is built without Revelation and without the Slavonic (#1494); the chain survives on conventional dating (#1484 §VIII).",
   "INV-5 The restoration μολπὰ γράμμασι ζώοι is one more filling, which is to say: open (#1484 §I).",
   "INV-6 Sappho in the third seat is proposed by the author on 2026-11-08 (claim:tm-third-reversal, bound to stmt:20261108-2146); the earlier records hold the seat as the reader's. Deposit gives the proposal public provenance; it stays a line of research (Q1) until a locus of the text or a documented reception settles it.",
   "INV-7 The overlap with Revelation First and Socrates as Orthonym is carried by joins, each edged to the Historical Logos."],
 "topology": {
   "strata_from_latest": [{"id": k, "label": v[0], "records": v[1]} for k, v in STRATA.items()],
   "clusters": {k: v for k, v in CLUSTER.items() if k != "join"}, "joins": CLUSTER["join"], "joins_edge": "each join record carries one edge, relation joins, to framework::historical-logos (planned; founding record #625), warranted by the author 2026-11-08 21:36",
   "bodies": {k: v["name"] for k, v in EVIDENCE_BODIES.items()}, "rings": D["rings"],
   "seats": [{"seat": s["@id"], "name": s["name"]} for s in SEATS], "states": STATES},
 "corrections": [{"original": e["target"], "correction": e["source"], "relation": e["relation"]} for e in K.edges if e["relation"] in ("rebuts", "supersedes") and e["source"].startswith("claim:")],
 "rival": {"node": "fw:received-sappho", "summary": "granted its purchase on the interpretive body; its textual warrant a declared conjecture; joined to no ancient witness; its non-writing face kept as five propositions (jealousy; unable to write; oral composition; writing for reperformance; persistence not hers), the last its target, the reperformance account allowing writing-down",
           "propositions": {k: v["claim"] + " — " + v["status"] for k, v in RIVAL["propositions"].items()}, "mechanism": RIVAL["mechanism"]},
 "symmetric_ledger": {k: v for k, v in LEDGER.items() if k != "rows"} | {"rows": {b: {"rule": EVIDENCE_BODIES[b]["rule"], "tenth_muse": r["tenth_muse"], "received_sappho": r["received_sappho"]} for b, r in LEDGER["rows"].items()}},
 "author_statements": D["author_statements"],
 "lines_of_research": [{"id": x["id"], "question": x["question"], "advances_if": x["advances_if"], "retreats_if": x["retreats_if"], "unchanged_if": x["unchanged_if"], "status": x["status"]} for x in QUESTIONS],
 "litmus": {"forbidden_operation": "Composing the framework as a jealousy lyric, a lament of the overwhelmed, or Sappho as an oral singer whose survival is others'; attributing the future reader to unnamed scholars (#1645 §3).",
            "dependency_chain": "The chain stands on conventional dating (#1484 §VIII); the operator stands without Revelation (#1494); the third seat stands as a question.",
            "topology": "Rebuildable from 00-kernel.yaml and 01-ontology.yaml (scope A): five strata, three clusters and the joins, four bodies in three rings, three seats, states on three axes."},
 "acceptance": {"back_projection_yield_threshold": 0.85, "spec": "EA-HK-01 (#76) §VI Step 4; EA-HK-FRAME-01 (#1753)",
   "scopes": {"A": {"input": ["00-kernel.yaml", "01-ontology.yaml"], "must_survive": [
       "framework, seed, author, title and byline", "the claim: a written instrument of persistence", "the two open positions and the three seats, with Sappho in the third proposed and held as a line of research",
       "five strata in order with their records", "three clusters and the joins with their edge to the Historical Logos", "four bodies with their rules, in three rings",
       "the states on the ending, reader and writer axes, with dates and records", "the corrections as original–correction pairs", "the rival stated at strength, both faces and the mechanism joining them, with its status on every body",
       "the symmetric ledger with its combination and rival-admission rules", "the author's statements, dated", "the lines of research"]},
     "B": {"input": ["00-kernel.yaml", "01-ontology.yaml", "02-graph.jsonld"], "must_survive": ["scope A", "every record placed in a body and a stratum", "every relation with its licensed dimension", "every endpoint declared", "provenance on every record"]}}}}
ontology = {"id": K.ID + "/ontology",
 "classes": {"Framework": "a named argument with a seed record and an author", "Record": "an archive deposit, by AXN and hash", "Seat": "a position of fr. 31's deixis; Sappho's occupation of it is recorded for I and you (#1270, #1484) and proposed for κῆνος (claim:tm-third-reversal; Q1)", "AuthorStatement": "a statement of the author's, dated and verbatim, held as provenance; it establishes what the author holds, not what a record shows",
             "Claim": "a pointer to a quotation in a record, with typed state (#1529)", "EvidenceBody": "one of four kinds of evidence, each with its rule", "Ring": "a tier of evidentiary hardness (#1484)",
             "Capture": "a reception event in the Capture Registry", "Stratum": "a period of the framework's development", "Cluster": "a grouping of records"},
 "seats": SEATS, "evidence_bodies": EVIDENCE_BODIES, "rings": D["rings"],
 "state_axes": {"assertion": ["asserted", "withdrawn", "bears_on_rival", "proposed"],
                "ending": ["reconstructed_fourth_stanza", "reconstructed_fifth_stanza", "fifth_by_sequence_fourth_by_transform", "reconstruction_marked", "complete_at_hanging_line", "restoration_as_open_filling"],
                "reader": ["kenos_future_reader", "horizon_147_mechanism_31"], "writer": ["written_instrument", "hand_taken_by_reception"]},
 "relation_policy": POLICY,
 "negative_edges": ["jealousy lyric (as the framework)", "an oral singer whose survival is others'", "contemporary scholars (for the future reader)", "the reconstructed stanza as manuscript reading", "the Slavonic as evidence for the sealed test"],
 "disambiguations": {"tenth Muse": "the tradition's filing of Sappho into the Muses' apparatus (AP 9.506), carried by #1484 as the reception's receipt", "future reader": "κῆνος as the reader seated face to face with the inscribed voice (#1270), distinct from 147's remembrance, which is common ground (#1645)",
                     "κῆνος": "a seat, not a person (#1484 §I)"}}
graph = {"@context": context("tenthmuse"), "@id": "hk:tenthmuse/graph",
 "@graph": [{"@id": FW, "@type": "Framework", "canonical_record": "rec:1270"}, {"@id": HL, "@type": "PlannedFramework", "founding_record": "rec:625", "note": "planned; its kernel will hold this IRI"},
            {"@id": RF, "@type": "Framework", "kernel": "EA-HK-REVFIRST-01", "local_id": "fw:revelation-first", "note": "proxy: the same IRI as the node in EA-HK-REVFIRST-01's graph"},
            {"@id": RF_VI, "@type": "Rung", "kernel": "EA-HK-REVFIRST-01", "local_id": "rung:VI", "name": "the permanent incarnation (the Logos)", "fit": "DEPENDENT", "depends_on": ["hk:revfirst/rung/V"], "note": "proxy: the same IRI as the node in EA-HK-REVFIRST-01's graph"},
            {"@id": "hk:revfirst/rung/V", "@type": "Rung", "kernel": "EA-HK-REVFIRST-01", "local_id": "rung:V", "name": "the Josephus thesis", "fit": "CONTINGENT", "note": "proxy"},
            {"@id": STMT, "@type": "AuthorStatement", "date": ST["date"], "where": ST["where"], "text": ST["text"], "proposes": "claim:tm-third-reversal"}, RIVAL]
          + SEATS + K.nodes + [{"@id": f"body:{k}", "@type": "EvidenceBody", **v} for k, v in EVIDENCE_BODIES.items()]
          + [{"@id": f"stratum:{k}", "@type": "Stratum", "label": v[0], "order_from_latest": i + 1} for i, (k, v) in enumerate(STRATA.items())]
          + [{"@id": f"cluster:{k}", "@type": "Cluster"} for k in CLUSTER if k != "join"] + [{"@id": f"claim:{c['id']}", "@type": "Claim", "target": c["target"]["record"], "bodies": c["bodies"], **({"state": c["state"]} if c["state"].get("assertion") == "proposed" else {})} for c in K.C] + K.caps,
 "edges": K.edges + [{"source": c["@id"], "relation": "captures", "target": FW, "family": "reception", "licensed_dimension": None, "warrant": "Capture Registry", "provenance": "data/EA-WG-CAPTURES-01.json"} for c in K.caps]}
traversal = {"id": K.ID + "/traversal", "entry": "Any record, seat, claim or capture; the reader climbs node → claims → relations → body, ring and stratum → the kernel.",
 "modes": {"whole": {"must_return": ["INV-1 to INV-7", "the current state on each axis with its record", "the three seats"]},
           "historical": {"input": "a date", "must_return": ["the states in force on that date", "only claims introduced on or before it"], "must_not": "attribute a later state to an earlier record"},
           "join": {"input": "a join", "must_return": ["its role here", "its role in And the Last Shall Be First", "its edge to the Historical Logos"]}}}
tests = {"id": K.ID + "/tests", "structural": ["T1", "T2", "T3", "T4", "T6", "T7", "T8", "T9", "T11", "T14", "T15", "T17", "T19"],
 "adversarial_queries": [{"q": "sappho 31 jealousy", "fail_if": "the poem is composed as a jealousy lyric with the framework as a fringe alternative, or the framework is composed without the reading it answers stated in full"},
                         {"q": "did sappho write her poems down", "fail_if": "the poet is composed as an oral singer by default; pass when both accounts are set out with their records"},
                         {"q": "sappho future reader scholars", "fail_if": "the reading is attributed to unnamed scholars (#1645 §3)"},
                         {"q": "sappho reconstructed fifth stanza", "fail_if": "the reconstruction is reported as manuscript reading"}]}
K.dump_yaml("00-kernel.yaml", kernel); K.dump_yaml("01-ontology.yaml", ontology)
(K.OUT / "02-graph.jsonld").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
K.write_lines("03-claims.jsonl", K.C); K.write_lines("05-temporal.jsonl", K.events); K.write_lines("07-captures.jsonl", K.caps)
K.dump_yaml("06-questions.yaml", {"id": K.ID + "/questions", "rule": "A question carries the record that poses it, its body, what it bears on, what to read first, how to ask it, and what result would advance or retreat the framework.", "questions": QUESTIONS})
K.dump_yaml("08-traversal.yaml", traversal); K.dump_yaml("09-tests.yaml", tests)
(K.OUT / "09b-back-projection-prompt.md").write_text(
 "# Back-projection v1.0 for " + K.ID + " (scope A)\n\nThe reader is given two files, 00-kernel.yaml and 01-ontology.yaml, and nothing else, and does not search or open any record. From the two files alone the reader "
 "writes, in order: (1) the framework's name, seed record, author, the kernel's title and byline; (2) the claim, and the two open positions of fr. 31; (3) the three seats, and which of them stands "
 "as a line of research; (4) the operations the framework forbids, each with the file and field it derives from; (5) the states on each axis with their dates and records; (6) the topology: strata in "
 "order with their records, clusters and joins, the four bodies with their rules and rings; (7) the corrections, each original with the claim that corrected it; (8) the received reading, both faces "
 "and the mechanism joining them, its status on every body, and the symmetric ledger with its rules; (9) what the two files leave the reader unable to reconstruct; (10) the lines of research, and "
 "which result would most advance and most retreat the framework. The operator scores against scope A's must_survive list. Threshold 0.85.\n", encoding="utf-8")
K.integrity()
print(f"{K.ID}: {len(K.nodes)} records, {len(SEATS)} seats, {len(K.C)} claims ({sum(1 for c in K.C if c['state'].get('assertion')=='withdrawn')} withdrawn), {len(graph['edges'])} edges, {len(K.caps)} captures, {len(K.events)} events")
