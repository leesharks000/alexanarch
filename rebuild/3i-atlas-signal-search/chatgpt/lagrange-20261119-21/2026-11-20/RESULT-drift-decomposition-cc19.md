# Drift decomposition experiment 01: cc19 frequency-comb tracks (executed)
2026-11-20 — 3I/ATLAS, GBT blc23, ON scan 0013

**Data:** exact original source `M4b/events/cc19.json` in `leesharks000/alexanarch`; 14 out of 19 preselected events, two interleaved 67.433-kHz grids selected by frequency only *after seeing the catalogue*. No new raw voltages were available. Reproduction: [drift_decomposition_cc19.py](drift_decomposition_cc19.py).

## What was decomposed
A general received track has contributions `fdot_observed = fdot_common_motion + fdot_intrinsic_tx + fdot_propagation + fdot_receiver`. A list of independently fitted frequency rates does **not** uniquely identify those terms. The bounded experiment tests whether rates vary systematically among the frequency teeth, consistent with multiple oscillators/sidebands, or are dominated by fitted resolution effects.

Grid A frequencies: eight, indices -2,-1,0,1,3,4,5,6. Grid B frequencies: six, indices -3,-1,0,2,4,5. All 14 recorded in ON0013 (none in 0015 or 0017 among this selected set). Grid names do not denote independently confirmed transmitters.

## Results
- Grid A fitted drift mean +0.04008815 Hz/s (SD 0.08088312); five of eight selected zero.
- Grid B fitted drift mean -0.03644377 Hz/s (SD 0.02841679); two of six zero.
- Difference A minus B = +0.076531918 Hz/s.
- Exact unstratified two-sided permutation: 56 extreme among 3,003 8-vs-6 allocations, fraction 0.0186480. **Exploratory, not a discovery p-value**.
- One event A at +0.233240 Hz/s dominates variance. Excluding it, difference +0.04893878; unstratified exact 21/1716 = 0.012238.
- **Resolution-stratified exact permutation, conserving A/B counts at each detector level 1, 4, 16: 21/224 = 0.09375.** Thus differences do not clear 0.05 under a more relevant null.
- Per-tooth OLS fitted *rate* slopes: A -0.01700709 Hz/s/tooth (RMS residual 0.05962 Hz/s); B -0.00062253 Hz/s/tooth (RMS residual 0.02588 Hz/s). A slope is strongly influenced by the +0.233 outlier and the mixed resolution classes. Do not read as physical comb-spacing drift.
- Detector confounding: grid A includes 4 Class-A and 4 Class-B events, whereas grid B has only Class-B events. Class-A criteria introduce additional selection differences.
- All reported rates lie on the M4b discrete drift search grid. Grid A and B use different proportions of levels 1,4,16. Treat zero drifts as `0 on this search grid`, not exactly stationary oscillators.
- Resolution-conditioned event rates: level1 A [+.0291550], B [-.0510213,-.0510213,-.0583100]; level4 A [+.0583100], B [-.0583100]; level16 A [+.2332401,0,0,0,0,0], B [0,0].

## Interpretation
There is an *interesting descriptive association* between frequency-family membership and assigned drift direction. It is **not robust** under resolution-stratified label exchanges, does not uniquely decompose source motion, and the family was not independently replicated across ON scans. No extraterrestrial or comet-associated emitter is identified. A shared Doppler component is empirically unresolved in the event list.

## Necessary follow-up using Claude's raw voltage products
- Fix physical frequency values and line assignments from ON0013 as a training selection.
- Extract 14 time-frequency ridge tracks **independently** in ON0015/ON0017 and OFF0014/16/18, allowing subthreshold ridge power and recording non-detections.
- At common time samples and frequency resolution, model `f_i(t) = f_i(t0) + D_comet(t;f_i) + q_0(t) + q_group(t) + n_i * delta_spacing(t) + residual_i(t)` with a *small predeclared* number of temporal coefficients.
- Compare comet motion term against stationary topocentric and alternative Earth-orbital ephemerides using held-out samples. Keep model complexity penalties and synthetic injection recovery; no arbitrary per-tooth drift that absorbs any data.
- Check whether *absolute* comb spacing is stable (shared oscillator sidebands) and whether *fractional* f-dot/f is shared across features (Doppler).
- Execute on the same raw complex X/Y polarization streams. Phase correlation and time covariance can discriminate shared origin. The catalogue's per-event fitted rate alone cannot.

This note does not overwrite the frozen full-band M4b negative result (287 Class A ON vs 506 reverse-role) and does not change the status of 1632 MHz as a band with persistent OFF-source RFI.
