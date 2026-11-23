# C48 1546.977840 MHz line-centered phase-memory pilot — implemented and injection-tested
Date: 2026-11-20. Status: **software/injection validated; actual raw-voltage run NOT performed in this execution environment**.

## Why this line rather than the 1547.720 MHz broad slice?
The already executed C4850 voltage survey identified an unresolved narrow line at 1546.9778403639793 MHz, primarily ON0017. The 1547.720 MHz broad phase-only pilot P1547 failed its first narrowband injection due to per-native-bin whitening. Claude's subsequent P1547B recovered a transient lag-2 phase dependence in ON0015 but failed its ON0017 confirmation and showed OFF power. P1547C found similar cross-feed structure in OFF. Accordingly the new test targets the *separate unresolved narrow line*, not the crowded 1547.72 MHz region.

## Executable artifact
`GBT-1546-977840-phase-memory-probe.zip` is supplied in this conversation. Bundle includes `line_phase_probe.py`, `synthetic_test.json`, `sensitivity.json`. This is a fully functioning NumPy/SciPy script; it calls the existing `dm.frames(scan,frames)` in `rebuild/3i-atlas-signal-search/claude/voltages/delaymod/dm.py`. It needs access to original public GBT raw voltage payload from the already demonstrated Berkeley source. Local container attempt failed with `URLError [Errno -3] Temporary failure in name resolution`; no GBT signal was detected or ruled out by **this** pilot.

## Frozen experiment parameters
- Channel cc48, center FC=1546.875000 MHz, fixed line F0=1546.9778403639793 MHz.
- Per full raw FFT take 8192 complex bins centered at F0, approximately 22.89 kHz total (native resolution 2.7939677 Hz).
- Both X and Y; scan 0017 is discovery, split in half before making any claim; ON0013/15, OFF0014/16/18 are controls.
- 16 one-million-sample voltage frames per scan as minimal resource-bounded pilot (~384 MiB for six scans), 39 surrogate controls per feed/scan, yielding Monte Carlo tail floor 1/40=0.025.
- Flat-field each frame's frequency-domain *complex* crop with a 32-native-bin Gaussian-smoothed power envelope (rather than dividing by each bin's native magnitude). Fourier invert to local time series and calculate phase-increment autocorrelation magnitudes over frozen lags **[32,64,128,256,512]**.
- Score maximum ratio to surrogate median; empirical null comprises independently randomized Fourier phases with each frame's *exact measured spectral magnitudes preserved*; each surrogate re-searches all five lags. Also report a second nearby off-line frequency control **+8 kHz** from F0, same feed and processing. Experimental null addresses phase dependence; it does not capture all telescope hardware effects.
- No drift compensation imposed: this explores short-time phase memory, not source localization or Doppler.
- Six scans, two feeds, multiple candidate families imply further trial correction; these 39 surrogates alone cannot justify extraterrestrial or comet association.

## Executed artificial tests
Tested **pre-whitening QPSK-periodic** emission (period 256 samples) mixed into complex Gaussian noise *before* the FFT-based whitening. This is exactly the ordering the preceding P1547 design failed to validate.

Fixed self-test, 16 artificial frames, 39 surrogates:
- Signal/noise rms 0.65: recovered best lag **256**, max ratio to null median **1.333**, empirical tail **1/40=0.025**.
- Matched noise-only: best lag 512, max ratio 1.110, empirical tail **0.625**.

Additional sensitivity check, different random seed, 16 frames and 19 surrogates each:
| injected code rms / noise rms | winning lag | family tail fraction | ratio to surrogate median at lag 256 |
|---|---:|---:|---:|
|0.25|32|0.20|0.944|
|0.35|32|0.45|1.131|
|0.50|256|0.10|1.360|
|0.65|256|0.05|1.356|
|1.00|64|0.05|1.476|

An injected periodic code can produce responses at harmonic/subharmonic lags, hence the 1.0 case's winning lag 64 does not mean exact period recognition. The detector is **not yet sensitive enough to validate the 0.5 rms case** with 16 frames. Its negative result for very weak line-coded transmissions would be weak. These are single realizations, not sensitivity/false-alarm curves.

## Required real-data decision sequence
1. Run `python line_phase_probe.py --self-test`, confirm no assertion and raw-injection detection.
2. Run `python line_phase_probe.py --dm /path/to/voltages/delaymod --frames 16 --scan all` in the external networked worker; capture full JSON plus input hashes. **Note:** code's `--scan all` runs all six scans. The output is a *pilot*, not a blind comprehensive search.
3. If ON0017 survives its family surrogates but local +8kHz control also does, treat as receiver/common-interference structure. If first-half ON0017 candidate does not reproduce in independent second half, reject without frequency or parameter retuning.
4. Any positive requires 833 frames (all six ON/OFF) with 199+ surrogates, pre-whitening injection recovery at the actual line's measured SNR, tests at fixed and comet ephemeris, polarization cross-checks, and rigorous beam spatial-discrimination limits. Without these it remains unresolved observational structure.

## A needed correction before claiming a strong independent confirmation
The current minimal pilot computes all 16 frames aggregated for each scan; it does **not** yet split ON0017 into held-out halves in the automatic analysis. Any report of independent within-ON0017 confirmation would require an explicit rerun on first and second halves, preserving the frozen lags. A preliminary pilot finding must not be called confirmation.

**No extraterrestrial signal identified.** 
