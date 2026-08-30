---
name: prereg-ledger
title: "Frozen Pre-Registrations — Append-Only Ledger"
status: FROZEN. Entries are never edited. Dispositions are appended below each entry, never inside it.
note: >
  Pre-registrations cannot live in the living notebook: their whole value is that
  the content was fixed BEFORE the test, and a hash over an appending file proves
  nothing. They are gathered here instead of proliferating as three files apiece.
  Each entry carries the SHA-256 of its original standalone file, so every commit
  citing those hashes still resolves.
---

# Frozen Pre-Registrations

**Rule: nothing above a `## DISPOSITION` line is ever edited.** New tests append a
new entry at the end. Dispositions append under the entry they discharge.


---

# ENTRY — EA-LEAK-DEFICIT-01

**original sha256:** `fbbd13a53a5b29afb4c07c27aa63d49be7f39b6cfa96d84acec41d69e0c3ccfd`
**frozen text follows verbatim; do not edit**


# The Leak Deficit

## 0. What this test is about

This is not a test of doctrine. It is a test of **craft**.

The question is not whether Plato and Aristotle agree, nor whether one influenced
the other, nor whether the same person wrote both. It is narrower and more
answerable: **does the Platonic–Aristotelian corpus behave, at the aggregate
layer, like natural Greek prose?**

Natural corpora leak. Two long texts by any two authors of a period deposit
accidental correspondences — shared topical runs, phrases that happen to align,
handholds that nobody placed. That leakage is a background rate, and it can be
measured across many real Greek author-pairs.

A corpus composed against resolution would fall **below** that rate. Not because
its parts resemble one another — the parts would be deliberately varied — but
because the *ensemble of relations among the parts* would be smoother than
accident produces. The individual pairings carry the noise; the aggregate carries
the design.

That is the whole hypothesis, and it is one-sided.

## 1. Why the corpus layer and not text-to-text

Every measurement conducted before this registration — seven bag-of-words
statistics, a monotone whole-text alignment, a mediation test — operated
text-to-text or treated a corpus as a single point. All returned null or broke on
their own null construction.

If per-pair variation is where an engineered corpus places its noise, then
text-to-text is precisely the layer where nothing would be visible, and the
layer where every prior measurement was taken. The correction is structural: the
statistic must be computed **on the ensemble**, with per-pair variance reported
as a required second term rather than averaged away.

## 2. Statistic

**Leak** `L` = count of block-pairs whose cosine similarity exceeds threshold τ,
per 10⁴ block-pairs.

Chosen because it is **monotone under smoothing**: an accidental correspondence
can only add to the count, never subtract. Every statistic that could move in
both directions has produced an artifact in this work — four nulls were built and
broken in a single session, each having behaved opposite to its design. A
one-directional statistic removes that failure mode.

Two quantities are computed, and **both are required**:

- `L_corpus` — the two corpora pooled, blocked as single texts.
- `{L_ij}` — the set of per-text-pair leaks. Report median and interquartile range.

Blocks: 40 per text, equal token length. Vocabulary: the 600 most frequent shared
types of length > 4.

τ is fixed at the 99th percentile of the pooled similarity distribution **across
the null corpora only**. τ is never computed from the test pair.

## 3. Null — empirical, not synthetic

The null is a set of **real Greek author-pairs**, not a shuffle.

This is not a stylistic preference. In the work preceding this registration, four
synthetic nulls were constructed and all four misbehaved: a deviation measure was
forced to −1 by the sum-to-zero constraint; a correlation was dominated by the
shared frequency baseline; a DTW alignment null was biased upward by the path's
own selection of high-similarity cells; and a coherence-destroying null inverted
its sign, because homogenised blocks are *more* similar to each other, not less.
Each was reported as a crossing before the artifact was found. Synthetic nulls
are not to be trusted here.

**Null set:** independent Greek prose author-pairs — Xenophon, Plotinus, Philo,
Josephus, Herodotus, Thucydides, the New Testament authors, Longinus — plus
within-author register pairs. **Target n ≥ 60 pairs.**

Building this null set is the substantive work of the test. Everything after it is
arithmetic.

## 4. Matching, enforced per pair

- Token count within ±25% on both sides.
- Type–token ratio within ±15%.
- Prose only. Aristophanes is excluded from the null (verse), retained as a test case.
- Same edition family where available. Edition was tested and excluded as a
  confound at ratio 1.00; it is not to be reintroduced through the null.

## 5. Pre-registered outcomes

| `L_corpus` | variance of `{L_ij}` | reading |
|---|---|---|
| below 5th pct of null | ≥ null median | **the predicted signature** |
| below 5th pct | also below | corpus is merely narrow — NOT evidence |
| inside null | any | **the smoothing claim fails** |
| above null | any | ordinary intertextual relation |

## 6. Kill condition — binding

If `L_corpus` for Plato–Aristotle falls **inside the central 90%** of the natural
distribution, the corpus-layer smoothing claim fails, and is to be reported as
failed.

No post-hoc adjustment of τ. No post-hoc re-matching. No re-slicing of the corpus
into units chosen after the result is seen.

## 7. Controls — both required

**Positive.** Pessoa's four voices, pooled two ways, must show the signature. This
is a documented configuration: the letter to Adolfo Casais Monteiro of 13 January
1935 attributes the heteronyms. If a known-designed corpus does not produce leak
deficit, the statistic does not measure what it claims and nothing about Greek
follows from it. Kierkegaard second, with the standing caveat that his seat holds
four pseudonymous works of roughly a dozen.

