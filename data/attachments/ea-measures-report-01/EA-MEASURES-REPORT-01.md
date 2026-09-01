---
id: EA-MEASURES-REPORT-01
title: "Inheritance Is Observable, Embodiment Is Not: A Functional Comparison of the Platonic and Aristotelian Corpora, and the Insufficiency of Lexical Measurement for Maker-Count"
designator: EA-MEASURES-REPORT-01
version: v1.0, 2026-08-31
author: Sharks, Lee
orcid: 0009-0000-1599-0703
status: TECHNICAL REPORT — deposited as the evidentiary companion to an article under review; the article cites this report and does not reproduce its figures
sources: EA-NOTEBOOK-01 (Rounds 12–13, 19, 21–25, 27–30, 33–39, 43, 48); EA-AUTHORSHIP-MEASURES-01 (M6, M10, M11, M13, M14, M16, M28, M30, M33, M34, M36, M38, M39, M43–M45, M48–M50); EA-YIELD-02 (registered 7bcbbb0fbe69c82c…); EA-COMPLETE-01 (registered c185adb40e7b33df…); EA-CORPORA-08, -10, -11
license: CC BY 4.0
---

## WHAT THIS DOCUMENT IS

**1.** This is the technical report behind a short section of a companion article on the unity of the Platonic and Aristotelian corpora. The article reads texts; this report reports measurements, with their designs, their controls, their failures, and their limits. **Nothing here is an argument about authorship.** It is the record of what a set of instruments returned when pointed at two corpora, and of what killed most of them.

**2.** It has two parts. **Part I** reports the one measurement in the investigation that returned a positive: a six-function specification of a transmission apparatus, fixed before any text was assigned, which both corpora fill at the level of the individual work, with one function completed across the boundary between them — and the controls that make the result a result, and the concession that keeps it from being more than it is. **Part II** reports the instruments that read lexical distribution, every one of which was destroyed by a control run in the same session, and draws the formal result the title states: inheritance between authorial positions is observable; how many embodied makers occupied the positions is not thereby observable.

**3.** **Register and provenance.** Every number below is carried from a working notebook (EA-NOTEBOOK-01) and a measurements register (EA-AUTHORSHIP-MEASURES-01) in which results were recorded as they landed, with retractions kept in place and their refutations attached; the round and measurement identifiers are given so the trail can be followed. The notebook's discipline — the ordinary reading stated first and in full, every result carrying the limit that travels with it, a number not in the file did not happen — governs this report as it governed the notebook. Paragraphs are numbered for citation. Markers of the form ⚠ flag a limit, a retraction, or a result weaker than it looks; they are part of the record, not decoration.

**4.** **Corpora and methods, in brief.** Greek texts are the Perseus canonical-greekLit TEI (perseus-grc2) for Plato and the *Metaphysics*, and the OpenGreekAndLatin First1KGreek TEI (1st1K-grc1) for the Organon, *De anima*, *De memoria*, and *GC*; retroversions and works of disputed period were excluded from the seated Aristotelian corpus. Comparison corpora: Josephus, Philo, Plotinus, the New Testament, nine Attic orators (EA-CORPORA-08), Thomas Aquinas from the Corpus Thomisticum (6,698,317 tokens, three-way split: independent / Aristotle-commentary / other-commentary; EA-CORPORA-10), Albert the Great from the Borgnet *Opera omnia* (nine of thirty-eight volumes, OCR text usable for structural and function-word measures and unsafe for rare lexemes), Fernando Pessoa from Arquivo Pessoa (1,254,436 tokens, 25 positions; EA-CORPORA-11), and the modern documentary master–student pairs named in Part II. Distributional measures are computed on function-word profiles (top-120 to top-160 forms) over fixed-size contiguous blocks (2,500–4,000 tokens), with dispersion as mean pairwise block distance and partition effects reported as ratio of cross-label to within-label distance with Z against random relabelling of the same index set. Percentiles are against synthetic multi-author pools (n = 400, five works each). The naming-gap probe counts explicit flags of an unnamed class followed by a coinage (ἀνώνυμον … ὀνοματοποιεῖν and equivalents; Latin *innominat-*), per 100k tokens, against a division-density denominator per 10k.

**4a.** **Provenance of the six-function specification.** The specification was not induced from the Platonic and Aristotelian corpora. It was generated in a separate investigation of textual transmission — the future-reader framing that preceded Round 12 — and registered (EA-YIELD-02) before any Platonic or Aristotelian text was assigned to it. No claim from that investigation is presupposed in this report; the specification's external origin is what makes the assignment rule of Part I a test rather than a description.

**5.** **What the report does not contain.** No argument that one person wrote both corpora. No claim that the apparatus of Part I is neutral (it was specified by an investigator who expected to find it, and says so). No use of any measurement as evidence about the count of embodied makers, since Part II's result is that the measurements do not carry that information. And no reproduction of the companion article's readings; where a paragraph below refers to "the companion article," it refers to that reading and does not depend on it.

---

# PART I — THE FUNCTIONAL COMPARISON

**1.** The companion article reads two corpora as demonstrating one capacity under opposite conditions. **This part reports them doing one thing, and reports it with its controls.**

**2.** ⚠ **And it is the paper's only positive measurement.** Everything in Part II
failed a control. **This did not**, and it is placed before Part II so that the failures
are read against a result rather than in place of one.

---

## 1. THE SEPARATION IS MAXIMAL

**3.** On the declared partition, the two corpora are as far apart as anything this
investigation measured.

    Z = +39.18 on the declared partition
    first-person narration    100.76 / 10k   against   6.04
    vocative                   64.30         against   8.64
    reporting verbs           111.78         against  23.89

**4.** **And it runs the other way on the mathematics:** ἀνάλογον **10.3×**, διάστημα
**8.5×**, μονάς **8.1×** denser in Aristotle.

**5.** > **Dialogue against treatise, narrative against exposition. Whatever else is
> true, these are not two samples of one manner.**

---

## 2. AND THE SEPARATION IS THE OBJECT

**6.** **Aristotle's internal variance is the strongest anomaly this investigation
ever measured.** Across his works he disperses far more than a single author should —
enough that the first measure of it (M10) read him as exceeding synthetic
multi-author pools.

