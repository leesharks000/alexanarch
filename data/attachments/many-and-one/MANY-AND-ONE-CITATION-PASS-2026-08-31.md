---
id: MANY-AND-ONE-CITATION-PASS-2026-08-31
title: "The Citation Pass — register of checks"
status: RUN 2026-08-31, Greek-loci and bibliographic phases complete. The print-edition check remains open.
substrate: AI-assisted (Claude, Anthropic); all checks against fetched records named per entry
---

# THE CITATION PASS — REGISTER

**What this is.** Every Greek quotation and locus in MANY-AND-ONE-COMPLETE v2.3,
and every modern bibliographic entry, checked against fetchable canonical records.
Produces v2.4. Emendations were applied in the paper and are restated here with
their evidence; variances are registered and not emended; what could not be
reached is named as unreached.

**What this is not.** Not the print-edition check. The OCT/Teubner apparatus,
Kühn's pages, Voigt's apparatus and sigla, Wehrli's numbering remain unverified
against paper. Every entry below names the electronic edition it was checked
against; where that edition's lineation is coarser than the claim, the entry says
so.

## METHOD

**Sources.**
- Plato: PerseusDL canonical-greekLit TEI, `tlg0059.tlgNNN.perseus-grc2`
  (Apology 002, Phaedo 004, Theaetetus 006, Sophist 007, Statesman 008,
  Symposium 011, Phaedrus 012, Republic 030, Timaeus 031, Laws 034,
  Epistles 036). Stephanus section milestones: **exact-section precision.**
- Aristotle, Perseus: Metaphysics `tlg0086.tlg025.perseus-grc2`, Poetics tlg034 —
  Bekker page + line milestones: **page + ~5-line precision.**
- Aristotle, First1KGreek (OpenGreekAndLatin), `1st1K-grc1`: APr tlg001,
  De anima tlg002, Categories tlg006, GC tlg013, De interpretatione tlg017,
  De memoria tlg024, SE tlg040. Book/chapter divs only: **chapter precision**,
  with Bekker columns given as position-fraction ESTIMATES (±1 column) where
  needed.
- [Longinus]: `tlg0560.tlg001.perseus-grc2` (Περὶ ὕψους), chapter/section
  milestones.
- Bibliography: api.crossref.org (query.bibliographic), api.openalex.org,
  archive.org advancedsearch. Record identifiers per entry.

**Matching.** Accent-insensitive, breathing-insensitive, Greek-letters-only
normalization on both sides; multi-fragment quotes required within a ~3,500-char
window; misses diagnosed by halves. The verification engine and its full output
were produced in-session (citepass.py; passout capture); this register is their
compression and, per the evidentiary-basis rule, the surviving record — the
session-local raw output is not separately preserved, and that absence is stated
here.

## PHASE ONE — GREEK LOCI

### Sophistici Elenchi (1st1K tlg040; last chapter = div 33 of 33)

- G1 Σωκράτης ἠρώτα, ἀλλ᾽ οὐκ ἀπεκρίνετο· ὡμολόγει γὰρ οὐκ εἰδέναι — claimed
  183b7–8 → found last chapter §12. **VERIFIED** (chapter identity carries the
  Bekker page; line numbers are the carried claim, print check).
- G2 οὐ τὸ μὲν ἦν τὸ δ᾽ οὐκ ἦν προεξειργασμένον, ἀλλ᾽ οὐδὲν παντελῶς ὑπῆρχεν —
  claimed SE 34 183b → last chapter §15. **VERIFIED.** Text reads **Ταύτης δὲ
  τῆς πραγματείας** — the paper's inline "ταύτης τῆς πραγματείας" drops the
  interposed δὲ. **REGISTERED**, load-bearing for the Hitchcock question at
  [X.7]; the quotation in running prose, not emended.
- G3 περὶ δὲ τοῦ συλλογίζεσθαι παντελῶς οὐδὲν εἴχομεν πρότερον ἄλλο λέγειν —
  last chapter §18. **VERIFIED.**
