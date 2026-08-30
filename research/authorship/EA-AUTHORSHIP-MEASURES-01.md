---
id: EA-AUTHORSHIP-MEASURES-01
title: "The Measurement Register: Every Number Produced by the Authorship Investigation, With Its Refutations"
status: WORKING REGISTER — cumulative, additive, not a paper
opened: 2026-08-29
author: Sharks, Lee
orcid: 0009-0000-1599-0703
substrate: AI-assisted (TACHYON / Claude, Anthropic) under MANUS direction
purpose: >
  So that work can continue from full frame across contexts. Every measurement
  below was computed against commit-pinned seated corpora. Numbers are recorded
  with the conditions that produced them, and refutations are recorded beside the
  claims they killed. Nothing here is summarised out of existence because it came
  out negative.
---

# The Measurement Register

## 0. How to read this

Findings are numbered and stated with their conditions. Where a finding was later
refuted, the refutation is attached to it, not filed separately. Where a null is
uninformative rather than negative, that is said.

Unless stated otherwise: distance = cosine distance on **particle-transition
profiles** (function-word bigrams, top 300, diacritics stripped, final sigma
normalised), computed per work, on corpora seated under EA-CORPORA.

---

## 1. CALIBRATION CONSTANTS

These are the reference bands everything else is read against. They are the most
reusable thing in this document.

**M1 — Same-author band, Greek prose. ⚠ RECOMPUTED — Josephus only.**
**0.0148 – 0.0323**, n=6 pairs, mean **0.0248**. Josephus across four works and
four registers (*BJ*, *AJ*, *Vita*, *CA*) — war narrative, antiquities,
autobiography, polemic — and he stays inside 0.0323.

  → The original band cited Xenophon Socratic-vs-history alongside Josephus.
    **Xenophon is inside the candidate cluster (M33) and cannot calibrate a
    same-author band without assuming the answer.** His within-author dispersion
    is mean 0.0530, max 0.1598 — including him would have raised the ceiling from
    0.0323 to 0.1598, a fivefold inflation of what counts as "one author."
  → Josephus is **the only clean same-author reference entirely outside the
    hypothesis space.** Every band comparison in this register should be read
    against 0.0148–0.0323.
  → Plato|Xenophon at 0.0235 remains inside the corrected band; the M8 observation
    survives the recomputation, its inference does not (M33).

**M2 — Within-author dispersion, per work, by author.**

    thucydides   0.0097    (n=8)
    herodotus    0.0103    (n=9)
    plotinus     0.0130    (n=6)
    philo        0.0197    (n=29)
    josephus     0.0264    (n=4)
    aristophanes 0.0358    (n=11)
    xenophon     0.0533    (n=9)
    plato        0.0570    (n=24)
    ARISTOTLE    0.1033    (n=30)   ← highest in the sample by a factor of two

**M3 — Genre versus author effect. ⚠ CIRCULAR — the author term is void.**
Genre effect **+0.0023**, from Xenophon's fourteen works across Socratic dialogue,
history, encomium and technical treatise. That term stands: it is within-author.

The author term of **+0.0078** does **not**. It was computed as *Plato-dialogue vs
Xenophon-Socratic minus Plato-self* — i.e. **from a Plato|Xenophon comparison,
treating them as two authors.** Xenophon is a *candidate position* in the
configuration under test (seated held apart, EA-CORPORA-06/01), so using him as
the definition of "a different author" assumes the answer. See **M33** for the
clean baseline and the standing rule.

  → The "authorship moves this 3.4× more than genre" claim is **withdrawn**. It
    rested on the contaminated term.

**M33 — THE CANDIDATE CLUSTER, AND WHAT MAY NOT BE ASSUMED ABOUT IT.**
*(2026-08-29. Voids the author term of M3; corrects M8's framing; constrains all
future control selection.)*

**The cluster is {plato, aristotle, aristophanes, xenophon}.** No pair inside it
may be used as a control **of any kind — known-different OR known-same** — without
an explicit defence of the assumption. The rule is **bidirectional**: if the
hypothesis is live, a within-cluster pair's *sameness* is as much in question as
its difference. Xenophon's within-author dispersion calibrating a same-author band
(M1, corrected) was exactly this error in the other direction. The hypothesis under test would readily
expand to include all four, and — the point that makes this binding — **if one
configuration were established, more than one becomes more likely, not less**,
since an existence proof lowers the prior for the practice. Nothing here supposes
the expansion. It refuses the assumption in either direction.

**Clean baseline, author effect = between-author distance minus the mean of the
two within-author dispersions:**

    OUTSIDE the cluster    n=10   mean +0.0760   range +0.0316 to +0.1358
    CROSS cluster/outside  n=20   mean +0.0729
    WITHIN the cluster     n= 6   mean +0.0587   range +0.0299 to +0.0787

**Plato|Xenophon = +0.0299 — the lowest value in the table, below the
out-of-cluster minimum of +0.0316.** The pair used as the operational definition
of "two authors" is the closest pair in the sample.

**The cluster is not uniform.** Plato, Xenophon and Aristophanes are mutually
close (+0.0299, +0.0356, +0.0583); Aristotle is far from all three (+0.0716 to
+0.0787), inside the ordinary out-of-cluster range. Consistent with register —
three dialogic writers against one treatise writer — but no longer an authorship
finding, because the baseline it was read against was contaminated.

**Consequently contaminated and marked:**
- **M3** author term — void, above.
- **M8** — the framing *"two men nobody has ever proposed as one"* is false and is
  withdrawn; the distance stands, the inference from it does not.
- **M10 / M28** synthetic multi-author pools drew from Plato, Philo, Xenophon,
  Plotinus and Josephus — **two cluster members inside a pool labelled
  multi-author.** The M28 conclusion (subject explains the dispersion) is
  unaffected, since it rests on within-Aristotle domain partitions, but the pool
  comparison should be rebuilt from outside the cluster.
- **The feasibility check of the adversarial design** scored Plato|Xenophon and
  Xenophon|Aristophanes as known-different truths; both are within-cluster, so the
  reported 1-of-3 agreement rate is computed against an invalid panel and must be
  redone.

**Unaffected and verified:** the 61-pair empirical null pairs Xenophon only with
Philo, Thucydides, Herodotus, Josephus, Longinus, Plotinus and the NT authors —
all cross-cluster — and excludes Aristophanes as verse. Plato and Aristotle are
not in it. **The null is clean.**

---

## 2. THE PLATO–ARISTOTLE MEASUREMENTS

**M4 — Raw separation.** Plato|Aristotle per work: **0.1578**. Rank **29 of 45**
author-pairs — the far half.

**M5 — Standardised separation.** Between-author distance divided by the mean of
the two authors' internal dispersions. Plato|Aristotle = **1.975, rank 7 of 36**
— among the LEAST separated pairs in the corpus. Herodotus|Thucydides, exact
contemporaries in one genre, = **8.867**. Plotinus|Herodotus = 12.574.

  → **This corrected an error made earlier in the same session.** "Twelve times a
    normal author gap" compared a raw distance against an effect size. Adjusted
    for dispersion, the pair is unremarkable and on the close side.

**M6 — Declared-author partition strength.** Plato vs Aristotle by declared
author, 65 works: within/between **0.548**, and the true partition sits at the
**100th percentile of random partitions, Z = +39.18**. The names are
overwhelmingly strong containers.

**M7 — Reference point for M6.** The New Testament by listed author, same test:
within/between **0.869**, Z = **+2.83**. NT names carry signal but do not contain
their voices; "John" spans Gospel 0.0923 / Epistles / Revelation up to **0.1842**,
and Matthew|Luke (**0.0167**) is closer than Luke|Acts (**0.0183**).

**M8 — Plato is closer to Xenophon than to Aristotle.** Plato dialogues |
Xenophon Socratic works = **0.0235** — *inside the M1 same-author band*, tighter
than Josephus's *Vita* from his *Antiquities*.
  → ⚠ The original gloss, *"two men nobody has ever proposed as one,"* is
    **withdrawn** (M33). The measurement stands; the independence it assumed does
    not.

**M9 — Aristotle's isolation.** His self-distance (0.1033) **exceeds** his
distance to Plotinus (0.0810), a man born six centuries later. He is further from
Xenophon and Thucydides than Plato is from Homer.

---

## 3. WHAT ARISTOTLE'S HETEROGENEITY IS

**M10 — Exceeds multi-author pools. ⚠ SUPERSEDED BY M28 — the anomaly is the
subject, not the author.** Aristotle's mean internal dispersion (0.1033) sits at
the 100th percentile of 200 synthetic five-author pools drawn from Plato, Philo,
Xenophon, Plotinus and Josephus and matched to n=30 (pool mean 0.0665, sd 0.0062,
max 0.0819).
→ The figure is correct and the inference drawn from it was wrong. **Holding
subject constant removes it entirely** (M28). Do not quote 0.1033 as an
authorship anomaly.

**M11 — What the dispersion tracks.** Partition tests inside Aristotle, 30 works,
3,000 random partitions each:

    DOMAIN (subject matter)        ratio 1.373   100th pct   Z = +4.25
    received authenticity          ratio 1.506   100th pct   Z = +3.47
    EDITION (Perseus / First1K)    ratio 0.993    50th pct   Z = −0.10

  → Edition **excluded** as a confound, at the work level, confirming the
    corpus-level test at ratio 1.00.
  → **Subject dominates.** The leading explanation is one man across an
    exceptionally wide register range.
  → The authenticity signal is real but **confounded**: Andronicus drew that
    partition on internal-consistency grounds, so it may be recovering the
    stylistic structure it was built from. The two hypotheses predict the same
    measurement.

**M12 — Conservative headline. ⚠ REVISED BY M28.** The earlier form —
*the most internally heterogeneous single-author object in the sample, and that
heterogeneity is primarily register* — was directionally right and understated
the cause. **Corrected: the heterogeneity is the object. Aristotle-within-object
is ordinarily consistent, and in ethics is one of the most consistent writers in
the sample.**

**M28 — THE SUBJECT DETERMINES THE SHAPE.** *(2026-08-29, supersedes M10, revises
M11 and M12.)*

Domain effect, measured per author with 2,000 random partitions:

    author      n    within-domain   cross-domain   ratio       Z
    Aristotle   26         0.0667         0.0993   1.489   +4.54
    Plato       20         0.0499         0.0592   1.186   +1.75

Subject determines Aristotle's shape **about 2.6× more strongly than Plato's**.

And holding subject constant, the M10 anomaly **disappears**. Aristotle's
within-domain dispersion overall is **0.0571** — Plato's total figure is 0.0570.
Domain by domain, against 400 synthetic five-work multi-author pools
(mean 0.0669, sd 0.0208):

    ethics   0.0226  →   0.5th pct of multi-author pools
    psych    0.0390  →   6.5th
    nat      0.0465  →  16.2th
    polit    0.0584  →  39.0th
    bio      0.0680  →  56.8th
    poet     0.0707  →  61.2th
    logic    0.0942  →  88.5th

**Within ethics, Aristotle is tighter than 99.5% of multi-author pools** —
tighter than Josephus (0.0264), tighter than Philo (0.0197) relative to the pool
baseline. What made him look like many authors is that he wrote about many
things.

