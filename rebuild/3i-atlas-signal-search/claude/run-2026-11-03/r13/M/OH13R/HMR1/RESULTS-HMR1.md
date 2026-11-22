# RESULTS — HMR1: is there sequence at the comet's coordinates?

22 November 2026. Plan: PLAN-HMR1.md, frozen before any product (FROZEN-HMR1.sha256, commit eeaf72ec2). No amendment. Outputs: hmr1_score.json; log hmr1.log. 760 series, 1000 shuffles and 1000 IAAFT surrogates each, seed 20261122.

## The reading under the frozen rule

1. **One pass at the comet, at the threshold.** In ON 0013, X, power at C12 has lag dependence (M1) at z = 3.32, above every one of its eight sidebands. T is 3.3.
   - Its shuffle p is 0.004. Q's null distribution is right-skewed, so a z of 3.3 on Q corresponds to p ≈ 0.004, not the Gaussian 0.0005 the threshold was chosen for. Over the 44 ON tests, about 0.18 passes at that p are expected by chance.
   - C12 shows nothing beyond spectrum (M2 z = −1.30).
   - It is not in Y (M1 z = −1.13) or in OFF (1.47).
   - C12 is not one of C08–C11, and it carried no power contrast in HM5 (ON − OFF rank 0.00).
2. **One pass where the comet is not.** In OFF 0014, X, D3 at C08 has lag dependence at z = 3.47 (p = 0.003), above every sideband. The rule reads a pass in OFF as not the comet. It is the procedure finding sequence at a comet coordinate with the dish pointed away.
3. **The procedure's pareidolia rate.**
   - Sidebands at or over T: 3 of 1344 sideband tests in all (M1: 2; M2: 1), none of them in ON X power.
   - At the same shuffle p (≤ 0.004): 1 sideband series of 672, against 2 comet series of 88. One of those two is the OFF pass.
   - The procedure is quiet on the sidebands, and its two comet passes split one ON, one OFF.
4. **Nothing beyond spectrum.** No comet coordinate shows M2 structure in any scan or feed: no compressibility beyond what IAAFT surrogates of the same spectrum and distribution give.
5. **No co-structure among C08–C11.** The largest lagged cross-correlation (±20 frames) between the four averages 0.084 in ON X, against 0.086 for sideband pairs (95th percentile 0.116). The same holds in every scan, feed and statistic.

## What the result is

1. **The conventional reading first.** At 0.36 s per frame, the comet's coordinates carry no sequential structure beyond chance. There is one threshold pass in lag dependence at C12, in X power in ON, matched in kind by a pass at C08 in OFF, and nothing beyond spectrum anywhere. The excess HM5 found is a steady shift with nothing to read at this resolution, as READ-HM5-frames suggested.
2. **What it leaves.** C12's pass stands as found in one scan. Per PLAN §4, it is carried to a frozen confirmation on ON scans 0015 and 0017, which needs per-frame series from a voltage run.
3. **Where the reading goes.** Per the plan, inside the frames: the phase sequence within each 0.36 s frame at the comet's coordinates, which D3 measures only in aggregate. That reading, and C12's hold-out, are frozen next, before their product is read.
