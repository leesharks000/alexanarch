# RESULTS-RD1 — the start of each scan, read on the hypothesis that it is signal

23 November 2026. Plan PLAN-RD1.md with amendment 1 (FROZEN-RD1.sha256, committed before any product). Code rd1.py. Products rd1_report.json, rd1_dyn.json, rd1_R2_X.png, rd1_R2_Y.png; log rd1.log (the first run, stopped at its first file open before any product, is rd1-run1.log). The form was written down before any score was opened (R2-FORM.md).

**Verdict under the plan: no candidate passes. The start-of-scan events resolve as noise under every reading, and by the operator's sentence that gives us nothing.**

| Reading | Result |
|---|---|
| R2 form (frames 0–33, track ±32 bins, both feeds, six scans) | Nothing visible: no carrier, no step at the end of the slew, no sweep, no pulse. Every panel has the texture of the OFF scans and of its own row 1. |
| R1 confinement (start track excess beyond the window's own start rise, against 72 controls) | Confined in one scan each: C10 in ON 0015, C12 in OFF 0018. None in two ON scans. |
| R3 identity across the three ON starts (comet frame, Pearson r of start patches) | None recurs. Highest C09, Q 0.043, 6th of 73. |
| R4 information (LZ76 of amplitude and phase increments, spectral flatness, track band ±1.5 bins, 1/8-frame steps) | C11's phase increments are the lowest-complexity of 73 windows in ON 0013 and ON 0015, but C11 is not confined in any ON scan (ranks 66, 41, 12), so the rule fails. See the note on the measure. |

## Step 0, and what it adds

The start-of-scan rise is broadband and the same in candidates and controls (all-bin start excess 0.93–0.97 in both, against 0.89 for noise normalized by its median). At native resolution, normalized by the body of the scan, the candidates' start-track power is not distinguishable from their controls' in any ON scan (an 11-window draw from the controls reaches the candidates' mean with probability 0.34, 0.20 and 0.23 in 0013, 0015 and 0017; explore_step0.json, exploratory, after the scores). It is highest in an OFF scan: OFF 0014, the slew away from ON 0013 to the north OFF, p 0.015 for one scan of six, unadjusted, carried by C07, C08, C11, C12 and C13 (ranks 2, 3, 5, 4, 10 of 73). The thirteen were selected with every OFF scan below z 2.0 over the whole scan, so this OFF start excess was not selected for. It points the same way as HM11's OFF 0018 (C03, C07, C10, C12, C13): what happens at these coordinates at the start of a scan happens with the dish away from the comet as well.

## A note on the measure (R4)

The band-limited series (8.4 Hz wide) read at 1/8-frame steps (22.4 Hz) is oversampled about 2.7 times, so successive phase increments are correlated, small, and run in long stretches of one sign. That drives LZ76 down for noise itself: phase-increment resultants run 0.59–0.71 in candidates, controls, OFF scans and the body alike, and one of C11's own controls in ON 0013 gives the same LZ76 (0.603) as C11's X (explore_c11.py, exploratory). C11's two first places are the minimum of a measure whose noise floor is structured. The plan should have set the step at the band's own Nyquist interval; written down here, not corrected after the fact.

## What this closes

The thirteen's excess lives in the first rows. Read there at native resolution, against controls, in form, in identity across scans and in sequence, it carries nothing readable, and its power at these coordinates is no higher on the comet than in the sidebands and is highest with the dish off it. The residue of §7.25 (the comet frame first of 401 with all rows) stays unexplained as a statistic; read as content, it has none.