- G4 shoemaker clause οὐ γὰρ τέχνην ἀλλὰ τὰ ἀπὸ τῆς τέχνης… — §17. **VERIFIED.**
- G5 βεβοήθηκε μὲν πρὸς τὴν χρείαν, τέχνην δ᾽ οὐ παρέδωκεν — §17. **VERIFIED.**
- G6 πολλὰ καὶ παλαιὰ τὰ λεγόμενα — §18. **VERIFIED.**
- G7 οἷον ἐκ διαδοχῆς, the Tisias succession — §15. **VERIFIED.**
- G8 τοῖς μὲν παραλελειμμένοις τῆς μεθόδου συγγνώμην… πολλὴν ἔχειν — §18
  (claimed 184b). **VERIFIED.**
- G9 παρὰ τὰς ἄλλας πραγματείας τὰς ἐκ παραδόσεως ηὐξημένας — §18. **VERIFIED.**
- G10 ὅπως λόγον ὑπέχοντες φυλάξομεν τὴν θέσιν — §11, adjacent to G1 as the
  paper claims ("the sentence before"). **VERIFIED.**
- G11 μέγιστον γὰρ ἴσως ἀρχὴ παντός, ὥσπερ λέγεται — §14. **VERIFIED**, in the
  priority paragraph as claimed.
- G12 ἐξ ὑπαρχῆς — **present, one hit, last chapter §13.** The Order-section
  claim that the phrase stands in the same stretch is **VERIFIED.**
- G13 διὰ τῶν ὀνομάτων — ch. 1 §4 (claimed 165a). **VERIFIED.**
- G14 φαινομένων μὲν ἐλέγχων ὄντων δὲ παραλογισμῶν — ch. 1 §1 (claimed
  164a–165a). **VERIFIED.**

### Prior Analytics I.31 (1st1K tlg001)

- G15 μικρόν τι μόριόν ἐστι τῆς εἰρημένης μεθόδου — I.31. **VERIFIED** (claimed
  46a31; chapter precision).
- G16 οἷον ἀσθενὴς συλλογισμός — I.31. **VERIFIED.**
- G17 ὥστ᾽ οὔτε ὅ τι ἐνδέχεται συλλογίσασθαι διαιρούμενοι ξυνίεσαν — I.31.
  **VERIFIED against this edition's nominative διαιρούμενοι**, the form the
  paper prints. The dative διαιρουμένοις does not occur in the 1st1K text;
  whether an OCT prints it is a print-check item.
- G18 the letters run: ἢ θνητὸν μὲν ἢ ἀθάνατον ἀναγκαῖον… οὐκ ἀναγκαῖον, ἀλλ᾽
  αἰτεῖται· τοῦτο δ᾽ ἦν ὃ ἔδει συλλογίσασθαι — I.31. **VERIFIED.**
- G19 ῥᾴδιον ἰδεῖν — I.31. **VERIFIED.**
- G20 **ὑπάρχω recount.** 1st1K APr normalized text: υπαρχ 1,199 + υπηρχ 21 +
  υπαρξ 119 = 1,339 stem-family hits; raw υπαρχ alone 1,199 against the carried
  **1,182** — within 1.5%. **CORROBORATED**; exact figure is edition- and
  tokenization-dependent (the 1st1K body may carry apparatus Greek), and the
  carried number is the seated corpus's. Not emended.

### Metaphysics Λ 9 (perseus-grc2; Bekker page+line milestones)

- G21 αὑτὸν ἢ ἕτερόν τι — 1074b l.20. **VERIFIED.**
- G22 αὑτὸν ἄρα νοεῖ… ἡ νόησις νοήσεως νόησις — 1074b l.30–35 (claimed
  1074b33–35). **VERIFIED-EXACT.**
- G23 ἄλλο τι ἂν εἴη τὸ τιμιώτερον… τὸ νοούμενον — 1074b l.30. **VERIFIED.**
- G24 οὐχ ἑτέρου οὖν ὄντος τοῦ νοουμένου καὶ τοῦ νοῦ, ὅσα μὴ ὕλην ἔχει, τὸ αὐτὸ
  ἔσται, καὶ ἡ νόησις τῷ νοουμένῳ μία — **found at page 1075a line 1.** The
  paper's central locus, 1075a1, **VERIFIED-EXACT.**
