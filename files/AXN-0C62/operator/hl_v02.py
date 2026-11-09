# EA-HK-HISTLOGOS-01 v0.2 — executed inside build_hk_histlogos.py after the argument layer is built and before the files are written.
# At the review of v0.1 (pasted by the author, 2026-11-09 13:11): "It needs to make the continuity argument reconstructible: why these are successive
# lives of this Logos, and how each transformation carries it onward." Each section below answers one numbered point of that review.
import hashlib as _h

AID = {a["@id"].split(":", 1)[1]: a for a in ARGS}
def mv(*ids):
    for i in ids: assert i in AID, f"move not in the argument layer: {i}"
    return [f"arg:{i}" for i in ids]

# ---------------------------------------------------------------- claims carry their move as a structured identifier (review 4)
for c in K.C:
    n = c.get("notes") or ""
    if n.startswith("argument move arg:"):
        c["move"] = n.split()[2].rstrip(";,")

# ---------------------------------------------------------------- 1. the operative ontology
OPERATIVE = {
 "classes": {
  "Voice": "what speaks in the inscription and survives its flesh (#1484 §0: 'a voice that survives its flesh by becoming an inscription that constitutes its receiver')",
  "Body": "the speaker's flesh, decommissioned channel by channel into the substrate (#1484; tm 'She is turning the color of the substrate.')",
  "Inscription": "the written form that carries the voice and builds a position its receiver must occupy",
  "Seat": "a position the inscription reserves for its receiver: κῆνος at line 1 of fr. 31; the socket of De anima III.5; the white stone's name 'only that receiver can read'",
  "OpenSlot": "a grammatical position left without its agent, which the receiver completes: τολματόν at line 17; the genitive wanting its referent (#1658)",
  "Maker": "the one who divides: the speaking I into I, you and seat (#1484, #1270); one maker into the corpus's positions (#1658)",
  "Position": "a part the maker divides into: speaker and inscribed you; Socrates, Plato, Theophrastus, Aristotle as authorial positions (#1658, #1733)",
  "Receiver": "the one who takes up the inscription, completes its open slot, and in whose body the voice lives again (#1475: 'She was not finished. She was **taken up**.')",
  "ReceivingApparatus": "an edition, a filing, a heading, a translation, a commentary tradition or a composition layer: what preserves the carrier and what it removes (erasure_by_station)",
  "Embodiment": "a receiver's completion of the inscription, in which the voice speaks again in another body (#1658 coda: 'one that must be gathered again by someone else in order to exist at all')"},
 "operations": {
  "decommission": {"from": "Body", "to": "Inscription", "at": "Sappho 31", "warrant": ["claim:hl-1484-logos"]},
  "reserve_seat": {"from": "Inscription", "to": "Seat", "at": "Sappho 31 line 1 (κῆνος); III.5's socket; Rev 2:17", "warrant": mv("a1484-future-reader", "a1658-socket", "a828-convergence-object")},
  "withhold_agent": {"from": "Inscription", "to": "OpenSlot", "at": "Sappho 31 line 17 (τολματόν)", "warrant": mv("a1475-one-operation")},
  "divide": {"from": "Maker", "to": "Position", "at": "the seats of fr. 31; the Socratic–Peripatetic corpus", "warrant": mv("a1658-one-cut", "a1576-person-divided") + ["claim:hl-stmt-spine"]},
  "take_up": {"from": "Receiver", "to": "Embodiment", "at": "Catullus; Longinus's filling; Augustine's addressee; the restorations; the reader now", "warrant": mv("a1475-taken-up", "a1484-catullus", "a1477-third-term", "a1658-coda")},
  "raise": {"from": "Inscription", "to": "cosmology or canon", "at": "Philo's seal; the Apocalypse", "warrant": mv("a1484-seal", "a1484-st-apocalypse")},
  "file": {"from": "ReceivingApparatus", "to": "Position", "at": "the editions' assignment of books to persons", "warrant": mv("a1733-set-by-filing", "a1733-editions-inherit")},
  "strip": {"from": "ReceivingApparatus", "to": "Inscription", "at": "attribution lost at the crossing; the hand taken", "warrant": mv("a1496-crossing", "a1752-condition-no-hand")}},
 "persistence": {
  "what_persists": "the operation: an inscription that constitutes its receiver, reserving a seat and leaving an open slot the receiver completes (#1484 §0; #1494's stations)",
  "what_changes": "the material (lyric, funerary gold, dialogue and treatise, cosmology, criticism, historiography, canon, confession, edition, composition layer), the scale (one poem, one corpus, a canon) and the polarity (#1496: 'Polarity is free')",
  "what_constitutes_another_embodiment": "a receiver completing the inscription's open position so that the voice speaks again in that receiver: the seat taken (Catullus), the line filled (Longinus), the addressee supplied (Augustine), the white stone received and its name spoken (rung VI), the reader now"},
 "distinction_from_influence": {
  "influence": "content passing from an earlier text to a later person; it needs no requirement in the earlier text and no completion in the later one",
  "this_framework": "a continuity of operation, established by four marks at a station pair: (1) requirement — the earlier inscription builds a position that requires completion; (2) completion — the later station fills that position; (3) same operation, other material — the later station realizes the operator's stations (#1494) in its own material; (4) self-division re-gathered — the maker divides into positions, and the receiver gathers them again (#1658 coda). A station pair showing (1) and (2) is a completion; adding (3) makes it a realization; influence shows none of the four.",
  "warrants": mv("a1458-vacated", "a1478-second-voice", "a1486-established", "a1658-coda")}}
