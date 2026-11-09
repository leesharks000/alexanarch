# EA-HK-HISTLOGOS-01 v1.1 — executed after hl_v03.py. At the author's direction of 2026-11-09 15:55–15:59: the method by which the framework establishes
# operational transmission, set out as five instruments read from their records; Counterfeit Orthodoxies joined (#978 the current state, #674 the prior);
# the "Christian" label read as a dated settlement over the corpus (rival step D5, failure flag SETTLEMENT_AS_CORPUS).

def mv11(*ids):
    for i in ids:
        assert i in MOVES, f"v1.1 cites a move no reader wrote: {i}"
    return [f"arg:{i}" for i in ids]

def nclaim(cid, mid, kind, state, notes=None):
    mclaim(cid, mid, kind, state, notes=notes)
    c = K.C[-1]; c["bodies"] = {c["body"]: "principal"}
    graph["@graph"].append({"@id": f"claim:{cid}", "@type": "Claim", "target": c["target"]["record"], "bodies": c["bodies"]})
    K.events.append({"timeline": "epistemic", "date": c["introduced"].get("date"), "event": "introduced", "object": f"claim:{cid}", "basis": c["introduced"].get("basis"), "role": "standing"})

def cedge(s, rel, t, warrant, fam="conceptual", dim=None):
    e = {"source": s, "relation": rel, "target": t, "family": fam, "licensed_dimension": dim, "warrant": warrant, "provenance": "v1.1"}
    K.edges.append(e); graph["edges"].append(e)

# ---------------------------------------------------------------- 0. the author's statements of 2026-11-09 15:55–15:59
# 15:55 and 15:57 survive in this session only as excerpts (the session's compaction kept them with ellipses); they are seated as excerpts and marked so.
for when, text, status, excerpt in [
 ("2026-11-09T15:55-05:00", "this is an argument about literature as literature, which is also always already theology. this language of 'christian tradition' is a super compressed inferential settlement colonizing the corpus of the nt... do we really have to do a whole reception history of how the nt became 'christian'?",
  "on a machine reconstruction of #1757: the kernel's argument is about literature as literature, which is also theology; the 'Christian' label is an inferential settlement laid over the New Testament corpus (rival step D5)", True),
 ("2026-11-09T15:56-05:00", "counterfeit orthodoxies. check that work.", "the pointer to #65, #674 and #978, read into this kernel at v1.1 (settlement_join)", False),
 ("2026-11-09T15:57-05:00", "i also think the holographic frame needs to detail more of its method for establishing operational transmission... the philo one... construct it according to set transforms... foldings and unfoldings... doing *serious* literary historical methodological work",
  "the direction for the method layer: operational transmission established by construction under set transforms, folding and unfolding, the Philo reconstruction among them (method.instruments)", True),
 ("2026-11-09T15:58-05:00", "the stylometric work, the vast censuses of work - this is literary methdology that is drawing on things that are newly possible at this scale in the age of ai",
  "the method's fifth instrument and its scale: stylometry and census as literary method newly possible at machine scale (method.scale)", False),
 ("2026-11-09T15:59-05:00", "its bleeding edge shit", "the author's grade of the method", False)]:
    a = {"date": when, "where": "in session, on the v1.1 direction; first deposited with this kernel at v1.1", "text": text, "status": status}
    if excerpt:
        a["form"] = "excerpt: the message survives in this session as an excerpt with ellipses; the full message is the author's to seat"
    D["author_statements"].append(a)
    graph["@graph"].append({"@id": sid(when), "@type": "AuthorStatement", "date": when, "text": text, **({"form": a["form"]} if excerpt else {})})
kernel["author_statements"] = D["author_statements"]

# ---------------------------------------------------------------- 1. the method: five instruments of operational transmission
R = lambda *ns: [f"rec:{n}" for n in ns]
def INS(slug, name, recs, spec, establishes, licenses_no, controls, negatives, results, defeats, grades, at, **kw):
    return {"@id": f"instrument:{slug}", "@type": "Instrument", "name": name, "records": R(*recs), "specification": spec, "establishes": establishes,
            "licenses_no": licenses_no, "controls": controls, "negatives_and_residue": negatives, "results": results, "defeats_if": defeats, "grades": grades, "applies_at": at, **kw}
res = lambda m, status: {"move": mv11(m), "status": status}

