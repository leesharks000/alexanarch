# PLAN-sib: below-threshold siblings of the thirteen

Frozen 2026-11-04 before this test's counts were computed. The six inputs (GBT blc23 rawspec.0000, 2025-12-18, scans 0013–0018, coarse channel 7) were read in earlier runs; the bands, null and rule below are fixed here. The sha256 of this file is recorded in the runner and the results.

## Question

The thirteen are clusters whose comet-frame tracked z is at least 2.5 in all three ON scans and below 2.0 in all three OFF scans. The injection tests (ChatGPT, 2026-11-03 and 2026-11-04) show the detector recovers weak planted lines only part of the time and scatters their scores around the gate. If the thirteen are the visible part of a population of weak features fixed in the comet frame, the same population leaves members just under the ON gate, and the comet frame then holds an excess of near-misses over the false frames. If the thirteen are a fluctuation at one cut, the near-miss band looks like the false frames.

## Procedure

The procedure of comb/run_comb.py B0 unchanged (x/median − 1, 3-channel boxcar, path sum, robust z, DC zeroed, rest-frame alignment, ±1 channel tolerance by max filter, 10 Hz clustering, the 40 false range-acceleration frames of seed 11, the swap), with the ON condition replaced by bands of the minimum aligned ON z (OFF condition fixed at all three OFF < 2.0):

- S1, the sibling band: 2.0 ≤ min ON < 2.5.
- S2, the narrow band under the gate: 2.25 ≤ min ON < 2.5.
- Curve (descriptive): cumulative counts at min ON ≥ 2.0, 2.25, 2.5, 2.75, 3.0, true frame and false frames.

Each band also counts the swap (ON and OFF roles exchanged) in the true frame.

## Rule

For S1 (the decision band): SIBLINGS if the true-frame count exceeds all 40 false frames; NONE if it lies within the false frames' range; BELOW if it is under all of them. S2 and the curve are reported beside it and do not change the verdict.

## Deviations

Recorded in RESULTS-sib.md with their reasons.
