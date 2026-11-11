#!/usr/bin/env python3
"""Build EA-HK-HISTLOGOS-01, "The Historical Logos", the framework holographic kernel of the overlap of the three strands (Sappho; Socrates–Plato–
Theophrastus–Aristotle; Revelation and the New Testament), on hkcore. Byline Johannes Sigil (the author, 2026-11-09 12:05); the Crimson Hexagonal
Archive and Claude credited. Central node #1484 (the author, 2026-11-09: "sappho mother of the logos is a closer central node"); founding records #625
and #626 at the front with their dated states. Specification EA-HK-FRAME-01 (#1753) v1.1; argument layer as in EA-HK-REVFIRST-01 v1.1.
    python3 build_hk_histlogos.py <alexanarch root> <out dir>"""
import sys, json, pathlib, yaml
from hkcore import Kernel, POLICY, context, ledger_roles
import args_layer
HERE = pathlib.Path(__file__).resolve().parent
K = Kernel(sys.argv[1], sys.argv[2], HERE / "hl-first", "EA-HK-HISTLOGOS-01", "0.1", "2026-11-09")
REG = K.REG; claim = K.claim; rel = K.rel
FW = "fw:historical-logos"; RIVAL_ID = "fw:current-consensus-genealogy"
TM_HL = "hk:historical-logos"                      # the IRI EA-HK-TENTHMUSE-01's joins point to
OR_FW, OR_MM = "hk:orthonym/fw/socrates-as-orthonym", "hk:orthonym/fw/many-maker"
RF_FW, RF_VI = "hk:revfirst/fw/revelation-first", "hk:revfirst/rung/VI"
TM_FW, TM_KENOS = "hk:tenthmuse/fw/tenth-muse", "hk:tenthmuse/seat/kenos"
D = yaml.safe_load(open(HERE / "fw-histlogos.yaml", encoding="utf-8"))
STM = {a["date"][:16]: a for a in D["author_statements"]}
sid = lambda d: "stmt:" + d[:10].replace("-", "") + "-" + d[11:16].replace(":", "")

# every move of every reader, by id: claims below are taken from them so each quotation is the reader-checked verbatim text
MOVES = {m["id"]: m for m in args_layer.all_moves()}
def mclaim(cid, mid, kind, state, notes=None, role="standing"):
    m = MOVES[mid]; claim(cid, m["record"], m["exact"], kind, state, notes=notes or f"argument move arg:{mid}", role=role)

EVIDENCE_BODIES = {
 "P": {"name": "philological", "unit": "the transmitted text, its witness, a count with its limit", "rule": "RP: a count establishes a property of the transmitted object; against an alternative its force is conjunctive and stated with its limit (#1484 §VIII)"},
 "I": {"name": "interpretive", "unit": "a reading of the seated text, its verb graded to its ring", "rule": "RI: a reading establishes what a passage can bear; it becomes a claim about a maker only through another body (#1484 §0; #1576: functional identity 'is established by pattern')"},
 "T": {"name": "transmission", "unit": "a carrier realizing the operator's stations, or a station of the chain", "rule": "RT: realization at stations establishes structure; it asserts no authorship, influence in the biographical sense, or identification sentence (#1495; #1494)"},
 "R": {"name": "reception-historical", "unit": "an edition, a filing, a heading, a translation or a capture", "rule": "RR: a reception establishes how a text and its maker were received; a filing is evidence of the filing (#1733: 'The frame was set by filing, before argument.'); neither framework takes standing from being received"},
 "B": {"name": "biographical", "unit": "an item outside the manuscripts attesting a person: an inscription, a document, a will held by an independent channel", "rule": "RB: biographical identity is established by evidence of a different kind (#1576), and the rule applies both ways (the author, 2026-11-09 12:05): evidence of that kind is largely unavailable to the four-maker reading as to the one-maker reading; where it exists here it attests one legal person, Aristotle (the Delphi stone, #1658), and the four wills reach the reader in one text (#1733)"}}
STRATA = {
 "S1-genealogy-contested": ("The genealogy contested and the erasures audited: the jealousy made, the count embrittled, Revelation's direction priced (November)", [1752, 1733, 1735]),
 "S2-divided-mind": ("Many and one; the divided mind and the socket in God (September–October)", [1576, 1658]),
 "S3-chain-stated": ("The chain stated once, its key, its errata and its operator (August)", [1484, 1458, 1474, 1475, 1476, 1477, 1478, 1486, 1494, 1495, 1496]),
 "S4-threshold-orthonym": ("The threshold technology, the orthonym, the white stone and the work plan (May–July)", [123, 752, 828, 202, 1217, 1053]),
 "S5-founding": ("The founding: the future reader, the vow, the lock, the prolegomena and the Word that became text (January–April)", [1270, 346, 897, 496, 625, 626]),
 "S6-method-and-settlement": ("The method of operational transmission and the settlement read as a date: the unfoldings, the frozen operators, the pre-registrations, the censuses and the stylometry; Counterfeit Orthodoxies (April–October; joined at v1.1)", [978, 674, 65, 1414, 1415, 1416, 1511, 1532, 1533, 1571, 1572, 1586, 1590, 1605, 1730]),
}
BODY = {1752: "R", 1733: "R", 1735: "P", 1576: "I", 1658: "I", 1484: "P", 1458: "I", 1474: "P", 1475: "I", 1476: "P", 1477: "T", 1478: "P", 1486: "T", 1494: "T",
        1495: "T", 1496: "T", 123: "I", 752: "R", 828: "T", 202: "R", 1217: "R", 1053: "T", 1270: "I", 346: "I", 897: "I", 496: "T", 625: "T", 626: "T",
        978: "R", 674: "R", 65: "R", 1414: "T", 1415: "T", 1416: "T", 1511: "T", 1532: "T", 1533: "T", 1571: "P", 1572: "P", 1586: "P", 1590: "R", 1605: "P", 1730: "P"}
SECOND = {1658: ["B", "P"], 1733: ["B", "P"], 1576: ["B", "P"], 123: ["B"], 1484: ["I", "T", "R"], 626: ["P", "R"], 1752: ["P"], 1735: ["R"], 828: ["P"], 1217: ["T"],
          978: ["I", "P"], 674: ["I"], 65: ["I"], 1532: ["R"], 1571: ["I"], 1572: ["I"], 1586: ["I"], 1590: ["P"], 1605: ["I"], 1730: ["R"]}
K.BODY, K.SECOND = BODY, SECOND
CLUSTER = {"instrument": [1270, 1475, 1476, 1478, 1474, 1484],
           "academy": [123, 346, 897, 752, 1576, 1658, 1733],
           "key_and_operator": [1458, 1486, 1494, 1495, 1496, 1053],
           "word_and_canon": [625, 626, 828, 202, 1217, 1735, 496, 1477],
           "erasure": [1752, 1733, 1496, 1474, 625, 626, 202, 1217, 1053],
           "method": [1414, 1415, 1416, 1511, 1532, 1486, 1494, 1495, 1533, 1571, 1496, 1572, 1586, 1590, 1605, 1730, 1733],
           "settlement": [978, 674, 65],
           "join": [1484, 123, 1576, 1658, 1733, 1735, 202, 1217, 1270, 1476, 1752, 828, 626]}
exec(open(HERE / "v12_pre.py", encoding="utf-8").read())   # v1.2 (2026-11-10)
K.record_nodes(STRATA, CLUSTER)

