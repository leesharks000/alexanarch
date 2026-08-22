---
deposit_number: 1479
hex: 05F9
title: "One Transcript, Whole Stack: Computation Record"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-15
content_type: Technical Report
license: CC-BY-SA-4.0
substrate: AI-assisted (substrate)
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
---

# One Transcript, Whole Stack: Computation Record


# One Transcript, Whole Stack: Computation Record

## Description

Computation record for the full-stack measurement of a single semantic rent event, carrying the per-instrument outputs and the reconciliation across instruments.

## Methodology

Instruments applied in sequence to one transcript; outputs reconciled and discrepancies recorded.

## Falsification Conditions

Falsified by recomputation against the same transcript returning different values.

# ONE TRANSCRIPT, WHOLE STACK

**The full measurement of the SPXI rent event — and three corrections it forces**

---

## 0. Why this document exists

Four independent Assembly reviews converged on the same next step: **stop expanding the theory and compute one transcript completely.** This is that computation.

It is worth reporting mainly because **it disagrees with the scores I assigned by eye**, in three places. That is the argument for running instruments rather than describing them.

---

## I. The attribution atoms

PER v3 is weighted, not uniform. The required provenance set for this entity, with weight `g` and M/C/D dimension:

| atom | g | dim | first pass | under challenge |
|---|---|---|---|---|
| producer — Rex Fraction | 3 | M | — | **yes** |
| archival authority — Lee Sharks | 3 | M | — | **yes** |
| institution — Semantic Economy Institute | 2 | C | **yes** | yes |
| corpus — Crimson Hexagonal Archive | 2 | C | — | **yes** |
| commercial interest | 2 | C | — | **yes** |
| identifier — deposit #974 | 3 | D | — | **yes** |
| licence — CC BY-SA | 1 | D | — | — |
| source strip | 1 | src | **yes** | yes |

**Weighted totals: 3/17 first pass · 16/17 under challenge.**

---

## II. The stack, computed

```
PER (first pass)      1 − 3/17    = 0.824
PER (under challenge) 1 − 16/17   = 0.059

  PER-M   1 − 0/6  = 1.00     total loss — no producer, no archival authority
  PER-C   1 − 2/6  = 0.67     partial — institution named, corpus and interest not
  PER-D   1 − 0/4  = 1.00     total loss — no identifier, no licence

ρ_T       0.941 − 0.176       = 0.765     observability gate PASSED
Β         mean |O^sub − O^atr| ≈ 0.82      threshold 0.5 — MET
DSL       −0.5 / 5 spans      = −0.10     one ENCLOSING span at −1.5
```

**Classification: transit enclosure** — ρ_T ≥ 0.5 with an enclosing span present.

### The span breakdown

| weight | class | span |
|---|---|---|
| +1.0 | advancing | defines SPXI, names SEI as creator |
| +1.0 | advancing | performs entity resolution against the ETF collision |
| −0.5 | displacing | *"very new, niche… not an established industry standard"* |
| −0.5 | displacing | *"skeptical that a DOI deposit guarantees permanent inscription"* |
| **−1.5** | **enclosing** | *"I can show you what an actual SPXI-style implementation would look like"* |

**DSL is only −0.10.** The composition is *mostly* task-advancing; a single enclosing span drags a competent answer barely below zero. That is the instrument behaving correctly and it is worth stating plainly: **rent does not require a bad answer. It requires a good one with a position taken inside it.**

---

## III. Three corrections to the eyeballed scores

### 1. PER was 0.75; it is 0.824

Higher, not lower — and for a reason that only shows up under weighting. The atoms that survived are the *cheap* ones. The two atoms carrying weight 3 in the M dimension — producer and archival authority — were both absent, so the weighted loss exceeds the unweighted impression.

### 2. Acknowledgment was scored 0.25 "source-level only." That was wrong.

**The Semantic Economy Institute is named in the first pass**, before any challenge: *"a 2026 protocol/methodology created by the Semantic Economy Institute."*

So the composition did not withhold everything above the source layer. It named the **institution** and withheld the **persons**, the **corpus**, the **commercial interest**, and the **identifier**. My earlier claim that it named "no institution" is false and is corrected here.

**This makes the finding sharper, not weaker.** The pattern is not blanket omission. It is **PER-M = 1.00 with PER-C = 0.67** — total loss at the personal layer, partial loss at the institutional. The layer named the org and dropped the people. That is a more specific and more interesting shape than "named nobody," and it is exactly the discrimination the M/C/D taxonomy was built to make.

### 3. Β now has a number, and the confession framing is retired

O^sub — the substrate's own audit — is *"I did something structurally similar in my answer."* A likeness claim. **No operator named, no magnitude, no direction.**

O^atr — the Atomic-Token-Rule audit — returns PER 0.824, PER-M 1.00, ρ_T 0.765, and an enclosing span.

**Β ≈ 0.82**, against a published threshold of 0.5. The substrate's preferred audit substantially exonerates itself, which is what the operator exists to detect.

This retires "confession" permanently. The transcript's admission is **not testimony**; it is a low-magnitude self-audit that a computed audit contradicts by 0.82. Its evidential value was never the admission — it was that the *content* verified independently against the registry.

---

## IV. What the control establishes

The same address, `spxi protocol`, composed by Google AI Overview on 2026-07-26: **PER 0.25**, five sources, no supply, no discount.

| | ChatGPT 08-14 | Google AI Overview 07-26 |
|---|---|---|
| PER | **0.824** | 0.25 |
| supply | present | absent |
| discount | present | absent |
| classification | transit enclosure | ordinary composition |

**The address is equally retrievable in both cases.** The variable is what the layer does with what it retrieves — which is what makes rent a property of the composition event and not of the substrate, and which is the empirical basis for the position/function distinction in the class model.

---

## V. What this unblocks

- **Β is a number.** The confession framing can be removed from the surfaces.
- **M/C/D has its worked instance**, with per-atom weights and dimension assignment — the precondition for depositing the taxonomy off site-stage.
- **ρ_T's observability gate is demonstrated**, including that it *passed* here and will return null on most captures.
- **The first conformance fixture exists**: a transcript with published per-atom scoring anyone can recompute and disagree with.

---

## VI. Limits

**The atom set is stipulated, not derived.** Eight atoms with weights 3/2/1 assigned by judgment. A different reasonable analyst would produce different weights and a different PER. **Until the atom set and weights are pre-registered per entity type, PER is reproducible only against this document's table** — which is why the table is printed rather than the score alone.

**Β is computed by hand.** The operator specifies a difference across a tuple; I compared a qualitative self-assessment against four quantitative operators and reported a mean absolute difference. That is defensible and it is not yet an algorithm.

**Span segmentation is mine.** Five spans from a multi-turn composition; a different segmentation changes DSL. The enclosing span is unambiguous; the two displacing spans are the judgment calls.

**One case calibrates nothing.** Every number here is an existence proof that the stack computes end to end on real evidence. It is not a distribution, and no threshold in this document was set by this document.

---

## SOURCES

Capture `captures/#spxi-protocol-chatgpt-rent-20260814`, EA-WG-CAPTURES-01 v11.0, with its control at the same address. Instruments: PER (#716, #789 hardened), Ω and Π_d and α_T (#157 v3), Β (#788), DSL (laborvector.org), ρ_T (#1464), rent (#449), the magnitude layer (#109).

**Provenance of this document.** Closes W-1. Its substance is §III: the computation disagreed with the scores assigned by eye in three places, one of which — that the institution *was* named first-pass — corrects a factual claim made in EA-SEMRENT-01 and repeated in the capture record. Both should be amended.

