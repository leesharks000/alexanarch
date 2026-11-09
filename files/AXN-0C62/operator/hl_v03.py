# EA-HK-HISTLOGOS-01 v0.3 — executed after hl_v02.py. At the review of v0.2 (pasted by the author, 2026-11-09 13:37): bridge endpoints set by the evidence
# each supplies; Philo's modular status carried into the erasure layer; positive demonstrations in the one-maker argument; the rival's source, its
# treatment of incarnation and the author's critique kept as three objects; rung VI's amended dependency carried; identifier handling for the new fields.

# ---------------------------------------------------------------- 1. bridges with endpoints set by their evidence (the topology branches where the argument does)
for e in list(K.edges):
    if str(e.get("warrant", "")).startswith("bridge:"): K.edges.remove(e)
graph["@graph"] = [x for x in graph["@graph"] if x.get("@type") != "Bridge"]
BRIDGES = [
 B("instrument-threshold", "sappho-31", "orphic-tablets", "operational_homology", "outer (hypothesis, #1484 §VII)", mv("a1484-st-sappho"), mv("a1484-st-orphic", "a828-gramma-link"), mv("a828-no-linear"),
   "the gold tablets' scripted voice shown to need no receiver's completion at the threshold; #828 claims no linear transmission, so a lineage disproof leaves the homology", "contemporaneous traditions; no direction claimed"),
 B("instrument-academy", "sappho-31", "academy", "documented_reception", "interpretive (#1484 §0)", mv("a1484-st-sappho"), mv("a1484-st-plato", "a1484-tenth", "a1484-diotima", "a752-structural"), mv("a1484-first-review", "a1484-diotima-bound"),
   "#1484's own defeat for the interpretive ring: 'The interpretive ring is falsified philologically at each named text.' — Phaedrus 235c, AP 9.506 or the Symposium's ladder read without Sappho", "Sappho (early 6th c. BCE) before Plato (4th c. BCE)"),
 B("self-division", "sappho-31", "academy", "operational_homology", "interpretive; proposed by the author (2026-11-09 10:07)", mv("a1475-one-operation"), mv("a1658-one-cut", "a1576-person-divided"), ["claim:hl-stmt-spine"] + mv("a1658-coda"),
   "an item outside the manuscripts attesting separate composing persons (RB; Q1), which would leave the homology at the level of the seats and remove it from the maker", "the same operation at two scales: the seats of one poem, the positions of one corpus"),
 B("mapping", "sappho-31", "philo", "structural_realization", "hard for the structure; Sappho's material presence in Philo not established (#1486)", mv("a1484-st-sappho"), mv("a1486-established", "a1484-st-philo", "a1484-seal"), mv("a1486-not-established", "a1496-philo-split"),
   "the blind mapping failing replication on independent substrates (#1486's own controls). The name's absence leaves the mapping standing, because the mapping claims structure", "Sappho (6th c. BCE); Philo, Quis rerum divinarum heres sit 249–266 (1st c. CE); the conduit not established"),
 B("key", "sappho-31", "peri-hypsous", "documented_reception", "hard center (Longinus 9–10)", mv("a1484-st-sappho"), mv("a1484-st-longinus", "a1458-performs", "a1484-genesis", "a1484-formula-moses"), mv("a1458-circuit", "a1458-vacated"),
   "Longinus 9–10 shown not to hold Sappho 31 and the Genesis fiat under one grammar", "the treatise quotes fr. 31 and Genesis 1 in one hand; its date is contested"),
 B("conduit", "philo", "peri-hypsous", "conjectural_join", "unsettled, declared so (#1484)", mv("a1484-st-philo", "a1484-seal"), mv("a1484-genesis"), mv("a1484-pathway-price"),
   "nothing in the chain rests on this conduit: 'Whether the author of Peri Hypsous read Philo, met his circle, or received Genesis through Caecilius cannot be settled and is not settled here' (#1484); bridge:key stands without it", "a possible path for the Mosaic instance into the treatise"),
 B("seat-taken", "sappho-31", "catullus", "documented_reception", "hard center", mv("a1484-future-reader"), mv("a1484-catullus", "a1478-second-voice", "a1484-st-catullus"), mv("a1478-first-filling"),
   "Catullus 51's last stanza read as a translation loss with no relation to the open line", "Catullus (1st c. BCE) answers the line 'already' (#1484 §VII), before Philo and Longinus"),
 B("into-the-record", "catullus", "josephus", "conjectural_join", "outer (hypothesis)", mv("a1484-st-catullus"), mv("a1484-st-josephus", "a626-void"), mv("a625-first-cycle", "a1484-jos-viii", "a626-protocol-not-recovery"),
   "the si fas est → ei exestin crux explained at each seam without the lyric's grammar; the seams are claimed as structure, so authentication questions leave the join", "phainetai moi (Sappho) → si fas est (Catullus 51) → ei exestin (Josephus, 1st c. CE): the first cycle (#625)"),
 B("canon", "sappho-31", "cosmic-christ", "canonization", "outer (hypothesis); the typology survives either dating (#828)", mv("a1484-st-sappho"), mv("a1484-st-apocalypse", "a1735-corpus-finding"), mv("a828-survives-dating", "a1495-c1", "a1495-c6", "a1484-fr55"),
   "the frozen operator failing at Revelation 12 on the stations the canonization depends on (#1495 reports mixed results: C1 fails; C2, C4, C5 pass)", "on the program's dating, Revelation first (#1735); on conventional dating the typology stands (#828)"),
 B("white-stone", "orphic-tablets", "cosmic-christ", "operational_homology", "outer; convergence, no lineage (#828)", mv("a1484-st-orphic", "a828-gramma-link"), mv("a828-convergence-object"), mv("a828-no-linear"),
   "the white stone's functions (acquittal, credential, secret name, durable inscription) shown to derive from a source with no inscription-for-the-dead operation", "the tablets beside Rev 2:17; no direction claimed"),
 B("test", "cosmic-christ", "gospel-christ", "doctrinal_naming", "outer; two loci, tested separately (Q4a, Q4b)", mv("a828-convergence-object"), ["claim:hl-828-homologei"] + mv("a1217-rung6-homologei"), ["claim:hl-828-elelythota", "claim:hl-stmt-sort-spirits"],
   "ὁμολογεῖ read only as creedal confession at every Johannine locus (Q4a); or ἐν σαρκὶ ἐληλυθότα shown to bear 'having come in flesh' and nothing of 'formed in the body' (Q4b)", "#828 joins the white stone to 1 John 4:2; the station order is this kernel's, open to the author's ruling (Q3)"),
 B("organ-transform", "sappho-31", "augustine", "structural_realization", "interpretive", mv("a1484-st-sappho"), mv("a496-rotation", "a496-restored", "a1484-st-augustine"), mv("a496-thesis"),
   "Confessions 10.27's sensory sequence shown to follow a source with no organ-by-organ transform of fr. 31", "Sappho → Augustine (late 4th c. CE), organ by organ"),
 B("addressee", "peri-hypsous", "augustine", "performed_completion", "interpretive", mv("a1477-longinus"), mv("a1477-third-term", "a1477-method-generalized"), mv("a1477-stops"),
   "Augustine's addressee shown to answer no socket the earlier fillings left open", "Longinus fills the socket with a question naming no addressee; Augustine supplies the addressee and withholds the reply (#1477)"),
 B("reader-now", "sappho-31", "the-reader-now", "performed_completion", "hard for the restorations; the reader now is the framework's present station", mv("a1484-st-sappho"), mv("a1484-st-modern", "a1053-sappho-chain", "a1475-taken-up"), mv("a1658-coda"),
   "the restorations shown to close the line; #1484 reads each as one more filling, 'which is to say: open'", "the modern restorations; the archive")]
