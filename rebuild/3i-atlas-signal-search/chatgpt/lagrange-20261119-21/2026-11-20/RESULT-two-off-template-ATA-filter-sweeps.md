# 3I/ATLAS — two off-template signal sweeps executed on real ATA power arrays (2026-11-20)

**Experiment:** Instead of searching many more frequencies, test a couple of detector shapes on a fixed window without assuming a narrow carrier, constant slope or known modulation. **Result: no additional robust unexplained candidate.** This is an actual data reduction; full code, outputs and six-scan data inputs available in conversation artifact `ata_weird_filter_sweeps_2026-11-20.zip` (analysis source is not automatically on GitHub).

## Grounded data
The user's `ATA-3664-association-progress-2026-11-17.zip` contains six genuine July 3 2025 Allen Telescope Array measured **power** windows, `windows/scan-{0..5}.npz`, each **2 beams × 19 integrations × 10487 bins**, Δf=1.90734863 Hz, centered near 3664 MHz, spanning 20 kHz. Total **2,391,036 measured powers**. This is Stokes I, not complex-phase raw voltage. Metadata stores original telescope URLs, pointing and checksum info.

## Actual sweeps
- **P — nonlinear multiscale persistence.** Per-row log-power baseline removal (513-bin median) + robust MAD normalization + six-MAD clipping. Gaussian frequency smoothing σ=[2,8,32,128] bins. Rank locations by half the median plus half the 35th percentile of power across 19 time integrations. Scans all bins, both beams; no frequency-drift hypothesis.
- **T — unanticipated evolving texture.** Same robust normalized input, tanh transform; remove the time-constant spectrum and time-row mean; scan 256-bin (~488 Hz) time-frequency tiles for leading temporal singular value energy fraction. Detects some evolving correlated multi-frequency structures, not only lines or chirps.

For each sweep/scan compare the **maximum score over its shapes and positions** to 48 null realizations independently circularly shifting measured frequency spectra across time rows, retaining the actual per-row power distributions and RFI peaks but breaking exact frequency persistence. These are *structural shuffle nulls*, not fully physical beam/satellite noise models. Per scan p is (1+extremes)/(1+48), not corrected across six scans or both sweeps.

## Outcome
- P's maximum in **all six scans**: **3664.0002641678 MHz**, always σ=2 bins. Secondary beam's normalized persistence score is **95.9–99.8%** of primary. The frequency is part of the **previously known** 3664 MHz carrier family, not a new source. Each scan has 0/48 null maxima as high → nominal p floor **1/49 = 0.0204 per scan**. This is proof that the filter detects stable structure under this shuffle, **not** evidence of aliens.
- T's maxima: leading singular-value energy fraction **0.0902–0.0946**, versus median null maxima ~0.098–0.0995. Per-scan shuffle-tail fractions 0.94–1.0. No unusual evolving texture.

## Excision/ablation check
A first attempt zeroing ±1000 Hz revealed a false peak immediately outside the excision band, due to filter-edge leakage. Corrected: zero ±1400 Hz and prohibit peaks within a **larger ±1700 Hz guard** around 3664 MHz.

With 24 null shuffles/scan:
- P maximum scores fall from about **5.18–5.29** to **0.27–0.39**; winning frequency bins differ (10486,7922,1912,2110,3997,8130 across scans 0–5). Per-scan nominal tails **0.08, 0.20, 0.16, 0.08, 0.04, 0.40**. The 0.04 is 1/25 Monte Carlo floor, one scan among six and many exploratory choices: **not significant**.
- T's best residual textures remain consistent with shuffled maxima (all tails 1.0).

## What this actually establishes
Both detector families were run **on real recorded time-frequency power**, not preselected event lists. The experiments did not identify any robust new nonstandard signal family. They do **not** exclude phase-only encodings, wideband signals, signals with exactly noise-like power statistics, fast transients, or source motion escaping the limited local window.

**Next experiment (if pursued):** run a completely different detector on *phase-resolved* voltages or a broad coherent power feature with simulated weird but physically plausible injections, and use genuine other-beam/other-pointing negatives rather than only independently shifted rows. Preserve a held-out time interval for blind scoring.

**Reproduction:** archive bundle in conversation includes `weird_sweeps.py`, `weird_sweeps_ablate.py`, primary/ablation JSONs and full technical writeup; input NPZs are inside the previously uploaded ATA archive. Python3 NumPy and SciPy; seed 20261120. Note that the randomized smoothed scale arrays are shifted separately (not a joint multi-scale physical signal null).