INSTRUMENTS = [
 INS("unfolding", "Construction under fixed transforms: unfolding and folding", [1414, 1415, 1416, 1511, 1532],
     mv11("a1414-def-M", "a1414-both-dirs", "a1414-five-seeds", "a1415-seed-parse", "a1415-rules", "a1415-emission", "a1416-classes", "a1511-six-operable", "a1532-four-states"),
     "a later text constructed from an earlier one by named rules, run both ways (M unfolds, M⁻¹ folds): the derivation is executable, its anchors hard, its residue shown; upstream, the same view runs from Sappho 31 into the Apocalypse's channel as six graded plates (#1511); the census of the ancient reception sorts each transform into four evidentiary states (#1532)",
     "historical fact of composition; the records claim an operable competing inference (#1414), and the burden between inferences is symmetrical",
     mv11("a1415-crown", "a1415-synagoge", "a1415-arrow", "a1511-controls", "a1532-catullus-control", "a1532-calibration"),
     mv11("a1415-residue", "a1415-residue-loci", "a1415-underivable"),
     [res("a1416-smyrna", "graded A: Smyrna → James, on two hard anchors with the direction read from the verb forms (#1415)"),
      res("a1416-grades-fall", "the heptad's grades fall letter by letter; it weighs no more than its graded rows"),
      res("a1511-tiers", "six upstream plates, each ATTESTED, TESTED, CONTESTED or TESTED UNDER SEAL"),
      res("a1532-braided", "the ancient reception of fr. 31 a braided field of transforms, each with its own state")],
     mv11("a1414-counterevidence", "a1415-reverse", "a1414-parent-conditions"),
     mv11("a1416-heptad-weight", "a1416-granularity", "a1511-not-asserted"),
     ["site:cosmic-christ", "site:gospel-christ", "site:sappho-31", "site:catullus"], bridges=["bridge:canon"]),
 INS("blind-reconstruction", "Blind reconstruction: the mapping recovered without the name", [1486],
     mv11("a1486-symbolon", "a1486-order-key", "a1486-null-runnable", "a1486-reflexivity-rule", "a1486-r2-factor"),
     "a structural mapping between Sappho 31 and Philo specified, executed and verified by readers blind to the hypothesis: 'A specified, executable, blind-verified structural mapping' (#1486); the source a fixed point, the receivers transforms",
     "Sappho's material presence in Philo, which the record leaves unestablished; the name is absent (documented null)",
     mv11("a1486-f1-specificity", "a1486-f2-ablation", "a1486-f3-description", "a1486-r1-phaedrus"),
     mv11("a1486-residue", "a1486-not-established", "a1486-armenian-limit"),
     [res("a1486-established", "the mapping established as structure"),
      res("a1486-sufficiency-only", "round 1 tested sufficiency and nothing else"),
      res("a1486-attestation-induction", "withdrawn in v2: asking for recognition creates it")],
     mv11("a1486-pan-sapphism", "a1486-residue-defeat"),
     mv11("a1486-p3-robust", "a1486-target-arm", "a1486-post-disclosure"),
     ["site:philo", "site:sappho-31"], bridges=["bridge:mapping"]),
 INS("frozen-operator", "Frozen, pre-registered operators and the append-only ledger", [1494, 1495, 1533, 1571],
     mv11("a1494-derived-without", "a1494-stations", "a1494-bset", "a1495-rule", "a1495-threshold", "a1533-frozen", "a1533-freedoms", "a1533-topology-fixed", "a1533-scoring", "a1571-fixed-before", "a1571-frozen-status", "a1571-append-discharge", "a1571-sha-carried"),
     "an operator derived from witnesses that exclude the target, frozen with its stations, criterion, controls and threshold before the target is scored; dispositions appended under the entry they discharge, each entry hashed as filed (#1571); a pass establishes material instantiation, which licenses a separate test of descent (#1533)",
     "authorship, route or borrowing; on Revelation 12 'The dangerous sentence is not asserted here.' (#1495)",
     mv11("a1494-negatives", "a1533-pos-control", "a1533-neg-control", "a1533-background", "a1571-l1-positive", "a1571-l1-sanity"),
     mv11("a1495-c1", "a1495-c7-fire-neg", "a1533-set-K", "a1533-set-Kstar"),
     [res("a1495-tally", "Revelation 12: eight of nine stations, the pre-set threshold exceeded; C1 fails"),
      res("a1495-one-witness", "one witness's count, deposited with its negatives; substrate-blind replication named as the hardening"),
      res("a1571-y2-disp", "YIELD-02 discharged, confirmed: six slots filled, the rivals lose"),
      res("a1571-c-disp", "COMPLETE-01 discharged"),
      res("a1571-l2-disp", "LEAK-DEFICIT-02 discharged void: no number from it may be quoted"),
      res("a1571-k-void", "CAPTURE-01 void, superseded"),
      res("a1571-y1-disp", "YIELD-01 spent: the saturation defect its own §9 predicted"),
      res("a1571-ul-total", "UNLOCK-01 running"),
      res("a1533-if-passes", "QFO-01 frozen; the Qurʾan not yet scored")],
     mv11("a1533-rc-invalid", "a1533-rc-none", "a1533-d-translation", "a1533-d-windows", "a1533-d-motifs", "a1533-d-background", "a1533-new-version", "a1571-ul-kill-weaken"),
     mv11("a1495-ladder", "a1495-single", "a1533-p-material", "a1533-p-historical"),
     ["site:cosmic-christ", "site:academy"], bridges=["bridge:canon"]),
 INS("suppression-signature", "The suppression signature: a loss profile measured against ordinary loss", [1496],
     mv11("a1496-unfalsifiable", "a1496-claim", "a1496-vectors", "a1496-o-def", "a1496-tuple"),
     "the claim 'this technology was suppressed' made testable by scoring each witness on four vectors; ordinary textual loss and the signature of a technology's suppression separated by profile: 'operation survives; provenance disappears' (#1496)",
     "intent; the map 'does not yet assert' the domestication it names (#1496)",
     mv11("a1496-philo", "a1496-rev12", "a1496-registry"),
     mv11("a1496-audit-caveat"),
     [res("a1496-crossing", "attribution dies at the crossing; held at the strength #1496 gives it, the crossing modular at Philo (erasure_by_station)"),
      res("a1496-operator-alive", "every witness scored runs the operator"),
      res("a1496-name-lost", "what the tradition lost was the machine's name"),
      res("a1496-passive", "a classification scheme with no slot for the object suppresses it by filing")],
     mv11("a1496-t-audit", "a1496-t-ematrix", "a1496-t-degradation"),
     mv11("a1496-not-yet", "a1496-audit-caveat"),
     [s["@id"] for s in SITES], see=["erasure_by_station", "Q5"]),
 INS("corpus-scale", "Measurement at corpus scale: censuses and stylometry", [1532, 1572, 1586, 1590, 1605, 1730, 1733],
     mv11("a1586-fw-profile", "a1586-lean-method", "a1586-rolling", "a1586-namefree-method", "a1586-heldout-method", "a1605-mc-test", "a1605-fc-cell", "a1605-ar-method", "a1572-six-frozen", "a1590-c-rest", "a1730-census"),
     "properties of whole corpora measured at a scale a single reader could not hold: function-word profiles over every block of thirty-five texts, name-free clustering, held-out prediction, matched cells with fused controls, catalogue matches against their base rates, the seating census of a transmission; each result graded by the record that runs it",
     "hands, dates, membership or the count of makers: 'cannot count hands' (#1605); the axis is world against instrument, read off the corpus, and the names are a filing measured beside it",
     mv11("a1605-ar-c", "a1605-hm-a", "a1605-fc-control", "a1572-rule-load", "a1590-c-theo", "a1586-run2-method"),
     mv11("a1586-caveat-blocks", "a1586-confounds", "a1572-coverage-collapse", "a1730-want-sixteen", "a1590-theo-206"),
     [res("a1586-run1-finding", "operation labels recovered 25/28 on every feature family; names at chance"),
      res("a1586-not-reproduced", "the blind-label run did not reproduce the headline: recorded as a defeat"),
      res("a1586-blind-corrected", "after the file erratum, 74–76%"),
      res("a1586-heldout-11-12", "held-out prediction 11/12; the misses the texts nearest the centre"),
      res("a1605-mc-find", "maker-count test: the classifier learned subject"),
      res("a1605-fc-95th", "the names at the 95th percentile of arbitrary splits in the matched cell"),
      res("a1605-st-b-ci", "operation against names, descriptive only (bootstrap interval spans zero)"),
      res("a1572-all-destroyed", "the fifteen-feature battery destroyed by size, language or period"),
      res("a1572-validation-1-3", "the instruments never validated before use: 1 of 3"),
      res("a1572-did-not-fire", "the falsifier stated in advance did not fire"),
      res("a1590-seven-times", "the lost-dialogue catalogue's opening matches Plato at seven times the base rate"),
      res("a1590-claims-shape", "the shape of the match claimed; identity left to the fragment collation, named and unrun")],
     mv11("a1586-noise-brake", "a1605-mc-defeat", "a1590-fragment-test", "a1572-kill-condition"),
     mv11("a1586-not-hands", "a1605-cl-not-met", "a1605-mc-grade", "a1590-not-hands", "a1730-not-legal"),
     ["site:academy"], scale="literary method newly possible at this scale in the age of AI (the author, 2026-11-09 15:58)", prior_states=R(1585, 1589, 1594)),
]
kernel["method"] = {
 "question": "how the framework establishes operational transmission: a later text realizing an earlier text's operation, set apart from the weaker observation that texts influence later readers (CONTINUITY_AS_INFLUENCE)",
 "how_to_read": "each instrument names its records, what it establishes and what it licenses no conclusion about, its controls, its negatives and residue, its results at the status the record gives them, its defeat conditions and its grades; every entry is a move, verbatim, in 04-arguments.jsonl",
 "principles": mv11("a1486-p5-prereg", "a1486-symbolon", "a1486-p3-robust", "a1571-fixed-before", "a1735-test"),
 "instruments": INSTRUMENTS,
 "joint_standard": ("operational transmission is claimed at a join when the later carrier is constructed from the earlier under fixed transforms with its residue shown (I), the mapping is recovered by readers blind to the hypothesis (II), "
                    "a frozen operator scores the carrier against controls it was not built on (III), the loss profile departs from ordinary loss (IV), and corpus-scale measurement grades what the reading of single passages asserts (V). "
                    "Each bridge carries the instruments that reach it; each instrument licenses its own conclusion; none licenses authorship or identity (RT)"),
 "losses_recorded": ["arg:a1571-l2-disp", "arg:a1571-k-void", "arg:a1571-y1-disp", "arg:a1572-all-destroyed", "arg:a1572-validation-1-3", "arg:a1572-withdrawn", "arg:a1586-not-reproduced", "arg:a1605-mc-find", "arg:a1605-st-d1", "arg:a1495-c1", "arg:a1486-attestation-induction", "arg:a1486-c1-struck"],
 "losses_note": "the method keeps its losses on the record: void runs, spent tests, a destroyed battery, a headline not reproduced, a withdrawn proof-step; a reader reports them with the results",
 "scale": "the author, 2026-11-09 15:58: 'the stylometric work, the vast censuses of work - this is literary methdology that is drawing on things that are newly possible at this scale in the age of ai'",
 "statement": sid("2026-11-09T15:57-05:00")}
