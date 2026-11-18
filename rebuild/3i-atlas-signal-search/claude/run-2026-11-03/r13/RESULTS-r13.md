# RESULTS-r13: the thirteen again, under the cautions of 2026-11-18

Plan: PLAN-r13.md, v1 (sha256 8378dd33…) and v2 (16236a7d…), both in PLAN.sha256, frozen before any spectrum of this rerun was read. Code run_r13.py, fg.py, telemetry.py and f_check.py (CODE.sha256). Results in r13.json, F.json, F_check.txt, G.json, telemetry.json. Completed 2026-11-18.

## The gate

V0, all rows, comet frame: **13** true-frame clusters, against false frames 3.75 ± 2.05 (maximum 8). This is the original result, reproduced exactly. Passed.

## Result

**The thirteen's excess depends on the first rows of each scan.** Part A cuts the off-target time, and the count falls to the null.

| Variant | T | swap | false μ ± σ | max | d_max | exceeds | best line S | S rank of 41 |
|---|---|---|---|---|---|---|---|---|
| V0 all rows | 13 | 1 | 3.75 ± 2.05 | 8 | 6 | yes | 3.02 | 3 |
| V1 row 0 dropped in every scan | 7 | 5 | 2.85 ± 1.64 | 7 | 5 | no | 2.80 | 10 |
| V2 telemetry's off-target rows dropped | 5 | 5 | 3.17 ± 1.84 | 6 | 4 | no | 2.63 | 31 |

- **What V2 dropped.** From the voltage headers (A): 0013 row 0; 0014 rows 0–1; 0015 rows 0–1; 0016 rows 0–2; 0017 rows 0–1; 0018 row 0. The TRACK onset falls 0–2.1 s into each scan, and once tracking the pointing wobble stays at or below 0.81 arcmin, against a beam of about 7.4 arcmin.
- **The coordinates, one by one.** With all rows, each of C01–C13 has its smallest ON z at or above 2.5. With row 0 dropped, 11 of the 12 that are not interference fall below 2.5; only C05 holds in both cuts (2.71, 2.57). C01, the fixed-tone interference, holds in V1.
- **How large the drop is.** Removing one row of 49 should lower a steady tone's z by about 1 percent. These coordinates fall by about 20 percent. Their power sits disproportionately in each scan's first 6 s.
- **A rank that means nothing.** Each coordinate ranks 1 of 41 in B2 under every variant. That rank is selection, because the thirteen were chosen in the true frame, and it is not read.

**Reading under the plan's rule.** V1 and V2 bring T to or below its own false maximum, so the excess depends on off-target time. The thirteen behave as start-of-scan events, not as a tone fixed on the comet. What produces power at the start of each scan that aligns in the comet frame across the three ON scans is not determined here. Candidates are slew and settling, scan-start transients in the backend, and the first integration's partial content.

## The other parts

**Strength (B1).** The strongest comet-frame line, z = 3.02 in its weakest ON scan, ranks 3 of 41 (V0). The thirteen are a count excess, not a strong line.

**Beyond steady emission (I).** No statistic exceeds its false frames, in V0 or V2.

| Statistic | V0: T | V0: false max | V2: T | V2: false max |
|---|---|---|---|---|
| I1, one strong ON scan | 15 | 18 | 14 | 18 |
| I2, two of three ON scans | 36 | 49 | 41 | 44 |
| I3, single-row bursts | 61 | 74 | 61 | 72 |

**Wider signals (K).** No width exceeds.

| Kernel | V0: T | V0: false μ | V0: false max | V2: T | V2: false μ | V2: false max |
|---|---|---|---|---|---|---|
| 25 Hz | 3 | 1.35 | 6 | 3 | 1.25 | 3 |
| 92 Hz | 0 | 0.45 | 2 | 0 | 0.23 | 2 |

**Injection calibration (C).** Twenty comet-tracking tones were injected into the three ON scans, each one bin wide, with A in units of the scan's per-row robust σ.

| A | Recovered of 20 | Best line S | S rank of 41 |
|---|---|---|---|
| 0.25 | 0 | 3.02 | 3 |
| 0.5 | 1 | 3.13 | 3 |
| 1 | 16 | 4.87 | 1 |
| 2 | 20 | 8.62 | 1 |
| 4 | 20 | 16.74 | 1 |

Half recovery falls between A = 0.5 and A = 1, and the strength rule trips by A = 1. The thirteen's smallest-ON z of 2.5–3.0 matches A ≈ 0.5, the detector's floor.

**Other frames (D).** None exceeds.

| Frame | V0: T | V0: false max | V0: S rank | V2: T | V2: false max | V2: S rank |
|---|---|---|---|---|---|---|
| sign-flipped | 2 | 7 | 13 | 5 | 9 | 20 |
| geocentric | 7 | 8 | 14 | 7 | 11 | 17 |
| barycentric | 6 | 9 | 34 | 4 | 7 | 37 |
| topocentric (reference) | 3 | 10 | 17 | 2 | 9 | 30 |

The comet frame with all rows is the only frame with an excess.

**Ephemeris (E).** JPL solution #55 (Soln.date 2026-Oct-21). Moving a tone one channel across the 1,883 s cadence needs an acceleration error of 2.7e-7 km/s², 24 times smaller than the smallest false frame (6.3e-6 km/s²). The ephemeris is not a factor.

**Aggregate rank across channels (F, F_check).** These use stored rows only.
- *L band.* In 12 of the 63 surveyed channels other than the thirteen's, the true frame ranks in the top 4 of 41, against 6.1 expected (binomial p ≈ 0.018).
- *S, C and X.* 4 of 64, against 6.2 expected.
- *The null is not exchangeable.* False frames with small offsets rank systematically higher (Spearman ρ between |offset| and mean rank: 0.74 in L band, p ≈ 6e-8; 0.40 in S/C/X).
- *Against the nearest frames.* The L-band true frame is 7th of 41 by mean rank, behind false frames at −0.06, 0.10 and −0.11 Hz/s. The L-band aggregate excess is the procedure's, not the comet's.
- *The thirteen's channel by distance.* It gave 13 against at most 8 among the twelve nearest frames. That was its all-rows standing, which part A has now removed.
- *A deviation.* The two L-band sets in F.json were tie-broken separately, so they report 14 and 12; F_check uses average ranks.

**Twin independence (G).** In all twelve C/X twin pairs the relative-noise correlation is 0.64–0.98. No pair is byte-identical. No twin is independent, so twins are not a replication route.

## Deviations

- **The block time.** It is 0.179 s, not the 0.0447 s that v1 of the plan states. The telemetry sampling was every 4th block in file 0000 and every 32nd after, as planned.
- **Out-of-memory kills.** Part C, the injection, was killed once and moved per scan into the preparation step, with the arithmetic unchanged (CODE.sha256 logs the new hash). Part D was killed once and resumed in a fresh process. Each part is saved before the next begins.
- **F_check came after F.** It was written after F's result, to test the null. It is a check, not a part of the plan.

## Not run yet

Part H (strength, intermittency and injection on twelve S/C/X channels) has its runner written (run_h.py, hashed) and has not been run. Part J (comet-referenced voltage tests against 400 false frames) is not yet written.

## What this changes

The notebook (#1742) holds the thirteen as a below-threshold comet-frame excess that survives every null tried. Under the off-target row cut it does not survive. How the notebook takes this in is the operator's ruling.