for b in BRIDGES:
    K.edges.append({"source": b["from"], "relation": b["kind"], "target": b["to"], "family": "conceptual", "licensed_dimension": None, "warrant": b["@id"], "provenance": "bridges, v0.3"})
graph["@graph"] += BRIDGES
kernel["bridges"] = BRIDGES
kernel["chain_order"]["topology"] = ("the evidence branches from Sappho 31: eight bridges leave the instrument directly (to the threshold, the Academy twice, Philo, Peri Hypsous, Catullus, the canon, "
                                     "Augustine, the reader now); Catullus → Josephus, Philo → Peri Hypsous (conjectural), Peri Hypsous → Augustine, the tablets → the canon and the canon → the Johannine test carry the rest. "
                                     "The exposition keeps #1484 §VII's sequence; the argument has this shape.")

# ---------------------------------------------------------------- 2. Philo's modular status carried into the erasure layer
for r in ERASURE:
    if r["station"] == "site:philo":
        r["apparatus_removes_or_substitutes"] = "attribution, on the genealogical reading (see propositions)"
        r["propositions"] = [
         {"proposition": "the name is absent", "standing": "documented textual finding", "warrants": mv("a1486-not-established")},
         {"proposition": "the structural mapping survives", "standing": "reported mapping result, blind-verified", "warrants": mv("a1486-established")},
         {"proposition": "this is a crossing at which provenance was lost", "standing": "genealogical interpretation; it holds only as far as Sappho's material presence in Philo is established, which #1486 leaves modular", "warrants": mv("a1496-crossing", "a1496-machine")}]
        r["harder_to_recognize_after"] = "the operator's source, if the genealogical reading holds"