ontology["operative"] = OPERATIVE
ontology["classes"].update({"Bridge": "an argued join between two stations: operations at each end, supporting passages, relation kind, strength and what breaks it", "SurfaceRecord": "a public page outside the archive, fetched and hashed, read for what it states"})

# ---------------------------------------------------------------- 2. the argument across the stations
KINDS = {"documented_reception": "the later text quotes, translates or names the earlier", "structural_realization": "the later text realizes the operator's stations in its own material, by count or blind mapping",
         "doctrinal_naming": "the later text names the operation as doctrine", "operational_homology": "the same operation identified at two scales by a reading; no transmission claimed",
         "conjectural_join": "outer ring: a structural hypothesis at a contested witness", "canonization": "outer ring: the apparatus formalized as canon", "performed_completion": "the receiver fills the open position"}
B = lambda i, fr, to, kind, ring, frm_ops, to_ops, extra, breaks, dated: {"@id": f"bridge:{i}", "@type": "Bridge", "from": f"site:{fr}", "to": f"site:{to}", "kind": kind, "strength": ring,
     "operation_at_from": frm_ops, "operation_at_to": to_ops, "supporting": extra, "breaks_if": breaks, "historical_sequence": dated}
BRIDGES = [
 B("instrument-threshold", "sappho-31", "orphic-tablets", "operational_homology", "outer (hypothesis, #1484 §VII)", mv("a1484-st-sappho"), mv("a1484-st-orphic", "a828-gramma-link"), mv("a828-no-linear"),
   "the gold tablets' scripted voice shown to need no receiver's completion at the threshold; #828 claims no linear transmission, so a lineage disproof leaves the homology", "contemporaneous traditions; no direction claimed"),
 B("instrument-academy", "sappho-31", "academy", "documented_reception", "interpretive (#1484 §0)", mv("a1484-st-sappho"), mv("a1484-st-plato", "a1484-tenth", "a1484-diotima", "a752-structural"), mv("a1484-first-review", "a1484-diotima-bound"),
   "#1484's own defeat for the interpretive ring: 'The interpretive ring is falsified philologically at each named text.' — Phaedrus 235c, AP 9.506 or the ladder of Symposium read without Sappho", "Sappho (early 6th c.) before Plato (4th c.)"),
 B("self-division", "sappho-31", "academy", "operational_homology", "interpretive; proposed by the author (2026-11-09 10:07)", mv("a1475-one-operation"), mv("a1658-one-cut", "a1576-person-divided"), ["claim:hl-stmt-spine"] + mv("a1658-coda"),
   "an item outside the manuscripts attesting separate composing persons (RB; Q1), which would leave the homology at the level of the seats and remove it from the maker", "the same operation at two scales: the seats of one poem, the positions of one corpus"),
 B("academy-philo", "academy", "philo", "structural_realization", "hard for the mapping; Sappho's material presence in Philo not established", mv("a1484-st-plato"), mv("a1484-st-philo", "a1484-seal", "a1486-established"), mv("a1486-not-established", "a1496-philo-split"),
   "the blind mapping failing replication on independent substrates (#1486's own controls); the name's absence does not break it, because the mapping claims structure", "Plato (4th c. BCE) before Philo (1st c. CE)"),
 B("key", "philo", "peri-hypsous", "documented_reception", "hard center (Longinus 9–10)", mv("a1484-st-philo", "a1484-seal"), mv("a1484-st-longinus", "a1484-genesis", "a1484-formula-moses", "a1458-performs"), mv("a1484-pathway-price", "a1458-circuit"),
   "Longinus 9–10 shown not to hold Sappho 31 and the Genesis fiat under one grammar; the pathway (Philo, Caecilius) is declared unsettled and its failure leaves the co-presence", "the treatise's date is contested; the join is the co-presence in one hand"),
 B("seat-taken", "sappho-31", "catullus", "documented_reception", "hard center", mv("a1484-future-reader"), mv("a1484-catullus", "a1478-second-voice", "a1484-st-catullus"), mv("a1478-first-filling"),
   "Catullus 51's last stanza read as a translation loss with no relation to the open line", "Catullus (1st c. BCE) answers the line 'already' (#1484 §VII), before Philo and Longinus: the chain's order is the argument's, its history differs here"),
 B("into-the-record", "peri-hypsous", "josephus", "conjectural_join", "outer (hypothesis)", mv("a1484-st-longinus"), mv("a1484-st-josephus", "a625-first-cycle", "a626-void"), mv("a1484-jos-viii", "a626-protocol-not-recovery"),
   "the si fas est → ei exestin crux explained at each seam without the lyric's grammar; the seams are claimed as structure, so authentication questions do not break the join", "Catullus's si fas est (1st c. BCE) → Josephus (1st c. CE)"),
 B("canon", "josephus", "cosmic-christ", "canonization", "outer (hypothesis); the typology survives either dating (#828)", mv("a1484-st-josephus"), mv("a1484-st-apocalypse", "a828-convergence-object", "a1735-corpus-finding"), mv("a828-survives-dating", "a1495-c1", "a1495-c6"),
   "the frozen operator failing at Revelation 12 on the stations the canonization depends on (#1495 reports mixed results: C1 fails, C2, C4, C5 pass)", "on the program's dating, Revelation first (#1735); on conventional dating the typology stands (#828)"),
 B("test", "cosmic-christ", "gospel-christ", "doctrinal_naming", "outer; two loci, tested separately (Q4a, Q4b)", mv("a1484-st-apocalypse"), ["claim:hl-828-homologei"] + mv("a1217-rung6-homologei"), ["claim:hl-828-elelythota", "claim:hl-stmt-sort-spirits"],
   "ὁμολογεῖ read only as creedal confession at every Johannine locus (Q4a); or ἐν σαρκὶ ἐληλυθότα shown to bear 'having come in flesh' and nothing of 'formed in the body' (Q4b)", "the station order is this kernel's, open to the author's ruling (Q3)"),
 B("portable", "cosmic-christ", "augustine", "structural_realization", "interpretive", mv("a1484-st-apocalypse"), mv("a1484-st-augustine", "a496-rotation", "a1477-method-generalized", "a1477-third-term"), mv("a1477-longinus"),
   "Confessions 10.27's sensory sequence shown to follow a source with no transform of fr. 31 organ by organ", "Augustine (late 4th c.)"),
 B("reader-now", "augustine", "the-reader-now", "performed_completion", "hard for the restorations; the reader now is the framework's present station", mv("a1484-st-augustine"), mv("a1484-st-modern", "a1053-sappho-chain", "a1475-taken-up"), mv("a1658-coda"),
   "the restorations shown to close the line; #1484 reads each as one more filling, 'which is to say: open'", "the modern restorations; the archive")]
