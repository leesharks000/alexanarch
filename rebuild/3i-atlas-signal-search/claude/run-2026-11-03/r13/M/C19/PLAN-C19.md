# PLAN-C19: the cc19 frequency family in the raw voltages

Frozen before any C19 product. M4, M4b and their code are untouched.

## The lead

1. M4b cc19 (GBT, 2025-12-18, scans 0013–0018; FC 1631.8359375 MHz) holds 19 ON event records: 6 Class A nominations at 5 distinct frequencies, 13 Class B.
2. Fourteen of them sit on two interleaved arithmetic sequences sharing a step of 67,433.172 Hz, offset 20,152.417 Hz, RMS 8.87 Hz (Lagrange Observatory, RESULT-GBT-cc19-two-interleaved-combs.md, reproduced here exactly from M4b/events/cc19.json).
3. The sequences were found after looking at the catalogue. Nothing in this plan treats them as a blind detection.
4. The band (1626.5–1645.5 MHz) is an Earth-to-space mobile-satellite allocation. Allocation is a prior on interference, not a cut.

## The criterion (the author, 2026-11-18)

A lead must be in the comet, not interference, and weird as voltage. Replication across scans is not required; the OFF scans are the interference test, not a strength bar.

## Data

1. Coarse channel 19, scans 0013–0018, both polarizations, all 833 frames of N = 2^20 samples per scan, streamed from bldata.berkeley.edu by dm.frames (hash below), DF = 2.794 Hz.
2. Bin for topocentric frequency f: b = N/2 + (FC − f)/DF − 0.5 (the inverted mapping of mdhits.py).

## Targets (fixed before streaming)

1. E: the 14 comb event frequencies and the off-grid Class A at 1631.863676 MHz (15 lines).
2. G: every other position of both sequences (shared step, two intercepts from the shared fit) inside the channel, ±1.35 MHz of FC.
3. K: the candidate carrier centres for the sideband hypothesis, c_k = f_A0 + 10,076.21 Hz + k·33,716.59 Hz, inside the channel.
4. X: controls. Both sequences shifted by half a step (+33,716.59 Hz), and 60 positions drawn uniformly in the channel with seed 19, none within 500 Hz of E.

## Products (c19v.py, one stream per scan)

1. S_s: the scan-mean power spectrum, both polarizations, full resolution (float32).
2. R_s: per-row (17 frames, about 6.08 s) power in ±128 bins around every target, both polarizations.
3. P_s: per-frame power at each target, ±2 bins, at the fixed topocentric bin and at the comet-tracked bin (shift FC·(v(t) − v0)/C/DF from the frozen ephemeris, v0 at the scan's first frame).
4. V_s: per-frame complex spectra in ±8 bins around each E line, both polarizations (complex64), the voltage view.
5. Each product hashed in C19-PRODUCTS.sha256 as written.

## Analyses (c19a.py, after all six scans)

1. Presence. For every target, line strength in S_s (peak within ±3 bins over the median of ±128) per scan and polarization; E against G, K and X, ON against OFF.
2. The comb in the raw spectrum. Comb sum over the normalized S_s for steps 60–75 kHz at 0.5 Hz and every phase, with and without the E bins: does 67,433 Hz stand out of its own step distribution, in ON and in OFF?
3. Time structure. Correlation of the per-row and per-frame power series among E lines, within each sequence, across the two, and against X.
4. Kinematics (ChatGPT's test, 2026-11-20 14:45, kept as stated). Fit each E line's frequency in ON0013 alone; predict its frequency track in ON0015, ON0017 and all three OFF scans without refitting, under (F) a stationary topocentric carrier and (C) a carrier fixed in the comet's rest frame by the frozen ephemeris. Score both by predicted-track power and centroid residual.
5. Polarization. X/Y power ratio and XY coherence per E line against X.
6. Voltage. From V_s: line width, amplitude statistics (kurtosis, burstiness), and modulation of each E line, against X.
7. Catalogue null (c19n.py, no voltages). The same two-sequence search (shared step 60–75 kHz, two intercepts, 25 Hz tolerance, maximum members) run on every channel's M4b ON events and on each channel's role-reversed control list. Where cc19 ranks.

## Reading

1. A lead in the comet: present in ON, absent from all three OFF at both the fixed and the comet-predicted track, and model C predicting the held-out ON scans better than model F.
2. Interference: present in OFF at the fixed track. Then the products say what mechanism they can: a shared envelope (one emitter), a step continuing through G (a clock or raster), a centre in K (sidebands of one carrier).
3. Anything else is recorded as what it is. A negative here is a negative for narrowband lines in this channel, not for the comet.

## Limits

1. Narrowband only, at 2.794 Hz. Wideband structure is outside it.
2. M4b's out2/out3 were deleted after hashing; C19 works from fresh streams, not from them.
3. The catalogue null is selection-matched only in its detector, not in the act of looking that found cc19's family.

## Inputs (sha256)

84c73606b4880df68297c0866c645b0350c18a14b09d0fa101da7185f29deb7e  M4b/events/cc19.json
98a1c79d8ce229a949da9e3fdec4d8871995907f3cb985834d9c5da23d552b29  mvb.py
91c7cb62aeaad4c109164b2bf1cc84ded2f4ef0a25790402fb5d250a0d970ebe  mdhits.py
190992d522927fdef300252dadffa75584104c59297e79f5584c825a10b93acb  voltages/delaymod/dm.py
1bf4b7ffc4cefb4edff55c7a3ce2253676e9543526544589859503fb3e940354  voltages/delaymod/horizons-gbt-20251218.txt
3e14f22526c4db180969568dfb544c1bd4a1f0534f56a7ef6b1bdec451426ac3  lagrange-observatory:research/3i-atlas/2026-11-20/RESULT-GBT-cc19-two-interleaved-combs.md
ea724df3366b05eee93a2f22ff252b73adc39743ba58db7f43ee0b6198656764  lagrange-observatory:research/3i-atlas/2026-11-20/reproduce_cc19_comb.py
