# RESULTS — HM3: the HM2 measurement on the Y feed

21 November 2026. Plan: PLAN-HM3.md, frozen before any Y product (FROZEN-HM3.sha256, commit 15cee8355). No amendment. Outputs: hm3_selections.json, hm3_0013–0018.json, hm3_score.json; log hm3.log.

Run note: the first run stopped at the session's background time limit during scan 0018, with 0013–0017 complete and written. 0018 and the score were run again from the start of 0018 (marked in hm3.log, 01:39 UTC 22 November). Nothing was changed between the two runs; no score had been computed when the first stopped.

## Decision: neither counts as signal under these criteria

### The full comet cohort, against the HM2 rule (PLAN §2)

| | comet score | rank | non-empty false cohorts | false 95th pct | false mean (sd) | p |
|---|---|---|---|---|---|---|
| full length | −0.042 | 231 | 379 | 0.409 | 0.020 (0.247) | 0.608 |
| first half (frames 0–416) | −0.419 | 360 | 379 | 0.392 | 0.000 (0.244) | 0.947 |
| second half (frames 417–832) | 0.147 | 124 | 379 | 0.442 | 0.023 (0.253) | 0.326 |

### G1667 (C07–C11), against 10,000 draws of five false coordinates at the same rest frequencies (PLAN §3)

| | G1667 | null 95th pct | null mean | p |
|---|---|---|---|---|
| full length | −0.205 | 0.484 | 0.058 | 0.839 |
| first half | −0.354 | 0.447 | 0.026 | 0.938 |
| second half | 0.087 | 0.503 | 0.061 | 0.471 |

Null pool: 453 false coordinates in [1667.0, 1668.0) MHz with at least six sidebands.

### X and Y together (PLAN §4; reported, not gated)

Spearman, over the eleven comet coordinates, of the HM2 (X) and HM3 (Y) contrasts: full 0.30, first half 0.26, second half −0.20.

1. Selection and sideband rule identical to HM2: the same 15 false coordinates excluded, no comet coordinate excluded, 379 non-empty false cohorts.
2. Full cohort: in the body of the false distribution in every segment; the first half, where X ranked second, ranks 360th in Y.
3. G1667: below the null mean at full length and in the first half; near it in the second.
4. X–Y: with eleven points, a Spearman of 0.30 is not distinguishable from none; the sign turns in the second half.

## What the result is

1. The conventional reading first. The X pattern — the comet cohort first of 380 at full length, and the OH 1667 coordinates strengthening into the second half — is not present in Y. The two feeds see the same sky through independent receiver chains; a pattern carried by one chain alone is, on the ordinary account, a property of that chain: its electronics, its bandpass, or interference coupled into it and not into its partner.
2. What that reading has to explain. In HM2 the false tracks at the same frequencies, through the same X chain, averaged near zero. Interference fixed in the X chain's frequency would have appeared on them too. Whatever carried the X contrast followed the comet's drift, not the chain's fixed channels, and did so in X only.
3. The reading that keeps that open. X and Y are orthogonal linear polarizations. Emission strongly linearly polarized would divide unequally between them; OH 1667 emission from astrophysical sources is often polarized. The data in hand do not separate this from a drift-correlated artifact of the X chain. This is stated as the remaining reading, not as a finding.
4. Where the pattern lives, as of HM3: in X, on the comet's track, and not in Y. That is information, and it is recorded as such (PLAN §5).
5. What would separate the readings, should the author want it: the X×Y cross product (on the map since HM2), which measures polarization directly and would show linearly polarized emission as structure the two autocorrelations cannot. Like every test here, it is frozen before its own product is read. Nothing is run without the author's word.