- G25 εἰ ἄλλο τὸ νοεῖν καὶ τὸ νοεῖσθαι, κατὰ πότερον… — 1074b l.35. **VERIFIED.**
- G26 λείπεται ἀπορία, εἰ σύνθετον τὸ νοούμενον — 1075a l.5. **VERIFIED.**
- G27 ἀδιαίρετον πᾶν τὸ μὴ ἔχον ὕλην — 1075a l.5 (claimed a6–7). **VERIFIED.**

### De anima (1st1K tlg002; chapter precision)

- G28 Πότερον δὲ τούτων ἕκαστόν… χωριστὸν λόγῳ μόνον ἢ καὶ τόπῳ — II.2.
  **VERIFIED** (claimed 413b13–16).
- G29 divided plants; cut insects with sensation and locomotion — II.2.
  **VERIFIED.**
- G30 ἐντελεχείᾳ μὲν μιᾶς ἐν ἑκάστῳ φυτῷ, δυνάμει δὲ πλειόνων — II.2.
  **VERIFIED.**
- G31 Περὶ δὲ τοῦ νοῦ… καθάπερ τὸ ἀΐδιον τοῦ φθαρτοῦ — II.2. **VERIFIED**
  (claimed 413b24–27; the paper's "end of the chapter" is loose — the clause
  sits ~two-thirds through II.2 — registered, not emended).
- G32 τὸ δεκτικὸν τῶν αἰσθητῶν εἰδῶν ἄνευ τῆς ὕλης — II.12. **VERIFIED.**
- G33 the signet clause — text reads **ἄνευ τοῦ σιδήρου καὶ τοῦ χρυσοῦ**; the
  paper carried ἄνευ τοῦ σιδήρου ἢ χρυσοῦ. **DIVERGENT → EMENDED** in v2.4
  (Machine §5/T2).
- G34 III.5 cluster: τῷ πάντα γίνεσθαι / τῷ πάντα ποιεῖν; χωρισθεὶς δ᾽ ἐστὶ
  μόνον τοῦθ᾽ ὅπερ ἐστί; ὁ δὲ παθητικὸς νοῦς φθαρτός; ἄνευ τούτου οὐθὲν νοεῖ —
  III.5. **VERIFIED.**

### De memoria (1st1K tlg024; two chapters; Bekker by position ESTIMATE ±1 col.)

- G35 opening of the recollection chapter — text reads **Οὔτε γὰρ μνήμης ἐστὶν
  ἀνάληψις ἡ ἀνάμνησις οὔτε λῆψις** (ch. 2 opening; ESTIMATE ~451a, matching
  the carried 451a). **VERIFIED**; the paper's quotation drops the connective
  γὰρ — **REGISTERED**, standard practice for an incipit quotation, not
  emended.
- G36 λαβέσθαι ἀρχῆς — ch. 2, ESTIMATE ~451b. **VERIFIED.**
- G37 ἀφ᾽ ὁμοίου ἢ ἐναντίου ἢ τοῦ σύνεγγυς — ch. 2, ESTIMATE ~451b. **VERIFIED**;
  the paper attaches no Bekker line to it in §IV — correct as printed.
- G38 οἷον συλλογισμός τις — ch. 2, ESTIMATE **~453a**, matching the carried
  453a. **VERIFIED.**
- G39 Πολλάκις δ᾽ ἤδη μὲν ἀδυνατεῖ ἀναμνησθῆναι, ζητεῖν δὲ δύναται καὶ εὑρίσκει
  — ch. 2, ESTIMATE ~451b–452a. The carried **452a** (Order §3) is **within
  tolerance; UNRESOLVED at line precision** from this source. Print check.
- G40 κινοῦντι πολλά… ᾗ ἀκολουθήσει τὸ πρᾶγμα — ch. 2, ~451b–452a. **VERIFIED.**
- G41 Τὸ γὰρ μεμνῆσθαί ἐστι τὸ ἐνεῖναι δυνάμει τὴν κινοῦσαν — ch. 2, same
  stretch ("the same page", as the paper says). **VERIFIED.**

### GC, De interpretatione, Categories

