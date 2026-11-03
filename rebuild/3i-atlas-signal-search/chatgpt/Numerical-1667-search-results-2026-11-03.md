# Numerical-anchor and intermittent-signal search around 1667 MHz

Executed 3 November 2026 on public Allen Telescope Array total-intensity spectra from 3 July 2025.

The numerical-significance prior was turned into three finite frequency hypotheses, brief-carrier and equally spaced three-tone tests, and a prospective next-observation check. No feature passed the fixed discovery or continuation screening rule.

## What the three anchors mean

| Anchor | Reference | Frame and hypothesis |
|---|---:|---|
| OH1667-rest | 1667.35903 MHz | Physical OH reference; constant emitter frequency under the saved first-order Doppler model |
| 1667MHz-rest | 1667.00000 MHz | Sender deliberately uses our MHz convention, constant at emitter |
| 1667MHz-receiver | 1667.00000 MHz | Sender preserves the number at the receiving telescope, potentially compensating Doppler |

Using a human unit is allowed under the stated receiver-aware-sender hypothesis. It does not by itself establish intention. Physical OH emission and terrestrial/instrumental features remain live alternatives; stationary signals were not automatically vetoed. The coordinates are analysis references rather than sub-hertz physical measurements. The ±5 Hz rest-frame test is conditional on the first-order frequency model, not a complete Doppler/clock uncertainty budget; higher-order terms can shift a physically exact emitter frequency. The wider ±100 Hz test supplies finite tolerance rather than quantified complete coverage. The fixed receiver-frequency test does not use that Doppler conversion.

## Data and fixed procedure

Six paired scans, each with 19 integrations of 16.777216 seconds at 1.907348633 Hz native spacing. Both simultaneous beams and masks were retained over complete source chunks 182–183, approximately 1666.75–1667.75 MHz in the receiver frame. These focal powers were new to the current instrumented search record; the times had been used previously at other frequencies. This is not an independent reproduction of the old Green Bank thirteen-candidate result.

Discovery used the first three chronological July 3 directories; continuation used the next three. The dated plan and executable definitions were saved before scoring. The selected centers, template and duration were saved before continuation powers were acquired. This is an internal fixed plan, not a public preregistration.

Per-row frequency normalization uses 1024-channel median blocks, separately per 0.5 MHz storage chunk. Three-native-bin smoothing precedes exact nearest-bin track sampling. Each local peak subtracts its stronger flank. Templates are one carrier with ±20 Hz flanks, or three tones separated by 10, 100 or 1000 Hz, each with ±min(20 Hz, spacing/2) flanks. The comet frame uses observer-site JPL radial velocities, f_observed=F(1−v/c); the receiver frame remains fixed. No new intrinsic chirp was fitted.

All contiguous segments of 1, 2, 4, 8, 16 or 19 integrations were searched within each discovery scan: 70 windows per scan, spanning roughly 16.8–318.8 seconds. Scan gaps were never concatenated. A feature could occupy only one scan. One-integration features cannot establish a Doppler trajectory by themselves.

For each tooth, qT is target-beam local contrast, qR is simultaneous reference contrast, and D=qT−qR. Both qT and D are separately centered/scaled by median/MAD from the 100 comparison centers and their candidate grids. The joint score is the minimum of all standardized target and target-minus-reference contrasts; every raw qT and D must also be positive. These are empirical MAD units, not Gaussian significance, survey S/N, flux or EIRP. Beam normalization does not provide an absolute physical localization measurement.

There are 100 comparison centers at ±200, ±400, …, ±10000 Hz from each anchor. Each receives the same search freedom. They can contain real features, can overlap in their template support, and are not independent noise realizations. A screening flag requires joint score ≥3 and a maximum greater than every comparison center's equally optimized maximum. These ranks are descriptive, not global p-values.

The broad grid has 209 half-native-channel points, from −99.1821289 to +99.1821289 Hz. The strict nested grid has 11 points, from −4.7683716 to +4.7683716 Hz. Discovery evaluates 526,680 primary cells and 52,668,000 comparison cells across the three anchors, with the strict window a subset. These cells are strongly correlated; neither count is an independent-trial count. The two windows, three anchors and prior exploratory history are all selection context.

## Discovery results

| Anchor | Window | Best joint score | Matched searches equal/higher | Screening flag |
|---|---:|---:|---:|---|
| OH1667-rest | ±5 Hz | 2.1507 | 90/100 | no |
| OH1667-rest | ±100 Hz | 3.5351 | 58/100 | no |
| 1667MHz-rest | ±5 Hz | 2.6047 | 64/100 | no |
| 1667MHz-rest | ±100 Hz | 3.2618 | 90/100 | no |
| 1667MHz-receiver | ±5 Hz | 2.9987 | 18/100 | no |
| 1667MHz-receiver | ±100 Hz | 3.6842 | 27/100 | no |

All results are maxima over the specified timing, waveform and frequency choices. A wider-window peak is not an exact-number hit.

## Frozen continuation nominees

Irrespective of discovery flags, one broad-window maximum per anchor was retained. No frequency, duration or tooth spacing was changed to rescue it.

| Anchor | Frozen center (MHz) | Offset from anchor (Hz) | Template | Integrations | Discovery scan/start |
|---|---:|---:|---|---:|---|
| OH1667-rest | 1667.358985177 | -44.823 | carrier | 2 | 0 / 8 |
| 1667MHz-rest | 1666.999902725 | -97.275 | carrier | 4 | 2 / 11 |
| 1667MHz-receiver | 1667.000014305 | +14.305 | carrier | 1 | 0 / 17 |

