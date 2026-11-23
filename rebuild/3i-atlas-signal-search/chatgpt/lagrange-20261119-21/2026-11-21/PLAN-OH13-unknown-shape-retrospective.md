# OH13 retrospective: unknown-shape recognition, frozen 2026-11-21

**Status:** the candidate coordinates and prior controls have been reread; one phase-curvature detector has been implemented and synthetic-validated. **No reanalysis of the original GBT complex voltages has run in the ChatGPT container**, which lacks DNS access to Berkeley. No ET detection.

## Original object
[Original register](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/oh13/oh13_candidates.json) consists of C01–C13, from GBT scan 0013/15/17 ON and 0014/16/18 OFF on 2025-12-18, coarse channel 7, 1665.53–1668.46 MHz. Original detector specifically selected ON z≥2.5, OFF z<2.0 at comet-rest-frame frequencies. That behavior is *selection*, not new confirming evidence. C01/C02 intersect fixed interference carrier 1665.615127 MHz visible ON and OFF. Remaining 11 are not individually proved RFI, but the original 13 excess is fragile under thresholds and controls.

## Test an unfamiliar structure, not a message
Measure **unit-phase curvature** on original complex FFTs. For complex spectrum X[k], let u[k]=X[k]/|X[k]| and define at lag d:
`Q_d = |mean_k( u[k] u[k+2d] conj(u[k+d])² )|`.
Scan frozen d=1,2,4,8,16,32. This is invariant to an overall frequency-linear phase ramp, and doesn't require a carrier, code alphabet or drift. It is still a specific representation and not a universal detection of something unrecognizable.

Read 2048 native bins around each catalogued candidate's original `f_topo_first_Hz` in *each of six scans*, X and Y separately, plus same-scan sidebands at offsets ±12, ±24, ±48, ±96 kHz when in the coarse-channel passband (protect 10 kHz edges). Extract 16 full GBT complex-voltage frames for pilot per scan, split halves 8/8 without tuning on second half. Use existing `dm.frames` network decoder configured cc07, FC=1666.9921875MHz, and the historical `oh13_candidates.json`. The script computes an ideal independent-phase per-family Monte Carlo control per half (99 default). **Do not trust that p alone:** the receiver's own phase coupling is not captured by independent-phase surrogates. Empirical matched sideband comparisons, OFF same-frequency tests, receiver artifact rejection, candidate-count multiplicity corrections, and confirmation in an untouched ON scan are indispensable.

The candidate rests at a historically selected frequency; its power contrast and ON/OFF behavior are not an independent finding. The result may be a heterogeneity assessment with no signal interpretation.

## Executed synthetic self-test (on the local Python implementation)
A flat-spectrum *quadratic phase* waveform mixed with Gaussian complex noise: best family p=**0.01** versus 99 phase-randomized magnitude-preserving controls; pure noise p=**0.15**, narrow strong isolated tone p=**0.17**. This establishes detectability of one synthetic phase invariant, not sensitivity across unknown transmissions or telescope instrument noise.

## Original-voltage execution
Runnable GitHub script: [oh13_phase_curvature.py](oh13_phase_curvature.py). Also packaged as conversation download `OH13-unknown-signal-retrospective.zip`.

```bash
python oh13_phase_curvature.py --self-test
OPENBLAS_NUM_THREADS=1 python oh13_phase_curvature.py \
  --dm /path/to/alexanarch/rebuild/3i-atlas-signal-search/claude/voltages/delaymod \
  --catalog /path/to/alexanarch/rebuild/3i-atlas-signal-search/claude/oh13/oh13_candidates.json \
  --frames 16 --surrogates 99 --output OH13-raw-phase-features.json
```

A positive *pilot* must pass family/scale/frequency/candidate correction and matched sideband empirical ranking, then reproduce at same lag in independent ON0017 without retuning and not comparably in OFF. Follow with full 833 frame scan and carefully benchmark injected weak phase patterns before claiming sensitivity.

**Boundary:** cannot validate a truly unrecognizable signal by definition; we can widen representations and test whether our filters discard constructed out-of-family structures. No negative from these filters excludes what they cannot represent.