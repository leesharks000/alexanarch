# 3I/ATLAS GBT raw voltages: completed full-cadence C03 pass

Lee Sharks research session · 16 November 2026 · full-cadence plan v1 complete

**The full selected-channel voltage pass is complete. C03 gains no exceptional coherent support in the tested family. Its earlier weak power feature is reproduced, rather than newly refuted. The complete raw-header sequence strongly supports ON17 tracking near the comet after its initial snapshot. No emitter is identified.**

## Scope and provenance

The user authorized continuation after the three-window pilot. The expanded plan was saved as PLAN-full-cadence-v1.md, identity libfile_61471638399c81919f551d81ebaaf3bf, before new full-cadence source powers or phase statistics were decoded. The first-pass plan and results are preserved. Prior data and selected windows had already been inspected; this is a targeted analysis of the original observations, not a blind independent-epoch replication.

All **10,056 raw blocks**, 1,676 per scan for GBT L-band scans 0013–0018, were acquired for coarse channel7. That is **21,088,960,512 voltage bytes**, about 299.931883 seconds per scan. The 612 previously saved blocks were restored and reused; 9,444 blocks were newly read. The entire 1.35 TB node was not transferred. Public source: https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/ . Grouped HTTP byte ranges retrieved headers and the selected channel while omitting the other 63 coarse channels. Every range, block length, packet index and retained payload hash was checked.