- G42 ἐκ τῶν αὐτῶν γὰρ τραγῳδία καὶ κωμῳδία… γραμμάτων — GC I.2 (claimed 315b).
  **VERIFIED.**
- G43 τὰ ἐν τῇ φωνῇ… σύμβολα, καὶ τὰ γραφόμενα τῶν ἐν τῇ φωνῇ — De int. ch. 1
  (claimed 16a3–4). **VERIFIED.**
- G44 Ὁμώνυμα λέγεται ὧν ὄνομα μόνον κοινόν, ὁ δὲ κατὰ τοὔνομα λόγος τῆς οὐσίας
  ἕτερος — Categories, opening (claimed 1a1). **VERIFIED-EXACT** (it is the
  first sentence).

### Plato (perseus-grc2; exact Stephanus sections)

- G45 Sophist six-definition recap — θηρευτής 231d; ἔμπορος 231d; κάπηλος 231d
  (text order **περὶ αὐτὰ ταῦτα κάπηλος**; the paper's table label rearranges —
  **REGISTERED** as label form); αὐτοπώλης 231d; ἀθλητής/ἐριστική 231e; δοξῶν
  ἐμποδίων… 231e; ἀμφισβητήσιμον μέν, ὅμως δ᾽ ἔθεμεν 231e. Recap **VERIFIED at
  231d–e**; the paper's head emended from bare 231d in v2.4.
- G46 Soph. 232a diagnosis, entire (ὅταν ἐπιστήμων τις πολλῶν φαίνηται … πολλοῖς
  ὀνόμασιν ἀνθ᾽ ἑνὸς) — **VERIFIED-EXACT at 232a.**
- G47 Statesman 257d–258a entire: συγγένειαν 257d; πρόσωπον/κλῆσις ὁμώνυμος
  257d–258a; διὰ λόγων ἀναγνωρίζειν 258a; σοὶ δὲ νῦν ἀποκρινέσθω 258a; ὦ
  Σώκρατες, ἀκούεις δὴ Σωκράτους 258a; οὐδέτερα 258a. **ALL VERIFIED-EXACT.**
- G48 Statesman 260d ἀλλότρια νοήματα — **VERIFIED-EXACT.**
- G49 Theaetetus: κήρινον ἐκμαγεῖον at **191c** (the wax opens where the paper
  says); **ὃ ἔφαμεν ἀδύνατον at 196b, not 191c** — the impossibility verdict
  belongs to the twelve/eleven passage. **DIVERGENT → EMENDED** in v2.4: the
  seal-and-wax table and Machine T2 now read "abandoned at 196b," and the
  Machine's T2 range reads 191c–196b.
- G50 Phaedrus set: 249b–c (ἐκ πολλῶν ἰὸν αἰσθήσεων… τοῦτο δ᾽ ἐστὶν ἀνάμνησις);
  249c (ὑπομνήμασιν ὀρθῶς χρώμενος… τέλεος ὄντως μόνος); 265e (κατ᾽ ἄρθρα ᾗ
  πέφυκεν; κακοῦ μαγείρου); 266d (τά γ᾽ ἐν τοῖς βιβλίοις…); 275d–e (ὅταν δὲ
  ἅπαξ γραφῇ, κυλινδεῖται…); 276a (ὃς μετ᾽ ἐπιστήμης γράφεται… εἴδωλον); 276e–
  277a (φυτεύῃ τε καὶ σπείρῃ… ἔχοντες σπέρμα). **ALL VERIFIED-EXACT.**
- G51 Symposium set: 210b (πολλὴ ἄνοια…); 210c–d (βλέπων πρὸς πολὺ… ὥσπερ
  οἰκέτης); 223d (τοῦ αὐτοῦ ἀνδρὸς… ποιεῖν; καταδαρθεῖν τὸν Ἀριστοφάνη; οὐκ
  ἔφη μεμνῆσθαι τῶν λόγων); 209d (τίμιος δὲ παρ᾽ ὑμῖν καὶ Σόλων διὰ τὴν τῶν
  νόμων γέννησιν — the paper's "τίμιος διὰ…" is a compression of the full
  clause, locus exact); 209e (ἱερὰ πολλὰ… διὰ δὲ τοὺς ἀνθρωπίνους); 209c–d
  (καλλιόνων καὶ ἀθανατωτέρων; ἔκγονα). **ALL VERIFIED-EXACT.**