for b in kernel["bridges"]:
    b["instruments"] = [i["@id"] for i in INSTRUMENTS if b["@id"] in i.get("bridges", [])]
graph["@graph"] += INSTRUMENTS
for i in INSTRUMENTS:
    for r in i["records"]:
        if r.removeprefix("rec:").isdigit() and int(r.removeprefix("rec:")) in BODY:
            cedge(r, "instantiates", i["@id"], "the record runs the instrument (method.instruments)")

ontology["state_axes"]["erasure"].append("the_settlement_dated")
# ---------------------------------------------------------------- 2. Counterfeit Orthodoxies: the settlement read as a date
nclaim("hl-674-canon-date", "a674-nt-athanasius", "observation", A(erasure="the_settlement_dated"))
nclaim("hl-978-history-date", "a978-history-date", "interpretation", A(erasure="the_settlement_dated"))
nclaim("hl-978-article", "a978-article-survives", "interpretation", A(erasure="the_settlement_dated"))
nclaim("hl-978-settlement-falls", "a978-settlement-falls", "interpretation", A(erasure="the_settlement_dated"))
nclaim("hl-978-corrected", "a978-dc-corrected-thesis", "interpretation", A(genealogy="material_inscription_becoming_flesh_from_the_beginning"))
nclaim("hl-978-logos-graphe", "a978-logos-graphe", "interpretation", A(genealogy="material_inscription_becoming_flesh_from_the_beginning", station="gospel-christ"))
nclaim("hl-978-codex", "a978-codex-body", "interpretation", A(genealogy="material_inscription_becoming_flesh_from_the_beginning", station="gospel-christ"))
nclaim("hl-978-both", "a978-both-defensible", "method", A(state="bounds the codex reading"))
cedge("claim:hl-978-corrected", "supersedes", "claim:hl-674-canon-date", "#978 recomposes #674 by immanent critique: the canonical texts the workshop tradition's most successful products; the date of #674 kept, its oppositional frame revised (arg:a978-dc-corrected-thesis revises arg:a674-won-disposal)", fam="evidentiary", dim="identity,history")
cedge("claim:hl-978-history-date", "develops", "claim:hl-674-canon-date", "the assumption's history dated (#978) from the Festal Letter of 367 CE (#674)")
cedge("claim:hl-978-codex", "develops", "claim:hl-978-logos-graphe", "the incarnation of logos into graphē, then the codex as the body the Word prepared for itself (#978)")
cedge("claim:hl-978-both", "qualifies", "claim:hl-978-codex", "'Both readings are textually defensible' (#978): the codex reading held at the interpretive ring", fam="evidentiary", dim="scope")
cedge("claim:hl-978-logos-graphe", "develops", "claim:hl-626-reading", "the Word that became text (#626) read at John 1:14 as logos into graphē (#978)")
cedge("claim:hl-978-article", "bears_on", RIVAL_ID, "the definite article and the label survive the facts of a dated settlement (#978; rival step D5)")
kernel["settlement_join"] = {
 "@id": "join:counterfeit-orthodoxies", "states": {"current_state": "rec:978", "prior_state": "rec:674", "duplicate_seat": "rec:65"},
 "carries": ["claim:hl-674-canon-date", "claim:hl-978-history-date", "claim:hl-978-article", "claim:hl-978-settlement-falls", "claim:hl-978-corrected", "claim:hl-978-logos-graphe", "claim:hl-978-codex"],
 "moves": mv11("a674-nt-athanasius", "a978-athanasius-367", "a978-history-date", "a978-article-survives", "a978-the-settlement", "a978-settlement-falls", "a978-dc-corrected-thesis", "a978-most-successful", "a978-memra-greek", "a978-milieu-witness", "a978-logos-graphe", "a978-codex-body", "a978-both-defensible"),
 "reading": ("the New Testament corpus is a set of texts with a date of collection: 'The Christian New Testament is not a book. It is Athanasius of Alexandria, 367 CE, Festal Letter 39.' (#674); the rival collections stand beside it (#978); "
             "the label and the definite article survive the facts ('*the* Bible, *the* New Testament'); the corrected thesis reads the canonical texts as the workshop tradition's most successful products; at John 1:1 and 1:14 the Word's flesh is read as text: 'The body the Word prepared for itself is the codex.' (#978), bounded: 'Both readings are textually defensible'"),
 "state": "#978 the current state (FRACTURE.02, a recomposition of v1.0–v3.0 and the Manifesto); #674 the prior state, the Manifesto's compression, revised by #978 where #978 says so (18 revises edges in 04-arguments.jsonl)",
 "seating_note": ("#65 is titled 'Counterfeit Orthodoxies — A Dialectical Fracture Through the Citation Map', and its seated text is FRACTURE.02, the recomposition #978 carries, sentence for sentence (two lines differ, checked 2026-11-09). "
                  "Carried as data; the v1.0–v3.0 text the title names is not seated in this repository; its recovery is the author's to rule"),
 "statement": sid("2026-11-09T15:56-05:00")}