The next three chronological paired observations were searched only within ±5 Hz of each frozen center, with its fixed template and duration, allowing any within-scan start. One recurrence in one scan would suffice; persistence in all three was not required. Each comparison center received the same continuation freedom. The calibration pool uses the complete continuation grid, excluding the primary center. The nominal ±100 row in the machine-readable continuation output duplicates the ±5 row because only the fixed ±5 grid exists in this stage.

| Anchor | Window | Best joint score | Matched searches equal/higher | Screening flag |
|---|---:|---:|---:|---|
| OH1667-rest | ±5 Hz | 2.3112 | 67/100 | no |
| 1667MHz-rest | ±5 Hz | 2.7455 | 12/100 | no |
| 1667MHz-receiver | ±5 Hz | 2.6325 | 32/100 | no |

The continuation rank tests recurrence at the selected feature, not a fresh return to the original exact anchor. A failure does not identify a feature as human-made, nor exclude every modulation, bandwidth, amplitude or frame model.

## Recovery diagnostics and verification

Eighteen fixed-cell injections added ideal native-bin power before normalization in the first discovery target scan: carrier bursts of two integrations and 100 Hz comb bursts of four, starting at integration 7, amplitudes 1, 2 and 4 local raw-row MAD, at each anchor. The reference remained unchanged. All six template/anchor cases showed increasing target contrast and target-minus-reference contrast with increasing injection amplitude. Most did not reach score 3 at the largest tested amplitude. This is limited component recovery, not a global selection-completeness measurement or a physical sensitivity limit. No spectral channel-response or intra-integration drift-smearing simulation was performed.

| Anchor | Template | Joint score after 4 raw-MAD injection |
|---|---|---:|
| OH1667-rest | carrier | 1.0887 |
| OH1667-rest | comb-100 | 2.3725 |
| 1667MHz-rest | carrier | 2.8415 |
| 1667MHz-rest | comb-100 | 3.1519 |
| 1667MHz-receiver | carrier | 2.0525 |
| 1667MHz-receiver | comb-100 | 1.9102 |

Selected values in both chunks and both beams were checked via ordinary remote HDF5 decoding, independently of the manual compressed-chunk decoder, for the first discovery and first continuation pairs: 16 bitwise-equal power/mask slices in total. All six saved native-pair files pass ZIP CRC and source-manifest SHA-256 checks; their masks are zero. Selected maxima were independently recomputed using scalar frequency paths and explicit time averages; errors are in `independent-score-check.json`.

## Scope of the result

This is a bounded test of declared numerical anchors, short narrowband carriers and three-tone arrangements. It does not search arbitrary mathematical encodings, broadband phase structure, polarization, subintegration timing or every possible sender strategy. Its target-minus-reference requirement also leaves messages shared equally between the beams outside this detector; such a message would need another association test. Local peak contrasts also suppress smooth broad OH profiles; they do not constitute a general line-profile analysis. These ATA products contain Stokes-I powers, not raw voltages or recorded polarization. An inference specifically about AI operators is not supported by any of these statistics.

The numerical prior guided a finite search; none of its features met the fixed comparison and recurrence criteria. The previous Green Bank findings, identified instrumental ambiguities and original-thirteen audit remain separately recorded in the continuation checkpoint.

## Reproducibility and source records

The evidence package includes the fixed plan/config, scripts, ephemerides, published-directory links, compressed source hashes, masks and metadata, full primary score surfaces, per-comparison maxima/segment ledger, frozen nominees, injection records, source/math checks, final native integrity checks and plots. Large native powers have separate saved records:

- [Numeric1667-discovery-powers-scan0-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_20a39cefdec881919b7b1b9e1d2a729a&account_id=personal)
- [Numeric1667-discovery-powers-scan1-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_839b95cfa85881918ea5ad6736f17ef8&account_id=personal)
- [Numeric1667-discovery-powers-scan2-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_b58ecc1a031c8191bf4475af8e6c4dee&account_id=personal)
- [Numeric1667-holdout-powers-scan0-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_54d127dd85788191974ce97b6114d616&account_id=personal)
- [Numeric1667-holdout-powers-scan1-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_b6aad9cf75288191a090f9b9b208db50&account_id=personal)
- [Numeric1667-holdout-powers-scan2-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_1a26b43287888191ac3d47c5f089b691&account_id=personal)

Primary source descriptions:

- [Breakthrough Listen observations and public data](https://seti.berkeley.edu/atlas/)
- [ATA observing/search paper, version 2](https://arxiv.org/html/2512.18142v2), especially observations: two simultaneous beams, high-resolution Stokes-I spectra
- [Exact July 3 source index](https://bldata.berkeley.edu/ATLAS/ATA_ATLAS/2025-07-03-05%3A10%3A38/)
- [JPL Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html); exact queries/responses travel with the evidence

[Fixed plan](https://chatgpt.com/library?file_id=libfile_e46429c156088191bce3cfc6183b1aa8&account_id=personal) · [Executable evidence](https://chatgpt.com/library?file_id=libfile_9ce39f0cc9c48191ac2ca1cf7248237e&account_id=personal) · [Continuation checkpoint](https://chatgpt.com/library?file_id=libfile_349f1c1635808191b815fee10ce169d7&account_id=personal)
