# PLAN-OH13R: the original thirteen, object first, under every representation we have

Frozen before any OH13R product and before any channel-7 voltage was read for it, at the author's word (2026-11-21 11:24 and 11:25): "lets return to the initial hits. bring all the new filters to bear, in different configurations, on the assumption that we may not be able to recognize what is there. object first. we are *assuming* we do not yet have the means to recognize them, and seeing what resolves and doesnt. we try this tritone method along with other variations we have developed and any others that occur to us"; "and lets do the full 833 too, okay if we're running for awhile".

## The premise, and what it changes

The thirteen (oh13/oh13_candidates.json) were selected by one representation: tracked integrated power, ON z ≥ 2.5 in all three ON scans and OFF z < 2.0 in all three OFF scans. The premise here is that whatever is at those coordinates may not be recognizable to that representation or to any one we already use. So the run does three things, in this order.

1. **The object.** Each candidate is looked at before any detector runs: its dynamic spectrum along the comet track, at native resolution, in X and Y separately, in all six scans; its integrated profile; the phase of its centre bins over time. These portraits are products in their own right and are described as seen.
2. **Every representation.** Each candidate window, and a population of matched control windows processed identically, is put through the battery below, in several configurations.
3. **What resolves and what does not.** A detector "resolves" a candidate if the candidate stands apart from the controls under it, in all three ON scans, not in the OFF scans, and in both halves of the ON scans. Each detector's power to see its own target class at the candidates' level is measured by injection, so a detector that cannot see at that level is reported as blind there, and its silence is not read as absence.

Nothing that resolves is a lead unless it also passes the location test and an aggregate family test, as below. Selection by the original detector is not evidence; the candidates' original power contrast is the selection, and only what the other representations show beyond it counts.

## Data and windows

- GBT 3I/ATLAS raw voltages, blc23, scans 0013–0018, coarse channel 7 (FC 1666.9921875 MHz), **all 833 frames** of 2^20 samples per scan, read with voltages/delaymod/dm.py (frames, ephem). Frame j is at t = t0 + (j + ½)·0.358 s; the comet-frame track is f(t) = f_rest·(1 − v(t)/c) with v from the JPL Horizons range-rate table, as in dm.py.
- **Candidate windows**: for each of C01–C13 and each scan, 1,024 native bins (2,861 Hz) centred on the track at mid-scan, stored with 32 bins of margin each side (1,088 bins), both feeds, every frame, as float16 complex after scaling by 1/64. C01 and C02 are 51 Hz apart and share one window, kept under C02's centre; they are the known fixed tone at 1665.615 MHz and serve as an interference reference, not as candidates.
- **Matched controls**: six per candidate, at offsets ±3.2, ±6.4, ±9.6 kHz from the candidate centre, same width, same track (the same drift applied), same storage. An offset is replaced, in the order ±12.8, ±16.0, ±19.2 kHz, if its stored range would overlap another candidate's window or come within 1.5 kHz of a known fixed line (1665.615127, 1665.75011, 1666.0045, 1666.0091 MHz), or within 15 kHz of the coarse channel's edge. The same control set is used in every scan.
- **Configurations of frame**: *topocentric* (a fixed 1,024-bin selection, the centre 1,024 of the stored 1,088) and *comet* (per frame, the 1,024-bin selection follows the track by whole native bins).
- **Representations** built from a window's selection: the native frame spectra (2.79 Hz, 0.358 s); the time series z(t) at 2,861 Hz (per frame, the inverse FFT of the 1,024 bins, frames concatenated); and the segmented spectra R(L) of z(t) in segments of L = 64, 512 and 4,096 samples (44.7 Hz × 22.4 ms; 5.59 Hz × 179 ms; 0.70 Hz × 1.43 s). The **centre band** is the track ±8 Hz: native ±3 bins; R(64) the centre bin; R(512) ±1; R(4096) ±11.

## The battery

Each detector gives one scalar T per window, scan and configuration, computed identically on candidates and controls. Unit phasors are u = X/|X|.

