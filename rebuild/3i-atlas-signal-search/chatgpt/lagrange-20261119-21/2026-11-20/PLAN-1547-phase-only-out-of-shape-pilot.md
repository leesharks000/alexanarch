# Fixed-range GBT phase-information pilot — 1547.72 MHz (2026-11-20)

## Status
**Detector implemented and synthetic tests executed; real-data voltage run is NOT complete in ChatGPT runtime due to Berkeley DNS resolution failure.** Public complex raw GBT data are accessible from networked collaborator; already successful for C19. A complete runnable bundle (`phase_outofshape_gbt.py`, frozen detailed PLAN, validation JSON) was generated as a conversation attachment `GBT-1547-phase-information-pilot.zip` on 2026-11-20. The code should be transferred to the networked environment, retaining the frozen parameters.

## Source
Original public GBT 3I/ATLAS raw voltages, December 18 2025, scans 0013–0018 (ON/OFF alternation), channel cc48 at FC 1546.875 MHz. Existing GBT decoder is at `leesharks000/alexanarch/rebuild/3i-atlas-signal-search/claude/voltages/delaymod/dm.py`. Set `dm.CH=48`, `dm.FC=1595.21484375e6+93.75e6-(48.5)*2.9296875e6`.

Fixed search: **1547.720000 MHz center**, complex Fourier slice of **65,536 native bins** (~183.105 kHz; 1547.62845–1547.81155 MHz), **16 voltage frames per scan** (~5.73 s), both X and Y, all six scans. Transfer budget approximately 384 MiB of range-requested channel payloads, not 1.35 TB.

## Two deliberately unconventional filters
1. **Phase-increment memory**: FFT crop -> complex time series -> flat Fourier magnitude, preserve phase -> unit-phase temporal increments; calculate lagged complex dependence at lags [2,4,8,16,32,64,128,256,512] samples.
2. **Four-frequency phase closure**: within the spectrally whitened stream use non-overlapping 512-sample FFTs, 128 frozen nontrivial quartets with k+l=m+n, seed 20261120, and average unit-complex phasor closure. Invariant to common segment phase shifts and temporal origins, sensitive to some higher-order couplings invisible in ordinary averaged power spectra.

For each scan and feed generate **19 whole-frame Fourier-phase-randomized surrogates** preserving each frame's exact spectral magnitudes; compare each filter's maximum over its parameter family with matching maximum across nulls. 19 is a **pilot** with p floor 0.05, not sufficient to claim detection. Score additional two feeds × six scans × two filter families and use real pointing and instrumental negatives. A candidate trained in ON0015 must reproduce at the same lag/quartet in independent ON0017 and not be similarly present in OFF0014/16/18. Only then scale up to all 833 frames / scan and 199+ surrogates, plus injection recovery and independent RFI comparisons.

## Executed synthetic validation
- A repeated QPSK-like phase-coded sequence in complex noise (after spectral magnitude flattening) gave lag-2 phase-increment memory **0.001826**, whereas matched synthetic noise gave **0.000229**.
- An imposed balanced four-tone phase closure gave **0.702** at the frozen quartet, compared with **0.051** for noise at the same quartet.
- The entire analysis path including surrogate comparison passed a miniature smoke test. These tests validate specific capabilities of the detector, **not any signal in telescope data**.
- The attached full Python and validations were executed locally. The container lacked actual GBT complex voltage bytes; the checkpoint zip contains headers and download ledger but not payload blocks.

The freeze is deliberately narrow and confirmation-ready. Do not widen frequency or adjust tests based on results without versioning the plan. Even a reproducible phase dependence is not by itself extraterrestrial evidence.