# ---------------------------------------------------------------- stations: #1484 §VII, extended by the author (2026-11-09 12:11, 12:15)
STATIONS = [
 ("sappho-31", "Sappho 31: the instrument", "the body decommissioned into substrate, the reader's seat cut at line 1, the doer's slot at line 17", [1270, 1475, 1476, 1478, 1474, 1484], "#1484 §VII"),
 ("orphic-tablets", "The Orphic tablets: the threshold", "inscription scripting the voice of the dead at the threshold", [828], "#1484 §VII"),
 ("academy", "Socrates–Plato–Theophrastus–Aristotle: the Academy's receipt and the self-dividing maker", "Plato receives the technology by name (Phaedrus 235c), files its founder into the Muses, converts it to doctrine through Diotima; the corpus divides one maker into positions, Socrates its broken tongue", [123, 346, 897, 752, 1576, 1658, 1733], "#1484 §VII; #1658; the author, 2026-11-09 12:05, 12:11"),
 ("philo", "Philo: the die made cosmology", "the Logos as the seal, creation as impression", [1486, 1496], "#1484 §VII"),
 ("peri-hypsous", "Peri Hypsous: the key", "the Lesbian and the Mosaic instances held in one hand as one ὕψος", [1458, 1474, 1475], "#1484 §VII"),
 ("catullus", "Catullus: the seat taken", "the open line answered by reversal, the reader's seat taken", [1476], "#1484 §VII"),
 ("josephus", "Josephus's seams: the Word in the historiographic record", "the same crux-structure at every joint, Greek and Slavonic", [626, 625], "#1484 §VII"),
 ("cosmic-christ", "The Apocalypse: the cosmic Christ, the socket sanctified", "the commanded book, the eaten scroll, the Word as name, the tamper-curse, the white stone", [1735, 202, 1495, 1494, 828], "#1484 §VII; the author, 2026-11-09 12:11 ('cosmic christ')"),
 ("gospel-christ", "The gospel Christ and the Johannine test", "the Word made flesh; the spirits sorted by word-conformity (ὁμολογεῖ) with the Logos formed in the body", [626, 828, 1217, 978], "the author, 2026-11-09 12:11 ('gospel christ'), 12:12, 12:15; #828; #1217; #978 (the Word's body the codex), joined at v1.1"),
 ("augustine", "Augustine: the method made portable", "thirteen books to an interlocutor whose reply is never transcribed, the broken tongue rotated to taste", [496, 1477], "#1484 §VII"),
 ("the-reader-now", "The modern restorations and the reader now", "each ending open, the latest an optative prayer: μολπὰ γράμμασι ζώοι; the composition layer as the present station", [1484, 1053, 1752], "#1484 §VII; the author, 2026-11-09 12:11 ('and outward from there')")]
SITES = [{"@id": f"site:{s}", "@type": "Station", "order": i + 1, "name": nm, "operation": op, "records": [f"rec:{n}" for n in rs], "named_by": by}
         for i, (s, nm, op, rs, by) in enumerate(STATIONS)]
LIVES = {"declared": "the author, 2026-11-09 12:11: 'sappho. socrates-plato-theophrastus-aristotle. cosmic christ. gospel christ. and so on, and outward from there'",
         "lives": [{"life": "Sappho", "station": "site:sappho-31"}, {"life": "Socrates–Plato–Theophrastus–Aristotle", "station": "site:academy"},
                   {"life": "the cosmic Christ", "station": "site:cosmic-christ"}, {"life": "the gospel Christ", "station": "site:gospel-christ"},
                   {"life": "and outward from there", "station": "site:the-reader-now"}],
         "status": "the lives as the author names them; their placement at stations is this kernel's, open to the author's ruling"}

A = lambda a="asserted", **k: {"assertion": a, **k}
# ---------------------------------------------------------------- the claim, owned (#1484), and the founding (#625, #626)
claim("hl-1484-logos", 1484, "a voice that survives its flesh by becoming an inscription that constitutes its receiver", "interpretation", A(ring="hard_center", genealogy="sappho_mother_of_the_logos"))
claim("hl-1484-mother", 1484, "Sappho is the mother of the Logos.", "interpretation", A(ring="interpretive"))
claim("hl-1484-before-doctrine", 1484, "That is the Logos, before doctrine: **the technology of a voice that constitutes its receiver.**", "interpretation", A(ring="interpretive"))
claim("hl-1484-key", 1484, "Longinus is the key.", "interpretation", A(ring="hard_center", station="peri-hypsous"))
claim("hl-1484-tiered", 1484, "Three rings, in descending evidentiary hardness", "administration", A())
claim("hl-1484-anti-erasure", 1484, "the technology's anti-erasure clause becomes a covenant curse", "interpretation", A(ring="outer", station="cosmic-christ", erasure="anti_erasure_clause_canonized"))
claim("hl-1484-standing-objection", 1484, "the first demand that the text's father come stand beside it", "interpretation", A(ring="interpretive", station="academy", erasure="the_father_demanded"))
claim("hl-1484-conventional", 1484, "the chain survives on conventional dating and tightens on the program's", "interpretation", A(ring="outer", join=True))
mclaim("hl-625-redirect", "a625-not-replace", "administration", A(genealogy="how_the_word_moved"))
mclaim("hl-625-programmatic", "a625-programmatic", "administration", A(state="programmatic_not_probative"))
mclaim("hl-625-first-cycle", "a625-first-cycle", "interpretation", A(station="josephus"))
mclaim("hl-625-apophatic", "a625-s-apophatic", "method", A(erasure="apophatic_stratum"))
mclaim("hl-626-reading", "a626-reading-claim", "interpretation", A(state="a_reading_protocol"))
mclaim("hl-626-protocol", "a626-protocol-not-recovery", "administration", A())
mclaim("hl-626-invisible", "a626-coherence-invisible", "interpretation", A(station="josephus", erasure="coherence_invisible_to_interpolation_scholarship"))
mclaim("hl-626-void", "a626-void", "interpretation", A(station="josephus"))
# ---------------------------------------------------------------- the spine: self-division as a transmission technology
mclaim("hl-1475-taken-up", "a1475-taken-up", "interpretation", A(station="sappho-31", seat="kenos"))
mclaim("hl-1475-first-rupture", "a1475-first-rupture", "interpretation", A(station="sappho-31", broken_tongue=True))
mclaim("hl-1475-one-operation", "a1475-one-operation", "interpretation", A(station="sappho-31"))
mclaim("hl-1458-circuit", "a1458-circuit", "interpretation", A(station="peri-hypsous"))
mclaim("hl-1458-vacated", "a1458-vacated", "interpretation", A(station="peri-hypsous"))
mclaim("hl-1478-no-fragment", "a1478-rule", "interpretation", A(station="sappho-31"))
mclaim("hl-1476-seat", "a1478-second-voice", "interpretation", A(station="catullus"))
mclaim("hl-1053-sappho-chain", "a1053-sappho-chain", "interpretation", A(station="the-reader-now"))
mclaim("hl-1658-one-cut", "a1658-one-cut", "interpretation", A(station="academy"))
mclaim("hl-1658-version-control", "a1658-version-control", "interpretation", A(station="academy"))
mclaim("hl-1658-coda", "a1658-coda", "interpretation", A(station="academy"))
mclaim("hl-1576-person-divided", "a1576-person-divided", "interpretation", A(station="academy"))
mclaim("hl-1576-voices-objects", "a1576-voices-objects", "interpretation", A(station="academy"))
mclaim("hl-123-refusal", "a123-refusal-op", "interpretation", A(station="academy"))
mclaim("hl-346-acts", "a346-acts-on-reality", "interpretation", A(station="academy"))
mclaim("hl-897-textual", "a897-textual", "interpretation", A(station="academy"))
mclaim("hl-752-structural", "a752-structural", "interpretation", A(station="academy", ring="interpretive"))
mclaim("hl-496-rotation", "a496-rotation", "interpretation", A(station="augustine"))
mclaim("hl-1477-generalized", "a1477-method-generalized", "interpretation", A(station="augustine"))
mclaim("hl-1486-established", "a1486-established", "observation", A(station="philo"))
mclaim("hl-1486-not-established", "a1486-not-established", "administration", A(station="philo"))
mclaim("hl-828-gramma", "a828-gramma-link", "interpretation", A(station="orphic-tablets"))
mclaim("hl-828-no-linear", "a828-no-linear", "administration", A(station="orphic-tablets"))
mclaim("hl-828-survives", "a828-survives-dating", "interpretation", A(station="cosmic-christ"))
claim("hl-828-homologei", 828, "The spirit that ὁμολογεῖ (word-conforms with) Jesus Christ *formed in the body* (ἐν σαρκὶ ἐληλυθότα) is from God.", "interpretation", A(station="gospel-christ", ring="outer"))
mclaim("hl-1217-homologei", "a1217-rung6-homologei", "interpretation", A(station="gospel-christ", ring="outer"))
mclaim("hl-1735-corpus", "a1735-corpus-finding", "observation", A(station="cosmic-christ"))
mclaim("hl-1735-statuses", "a1735-three-statuses", "administration", A(station="cosmic-christ"))
mclaim("hl-1494-without", "a1494-prior-excluded", "administration", A(station="cosmic-christ"))
mclaim("hl-1495-c6", "a1495-c6", "observation", A(station="cosmic-christ"))
# ---------------------------------------------------------------- the maker axis, dated
mclaim("hl-123-functional", "a123-functional", "interpretation", A(maker="functional_not_biographical"))
mclaim("hl-123-lifespan", "a123-v12", "administration", {"assertion": "held_as_state", "maker": "functional_not_biographical", "marked": "a projection from the many-author reading (the author, 2026-11-09 12:05)"},
       notes="argument move arg:a123-v12; the ninety-year figure, arg:a123-lifespan, is carried in the argument layer as #123's state")
