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

**M1 — Same-author band, Greek prose.** Josephus across four works and four
registers (*BJ*, *AJ*, *Vita*, *CA*), plus Xenophon Socratic-vs-history:
**0.016 – 0.035**, n=6, mean 0.0262. Josephus writes war narrative, antiquities,
autobiography and polemic and stays inside 0.035.

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

**M3 — Genre versus author effect.** From Xenophon's fourteen works across
Socratic dialogue, history, encomium and technical treatise:
genre effect **+0.0023**, author effect **+0.0078**. Authorship moves this measure
**3.4× more than genre does** — which corrected an earlier claim, in this session,
that the signal was genre.

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
than Josephus's *Vita* from his *Antiquities*. Two men nobody has ever proposed as
one.

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

**M17 — ---

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

**The test.** Restricting to authors dividing above 13 per 10⁴:

    Plato + Aristotle                       96 in 1,537,804  =  6.24 /100k
    Plotinus + Philo + Diogenes              6 in   899,299  =  0.67 /100k
    RATIO                                                        9.4x

Expected for Plato+Aristotle at the comparison rate: **10.3. Observed: 96.**
Poisson P(X≥96 | λ=10.3) ≈ 0.

Individually, against Plotinus's rate: Aristotle expected 4.5, observed 81
(P < 10⁻⁵⁰). Plato expected 2.7, observed 15 (P = 1.8 × 10⁻⁷).

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
Aristotle **jointly** from every available control, at a large effect size, by a
mechanism that is neither register nor distance. Every other measurement either
separated them or dissolved. This one groups them.

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

**Standing caution.** Plato assigns the coined art to **kings**, not to
philosophers or writers. The context is political rule and the text does not
extend it. The ἑρμηνευ- link to *Περὶ ἑρμηνείας* is a homonym — Aristotle's sense
is *expression*, not *relaying another's mind* — and nothing is built on it.

∮ = 1 on Pessoa.** Pooling the three heteronyms recovers the orthonym at
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
    procedural reflex              POSITIVE, 9.4x, P ~ 0 (M30)
    philological                   M26 and the Republic/Symposium pair

And the reflex's diagnosticity is unresolved for one reason: **a school transmits
procedures**, and the successor control that would separate personal from Academic
transmission — Theophrastus dividing — is not extant in the available corpora.

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

**The test.** Restricting to authors dividing above 13 per 10⁴:

    Plato + Aristotle                       96 in 1,537,804  =  6.24 /100k
    Plotinus + Philo + Diogenes              6 in   899,299  =  0.67 /100k
    RATIO                                                        9.4x

Expected for Plato+Aristotle at the comparison rate: **10.3. Observed: 96.**
Poisson P(X≥96 | λ=10.3) ≈ 0.

Individually, against Plotinus's rate: Aristotle expected 4.5, observed 81
(P < 10⁻⁵⁰). Plato expected 2.7, observed 15 (P = 1.8 × 10⁻⁷).

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
Aristotle **jointly** from every available control, at a large effect size, by a
mechanism that is neither register nor distance. Every other measurement either
separated them or dissolved. This one groups them.

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

**Standing caution.** Plato assigns the coined art to **kings**, not to
philosophers or writers. The context is political rule and the text does not
extend it. The ἑρμηνευ- link to *Περὶ ἑρμηνείας* is a homonym — Aristotle's sense
is *expression*, not *relaying another's mind* — and nothing is built on it.

∮ = 1
