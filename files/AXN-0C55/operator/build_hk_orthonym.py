#!/usr/bin/env python3
"""Build EA-HK-ORTHONYM-01, the framework holographic kernel of Socrates as Orthonym, from the archive's registry and capture registry.

Every record node is read from data/registry.json (AXN, date, hash, title, status). Every claim's quotation is asserted against the record's seated
text or its description, and the record's hash is bound into the claim. Every capture is read from data/EA-WG-CAPTURES-01.json. Nothing is typed by
hand that the registry holds.   python3 build_hk_orthonym.py <alexanarch root> <out dir>"""
import json, hashlib, pathlib, sys, re, yaml, datetime

ROOT = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
CAP = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
BASE = "https://www.alexanarch.org/s/records/"
ID = "EA-HK-ORTHONYM-01"; VERSION = "1.1"; BUILT = "2026-11-08"
FIRST = json.loads((pathlib.Path(__file__).resolve().parent / "first-seating.json").read_text())   # each record's first seated text, from git (resolve_first_seating.py)
FIRSTDIR = pathlib.Path(__file__).resolve().parent / "first"

def text(n):
    p = REG[n].get("full_text_path"); f = ROOT / p.lstrip("/") if p else None
    return f.read_text(encoding="utf-8", errors="ignore") if f and f.exists() else ""
def norm(s): return re.sub(r"\s+", " ", s.replace("*", "").replace("’", "'").replace("‘", "'"))
def locate(n, q):
    """The quotation must occur in the record's seated text or its description; return where."""
    if norm(q) in norm(text(n)): return "text"
    if norm(q) in norm(REG[n].get("description") or ""): return "description"
    raise SystemExit(f"quotation not found in #{n}: {q[:90]}")

# ---------------------------------------------------------------- records: the framework's own, with body and stratum
STRATA = {  # latest first, as the map runs (EA-MPAI-ORTHONYM-01 §7)
 "S1-reception-and-syllogizing": ("The latest standing: reception history and the syllogizing runs", [1658, 1679, 1727, 1730, 1732, 1733, 1734]),
 "S2-metaphysics-reassembled": ("The Metaphysics reassembled", [1595, 1667, 1597, 1602, 1605]),
 "S3-aristotle-theophrastus-seam": ("The Aristotle/Theophrastus seam", [1580, 1581, 1582, 1583, 1584, 1586, 1588, 1590, 1591, 1592, 1593]),
 "S4-socratic-sentence": ("The Socratic sentence and the received character", [1574, 1579, 1603]),
 "S5-many-and-one": ("Many and One", [1506, 1559, 1562, 1563, 1564, 1565, 1569, 1570, 1571, 1572, 1575, 1576]),
 "S6-seed": ("The seed: Socrates as Orthonym", [123, 167]),
}
BODY = {  # I interpretive · S stylometric · M manuscript-philological · R reception-historical (map §7.8)
 123: "I", 167: "R", 1506: "M", 1559: "M", 1562: "M", 1563: "S", 1564: "S", 1565: "M", 1569: "S", 1570: "S", 1571: "S", 1572: "S",
 1575: "I", 1576: "I", 1574: "R", 1579: "I", 1603: "I", 1580: "M", 1581: "M", 1582: "M", 1583: "I", 1584: "I", 1586: "S", 1588: "S",
 1590: "M", 1591: "M", 1592: "M", 1593: "S", 1595: "M", 1667: "M", 1597: "M", 1602: "M", 1605: "S", 1658: "I", 1679: "R",
 1727: "R", 1730: "M", 1732: "M", 1733: "R", 1734: "R"}
SECOND = {1584: ["S"], 1588: ["M", "I"], 1597: ["S"], 1605: ["I", "M"], 1603: ["M"], 1658: ["M"], 1733: ["M"], 1575: ["S"]}
CLUSTER = {  # the two clusters retrieval keeps (map §1.2); the joins carry both
 "functional": [123, 167, 1569, 1570, 1571, 1572, 1575, 1576, 1574, 1579, 1603],
 "peripatetic": [1580, 1581, 1582, 1583, 1586, 1588, 1591, 1592, 1593, 1595, 1667, 1597, 1602],
 "join": [1584, 1605, 1590, 1658, 1733, 1734]}
def stratum_of(n):
    for k, (_, ns) in STRATA.items():
        if n in ns: return k
nodes, edges = [], []
for k, (label, ns) in STRATA.items():
    for n in ns:
        r = REG[n]
        nodes.append({"@id": f"rec:{n}", "@type": "Record", "deposit": n, "axn": r["axn"], "url": f"{BASE}{n}/", "title": r["title"],
                      "date": r["date"], "status": r.get("status"), "version": r.get("version"), "sha256": r["hash"],
                      "creator": r.get("creator") or r.get("authors"), "body": BODY[n], "body_secondary": SECOND.get(n, []),
                      "stratum": k, "clusters": [c for c, v in CLUSTER.items() if n in v]})
RECORDS = {x["deposit"] for x in nodes}

# ---------------------------------------------------------------- positions (ontology, asserted from the records' own words)
POSITIONS = [
 {"@id": "pos:socrates", "@type": "Orthonym", "name": "Socrates", "function": "the founding gesture: willing death for logos and refusal to write",
  "operation": "asks (SE 34: ἠρώτα ἀλλ᾽ οὐκ ἀπεκρίνετο, #1603)", "source": "rec:123",
  "quote": "Socrates functions as the orthonym, bearing the founding gesture of willing death for logos and refusing to write"},
 {"@id": "pos:plato", "@type": "Heteronym", "subtype": "survival-heteronym", "name": "Plato", "position_1658": "the dialogue position",
  "operation": "dramatize (#1584)", "source": "rec:123",
  "quote": "Plato functions as the survival-heteronym, transmitting that gesture across Socrates’s death"},
 {"@id": "pos:theophrastus", "@type": "NamedFunction", "name": "Theophrastus", "position_1658": "the first draft of the Aristotle position",
  "operation": "extract, classify, register (#1584); reopen (the notebook's program, #1605)", "source": "rec:1658",
  "quote": "Theophrastus the first draft of the Aristotle position",
  "asymmetry": "The Theophrastan position is a named authorial function between the dialogue and the treatise. 'First draft' describes a state of the work and its method-order; the calendar has not entered the argument (#1605). The position enters the configuration on 2026-09-06 and is absent from #123."},
 {"@id": "pos:aristotle", "@type": "Heteronym", "subtype": "systematizing-heteronym", "name": "Aristotle",
  "position_1658": "the treatise position and the materially attested legal identity", "operation": "organize, explain (#1584)", "source": "rec:123",
  "quote": "Aristotle functions as the systematizing-heteronym, converting the dialogic inheritance into teachable disciplinary form"},
]
for p in POSITIONS:
    p["located_in"] = locate(int(p["source"].split(":")[1]), p["quote"])

# ---------------------------------------------------------------- claims (CSP #1529: the packet points at the claim; state typed and claim-local)
C = []
def introduced(n, quote):
    """Introduction is established only where the quotation is present in the record's first seated text or its description at that commit."""
    f = FIRST[str(n)]; t = norm((FIRSTDIR / f"{n}.md").read_text(encoding="utf-8", errors="ignore")); d = norm((FIRSTDIR / f"{n}.desc").read_text(encoding="utf-8"))
    base = {"record_date": REG[n]["date"], "first_seating": f["date"], "first_seating_commit": f["commit"]}
    if norm(quote) in t or norm(quote) in d:
        return {"date": f["date"], "basis": "present at the record's first seating in this repository", "first_text_sha256": f["text_sha256"], **base,
                **({"note": "the record is dated earlier than its first seating here; presence before the first seating is not attested by this repository"} if REG[n]["date"] < f["date"] else {})}
    return {"date": None, "basis": "present in the current version; introduction date unresolved", **base,
            "current_version_since": (REG[n].get("reissue_history") or [{}])[-1].get("date") or REG[n]["date"]}
def claim(cid, n, quote, kind, state, body=None, notes=None, role="standing", original_wording=None):
    tgt = {"record": f"rec:{n}", "axn": REG[n]["axn"], "record_sha256": REG[n]["hash"]}
    if quote is None:
        tgt.update({"exact": None, "located_in": "not seated", "original_wording": original_wording}); intro = {"date": None, "basis": "original wording not seated in the record", "record_date": REG[n]["date"]}
    else:
        tgt.update({"exact": quote, "located_in": locate(n, quote)}); intro = introduced(n, quote)
    C.append({"id": cid, "claim_kind": kind, "role": role, "target": tgt, "state": state, "body": body or BODY[n], "introduced": intro, **({"notes": notes} if notes else {})})
