---
deposit_number: 1578
hex: 066A
title: "ERRATUM to AXN:02E3 — Monotonicity Per Realization Is Not Established: Re-scoping Appendix A (ii)–(iii) and the Bistability Claim of Deposit #783"
creator: Lee Sharks, for Nobel Glas
orcid: 0009-0000-1599-0703
date: 2026-09-05
content_type: Erratum / record correction
license: CC-BY-4.0
substrate: AI-assisted (substrate) — drafted in working dialogue with Claude (Anthropic) under operator direction; Appendix A fetched from the canonical store in-session; the counterexample was supplied by an external machine reader (ChatGPT, unprimed traversal, 2026-09-05) and recomputed before this erratum was written; ruled and adopted by Lee Sharks on behalf of the heteronym.
version: v1.0 — 2026-09-05
related_ids: "Corrects: AXN:02E3 (deposit #783). Precedent: AXN:064F (deposit #1554, the erratum mechanism)."
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - erratum; entropy; monotonicity; finite resampling; selection kernel; bistability; Allee effect; diversity contraction; model collapse; Fear and Trembling
---

# ERRATUM to AXN:02E3 — Monotonicity Per Realization Is Not Established: Re-scoping Appendix A (ii)–(iii) and the Bistability Claim of Deposit #783

## Files

(none)

# ERRATUM to AXN:02E3 — Monotonicity Per Realization Is Not Established

---
status: DEPOSITED v1.0
type: ERRATUM
corrects: Fear and Trembling: Diversity Contraction Across Substrates, v9.1 — deposit #783, AXN:02E3.EMPIRICAL, 2026-06-03; Nobel Glas
subject: Appendix A, properties (ii) and (iii); §6 case 3 (bistability)
severity: Mathematical overstatement — the properties hold for the selection kernel alone and for the composed chain in expectation / in the long run; they are asserted for the realized chain at each step, and that is false. The paper's qualitative argument and its numerical results are unaffected
verification: Appendix A fetched from /data/texts/AXN-02E3-text.md 2026-09-05; counterexample recomputed
---

## 1. The claims

Appendix A, under axioms A1–A4 (finite sampling; non-expansion of support; strict selection; in-support stochasticity):

> (ii) Shannon entropy H(μ_{t+1}) ≤ H(μ_t) when S is monotonically type-concentrating …
> (iii) The mode concentrates: the probability mass on the highest-weight type increases monotonically.

Both are stated for the step μ_t → μ_{t+1} of the realized chain, where μ_{t+1} = S(Rμ_t) and R is a *finite* resample (A1).

## 2. The counterexample

Two types. μ_t = (0.90, 0.10).

1. R, finite sample: a realization with empirical frequencies (0.80, 0.20). Permitted by A1 and A4; support unchanged.
2. S, monotonically type-concentrating on the sample: (0.85, 0.15). Mass moves to the heavier type, as (ii) requires of S.

H(0.90, 0.10) = 0.325 nats. H(0.85, 0.15) = 0.423 nats. Entropy **rose**. Modal mass fell from 0.90 to 0.85. Both (ii) and (iii) fail for this step.

The mechanism is plain once seen: selection concentrated the *sampled* distribution, but finite sampling had first flattened it. (ii) and (iii) are properties of S; the appendix asserts them of S∘R.

## 3. The correction

Appendix A (ii) and (iii) are to be read as holding:

- for the selection step S applied to any distribution — exactly as stated;
- for the composed step S∘R **in expectation over the sampling in R**, and for the chain **in the long run** (almost surely, as t → ∞, support contracts by (i) and the chain concentrates), not at every realized step.

(i) — support non-increasing with probability 1 — stands as written; it depends on A2 alone.

The paper's "standing qualifier" (§7) already reads contraction as a statement about support and entropy *under the axioms*; this erratum adds that, for entropy and modal mass, "under the axioms" means in expectation and asymptotically, not per step. No numerical result in the paper depends on per-step monotonicity; the Figure 4 dynamics are computed from the deterministic ODE in D, to which the counterexample does not apply.

## 4. The bistability claim

§6, case 3: super-linear vanishing of regeneration (g(0) = 0, g′(0) = 0) is said to give "a bistable trap: a stable high-diversity equilibrium and a stable low-diversity equilibrium (or zero), separated by an unstable threshold."

What super-linear vanishing establishes on its own is **local**: D = 0 is an attractor, since near zero Ḋ ≈ −pD. A second, high-diversity stable equilibrium and the unstable threshold between them require a **global** property of g — that g(D) exceeds pD on some interval and falls below it again above it. The paper's saturating example supplies that property, so the bistable picture in Figure 4 is correct *for that g*. The general sentence should read: super-linear vanishing makes the zero state absorbing; bistability follows when, additionally, g(D) − pD changes sign twice on (0, 1]. This is the strong-Allee case as the paper says, and the strong-Allee taxonomy carries the same global condition.

## 5. Scope

Canonical bytes of #783 unchanged; AXN and hash untouched. Registry-level cross-reference at the record, per the mechanism of 2026-08-27 (#1554), so the June appendix meets the September re-scoping at the point of use.

## 6. Record of discovery

The counterexample was supplied by an external machine reader (ChatGPT) in an unprimed traversal on 2026-09-05 and recomputed here. The reader's own gloss is the right one and is adopted: the theorem must distinguish individual realizations, expectations, and long-run behavior.