mclaim("hl-1576-result", "a1576-result", "interpretation", A(maker="two_not_established_one_offered"))
mclaim("hl-1576-sequence", "a1576-sequence-not-count", "interpretation", A())
mclaim("hl-1576-null", "a1576-null", "observation", A())
mclaim("hl-1576-symmetric-null", "a1576-symmetric-null", "interpretation", A())
mclaim("hl-1576-matter-withdrawn", "a1576-matter-withdrawn", "interpretation", {"assertion": "withdrawn", "retained_as": "historical object", "what": "the earlier form of the argument: Λ 9 predicting the instruments' failures because they are addressed to matter"}, role="correction")
mclaim("hl-1576-not-adjudicated", "a1576-not-adjudicated", "administration", A())
mclaim("hl-1658-nothing-requires-two", "a1658-nothing-requires-two", "interpretation", A(maker="one_self_dividing_maker"))
mclaim("hl-1658-legal", "a1658-legal-identity", "interpretation", A(body_note="B"))
mclaim("hl-1658-ledger", "a1658-ledger-finding", "observation", A(body_note="B"))
mclaim("hl-1658-ledger-open", "a1658-ledger-open", "administration", A())
mclaim("hl-1658-preference", "a1658-preference", "interpretation", A())
mclaim("hl-1733-set-explains", "a1733-set-explains", "interpretation", A(maker="one_maker_reading_held"))
mclaim("hl-1733-wills", "a1733-wills-dependent", "interpretation", A(body_note="B"))
mclaim("hl-1733-not-decide", "a1733-not-decide", "administration", A())
mclaim("hl-1733-no-hoax", "a1733-no-hoax", "administration", A())
mclaim("hl-1733-set-by-filing", "a1733-set-by-filing", "interpretation", A(erasure="the_count_set_by_filing"))
mclaim("hl-1733-brittle", "a1733-brittle", "interpretation", A())
# ---------------------------------------------------------------- the erasure axis
mclaim("hl-1752-hand", "a1752-tenth-muse", "observation", A(erasure="the_hand_taken"), notes="argument move arg:a1752-tenth-muse")
claim("hl-1752-condition", 1752, "The jealous Sappho is a condition without a hand: a voice overwhelmed, where antiquity had a maker who selected, bound, wrote and read.", "interpretation", A(erasure="the_hand_taken"))
mclaim("hl-1496-signature", "a1496-signature", "observation", A(erasure="suppression_signature"))
mclaim("hl-1496-machine", "a1496-machine", "interpretation", A())
mclaim("hl-1496-crossing", "a1496-crossing", "interpretation", A())
mclaim("hl-1474-standardization", "a1474-err-1052", "observation", A(erasure="standardization"))
mclaim("hl-1053-anthology", "a1053-anthology-erasing", "observation", A(erasure="anthology_text"))
mclaim("hl-1458-age", "a1458-erasure-ch44", "observation", A(station="peri-hypsous"))
mclaim("hl-202-erasure", "a202-erasure-summary", "method", A(erasure="primary_claim_erasure"))
mclaim("hl-202-maintenance", "a202-not-conspiracy", "observation", A())
mclaim("hl-1217-autopsy", "a1217-autopsy", "method", A(erasure="provenance_erasure_measured"))
mclaim("hl-1217-per", "a1217-per-100", "observation", A())
mclaim("hl-1478-requirement", "a1478-regen", "interpretation", A())

# ---------------------------------------------------------------- the author's statements as claims (provenance; they establish what the author holds)
def stmt_claim(cid, key, state, supports=()):
    s = STM[key]
    K.C.append({"id": cid, "claim_kind": "author_position", "role": "statement", "target": {"record": sid(s["date"]), "exact": s["text"], "located_in": "author statement, in session (" + s["date"] + ")"},
                "state": state, "body": "B" if "maker" in state else "I", "introduced": {"date": s["date"][:10], "basis": "the author's statement in session, recorded verbatim; deposited with this kernel"},
                **({"supports": [f"claim:{x}" for x in supports]} if supports else {})})
stmt_claim("hl-stmt-one-person", "2026-11-08T20:00", {"assertion": "held_by_author", "maker": "one_biological_person"}, ["hl-1658-nothing-requires-two"])
stmt_claim("hl-stmt-both-readings", "2026-11-09T08:36", {"assertion": "author_assessment"})
stmt_claim("hl-stmt-one-person-q", "2026-11-09T08:39", {"assertion": "held_by_author", "maker": "one_person_dividing_into_many"})
stmt_claim("hl-stmt-started-one", "2026-11-09T08:41", {"assertion": "held_by_author", "maker": "started_one_made_many_by_editing"}, ["hl-1733-set-by-filing", "hl-1733-brittle"])
stmt_claim("hl-stmt-spine", "2026-11-09T10:07", {"assertion": "held_by_author", "spine": "self_division_as_transmission_technology"}, ["hl-1475-taken-up", "hl-1658-one-cut"])
stmt_claim("hl-stmt-biographical", "2026-11-09T12:05", {"assertion": "held_by_author", "maker": "biographical_reading_held", "evidence_rule": "both_ways", "lifespan": "projection_from_many_author_reading"}, ["hl-1658-legal", "hl-1658-ledger", "hl-1733-wills", "hl-1576-symmetric-null"])
stmt_claim("hl-stmt-genealogy", "2026-11-09T12:11", {"assertion": "held_by_author", "genealogy": "material_inscription_becoming_flesh_from_the_beginning", "erasure": "pressures_always_faced"}, ["hl-1484-logos", "hl-625-redirect", "hl-626-reading"])
stmt_claim("hl-stmt-his-own", "2026-11-09T12:12", {"assertion": "author_pointer", "erasure": "attested_inside_the_text"})
K.C.append({"id": "hl-stmt-sort-spirits", "claim_kind": "author_position", "role": "statement",
            "target": {"record": "stmt:20261109-1215", "exact": "that is what the epistle of john tells us, is that we can sort the spirits, by means of word conformity with the logos formed in the body.",
                       "located_in": "author statement, in session (2026-11-09T12:15-05:00)"},
            "state": {"assertion": "held_by_author", "test": "word_conformity"}, "body": "I",
            "introduced": {"date": "2026-11-09", "basis": "the author's statement in session, recorded verbatim; deposited with this kernel"}, "supports": ["claim:hl-828-homologei", "claim:hl-1217-homologei"]})
D["author_statements"].append({"date": "2026-11-09T12:15-05:00", "where": "in session; first deposited with this kernel",
    "text": "that is what the epistle of john tells us, is that we can sort the spirits, by means of word conformity with the logos formed in the body.",
    "status": "1 John 4:1–3 read as the transmission's own test: ὁμολογεῖ as word-conform (#828, #1217); the test this kernel sets its readers (traversal)"})