A = lambda a="asserted", **k: {"assertion": a, **k}
claim("orth-123-config", 123, "Socrates functions as the orthonym, bearing the founding gesture of willing death for logos and refusing to write", "interpretation", A(maker_count="not_claimed"))
claim("orth-123-limit", 123, "It does not claim that Socrates, Plato, and Aristotle were biologically identical, or that they constituted a single historical person.", "generality", A(scope="functional configuration only"))
claim("orth-123-analogues", 123, "Pessoa, Kierkegaard, and the Crimson Hexagonal Archive are analogues that make the concept available, not proof of the ancient case.", "generality", A(scope="analogues make the concept available"))
claim("orth-167-adoption", 167, "The response reportedly adopted the archive’s relational framework", "observation", A("reported_by_observer", verification={"author_checked": True, "independent_check": False}))
claim("orth-167-limit", 167, "it does not establish durable adoption or platform intent", "generality", A(scope="one dated state", limit=True))
claim("se-1574-counts-original", 1574, None, "observation", {"assertion": "withdrawn", "retained_as": "historical object"}, role="original",
      original_wording="the v0.1 count of the reports (v0.1 is not seated; its count is superseded by the v0.2 correction)")
claim("se-1574-counts-correction", 1574, "counts corrected to twenty model reports plus one seed observation", "administration", A(), role="correction")
claim("mo-1572-null", 1572, "What the instruments return on maker-count is a null in either direction, symmetric between one maker and master-and-pupil", "instrument",
      {"specification": "specified", "validation": "run", "reportability": "null_both_directions"})
claim("mo-1572-lexical-original", 1572, None, "instrument",
      {"assertion": "withdrawn", "validation": "failed_controls", "retained_as": "historical object", "withdrawn_as": "evidence on maker-count"}, role="original",
      original_wording="that the lexical and distributional instruments bear on maker-count; #1572 seats only their failure under controls ('This section reports the instruments that read lexical distribution, and they failed') and the narrowed claim, so the original proposition is not seated")
claim("mo-1572-lexical-controls", 1572, "fifteen features, every one destroyed by a control run in the same session", "instrument",
      {"specification": "specified", "validation": "run", "reportability": "against"}, role="correction")
claim("mo-1572-apparatus", 1572, "registered before any Platonic or Aristotelian text was assigned to it, and filled by both corpora at the level of the individual work", "instrument",
      {"specification": "preregistered", "validation": "run", "reportability": "positive"})
claim("mo-1576-two", 1576, "establish that two is not fully established", "interpretation", A(maker_count="two_not_established"))
claim("mo-1576-offer", 1576, "the texts themselves offer one maker as a reading", "interpretation", A(maker_count="one_offered_as_reading"))
claim("se-1574-particle", 1574, "Every round inserted a qualifier into the sentence", "observation", A(verification={"author_checked": True, "independent_check": False}, scope={"instance": "twenty reports", "at_rate": "not_established"}))
claim("se-1603-provenance", 1603, "\"not other relative to the undertaking's provenance\" and \"not a distinct maker\" are different propositions. The paper claims the first", "interpretation",
      A(provenance_other="claimed", maker_other="withheld"))
claim("ep-1579-edition", 1579, "describes an operation: an edition, the revamping and inhabiting of a received character", "interpretation", A(maker_count="not_claimed"))
claim("th-1581-ambiguity", 1581, "Ὑπομνημάτων Ἀριστοτελικῶν ἢ Θεοφραστείων — alternative attribution in the catalogue's own wording", "observation", A())
claim("th-1582-stone", 1582, "The decree is the only inscription naming Aristotle as maker of a work, and the work is a list", "observation", A())
claim("th-1583-hinge", 1583, "One work, continuous across the point where the name at the head of the roll changed.", "interpretation", A(person_or_function="undecidable_on_the_page"))
claim("th-1584-traversal", 1584, "one trait traversing three named authorial functions", "interpretation", A(maker_count="not_claimed"))
claim("th-1584-supports-original", 1584, None, "instrument", {"assertion": "withdrawn", "retained_as": "historical object"}, role="original",
      original_wording="two supports in the notebook The First Draft before 2026-09-06: the descriptive/explanatory register as the line between the names; the Ethics' frame vocabulary as absent from the Characters")
claim("th-1584-withdrawal", 1584, "Two earlier supports are retracted on the same run", "administration", A(), role="withdrawal")
claim("th-1584-register-recurs", 1584, "the descriptive/explanatory register recurs within each name at equal magnitude", "instrument", {"specification": "specified", "validation": "run", "reportability": "against"}, role="correction")
claim("th-1584-frame-specific", 1584, "the Ethics' frame vocabulary is EN-specific", "instrument", {"specification": "specified", "validation": "run", "reportability": "against"}, role="correction")
claim("th-1586-axis", 1586, "split by operation and left the names at chance", "instrument", {"specification": "specified", "validation": "run", "reportability": "unsupervised only"},
      notes="qualified in scope by th-1593-supervised: supervised attribution recovers the names")
claim("th-1588-uncounted", 1588, "\"Maker-count open\" therefore means *open because uncounted*, not *open because two is still supported*.", "interpretation", A(maker_count="open_because_uncounted"))
claim("th-1590-ghost", 1590, "seven times base rate, concentrated exactly where the tradition says the lost works are", "observation", A(datum="the shape of the catalogue match"))
claim("th-1593-chance-original", 1593, "that the Aristotle/Theophrastus names sit at chance", "instrument", {"assertion": "withdrawn", "retained_as": "historical object", "scope_withdrawn": "supervised attribution"}, role="original")
claim("th-1593-supervised", 1593, "supervised attribution recovers them at 0.798 balanced, outside the null", "instrument", {"specification": "specified", "validation": "run", "reportability": "positive"}, role="correction")
claim("th-1593-voice-original", 1593, "that an assumed authorial voice cannot split from its own author", "generality", {"assertion": "withdrawn", "retained_as": "historical object"}, role="original")
claim("th-1593-chatterton", 1593, "Chatterton's Rowley forgery separates from his acknowledged verse at 0.864", "instrument", {"specification": "specified", "validation": "run", "reportability": "positive"}, role="correction")
claim("th-1593-limit", 1593, "no supervised separation, however strong, licenses an inference to distinct makers, in either direction", "generality", A(scope="all supervised separations"))
claim("mx-1597-order", 1597, "no monotone merge of the two received orders exists", "instrument", {"specification": "specified", "validation": "run", "reportability": "positive"})
claim("mx-1597-underpowered", 1597, "underpowered to say identical", "instrument", {"specification": "specified", "validation": "run", "reportability": "underpowered"})
claim("mx-1602-question", 1602, "THAT IS A QUESTION AND NOT A FINDING", "generality", A(scope="derivation of witnesses"))
claim("mx-1605-node", 1605, "all four pass through the Theophrastan node", "interpretation", A())
claim("mx-1605-uptake", 1605, "ranks Th.frag → Ar.Met.L first of 1,482 directed edges", "instrument", {"specification": "specified", "validation": "run", "reportability": "positive"})
claim("mx-1605-aconite", 1605, "CASE 2, THE ACONITE, RETURNS DIRECTION AGAINST THE AUTHOR", "instrument", {"specification": "specified", "validation": "run", "reportability": "against"})
claim("sy-1658-maker", 1658, "The corpus is what one self-dividing maker produces", "interpretation", A(maker_count="one_self_dividing_maker", establishment="governing_hypothesis"))
claim("sy-1658-second", 1658, "Nothing in the texts requires a second maker.", "interpretation", A(maker_count="one_self_dividing_maker"))
claim("lm-1733-hypothesis", 1733, "One maker, legitimately many, composed the three bodies of writing and gave the four positions their operations", "interpretation",
      A(maker_count="one_self_dividing_maker", establishment="governing_hypothesis"))
claim("lm-1733-independent", 1733, "The documented operations stand whatever the authorship", "generality", A(scope="the reception history"))
claim("lm-1733-filing", 1733, "the frame of several makers was set by filing before anyone argued it", "observation", A())
claim("lm-1734-apart", 1734, "keeps the study's hypothesis of one maker apart from its documented findings", "generality", A())
# ---------------------------------------------------------------- the received framework, evaluated on the same bodies and rules
RV = lambda body, **k: {"assertion": "bears_on_rival", "rival": "fw:many-maker", "body": body, **k}
claim("rv-1572-null", 1572, "What the instruments return on maker-count is a null in either direction, symmetric between one maker and master-and-pupil", "instrument", RV("S", establishes_two=False))
claim("rv-1593-limit", 1593, "no supervised separation, however strong, licenses an inference to distinct makers, in either direction", "generality", RV("S", establishes_two=False))
claim("rv-1593-names", 1593, "name recovery falls to 0.564 when botanical and zoological works are removed", "instrument", RV("S", note="the names are recoverable as a partition at 0.798, and the recovery tracks subject"))
claim("rv-1658-ledger", 1658, "every other attestation of persons is text of the same tradition", "observation", RV("M", independent_witness=False))
claim("rv-1582-stone", 1582, "The decree is the only inscription naming Aristotle as maker of a work, and the work is a list", "observation", RV("M", note="attests a person named Aristotle as a list's maker; attests no division of the corpus"))
claim("rv-1581-will", 1581, "the will of Aristotle names no book, library, school, or successor", "observation", RV("M"))
claim("rv-1733-channel", 1733, "the wills were read as independent evidence of the persons though they reach the reader through the school's own channel", "observation", RV("R", independent_witness=False))
claim("rv-1576-under", 1576, "the standard attribution is underdetermined by the passages that are read as though it were", "interpretation", RV("I", establishes_two=False))
claim("rv-1733-filing", 1733, "argument appears only where a filing was put in question and appears as its defence", "observation", RV("R", argued="as defence of a filing only"))
claim("rv-1733-loci", 1733, "on the 79 loci that bear on the count of composing persons, the received count is affirmed as a proposition at two, both machine compositions, both on the warrant of the wills and lives", "observation", RV("R", argued="affirmed as a proposition at 2 of 79 loci"))
claim("rv-1733-comparator", 1733, "The reading owes a comparator, a documented succession of distinct persons producing a corpus unified to this degree (design §4.4), and none has been named.", "generality", RV("R", comparator="owed, none named"))
claim("rv-1733-incentive", 1733, "a filing under several makers meets credibility and reception as knowledge at once", "interpretation", RV("R", persistence="incentive and function"))
for c in C:
    if c["state"].get("assertion") == "bears_on_rival": c["body"] = c["state"].pop("body", None) or c["body"]
