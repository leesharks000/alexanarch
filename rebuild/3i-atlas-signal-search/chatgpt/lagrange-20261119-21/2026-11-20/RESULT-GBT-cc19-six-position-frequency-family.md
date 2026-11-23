# GBT cc19: six-position frequency-family trace (catalogue-level inspection)
**Date:** 2026-11-20. **Observation:** GBT 3I/ATLAS 2025-12-18, coarse channel 19 (center 1631.8359375 MHz). **Status:** exploratory interpretation of *already exposed* original M4b candidates; no raw voltage rerun.

Original source [M4b/events/cc19.json](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/cc19.json), plan [PLAN-M4b.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/PLAN-M4b.md), algorithm [mdhits.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/mdhits.py).

## Result: the apparently missing two teeth have related events in the original ledger

Choose a **post-hoc** arithmetic grid from the original Class A outer frequencies 1631.7475084215403 and 1632.0846900343895 MHz, with five equal gaps. This forces endpoints to fit and gives a step of **67,436.32256985 Hz**. Evaluating *all* originally retained M4b event records and the `control_top` list:

| Grid integer | Predicted MHz | Closest recorded feature | Difference | Category |
|---:|---:|---|---:|---|
| 0 | 1631.747508421540 | 1631.747508421540, ON13 z=19.90, drift +0.05831 Hz/s | 0 Hz | Class A |
| 1 | 1631.814944744110 | 1631.814949214459, ON13 z=21.87, drift 0 | +4.47 Hz | Class A |
| 2 | 1631.882381066680 | 1631.882536690682, OFF18 reverse-role z=28.48, drift −0.45190 Hz/s | +155.62 Hz | Reverse-role Class B |
| 3 | 1631.949817389250 | 1631.949809845537, ON13 z=11.95, drift +0.02916 Hz/s | −7.54 Hz | Class B |
| 4 | 1632.017253711820 | 1632.017232477665, ON13 z=30.50, drift 0 | −21.23 Hz | Class A |
| 5 | 1632.084690034389 | 1632.084690034389, ON13 z=19.70, drift 0 | 0 Hz | Class A |

Two further reverse-role Class B events in OFF18 are around 1631.882792339 MHz (z=23.8, offset +411 Hz) and 1631.882948801 MHz (z=12.68, offset +568 Hz), with nonzero negative drifts. These are near the n2 position but **not yet shown to be the same physical line**; association needs corrected time-frequency tracks from raw windows. The exact n3 Class B event falls below the cross-ON threshold in ON15 (3.76) and narrowly ON17 (4.91), while passing the OFF veto, so it is not Class A.

### Implication
The four-Class-A spacing is not a four-line story with two blank slots. The original saved catalogue contains a **near-exact n3 weaker ON record and nearby n2 OFF records**. This is a better lead for exploring a broader receiver/transmitter structure than merely counting six Class A rows. But the grid was constructed after inspection; endpoints were chosen to make it fit; and the n2 OFF association is only approximate. Do not call it a confirmed six-tooth comb, a calibrated statistical excess, or astronomical origin.

Original M4b cc19 result is **six Class A event records, five distinct approximate frequencies**, 13 Class B, zero reverse-role Class A and 16 reverse-role Class B. One Class A at 1632.017 MHz is nominated twice (ON13 and ON17, identical other-scan scores).

## Confirmed detector constraints
`mdhits.py` searches maxima over linearly drifting traces at spectral resolutions L=1, 4, 16, then rescales them by local frequency-region median/MAD. Class A requires an ON hit z≥10, two other ON matched-window z≥5 and all OFF matched-window z<5. The extrapolation window grows with elapsed time and drift. The detector does **not** require a candidate's rate to equal the comet's predicted radial Doppler drift. The 4/5 distinct Class A zero-drifts (plus one +0.05831 Hz/s) therefore establish no comet-locked trajectory.

Neighbor results from canonical catalogues: cc17 (center 1637.6953125 MHz) A=0/control A=0; cc20 (1628.90625 MHz) A=0/control A=0; cc21 (1625.9765625 MHz) A=19/control A=8. These establish local channel heterogeneity, not global rarity.

## Physical-source discrimination
All six grid positions lie within **1626.5–1645.5 MHz**, a documented Inmarsat mobile-satellite earth-terminal uplink allocation. This makes local Earth-to-space uplink interference the leading hypothesis to test, but the allocation is not a specific transmitter fingerprint. See US 47 CFR §80.1077 and ETSI/telecom service records.

1. Reconstruct per-integration power and time-frequency curves at n0..n5 using the original cc19 raw voltages, separately ON13/15/17 and OFF14/16/18. Prespecify ±1 kHz around fixed six grid positions, plus a wider diagnostic RFI field.
2. Compare stationary topocentric, comet Doppler, and moving-satellite transmitter models with the same data and out-of-sample prediction. Class A is NOT proof of the comet model.
3. Distinguish true simultaneously active teeth (same temporal modulation/amplitude variation) from separate signals or processing sidebands. Check polarization, symmetry, receiver spectral artifacts, image frequencies and shared gain changes.
4. Search for exactly spaced teeth in RFI-occupied reference portions with a selection-matched null. Hold out unrelated frequency regions or observation sessions for validation; the six-position grid itself is exploratory and not a blind prediction.
5. Check radio-frequency occupancy and transmitter identification against ground-station logs / satellite ephemerides where available, and point-source localization. The GBT ON/OFF cadence is not simultaneous dual-beam localization.

## Access limitation
The GitHub archive stores event JSON, original analysis code, source-product checksums and `M4b-PRODUCTS.sha256`; it reports that the large `out3` stacks were hashed and deleted. I have not re-fetched the channel-19 original voltage blocks from Berkeley in this turn and have not measured a sky signal independently. Treat this document as a reproducible **catalogue-level inspection**, not a completed raw-data interference attribution.