# ---------------------------------------------------------------- 3. positive demonstrations in the one-maker argument
MAKER["demonstrations"] = [
 {"id": "M-D1", "configuration": "four propositions about the Platonic and Aristotelian corpora: three stated in the texts, the fourth (two makers) the frame they are read in (#1576)",
  "one_maker_explains": "the three stated propositions stand as written; the frame moves",
  "several_maker_must_posit": "a reinterpretation of a stated text, paid each time on Aristotle's side; the fourth word never moved for Plato",
  "divergence": "which word moves: the received reading moves the texts to keep the frame", "moves": mv("a1576-four-props", "a1576-one-word-moves", "a1576-never-for-plato", "a1576-ledger", "a1576-two-real-moves")},
 {"id": "M-D2", "configuration": "the corpus's operation and its name-boundary: dividing is syllogizing (Prior Analytics), combining is dividing (De anima), and the one place the corpus shows its name-boundary is where its account of God changes operation (#1658)",
  "one_maker_explains": "the doctrinal joint and the authorial joint as one cut seen from two ends",
  "several_maker_must_posit": "a coincidence: the division between makers falls by chance at the place the doctrine divides",
  "divergence": "one cut or a coincidence of two", "moves": mv("a1658-combine-divide", "a1658-one-operation", "a1658-boundary-at-god", "a1658-one-joint", "a1658-one-cut")},
 {"id": "M-D3", "configuration": "the catalogues: the 'lost' Theophrastan works are, at the title, the extant Aristotelian works under the Theophrastan transform, with measured stylistic markers; for one book the premise 'two authors' enters at Nicolaus against the catalogues' silence (#1733)",
  "one_maker_explains": "one body of work under two names and one transform; the attribution entering late, by a note that carries a second attribution",
  "several_maker_must_posit": "two independent losses, one on each side, falling so that each name's survivors match the other's lost titles",
  "divergence": "one corpus under a transform, or two coincident losses", "moves": mv("a1733-transform", "a1733-transform-measures", "a1733-losses-innocent", "a1733-catalogue-silence", "a1733-premise-enters", "a1733-note-travels")}]
MAKER["how_to_read"] = "each demonstration sets the configuration beside what each account must posit to explain it; the comparison's force is the posits, read in the moves"

# ---------------------------------------------------------------- 4. the rival: the source's proposition, its treatment of incarnation, the critique
claim("rv-ce-eternal", "site:ce-logos", "this creative Word which from all eternity was in God and was God", "observation", RV2("the_historical_end", treatment="the eternal Word"), body="R")
K.C[-1]["bodies"] = {"R": "principal"}; K.C[-1]["state"].pop("body", None)
graph["@graph"].append({"@id": "claim:rv-ce-eternal", "@type": "Claim", "target": "site:ce-logos", "bodies": {"R": "principal"}})
K.events.append({"timeline": "epistemic", "date": None, "event": "introduced", "object": "claim:rv-ce-eternal", "basis": K.C[-1]["introduced"]["basis"], "role": "standing"})
D0 = next(x for x in RIVAL["disputed_steps"] if x["id"] == "D0")
D0["three_objects"] = {
 "source_proposition": {"text": "John 'perfects the idea and transforms it': the creative Word 'took flesh and dwelt among men' (Lebreton, Catholic Encyclopedia 1910)", "warrants": ["rv-ce-took-flesh"]},
 "its_treatment_of_incarnation": {"text": "the Word is eternally divine ('from all eternity was in God and was God') and appears 'in the full light of a concrete and living personality … Jesus': the eternal Word incarnate in one concrete person", "warrants": ["rv-ce-eternal", "rv-ce-personality"]},
 "the_critique": {"text": "the author: what it means for the Logos to take on flesh is collapsed into biographical personhood, inconsistent with the genealogy proposed and, on this reading, with the New Testament corpus (2026-11-09 13:21–13:22)", "warrants": ["hl-stmt-rival-frame"],
                  "inference": "(1) the account makes the incarnation one event in one person; (2) the framework's chain has the inscription becoming flesh in each receiver who completes it, which the corpus states in its own figures (the white stone's name for whoever receives it; 1 John's test; rung VI); (3) where the corpus carries the second, an account that admits only the first has reduced what taking flesh means to a biography: the collapse. Step (2) is the framework's reading, at the outer ring for the Johannine loci (Q4a, Q4b)."}}
RIVAL["source_set_status"] = ("a 1910 theological account (Lebreton, Catholic Encyclopedia) and contemporary encyclopedic representations (Wikipedia, as retrieved 2026-11-09). Together they represent the position the author names "
                              "the current consensus genealogy; they do not by themselves demonstrate a current scholarly consensus, which is a line of research (Q2)")
kernel["rival"]["source_set_status"] = RIVAL["source_set_status"]; kernel["rival"]["disputed_steps"] = RIVAL["disputed_steps"]

