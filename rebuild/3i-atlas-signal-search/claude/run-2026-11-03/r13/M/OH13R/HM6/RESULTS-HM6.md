# RESULTS — HM6: the first pair on three tracks, and the OH line in each feed

22 November 2026. Plan: PLAN-HM6.md, frozen before any product (FROZEN-HM6.sha256, commit c626da32a). No amendment. Outputs: hm6_0013.npz/.json, hm6_0014.npz/.json, hm6_score.json; logs hm6-0013.log, hm6-0014.log, hm6-score.log. Both scans ran concurrently (with HMR1 at low priority) and finished within the time limit; nothing was resumed.

## Reproduction: passed

Track c reproduces HM5 exactly for D3 and power, in X and in Y, per coordinate and per cohort (X D3 1.29399, X power 1.09298, Y D3 0.03769, Y power 0.18844). Everything below was read only after this check.

**Separability.** The comet's drift across the scan is 11.65–11.67 native bins at every coordinate, above the plan's floor of 2, so the three tracks separate at all eleven.

## A. Comet's drift, or fixed at the dish (path 1)

| X | track c (comet drift) | track d (dish-fixed) | track f (drift mirrored) |
|---|---|---|---|
| D3 cohort score (rank /380) | 1.294 (1) | 0.289 (120) | 0.503 (43) |
| D3 comet mean rank, ON / OFF | 0.78 / 0.39 | 0.43 / 0.34 | 0.57 / 0.42 |
| power cohort score (rank /380) | 1.093 (20) | 0.188 (121) | −0.641 (347) |
| power, C08–C11 mean ON − OFF rank | 0.80 | 0.31 | −0.39 |

1. **X D3 follows the comet.** By the rule stated in advance (PLAN §3), the cohort's rank on track c (1st) is better than on both d (120th) and f (43rd).
   - Held fixed at the dish, the contrast falls into the body of the false cohorts. Mirrored, it falls further than the false 95th percentile.
   - The ON scan's rise on the comet's coordinates (mean rank 0.78) is there only on the comet's own drift.
2. **X power at C08–C11 follows the comet.** The C08–C11 mean on c (0.80) is greater than on d (0.31) and f (−0.39).
   - Coordinate by coordinate, C09 is the exception: on d it stands at 1.00, above its c value of 0.83. C09's power excess is at least as strong fixed at the dish as on the comet's drift.
   - C08 holds 0.75 on d against 1.00 on c. C10 and C11 drop to 0.25 and −0.75.
3. **The readings excluded.**
   - A fixed-frequency feature, from interference or from the receiver chain at one frequency, gives d ≥ c. That is not what the cohort shows in X D3 or in X power.
   - It is what C09 shows in power.
4. **One observation, stated as observation.** The false cohorts' power contrast (not their D3) is biased upward on track c (false mean 0.44, HM5 §D) and not on d (−0.01) or f (−0.02). The ON scan's general brightening on drifting tracks, noted in HM5 as the session's lowest-elevation effect, is a property of drifting windows, not of fixed ones. The comet cohort's rank is read against the false cohorts on the same track, so the comparison in item 1 carries the bias on both sides.

## B. The OH 1667.359 MHz line in each feed (path 2)

| | centre (σ) | controls at or below (/40) | control range | scatter (fraction of system power, per 2.8 kHz) |
|---|---|---|---|---|
| comet frame, X | +0.47 | 34 | −1.14 to +0.97 | 1.7 × 10⁻³ |
| comet frame, Y | −1.55 | 0 | −1.06 to +1.54 | 1.1 × 10⁻³ |
| comet frame, X + Y | −0.31 | 11 | −1.33 to +0.85 | 9.6 × 10⁻⁴ |
| dish frame, X | +0.33 | 32 | −1.11 to +0.97 | 1.8 × 10⁻³ |
| dish frame, Y | −1.81 | 0 | −1.23 to +1.82 | 9.6 × 10⁻⁴ |
| dish frame, X + Y | −0.41 | 8 | −1.35 to +0.87 | 9.3 × 10⁻⁴ |

5. **No line.** By the rule stated in advance (|centre| ≥ 3 and beyond all 40 controls in the comet frame), neither feed shows the comet's OH 1667 line, in emission or absorption.
   - Y's centre is below every control in both frames, at −1.55σ and −1.81σ. That is a dip of about 1.7 × 10⁻³ of the system power, far under the threshold, and it is as deep in the dish frame as in the comet frame. A comet line would favour the comet frame.
   - X sits above the middle of its controls.
6. **Sensitivity.** Three sigma is about 3–5 × 10⁻³ of the system power per 2.8 kHz in a single ON–OFF pair. That is the absorption calibration's floor (RESULTS-absorb-calib, three pairs in total power) at the noise of one pair.
7. **What it settles for C08–C11, as the plan said in advance.** The OH line is not seen in either feed. So it gives no wing for C08 or C09 to sit on, and it never bore on C10 or C11 (328 and 636 kHz away).

## What the result is

1. **The conventional reading first.**
   - The first pair's X contrast is not a fixed-frequency feature. D3 and the C08–C11 power both belong to the comet's drift and fade when the windows are held at the dish or given the mirrored drift. Interference at a fixed frequency, or a property of the X chain at a fixed frequency, would not do that.
   - The comet's natural OH line is not in either feed at this sensitivity, so it does not account for the power at C08–C11.
   - What the ordinary account still has is a property of the X chain at the ON pointing that acts on drifting windows: the false cohorts' upward bias on drifting tracks (item 4) shows that something of that kind is present in ON.
   - That bias is in power only. The comet's power stands 20th of 380 against it on track c. In D3 the false cohorts carry no such bias (false mean 0.001), and the comet's D3 stands first of 380 on its own drift only.
2. **What it does not settle.**
   - C09's power is as strong fixed at the dish as on the drift, and C09 was also the coordinate where Y's power was negative (READ-HM5-frames). C09 alone is open to the fixed-frequency reading.
   - Whether the X-only excess is the chain or emission polarized along X: the feeds never rotated against the sky (HM4, fact 3), and no public data could separate the two (the survey in PLAN-HM6).
3. **What follows, should the author want it.**
   - A drift test on 0015 and 0017 would ask whether the comet-drift dependence holds in the pairs where HM4 found the cohort weak. The same voltages, frozen before reading.
   - C12's hold-out from HMR1 needs those per-frame series too, and can share the run.
   - The request to Matt Lebofsky (drafted, unsent) asks for the Parkes sessions, whose rotating feeds could separate chain from sky.