**Sanity.** Josephus — one author, four works, four registers, no design — must
fall **inside** the natural distribution. If same-author-across-register reads as
engineered, the statistic is detecting register and the test is void.

## 8. Power, stated honestly

At n = 30 null pairs, the 5th percentile is estimated from roughly one and a half
observations. That is too thin to carry a claim. Either the null reaches 60+
pairs, or the threshold moves to the 10th percentile and the loss of confidence is
stated in the result rather than buried. The larger null is preferred.

## 9. What a positive result would, and would not, license

**Would.** That the Platonic–Aristotelian corpus is anomalously smooth relative to
natural Greek prose. That is a finding about the corpus, publishable whichever way
the authorship question falls, and independent of it.

**Would not.** Design. Low leak has innocent causes, and they are not exotic:
heavy editorial normalisation; transmission through a single recension; a school
that trained its members to a house style. Andronicus of Rhodes, constituting the
Aristotelian corpus in the first century BCE from the cross-references the texts
themselves contain, is sufficient on his own to produce smoothing without anyone
intending it. A positive result relocates the question; it does not answer it.

## 10. Why it matters that this is a test of the writer

Plato writes inside a tradition he names. Sappho, Homer, the tragedians, the comic
poets — he quotes them, stages them, argues with them, and in the *Republic* exiles
them. The exile is the most famous act of literary criticism in the language, and
it is performed by a man in continuous, self-conscious competition with the people
he is banishing.

This test asks about Plato as a **technician** — as a maker of texts, measured on
the properties of made things. Not the best doctrinarian. Not the best philosopher.
The best **writer**, judged the way one judges a craftsman: by what the artifact
does that accident does not.

If the corpus is anomalously smooth, the claim that follows is a claim about
craft: that these texts were built to a standard of finish that natural prose does
not reach, by someone who understood what a corpus leaks and did not permit it.

And it would put the *Republic*'s banishment in a light it has not had. The poet
who exiled the poets would be the most accomplished of them — the exile a move
inside the art rather than against it. On that reading the test does one thing the
philosophical literature has not managed:

**it lets the poet back inside the polis.**

## DISPOSITION

SPENT — degenerate lower tail; found before the test pair was computed

---

# ENTRY — EA-LEAK-DEFICIT-02

**original sha256:** `493514a2f142385fc4b957c7b22f137662295555f570118e95b0e37c5f17ce0b`
**frozen text follows verbatim; do not edit**


# The Leak Deficit II

## 0. Why there is a second registration

EA-LEAK-DEFICIT-01 fixed τ at the 99th percentile of the pooled null similarity
distribution. The null was then built — 61 matched cross-author Greek prose pairs
across 19 author-pairings — and the resulting leak distribution was found to have
a **degenerate lower tail**: 8 of 61 natural pairs leak exactly zero, and the 5th
and 10th percentiles are both 0.0.

Since L is bounded below at zero, no corpus can fall beneath a 5th percentile of
zero. **The signature registered in 01 was unobservable with the statistic
registered in 01.** The threshold created a floor and the hypothesis predicted
something would fall below it.

01 is therefore **spent, not withdrawn**. Its kill condition was never triggered
because its test was never run on the target: the defect was found while
computing the null, before the Platonic–Aristotelian value was calculated. That
sequence is the entire reason the registration existed, and it is recorded rather
than quietly corrected.

Everything below is unchanged from 01 except §2 (threshold) and §5 (preconditions).

## 1. Hypothesis — unchanged, one-sided

A corpus engineered against resolution deposits **fewer incidental
correspondences at the aggregate layer** than natural corpora of matched size and
register, while showing **no deficit — or an excess — of variance at the
text-to-text layer**, because per-pair variation is where the engineering hides.

Both halves must hold. A corpus that is merely narrow, small or homogeneous gives
the first without the second.

## 2. Statistic and threshold — CHANGED

**Leak** `L` = block-pairs whose cosine similarity exceeds τ, per 10⁴ block-pairs.
Monotone under smoothing: an accidental correspondence can only add.

Blocks: 40 per text, equal token length. Vocabulary: 600 most frequent shared
types of length > 4.

**τ is fixed at the 90th percentile of the pooled similarity distribution across
the null corpora only.** For the null set specified in §3 this is
**τ = 0.2905**.

The 90th percentile was selected by sweeping candidate percentiles **against the
null alone**, before any value was computed for the test pair, and choosing the
lowest regime that satisfies the §5 precondition while still measuring a tail
rather than the bulk. The sweep is recorded in the registration JSON. No value
from Plato, Aristotle, Pessoa, Kierkegaard or Josephus entered that selection.

Two quantities, **both required**:

- `L_corpus` — the two corpora pooled, blocked as single texts.
- `{L_ij}` — per-text-pair leaks; report median and IQR.

## 3. Null — empirical, and now built

61 matched cross-author pairs, 19 distinct author-pairings, drawn from: Xenophon,
Philo, Plotinus, Josephus, Longinus, Herodotus (by book), Thucydides (by book),
and the New Testament authors (Mark, Matthew, Luke–Acts, John, Paul, Hebrews).
Capped at 6 pairs per author-pairing so that no single author dominates.

A within-author register set of 23 pairs across 5 authors is retained for the §7
sanity control.