**7.** **Then the object is held constant.**

    author      n    within-domain   cross-domain   ratio       Z
    Aristotle   26         0.0667         0.0993   1.489   +4.54
    Plato       20         0.0499         0.0592   1.186   +1.75

**Subject determines Aristotle's shape about 2.6× more strongly than Plato's.**

**8.** **AND THE ANOMALY DOES NOT SHRINK. IT DISAPPEARS.**

    Aristotle, within-domain overall     0.0571
    Plato, total                         0.0570

**9.** > **A difference of one ten-thousandth.** Hold the object constant and the
> corpus that looked like several authors has a **within-domain dispersion
> numerically indistinguishable from Plato's overall dispersion.** ⚠ *A parity of
> dispersions, not of corpora: the two remain Z = +39.18 apart on the declared
> partition. What resolves is Aristotle's apparent many-authoredness, which is
> strongly object-conditioned; the number says nothing about the two corpora being
> one.*

**9a.** **And the parity has a measured base rate.** Eleven seated corpora, one
feature space, all 55 pairs: **|Δ| ≤ 0.0001 occurs 0 of 55 times.** The closest pair
in the whole set — Josephus 0.0208 against Philo 0.0211 — differs by 0.00026,
**two and a half times this gap.** ⚠ *Limitation, stated: that base rate is
total-against-total; this quantity is object-controlled residual against
uncontrolled total, a different pairing, and its own base rate is UNRUN — it needs
domain classifications that exist only for Aristotle. So: the parity is not a
generic artifact of dispersion measures; whether residual-against-total parity is
rare remains open.*

**10.** **And the residual is ordered by object, not by author.** Domain by domain,
against 400 synthetic five-work multi-author pools (mean 0.0669, sd 0.0208):

    ethics   0.0226   →   0.5th percentile of multi-author pools
    psych    0.0390   →   6.5th
    nat      0.0465   →  16.2th
    polit    0.0584   →  39.0th
    bio      0.0680   →  56.8th
    poet     0.0707   →  61.2th
    logic    0.0942   →  88.5th

**Within ethics, Aristotle is tighter than 99.5% of multi-author pools** — tighter
than Josephus, tighter than Philo, against the pool baseline.

**11.** **The ordering is read as the object-space of each domain.** ⚠ *A reading:
object-space is characterised here by description of the domains, not by an
independent metric of it.* *Ethics has one object
and one register. Logic ranges over categories, interpretation, analytics and
sophistical refutations — the widest internal object-space of the group.* **The
remaining dispersion tracks the heterogeneity of the subject matter within each
domain, not the author.**

**12.** > **What made him look like many authors is that he wrote about many things.**

---

## 3. AND THAT IS THE COMPANION ARTICLE'S FORMULA, AT CORPUS SCALE

**13.** **The companion article's second section gives a formula from *De anima* II.2 (413b):** a living thing is **ἐντελεχείᾳ μὲν μία, δυνάμει δὲ
πλείονες** — one in actuality, many in potentiality — and a cut does not create the
parts but actualises a plurality the unity already had.

**14.** **Section 2 above is that formula measured.** **One corpus, in actuality. Many, in
potentiality — and the cut that actualises them is the object.** Divide by object and
the many appear, at 1.489 and Z = +4.54. **Hold the object and the one returns, at
0.0571 against 0.0570.**

**15.** **AND THIS IS THE METHOD ITSELF.** *Division cuts
a genus at a differentia.* **Here the genus is a corpus and the differentia is the
object**, and the cut is the operation *APr* I.31 calls **μόριον τῆς εἰρημένης
μεθόδου**. **The corpus is divided by the operation the corpus theorises.**

**16.** **So the sequence the paper has been walking is measurable at its middle
term:**

    De an. 413b   the soul, one in actuality, many in potentiality        DOCTRINE
    here          the corpus, one when the object is held, many when
                  it is divided by object — 0.0571 against 0.0570         MEASURED
    Λ 9           the divine, where the terms division separates are not
                  other, and the division terminates                      Λ 1074b–1075a

**17.** > **First the soul divided across objects. Then the divine, where there is no
> object other than the knower and the division closes.** *The middle term is the one
> that can be counted, and it comes out at a ten-thousandth.*

**18.** **And the doctrinal reading is the corpus's own.** This is **mimesis in the
*Republic* III sense, moved from voice to form**: the tragedian disappears into his
character; **the treatise disappears into its object.** *On which Aristotle **has no
style because having one would be a failure of the method** — a consistent manner
across ethics and biology would mean the manner was not taking its shape from the
thing.*

**19.** ⚠ **AND IT DOES NOT ESTABLISH ONE HAND.** *A school trained to a method that
conforms to its object produces the same measurement, and the object-conformity is a
property of the method and not of a person.* **It removes an anomaly rather than
supplying a positive finding — but the anomaly it removes was the strongest one the
investigation had**, and what remains after its removal is agreement to four decimal
places.

---

## 4. AND THE APPARATUS IS FILLED TWICE, COMPLETELY

**20.** **Six functions, frozen before assignment**, from the archive's specification
of a transmission apparatus:

    T1  encoding          how a λόγος is put into a substrate
    T2  substrate         what receives the impression
    T3  decommissioning   how the source is withdrawn
    T4  withholding       what is deliberately not supplied
    T5  recovery          how a receiver reconstitutes it
    T6  verification      how a true instance is told from a false one

**21.** ⚠ **Assignment was made only from received characterisation of what each work
is ABOUT** — not from what appears in it. **That rule is load-bearing and §5 below
shows why.**

**22.** **PLATO — 6/6, in SIX DISTINCT DIALOGUES, no doubling, sharpness 1.00:**

    T1  encoding          Phaedrus 274b–278b     the critique of writing
    T2  substrate         Theaetetus 191c–196b   the wax block
    T3  decommissioning   Phaedo                 the death, channel by channel
    T4  withholding       Parmenides             objections raised, answer withheld
    T5  recovery          Meno 80d–86c           ἀνάμνησις
    T6  verification      Sophist 231b–236d      εἰκαστική against φανταστική