**The reading this supports.** This is mimesis in the *Republic* III sense moved
from voice to form: the tragedian disappears into his character, the treatise
disappears into its object. On that reading Aristotle **has no style because
having one would be a failure of the method** — a consistent manner across ethics
and biology would mean the manner was not taking its shape from the thing.

The residual ordering agrees: **ethics tightest, logic loosest.** Ethics has one
object and one register; logic ranges over categories, interpretation, analytics
and sophistical refutations — the widest internal object-space of the group. The
remaining dispersion tracks the heterogeneity of the subject matter *within* each
domain, not the author.

**What this does not establish.** That the corpus is by one hand. A school
trained to a method that conforms to its object would produce the same
measurement, and the object-conformity is a property of the method, not of a
person. It removes an anomaly rather than supplying a positive finding — but the
anomaly it removes was the strongest one the investigation had.

---

## 4. WHAT PLATO'S HETEROGENEITY IS

**M13 — Plato's variance is temporal, Aristotle's is topical.** Same partition
test, 24 Platonic works:

    CHRONOLOGY (early/middle/late)   ratio 1.442   100th pct   Z = +6.92
    DOMAIN (subject)                 ratio 1.130    91st pct   Z = +1.42
    FORM (dialogue / expository)     ratio 1.225    85th pct   Z = +1.08

  → The strongest partition effect measured in the entire session.
  → **Orthogonal axes.** Aristotle's dispersion is indexed by *what he is writing
    about*; Plato's by *where along a sequence*. Magnitudes fit: Plato 0.0570 is
    roughly half of Aristotle's 0.1033 — a subset, not an expansion.
  → **Caveat, standing.** The E/M/L stratification was built partly *from*
    stylometry, so this risks the circularity of M11. Denyer's argument (that
    Plato could write any style at any time) makes E/M/L a *repertoire* rather
    than a record — in which case Z=+6.92 detects a staged development, which is
    what "artificed" would claim. The measurement does not distinguish these.

**M14 — Plato's internal speaker structure.** From TEI `<said who=…>` markup:
56 speakers, 519,743 spoken words. Socrates 252,416 · Athenian Stranger 102,795 ·
Eleatic Stranger 29,497 · Timaeus 20,691.

Distances to Socrates: Athenian **0.0298**, Eleatic **0.0338** — both at the edge
of the M1 same-author band. Timaeus **0.0772** — nearly the full Plato–Aristotle
distance, inside one author.

**M15 — The equilateral.** Socrates | Athenian | Eleatic form a near-perfect
equilateral: balance (min/max displacement magnitude) **0.953**, angles 116.8° /
121.4° / 121.8°, spread under 5°. Nothing else measured comes close. **Not a size
artifact** — the three corpora are 252k / 103k / 29k words and their displacement
magnitudes are 11 / 11 / 11. Substituting Timaeus for the Eleatic collapses it to
0.719 / 41°.

**M26 — Plato writes in the form he banishes.** *Republic* 392d–394c defines the
wholly mimetic mode as speech with no reporting poet, and names it with tragedy
and comedy. Reporting-formula density per 10⁴ tokens: **20 of 31 works, 61% of the
corpus by volume, carry no reporting voice** (Crito 0.0, Statesman 1.1, Sophist
1.7, Laws 2.4, Gorgias 6.1). The *Republic* itself is **narrated at 144.1** —
Socrates reports the whole of it. The book performing the expulsion is written in
the mode that escapes it. Textual, not interpretive.

**M27 — Aristotle on the same axis.** Reporting **0.1** (lower than Plato's
dramatic dialogues), self-speaking **29.0** against their 25.3. Caveat: a treatise
has no reporting formulae because there is no conversation to report, and speaking
in his own person places Aristotle in the *un*-banished second mode. What survives
the caveat is the near-equality of self-speaking rates across the two most
formally opposed prose bodies in Greek — recorded as a measurement without an
account.

**M16 — Plato does not construct heteronymically.** Symposium speeches by
Stephanus range, against the real Aristophanes: Plato's Aristophanes speech is
**0.0854, rank 5 of 7** — Pausanias (0.0428), Socrates/Diotima (0.0556), Phaedrus
and Alcibiades are all closer to actual Aristophanic Greek. Meanwhile every speech
sits near the Plato corpus, Aristophanes' at **0.0380**. Given the one chance to
construct against a checkable target, the speech comes out *more* Platonic than
its neighbours, not less. **The only ancient case with an independently attested
target, and it reads negative.**

---

## 5. THE CALIBRATION CORPORA (known-designed)

**M17 — ∮ = 1 on Pessoa.** Pooling the three heteronyms recovers the orthonym at
**0.0258** — inside the M1 same-author band — while the best single heteronym is
Campos at 0.0498, then Caeiro 0.0903, Reis 0.2205. **Pooled beats best individual
by 1.93×.** Individually the voices do not look like Pessoa; summed, they do.

  Comparators: Josephus BJ+AJ+CA → Vita 1.08×; Kierkegaard A+B → signed 1.07×;
  Plato parts → Aristotle 1.01×; **Aristotle parts → Plato 0.78× (pooling makes
  it worse — his *Ethics* alone is closer to Plato than his whole corpus is).**

  Limits: ratio statistics carry a size confound; cross-language absolute
  comparison is shaky; Kierkegaard's seat holds four pseudonymous works of ~12.

**M18 — Ownership statistic.** Feature-ownership concentration, n=3 groups:
Plato-self 0.1025 · Kierkegaard 0.1188 · Xenophon-self 0.1349 · Pessoa 0.1442 ·
Plato|Aristotle|Xenophon 0.1890 · three independent Greeks 0.2044.
**One mind gives low ownership; many minds give high.** But the matched 2×2
design collapses it: Plato(2)+Aristotle(2) 0.1151 sits *between* two independent
controls (0.1038, 0.1242) and inside the within-author range (Plato alone 0.0830,
Aristotle alone 0.1179). **Register, not authorship.**

---

## 6. THE NEW TESTAMENT AS COMPARATOR

**M19 — Dionysius replicated.** Revelation | Gospel of John = **0.1319 / 0.1189**,
far outside anything the NT shows internally. The third-century stylistic
authorship judgment holds on this instrument.

**M20 — Revelation's nearest neighbour is Mark**, at **0.0329 / 0.0460** — inside
the M1 same-author band. Almost certainly shared Semitizing register rather than
shared hand, and the sharpest demonstration in the session that this measure reads
register as authorship.

**M21 — The Pauline ordering inverts the consensus.** Undisputed Paul | Pastorals
= **0.0494**; undisputed Paul | disputed (Eph/Col/2Thess) = **0.0873**. The
letters the field is most confident are pseudepigraphic score *closer* than the
ones it is least sure about. John's Gospel | Johannine epistles = 0.0665/0.0927 —
further apart than Paul from the Pastorals.

**M22 — NT criteria applied to Plato/Aristotle: one of five holds.**
cardinality mismatch ✗ · cross-name convergence ✗ · redundancy-with-complementarity ✗
(they are content-complementary and function-redundant, the inverse) ·
structured cross-attestation ✗ (one direction only) · **absent centre ✓**.
The one that holds is the one not measurable from texts, because its subject left
none.

---

## 7. NULL RESULTS THAT ARE NEGATIVE, NOT MERELY EMPTY

**M23 — No whole-text operator.** Monotone alignment (DTW on 40 blocks, 60-shuffle
null): *Timaeus*→*Metaphysics* Z = −0.46; *Symposium*→*Poetics* −0.68;
*Republic*→*Politics* +0.96; every candidate inside ±1.2. **No order-preserving
transform maps any Platonic dialogue onto any Aristotelian treatise.**

**M24 — Mediation through Aristophanes fails.** 100 routes, 2,000-shuffle direct
null: *Symposium*→*Poetics* direct = **−0.82**, rank 15 of 20 dialogues; nothing
in the sweep crosses 2 (max +1.89, the expected max of 20 draws). The mediation
sweep's apparent crossings sit inside a distribution whose mean is **+0.76**, i.e.
the statistic is biased upward by the DTW path's own selection.

**M25 — Corpus-layer leak deficit: TEST VOID.** EA-LEAK-DEFICIT-02
(sha256 493514a2f142385f…). Sanity control fired: Josephus pooled = **9881.2**,
Plato|Aristotle pooled = **9912.5**, both at the 100th percentile. One author's
works pooled and two authors' works pooled are indistinguishable, because pooling
homogenises blocks by construction while the null was built on single works. **No
number from that run may be quoted.**

---

## 8. FIVE BROKEN NULLS — do not rebuild these

Each was constructed, produced an apparent crossing, and was then found to be an
artifact. Four were reported as findings before the artifact was located.

1. **Deviation-from-group** — forced to r = −1 by the sum-to-zero constraint.
2. **Shared-region correlation** — dominated by the shared frequency baseline;
   high-frequency words are high for everyone.
3. **DTW mediation null** — biased upward by the path's own selection of
   high-similarity cells; mean Z **+0.76** across 100 routes, not 0.
4. **Coherence-destroying null** — inverted in sign; homogenised blocks are
   *more* similar to each other, not less.
5. **Within-row permutation** — left the global multiset unchanged, so real and
   null were identical by construction (all Z = 0.00 exactly).

**Consequence, now standing policy:** nulls for this work are **empirical** — real
matched author-pairs — not synthetic.

---

## 9. PRE-REGISTRATIONS

    EA-LEAK-DEFICIT-01   fbbd13a53a5b29af…   SPENT — tau at the 99th percentile
                                             gave a degenerate lower tail (8 of 61
                                             pairs leak exactly 0), so the
                                             predicted deficit was unobservable.
                                             Found before the test pair was
                                             computed.
    EA-LEAK-DEFICIT-02   493514a2f142385f…   DISCHARGED VOID — sanity control
                                             fired (M25).

The null set built for these — **61 matched cross-author Greek prose pairs across
19 author-pairings**, capped at 6 per pairing, from Xenophon, Philo, Plotinus,
Josephus, Longinus, Herodotus and Thucydides by book, and the NT authors — is
reusable and is the most expensive artifact produced.

---

## 10. OPEN, IN PRIORITY ORDER

1. ~~**Base rate for the *Republic* 395a / *Symposium* 223d contradiction**~~ —
   **RUN 2026-08-29, VERDICT: NOT ADJUDICATED** (EA-SNUB-01 §19-20). Loose
   criterion 653/16,449 = 4.0%, target unremarkable; strict criterion
   61/16,449 = 0.37%, target excluded on an adjacency technicality. Propositional
   contradiction is not separable by proximity-negation. The observation stays
   philological and cannot be promoted by statistics.
   **New M26 (see §4):** by *Republic* III's own criterion, 61% of the Platonic
   corpus is written in the banished mode, and the *Republic* is not.
2. **Authenticity within domain, inside Aristotle.** Hold subject constant and
   test spurious-vs-genuine. Breaks the M11 confound. Counts are thin (6 spurious
   of 30) so power may not exist.
3. **External dating against stylistic position** for M13's circularity — a
   dating source not downstream of style.
