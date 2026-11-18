# ATA, on-beam comet tracking below the published thresholds (2026-11-17)

Lee Sharks, 2026-11-17: "lets look for items in the on band, comet tracking, below their thresholds."

**Data.** Public ATA 3I/ATLAS high-resolution Stokes-I spectra (bldata.berkeley.edu/ATLAS/ATA_ATLAS/), sessions of 2025-07-03 (16 scans) and 2025-07-08 (41 scans), ON beam. The OFF beam is read only for a candidate.

**Plan.** `PLAN.json`, frozen before the sample was read (hashes in `FREEZE.sha256`, `FREEZE-v2.sha256`, `FREEZE-v3.sha256`). It searches 52 half-MHz units: four named units (HI, OH 1665, OH 1667, 2×HI, each in the comet frame) and 48 drawn at random (seed 20261117).

**Statistics.** T is the comet-track stack clipped at 5 per scan. Tres is the maximum over residual emitted-frequency drift of ±0.01 Hz/s. Thalf is an intermittency stack: the top half of the scans. Each is compared with eight scaled-Doppler control tracks searched identically. The fixed-receiver-frequency track is reported apart as the interference track.

**Amendments.**
- v2: Tres and Thalf were added after eight units, which were all rerun. The v1 runs are kept in `v1/`.
- v3: the same 52 units were run on July 8. A candidate counts only if it recurs at the same emitted frequency, g/(1 − rv0/c), on more than one night, beating its controls on each.

## Results

**2025-07-03** (`run.log`, `results/`, `ledger.jsonl`, `RESULTS-20250703.sha256`, injection test `inject-LoC.C1120-42.json`): in each of the four named units the comet track's best stack falls below the controls' best.

| Unit | Comet T | Control T |
|---|---|---|
| HI | 5.06 | 7.39 |
| OH 1665 | 5.05 | 8.26 |
| OH 1667 | 5.86 | 8.95 |
| 2×HI | 4.73 | 5.38 |

The 48 random units give the null range. No unit passes.

**2025-07-08** (`run-20250708.log`, `results-20250708/`, `ledger-20250708.jsonl`, `RESULTS-20250708.sha256`): completed 2026-11-18 02:19 UTC after three resumes (logged in the run log), each picking up at the unit where it stopped. Again the comet track falls below the controls in every named unit.

| Unit | Comet T | Control T |
|---|---|---|
| HI | 4.83 | 5.22 |
| OH 1665 | 4.33 | 4.89 |
| OH 1667 | 5.13 | 5.24 |
| 2×HI | 4.69 | 4.80 |

Random units run from about 4.2 to 5.2 on the comet track. One random unit, LoC.C0352 chunk 107, is high on every track (comet 13.1, controls 21.5, fixed 23.4): interference, not comet-following.

**Next.** The cross-night recurrence check (July 3 against July 8) is to be computed from the two ledgers. Then July 9 and 10 under the same plan.

**Not committed.** The per-unit stacks (`stacks/`, `stacks-20250708/`, `v1/stacks/`) are hashed in `STACKS-not-committed.sha256` and re-derivable with the code here.