**23.** **ARISTOTLE — 6/6, in FIVE distinct works, one doubling, sharpness 0.83:**

    T1  encoding          De interpretatione 16a  τὰ ἐν τῇ φωνῇ … σύμβολα, καὶ
                                                  τὰ γραφόμενα τῶν ἐν τῇ φωνῇ
    T2  substrate         De anima 424a           ὁ κηρὸς τοῦ δακτυλίου ἄνευ
                                                  τοῦ σιδήρου δέχεται τὸ σημεῖον
    T3  decommissioning   De anima III.5          the separable νοῦς  [doubles T2]
    T4  withholding       Metaphysics B           the aporiai, not all resolved
    T5  recovery          De memoria              ἀνάμνησις
    T6  verification      Soph. El. 164a          φαινομένων μὲν ἐλέγχων ὄντων
                                                  δὲ παραλογισμῶν

---

## 5. AND THE CONVERGENCE IS AT THE LEVEL OF THE DEVICE, NOT THE THEME

**24.** **T2 — the same analogy, and the second is the definitional form of the
first.** The *Theaetetus* wax block; and *De anima* 424a, the wax receiving the
signet's mark **ἄνευ τοῦ σιδήρου καὶ τοῦ χρυσοῦ** — without the iron and the gold — stated
as **τὸ δεκτικὸν τῶν αἰσθητῶν εἰδῶν ἄνευ τῆς ὕλης.** *form received without matter — the condition the companion article reads at Λ 9 and De an. 413b.*

**25.** **T5 — the same word.** **ἀνάμνησις** is the *Meno*'s term at 81d and the
title of Aristotle's treatise.

**26.** **T6 — the same discrimination, and both works are titled for the sophist.**
The *Sophist* separates **εἰκαστική** from **φανταστική**; the *Sophistici Elenchi*
separates **ἔλεγχοι** from **φαινόμενοι ἔλεγχοι**. *A true likeness from an apparent
one; a refutation from an apparent refutation.*

**27.** **T1 — the encoding stack is stated in the work whose title is the word
Plato uses for relaying another's mind.** *De interpretatione* — **ἑρμηνεία**, which
at *Statesman* 260d names the arts that relay **ἀλλότρια νοήματα** as against the
self-commanding genus. **And it is the work Andronicus judged spurious.**

**27a.** **And the self-commanding side of that contrast is a coinage.** The genus
was found nameless — **σχεδὸν ἀνώνυμον ὂν τυγχάνει τὸ τῶν αὐτεπιτακτῶν γένος** —
and named in the act: **αὐτεπιτακτική**, the art that issues from itself rather
than relaying another's mind. Kings are placed into it; it is **οὐ τὸ σμικρότατον
τῶν γενῶν** — not the smallest of the genera — and its remaining members are left
**unentered**, on the stated ground that the inquiry was for the ruler's sake.
**The distinction this paper turns on — speaking from oneself against relaying
another's mind — was available, named, and coined in the corpus, in a naming-gap,
and left open.** *What the passage does not do is apply it to authorship; the
unentered genera are unentered, and supplying them is an inference the text does
not license.*

**28.** > **These are not shared topics. They are the same device, the same term, and
> the same discrimination, distributed across two corpora that share almost no
> surface.**

---

## 6. AND ONE SLOT IS FILLED ACROSS THE BOUNDARY

**29.** **T2 is not merely matched. It is completed.**

    Theaetetus 191c    the wax opened, the route run, and abandoned (196b):
                       ὃ ἔφαμεν ἀδύνατον — what we said was impossible

    De anima 424a      the same figure, and the missing element supplied:
                       ἄνευ τῆς ὕλης

**30.** **No cross-reference. No announcement.** *One work attempts a procedure and
declares it impossible; another retains the machinery and supplies the term that
makes it work.*

**30a.** **And "no announcement" has a comparison class.** Matthew announces by
formula — ἵνα πληρωθῇ τὸ ῥηθέν. **Catullus announces three times over: the Sapphic
strophe (the metre is the citation), the translation form, and "Lesbia" — the woman
of Lesbos, first appearing inside the Sappho translation.** *Everyone who performs a
transformation this close announces it — the announcement is how the reader is told
to read it as a transformation.* **At the moment of greatest functional interlock,
this corpus does not.** ⚠ *The observable is exactly this and no more: at* De anima
*424a, completing the abandoned figure with the seal retained and ἄνευ τῆς ὕλης
supplied, there is no mention of Plato and no cross-reference to the* Theaetetus.
*Corpus-wide naming rates cannot see it and are not evidence of it either way.*

**30b.** **And a second slot of the same shape, found by argument-shape alone.**
*Parmenides* 132a — apply the account of largeness to itself, ἄπειρα τὸ πλῆθος, the
regress without limit, and **the answer withheld** — and *SE* 182a, the
definition-by-addition regress: *if the snub is concavity-of-nose, and there is a
snub nose, then there is a concave-nose nose.* **The same logical move, in disjoint
vocabulary, located by a search on the argument's shape with no shared word to
find.** Aporia in one corpus, apparatus in the other, twice. *Two is a class with
two members and a method that found the second unprompted; it is not yet a
phenomenon.*

**31.** **And the completion result across the four completion-slots: one figure, one
abandonment, two completions — three of the four one operation.**

**31a.** **The one operation, with both of its halves.** *De anima* states what
crosses — the σημεῖον without the iron and the gold. ***De memoria* 450a states what
must be true of the receiver for it to cross** — ἐνσημαίνεται οἷον τύπον, καθάπερ οἱ
σφραγιζόμενοι τοῖς δακτυλίοις — **and why reception fails: running water, too hard a
surface, the young flowing by growth, the old by decay.** Together, an account of
transmission with both halves — what is sent, and what a receiver must be. T1 is the
same mechanism as an invariance theorem: form constant across variable matter,
applied to script and speech. T4 is the weakest member and is marked so.

---

## 7. THE CONTROLS, AND THE ONE THAT VALIDATED THE RUN

**32.** **Four rivals were frozen with the apparatus** — the four causes, the divided
line, the cardinal virtues, and a random control.

    R1  four causes        4/6 on Plato, with the Timaeus doubling
    R2  divided line       6/6 NOMINAL — but ALL SIX SLOTS from one passage,
                           Rep. 509d–511e. SHARPNESS 0.
    R3  cardinal virtues   6/6 — but four slots from Republic IV alone
    R4  random control     0/6