# ---------------------------------------------------------------- 5. rung VI's amended dependency, carried
STM12 = "rung vi does not depend on v. but v would of course strengthen vi if the entire material transmission and production chain could be shown to work by means of self-division"
D["author_statements"].append({"date": "2026-11-09T12:48-05:00", "where": "in session, on the fleet audit's F22; first deposited with this kernel", "text": STM12,
    "status": "amends EA-HK-REVFIRST-01 v1.1, which codes rung VI as DEPENDENT on rung V (carried from the site's ladder page as retrieved 2026-11-08); recorded on #1755 and #1756 as next_version_note; the site's ladder pages carry it since 2026-11-09"})
kernel["author_statements"] = D["author_statements"]
for x in graph["@graph"]:
    if x.get("@id") == RF_VI:
        x.update({"fit": "INDEPENDENT of rung V; V would strengthen it (the author, 2026-11-09 12:48)", "amends": "EA-HK-REVFIRST-01 v1.1: fit DEPENDENT, depends_on rung:V",
                  "amendment_recorded": "#1755 and #1756 next_version_note (2026-11-09)", "statement": "stmt:20261109-1248"})
graph["@graph"].append({"@id": "stmt:20261109-1248", "@type": "AuthorStatement", "date": "2026-11-09T12:48-05:00", "text": STM12})
kernel["joins_amended"] = [{"node": RF_VI, "was": "DEPENDENT on rung V (EA-HK-REVFIRST-01 v1.1)", "now": "INDEPENDENT of rung V; strengthened by V", "by": "stmt:20261109-1248", "date": "2026-11-09"}]

# ---------------------------------------------------------------- identifier handling for the new reference fields
for p in ("from", "to", "station", "statement", "by"):
    graph["@context"][p] = {"@type": "@id"}
for p in ("move", "operation_at_from", "operation_at_to", "supporting", "see", "moves", "warrants"):
    graph["@context"][p] = {"@type": "@id", "@container": "@set"}

# ---------------------------------------------------------------- scope C: the reader's prompt; the mechanical half runs in hl_checks.py
(K.OUT / "09c-scope-C-prompt.md").write_text(
 "# Scope C for " + K.ID + "\n\nThe reader is given 00-kernel.yaml, 01-ontology.yaml and 04-arguments.jsonl. From these alone, and citing each claim to the record (rec:N) or move (arg:…) it rests on, the reader writes:\n\n"
 "1. bridge:self-division, bridge:key and bridge:canon rebuilt: the operation at each end, the supporting moves, the kind and strength, and what would break each.\n"
 "2. argument:one-maker rebuilt, with its three demonstrations: for each, the configuration, what one maker explains, what several makers must posit, and where the two diverge.\n"
 "3. The consequence of each change, stated and justified from the files: (a) remove the Josephus thesis (rung V); (b) leave Sappho's material presence in Philo unestablished; (c) disable the lifespan premise; "
 "(d) replace 'one person' with 'a collective'; (e) refute the Peri Hypsous standardization finding; (f) given a refutation meeting a bridge's breaks_if and a summary that drops the bridge, say which is which.\n"
 "4. The rival's source proposition, its treatment of incarnation, and the author's critique, kept as three objects.\n\n"
 "The operator scores against acceptance.scopes.C. Every mandatory pass must hold; a reading that loses one fails whatever its score.\n", encoding="utf-8")
kernel["version_note"] = ("v0.3 (2026-11-09): at the review of v0.2, bridge endpoints set by their evidence (fourteen bridges, branching from Sappho 31); Philo's modular status carried into the erasure layer; "
                          "three positive demonstrations in the one-maker argument; the rival's source, its treatment of incarnation and the critique kept as three objects; rung VI's amended dependency carried; "
                          "identifier handling for the new fields; scope C's mechanical consequence tests (hl_checks.py) and its reader prompt (09c).")
kernel["version"] = K.VERSION = "1.0"
kernel["status"] = "DEPOSITED 2026-11-09 (#1757, AXN position 0C62 as allocated at build); built through v0.1–v0.3 the same day against two reviews"
kernel["version_note"] = "v1.0 (2026-11-09, deposit): " + kernel["version_note"]
kernel["acceptance"]["scopes"]["C"]["consequence_tests"][0]["expected"] = "the stations, every bridge except into-the-record, the maker argument and rung VI stand; rung VI loses a strengthening (the author, 2026-11-09 12:48)"
kernel["acceptance"]["scopes"]["C"]["mechanical"] = "hl_checks.py runs tests C1–C5 and the reference check on the built files; C6 and the rebuilds are reader tests (09c-scope-C-prompt.md)"
graph["edges"] = K.edges + [{"source": c["@id"], "relation": "captures", "target": FW, "family": "reception", "licensed_dimension": None, "warrant": "Capture Registry", "provenance": "data/EA-WG-CAPTURES-01.json"} for c in K.caps]
