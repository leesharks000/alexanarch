# Green Bank high-time follow-up: the original thirteen-candidate band

8 November 2026 · analysis of public Breakthrough Listen total-power spectra · completed

## Result

No periodic feature passed the fixed ON-specific, frequency-localized screen. The burst comparisons likewise do not by themselves supply a comet-source identification. A recurring feature near **11.11 Hz** was followed explicitly as a broadband alternative; it is stronger in OFF16 than in ON13 and is therefore not ON-specific. Its physical origin was not identified.

This is a new time-resolution analysis of the **same six Green Bank observations**, not a new observing epoch or a test of the individual narrowband candidates’ modulation. The high-time product cannot separate those few-hertz-wide features from all other power within a 366-kHz channel.

## Data and extraction

All six scans 0013–0018 were read directly from the Berkeley public portal using HTTP byte ranges. Each contains 858,112 native samples at 349.525 microseconds, about 299.932 seconds per scan. ON scans are 13, 15 and 17; OFF scans are 14, 16 and 18. The prior unresolved ON17 actual-tracking question remains.

For each scan, the cutout preserves high-time indices 48–71: 24 channels, including nine target/boundary channels 56–64 and fifteen adjacent-frequency comparison channels. This is 123,568,128 original float32 values across all six scans. The selected compressed data chunks total **359.6 MB**, compared with **7.85 GB** for the six complete node files. Metadata, initial probes and retries add transfer overhead; the selected-payload number is not a claim about total network traffic. No complete node file was downloaded.

The saved narrowband candidate table maps C01–C03 nearest high-time index 64. The originally proposed eight-channel cutout 56–63 would not conservatively cover that boundary. Both boundary bins are included; FFT wrapping/overlap and channel response prevent equating a nearest-bin assignment with isolated candidate power. The actual public node spans a much wider band than the one candidate-bearing coarse channel.

All extracted powers were finite and positive in the inspected arrays; per-channel zero/negative counts and correlations are in the scan quality tables. Original per-scan headers, ETags, byte ranges and hashes are retained. Thirty direct HDF5 scalar checks agree exactly with the decoded native cutouts. Derived-statistic validation passed 36 checks, including independent complex DFTs and scalar bin reconstruction.

## Burst search

Two branches were retained: channel-wise fractional power relative to its scan median, and differential power after subtracting simultaneous neighboring-channel variation. Neighbor controls use a leave-one-out reference, so a control channel does not help subtract itself. Shared-channel behavior is treated as evidence about bandwidth, not an automatic source identification.

The fixed family contains 4,896 scan/channel/branch/bin-phase rows, at nine scales from 349.525 microseconds through approximately 10 seconds. Native and half-bin-offset branches were kept. A robust pointwise z score is not a global detection significance.

| Scan | Pointing | Largest target raw z | Largest target differential z | Largest neighboring raw z |
|---|---|---:|---:|---:|
| 13 | ON | 6.03 | 6.14 | 5.56 |
| 14 | OFF | 8.63 | 5.89 | 8.08 |
| 15 | ON | 5.74 | 5.87 | 6.14 |
| 16 | OFF | 6.01 | 5.68 | 5.89 |
| 17 | ON | 5.73 | 5.56 | 5.92 |
| 18 | OFF | 6.13 | 5.68 | 11.62 |

The largest first-ON excursion is a single native sample in channel 64, about 67.459 seconds into scan13: raw z=6.03, differential z=6.14. OFF14 reaches raw z=8.63 around 165.090 seconds, falling to z=5.89 after shared variation is removed. These selected extrema are not thirteen resolved pulses and are not tied individually to C03. Full peak times, bin durations, contiguous five-sigma durations and cross-channel context are retained.

The raw 0.100-second envelope also shows a shared OFF14 power dip of about 49% around 164.39 seconds, affecting target and neighboring RF channels together. This is retained as a measured shared excursion; it is not assigned a specific instrumental or terrestrial cause.

The paired ON/OFF comparison uses only three pairs. Its eight label swaps cannot yield a one-sided tail fraction below 1/8; inspecting multiple scales adds further selection. These comparisons are descriptive diagnostics, not a small global p value.

## Periodicity and the 11.11-Hz feature

The primary search covered temporal frequencies 0.1–1000 Hz with full-scan Fourier spectra and Welch estimates. It retained 1,440 top-five peak records and 253 consolidated frequency rules, checked at the same frequency against all scans and RF channels. Local power ratios use a 101-bin median reference with the central five bins excluded. The fixed screening thresholds are explicit in PLAN.md and summary.json. Validation exposed a sparse-footprint discrepancy in the installed one-dimensional filter; the corrected explicit two-dimensional reference agrees with direct order statistics, and all affected primary Fourier results were rerun. The retained regression witness records the correction.