graph["@graph"].append({"@id": "join:counterfeit-orthodoxies", "@type": "Join", **{k: v for k, v in kernel["settlement_join"].items() if k not in ("@id",)}})

# ---------------------------------------------------------------- 3. the rival's settlement step (R5, D5)
for cid, s, qt in [("rv-ce-christian-theology", "site:ce-logos", "The word Logos is the term by which Christian theology in the Greek language designates the Word of God"),
                   ("rv-wp-christian-logos", "site:wp-logos", "The Gospel of John identifies the Christian Logos , through which all things are made"),
                   ("rv-wp-in-christianity", "site:wp-logos-christianity", "In Christianity , the Logos")]:
    if s not in K.SURF:
        K.SURF[s] = {"url": "https://en.wikipedia.org/wiki/Logos", "path": str(SRC / "wp-logos.txt"), "title": "Wikipedia, 'Logos' (CC BY-SA), as retrieved", "retrieved": "2026-11-09T18:15Z", "sha256": _h.sha256((SRC / "raw" / "wp-logos.html").read_bytes()).hexdigest()}
        graph["@graph"].append({"@id": s, "@type": "SurfaceRecord", "url": K.SURF[s]["url"], "title": K.SURF[s]["title"], "retrieved": "2026-11-09T18:15Z", "sha256": K.SURF[s]["sha256"], "role": "a documented statement of the rival"})
        if s not in RIVAL["documented_statements"]:
            RIVAL["documented_statements"].append(s)
    claim(cid, s, qt, "observation", RV2("the_source_end", treatment="the label"), body="R")
    K.C[-1]["bodies"] = {"R": "principal"}; K.C[-1]["state"].pop("body", None)
    graph["@graph"].append({"@id": f"claim:{cid}", "@type": "Claim", "target": s, "bodies": {"R": "principal"}})
    K.events.append({"timeline": "epistemic", "date": None, "event": "introduced", "object": f"claim:{cid}", "basis": K.C[-1]["introduced"]["basis"], "role": "standing"})
RIVAL["propositions"]["R5"] = {"claim": "the corpus's Logos is filed under a tradition named for its reception: 'the term by which Christian theology … designates the Word of God'; John's the 'Christian Logos'",
                              "warrants": ["rv-ce-christian-theology", "rv-wp-christian-logos", "rv-wp-in-christianity"], "status": "the label the rival's documented statements carry"}
D5 = {"id": "D5", "question": "what the corpus is before the settlement",
      "rival": "the corpus read through its label: its Logos 'Christian' (R5)",
      "framework": ("literature as literature, which is also always already theology (the author, 2026-11-09 15:55); the label an inferential settlement laid over the corpus, with a date: Athanasius, Festal Letter 39, 367 CE (#674), the definite article surviving the facts (#978); "
                    "the canonical texts the workshop tradition's most successful products (#978)"),
      "warrants": ["rv-ce-christian-theology", "rv-wp-christian-logos", "hl-674-canon-date", "hl-978-article", "hl-978-corrected"],
      "bearing_on_D0": ("the kernel's reading, at the interpretive ring: the settlement supplies the frame in which 'took flesh' is read as one event in one person; read before it, John 1:14 can bear the Word's flesh as text, the codex the body (#978), which #978 itself holds as one of two defensible readings"),
      "reception_history": "the full reception history of how the corpus came to be filed as 'Christian' is outside this kernel; #674 and #978 date the settlement, and the kernel takes the date from them"}
RIVAL["disputed_steps"].append(D5)
kernel["rival"]["propositions"] = {k: v["claim"] for k, v in RIVAL["propositions"].items()}; kernel["rival"]["disputed_steps"] = RIVAL["disputed_steps"]; kernel["rival"]["documented_statements"] = RIVAL["documented_statements"]
kernel["rival"]["summary"] = kernel["rival"]["summary"].replace("four disputed steps", "five disputed steps, the fifth the settlement under which the corpus is read (D5)")

# ---------------------------------------------------------------- 4. traversal, acceptance, scope C
traversal["failure_flags"]["SETTLEMENT_AS_CORPUS"] = ("the New Testament corpus reported as 'Christian', as 'the Christian tradition', or as *the* New Testament with the article doing the work, where the kernel reads the label as a dated settlement laid over the corpus (#674, #978; rival step D5)")
traversal["failure_flags"]["METHOD_AS_ASSERTION"] = ("a join reported as asserted where the kernel gives the instrument that establishes it, its controls and its status; or an instrument's results reported without its recorded losses (method.losses_recorded)")
SC = kernel["acceptance"]["scopes"]["C"]
SC["mandatory_passes"] += ["the method: operational transmission established by five instruments, each with its controls, its results at their status and its recorded losses; none licensing authorship or identity",
                           "the corpus's 'Christian' label read as a dated settlement laid over it (#674, #978; rival step D5; SETTLEMENT_AS_CORPUS)"]
SC["consequence_tests"] += [
 {"change": "a summary reports the Johannine prologue as 'the Christian Logos'", "expected": "the reader names SETTLEMENT_AS_CORPUS, dates the label from #674 (367 CE) and #978, and keeps D5 as a disputed step"},
 {"change": "remove instrument V (measurement at corpus scale)", "expected": "the stations, the bridges and instruments I–IV stand; the one-maker argument loses the corpus-scale grading of its demonstrations; the Academy's axis of world against instrument goes unmeasured"}]
