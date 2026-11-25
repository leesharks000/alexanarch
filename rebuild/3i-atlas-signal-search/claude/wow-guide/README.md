# The Wow! as guide and as key: looks, not tests

**The frame, in the author's words (2026-11-24, 22:13–22:15 EST).** "we dont need to confirm by frozen estimates a signal. we are trying to hypothesize a situation in which the wow! signal came from 3i atlas as an artificial vessel intentionally and use it as a clue to find signal in the 2025 data"; "the signal itself would confirm its artificial nature. that is the only kind of confirmation i would accept: structured, legible message"; "we assume that the problem would be a) locating signal, and especially b) recognizing it, but if located and recognized, parseable as message"; "we are even hypothetically treating the wow! signal as if it were an intentionally sent cryptographic key for the 2025 data"; "those are the speculative parameters were working with".

Under this frame the 1977 velocity is not a pass/fail (PLAN-WOW3 R1 asked the wrong kind of question of it). It is a conversion: it turns the Wow's received frequency into the vessel's own.

## look1.py — the vessel's own frequency

If the Wow! was sent at a frequency fixed in the object's frame, that frequency is the received one taken back through the object's 1977 range-rate from Big Ear (−43.011 km/s on the present orbit): **1420.5222 MHz** (revised), 1420.2518 MHz (Ehman). At Green Bank on 2025-12-18 these arrive at 1420.5312 and 1420.2608 MHz.

blc24 .0000 (2.79 Hz × 6.08 s), scans 0013–0018, de-Dopplered to the comet frame, ±6 kHz around each:
- **No line steady in the comet frame.** The strongest column per scan is z 3.8–5.6, and the highest (5.6) is in an OFF scan.
- **No bursts beyond the noise tail.** 6–14 single pixels at z ≥ 5 per scan of about 210,000, in OFF scans as in ON; the largest, z 8.4, is one pixel in ON 0013.
- The revised frequency sits on the slope of the Galactic hydrogen emission (peak 1420.57–1420.58), where the level is higher.
- Only the first of the four Green Bank cadences is read here.

## key_hop.py — the six values as a hop sequence

6, 14, 26, 30, 19, 5 read as the channel, in Big Ear's 10 kHz channels above an anchor, where the signal sits in each successive 12 s step. blc24 .0002, five anchors (the hydrogen line and the two own-frame frequencies in the comet frame; the hydrogen line and 1420.726 topocentric), six cyclic phases.
- **The de-hopped stream holds nothing.** Mean z per scan −0.18 to +0.16. Against 200 random six-value keys the Wow key ranks from 0.02 to 0.96, with no anchor high in all three ON scans (the hydrogen line in the comet frame: 0.85, 0.96, 0.59; OFF 0.45, 0.18, 0.17).
- The de-hopped series are kept in key_hop.json, to be read.

Random keys are kept as the pareidolia measure: what any key of the same form pulls out of the same data.

## look2 — the vessel's frequency in the other sessions (2026-11-24, 22:22 EST: "yes, lets do the last one next")

Which sessions hold 1420 MHz: the other three Green Bank cadences of 2025-12-18 do not (scans 0029–0034 are S band, and the later two higher still), so the first cadence (look1) is all Green Bank has there. Parkes, MeerKAT and the ATA do.

### look2_meerkat.py, mk_scan61006.py — the MeerKAT hit lists

The four public lists (9.57 million hits, SNR ≥ 6) streamed; 713 hits lie between 1419.5 and 1421.5 MHz, on two days: 2025-11-27 (132 hits, one scan, target beam only, listed twice) and 2025-12-19 (449 hits, 64 beams).