**33.** > **COVERAGE ALONE DOES NOT DISCRIMINATE. The registered sharpness term
> does all the work** — and no rival produces six functions carried by **distinct
> works** in **both** corpora.

**34.** **AND THE RANDOM CONTROL SHOWS THE ASSIGNMENT RULE IS LOAD-BEARING.** Run
on the Johannine group:

    by "what the work is ABOUT"        0/6
    by "what APPEARS in the work"      6/6

**35.** The vine, the boats, the healings, the war in heaven, the merchants of Babylon,
the storm from the throne — **all present, and none of them what any book *is*.**

**36.** > **Under the appearance reading the entire run would have hit the void
> condition. The received-characterisation rule is not a formality. It is what makes
> the measure a measure.**

---

## 8. ⚠ WHAT THIS DOES NOT SHOW, AND IT IS THE WHOLE OF THE OBJECTION

**36a.** **What a school transmits, and what it cannot.** Statements transmit —
including *the master erred here*: inside the Organon, Plato appears **four times,
all in the *Topica*, all four as examples of definitional error.** **That is
evidence FOR the school hypothesis and is admitted as such.** An abandoned execution
is different: not a statement but **a hole with a shape** — and the corpus marks
these executions REFUTED, ὃ ἔφαμεν ἀδύνατον, so completing one requires reading a
failure as unfinished **against the doctrine's own verdict.** *Maas's errores
coniunctivi, one level up: shared correct method proves nothing; what discriminates
is a structure that could not have been transmitted as doctrine, because the
doctrine says it failed.*

**37.** **A SCHOOL WITH A SHARED PROGRAMME PRODUCES FUNCTIONAL CO-COVERAGE.** Two
generations working the same problems, with the second reading the first, would fill
the same six slots and would converge on the same devices. **6/6 does not discriminate
one maker from a research tradition, and no claim that it does is made here.**

**38.** **What it does show is narrower and is not nothing:**

- **the apparatus is complete in both corpora**, at the level of the individual work
- **the fillings converge at the device**, not at the topic — the same analogy, the
  same term, the same discrimination
- **one slot is completed across the boundary**, where one work declares a route
  impossible and another supplies the missing element without citing it
- **and no rival specification does this**, which means the six slots are not a shape
  that any organised corpus would fill

**39.** ⚠ **AND THE SLOTS WERE SPECIFIED FROM AN ARCHIVE'S OWN MODEL OF
TRANSMISSION.** *They were frozen before assignment and the rivals were frozen with
them, which is what makes the run testable. **But the apparatus is not neutral: it was
built by someone who expected to find it.*** *A reader who thinks the six functions
were chosen to fit should attack there, and ¶¶32–33's rival scores are the answer
offered.*

**39a.** **And the ceiling of every correspondence measure is fixed by its own
calibration.** The closest documented transformation in the comparison set —
Sappho 31 to Catullus 51 — aligns at **C = 0.688, slot by slot, sequence preserved
— and Catullus is not Sappho.** **Maximal closeness is compatible with distinct
authorship, demonstrably, in the standard case. Any correspondence value establishes
relation, never authorship** — which is the step at which every instrument in Part II
collapsed, stated here so it is not forgotten at the one instrument that returned a
positive. *And the test that would say whether this pair is the same KIND of object
as a documented heteronymic system is named and unrun: a remainder — something
invariant across the positions not explained by shared language, genre or subject.
Six-slot coverage is not that measure.*

---

## 9. WHAT PART I ESTABLISHES

**40.** **Two corpora whose separation is entirely accounted for by the object** — 0.0571
against 0.0570 once it is held — **fill one complete transmission apparatus between
them** — six functions, distinct
works, converging at the device, with one slot completed across the boundary.

**41.** **That is a positive result and it is the only one in the paper.**

**41a.** **And the conjunction has a comparison sample, thin and stated.** The
declared partition at **Z = +39.18** with the interlock at 6/6 — against: **Josephus,
unified at both levels; the New Testament, loose at both** (declared partition
**Z = +2.83**, slot-fill only at the author-group level); **Plotinus and Philo,
separated and not interlocked.** *Maximally separated at the substrate, maximally
interlocked at the function — nothing else in the sample does both, and the
conjunction has been measured once.* **That is the shape of a σύμβολον: halves that
do not resemble each other and only fit.** ⚠ *The comparison class is one
multi-author corpus plus the rival-lens controls, because the orator baseline failed
for the interlock measures. A school inheriting a transmission programme could
produce the interlock; the substrate divergence is ordinary for two authors. The
conjunction is what is unusual, and one measurement of it is one measurement.*

**42.** **It is consistent with one maker and consistent with a school**, and Part II
will show that no distributional instrument tells those apart. **This section does not
close the question. It establishes that there is a machine to have a question
about.**

---

## STANDING

**43.** **Frozen before assignment**, with the registration hash recorded in the
notebook (EA-YIELD-02, Round 12). **The first design of this measure was wrong and is
recorded as spent**: it measured whether a lens's *vocabulary* co-varies, which is not
what interpretive yield is.

**44.** **Checkable:** every locus is given and every Greek phrase is quoted. **The
rival scores at ¶¶32–33 and the Johannine control at ¶¶34–36 are from the same run.**

**45.** **Conceded in full at ¶37:** a school produces this. **And at ¶39:** the
apparatus was specified by someone expecting to find it, and that is where the
measure is weakest.

**46.** **Not claimed:** that the convergence is designed, or that it identifies a
maker. *It identifies an apparatus.*

---

## PART II — APPARATUS

---

## THE HETERONYMIC ARCHITECTURES ARE NOT ONE

**[H1] PESSOA CLOSES BY REMAINDER; THE CONFIGURATION WOULD CLOSE BY SUM.**

    PESSOA          progressive subtraction toward an invariant.
                    Caeiro 1.781 (sensation only) → Soares 1.632 (one street) →
                    Mora 1.437 (one doctrine) → Reis 1.374 (one meter) →
                    Campos 1.129 (everything) → orthonym 1.033 (no restriction)
                    The series is a search DOWNWARD: what is the least one can
                    specify and still get a self that coheres?
                    And the orthonym's shape — loosest, least container-like,
                    as far from itself as from the voices it generates — is
                    the intra-Aristotle shape: M10 measured Aristotle's
                    dispersion at 0.1033, above the 100th percentile of
                    synthetic five-author pools, in the one comparison corpus
                    whose single authorship is documented.

    THE CONFIGURATION   complementary coverage. Positions need not approach an
                    invariant remainder; they can be complementary pieces.