- G52 Republic: 395a (δύο μιμήματα; κωμῳδίαν καὶ τραγῳδίαν ποιοῦντες); 395b
  (κατακεκερματίσθαι ἡ τοῦ ἀνθρώπου φύσις). **VERIFIED-EXACT.** 507a — the text
  reads **κίβδηλον ἀποδιδοὺς τὸν λόγον τοῦ τόκου** (and κιβδήλου at 366b);
  the carried "κίβδηλος λόγος" as a quotation was **DIVERGENT → EMENDED** in
  v2.4 to the actual form.
- G53 Laws 742a ἔντιμον / ἀδόκιμον — **VERIFIED-EXACT.**
- G54 Epistle II 314c οὐδ᾽ ἔστιν σύγγραμμα Πλάτωνος… καλοῦ καὶ νέου γεγονότος —
  **VERIFIED-EXACT.**
- G55 Phaedo 59b Πλάτων δὲ οἶμαι ἠσθένει — **VERIFIED-EXACT.**
- G56 Timaeus 29b (μέγιστον δὴ παντὸς ἄρξασθαι κατὰ φύσιν ἀρχήν); 29c (πρὸς
  γένεσιν οὐσία…; ἀπεικασθέντος… εἰκόνος); 29c–d (φύσιν ἀνθρωπίνην ἔχομεν; τὸν
  εἰκότα μῦθον… μηδὲν ἔτι πέρα ζητεῖν). **ALL VERIFIED-EXACT.**

### [Longinus], Περὶ ὕψους 10 (perseus-grc2) — the Sappho edge

- G57 The transmitted seam, De subl. 10.2: "…τεθνάκην δ᾽ ὀλίγω ᾽πιδεύην
  φαίνομαι. ἀλλὰ πᾶν τολματόν, ἐπεὶ καὶ πένητα — οὐ θαυμάζεις ὡς…" **The
  quotation as transmitted runs past the stanza-break to ἐπεὶ καὶ πένητα, and
  Longinus's very next words are οὐ θαυμάζεις.** This verifies Round 44's
  extension reading, verifies the archive chain's second member as the
  transmitter's own next words, and contradicted [T1]'s original first sentence
  ("ἀλλὰ πᾶν τόλματον is where the quotation ends") — **DIVERGENT → EMENDED**:
  [T1] now reads that the stanza breaks at the τόλματον clause and the
  quotation runs one clause further. **Edition forms REGISTERED:** Perseus-
  Longinus prints πᾶν τολματόν; Voigt's convention is πὰν τόλματον; the paper,
  which names Voigt/Lobel–Page as its editions, was standardized to the Voigt
  form in both occurrences (it had mixed πᾶν and πὰν). Voigt's obeli on καὶ
  πένητα are a print-check item; the Perseus text carries the words undaggered.

## PHASE TWO — BIBLIOGRAPHY

Verified in author, title and year against the named record:

- Love, *Attributing Authorship* (2002) — Crossref doi:10.1017/cbo9780511483165. **VERIFIED.**
- Foucault, "What Is an Author?" — essay 1969; English in *Language,
  Counter-Memory, Practice*, ed. Bouchard, trans. Bouchard–Simon (Cornell,
  1977) — Crossref (1978 MLN review; 2019 reissue doi). **VERIFIED.**
- Barthes, "The Death of the Author" (1967) — aggregator records only; 1967
  (Aspen) is the standard first publication, French 1968. **VERIFIED-AS-STANDARD.**
- *Cambridge Handbook of Literary Authorship*, eds. Berensmeyer, Buelens,
  Demoor — Crossref doi:10.1017/9781316717516 gives **2019**; the paper carried
  2021. **DIVERGENT → EMENDED.**
- Dorion, *Aristote: Les réfutations sophistiques* (1995) — two 1998 reviews
  (Philosophiques; Phoenix). **VERIFIED.**
