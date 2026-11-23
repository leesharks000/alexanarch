# Off-template spectral-echo sweep and next GBT phase target (2026-11-20)

## Executed: ATA spectral echoes
Input: six measured ATA power windows near 3664 MHz, both simultaneous beams, 19 time integrations, 10487 frequency bins each (1.90734863 Hz resolution). Known 3664 MHz line family excised ±1700 Hz.

Filter: average time/beam residual log-power after local spectral baseline/MAD normalization and clip. Search frequency autocorrelation lags 64–1600 bins (122–3052 Hz) for maximal positive repeated spectral pattern, without Doppler, particular line shape or known code.

Null: 199 random independent 64-bin block frequency permutations within two sides of excised central band, preserving within-block spectral relationships. Each null searches the same global max across lags.

**Result:** best lag 747 bins = **1424.78943 Hz**; mean normalized autocorrelation **0.00993636**; median shuffled maximum **0.01150522**; null max **0.01492117**, nominal tail **0.945**. No anomalous spectral echo. This is an executed sweep on actual data, but its null is not a full astrophysical receiver model.

Reproduction package in this conversation: `ATA-spectral-echo-search-2026-11-20.zip`, with `echo_search.py`, `echo_result.json`, and narrative note. The earlier ATA association-progress archive supplies the original NPZ measurement files.

## New raw-voltage external outcome
Claude independently ran P1547 on the public GBT voltages; the 1547.720 MHz phase-only pilot is negative. **Critical injection-derived limitation:** the detector's full-resolution Fourier-magnitude flattening suppresses weak line-spectrum phase structures injected before whitening, so the negative result applies only to the class of broadband phase dependence accessible to this transformation.
[Full results](RESULT-GBT-cc48-1547-phase-pilot-P1547.md).

Claude's raw-voltage cc48/cc50 survey also finds one **unresolved** cc48 line at **1546.977840 MHz** in ON0017, moderately bursty, polarized, and better tracked at fixed topocentric frequency than comet drift. ON excess cannot presently be spatially localized: OFF sensitivity insufficient to constrain a 30 dB attenuated counterpart. No ET or comet association.
[Full results](RESULT-GBT-cc48-cc50-raw-voltages-C4850.md).

## Frozen next experiment proposal — narrow target, new filter
- Target 1546.977840 MHz using cc48 original X/Y complex voltages in all six scans; use ON0017 internal first-half discovery and second-half confirmation, plus three OFF-pointing controls, same fixed frequency and same data-dependent thresholds.
- Pre-data injection gate **required**: inject repeated narrowband phase-coded sequence and balanced four-tone phase closure *before* any spectral whitening, with power comparable to surrounding noise. The previous P1547 design failed this crucial pre-whitening injection.
- Modify whitening: retain spectral envelope at ~hundreds-native-bin scale instead of flattening every native bin; test phase-memory and four-frequency closure across one predeclared modest parameter family. Compare to phase-randomized, time-reversed and block-exchanged surrogate controls.
- In parallel, amplitude-condition short-time phase recurrence using only frozen burst quantiles; test independent ON0017 halves, OFF and X/Y channels.
- Do not count repeatability of a phase anomaly as comet sky localization. Calibrate the spatial discrimination with beam response and realistic injections.

The new GBT experiment is **proposed, not executed**. No new extraterrestrial signal was identified.