> **There is no single P(E|H_H) until the type of heteronymic construction is
> specified.** *This prevents the mirror of the error the paper charges: defining
> heteronymy elastically enough to absorb every result.*

**[H2] AND THE DEATH OF THE MASTER IS NOT INDEPENDENT EVIDENCE.** Pessoa gives Caeiro
a lifespan, a last poem dictated on the day of death, disciples reporting his speech,
and names **the school** — *as obras do Mestre e algumas do discípulo directo*. **The
master position is constituted by dying.** ⚠ *And Pessoa was reading Plato. Two of the
best-documented heteronymists built the Socratic structure, and imitation cannot be
distinguished from convergence on the cases available.* **But note what the
imitation reading concedes: they imitated it AS a heteronymic architecture** —
reading master-disciple-school-death as a way to build authorial positions, and
finding it good enough to copy — *a reading of the corpus made by the two moderns
best qualified to recognise the operation. Not evidence. Not nothing either.*

---

## THE SCHOLASTIC CONTROL, AND WHY IT FAILED

**[C1] ALBERT AND AQUINAS ARE NOT A CONTROL FOR OBJECT-CONDITIONING.**

**They are the best available control for PERSON-DISTINCTNESS** — canonization
proceedings, Dominican chapter records, university registers: evidence with no
relation to textual style.

**⚠ AND THEY ARE INSIDE THE ARISTOTELIAN TRANSMISSION.** Both are commentators on
Aristotle; the *Summa*'s quaestio-and-articulus structure is the Aristotelian
partition applied to theology. **So Aquinas's 1.503 is not an independent author
reaching Aristotle's 1.489 — it is the ratio appearing in its most saturated
inheritor.** *M43's title claimed the control problem was solved. It is not, and the
correction is carried in the register.*

**[C2] AND THE TABLE REFUTES ITS OWN USE.** 1.489 → 1.503 → 1.762 → 2.707. **The ratio
tracks how unlike the objects are. It never tracked how many authors there were.**

**[C3] THEOPHRASTUS WAS VOIDED FIRST, ON THE SAME GROUND (M36).** *The negative class
M36a demanded — a corpus performing heavy division-and-classification on an object
that is not the Aristotelian corpus, standing outside its transmission — remains
EMPTY. That may be a structural property of the object rather than a gap in the
search.*

---

## THE COMPARATIVE PAIRS

**[P1] THE BATTERY'S CLASS 1**, on documentary attestation only, with ancient
attestations excluded as circular: **Wundt → Titchener** (Leipzig PhD 1892,
university records); **Freud → Jung** (1907–13 correspondence, IPA presidency);
**Albert → Aquinas** (Dominican chapter records).

**[P2] AND THE GREEK PAIRS THAT KILLED IT.** **Lysias → Isocrates**, with no teaching
relation, outscores **Isaeus → Demosthenes**, which has one, on every inheritance
feature. **Herodotus → Thucydides** is contemporary and scores like the distant pairs
— Ionic against Attic. *The battery reads period and dialect.*

**[P3] HERODOTUS → JOSEPHUS** as the distant-lineage control. *Josephus also carries
the archive's separate Revelation-priority work and is named here only as a battery
member.*

---


# PART II — THE INSUFFICIENCY OF LEXICAL MEASUREMENT

**1.** The companion article establishes an operation at the level of λόγος and an
identity there. **This part measures the matter.**

**2.** **It is placed here and not first because the companion article offers a reading of the level at
which it fails** — carried as reading, not as prediction; section VII below withdraws the
proof-step — stated before any instrument was built: **οὐχ ἑτέρου ὄντος τοῦ νοουμένου καὶ τοῦ
νοῦ, ὅσα μὴ ὕλην ἔχει** — the identity holds **in whatever has no matter**. And *Phdr.*
276a distinguishes the corpus's λόγος from its written **εἴδωλον**.

**3.** **What follows is not the concession the reader expects. It is the predicted
result, reported in full, including the parts that came out otherwise.**

---

## 0. THE SCOPE OF THIS SECTION'S CLAIM

**Part I reported a positive.** The apparatus is complete in both corpora, the fillings
converge at the device, and one slot is completed across the boundary. **That
instrument read the relation between operations.**

**This section reports the instruments that read lexical distribution, and they
failed.** ⚠ **So the claim is narrowed to what it can carry:** *the LEXICAL and
DISTRIBUTIONAL instruments do not identify latent maker-count.* **Not every
instrument — the ones addressed to the substrate.**

> **The instrument that read the relation between operations found something. The
> instruments that read the substrate did not.**

## I. WHAT WAS BUILT, AND WHAT KILLED IT

**4.** Fifteen distributional features were built to distinguish an **embodied**
master-student relation from a **constructed** one. Every one was destroyed by a
control run in the same session.

    SIZE       downsampling class-1 masters to 20,027 tokens moved four
               features into the heteronymic range. Wundt→Titchener's
               novel-vocabulary rate: 7.3 → 15.5

    LANGUAGE   every Greek pair 59–79 on trigram overlap; every non-Greek
               87–90. A z of −10.35 was GREEK WORD ORDER, and within Greek
               the target sits at the TOP of the range

    PERIOD     Lysias→Isocrates, with NO teaching relation, outscores
               Isaeus→Demosthenes, which has one, on every inheritance
               feature. Herodotus→Thucydides is contemporary and scores
               like the distant pairs — Ionic against Attic

    BROKEN     and one control was itself broken, and is recorded as broken:
               random token sampling destroys the block structure the
               coverage measure reads

**5.** **Coverage geometry looked excellent and collapsed under contiguous
size-matching** — and both halves belong in the record. At full corpus size it was
the first clean separation any measure produced: documented pupils cover 69–98% of
the master's ground, heteronymic disciples 0–20, **and Plato→Aristotle sat at 66.8,
inside the pupil band.** Size-matched with contiguous windows, **the target fell to
18.8 — inside the heteronymic band — and Albert→Aquinas to 0.0, below every
heteronymic pair.** The measure reads corpus size. **Reception capture was measured
and is explicitly non-discriminating. The formulaic n-gram result was a language
artifact.**

