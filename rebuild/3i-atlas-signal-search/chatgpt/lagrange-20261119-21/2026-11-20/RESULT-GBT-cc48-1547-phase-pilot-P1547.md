# GBT cc48, 1547.72 MHz, phase-only pilot: no candidate; the design blind to line-spectrum signals before whitening

**2026-11-20.** Executed on the public GBT voltages (scans 0013–0018, first 16 frames, both feeds, 65,536 bins centred at 1547.720 MHz) from [PLAN-1547-phase-only-out-of-shape-pilot.md](PLAN-1547-phase-only-out-of-shape-pilot.md). That plan's code is a ChatGPT attachment not in this repository, so the run is an independent implementation of its text, with the open definitions fixed before any data.

Canonical run, frozen plan, code, hashes: [PLAN-P1547.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/PLAN-P1547.md) (with amendment 1, recorded before the telescope data), [RESULTS-P1547.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/RESULTS-P1547.md), [P1547-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/P1547-PRODUCTS.sha256), [p1547.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/p1547.py).

The text below is RESULTS-P1547 as committed there.


Run 2026-11-20 under PLAN-P1547 (sha256 9a0c7241…, with amendment 1, recorded before any telescope data), an independent implementation of ChatGPT's frozen plan (Lagrange Observatory, PLAN-1547-phase-only-out-of-shape-pilot.md, sha256 63154ed3…). GBT 3I/ATLAS scans 0013–0018 (2025-12-18), coarse channel 48, the first 16 frames of each scan, both feeds, 65,536 bins centred at 1547.720 MHz, streamed from bldata.berkeley.edu (384 MiB). Products and hashes in P1547-PRODUCTS.sha256.

## Reading

1. **No candidate.** In ON0015, the discovery scan, neither filter reaches the family test in either feed: phase-increment memory p = 0.90 (X) and 0.15 (Y), four-frequency closure p = 0.10 (X) and 0.45 (Y), against a floor of 0.05. The confirmation and control gates are not reached.
2. **Across all 24 tests** (6 scans × 2 feeds × 2 filters), two reach p = 0.05: phase memory in ON0013 X (lag 512, score 1.45× the median surrogate maximum) and closure in ON0017 Y (quartet 127, 1.15×). About 1.2 are expected by chance. Neither is in the discovery scan, and an OFF scan comes as close (OFF0016 Y phase memory, p = 0.10, 1.37×).
3. **What the test could see.** By the synthetic validation (amendment 1), the filters detect phase structure injected after whitening (phase memory 169×, closure 20× the surrogates) and do not detect a repeated code or a set of balanced tones injected before whitening, as a signal arrives, even at the noise's own power across the whole slice. Whitening each frame at full resolution reduces any line-spectrum signal to its share of the 65,536 bins. The negative is therefore a negative for broadband phase dependence at this frequency in these 16 frames, and says nothing about periodic or tonal phase structure, which this design cannot see.

## Family scores

| scan | role | feed | memory p | lag | score/surr. max | closure p | quartet | score/surr. max |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 0013 | ON | X | 0.05 | 512 | 1.45 | 0.85 | 109 | 0.88 |
| 0013 | ON | Y | 0.95 | 2 | 0.77 | 0.85 | 123 | 0.91 |
| 0014 | OFF | X | 0.30 | 16 | 1.09 | 0.35 | 91 | 1.05 |
| 0014 | OFF | Y | 0.65 | 512 | 0.94 | 0.75 | 99 | 0.92 |
| 0015 | ON | X | 0.90 | 8 | 0.79 | 0.10 | 63 | 1.19 |
| 0015 | ON | Y | 0.15 | 2 | 1.17 | 0.45 | 36 | 1.02 |
| 0016 | OFF | X | 0.30 | 32 | 1.16 | 0.60 | 92 | 0.96 |
| 0016 | OFF | Y | 0.10 | 16 | 1.37 | 0.95 | 39 | 0.84 |
| 0017 | ON | X | 0.90 | 32 | 0.79 | 0.45 | 109 | 1.04 |
| 0017 | ON | Y | 0.85 | 4 | 0.85 | 0.05 | 127 | 1.15 |
| 0018 | OFF | X | 1.00 | 4 | 0.64 | 0.20 | 100 | 1.11 |
| 0018 | OFF | Y | 0.15 | 512 | 1.17 | 0.40 | 22 | 1.06 |

"score/surr. max" is the real family score over the median of the 19 surrogate family maxima.

## Against ChatGPT's validation

ChatGPT's figures (lag-2 memory 0.001826 against 0.000229 for noise; closure 0.702 against 0.051) and this run's are on different normalizations and are not compared number for number. Both validations pass at the stage ChatGPT tested, after whitening; ChatGPT's plan does not report a test before whitening. The closure figure for noise agrees in scale (0.051 there; median surrogate maximum 0.047–0.054 here).

## Limits

1. A pilot: 16 frames and 19 surrogates, p floor 0.05.
2. This implementation is not ChatGPT's code, which is a conversation attachment and not in Lagrange; the quartet draw and the memory statistic's normalization are this run's (PLAN-P1547).
3. The design's blindness to line-spectrum signals (reading 3) is the plan's, not a defect of this run; a version that whitens at coarser resolution (the 512-sample segments, or a smoothed magnitude) would keep that class in view. That would be a new plan, frozen before it runs.