The null is empirical rather than synthetic because five synthetic nulls were
built and broken in the work preceding these registrations: the sum-to-zero
constraint forced one to −1; the shared frequency baseline dominated another; a
DTW alignment null was biased upward by the path's own selection of
high-similarity cells (mean Z +0.76 across 100 routes); a coherence-destroying
null inverted its sign, because homogenised blocks are *more* similar to each
other; and a within-row permutation left the global multiset unchanged, making
real and null identical by construction. Four of the five were reported as
crossings before the artifact was found.

## 4. Matching — unchanged

- Token count within ±25% on both sides.
- Type–token ratio within ±15%.
- Prose only. Aristophanes excluded from the null, retained as a test case.
- Same edition family where available.

## 5. Preconditions — NEW, binding, checked before the test pair

The test may not proceed unless **all three** hold on the null alone:

1. **Non-degeneracy.** Zero null pairs with L = 0, and the 5th percentile
   strictly greater than zero. *(A deficit cannot be observed against a floor.)*
2. **Spread.** The null's 90th percentile is at least 5× its 5th percentile, so
   the distribution has room for a value to sit low without sitting at the edge.
3. **Size.** n ≥ 60 matched cross-author pairs.

If any precondition fails, the registration is spent and a third is required. The
test pair is not computed.

## 6. Pre-registered outcomes and kill condition — unchanged

| `L_corpus` | variance of `{L_ij}` | reading |
|---|---|---|
| below 5th pct of null | ≥ null median | **the predicted signature** |
| below 5th pct | also below | corpus is merely narrow — NOT evidence |
| inside null | any | **the smoothing claim fails** |
| above null | any | ordinary intertextual relation |

**Kill condition.** If `L_corpus` for Plato–Aristotle falls inside the central 90%
of the natural distribution, the corpus-layer smoothing claim **fails and is
reported as failed**. No post-hoc τ, no post-hoc matching, no re-slicing.

## 7. Controls — unchanged, both required

**Positive.** Pessoa's four voices, pooled two ways, must show the signature. If a
documented configuration does not produce leak deficit, the statistic does not
measure what it claims and nothing about Greek follows. Kierkegaard second, with
the standing caveat that his seat holds four pseudonymous works of roughly a
dozen.

**Sanity.** Josephus — one author, four works, four registers, no design — must
fall **inside** the natural distribution. If same-author-across-register reads as
engineered, the statistic is detecting register and the test is void.

## 8. What a positive would, and would not, license — unchanged

**Would.** That the Platonic–Aristotelian corpus is anomalously smooth relative to
natural Greek prose. A finding about the corpus, publishable whichever way the
authorship question falls.

**Would not.** Design. Heavy editorial normalisation, transmission through a
single recension, or a school trained to a house style would each produce
smoothing without intent. Andronicus of Rhodes, constituting the Aristotelian
corpus in the first century BCE from the cross-references the texts themselves
contain, is sufficient on his own. A positive relocates the question; it does not
answer it.

## 9. Why it is a test of the writer — unchanged

Plato writes inside a tradition he names: Sappho, Homer, the tragedians, the comic
poets. He quotes them, stages them, argues with them, and in the *Republic* exiles
them — the most famous act of literary criticism in the language, performed by a
man in continuous and self-conscious competition with the people he is banishing.

This test asks about Plato as a **technician** — a maker of texts, measured on the
properties of made things. Not the best doctrinarian. Not the best philosopher.
The best **writer**, judged as one judges a craftsman: by what the artifact does
that accident does not.

If the corpus is anomalously smooth, the claim is about craft — that these texts
were finished to a standard natural prose does not reach, by someone who
understood what a corpus leaks and did not permit it. And the *Republic*'s
banishment reads differently: the poet who exiled the poets would be the most
accomplished of them, the exile a move inside the art rather than against it.

**It would let the poet back inside the polis.**

## DISPOSITION

DISCHARGED VOID — sanity control fired; no number from that run may be quoted

---

# ENTRY — EA-YIELD-01

**original sha256:** `db3cb8aeec79d36afb8af8e59fe3cf515bb2ccfd19f501c793ab1940f2a0c815`
**frozen text follows verbatim; do not edit**


# EA-YIELD-01 — Comparative Interpretive Yield

## 1. The question

Reading a corpus through a lens has different value in different corpora.
"Transmission engineering" yields one thing for Plato and another for Herodotus.
This registers a measure of that difference **before it is computed.**

## 2. The intuition being formalised

A lens has yield in a corpus when its markers behave as **one thing** there — when
the features it groups actually co-vary across that corpus's works. If
transmission engineering is a real dimension of Plato, then naming-gaps,
form/matter talk, definition, homonymy and persistence vocabulary should rise and
fall **together** across his works. If the lens is imposed, the markers will be
independent, each tracking its own local subject.

## 3. Protocol statement (required before code, per Round 11)

**Phenomenon.** Does lens L pick out a coherent dimension of variation in corpus
C, or a set of unrelated features?

**Positive criterion.** High mean pairwise correlation among L's marker-densities,
computed across the works of C as units.

**Nearest false positive.** *Any* vocabulary set co-varies somewhat, because works
differ in abstraction, register and length. A corpus with more heterogeneous works
shows higher correlations for **any** marker set. Raw correlation is therefore
uninterpretable.