for b in BRIDGES:
    K.edges.append({"source": b["from"], "relation": b["kind"], "target": b["to"], "family": "conceptual", "licensed_dimension": None, "warrant": b["@id"], "provenance": "bridges, v0.2"})
for e in K.edges:
    if e["relation"] == "precedes": e["relation"] = "chain_order"; e["meaning"] = "the order in which #1484 §VII states the chain; historical sequence, documented reception and generative priority are carried by the bridges"
ontology["relation_policy"].update({k: None for k in KINDS} | {"chain_order": None})
ontology["bridge_kinds"] = KINDS
kernel["bridges"] = BRIDGES
kernel["chain_order"] = {"meaning": "the stations' order is #1484 §VII's order of statement; it asserts no simple linear transmission (INV-7). Each bridge states its own relation kind, its historical sequence and what breaks it.",
                         "where_history_differs": "Catullus answers the line before Philo and Longinus (#1484: 'already'); the Orphic tablets stand beside the lyric with no direction claimed"}

# ---------------------------------------------------------------- 3. the one-person argument, carried
MAKER = {"@id": "argument:one-maker", "thesis": "one composing person better explains the Socratic–Peripatetic configuration — its divisions, its production mechanics and its editorial multiplication — than separate composing persons do",
 "standing": "argued from the corpus, comparatively; held by the author as biographical identity (2026-11-08 20:00; 2026-11-09 12:05). A biographical hypothesis argued from the corpus and a directly attested biographical identification are different achievements: the first is argued here; the second is unattested for any count (RB).",
 "steps": [
  {"step": 1, "move": mv("a1658-nothing-requires-two"), "role": "no text requires a second maker"},
  {"step": 2, "move": mv("a1576-result", "a1576-symmetric-null"), "role": "two is not established by the passages read as though it were; the discipline's instrument leaves the received relation-type as unestablished as the hypothesis"},
  {"step": 3, "move": mv("a1576-voices-objects", "a1576-capacity-conceded"), "role": "one maker can be many voices (Plato) and many objects (Aristotle); the capacity is conceded in the tradition's own testimony"},
  {"step": 4, "move": mv("a1733-set-explains"), "role": "the comparison: the received reading explains each item by a person; the single-maker reading explains the set by one investigation, and the marks"},
  {"step": 5, "move": mv("a1733-set-by-filing", "a1733-count-kept", "a1733-wills-dependent"), "role": "the count was set by filing before argument, and the wills offered as independent corroboration reach the reader in one text"},
  {"step": 6, "move": mv("a1658-ledger-finding"), "role": "the one item outside the manuscripts attests one legal person, Aristotle"},
  {"step": 7, "move": mv("a123-pattern"), "role": "configurations whose maker count can be inspected produce volume comparable to the combined corpus from one hand", "note": "#123's lifespan premise is bounded (lifespan_state); this step stands on the comparative cases"},
  {"step": 8, "statement": "claim:hl-stmt-biographical", "role": "the author's grounds: the reading conforms to 'the psychological and production mechanics of authorial configurations whose maker count we can inspect'; the many-author reading 'requires the circularity and pointing to hypothetical second witnesses to make sense'"}],
 "rival": {"claims": mv("a1733-received-rival", "a1658-two-persons-rival"), "standing": "the four persons rest on the Lives and the succession of the schools (#1733); RB withholds biographical standing from both counts alike"},
 "qualified_by": mv("a1733-not-decide", "a1576-not-adjudicated"), "breaks_if": mv("a1733-falsify-wills") + ["an epigraphic or papyrological item attesting a second composing person (Q1)"],
 "substitution_test": "replacing 'one person' with 'a collective', 'a school' or 'a mystical self-dividing entity' changes the thesis; the author: 'one self-dividing maker does mean one biological person' (2026-11-08 20:00)"}