- Dorion, "The Rise and Fall of the Socratic Problem," *Cambridge Companion to
  Socrates* — doi:10.1017/ccol9780521833424.001, record year 2010; carried 2011
  (standard imprint). **VARIANCE REGISTERED.**
- Hasper — active specialist on *SE* confirmed (CQ 58, 2008,
  doi:10.1017/s0009838808000062); the specific completeness-claim piece **not
  resolved via API**; apparatus already carries it as named-not-read. **CARRIED.**
- Hitchcock (via Corcoran) — no full cite in the apparatus; **not resolved via
  API. CARRIED**, print check.
- Mueller — *Alexander of Aphrodisias on Aristotle Prior Analytics 1.23–31*
  exists as titled (Bloomsbury Ancient Commentators,
  doi:10.5040/9781472551627). **VERIFIED-TITLE**; translator credit and year to
  print check.
- Ebbesen, *Commentators and Commentaries on Aristotle's Sophistici Elenchi*
  (1981) — Brill doi:10.1163/9789004543058. **VERIFIED.**
- Vlasits, *Platonic Division and the Origins of Aristotelian Logic* (Berkeley
  diss., 2017) — the dissertation itself not resolved via API; the author
  verified (Crossref 2021 chapter). **CARRIED-AUTHOR-VERIFIED.**
- Nightingale, *Genres in Dialogue* (1995) — doi:10.1017/cbo9780511582677. **VERIFIED.**
- Ong, *Orality and Literacy* (1982) — doi:10.4324/9780203328064. **VERIFIED.**
- Burnet, *Plato's Phaedo* (1911) — Internet Archive, four 1911 records (e.g.
  platosphaedo00platuoft). **VERIFIED.**
- Taylor, *Socrates* (carried 1932) — IA's earliest record 1933
  (bwb_P9-CZA-416), later 1951/1953/1954 editions. Title verified (the v2.4
  retitle stands); **year VARIANCE REGISTERED**, print check between 1932/1933.
- Vlastos, *Socrates: Ironist and Moral Philosopher* (1991) —
  doi:10.1017/cbo9780511518508 + 1992 CW review. **VERIFIED.** "The Historical
  Socrates and Athenian Democracy," *Political Theory* 11 (1983) — carried;
  consistent with the record set; **CARRIED, print check for pages.**
- Kahn, *Plato and the Socratic Dialogue* (1996) — doi:10.1017/cbo9780511585579
  (record year 1997, online edition); carried 1996 is the imprint. **VERIFIED,
  VARIANCE REGISTERED.**
- Cooper (ed.), *Plato: Complete Works* (1997) — 1998 CR review of
  Cooper–Hutchinson. **VERIFIED.**
- Moore, "Chaerephon the Socratic," *Phoenix* 67 (2013) — Christopher Moore,
  doi:10.7834/phoenix.67.3-4.0284. **VERIFIED-EXACT.**
- Danzig, *Apologizing for Socrates: How Plato and Xenophon Created Our
  Socrates* (2010) — doi:10.5771/9780739132463 (record 2012, e-edition);
  carried 2010 is the Lexington imprint. **VERIFIED, VARIANCE REGISTERED.**
- Nehamas, *The Art of Living* (1998) — carried; standard. **CARRIED.**
- Lefkowitz, *The Lives of the Greek Poets* (2nd ed. 2012) — JHUP
  doi:10.56021/9781421404639; 1st ed. attested by 1983 Phoenix review. **VERIFIED.**
- Fairweather, "Fiction in the Biographies of Ancient Writers," *Ancient
  Society* 5 (1974) — **not resolved via API** (Crossref backfile gap; OpenAlex
  rate-limited); widely cited standard article. **CARRIED**, print check.
- Denyer, *Plato: Alcibiades* — CUP doi:10.1017/cbo9781139167079 (2001);
  *Plato: Protagoras* — 2009 Elenchos review of the CUP edition (2008).
  **VERIFIED** (the paper carries no years for these; none needed).
- Boys-Stones and Rowe, *The Circle of Socrates* (2013) — 2014/2015 reviews
  (Teaching Philosophy; Ancient Philosophy). **VERIFIED.**