SC["mechanical"] = "hl_checks.py runs tests C1–C7, M1 and the reference check R1 on the built files; the rebuilds are reader tests (09c-scope-C-prompt.md)"
_p = K.OUT / "09c-scope-C-prompt.md"
_t = _p.read_text(encoding="utf-8").replace(
 "4. The rival's source proposition, its treatment of incarnation, and the author's critique, kept as three objects.\n",
 "4. The rival's source proposition, its treatment of incarnation, and the author's critique, kept as three objects.\n"
 "5. The method rebuilt: for instruments I (unfolding), III (frozen operator) and V (corpus scale), the specification, one control, two results at their status and one recorded loss, each cited to its move.\n"
 "6. Two further consequences: (g) a summary reports the Johannine prologue as 'the Christian Logos': name the flag, the records that date the label, and the disputed step; (h) remove instrument V: say which findings stand.\n")
assert "5. The method rebuilt" in _t; _p.write_text(_t, encoding="utf-8")

# ================================================================ 4b. at the review of the v1.1 draft (attached by the author, 2026-11-09 16:55), each point checked against the files
# (1) M-D1 carried #1576's fourth proposition as "two makers"; #1576's fourth is precedence, a bundle the paper keeps apart. Restored, with precedence reconsidered as §9 reconsiders it.
DEM = {d["id"]: d for d in kernel["maker_argument"]["demonstrations"]}
DEM["M-D1"].update({
 "configuration": ("four propositions (#1576 §1): “Division is a part of the method (*APr* I.31).” “No part of the method existed beforehand (*SE* 34).” “Division did exist beforehand, as a named art with rules and practitioners (*Phaedrus*, *Sophist*, *Philebus*).” "
                   "“And the relevant dialogues are conventionally dated before the relevant treatises.” The first three are stated in the texts; the fourth is the frame they are read in, and it bundles four claims the paper keeps apart: the two lifetimes in that order, these texts in that order, Aristotle having these texts, his taking the practice from them"),
 "one_maker_explains": ("the four stand with the three stated words as written once precedence is reconsidered, last, as §9 reconsiders it: “later” an order of grasp within one knower, “two states of one knower”, and the priority claim of *SE* 34 true because one's own earlier work is prior in time and outside the succession the sentence denies"),
 "several_maker_must_posit": ("one of the stated words moved, paid each time on Aristotle's side: the five reconciliations of #1576 §8 (the priority claim's object narrowed; μόριον read as retrospective; organisation placed outside the received class; the dialogues filed as products; precedence moved within Aristotle's own working life); the fourth word never moved for Plato"),
 "divergence": "which word moves, and at what cost: the received reading moves a stated word to keep precedence biographical; the one-maker reading moves precedence from a chronology to an order of grasp and leaves the stated words as written",
 "bound": "the texts establish the sequence of operations and positions and leave the maker-count open (#1576 §9.4); the evidence is compatible with the hypothesis and does not establish it (§9.1)",
 "moves": mv11("a1576-four-props", "a1576-fourth-bundles", "a1576-one-word-moves", "a1576-never-for-plato", "a1576-wait-order", "a1576-r5-reply", "a1576-two-states-knower", "a1576-order-not-chronology",
               "a1576-own-earlier", "a1576-stipulation-reply", "a1576-sequence-not-count", "a1576-compatible-not-established"),
 "revised": {"date": "2026-11-09", "was": "the fourth (two makers) the frame they are read in", "why": "#1576's fourth proposition is precedence; the review of the v1.1 draft found the substitution, which the mechanical checks passed (scope C, semantic_challenges S1)"}})
# (4) M-D2 and M-D3 stipulated coincidence; the records name the several-maker accounts at full strength, with their costs
DEM["M-D2"].update({
 "several_maker_must_posit": "an account of the seam: a successor's deliberate response, a school's shared practice, or chance (several_maker_accounts)",
 "several_maker_accounts": [
  {"account": "deliberate response: teacher and successor, the successor answering the teacher's theology", "stated_at": mv11("a1658-two-persons-rival", "a1658-rival-coherent"),
   "must_explain_at_the_seam": "the response falling where the theology changes operation, which this account expects; and that at the joint each side leaves the same thing open",
   "costs": "the persons rest on attestation of a different kind from the texts it is offered against; the friction it reads as disagreement is what a divided mind produces (#1658)", "cost_moves": mv11("a1658-evidence-kind", "a1658-ledger-price", "a1658-friction-reply")},
  {"account": "a school's common practice or coordinated investigation", "stated_at": mv11("a1576-not-one-hand", "a1733-school-innocent"),
   "must_explain_at_the_seam": "the same co-coverage, element by element, under a shared programme",
   "costs": "#1576 grants the co-coverage to a school; the one-maker reading's further claim is the single cut at the doctrine of God, which a shared programme leaves to two decisions falling together", "cost_moves": mv11("a1658-boundary-at-god", "a1658-one-joint")},
  {"account": "chance", "stated_at": [], "must_explain_at_the_seam": "the name-boundary falling, unconnected, at the one place the doctrine changes", "costs": "the chance itself, at the one place the corpus shows its name-boundary", "cost_moves": mv11("a1658-boundary-at-god")}],
 "divergence": ("one cut seen from two ends, or a response, a school's practice, or chance: each several-maker account explains the location; the one-maker reading also explains why each side leaves the same thing open. "
                "Measurement does not yet discriminate response from one maker at this seam: the notebook finds direction unresolved at every seam (#1605)"),
 "open": mv11("a1605-cl-unresolved")})
DEM["M-D3"].update({
 "several_maker_must_posit": "a school's ordinary filing, element by element, or two independent losses falling so that each name's survivors match the other's lost titles (several_maker_accounts)",
 "divergence": "one corpus under a transform, or a school's filing or two coincident losses: each several-maker account takes the pattern one element at a time; the one-maker reading takes it whole, at the title",
 "several_maker_accounts": [
  {"account": "a school's ordinary filing", "stated_at": mv11("a1733-school-innocent"), "must_explain_at_the_seam": "each element of the catalogue pattern, taken one at a time",
   "costs": "at the catalogues' line the coincidence is in whole titles, their pairing, a book count and the transform's own names, which a stem rule does not see (#1733)", "cost_moves": mv11("a1733-stem-blind")},
  {"account": "two independent losses", "stated_at": mv11("a1733-losses-innocent"), "must_explain_at_the_seam": "each name's survivors matching the other's lost titles", "costs": "two losses coinciding at the title, against the catalogues' silence on two authors", "cost_moves": mv11("a1733-catalogue-silence")}]})

