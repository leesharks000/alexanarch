# ATA 3664 MHz: two information-dependence filters (executed, 2026-11-20)

**Input:** six real ATA measured power windows (2 simultaneous beams × 19 time integrations × 10,487 channels each; 2,391,036 measurements). Source archive: `ATA-3664-association-progress-2026-11-17.zip`. **Power only**, no raw complex I/Q phase. This is a completed experiment on actual data, not a conceptual proposal.

## Fixed preprocessing
Log power; 513-bin median continuum subtraction; robust MAD scaling and clipping to ±6; remove stationary per-channel fingerprint and per-row common gain trend. Guard band ±1700 Hz around previously identified 3664 MHz carrier. 33 fully unmasked 256-bin (~488 Hz) bands remain.

## Test A — interbeam matching-band amplitude information
In each band, compute each beam's 19-point envelope of residual absolute deviations and positive residuals, then normalized same-band time-series correlations. Score the absolute signed *six-scan mean* across all 33 bands × 2 envelopes. Use 199 globally scored null trials shifting the entire beam-1 time series by 1–18 samples independently in each scan, preserving the within-beam frequency covariance.

**Observed maximum 0.296006** at **3663.990732 MHz** (positive residual envelope). Per-scan correlations: 0.795, −0.139, 0.630, 0.566, −0.087, 0.011. Global shuffled tail **p=0.235**. Not significant.

## Test B — nonlocal frequency-band dependence
Form median-absolute-deviation 19-point envelopes for each band, average the two beams, normalize. Search every nonadjacent pair of bands (exclude positions differing by ≤2); score absolute *signed six-scan mean* Pearson correlation. Generate 199 global-max null trials by independently circularly shifting each band envelope within each scan.

**Observed maximum 0.289260**, pair centers **3663.992685 and 3663.998056 MHz**; per-scan correlations −0.105, −0.154, −0.112, −0.390, −0.441, −0.534. Global shuffled tail **p=0.700**; null maximum median 0.29993, p95 0.35409. Not significant.

## Status and limitations
No new reproducible anomalous information-like dependency recovered in this window. The nulls preserve useful receiver/spectral structure but are not complete physical RFI models; 19 time samples have low power for hidden codes. Searches were confined to two predeclared detector families and the existing ~20 kHz ATA window. No claim about phase coding, encryption, noise-matched signals, wideband spread-spectrum or other observations.

Reproduction code, exact numerical output and full research note provided as `ata_information_dependence_sweeps_2026-11-20.zip` in the conversation. These require the previously uploaded six `windows/scan-*.npz` inputs.

**Next discriminating modality:** retrieve genuinely complex I/Q data, then test phase increments/bispectral relations with receiver, cross-beam, off-pointing and injection controls. The current NPZ archive has only `power`, `frequency_hz`, `metadata`.