After ON13/ON15 peaks suggested a recurrence, a separately saved adaptive plan fixed 11.095–11.125 Hz and tested the median of all 24 RF channels, the target nine, and the fifteen neighbors. It retained raw common-mode behavior so a broadband signal would not disappear solely because it was subtracted. Later scans were uninspected continuations for this statistic, within the same observation series.

| Scan | Pointing | All-channel peak frequency (Hz) | Local power ratio | Fitted fractional amplitude |
|---|---|---:|---:|---:|
| 13 | ON | 11.109189 | 54.85 | 0.0348% |
| 14 | OFF | 11.112523 | 2.78 | 0.3311% |
| 15 | ON | 11.115857 | 5.23 | 0.0070% |
| 16 | OFF | 11.112523 | 175.88 | 0.0856% |
| 17 | ON | 11.105855 | 126.89 | 0.0527% |
| 18 | OFF | 11.109189 | 71.75 | 0.0460% |

The OFF16 line contrast is about 3.2 times ON13’s in the all-channel statistic. This defeats the proposed ON-only recurrence. OFF14 illustrates why line contrast and absolute Fourier amplitude must be separated: its fitted amplitude is larger, but so is its surrounding temporal-power background, giving a much weaker normalized line. A fitted sine coefficient is a descriptive Fourier component, not proof of a stable sinusoidal transmitter. Half-scan measurements for all three aggregate series are in adaptive-11hz-common-mode.csv.

No specific human transmitter, clock or calibration system was identified. Shared RF-channel structure and OFF recurrence are consistent with interference or instrumental variation, but do not distinguish those mechanisms. Raw-header CAL_FREQ/CAL_MODE/CAL_DCYC and actual pointing/gain records would be useful for source diagnosis; these fields are defined in the Breakthrough Listen data-format documentation, not present in the inspected HDF5 attributes.

## Sensitivity and what this does not test

We ran **896 burst injections** and **288 sinusoidal injections** into representative real target/control sequences. Burst widths were 1, 16, 256 and 4096 samples (0.350 ms, 5.59 ms, 89.5 ms and 1.432 s). Amplitudes are added fractions of one broad channel’s system power. These are prescribed-location/frequency recovery demonstrations, not blind-survey completeness.

In channel64, differential bursts at 3% peak fractional amplitude and 1.432-second FWHM were recovered in 8/8 trials. Single-sample bursts at 30% were recovered in only 1/8; at 100%, 8/8. Sinusoids at 1, 10 and 100 Hz with 0.1% fractional amplitude were recovered for all four tested phases in the raw channel64 branch. All amplitudes, backgrounds and branch differences remain in the injection tables.

One high-time channel is **131,072 times wider** than a 2.794-Hz native narrowband channel. Using the prior conditional C03 fit (26.36 mW EIRP at 1.798 au) gives about 2.900 Jy Hz of integrated flux. Under the same illustrative 12.5-Jy system calibration, putting all of it in one broad channel adds only **0.633 parts per million** of system power. That is roughly 1,600 times below the 0.1% sinusoidal amplitude demonstrated above. This is an illustrative dilution calculation with uncertain calibration/response, not an amplitude upper limit on C03.

Accordingly, the present result does **not** establish that C03 has no modulation, that the thirteen features are all human emissions, or that all deliberately structured emission is absent. It establishes what these particular broad high-time bins did under the stated tests. Voltage phase, individual narrowband modulation and polarization are not recovered by this single-IF total-power product.

## Reproducibility and next useful step

The compact evidence archive contains the scripts, plans, original candidate records, per-scan metadata and byte-range hashes, all burst/peak/crosscheck ledgers, injection trials, diagnostic plots and validation results. Six separate native ZIPs preserve the original-resolution cutouts; confirmed IDs are in results/checkpoint-state.json. Dense scratch Fourier arrays and redundant event cutouts are regenerable from the native inputs and code.

For the individual narrowband candidates, the next informative product remains the recorded voltages or a suitable intermediate time/frequency product. For the newly measured 11.11-Hz broadband feature, original acquisition/calibrator headers and antenna/gain records would test an instrumental origin directly. More cuts on these same 366-kHz bins cannot isolate the narrow lines. No external message was sent.

## Sources

- Public observation files: https://bldata.berkeley.edu/ATLAS/GB_ATLAS/
- Original thirteen-candidate table and prior physical comparison: inputs/C03-equal-strength-envelope-evidence.zip and inputs/Original13-temporal-profiles.csv, restored with original hashes.
- Lebofsky et al., *The Breakthrough Listen Search for Intelligent Life: Public Data, Formats, Reduction and Archiving*, raw-header definitions: https://seti.berkeley.edu/listen2019/BLdata2019.pdf
