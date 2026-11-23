# Six 1631.75–1632.08 MHz Class A records — source traced and reconstructed
**Recovery date:** 2026-11-20. **Observation:** GBT L-band scans 0013–0018, 2025-12-18. **Original experiment:** M4b drift-aware analysis, coarse channel cc19, centre 1631.8359375 MHz. This is NOT an ATA six-event list.

## Canonical source
- Original catalogue: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/cc19.json
- Original frozen plan: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/PLAN-M4b.md
- Commit recording cc19 Class A=6, control A=0: https://github.com/leesharks000/alexanarch/commit/2caa44bafbf0732c37a366568ac1fc1c4a690270

## Recovered event table

All frequency coordinates below are the original catalogue's `mhz_topo` values, *not* independently Doppler-corrected rest frequencies. `z` denotes the plan's local hit statistic. Class A selection requires non-veto in all three OFF scans and evidence above Z_VETO=5 in both other ON scans; no claim of calibrated significance is implied.

| Catalogue A row | Nominating scan | Topocentric MHz | Drift Hz/s | Local z | Other ON scores | OFF scores | Resolution |
|---:|---|---:|---:|---:|---|---|---:|
| 1 | 0013 | 1632.017232477665 | 0 | 30.50 | 0015: 6.35; 0017: 10.22 | 0014: 3.84; 0016: 4.60; 0018: 2.72 | 16 |
| 2 | 0013 | 1631.8149492144585 | 0 | 21.87 | 0015: 8.34; 0017: 7.77 | 0014: 3.23; 0016: 3.78; 0018: 1.36 | 16 |
| 3 | 0013 | 1631.7475084215403 | +0.0583100328 | 19.90 | 0015: 7.27; 0017: 7.19 | 0014: 3.46; 0016: 3.06; 0018: 1.58 | 4 |
| 4 | 0013 | 1632.0846900343895 | 0 | 19.70 | 0015: 6.92; 0017: 9.10 | 0014: 2.94; 0016: 1.96; 0018: 3.62 | 16 |
| 5 | 0013 | 1631.8636760115623 | 0 | 19.47 | 0015: 7.60; 0017: 7.94 | 0014: 3.26; 0016: 3.74; 0018: 3.90 | 16 |
| 6 | 0017 | 1632.017321884632 | −0.1166200656 | 10.22 | 0013: 30.50; 0015: 6.35 | 0014: 3.84; 0016: 4.60; 0018: 2.72 | 16 |

**Critical de-duplication:** Row 6 and row 1 are the same physical line association nominated independently in scan 0017 versus 0013. Their frequencies differ by just **89.407 Hz** and their logged companion scan scores are exactly the same (row 6's 0013 score 30.50; row 1's 0017 score 10.22; both 0015 6.35, and identical three OFF scores). This is **six Class A event records but approximately five distinct candidate locations**, not six independent replicated emitters. Neither the original event count nor its control count should be silently altered; report both raw and deduplicated counts.

## Newly inspected frequency-grid regularity (exploratory/post hoc)

Four of the five locations, sorted, lie near an equally spaced grid, with integers `n=0,1,4,5`:
- n0: 1631.7475084215403 MHz
- n1: 1631.8149492144585 MHz (+67,440.793 Hz)
- n4: 1632.017232477665 MHz (+269,724.056 Hz)
- n5: 1632.0846900343895 MHz (+337,181.613 Hz)

Spacing inferred from the endpoints is **67,436.323 Hz**. Relative to this post-hoc grid the n1 residual is +4.47 Hz; n4 residual −21.23 Hz. The fifth distinct Class A line at 1631.8636760115623 MHz does **not** fit the same grid (nearest-grid mismatch ~18.7 kHz). This regularity is descriptive, *not an independently nominated frequency-comb detection*: the grid was found after looking at the catalogue, and the original coarse search uses native bin widths of ~44.7 Hz at resolution 16. A shared transmitter, receiver artifact, or frequency-allocation structure must be investigated before any nonterrestrial interpretation.

## Competing explanations and test requirements

1. **MSS uplink/RFI:** 1626.5–1660.5 MHz includes mobile-satellite Earth-to-space transmissions. Allocation overlap is supporting context for a terrestrial explanation, not transmitter identification.
2. **Stationary topocentric:** 4/5 distinct Class A lines have zero nominated drift, and the remaining +0.0583 Hz/s is shallow, so a fixed recorded-frequency model is a serious competitor to a comet-following emitted tone. The class A nomination only enforces cross-scan consistency within tolerance, not a demonstrated comet frame.
3. **Comb or common origin:** test all on- and off-scan fine spectra for the 67.44 kHz teeth plus missing teeth n2, n3. Compare how teeth move relative to known satellite emissions and to reference spectral bands. Include weaker Class B candidates, but treat additions as exploratory.
4. **Native voltages:** reload cc19 raw voltage windows (if recoverable) and quantify line shape, simultaneous occurrence, polarization, bursts and off-axis behavior with fixed frequencies. Explicitly distinguish the existing GBT ON/OFF cadence from ATA two simultaneous beams.
5. **Controls:** preserve original control A=0, B=16; do matched RFI-occupancy nulls, role exchange, fixed-frequency continuation and alternate Doppler fits, not only raw event counts.

## Data provenance and present limits
The canonical cc19 JSON contains `n.A=6`, `n.B=13`, `control_n.A=0`, `control_n.B=16`; thresholds `Z_HIT=10, Z_VETO=5, K=0.5, BLK=1024`. Frozen plan SHA-256 stated in catalogue is `00e0b3bba5ef1769dfcaabe0253b0494278a3ba4f4530efa84f4acd90d85bc4d`. This record extracts *published original run values*; the cc19 raw voltage samples have NOT been independently downloaded and rerun in this follow-up. Do not claim a fresh sky test, identified emitter, or calibrated global p-value.

**Prioritization:** the most diagnostic immediate follow-up is the fixed four-tooth comb versus constant-recorded-frequency, comet-Doppler and satellite-interference predictions, rather than claiming six separate exceptional signals.