**5a.** ⚠ **AND THE INSTRUMENT SET WAS NEVER VALIDATED BEFORE USE, WHICH IS
DISCLOSED HERE BECAUSE THE SECTION'S AUTHORITY DEPENDS ON IT.** No measure built in
this investigation was scored on known-status pairs before being applied to the
question. Checked once, late: **agreement on known-status pairs was 1 of 3, and one
instrument classified Plato|Xenophon as SAME at 0.0330 against a known-different
truth.** *You cannot detect an object that defeats measurement until your measures
are characterised on objects that do not.* **Read one way this is the section's
sharpest support — instruments that cannot sort Plato from Xenophon are
non-probative a fortiori. Read the other way it means some nulls above are facts
about uncharacterised instruments rather than about the object. Both readings are
open, and the validation suite that would close them does not exist.**

## Ia. AND FOUR FURTHER MEASURES BELONG IN THE REPORT

**M30 — the naming-gap reflex is shared at 9.4×, P ≈ 0**, with Aristotle's own policy
at *NE* 1108a and the *Topics* faulting Plato for the same practice. **And the transfer
class: five of eight charges Aristotle brings against Plato run backwards** —
**μεταφορ-** occurs **zero** times in Plato and 112 times in Aristotle, who faults
Plato for speaking metaphors in a word Plato never uses. *The internal control fires
correctly: **μῦθος** does not transfer.*

**R38 — the target, scored descriptively, and the score is not in the thesis's
favour.** With the battery's non-discrimination established first (novel-vocabulary
and direction-uniformity were size artifacts; the bands are three points wide), the
target was placed: **its values are invariant under a 23× change in master-size** —
the only pair in the set whose numbers are not an artifact of how much text survives
— **and, size-matched, it sits at or beyond the class-1 end, not the heteronymic
end: F4 at 29.0, above class 1's 24.5 and above the heteronymic maximum of 23.9.**
*Descriptive placement only; §150's verdict — no demonstrated discriminatory power —
governs it, and "inside class 1's band" is not evidence of membership. It is
reported because omitting an adverse placement while carrying the favourable
non-results would be the selective reporting this section exists to refuse.*

**M38 — the two-sided ledger, and it is the honest cost comparison.** Five latent
assumptions on the inheritance account; four on the configurational one after K1 was
withdrawn. **Neither is free, and both are stated.**

**M45 — a default earns prior, not likelihood.** The received account gets its
historical prior, the external record and the prima facie partitions. **It does not
automatically get P(E|H_S)=1 for every internal observation because a story of
influence can be constructed afterward.** *This is the answer to "the same results
follow without the hypothesis," and it is an argument about burden.*

**M39 and M44 — the anchoring is asymmetric and the adjudicator is inside.** Aristotle
is the only position with an epigraphic anchor (the Delphic decree, at S9b's reduced
strength). **And the attribution apparatus demonstrably manufactured figures it then
adjudicated:**

    HICETAS and ECPHANTUS of Syracuse   argued to be CHARACTERS in dialogues by
                                        Heraclides of Pontus, received by the
                                        doxographic tradition as historical
                                        philosophers with doctrines

    TIMAEUS OF LOCRI                    acquires a biography, then a FORGED
                                        CORPUS in his name. Other ancient reports
                                        are likely based on Plato's Timaeus or on
                                        the spurious works, and some hold that
                                        Plato used him as a MASK for Archytas

> **A speaking position generated a philosopher, who then received a bibliography.
> The reputational mechanism did not detect these. It produced them.**

⚠ *Standard scholarship on those figures, not this paper's inference. What it
establishes is that the apparatus which adjudicates attribution has, in documented
cases, manufactured the parties to the adjudication.*

## II. AND TWO CONTROLS FAILED AFTER BEING RELIED UPON

**6.** **These are reported because a paper that faults an apparatus for suppressing
its own negative results cannot suppress its own.**

**7.** **AQUINAS CANNOT NORMALISE ARISTOTLE'S OBJECT-CONDITIONING.** The argument was:
Aristotle's ratio of 1.489 is ordinary, because Aquinas — a securely distinct single
author — reaches 1.503. **Aquinas's partition apparatus is Aristotle's.** The
*Summa*'s quaestio-and-articulus structure is the Aristotelian partition applied to
theology, so 1.503 is not an independent author reaching the ratio but **the ratio
appearing in its most saturated inheritor.** The object was measured with a
descendant of itself.

**8.** And the table refutes its own use: **1.489 (Aristotle) → 1.503 (Aquinas
independent) → 1.762 (Aquinas on Aristotle) → 2.707 (Aquinas on unlike objects).**
**The ratio tracks how unlike the objects are. It never tracked how many authors
there were.**

**9.** **CONFINEMENT OF ATTESTATION DOES NOT DISCRIMINATE.** Socrates is 99.5%
confined to the four-corpus cluster — and **Protagoras is 99.8%**, Gorgias 99.0%,
Prodicus 98.5%, against Cleon 64.6%, Pericles 63.9%, Alcibiades 56.4%, Themistocles
25.4%. **The split is by kind of figure. Being a subject of philosophical dialogue
produces confinement, and no one holds that Protagoras was constructed.**

---

## III. THE FORMAL RESULT

**10.** **Master-student and heteronymic configuration are not competing
relation-types.** A heteronymic system **instantiates** master and disciple — Pessoa
states his own school in those words, master and direct disciple. **Same surface
relation. Only the latent maker-count differs.**

**11.** > **INHERITANCE IS OBSERVABLE. EMBODIMENT IS NOT THEREBY OBSERVABLE.**

**12.** **So the surface relation was never going to decide.** The received account
cannot use *master and student* to explain the textual architecture and
simultaneously use that architecture as evidence that there were two makers.

---

## IV. ⚠ AND IT IS NOT ALL NULL — BUT LESS THAN IT LOOKS

**13.** **Size-matched, Plato→Aristotle sits INSIDE the documented direct-inheritance
range on every tested feature**, at z between −1.06 and +0.29. **And Albert→Aquinas,
a documented master-student pair, falls BELOW every heteronymic pair.**

