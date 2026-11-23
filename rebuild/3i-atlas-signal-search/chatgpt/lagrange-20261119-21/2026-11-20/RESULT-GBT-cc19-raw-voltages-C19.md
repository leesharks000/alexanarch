# GBT cc19 in the raw voltages: the two-sequence family is a real comb, off-target, not the comet

**2026-11-20.** Executed on the public GBT voltages (bldata.berkeley.edu, range requests), all six scans 0013–0018 of coarse channel 19, both polarizations. This answers the raw-voltage tests asked for in [RESULT-GBT-cc19-two-interleaved-combs.md](RESULT-GBT-cc19-two-interleaved-combs.md), [PLAN-occupied-bands-comet-matched-discrimination.md](PLAN-occupied-bands-comet-matched-discrimination.md) and [RESULT-occupied-band-tests-executed-catalogue-and-header.md](RESULT-occupied-band-tests-executed-catalogue-and-header.md), whose access blocker did not apply from this environment.

Canonical run, frozen plan, code, hashes: [PLAN-C19.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C19/PLAN-C19.md) (frozen before any product), [RESULTS-C19.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C19/RESULTS-C19.md), [C19-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C19/C19-PRODUCTS.sha256), extractor [c19v.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C19/c19v.py), analyses [c19a.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C19/c19a.py), [c19b.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C19/c19b.py), catalogue null [c19n.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C19/c19n.py).

The text below is RESULTS-C19 as committed there.

---


Run 2026-11-20 under PLAN-C19 (sha256 9dd95c7c…), GBT 3I/ATLAS scans 0013–0018 (2025-12-18), coarse channel 19, FC 1631.8359375 MHz, all 833 frames per scan, both polarizations, streamed from bldata.berkeley.edu. Products and hashes in C19-PRODUCTS.sha256.

## Reading, in one paragraph

The family is real and it is not the comet. The raw spectra hold a line comb at the catalogue's step in an OFF scan as fully as in the first ON scan. Its power fades through the observation whatever the pointing, and its teeth hold their topocentric frequencies while the comet's would fall 0.11–0.12 Hz/s. A source at the comet's position would be 30 dB or more fainter in the OFF pointings, 7.8 beamwidths away; this one keeps 24–115% of its ON power there. It reaches the dish through the sidelobes in both pointings: one transmission about 0.7 MHz wide at 1631.5–1632.2 MHz, inside the Earth-to-space mobile-satellite uplink, with a 67,433 Hz line structure (a period of 14.83 μs) and a slowly widening spacing between its two strongest teeth. Its identity is not established.

## The frozen analyses