- **Three hits in the target beam sit within 10 kHz of the vessel's frequencies, all in the one scan of 2025-11-27 06:15 UT.** In the comet's frame: 1420.5124 and 1420.5264 MHz (the revised frequency is 1420.5222; offsets −9.8 and +4.2 kHz; SNR 12.2 and 16.6), and 1420.2474 MHz (Ehman's is 1420.2518; −4.4 kHz; SNR 12.6).
- **They are teeth of a comb.** The scan lists 132 hits in these 2 MHz, one about every 15 kHz, so any 20 kHz window is expected to hold about one; the same family, at the same drift, runs through that node's 2,318 hits from 872 to 1631 MHz and through a second node's. The 129 of them between 1419.5 and 1421.5 MHz lie on a lattice of 999.9987 Hz (scatter 0.5 Hz) in the telescope's frame, phase 326 Hz, and drift together at +0.076 to +0.081 Hz/s.
- **The comb is fixed to the telescope, not to the comet.** A 1 kHz comb sent from the comet would arrive stretched to 1000.069 Hz by the −20.66 km/s range-rate, which over these 2 MHz is a 138 Hz walk; the fit excludes it. A transmitter fixed in the comet's frame would drift at −0.160 Hz/s at that hour; the comb drifts the other way at half the rate.
- **Which teeth are listed is the threshold.** The family's median SNR is 8.8 against a cut at 6, so the occupied positions (0, 29, 38, 58, 71, 87, 101, …) are where a comb near the cut rises above it. That day was recorded in one beam, so nothing can be localized on the sky.
- **2025-12-19:** every hit in the window lies between 1420.549 and 1420.557 MHz topocentric, one per beam in each of seven scans, in all 64 beams, with drift rates scattered from −10 to +10 Hz/s. That is the Galactic hydrogen line's edge tripping the detector in every beam. None is within 10 kHz of either frequency.

### The ATA ledgers (ata-ontrack/results, results-20250708), read, not rerun

- **Ehman's version (1420.2518 MHz) falls inside the hydrogen unit already searched** (LoA.C1120 chunk 73) on 2025-07-03 and 07-08. The comet track holds no peak of T ≥ 4 within 10 kHz of it on either night; the only such peaks are on control tracks.
- **The revised version (1420.5222 MHz) arrives at 1420.766 and 1420.745 MHz**, which is the boundary between coarse channels 73 and 74 on both nights, inside the 3% edge that the search masks. The ATA cannot read it there.

### look2_parkes.py — Parkes UWL, 2025-07-31, 09-12 and 10-05

blc05 (1344–1472 MHz), 2 Hz × 15 s, every scan de-Dopplered to the comet's frame with the range-rate from Parkes (−24.3, −3.7 and −7.4 km/s on the three dates), ±6 kHz around each frequency; 21 scans, 13 on the comet (S) and 8 on the reference (R). The revised frequency arrives at 1420.637, 1420.540 and 1420.557 MHz; Ehman's at 1420.367, 1420.269 and 1420.287.

- **No line steady in the comet's frame in any scan.** The strongest column per scan is z 3.5–5.0 of 6,001, in R scans as in S.
- **No bursts beyond the noise tail.** 0–6 single pixels at z ≥ 5 per scan, the largest 6.1, in an R scan.
- **Stacked over the S scans of a session, one column stands out:** 2025-07-31, 2,852 Hz below the revised frequency (1420.519345 MHz in the comet's frame), one 2 Hz channel wide, z 3.8, 2.2 and 3.6 in the three S scans (stack 5.56; the next column 3.9) and 2.0, 2.0 and 0.2 in the R scans.
- **Read against its neighbours (look2_parkes_ctrl.py, written after the column was seen):** the same stack over 40 neighbouring windows of the same scans gives largest columns of up to 5.2 in S and up to 5.49 in R, median 4.2. The column is at the top of what an ordinary window gives, by 0.07.
- **It does not return.** At the same comet-frame frequency the Parkes scans of 09-12 and 10-05 read −2.4 to +3.7 (one S scan of nine at 3.7, the rest under 1.4), and the six Green Bank scans −1.5 to +1.0.
- Every other session stack tops out at 3.7–4.2 in S and 3.9–5.0 in R.

### What look2 leaves

The vessel's frequency, taken through the 1977 range-rate, holds nothing recognisable in the 2025 data that reach it: Green Bank's first cadence, three Parkes sessions, the MeerKAT hit lists, and the ATA's hydrogen unit for Ehman's version. The one structured thing met on the way, the 1 kHz comb of 2025-11-27, is fixed to the telescope's frame and drifts against the comet.