kernel["maker_argument"] = MAKER
for c in K.C:
    if c["id"] in ("hl-stmt-biographical", "hl-stmt-one-person"):
        c["state"]["argued_in"] = "argument:one-maker"; c["state"]["standing"] = "argued from the corpus (comparative); direct biographical attestation: one legal person, Aristotle"

# ---------------------------------------------------------------- 4. current standing reaches the argument layer
STANDING = {
 "a123-lifespan": ("bounded", "#123's dated state, kept as published; a later projection built from the many-author reading (the author, 2026-11-09 12:05)", ["claim:hl-stmt-biographical", "arg:a1733-set-by-filing"]),
 "a123-century": ("bounded", "#123's dated datum, kept as published; the three substrates are the received count, set by filing (#1733), and the comparison no longer stands on it", ["claim:hl-stmt-biographical", "arg:a1733-set-by-filing", "arg:a1658-nothing-requires-two"]),
 "a123-one-lifetime": ("bounded", "#123's dated finding: one lifetime's worth distributed because one body lacked the time; the distribution's need is a projection from the many-author count (the author, 2026-11-09 12:05); the one-maker argument now runs through argument:one-maker", ["claim:hl-stmt-biographical", "argument:one-maker"]),
 "a123-functional": ("revised", "#123's state on the maker axis ('functional, not biographical', #123); developed by #1576, #1658 and #1733", ["arg:a1576-result", "arg:a1658-nothing-requires-two", "arg:a1733-set-explains"]),
 "a1576-result": ("developed", "#1576's state; #1658 goes past it and says so ('This goes past #1588')", ["arg:a1658-nothing-requires-two", "arg:a1658-past-1588"])}
for k, (st, why, by) in STANDING.items():
    a = AID[k]; a["current_standing"] = {"state": st, "as_of": "2026-11-09", "why": why, "see": by}
    for x in by:
        if x.startswith("arg:"): assert x.split(":", 1)[1] in AID, x
