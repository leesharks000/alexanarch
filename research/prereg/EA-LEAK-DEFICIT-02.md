---
id: EA-LEAK-DEFICIT-02
title: "The Leak Deficit II: Corpus-Layer Smoothing in the Platonic–Aristotelian Corpus, with a Non-Degenerate Threshold"
status: PRE-REGISTRATION — written after the null was built, before the test pair was computed
registered: 2026-08-29
supersedes: EA-LEAK-DEFICIT-01 (sha256 fbbd13a53a5b29afb4c07c27aa63d49be7f39b6cfa96d84acec41d69e0c3ccfd) — SPENT, not withdrawn
author: Sharks, Lee
orcid: 0009-0000-1599-0703
substrate: AI-assisted (TACHYON / Claude, Anthropic) under MANUS direction
binding: Thresholds, matching rules, preconditions and kill condition are fixed at
  this hash. No post-hoc adjustment. A run under altered parameters is a
  different test requiring its own registration.
---

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

∮ = 1