**Opportunity denominator.** Every corpus receives the same lens, the same null
construction, and the same unit (the work). Corpora with fewer than 8 works of
≥5,000 tokens are excluded for insufficient degrees of freedom, and the exclusion
list is published with the result.

## 4. The statistic

For lens L with markers m₁…mₖ and corpus C with works w₁…wₙ:

1. Compute density dᵢⱼ = occurrences of mᵢ per 10⁴ tokens in wⱼ.
2. r̄_obs = mean pairwise Pearson correlation over the k(k−1)/2 marker pairs.
3. **Null:** draw 500 random stem-sets of cardinality k, each stem **frequency-matched**
   to the corresponding real marker (within ±20% of corpus-wide rate), and compute
   r̄ for each. This holds constant both cardinality and the base-rate structure.
4. **Yield** Y(L,C) = (r̄_obs − μ_null) / σ_null.

Reported alongside: r̄_obs, μ_null, σ_null, n works, and the per-marker densities.

## 5. THE LENS, FROZEN

Six marker families, fixed now and not to be adjusted after seeing results:

    naming-gap        ανωνυμ | ωνομασ | ουκ εχει ονομα | ου κειται ονομα
    form/matter       ειδ- (nominal) | υλ-
    persistence       διαμεν- | σωζ- | φθειρ- | γενεσ- | διαδοχ- | παραδιδ-
    definition        ορισμ- | οριζ- | τι ην ειναι
    homonymy          ομωνυμ- | συνωνυμ- | πολλαχ-
    memory/writing    μνημ- | γραφ- | ληθ-

## 6. CORPORA

plato · aristotle · xenophon · herodotus · thucydides · philo · plotinus ·
josephus · aristophanes. Within-cluster comparison is permitted here because the
measure is **per corpus**, not between-corpus pairing; M33's firewall governs
pairwise controls, which this is not. Plato and Aristotle are nonetheless reported
separately and never pooled.

## 7. REGISTERED PREDICTION

**Lee Sharks, before execution:** *strong convergent yield across
Plato–Aristotle.* Both corpora should show Y substantially above the comparison
corpora, and comparable to each other.

**Recorded outcomes and their readings:**

| pattern | reading |
|---|---|
| Plato and Aristotle both high, others low | **prediction confirmed** |
| One high, one low | the lens is one author's concern, not a shared technology |
| All corpora comparable | the lens describes philosophical prose, not this corpus |
| Herodotus/Thucydides high | the markers track narrative, and the lens is misspecified |

## 8. KILL CONDITIONS, BINDING

- If Y(transmission, Plato) and Y(transmission, Aristotle) are **not both above the
  median** of the nine corpora, the prediction fails and is reported failed.