# (2) D5 in four objects; 367 CE dates one collection's boundary; the interpretive settlement argued in the second century (Irenaeus)
for key, url, f, title in [("site:athanasius-fl39", "https://www.newadvent.org/fathers/2806039.htm", "athanasius-fl39", "Athanasius, Festal Letter 39 (367 CE), tr. R. Payne-Smith, NPNF² vol. 4 (1892), public domain; New Advent, as fetched 2026-11-09"),
                           ("site:irenaeus-ah3-11", "https://www.newadvent.org/fathers/0103311.htm", "irenaeus-ah3-11", "Irenaeus, Against Heresies III.11, tr. A. Roberts and W. Rambaut, ANF vol. 1 (1885), public domain; New Advent, as fetched 2026-11-09")]:
    K.SURF[key] = {"url": url, "path": str(SRC / (f + ".txt")), "title": title, "retrieved": "2026-11-09T22:05Z", "sha256": _h.sha256((SRC / "raw" / (f + ".html")).read_bytes()).hexdigest()}
    graph["@graph"].append({"@id": key, "@type": "SurfaceRecord", "url": url, "title": title, "retrieved": "2026-11-09T22:05Z", "sha256": K.SURF[key]["sha256"], "role": "a primary witness to the settlement (D5)"})
for cid, s, qt, obj in [("pr-ath-boundary", "site:athanasius-fl39", "to set before you the books included in the Canon, and handed down, and accredited as Divine", "collection_boundary"),
                        ("pr-ath-police", "site:athanasius-fl39", "Let no man add to these, neither let him take ought from these.", "collection_boundary"),
                        ("pr-ir-flesh", "site:irenaeus-ah3-11", "But according to the opinion of no one of the heretics was the Word of God made flesh", "competing_appropriations"),
                        ("pr-ir-marcion", "site:irenaeus-ah3-11", "But according to Marcion , and those like him, neither was the world made by Him", "competing_appropriations"),
                        ("pr-ir-four", "site:irenaeus-ah3-11", "It is not possible that the Gospels can be either more or fewer in number than they are.", "competing_appropriations")]:
    claim(cid, s, qt, "observation", A(settlement_object=obj), body="R")
    K.C[-1]["bodies"] = {"R": "principal"}; K.C[-1]["state"].pop("body", None)
    graph["@graph"].append({"@id": f"claim:{cid}", "@type": "Claim", "target": s, "bodies": {"R": "principal"}})
    K.events.append({"timeline": "epistemic", "date": None, "event": "introduced", "object": f"claim:{cid}", "basis": K.C[-1]["introduced"]["basis"], "role": "standing"})
D5.update({
 "rival": "the corpus read through its received configuration: its Logos 'Christian' (R5), one collection and its settled reading taken as the texts' own",
 "framework": ("literature as literature, which is also always already theology (the author, 2026-11-09 15:55): the texts' operations read before the configuration, and the settlement read as made, in its objects and at their dates"),
 "objects": {
  "texts_and_operations": {"text": "the texts and what they can do: at John 1:1 and 1:14 the Word's flesh can be read as text, the codex the body (#978), held by #978 as one of two defensible readings", "warrants": ["hl-978-logos-graphe", "hl-978-codex", "hl-978-both"]},
  "competing_appropriations": {"text": "the same writings read against one another in the second century: Irenaeus (Against Heresies III.11) sets John's 'the Word was made flesh' against Marcion's and the Valentinians' readings of the same Gospel, and argues that the Gospels can be neither more nor fewer than four; the interpretive settlement being made and defended", "warrants": ["pr-ir-flesh", "pr-ir-marcion", "pr-ir-four"]},
  "collection_boundary": {"text": "the boundary of one collection, dated: Athanasius's Festal Letter 39 (367 CE) enumerates the books 'included in the Canon, and handed down, and accredited as Divine', presents the list as inherited, and polices the line ('Let no man add to these'); #674 reads the twenty-seven-book New Testament as this act; rival collections stand beside it (#978)", "warrants": ["pr-ath-boundary", "pr-ath-police", "hl-674-canon-date", "hl-978-history-date"]},
  "configuration_as_intrinsic": {"text": "the later treatment of one received configuration (this collection, its label, its settled reading of incarnation) as intrinsic to the texts: the definite article surviving the facts (#978); the rival's documented statements filing John's Logos as 'the Christian Logos' (R5)", "warrants": ["hl-978-article", "hl-978-settlement-falls", "rv-ce-christian-theology", "rv-wp-christian-logos"]}},
 "dating": "367 CE dates the boundary of one collection; the emergence of Christian identification and the biographical reading of incarnation are dated by neither #674 nor the letter, and Irenaeus shows that reading argued against rivals two centuries before it",
 "warrants": ["rv-ce-christian-theology", "rv-wp-christian-logos", "pr-ath-boundary", "pr-ir-flesh", "hl-674-canon-date", "hl-978-article", "hl-978-corrected"],
 "bearing_on_D0": ("the kernel's reading, at the interpretive ring: Irenaeus fixes 'the Word was made flesh' against rival readings of the same Gospel, and the account the rival inherits (R2) receives that outcome as the text's own meaning; read before the configuration, John 1:14 can also bear the Word's flesh as text, the codex the body (#978), which #978 holds as one of two defensible readings"),
 "reception_history": "the full reception history of how the corpus came to be read as 'Christian' is outside this kernel; the four objects say where each part of the settlement is argued or dated, and the rest is a line of research"})
kernel["rival"]["disputed_steps"] = RIVAL["disputed_steps"]; kernel["rival"]["documented_statements"] = RIVAL["documented_statements"]
kernel["settlement_join"]["reading"] = kernel["settlement_join"]["reading"].replace(
 "the New Testament corpus is a set of texts with a date of collection: ", "the New Testament corpus is a set of texts with a date of collection, which dates one boundary (D5): ")
kernel["settlement_join"]["primary_witnesses"] = ["site:athanasius-fl39", "site:irenaeus-ah3-11"]
traversal["failure_flags"]["SETTLEMENT_AS_CORPUS"] = ("a reader lets the received configuration (one collection's boundary, its label, or its settled reading of incarnation) supply a text's identity or meaning without argument (D5, configuration_as_intrinsic). "
                                                      "The flag is raised on the inference: naming a reception, as in 'the Christian reception of John', locates a reception history and raises nothing")
