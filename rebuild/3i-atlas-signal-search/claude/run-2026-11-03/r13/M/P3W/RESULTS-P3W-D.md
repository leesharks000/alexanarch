# RESULTS-P3W-D: validation accepted; the six scans read; one candidate, ON0017 Y+, fails the location rule; no lead

Run 2026-11-21 under PLAN-P3W-D (sha256 b9f5e852…), with p3wd.py (sha256 b0340dc8…) over p3w.py; both hashes checked after the run (FROZEN-P3W-D.sha256). Validation 1,257 s (validationD.json); then the six scans (p3wd_00NN.json) and the reading against the gates (p3wd_gates.json).

## Validation: accepted

| form | 0.25 | 0.5 |
|---|---|---|
| sum within X | p 0.125 | **p 0.025, pair 137–301, 3.14×** |
| difference within X | p 0.10 | **p 0.025, pair 137–301, 3.26×** |
| sum across feeds | p 0.275 | **p 0.025, pair 137–301, 2.73×** |
| difference across feeds | p 0.25 | **p 0.025, pair 137–301, 2.97×** |

| criterion | rule | result | |
|---|---|---|---|
| four forms at 0.5 | each p ≤ 0.05 at the injected pair | all four | met |
| noise only | ≤ 12 of 120 family tests at p ≤ 0.05 | 7 of 120 | met |
| one stationary tone, 5 runs | ≤ 3 of 30 | 2 of 30 | met |
| five tones, same fractional bin, 5 runs | ≤ 3 of 30 | 0 of 30 | met |
| five tones, mixed fractional bins, 5 runs | ≤ 3 of 30 | 0 of 30 | met |
| uncoupled pair at 0.5, 5 runs | ≤ 3 of 30 | 1 of 30 | met |
| burst (reported) | — | X+ 0.05, X− 0.025; the rest 0.1–0.725 | reported |

The steady-tone controls that failed P3W-B and P3W-C are clean without the seam: 2 of 90 tests at p ≤ 0.05 across the three, under the 5% an exact null gives. The burst flags within X, as the plan said it would by construction. 0.25 is not reached by any form in this run (P3W-C reached it once); sensitivity stands at 0.5.

## Reading

1. **One candidate.** Of the 18 ON-scan families on the target slice, one reaches p ≤ 0.05: **ON0017, Y+ (sum form within feed Y), pair 217–293, p 0.05**, score 0.0654 against a surrogate-maximum median of 0.0581 (1.12×) and a surrogate median at the pair of 0.0132. About 0.9 such candidates are expected by chance.
2. **Holdout in time: passed.** Each half of the scan gives the pair on its own: A 0.052, analytic p 0.0038; A 0.056, p 0.0016 (gate ≤ 0.01).
3. **Location: failed.** At the same pair and family, neither adjacent OFF scan stands above its own surrogate maximum (OFF0016 A 0.0078, below its median; OFF0018 A 0.0261 against a maximum of 0.0328). But OFF0018 holds an excess of 0.0138 over its surrogate median, and the ON excess is 0.0522, a ratio of **3.77, under the plan's 4**. The pair's coupling stands in the following OFF pointing at about a quarter of its ON strength.
4. **Control slices quiet at the pair** (ctrl25k A 0.0287 against a maximum of 0.0317; hidrift 0.0100 against 0.0301).
5. **The aggregate is chance.** Across all 108 family tests (6 scans × 3 slices × 6 families), 8 reach p ≤ 0.05 against about 5.4 expected; the chance of 8 or more is 0.17. Five are in ON scans and three in OFF. On the target slice: ON0017 Y+, OFF0016 X−, OFF0018 X+.

**Verdict under the plan: no lead.** The candidate fails gate 3, and no aggregate family test stands out. It is the first candidate the P3W line has produced, and it holds in both halves of the scan; what keeps it from being a lead is that the following OFF pointing carries the same coupling at a quarter of its strength, and a coupling present off the comet is not at the comet.

## What this run establishes

- The two-part signal, in either form, within either feed or across them, at a per-bin amplitude ratio of 0.5 (each component a quarter of its bin's noise power, invisible in power), is absent from C21's first 32 frames in all six scans and three slices, except for ON0017's pair 217–293, which the location test sets aside.
- Steady carriers no longer bias the test.
- Limits as PLAN-P3W gives them: couplings constant over the 32 frames only (a Doppler-drifting third is outside), segments of 512, C21 only.

Products: PLAN-P3W-D.md, p3wd.py, FROZEN-P3W-D.sha256, validationD.json, p3wd_0013–0018.json, p3wd_gates.json and this file, hashed in P3W-D-PRODUCTS.sha256. valD.log, scanD.log and readD.log are the run's console logs and are not hashed.