4. **A recognition measure reading λόγος rather than ὕλη** (EA-SNUB-01 §6).
   Untouched, hardest, and the one the whole line of work is missing.

---

# PART II — THE TERRAIN

*Added 2026-08-29. Everything attempted, including what failed, what was
superseded, what was left half-run, and what was never started. A later instance
should be able to see the whole floor, not only the standing results.*

---

*Everything attempted, including what failed, what was superseded, what was left
half-run, and what was never started.*

## 11. MEASURED, THEN SUPERSEDED OR FOUND CIRCULAR

**T1 — Ending profiles (aporia vs closure).** Genuine Aristotle 7/7 CLOSED
(aporia 1, closure 23); Plato majority OPEN (aporia 22, closure 15); the single
Aristotelian work with an open ending is *Oeconomica*, which is **spurious**.
→ **CIRCULAR.** The result was sharpened by excluding the spuria, and the spuria
are classified spurious partly *because* they read differently. A category built
from the consistency being measured was used to measure it. Recorded because the
error is instructive, not because the number stands.

**T2 — Coverage complementarity on the virtues.** Courage: *Laches* 0 definitional
formulas, Aristotle 7 — and he closes it explicitly (*σχεδὸν εἴρηται*) while the
*Laches* ends with an appointment to meet tomorrow. Temperance 1 vs 8. Friendship
0 vs 4. **But:** piety is dropped by both (ὁσιοτ- appears 0 times in Aristotle's
genuine ethical corpus), and the beautiful is duplicated (*Hippias Major* 17 vs
Aristotle 15).
→ **Inconclusive, and it favours influence.** Systematic design predicts complete
coverage without duplication; what was found is incomplete coverage with one
dropped question and one duplication — the profile of a successor finishing what
interested him.

