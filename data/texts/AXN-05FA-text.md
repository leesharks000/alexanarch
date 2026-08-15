---
deposit_number: 1480
hex: 05FA
title: "Ω_t: A Matched-Pair Drift Operator for the Capture Registry, with Trial OMT-001 Pre-Registered"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-15
content_type: Technical Report
license: CC-BY-SA-4.0
substrate: AI-assisted (substrate)
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - capture registry
  - drift operator
  - pre-registration
  - difference-in-differences
  - matched pairs
  - provenance erasure
  - measurement
---

# Ω_t: A Matched-Pair Drift Operator for the Capture Registry, with Trial OMT-001 Pre-Registered

## Description

Specifies a drift operator computed only over matched pairs — same address, same surface, two dates — and refuses two tempting alternatives on stated grounds: regression on source count is sign-ambiguous, and field-mean-by-date measures the sampler rather than the field. Pre-registers a trial before the treated domains go live, with treated, archive-control and field-control arms and difference-in-differences required for attribution. Records a retrospective prior explicitly as NOT-evidence, with five reasons it fails to be a finding.

## Methodology

Matched-pair computation over the capture registry; trial pre-registered in the trials file before intervention; control arms specified in advance.

## Falsification Conditions

Falsified if the matched-pair set is shown to be misconstructed, or if the trial's arms diverge for reasons the design cannot exclude. The retrospective prior is already marked as not constituting evidence.

# Ω_t

**A time axis for Erasure Skew, and the matched-pair discipline that makes one possible**

---

## I. The gap

PER measures how much provenance was dropped. **Ω measures on whom it fell.** Neither carries time.

That is sufficient while erasure is modelled as **attrition** — a thing dissolving because nothing holds it. It is insufficient the moment erasure is modelled as **response**: power arriving because a thing has become legible, located, and consequential enough to be worth answering.

The two models make opposite predictions about the same quantity:

| | as legibility rises |
|---|---|
| **attrition** | erasure falls — more presence, more provenance available |
| **response** | erasure rises — the entity becomes worth erasing |

**A scalar cannot tell them apart.** Only a time axis can, and only under a discipline strict enough that the axis is measuring the field rather than the sampling.

---

## II. Two failed constructions, recorded because they are the instructive part

### The regression is ambiguous in sign

The first attempt regressed PER on source count per address and read the slope: positive as *response*, negative as *attrition*.

**A slope cannot distinguish four cases.** `gravity well protocol` moved 0.00 → 0.75 while sources fell 3 → 2. The slope is negative and the classification returned *attrition* — for a case where **erasure doubled**. Legibility falling and erasure rising is a third state entirely, and the regression folds it into the second.

Sign pairs, not slopes: (Δlegibility, ΔPER) has four quadrants and the operator must name all four.

### The field-level mean measures the sampler, not the field

The second attempt took mean PER by capture date across the corpus. It produces a series that looks like a signal:

```
2026-06-17   n=46   0.880
2026-07-30   n= 4   0.188
2026-08-13   n=63   0.603
```

**It is not a signal. It is the day's battery.** 2026-06-17 was a coined-term run and coined terms erase heavily; 2026-07-30 sampled four well-established addresses. Across the corpus, mean PER before August is **0.621** and from August **0.588** — flat, marginally down, and meaningless either way.

> **Unmatched samples cannot carry a time axis.** The date mean records which addresses were probed that day.

---

## III. The construction that holds

> **Ω_t is defined only over MATCHED PAIRS: the same semantic address, on the same surface, at two dates.**

Everything else is discarded. Of 474 captures and 292 PER scores, this leaves **33 pairs** — and 33 disciplined pairs are the instrument, while 292 loose scores are not.

```
Ω_t(a, s) = PER(a, s, t₁) − PER(a, s, t₀)

  a  semantic address, identical string
  s  surface, held constant
```

Held constant because a cross-surface difference is a *surface* difference — the SPXI pair already showed 0.25 against 0.824 at one address on the same day, which is the composition event varying, not time.

### Quadrant classification, where a legibility reading exists