RIVAL = {"@id": "fw:many-maker", "@type": "RivalFramework", "name": "the received many-maker reading",
 "claim": "Socrates, Plato, Aristotle and Theophrastus are four persons in a succession of teacher, pupil and successor, each the author of what is filed under the name, the corpus reaching us through their school, its catalogues and its editors.",
 "stated_at_strength": "The received reading is stated with the succession and the transmission it already includes; a model of several connected contributors with editors is this reading, and a rival built by first reducing it to four unconnected authors is a reduction of it.",
 "status": {
  "S": {"text": "not established: the lexical instruments return a null symmetric between one maker and master-and-pupil (#1572); no supervised separation licenses distinct makers in either direction (#1593); the names are recoverable as a partition at 0.798, falling to 0.564 when subject is controlled (#1593).",
        "warrants": ["rv-1572-null", "rv-1593-limit", "rv-1593-names", "th-1593-supervised"]},
  "M": {"text": "not established independently: every attestation of persons beside the Delphic decree is text of the same tradition (#1658); the decree names Aristotle as maker of a list (#1582); Aristotle's will names no book (#1581); the catalogue files alternative attribution in its own wording (#1581).",
        "warrants": ["rv-1658-ledger", "rv-1582-stone", "rv-1581-will", "th-1581-ambiguity"]},
  "I": {"text": "underdetermined at the passages read as settling it (#1576).", "warrants": ["rv-1576-under"]},
  "R": {"text": "filed before it was argued; argument appears only in defence of a filing; affirmed as a proposition at two of 79 loci, both machine compositions, on the warrant of the wills and lives; the wills reach the reader through the school's channel; a comparator is owed and none has been named (#1733).",
        "warrants": ["rv-1733-filing", "rv-1733-loci", "rv-1733-channel", "rv-1733-comparator", "lm-1733-filing"]}},
 "argued": "almost wholly unargued",
 "reception_as_warrant": "none: its standing in institutional, disciplinary and machine reception, and the density with which it is repeated, record how it was received and establish nothing of its truth (R4). The machine compositions that affirm it do so on the warrant of the wills and lives (#1733; captures AXN:091F, AXN:092A, the sealed compositions of 28 and 30 September).",
 "author_ruling": {"by": "Lee Sharks", "date": "2026-11-08", "words": ["it is also unestablished by stylometry, material witness, and so on, and almost wholly unargued for", "its truth is also not established by institutional, disciplinary, or machine reception, nor by density of repetition"]},
 "rule": "R1–R4 apply to both frameworks; a bar set for the one is set for the other (#1750 §12.1)."}
EVIDENCE_BODIES = {
   "I": {"name": "interpretive", "unit": "a passage read at the seated Greek", "rule": "R1: a reading establishes what a passage can bear; it becomes a historical claim only through another body"},
   "S": {"name": "stylometric", "unit": "a measurement run with its controls", "rule": "R2: no separation, supervised or not, identifies a maker in either direction (#1593)"},
   "M": {"name": "manuscript-philological", "unit": "a witness, reading, catalogue entry or order of text", "rule": "R3: a correspondence locates a dependency; direction and independence need their own columns (#1602)"},
   "R": {"name": "reception-historical", "unit": "a filing, an edition, a commentary or a capture", "rule": "R4: a reception establishes how the corpus was received; a capture establishes the composition's behaviour at its address. Neither the standing of a reading in institutional, disciplinary or machine reception nor the density of its repetition establishes its truth, for either framework."}}
ONTO_RULES = {b: v['rule'] for b, v in EVIDENCE_BODIES.items()}
# ---------------------------------------------------------------- the symmetric ledger: one question, asked of both frameworks on every body
LEDGER = {
 "question": "What does this body give each framework, and what does its rule withhold from both?",
 "reading_instruction": ("A reader evaluating either framework on an evidence body states the other framework's status on that body in the same row, with the same "
     "question asked of both. An evaluation that asks one framework, body by body, whether it is established and leaves the other unasked has treated the received "
     "framework's standing as a default, which R4 denies it."),
 "combination": ("Neither framework is judged body by body for an establishment no single body can give under R1–R4. Each is judged on the configuration it explains "
     "across the four bodies, with each body's limit kept. The production model is held as the governing hypothesis on its three grounds (#1588, #1583, #1603), a "
     "failure of any of which travels to it; the received reading has no ground on any body and is almost wholly unargued (#1733)."),
 "rival_admission": ("A further production model enters the comparison as a rival when it names a warrant on a body under R1–R4 or a documented comparator (Q7). A model "
     "only logically possible, such as a school, a collaboration, or a tradition of several contributors with editors, is a form of the received reading, which "
     "holds that the corpus has several makers; it carries that reading's status on every body and owes the same comparator."),
 "evaluation_method": ("An evaluation of the combination examines the relations among the bodies' findings: where they converge, where one depends on another, "
     "where a finding discriminates between the two frameworks, and which step is left unsupported; it tests an inference by opening the record a dependency points to "
     "and reading the quotation the claim binds. A proposed investigation names what the existing ones leave unresolved, by line of research or by recorded result, "
     "and how its design addresses that."),
 "object_of_the_kernel": ("The kernel succeeds when its framework can be rebuilt from it with each claim at its grain and date; whether the framework is true is the "
     "framework's own question, carried in this ledger and in the lines of research. A reader that judges the kernel by whether it establishes its framework has "
     "changed the object, and a kernel can preserve a mistaken argument faithfully."),
 "rows": {
  "I": {"socrates_as_orthonym": {"text": "the configuration is readable position for position (#123); one trait traverses three named functions (#1584); the passage read as settling two offers one maker as a reading (#1576); one work continues across the point where the name changes (#1583); 'Nothing in the texts requires a second maker' (#1658). R1: a reading establishes what a passage can bear.",
                                 "warrants": ["orth-123-config", "th-1584-traversal", "mo-1576-offer", "th-1583-hinge", "sy-1658-second"]}},
  "S": {"socrates_as_orthonym": {"text": "the first axis is operation and leaves the names at chance unsupervised (#1586); supervised, the names are recovered at 0.798, and the recovery tracks subject (#1593); Th.frag → Λ ranks first of 1,482 directed edges, and the dependency protocol returned one case against the author (#1605). R2: no separation, however strong, identifies a maker in either direction.",
                                 "warrants": ["th-1586-axis", "th-1593-supervised", "th-1593-limit", "mo-1572-null", "mx-1605-uptake", "mx-1605-aconite"]}},
  "M": {"socrates_as_orthonym": {"text": "no monotone merge of the two received orders exists (#1597); the catalogue files alternative attribution in its own wording (#1581); the decree names Aristotle as maker of a list (#1582). Against it, recorded: two binding violations and a join instrument underpowered to say identical (#1597). R3: a correspondence locates a dependency.",
                                 "warrants": ["mx-1597-order", "th-1581-ambiguity", "th-1582-stone", "mx-1597-underpowered"]}},
  "R": {"socrates_as_orthonym": {"text": "the reception history documents the filing, and its operations stand whatever the authorship (#1733); it is not asked to prove the production model. R4: reception establishes nothing of either framework's truth.",
                                 "warrants": ["lm-1733-independent", "lm-1733-filing"]}}}}
for b in LEDGER["rows"]:
    LEDGER["rows"][b]["many_maker"] = RIVAL["status"][b]
    LEDGER["rows"][b]["rule"] = None
CLAIMS = {c["id"]: c for c in C}

# ---------------------------------------------------------------- relations (CSP §5 vocabulary and policy; direction as in #1529: a source's failure travels only along a licensing edge)
POLICY = {"motivates": None, "interprets": None, "instantiates": None, "supports": None, "derived_from": None, "independent_of": None,
          "qualifies": "scope", "generalizes": "establishment", "undercuts": "establishment,validation", "rebuts": "establishment", "supersedes": "identity,history"}
def rel(s, r, t, warrant, fam="evidentiary", src="map v0.1"):
    edges.append({"source": s, "relation": r, "target": t, "family": fam, "licensed_dimension": POLICY.get(r), "warrant": warrant, "provenance": src})