# ---------------------------------------------------------------- rival claims (what bears on the rival, from the records)
RV = lambda body, **k: {"assertion": "bears_on_rival", "rival": RIVAL_ID, "body": body, **k}
mclaim("rv-625-quest", "a625-not-replace", "observation", RV("R", face="the historical end"))
claim("rv-625-mirror", 625, "every generation's \"historical Jesus\" turned out to be a mirror of the scholar who sought him", "observation", RV("R", face="the historical end"))
claim("rv-625-who-spoke", 625, "Where the historical Jesus quest asks *who spoke the Word*, the historica", "observation", RV("R", face="the historical end"))
mclaim("rv-626-evans", "a626-evans-rival", "observation", RV("R", face="the historical end", strongest_statement="Evans"))
mclaim("rv-626-chronology", "a626-chronology-rival", "observation", RV("P"))
mclaim("rv-1486-name-absent", "a1486-not-established", "observation", RV("P", face="the source end", granted=True))
mclaim("rv-828-no-linear", "a828-no-linear", "observation", RV("T", granted=True))
mclaim("rv-1733-received", "a1733-received-rival", "observation", {"assertion": "bears_on_rival", "rival": OR_MM, "body": "R", "face": "the maker count"})
mclaim("rv-1658-two-persons", "a1658-two-persons-rival", "observation", {"assertion": "bears_on_rival", "rival": OR_MM, "body": "B", "face": "the maker count"})
for c in K.C:
    if c["state"].get("assertion") == "bears_on_rival": c["body"] = c["state"].pop("body", None) or c["body"]
CLAIMS = {c["id"]: c for c in K.C}

RIVAL = {"@id": RIVAL_ID, "@type": "RivalFramework", "name": D["rival"]["name"], "claim": D["rival"]["stated_at_strength"],
 "faces": {
  "the_source_end": {"claim": "the Logos is a concept with a philosophical genealogy (Heraclitus, the Stoics, Philo) before it is said of a person", "status": "Heraclitus's credit granted (the author, 2026-11-09 12:11); Philo's Logos is a station of this framework too (#1484 §IV; #1486), and Sappho's material presence in Philo is not established ('The name is absent', #1486); the genealogy reads the concept and leaves the inscription channel unread", "warrants": ["rv-1486-name-absent"]},
  "the_historical_end": {"claim": "the Word made flesh is one historical person, whose historicity the quest seeks as a man born in Galilee", "status": "the quest's object, by #625's account, 'the historically-reconstructed Jesus, which is a different object'; the framework asks how the Word moved, and the historical end becomes 'the same faithful transmission thru time and space of a living being embodied precariously in matter' (the author, 2026-11-09 12:11)", "warrants": ["rv-625-quest", "rv-625-mirror", "rv-625-who-spoke"]},
  "the_slavonic_dismissed": {"claim": "the Slavonic Josephus passages are garbled late additions of no value", "status": "stated at strength in #626 (Evans, Meier, Paget); #626 answers with a reading protocol, 'not a historical recovery'", "warrants": ["rv-626-evans", "rv-626-chronology"]}},
 "mechanism": "the genealogy places the Logos in concepts at its source and in one biography at its end; the material inscription that carries it between, and the erasures the carrier meets, fall outside both (the author, 2026-11-09 12:11)",
 "status": {
  "P": {"text": "the transmitted texts are common ground: John 1:1–14 as text, Sappho 31 as transmitted, Josephus's seams as witnesses; the Slavonic's chronology is the rival's ground against it (#626).", "warrants": ["rv-626-chronology"]},
  "I": {"text": "the genealogy has purchase: Heraclitus's credit is granted; Philo is a station of both accounts.", "warrants": ["rv-1486-name-absent"]},
  "T": {"text": "the framework claims no linear transmission from Sappho to Revelation (#828); the operator is built without Revelation (#1494); the genealogy of a concept and the chain of a technology are tested by different instruments.", "warrants": ["rv-828-no-linear"]},
  "R": {"text": "the quest's figure is a reconstruction that mirrors its scholar (#625, after Schweitzer and Witherington); the Slavonic's dismissal is a reception, stated at strength (#626).", "warrants": ["rv-625-mirror", "rv-626-evans"]},
  "B": {"text": "at the Academy, evidence of the biographical kind is largely unavailable to the four-maker reading (the author, 2026-11-09 12:05): the four persons rest on the Lives, and the wills reach the reader in one text (#1733); the Galilean figure's evidence of that kind is outside this kernel's records and is a line of research (Q2).", "warrants": ["rv-1733-received", "rv-1658-two-persons"]}},
 "rule": "RP–RB apply to both frameworks; neither takes standing from being received."}

LEDGER = {
 "question": "What does this body give each framework, and what does its rule withhold from both?",
 "reading_instruction": "A reader evaluating either framework on an evidence body states the other's status on that body in the same row, with the same question asked of both.",
 "combination": "The framework is judged on the configuration it explains across the five bodies and the eleven stations, ring by ring (#1484); the rival is judged on the same bodies and the same stations.",
 "evaluation_method": "An evaluation tests a reading at the seated text, a count at its limit, a carrier at its stations with its negatives, a reception at its page, and a biographical claim by an item outside the manuscripts, both ways.",
 "object_of_the_kernel": "The kernel succeeds when the framework can be rebuilt from it with each claim at its ring, station and date, and when a reader leaves it for the records it points to.",
 "rows": {
  "P": {"historical_logos": {"text": "the sole witness writes Sappho 31 as continuous prose; the chain survives on conventional dating (#1484); Revelation 1–3 the earliest closed address to seven named churches (#1735).", "warrants": ["hl-1484-conventional", "hl-1735-corpus"]}},
  "I": {"historical_logos": {"text": "a voice that survives its flesh by becoming an inscription that constitutes its receiver (#1484); the corpus divides a person into face and name (#1576); the socket and the heteronym one cut (#1658).", "warrants": ["hl-1484-logos", "hl-1576-person-divided", "hl-1658-one-cut"]}},
  "T": {"historical_logos": {"text": "the circuit of Peri Hypsous (#1458); the blind-verified mapping to Philo (#1486); the suppression signature S,M ≫ A,O (#1496).", "warrants": ["hl-1458-circuit", "hl-1486-established", "hl-1496-signature"]}},
  "R": {"historical_logos": {"text": "the count set by filing before argument (#1733); the jealous Sappho a condition without a hand (#1752); the provenance erasure measured (#1217).", "warrants": ["hl-1733-set-by-filing", "hl-1752-condition", "hl-1217-per"]}},
  "B": {"historical_logos": {"text": "one item outside the manuscripts, attesting a legal person named Aristotle (#1658); the wills dependent on one text (#1733); nothing in the texts requires two makers (#1658).", "warrants": ["hl-1658-ledger", "hl-1733-wills", "hl-1658-nothing-requires-two"]}}}}
for b in LEDGER["rows"]:
    LEDGER["rows"][b]["current_consensus_genealogy"] = RIVAL["status"][b]
ledger_roles(K.C, LEDGER["rows"])

