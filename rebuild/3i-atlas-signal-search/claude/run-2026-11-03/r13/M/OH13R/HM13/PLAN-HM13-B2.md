# PLAN-HM13-B2: cc21 and Iridium's 90 ms frame

Frozen before any B2 product; hashes in FROZEN-HM13-B2.sha256, committed before the self-test and before any stream. Failing a frozen test bars nothing. M4b, C4850, HM12 and their code are untouched.

## The question, as named in advance

PLAN-HM13-B3B5 §B2 (committed 2026-11-22): cc21 has 19 class-A events against 8 in its role-reversed control (RESULTS-M4b, 1625.12–1625.29 MHz, drifts −7.35 to +1.69 Hz/s, inside 1616–1626.5 MHz, Iridium). "Iridium's TDMA frame is 90 ms, an envelope line at 11.11 Hz, the frequency of the unassigned component in ChatGPT's raw-power report (RESULTS-HM12 A6). Whether cc21's class-A events carry an 11.11 Hz envelope is to be measured there, not assumed."

Two facts recorded before streaming:
1. M4b saved 40 ON events and 15 role-reversed events for cc21; three of the 40 are class A (ON 0013 1625.293611 MHz, +1.691 Hz/s; ON 0015 1625.120424 MHz, −6.064 Hz/s; ON 0015 1625.120737 MHz, −7.347 Hz/s). The other 16 class-A events are not in the file. The channel-wide map below is what reaches them.
2. The first of the three is N1625's event: its target, 1625.2936106 MHz, lies in cc21 (RESULTS-HM13 B5). It is added as target N.

## Data

Coarse channel 21 (centre 1625.9766 MHz), scans 0013–0018, both polarizations, all 833 frames, streamed by dm.frames as in PLAN-C4850. Frames are N = 2²⁰ samples, 0.35791 s, unwindowed, contiguous.

## Products (hm13b2.py, one stream per scan)

1. **Envelopes.** Each frame's spectrum (dm.fft) is cut into 1024 tiles of 1024 bins (2.861 kHz each). Each tile is inverse-transformed to its complex baseband, and its power is averaged over 16 samples: 64 envelope samples per frame, 178.81 Hz, 53,312 samples per scan per tile per polarization.
2. **Envelope spectra.** Per tile and polarization, the power spectrum of the mean-removed envelope, 0–60 Hz, resolution 0.003354 Hz.
3. **Scores.** r(ν) = the largest envelope power within 0.01 Hz of ν, over the median of the power 0.2–1.0 Hz from ν, excluding everything within 0.05 Hz of a harmonic of 11.1111 Hz or of the frame rate 2.79397 Hz. H_I = Σ r(k · 11.1111 Hz), k = 1–4. H_c = the same sum at each of 20 control base frequencies, drawn uniformly from 9–13 Hz with seed 2121, kept only when none of their first four harmonics comes within 0.05 Hz of either family, and at least 0.1 Hz apart.
4. **Spectra for location**: S, the scan-mean power spectrum, and Sc, the same in the comet's frame, as in PLAN-C4850.
5. Saved per scan: S, Sc, r at the four harmonics, H_I and H_c for every tile, and the envelope spectra of the target tiles. Hashes in B2-PRODUCTS.sha256.

The frame rate of our own FFT frames, 2.79397 Hz, has its fourth harmonic at 11.176 Hz, 0.065 Hz from 11.111 Hz (19 resolution bins). It is excluded from the backgrounds, and it is not inside the 0.01 Hz peak window.

## Targets (targets_hm13b2.json, built by hm13b2_targets.py from M4b/events/cc21.json before streaming)

Every saved E (40) and Q (15) event and target N. Each carries the tile holding its recorded topocentric frequency and the two neighbours: a drift of 7.35 Hz/s moves a line about 0.77 tile in a scan.

## Self-test (before any stream; hm13b2.py synth)

Gaussian noise, 833 frames, both polarizations. Into tile 300 a tone gated on for 8.28 ms in every 90 ms (Iridium's burst inside its frame), drifting −7.35 Hz/s from 300 bins above the tile's centre.
1. Seed 1, amplitude 0.075σ: **passes if tiles 299–301 are flagged** (H_I above θ below) in at least one polarization.
2. Seed 2, amplitude 0: **passes if no more than 6 valid tiles are flagged**, counting both polarizations (expected about 2).
3. Seed 3, amplitude 0.03σ: recorded, not gating.

If 1 or 2 fails, the failure is recorded, and the plan is amended in a new commit before any stream.

## The rule (hm13b2_read.py)

1. **Threshold.** Per scan and polarization, θ is the 99.9th percentile of H_c over the valid tiles (the central 92%: tiles 41–982) and the 20 controls. A tile is **flagged** in a scan if H_I > θ in either polarization.
2. **The question.** A target carries an 11.11 Hz envelope if one of its tiles is flagged in its own scan. This is answered for every E, Q and N target, and by name for the three saved class-A events.
3. **The channel map.** For every valid tile flagged in an ON scan: the scans in which it is also flagged. A tile flagged in ON and not in any OFF scan is listed as ON-only.
4. **Location**, per target, as PLAN-C4850 analysis 1 (excess at the fixed bin in S and on the comet track in Sc, in every scan).
5. **A lead** is only what PLAN-C4850's rule calls one: an ON target whose power in every OFF scan, fixed and comet track, is below 1% of its ON power or at noise. An 11.11 Hz envelope makes nothing a lead, and its absence makes nothing a lead.

## Reading, set before the data

1. If cc21's class-A events carry the envelope, and it stands in the OFF scans at the same tiles, they are read as Iridium's frame. That is RESULTS-M4b's reading, now measured: what resembles our own transmission is set aside as ours.
2. If they do not carry it, that is recorded as what it is. The events stay read as interference, by band and drift, until the location test says otherwise.
3. HM12 A6's 11.11 Hz component was measured in a different product, raw power. A frame found here is a candidate mechanism for it, not shown to be it.

## Limits

1. A tile is 2.861 kHz wide, and an Iridium channel is about 31.5 kHz: the envelope is read in a slice of the burst's spectrum.
2. A drifting line crosses tiles. Three tiles per target cover the drift but dilute the envelope.
3. The threshold is set from control frequencies in the same data. Interference with envelope structure at the control frequencies raises θ.

## Inputs (sha256)

In FROZEN-HM13-B2.sha256: this plan, hm13b2.py, hm13b2_targets.py, hm13b2_read.py, targets_hm13b2.json, M4b/events/cc21.json, voltages/delaymod/dm.py, voltages/delaymod/horizons-gbt-20251218.txt, C4850/PLAN-C4850.md.