1. **Presence (analysis 1).** At native resolution (2.794 Hz) the 15 catalogue lines stand modestly above the controls in ON0013 (median peak/median 1.20 against 1.06 for the random controls, p99 1.10) and fall to the controls' level by ON0017. At 16-bin resolution (44.7 Hz, M4b's level) they reach z 8–15 in ON0013 and stay mostly at z ≤ 5 elsewhere. Two untargeted grid positions carry the comb's power: **A n=2 at 1631.882374 MHz** (z 310, 111, 163, 51 in 0013–0016) and **B n=1 at 1631.835093 MHz** (z 129, 53, 31, 23). B n=1 is ChatGPT's 11 Hz ON/OFF pair from the M4 comet-frame catalogue (ON0013 z 148.6 at 1631.83510 MHz). Three more grid positions light in ON0013 (B3, B−2, A7). The sideband-centre positions (K) stay at noise in every scan.
2. **The comb in the raw spectrum (analysis 2).** At native resolution too few peaks pass z 8 to test (1–4 per scan). Run at 16-bin resolution (amendment 3 below).
3. **Time structure (analysis 3).** Frame-to-frame power correlations among the catalogue lines are small (within-sequence 0.03 in ON0013, 0.01 elsewhere; random pairs 0.00). The two strong teeth co-vary on 6 s averages in 0013 (0.40) and 0016 (0.75) and not in 0014–0015.
4. **Kinematics (analysis 4, ChatGPT's test).** Fitted on ON0013 alone and scored without refit, the stationary track carries more of each line's power than the comet track in the held-out scans: all 15 lines in OFF0014, 12 of 15 in ON0015. The margins are small because the lines are faint.
5. **Polarization (analysis 5).** In ON0013 the lines are partly coherent between the feeds (X–Y coherence median 0.093 against 0.044 off the line); afterwards they sink to the noise (0.02). Feed power ratio about 1.0–1.1 for the catalogue lines; B n=1 is steady at X/Y ≈ 0.5 in every scan, ON and OFF.
6. **Voltage (analysis 6).** Amplitude statistics of the catalogue lines (top-5% power share 0.104–0.106, kurtosis 4.1) do not depart from their surroundings. Nothing in the voltages marks them as weirder than a faint carrier.
7. **Catalogue null (analysis 7).** On M4b's ON events, cc19 alone reaches 14 members on two interleaved sequences (18 distinct locations); the next of 64 channels reaches 8; no role-reversed control list passes 5; uniform random lists of cc19's size never pass 6 in 200 draws (p < 0.005). The family is structure, not chance spacing.

## Amendments after the freeze

Added 2026-11-20 from 15:08 on ChatGPT's drift-decomposition proposal (a stationary carrier has two explanations, a nearby transmitter or a Doppler-compensating one, so drift cannot exclude the comet by itself), and on the first pass's read-off. Recorded as amendments; c19b.py.

1. **Location, which drift cannot evade.** Line power above the local median, in units of one bin's noise:

   | | ON13 | OFF14 | ON15 | OFF16 | ON17 | OFF18 |
   |---|---:|---:|---:|---:|---:|---:|
   | A n=2 | 67.99 | 16.48 | 19.38 | 10.09 | 3.11 | 2.22 |
   | B n=1 | 15.35 | 4.99 | 4.34 | 3.21 | 2.75 | 3.11 |
   | 15 catalogue lines | 18.12 | 6.49 | 6.45 | 4.58 | 4.64 | 4.24 |

   The GBT beam at 1.632 GHz is about 7.7′ (FWHM); the OFF pointings are 60′ off, about 7.8 beamwidths, where a source at the comet's position falls by 30 dB or more. The OFF/adjacent-ON ratios here run 0.24–1.15. ON0017 is weaker than OFF0014 and OFF0016. The ON0013 excess is the start of a fade, not the pointing.
2. **Drift decomposition of the strong teeth.** Per-row (6.08 s) centroid tracks, both feeds:
   - B n=1 holds 1631.83508–1631.83510 MHz across all six scans; one linear fit gives −0.0045 Hz/s, RMS 6.9 Hz over 216 rows.
   - A n=2 rises from 1631.882377 to 1631.882436 MHz; one linear fit gives +0.0415 Hz/s, RMS 17.6 Hz over 253 rows; within-scan slopes scatter from −0.16 to +0.25 Hz/s.
   - The comet's drift is −0.107 to −0.124 Hz/s across the six scans.
   - The spacing between them widens: 47,287.4, 47,291.8, 47,302.3, 47,339.4, 47,359.9, 47,341.7 Hz. Under one shared motion two carriers 47 kHz apart would drift alike to 0.003%; their fractional drifts differ. The comb's teeth carry independent frequency processes, or their spacing is not held by one oscillator.
3. **The comb in the raw spectrum, at 16-bin resolution.** The 60 strongest peaks above z 8 in each scan-mean spectrum, then the same two-sequence search as analysis 7: ON0013 17 of 31 peaks at step 67,429.6 Hz; **OFF0014 15 of 32 at 67,433.8 Hz**; ON0015 8 of 19; OFF0016 6 of 15; ON0017 9 of 22 at 67,432.4 Hz; OFF0018 3 of 10. Random lists of 19–40 reach 5–7. The comb stands in the raw data of an OFF scan, not only in the catalogue.
4. **The centre offset.** B n=1 sits 848 Hz below the coarse channel's centre. No other channel's M4 top lists hold a line at that offset (3,586 entries), so it is not a per-channel artefact. The 67,433 Hz grid does not continue into the other 63 channels (7 on-grid top lines of 3,586, 5.4 expected by chance), so it is not a broadband clock.

## Error recorded

The first stream stored the per-row windows (R) as float16, and the powers overflowed it; R was infinite in all four scans written. Those files are kept in first-stream/ with their hashes (first-stream-R-overflow.sha256); their S, Pf, Pc and V are intact and agree with the rerun. The rerun stores R normalized by its window median (RM keeps the medians).

## Limits

1. Narrowband, 2.794 Hz; wideband structure is outside it.
2. The emitter's direction is not measured: a single dish's ON and OFF say only that it is not at the comet.
3. Transmitter identity is not established. The band (1626.5–1660.5 MHz) carries uplinks from terminals on the ground, at sea and in aircraft; no published bearer with a 67,433 Hz structure was found, and Green Bank's public RFI pages list nothing known at 1600–1700 MHz.
4. The v_00NN.npz products (about 25 MB each) are hashed and kept outside git; c19v.py regenerates them from the public voltages.

## Next

1. The same reading in cc48 (1546.9 MHz) and cc50 (1541.0 MHz), where M4b's Class A counts exceed their controls (ChatGPT's list, PLAN-occupied-bands, Lagrange Observatory 2026-11-20).
2. The adjacent channels cc18 and cc20 at ON0013, to bound the transmission's edges.