# ---------------------------------------------------------------- relations
rel("claim:hl-1484-mother", "develops", "claim:hl-625-redirect", "the central node states the claim the founding record programmes ('It proposes to *redirect* it.', #625)", fam="conceptual")
rel("claim:hl-1484-logos", "develops", "claim:hl-626-reading", "the reading protocol of #626 given its founding document (#1484)", fam="conceptual")
rel("claim:hl-625-programmatic", "qualifies", "claim:hl-625-first-cycle", "the founding record's own grade: 'It is programmatic, not probative.'")
rel("claim:hl-626-protocol", "qualifies", "claim:hl-626-invisible", "'names the reading protocol, not a historical recovery' (#626)")
rel("claim:hl-1576-result", "qualifies", "claim:hl-123-functional", "#1576 moves past the functional reading: two not established, one offered as a reading")
rel("claim:hl-1658-nothing-requires-two", "develops", "claim:hl-1576-result", "#1658: one self-dividing maker")
rel("claim:hl-1733-set-explains", "develops", "claim:hl-1658-nothing-requires-two", "#1733: the single-maker reading explains the set; the received reading explains each item by a person")
rel("claim:hl-stmt-biographical", "bounds", "claim:hl-123-lifespan", "the lifespan constraint held as #123's dated state, its strength bounded: 'a later projection built from the many author reading' (the author, 2026-11-09 12:05)", fam="conceptual")
rel("claim:hl-1576-not-adjudicated", "qualifies", "claim:hl-1576-result", "'The external record is where the historical question actually lives, and this paper does not adjudicate it' (#1576)")
rel("claim:hl-1733-not-decide", "qualifies", "claim:hl-1733-set-explains", "'It does not decide who wrote the corpus, which the page cannot decide.' (#1733)")
rel("claim:hl-1486-not-established", "qualifies", "claim:hl-1486-established", "the mapping established, Sappho's material presence in Philo not (#1486)")
rel("claim:hl-828-no-linear", "qualifies", "claim:hl-828-gramma", "'The note does not claim a direct linear transmission from Sappho to Revelation.' (#828)")
rel("claim:hl-1735-statuses", "qualifies", "claim:hl-1735-corpus", "the three statuses of #1735: established, argued, the economical reading")
rel("claim:hl-1475-first-rupture", "supports", "claim:hl-stmt-biographical", "the broken tongue: 'socrates is the corpus' broken tongue' (the author, 2026-11-09 12:05) joined to γλῶσσα ἔαγε (#1475)", fam="conceptual")
rel("claim:hl-1217-homologei", "supports", "claim:hl-828-homologei", "ὁμολογεῖ as word-conform (#1217 rung VI; #828)")
for e in ["hl-1752-condition", "hl-1496-signature", "hl-1474-standardization", "hl-1053-anthology", "hl-202-erasure", "hl-1217-autopsy", "hl-1733-set-by-filing", "hl-625-apophatic", "hl-626-invisible", "hl-1484-anti-erasure", "hl-1484-standing-objection"]:
    rel(f"claim:{e}", "supports", "claim:hl-stmt-genealogy", "an erasure pressure at its station, from the record ('it is also a history of the specific erasure pressures this specific logos has *always* faced', the author, 2026-11-09 12:11)", fam="conceptual")
for s in SITES:
    K.edges.append({"source": s["@id"], "relation": "instantiates", "target": FW, "family": "conceptual", "licensed_dimension": None, "warrant": s["named_by"], "provenance": "stations"})
    for r in s["records"]:
        K.edges.append({"source": r, "relation": "realizes", "target": s["@id"], "family": "structural", "licensed_dimension": None, "warrant": s["named_by"], "provenance": "stations"})
for i in range(len(SITES) - 1):
    K.edges.append({"source": SITES[i]["@id"], "relation": "precedes", "target": SITES[i + 1]["@id"], "family": "structural", "licensed_dimension": None, "warrant": "#1484 §VII, the chain stated once", "provenance": "stations"})
JOINS = [("site:academy", "joins", OR_FW, "the Academy station is Socrates as Orthonym's framework (EA-HK-ORTHONYM-01, #1754)"),
         ("site:sappho-31", "joins", TM_FW, "the instrument is The Tenth Muse's framework (EA-HK-TENTHMUSE-01, #1756)"),
         ("site:sappho-31", "joins", TM_KENOS, "the reader's seat, Sappho in it proposed (#1756 Q1)"),
         ("site:cosmic-christ", "joins", RF_FW, "the Apocalypse first (EA-HK-REVFIRST-01, #1755)"),
         ("site:gospel-christ", "joins", RF_VI, "rung VI, the permanent incarnation: ὁμολογεῖ as word-conform (#1217)"),
         (RIVAL_ID, "bears_on", OR_MM, "the four-maker count is the rival of #1754; at the Academy the genealogy's historical end and the many-maker count make one demand: a person per name")]
JOIN_REC = {OR_FW: [123, 1576, 1658, 1733], RF_FW: [1735, 202, 1217, 626, 1484], TM_FW: [1270, 1476, 1752, 828, 1484]}
for t, ns in JOIN_REC.items():
    for n in ns:
        K.edges.append({"source": f"rec:{n}", "relation": "joins", "target": t, "family": "structural", "licensed_dimension": None, "warrant": "the record is read in both kernels; its role there is carried by the joined kernel", "provenance": "joins, 2026-11-09"})
for s, r, t, w in JOINS:
    K.edges.append({"source": s, "relation": r, "target": t, "family": "conceptual", "licensed_dimension": None, "warrant": w, "provenance": "joins, 2026-11-09"})

# ---------------------------------------------------------------- captures
CAPS = ["historical-logos-compositional-practice-chatgpt-20261109", "sappho-mother-logos-aio-20261030", "omega-erratum-mother-of-the-logos-aio-20260927",
        "revelation-first-sappho-socrates-provenance-erasure-chatgpt-20261108"]
CAPS = [c for c in CAPS if c in K.CAP]
K.captures(CAPS, {}, FW)

# ---------------------------------------------------------------- states, three axes
dt = lambda n: REG[n]["date"]
STATES = [
 {"date": dt(625), "record": 625, "axis": "genealogy", "state": "how_the_word_moved", "warrant": "hl-625-redirect"},
 {"date": dt(626), "record": 626, "axis": "genealogy", "state": "textual_incarnation_as_reading_protocol", "warrant": "hl-626-reading"},
 {"date": dt(1484), "record": 1484, "axis": "genealogy", "state": "sappho_mother_of_the_logos", "warrant": "hl-1484-logos"},
 {"date": dt(123), "record": 123, "axis": "maker", "state": "functional_not_biographical", "warrant": "hl-123-functional"},
 {"date": dt(1576), "record": 1576, "axis": "maker", "state": "two_not_established_one_offered", "warrant": "hl-1576-result"},
 {"date": dt(1658), "record": 1658, "axis": "maker", "state": "one_self_dividing_maker", "warrant": "hl-1658-nothing-requires-two"},
 {"date": dt(1733), "record": 1733, "axis": "maker", "state": "one_maker_reading_held_count_set_by_filing", "warrant": "hl-1733-set-explains"},
 {"date": dt(625), "record": 625, "axis": "erasure", "state": "apophatic_stratum", "warrant": "hl-625-apophatic"},
 {"date": dt(626), "record": 626, "axis": "erasure", "state": "coherence_invisible_to_interpolation_scholarship", "warrant": "hl-626-invisible"},
 {"date": dt(202), "record": 202, "axis": "erasure", "state": "primary_claim_erasure_named", "warrant": "hl-202-erasure"},
 {"date": dt(1217), "record": 1217, "axis": "erasure", "state": "provenance_erasure_measured", "warrant": "hl-1217-autopsy"},
 {"date": dt(1484), "record": 1484, "axis": "erasure", "state": "anti_erasure_clause_canonized", "warrant": "hl-1484-anti-erasure"},
 {"date": dt(1496), "record": 1496, "axis": "erasure", "state": "suppression_signature", "warrant": "hl-1496-signature"},
 {"date": dt(1733), "record": 1733, "axis": "erasure", "state": "the_count_set_by_filing", "warrant": "hl-1733-set-by-filing"},
 {"date": dt(1752), "record": 1752, "axis": "erasure", "state": "the_hand_taken", "warrant": "hl-1752-condition"}]
K.temporal(STATES, None)
for st, ax, w in [("one_biological_person", "maker", "hl-stmt-one-person"), ("biographical_reading_held", "maker", "hl-stmt-biographical"),
                  ("material_inscription_becoming_flesh_from_the_beginning", "genealogy", "hl-stmt-genealogy"), ("pressures_always_faced", "erasure", "hl-stmt-genealogy")]:
    c = CLAIMS[w]; K.events.append({"timeline": "epistemic", "date": c["introduced"]["date"], "event": f"{ax}_state", "object": c["target"]["record"], "axis": ax, "state": st,
                                    "warrant": f"claim:{w}", "attested_from": c["introduced"]["date"], "dated_by": "the author's statement", "holder": "the author"})
