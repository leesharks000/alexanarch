# RESULTS-lee: the global look-elsewhere count for the thirteen

Plan: lee/PLAN-lee.md, sha256 3e8e00cccd00137248521a425320ad6c86961470af17d3251250c6493bbbd439, frozen before any channel of the survey was computed. Stopping rule: lee/STOP-lee.md, sha256 16b8a5f2451fccbe40e5232e931a43f6728397ea0c089a5f9fe9d5b39870fc1f, fixed at 34 channels complete by sample size alone. Runner lee/run_lee.py (sha256 3386eb5e…), summary lee/summarize.py (sha256 57b26a51…), output lee.json (channels and summary) and summary.json. Data: Breakthrough Listen GBT, 2025-12-18, rawspec.0000, scans 0013–0018, nodes blc22–blc25, read by HTTP range reads 2026-11-04, about 16:55–22:16 EST. Logs: run-first-attempt.log, run-earlier.log, run.log, driver.log.

**Result.** 64 of the 256 L-band coarse channels: blc23 coarse channel 7, the fifteen channels of lheld (index ≡ 7 mod 8), and 48 others (see Deviations). Coarse channel 7 has E = 4.52 (13 against 3.75 ± 2.05, maximum 8). No other channel reaches it: **p_LEE = 1/64 (0.016)**, the smallest value the sample allows. Over coarse channel 7 with the 48 surveyed channels alone, p_LEE = 1/49. **N_FLAG = 1** (coarse channel 7), against a chance expectation of 1.56 over 64 channels (1.20 over 49).

| rank | channel | f mid (MHz) | T | swap | false mean ± sd | false max | E | flag |
|---:|---|---:|---:|---:|---|---:|---:|---|
| 1 | blc23 cc07 | 1666.992 | 13 | 1 | 3.75 ± 2.05 | 8 | 4.52 | yes |
| 2 | blc23 cc13 | 1649.414 | 7 | 5 | 3.33 ± 1.56 | 7 | 2.36 | no |
| 3 | blc22 cc25 | 1801.758 | 7 | 4 | 3.20 ± 1.62 | 7 | 2.35 | no |
| 4 | blc25 cc61 | 1133.789 | 8 | 11 | 4.35 ± 1.56 | 9 | 2.34 | no |
| 5 | blc24 cc52 | 1347.656 | 6 | 4 | 3.05 ± 1.45 | 6 | 2.04 | no |
| 6 | blc22 cc38 | 1763.672 | 7 | 3 | 3.65 ± 1.70 | 8 | 1.97 | no |
| 7 | blc23 cc39 | 1573.242 | 259 | 196 | 135.85 ± 62.96 | 299 | 1.96 | no |
| 8 | blc22 cc62 | 1693.359 | 12 | 11 | 6.55 ± 2.82 | 14 | 1.93 | no |
| 9 | blc25 cc28 | 1230.469 | 9 | 4 | 4.15 ± 2.58 | 13 | 1.88 | no |
| 10 | blc24 cc60 | 1324.219 | 7 | 4 | 3.45 ± 1.97 | 9 | 1.80 | no |

Across the other 63 channels E is 0.22 ± 1.18 (largest 2.36). The second-ranked channel's true count equals its largest false frame; no channel besides coarse channel 7 exceeds every false frame.

Interference. Nine channels have false-frame means above 8, all in allocations with dense transmitters: 1163.1 and 1171.9 MHz (GNSS L5/E5a, 1164–1189 MHz; the 1171.9 channel's false frames run 481.6 ± 1399.9, maximum 8936), 1309.6 MHz (aeronautical radar, 1215–1400 MHz), 1526.4, 1543.9, 1549.8 and 1558.6 MHz (mobile-satellite downlinks, 1525–1559 MHz), 1573.2 MHz (GPS L1) and 1620.1 MHz (Iridium, 1616–1626.5 MHz). Their E values run from −1.53 to 1.96: dense interference raises a channel's counts in every frame alike and gives no comet-frame excess over its own false frames.

## Reading

The look-elsewhere question was how often a channel of this cadence, run through the same procedure, gives a comet-frame excess the size of coarse channel 7's. In a quarter of the band, three quarters of it drawn at random, none does; the next largest is about half its size in E, and coarse channel 7 is the only channel to exceed all its false frames, where about 1.6 would be expected by chance. The selection of coarse channel 7 among the channels of the band does not account for the thirteen at the resolution of this sample. Bounds: 192 channels are not surveyed (listed in summary.json) and could hold others; p_LEE cannot fall below 1/64 here; the survey uses the time-median normalization under which the thirteen appear and bears on channel selection only, leaving the normalization and threshold sensitivity of §7.9 and §7.17 where they stood.

## Deviations

- Channel order: a fixed random order (seed 29) with coarse channel 7 first, set after the first attempt and before the survey proper, so that a survey stopped early is a random sample of the band. The first attempt ran in index order and completed one channel, blc22 coarse channel 0, which is kept (its E is −1.36). The 48 surveyed channels are therefore the first 47 of the seed-29 order and blc22 coarse channel 0; STOP-lee.md describes all 48 as taken in the seed-29 order, which holds for 47. Over coarse channel 7 with the 47 alone p_LEE is 1/48.
- Coarse channel 7 was recomputed by the survey (T 13, swap 1, 3.75 ± 2.05, maximum 8, as comb/comb.json B0): comb.json does not store the false frames' swaps that FLAG needs.
- Fetch threads: two per channel; six ran slower than sequential on the first attempt (run-first-attempt.log, 470 s wait and a ContentLengthError retry).
- Stopping: 64 channels by STOP-lee.md, on Lee Sharks's ruling of 2026-11-04 ("a healthy random sampling is enough, and others can check the rest if theres something worth checking"); the runner was stopped at 64 before its own summary block, and summarize.py computes the summary by the plan's definitions.
- Interruptions: the process stopped three times (background time limits at 19:05 and 21:14, a workspace restart near 19:10); each time it resumed from lee.json, and the channel in progress at the restart was read again. No channel's result was affected.
- The survey can be continued from lee.json with run_lee.py unchanged; the summary then needs summarize.py run again.