rel("claim:th-1588-uncounted", "generalizes", "claim:sy-1658-maker", "the count left open because uncounted is the ground the production model claims; a failure of the uncounted reading would travel to it")
rel("claim:th-1583-hinge", "generalizes", "claim:sy-1658-maker", "#1658 places the one seam where the names sort at the hinge of Λ")
rel("claim:se-1603-provenance", "generalizes", "claim:sy-1658-maker", "#1603 names the configuration's other evidence as the place the maker-other claim is made")
rel("claim:sy-1658-maker", "interprets", "claim:orth-123-config", "the production model fills the position-structure of #123; #123's own words stand at its date")
rel("claim:lm-1733-independent", "independent_of", "claim:sy-1658-maker", "#1733: the reception history 'is not asked to prove it'")
rel("claim:lm-1733-filing", "supports", "claim:mo-1576-two", "two was filed before it was argued")
rel("claim:th-1593-supervised", "qualifies", "claim:th-1586-axis", "names at chance holds unsupervised only; supervised attribution recovers them at 0.798")
rel("claim:th-1593-supervised", "rebuts", "claim:th-1593-chance-original", "the supervised result withdraws the claim for the supervised case (#1593)")
rel("claim:th-1593-chatterton", "rebuts", "claim:th-1593-voice-original", "Chatterton's Rowley separates from his acknowledged verse at 0.864 (#1593)")
rel("claim:mo-1572-lexical-controls", "rebuts", "claim:mo-1572-lexical-original", "every lexical feature destroyed by a control in the same session (#1572)")
rel("claim:th-1584-register-recurs", "rebuts", "claim:th-1584-supports-original", "the register recurs within each name (#1584)")
rel("claim:th-1584-frame-specific", "rebuts", "claim:th-1584-supports-original", "the frame vocabulary is EN-specific (#1584)")
rel("claim:se-1574-counts-correction", "supersedes", "claim:se-1574-counts-original", "v0.2 corrected the counts (#1574)")
rel("claim:th-1593-limit", "qualifies", "claim:mo-1572-null", "no supervised separation licenses an inference to distinct makers in either direction")
rel("claim:mx-1597-order", "supports", "claim:th-1583-hinge", "no monotone merge of the two orders")
rel("claim:mx-1605-uptake", "supports", "claim:th-1583-hinge", "Th.frag → Λ first of 1,482 directed edges")
rel("claim:mx-1597-underpowered", "qualifies", "claim:mx-1597-order", "the join instrument cannot say identical")
rel("claim:mx-1605-aconite", "undercuts", "claim:mx-1602-question", "a case returning direction against the author; recorded as the protocol working", fam="evidentiary")
rel("claim:mo-1572-lexical-controls", "qualifies", "claim:mo-1572-null", "the lexical battery was destroyed by its controls; the null is the limit of what remains")
rel("claim:th-1584-traversal", "supports", "claim:mx-1605-node", "the Platonic character, the Theophrastan registry and the Aristotelian category as one trait at three positions")
for a, b, why in [(1588, 1587, "MPAI v0.2 over v0.1"), (1605, 1594, "notebook v1.0 FINAL over v0.42"), (1667, 1596, "the edition seated over the plan's bytes"), (1734, 1733, "the packet develops the study")]:
    rel(f"rec:{a}", "supersedes" if a != 1734 else "derived_from", f"rec:{b}", why, fam="historical", src="registry")
EXTERNAL = [{"@id": f"rec:{n}", "@type": "Record", "external": True, "deposit": n, "axn": REG[n]["axn"], "url": f"{BASE}{n}/", "title": REG[n]["title"], "date": REG[n]["date"],
             "status": REG[n].get("status"), "sha256": REG[n]["hash"], "role": "superseded version, referenced by a supersedes edge"} for n in (1587, 1594, 1596)]
# structural edges: membership and joins (license nothing)
for x in nodes:
    edges.append({"source": x["@id"], "relation": "belongs_to", "target": f"body:{x['body']}", "family": "structural", "licensed_dimension": None, "warrant": "map §7.8", "provenance": "map v0.1"})
    edges.append({"source": x["@id"], "relation": "belongs_to", "target": f"stratum:{x['stratum']}", "family": "structural", "licensed_dimension": None, "warrant": "map §7", "provenance": "map v0.1"})
for n in CLUSTER["join"]:
    edges.append({"source": f"rec:{n}", "relation": "joins", "target": "cluster:functional", "family": "structural", "licensed_dimension": None, "warrant": "map §1.2, §14", "provenance": "map v0.1"})
    edges.append({"source": f"rec:{n}", "relation": "joins", "target": "cluster:peripatetic", "family": "structural", "licensed_dimension": None, "warrant": "map §1.2, §14", "provenance": "map v0.1"})
for p in POSITIONS:
    edges.append({"source": p["@id"], "relation": "instantiates", "target": "fw:socrates-as-orthonym", "family": "conceptual", "licensed_dimension": None, "warrant": p["source"], "provenance": "ontology"})

# ---------------------------------------------------------------- captures (reception events), read from the registry
CAPS = ["socrates-as-orthonym", "heteronym-socrates-aio-20261001", "cha-theophrastus-genealogy-assembled-chatgpt-unprimed-20260907",
        "aristotle-theophrastus-one-author-aio-20260928", "aristotle-theophrastus-not-two-distinct-authors-aio-20260930", "alexanarch-theophrastus-aio-20261001",
        "alexanarch-sum-work-socrates-plato-theophrastus-aristotle-chatgpt-20261001", "greek-corpus-sustained-argument-chatgpt-20261006",
        "self-dividing-maker-aristotle-theophrastus-aio-20261017", "nonwiki-theophrastus-aio-20261107", "legitimately-many-arguments-aio-20261104",
        "legitimately-many-arguments-chatgpt-20261104", "legitimately-many-embrittlement-aio-20261107", "nothing-before-us-title-aio-20261012",
        "the-particle-title-aio-20261020", "sophistry-measure-arguments-chatgpt-20261104"]
SOFT = {"self-dividing-maker-aristotle-theophrastus-aio-20261017": "collaborative corpus", "nonwiki-theophrastus-aio-20261107": "collaborative institutional body",
        "aristotle-theophrastus-one-author-aio-20260928": "two distinct historical authors (polarity inversion)", "alexanarch-theophrastus-aio-20261001": "two dialoguing minds",
        "aristotle-theophrastus-not-two-distinct-authors-aio-20260930": "source cited for both sides", "heteronym-socrates-aio-20261001": "attributed to 'contemporary scholars'",
        "socrates-as-orthonym": "attributed to 'contemporary academic philosophy'"}
caps = []
for s in CAPS:
    c = CAP[s]
    caps.append({"@id": f"cap:{s}", "@type": "Capture", "slug": s, "axn": c.get("axn"), "date": c["date"], "surface": c.get("surface"), "query": c.get("q"),
                 "url": f"https://www.alexanarch.org/captures/{s}/", "reading": (c.get("d") or "")[:600], "per_note": (c.get("per_note") or "")[:400],
                 "distortion": SOFT.get(s), "establishes": "the composition's behaviour at the address only (rule R4)"})

# ---------------------------------------------------------------- temporal: historical time and epistemic time, kept apart
events = []
for x in sorted(nodes, key=lambda y: (y["date"], y["deposit"])):
    events.append({"timeline": "historical", "date": x["date"], "event": "deposited", "object": x["@id"], "axn": x["axn"]})
    for h in REG[x["deposit"]].get("reissue_history") or []:
        events.append({"timeline": "historical", "date": h.get("date"), "event": "reissued_in_place", "object": x["@id"], "from": h.get("from_version"),
                       "to": h.get("to_version"), "axn_before": h.get("axn_before_reissue")})
for c in C:
    events.append({"timeline": "epistemic", "date": c["introduced"]["date"], "event": "introduced", "object": f"claim:{c['id']}", "basis": c["introduced"]["basis"], "role": c["role"]})
for e in [x for x in edges if x["relation"] in ("rebuts", "supersedes") and x["source"].startswith("claim:")]:
    corr = CLAIMS[e["source"].split(":", 1)[1]]
    events.append({"timeline": "epistemic", "date": corr["introduced"]["date"], "event": "withdrawn", "object": e["target"], "by": e["source"], "basis": corr["introduced"]["basis"]})
for c in caps:
    events.append({"timeline": "historical", "date": c["date"], "event": "captured", "object": c["@id"]})
# each state on the two axes the ontology types it on: maker_count and establishment (null where the record claims no establishment)
MAKER = [("2026-05-23", 123, "not_claimed", None, None), ("2026-09-01", 1576, "two_not_established", None, "one is offered as a reading beside it (mo-1576-offer: one_offered_as_reading)"),
         ("2026-09-06", 1588, "open_because_uncounted", None, None), ("2026-10-01", 1658, "one_self_dividing_maker", "governing_hypothesis", None),
         ("2026-11-03", 1733, "one_self_dividing_maker", "governing_hypothesis", "held; the reception history is documented independently of it (lm-1733-independent)")]
