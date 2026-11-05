# ATA upper-strip feasibility pilot

Completed 2026-11-05T15:16:59.874611+00:00. **The fixed strong-tone recovery requirement passed in all four ATA regions.** This was a software/data-quality pilot, not a new astronomical signal search.

The data header fixes ATA’s actual upper channel-cell edge at **3687.750000 MHz**. The originally proposed 3687.750–3688 MHz portion is absent from this tuning. The separate Parkes header audit shows that the recorded ATA strip also lies within Parkes blc27 coverage; it is not an otherwise unobserved frequency gap. Parkes’s July 31 reference observation was used only for quality checks here.

| ATA sample (MHz) | Target-only recoveries | Shared-equal-raw passes | Required strong recoveries |
|---|---:|---:|---:|
| low: 3648.010000–3649.010000 | 6/12 | 0/12 | 2/2 |
| middle: 3667.500000–3668.500000 | 7/12 | 0/12 | 2/2 |
| edge: 3686.740000–3687.740000 | 6/12 | 0/12 | 2/2 |
| centre: 3351.500000–3352.500000 | 6/12 | 0/12 | 2/2 |

The 96 fixed cases comprise four regions, amplitudes 2/4/8/16 measured local raw-row MAD, durations 1/4/19 integrations, and target-only versus the same absolute raw increment before float32 rounding in both simultaneous beams. The known location was fixed before power decoding; only its ±1-native-bin neighbourhood was eligible. Start was fixed at zero. These are sparse feasibility benchmarks, not estimated detection probabilities. ON and J are robust standardized detector scores, not calibrated Gaussian significance. Shared equal-raw increments can produce unequal standardized beam scores; any shared passes are documented rather than tuned away.

| Sample | Beam 0 median raw power | Beam 1 median raw power | Beam 0 fractional raw MAD | Beam 1 fractional raw MAD |
|---|---:|---:|---:|---:|
| low | 6.59533e+10 | 6.59346e+10 | 0.30163 | 0.30142 |
| middle | 5.90408e+10 | 5.9048e+10 | 0.30138 | 0.30139 |
| edge | 5.386e+10 | 5.38746e+10 | 0.30137 | 0.30140 |
| centre | 5.92578e+10 | 5.92365e+10 | 0.35552 | 0.35553 |

All ATA native powers are finite and positive; all acquired masks are zero. Raw power levels across tunings depend on receiver gain and band response as well as sky/system power. Similar fractional noise and passing raw-power injections do not establish equal astronomical sensitivity, especially near a passband edge. No flux-calibrated threshold can be stated from this pilot.

The zero-injection background passed the same known-location screen in **0/12** fixed region/duration checks. A background pass would make recovery at that coordinate ambiguous. The two beam arrays have different power hashes; their sampled backgrounds are correlated (median within-row, central-three-MAD correlations: low 0.757, middle 0.759, edge 0.762, centre 0.820). These are not independent noise streams. No measured celestial beam-leakage calibration was obtained: a real sky tone entering the reference beam could be penalized by J. The synthetic target-only recovery result is conditional on the injected occupancy.

The centre comparison is not a clean, featureless band. Fractions above each raw row’s median + 8 MAD are:

| Region | Beam 0 | Beam 1 |
|---|---:|---:|
| low | 0.000000% | 0.000000% |
| middle | 0.000000% | 0.000000% |
| edge | 0.000321% | 0.000311% |
| centre | 0.665946% | 0.665153% |

The strongest raw outliers are in the comparison extract; their origin was not established here. The fixed injection recovery and robust baseline checks passed despite these features. No such feature was nominated as an astronomical candidate.

Parkes reference checks:

| Region | Integrations | Frequency step (Hz) | Finite / positive fraction | Fractional raw MAD |
|---|---:|---:|---:|---:|
| low | 20 | -2.000000 | 1.000000 / 1.000000 | 0.13175 |
| middle | 20 | -2.000000 | 1.000000 / 1.000000 | 0.12985 |
| edge | 20 | -2.000000 | 1.000000 / 1.000000 | 0.13026 |

Parkes’s negative frequency increment was retained. Its reference slices are not a test of comet emission, and ATA ephemerides were not applied to Parkes. Parkes source powers remain uninspected.

Validation: **32** independent native-source HDF5 comparisons were bitwise equal, spanning data and masks in every ATA region and beam. All four zero-amplitude injections were bitwise unchanged. Gaussian bin-integral quadrature maximum error: **4.09e-10**. Ascending/descending-axis numerical agreement: **9.32e-13**. Independent direct-native-bin versus prefix score maximum error across all recovery cases: **0**. Every archive was CRC-checked; source ranges, chunks and arrays carry SHA-256 records.

Completed ATA payload-range transfers: 1189.290 MB; Parkes reference payload ranges: 120.000 MB, plus 22.938 MB of unique source metadata blocks and 0.266 MB of preview headers. Coalesced ATA ranges include gap bytes that were not decoded as target powers. The 1.6 GB ceiling and two-request cap were respected. No full 40 MHz acquisition was started.

What remains: document or model celestial leakage into the reference beam before using it as a hard veto (or retain a separately controlled shared-beam branch); identify any prior exposure and actual status of the separate survey; freeze the ATA discovery/reserve split, controls, multiplicity accounting, sensitivity/quality exclusions and candidate limits before additional source powers; run that defined search; freeze ATA nominees before checking Parkes comet observations with its own observer geometry. A later-epoch Parkes non-recurrence would constrain persistent signals, not automatically exclude a July 3 transient.

Saved evidence (each includes source chunks/ranges, native extracts, relevant code and checks):

- [ATA-upper-pilot-C0928-0-evidence.zip](https://chatgpt.com/library?file_id=libfile_b62539c73020819193d3f311ac9ce03c&account_id=personal)
- [ATA-upper-pilot-C0928-1-evidence.zip](https://chatgpt.com/library?file_id=libfile_ece347eb78308191b2a1920131dee4f2&account_id=personal)
- [ATA-upper-pilot-C1504-0-evidence.zip](https://chatgpt.com/library?file_id=libfile_0036c118abfc8191a40ac5ddeb7be3eb&account_id=personal)
- [ATA-upper-pilot-C1504-1-evidence.zip](https://chatgpt.com/library?file_id=libfile_875c2b272de481918521405b499c5e6b&account_id=personal)
- [ATA-upper-pilot-parkes-evidence.zip](https://chatgpt.com/library?file_id=libfile_8565f28d3fa0819194c340f1b3f99a7b&account_id=personal)

The final compact evidence packet contains all code, metadata, fixed plan, per-case results and summary needed alongside those native evidence parts. Prior 3332–3339 MHz and older branches remain separate; this pilot does not revise their outcomes.
