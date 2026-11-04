# PLAN-bg: the thirteen against three further background models

Frozen 2026-11-04 before this test's counts were computed. The six inputs (GBT blc23 rawspec.0000, 2025-12-18, scans 0013–0018, coarse channel 7) were read in earlier runs; the nulls, draws, seeds and rule below are fixed here. The sha256 of this file is recorded in the runner and the results.

## Question

The 13 is measured against one null: forty false range-acceleration frames (3.75 ± 2.05, maximum 8). A null built a different way can give a different expectation. Three more are fixed here, each keeping the true comet frame and the procedure of §7.1 (x/median − 1, 3-channel boxcar, path sum, robust z, DC zeroed, rest-frame alignment, ±1 channel tolerance, min ON ≥ 2.5, all OFF < 2.0, 10 Hz clustering), and each destroying one thing the true frame would need from a source on the comet.

- N1 time-shuffled rows. Within each scan, the order of the 49 normalized rows is permuted (each scan independently), keeping every row's spectrum and every channel's time median and destroying any tone's track through the scan. 40 draws, seed 101.
- N2 role partitions. The true comet frame with every assignment of three of the six scans to the ON role and the other three to OFF: 20 partitions, one of them the true assignment and one its swap. The true assignment's rank among the 20.
- N3 phase-randomized rows. Each normalized row (before the boxcar) replaced by the inverse real FFT of its own amplitude spectrum with uniform random phases (the zero and Nyquist terms kept), keeping each row's power and its correlation across channels and destroying every line's position. 40 draws, seed 103.

## Rule

For each null: EXCEEDS if the true count (13) is above every draw (for N2, above every one of the other 19 partitions); WITHIN otherwise. Reported with each null's mean, sd, maximum and the fraction of draws at or above 13. The three verdicts stand side by side; none overrides the others.

## Deviations

Recorded in RESULTS-bg.md with their reasons.