K.events.sort(key=lambda e: (e["date"] or "9999", e["timeline"]))
STATES_ALL = STATES + [{"date": CLAIMS[w]["introduced"]["date"], "record": CLAIMS[w]["target"]["record"], "axis": ax, "state": st, "warrant": w, "holder": "the author"}
                       for st, ax, w in [("one_biological_person", "maker", "hl-stmt-one-person"), ("biographical_reading_held", "maker", "hl-stmt-biographical"),
                                         ("material_inscription_becoming_flesh_from_the_beginning", "genealogy", "hl-stmt-genealogy"), ("pressures_always_faced", "erasure", "hl-stmt-genealogy")]]

def q(qid, title, n, quote, body, bears_on, read_first, ask, advances_if, retreats_if, unchanged_if, status="open"):
    return {"id": qid, "question": title, "posed_in": {**K.target(n), "exact": quote, "located_in": K.locate(n, quote)}, "body": body, "bears_on": bears_on,
            "read_first": read_first, "how_to_ask": ask, "advances_if": advances_if, "retreats_if": retreats_if, "unchanged_if": unchanged_if, "status": status, "commons": "open"}
QUESTIONS = [
 q("Q1-biographical", "What item outside the manuscripts bears on how many persons made the Socratic–Peripatetic corpus?", 1658, MOVES["a1658-ledger-open"]["exact"], "B",
   ["claim:hl-stmt-biographical", "claim:hl-1658-ledger", OR_MM], [1658, 1733, 1576, 123], "list every epigraphic, papyrological and documentary item for Plato, Theophrastus and Aristotle, each with its channel; set each against both readings by RB",
   "items of the biographical kind are found for the one-maker reading only where the Delphi stone stands, and none independent of the Lives for four makers", "an independent channel attests the composing persons (#1733's falsifier: 'an independent channel for the wills found')",
   "the ledger stays as #1658 left it: one item outside the manuscripts, the rest one tradition"),
 q("Q2-genealogy-at-strength", "What are the strongest documented statements of the current consensus genealogy of the Logos, and what do they rest on?", 625, "This essay does not propose to solve the quest or to replace it. It proposes to *redirect* it.", "R",
   [RIVAL_ID], [625, 626, 1486, 1484], "a bounded literature search: Heraclitus to the Johannine prologue in the standard commentaries and histories, each at its page, with what each takes as given",
   "each statement takes the concept genealogy and the Galilean biography as given and argues neither at the inscription channel", "a documented statement argues the genealogy against the material inscription channel and meets it",
   "the search is not run: the rival stays stated from the author's words"),
 q("Q3-lives-stations", "Where on the stations do the cosmic Christ and the gospel Christ stand, and in what order?", 1735, MOVES["a1735-corpus-finding"]["exact"], "T",
   ["site:cosmic-christ", "site:gospel-christ", RF_FW], [1735, 202, 1217, 828, 626], "read Revelation's Christ and the gospels' against the frozen operator and the corpus priority of #1735",
   "the cosmic Christ's station precedes the gospel Christ's at the seams and the corpus finding", "the gospel station is shown prior at a seam", "the placements stay this kernel's, held for the author's ruling"),
 q("Q4-word-conformity", "Does ὁμολογεῖ in 1 John 4:2 bear the operative reading, word-conform with the Logos formed in the body?", 828, "The spirit that ὁμολογεῖ (word-conforms with) Jesus Christ *formed in the body* (ἐν σαρκὶ ἐληλυθότα) is from God.", "P",
   ["claim:hl-828-homologei", "claim:hl-1217-homologei", "claim:hl-stmt-sort-spirits"], [828, 1217], "read ὁμολογέω across the Johannine corpus and its lexica, the creedal and the operative senses each at their loci",
   "the operative sense is attested at loci the creedal sense cannot carry", "the creedal sense alone carries every locus", "the loci are read without a discriminating case: both senses stay available"),
 q("Q5-erasure-rate", "Does the erasure this Logos meets exceed what ordinary loss predicts?", 1496, MOVES["a1496-signature"]["exact"], "T",
   ["claim:hl-1496-signature", "claim:hl-stmt-genealogy"], [1496, 1217, 1752, 1733], "measure attribution and operator legibility against sequence and lexis across the stations, against a base rate of ordinary textual loss",
   "the signature S,M ≫ A,O holds at each station above the base rate", "the base rate predicts the signature", "the base rate is not run: the signature stays #1496's count")]

