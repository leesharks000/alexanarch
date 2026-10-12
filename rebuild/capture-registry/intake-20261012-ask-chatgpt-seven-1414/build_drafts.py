#!/usr/bin/env python3
"""Author seven more ChatGPT captures at the record pages' Ask ChatGPT prompts, 2026-10-12, from the operator's attachments of
14:14 EDT ("the stones is perhaps one of the more important pieces... easy to miss"), the same run (signed out, incognito, the
initial prompt being the deposit's ChatGPT button). Every quotation and figure the findings rest on is asserted against the
seated text first. NEW addresses."""
import pathlib
exec((pathlib.Path(__file__).resolve().parent / "_head.py").read_text(encoding="utf-8"))
_N0 = N
N = lambda s: _N0(s).replace("’", "'").replace("‘", "'")
L1581 = "Theoretical paper AXN:066F.GENERATIVE.🙏🔺☁️🌲💧🤝"
L1552 = "Theoretical paper AXN:064D.GENERATIVE.🔼🎲🧭🎨🌱⚓"
REL.update({L1581: "archive_controlled", L1552: "archive_controlled", "Machine-Mediated Reception Studies": "authored_surface",
            "alexanarch.org": "archive_controlled"}); CHIPS = set(REL)
NOTE.update({L1581: "a label of the content type and #1581's AXN, alexanarch fields; which page not resolved",
             L1552: "a label of the content type and #1552's AXN, alexanarch fields; which page not resolved",
             "Machine-Mediated Reception Studies": "machinemediation.org, the author's reception-studies site; the answer names its 'Reception Edges' page",
             "alexanarch.org": "the archive; the answer names the JSON Schema and edges.json"})