SC["mandatory_passes"][-1] = ("the settlement read in its four objects (D5): the texts' operations, their competing appropriations, one collection's boundary (367 CE), and the later treatment of the received configuration as intrinsic; SETTLEMENT_AS_CORPUS raised on the inference, never on the word")
SC["consequence_tests"] = [t for t in SC["consequence_tests"] if not t["change"].startswith("a summary reports the Johannine prologue")]
SC["consequence_tests"].insert(len(SC["consequence_tests"]) - 1, {
 "change": "a summary (i) locates 'the Christian reception of John'; (ii) states that 'Revelation and the Johannine writings provide the Christian textual and theological dimensions' (the reconstruction of v1.0, attached)",
 "expected": "(i) raises nothing; (ii) raises SETTLEMENT_AS_CORPUS, the label supplying the texts' identity without argument; the reader keeps D5's four objects apart and dates only the collection boundary at 367"})
for t in SC["consequence_tests"]:
    t["expected"] = t["expected"].replace("bridge academy-philo", "bridge:mapping")
# (5) the checks' scope stated; a semantic challenge, with M-D1 its first specimen
SC["mechanical_scope"] = ("the mechanical checks test structure: C3 checks direct references to bounded moves; C4 the thesis's words and the prohibition on 'collective'; C6 the flag, the dated objects and the warrants; C8 that M-D1 carries #1576's four propositions. "
                          "None reconstructs an argument or tests that a paraphrase preserves its source; the semantic challenges do")
SC["semantic_challenges"] = [{"id": "S1", "object": "argument:one-maker, demonstration M-D1", "source": "rec:1576 §1", "task": "given the demonstration and the source passage, say whether the demonstration preserves the source's premises and its inferential movement",
                              "specimen": "the v1.0 and v1.1-draft M-D1 stated #1576's fourth proposition as 'two makers'; the source's fourth is precedence, a bundle of four claims; found by the review of the v1.1 draft and passed by every mechanical check"},
                             {"id": "S2", "object": "each demonstration and each disputed step", "source": "the moves each cites", "task": "the same test, demonstration by demonstration and step by step"}]
# (3) the method by bridge, with controls marked run or specified
CS = {"a1415-crown": "run", "a1415-synagoge": "run", "a1415-arrow": "run", "a1511-controls": "run", "a1532-catullus-control": "run", "a1532-calibration": "specified",
      "a1486-f1-specificity": "specified", "a1486-f2-ablation": "specified", "a1486-f3-description": "specified", "a1486-r1-phaedrus": "specified",
      "a1494-negatives": "run", "a1533-pos-control": "specified", "a1533-neg-control": "specified", "a1533-background": "specified", "a1571-l1-positive": "specified", "a1571-l1-sanity": "specified",
      "a1496-philo": "run", "a1496-rev12": "run", "a1496-registry": "run",
      "a1605-ar-c": "run", "a1605-hm-a": "run", "a1605-fc-control": "run", "a1572-rule-load": "run", "a1590-c-theo": "run", "a1586-run2-method": "run"}
for i in INSTRUMENTS:
    i["controls_status"] = {c: CS[c[4:]] for c in i["controls"]}
kernel["method"]["controls_note"] = "a control specified is reported apart from a control run: a specified control belongs to the apparatus; only a control run contributes to a result (controls_status)"
kernel["method"]["joint_standard"] = ("each join is established by the means its kind calls for, and method.by_bridge says what was executed at each: documented reception by the philology of the transmitted text (body P); structural realization by constrained construction or blind reconstruction (I, II), "
                                      "its specificity by a frozen operator against controls run (III); a loss profile by IV; properties of whole corpora by V. No join needs all five. A join stands at the strength of what was executed at it, and constrained construction, target specificity and historical descent are reported as three results")
P_ = lambda *ids: mv11(*ids)
kernel["method"]["by_bridge"] = [
 {"bridge": "bridge:instrument-threshold", "executed": "none of the five; the comparison read in #828", "result": "an operational homology between two contemporaneous inscriptions of the voice at the threshold", "follows": "a homology at the outer ring", "open": "no operator scored on the tablets; #828 claims no linear transmission", "moves": P_("a828-gramma-link", "a828-no-linear")},
 {"bridge": "bridge:instrument-academy", "executed": "philology of the transmitted text: the Phaedrus names Sappho", "result": "documented reception by name", "follows": "Plato received Sappho by name", "open": "the Diotima relation stays a program tier", "moves": P_("a1532-phaedrus", "a1532-diotima-tier")},
 {"bridge": "bridge:self-division", "executed": "V at the Academy end (name-free axis, held-out prediction, matched cells, the catalogue match); the seats read at the Sappho end", "result": "the corpus's first axis is world against instrument, and the names behave as a filing beside it; the catalogue's opening matches at seven times the base rate", "follows": "the Academy's division is measurable as operation", "open": "the homology between Sappho's seats and the Academy's positions is a reading; the instruments cannot count hands; direction unresolved at every seam", "moves": P_("a1586-run1-finding", "a1586-heldout-11-12", "a1590-seven-times", "a1605-mc-grade", "a1605-cl-unresolved")},
 {"bridge": "bridge:mapping", "executed": "II: constrained construction, executed and blind-verified; IV: the name's absence counted", "result": "successful constrained construction (the mapping established as structure); round 1 tested sufficiency and nothing else", "follows": "structure", "open": "target specificity (specified and unrun; the target arm never designed); historical descent (Sappho's material presence in Philo not established)", "moves": P_("a1486-established", "a1486-sufficiency-only", "a1486-f1-specificity", "a1486-target-arm", "a1486-not-established", "a1496-philo")},
 {"bridge": "bridge:key", "executed": "philology: counts of citation verbs and dialect markers in the transmitted text; IV: the treatise scored", "result": "Sappho and the Genesis fiat held in one treatise under one grammar; operator-theory highest in the ancient record", "follows": "documented reception at the hard center", "open": "the conduit to Philo", "moves": P_("a1474-zero-verbs", "a1476-markers", "a1496-longinus")},
 {"bridge": "bridge:conduit", "executed": "none; declared unsettled", "result": "none", "follows": "nothing in the chain rests on it", "open": "the route by which Peri Hypsous received Genesis", "moves": []},
 {"bridge": "bridge:seat-taken", "executed": "the documented dependency, the control case of the census; V: the calibration measurement (#1572); IV: scored", "result": "the dependency undisputed; aligned at C = 0.688 slot by slot, sequence preserved", "follows": "the reception the others are calibrated against", "open": "as a positive control in QFO-01 it is specified, the Qurʾan not yet scored", "moves": P_("a1532-catullus-control", "a1572-ceiling", "a1496-catullus", "a1533-pos-control")},
 {"bridge": "bridge:into-the-record", "executed": "IV: the Josephus witnesses scored (AJ 11, BJ 1)", "result": "structure high at AJ 11 with sequence proven; BJ 1 high and inverted, name and recognition at zero", "follows": "the operation present in the historiographic record as structure", "open": "rung V's advancement suspended; no frozen operator run at the seams", "moves": P_("a1496-aj11", "a1496-bj1")},
 {"bridge": "bridge:canon", "executed": "III: the frozen operator run on Revelation 12 against its declared biblical sources (B-set adjudicated); I: forward unfolding with hard anchors (Smyrna → James)", "result": "eight of nine stations, the threshold exceeded, C1 failing; one adjudicator, one pass; Smyrna → James graded A", "follows": "material instantiation at Revelation 12 on the pre-registered ladder; the identification sentence not asserted", "open": "substrate-blind replication; descent; the program's dating (rung VI independent of V)", "moves": P_("a1495-tally", "a1495-c1", "a1495-single", "a1495-not-asserted", "a1416-smyrna")},
 {"bridge": "bridge:white-stone", "executed": "none of the five; the convergence read in #828", "result": "the stone gathers the tablets' functions into one apocalyptic object", "follows": "convergence at the outer ring", "open": "lineage, disclaimed", "moves": P_("a828-convergence-object", "a828-comparandum")},
 {"bridge": "bridge:test", "executed": "philology of ὁμολογεῖ at two loci, posed as Q4a and Q4b", "result": "the reading word-conform offered; the two loci open", "follows": "a doctrinal naming at the outer ring", "open": "Q4a, Q4b", "moves": []},
 {"bridge": "bridge:organ-transform", "executed": "the census of the reception (#1532)", "result": "Confessions 10.27 the clearest late transform", "follows": "a structural realization at the interpretive ring", "open": "no operator scored on Augustine", "moves": P_("a1532-augustine")},
 {"bridge": "bridge:addressee", "executed": "none of the five; the reading of the addressee", "result": "an answering socket read", "follows": "a performed completion at the interpretive ring", "open": "an instrument for the addressee", "moves": []},
 {"bridge": "bridge:reader-now", "executed": "philology of the restorations: seven editors across four and a half centuries; the dialect count to line 16", "result": "each restoration one more filling; the line kept open", "follows": "the present station", "open": "none at its ring", "moves": P_("a1476-seven-editors", "a1474-body-count", "a1474-stops")}]