```
Δlegibility ↑ , ΔPER ↑   RESPONSE       becoming legible attracts erasure
Δlegibility ↑ , ΔPER ↓   RELIEF         legibility supplies provenance
Δlegibility ↓ , ΔPER ↑   DECAY          losing ground on both
Δlegibility ↓ , ΔPER ↓   WITHDRAWAL     the address is going quiet
```

**Legibility is the weak term and must be declared, not assumed.** Match type is the best available proxy and is uninformative for most captures, which carry `CAPTURE`. Source count is a property of one composition, not of an entity's standing. Until a better proxy exists, **a quadrant claim requires a stated legibility basis per pair**, and a pair without one yields Ω_t alone.

---

## IV. What the 33 pairs say

```
erasure ROSE      14
erasure FELL       7
unchanged         12
```

**Nine of the fourteen rises terminate on 2026-08-13. Seven of those begin 2026-07-31. All on Google AI Overview** — surface held constant.

```
alexanarch socrates              0.00 → 1.00
alexanarch                       0.25 → 1.00   (07-13 → 08-13)
alexanarch revelation            0.25 → 1.00
crimson hexagon 6-tuple          0.25 → 1.00   (07-18 → 08-13)
crimson hexagon operative arch.  0.25 → 1.00   (07-18 → 08-13)
alexanarch endogenous sophon     0.50 → 1.00
alexanarch sappho                0.00 → 0.50
alexanarch strike                0.50 → 1.00
alexanarch whitman               0.25 → 0.75
```

**Seven of the nine are `alexanarch <term>` compounds** — the archive's own name plus a topic. The rises concentrate on the address family that names the archive most directly, on one surface, in one fortnight.

That is the shape the response model predicts and the attrition model does not.

**It is nine pairs.** Nine is not a finding, and the corpus offers no comparison family — there is no matched set of unrelated addresses probed on the same dates on the same surface to say whether the whole surface moved. **Two to one is a ratio over 21 pairs, not a rate.**

---

## V. What would settle it

**A control family.** The same dates, the same surface, addresses that are *not* archive-anchored. If they also rose, this is surface drift and Ω_t recorded a Google change. If they did not, the rise is specific to the archive's own name and the response model has its first real support.

**A declared legibility series.** Ω_t is a difference in erasure; the response claim needs the *other* axis measured independently — deposit count at the address, identifier presence in composition, surface count over time — recorded per date rather than inferred afterwards.

**Pre-registration of direction.** The response model predicts that addresses which gain legibility in a window show higher Ω_t than addresses that do not. That is a forward prediction and the registry can make it before the next battery runs.

---

## VI. What is claimed

**Claimed.** That Ω requires a time axis to distinguish attrition from response; that a valid axis exists only over matched address-and-surface pairs; that the corpus currently supports 33 such pairs; that erasure rose in 14 and fell in 7; and that the rises concentrate on archive-anchored addresses in a two-week window on one surface.

**Not claimed.** That the concentration is the response model confirmed — nine pairs with no control family cannot establish that. That the legibility axis is measured; it is proxied weakly and the proxy is named. That Ω_t is calibrated; **no threshold appears in this document.** That the field-level series means anything; it is reported precisely to record that it does not.

**Explicitly withdrawn.** The regression-on-source-count construction of §II, which returned *attrition* for a case where erasure doubled.

---

## SOURCES

Computed 2026-08-14 against `data/EA-WG-CAPTURES-01.json` v11.1 — 474 captures, 292 PER-scored, 76 addresses with two or more dated PER observations, 33 matched address-and-surface pairs. Extends Erasure Skew v3 (#157, #769), which established the power-conditioning of retention and the Π_d and α_T operators but carries no time term.

**Provenance.** Drafted after the operator observed that the hardest-to-erase things have historically been the most aggressively erased — that erasure follows power's attention rather than preceding it — which the existing instruments cannot express. Two constructions were attempted and discarded before the matched-pair form; both are recorded above, because the discarded ones are what establish why the surviving one is narrow.