| | detector | representation | T |
|---|---|---|---|
| D1 | power (the original's quantity) | native | centre-band mean power over the scan ÷ the window's median bin power (centre ±20 bins excluded) |
| D2 | phase memory | R(512), R(4096) | max over centre-band bins and lags 1, 2, 4, 8 of \|mean_s u[s+ℓ,k]·conj u[s,k]\| |
| D3 | phase curvature (ChatGPT's frozen OH13 statistic) | native, centre ±64 bins | for d = 1, 2, 4, 8, 16, 32 separately: mean over frames of \|mean_k u[k]u[k+2d]conj(u[k+d])²\| |
| D4 | three-wave closure | R(512) | max over k in the centre band and l (\|l−k\| ≥ 2) of \|mean_s u[k]u[l]conj u[k+l−c]\|, c the centre index |
| D5 | the two-part signal (P3W families) | R(64), R(512) | for each of X+, X−, Y+, Y−, XY+, XY−: max over k in the centre band and l (\|l−k\| ≥ 2) of the family's \|mean_s\| (P3W's stats) |
| D6 | cross-feed coherence | R(512), R(4096) | max over the centre band of \|mean_s X·conj Y\| / √(mean\|X\|²·mean\|Y\|²) |
| D7 | translated shape recurrence (N1625) | R(512) log-power vectors | N1625's family score, best over lags and shifts |
| D8 | hidden modulation | centre-band power series from R(64) and R(512) | max of its periodogram over cycle frequencies 0.05–20 Hz (R(64)) and 0.01–2.5 Hz (R(512)) ÷ the periodogram's median |
| D9a | non-Gaussianity | R(64) centre bin | excess kurtosis of the complex amplitude, mean\|x\|⁴/(mean\|x\|²)² − 2 |
| D9b | compressibility | R(512) centre bin | phase increments quantized to 16 levels; T = −(zlib length ÷ length) |
| D10 | spectral echo | native, integrated | max \|autocorrelation\| of the detrended log power spectrum of the window at lags 4–400 bins |
| D11 | delayed copy | z(t) | max over τ = 4–1,024 samples of \|mean z(t)·conj z(t+τ)\| ÷ mean\|z\|² |

D1, D2, D3, D4, D7, D8, D9, D10 and D11 are computed for X and for Y separately; D5 and D6 carry the feeds in their families. Every detector runs in both frame configurations. Counting each detector × representation × parameter × feed × frame as one statistic gives 96 statistics (listed in the code, `STATS`).

## Inference

1. **Per scan, against the controls.** For a statistic T and scan s, each window's empirical p is (1 + the number of control windows with T at least as large) / (1 + the number of control windows), over all control windows of all candidates in that scan (a control is scored leaving itself out).
2. **Resolution.** A window resolves under T if p ≤ 0.10 in each of the three ON scans, p > 0.10 in each of the three OFF scans, and, computing T on the first and on the second half of each ON scan separately, the sum over ON scans of −ln p exceeds the 90th percentile of the same sum over the controls in each half.
3. **The null rate of resolution** is measured, not assumed: the same rule applied to every control window gives the false-resolution rate per statistic and overall.
4. **Aggregate family test**, per statistic: the mean over C03–C13 of the location contrast Δ = Σ_ON −ln p − Σ_OFF −ln p, against the means of 10,000 random sets of 11 control windows. Reported with its p; Bonferroni over the 96 statistics; and the count of statistics at p ≤ 0.05 against the 4.8 expected.
5. **Lead.** A candidate that resolves under a statistic is a lead only if, under that same statistic, its Δ exceeds every control window's Δ, and the aggregate tests show more resolutions among the candidates than the control population's rate allows (binomial, p ≤ 0.05). The location test is decisive: a resolution with the OFF scans at a quarter or more of the ON excess is not at the comet, as in PLAN-P3W.
6. **C01/C02** are scored like the candidates and reported as the interference reference: what each detector makes of a known ground tone.

## Injection: what each detector can see at the candidates' level

Before the candidates' results are read, synthetic objects are injected into six control windows (one per candidate C03, C05, C07, C09, C11, C13) in the three ON scans only, following the comet track, and the resolution rule is applied to them. The level is set from the selection, not from the new data: the original z ≈ 2.7 per ON scan over 49 steps with a 3-channel boxcar corresponds to a mean power excess of about 0.16 of one native bin's noise power, summed over the centre band. Each class is injected at 1×, 3× and 10× that total power:

| class | target detector |
|---|---|
| a. steady tone on the comet track | D1 |
| b. tone with a slow random-walk phase | D2 |
| c. flat-spectrum quadratic-phase chirp over the centre ±64 bins | D3 |
| d. three-wave triple (k, l, k+l−c), phases locked | D4 |
| e. coupled two-part pair, sum form, within X | D5 |
| f. the same signal in both feeds | D6 |
| g. a spectral shape that recurs, shifted, every 64 segments | D7 |
| h. a tone switched on and off at 1.3 Hz | D8 |
| i. a tone in bursts of 50 ms | D9 |
| j. a narrowband pattern copied at a 200-bin offset | D10 |
| k. noise with a copy delayed by 300 samples | D11 |

A detector whose class does not resolve at 10× is reported as blind to its class at these levels; at 3×, as seeing it only well above the candidates' level.

## Products and stopping

Windows (`win_SCAN.npy`, hashed, kept while the session runs), portraits (`object/`), statistics (`stats.json`), injection results (`inject.json`), the reading (`RESULTS-OH13R.md`) and hashes. Nothing here is tuned after the candidates' statistics are read; any later change is a new plan.

## Amendment 1 (2026-11-21, before any portrait or statistic was computed; the extraction was running and only its progress log had been read)

1. **The comet frame is made by continuous de-Doppler**, not by whole-bin selection. Whole-bin following leaves a residual offset of up to half a native bin (1.4 Hz) whose phase runs freely across the scan and breaks every long phase average (D2 at long lags, D4, D5, D6). The comet configuration is now the topocentric selection's time series multiplied by exp(−iΦ(t)), with Φ(t) = 2π∫off(t)dt the continuous phase of the track's offset from the window centre (interpolated between frame centres), re-transformed per frame. `common.selection` returns the topocentric selection only; `common.phase_track` and `common.dedop` make the comet frame. This is what "follows the track" was meant to do; the topocentric configuration is unchanged.
2. **Injections** are made on the topocentric selection, following the track with the same continuous phase Φ, and then pass through both configurations like the data.
3. **Class details fixed in the code**: d, tones at +1, +37 and +38 R(512) bins from the track (k + l − c = m); e, tones at 0 and +53 R(512) bins; g, eight tones at random offsets within ±40 R(512) bins, present in every 64th segment. A code check on synthetic noise at 30× (not part of the run) moved the target statistics of a, b, d, e, f, h, i and j and left c, g and k unmoved at that level; c, g and k carry their power spread over many bins or a low duty cycle, and the injection test will report whether any level reaches them.
