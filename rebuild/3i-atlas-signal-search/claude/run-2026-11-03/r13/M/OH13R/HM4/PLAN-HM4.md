# PLAN-HM4 — tracking X

Frozen 21 November 2026, before any HM4 product is read, at the author's word (21:09: "lets track down x").

**What is looked for.** As in HM3, in the author's words: "what were looking for, is something with meaning - and we do not know that that looks like. we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning." HM4 is a tracking test. It decides no survival; it asks where, when and in what form the HM2 X pattern lives, and each outcome below is stated in advance as what it can and cannot say. It forbids no further test.

**Why.** HM2 (X feed): comet cohort first of 380 at full length (p 0.0026), second in the first half, 45th in the second; the OH 1667 coordinates C07–C11 held or strengthened into the second half while same-frequency false coordinates averaged near zero. HM3 (Y feed, frozen): neither the cohort nor G1667 present (cohort rank 231 full, 360 first half; G1667 p 0.84). The pattern is in X, on the comet's track, and not in Y.

**Facts fixed before this plan, from the raw headers and geometry (no product read).**
1. All six scans: GBT, Rcvr1_2, FD_POLN = LIN (linear feeds X and Y), GUPPI.
2. The session was at low elevation, rising in the east: zenith angle 81.3° (0013) to 76.7° (0018), azimuth 88°–93°. Elevation 9°–13°.
3. The parallactic angle stayed at −52.0° ± 0.2° across the ON scans (−51.7° at the end of 0018). The feeds did not rotate against the sky. A wave polarized along the X feed's axis and a property of the X chain therefore cannot be separated by rotation in these data. This is stated now so that no outcome is later read as having separated them.

**Code check before freezing.** hm4.py was run for 8 frames of scan 0013 into the session scratchpad, to check that it runs and that its arrays have the right shape. No value was read and nothing was scored. The output is not part of HM4.

1. **Data and fixed choices.** The six scans, all 833 frames, both feeds. Everything else exactly as HM2 with Amendment 1 (hm2.py): the selections (hm2_selections.json, copied as hm4_selections.json), windows, reference windows skipped, six-sideband rule, D3 at d = 2, continuous comet- or false-frame de-Doppler, halves at frame 417. Per-frame accumulations are kept in eight equal segments, s0–s7 (segment g holds frames j with ⌊8j/833⌋ = g; s0–s3 is the HM2 first half exactly).
2. **A. Reproduction.** The X feed, full and both halves, must reproduce hm2_score.json's comet cohort scores to 1e-9. If it does not, nothing else is read, and the discrepancy is reported.
3. **B. Time map, X.** Comet cohort score and G1667 (C07–C11, null of 10,000 draws of five from the same-frequency false pool, seed 20261121, as HM3) in each segment s0–s7. Also each ON–OFF scan pair separately (0013–0014, 0015–0016, 0017–0018), full and halves: the contrast is that pair's ON rank minus OFF rank. Reported, not gated. Readings stated now:
   - The X contrast carried by one segment or one pair is localized in time: an event, not a steady property.
   - The X contrast spread across segments and pairs is steady over the session.
   - Neither reading says source.
4. **C. Feed basis.** The same measurement on P+ = (X + Y)/√2 and P− = (X − Y)/√2, the linear feeds rotated by ±45°. These are formed on the spectra, which is exact because the transform is linear. Reported: comet cohort and G1667 in each. The asymmetry A = score(P+) − score(P−) is reported for the cohort, against the false cohorts' asymmetries (two-sided), and for G1667, against 10,000 same-pool draws' |A| (two-sided, seed 20261121). Readings stated now:
   - **|A| within the null.** The pattern lies on the X axis only. Either the X chain carries it, or the incoming wave is polarized along the X feed's axis. By fact 3, these data cannot separate the two.
   - **|A| beyond the null 95th percentile, both halves the same sign.** The pattern has a component off the X axis, with a definite sign between X and Y. A property of the X chain alone cannot make one: Y's own noise is symmetric in sign, so it adds to P+ and P− alike. That is a polarized component of what arrives at both feeds. It is still not a source.
5. **D. Power, X.** At each window's track centre: per frame, the centre bin's power over the mean power of the 129 bins around it, averaged. Scored with the same ON–OFF rank contrast against the sidebands, for the comet cohort and G1667, full and halves. Readings stated now:
   - **D3 contrast with a power contrast.** A narrowband feature in X that adds power on the track.
   - **D3 contrast without one.** Phase structure in X with no excess power on the track.
6. **What stays fixed.** No other lag, statistic, frame, combination or segmentation within HM4, and nothing tuned after the score. Any amendment is recorded before results. A run stopped by the session's time limit is resumed from the start of the unfinished scan and marked in the log. Further tests, if the author wants them, are frozen from what HM4 shows before their own product is read.
