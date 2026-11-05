# RESULTS-ata36: the comet frame in 3648–3688 MHz, ATA 2025-07-03

Plan: ata36/PLAN-ata36.md, sha256 df74d8d5030f4c517d4c51b3190d95292fa548313c9dfeabe0e071d299979a7a, frozen before any power of the strip was counted. Runner run_ata36.py (sha256 382b5bbd…), output disc.json (sha256 e32da205…) and nominees.json (sha256 93821698…), Horizons rows horizons.json, logs run.log, run-earlier.log, driver.log; mechanics check test_inject.py and test_inject.log. Data: ATA 2025-07-03, tuning LoD.C1504, the first eight of the session's 16 scans, both beams, 3648.0–3687.75 MHz in 40 blocks of 524,288 channels, read 2026-11-04 22:16 to 2026-11-05 02:54 EST.

**Result. Nothing in the strip.** The true comet frame gives 0 clusters, the beam swap 0, and all forty false range-accelerations 0, with their swaps 0. E is 0 and FLAG is false. No nominee was produced, so under the plan the held-out eight scans have nothing to test and were not read.

| frame | on-source clusters | swap |
|---|---:|---:|
| true comet frame | 0 | 0 |
| 40 false accelerations | 0 in every frame | 0 in every frame |

**The strip's noise against the tuning's middle.** The robust scatter of x/median − 1 per sample is 0.1177 in the strip (640 file-blocks) against 0.1178 at 3605–3635 MHz (64 file-blocks); the ratio is 0.999, inside the plan's factor of 1.5, so the strip is reported whole, with no roll-off at the top of the tuning.

## Reading

The gate is strict by design: beam-0 z ≥ 2.5 in at least six of eight scans, a mean z of 3.0 or more, and beam 1 below 2.0 in all eight. Pure noise does not pass it anywhere in 20.8 million channels in any of 82 frames, which is what makes a pass meaningful and also what bounds the null. The only measure of reach the run carries is the mechanics check of test_inject.log: a tone multiplying the power along the comet path by 1.3 in every sample of beam 0 was found at its channel by the true frame (mean z up to 6.18) and by none of the forty false frames; at 1.05 it was found by none. The search therefore excludes a steady comet-borne tone in this strip at roughly that level and above, during the first eight scans of July 3; a fainter, intermittent or later signal is not excluded. No completeness curve was run.

In the context of the survey: this strip is the one part of the public 3I/ATLAS data held by no other study (ATA July 3 only), and the class it tests, a tone drifting with the comet, is the class the published ATA filter removed by its sign (draft §5.1). In the public data that class now holds nothing at this strip.

## Deviations

- The scatter reference was sampled: four blocks of 524,288 channels at 3605, 3615, 3625 and 3635 MHz, where the plan names 3600–3640 MHz.
- The mechanics check (test_inject.py) read one block of 16,384 discovery channels at 3670 MHz before the run, recorded in test_inject.log; it reported 0 uninjected hits in that block.
- Interruptions: the runner was stopped by background time limits and resumed from disc.json each time (driver.log); no block's result was affected.
- No held-out power was read, since the plan's continuation applies only to nominees and there were none.
