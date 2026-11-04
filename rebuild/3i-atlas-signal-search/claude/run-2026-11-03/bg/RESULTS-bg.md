# RESULTS-bg: the thirteen against three further background models (frozen test)

Plan: bg/PLAN-bg.md, sha256 b8fd193abad6f20c3a6c8e552da6eecfa4d063ba34859c3f54987b615d186b0a, frozen before the counts were computed. Data: GBT blc23 rawspec.0000, 2025-12-18, scans 0013–0018, coarse channel 7, re-read 2026-11-04 by bg/fetch_cc.py (fetch.log). Runner bg/run_bg.py (sha256 1df1d216…), output bg.json (sha256 135891ba…), log run.log. Run 2026-11-04, 16:36–16:45 EST, one pass, no errors. The true assignment reproduces 13.

**Verdict: EXCEEDS under all three.** No draw of any null reaches 13.

| null | what it keeps | what it destroys | mean ± sd | max | fraction ≥ 13 | verdict |
|---|---|---|---|---:|---:|---|
| N1 time-shuffled rows (40) | each row's spectrum, each channel's time median | a tone's track through the scan | 4.33 ± 1.86 | 8 | 0.0 | EXCEEDS |
| N2 role partitions (19 others) | the data and the comet frame | which scans are ON | 3.90 ± 1.86 | 6 | 0.0 | EXCEEDS (rank 1 of 20, no ties) |
| N3 phase-randomized rows (40) | each row's power and its correlation across channels | every line's position | 2.35 ± 1.62 | 6 | 0.0 | EXCEEDS |
| (earlier) false range-accelerations (40) | the data, the ON/OFF roles | the comet's motion | 3.75 ± 2.05 | 8 | 0.0 | — |

## Reading

Four nulls built four different ways agree on an expectation of 2.4–4.3 clusters with maxima of 6–8, and the true assignment gives 13. The excess needs all three things the nulls take away: the order of the rows within each scan (N1), the assignment of the comet's beam to scans 0013, 0015 and 0017 (N2: of the twenty ways to choose three ON scans, the true one gives 13 and no other gives more than 6), and the positions of features in frequency (N3). The comet frame itself was the fourth (the false accelerations).

These nulls bear on the reading in §7.17 (RESULTS-sib). There the excess was found to occupy the slice 2.5–2.75 without siblings beneath it, and its shape was read as a fluctuation at the cut. A fluctuation of the data at that cut would appear in the nulls as often as in the true frame, and in 139 draws across four nulls none reaches 13. What is now measured is a beam-sided, order-dependent, comet-frame excess concentrated in one narrow slice of the score with no tail below it; the two results stand together and neither is yet explained. The nulls share every draw's channel and threshold choices, so they say nothing about how often an excess of this size appears somewhere among all the channels and cuts examined (work plan item 8, the global look-elsewhere count).

## Deviations

None. The raw spectra were deleted after the run; fetch_cc.py re-reads them by name.