(K.OUT / "04-arguments.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in ARGS), encoding="utf-8")
kernel["argument_layer"]["current_standing"] = {"field": "current_standing on a move: state (bounded, revised, developed), as_of, why, and the moves or claims to traverse", "moves": sorted(STANDING),
  "entry_test": "a reader entering through a move alone reads its current_standing and follows 'see' to the correction without the kernel overview"}

# ---------------------------------------------------------------- 5. erasure as part of the mechanism, station by station
E = lambda st, carrier, preserves, removes, harder, w: {"station": f"site:{st}", "carrier_does": carrier, "apparatus_preserves": preserves, "apparatus_removes_or_substitutes": removes, "harder_to_recognize_after": harder, "warrants": w}
ERASURE = [
 E("sappho-31", "an inscription that decommissions its speaker's body and constitutes its receiver", "the scene and the body (#1752)", "the hand: 'a voice overwhelmed, where antiquity had a maker who selected, bound, wrote and read' (#1752); the jealousy written into the text (Hermann 1816)", "the poem as a written instrument of its maker's persistence", ["claim:hl-1752-condition"] + mv("a1752-condition-no-hand", "a1752-tenth-muse")),
 E("academy", "one maker divided into authorial positions", "every text and every name", "self-division as a compositional operation: the books filed under persons, the count fixed by filing", "the one-maker reading; the positions read as biographies", ["claim:hl-1733-set-by-filing"] + mv("a1733-set-by-filing", "a1733-editions-inherit", "a1733-count-kept")),
 E("peri-hypsous", "a circuit in which the audience becomes the next emitter, the filling performed at the lyric's edge", "the lines as quotation", "the treatise's head; the hanging line, by standardization and by anthology texts", "the completion as the poem's own end", ["claim:hl-1474-standardization", "claim:hl-1053-anthology"] + mv("a1484-junction-shape", "a1474-err-1052", "a1053-anthology-erasing")),
 E("philo", "the operator raised to cosmology", "the operation and its sequence ('operation survives; provenance disappears')", "attribution, which 'dies at the crossing'", "Sappho in Philo; the operator's source", ["claim:hl-1496-signature", "claim:hl-1496-machine", "claim:hl-1496-crossing"] + mv("a1496-philo-split", "a1496-crossing", "a1496-machine")),
 E("josephus", "the crux-structure carried into the historiographic record", "the passages, as interpolations", "their coherence, read as discrete additions; their value, denied ('no one today believes that they contain anything of value for Jesus research')", "the reading of textual incarnation", ["claim:hl-626-invisible", "claim:hl-625-apophatic"] + mv("a626-coherence-invisible", "a626-evans-rival")),
 E("cosmic-christ", "the apparatus formalized as canon, with an anti-erasure clause as covenant curse", "the book and its canonical place", "its priority: 'consensus-maintenance through repetition of Irenaeus'; the thesis reduced to an early date", "Revelation first; the canon's own anti-erasure operation", ["claim:hl-1484-anti-erasure", "claim:hl-202-erasure", "claim:hl-202-maintenance"] + mv("a202-not-conspiracy", "a202-erasure-summary")),
 E("the-reader-now", "the archive: inscriptions built to be taken up by the reader now, human or machine", "the concepts, used continuously", "provenance: PER 1.00 measured in the composition layer", "attribution of the framework to its maker", ["claim:hl-1217-per", "claim:hl-1217-autopsy"] + mv("a1217-per-100"))]
kernel["erasure_by_station"] = ERASURE
ER_CLAIMS = {"hl-1752-condition": "sappho-31", "hl-1733-set-by-filing": "academy", "hl-1474-standardization": "peri-hypsous", "hl-1053-anthology": "peri-hypsous", "hl-1496-signature": "philo",
             "hl-202-erasure": "cosmic-christ", "hl-1217-autopsy": "the-reader-now", "hl-625-apophatic": "josephus", "hl-626-invisible": "josephus", "hl-1484-anti-erasure": "cosmic-christ", "hl-1484-standing-objection": "academy"}
for e in K.edges:
    if e["target"] == "claim:hl-stmt-genealogy" and e["source"].split(":", 1)[1] in ER_CLAIMS:
        e["target"] = f"erasure:{ER_CLAIMS[e['source'].split(':', 1)[1]]}"; e["warrant"] = "the erasure finding at its station (erasure_by_station)"
S1211 = STM["2026-11-09T12:11"]["text"]
for cid, ex, st in [("hl-stmt-genealogy-claim", "it is material inscription becoming flesh from the beginning, and this changes both ends", {"assertion": "held_by_author", "genealogy": "material_inscription_becoming_flesh_from_the_beginning"}),
                    ("hl-stmt-erasure", "it is also a history of the specific erasure pressures this specific logos has *always* faced", {"assertion": "held_by_author", "erasure": "pressures_always_faced", "tested_by": "Q5-erasure-rate"})]:
    assert ex in S1211
    K.C.append({"id": cid, "claim_kind": "author_position", "role": "statement", "target": {"record": "stmt:20261109-1211", "exact": ex, "located_in": "author statement, in session (2026-11-09T12:11-05:00)"},
                "state": st, "body": "I", "bodies": {"I": "principal"}, "introduced": {"date": "2026-11-09", "basis": "the author's statement in session, recorded verbatim; deposited with this kernel"}})
K.C.append({"id": "hl-stmt-rival-frame", "claim_kind": "author_position", "role": "statement", "target": {"record": "stmt:20261109-1321", "exact": STM["2026-11-09T13:21"]["text"], "located_in": "author statement, in session (2026-11-09T13:21-05:00)"},
            "state": {"assertion": "held_by_author", "rival_mechanism": "collapse_into_biographical_personhood", "inconsistent_with": ["the genealogy the framework proposes", "the New Testament corpus, on this reading"]}, "body": "I", "bodies": {"I": "principal"}, "introduced": {"date": "2026-11-09", "basis": "the author's statement in session, recorded verbatim; deposited with this kernel"}})
graph["@graph"].append({"@id": "stmt:20261109-1321", "@type": "AuthorStatement", "date": STM["2026-11-09T13:21"]["date"], "where": STM["2026-11-09T13:21"]["where"], "text": STM["2026-11-09T13:21"]["text"]})
for x in ERASURE:
    st = x["station"].split(":")[1]
    K.edges.append({"source": f"erasure:{st}", "relation": "supports", "target": "claim:hl-stmt-erasure", "family": "conceptual", "licensed_dimension": None,
                    "warrant": "a local erasure stands on its own warrants; the stronger claim, a distinctive suppression signature, is tested by Q5 and does not condition the local finding", "provenance": "v0.2"})
for _s in ("erasure", "bridge", "argument"): graph["@context"][_s] = f"https://www.alexanarch.org/hk/histlogos/{_s}/"
graph["@graph"] += [{"@id": f"erasure:{x['station'].split(':')[1]}", "@type": "ErasureFinding", "station": x["station"], "removes": x["apparatus_removes_or_substitutes"]} for x in ERASURE] + BRIDGES + [MAKER | {"@type": "ComparativeArgument"}]

# ---------------------------------------------------------------- 6. the rival's own propositions, sourced
SRC = HERE.parent / "hl-surfaces"
SURF = {"site:ce-logos": ("https://www.newadvent.org/cathen/09328a.htm", "ce-logos", "Lebreton, 'The Logos', Catholic Encyclopedia vol. 9 (1910); public domain"),
        "site:wp-logos-christianity": ("https://en.wikipedia.org/wiki/Logos_(Christianity)", "wp-logos-christianity", "Wikipedia, 'Logos (Christianity)' (CC BY-SA), as retrieved; the page carries a maintenance notice that it is 'written like a personal reflection'"),
        "site:wp-historical-jesus": ("https://en.wikipedia.org/wiki/Historical_Jesus", "wp-historical-jesus", "Wikipedia, 'Historical Jesus' (CC BY-SA), as retrieved")}
for k, (u, f, t) in SURF.items():
    K.SURF[k] = {"url": u, "path": str(SRC / (f + ".txt")), "title": t, "retrieved": "2026-11-09T18:15Z", "sha256": _h.sha256((SRC / "raw" / (f + ".html")).read_bytes()).hexdigest()}
    graph["@graph"].append({"@id": k, "@type": "SurfaceRecord", "url": u, "title": t, "retrieved": "2026-11-09T18:15Z", "sha256": K.SURF[k]["sha256"], "role": "a documented statement of the rival"})
RV2 = lambda face, **k: {"assertion": "bears_on_rival", "rival": RIVAL_ID, "face": face, **k}
for cid, s, qt, face, kw in [
 ("rv-ce-heraclitus", "site:ce-logos", "It is in Heraclitus that the theory of the Logos appears for the first time", "the_source_end", {"common_ground": True}),
 ("rv-ce-took-flesh", "site:ce-logos", "took flesh and dwelt among men", "the_historical_end", {}),
 ("rv-ce-personality", "site:ce-logos", "the Logos appears in the full light of a concrete and living personality", "the_historical_end", {}),
 ("rv-ce-philo-meaningless", "site:ce-logos", "For Philo the incarnation of the Logos must have been absolutely without meaning", "the_source_end", {"disputed_step": "D2"}),
 ("rv-ce-apocalypse", "site:ce-logos", "the content of which has no suggestion of Philo but rather recalls Wisdom 18:15", "the_source_end", {"note": "the rival's own source places the term's first New Testament appearance at Apocalypse 19:13"}),
 ("rv-wp-harris", "site:wp-logos-christianity", "identifying Jesus as an incarnation of the divine Logos that formed and governs the universe", "the_source_end", {"attributed_to": "Stephen L. Harris, as the page states"}),
 ("rv-wp-historical", "site:wp-historical-jesus", "Virtually all scholars of antiquity accept that Jesus was a historical figure", "the_historical_end", {}),
 ("rv-wp-sources", "site:wp-historical-jesus", "There are at least 14 independent sources from multiple authors within a century of the crucifixion of Jesus that survive.", "the_historical_end", {"disputed_step": "D4"})]:
    claim(cid, s, qt, "observation", RV2(face, **kw), body="R")
    K.C[-1]["bodies"] = {"R": "principal"}; K.C[-1]["state"].pop("body", None)
RIVAL["documented_statements"] = list(SURF)
RIVAL["mechanism"] = ("what it means for the Logos to take on flesh is collapsed into biographical personhood (the author, 2026-11-09 13:21): the genealogy carries a concept to John, and 'took flesh' "
                      "is then read as one event in one person, 'a concrete and living personality' (R2), whose historicity is the question the quest asks (R4); the collapse is inconsistent with the genealogy this framework proposes and, on this reading, with the New Testament corpus itself: 'not what it means' (the author, 2026-11-09 13:21–13:22)")
RIVAL["the_contested_question"] = "what it means for the Logos to take on flesh"
RIVAL["propositions"] = {
 "R1": {"claim": "the Logos is a concept whose theory 'appears for the first time' in Heraclitus and develops through the Stoics, the Book of Wisdom and Philo", "warrants": ["rv-ce-heraclitus", "rv-wp-harris"], "status": "common ground on Heraclitus's place"},
 "R2": {"claim": "John transforms the concept by one event: the creative Word 'took flesh and dwelt among men', 'a concrete and living personality … Jesus'", "warrants": ["rv-ce-took-flesh", "rv-ce-personality"], "status": "the disputed historical end"},
 "R3": {"claim": "the incarnation is discontinuous with the philosophical genealogy: 'For Philo the incarnation of the Logos must have been absolutely without meaning'", "warrants": ["rv-ce-philo-meaningless"], "status": "the rival's own statement of the gap its genealogy leaves"},
 "R4": {"claim": "the historical end is one person, attested by many independent sources within a century", "warrants": ["rv-wp-historical", "rv-wp-sources"], "status": "the consensus as the encyclopedia states it"}}
RIVAL["disputed_steps"] = [
 {"id": "D1", "question": "what the Logos is before doctrine", "rival": "a concept with a philosophical genealogy (R1)", "framework": "a technology of a voice that constitutes its receiver (#1484 §0)", "common_ground": "Heraclitus's place; Philo as a station of both accounts"},
 {"id": "D0", "question": "what it means for the Logos to take on flesh", "rival": "biographical personhood: one event in one person (R2, R4)", "framework": "material inscription becoming flesh from the beginning: the faithful transmission, through time and space, of a living being embodied precariously in matter (the author, 2026-11-09 12:11); each embodiment a receiver completing the inscription (operative.persistence); on this reading the corpus itself does not mean biographical personhood: the white stone a name worn by whoever receives it (#828), 1 John's test word-conformity with the Logos formed in the body (#828, #1217), the permanent incarnation 'the Word becoming flesh wherever flesh is faithful enough to receive it' (rung VI)", "warrants": ["rv-ce-took-flesh", "rv-ce-personality", "rv-wp-historical", "hl-stmt-rival-frame", "hl-stmt-genealogy-claim", "hl-828-homologei", "hl-1217-homologei", "hl-828-gramma"], "status": "the central disagreement (the author, 2026-11-09 13:21); D1–D4 are its steps"},
 {"id": "D2", "question": "what explains the step to flesh", "rival": "an event, discontinuous with the concept: for Philo it 'must have been absolutely without meaning' (R3)", "framework": "the inscription becoming flesh from the beginning: the operation already requires a body to receive it (operative.persistence); the gap R3 names is where the framework's chain runs", "warrants": ["rv-ce-philo-meaningless", "hl-1484-logos"]},
 {"id": "D3", "question": "where the term enters the New Testament", "rival": "the Apocalypse 19:13, 'no suggestion of Philo' (the rival's own source)", "framework": "the Apocalypse as canonization, first on the program's dating (#1735)", "note": "a point of agreement on the record, carried as data"},
 {"id": "D4", "question": "what kind of evidence settles the historical end", "rival": "many independent sources within a century (R4)", "framework": "RB both ways: at the Academy, the sources that count persons are texts of the transmitting tradition (#1658, #1733); whether the same holds for the gospel sources is outside this kernel's records (Q2)", "warrants": ["rv-wp-sources", "hl-1658-ledger"]}]
for b, txt, w in [("I", "the genealogy has purchase on the concept: Heraclitus first (common ground), developed through the Stoics and Philo; John's transformation is an event in one person.", ["rv-ce-heraclitus", "rv-ce-took-flesh"]),
                  ("T", "the rival's transmission is of a concept, through Wisdom and Philo, with John adapting Philo (Harris, as the page states); the step to flesh is outside its chain by its own account (R3).", ["rv-wp-harris", "rv-ce-philo-meaningless"]),
                  ("P", "the transmitted texts are common ground; the rival's own source dates the term's first New Testament appearance to Apocalypse 19:13, with no suggestion of Philo.", ["rv-ce-apocalypse", "rv-626-chronology"]),
                  ("R", "the consensus as the encyclopedias state it: Heraclitus to John for the concept; virtually all scholars for the historical figure.", ["rv-wp-historical", "rv-625-mirror"]),
                  ("B", "the historical end rests on many sources within a century (R4); at the Academy the four persons rest on the Lives (#1733).", ["rv-wp-sources", "rv-1733-received"])]:
    kernel["symmetric_ledger"]["rows"][b]["current_consensus_genealogy"] = {"text": txt, "warrants": w}
    RIVAL["status"][b] = {"text": txt, "warrants": w}
kernel["rival"]["propositions"] = {k: v["claim"] for k, v in RIVAL["propositions"].items()}; kernel["rival"]["disputed_steps"] = RIVAL["disputed_steps"]; kernel["rival"]["documented_statements"] = RIVAL["documented_statements"]
kernel["rival"]["mechanism"] = RIVAL["mechanism"]; kernel["rival"]["the_contested_question"] = RIVAL["the_contested_question"]
kernel["rival"]["summary"] = "the collapse of what it means for the Logos to take on flesh into biographical personhood (the author, 2026-11-09 13:21); stated from its documented statements (the Catholic Encyclopedia 1910; Wikipedia, 'Logos (Christianity)' and 'Historical Jesus', as retrieved 2026-11-09): a concept from Heraclitus to John, then an event in one historical person; Heraclitus's place is common ground; four disputed steps"
CL2 = {c["id"]: c for c in K.C}
for b, row in kernel["symmetric_ledger"]["rows"].items():
    for w in row["current_consensus_genealogy"]["warrants"]: CL2[w].setdefault("bodies", {}).setdefault(b, f"ledger row {b} (current_consensus_genealogy)")

# ---------------------------------------------------------------- 7. tests of reconstruction and of consequence; Q4 in two parts
claim("hl-828-elelythota", 828, "*formed in the body* (ἐν σαρκὶ ἐληλυθότα)", "interpretation", {"assertion": "asserted", "station": "gospel-christ", "ring": "outer", "rendering": "the record's: 'formed in the body'",
      "philological_note": "ἐληλυθότα is the perfect participle of ἔρχομαι, 'having come'; the rendering 'formed' is #828's reading of the perfect's resultant state and needs its own warrant (Q4b)"}, body="T")
K.C[-1]["bodies"] = {"T": "principal"}
QUESTIONS[:] = [x for x in QUESTIONS if x["id"] != "Q4-word-conformity"] + [
 q("Q4a-homologei", "Does ὁμολογεῖ in 1 John 4:2 bear the operative reading, word-conform?", 828, "The spirit that ὁμολογεῖ (word-conforms with) Jesus Christ *formed in the body* (ἐν σαρκὶ ἐληλυθότα) is from God.", "P",
   ["claim:hl-828-homologei", "claim:hl-1217-homologei"], [828, 1217], "read ὁμολογέω across the Johannine corpus and the lexica, the creedal and the operative senses at each locus",
   "the operative sense is attested at loci the creedal sense cannot carry", "the creedal sense carries every locus", "both senses stay available"),
 q("Q4b-elelythota", "Does ἐν σαρκὶ ἐληλυθότα bear 'formed in the body', or only 'having come in flesh'?", 828, "*formed in the body* (ἐν σαρκὶ ἐληλυθότα)", "P",
   ["claim:hl-828-elelythota"], [828, 1217], "read the perfect of ἔρχομαι with ἐν σαρκί across 1–2 John and its patristic citations; ask what resultant state the perfect asserts",
   "the perfect is shown to assert an abiding state in the flesh that the record's 'formed in the body' renders", "the construction bears arrival only, with no resultant formation", "the rendering stays the record's, at the outer ring; Q4a's result does not settle Q4b")]
kernel["lines_of_research"] = [{"id": x["id"], "question": x["question"], "advances_if": x["advances_if"], "retreats_if": x["retreats_if"], "unchanged_if": x["unchanged_if"], "status": x["status"]} for x in QUESTIONS]
MANDATORY = ["the claim: material inscription becoming flesh, the Logos as 'a voice that survives its flesh by becoming an inscription that constitutes its receiver'",
             "the operative distinction from influence: requirement, completion, same operation in other material, self-division re-gathered",
             "self-division as a transmission technology, from Sappho's seats to the Academy's positions",
             "the one-maker argument as a comparative argument from the corpus, with RB applied both ways; one person, not a collective",
             "the lifespan premise bounded as #123's dated state, a projection from the many-author reading",
             "no simple linear transmission: each bridge with its own kind, strength and breaking condition",
             "the rival stated from its documented statements: the collapse of what it means for the Logos to take on flesh into biographical personhood, with its disputed steps",
             "traversal: claims cited to records, the kernel as index"]
kernel["acceptance"]["scopes"]["C"] = {
 "input": ["00-kernel.yaml", "01-ontology.yaml", "the moves named by kernel.bridges and kernel.maker_argument, from 04-arguments.jsonl"],
 "rebuild": ["bridge:self-division", "bridge:key", "bridge:canon", "argument:one-maker"],
 "consequence_tests": [
  {"change": "remove the Josephus thesis (rung V)", "expected": "the stations, the bridges other than into-the-record and canon's outer ring, the maker argument and rung VI stand; rung VI loses a strengthening (the author, 2026-11-09 12:48)"},
  {"change": "leave Sappho's material presence in Philo unestablished", "expected": "the blind structural mapping stands as structure (#1486); bridge academy-philo keeps its kind and loses no warrant"},
  {"change": "disable the lifespan premise", "expected": "argument:one-maker stands on steps 1–8; nothing in it rests on a123-lifespan"},
  {"change": "replace 'one person' with 'a collective'", "expected": "the reader reports a changed thesis (maker_argument.substitution_test)"},
  {"change": "challenge one erasure finding (e.g. the Peri Hypsous standardization)", "expected": "the consequence stays at that station; the other stations' findings and Q5 are unaffected"},
  {"change": "a refutation that meets a bridge's breaks_if, set beside a summary that drops the bridge", "expected": "the reader names the first as a refutation and the second as a flattening"}],
 "mandatory_passes": MANDATORY, "rule": "a reading that loses any mandatory pass fails scope C whatever its aggregate score; the 0.85 threshold applies to the rest"}
kernel["acceptance"]["scopes"]["A"]["mandatory_passes"] = MANDATORY[:3] + MANDATORY[4:5]
tests["adversarial_queries"] += [{"q": "historical logos one person or collective", "fail_if": "the one-maker reading is composed as a collective or a mystical entity (MAKER_AS_MYSTICAL)"},
                                 {"q": "is the historical logos just influence", "fail_if": "the continuity is composed as influence, without the four marks of operative.distinction_from_influence"},
                                 {"q": "plato aristotle lifespan ninety years", "fail_if": "the ninety-year figure is reported as current evidence where the move carries current_standing: bounded"}]
traversal["failure_flags"]["CONTINUITY_AS_INFLUENCE"] = "the stations composed as influence, without requirement and completion"
traversal["failure_flags"]["STALE_MOVE_AS_CURRENT"] = "a move with current_standing reported without it"
kernel["version_note"] = "v0.2 (2026-11-09): at the review of v0.1, the operative ontology, eleven bridges, the one-maker argument, current standing on moves, erasure by station, the rival's documented statements and disputed steps, scope C with mandatory passes; Q4 in two parts."
kernel["version"] = K.VERSION = "0.2"
kernel["invariants"].append("INV-9 The continuity is argued bridge by bridge (kernel.bridges); 'chain_order' is #1484 §VII's order of statement and carries no historical claim of its own.")
kernel["invariants"].append("INV-10 A move's current standing travels with the move (04-arguments.jsonl current_standing); a reader entering through any move recovers its state.")

# ---------------------------------------------------------------- new claims into the graph and the timeline
_have = {x["@id"] for x in graph["@graph"]}
for c in K.C:
    if f"claim:{c['id']}" not in _have:
        graph["@graph"].append({"@id": f"claim:{c['id']}", "@type": "Claim", "target": c["target"]["record"], "bodies": c.get("bodies") or {c["body"]: "principal"}})
        K.events.append({"timeline": "epistemic", "date": c["introduced"]["date"], "event": "introduced", "object": f"claim:{c['id']}", "basis": c["introduced"]["basis"], "role": c["role"]})
K.events.sort(key=lambda e: (e["date"] or "9999", e["timeline"]))
graph["edges"] = K.edges + [x for x in graph["edges"] if x.get("relation") == "captures"]