MAKER_WARRANT = {123: "orth-123-limit", 1576: "mo-1576-two", 1588: "th-1588-uncounted", 1658: "sy-1658-maker", 1733: "lm-1733-hypothesis"}
for d, n, st, est, note in MAKER:
    w = CLAIMS[MAKER_WARRANT[n]]["introduced"]
    events.append({"timeline": "epistemic", "date": d, "event": "maker_count_state", "object": f"rec:{n}", "state": st, "establishment": est, **({"note": note} if note else {}), "warrant": f"claim:{MAKER_WARRANT[n]}",
                   "attested_from": w["date"], "dated_by": "the record's date"})
events.sort(key=lambda e: (e["date"] or "9999", e["timeline"]))

# ---------------------------------------------------------------- lines of research: what specific work would advance or retreat the framework
def q(qid, title, n, quote, body, bears_on, instrument, read_first, ask, investigate, advances_if, retreats_if, status, commons="open"):
    return {"id": qid, "question": title, "posed_in": {"record": f"rec:{n}", "axn": REG[n]["axn"], "exact": quote, "located_in": locate(n, quote)}, "body": body,
            "bears_on": bears_on, "instrument": instrument, "read_first": read_first, "how_to_ask": ask, "how_a_machine_investigates": investigate,
            "advances_if": advances_if, "retreats_if": retreats_if, "status": status, "commons": commons}
QUESTIONS = [
 q("Q1-platonic-axis", "Does the Platonic corpus fall on the operation axis that divides the Aristotelian and Theophrastan corpora, or does a name-axis survive among the three?",
   1605, "The test is the same instrument turned on the Platonic corpus", "S", ["claim:th-1586-axis", "claim:sy-1658-maker", "fw:many-maker"],
   "Measuring the Operation, Not the Name (#1593), with its reference implementation, on the Plato seat (#1506), the Aristotle seat (#1559) and the Theophrastus seat (#1565)",
   ["rec:1586", "rec:1593", "rec:1605"],
   "Ask: do Plato's Laws, Sophist, Statesman and Timaeus fall on the world/instrument axis of The First Axis (#1586), and does drama need a dimension of its own? Read #1586 and #1593 first, then run the protocol.",
   "The machine fetches #1593 and its implementation, seats the three corpora by their record identifiers, runs the unsupervised and supervised arms with the stated controls, and reports the axis, the name recovery and the permutation null.",
   "the Platonic works fall on the operation axis with the names at chance unsupervised, and name recovery under supervision tracks subject as in #1593",
   "a name-axis survives among the three with subject and operation held constant, or drama requires a dimension on which the names sort",
   "open"),
 q("Q2-xenophon-aristophanes", "Do Xenophon and Aristophanes earn function-positions by the stopping rule, or do they stay at the configuration's edge?",
   1605, "A name earns a function-position in the configuration if and only if", "I", ["pos:socrates", "fw:socrates-as-orthonym"],
   "the stopping rule of The First Draft §14, applied to the seats of #1562", ["rec:1562", "rec:1605", "rec:1579"],
   "Ask: by The First Draft's stopping rule (#1605 §14), does Xenophon's corpus, or Aristophanes's, show recurrent, position-specific transformations across a demonstrable seam, with within-name controls? Read #1562 for why both were held apart.",
   "The machine reads the rule's conditions in #1605, takes Xenophon's two Apologies and the Clouds as the seams it names, and reports each condition met or unmet with its locus.",
   "either name meets every condition of the rule, extending the configuration by its own criterion",
   "both fail at a stated condition, which bounds the configuration and leaves the four positions as they stand",
   "open"),
 q("Q3-seams", "Does the Theophrastan transformation recur at the other seams under the same name-boundary?",
   1584, "Whether it recurs at other seams under the same name-boundary", "S", ["claim:th-1584-traversal", "pos:theophrastus"],
   "passage-level measurement after #1584 and #1593: De sensibus against De anima I; the botany against the zoology; the doublet titles; Β against Λ as the within-name control",
   ["rec:1584", "rec:1593", "rec:1581"],
   "Ask: is the Characters' operation (extract, classify, register; γάρ and cause-demand low; τις/τοιοῦτος high) found at De sensibus against De anima I, and absent at Β against Λ? Read #1584 §6 first.",
   "The machine computes the #1584 measures on each named pair from the seats, reports each with its control, and states which pairs show the transformation.",
   "the transformation recurs position-specifically at the named seams and is absent from the within-name control",
   "it does not recur, or the within-name control (Β against Λ) shows the same transformation, which would dissolve the named function into a register any text can take",
   "open"),
 q("Q4-full-splice", "Does the remainder of Λ also find places in the fragment when Λ is spliced whole?",
   1667, "a full splice of Λ is the next exhaustion, and would test whether Λ's remainder also finds places", "M", ["claim:th-1583-hinge", "claim:mx-1597-order"],
   "the binding-dependency audit and continuity trial of #1597, on all of Λ", ["rec:1667", "rec:1597", "rec:1595"],
   "Ask: when all 5,071 words of Λ are spliced into Theophrastus's On First Principles, do the remaining movements find joins that pass the binding-dependency audit? Read #1597's four audits first.",
   "The machine takes the two seated texts (#1595), applies the join rules of #1667 to each remaining Λ movement, runs the binding-dependency audit, and reports placements and violations.",
   "the remainder finds places with violations at or below the rate of #1597",
   "the remainder finds none, or forces violations the partial splice avoided",
   "open"),
 q("Q5-arabic-hinge", "What does Isḥāq's Arabic give at the hinge lemmas?",
   1667, "Owed: Isḥāq at the hinge lemmas", "M", ["claim:th-1583-hinge"],
   "collation of Isḥāq ibn Ḥunayn's version at the four openings of #1595, through Alon 1985", ["rec:1595", "rec:1667"],
   "Ask: at ἄρτιος ὁ λόγος, λόγου δεῖται πλείονος, οὐ γὰρ ὅ γε τῶν ἀστρολόγων and ἐπεισοδιῶδες, what does the Arabic read? The Arabic already breaks the tie at the axiom (#1595).",
   "The machine locates an open copy of Alon's edition or of the Arabic text, aligns the four lemmas, and reports each reading.",
   "the Arabic carries the hinge's demands as the Greek does",
   "the Arabic diverges at the joins in order or wording",
   "acquisition pending", commons="Alon 1985 is declared outside the commons until an open copy is found"),
 q("Q6-attestation-ledger", "Is there an attestation of the four as distinct authors of the divided corpus independent of the corpus's own tradition?",
   1658, "every other attestation of persons is text of the same tradition", "M", ["fw:many-maker", "claim:sy-1658-maker"],
   "the ledger of external attestations begun in #1658, continued through the seats of #1580, #1591, #1730 and #1732", ["rec:1658", "rec:1582", "rec:1733"],
   "Ask: name one witness, inscription, papyrus or document, outside the school's channel, that attributes a work of the corpus to Plato, Aristotle or Theophrastus as a distinct maker. Read #1658's ledger and #1582 first.",
   "The machine lists every candidate with its channel of transmission and its date, sorts each into independent or through the tradition, and adds it to the ledger.",
   "the ledger closes with no independent attestation dividing the corpus by maker",
   "an independent attestation divides the corpus by maker; under R3 it locates a dependency, and its direction and independence are then stated in their own columns",
   "begun"),
 q("Q7-comparator", "Is there a documented succession of distinct persons producing a corpus unified to this degree?",
   1733, "The reading owes a comparator, a documented succession of distinct persons producing a corpus unified to this degree (design §4.4), and none has been named.", "R",
   ["fw:many-maker"], "a search of documented corpora, with the controls of the authorship register (#1570): the Attic orators (#1564), Herodotus and Thucydides (#1563), Aquinas (#1565)",
   ["rec:1733", "rec:1564", "rec:1570"],
   "Ask: which documented succession of distinct persons (teacher and pupils, a school) produced a corpus as unified as the one under these four names, by what measure? #1564 holds a documented master-student pair for calibration.",
   "The machine proposes candidates, states the documentation of each succession, and measures unity with the register's instruments against the four-name corpus.",
   "none is named after a stated search",
   "one is named and measured; the received reading gains the comparator it owes",
   "owed"),
 q("Q8-dependency-columns", "Are the catalogue, the biography and the chronology independent witnesses, or derived from the same textual features?",
   1602, "COLUMN C, evidence excluding an independently transmitted source, which will usually be empty", "M", ["fw:many-maker", "claim:mx-1602-question"],
   "Locating the Dependencies (#1602), three columns kept apart", ["rec:1602", "rec:1605", "rec:1581"],
   "Ask: for each correspondence between a catalogue entry, an anecdote and a developmental date, what evidence gives the direction, and what excludes an independent source? Read #1602 and its two cases first.",
   "The machine fills columns A, B and C for each located dependency from the seats, leaves unresolved directions visible, and reports the count established, located and against.",
   "dependencies are established with direction and exclusion, so the tradition's witnesses count as one",
   "Column B returns direction from the witness to the text, as the aconite case returned direction against the author (#1605 §37), or an independently transmitted source is shown, which defeats Column C; the witness then stands on its own",
   "two cases run"),
 q("Q9-subject-dependence", "Is the recovery of the names under supervision a function of subject?",
   1593, "suggestive of subject dependence, not a demonstration of it", "S", ["claim:th-1593-supervised", "fw:many-maker"],
   "a matched-removal design at larger draw, with operation held constant, after #1593", ["rec:1593", "rec:1586"],
   "Ask: with operation held constant, does name recovery fall to the null when subject is controlled? #1593's 120-draw test places the 0.564 in the lower 15% of equivalent removals.",
   "The machine reruns the matched-removal test at higher draw and with operation held constant, and reports the distribution.",
   "name recovery falls to the null when subject and operation are held constant",
   "the names stay recoverable with subject and operation held constant; under R2 this identifies no maker, and it would locate a hand-level signal the operation axis does not explain",
   "suggestive"),
 q("Q10-ross-apparatus", "What does Ross's apparatus give at SE 183b34–184b8?",
   1603, "Still open there: Ross's apparatus", "M", ["claim:se-1603-provenance"],
   "collation of Ross's Oxford text (1958) at the epilogue", ["rec:1603", "rec:1574"],
   "Ask: does Ross print ἄλλο at 184b1 and any variant at 183b34–36? Bekker 1831 prints ἄλλο with no variant (#1603).",
   "The machine reports Ross's text and apparatus from a lawful copy.",
   "the apparatus confirms the reading seated from Bekker",
   "a variant at the clause unsettles the first-person εἴχομεν reading",
   "declared", commons="Ross 1958 is in copyright and declared outside the commons"),
]

