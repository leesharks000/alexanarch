# 3I/ATLAS cc19 — frequency separation audit on original frozen event catalogue
2026-11-20. Executed: read original GitHub `r13/M/M4b/events/cc19.json` and perform ordinary least squares on 14 retrospectively assigned events; this is NOT raw-voltage spectral tracking.

## Data
Source: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/cc19.json

All **14** assigned events are from ON scan **0013**. A is 8 events, B is 6. Tooth assignments inherited from post-hoc frequency-only candidate identification (do not use this data for naive discovery p-values).

| family | tooth n | frequency MHz | detector resolution (bins per cell) | fitted Hz/s |
|---|---:|---:|---:|---:|
|A|-2|1631.6126212477684|16|+.2332401312|
|A|-1|1631.680078804493|16|0|
|A|0|1631.7475084215403|4|+.0583100328|
|A|1|1631.8149492144585|16|0|
|A|3|1631.949809845537|1|+.0291550164|
|A|4|1632.017232477665|16|0|
|A|5|1632.0846900343895|16|0|
|A|6|1632.1521028876305|16|0|
|B|-3|1631.5653710626066|1|-.0510212787|
|B|-1|1631.7002344876528|4|-.0583100328|
|B|0|1631.7676529288292|16|0|
|B|2|1631.9025233387947|16|0|
|B|4|1632.0373895578086|1|-.0510212787|
|B|5|1632.1048219688237|1|-.0583100328|

## Calculations completed
Fit the model `f_Hz = a + n*spacing + isB*offset` with 14 frequencies.
- Fitted grid interval **67,433.17161935 Hz**.
- B relative A offset **20,152.41708348 Hz**.
- Grid offset / interval **0.29885** approximately.
- Joint RMS residual **8.87496214 Hz**; maximum absolute residual **20.18243943 Hz**.
- OLS regression standard errors (conditional on fixed memberships and independent equal-variance residual assumption): spacing **0.96868 Hz**, B offset **5.46719 Hz**. Because the membership and tooth spacing were *selected from the same catalogue*, these standard errors are descriptive, not confidence intervals for an externally discovered comb.
- Independent A-only fit: **67,434.48320776 Hz**, RMS **9.65156038 Hz**, max abs **14.93609 Hz**.
- Independent B-only fit: **67,431.49129256 Hz**, RMS **4.50996531 Hz**, max abs **9.22208 Hz**.
- Difference A minus B in fitted intervals: **2.99191520 Hz/tooth**. Expanded 4-column OLS fit (`a, n, isB, n*isB`) estimates interaction **-2.99191520** with conditional regression SE **1.8158284 Hz**; F improvement over common-spacing model is **2.7149** with 1 and 10 residual d.f. This does not compellingly reject shared spacing.
- Native spectral bin width **2.793967724 Hz**; level16 bin width **44.7034836 Hz**. Some apparent positions arose from level16 searches and are not known to this precision as isolated physical line centroids. Note a fit RMS <44.7 Hz cannot by itself verify phase coherence.
- Grid spacing / native bin **24135.27223**; grid offset / native bin **7212.83103**; not obvious exact integers, but sufficiently near grid quantization that raster/algorithmic origins must be tested.

### Consecutive observed teeth: per-tooth spacing (Hz)
A adjacent observed teeth (missing teeth handled by dividing interval by n-gap): **67457.56, 67429.62, 67440.79, 67430.32, 67422.63, 67457.56, 67412.85**.
B: **67431.71, 67418.44, 67435.20, 67433.11, 67432.41**.

## Interpreting spacing vs spacing-change
These are candidate-start frequencies recorded within **one ON scan**; differing candidate drift estimates do not establish simultaneous line-frequency tracks at common timestamps. The catalog alone **cannot evaluate d(f_i-f_j)/dt**. It cannot establish that constant grid spacing persists throughout ON13, let alone later ON scans.

The prior drift decomposition audit shows apparent A/B mean fitted-rate difference +0.07653 Hz/s, but resolution-stratified exact permutation 21/224=0.09375. Mixed resolutions and Class A/B biases make an empirical separation-rate claim premature. An extrapolation of per-event rate fits into synchronous trajectories would improperly assume common start time, which the event catalogue does not guarantee.

Next: extract common-timestamp frequency ridge centroids/power for all 14 teeth from **raw** channel-19 spectra in ON13, later ON15/ON17, and OFF controls; report pairwise Δf(t), a(t), possible jitter, correlated modulation across polarization, and the same measurements at jittered fake-grid frequencies and nearby RFI-dominated channels. Keep the frozen grid parameters (67433.171619 Hz / 20152.417083 Hz) fixed when scoring heldout data.

## Standing
The 14 selected frequencies have striking approximate arithmetic regularity. This is catalogue-level organization, potentially a single multi-line carrier group or selection/instrument/satellite artifact. It has not been independently confirmed as a physical emitter, persistent comb, or extraterrestrial transmission.