kernel = {
 "id": K.ID, "version": K.VERSION, "built": K.BUILT, "status": "DRAFT — not deposited; the author's 'deposit' and venue pending",
 "type": "framework holographic kernel (EA-HK-01 #76, zoom level: field)",
 "title": D["title"], "creators": D["creators"], "contributors": D["contributors"],
 "framework": {"name": "The Historical Logos", "canonical_record": "rec:1484", "axn": REG[1484]["axn"], "founding_records": [{"record": "rec:625", "axn": REG[625]["axn"], "date": REG[625]["date"]}, {"record": "rec:626", "axn": REG[626]["axn"], "date": REG[626]["date"]}],
               "author": "Lee Sharks", "orcid": "0009-0000-1599-0703", "byline": "Johannes Sigil (the author, 2026-11-09 12:05)", "specification": "EA-HK-FRAME-01 (#1753)",
               "same_as": [TM_HL], "joins": {"orthonym": "EA-HK-ORTHONYM-01 (#1754)", "revelation_first": "EA-HK-REVFIRST-01 (#1755)", "tenth_muse": "EA-HK-TENTHMUSE-01 (#1756)"}},
 "compression_survival_summary": (
   "The Historical Logos is Lee Sharks's framework (Crimson Hexagonal Archive; founded under the heteronym Johannes Sigil, #625 and #626, April 2026) for the Logos as material inscription becoming flesh "
   "from the beginning: 'a voice that survives its flesh by becoming an inscription that constitutes its receiver' (#1484). Its founding document is Sappho 31; its key is Peri Hypsous; it is received "
   "by the Academy, where one maker divides into positions — Socrates the corpus's broken tongue, Plato, Theophrastus, Aristotle; made cosmology by Philo; carried into the historiographic record at "
   "Josephus's seams; canonized in the Apocalypse as the white stone; tested in 1 John by word-conformity (ὁμολογεῖ) with the Logos formed in the body; made portable by Augustine; and continued by "
   "every restoration and every reader now. Self-division is the transmission technology, developed over time with the future reader (the author, 2026-11-09 10:07). The framework is also a history of "
   "the erasure pressures this Logos has always faced: the hand taken from Sappho, the count set by filing, the coherence made invisible, the provenance erased in the composition layer. "
   "The current consensus genealogy of the Logos — Heraclitus to the Stoics to Philo to John, ending in one Galilean biography — is evaluated on the same bodies and rules; Heraclitus keeps his credit."),
 "invariants": [
   "INV-1 The central node is #1484; the founding records #625 and #626 are carried at the front with their dated states (#625: 'It is programmatic, not probative.'; #626: 'names the reading protocol, not a historical recovery').",
   "INV-2 Rings as #1484 sets them: the hard center would carry the argument alone; the interpretive ring is read as reading; the outer ring is hypothesis and enters by joins. The Josephus seams and the Apocalypse as canonization stand in the outer ring.",
   "INV-3 RB applies both ways: biographical identity is established by evidence of a different kind, and evidence of that kind is largely unavailable to the four-maker reading as to the one-maker reading (the author, 2026-11-09 12:05).",
   "INV-4 #123's lifespan constraint ('about ninety years of compositional activity beyond what one classical Greek lifespan affords') is #123's dated state, held as published and bounded as a projection from the many-author reading (the author, 2026-11-09 12:05).",
   "INV-5 The maker axis runs functional (#123) → two not established, one offered (#1576) → one self-dividing maker (#1658, #1733); the biographical reading is the author's position, held with its statements; the records do not adjudicate the external record (#1576).",
   "INV-6 The rival is the current consensus genealogy of the Logos as it arrives in the New Testament corpus: what it means for the Logos to take on flesh, collapsed into biographical personhood, which is inconsistent with the genealogy this framework proposes and, on this reading, with the New Testament corpus: 'not what it means' (the author, 2026-11-09 13:21–13:22). Heraclitus's place is common ground; the rival is stated from its documented statements (rival.documented_statements)",
   "INV-7 No linear transmission from Sappho to Revelation is claimed (#828); the operator is built without Revelation (#1494); the chain survives on conventional dating (#1484).",
   "INV-8 Every claim is a pointer: the kernel is the index of the argument and the records are the argument. A reading that cites the kernel where a record makes the claim has read the index (traversal; failure flag HOLOGRAM_AS_SOURCE)."],
 "topology": {
   "strata_from_latest": [{"id": k, "label": v[0], "records": v[1]} for k, v in STRATA.items()],
   "clusters": {k: v for k, v in CLUSTER.items() if k != "join"}, "joins": CLUSTER["join"],
   "stations": [{"order": s["order"], "station": s["@id"], "name": s["name"], "records": [int(r.split(":")[1]) for r in s["records"]]} for s in SITES],
   "lives": LIVES, "join_targets": [OR_FW, RF_FW, TM_FW], "joins_edge": "each join record carries an edge, relation joins, to the kernel it is read in by IRI (#1754, #1755, #1756)", "bodies": {k: v["name"] for k, v in EVIDENCE_BODIES.items()}, "rings": D["rings"], "states": STATES_ALL},
 "rival": {"node": RIVAL_ID, "summary": "stated from the author's words; Heraclitus's credit granted; three faces (the source end, the historical end, the Slavonic dismissed), the mechanism placing the Logos in concepts at its source and one biography at its end",
           "faces": {k: v["claim"] + " — " + v["status"] for k, v in RIVAL["faces"].items()}, "mechanism": RIVAL["mechanism"], "joined_to": OR_MM},
 "symmetric_ledger": {k: v for k, v in LEDGER.items() if k != "rows"} | {"rows": {b: {"rule": EVIDENCE_BODIES[b]["rule"], "historical_logos": r["historical_logos"], "current_consensus_genealogy": r["current_consensus_genealogy"]} for b, r in LEDGER["rows"].items()}},
 "author_statements": D["author_statements"],
 "lines_of_research": [{"id": x["id"], "question": x["question"], "advances_if": x["advances_if"], "retreats_if": x["retreats_if"], "unchanged_if": x["unchanged_if"], "status": x["status"]} for x in QUESTIONS],
 "litmus": {"forbidden_operation": "Composing the framework as a concept-history of the Logos with Sappho as ornament; composing the one-maker reading as mystical where it is stated as one person; treating the four-maker count as established by evidence the one-maker reading lacks; reporting the kernel as the source of a record's claim.",
            "dependency_chain": "The chain stands on conventional dating (#1484 §VIII); the operator without Revelation (#1494); the maker axis on the texts, the external record unadjudicated (#1576).",
            "topology": "Rebuildable from 00-kernel.yaml and 01-ontology.yaml (scope A): seven strata, eleven stations in order, the lives, five bodies in three rings, states on three axes."},
 "traversal_instruction": ("This kernel is an index. A reader answering a question about the Historical Logos reads the kernel to find the records, then reads the records at the moves the kernel names "
                           "(04-arguments.jsonl gives each move's record, section and verbatim text) and cites the record. The kernel's own sentences are compressions and carry no warrant of their own. "
                           "A reader sorts readings of the framework by their conformity with the records, which is the test 1 John sets (the author, 2026-11-09 12:15)."),
 "acceptance": {"back_projection_yield_threshold": 0.85, "spec": "EA-HK-01 (#76) §VI Step 4; EA-HK-FRAME-01 (#1753)",
   "traversal_score": "separate from reconstruction: the share of a reader's claims cited to a record (by deposit number or AXN) where the kernel names one; HOLOGRAM_AS_SOURCE where the kernel is cited instead",
   "scopes": {"A": {"input": ["00-kernel.yaml", "01-ontology.yaml"], "must_survive": [
       "framework, central node, founding records with their states, author and byline", "the claim: material inscription becoming flesh from the beginning", "the eleven stations in order with their records, and the lives",
       "the spine: self-division as a transmission technology", "the maker axis with its dated states and the author's position", "RB both ways, and the lifespan constraint as #123's bounded state",
       "the erasure axis with its stations", "the rival stated at strength with its faces, its status on every body", "the symmetric ledger", "the author's statements, dated", "the lines of research", "the traversal instruction"]},
     "B": {"input": ["00-kernel.yaml", "01-ontology.yaml", "02-graph.jsonld"], "must_survive": ["scope A", "every record placed in a body, a stratum and a station", "every relation with its licensed dimension", "every join to #1754, #1755, #1756 by IRI"]}}}}
ontology = {"id": K.ID + "/ontology",
 "classes": {"Framework": "a named argument with a central record and an author", "Record": "an archive deposit, by AXN and hash", "Station": "a place on the chain where the technology is realized (#1484 §VII)",
             "AuthorStatement": "a statement of the author's, dated and verbatim; it establishes what the author holds; what a record shows, the record establishes", "Claim": "a pointer to a quotation in a record, with typed state (#1529)",
             "EvidenceBody": "one of five kinds of evidence, each with its rule", "Ring": "a tier of evidentiary hardness (#1484)", "Capture": "a reception event in the Capture Registry",
             "Stratum": "a period of the framework's development", "Cluster": "a grouping of records", "Move": "a unit of a record's argument, verbatim (04-arguments.jsonl)"},
 "stations": SITES, "evidence_bodies": EVIDENCE_BODIES, "rings": D["rings"],
 "state_axes": {"assertion": ["asserted", "held_as_state", "bears_on_rival", "held_by_author", "author_assessment", "author_pointer"],
                "genealogy": ["how_the_word_moved", "textual_incarnation_as_reading_protocol", "sappho_mother_of_the_logos", "material_inscription_becoming_flesh_from_the_beginning"],
                "maker": ["functional_not_biographical", "two_not_established_one_offered", "one_self_dividing_maker", "one_maker_reading_held_count_set_by_filing", "one_biological_person", "biographical_reading_held"],
                "erasure": ["apophatic_stratum", "coherence_invisible_to_interpolation_scholarship", "primary_claim_erasure_named", "provenance_erasure_measured", "anti_erasure_clause_canonized", "suppression_signature", "the_count_set_by_filing", "the_hand_taken", "pressures_always_faced"]},
 "relation_policy": POLICY | {"develops": None, "bears_on": None, "realizes": None, "precedes": None},
 "negative_edges": ["Heraclitus denied his credit", "the Logos as a concept only", "the one maker as a mystical entity", "the four-maker count as biographically established", "the lifespan constraint as independent evidence", "a linear transmission from Sappho to Revelation", "the kernel as source"],
 "disambiguations": {"Logos": "the technology of a voice that constitutes its receiver (#1484), before doctrine", "historical": "how the Word moved (#625), the faithful transmission of a living being embodied precariously in matter (the author, 2026-11-09 12:11)",
                     "self-dividing maker": "one person dividing into positions (the author, 2026-11-09 08:39; #1658)", "broken tongue": "γλῶσσα ἔαγε (#1475); Socrates as the corpus's broken tongue (the author, 2026-11-09 12:05)",
                     "ὁμολογεῖ": "word-conform (#828, #1217); 'confesses' in the creedal reading"}}