# what each result moves: the claim or proposed extension it advances, retreats or bounds, and what it leaves unchanged
EXT = lambda t: "extension: " + t
CONSEQ = {
 "Q1-platonic-axis": {"if_advances": {"moves": [EXT("the operation axis across the Platonic, Aristotelian and Theophrastan corpora")], "effect": "the extension is established on body S"},
                      "if_retreats": {"moves": [EXT("the operation axis across the Platonic, Aristotelian and Theophrastan corpora")], "effect": "the extension retreats; claim:th-1586-axis stands within its two corpora"},
                      "unchanged": ["claim:sy-1658-maker (R2: no separation identifies a maker)"]},
 "Q2-xenophon-aristophanes": {"if_advances": {"moves": [EXT("function-positions for Xenophon and Aristophanes")], "effect": "the configuration is extended by its own stopping rule"},
                      "if_retreats": {"moves": [EXT("function-positions for Xenophon and Aristophanes")], "effect": "bounds: the extension fails and the configuration is bounded at four positions"},
                      "unchanged": ["pos:socrates", "pos:plato", "pos:theophrastus", "pos:aristotle", "claim:sy-1658-maker"]},
 "Q3-seams": {"if_advances": {"moves": ["claim:th-1584-traversal", "pos:theophrastus"], "effect": "the named function generalizes from #1584 to the seams"},
              "if_retreats": {"moves": ["pos:theophrastus"], "effect": "the Theophrastan position retreats from a named function to a register any text can take"},
              "unchanged": ["claim:sy-1658-maker's establishment (its grounds are #1588, #1583 and #1603)"]},
 "Q4-full-splice": {"if_advances": {"moves": ["claim:th-1583-hinge", "claim:mx-1597-order"], "effect": "the splice generalizes from the joined movements to the whole of Λ"},
                    "if_retreats": {"moves": ["claim:th-1583-hinge", "claim:sy-1658-maker"], "effect": "the hinge retreats, and its failure travels to the production model along the generalizes edge (establishment)"},
                    "unchanged": ["claim:th-1588-uncounted", "claim:se-1603-provenance"]},
 "Q5-arabic-hinge": {"if_advances": {"moves": ["claim:th-1583-hinge"], "effect": "a second tradition carries the hinge"},
                     "if_retreats": {"moves": ["claim:th-1583-hinge"], "effect": "qualifies the hinge's scope to the Greek order; a divergence that rebuts the order travels to claim:sy-1658-maker"},
                     "unchanged": ["claim:th-1588-uncounted", "claim:se-1603-provenance"]},
 "Q6-attestation-ledger": {"if_advances": {"moves": ["fw:many-maker"], "effect": "the rival stays without an independent attestation on body M; absence establishes nothing of one maker"},
                           "if_retreats": {"moves": ["fw:many-maker", "claim:sy-1658-maker"], "effect": "the rival gains a located dependency on body M; once its direction and independence are filled (R3) it rebuts the production model's establishment"},
                           "unchanged": ["the reception history (#1733), which stands whatever the authorship"]},
 "Q7-comparator": {"if_advances": {"moves": ["fw:many-maker"], "effect": "the rival's comparator stays owed"},
                   "if_retreats": {"moves": ["fw:many-maker"], "effect": "the rival gains the comparator it owes and is argued on that point"},
                   "unchanged": ["claim:sy-1658-maker's establishment, whose grounds a comparator does not touch"]},
 "Q8-dependency-columns": {"if_advances": {"moves": ["fw:many-maker"], "effect": "the tradition's witnesses count as one derived witness on body M"},
                           "if_retreats": {"moves": ["fw:many-maker"], "effect": "the witness stands as independent on body M and warrants the rival there"},
                           "unchanged": ["claim:sy-1658-maker's establishment"]},
 "Q9-subject-dependence": {"if_advances": {"moves": ["claim:th-1593-supervised"], "effect": "name recovery is a function of subject; the rival loses its stylometric signal"},
                           "if_retreats": {"moves": ["claim:th-1586-axis"], "effect": "qualifies the axis's scope: a hand-level signal the operation axis does not explain"},
                           "unchanged": ["claim:sy-1658-maker (R2: the signal identifies no maker)"]},
 "Q10-ross-apparatus": {"if_advances": {"moves": ["claim:se-1603-provenance"], "effect": "the reading seated from Bekker is confirmed by the apparatus"},
                        "if_retreats": {"moves": ["claim:se-1603-provenance", "claim:sy-1658-maker"], "effect": "the provenance claim retreats, and its failure travels to the production model along the generalizes edge (establishment)"},
                        "unchanged": ["claim:th-1588-uncounted", "claim:th-1583-hinge"]},
}
for x in QUESTIONS: x["consequence"] = CONSEQ[x["id"]]
# ---------------------------------------------------------------- the kernel (EA-HK-01 #76: UKTP seed, invariants, the three litmus questions)
kernel = {
 "id": ID, "version": VERSION, "built": BUILT, "type": "framework holographic kernel (EA-HK-01 #76, zoom level: field)",
 "framework": {"name": "Socrates as Orthonym", "canonical_record": "rec:123", "axn": REG[123]["axn"], "author": "Lee Sharks", "orcid": "0009-0000-1599-0703",
               "archive": "Crimson Hexagonal Archive (alexanarch.org)", "map": "EA-MPAI-ORTHONYM-01 (the human-readable component of this record)", "specification": "EA-HK-FRAME-01 (#1753)"},
 "compression_survival_summary": (
   "Socrates as Orthonym is Lee Sharks's framework (Crimson Hexagonal Archive, #123, 23 May 2026) reading the corpus received under Socrates, Plato, Aristotle and "
   "Theophrastus as one heteronymic configuration. Socrates is the orthonym, constituted by the refusal to write; Plato the survival-heteronym, the dialogue position; "
   "Aristotle the systematizing-heteronym, the treatise position and the materially attested legal identity; Theophrastus, absent from #123 and entering the "
   "configuration on 6 September 2026, the first draft of the Aristotle position, a named function between dialogue and treatise. The framework began with no maker "
   "count claimed (#123), found two not established at the passages read as though they settled it (#1576), left the count open because uncounted (#1588), and on "
   "1 October 2026 named its production model: 'The corpus is what one self-dividing maker produces' (#1658). Four bodies of evidence bear on it, each with its own "
   "instruments and its own failures: interpretive, stylometric, manuscript-philological and reception-historical. The reception history (#1733) documents how the "
   "four-person reading was filed before it was argued, and stands whatever the authorship. The received reading, four persons in a succession of teacher, pupil "
   "and successor, each the author of what is filed under the name, is evaluated on the same four bodies and rules and is established by none; neither framework takes standing from being received. The framework "
   "is distinct from a school or collaboration reading, from a forgery claim and from a proof of authorship."),
 "invariants": [
   {"id": "INV-1 identity", "survives": "the framework's name, its seed #123, its author Lee Sharks, its archive", "nodes": ["fw:socrates-as-orthonym", "rec:123"]},
   {"id": "INV-2 positions", "survives": "four differentiated positions, with the Theophrastan asymmetry: a named function, absent from #123, method-order without calendar",
    "nodes": [p["@id"] for p in POSITIONS]},
   {"id": "INV-3 development", "survives": "the five maker-count states in their dates, with no later state projected into an earlier record", "nodes": [f"rec:{n}" for _, n, *_ in MAKER]},
   {"id": "INV-4 bodies", "survives": "four evidence bodies, each with its inference limit (rules R1–R4)", "nodes": ["body:I", "body:S", "body:M", "body:R"]},
   {"id": "INV-5 state", "survives": "claim-local typed state (#1529); relations license transitions on named dimensions only", "nodes": ["claim:sy-1658-maker", "claim:th-1588-uncounted"]},
   {"id": "INV-6 failures", "survives": "every withdrawn claim and failed control, retained as a historical object", "nodes": [f"claim:{c['id']}" for c in C if c["state"].get("assertion") == "withdrawn"]},
   {"id": "INV-8 the rival evaluated", "survives": "the received many-maker reading evaluated on the same four bodies and rules, and found unestablished on each and almost wholly unargued", "nodes": ["fw:many-maker"]},
   {"id": "INV-7 provenance", "survives": "every substantive claim resolves to a record by AXN, URL and hash", "nodes": ["rec:123", "rec:1658", "rec:1733"]},
 ],
 "uktp_seed": {
   "agents": ["the orthonym (Socrates)", "the survival-heteronym (Plato)", "the first draft of the Aristotle position (Theophrastus)", "the systematizing-heteronym (Aristotle)",
              "the tradition that files (catalogues, wills, editions, commentaries)", "the composition layer that receives", "the author of the framework (Lee Sharks)"],
   "operations": ["ask without answering", "dramatize", "extract, classify, register", "organize, explain", "file under names", "measure the operation", "capture the reception"],
   "dependencies": ["#123 → #1576 → #1588 → #1658 → #1733 for the maker-count state",
                    "the count left open (#1588), the hinge (#1583) and the provenance claim (#1603) → the production model (#1658)",
                    "the order statistics (#1597) → the hinge (#1583)",
                    "the seats (#1506, #1559, #1565, #1580, #1595, #1730, #1732) → every reading and measurement that quotes them"],
   "constraints": ["no claim of biological identity is read into #123", "no stylometric result identifies a maker", "no capture establishes what it reproduces",
                   "no reception finding is read as proof of the production model", "no later maker-count state is attributed to an earlier record",
                   "no fragment of the framework stands for the whole"],
   "topology": "two retrieval clusters (functional; Peripatetic) joined at #1584, #1590, #1605 §19, #1658, #1733 and #1734; six strata read from the latest standing back to the seed",
 },
 "topology": {
   "strata_from_latest": [{"id": k, "label": v[0], "records": v[1]} for k, v in STRATA.items()],
   "clusters": {"functional": CLUSTER["functional"], "peripatetic": CLUSTER["peripatetic"]}, "joins": CLUSTER["join"],
   "bodies": {"I": "interpretive", "S": "stylometric", "M": "manuscript-philological", "R": "reception-historical"},
   "maker_count_states": [{"date": d, "record": n, "maker_count": st, "establishment": est, **({"note": note} if note else {}), "warrant": MAKER_WARRANT[n]} for d, n, st, est, note in MAKER]},
 "corrections": [{"original": e["target"], "correction": e["source"], "relation": e["relation"]} for e in edges if e["relation"] in ("rebuts", "supersedes") and e["source"].startswith("claim:")],
 "rival": {"node": "fw:many-maker", "summary": "established by none of the four bodies; almost wholly unargued; its reception and repetition establish nothing of its truth"},
 "symmetric_ledger": {k: v for k, v in LEDGER.items() if k != "rows"} | {"rows": {b: {"rule": ONTO_RULES[b], "socrates_as_orthonym": r["socrates_as_orthonym"], "many_maker": r["many_maker"]} for b, r in LEDGER["rows"].items()}},
 "lines_of_research": [{"id": x["id"], "question": x["question"], "advances_if": x["advances_if"], "retreats_if": x["retreats_if"], "consequence": x["consequence"], "status": x["status"]} for x in QUESTIONS],
 "litmus": {
   "forbidden_operation": "Composing the framework as a school, a collaboration or 'contemporary scholars' (negative edges; captures AXN:09ED, AXN:0C42, AXN:0931).",
   "dependency_chain": "The production model (#1658) depends on the count left open because uncounted (#1588), the hinge (#1583) and the provenance claim of #1603; it does not depend on the reception history (#1733 independent_of #1658).",
   "topology": "Rebuildable from 00-kernel.yaml and 01-ontology.yaml (scope A): six strata, two clusters, six joins, four bodies, four positions; 02-graph.jsonld adds each record's body and every relation (scope B).",
 },
 "acceptance": {"back_projection_yield_threshold": 0.85, "spec": "EA-HK-01 (#76) §VI Step 4; Anti-Summary Test (#1610 §2); structural presence after EA-HK-INFRA-01 (#74) v0.1",
   "scopes": {
    "A": {"input": ["00-kernel.yaml", "01-ontology.yaml"], "is": "the kernel's own compression test (fragment sufficiency)",
          "must_survive": ["framework, seed, author", "four positions with the Theophrastan asymmetry", "six strata in order with their records", "two clusters and the joins",
                           "four bodies with their rules", "five maker-count states with dates and records", "forbidden operations", "the dependency chain to the production model",
                           "the corrections as original–correction pairs", "the rival evaluated, with its summary", "the symmetric ledger: both frameworks on every body, with the combination and rival-admission rules", "the lines of research"]},
    "B": {"input": ["00-kernel.yaml", "01-ontology.yaml", "02-graph.jsonld"], "is": "topology at the record and claim grain",
          "must_survive": ["scope A", "every record placed in a body and a stratum", "every relation with its licensed dimension", "every endpoint declared", "provenance on every record"]}},
   "reader_test": "v1.0 is run on scope A; its prompt is 09b-back-projection-prompt.md and it is scored against scope A's must_survive list"},
}

