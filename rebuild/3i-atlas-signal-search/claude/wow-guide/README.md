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

## key_gate.py — the six values as time gates and as symbol lengths (2026-11-24, 22:48 EST: "lets do the time gate reading")

6 + 14 + 26 + 30 + 19 + 5 = 100. Read as durations in a unit u, the key repeats every 100 u. Two readings, each per channel and at every start phase: **G1, gates** (on 6, off 14, on 26, off 30, on 19, off 5, either sign), and **G2, symbol lengths** (six successive levels lasting 6, 14, 26, 30, 19, 5). Units: 0.72 s (the key spans the Wow's 72 s), 1 s, 1.2 s, and a hundredth of the scan (3.0 s). blc24 .0002 (2.86 kHz × 1.07 s, 65,536 channels, 1313–1501 MHz), scans 0013–0018. Measured against 50 random keys of six parts summing to 100. The run was stopped once at the session's 30-minute limit and resumed for scan 0018 (key_gate_run1.log, key_gate_run2.log).

- **Gates: nothing.** The key's upper tail (the 99.99th percentile of channels) ranks 0.02–0.40 among the random keys in every scan and unit.
- **Symbol lengths at 1 s stand at the top in the three scans on the comet:** ranks 1.00, 0.98, 1.00, against 0.46, 0.56, 0.84 in the OFF scans. At the other units, ON and OFF are mixed (0.14–0.94 ON, 0.08–0.98 OFF).
- **At the anchors, nothing.** The hydrogen line and the vessel's two frequencies (comet frame), and the hydrogen line and 1420.726 (topocentric): of 240 anchor readings, 12 rank at or above 0.95 against the random keys, which is the one in twenty that chance gives, six ON and six OFF; no anchor channel is above the 99.4th percentile of its scan's channels.

### key_gate_perm.py — the 1 s symbol reading, read (post hoc)

- **Order against size.** Against 60 other orderings of the same six values the key ranks 1.00, 0.75, 0.98 in the ON scans and 0.22, 0.42, 0.93 in the OFF scans. The margins are small: 64.9 against the orderings' 57.6–63.8 in scan 0013; 71.1 against 67.2–72.2 in 0017.
- **Where the channels are.** Channels high in an ON scan and quiet in the OFF after it: 44, 8 and 102 for the key (orderings' medians 37, 8, 94). Of the 44, 39 lie at 1375–1382 MHz; of the 102, 97. That is the GPS L3 transmission centred on 1381.05 MHz, which comes in bursts. It was on during scans 0013 and 0017 and strongest during OFF scan 0016 (980 channels above the line), where the key ranks 0.42. The channels follow L3's schedule, not the pointing.
- **The one cluster outside L3, 1478.49–1478.60 MHz** (read_1478.py): an emitter present in all six scans, ON and OFF (mean excess 0.26–1.0 of the band's power), wandering from 1478.51 to 1478.58 MHz across the half hour, with step-ups of 6 to 30 s. It does not follow the pointing.

### What the time-gate reading leaves

The key as gates opens nothing. The key as symbol lengths at 1 s ranks high in the ON scans, and what it ranks high on is the burst timing of GPS L3 in those minutes, by a small margin over other orderings of the same six numbers; where L3 is strongest the key is ordinary. Nothing at the hydrogen line or at the vessel's frequencies answers to it.

## key_perm.py — the six values as a permutation (2026-11-24, 23:42 EST: "yup, lets run the permutation reading")

6, 14, 26, 30, 19, 5 ranked by size are 2, 3, 5, 6, 4, 1: an order for six things. Read as a transposition key, the stream was scrambled in blocks of six and the key puts each block back. Both conventions are read: **S** = (2, 3, 5, 6, 4, 1), take the block's slots in that order, and its inverse **S⁻¹** = (6, 1, 2, 5, 3, 4). **P1, in time:** blocks of six successive steps of each channel (steps of 1.07 s, 6.4 s, and 11.8 s, Big Ear's step). **P2, in frequency:** blocks of six adjacent channels of each scan's mean spectrum. A right key would make the stream more orderly than it is as recorded; order is the correlation of each sample with the next after re-ordering, at every block alignment. The measure is exhaustive: all 720 orders of six, the recorded order among them. Data: blc24 .0002 (65,536 channels), scans 0013–0018, and look1's fine-resolution windows at the vessel's two frequencies.

- **No channel is put in order by the key.** Channels made orderly (z ≥ 5) under S and S⁻¹ number what any order gives (scan 0013 at 1.07 s: 198 and 204, the 720 orders' median 198, the recorded order 187); ranks 0.42–0.83, in ON and OFF alike, with one 0.06.
- **No channel is lifted above its recorded order in all three ON scans,** under either key, at any step. Scan 0017 has 12 lifted under S, which is the median of all orders there; eleven are one emitter at 1373.87–1373.90 MHz that any re-ordering lifts.
- **In frequency the recorded order is the most orderly of all 720 in every scan** (z 190–200; S 183–192, S⁻¹ 181–189, ranks 0.60–0.68 and 0.23–0.33). The spectrum is not scrambled in sixes.
- **At the anchors, nothing.** P1: 10 of 180 readings rank at or above 0.95 where chance gives 9, the largest z 3.5, none at the same anchor in two ON scans. P2: no anchor window ranks above 0.76.
- **At fine resolution (2.79 Hz, the vessel's frequencies):** no column made orderly by any order; along frequency S ranks 0.27–0.88 and S⁻¹ 0.01–0.99, the two highest (0.99, 0.96) at Ehman's frequency in OFF 0014 and ON 0015.
- **A property of the key itself:** averaged over the whole band S ranks about 0.75 and S⁻¹ about 0.87 in every scan, ON and OFF, coarse and fine. S keeps slots 2–3 and 5–6 side by side, as the recorded order has them, and the receiver's noise has a slight correlation from one step to the next; any order that keeps neighbours together inherits it.

### What the permutation reading leaves

The key as a transposition restores nothing: the data are most orderly as recorded.

## Where the key readings stand

Hop sequence, time gates, symbol lengths, transposition: each run over the 1420 MHz node with its random or exhaustive measure, none opening anything at the hydrogen line or at the vessel's frequencies. Not run: the six values as a spreading code, which needs voltages at 1420 MHz (public raw voltages cover blc23 only, 1501–1688 MHz).
