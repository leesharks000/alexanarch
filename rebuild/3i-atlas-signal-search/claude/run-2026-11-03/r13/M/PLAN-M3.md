# PLAN-M stage 3: weird as voltage

Written 2026-11-18, before any M2 hit was read. The author, 18:04: "it doesn't necessarily need to be weirder in frequency or likelihood than what off produces... it needs to be in comet, not interference, and weird as voltage". Hash in PLAN-M3.sha256.

## What a hit is

The OFF scans are the not-interference test, not a strength bar. A hit, per PLAN-M2:
- comet-tuned in one ON scan (z ≥ 4, beating every false frame ≥ 6 bins distinct by 1.0);
- absent (z < 2 within ±3 bins) from all three OFF scans.

PLAN-M2's ranking against OFF "hits" is not used for nomination here. The ten highest-z hits per ON scan are taken, a cap set by compute.

## Extraction

The coarse channel is streamed again. For each frame (2^20 samples, 0.358 s):
1. Take the hit's bin along the comet's Doppler track: b(t) = p + rint(FC·(v(t) − v0)/c/Δ), where v0 is the first kept row's velocity, as in the stack.
2. Slice ±64 bins and inverse-transform. This gives 128 complex samples per frame per feed, a 357.6 Hz band at 357.6 samples/s.

The frames are concatenated over the scan, with V2's off-target rows excluded. The same extraction is made at:
- six local comparisons, at ±1,800, ±3,600 and ±7,200 bins (±5.0, ±10.1, ±20.1 kHz), in the same scan;
- the hit's rest frequency in each OFF scan, registered by v0 and tracked by that scan's own Doppler.

## The checks, per series and per feed

- **W1, envelope periodicity.** Take the power spectrum of |x|² − mean. W1 is its maximum over 0.1–50 Hz, excluding ±0.05 Hz around multiples of the frame rate (2.794 Hz), divided by its median there.
- **W2, carrier suppression.** pr1 = max/median of |FFT x|²; pr2 = max/median of |FFT x²|². A hit is flagged for suppressed carrier when pr2 exceeds 1.5× every comparison's pr2 and pr2/pr1 exceeds 1.5× every comparison's pr2/pr1. A carrier puts its line in x; phase keying removes it from x and leaves it in x².
- **k4 = E|x|⁴ / (E|x|²)².** Reported, not used to nominate. Gaussian noise gives 2, a steady tone less.

## Weird as voltage

A hit is nominated if, in either feed:
- W1 exceeds 1.5× the largest W1 of its six local comparisons and of its three OFF series; or
- W2's suppressed-carrier flag holds against the same nine.

A nomination is a lead for a closer voltage look (its envelope line, its symbol rate, its sidebands). Its properties then set where to look next.

## The battery on synthetic series, before any data

In 800 frames of Gaussian noise, with a carrier at 0.7 of the noise amplitude:

| Series | W1 | pr1 | pr2 | pr2/pr1 |
|---|---|---|---|---|
| Noise | 15.5 | 18 | 17 | 0.9 |
| Steady tone | 12.3 | 72,700 | 8,920 | 0.12 |
| On/off keying at 1.3 Hz | 2,005 (at 1.30 Hz) | 18,200 | 3,000 | 0.16 |
| BPSK at 2 symbols/s | 12.4 | 707 | 8,780 | 12.4 |

The first draft's rule, pr1 not raised, would have missed BPSK, because noise comparisons put any signal's pr1 above theirs. It was replaced by the ratio before freezing.

## Limits, stated before the result

- **No injection yet.** This battery has no injection calibration of its own. The ChatGPT boundary report (external/chatgpt-20261118) gives sensitivities for a similar envelope and squared-phase screen at 8 Hz bandwidth.
- **Frame boundaries.** Concatenating frames introduces discontinuities at the frame rate, so W1 excludes its harmonics. Other artifacts of the per-frame slicing are shared with the comparisons, which is why the comparisons are the reference.
