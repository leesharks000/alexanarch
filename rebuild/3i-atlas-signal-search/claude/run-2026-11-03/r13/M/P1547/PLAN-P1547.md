# PLAN-P1547: the 1547.72 MHz phase-only pilot, run from ChatGPT's frozen plan

Frozen before any P1547 product. The source plan is ChatGPT's, frozen in the Lagrange Observatory (research/3i-atlas/2026-11-20/PLAN-1547-phase-only-out-of-shape-pilot.md, sha256 63154ed3…, commit a835862). Its code (phase_outofshape_gbt.py) is a ChatGPT conversation attachment and is not in Lagrange; this run is an independent implementation from the plan's text. Where the text leaves a definition open, the choice is fixed below before the data are read, and marked as this run's.

## Data (the plan's)

GBT 3I/ATLAS raw voltages, 2025-12-18, scans 0013–0018, coarse channel 48 (FC 1546.875 MHz), both feeds, the first 16 frames of each scan (2^20 samples a frame, about 5.73 s), streamed by dm.frames: 64 MiB a scan, 384 MiB in all. Native resolution DF = 2.794 Hz.

## The slice (the plan's)

65,536 native bins centred at 1547.720000 MHz (about 183.1 kHz, 1547.62845–1547.81155 MHz). In dm.fft's shifted order the bin of frequency f is b = N/2 + (FC − f)/DF − 0.5; the slice is the 65,536 bins centred on the rounded b of 1547.72 MHz. The order of the slice is reversed in frequency against the sky (the channel's spectrum is inverted); neither statistic depends on it.

## Whitening (the plan's; the operation this run's)

Each frame's slice F is set to F/|F| (bins with |F| = 0 set to 1) and inverse-transformed to a complex series z of 65,536 samples: flat Fourier magnitude, phase kept.

## Filter 1: phase-increment memory

u[t] = z[t+1]·conj(z[t]) / |z[t+1]·conj(z[t])|. For each lag L in [2, 4, 8, 16, 32, 64, 128, 256, 512]: A(L) = |Σ u[t+L]·conj(u[t])| / (number of terms), the sum over all t in each frame and over the 16 frames of the scan (this run's: one complex mean per scan and feed). The family score is max over L.

## Filter 2: four-frequency phase closure

Each frame's z cut into 128 non-overlapping 512-sample segments, each transformed (numpy fft), phases φ. 128 quartets (k, l, m, n), drawn once with numpy default_rng(20261120): k, l, m uniform on 1..511, n = k + l − m, kept if 1 ≤ n ≤ 511 and {k, l} ≠ {m, n}, distinct quartets, until 128 (this run's draw; ChatGPT's 128 may differ). Closure Q(q) = |mean over all 2,048 segments of exp i(φk + φl − φm − φn)|. Family score: max over q.

## Surrogates (the plan's)

For each scan and feed, 19 surrogates: each frame's slice given uniform random phases with its magnitudes kept (after whitening the magnitudes are 1), seeds fixed (default_rng(1547000 + 100·scan_index + 10·feed + k) — this run's). Both filters run on each.

## Reading (the plan's gates, made exact here)

1. Family test per scan, feed and filter: the rank of the real family score among the 19 surrogate family scores; p = (1 + number of surrogates ≥ real) / 20, floor 0.05.
2. A candidate: in ON0015, a feed and filter with p = 0.05; its parameter is the argmax (lag or quartet).
3. Confirmation in ON0017 at that parameter, same feed and filter, without retuning: the real value above all 19 surrogate values at that parameter.
4. Controls: in each of OFF0014, OFF0016 and OFF0018, at that parameter, the real value is not above all 19 surrogates. ON0013 is reported, not gated.
5. A candidate that passes 2–4 is a lead for the plan's scale-up (all 833 frames, 199+ surrogates, injections), and is not more than that. Anything else is recorded as what it is.

## Validation before the data (this run's)

The same code on synthetic complex noise of the same shape: (a) a repeated QPSK-like phase-coded sequence added, (b) a balanced four-tone set imposed at the first frozen quartet, and (c) plain noise; each scored against its own 19 surrogates. The detector is accepted if (a) and (b) reach p = 0.05 on their filter and (c) does not on either.

## Limits

1. 16 frames and 19 surrogates: a pilot. The p floor is 0.05, and with 6 scans × 2 feeds × 2 filters some p = 0.05 are expected by chance (about 1 in 20 tests).
2. The phase structure of the instrument (the polyphase filterbank and 8-bit requantization) is not modelled; it would stand in OFF as well as ON, which is what the controls are for.
3. This implementation is not ChatGPT's; agreement or disagreement with its numbers is a check of both.

## Amendment 1 (2026-11-20, before any telescope data was read)

The first synthetic run injected at full rate (a QPSK sequence wider than the slice, four tones added and then re-whitened) and neither filter responded. The validation was rebuilt at slice rate in two stages (p1547.py synth, synth.json):

1. **Injected after whitening** (ChatGPT's capability check): phase-increment memory at 168.6× the median surrogate maximum (p = 0.05), four-frequency closure at 19.7× (p = 0.05, at the injected quartet). The implementation detects what the plan's validation tested.
2. **Injected before whitening**, as a signal arrives in the voltages, at 0.25, 0.5 and 1.0 of the noise rms across the whole 183 kHz slice: neither filter reaches p = 0.05 on either signal (score/surrogate maximum 0.81–1.27).

Mechanism: a repeated code and a set of steady tones are line spectra. Whitening each frame at the slice's full resolution (65,536 bins) sets every bin to unit magnitude, so a signal whose power sits in a few hundred lines is reduced to that fraction of the whitened series, whatever its strength. The structure both filters look for is the structure the whitening removes. The validation criterion of this plan for the pre-whitening case is therefore not met, and the run below tests only phase structure that survives full-resolution whitening (broadband phase dependence). The frozen definitions are not changed; the telescope run proceeds as frozen, and is read under this limit.
