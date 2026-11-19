# M4 nominations: running notes

**Correction (2026-11-19).** Commit 398a499741 ("cc01-cc06 complete, 0 nominations") and the bundle issue that carried it were wrong. The log at that commit already recorded 12 nominations in cc03. The log and volt/cc03.json are correct; only the commit message and the summary misstated it.

These notes are read-off, not results. RESULTS-M4.md is written when the band is complete.

## cc03 (centre 1678.7109 MHz): 12 nominations, all W1

1. All twelve lie at 1679.70–1679.98 MHz topocentric, across all three ON scans: 0013 (3), 0015 (6), 0017 (3).
2. Envelope lines: 0.10–0.13 Hz in 0013 and 0015 (W1 up to 198), and 29.999 Hz in 0017 (W1 597 and 601 at 1679.9789 MHz, z 15.2 and 13.0).
3. The same frequencies stand in the OFF scans' top hits from M4/cc03.json: 1679.9813 MHz in OFF0014, OFF0016 and OFF0018; 1679.9788 MHz in OFF0016; 1679.85 MHz in OFF0016 and OFF0018. on_hits_beyond_every_off is empty.
4. The emitter is therefore present with the telescope pointed off the comet. W1 nominates against the OFF series at the hit's own bin, and a source that drifts in frequency between scans passes that test while being off-source.
5. Reading: terrestrial. 1675–1683 MHz is allocated to meteorological aids, the band of radiosondes. A radiosonde drifts in frequency and keys telemetry in frames. The allocation, the drift and the frame-rate envelope still need checking against the scan times and the twice-daily (00Z, 12Z) launch schedule before this reading is entered as a finding.

## cc08 (centre 1664.0625 MHz): 1 nomination, W1

1. 0013#1, feed Y: 1663.3270 MHz topocentric, z 7.25, W1 29.7 at 0.181 Hz, k4 2.19.
2. It appears in ON0013 only. Neither ON0015 nor ON0017 has it among their top hits. A source on the comet should recur in every ON scan once Doppler-corrected.
3. Nothing in the OFF scans' top hits lies at this frequency; the nearest are 1663.3449 MHz (OFF0014, 18 kHz away), 1663.4232 MHz and 1663.2438 MHz.
4. It sits inside 1660–1670 MHz, a band protected for radio astronomy.
5. Standing: a single-scan lead. Plan step: the closer voltage look of PLAN-M3 (its envelope line, its symbol rate, its sidebands), and whether it falls below the top-hit cap in 0015 and 0017 rather than being absent from them.
