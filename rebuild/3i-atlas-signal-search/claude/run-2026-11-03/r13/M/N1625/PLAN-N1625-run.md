# PLAN-N1625-run: ChatGPT's translated-shape recurrence test, implemented, with the event's location test

Frozen before any N1625 product. The source plan is ChatGPT's (Lagrange Observatory, research/3i-atlas/2026-11-20/PLAN-N1625-translated-shape-recurrence.md, sha256 6499cb68…). Its code, n1625.py, is a conversation attachment not in Lagrange; this run implements the plan's text independently. Choices the text leaves open are fixed here and marked as this run's.

## The event

M4b cc21 (events/cc21.json): ON0013, level 4, z_local 58.1, starting at 1625.2936106175184 MHz at the scan's start and drifting +1.691 Hz/s (mdhits.py: the track runs from mhz_topo to mhz_topo + hz_per_s × SPAN). The comet's drift at this frequency is about −0.11 Hz/s. The first 32 frames hold the start of the track.

## Part 1: the plan's test

Data: cc21 (FC 1625.9765625 MHz), scans 0013–0018, both feeds, the first 32 frames. Three slices of 65,536 native bins each: centred on 1625.2936106 MHz (target); +25 kHz (control); 1625.1204237 MHz (the high-drift control). Each frame's crop inverse-transformed and the 32 frames concatenated (2,097,152 samples), cut into 4,096 blocks of 512 samples.

This run's fixed definitions:
- Block spectra |FFT(Hann · block)|², shifted. Each divided by its own median over bins, clipped at 100, log.
- Baseline: a 33-bin running mean (scipy uniform_filter1d, mode "wrap"), subtracted. Each block scaled to unit L2, with the norm floored at the 20% quantile of the block norms of that scan, feed and slice.
- For lag L in [4, 16, 64, 256, 1024] and shift s in −8…+8: c(t) = v[t] · roll(v[t+L], −s). The four-occurrence score is S(L, s, t) = min(c(t), c(t+L), c(t+2L)): a shape recurring three times at lag L, moving s bins each time. Family score: the maximum over L, s and t, among candidates whose participation ratio (Σw)²/Σw² ≥ 4. Here w is the sum over the three pairs of the positive part of v[t]·roll(v[t+L], −s). The ten highest t are examined per (L, s).
- Also reported: the family score with s = 0 excluded; and the leave-one-bin-out score, with the bin of greatest mean power in the scan's block spectra set to zero before scaling.
- Null: 199 permutations of block order within each of the 128 32-block tiles. Family p = (1 + permutations ≥ real)/200.
- Gates:
  - ON0013's first half (frames 0–15, 2,048 blocks; lags up to 256) is the discovery set.
  - Its second half is the holdout. There, the same L and s, maximised over t, must reach p ≤ 0.05 against that half's own permutations.
  - The same (L, s) is then reported in ON0015, ON0017 and the three OFF scans, in both feeds and in the two control slices.
  - A candidate that also stands in the controls, or in the OFF scans at a like level, is interference or uncertain, not a lead.

## Self-test (before the data; the plan's criteria)

- Noise at slice rate, 2,097,152 samples, with a motif made in the voltages before spectral estimation:
  - 4–8 tones, the count random per seed;
  - one 512-sample packet every 16 blocks, with a random common phase and a random envelope factor of 0.5–1.5 per packet;
  - the whole shape translated by s ∈ {−2, −1, 1, 2} bins per repetition, s random per seed;
  - total motif rms 0.25, 0.5 and 1.0 of the noise rms;
  - 20 seeds each.
- 100 noise-only trials.
- A stationary tone and a hopping tone (a random bin each block), each at rms 1.0.
- 19 permutations a trial, floor 0.05, as ChatGPT's self-test.
- Accepted if:
  - recovery at 1.0 is at least 16 of 20;
  - noise passes at most 10 of 100;
  - neither tone is flagged.

If the injections fail, the run stops at the self-test, as the plan requires.

## Part 2: the event's location (added here)

- The full 833 frames of each scan, both feeds.
- Per 17-frame row, the power in native bins from f0 − 1 kHz to f0 + 3.3 kHz (f0 = 1625.2936106 MHz), covering the track's linear extension through all six scans. Scan starts are 0, 317, 635, 953, 1271 and 1588 s after ON0013's.
- Reported:
  - the line's own track in ON0013, fitted;
  - its power along that track, extended linearly, in each later scan.
- The location criterion is C19's: a line whose OFF power is a sizeable fraction of its ON power is not at the comet.

## Limits

- A pilot, with the plan's limits.
- The block-order null tests temporal ordering, not origin.
- This implementation is not ChatGPT's.
