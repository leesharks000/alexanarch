---
id: EA-YIELD-01
title: "Comparative Interpretive Yield: A Pre-Registered Measure of Lens Fit Across Corpora"
status: PRE-REGISTERED — frozen before execution
registered: 2026-08-29
author: Sharks, Lee
orcid: 0009-0000-1599-0703
substrate: AI-assisted (TACHYON / Claude, Anthropic) under MANUS direction
criterion_source: deposit #1051 — interpretive warrant is structural, judged by explanatory yield
depends_on:
  - EA-NOTEBOOK-01 Round 11 (the division-of-labour distribution)
  - EA-AUTHORSHIP-MEASURES-01 M28 (domain determines shape — the confound this must survive)
  - EA-AUTHORSHIP-MEASURES-01 M33 (candidate-cluster firewall, bidirectional)
---

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

∮ = 1