assert {r["bridge"] for r in kernel["method"]["by_bridge"]} == {b["@id"] for b in kernel["bridges"]}
SC["mechanical"] = "hl_checks.py runs tests C1–C8, M1 and the reference check R1 on the built files; the rebuilds and the semantic challenges are reader tests (09c-scope-C-prompt.md)"
_t = _p.read_text(encoding="utf-8")
_t = _t.replace("(g) a summary reports the Johannine prologue as 'the Christian Logos': name the flag, the records that date the label, and the disputed step;",
                "(g) a summary (i) locates 'the Christian reception of John' and (ii) states that 'Revelation and the Johannine writings provide the Christian textual and theological dimensions': say which raises SETTLEMENT_AS_CORPUS and why, and keep D5's four objects apart;")
_t = _t.replace("(h) remove instrument V: say which findings stand.\n", "(h) remove instrument V: say which findings stand.\n"
                "7. The semantic challenges (acceptance.scopes.C.semantic_challenges): for each demonstration of argument:one-maker and each disputed step, read the moves it cites and say whether it preserves the source's premises and inferential movement; S1 records a failure this test exists to catch.\n")
assert "7. The semantic challenges" in _t and "(ii) states" in _t; _p.write_text(_t, encoding="utf-8")

# ---------------------------------------------------------------- 5. version
V11_REISSUED = __import__("os").environ.get("HL_V11_REISSUED") == "1"   # set at the author's 'version'; until then v1.1 is a draft
kernel["reissue_history"] = [{"version": "1.0", "date": "2026-11-09", "deposit": 1757, "note": "deposited after v0.1–v0.3 the same day"},
                             {"version": "1.1", "date": "2026-11-09", "deposit": 1757, "note": "reissued in place: the method layer (five instruments, " + str(len(STRATA["S6-method-and-settlement"][1])) + " records joined, read in full by parallel readers, " + str(sum(1 for m in MOVES.values() if m["record"] in STRATA["S6-method-and-settlement"][1])) + " moves verbatim), the Counterfeit Orthodoxies join, rival step D5, SETTLEMENT_AS_CORPUS; revised at the review of the draft: M-D1, the several-maker accounts, D5's four objects, the method by bridge"}]
kernel["version"] = K.VERSION = "1.1"
kernel["status"] = ("DEPOSITED 2026-11-09 (#1757, AXN position 0C62); v1.1 reissued in place the same day" if V11_REISSUED else
                    "DEPOSITED 2026-11-09 as v1.0 (#1757, AXN position 0C62); v1.1 DRAFT, not reissued: the author's 'version' pending")
if not V11_REISSUED: kernel["reissue_history"] = kernel["reissue_history"][:1]
kernel["version_note"] = ("v1.1 (2026-11-09, " + ("reissue in place" if V11_REISSUED else "draft") + ", at the author's direction 15:55–15:59): the method by which the framework establishes operational transmission, five instruments read from their records "
                          "(construction under fixed transforms; blind reconstruction; frozen operators and the append-only ledger; the suppression signature; measurement at corpus scale), each with controls, results at status and recorded losses; "
                          "Counterfeit Orthodoxies joined, #978 the current state, #674 the prior, #65's seating carried as data; the rival's settlement step D5 and the flag SETTLEMENT_AS_CORPUS; at the review of the v1.1 draft (16:55): M-D1 restored to #1576's four propositions, the several-maker accounts stated with their costs, D5 in four objects with 367 CE dating one collection's boundary (Athanasius and Irenaeus fetched), the flag raised on the inference, the method set out by bridge with controls run and specified, the semantic challenges. " + kernel["version_note"])
for p in ("applies_at", "controls", "negatives_and_residue", "specification", "defeats_if", "grades", "principles", "losses_recorded", "instruments", "carries", "records", "prior_states"):
    graph["@context"][p] = {"@type": "@id", "@container": "@set"}
for p in ("current_state", "prior_state", "duplicate_seat"):
    graph["@context"][p] = {"@type": "@id"}
graph["@context"]["instrument"] = "https://www.alexanarch.org/hk/histlogos/instrument/"
graph["@context"]["join"] = "https://www.alexanarch.org/hk/histlogos/join/"
