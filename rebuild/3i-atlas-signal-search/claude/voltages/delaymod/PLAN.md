# GBT 3I/ATLAS raw voltages — delayed-copy and modulation search, plan v1

Written 2026-11-17, before any voltage in this pass is decoded. Hash in FREEZE.sha256.

## Data

Breakthrough Listen, public: https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/ — GUPPI raw, blc23, MJD 61027 (2025-12-18 UT), L-band scans 0013–0018 (ON 13/15/17 on 3I/ATLAS, OFF 14/16/18). Coarse channel 7 only (centre 1666.9921875 MHz, 2.9296875 MHz, two complex linear polarizations, int8, TBIN 0.341333 µs). Per block: 7168-byte header (DIRECTIO), then 64 channels × 2,097,152 bytes; channel 7 is read by HTTP multi-range. Nothing raw is stored; products only. Decoding follows rawspec: value/127, clipped at −1.

Frames: 2^20 samples (2 blocks, 0.357914 s); 838 frames per scan; integrations of 17 frames (49 per scan, as rawspec). Frequency orientation is checked empirically on the fixed tone at 1665.615127 MHz before use; the expected mapping is sky f = fc − b, b the baseband frequency, so fine index i = N/2 + b/Δ matches rawspec's index (Δ = 2.7939677 Hz).

Validation gate (must pass before any result is read): the decoded power spectrum, put through the oh13 comet-frame procedure (code/cometframe_raw.py: median-normalise, 3-bin boxcar, comet-path stack, robust z), reproduces C03's tracked z in scan 0013 (3.0) to within 0.1.

Comet Doppler: JPL Horizons, C/2025 N1, observer at GBT (−79.8398, 38.4331, 0.807 km), 1-minute deldot, saved and hashed.

## What is being looked for

A sender that knows our narrowband drift search would not need to put power into one drifting tone. Two forms that search cannot see:

**D. Delayed copy.** The emission contains itself again after a lag τ: an echo, a repeat, or a copy on the other polarization.
- D1 short lag (0.34 µs – 0.179 s): whitened autocorrelation of each polarization and the X–Y cross-correlation, from the scan-mean 2^20 spectrum (spectrum ÷ 1025-bin running median − 1, inverse FFT). A copy x(t)+a·x(t−τ) puts ripple of period 1/τ into the spectrum and a peak at τ.
- D2 long lag (22.4 ms – 150 s): a 512-bin × 22.4-ms power grid per polarization (1024-point FFTs, 64 averaged per step, pairs of bins summed); per-bin normalised time autocorrelation; the bin-averaged autocorrelation ρ̄(τ); X–Y cross-correlation over time.

**M. Modulation.**
- M1 suppressed carrier. Squaring a BPSK signal strips its ±1 modulation and leaves a line at twice the carrier; the fourth power does the same for QPSK. Spectra of x², x⁴ (per polarization, summed) at 2^20, 49 integrations, put through the same comet-frame procedure as the original thirteen (multiplier 2 and 4 on frequency and drift), with 40 false-drift frames as the null. P1 (plain power) is run identically as the control product and must give back the original result.
- M2 envelope modulation, wide. Scan-mean |FFT(|x|²)|² at 2^20 per polarization: lines at a modulation rate, symbol rate, or the spacing of a multi-carrier set (0–1.46 MHz, 2.79 Hz resolution). And per-bin power spectra of the D2 grid: modulation 0.0067–22 Hz localised in a 5.7-kHz bin (the channel-wide 11.11 Hz component is the known reference here).
- M3 envelope modulation, local. Around each of the thirteen coordinates and 100 controls (rest-frequency offsets ±1…±50 kHz from C03), per frame: ±2.86 kHz around the comet-tracked frequency extracted from the frame FFT, back to a 5.72-kHz stream, its |·|² Fourier power accumulated: sidebands and envelope rates 2.8 Hz – 2.86 kHz at the coordinate.

## Rules

Thresholds are robust z (median, 1.4826 MAD) against each product's own reference population, not Gaussian sigma.

- Comet-referenced (M1, M3): a feature counts only if z ≥ 2.5 in all three ON and z < 2.0 in all three OFF at the same rest coordinate (±1 bin); counts are reported at 2.5/2.0 and 3.0/2.0. M1 compares the comet frame's count with the 40 false-drift frames (exceeds the null maximum, or the 95th percentile). M3 ranks each coordinate's ON-minimum against the 100 controls.
- Receiver-frame (D1, D2, M2): the count of ON-only features (z ≥ 5 in all ON, < 3 in all OFF, same lag/bin ±1) under the true labelling is compared with the other 19 ways of choosing three of the six scans. A labelling-specific excess is what would count.
- Anything clearly communication-shaped (a structured repeat, a sideband pattern, a lattice of lines) is reported whether or not it fits these cuts, labelled as outside the rules.
- Every product, list and figure is saved and hashed. Sparse lists keep every bin with z ≥ 2.0 per frame and scan for M1; dense products are kept as float16 where marked.

## Not covered

Lags beyond 150 s; delayed copies that change frequency between copies; cross-band copies (a pattern in one bin recurring in another); modulation slower than 1/300 s; any channel other than 7; phase connection across scans.