**T3 — The nine-author landscape on aggregate profiles.** Produced
Aristotle|Plotinus 0.0310 as the second-closest pair in the set.
→ **SCALE ERROR.** Aggregate profiles (mean across an author's works) and per-work
profiles are not comparable, and averaging destroys exactly the variance that
matters. Superseded by M4/M5, computed per work. The 0.0310 figure must not be
quoted against per-work numbers.

**T4 — Tiling / exclusivity.** Vocabulary exclusivity: Kierkegaard A|B — the
purest symbolon available — is the **least** exclusive pair measured (0.4900).
→ Correct but the wrong operationalisation. Two halves of a broken token *share
the break line*; exclusivity measures distance in topic, not shape.

**T5 — Shared-region correlation.** Designed pairs occupy both extremes (Pessoa
Caeiro|Reis 0.4479, Pessoa heteronyms|orthonym 0.8203) while independent pairs
cluster at 0.54–0.62 and Plato|Aristotle sits at 0.6160, the base rate.
→ **Does not separate.** Designed configurations have high *variance* in pairwise
similarity, not a characteristic level. Suggestive and unused.

**T6 — Effective rank / span of deviations.** Kierkegaard 0.895, Josephus 0.952,
Plato-4-groups 0.839, Greek-4-independent 0.932, Plato+Aristotle 0.820.
→ **Does not separate.** All within 0.82–0.95.

**T7 — Aristotle's attribution practice.** Across 48 works, unnamed attribution
(τινές, φασί, λέγεται, οἱ μέν…οἱ δέ) runs **3.83 per named predecessor**; in the
*Metaphysics* alone **4.48**, with λέγεται at 309. The systematizing position
doing the doxography that grounds most of what we think we know about who held
what attributes anonymously four times for every naming.
→ Measured, never used. Relevant to any argument about how attribution behaves
inside the corpus.

**T8 — Folding / uptake retention.** Source-vocabulary retention when one text is
folded into another: Sappho 31 → Longinus **100%** (the seat states Longinus is
the sole direct carrier); LXX Pentateuch → Philo **76%**; LXX → Josephus *AJ*
**44%**; Plato → Aristotle *Metaphysics* **33%**; Plato → Xenophon **0%**.
→ Interesting and unfinished. Ezekiel/Daniel → Revelation failed on a filename
glob and was never rerun.

## 12. DOCUMENTARY FINDINGS (non-stylometric, and they hold)

**T9 — Authorial identity was obscurable in this exact period and circle.**
Aristophanes produced his first three plays under other men's names — *Banqueters*
(427), *Babylonians* (426), *Acharnians* (425), all διὰ Καλλιστράτου — describes
the practice himself at *Wasps* 1017–22, and continued it after he had a name
(*Lysistrata* 411 via Callistratus, *Frogs* 405 via Philonides). The civic
didascalic record carries the **producer, not the poet**. Cleon's prosecution over
the *Babylonians* cannot be resolved as against Aristophanes or Callistratus.
Biographical facts about "Aristophanes" — baldness, the Aegina connection — are
extracted from plays whose named author may be a different man.

**T10 — Base rate around T9.** Ps.-Xenophon's *Athenaion Politeia* sat in
Xenophon's corpus from antiquity, questioned by Demetrius of Magnesia but quoted
as Xenophon by Stobaeus, author never identified. The Hippocratic corpus: ~60
treatises under one name, multiple hands, this exact window.

**T11 — The Aristotelian corpus boundary is an inference.** Andronicus of Rhodes
constituted it in the 1st c. BCE, ~250 years after, working from the
cross-references the texts themselves contain plus school documents. His catalogue
is not extant. **He judged *De interpretatione* spurious**; the field now receives
it as genuine. *Metaphysics* A's authenticity was questioned in Alexander's time,
with Asclepius reporting attribution by some to Pasicles of Rhodes — and A is the
book the paper's worked case is built on.

**T12 — The recursion.** The Athenian didascalic records descend from Aristotle's
lost *Didascaliae*. The one surviving contemporary inscription naming a principal
(FD III 1, 400, *ante* 329) crowns Aristotle and Callisthenes **for compiling the
register of Pythian victors**. The compiler of the record that assigns plays to
authors is the figure whose own corpus's partition is in question, and that record
by convention sometimes names the producer instead of the poet.

## 13. CORPUS AVAILABILITY — what exists, what does not, and how retrieval fails

**T13a — RESOLVED 2026-08-29.** Herodotus and Thucydides, listed as unseated
dependencies in the first version of this register, are now seated as
EA-CORPORA-07/01 and 07/02 (deposit #1563). The empirical null's seventeen units
from these authors now rest on archive-held, commit-pinned material rather than a
census checkout.

**T13 — Unavailable at any pin.** Iamblichus and Damascius: absent from
canonical-greekLit and First1KGreek under every author string. Prior attempts
failed for this reason, not for want of searching.

**T14 — Kierkegaard's *Samlede Værker* is unusable.** All 25 volumes are on
archive.org, unrestricted, with full text — and the OCR has failed completely
because the editions are **Fraktur**. Danish common-word rate 0.13–0.14 uniformly
across sampled segments, against 0.28 for genuine Danish. 0/12 clean segments in
either volume tested. A naive quality gate at 0.10 passes them; it must not be.
→ **The seven missing pseudonyms** — Constantin Constantius, Vigilius Haufniensis,
both Climacus positions, Hilarius Bogbinder, Frater Taciturnus, Inter et Inter —
require a source outside reach (SKS at sks.dk, not allowlisted).

**T15 — Pessoa's minor heteronyms are unavailable.** pt.wikisource carries only
Caeiro, Reis, Campos and the orthonym. Bernardo Soares, Alexander Search, António
Mora, the Barão de Teive, Vicente Guedes: no categories, nothing usable on
archive.org.

**T16 — Two silent retrieval failures, both recorded in their seats.**
(a) The Wikisource **extracts** API returns *empty* bodies for short lyrics whose
text sits inside `<poem>` templates, while longer prose-poems extract normally —
so an extracts-based fetch yields Campos nearly complete and Caeiro and Reis
nearly empty, **and reports no error**. Raw wikitext via `prop=revisions` is
required.
(b) Danish Wikisource pages for *Enten–Eller* are **djvu transclusions**:
`prop=revisions` returns only a `<pages index=…>` stub, so a raw-wikitext fetch
yields nothing, **also with no error**. `action=parse` resolves them.

**T17 — A structural limit on the calibration set.** The two strongest NT criteria
— name-to-voice cardinality mismatch, and cross-name convergence exceeding
within-name — **require multiple positions under one declared name**. Pessoa and
Kierkegaard are one-name-one-voice by construction (the sole exception being
Victor Eremita carrying A and B). So those criteria **cannot be calibrated** on
the known-designed corpora. The corpora that have the structure are the New
Testament and, on the hypothesis, the Platonic corpus.

## 14. TRIED AND LEFT DANGLING

- **Xenophon seated** (EA-CORPORA-06/01) and used for M3, but the full
  genre-controlled instrument was never built on him.
- **The 4-fold leave-one-out on Pessoa.** M17 pools three heteronyms to recover
  the orthonym. The design calls for withholding *each* of the four in turn, so
  that recovery can be checked on voices nobody considers special. Three folds
  unrun.
- **Ezekiel/Daniel → Revelation folding retention** (T8) — failed on a glob,
  never rerun.
- **The 31-term class** (EA-SNUB-01 §13). Identified, never characterised. Do they
  share a semantic character — technical vocabulary Aristotle needed — or is the
  list arbitrary? συμβεβηκός (2× → 449×) suggests the former.
- **Republic 395a / Symposium 223d base rate** (EA-SNUB-01 §18). The single most
  important open item; see §10.1.

## 15. PROPOSED AND NEVER ATTEMPTED

- ~~**A recognition measure reading λόγος rather than ὕλη.**~~ **PROTOTYPE EXISTS
  (2026-08-29). See M29.** Three unprompted positives; diagnosticity unresolved.
- **Directionality.** Does any term run the other way — terminal Aristotelian
  position to technical Platonic use? Under the received chronology it cannot; on
  any reading that questions the chronology, the absence is a datum. The 31-term
  class supplies the denominator.
- **Authenticity within domain, inside Aristotle.** Holds subject constant to break
  the M11 confound. Power may not exist (6 spurious of 30).
- **External dating against stylistic position**, for M13's circularity.
- **Non-monotone / permuted alignment.** M23 tested order-preserving transforms
  only. A systematically reordered mapping would not register.
- **Alignment on a unit other than the token block** — syntactic shape, argument
  move, figure. The alignment scaffold accepts any unit and any similarity
  function; swapping the block-content vector is a small change.

## 16. THE STATE OF THE QUESTION, STATED FLATLY

Nothing measured marks the Plato–Aristotle pair as anomalous for two
contemporaneous authors. The declared partition is overwhelming (M6). The
standardised separation is on the *close* side (M5). One of five NT criteria holds
(M22), and it is the one not measurable from texts. No whole-text operator exists
(M23). The one ancient case with a checkable target reads negative (M16).

What was anomalous was **Aristotle's internal heterogeneity** (M10) — and as of
M28 it is not. Holding subject constant removes it: within-domain 0.0571 against
Plato's total 0.0570, and within ethics tighter than 99.5% of multi-author pools.
The heterogeneity is the object, which is a claim about method rather than about
hands. The authenticity signal remains confounded by the criteria that produced
the authenticity labels, and the corpus boundary remains an inference by an editor
whose judgments have been overturned (T11).

**With M28 the investigation had no standing statistical anomaly.** Every
substrate-reading lead was closed or explained.

**M30 reopened it, on a different axis.** The naming-gap reflex groups Plato and
Aristotle at 9.4× the rate of other high-division authors, P ≈ 0, and survives the
controls that killed everything else because it is a count of an arbitrary
procedural habit rather than a measure of similarity. Plotinus divides harder than
Aristotle and never does it; the multi-hand Hippocratic corpus does not do it at
all.

The standing position is therefore:

    substrate stylometry           no anomaly; the pair is ordinary or close
    Aristotle's heterogeneity      explained — it is the object (M28)
    whole-text transform           negative (M23)
    MECHANISM                      NEGATIVE — Plato's constructed Aristophanes
                                   ranks 5 of 7 against the real one (M16)
    procedural reflex              POSITIVE — 10.5x at work level, p = 0.0007;
                                   diagnosticity UNDECIDABLE-PENDING, not merely
                                   blocked — no admissible control exists, since
                                   any corpus performing the operation is
                                   Academy-descended (M30, M36)
    forgery/legitimacy census      ψευδεπίγραφος and προσωπεῖον BOTH ZERO in
                                   every seated corpus; the frame is kinship and
                                   standing, not inscription (M35)
    lexical exclusion              POSITIVE — Socrates 0/144 against Callias
                                   5/35 in snub contexts, p = 0.00022 (M34)
    philological                   M26, M31, M32, and the Republic/Symposium pair

And the reflex's diagnosticity is unresolved for one reason: **a school transmits
procedures**, and the successor control that would separate personal from Academic
transmission — Theophrastus dividing — is not extant in the available corpora.

**M16 belongs in this table and was previously buried.** Plato's constructed
Aristophanes ranks **5 of 7** Symposium speeches for resemblance to the real
Aristophanes, and sits at **0.0380** from the Plato corpus — *more* Platonic than
its neighbours. It is the only ancient case with an independently attested target,
and it is the direct test of the **mechanism** the unity hypothesis requires:
sustained voice separation across a large corpus. It reads negative. Continuity
(M30, M34) and capacity-for-separation (M16) are different claims, and the
investigation currently has positives on the first and a negative on the second.

The strongest unrefuted observation in the entire line of work is a philological
one: **the same formula, asserted and denied, on the exact question at issue,
with the affirming instance placed where its demonstration is destroyed in
transmission** (EA-SNUB-01 §16–18). It has not yet met a base rate.

---

## 17. M29 — THE PROCEDURAL INSTRUMENT

*Added 2026-08-29. Supersedes §15's "never attempted" entry for the λόγος measure.*

EA-SNUB-01 §6 derived a recognition criterion from the snub passage itself:
**matter individuates, form recurs, so what persists across substrates is the
account and not the instance.** §7 and §15 both listed a measure reading λόγος
rather than ὕλη as untouched and as the gap in the whole line of work.

It is no longer untouched. Three searches built in Rounds 4–7 of EA-SNUB-01 read
**operations** rather than substrate, and all three returned unprompted positives
in a session where every substrate-reading instrument returned null or artifact.

**The three hits.**

1. **Terminal aporia → technical uptake.** σιμόν at *Theaetetus* 209c, the failed
   individuating mark, becomes Aristotle's canonical case of enmattered form.
   Found by lexical search; the positional claim was refuted by base rate
   (EA-SNUB-01 §9), the semantic reading survives.

2. **Self-application regress.** *Soph. El.* 182a — if snub is concavity-of-nose
   and there is a snub nose, there is a concave-nose nose — returns *Parmenides*
   132a, the Third Man, by argument shape with **zero lexical overlap.** Found
   without being shown where to look.

3. **Divide, flag, coin.** Run a division far enough and you reach a class the
   language has no word for. Both corpora stop, say so, and coin a name.
   Platonic instances occur in exactly the four works that classify — *Sophist*
   (×3), *Statesman*, *Theaetetus*, *Timaeus* (×3) — and nowhere else in Plato.
   Aristotle states the policy outright at *NE* 1108a: πειρατέον αὐτοὺς
   ὀνοματοποιεῖν σαφηνείας ἕνεκα.

**Why it works where the others failed.** Method is what maintains its shape
across shifting matter. Every substrate instrument reads ὕλη — particles,
frequencies, blocks, register — and ὕλη is what individuates. The procedural
searches read the operation, which is what recurs.

**The problem, stated as strongly as it can be put against the instrument.**
Method is precisely what a school transmits. A student acquires his master's
procedures more reliably than his vocabulary, his register, or his opinions. So
procedural continuity is simultaneously the **most detectable** thing across the
boundary and the **least diagnostic** for authorship: its presence is predicted
equally well by ordinary teaching.

**The sharpening that would make it diagnostic.** Not whether both use division —
everyone in the Academy divided — but whether they share **arbitrary** features of
the method: reflexes not determined by the method's purpose. Nothing requires a
divider to stop and coin; leaving the class unnamed and proceeding is available
and costs nothing. Both stop. Both flag. Both coin.

**The test, and its denominator. RUN 2026-08-29 for reflex 3 — see M30.**
Plato and Aristotle share the naming-gap reflex at **9.4× the rate of other
high-division authors**, P ≈ 0, with Plotinus dividing harder than Aristotle and
never doing it, and the multi-hand Hippocratic corpus at zero. That is the first
positive result the investigation has produced. Reflexes 1 and 2 remain untested
against a denominator, and the decisive successor control (Theophrastus dividing)
is not extant in the available corpora.

---

## 18. M30 — THE NAMING-GAP REFLEX

*Added 2026-08-29. The first measurement in this investigation that groups Plato
and Aristotle rather than separating them. Partly answers M29's diagnosticity
question.*

**The reflex.** Run a division far enough and you reach a class the language has
no word for. Nothing about διαίρεσις requires you to stop and say so — leaving the
class unnamed costs nothing and proceeds. Plato and Aristotle both stop, both
flag it, and both coin. Aristotle writes the policy down at *NE* 1108a:
πειρατέον αὐτοὺς ὀνοματοποιεῖν σαφηνείας ἕνεκα — *we must coin names ourselves for
the sake of clarity.*

**Measured as instances per 100,000 tokens**, counting ἀνώνυμ-, οὐκ ἔχει ὄνομα,
οὐ κεῖται ὄνομα, οὐκ ὠνόμασται and cognates:

    corpus                    gap/100k    raw / tokens        division/10k
    ARISTOTLE                     8.43    81 /   960,910             30.9
    Diogenes Laertius             2.74     3 /   109,679             16.1
    PLATO                         2.60    15 /   576,894             15.4
    Herodotus                     2.16     4 /   184,935              3.7
    Aristophanes                  1.96     2 /   102,058              4.0
    Josephus                      0.64     3 /   467,569              5.4
    Plotinus                      0.47     1 /   214,028             36.8
    Philo                         0.35     2 /   575,592             13.3
    Xenophon                      0.32     1 /   310,278              1.7
    Thucydides                    0.00     0 /   150,157              1.2
    Hippocratic (multi-hand)      0.00     0 /    98,175              2.4
    Greek NT                      0.00     0 /   116,244              1.3

**The reflex is not a function of dividing.** Plotinus has the **highest division
density in the sample** — 36.8 against Aristotle's 30.9 — and one instance in
214,000 words. Philo divides at 13.3, comparable to Plato, and has two in 575,000.

**The test. ⚠ INFERENCE CORRECTED — the token-level p-value was indefensible.**

*Token level, descriptive only.* Restricting to authors dividing above 13 per 10⁴:

    Plato + Aristotle                       96 in 1,537,804  =  6.24 /100k
    Plotinus + Philo + Diogenes              6 in   899,299  =  0.67 /100k
    RATIO                                                        9.4x

The Poisson figure originally recorded here — P(X≥96 | λ=10.3) ≈ 0 — **is
withdrawn.** It treats 96 tokens as independent arrivals under one homogeneous
rate. They are not independent: they cluster by work (*NE* 11, *HA* 12, *Sophist*
3, *Timaeus* 3) and by construction. The effective experimental unit is the
**work**, not the token, and an infinitesimal p on clustered events gives a false
impression of replication.

*Work level, the honest unit.* A work counts once if it carries the reflex at all,
restricted as before to works dividing above 13 per 10⁴:

    Plato + Aristotle       16 of 32 works    50.0%
    Plotinus + Philo         1 of 21 works     4.8%
    RATIO                                      10.5x
    Fisher exact, two-sided                    p = 0.0007

**The effect survives the correct unit and the ratio is marginally larger.** The
defensible statement is *p = 0.0007 across 53 works*, not P ≈ 0. Per-corpus: Plato
4/9, Aristotle 12/23, Plotinus 1/6, **Philo 0/15**.

**Why this survives what killed everything else.**

- **Not a distance**, so register cannot mimic it. Plotinus and Philo write the
  same philosophical prose in the same tradition and do not do it.
- **Not the method**, since the two highest dividers in the sample sit at opposite
  ends of the measure.
- **Not generic to classification.** The Hippocratic corpus — thirteen works,
  multiple hands, classifying diseases — has **zero in 98,175 tokens.**
- **A count, not a similarity**, so none of the five broken nulls (§8) applies.

**What it does not show.** A school transmits reflexes, and an arbitrary
procedural habit is the most transmissible thing there is. This is consistent with
ordinary teaching and does not establish common authorship.

**The decisive control is missing.** Theophrastus — Aristotle's actual successor —
survives in the available corpora only as *Characters*, which does not divide.
Xenocrates and Speusippus are not extant. So whether the reflex is *personal* or
*Academic* cannot presently be determined, and that is the question that would
make it diagnostic.

**Status.** The first result in this investigation that distinguishes Plato and
Aristotle **jointly** from every available control, by a mechanism that is neither
register nor distance. Every other measurement either separated them or dissolved.
This one groups them, at **p = 0.0007 on 53 works**.

**Never to be quoted without the missing control. ⚠ AND THE CONTROL IS NOT
THEOPHRASTUS — see M36.** The claim recorded here, that Theophrastus survives only
as *Characters*, was **false and never searched**; the philosophical works were in
First1KGreek all along and are now seated. But when run, the result is **void as a
control result**: Theophrastus cannot be established outside the configuration
(M36), being defined by his relation to Aristotle, writing continuations of the
abandoned Aristotelian programme, and sharing a single transmission channel with
it. **M30's diagnosticity is not resolved by him and may be undecidable in
principle** (M36b). School transmission remains live; it has not been confirmed.

**Denominator, stated.** Of five Aristotelian snub-arguments given Platonic-vocabulary
signatures and searched (Notebook Part I, Round 4), **one mapped** — the
self-application regress. Of the procedural reflexes since pursued, three were
tested and three hit. The full inventory of candidate operations — elenchus,
doxography, myth-making, definition by genus and difference — has **not** been
built, and until it is, three-of-three is a numerator without its denominator.

---

## 19. M31 — αὐτεπιτακτική: the coined self-commanding position

*Added 2026-08-29. See EA-SNUB-01 §24–27 for the passage and its cautions.*

*Statesman* 260d–e, position 0.064 — one of the four Platonic works carrying the
M30 naming-gap reflex. The Eleatic Stranger enumerates the directive arts that
relay **ἀλλότρια νοήματα**, another's thoughts — ἑρμηνευτική, κελευστική, μαντική,
κηρυκική — finds that *σχεδὸν ἀνώνυμον ὂν τυγχάνει τὸ τῶν **αὐτεπιτακτῶν** γένος*,
and coins **αὐτεπιτακτική** for the position that issues from itself. The
remainder is dismissed with *ὄνομα ἕτερον αὐτοῖς παραχωρήσαντες θέσθαι τινά* — let
them set themselves some other name.

**Recorded as a fact about the corpus, not an inference about its authorship.**
The distinction between speaking from oneself and relaying another's mind was
available, named, and coined by Plato in the act of finding Greek short of a word
for it.

**⚠ CORRECTED same day.** The first version of this entry said Plato *assigns*
the coined art to kings, and that the class is political rule. That inverted the
containment. **τὸ μὲν τῶν βασιλέων γένος εἰς τὴν αὐτεπιτακτικὴν θέντες** — τίθημι
+ εἰς: kings are placed **into** the self-commanding, which is the container. And
at 267b: **ζῳοτροφικὴ δὲ πάλιν αὐτεπιτακτικῆς οὐ τὸ σμικρότατον τῶν γενῶν
ἀπεσχίζετο** — animal-rearing split off from the self-commanding, *not the
smallest of the genera*. **Other genera exist inside the class and Plato says so**,
declining them with τοῦ γὰρ ἄρχοντος ἕνεκα ἡμῖν ἡ μέθοδος ἦν — our method was for
the sake of the ruler.

**So the class is open by construction and marked as open.** The position that
speaks from itself is named, is explicitly larger than any of its instances, and
is abandoned mid-division with its remaining genera unentered.

**Standing caution, corrected.** Plato does not apply this to authorship, and the
unentered genera are unentered — supplying them is an inference the text does not
license. The ἑρμηνευ- link to *Περὶ ἑρμηνείας* remains a homonym; Aristotle's
sense is *expression*. Nothing is built on it.

---

## 20. M32 — κερματισμός and the two demands for recombination

*Added 2026-08-29. See EA-SNUB-01 §28–33.*

**κερματίζω**, to mint a unity into small change, is Plato's standing metaphor for
the one broken into many (*Meno* ×2, *Parmenides*, *Republic* 0.675, *Timaeus* ×3,
*Cratylus*). It is the **stated ground** of the denial at *Republic* 395b: *εἰς
σμικρότερα κατακεκερματίσθαι ἡ τοῦ ἀνθρώπου φύσις* — human nature is minted into
denominations too small to hold two arts. The incapacity is a fact about
fragmentation, not about poets.

    Symp 191d  0.366  one cut into two; each a σύμβολον; Eros makes ἓν ἐκ δυοῖν
                      and ἰάσασθαι τὴν φύσιν τὴν ἀνθρωπίνην
    Rep 395b   0.237  κατακεκερματίσθαι ἡ τοῦ ἀνθρώπου φύσις → οἱ αὐτοὶ οὐ δύνανται
    Rep 473d   0.509  εἰς ταὐτὸν συμπέσῃ, δύναμίς τε πολιτικὴ καὶ φιλοσοφία;
                      those travelling χωρὶς ἐφ᾽ ἑκάτερον excluded by necessity
    Symp 223d  0.996  τοῦ αὐτοῦ ἀνδρός — the same man must hold both arts

The lexical link between the first two is exact: *Republic* 395b says **ἡ τοῦ
ἀνθρώπου φύσις** is minted into pieces; *Symposium* 191d says Eros attempts
**ἰάσασθαι τὴν φύσιν τὴν ἀνθρωπίνην** by making one from two. Same subject,
opposite verbs.

*Republic* 473d demands the inverse of κερματισμός and is introduced as what will
drown its speaker in **γέλως** — in the book that has just ruled no one can hold
comedy and tragedy together.

**Not established:** that any of this concerns authorship. Both recombinations are
stated of their own subjects — political power and philosophy in a ruler, two
poetic arts in a maker. What the corpus supplies is the structure, not its
application.

---

## 21. EA-KERMA-01 — the reconstruction

*Added 2026-08-29. sha256 51be41d0b6ee194c7a65654f96387395…*

A separate document assembles the M32 loci into an argument and states where
heteronymy would sit in it. Recorded here as a pointer, not a finding.

**The move:** the σύμβολον is not a broken object but an object broken **by
agreement** — the break line is the credential, not the damage. Rubble cannot be
recognised; a token is recognised precisely at its fracture. So: *you cannot
un-cut human nature, you can cut it on purpose.* Heteronymy would convert
κερματισμός from a wound into a method — the fragmentation ratified rather than
reversed, and thereby made legible.

**Why it resolves 395b against 473d:** it accepts the denial as premise (no single
undivided nature holds two arts) and satisfies the requirement in a coordinated
multiplicity whose parts **sum rather than resemble**. ---

## 22. EA-PINAX-01 — the calibration-object hypothesis

*Added 2026-08-29. sha256 cb14e25a66fb30d36f6964b1e2c7721c… Pointer, not a finding.*

The standing objection was that antiquity built an authenticity apparatus and
would therefore have caught a construction. The hypothesis inverts it: **the
technology is the output.** Criteria must be fitted to a case whose answer is
known, and a deliberately structured corpus is a **calibration object** — the
*Pinakes* with incipit and stichometric checksum, the obelus, the
νόθος/ἀντιλεγόμενα vocabulary, and the practice of transmitting corpora **with**
their disputes are what working on one produces.

**It reframes two measured results.** M11's authenticity signal at Z = +3.47 was
flagged circular because Andronicus sorted partly by style; under this hypothesis
the circularity **is the datum**. And M30's naming-gap reflex reads as a
cataloguer's discipline rather than a school habit — an unnamed class is an
unshelvable class, and the *Poetics*' unnamed-genre problem is a cataloguer's
problem.

**Its danger is stated in the document, at length.** It explains everything,
including every null; both hypotheses predict the *Pinakes*. §4 exists so the
property cannot operate silently.

**The one asymmetric prediction:** an instrument built on a calibration object
**overfits it**. The registered test measures **the history of judgements, not the
texts** — verdict density, decisiveness (stated grounds), and reversal rate,
across the Platonic-Aristotelian, Hippocratic, Homeric, Pythagorean and Orphic
traditions. It counts verdicts rather than measuring similarity, so none of the
five broken nulls (§8) applies. Kill condition binding on decisiveness; void
condition if survival cannot be normalised against citation volume.

---

## 23. M34 — THE EXCLUDED TWIN

*Added 2026-08-29. The cleanest single measurement in this register: one name
against its own placeholder-twin, inside one corpus, needing no register control,
no genre matching and no constructed null.*

**The bearers of the snub in Aristotle**, counted across all 46 σιμ- tokens by
what stands within ±30 tokens:

    ῥίς      nose      102        ΚΑΛΛΙΑΣ            5
    σάρξ     flesh      14        ἄνθρωπος           4
    ὀφθαλμός eye         5        ζῷον, σκέλος     3, 3
    χαλκός, κύκλος    1, 1        **ΣΩΚΡΑΤΗΣ         0**

**Σωκράτης appears 144 times in Aristotle** — 45 of them in the *Metaphysics*,
the very work where the snub is defined five times — and **nine times paired with
Callias as the stock placeholder individual**: *οὐ γὰρ ἄνθρωπον ὑγιάζει ὁ
ἰατρεύων ἀλλὰ **Καλλίαν ἢ Σωκράτην*** (*Metaph.* 0.004); *ὁδὶ μὲν ὁ ἀριθμὸς
ἄνθρωπος, ὁδὶ δὲ **Σωκράτης**, ὁδὶ δὲ **Καλλίας*** (0.087).

**Zero within forty tokens of any σιμ-, anywhere in the corpus.**

**The base-rate test says nothing, and must be stated first.** Expected
Socrates-near-snub if the two were independent: 144 × 46 × 80 / 960,910 = **0.55**.
Observed 0. P(0 | Poisson 0.55) = **0.58**. On raw base rate the absence is
unremarkable, and a reviewer will reach for this first. Correctly.

**The right comparison is against his co-placeholder**, because Callias and
Socrates are the *same kind of item* in Aristotle's apparatus — the interchangeable
concrete individual, named together in the pattern *Καλλίαν ἢ Σωκράτην*:

    Callias  in snub contexts     5 / 35   = 14.3%
    Socrates in snub contexts     0 / 144  =  0.0%
    Fisher exact, two-sided                  p = 0.00022
    At Callias's rate, expected 20.6.  Observed 0.

**Both readings, and the innocent one is not weak.** Socrates already carries the
snub as a **biographical** fact, so using him would import unwanted associations
into a technical example; Aristotle picks the neutral twin *because* Socrates is
not neutral. That fully explains the distribution.

But it concedes the premise: **Socrates is the one individual whose snubness is
unavailable for use as a variable.** Everywhere else in Aristotle he is exactly a
variable — the man who is pale, or sick, or an instance of number — freely
interchangeable with Callias. At the snub, and only there, he stops being
substitutable. And the mark he cannot be substituted at is his own face.

**The Platonic side, for the record.** Plato's three snub instances are about
**naming**, not defining. *Theaetetus* 209c requires that this snubness, differing
from all others seen, *διάφορόν τι **μνημεῖον** παρ᾽ ἐμοὶ ἐνσημηναμένη καταθῆται* —
**deposit a memorial** in another mind — and it fails to. *Republic* 474d is a
renaming: the lover calls the snub one *ἐπίχαρις*, charming, and the hooked one
*βασιλικόν*, kingly. Plato names; Aristotle defines; and the bearer changes hands
between them.

**Status.** A measured, non-circular exclusion at p = 0.00022, with a sufficient
innocent explanation attached. Not evidence of design. It establishes only that
the corpus treats one individual's snubness as unusable where every comparable
individual's is usable.


---

## 24. M35 — THE FORGERY AND LEGITIMACY CENSUS

*Added 2026-08-29. Notebook Round 15 carries the passages; this is the lookup form.*

Full census of the authenticity families across both corpora:

    term                            PLATO   ARIST
    σύγγραμμα writing-as-thing         37       3
    εἴδωλον image                      72      13
    μίμημα copy                        54       7
    κίβδηλος counterfeit/debased       13       4
    δόκιμος assayed, approved          28      24
    ἀδόκιμος rejected in assay          3       2
    πλάσμα / πλαστός fabricated        16      32
    φάντασμα appearance                31      47
    ὑποκριτής actor                    10      32
    γνήσιος legitimate                 16       6
    νόθος bastard                      11       4
    παράσημος false-stamped             1       4
    ψευδεπίγραφος                       0       0
    προσωπεῖον mask                     0       0

**Two nulls.** ψευδεπίγραφος is **zero in every seated corpus** — Plato, Aristotle,
the nine orators, Philo, Josephus, the NT. There was no word for a falsely-titled
book. προσωπεῖον, the theatrical mask, is likewise **zero in both corpora** — the
mask is not their tool for authorial voice, which constrains any persona reading.

**The division of labour — ⚠ SUGGESTIVE, NOT MEASURED.** Plato leans to the
**image** vocabulary (εἴδωλον, μίμημα, σύγγραμμα); Aristotle to the **detection**
vocabulary (πλάσμα, φάντασμα, ὑποκριτής); δόκιμος is shared at 28/24. **These are
raw counts.** Establishing a division of labour as a quantitative result requires
semantic disambiguation of each family, normalisation, a frozen vocabulary set
fixed before counting, and comparison corpora. **None of that has been done**, and
the phrase "division of labour" is used descriptively here, not as a finding.

**The frame is kinship, not inscription.** In Isaeus — γνήσιος at **23.72/10k**,
the densest in the sample — legitimacy is litigated by μαρτυρ- (279), ἐγγύη (91),
εἰσάγω (45) and φράτηρ (35), with **zero** blood-vocabulary. A νόθος can be the
father's certain child. **Legitimacy is standing, not paternity**, and it is
re-litigable on testimony. Applied to texts, the ancient mechanisms were asking
*does this work have standing in the corpus*, not *whose hand wrote it*.

**M35a — the coin runs continuous.** *Rep.* 395b: κατακεκερματίσθαι sits four
lines from μιμήματα — nature minted into denominations too small to imitate many
things well. *Rep.* 507a: εὐλαβεῖσθε … **κίβδηλον ἀποδιδοὺς τὸν λόγον** τοῦ τόκου
— the account handed over may be debased coin, with τόκος and ἔκγονον joining coin
to kinship in one clause. *Laws* 742a: currency **ἔντιμον** to citizens,
**ἀδόκιμον** to everyone else — standing-not-paternity, in coin.

**M35b — *NE* 1165a.** δίκαιον ἐγκαλεῖν τῷ ἀπατήσαντι, **καὶ μᾶλλον ἢ τοῖς τὸ
νόμισμα κιβδηλεύουσιν, ὅσῳ περὶ τιμιώτερον ἡ κακουργία** — Aristotle grades false
personation **above** coin-forgery on one scale.

**M35c — orator control.** The orators are professionally fluent in forgery
(πλάσμα, πλαστόν, σκευώρημα, of opponents' documents) and **say nothing about the
standing of the speech being read**: σύγγραμμα is **zero in seven of nine**, the
exception being Isocrates, who wrote for readers.

---

## 25. M36 — THE THEOPHRASTUS RESULT IS VOID AS A CONTROL

*Added 2026-08-29. Supersedes the same-day claim that school transmission was
confirmed.*

**The blocker was false.** M30's diagnosticity was recorded three times as blocked
because Theophrastus "survives only as *Characters*." **That was an assumption,
never a search.** First1KGreek was checked out locally all day and contains
*Historia Plantarum*, *De causis plantarum*, *De sensibus*, *De igne* and the
*Metaphysica* — now seated as EA-CORPORA-09/01, 15 works, 208,324 tokens.

**The numbers.** Theophrastus 5.43/100k; high-division works carrying the reflex
2/5 = 0.400 against Plato+Aristotle 16/32 = 0.500; **Fisher exact p = 1.0000**.
*Historia Plantarum* alone carries nine instances at division 29.9/10k.

**⚠ AND THE RESULT IS VOID AS A CONTROL RESULT.** On seeing it I reported that
school transmission was confirmed. That was **inherited inference, not
measurement**, and it violates M33 — I used a figure as a control without first
asking whether he can be inside the configuration.

**Theophrastus is the Chaerephon shape.** The Chaerephon problem, as recorded in
the Aristophanes seat: the Suda's entry on Chaerephon is sourced from the scholia
to *Clouds* 144 — **the biographical record is downstream of the text it is meant
to attest.** Theophrastus is defined by his relation to Aristotle (successor as
scholarch, heir to the library and manuscripts by Aristotle's will), and his major
works are **continuations** — *HP* extending *HA*, *De causis* extending the causal
analysis, his *Metaphysica* a fragment picking up where the aporiai stop. That is
the profile of **another completed abandonment**, which is what EA-COMPLETE-01
exists to detect. And the Aristotelian corpus reaches us **through Theophrastus's
library** — Neleus, Scepsis, Apellicon, Sulla, Andronicus — so the two texts share
one transmission channel and their agreement in editorial habit is not independent.

**Seat stands as a corpus. ⚠ CORRECTED PHRASING: the measurement stands; its use
as an authorship discriminator is void.** Conditional on the received succession
account, Theophrastus's hit is evidence that **this procedural reflex can propagate
down an intellectual lineage** — which matters to H_S even though it does not
separate H_S from H_H.

**M36a — the control criterion, stated.** A control must be **impossible to be
inside the configuration**, which requires either (i) **no causal contact** — a
corpus that could not have received the method — or (ii) **independent attestation
of the author's existence** by sources outside the configuration.
  → ⚠ **See M39.** I stated criterion (ii) and did not notice that exactly one
    member of the candidate cluster satisfies it: **Aristotle**, by FD III 1, 400.
    Socrates, Plato and Aristophanes do not. Theophrastus
fails both. Demosthenes passes (ii) via inscriptions and decrees. **The Hippocratic
corpus passes (i)** — largely pre-Platonic, Coan and Cnidian, medical rather than
Academic — and stands at **0 of 15**, the one control nobody can absorb.

**M36b — the reflex is not identifiable from presently available within-tradition
controls.** *(Originally written "undecidable in principle" — too strong, corrected.
"In principle" would require excluding external, cross-cultural, documentary and
later known-author calibration routes as well, which has not been done.)* The operation requires
division, and in Greek prose division is Academy-descended. **Any corpus that
performs the operation is downstream; any corpus that is not downstream does not
perform it.** If that holds, M30's diagnosticity is not merely blocked pending a
corpus — it is undecidable, which is what EA-UNRES-01 predicts an engineered
object produces. Recorded as a conjecture requiring its own test, not as a result.


---

## 26. M37 — COMPLEMENTARITY: THE MEASURE FAILS ON VOCABULARY AND THE OBJECT IS LEVEL-DEPENDENT

*Added 2026-08-29. Records a proposed discriminator, its failure at the level
first tried, and what the existing data already says at the level that works.*

**The proposal.** Inheritance should produce **redundancy** — the student
possesses what the teacher taught, so overlap is high and the union barely exceeds
either part. Deliberate partition should produce the opposite: small intersection,
union far more complete than either part. Formally, coverage of the union over
redundancy between the parts.

**It fails on content vocabulary.** Top-1500 content words, redundancy =
|A∩B|/|A∪B|, union gain = |A∪B|/max(|A|,|B|):

    pair                                    redund   union gain
    PLATO | ARISTOTLE                        0.340       1.493
    Isaeus | Demosthenes  (succession)       0.310       1.527
    Herodotus | Thucydides (independent)     0.198       1.669
    Aristotle | Theophrastus                 0.323       1.511
    Plato | Xenophon                         0.302       1.537
    Philo | Plotinus (independent)           0.296       1.543

Everything lies in 0.20–0.34. **Documented succession and documented independence
are indistinguishable**, and Plato–Aristotle is the *most redundant* pair in the
set — the opposite of the partition prediction. Content vocabulary tracks shared
subject matter, so the measure reads topic overlap and nothing else.
**Do not rebuild it at this level.**

**And the object is level-dependent, which is the finding.**

**At the slot level the pair is REDUNDANT.** Each fills 6 of 6 (Round 12). Union
gain 1.0. That is inheritance behaviour. The Johannine group is the one that
partitions — six slots across three books, **no slot doubled**, union gain 3.0
over its parts.

**At the execution level within a shared function they are COMPLEMENTARY** (M35):

    εἴδωλον 72/13 · μίμημα 54/7 · σύγγραμμα 37/3      ← Plato: representation
    πλάσμα 16/32 · φάντασμα 31/47 · ὑποκριτής 10/32   ← Aristotle: detection
    δόκιμος 28/24                                      ← shared: the assay

**Statement of the object, at the size the evidence carries:** *redundant in which
functions they perform, complementary in how they execute them.* Both cover the
whole apparatus; each holds a different end of the operation. That is **not**
tiling and is a different signature from the Johannine partition. It needs its own
specification before it gets a measurement, and no measurement of it is registered
here.

**M37a — Theophrastus was never logically decisive.** M30's "decisive successor
control" language overstated what any such control could do, independently of
M36's exteriority problem. A hit is explained by school transmission **and** by an
extended configuration — if one configuration were demonstrated, the prior on
further differentiated positions rises. A miss is explained by four ordinary
considerations: students need not inherit every reflex; doctrine can transmit
without craft; genre can suppress; the surviving Theophrastean material may sample
the wrong register. **Neither outcome discriminates.** The language is corrected.

**M37b — the design that replaces it.** Fix labels **outside** the phenomenon
under measurement. An externally secured **different-person** control requires
evidence not derived from style, doctrine, literary tradition or attribution
history — autographs, independently dated correspondence, documentary provenance.
An externally secured **one-person/many-voice** control requires the heteronymic
relation to be documented rather than inferred, which is why Pessoa is valuable.
Then the ancient objects — Plato, Aristotle, Xenophon, Aristophanes, Theophrastus
— enter **unlabelled**, and the question becomes a classification with the labels
fixed elsewhere. This moves the methodological problem out of the corpus instead
of shifting the arbitrary boundary one name outward.

**M37c — the inferential standard.** No single observation need distinguish school
from configuration; that standard is too strong for historical inquiry. The
contest is comparative likelihood over a **bundle**: substrate divergence,
functional tiling, arbitrary procedural reflex, negative exclusion (M34),
completion structure, the counterfeit/personation apparatus (M35), authorial
self-erasure. School transmission may accommodate each item singly. **The question
is whether it predicts their joint configuration**, and how many auxiliary
assumptions it accumulates in doing so — against a heteronymic hypothesis carrying
an enormous prior penalty that must be earned by **compression**: does one latent
configuration explain many otherwise independent peculiarities with fewer
auxiliary assumptions?


---

## 27. M38 — THE AUXILIARY LEDGER: CHARGING BOTH MODELS

*Added 2026-08-29. Methodological standing, extending M37c. The contribution is
not a measurement; it is an accounting rule that the investigation has been
applying asymmetrically, by me, all day.*

**The asymmetry, stated.** Inheritance has been permitted to be a very
high-capacity explanation; unity has not. Every structure this investigation found
was absorbed by the received model **and the absorption was never charged**:

    same arbitrary procedural reflex        → school habit
    same six-slot functional architecture   → inherited programme
    Plato abandons, Aristotle completes     → student solves master's problem
    Aristotle catalogues Plato's method     → student catalogues master's errors
      as definitional fault (Topica ×4)
    complementary vocabulary and roles      → specialisation
    substrate separation at Z = +39.18      → genre, register, object

Each is a good explanation. **Several are almost certainly true.** But the model
being invoked is no longer P → A. It is P → A *plus* a selective-transmission
account in which the student retains some arbitrary reflexes and not others,
radically changes substrate, picks up specifically **abandoned** rather than
developed problems, completes them with apparatus the master lacked, preserves the
master's figure while completing what it failed at, distributes rather than
repeats functions, and negates inherited formulations while preserving the
operations beneath them.

**⚠ THE ORIGINAL LEDGER WAS WRONG IN TWO WAYS AND IS REBUILT BELOW.** It listed
ten items as ten independent auxiliaries, when several flow from one latent
assumption; and it charged only H_S, which is the same asymmetry this entry exists
to correct, merely reversed.

**REBUILT — grouped by the smallest latent assumption that generates each set.**

**H_S — inheritance. Latent assumptions, not observation-counts:**

    L1  Aristotle is an unusually close successor systematically working through
        UNRESOLVED Platonic problems.
        → generates: the abandoned-execution selection, completion by apparatus
          the master lacked, retention of the master's figure at its failure
          point, and the six-slot co-filling.   [was A3, A4, A5, A8]

    L2  Arbitrary procedural habits transmit within a school alongside method.
        → generates: the naming-gap reflex (M30).   [was A1]
        → SUPPORTED: Theophrastus carries it (M36), which is direct evidence for
          L2 conditional on the received succession.

    L3  Register and object diverge sharply between dialogue and treatise.
        → generates: the Z = +39.18 partition, and much of the vocabulary split.
          [was A2, part of A6]

    L4  A successor specialises where the master did not.
        → generates: the representation/detection lean (M35).   [was A6]

    L5  Local causes, individually unexplained by L1–L4.
        → the Socrates/Callias exclusion at p = 0.00022 (M34); Phaedo 59b; the
          authorship denial at Letter II 314c.   [was A7, A9, A10]

**Five latent assumptions, not ten auxiliaries.** L1–L4 are ordinary and L2 now
has direct support. **L5 is where H_S is genuinely paying**, and it is the honest
locus of the dispute.

**H_H — configuration. Its own ledger, which must be equally ugly:**

    K1  Chronology. The received dating must be wrong or the corpus's composition
        order must differ from its attributed order.
    K2  A historical-person architecture. What the attested Aristotle IS relative
        to the authorial position — patron, writer, appropriated name, occupied
        role — must be specified, and is not.
    K3  Why externally transmitted biographical distinctions exist at all, and in
        the detail they do.
    K4  Why expected signatures are ABSENT: no προσωπεῖον vocabulary (M35), no
        ψευδεπίγραφος, and M16's Aristophanes result requiring reinterpretation
        rather than prediction.
    K5  The documentary machinery required to sustain the partition across
        centuries of transmission, cataloguing and athetesis.

**Neither ledger is short. That is the point.** The contest is which set of latent
assumptions is smaller and less tailored — **not** which model can accommodate the
observations, since both can.

**M38a — the null's kill condition is missing, and this is the real defect.**
This investigation has pre-registered kill conditions for the heteronymic reading
repeatedly, and they have fired: EA-LEAK-DEFICIT-01 spent, -02 void, EA-YIELD-01
spent, M30's Poisson withdrawn, the snub position refuted, *Poetics* namelessness
refuted, my own completion verdict reversed twice. **The ledger is built so failed
predictions stay attached.**

**No equivalent has ever been demanded of the received model.** So it must be
asked directly:

> **What observation would make "Plato influenced Aristotle" insufficient?**

And the worrying property is that the received model assimilates all four
directions of evidence without adjustment:

    different style        → different authors
    same method            → teacher transmitted it
    contradiction          → the student rejected the master
    continuity beneath     → the student developed the master
      the contradiction

Difference, similarity, contradiction and continuity are all absorbed. That does
not make the model false — a mature historical model should explain many kinds of
evidence — but a hypothesis that no configuration of evidence can strain has
stopped discriminating and become **the grammar in which results are narrated.**

**I do not currently have a kill condition for H_S**, and I could not construct
one when I tried: the best candidate — that Aristotle faults Plato for coining
(*Topica*) while stating coining as his own policy (*NE* 1108a) — is absorbed by
both models. That absence is recorded as a defect of the investigation, not
resolved.

**M38b — the correct contest.** Not *can inheritance tell some story about E?* —
it can, and elastic hypotheses always can. The contest is:

    P(E | H_S)  versus  P(E | H_H)

with the likelihood under H_S **not** assessable by inventing the best inheritance
story after seeing each datum, since that is P(E | H_S, A₁…Aₙ) with every Aᵢ
tailored to its observation. **The auxiliaries must be charged.**

And H_H is charged in the opposite direction: an enormous prior penalty, because
the record presents Socrates, Plato and Aristotle as distinct persons in
succession. It can only earn that penalty by **compression** — one latent
configuration making many otherwise independent peculiarities consequences of a
single construction.

    H_S :  historical prior advantage, auxiliary-expensive
    H_H :  prior-expensive, compression advantage

**The question the paper has to answer is which model makes the observed total
architecture less surprising after both are charged for everything they assume** —
and specifically why two extraordinarily well-separated textual containers behave
as unusually complementary machinery. *Teacher and student* is an answer to that.
It is not automatically a complete one.

**Status.** An accounting rule, not a result. Recorded because the investigation
applied the asymmetry silently toward the received model for most of the day —
**and then, on correcting it, began applying the mirror-image asymmetry toward the
configurational reading** (see M39, M40b, M40c, all corrected). 

**The governing danger, stated as the rule this entry now enforces:** *do not cure
an unfalsifiably elastic H_S by making H_H equally elastic.* The required
architecture is: nothing simply assumed, nothing simply discarded, every datum
retains provenance, **both models pay for auxiliaries, and both models must be
capable of losing.**


---

## 28. M39 — THE CERTIFICATION ASYMMETRY: ARISTOTLE IS THE ONLY ANCHORED POSITION

*Added 2026-08-29. A correction to how M36a's own criterion was applied. I stated
the criterion and did not notice that exactly one figure in the candidate cluster
meets it.*

**M36a requires of a control: independent attestation of the author's existence by
sources outside the configuration.** Applied to the cluster itself:

    SOCRATES      wrote nothing. Attested through Plato, Xenophon and
                  Aristophanes — all three INSIDE the cluster (M33). The
                  Chaerephon problem in its purest form: the biographical record
                  is downstream of the texts it is meant to attest.
    PLATO         attested through his own corpus and the tradition that corpus
                  generated. Letter II 314c denies the corpus is his; Letter XIII
                  transmits its own athetesis. No external documentary anchor.
    ARISTOPHANES  produced under other men's names for a decade (T9); the civic
                  didascalic record carries the PRODUCER. Biographical facts are
                  extracted from plays whose named author may be another man.
    XENOPHON      held apart as a candidate position (M33).
    ─────────────────────────────────────────────────────────────────────────
    ARISTOTLE     **FD III 1, 400** (*ante* 329) — a contemporary Delphic decree
                  crowning Aristotle and Callisthenes. Epigraphic, non-literary,
                  outside the configuration. **Passes M36a.**

**⚠ CORRECTED. Established:** *Aristotle is presently the only candidate position
with an **identified** external epigraphic anchor.* The stronger form originally
written here — that he is the **only** member with such certification — is a
**negative documentary claim** (¬E_Socrates ∧ ¬E_Plato ∧ ¬E_Aristophanes ∧
¬E_Xenophon) requiring an exhaustive survey that **has not been performed**. ∃E_A is
established; the negations are not.

**And a second correction: the stone anchors the PERSON, not textual paternity.**
Aristotle existed ⇏ Aristotle authored the Aristotelica. Under any configurational
reading a real Aristotle could be patron, recipient, collaborator, appropriated
identity or named position. The inference from certification to authorship does not
run.

**This inverts the frame the investigation has been using.** Aristotle has been
treated throughout as the anomaly requiring explanation — the heterogeneous corpus
(M10, dissolved by M28), the excluded twin (M34), the completions (Round 13). He
is the **anchored** position. On any configurational reading he is the terminus:
the one member certified to have been a person.

**M39a — what the completions then say.** M35 established that ancient legitimacy
is **standing, not paternity** — conferred by acknowledgment and witness, and
re-litigable on testimony. Under that frame, completing what a predecessor left
undone is how an heir **takes the estate**. Aristotle finishing the abandoned wax
block with ἄνευ τῆς ὕλης, converting aporia into method, supplying the receiver's
physiology at *De mem.* 450a — each is a claim to standing over the corpus
completed. Not *I succeeded Plato* but *what Plato left undone is mine and I can
discharge it.*

**Methodologically, the completions assert that Aristotle is the authentic Plato.**

**M39b — and this does NOT discriminate.** A student who completes his master's
unfinished work is equally the legitimate heir, and both readings license the same
claim. This is M38's problem arriving in a new location, and it is recorded as
such rather than resolved.

**What is not symmetric between the readings is the anchoring.** Under inheritance
the certification is **incidental** — of course the latest of the three has the
best documentation; he was a court figure and a compiler of civic records. Under
the configurational reading it is **structural**: the certified position is the one
that must be real, and it is the position that ends holding everything.

**M39c — T12's recursion, sharpened.** The single external anchor in the entire
configuration is FD III 1, 400 — and it crowns Aristotle **for compiling the
register of Pythian victors**. The one contemporary document certifying the
existence of any figure in the cluster certifies **the man who built the
attribution apparatus**, for building it. The Athenian didascalic records descend
from his lost *Didascaliae*; that record by convention sometimes names the producer
rather than the poet (T9, T12).

**Status.** A documentary asymmetry, verified against the record, with its
non-discriminating character stated. It licenses no authorship conclusion. What it
changes is which position the investigation should treat as given: **not Plato,
whose corpus denies its own authorship in his name, but Aristotle, who has a
stone.**


---

## 29. M40 — THE SUPPRESSED PREMISE: A META-PERFORMATIVE PRIORITY CLAIM

*Rewritten 2026-08-29 after the earlier version was twice wrong — first for
psychological framing, then for a lexical test that got the answer backwards. This
is the entryway to the paper and is treated at full weight.*

## 29.1 The three texts

**(i) Plato names the apparatus as a method, in his own voice.**
*Phaedrus* 266b:

> τούτων δὴ ἔγωγε αὐτός τε **ἐραστής**, ὦ Φαῖδρε, **τῶν διαιρέσεων καὶ συναγωγῶν**,
> **ἵνα οἷός τε ὦ λέγειν τε καὶ φρονεῖν**

*Of these I am myself a lover, Phaedrus — of the **divisions and collections** —
**in order to be able to speak and to think**.*

Not a one-off argument. A named procedure, held as such, **for the sake of a
capacity**. And *Meno* 86e names a second: *συγχώρησον **ἐξ ὑποθέσεως** αὐτὸ
σκοπεῖσθαι … **ὥσπερ οἱ γεωμέτραι*** — investigation from a hypothesis, on the
geometers' model. To which the *Parmenides* adds the third: the exhaustive
derivation of consequences from *εἰ ἓν ἔστιν* and *εἰ ἓν μὴ ἔστιν*.

**(ii) Aristotle classifies that apparatus as syllogistic.**
*Prior Analytics* I.31, 46a31:

> ὅτι δ᾽ ἡ διὰ τῶν γενῶν **διαίρεσις μικρόν τι μόριόν ἐστι τῆς εἰρημένης μεθόδου**,
> ῥᾴδιον ἰδεῖν· **ἔστι γὰρ ἡ διαίρεσις οἷον ἀσθενὴς συλλογισμός**· ὃ μὲν γὰρ δεῖ
> δεῖξαι **αἰτεῖται**, συλλογίζεται δ᾽ ἀεί τι τῶν ἄνωθεν.

*Division through genera is **a small part of the method described**; for division
is **a kind of weak syllogism** — it begs what it must prove, and always deduces
something from higher up.*

This is the load-bearing sentence. Aristotle does not place Platonic division
*outside* his subject as a different sort of thing. He places it **inside**:
*μόριον τῆς εἰρημένης μεθόδου*, a part of the stated method, and *συλλογισμός* by
species — defective, question-begging, but of the kind.

**(iii) Aristotle denies that the apparatus had any predecessor.**
*Sophistici Elenchi* 183b–184b. He first defines what ordinary development looks
like, by name and by lineage:

> οἱ δὲ νῦν εὐδοκιμοῦντες παραλαβόντες παρὰ πολλῶν **οἷον ἐκ διαδοχῆς** κατὰ μέρος
> προαγαγόντων οὕτως ηὐξήκασι, **Τισίας** μὲν μετὰ τοὺς πρώτους, **Θρασύμαχος** δὲ
> μετὰ Τισίαν, **Θεόδωρος** δὲ μετὰ τοῦτον

and then denies it of his own:

> ταύτης δὲ τῆς πραγματείας **οὐ τὸ μὲν ἦν τὸ δ᾽ οὐκ ἦν προεξειργασμένον, ἀλλ᾽
> οὐδὲν παντελῶς ὑπῆρχεν** … περὶ δὲ τοῦ συλλογίζεσθαι **παντελῶς οὐδὲν εἴχομεν
> πρότερον ἄλλο λέγειν**

*Not that part was worked out and part was not — **there was absolutely nothing.***

## 29.1b The instruction to supply what is left out — *APr* I.32, verified

Immediately after the division chapter, Aristotle turns to reducing arguments to
the figures, and instructs the analyst:

> καὶ εἰ μὴ ἄμφω εἰλημμέναι εἶεν, **αὐτὸν τιθέντα τὴν ἑτέραν** … ἢ ταύτας μὲν
> προτείνουσι, **δι᾽ ὧν δ᾽ αὗται περαίνονται, παραλείπουσιν** … σκεπτέον οὖν εἴ τι
> περίεργον εἴληπται καί **τι τῶν ἀναγκαίων παραλέλειπται**, καὶ τὸ μὲν θετέον τὸ
> δ᾽ ἀφαιρετέον

*If both premises have not been taken, **the analyst must himself supply the
other** … sometimes they propose these but **omit those through which these are
concluded** … examine whether something superfluous has been taken and **whether
something necessary has been left out**, and add the one and remove the other.*

**The lexical link is exact.** παραλέλειπται here; and the *Sophistici Elenchi*
closes by asking pardon **τοῖς παραλελειμμένοις** — for what has been left out.
Same verb, same participle: the chapter that teaches the reader to supply the
omitted premise, and the treatise-group that ends by asking indulgence for an
omission.

**Also in I.31, and sharper than the "weak syllogism" line:**

> **οὔτε ὅ τι ἐνδέχεται συλλογίσασθαι διαιρούμενοι ξυνίεσαν**

*They did not understand **what can be syllogized by dividing**.* Not that they had
no syllogistic — that they **had one and did not understand what it could
conclude**. A diagnosis of defective execution of an existing apparatus.

## 29.2 The contradiction, in Aristotle's own terms

    APr I.31    Platonic division IS a syllogism, and a part of the method
    Phaedrus    division IS Plato's stated method, held for the sake of a capacity
    SE 184b     of this method, nothing whatever existed before

**The usual escape is not available, and the reason is a point about charity.**

One would ordinarily say Aristotle means the *formal system* only — reading *ταύτης
δὲ τῆς πραγματείας … οὐδὲν παντελῶς ὑπῆρχεν* as *of **this systematic treatment**
nothing existed*, so that Platonic division falls outside the scope of the denial.
The grammar permits it. **⚠ I first recorded that as a defensible alternative and
withdraw it here, on the following ground.**

Consider what the narrow reading attributes to him. He has written that division
**is** a syllogism, that it is a **part of the method described**, and that its
practitioners **did not understand what can be syllogized by dividing** — three
statements that place the Platonic apparatus inside his subject and concede that
there is something there to reason with. The narrow reading then has him close the
treatise-group by declaring that nothing existed, rescued only by taking
*πραγματεία* in a sense that excludes what he has just included.

**That is an equivocation on his own technical term at the one point where his
standing depends on it** — committed by the author of the *Sophistici Elenchi*, in
the closing paragraph of the *Sophistici Elenchi*, in the corpus that gives us
ὁμωνυμία and catalogues the fallacies of ambiguity. It convicts him of precisely
the fault his book exists to expose, in order to preserve a chronology he never
asserts.

**Charity runs the other way.** Take him to mean what he says, in one consistent
technical sense, in both places. Then he neither contradicts himself nor equivocates:
he states two things that are jointly true only if the Platonic apparatus is not
prior to him in the relevant sense, and — one chapter after diagnosing division —
instructs the reader to **supply what has been left out**.

**The softer reading is not the more generous one. It is a milder accusation**
(sloppiness rather than a claim), purchased by protecting the received chronology.
Holding him to his own terms lets the chronology take the strain instead, which is
what the argument does.

## 29.3 Why this is a syllogism and not a complaint

The passage does not assert the contradiction. It **supplies two premises and
withholds the third**, and the third is the Platonic corpus:

    1.  If an apparatus existed in a predecessor, mine arose by succession.   [SE]
    2.  Mine did not arise by succession: nothing whatever existed before.    [SE]
    3.  Plato contains a prior apparatus — and I have classified it as
        syllogistic.                                              [APr, UNSPOKEN
                                                                   AT SE]
    ∴   Plato does not occupy the predecessor relation.

**Premise 3 is deliberately not spoken in the passage.** The reader must supply
it, from a corpus he already possesses. That makes the passage an **enthymeme
whose suppressed premise is an authorial corpus.**

And the recursion is exact: *the claim that syllogistic had no predecessor is
intelligible only by syllogistically processing its predecessor.* The instrument
required to detect the contradiction is the instrument whose invention is being
claimed. Aristotle closes by asking the audience to judge — *τοῖς δ᾽ εὑρημένοις
πολλὴν ἔχειν χάριν*, give much gratitude for **what has been found** — while
excusing *τοῖς παραλελειμμένοις*, **what has been left out**. What a syllogism
teaches a reader to recover is precisely the premise left out.

## 29.4 What the structure does that a declaration could not

Had Aristotle written *Plato's logical work is mine*, that would be a declaration
— forgeable, deniable, dismissible, and destructive of the construction it
declares.

Instead the claim is encoded **in the very technology whose invention it asserts**.
To receive it, a reader must know how to operate the thing. So:

> **the ownership claim, if it is one, is authenticated by performance rather than
> by declaration.**

That fits the standing frame exactly (M35): legitimacy is conferred by
acknowledgment and established by what can be executed, not by an external token —
and M35b records Aristotle grading **personation above coin-forgery** on one scale.
An assay that must be performed cannot be counterfeited by assertion.

## 29.5 The operation crosses the authorial boundary

Neither corpus contains the complete argument.

    PLATO      supplies the apparatus — the suppressed premise
    ARISTOTLE  supplies the classification of it as syllogism, and the denial
    THE READER supplies the inference

Three positions: **premise → inferential apparatus → recognition** — and the
recognition is about the relation between the positions that supplied the first
two. This is the functional interlock of Round 12 appearing in a single argument
rather than across a slot table, and it is the sharpest instance of it recorded.

## 29.6 What is established and what is interpretation

**ESTABLISHED, documentary:**
- Plato names divisions-and-collections as a method held for a capacity, and the
  hypothetical method on the geometers' model.
- Aristotle classifies division as *οἷον ἀσθενὴς συλλογισμός* and as *μόριον τῆς
  εἰρημένης μεθόδου*.
- Aristotle states that for this subject *οὐδὲν παντελῶς ὑπῆρχεν*, in explicit
  contrast to a named succession he supplies as the comparison case.
- Therefore: **Aristotle's priority claim places the Platonic apparatus on his side
  of the "before me" boundary.**

**INTERPRETATION:** the heteronymic reading resolves that placement literally —
the Platonic apparatus is not "before Aristotle" because it belongs to the same
maker.

**ALTERNATIVES that must be charged as auxiliaries, not assumed:**
*(a)* Aristotle is inconsistent across works, denying at *SE* what he grants at
*APr*. *(b)* He means the formal system narrowly and speaks loosely — foreclosed
by *μόριον τῆς εἰρημένης μεθόδου*, which places division inside the method.
*(c)* Priority rhetoric is conventional — but the passage supplies the succession
counter-case itself, by name and lineage, which conventional boasting does not do.

**What it is not:** psychology, estate metaphor, or biographical resentment. The
earlier versions of this entry contained all three and they are withdrawn. This
version rests on three quotations and one classification.

## 29.7 ⚠ THE TEST I RAN THAT WAS WORTHLESS

Asked whether Plato has an apparatus Aristotle's sentence ranges over, I froze
five criteria and searched for **the lexeme συλλογ-**. Result: 51 tokens in Plato,
of which **34 are σύλλογος/συλλογή — assembly, gathering, meeting**; συλλογισμός
appears **twice**. I reported that Plato "scores weakly," that the minor premise
failed, and that the priority claim was ordinary and true.

**That was the fourth substitution of vocabulary for substance in one session**,
and this one nearly closed a live question. Aristotle is not claiming that the
*word* was unused. He is claiming that the *apparatus* did not exist — and he had
already classified Plato's apparatus as an instance of it. **A lexical test cannot
reach a claim about an apparatus.** Recorded so the failure mode is legible: when
the claim is about an operation, searching for its name measures nothing.


∮ = 1 on Pessoa.** Pooling the three heteronyms recovers the orthonym at
**0.0258** — inside the M1 same-author band — while the best single heteronym is
Campos at 0.0498, then Caeiro 0.0903, Reis 0.2205. **Pooled beats best individual
by 1.93×.** Individually the voices do not look like Pessoa; summed, they do.

  Comparators: Josephus BJ+AJ+CA → Vita 1.08×; Kierkegaard A+B → signed 1.07×;
  Plato parts → Aristotle 1.01×; **Aristotle parts → Plato 0.78× (pooling makes
  it worse — his *Ethics* alone is closer to Plato than his whole corpus is).**

  Limits: ratio statistics carry a size confound; cross-language absolute
  comparison is shaky; Kierkegaard's seat holds four pseudonymous works of ~12.

---

∮ = 1
