# PLAN-L1546: the 1546.977840 MHz line-centred phase-memory probe, run from ChatGPT's frozen plan

Frozen before any L1546 product. The source plan is ChatGPT's (Lagrange Observatory, research/3i-atlas/2026-11-20/PLAN-1546-977840-line-phase-injection-validated.md, sha256 a15946fd…). Its code, line_phase_probe.py, is a conversation attachment not in Lagrange; this run implements the plan's text independently. Choices the text leaves open are fixed here, before any voltage is read, and marked as this run's.

## The plan's parameters, as frozen there

- Coarse channel 48, FC 1546.875 MHz; line F0 = 1546.9778403639793 MHz (C4850 reading 2).
- Per frame (2^20 samples), the 8,192 native bins centred on F0 (about 22.9 kHz; centre bin 487,480 in dm.fft's order, as ChatGPT's sanity check also gives).
- Flat-field: each frame's complex crop divided by the square root of its power smoothed by a Gaussian of σ = 32 native bins (this run: scipy.ndimage.gaussian_filter1d, mode "reflect"), so lines are kept at their height above the local level; inverse transform to an 8,192-sample series.
- Unit phase increments u[t] = z[t+1]·conj(z[t])/|…|; phase-increment autocorrelation at lags 32, 64, 128, 256, 512. This run: A(L) = |Σ u[t+L]·conj(u[t])| / (number of terms), the sum over all t and frames of the set (as P1547).
- Score: the maximum over the five lags of A(L) over the surrogates' median at that lag. Null: 39 surrogates per scan and feed, each frame's crop with its exact magnitudes and uniform random phases, through the same processing; each surrogate scored the same way against the same medians; family p = (1 + surrogates with score ≥ real)/40, floor 0.025. Seeds this run's: default_rng(15469 + 1000·scan_index + 100·feed + 10·set + k).
- A control at F0 + 8 kHz, same feed and processing.
- Both feeds; six scans. ON0017 the discovery scan, also run on its two halves (frames 0–7 and 8–15) without retuning; ON0013, ON0015 and the OFF scans controls.

## Set A, the plan's frames

The first 16 frames of each scan.

## Set B, declared here before any phase result

The plan notes that 16 frames "may miss the original ON0017 burst". C4850's per-frame power at the line in ON0017 (v_cc48_0017.npz, Pf, a product of an earlier run) is lowest at the scan's start (first 16 frames 1.05×10^6, scan mean 1.55×10^6) and strongest in the 16-frame window starting at frame 401 (3.77×10^6). Set B is frames 401–416 of every scan, the same indices in each, halves 401–408 and 409–416 for ON0017. Everything else as Set A.

## Reading (the plan's decision sequence, made exact)

1. Self-test first (below).
2. A candidate: ON0017 with family p ≤ 0.05 in a feed.
3. If the +8 kHz control in the same scan and feed also reaches p ≤ 0.05, receiver or common-interference structure.
4. If the candidate's winning lag does not reach p ≤ 0.05 at that lag in each ON0017 half (the lag held, no retuning), rejected.
5. Controls: the same lag in each OFF scan, reported with its ratio; a lead must stand above the OFF scans.
6. Any survivor is a lead for the plan's scale-up (833 frames, 199+ surrogates, injection at the line's measured SNR, fixed and comet tracks, polarization, beam limits), and nothing more.

## Self-test (before the data)

Slice-rate complex Gaussian noise, 16 frames of 8,192 samples, a repeated QPSK sequence of period 256 samples added before the flat-field at 0.65 of the noise rms, and plain noise; 39 surrogates each. Accepted if the injection gives family p ≤ 0.05 and the noise does not.

## Limits

The plan's: a pilot, single realizations, trials across scans, feeds, sets and controls not corrected; a negative for weak coded transmissions is weak (the plan's sensitivity table). This implementation is not ChatGPT's.

## Amendment 1 (before any voltage was read)

The self-test fails as frozen: the period-256 injection at 0.65 of the noise rms gives family p = 0.675, plain noise p = 0.125 (selftest.json). The injection does raise the phase-increment memory, at lag 256 to 59.3 and lag 512 to 62.4 (×10⁻³) against 6.1 and 5.1 for noise; but its magnitude-preserving surrogates reach 47.6 and 47.2. A repeated code is a line spectrum, its period carried by the magnitudes, and a random-phase surrogate with those magnitudes repeats with the same period. A null that keeps each frame's exact magnitudes cannot see periodic structure; it tests only phase dependence beyond what the power spectrum implies. ChatGPT's reported self-test (p = 0.025) is not reproduced by this implementation of the plan's text, and the difference is not resolved here.

The frozen test runs unchanged and is read under that limit. Added, as the comparison the self-test shows does respond: the raw A(L) at the line against the +8 kHz control in the same frames, scan and feed, and against the OFF scans at the same frames. A line whose raw memory exceeds its control and stands in ON0017 above the OFF scans is reported as such; with no surrogate test behind it, it is a description, not a detection.