**14.** **That is a result and it is stated. Then it is qualified, because the
qualification is the honest part.**

**15.** ⚠ **THE BAND IS ONE OUTLIER WIDE.** Against the two modern pairs alone —
Wundt→Titchener and Freud→Jung — class 1 is tight (F2 98.3–99.7, F3 0.618–0.740, F4
26.1), and **the target sits OUTSIDE on F2 and F4.** **Albert→Aquinas is what widens
the band enough to contain it** — and Albert→Aquinas is the pair **triangulated by
the target itself**, since both members are commenting on Aristotle (section II).

**16.** > **The one pair that makes the target look ordinary is the pair that is
> downstream of the target.**

**17.** **What survives:** one weak result, from one pair, with no base rate, on a
band whose width depends on a contaminated member. **Said plainly, because saying it
otherwise would be the failure this paper is about.**

---

## IVa. AND THE SCHOOL RIVAL WAS MEASURED, THREE WAYS

**17a.** **Part I concedes three times that a school could produce the machine. Here
is what the school structure was measured to produce.**

**17b.** **THE REFLEX DOES NOT TRANSMIT.** The naming-gap reflex — halt at an
unnamed class, flag it, coin — is shared by the two Greek corpora (Plato 2.60,
Aristotle 8.43 per 100k, both at heavy division rates). On the one documented
master-student pair under maximal transmission pressure: **Albert the Great shows
ZERO instances in 1,140,474 tokens of Sentences commentary while dividing at
16.4/10k** — ample opportunity, none taken — with the positive control passing (the
same probe finds **20 instances in his Aristotle commentaries**, glossing *NE*
1107b, *Graece innominatus est*). Aquinas independent: 1.07 — **one-eighth his own
rate when glossing Aristotle** (3.72), and five times his rate on Scripture (0.22).
**The reflex arrives with the source text and does not become a habit. The
documented pair does not share it. The Greek pair both carry it.** ⚠ *Limits,
flatly: one control pair is one draw; Greek philosophical prose may carry the reflex
where scholastic Latin does not; the OCR caveat stands for a rare lexeme (the
positive control makes it unlikely); nine Borgnet volumes of thirty-eight; and the
registered order of operations was not followed — this is a comparison, not the
classification test.*

**17c.** **A SCHOOL DEFAULTS TO COMMENTARY, AND COMMENTARY IS THE OPPOSITE SHAPE.**
Aquinas announces his master at saturation — 14.4 per 10k in the Metaphysics
commentary, **21.9 in the independent Summa** — and expands his source **4.61×.**
Against which the closest documented transformation compresses: sixteen lines for
seventeen, register-shifted. *A pupil in the room does not need to fulfil his
master. He can cite him.* **The falsification programme is stated and open:** eight
directly-attested contact pairs, each scorable on the same three properties; **one
pair producing unannounced, sequence-kept, transformative interlock across an
apparatus kills the claim.** Williams→Ginsberg is the sharpest unrun — the master
wrote the introduction to *Howl*, announcement by the master being what direct
contact characteristically produces. ⚠ *One school pair measured; a commentary set
against a poem across genres; this is what the structure defaults to, not a rate.*

**17d.** **AND THE SOURCE-NAMING RATES RUN THE WRONG WAY FOR PROXIMITY.** Aristotle
names Plato at **0.70 per 10k** (Σωκρατ- excluded as the variable, per M34).
Aquinas names Aristotle at 12.0–14.8; Albert at 16.2. **At the same institutional
proximity — direct pupil, same school, twenty years — the scholastics name their
master 17 to 23 times more often.** The received account absorbs this as *Aristotle
was unusually independent* — true, standard, and now a measured auxiliary rather
than a free one. ⚠ *The limit is real and travels: fourth-century Greek and
thirteenth-century Latin naming conventions are not controlled, and the one Greek
calibration at the same proximity (Theophrastus) is a fact about Greek citation
convention that this comparison has not absorbed. Carried as a source-naming fact
with its convention caveat, not as a test of any operator.*

**17e.** > **None of the three establishes one hand.** Two corpora sharing a habit a
> Latin pair does not share is a difference between pairs. A default is not a rate.
> A naming asymmetry has an uncontrolled convention under it. **What the three do is
> put content into the concession: "consistent with a school" now names a structure
> with measured defaults, and the measured defaults are not what this configuration
> shows.**

---

## V. THE FALSIFIER THAT DID NOT FIRE

**18.** **This is what keeps Part II from being unfalsifiable by construction.**

**19.** **Stated in advance:** if Plato→Aristotle had fallen **below the heteronymic
floor** — outside the constructed-configuration range on the size-matched features —
the configurational reading would have been damaged in the ordinary way, and the
paper would say so here.

**20.** **It did not happen.** The target sits inside the range. **That is not
confirmation and it is not nothing: it is a test that could have gone the other way
and went this way.**

---

## VI. THE SHAPE OF THE FAILURE

**21.** Round 48 ran several partitions of the same material and ranked them by
recoverability:

    AUTHOR (declared)         1.228     ← the only strongly-encoded partition
    ─────────────────────────────────
    BEING vs BECOMING         1.058
    SOUL vs BODY              1.046
    ONE vs MANY               1.040
    SAME vs OTHER             1.024
    NECESSITY vs CHANCE       1.017

**22.** > **The surface encodes exactly one partition strongly, and it is the one
> whose evidential value is nil.**

**23.** **The text is maximally legible about the declared boundary — the boundary
sections III above showed cannot identify maker count — and nearly illegible about every
distinction the companion article turns on.** Within Plato, SAME vs OTHER falls to **1.007, Z +1.5**:
indistinguishable from noise.

**24.** **And above/below does not cut across the author boundary.** Holding level
constant makes author separation **stronger** — 1.472 within "above" against 1.306
overall. **The declared partition dominates.**

---

## VII. WHAT THE NULLS DO AND DO NOT SHOW

**25.** ⚠ **THE CLAIM MADE HERE IS EPISTEMIC, NOT METAPHYSICAL. An earlier form of
this section said that Λ 1075a1 predicted these nulls, because the instruments are
"addressed to ὕλη." That is withdrawn as a proof-step.**

