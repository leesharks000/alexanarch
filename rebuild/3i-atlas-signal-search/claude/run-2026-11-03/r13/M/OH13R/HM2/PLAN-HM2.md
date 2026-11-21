# PLAN-HM2: the Receiver Test at 400 false drifts, with a fixed sideband rule and held-out halves

Frozen before any HM2 product, at the author's word (2026-11-21 15:02, "it came in second. is that not worth testing further?"; 15:05, "and yes - go"), on RESULTS-EA-3I-HAILMARY-01.

**Why.** The Receiver Test ranked the comet cohort second of 40 (p 0.05). With 40 false cohorts its p cannot fall below 1/41, and the second place turned, read afterwards, on one false window scored against two sidebands (F14s1). This plan gives the rank a resolution and fixes the sideband rule before any data.

1. **Drifts.** The original detector unchanged (cometframe_raw.py, z_on 2.5, z_off 2.0, rows within 10 Hz merged) at 400 false drifts: −1.000 to +1.000 Hz/s in steps of 0.005, |d| < 0.005 excluded. Rate d → cf.coincidences(d·C/1.667e9). Empty cohorts kept and counted.
2. **Windows.** As the Receiver Test (hm.py hm_windows): C03–C13 on the comet track; each false selection on its own track; references (within 1.5 kHz of a known line or 15 kHz of the edges) leave their cohort; up to eight sidebands per coordinate from OH13R's offsets in order, clear of lines, edges and every other window of the same frame.
3. **The sideband rule, fixed now.** A coordinate is scored only if it has at least six sidebands. The rule applies to every cohort, the comet's included; a cohort left with no scored coordinate is empty. Excluded coordinates are listed.
4. **Measurement.** OH13R's D3 at d = 2, X only (the frozen statistic), comet- or false-frame continuous de-Doppler, all 833 frames of the six scans, accumulated separately over frames 0–416 (first half) and 417–832 (second half); the full-length value is the frame-weighted mean of the two.
5. **Score.** As the Receiver Test: per scan, each coordinate's percentile rank among its sidebands, (#below + ½ #tied) / n; contrast = mean rank over the ON scans − mean rank over the OFF scans; cohort score = mean contrast × √n. Full length, and each half on its own.
6. **Decision.**
   - p_full = (1 + #false cohorts with score ≥ the comet's) / (1 + #non-empty false cohorts).
   - **Survives** if p_full ≤ 0.01, and in each half the comet cohort's score is at or above the 95th percentile of the non-empty false cohorts' scores in that half. A survivor is still not a source. It is the first feature of the search that its own selection does not account for, and it calls for a plan on independent data (another epoch or telescope). Nothing further is run on these data.
   - **Retires** otherwise: the selection explanation stands with resolution, and the original thirteen close.
7. **What stays out.** No other lag, feed or frame is read; no injection is added; nothing is tuned after the score.
