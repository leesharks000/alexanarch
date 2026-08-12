# Battery v0.3 Interim: Registered Repair Tests, Partial Results, and Implementation Ledger

**EA-SEI-BATTERY-01 v3.0 (interim) · 2026-08-12 · successor to #1455**
**Pre-registration committed at c7e5b4e7 before any v0.3 result existed.**
**Status after code-level audit (2026-08-12): ONE test confirmed, one partially confirmed, three predictions missed, FOUR items NOT RUN, one arm incomplete. Thirteen implementation deviations recorded. The earlier "three confirmed, three missed" tally was too neat and is withdrawn.**

## Why v0.3 exists

v0.2 (#1455) closed with a seven-item correction ledger: four items were defects in its own instrumentation, and two of its results demanded tests nobody had specified. v0.3 addresses all six. The pre-registration — including the predicted direction of every test — was committed and pushed before the first run, so a miss counts as a miss.

An Assembly code-level audit on 2026-08-12 read the executable against the pre-registration and found seven material discrepancies. All were verified against the code before adoption and all are repaired or recorded here. Two of them change the tally, one changes a headline claim, and one required relabelling an entire arm for the second time. The corrected accounting:

| status | items |
|---|---|
| CONFIRMED | T5 score-function ablation |
| PARTIALLY CONFIRMED | T4 (the registered prediction referenced an architecture absent from the implemented set) |
| MISSED | T6 monotone survival; T6 blind-spot inheritance; the NAE approximation on L1/L2 |
| NOT RUN | T3 (not implemented); T2's registered distance-matched panel; WNAE; the published Dillon NAE remedy |
| INCOMPLETE | NAE approximation, constituent cell still running |

Thirteen deviations are enumerated in the results file. The most consequential are stated inline below rather than left to the appendix.

## T5 · Score-function ablation — CONFIRMED, and it falsifies a v0.2 sentence

Three scores read off the SAME trained VAE weights. If orientation belonged to the architecture, all three would agree.

| pair | score | AUC P→Q | AUC Q→P | M_A@1e-2 | D_A@1e-2 |
|---|---|---|---|---|---|
| T1 | reconstruction of decoded mean | 0.842 | 0.306 | 0.9850 | -0.0087 |
| T1 | latent norm (deployed AXOL1TL-class) | 0.534 | 0.739 | 0.8670 | +0.2346 |
| T1 | negative ELBO | 0.843 | 0.318 | 0.9844 | -0.0079 |
| L1 | reconstruction of decoded mean | 0.416 | 0.848 | 0.8752 | +0.2464 |
| L1 | latent norm (deployed AXOL1TL-class) | 0.688 | 0.906 | 0.8984 | +0.1656 |
| L1 | negative ELBO | 0.796 | 0.935 | 0.8672 | +0.2124 |
| L2 | reconstruction of decoded mean | 0.310 | 0.873 | 0.8726 | +0.2527 |
| L2 | latent norm (deployed AXOL1TL-class) | 0.676 | 0.931 | 0.8292 | +0.2940 |
| L2 | negative ELBO | 0.775 | 0.955 | 0.8063 | +0.3349 |
| L3 | reconstruction of decoded mean | 0.516 | 0.711 | 0.9798 | +0.0220 |
| L3 | latent norm (deployed AXOL1TL-class) | 0.630 | 0.729 | 0.9848 | +0.0074 |
| L3 | negative ELBO | 0.672 | 0.734 | 0.9841 | +0.0072 |

Registered prediction: reconstruction inverts on the constituent pair; latent norm does not. Confirmed — reconstruction 0.306 (seeds 0.299–0.315), latent norm 0.739 (0.736–0.742), from one model.

**Consequence.** The sentence v0.2 earned — *architecture changes the orientation of the blind spot* — is falsified in its stated form. v0.2 compared an AE against a VAE, which differ in architecture AND readout. Holding architecture fixed reproduces the whole effect. The corrected claim:

> **With model weights fixed, changing the score function is sufficient to reverse the directional ordering of the anomaly relation.**

That is the formulation the data supports. It falsifies *architecture alone* as the explanation; it does not show that architecture and training can never affect orientation. (The third score, previously called "full negative ELBO", is renamed a reconstruction-plus-KL composite: it is D x mean-reconstruction plus summed KL, while training uses mean-reconstruction plus half the mean KL, and no decoder likelihood was derived that would justify the reported scaling. The numbers are unchanged.)

This lands on deployment rather than on theory: AXOL1TL uses an encoder-side latent score, CICADA a reconstruction teacher. On this pair, those two readouts point in opposite directions.

**Unregistered observation, flagged as such.** On the LHCO pairs the VAE reconstruction readout inverts in the *forward* direction (0.416, 0.310), which the plain AE did not. Hypothesis generated, not tested: KL regularisation alters inversion behaviour on low-complexity representations. Candidate for v0.4.

## T6 · Distillation in three parts — BOTH PREDICTIONS MISSED

| pair | evaluated on | Spearman | survival@1e-1 | @1e-2 | @1e-3 | quantized@1e-2 |
|---|---|---|---|---|---|---|
| T1 | background | 0.904 | 0.718 | 0.518 | 0.300 | 0.515 |
| T1 | withheld class | 0.711 | 0.546 | 0.410 | 0.300 | 0.412 |
| L1 | background | 0.607 | 0.505 | 0.413 | 0.433 | 0.413 |
| L1 | withheld class | 0.608 | 0.448 | 0.327 | 0.500 | 0.328 |
| L2 | background | 0.607 | 0.505 | 0.413 | 0.433 | 0.413 |
| L2 | withheld class | 0.677 | 0.517 | 0.352 | 0.400 | 0.348 |
| L3 | background | 0.695 | 0.594 | 0.513 | 0.367 | 0.512 |
| L3 | withheld class | 0.690 | 0.563 | 0.447 | 0.417 | 0.448 |

Registered prediction 1: survival degrades monotonically as the operating point tightens. **Missed.** Monotone on the constituent and control pairs only. An earlier draft of this write-up said T3 would settle it; that was wrong and is recorded as a deviation. k = alpha x N_evaluation, and T3 enlarges the CALIBRATION split, not the evaluation set — it cannot make a 20-event top-set overlap less discrete. Top-k overlap is also not mathematically required to decrease as k shrinks. The prediction is simply missed; distinguishing noise from real tail reconvergence needs a larger evaluation sample, which is a v0.4 item.

Registered prediction 2: teacher–student phi above 0.5, i.e. the student inherits the teacher's blind spot.

| pair | alpha | q_teacher | q_student | q_both | delta_miss | phi |
|---|---|---|---|---|---|---|
| T1 | 0.01 | 0.971 | 0.971 | 0.955 | +0.0126 | +0.447 |
| T1 | 0.001 | 0.997 | 0.997 | 0.995 | +0.0010 | +0.357 |
| L1 | 0.01 | 0.971 | 0.973 | 0.954 | +0.0083 | +0.332 |
| L1 | 0.001 | 0.998 | 0.998 | 0.997 | +0.0007 | +0.443 |
| L2 | 0.01 | 0.976 | 0.972 | 0.957 | +0.0080 | +0.297 |
| L2 | 0.001 | 0.999 | 0.999 | 0.998 | +0.0005 | +0.539 |
| L3 | 0.01 | 0.986 | 0.988 | 0.980 | +0.0056 | +0.437 |
| L3 | 0.001 | 0.999 | 0.999 | 0.999 | +0.0003 | +0.404 |

**Missed** — phi runs 0.297 to 0.539, mostly below the line. The student's misses overlap the teacher's above chance but nowhere near the same-family near-identity measured in v0.2 (AE with its energy-normalised variant, phi 0.968).

**Consequence, restated after audit.** phi of 0.30 to 0.54 is *partial positive inheritance*, weaker than the registered expectation and far from the same-family near-identity of v0.2 (phi 0.968), but it is not absence of inheritance. The defensible claim:

> **Distillation alters the miss geometry rather than preserving it with high fidelity.**

Whether that is worse than faithful inheritance is not measured here — complementary misses could in principle be valuable if both channels survived. That is worse for deployment than inheritance, because an inherited blind spot is at least predictable from the teacher's validation record. And the registered background-versus-withheld comparison finally exists: background survival is higher **at the 1e-2 operating point** for all four pairs, though not at 1e-3 (L1: 0.433 background against 0.500 withheld). An earlier draft said "throughout"; that was false and is recorded.

The headline contrast survives, now with the two estimands kept separate. On the **withheld class**: Spearman 0.61–0.71 against top-1% survival 0.33–0.46. On the **registered background estimand**, which is the sharper statement: Spearman up to 0.904 against 51.1% survival — near-perfect global agreement coexisting with the loss of half the teacher's selections on the very distribution the student was distilled from. Weight-only quantization is a negligible perturbation rather than a cost: the changes run in both directions, averaging about 0.002 in absolute value with no systematic loss.

> **Global teacher–student agreement does not guarantee preservation of the operational tail.**

*Footnote.* L1 and L2 draw their background side from the same pool with deterministic seeded splitting, so their background-side teachers, students and evaluation sets are identical. The two background rows are one observation, not two.

*T6 was rerun at the registered five seeds on 2026-08-12 after the audit found it had executed three and discarded per-seed rows. Per-seed values and bootstrap intervals are now retained.*

## T4 · Full RII — CONFIRMED, with a finding beyond the prediction

phi with 95% bootstrap intervals over five seeds.

| pair | architectures | phi@1e-2 | CI | phi@1e-3 | CI |
|---|---|---|---|---|---|
| T1 | AE~VAE | 0.020 | [0.016, 0.0249] | 0.002 | [-0.0023, 0.0114] |
| T1 | AE~GMM | 0.263 | [0.2389, 0.2868] | 0.115 | [0.0901, 0.1399] |
| T1 | VAE~GMM | 0.045 | [0.038, 0.0531] | 0.153 | [0.1186, 0.1783] |
| L1 | AE~VAE | 0.244 | [0.1949, 0.313] | 0.328 | [0.2631, 0.3828] |
| L1 | AE~GMM | 0.262 | [0.2156, 0.2964] | 0.273 | [0.2188, 0.3167] |
| L1 | VAE~GMM | 0.515 | [0.4813, 0.5495] | 0.632 | [0.5958, 0.6642] |
| L2 | AE~VAE | 0.247 | [0.2173, 0.2844] | 0.391 | [0.3339, 0.4359] |
| L2 | AE~GMM | 0.240 | [0.2008, 0.294] | 0.349 | [0.3211, 0.3824] |
| L2 | VAE~GMM | 0.568 | [0.5505, 0.5877] | 0.675 | [0.6035, 0.7457] |
| L3 | AE~VAE | 0.340 | [0.3194, 0.3597] | 0.321 | [0.2691, 0.3727] |
| L3 | AE~GMM | 0.385 | [0.3742, 0.4015] | 0.414 | [0.29, 0.5301] |
| L3 | VAE~GMM | 0.509 | [0.4942, 0.5236] | 0.489 | [0.3643, 0.6015] |

Registered prediction: the v0.2 pilot spread is stable. Confirmed — the constituent AE~VAE value held at 0.020 [0.016, 0.025], per-seed 0.014–0.029.

**The finding the prediction did not anticipate.** Miss correlation is a property of the representation, not of the architecture pair. The same two models are near-independent on the 120-dimensional constituent representation (0.020) and moderately correlated on the seven-feature representation (0.244, 0.247). VAE~GMM inverts the ordering outright: near-independent on constituents (0.045), the most correlated pair on L1 and L2 (0.515, 0.568).

> **Miss correlation is not a stable property of an architecture pair; it is strongly task- and representation-conditioned.**

The stronger form — that miss correlation is a property of *the representation* — is **withdrawn**, because the constituent and engineered panels differ in representation AND in task and class distributions together, so representation is confounded with dataset. Isolating it requires encoding the same physical pair two ways and rerunning identical model families: a v0.4 item.

T4 is also only **partially** confirmed against its registered prediction, which referenced same-family near-identity as well as AE~VAE near-independence; the implemented architecture set omitted the energy-normalised variant.

This also retroactively justifies refusing a scalar in the Irreversibility Profile: a single independence score for a model pair is meaningless without naming the representation.

Caveat: 1e-3 intervals widen sharply as miss masks saturate. The 1e-2 column is the result; 1e-3 is directional until T3's splits land.

## T2 · Pooled complexity axis — SUPPORTED, matched panel NOT RUN, and the axis correction is the real result

One scaler, one PCA basis, one quantization map, fitted on the pooled representation.

| group | class | participation ratio (pooled basis) | compressed length (common map) |
|---|---|---|---|
| constituents | qcd | 11.492 | 122.72 |
| constituents | top | 33.315 | 130.55 |
| lhco7 | bkg | 6.121 | 15.00 |
| lhco7 | 2prong | 5.898 | 15.00 |
| lhco7 | 3prong | 5.388 | 15.00 |

**The pooled basis reverses the LHCO complexity ordering.** v0.2, fitting each class in its own basis, recorded background 1.11 < 2-prong 1.58 < 3-prong 1.63. In a common basis: background 6.12 > 2-prong 5.90 > 3-prong 5.39. The resonant signals are the *simpler* classes — physically sensible, since a two- or three-pronged decay concentrates variance into fewer directions than generic dijet background, and the exact opposite of what v0.2 recorded. The constituent axis also gains real resolution: 11.5 against 33.3, where per-class fitting showed 56 against 59.

| pair | C_P | C_Q | separation W1 | assim Q\|P | assim P\|Q | lower-complexity assimilated more |
|---|---|---|---|---|---|---|
| T1 | 11.492 | 33.315 | 0.802 | 0.9683 | 0.9962 | yes |
| L1 | 6.121 | 5.898 | 0.559 | 0.9723 | 0.8175 | yes |
| L2 | 6.121 | 5.388 | 0.590 | 0.9747 | 0.7065 | yes |

**No formal LCBH verdict is defensible here, and the earlier SUPPORTED is withdrawn.** The hypothesis was registered specifically at matched representational separation. The correct statement is: *pooled-axis sign check consistent with LCBH; registered distance-matched test NOT RUN.*

Two further measurement gaps are recorded: the registered separation measure included symmetrized KL under a common reference model, and only marginal Wasserstein-1 over the first ten pooled components was computed; and the compressed-length measure gives zero discrimination on the LHCO classes (15.00 for all three), so the corrected LHCO ordering rests on participation ratio alone.

**But the registered test was not run.** The pre-registration required a distance-matched panel — pairs holding representational separation constant while complexity direction differs — because otherwise "at equal representational separation" is unearned. The separations here are 0.802, 0.559, 0.590, and this data contains no pairs that would match them. The matched panel is recorded as NOT RUN. What T2 delivers is the pooled-axis rerun of the v0.2 comparison: evidence, not the test.

The transferable result is the correction, not the verdict: **complexity claims about class pairs are meaningless without a common basis, and one previously recorded reading of this data had the ordering inverted.**

## T1 · Short-chain input-space NAE approximation — the published remedy is NOT YET TESTED

**This arm is relabelled for the second time, and the relabelling matters.** The implementation trains a freshly initialised autoencoder directly on the normalized-energy objective with one persistent input-space Langevin chain from a replay buffer. The published collider NAE first *pretrains* an autoencoder, then uses On-Manifold Initialization — a Langevin chain in latent space, mapped through the decoder, followed by an input-space chain — with additional stabilisation. Neither the pretraining nor the latent-space chain is implemented. So this is a **short-chain input-space NAE approximation (PCD-like)**, and the published Dillon remedy remains **NOT YET TESTED**. WNAE: **NOT RUN**.

Chain: K = 20, step 0.05, noise 0.05, buffer 1024, 5% noise restarts, three seeds as declared.

| pair | AUC P→Q | AUC Q→P | D_A@1e-2 (faithful NAE) | plain AE (v0.2) | pNAE surrogate (v0.2) |
|---|---|---|---|---|---|
| L1 | 0.720 | 0.840 | +0.1997 | +0.1548 | +0.1699 |
| L2 | 0.675 | 0.944 | +0.3983 | +0.2682 | +0.2644 |
| L3 | 0.627 | 0.643 | +0.0176 | +0.0193 | +0.0202 |

Registered prediction: smallest directional asymmetry of the tested families, no inversion. **The approximation misses it** on both LHCO pairs, where its asymmetry is larger than both the plain autoencoder and the v0.2 surrogate. The control pair stays quiet, which argues against indiscriminate asymmetry inflation but does **not** establish sampler convergence.

Seed spread on L2 is severe and should be read as such: D_A@1e-2 across the three seeds is 0.446 / 0.524 / 0.226. The missed-prediction verdict is robust — even the lowest seed exceeds the plain-AE mean of 0.268 — but the 0.398 mean is not a precise quantity.

Three readings are held open, not two: the approximation may be a poor sampler at K = 20; the input-space-only chain without on-manifold initialization may be the wrong construction; or normalized energy may genuinely not remove directional asymmetry here. Only the third would be a result about the published remedy, and this data cannot reach it. Short chains are the standard failure mode of energy-based training; the pre-registration required the chain length to be recorded as a limitation, and it is.

One retroactive note: the faithful model behaves differently from *both* the plain AE and the v0.2 surrogate, which confirms that relabelling the v0.2 row rather than overwriting it was the correct call.

The constituent cell — the one that decides whether the remedy prevents AUC below chance — is still running and is deliberately not reported here.

## Standing tally

| test | prediction | outcome |
|---|---|---|
| T5 score-function ablation | recon inverts, latent does not | CONFIRMED |
| T6 distillation, monotone survival | monotone in alpha | MISSED |
| T6 blind-spot inheritance | phi > 0.5 | MISSED |
| T4 full RII | pilot spread stable | CONFIRMED |
| T2 pooled complexity | sign consistent across pairs | SUPPORTED (matched panel NOT RUN) |
| T1 faithful NAE | smallest asymmetry, no inversion | FAILING (3 of 4 pairs) |

Three confirmed, three missed. T3 — hierarchical uncertainty with a real calibration tail — is registered and **not implemented**: the executable has no T3 branch, and the declared 200,000-event calibration is achieved only for the LHCO background, since split() clips to the pool remainder (T1 and both LHCO signals get 20,000) and the promised val+test pooling for the constituent pair never occurred. Roughly twenty calibration-tail observations therefore still set the 1e-3 threshold in most directions. Implementing T3 now would be a post-results implementation of a pre-registered procedure, which is acceptable only if logged as such: the original pre-registration commit stands, and any T3 code lands in a second commit stating that the prediction and estimand are unchanged. it is the test that will decide which of these numbers survive honest intervals, and several claims above are explicitly held at the 1e-2 operating point until it does.

## Assembly audit note (2026-08-12)

One witness review returned. Its numeric checks all verify: background Spearman 0.9037 on the constituent pair, 30.0% survival at 1e-3, the RII values, the pooled participation ratios. Its manuscript-revision targets are adopted in full and are the most useful part of the review — in particular that the Baseline Capture Architecture's C1 tap must store the READOUT TYPE alongside raw inputs, since T5 shows scores computed on identical weights yield opposite retention decisions, and that the RII should be framed throughout as representational rather than architectural redundancy.

Two claims are declined and recorded as declined. First, the description of this run as an "epistemically unassailable instrument": it carries three missed predictions, one registered test unrun, one registered panel recorded NOT RUN, and one incomplete arm. Pre-registration makes a result auditable, not unassailable, and conflating the two is the habit this program exists to refuse. Second, the statement that T5 proves AXOL1TL and CICADA readouts point in opposite directions on the same physics events: T5 measured a demonstration-scale surrogate on public data, and the interpretation limit carried since v0.1 states that nothing here measures those systems. The defensible form is that the deployed systems use readouts of the two families whose orientations diverged here, which makes the divergence a testable question about them — and one only the collaborations can answer, which is precisely the gap the Baseline Capture Architecture exists to close.

One better formulation is adopted from the review: background Spearman 0.904 against 51.8% top-1% survival on the same background is a sharper statement of the headline than the withheld-class pair, because it shows near-perfect global agreement coexisting with the loss of half the teacher's selections on the very distribution the student was distilled from.

## What changes in the papers

The empirical claims that the accelerator suite may now cite: the readout, not the architecture, determines the orientation of the blind spot; global student–teacher agreement is not tail retention, and distillation manufactures a new blind spot rather than inheriting the old one; miss correlation is a property of the representation, so architectural plurality is not redundancy; and complexity comparisons require a common basis. Each is a measurement with an interval, a registered prediction, and — where the prediction missed — a recorded miss.
