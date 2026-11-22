# PLAN-HM6 — the first pair, on three tracks; and the OH line in each feed

Frozen 22 November 2026, before any HM6 product is read, at the author's word (10:42: "lets begin working through tests 1-4"). It takes paths 1 and 2 of that morning's list as far as the public data allow. Path 3 (the per-frame read) is READ-HM5-frames.md; path 4 goes to its own plan.

**What is looked for.** As in HM3–HM5, in the author's words: "what were looking for, is something with meaning - and we do not know that that looks like. we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning." HM6 asks two ordinary questions of the first pair's contrast: does it follow the comet's drift or stay fixed at the dish, and is the comet's own OH line in either feed.

**What the public data allow (survey of 22 November, recorded before this plan).**
- Raw voltages, with X and Y apart and with phase, exist publicly for scans 0013–0018 on node blc23 only (bldata GB_ATLAS_raw: six scans). No other scan, target or session has public voltages.
- The night's other three cadences (0029–0034, 0045–0050, 0061–0066) were observed in other bands (S, C and X band; RESULTS-2380, RESULTS-ka), so there is no L-band data at higher elevation that night.
- The public spectral products (GBT rawspec, ATA July 3, Parkes July 31) are total power (nifs = 1): the feeds cannot be separated in them.
- Listed but walled (HTTP 403): ATA July 5, 9, 10 and 30, including the July 30 visibilities (uvh5, with calibrators 3C286 and 1714-252); Parkes September 12 and October 5 2025, every node.
So a test of the receiver chain against a scan that cannot contain the comet is not possible in public data. What these voltages can still separate is whether the contrast moves with the comet's drift or stays fixed at the dish.

**Code check before freezing.** hm6.py was run for 8 frames of 0013 and 0014 into the session scratchpad, with scoring, to check that it runs and that its outputs have the right structure. No value was read. The output is not part of HM6.

1. **Data and fixed choices.**
   - Scans 0013 (ON) and 0014 (OFF), all 833 frames, both feeds.
   - Windows, selections and sideband rule exactly as HM5 (hm6_selections.json is hm5_selections.json); D3 at d = 2; power as HM4 §D.
   - Three tracks for every window, the comet cohort and the 379 false cohorts alike:
     - **c**, the window's own drift (for the comet cohort, the comet's), exactly as HM5;
     - **d**, held fixed at the dish: no drift, the window at its mid-scan topocentric bin for the whole scan;
     - **f**, the drift mirrored about the mid-scan frame.
   - The drift across the scan, in native bins (2.794 Hz), is reported per comet coordinate.
2. **Reproduction.** Track c must reproduce HM5's full-series cohort score and every per-coordinate ON − OFF rank for D3 and power, in X and in Y, to 1e-9. If it does not, nothing else is read.
3. **A. Comet's drift or dish-fixed (path 1).** For D3 and power, X and Y, on each track: the cohort score and its rank against the 379 false cohorts scored on the same track; the per-coordinate ON − OFF rank; and, for power, the mean over C08–C11.
   - **Follows the comet:** for X D3, the cohort's rank on track c better than on both d and f; for X power, the C08–C11 mean on c greater than on both d and f.
   - **Fixed at the dish:** the value on d at least the value on c. That is what interference or a property of the receiver chain at a fixed frequency would give.
   - **Otherwise** it is stated as not decided by this test.
   - Where a coordinate's drift is under 2 native bins, its three tracks are too close to separate, and that coordinate is reported as not separable.
4. **B. The OH 1667.359 MHz line in each feed (path 2).**
   - From every frame's full spectrum, per feed: ±70 kHz around 1667.359 MHz at native resolution, summed over frames, in the comet frame (shifted each frame by the comet's range-rate) and in the dish frame (fixed at the mid-scan position).
   - Statistic as RESULTS-absorb-calib: ON/OFF − 1, rebinned to 2.8 kHz, cubic baseline over ±70 kHz excluding ±8 kHz, the mean within ±4 kHz in units of the robust scatter, against 40 controls at ±15 to ±55 kHz. Signed: negative is absorption, positive emission. Reported for X, Y and X + Y.
   - 1665.402 MHz lies outside the coarse channel the voltages hold (1665.53–1668.46 MHz) and is not tested here.
   - **A line:** |centre| ≥ 3 and beyond all 40 controls in the comet frame. The same sign in X and Y is the comet's OH seen in both feeds; one feed only is stated as that; neither is not seen, at the sensitivity stated.
   - Stated now, before the result: C08–C11 lie 54 to 636 kHz from 1667.359 MHz (+54, +71, +328, +636 kHz). Comet OH lines are a few kHz wide, so this test bears on C08 and C09 only through any wing the data show. Whatever it finds, it does not by itself explain C10 and C11.
5. **What stays fixed.** No other pair, track, statistic or window within HM6, and nothing tuned after the score. Any amendment is recorded before results. A run stopped by the session's time limit is resumed from the start of the unfinished scan and marked in the log. Further tests are frozen from what HM6 shows before their own product is read; failing a frozen test bars nothing.
