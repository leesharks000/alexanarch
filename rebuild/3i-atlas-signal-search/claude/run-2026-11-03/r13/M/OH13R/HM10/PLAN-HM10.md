# PLAN-HM10: the comet's OH line, measured and calibrated

Frozen 22 November 2026, before any HM10 product is read, at the author's word (16:58 EST): "yes lets measure the oh line."

**Why.** Comets make OH from water, and sunlight pumps it, so the 18 cm lines appear in absorption or emission. That is the one effect a normal comet is known to have at these frequencies. Seeing it, or failing to see it at a known depth, calibrates what the search can see. MeerKAT (ATel #17473) reported 3I/ATLAS's OH in absorption on 2025-10-24, at −8.4 ± 3.1 mJy (1665) and −14.2 ± 3.4 mJy (1667).

**What is already known.**
- absorb-calib (absorb/PLAN-absorb-calib.md, 20 November) read the public rawspec spectra of this session, all three pairs. It did not recover the line, and set a three-sigma floor near 1 × 10⁻³ of the system power per 2.8 kHz bin (about 11–12 mJy at an assumed 10 Jy). Its statistic was the mean within ±4 kHz.
- HM6 read the voltage spectrum at 1667 MHz in the first pair and found no line.
- Neither tested whether the pipeline recovers an injected line of known depth, and neither filtered for a line of the comet's real width across both main lines at once. HM10 does both.
- The voltage spectra for 0015–0018 (kept by HM8 as ohC) have not been read.

**Code check before freezing.** hm10.py ran `selftest` on synthetic spectra only: noise on a cubic bandpass, then with a 5:9 absorption pair of depth 1.5 × 10⁻³ at the comet's velocity. Without the line the z values were −0.2 to −0.4. With it they were −2.9 to −3.6. No product was opened.

## 1. Data

- **(A) Public rawspec.0000** total-power spectra (2.794 Hz × 6.08 s), scans 0013–0018, read remotely as absorb-calib read them, ±90 kHz around each line.
- The comet frame comes from the session's Horizons range-rate at the GBT (voltages/delaymod/horizons-gbt-20251218.txt), shifted per spectrum.
- Pairs as absorb-calib: 0013 against 0014; 0015 against the mean of 0014 and 0016; 0017 against the mean of 0016 and 0018.
- **(B) The voltage spectra at 1667 MHz**, X and Y apart, ±70 kHz, in the comet frame: HM6's for 0013/0014 (read before, by HM6) and HM8's for 0015–0018 (not read). The 1665 MHz line lies outside the voltages' coarse channel.

## 2. The measurement

1. Per line and pair: ON/OFF − 1, pooled over the three pairs with equal weight, rebinned to 1.4 kHz.
2. **Matched filter.**
   - Model: a cubic baseline per line, plus one amplitude A on a Gaussian of FWHM 1, 2 or 3 km/s centred on the comet's rest velocity.
   - The joint statistic fits 1665 and 1667 together, at the LTE ratio 5:9 with 1667 the stronger, with A the 1667 peak as a fraction of system power.
   - Each line is also fitted alone, and per pair (2 km/s).
   - 1612.231 MHz (satellite) is fitted alone and reported.
3. **The null.** The same fit with the template centred at 72 line-free offsets, ±25 to ±60 kHz in 1 kHz steps. σ is the controls' robust scatter. z = A / σ, with A's rank among the controls. Negative is absorption, positive emission.
4. **Calibration by injection.**
   - Absorption pairs (5:9) of 1667 peak depth 0.5, 1, 1.5, 2 and 3 × 10⁻³ of system power, at each of the three widths, are multiplied into the ON spectra of all three pairs. They go at 12 line-free offsets (every sixth control), never at the comet's velocity.
   - The joint filter recovers each one.
   - Reported: recovered over injected, and how many of 12 reach z ≤ −3.
   - **The floor** is the smallest injected depth that reaches z ≤ −3 in at least 11 of 12. It is converted to mJy at an assumed 10 Jy (absorb-calib's assumption; the public product is uncalibrated, so all mJy values are approximate).
5. **The voltages (B).** The same filter at 1667, X and Y apart, pooled over the three pairs. The feeds' agreement in sign and size is reported.

## 3. Reading

- **A line:** for some width, the joint statistic reaches |z| ≥ 4 at the comet's velocity and lies beyond all 72 controls, with the 1665 and 1667 single-line amplitudes of the same sign. Sign is not predicted. Whether OH absorbs or emits depends on the comet's velocity relative to the Sun, and that is not computed here. The voltages' X and Y are then read for agreement.
- **Otherwise:** no line at the calibrated floor. The floor is compared with MeerKAT's October depths. A floor above them says the December data could not have seen an October-strength line. A floor below them says the line, if present, had weakened, or its pumping had changed.
- Either way the result says what this pipeline can and cannot see of the one natural signal the comet is known to produce. That calibrates every narrowband reading in the series.

## 4. What stays fixed

No other window, width, baseline order, control set, injection depth or threshold, and nothing tuned after the score. Failing a frozen test bars nothing.

FROZEN-HM10.sha256 hashes this plan and hm10.py.