- Nagy, *Homeric Questions* (1996) — doi:10.7560/755611. **VERIFIED.**
- Hadot, *Philosophy as a Way of Life* (trans. Chase, 1995) — record set
  consistent. **VERIFIED-AS-STANDARD.**
- Speyer, *Die literarische Fälschung im heidnischen und christlichen Altertum*
  (1971) — 1973/1974 reviews (BZ; CR). **VERIFIED.**
- Casson, *Libraries in the Ancient World* (2001) — Yale
  doi:10.12987/9780300133134 (e-edition 2017); carried 2001 imprint. **VERIFIED.**
- Canfora, *The Vanished Library* (trans., carried 1989) — 1992 CW review.
  **VERIFIED.**
- MacLeod (ed.), *The Library of Alexandria* (2004) — I.B. Tauris
  doi:10.5040/9780755625949, incl. Barnes chapter. **VERIFIED.**
- Delia, "From Romance to Rhetoric," *AHR* 97 (1992) — doi:10.2307/2165947. **VERIFIED.**
- Blum, *Kallimachos* (1977; trans. Wellisch, Madison 1991) — Wisconsin record
  + 1993 Library Quarterly review. **VERIFIED.**
- Kenyon — *Athenaion Politeia* editio princeps, London 1891 — Internet
  Archive, multiple 1891 records (athenainpolite00arisuoft; Kenyon ed.).
  **VERIFIED**; grounds the [F.13] emendation.
- Reynolds and Wilson, *Scribes and Scholars* — 3rd ed. 1991 in Crossref
  (doi:10.1093/oso/9780198721451.001.0001); carried 4th ed. 2013 standard, not
  in record. **VERIFIED-EDITION-LINE**, 4th-ed. year to print check.
- Johnson, *Readers and Reading Culture in the High Roman Empire* (2010) —
  doi:10.1093/acprof:oso/9780195176407.001.0001. **VERIFIED.**
- Johnson and Parker (eds.), *Ancient Literacies* (2009) — OUP record 2011
  (paperback/online); carried 2009 hardback imprint. **VERIFIED, VARIANCE
  REGISTERED.**
- Print-only apparatus — Wehrli (*Die Schule des Aristoteles*, Aristoxenus fr.
  1), Voigt (*Sappho et Alcaeus*, 1971), Lobel–Page (*PLF*, 1955), Campbell
  (Loeb *Greek Lyric*), Blass, Worthington, Kühn (Galen XVII.A.606–607),
  al-Fārābī's abridgement, Havelock, CPF — **not checkable via these APIs;
  CARRIED**, exactly as the apparatus already flags. [F.18]'s own caution
  stands verbatim.

## EMENDATIONS APPLIED IN v2.4 (restated with evidence)

1. *De an.* 424a: ἢ χρυσοῦ → **καὶ τοῦ χρυσοῦ** (G33).
2. ὃ ἔφαμεν ἀδύνατον reseated at **196b**; wax remains 191c; Machine T2 range
   191c–196b (G49).
3. *Sophist* recap locus **231d–e** (G45).
4. [T1] quotation-edge sentence brought into agreement with the transmitted
   text and its own correction paragraph (G57).
5. Sappho's line standardized to the **Voigt form πὰν τόλματον** in both
   occurrences (G57).
6. *Rep.* 507a quoted in its actual form, **κίβδηλον ἀποδιδοὺς τὸν λόγον**
   (G52).
7. Taylor retitled ***Socrates*** (phase two; year variance registered).
8. [F.13] given its **editio princeps (Kenyon, 1891)** and acquisition dates
   (phase two, IA records).
9. *Cambridge Handbook of Literary Authorship*: 2021 → **2019** (phase two,
   Crossref).

## STANDING

- **The print-edition check is open**: OCT/Teubner apparatus and lineation,
  Kühn's pages, Voigt's apparatus and obeli, Wehrli's numbering, Fairweather,
  the Hitchcock item, Taylor's imprint year, Bekker lines for every 1st1K-
  checked work, De mem. 451b/452a for the ἀδυνατεῖ clause.
- Divergences between electronic-record years and standard imprint years are
  registered above and were not emended.
- Everything the apparatus marks "named and not consulted" remains so marked;
  nothing was upgraded by this pass.

∮ = 1