The public baseline is Glas and Trace's *What the Filters Kept* (#1742 v1.2) and Sharks's *A Firm No* (#1743 v1.1); the private 8 November power/gain and follow-up results remain distinct. No email, public deposit or automation was made.

## Full header audit

All 10,056 block headers have the expected packet-index progression. They report zero NDROP and DROPBLK for the recorded blocks. CAL_MODE remains OFF and CAL_FREQ 0. These findings do not identify the physical origin of any feature or translate lifetime counters into percentages of a scan lost.

For ON17, blocks 0–8 retain the initial UNKNOWN state and discrepant position. Block 9, at1.610613 seconds, changes to TRACK near the comet. The remaining **1,667 blocks stay in TRACK**. From 10 seconds onward, the largest recorded separation from the interpolated saved ICRF comet position is approximately **0.0525 arcmin**, with median 0.0175 arcmin. The OFF pointings settle approximately one degree away, as expected for this cadence. ON13/15 also remain near the comet after their opening positions.

This is stronger evidence than the pilot's file-boundary samples. The initial header should no longer be used as evidence that ON17 was persistently off target. These are instrument-status fields with update latency, finite precision and approximate ephemeris interpolation; they are not an independent antenna-metrology record or a calibrated astrometric error bound. On-target tracking leaves interference and noise open as explanations.

![ON17 complete header sequence](sandbox:/workspace/scratch/9f78dcee6678/atlas-voltage-full-20261116/deliverables/GBT-ON17-full-header-track.png)

## Decoder and numerical checks

The implementation follows the official rawspec signed-int8 normalized conversion and verified FFT frequency orientation. Across the three independent reference rows 0/24/48 of scan 0013,3,145,728 original fine bins reproduce with maximum relative difference **1.358×10⁻⁶**, without amplitude or frequency fitting. All **10,056 polarization FFT energy checks** pass Parseval conservation, maximum relative difference approximately **1.020×10⁻⁷**. The count is838 FFTframes×2 polarizations×6 scans.

Ten independent explicit inverse-DFT sums verify actual raw-to-subband projection, maximum absolute complex-sample discrepancy6.04×10⁻¹⁰. Twelve direct DFT checks verify the residual-frequency evaluation against ZoomFFT, maximum relative discrepancy7.65×10⁻¹².

Five synthetic raw-stream tone/chirp tests check physical frequency sign and phase progression across FFT/raw-block boundaries. Coherent voltage gain is at least 0.9954 in these tests, including a 250 Hz offset with −0.12Hz/s drift. Rectangular per-frame projection has finite boundary-sample response; the retained-power and boundary-error measurements are saved. The derived complex streams must not be described as unchanged GUPPI bytes.

## The earlier power measurement is reproduced

The 49 native 17-FFT fine integrations were reconstructed for every scan. Applying the inherited fixed physical Gaussian line template and 100 frequency controls gives:

| Scan | Comet-tracked strict score | Current receiver-fixed score |
|---|---:|---:|
| ON 0013 | 2.667040 | -1.275570 |
| OFF 0014 | 1.820874 | 1.505940 |
| ON 0015 | 2.398160 | 0.474134 |
| OFF 0016 | -0.062943 | 0.444743 |
| ON 0017 | 1.848898 | -1.373091 |
| OFF 0018 | -0.958087 | -1.052189 |

The primary comet-template per-integration amplitude arrays agree with the old benchmark within 1.76×10⁻⁶ in dimensionless amplitude. The original strict three-ON gate still fails. This does not overwrite the older tolerance-dependent thirteen-feature detector.

**Receiver-anchor history qualification:** the older physical-benchmark code actually anchored its receiver diagnostic at the first fine integration midpoint, 1665644320.549328 Hz, despite prose describing the first ON midpoint. The current saved plan uses 1665644304.702512 Hz. The 15.846816 Hz difference means those receiver arrays are not a direct decoder-parity comparison. This was caught in validation; the initial unmatched comparison is retained and qualified. It does not affect the primary comet-template reproduction or the prespecified new phase search.

## Coherent family: target and controls searched identically

For C03, 100 local rest-frequency controls at ±1 through ±50 kHz, and the twelve other original coordinates, the decoder retained two complex receiver-basis streams in fixed 256-bin subbands. Their sample rate is about 715.256 Hz and bandwidth about 715.256 Hz. Subband centers stay fixed in the receiver frame across all six scans. The original Doppler trajectory remains inside the selected C03 band. There is no phase connection across different scans.

Two phase models were evaluated: the comet's saved Doppler trajectory and a fixed receiver anchor. Each uses the same residual-frequency bank within ±8 Hz (367 frequencies, spacing about 0.04366 Hz) and four non-overlapping coherence lengths: **0.357914, 1.431656, 5.726623 and 22.906492 seconds**. A family maximum searches all four lengths and all residual frequencies. Every control receives the same search. Robust scores use the control bank's empirical median and MAD; they are **not Gaussian sigma values or calibrated false-alarm probabilities**.

| Scan | Comet family maximum | Controls at least as high | Receiver family maximum | Controls at least as high |
|---|---:|---:|---:|---:|
| ON 0013 | 4.135 | 18/100 | 3.435 | 61/100 |
| OFF 0014 | 4.444 | 3/100 | 4.616 | 4/100 |
| ON 0015 | 3.824 | 34/100 | 3.173 | 87/100 |
| OFF 0016 | 3.286 | 72/100 | 3.532 | 58/100 |
| ON 0017 | 3.803 | 38/100 | 4.007 | 22/100 |
| OFF 0018 | 3.241 | 70/100 | 3.180 | 83/100 |

The three ON results have 18, 34 and 38 of 100 controls at least as high in the comet model. An OFF scan ranks closer to the high end than any ON. **The tested coherent family provides no exceptional, ON-specific support for C03.** This is a comparative finite-bank result, not proof of no source. Short coherence, frequency wandering, other drift laws, modulation outside this family, or a signal below its sensitivity are not excluded.

An explicitly post-hoc shared-template contrast, max[minON(z)−maxOFF(z)], is exceeded by 42 of 100 controls in the comet model and 26 of 100 in the receiver model. It is a supplementary diagnostic, not an additional independent significance test. The secondary CSV includes the other twelve original coordinates; its normalization uses C03's local control bank, so it does not furnish calibrated per-coordinate significances elsewhere in the channel.

![C03 against identical control families](sandbox:/workspace/scratch/9f78dcee6678/atlas-voltage-full-20261116/deliverables/GBT-C03-full-cadence-phase-controls.png)

## Injection recovery

Eighty-eight finite receiver-unit injections were run on the measured complete scan 0013streams: C03 and ten fixed controls, single-polarization or both-polarization additions, with voltage amplitudes 0, .01, .03, .1 times the respective subband receiver RMS. The detector uses the same 64-frame coherence calculation, actual Doppler phase, normalization and residual bank. Recovery requires a peak near the injected frequency and above the 95th-percentile full-family control threshold. This is a constructed benchmark, not survey completeness.

| Injection amplitude / receiver RMS | X only recovered | Both polarizations recovered |
|---|---:|---:|
| 0 | 0/11 | 0/11 |
| .01 | 7/11 | 11/11 |
| .03 | 11/11 | 11/11 |
| .1 | 11/11 | 11/11 |

Zero-amplitude identity passes. Eleven independent coherent zero-bin sums agree with the numerical search to about1.01×10⁻¹². The finite recoveries show that this implementation responds to phase-matched tones in measured noise. They do not provide calibrated flux/EIRP limits, a global probability or a general exclusion of the earlier weak power feature.

## Full raw-power diagnostics

The earlier approximately 11.11 Hz component is present in this raw coarse-channel power. This band was selected in the earlier work, so the present measurement is not a blind discovery. Its all-row, Hann-periodogram peaks and ratios to the neighboring spectral median are:

| Scan | Peak frequency, Hz | Peak/local median power |
|---|---:|---:|
| 0013 | 11.112523 | 8.29 |
| 0014 | 11.112523 | 9.25 |
| 0015 | 11.122525 | 5.27 |
| 0016 | 11.112523 | 377.76 |
| 0017 | 11.112523 | 47.98 |
| 0018 | 11.109189 | 42.36 |

The largest ratio is in OFF16. This remains inconsistent with treating the component as ON-specific. Its physical origin is unassigned; recorded CAL_MODE=OFF does not by itself identify or rule out every instrumental mechanism.

OFF14's broad raw-power excursion is visible in the same general interval as before. In this 2.93 MHz channel and 100-ms binning, the minimum is approximately 0.594 of a local 30-second median at 163.95 seconds. The older roughly 49% dip at 164.39 seconds used a different, wider power proxy and binning. These are distinct measurements; neither replaces the other. No new quality mask was applied to the primary phase or power statistics.

## What this settles and what it does not

The raw voltages were retained, acquired and successfully decoded. The full header sequence supports ON17 being on target after the initial snapshot. The old C03 strict power measurement is reproducible directly from those voltages. The tested coherent-tone family adds no exceptional ON-specific evidence for it. The thirteen remain unresolved, without an identified human or extraterrestrial emitter.

Retained products include twelve separately hashed archives: fine powers and phase-preserving complex subband streams for each scan. These are sufficient to repeat the completed measurement and phase comparisons offline. The complete source-range ledger and raw headers preserve acquisition provenance. The full 21.09 GB coarse-channel payload is not all duplicated in these archives; further whole-channel waveform analyses would need the source blocks, which remain public and locally cached at completion. Original first-pass raw excerpts remain separately preserved.

The evidence package includes the plan, code, all control banks, injections, checks, original comparison inputs, header audits, fast-power arrays, plots and offline restoration instructions. All bounded science jobs are complete. No background execution is required to preserve this result.