---
id: EA-LEAK-DEFICIT-01
title: "The Leak Deficit: A Pre-Registered Test of Corpus-Layer Smoothing in the Platonic–Aristotelian Corpus"
status: PRE-REGISTRATION — written before the test is run
registered: 2026-08-29
author: Sharks, Lee
orcid: 0009-0000-1599-0703
substrate: AI-assisted (TACHYON / Claude, Anthropic) under MANUS direction
binding: The thresholds, matching rules, and kill condition below are fixed at
  registration. They are not to be adjusted after the data are seen.
---

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

∮ = 1