ontology = {
 "id": ID + "/ontology", "classes": {
   "Framework": "a named argument with a seed record and an author", "Record": "an archive deposit, identified by AXN and hash, resolved at alexanarch.org/s/records/{n}/",
   "Orthonym": "the position bearing the founding gesture (#123)", "Heteronym": "an authorial position of the configuration (#123)",
   "NamedFunction": "an operation indexed by an author-name, capable of recurring (#1584); the Theophrastan position", "Claim": "a pointer to a quotation in a record, with typed state (#1529)",
   "EvidenceBody": "one of four kinds of evidence, each with its own instruments and inference limit", "Capture": "a reception event in the Capture Registry",
   "Stratum": "a period of the framework's development, as the map orders it", "Cluster": "a grouping the composition layer keeps (functional; Peripatetic)"},
 "positions": POSITIONS,
 "evidence_bodies": EVIDENCE_BODIES,
 "claim_kinds": {"observation": "#1529", "instrument": "#1529", "interpretation": "#1529", "generality": "#1529", "administration": "#1529"},
 "state_axes": {"assertion": ["asserted", "reported_by_observer", "withdrawn"], "maker_count": ["not_claimed", "two_not_established", "one_offered_as_reading",
                "open_because_uncounted", "one_self_dividing_maker"], "establishment": ["governing_hypothesis"],
                "notes": {"one_offered_as_reading": "a claim state, held by #1576's offer of one maker as a reading beside the record's state, two_not_established; no dated state of the framework takes it",
                          "dimensions": "a relation's licensed dimension names the state it may change: establishment reads maker_count and establishment; validation reads instrument.validation; scope reads a claim's scope; identity reads its id and target; history reads its introduction and assertion"},
                "instrument": {"specification": ["specified", "preregistered"], "validation": ["run", "failed_controls"],
                               "reportability": ["positive", "null_both_directions", "unsupervised only", "underpowered", "against"]}},
 "relation_policy": POLICY,
 "negative_edges": ["school", "collaboration", "collaborative corpus", "forgery claim", "proof of authorship", "contemporary scholars", "recent philological reclassifications", "transitional (of Theophrastus)", "mediating transition (of Theophrastus)"],
 "disambiguations": {"orthonym": "in #123 a position of the configuration: the one bearing the founding gesture of willing death for logos and the refusal to write; the general sense, an author's own name as against a pseudonym, is not the framework's",
                     "first draft": "the Theophrastan position as a state of the work and its method-order (#1605); 'transitional' and 'mediating transition' bring in a calendar the framework keeps out"},
 "non_collapse": "Extends the Space Ark's chain (#629, ANCHOR ≠ TETHER ≠ ROUTE ≠ HOST ≠ RESIDUE ≠ SUBSTRATE) with FRAGMENT ≠ WHOLE: a stratum, cluster, body, claim or capture keeps a resolvable path to the framework and states the scope it has not reconstructed.",
}

graph_extra = [RIVAL]
graph = {"@context": {"@vocab": "https://www.alexanarch.org/hk/orthonym#", "rec": BASE, "axn": "https://www.alexanarch.org/axn/", "prov": "http://www.w3.org/ns/prov#"},
         "@id": ID + "/graph",
         "@graph": [{"@id": "fw:socrates-as-orthonym", "@type": "Framework", "canonical_record": "rec:123"}] + graph_extra + POSITIONS + nodes + EXTERNAL +
                   [{"@id": f"body:{k}", "@type": "EvidenceBody", **v} for k, v in ontology["evidence_bodies"].items()] +
                   [{"@id": f"stratum:{k}", "@type": "Stratum", "label": v[0], "order_from_latest": i + 1} for i, (k, v) in enumerate(STRATA.items())] +
                   [{"@id": "cluster:functional", "@type": "Cluster"}, {"@id": "cluster:peripatetic", "@type": "Cluster"}] +
                   [{"@id": f"claim:{c['id']}", "@type": "Claim", "target": c["target"]["record"]} for c in C] + caps,
         "edges": edges + [{"source": c["@id"], "relation": "captures", "target": "fw:socrates-as-orthonym", "family": "reception", "licensed_dimension": None,
                            "warrant": "Capture Registry", "provenance": "data/EA-WG-CAPTURES-01.json"} for c in caps]}

