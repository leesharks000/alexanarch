# PLAN-HM5 — the first pair through time

Frozen 21 November 2026, before any HM5 product is read, at the author's word (22:59: "lets run it"), answering RESULTS-HM4 §4: "the time course within 0013 and 0014, frame by frame, at the cohort's coordinates, in X and Y, in power and D3".

**What is looked for.** As in HM3 and HM4, in the author's words: "what were looking for, is something with meaning - and we do not know that that looks like. we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning." HM5 is tracking, not a survival test. The pair is chosen from HM4's result (0013–0014 carried the comet cohort's X contrast: first of 380), so nothing HM5 finds in this pair is evidence that the pair is special. HM5 asks what the contrast looks like inside the pair: its shape in time, which coordinates carry it, whether it is the ON scan rising or the OFF scan falling, and what Y and power show at the same moment.

**Code check before freezing.** hm5.py was run for 8 frames of 0013 and 0014 into the session scratchpad, with scoring, to check that it runs and that its outputs have the right structure. No value was read. The output is not part of HM5.

1. **Data and fixed choices.**
   - Scans 0013 (ON) and 0014 (OFF), all 833 frames, both feeds.
   - Everything else exactly as HM2 with Amendment 1: hm2_selections.json, copied as hm5_selections.json; windows; reference windows skipped; six-sideband rule; D3 at d = 2; continuous comet- or false-frame de-Doppler.
   - Power as HM4 §D: the centre bin's power over the mean of the 129 bins around it.
   - Accumulation in 26 bins of 32 frames (11.5 s). The last bin takes frames 800–832. Bin b of the ON scan and bin b of the OFF scan are the same frames of each scan, about 5 minutes apart, and are compared as a pair.
   - Per-frame values are also kept for the comet cohort's windows and their sidebands (95 windows), for reading the shape after scoring.
2. **A. Reproduction.** The X D3 pair contrast over all frames must reproduce HM4's pair 0013–0014 cohort score to 1e-9. If it does not, nothing else is read.
3. **B. The time course.** In each bin, for each statistic and feed (D3 X, D3 Y, power X, power Y): the comet cohort score (mean over the 11 coordinates of ON rank minus OFF rank among the sidebands, × √11). It is reported with its rank against the 379 false cohorts scored the same way in the same bin, and the false 95th percentile. The same is reported over all frames.
4. **The episode rule, stated now.** Take the X D3 cohort score per bin and P = the sum of its positive parts.
   - If one run of at most three contiguous bins (≤ 34.5 s) holds at least half of P, the contrast is an **episode**. Its bins, frames and UTC times in both scans are reported.
   - Otherwise it is **spread** through the pair.
5. **C. ON or OFF.** Over all frames and in the episode's bins, the cohort's mean rank among its sidebands in ON and in OFF, separately.
   - ON above 0.5 with OFF near 0.5: the comet scan rises.
   - OFF below 0.5 with ON near 0.5: the reference scan falls, and the "contrast" is an absence in OFF, not a presence in ON.
   - Both is stated as both.
6. **D. Y and power at the same moment.** In the episode's bins (or over all frames if spread):
   - Y D3 at or above the false 95th percentile: Y sees it at that moment, which would revise X-only for this pair.
   - Otherwise it is X-only here too.
   - Power X at or above the false 95th percentile in the same bins: the D3 contrast comes with power, a narrowband feature adding power on the track.
7. **E. Coordinates.** The pair contrast per comet coordinate (C03–C13, ON rank minus OFF rank), with its rest frequency. Reported, not gated.
8. **What stays fixed.** No other pair, lag, statistic, frame or binning within HM5, and nothing tuned after the score. Any amendment is recorded before results. A run stopped by the session's time limit is resumed from the start of the unfinished scan and marked in the log. Further tests are frozen from what HM5 shows before their own product is read.