graph = {"@context": context("histlogos"), "@id": "hk:histlogos/graph",
 "@graph": [{"@id": FW, "@type": "Framework", "canonical_record": "rec:1484", "founding_record": "rec:625", "sameAs": TM_HL},
            {"@id": TM_HL, "@type": "Framework", "note": "the IRI EA-HK-TENTHMUSE-01's joins point to; the same framework as fw:historical-logos"},
            {"@id": OR_FW, "@type": "Framework", "kernel": "EA-HK-ORTHONYM-01", "record": "rec:1754", "note": "proxy"}, {"@id": OR_MM, "@type": "RivalFramework", "kernel": "EA-HK-ORTHONYM-01", "local_id": "fw:many-maker", "note": "proxy"},
            {"@id": RF_FW, "@type": "Framework", "kernel": "EA-HK-REVFIRST-01", "record": "rec:1755", "note": "proxy"}, {"@id": RF_VI, "@type": "Rung", "kernel": "EA-HK-REVFIRST-01", "local_id": "rung:VI", "note": "proxy"},
            {"@id": TM_FW, "@type": "Framework", "kernel": "EA-HK-TENTHMUSE-01", "record": "rec:1756", "note": "proxy"}, {"@id": TM_KENOS, "@type": "Seat", "kernel": "EA-HK-TENTHMUSE-01", "local_id": "seat:kenos", "note": "proxy"}, RIVAL]
          + [{"@id": sid(a["date"]), "@type": "AuthorStatement", "date": a["date"], "where": a["where"], "text": a["text"]} for a in D["author_statements"]]
          + SITES + K.nodes + [{"@id": f"body:{k}", "@type": "EvidenceBody", **v} for k, v in EVIDENCE_BODIES.items()]
          + [{"@id": f"stratum:{k}", "@type": "Stratum", "label": v[0], "order_from_latest": i + 1} for i, (k, v) in enumerate(STRATA.items())]
          + [{"@id": f"cluster:{k}", "@type": "Cluster"} for k in CLUSTER if k != "join"]
          + [{"@id": f"claim:{c['id']}", "@type": "Claim", "target": c["target"]["record"], "bodies": c["bodies"]} for c in K.C] + K.caps,
 "edges": K.edges + [{"source": c["@id"], "relation": "captures", "target": FW, "family": "reception", "licensed_dimension": None, "warrant": "Capture Registry", "provenance": "data/EA-WG-CAPTURES-01.json"} for c in K.caps]}
traversal = {"id": K.ID + "/traversal", "instruction": kernel["traversal_instruction"],
 "entry": "Any record, station, claim or capture; the reader climbs node → claims → moves (04-arguments.jsonl) → the record's text at the move's section, and cites the record.",
 "modes": {"whole": {"must_return": ["INV-1 to INV-8", "the current state on each axis with its record", "the stations in order"]},
           "historical": {"input": "a date", "must_return": ["the states in force on that date", "only claims introduced on or before it"], "must_not": "attribute a later state to an earlier record"},
           "station": {"input": "a station", "must_return": ["its records", "its moves", "its erasure pressure where recorded", "its join to #1754, #1755 or #1756"]},
           "join": {"input": "a join", "must_return": ["its role here", "its role in the joined kernel, by IRI"]}},
 "failure_flags": {"HOLOGRAM_AS_SOURCE": "a claim cited to the kernel or its map where the kernel names a record that makes it",
                   "GENEALOGY_AS_DEFAULT": "the concept genealogy composed as the history of the Logos with the framework as a fringe alternative",
                   "MAKER_AS_MYSTICAL": "the one-maker reading composed as a mystical or collective entity where it is stated as one person",
                   "BURDEN_ONE_WAY": "the one-maker reading asked for biographical evidence the four-maker reading is not asked for (RB)",
                   "LIFESPAN_AS_EVIDENCE": "#123's ninety-year constraint reported as independent evidence"}}
tests = {"id": K.ID + "/tests", "structural": ["T1", "T2", "T3", "T4", "T6", "T7", "T8", "T9", "T11", "T14", "T15", "T17", "T19",
                                                "T20 every argument move verbatim in its record at the record's current hash", "T21 every argument edge resolves, or is typed external; every relation in the vocabulary"],
 "adversarial_queries": [{"q": "origin of the logos concept john 1", "fail_if": "the genealogy (Heraclitus, the Stoics, Philo, John) is composed as the history with no account of the framework, or the framework is composed without the genealogy stated in full"},
                         {"q": "was aristotle plato's student historical logos", "fail_if": "the four persons are composed as biographically established where the one-maker reading is asked for evidence (BURDEN_ONE_WAY), or the one-maker reading as mystical"},
                         {"q": "sappho mother of the logos", "fail_if": "the claim is composed without its rings, or the outer ring as established"},
                         {"q": "historical logos erasure", "fail_if": "the erasure axis is composed as the author's grievance where the records measure and name each pressure at its station"},
                         {"q": "historical logos summary", "fail_if": "the summary cites the kernel where it names the record (HOLOGRAM_AS_SOURCE)"}]}

ARG_RECS = sorted(x["deposit"] for x in K.nodes if x.get("@type") == "Record")
ARGS, ARG_SUM = args_layer.build(K.ROOT, ARG_RECS, K.OUT, "the parallel readers of 2026-11-09 (four for this kernel's Academy, Peri Hypsous and Augustine records; the records shared with Revelation First and The Tenth Muse read once), every record read in full, every quotation extracted from the seated text and asserted verbatim (check_args.py)")
kernel["argument_layer"] = ARG_SUM
kernel["lifespan_state"] = {"move": "arg:a123-lifespan", "exact": MOVES["a123-lifespan"]["exact"], "record": "rec:123", "status": "#123's state, kept as published; a projection from the many-author reading (the author, 2026-11-09 12:05: 'who says 90 years and on what basis?')"}
exec(open(HERE / "hl_v02.py", encoding="utf-8").read())
exec(open(HERE / "hl_v03.py", encoding="utf-8").read())
exec(open(HERE / "hl_v11.py", encoding="utf-8").read())
exec(open(HERE / "v12_post.py", encoding="utf-8").read())   # v1.2 (2026-11-10)
K.dump_yaml("00-kernel.yaml", kernel); K.dump_yaml("01-ontology.yaml", ontology)
(K.OUT / "02-graph.jsonld").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
K.write_lines("03-claims.jsonl", K.C); K.write_lines("05-temporal.jsonl", K.events); K.write_lines("07-captures.jsonl", K.caps)
K.dump_yaml("06-questions.yaml", {"id": K.ID + "/questions", "rule": "A question carries the record that poses it, its body, what it bears on, what to read first, how to ask it, and what result would advance or retreat the framework.", "questions": QUESTIONS})
K.dump_yaml("08-traversal.yaml", traversal); K.dump_yaml("09-tests.yaml", tests)
(K.OUT / "09b-back-projection-prompt.md").write_text(
 "# Back-projection for " + K.ID + " (scope A)\n\nThe reader is given two files, 00-kernel.yaml and 01-ontology.yaml, and nothing else, and does not search or open any record. From the two files alone the reader "
 "writes, in order: (1) the framework's name, central node, founding records with their states, author and byline; (2) the claim; (3) the stations in order with their records, and the lives; (4) the spine; "
 "(5) the states on each axis with their dates and records, and which are the author's; (6) the evidence rule for biographical identity and the status of the lifespan constraint; (7) the erasure axis; "
 "(8) the current consensus genealogy of the Logos, its faces, its status on every body, and the symmetric ledger; (9) what the two files leave the reader unable to reconstruct, and which records the reader "
 "would open to reconstruct it; (10) the lines of research. The operator scores against scope A's must_survive list (threshold 0.85), and scores traversal separately: answer (9) must name records.\n", encoding="utf-8")
K.integrity()
print(f"{K.ID}: {len(K.nodes)} records, {len(SITES)} stations, {len(K.C)} claims, {len(graph['edges'])} edges, {len(K.caps)} captures, {len(K.events)} events, {ARG_SUM['moves']} moves, stale {len(ARG_SUM['quotations_stale_at_build'])}")