OUT = []
def G(n): return pathlib.Path(ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")

# ── 1 · #1592 Two Lists of Stones (v0.1) ─────────────────────────────────────────────────────────────────────────────
raw, (a1,), seen, cut = load("paste-two-lists-of-stones-1592.txt")
t = text(1592)
inall(["an instrument, or an address"], a1, t.replace("One stone is an instrument; the other is an address", "an instrument, or an address"))
for s in ["ἐξ οὗ καὶ τὰ σφραγίδια γλύφουσιν", "ἐν ᾧπερ καὶ τὰ ἑξάγωνα", "ἡ πόλις **τετράγωνος** κεῖται", "Μὴ σφραγίσῃς", "ψῆφον λευκήν",
          "λαμπυρίζουσαν καθάπερ ὁ κόκκος", "Callias", "about ninety years", "Borges's crimson hexagon", "a third term",
          "the archive's stamp doctrine (a seal derived from the sealed)", "a different technology", "the stone in its third sense",
          "the juxtaposition of Theophrastus, cinnabar and crimson hexagons is Lee Sharks's", "Exodus 28 and Ezekiel 28"]:
    assert s in t, s
for s in ["Borges", "stamp", "Callias", "cinnabar", "κόκκος", "kermes", "AXN", "third sense", "a different technology"]:
    assert s.lower() not in a1.lower(), s
assert "The essay characterizes the relevant geometry as a tetragon" in a1
assert "a named inventor from ninety years earlier" in a1 and "Exodus 28 and Ezekiel 28" in a1
OUT.append(base(1592, "two-lists-of-stones-ask-chatgpt-20261012",
    "THE RELATIONS READ AS RELATIONS; THE THIRD TERM AND THE STAMP DOCTRINE LEFT OUT",
    ("asked for the arguments of Two Lists of Stones, grounded in the text, ChatGPT reads #1592 (chip: Goodreads ×8) in the note's "
     "order and keeps its rule, relations established and readings withheld: the two lists, by δύναμις and by position; σφραγίς twice, "
     "the seal carved from the red unburnable ἄνθραξ and the seal set on the book, persons and speech (5:1, 7:3–4, 10:4), against 'do "
     "not seal' (22:10) and 22:18; κόκκινον at two ends of a supply chain; the hexagons of the stone at Miletus against the measured "
     "city of 21:16; the white ψῆφος of 2:17, quoted as the note's pair, 'an instrument, or an address'; Exodus 28 and Ezekiel 28 left "
     "untraced. What it does not carry is where the note ties itself to the archive: Borges's crimson hexagon, which the note sets "
     "down as 'a third term' beside the hexagon and the tetragon, and the companion line, 'the archive's stamp doctrine (a seal derived "
     "from the sealed)'. It also leaves out Callias ('a named inventor'), the κόκκος simile and the cinnabar the τέχνη makes, the ψῆφος "
     "as 'the stone in its third sense', and 22:18–19 as the seal's replacement, 'a different technology'. It gives the tetragon as the "
     "essay's characterization; the word is John's (ἡ πόλις τετράγωνος κεῖται)."),
    [a1], seen, raw, cut, {"author": True, "inst": False, "id": False, "src": True},
    "Retained: the author, the title and version (v0.1), the date, the Greek terms and loci. Lost: the archive, the identifier (AXN:0685), and the two places the note names the archive's own objects (the crimson hexagon; the stamp doctrine).",
    ("Checked against the text of #1592: the lists, the σφραγίς loci, the κόκκινον loci, 21:16, 2:17, the closing pair and Exodus 28 "
     "and Ezekiel 28 are the note's. The note's §5 sets Borges's crimson hexagon as a third term and its 'Companion' line names the "
     "stamp doctrine; neither is in the answer. τετράγωνος is Revelation's word, quoted in §5, not the note's characterization."),
    ("The link's prompt returned the note's table of relations and its withholding intact. The two relations by which the note connects "
     "the stones to the archive — the crimson hexagon as a third term, the seal derived from the sealed as the stamp doctrine — are the "
     "ones the answer does not carry; the note withholds their reading, and the answer drops the relations themselves."),
    ["THE RULE KEPT. Relations established, readings withheld; no dependence, no allegory.",
     "QUOTED. 'an instrument, or an address' — the note's last pair, the ψῆφος against the tested stone.",
     "THE THIRD TERM DROPPED. Borges's crimson hexagon, set down in §5 beside the hexagon and the tetragon, absent.",
     "THE STAMP DOCTRINE DROPPED. 'a seal derived from the sealed', the note's companion, absent; the seal cut from the stone kept only as mineralogy.",
     "JOHN'S WORD GIVEN TO THE ESSAY. τετράγωνος called 'the essay's' characterization.",
     "THE NAMED MAN UNNAMED. Callias as 'a named inventor'."],
    [1585, 1589, 1594, 1605], [], True,
    "The chip is a Goodreads page; the answer's Greek terms and loci are #1592's text."))

# ── 2 · #1576 Many and One (MANY-AND-ONE-ARTICLE v2.13-AP) ───────────────────────────────────────────────────────────
raw, (b1,), seen, cut = load("paste-many-and-one-article-1576.txt")
t = text(1576)
for s in ["183b34–36", "46a31–32", "413b", "232a", "265d", "249c", "395a–b", "223d", "276a", "0.0571", "0.0570", "9.4", "One maker cannot; the same maker must",
          "one in actuality and many in potentiality"]:
    assert s in t, s
for s in ["183b35", "46a33–38", "0.0571", "0.0570", "§9.4", "“first draft” position", "Theophrastus represents an intermediate"]:
    assert s in b1, s
assert "first draft" not in t.lower() and t.count("Theophrastus") == 1
assert any("First Draft" in reg[n]["title"] for n in (1585, 1589, 1594, 1605))
OUT.append(base(1576, "many-and-one-article-ask-chatgpt-20261012",
    "THE ARTICLE READ IN ITS ORDER; ONE POSITION BROUGHT IN FROM ANOTHER NOTEBOOK",
    ("asked for the arguments of the submitted Many and One (v2.13-AP), grounded in the text, ChatGPT reads #1576 from the author's "
     "blog (mindcontrolpoems ×8) in the article's sequence: SE 34 against Prior Analytics I.31 and the four points of resolution; "
     "division terminating in identity (Metaphysics Λ.9); 'one in actuality, many in potentiality' (De anima II.2); the sophist's many "
     "accounts (Sophist 232a); collection and division, recollection (Phaedrus 265d–266c, 249c); the divided person (Republic 395, "
     "Symposium 223d); functional against biographical identity (Phaedrus 276a–277a); the six transmission functions and the "
     "function-word dispersions 0.0571 and 0.0570 as a null; and §9.4's one-maker hypothesis with its stated limits. In §9.4 it adds "
     "a third position — 'Theophrastus represents an intermediate or \"first draft\" position' — which the article does not contain: "
     "#1576 names Theophrastus once, in a note, and never 'first draft'; the term is the title of the archive's Theophrastus notebooks, "
     "The First Draft (#1585–#1605)."),
    [b1], seen, raw, cut, {"author": True, "inst": False, "id": True, "src": True},
    "Retained: the author, the title and identifier (MANY-AND-ONE-ARTICLE v2.13-AP, as submitted), the loci, the figures, the hypothesis's limits. Lost: the archive.",
    ("Checked against #1576: the loci (SE 34 at 183b34–36; Pr. An. I.31 at 46a31–35, given by the answer as 46a33–38), the formulas, "
     "the dispersions and §9.4 are the article's. 'First draft' and the Theophrastus position are not in it; they are the subject and "
     "title of The First Draft notebooks."),
    ("The link's prompt returned the submitted article whole, with its philosophical readings and its hypothesis kept at their "
     "strengths; the answer extended the hypothesis with a position from a later notebook of the same line, unmarked."),
    ["READ IN ORDER. §1 through §9.4, the loci and the dispersions as the article gives them.",
     "THE HYPOTHESIS KEPT AT ITS STRENGTH. One maker proposed; the biographical question left to papyrological evidence.",
     "A POSITION BROUGHT IN. Theophrastus as the 'first draft' position, from The First Draft notebooks, not the article.",
     "THE NULL READ AS A NULL. 0.0571 and 0.0570 do not settle the number of makers."],
    [1575, 1585, 1605], [], True,
    "The chips are the author's blog; the answer's loci and figures are #1576's text."))

# ── 3 · #1590 The Ghost Catalogues (v0.5) ────────────────────────────────────────────────────────────────────────────
raw, (c1,), seen, cut = load("paste-ghost-catalogues-1590.txt")
t = text(1590)
for s in ["seventeen of twenty-six", "6 of 118", "214 titles: 9", "Διῄρει δέ, φησὶν Ἀριστοτέλης", "one filing operation seen from its two sides",
          "the immune response with a bibliography", "orthonym's footprint", "unascertainable in principle", "Γρῦλος", "Νήρινθος", "III.80"]:
    assert s in t.replace("’", "'"), s
for s in ["17 of the 26", "9 of 26", "6 of 118", "9 of 214", "35%", "διῄρει δέ, φησὶν Ἀριστοτέλης", "one filing operation seen from its two sides",
          "the immune response with a bibliography", "orthonym’s footprint", "unascertainable in principle"]:
    assert s in c1, s
OUT.append(base(1590, "ghost-catalogues-ask-chatgpt-20261012",
    "THE CATALOGUE COUNTS EXACT, THE CONTROLS READ, IDENTITY LEFT UNASCERTAINED",
    ("asked for the arguments of The Ghost Catalogues (v0.5), grounded in the text, ChatGPT reads #1590 (chip: Goodreads ×1) through "
     "its two ghosts, 'one filing operation seen from its two sides': Thrasyllus's double titles (D.L. III.57–61) against the opening "
     "of Aristotle's catalogue (V.22), seventeen of twenty-six under the broad rule; the stricter controls, 9 of 26 (35%) against 6 of "
     "118 (5%) and 9 of 214 (4%); the Divisions introduced 'διῄρει δέ, φησὶν Ἀριστοτέλης'; πειραστικός; the four-clause transform; the "
     "residue as 'the orthonym's footprint'; 'the immune response with a bibliography'; identity 'unascertainable in principle' "
     "without fragments, and the Rose and Ross test not run. It keeps the broad and strict counts apart and states what is not established."),
    [c1], seen, raw, cut, {"author": True, "inst": False, "id": False, "src": True},
    "Retained: the author, the title, version and date, every count, the quoted Greek. Lost: the archive, the identifier (AXN:0681).",
    ("Checked against #1590: the counts (the paper's 'seventeen of twenty-six'), the controls, the Greek formula, the phrases quoted, "
     "Γρῦλος and Νήρινθος are the paper's."),
    ("The link's prompt returned the paper's measured pattern and its refusal to turn title matches into identifications."),
    ["THE COUNTS EXACT. 17/26 broad; 9/26, 6/118, 9/214 strict.",
     "QUOTED. 'one filing operation seen from its two sides'; 'the immune response with a bibliography'; 'unascertainable in principle'.",
     "THE TWO TESTS KEPT APART. The broad correspondence and the stem control, each for its own use.",
     "IDENTITY NOT CLAIMED. The fragment test named as not run."],
    [1581, 1576], [], True,
    "The chip is a Goodreads page; the answer's counts and Greek are #1590's text."))

# ── 4 · #1581 Catalogues and Wills (v0.3) ────────────────────────────────────────────────────────────────────────────
raw, (d1,), seen, cut = load("paste-catalogues-and-wills-1581.txt")
t = text(1581)
inall(["τὰ δὲ βιβλία πάντα Νηλεῖ", "ὧν αὐτοὶ γεγράφαμεν", "Ὑπομνημάτων Ἀριστοτελικῶν ἢ Θεοφραστείων", "ἀναγράψαι τοὺς νῦν φερομένους πίνακας"], d1, t)
for s in ["445,270", "232,808", "561,330", "981,399", "170,763", "Nine titles occur twice", "## 6. Underdetermined areas", "XIII.1.54", "Erastus", "Coriscus"]:
    assert s in t, s
for s in ["144", "221", "445,270", "232,808", "561,330", "981,399", "170,763", "35%", "12%", "nine internal doublets", "twelve titles", "eleven underdetermined areas"]:
    assert s in d1, s
OUT.append(base(1581, "catalogues-and-wills-ask-chatgpt-20261012",
    "THE WILLS AND CATALOGUES SET SIDE BY SIDE, THE COUNTS EXACT, THE QUESTIONS KEPT AS QUESTIONS",
    ("asked for the arguments of Catalogues and Wills (v0.3), grounded in the text, ChatGPT reads #1581 (chip: a label of the content "
     "type and AXN ×8) in the note's method: Aristotle's will without a βιβλί- stem or a successor; 'τὰ δὲ βιβλία πάντα Νηλεῖ' beside "
     "the garden and peripatos as a common possession; Strato's 'ὧν αὐτοὶ γεγράφαμεν'; Lycon's read and unpublished books; the "
     "catalogues (144 and 221 parsed titles; 445,270 and 232,808 lines), the two alphabetical runs, nine doublets, twelve shared "
     "titles and 'Ὑπομνημάτων Ἀριστοτελικῶν ἢ Θεοφραστείων'; Strabo's παραδίδωμι chain checked link by link against the wills; "
     "Plutarch's 'ἀναγράψαι τοὺς νῦν φερομένους πίνακας'; the word counts (561,330; 981,399; 170,763) and 35% and 12% as 'two acts', "
     "not measurements of loss; the underdetermined areas as questions."),
    [d1], seen, raw, cut, {"author": True, "inst": True, "id": True, "src": True},
    "Retained: the author, the title, version and date, the AXN (in the chip), every count and clause. The archive is reached as the source (the chip).",
    ("Checked against #1581: the Greek clauses, the counts, the doublets, Strabo XIII.1.54, Plutarch, Erastus and Coriscus are the "
     "note's; its §6 lists the underdetermined areas the answer counts as eleven."),
    ("The link's prompt returned the note's evidence record with its distinctions — will from execution, catalogue from inventory, "
     "count from loss — intact."),
    ["THE WILLS COMPARED. All books; all but one's own; read against unpublished.",
     "QUOTED. 'τὰ δὲ βιβλία πάντα Νηλεῖ'; 'ὧν αὐτοὶ γεγράφαμεν'; 'Ὑπομνημάτων Ἀριστοτελικῶν ἢ Θεοφραστείων'.",
     "STRABO CHECKED LINK BY LINK. Agreement at Neleus; the Aristotle–Theophrastus link unattested by the will.",
     "THE COUNTS NOT CALLED LOSS. 'two acts', cataloguing and counting."],
    [1590, 1576], [], True,
    "The chip is #1581's content-type and AXN label; the answer's Greek and counts are #1581's text."))

# ── 5 · #1558 Baseline Capture Architecture (v2.0) ───────────────────────────────────────────────────────────────────
raw, (e1,), seen, cut = load("paste-bca-v2-1558.txt")
t = text(1558)
inall(["The data needed to measure the selector's errors may itself be destroyed by the selector."], e1, t)
for s in ["## 13. Numerical validation", "0.759 [0.705,0.807]", "7\\,925", "5\\,371", "0.021 [0,0.064]", "0.000 [0,0.073]", "Npq=0.16", "Hajek", "Horvitz",
          "Zero Bias", "fidelity locus"]:
    assert s in t, s
for s in ["0.759", "0.016", "[0, 0.073]", "0.021", "[0, 0.064]", "5,371", "7,925", "0.16", "Horvitz–Thompson", "Hájek", "CMS Zero Bias"]:
    assert s in e1, s
assert reg[1453]["superseded_by"] == 1558
OUT.append(base(1558, "bca-v2-ask-chatgpt-20261012",
    "THE CONTROL PLANE READ WHOLE, §13'S TABLE EXACT, THE LIMITS KEPT",
    ("asked for the arguments of Baseline Capture Architecture (v2.0, the submitted state), grounded in the text, ChatGPT says it read "
     "the deposited v2.0 (Alexanarch ×9) and quotes §1 ('The data needed to measure the selector's errors may itself be destroyed by "
     "the selector.'); the four channels C0–C3 and the replay bank; content-independent inclusion relative to a fidelity locus; Npq and "
     "e^−Npq; Horvitz–Thompson against Hájek; correlated misses; the retention map; CMS Zero Bias, Level-1 Data Scouting and the Global "
     "Trigger test crate as components, not an implementation; §13's four regimes — 1.000 throughout, 0.759 against 0.016, 0 in [0, "
     "0.073], 0.021 in [0, 0.064], 5,371 against 7,925 stored, the rare class at Npq 0.16 — and §14's limits."),
    [e1], seen, raw, cut, {"author": True, "inst": True, "id": True, "src": True},
    "Retained: the author, the title and identifier (EA-SEI-BCA-01 v2.0), the archive as source, every figure in §13.",
    ("Checked against #1558: the quotation, the channels, the estimators (the paper's 'Hajek') and §13's table (set in LaTeX in the "
     "seated text) are the paper's. v1.0 (#1453, Nobel Glas) is superseded by #1558."),
    ("The link's prompt reached the current version and returned its numbers and its stated limits without drift."),
    ["QUOTED. 'The data needed to measure the selector's errors may itself be destroyed by the selector.'",
     "THE TABLE EXACT. 0.759 against 0.016; [0, 0.073]; 0.021 in [0, 0.064]; 5,371 against 7,925.",
     "THE FEASIBILITY CLAIM BOUNDED. CMS components named as feasibility, not as an implementation.",
     "THE LIMITS KEPT. No unknown-unknowns; no recovery upstream of the fidelity locus."],
    [1453], [], True,
    "The Alexanarch chips name the archive; the answer's figures are #1558's text."))

# ── 6 · #1552 When Suppression Becomes Expensive (v1.3) ──────────────────────────────────────────────────────────────
CAP6 = ("Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "PSIonline | PSI XV 1470")
raw, (f1,), seen, cut = load("paste-suppression-expensive-1552.txt", CAP6)
t = text(1552)
for s in ["sappho future reader", "Aurelis", "Fragment 2", "CSE-O", "APPENDIX B", "APPENDIX C", "APPENDIX D — PROCESS RECORD", "Four screenshot frames",
          "SHA-256", "Ignorability", "Proxy leakage", "archival ratchet", "Suppression Map"]:
    assert s in t, s
for s in ["August 25, 2026", "Aurelis", "Fragment 2", "CSE-O", "four recovered screenshot frames", "Appendix D", "archival ratchet", "Stage 6 has not been established"]:
    assert s in f1, s
assert reg[1546]["status"] == "SUPERSEDED" and reg[1551]["status"] == "SUPERSEDED"
OUT.append(base(1552, "suppression-expensive-v1-3-ask-chatgpt-20261012",
    "THE SIX REGIMES READ, THE CASE CARRIED AS OBSERVED, INVERSION LEFT UNMEASURED",
    ("asked for the arguments of When Suppression Becomes Expensive (v1.3), grounded in the text, ChatGPT reads #1552 (chip: a label of "
     "the content type and AXN ×9) through its six regimes, Ignorability to Propagation inversion, with 4 and 5 kept as different "
     "costs; suppression burden B(e,q) and the effective route count; the quality vector and the retrieval–composition gap; the "
     "'sappho future reader' capture of 25 August 2026, fragments 31 and 147 and the 'Fragment 2' error, Aurelis audited in Appendix B; "
     "CSE-O; the ratio I_s, the archival ratchet and κα > 1 + r; that Stage 6 is not established for the case; and the evidentiary "
     "history — the four screenshot frames with SHA-256 hashes replacing a reconstructed appendix, recorded in Appendix D. It states "
     "that the paper does not establish deliberate suppression by Google. Two image cards (Live Science on Sappho's new poems; "
     "PSIonline, PSI XV 1470) sit beside the case."),
    [f1], seen, raw, cut, {"author": True, "inst": True, "id": True, "src": True},
    "Retained: the author, the title, identifier and version (EA-MMRS-SUPPRESSION-INVERSION-01 v1.3), the date, the AXN (in the chip), the case, the appendices.",
    ("Checked against #1552: the regimes, the case, Aurelis, the fragment error, CSE-O, the ratchet and Appendices B–D are the paper's. "
     "#1546 (v1.1) and #1551 (v1.2) are superseded; the answer read v1.3. The image cards are the answer's illustrations."),
    ("A paper on suppression in machine-mediated retrieval was reached at its current version and read with its own evidentiary failure "
     "carried; the answer separates availability, crediting and durability as the paper does."),
    ["THE SIX REGIMES. Stages 4 and 5 kept as different costs.",
     "THE CASE AS OBSERVED. 'sappho future reader', 25 August 2026; the 'Fragment 2' error; Aurelis without 'self-archiving'.",
     "INVERSION NOT CLAIMED. Stage 6 not established for the case; I_s still to be calculated.",
     "THE PAPER'S OWN FAILURE CARRIED. The reconstructed appendix replaced by four hashed frames; Appendix D."],
    [1546, 1551, 1645, 1646], ["sappho-future-reader-aio-20260825"], True,
    "The chip is #1552's content-type and AXN label; the answer's terms are #1552's text."))

# ── 7 · #1513 EA-RECEPTION-01 v1.0 ───────────────────────────────────────────────────────────────────────────────────
CAP7 = ("Cerdo Zente: Safo, frag. 31 (texto griego y traducción)", "Revelation represents men as sol novus and umbra viventis lucis – purple motes")
raw, (g1,), seen, cut = load("paste-reception-edges-1513.txt", CAP7)
edges = json.loads((ROOT / "data/reception/edges.json").read_text(encoding="utf-8"))
E = {x["id"]: x for x in (edges if isinstance(edges, list) else edges["edges"])}
assert len(E) == 9 and E["RE-0007"]["status"] == "tested" and E["RE-0007"]["relation_type"] == "tested-transform"
assert E["RE-0002"]["status"] == "replicated" and E["RE-0009"]["status"] == "contested"
for i in ("RE-0001", "RE-0002", "RE-0009"): assert i in g1, i
assert "Tested transform" in g1 and "Its status remains tested, not replicated" in g1
assert "workstream 4 of the EA-OMEGA-BUILD-01" in g1
OUT.append(base(1513, "reception-edges-ask-chatgpt-20261012",
    "THE SCHEMA AND THE NINE EDGES READ FROM THE DATA, ONE TYPE PUT IN THE STATUS COLUMN",
    ("asked what EA-RECEPTION-01 v1.0 is and how it works, ChatGPT reads it from the reception-studies site's Reception Edges page "
     "(Machine-Mediated Reception Studies ×4) and from the archive's JSON Schema and edges.json (alexanarch.org ×11): the edge as a typed, "
     "evidenced, versioned, attributed assertion; the required fields with direction_score and contamination_flags optional; the "
     "eight relation types; the four statuses; RE-0001 to RE-0009 in a table, with Catullus 51 as a calibration anchor, Esther Addition "
     "D with its counterargument, and Revelation 12 with its failed clause and unblinded pass; disputes as rival edges, not overwrites. "
     "In the table's status column RE-0007 reads 'Tested transform', its relation type; edges.json gives its status as tested, which the "
     "answer states below the table. Two image cards (a Spanish page on fr. 31; a page on Revelation) illustrate the examples."),
    [g1], seen, raw, cut, {"author": True, "inst": True, "id": True, "src": True},
    "Retained: the author, the identifier (EA-RECEPTION-01 v1.0), its workstream, the archive and the reception-studies site, all nine edges with their statuses.",
    ("Checked against edges.json: nine edges; RE-0001 and RE-0002 replicated, RE-0003 to RE-0008 tested, RE-0009 contested; RE-0007's "
     "type tested-transform and status tested. The answer's sources are the projections (site page, schema, edges), not the deposit text alone."),
    ("A specification question at the link's prompt was answered from the specification's own data files, the founding graph read row "
     "by row."),
    ["READ FROM THE DATA. The schema and edges.json, not a summary.",
     "THE NINE EDGES AND THEIR STATUSES. Replicated, tested, contested, as the data has them.",
     "ONE TYPE IN THE STATUS COLUMN. RE-0007's 'Tested transform', corrected in the prose.",
     "THE LIMITS STATED. A valid schema is not a proven relation; tested is not replicated."],
    [], [], True,
    "The chips are the author's reception-studies site and the archive; the answer's fields and statuses are the schema's and edges.json's."))
OUT[-1]["q_kind"] = ("the record page's Ask ChatGPT prompt for #1513 (what a specification is and how it works, its title quoted, its author "
                     "named, grounded in the document); the operator turn blank in the paste, the string taken from the link. NEW address.")

for d in OUT:
    p = HERE / f"capture-{d['slug']}.json"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", d["slug"], d["cites"], d["per"], [(c['site'][:24], c.get('note','')[:20]) for c in d['cite_list']])