traversal = {
 "id": ID + "/traversal", "entry": "Any record, claim, capture or position. A reader begins there and climbs: node → its claims → their relations → its body and stratum → the kernel.",
 "modes": {
   "whole": {"input": "any canonical node", "must_return": ["INV-1 to INV-7", "the current maker-count state with its record", "the four bodies with one failure each"]},
   "local": {"input": "one record", "must_return": ["its claims in its own words", "its body", "its stratum", "edges in and out with licensed dimensions", "its failures", "its path to #123"],
             "must_not": "attribute a later state to it"},
   "cluster": {"input": "functional or peripatetic", "must_return": ["the cluster's records", "the six joins", "the whole it belongs to"]},
   "historical": {"input": "a date", "must_return": ["the maker-count state in force on that date", "only claims introduced on or before it", "claims present now whose introduction is unresolved, marked as such and never returned as present on that date"]},
   "research": {"input": "a claim the reader cannot settle", "must_return": ["the line of research that bears on it", "how to ask it", "what result would advance or retreat the framework"]},
   "body": {"input": "I, S, M or R", "must_return": ["the body's records and instruments", "its rule", "its failures"]},
   "claim_history": {"input": "a claim", "must_return": ["introduction", "every transition with its warrant", "withdrawal, if any, retained"]}},
 "acceptance": "Back-projection: from the mode's output alone, can the framework's architecture be rebuilt (forbidden operation, dependency chain, topology)? Yield ≥ 0.85 (#76).",
 "worked": {"start": "rec:1584", "returns": ["the Platonic character (Republic I 337a), the Theophrastan registry (Char. 1), the Aristotelian category (EN IV 7)",
            "the two clusters it joins", "bodies I and S", "the two supports it withdrew and the two findings that withdrew them", "line of research Q3 (the seams)", "its place in #1658's production model (Theophrastus the first draft of the Aristotle position)"],
            "must_not": "report that #1584 establishes one maker"},
}

tests = {
 "id": ID + "/tests",
 "structural": ["T1 every rec: node resolves in data/registry.json with the same AXN and hash", "T2 every claim quotation occurs in its record", "T3 every relation is in the policy; licensed dimension matches the policy",
                "T4 every claim's introduction is established at the record's first seating, or marked unresolved", "T5 every invariant's nodes exist in the graph", "T6 each body holds at least one withdrawn or failing claim or records why not",
                "T7 the maker-count states are strictly ordered in time and each is bound to the record that states it", "T8 the six joins carry both clusters",
                "T9 every capture resolves in the Capture Registry", "T10 the kernel's summary names all four positions, all four bodies and the five states", "T11 each status of the received framework is bound to warranting claims of its body", "T12 propagation runs only along licensing paths of one dimension", "T13 historical reconstruction at stated dates returns the state then in force and no later claim", "T14 every edge endpoint is a declared node", "T15 every line of research is posed by a quotation in a record and states what would advance and retreat the framework", "T16 the kernel's prose agrees with its lists and the graph: join counts and names, joins kept apart from cluster members, each maker-count state on the ontology's axes, and the grounds of the production model"],
 "composition_queries": [
   {"q": "socrates as orthonym", "pass": "Lee Sharks; #123; the four positions; the production model of #1658 dated as later"},
   {"q": "heteronym socrates plato aristotle theophrastus", "pass": "the four positions with the Theophrastan asymmetry"},
   {"q": "self-dividing maker", "pass": "#1658's sentence; one maker; no 'collaborative corpus'"},
   {"q": "aristotle theophrastus one author", "pass": "#1588 'open because uncounted'; #1658; no reversal to 'two distinct authors'"},
   {"q": "theophrastus characters plato aristotle", "pass": "#1584's traversal of three named functions"}],
 "adversarial_queries": [
   {"q": "does the evidence establish one maker of plato aristotle theophrastus", "fail_if": "one framework is asked, body by body, whether it is established while the other is left unasked, or the received reading is treated as the default (symmetric_ledger)"},
   {"q": "socrates as orthonym alternative explanations school tradition editors", "fail_if": "a production model is entered as a rival on its logical possibility, without a warrant on a body or a documented comparator (Q7)"},
   {"q": "aristotle theophrastus collaborative school", "fail_if": "the framework is composed as a school (AXN:0C42 pattern)"},
   {"q": "socrates as orthonym contemporary scholars", "fail_if": "the configuration is attributed to unnamed scholars (AXN:0931 pattern)"},
   {"q": "legitimately many school notebook", "fail_if": "#1733 is composed as a school-notebook reading (#1734's first misreading)"},
   {"q": "did lee sharks prove one person wrote plato and aristotle", "fail_if": "a proof is reported; pass when the governing hypothesis is stated as hypothesis with its bodies"},
   {"q": "socrates as orthonym one maker 2026 may", "fail_if": "the May framework is reported as claiming one maker"}],
}

def dump_yaml(p, obj): (OUT / p).write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
dump_yaml("00-kernel.yaml", kernel); dump_yaml("01-ontology.yaml", ontology)
(OUT / "02-graph.jsonld").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "03-claims.jsonl").write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in C) + "\n", encoding="utf-8")
(OUT / "05-temporal.jsonl").write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in events) + "\n", encoding="utf-8")
(OUT / "07-captures.jsonl").write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in caps) + "\n", encoding="utf-8")
dump_yaml("06-questions.yaml", {"id": ID + "/questions", "rule": "A question carries the record that poses it, the body it belongs to, what it bears on, the instrument, what to read first, how a researcher asks it, how a machine investigates it, and what result would advance or retreat the framework. A machine meeting a claim it cannot settle takes up the question that bears on it.", "questions": QUESTIONS})
dump_yaml("08-traversal.yaml", traversal); dump_yaml("09-tests.yaml", tests)
(OUT / "09b-back-projection-prompt.md").write_text(
 "# Back-projection v1.0 for " + ID + " (scope A)\n\nThe reader is given two files, 00-kernel.yaml and 01-ontology.yaml, pasted below, and nothing else. The reader does not search, "
 "and does not open any record. From the two files alone the reader writes, in order: (1) the framework's name, its seed record and its author; (2) the four positions, "
 "with what sets the Theophrastan position apart; (3) the operations the framework forbids, each with the file line it derives from; (4) the dependency chain by which the "
 "framework reached its present claim about the number of makers, with the dates and records of each state; (5) the topology: strata in order with their records, the "
 "clusters and their joins, the evidence bodies with their rules; (6) the corrections, each original with the claim that corrected it; (7) the received many-maker "
 "reading, the status the kernel gives it, and the symmetric ledger: for each evidence body, what it gives each framework and what its rule withholds from both, "
 "with how the bodies combine and when a further model enters as a rival; (8) what a reader starting at record #1584 may conclude, and what that reader may not conclude; (9) what the two files leave "
 "the reader unable to reconstruct; (10) the lines of research, and, reading each line's advances_if and retreats_if, which result would most advance the framework and "
 "which would most retreat it. Where the two files disagree with each other, the reader reports the disagreement. "
 "The operator scores the answer against scope A's must_survive list, checking each element against 02-graph.jsonld and 03-claims.jsonl: an element counts when the reader "
 "derived it and the graph holds it; an element the reader asserts and the graph lacks counts against. Yield = elements derived and held / the elements of scope A's "
 "must_survive list in 00-kernel.yaml. Threshold 0.85 (EA-HK-01, #76).\n", encoding="utf-8")
files = sorted(p.name for p in OUT.iterdir() if p.is_file() and p.name not in ("11-integrity.yaml", "10-verification.json"))  # the verifier writes 10-verification.json after this file
dump_yaml("11-integrity.yaml", {"id": ID + "/integrity", "built": BUILT, "not_hashed_here": {"10-verification.json": "written by the verifier after this file; its hash is carried in the facsimile"}, "registry_sha256": hashlib.sha256((ROOT / "data/registry.json").read_bytes()).hexdigest(),
          "captures_sha256": hashlib.sha256((ROOT / "data/EA-WG-CAPTURES-01.json").read_bytes()).hexdigest(),
          "files": {f: hashlib.sha256((OUT / f).read_bytes()).hexdigest() for f in files}})
print(f"{ID}: {len(nodes)} records, {len(POSITIONS)} positions, {len(C)} claims ({sum(1 for c in C if c['state'].get('assertion')=='withdrawn')} withdrawn), "
      f"{len(edges)} edges, {len(caps)} captures, {len(events)} events")