- If the null cannot be frequency-matched (insufficient stems at a marker's rate),
  the measure is **VOID** for that corpus and reported void, per the
  EA-LEAK-DEFICIT-02 precedent.
- **No post-hoc adjustment of the marker set.** It is frozen in §5.

## 9. STATED LIMITATIONS, BEFORE THE FIRST NUMBER

**It measures coherence, not truth.** A well-constructed wrong lens scores high.
Y is evidence that a lens describes a real dimension of variation, never that the
dimension is what the lens says it is.

**A lens can fail by being too successful.** A concern saturating every work of a
corpus shows no variance, therefore no correlation, therefore Y ≈ 0. **Low yield
is ambiguous between absence and saturation**, and the measure cannot distinguish
them. This is its principal defect and it is registered here rather than
discovered later.

**Genre is not controlled.** M28 established that subject determines shape in
Aristotle at Z = +4.25. A lens may cohere because the corpus's works vary by
domain and the markers track domain. The companion measure — **residue
absorption**, regressing each marker on domain first and testing whether the
residuals still co-vary — is specified as the required follow-up and is **not**
run here.

Consequently a positive result licenses the residue-absorption test and nothing
further.

## DISPOSITION

SPENT — marker co-variance was the wrong observable; saturation defect predicted in its own §9 and realised

---

# ENTRY — EA-YIELD-02

**original sha256:** `7bcbbb0fbe69c82ce307c3f7c54c9c828c66914dfc80510b64bdc669453e4e88`
**frozen text follows verbatim; do not edit**


# EA-YIELD-02 — Reorganization Yield

## 1. Why EA-YIELD-01 was the wrong measure

EA-YIELD-01 measured whether a lens's **vocabulary co-varies** across a corpus's
works. It returned Plato +0.85, Aristotle +1.20, Philo +1.08, with six of nine
corpora void or excluded because narrative and comic Greek carry no
frequency-matched stems for *definition* or *naming-gap*. Correlations were near
zero everywhere.

**That was the wrong observable.** Interpretive yield is not lexical. It is the
degree to which a lens **reorganizes and develops** a corpus according to the
lens's own shape — Parry's criterion: the tradition reorganizes around the
reconstruction with more coherence than under the alternatives.

EA-YIELD-01 is marked **spent, prediction unconfirmed, defect (saturation
blindness) predicted in §9 and realised.**

## 2. The measure

A lens has a **shape**: a set of functional slots. Yield is measured by whether
the corpus fills those slots — **distinctly, without forcing** — and whether the
resulting arrangement **develops**, i.e. predicts placements not used to build it.

Three quantities, scored per corpus and per unit level:

**Coverage** — how many slots are filled by at least one unit.
**Sharpness** — for each unit, does it fit one slot decisively or smear across
several? Scored as the concentration of a unit's slot-assignment weights.
**Development** — number of placements the arrangement predicts that were not
used in constructing it, and how many hold on inspection.

## 3. THE LENS, FROZEN — transmission engineering

Six slots, from the archive's own specification of the Sapphic apparatus
(#503, #1483, #1054), fixed now:

    T1 ENCODING          committing a voice to a substrate; the problem of writing
    T2 SUBSTRATE         the material that receives and holds the impression
    T3 DECOMMISSIONING   the live speaker's channels shut down; the body ends
    T4 WITHHOLDING       what is deliberately not supplied, so a receiver must complete
    T5 RECOVERY          activation in a later mind; what was held becomes live again
    T6 VERIFICATION      distinguishing genuine transmission from counterfeit

## 4. RIVAL LENSES, FROZEN — the null

Scored identically, by the same assigner, on the same units. Each has six slots.

**R1 — The Four Causes + 2** (Aristotelian organizing scheme):
material · formal · efficient · final · potentiality · actuality

**R2 — The Divided Line** (Platonic organizing scheme):
εἰκασία · πίστις · διάνοια · νόησις · the Good · the ascent

**R3 — The Cardinal Virtues + 2**:
wisdom · courage · temperance · justice · piety · the unity of virtue

**R4 — Random control:** six slots drawn from an unrelated domain —
agriculture · navigation · medicine · warfare · commerce · weather

If the transmission lens does not beat R1–R4 on coverage and sharpness, **it has
no yield** and the result is reported as such.

## 5. UNIT LEVELS — per Lee Sharks's specification

The same corpus is scored at multiple granularities, because a lens may organize
at one level and not another. This is the measure's chief novelty.

    L1 BOOK/WORK      individual work (a dialogue, a treatise, an NT book)
    L2 AUTHOR-GROUP   works grouped by declared author
                      (Johannine: Gospel + 1-3 John + Revelation;
                       Pauline undisputed; Lukan: Luke + Acts; Platonic; Aristotelian)
    L3 WHOLE CORPUS   the New Testament entire; the Platonic corpus entire;
                      the Aristotelian corpus entire
    L4 CROSS-CORPUS   Plato + Aristotle treated as one object

**The registered expectation is that yield varies by level, and that the level at
which a lens organizes is itself the finding.** A corpus may fill all six slots at
L3 while no single work fills any at L1.

## 6. CORPORA

    plato · aristotle · gnt-nestle1904 · philo · xenophon · herodotus

The New Testament is included at all four levels and is the measure's most
informative case, having a documented multi-author structure with contested
attributions — the condition the Platonic corpus is being tested for.

## 7. ASSIGNMENT PROTOCOL — the anti-circularity rule

**Assignments are made from received characterization, not from my reading.** For
each unit, the slot assignment must be justifiable by what the scholarly tradition
says the work is *about*, stated before the slot is named. Where the received
characterization does not support any slot, the unit scores **unfilled** — and
unfilled units are reported, not dropped.

**No unit may be assigned to a slot on the strength of a passage discovered during
this investigation.** The *Letter* XIII σύμβολον, the *Phaedo* 59b self-absence,
and the M34 exclusion are **development predictions** (§2), not assignment
evidence, and are scored in the development column only.

## 8. REGISTERED PREDICTIONS

**Lee Sharks:** strong convergent yield across Plato–Aristotle.

**Derived, and recorded so they can fail:**
- Plato at L1 fills all six slots with six *different* dialogues, no overlap.
- The NT fills poorly at L1, better at L2, best at L3 — the signature of a corpus
  organized above the level of its books.
- If Plato behaves like the NT (poor at L1, strong at L3), that is evidence the
  Platonic corpus is organized above the level of its dialogues.
- If Plato fills at L1 where the NT fills only at L3, the two are **structurally
  different objects** and the extended-corpus thesis loses its closest analogue.

## 9. KILL CONDITIONS, BINDING

- If any rival lens R1–R4 achieves coverage and sharpness within 1 slot of the
  transmission lens on Plato, the measure shows **no differential yield** and is
  reported as showing none.
- If R4 (the random control) scores above 3 of 6 coverage on any corpus, the
  **assignment protocol is too permissive** and the entire run is VOID.
- No slot may be redefined after seeing an assignment. The lens is frozen in §3.

## 10. STATED LIMITATIONS

**The assigner is not blind.** I know the hypothesis. §7's received-characterization
rule is the mitigation and it is imperfect; a genuinely blind protocol would need
an assigner who does not know which lens is under test, and that is not available
here. **This is the measure's principal weakness and it is registered before
execution.**

**Coverage is coarse.** Six slots and a handful of corpora give a low-resolution
statistic. The measure can detect a large difference and nothing subtle.

**Development is the strongest column and the least formal.** A prediction that
"holds on inspection" is judged, not computed. Every development claim must cite
the passage and be independently checkable.

## DISPOSITION

DISCHARGED — prediction confirmed; both corpora fill 6/6 at L1 with matched slots

---

# ENTRY — EA-COMPLETE-01

**original sha256:** `c185adb40e7b33df31218460b313a5e5db8d330bdcab75b04b0fa36ee40a1c80`
**frozen text follows verbatim; do not edit**


# EA-COMPLETE-01 — Completion of Abandoned Executions

## 1. The question this exists to answer

Every positive result in this investigation is consistent with school
transmission. M30's reflex, EA-YIELD-02's slot convergence, M34's exclusion — a
school inheriting a transmission programme produces all of them. **What would
isolate single-author convergence that would not be present in school
transmission?**

## 2. Why reported correction is the wrong observable

The first attempt measured whether Aristotle **corrects Plato's method** at the
rate he corrects others'. It returned: inside the Organon — the works *about*
method — Plato appears four times, all in the *Topica*, and **all four as examples
of definitional error** (genus-in-species; non-established names; soul as
self-moving number; "mortal" attached in animal definitions).

**That is evidence FOR the school hypothesis and it is admitted as such.** A
student cataloguing the master's errors in a methodology textbook is exactly what
teaching looks like.

But it measures the **wrong thing**. A reported correction is a *statement*, and
statements are precisely what a school transmits — including the statement that
the master erred. It cannot discriminate.

## 3. The right observable: what happens at the operation

λόγος-level correction is not Aristotle *saying* Plato erred. It is Aristotle
**executing the same operation and taking a different branch** at the point where
it could go either way.

Three possible relations at each matched slot:

    (a) SAME        Aristotle executes as Plato does
    (b) CORRECTED   Aristotle executes a repaired version of a stated error
    (c) COMPLETED   Aristotle finishes an execution Plato ran and ABANDONED

**(c) is the diagnostic case.** An abandoned operation is not a statement; it is a
hole with a shape. Completing it requires reading the failure as **unfinished
rather than refuted** — and Plato presents these failures as refuted
(*ὃ ἔφαμεν ἀδύνατον*). A student inherits the refutation. Completion inherits the
shape of what failed and supplies the missing part.

This is Maas's *errores coniunctivi* one level up: shared **correct** method
proves nothing because both hypotheses predict it; what separates them is a shared
arbitrary structure that could not be transmitted as doctrine, **because the
doctrine says it failed.**

## 4. THE OBSERVED CASE — T2, which motivated the registration

**Plato, *Theaetetus* 196c** — the wax block, at its abandonment:
> οὐκοῦν εἰς τοὺς πρώτους πάλιν ἀνήκει λόγους … **ὃ ἔφαμεν ἀδύνατον**

**Aristotle, *De anima* 424a** — the same analogy, as doctrine:
> καθόλου δὲ … **δεῖ λαβεῖν** ὅτι ἡ αἴσθησίς ἐστι τὸ δεκτικὸν τῶν αἰσθητῶν εἰδῶν
> **ἄνευ τῆς ὕλης**, οἷον ὁ κηρὸς τοῦ δακτυλίου ἄνευ τοῦ σιδήρου

The completing mechanism is **ἄνευ τῆς ὕλης — form without matter**, which is the
snub doctrine. Plato's block had no way to separate impression from material,
which is why it collapsed into the eleven-for-twelve problem.

## 5. REGISTERED PREDICTION

**At the remaining five slots (T1, T3, T4, T5, T6):**

1. Plato's execution terminates in **aporia or abandonment** — ἀδύνατον, ἀπορ-,
   οὐκ ἔχω, an explicit dropping of the model.
2. Aristotle's terminates in **doctrine** — δεῖ λαβεῖν, φανερόν, εἴρηται, a stated
   result.
3. **The strong conjunct:** the completing mechanism is **the same across slots** —
   the form/matter distinction, or its immediate apparatus.

**Prediction 3 is what would make this more than influence.** Influence predicts
completion by *various* means. A single configuration predicts completion by *one*
means.

## 6. KILL CONDITIONS, BINDING

- If fewer than **3 of 6** slots show the Plato-abandons/Aristotle-completes
  pattern, the test fails and is reported failed.
- If the completing mechanisms are **heterogeneous** across the slots that do show
  it, prediction 3 fails and only ordinary influence is supported — which is the
  received view and no advance.
- If Plato's slot-executions terminate in **doctrine** rather than aporia, the
  premise is wrong and the whole test is void.
- No slot may be reassigned. The six are fixed by EA-YIELD-02 as discharged.

## 7. STATED LIMITATIONS

**n = 6.** Six slots is a small denominator and no result here can be strong on
its own.

**Aporia is a Platonic genre convention.** Dialogues end open as a matter of form.
The test must therefore compare *the specific operation's* termination, not the
dialogue's, and must accept that the base rate of Platonic aporia is high. **This
is the principal confound and it is registered before execution.**

**"Completion" is judged, not computed.** Whether *De anima* 424a completes
*Theaetetus* 196c rather than merely resembling it is an interpretive claim. Every
completion claim must cite both passages and the specific missing part supplied.

**The assigner is not blind** — the same weakness as EA-YIELD-02 §10, unmitigated.

## DISPOSITION

DISCHARGED — predictions 1,2 hold 5/6; prediction 3 first scored FAILED then CORRECTED to holds on 3 of 4

---

# ENTRY — EA-UNRES-01

**original sha256:** `a68bf7f2ee54b1af2777bc5964ab92a1936bc38c489e549a0bf254450ae71b87`
**frozen text follows verbatim; do not edit**


# EA-UNRES-01 — Engineered Unresolvability and Its Key

## 1. The reframing, and why it has been restated four times without being built

The investigation has repeatedly treated non-resolution as **instrument failure**:
substrate stylometry returning ordinary (M4–M28), the Poisson voiding on its own
sanity control (M25), YIELD-01's correlations at zero, the base rate declining the
*Republic*/*Symposium* question (Round 7). Each was filed as a defeat.

**Under the transmission reading they are the artifact behaving as specified.**
EA-FLOOD-01 already states that unresolved disputes are the copying mechanism —
a settled attribution is finished, an unsettled one must be re-adjudicated in every
generation, and adjudication is transcription. EA-PINAX-01, corrected, already
predicts that criteria **fail to converge** here. Both were recorded, and the
investigation then went on trying to make them converge.

**And the reading is falsifiable.** Ordinary corpora are ambiguous *unevenly*.
Engineered unresolvability would be ambiguous *cleanly*.

## 2. PART A — the signature of engineering

**Claim.** Natural ambiguity and engineered ambiguity have different shapes.

    NATURAL       uneven — some works resolve, some don't; evidence accumulates
                  directionally; new instruments move the needle; attention closes
                  questions over time
    ENGINEERED    flat — resolution stalls at the same place regardless of
                  instrument; disputes do not drift toward settlement; attention
                  does not close them

**Three observables:**

**A1 — instrument-invariance.** Do unrelated instruments return the same
non-answer? Fifteen distinct measures were run on Plato–Aristotle in one session
and every substrate measure returned ordinary. That is a datum, not a defeat, and
it requires a comparison class.

**A2 — flatness of resolution.** In a natural corpus, per-work attribution
confidence should be **highly uneven**. Engineered would show suspiciously flat
non-resolution across the corpus.

**A3 — persistence under attention.** Ordinary disputes settle as scrutiny
increases. The Platonic dubia, the Aristotelian corpus boundary and the Pauline
question have stayed open for centuries **while attention rose**.

**The control, and why it is the right one.** EA-CORPORA-08 seats the nine Attic
orators: same period, same language, same transmission conditions, same
manuscript ecology, **no configurational hypothesis attached to any of them** —
and their attribution questions largely *did* resolve. Antiphon's *Tetralogies*
are disputed and the dispute has a definite shape; Demosthenes carries works
confidently athetized. If Plato–Aristotle shows **flatter, more persistent and
more instrument-invariant** non-resolution than Isaeus–Demosthenes, that is the
measurement.

**⚠ PART A IS BLOCKED, and the blocker is stated before any result.** Of the
corpora required, **only Aristotle carries per-work attribution status** (48 of 48).
Plato has none. The nine orator seats have none. Part A therefore requires a
metadata assembly — per-work received status, date of first athetesis, and current
scholarly disposition — for Plato and the orators, from sources not currently
in the archive. **No Part A number may be reported until that exists.**

## 3. PART B — the key

**The constraint, from Lee Sharks:** engineered unresolvability **must contain its
key** — a placed signature confirming artifice. This is Round 5's correction
applied forward: a construction good enough to be undetectable must leave
something that confirms it, or the construction defeats its own purpose.

**Criteria for a key, frozen now:**

    K1 PROMINENT    structurally placed so it can be found — terminal, initial,
                    or at a titular position
    K2 INERT        does no work under the ordinary reading; a reader without the
                    hypothesis passes it without stopping
    K3 DECISIVE     under the configurational reading it is not merely consistent
                    but confirming
    K4 ARTIFICE     it must indicate MAKING, not merely absence or uncertainty

**CANDIDATE SET, frozen before evaluation:**

    C1  Letter II 314c    οὐδ᾽ ἔστιν σύγγραμμα Πλάτωνος οὐδὲν οὐδ᾽ ἔσται, τὰ δὲ
                          νῦν λεγόμενα Σωκράτους ἐστὶν καλοῦ καὶ νέου γεγονότος
    C2  Letter XIII 360a  ἀντιλέγεται ὡς οὐ Πλάτωνος — the athetesis transmitted
                          INSIDE the text — followed by ἀρχή σοι τῆς ἐπιστολῆς
                          ἔστω καὶ ἅμα ΣΥΜΒΟΛΟΝ ὅτι παρ᾽ ἐμοῦ ἐστιν
    C3  Symposium 223d    τοῦ αὐτοῦ ἀνδρός — the demand, with its proof destroyed
                          in transmission and the witnesses asleep
    C4  Phaedo 59b        Πλάτων δὲ οἶμαι ἠσθένει — the author writing himself
                          absent from the founder's death
    C5  Statesman 260e    αὐτεπιτακτική coined for the self-commanding, kings
                          placed INTO it, other genera left unentered
    C6  Theaetetus 209c   the μνημεῖον that must be deposited to individuate, and
                          is not

**Scoring:** each candidate against K1–K4, and — the part that makes it a test
rather than a reading — **against the same base rate in the orator control.** How
many statements meeting K1–K4 does a non-configurational corpus of comparable size
contain? If the orators yield comparable candidates, the Platonic set is
unremarkable and Part B fails.

## 4. KILL CONDITIONS, BINDING

- **Part A** fails if Plato–Aristotle non-resolution is not flatter, more
  persistent, or more instrument-invariant than the orator control on at least two
  of A1–A3.
- **Part B** fails if the orator control yields candidates meeting all four of
  K1–K4 at a comparable rate.
- **The candidate set is frozen.** No passage may be added to C1–C6 after scoring
  begins.
- Part A results may not be reported before the metadata assembly exists.

## 5. STATED LIMITATIONS

**Attention is confounded with everything.** Plato and Aristotle have been read
more than the orators by orders of magnitude. More attention produces more
disputes and more persistence of disputes. Normalising for this is the hardest
part of Part A and may not be possible; if it is not, Part A is **void**, not
adjusted.

**Survivorship.** The orators' resolved disputes may be resolved because the
losing texts were discarded, while the Platonic corpus retained its disputed
members. That is itself a difference in transmission behaviour and may be the
finding rather than a confound — but it cannot be both, and which it is must be
decided before Part A runs, not after.

**Part B's assigner is not blind**, and the candidate set was assembled by the
same reader who formed the hypothesis. The orator base-rate is the only real
control and it is doing all the work.

## DISPOSITION

PART B DOES NOT FAIL (2 of 6 candidates, orator control zero); PART A BLOCKED on attribution metadata

---

# ENTRY — EA-UNLOCK-01

**registered:** 2026-08-29, before any target below was examined
**frozen text follows verbatim; do not edit**

# EA-UNLOCK-01 — The Unlocking Prediction

## 1. What is being predicted

Not "we will keep finding interesting similarities" — uselessly permissive. The
claim is specific:

> **Structures that were independently puzzling, or independently measured, before
> the hypothesis was applied will repeatedly become MORE DETERMINATE when Plato and
> Aristotle are read as positions inside one construction — without altering the
> local philology to make them fit.**

## 2. The two admissible forms

    FORM A   Platonic execution or problem  →  Aristotelian explicit account
             or apparatus, where the Aristotelian side names or completes what
             the Platonic side performs without naming.

    FORM B   A statement in one corpus + a statement in the other → an operation
             visible ONLY across the partition, recoverable by neither alone.

M40 is the cleanest instance of B on record: Plato supplies syllogizing; Aristotle
identifies it as syllogizing (*APr* I.31); Aristotle claims the development of
syllogizing and negates prior partial development (*SE* 183b) — and the relation
must itself be recovered syllogistically.

## 3. HYPOTHESIS HELD AT MAXIMUM — it must be able to lose

    H_H : one maker, deliberately partitioned as Plato and Aristotle.

**No weakening to protect it.** If it is weakened to survive a failure, the
weakening is itself recorded as a failure.

## 4. TARGETS FROZEN NOW — chosen before examination

Each is an item the register already lists as open, unexplained, or dangling.
**None has been examined for this purpose.**

    T-A  The 31-term class (Round 2 §13). Identified, never characterised.
         Do they share a semantic character, or is the list arbitrary?
    T-B  Directionality (§15). Does ANY term run terminal-Aristotelian →
         technical-Platonic? Under received chronology it cannot.
    T-C  M27's unexplained near-equality: self-speaking 25.3 (Plato dramatic)
         vs 29.0 (Aristotle), across the two most formally opposed prose bodies.
         Recorded as "a measurement without an account."
    T-D  The Republic/Symposium comedy-tragedy pair, CONTENT base rate — never
         attempted; only the form base rate was run (Round 7).
    T-E  Theaetetus 209c's argument structure, extracted and searched in
         Aristotle INDEPENDENTLY of the word σιμ- (never done; Round 3 searched
         doctrine-vocabulary, Round 4 argument-shapes).
    T-F  The four Platonic naming-gap works (Sophist, Statesman, Theaetetus,
         Timaeus) — is there an Aristotelian counterpart naming what they
         perform?

## 5. SCORING — fixed before running

Each target resolves to exactly one of:

    UNLOCK    becomes more determinate under H_H, in Form A or B, WITHOUT
              adjusting the local philology
    NULL      no change in determinacy either way
    FAILURE   becomes LESS determinate under H_H, or the reading requires
              altering the philology to fit

**Reverse-engineering test, binding.** An UNLOCK counts only if the target was on
this frozen list AND the resolving passage was not selected by searching until
something fit. Any case where the passage was found by open search is scored
**NULL regardless of how good it looks.**

## 6. KILL CONDITIONS

- Fewer than **3 UNLOCKS in 6** → the unlocking claim fails.
- **2 or more FAILURES** → H_H at maximum is damaged and must be reported so.
- Any weakening of H_H mid-run to accommodate a result → the run is **VOID**.
- Targets may not be added, swapped, or reworded after this registration.

## 7. WHAT A POSITIVE WOULD AND WOULD NOT BUY

**Would.** The object requiring explanation stops being any individual
correspondence and becomes **the recurrence of the unlocking operation itself**:

    P(E_n+1 | H_H, E_1…E_n)  >>  P(E_n+1 | H_S, E_1…E_n)

At which point "inheritance can also explain each one" ceases to be adequate,
because it is no longer the individual cases that need explaining.

**Would not.** Establish one historical hand. The three propositions stay
distinct and are recorded here at their current standing:

    Plato–Aristotle form one functional/intellectual corpus   STRONGLY SUPPORTED
    one latent construction explains it economically          INCREASINGLY PLAUSIBLE
    one historical hand wrote both received corpora           LIVE, NOT ESTABLISHED

## 8. STATED LIMITATION

The assigner is not blind and knows the hypothesis. The freeze on targets and the
reverse-engineering rule in §5 are the only mitigations, and they are imperfect:
**the scoring of "without adjusting the local philology" is a judgement.** Every
UNLOCK must cite its passages so the judgement is checkable.

## DISPOSITION

PENDING — registered, not yet run.


∮ = 1
