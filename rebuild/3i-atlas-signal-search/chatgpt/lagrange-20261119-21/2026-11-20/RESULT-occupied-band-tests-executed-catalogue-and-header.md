# Executed bounded tests: occupied-band comet-source discrimination, GBT 2025-12-18
**Date:** 2026-11-20. **Scope:** original stored M4 comet-frame peak catalogs and user-provided GBT acquisition/header checkpoint. The raw-voltage track-comparison experiment was NOT executed: voltage samples are not present in local data archive, and `bldata.berkeley.edu` DNS resolution failed from this execution environment.

## Test 1 — ON/OFF telescope pointing and acquisition integrity (executed locally)
Input: user-provided `GBT-full-cadence-acquisition-checkpoint-2026-11-16.zip` extracted locally. Verified `header-audit-summary.json` and `native-ledger.json`.
- All six scans 0013–0018: 1,676 blocks each and zero drops; ledger 10,056 block entries.
- Median comet-pointing separation **after 10 s**, arcminutes:
  - ON13 0.0180142; ON15 0.0197848; ON17 0.0174836
  - OFF14 59.997503; OFF16 60.000006; OFF18 60.001723
- These confirm the recorded ON/OFF pointing roles and packet continuity. They are metadata tests, not proof of signal origin.
- The checkpoint lists per-block sample hashes but no 2 MiB raw complex sample payloads. Those bytes were not recoverable in this session.

## Test 2 — independent near-frequency ON/OFF evidence from comet-frame M4 catalogues (executed via GitHub connector)
Sources for each channel:
`https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4/ccNN.json`

Preexisting data arrays: top ten original **M4 comet-frame scores** per scan, NOT the M4b drift-track events. For each of 3 ON scans' ten `top` entries, find the nearest frequency in the 3 OFF scans' ten `top` entries, with `abs(delta Hz)` threshold. This is a deterministic retrospective diagnostic, not a test of every spectrum bin, and not an exhaustive source-identification classifier.

| cc | freq vicinity MHz | ON retained | OFF retained | ON entries within 25 Hz of some OFF | within 100 Hz | within 500 Hz |
|--:|--:|--:|--:|--:|--:|--:|
| 19 | 1632 | 30 | 30 | 3 | 8 | 9 |
| 21 | 1626 | 26 | 30 | 0 | 0 | 0 |
| 22 | 1623 | 30 | 30 | 0 | 0 | 0 |
| 23 | 1620 | 30 | 30 | 0 | 0 | 0 |
| 48 | 1547 | 30 | 30 | 5 | 5 | 8 |
| 50 | 1541 | 30 | 30 | 0 | 0 | 1 |

Selected cc19 direct pairs, nearest OFF across the three OFF scans:
- ON13 1631.8351048976183 MHz, z148.625; OFF14 1631.8351160734892 MHz, z18.203125; separation 11.1758709 Hz.
- ON17 1632.0047210901976 MHz, z41.6875; OFF18 1632.0048021152616 MHz, z8.3515625; separation 81.025064 Hz.
These demonstrate strong near-frequency energy in OFF records. No evidence is offered that either is the exact same physical source; the frequency-only match omits drift and per-integration structure.

Interpretation constraints: the small OFF overlaps for channels 21–23 **cannot** be read as comet localization. Fast satellite drift will move lines far in frequency between scans; the top-10 cap preferentially loses weaker OFF matches. The channels differ drastically in interference occupancy. The original comet-stack hit score z is not an absolute flux and the ON/OFF score ratios cannot be converted into antenna directivity without a beam model.

## Test 3 — M4b comparator (existing frozen results, newly checked against relevant source)
Source: `RESULTS-M4b.md` same source directory.
64 channels; Class A ON 287 vs reversed-role Class A 506. For cc19 A=6 vs 0, cc21 A=19 vs 8, cc48 A=58 vs 8, cc50 A=34 vs 3. However Class A is association to *the candidate's own fitted drift*, not to the ephemeris of 3I/ATLAS. `M4/ccNN.json` comet-frame products have a different weakness: OFF frequency-bin tests can miss drifting RFI. Neither alone executes the user-requested **predictive comet-motion comparison**.

## Source data access attempt
The provided zip contains raw-acquisition scripts plus a full hash/headers ledger for 10,056 sampled 2-MiB channel blocks but not the 21,088,960,512 sample bytes. Attempted a direct HTTP request to `https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/`; runtime returned `URLError: [Errno -3] Temporary failure in name resolution`. No large raw-data download or signal-phase fit was performed. No fake raw-voltage result should be inferred from the successes above.

## Remaining decisive execution
Using a networked environment with raw range retrieval, run the paired hypothesis test described in [the frozen occupied-band plan](PLAN-occupied-bands-comet-matched-discrimination.md). Evaluate **comet-ephemeris predicted frequency track**, **stationary topocentric**, and **orbital-transmitter trajectory** on *the same per-integration data*, fitted on ON13 then scored without refit on ON15/ON17 and OFF14/16/18. Start with cc19 and cc48, then cc21, cc22, cc23, cc50; retain controls and injections. A drift-slope resemblance or coincidence in an allocated band does not resolve source origin.

### Bottom line
The acquisition records validate the pointing control. A modest but real deterministic catalogue comparison finds multiple strong emissions in cc19 on nearby ON and OFF frequencies. No comet-locked signal was demonstrated or excluded by raw-voltage model comparison in this execution.