**26.** **The objection is good and is stated:** lexical frequencies, function-word
profiles, syntax, n-grams and genre signatures are **formal properties of linguistic
artifacts** at least as much as they are substrate properties. **Calling them ὕλη in
the technical sense of Λ 9 is not established**, and the companion article's λόγος-level identity is
not licensed to do the explanatory work of predicting a measurement outcome.

**27.** **What this section establishes without that bridge is sufficient:**

> **The tested distributional features do not identify latent maker-count after
> controls. INHERITANCE IS OBSERVABLE. EMBODIMENT IS NOT THEREBY OBSERVABLE.**

**28.** **That is an epistemic insufficiency, demonstrated by measurement**, and it
holds whatever one thinks of the companion article.

**29.** **And the instruments are not weak.** They resolve size, language, period,
dialect, genre and subject with high precision — Z = +39.18 on the declared
partition, Z = +145.96 on author in Round 48's chunk set. **They see a great deal.
What they do not see is how many makers occupied the positions they resolve.**

**30.** *The reader who accepts the companion article's identity will find the failure unsurprising. The reader who
does not is left with the same result, established the same way. **The section is
designed so that nothing in the companion article is needed to read it.***

**31.** ⚠ **AND THIS DOES NOT ESTABLISH THE HISTORICAL CLAIM.** That one person wrote
the corpus is a fact about embodiment — how many embodied makers occupied the
positions — and this section's formal result is that embodiment is not thereby
observable. **Part II is the record of its not being recoverable
from text. The λόγος-level identity explains the failure. It does not supply the
fact.**

---

## VIII. WHAT PART II ESTABLISHES

**32.** **Relation-type is not recoverable from lexical distribution** — not
pupillage, not constructed lineage, not heteronymic construction. What these
instruments see is period, dialect, genre, subject and corpus size.

**32a.** > **The interlock, if it exists, is not in the distributions. It is in the
> propositional structure the companion article reads and the completions Part I counted — neither of
> which any instrument in this section can reach.**

**33.** **The received account's central explanatory move is therefore unavailable to
it as evidence.** *Master and student* describes a relation between positions and
does not identify how many makers occupied them.

**34.** **And the question is not decidable at this level.** the companion article offers a
reading of why; **this section does not depend on it.** What it reports is that the
instruments built to decide it do not decide it, and why each failed.

---

## STANDING

**35.** **Every measurement is in EA-AUTHORSHIP-MEASURES-01 with its conditions and
its refutation.** M48 (the battery and its four killers), M50 (non-identifiability),
M43 as corrected (the Aquinas control), M28, Round 43 §181 (confinement), Round 48
(the ranking), Round 24 (the reflex does not transmit, with its limits), Round 28
(the school default, voided as an operator test and carried as characterization),
Round 29 (source-naming, with the convention caveat), Round 38 §151 (the
descriptive placement), Round 19 §74 (the parity base rate), and the validation
check of Pinax §7(c).

**36.** **Reported as failures after reliance:** §§7–9. **Reported as weaker than it
appears:** §§15–17. **Reported as a test that could have gone otherwise:** §§18–20.

**37.** **This section does not argue.** It reports, and the argument for its
placement is the companion article's, not its own.


---

## NOTES

*Apparatus entries bearing on this section, from
`EA-MANY-AND-ONE-APPARATUS.md`. Compression of engagement already performed; editions
and dates are as carried and are not re-verified. Items marked ⚠ named-and-not-
consulted are stated as such.*

**[II.1] On attribution method.** **Love**, *Attributing Authorship* (2002), is the
standard: attribution claims require converging evidence of distinct kinds and
stylometric evidence alone is not probative of identity. **Part II's result is that
standard, applied and reported.**

**[II.2] On the one instrument that returned a positive.** EA-YIELD-02 read λόγος,
not ὕλη — six transmission functions, Plato 6/6 across six dialogues at sharpness
1.00, Aristotle 6/6 across five works. **The school caveat stands and is the reason it
is not decisive:** a research tradition with a shared programme produces functional
co-coverage.

**[II.3] On what the nulls do not license.** **Distinct textual voice does not entail
distinct maker (M48, M50).** *This cuts against the thesis as much as for it, and
the companion article states the cost: the argument loses the right to use stylistic athetesis as a
filter.*

**[II.4] On the papyrological record.** *Corpus dei Papiri Filosofici Greci e Latini*
(Olschki, 1989–) is where independent physical evidence for the corpus's early
circulation would be found. **It has not been consulted by this investigation and is
named as the standing external check** — the kind of evidence Part II says would bear on
the question and this paper does not have.

---

## UNRUN, AND NAMED SO THEY CAN BE RUN AGAINST THIS REPORT

**1.** The residual-against-total base rate for the dispersion parity (Part I §2, ¶9a): needs domain classifications for the comparison corpora, which exist only for Aristotle.

**2.** The remainder test (Part I §8, ¶39a): whether anything is invariant across the two corpora's positions that is not explained by shared language, genre or subject — the measure on which the Greek pair would be the same *kind* of object as a documented heteronymic system.

**3.** The validation suite (Part II ¶5a): every instrument against a panel of known-status pairs, with per-method accuracy and pairwise agreement recorded, as a precondition for any adversarial test.

**4.** The falsification programme for the school default (Part II ¶17c): the eight directly-attested contact pairs on the three properties; Williams→Ginsberg the sharpest unrun.

**5.** The Theophrastus calibration of Greek source-naming convention at institutional proximity (Part II ¶17d).

**6.** The four-functional-roles measurement (Round 43 §181): whether a figure occupying four distinct functional roles across four corpora — speaking position, silent example, target, reported master — is ordinary in the class of philosophical subjects, which is the measurement the confinement test named as the one actually needed.

**7.** The independently-specified form-track (companion article §9.1): whether the corpus orders along a track defined from generic, argumentative or object-level criteria without recourse to the stylometric variables that built the early/middle/late stratification.

---

## RELATION TO THE COMPANION ARTICLE

The companion article — under review, its title withheld here so that this deposit is not a prior circulation of it — carries §§1–7 as readings of specific texts, this report's Parts I and II in a single compressed section, and a hypothesis with its cost. The article does not depend on this report for any reading. This report does not depend on the article for any number.

∮ = 1
