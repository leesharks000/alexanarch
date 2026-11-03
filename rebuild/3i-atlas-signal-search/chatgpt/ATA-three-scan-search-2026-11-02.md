# Three-scan search of excluded ATA spectra

Computational research note prepared for Lee Sharks · 2 November 2026

**Result:** This 1 MHz, three-scan search found no convincing target-specific persistent signal. It did identify a substantive discrepancy between the published positive-only drift filter and the negative received-frequency drift expected for a constant rest-frequency emitter moving with 3I/ATLAS at these times. These are separate findings.

This is an independent exploratory analysis of public spectra, not a rerun of the authors' native pipeline or an independent confirmation by another research group.

## Data and scope

We extracted chunks 150 and 151 of the LoA.C0352 filterbanks in both beams for the first three listed July 3 scans in the public ATA archive [1]. Their frequency range is **1074.750001–1075.749999 MHz**. The portion from 1075 MHz upward falls inside the paper's documented 1075–1116 MHz blanking interval [2].

| Scan | File start, UTC, 3 July 2025 | Samples per beam | Integrated time | Target-favored maxima | Reversed-beam maxima |
|---|---|---:|---:|---:|---:|
| 0 | 06:56:32 | 19 | 318.767 s | 4 | 1 |
| 1 | 07:04:44 | 19 | 318.767 s | 4 | 1 |
| 2 | 07:11:28 | 19 | 318.767 s | 0 | 5 |
| Total | | 57 | 956.301 s | 8 | 7 |

Frequency resolution is 1.9073486328125 Hz; integration time is 16.777216 s. Both-beam time/frequency coordinates and sampling agree. Beam 0's header declination matches the pointing center recorded in the status dump, while beam 1 is displaced by approximately 0.262 degrees in declination, corroborating the target/reference assignment. Every extracted instrument-mask value is zero; that describes the supplied quality mask and does not establish that the spectra are interference-free. These files contain channelized spectral powers, not raw voltages.

The local protocol was frozen before fetching the new slices, with SHA-256 `b22c1e31519974b7eefcf4c3a6dc41ccf0298f126df0d45cb8ca93d011cc0052`. This was not a public preregistration. Scan 0's lower 0.5 MHz had already been inspected in our earlier pass. The remaining 2.5 MHz-scan slices were new to this analysis.

Initial extraction transferred 350,776,488 bytes, avoiding full downloads of the six multi-gigabyte source files. Two local compressed archives failed ZIP integrity checks. They were rebuilt from the saved remote byte ranges; every re-fetched compressed chunk and reconstructed array matched its original hash. The cause of those local truncations was not established. All six final archives passed array-hash verification before the successful search. The repair ledger and failed-attempt log are retained. Extraction now verifies temporary archives before atomic replacement.

## Fixed search and controls

We searched persistent linear tracks from −4 to +4 Hz/s at 1,272 trial drifts. Grid spacing is one channel across the first-to-last sample interval, approximately 0.006316 Hz/s; the grid also includes specified endpoints and calibration drifts. Starting channels are searched wherever the full track fits inside the extracted band. Array-boundary tracks are outside this search's coverage. Separated maxima have a minimum starting-frequency spacing of 250 Hz; they are not a count of independent emitters or of every accepted mathematical trial.

Each beam was normalized by a 2,049-channel local mean, then centered and scaled using its row median and median absolute deviation. The track width increases with the drift-induced smearing within a recorded integration. The simultaneous clipped beam-noise correlations were 0.343, 0.323 and 0.299 in the three scans.

The same trajectory had to satisfy all of:

- Target standardized sum ≥10.
- Reference standardized sum ≤max(5, target/√28).
- Correlation-adjusted differential score ≥8.
- Differential scores ≥3 separately in odd and even time bins.

We applied identical criteria with the beam roles reversed. We did not apply the paper's frequency or drift blanking to discovery. These standardized sums are **neither published bliss SNR values nor calibrated Gaussian significances**. Clipped correlation correction does not account for the full non-Gaussian interference distribution or the number of search trials.

All 15 selected maxima were independently rescored by direct array summation. The largest difference from the search kernel's differential score was 0.00000162.

## What the spectral candidates actually do

All eight target-favored and seven reversed-beam maxima start inside the paper's blanked frequency interval. Most belong to the shared complex near 1075.010 MHz; the others lie near 1075.0608 MHz and 1075.0000 MHz. They do not constitute 15 separate spectral sources.

Paired waterfall inspection shows the selected paths crossing, grazing, or partially following features visible in both beams. Differences in brightness along those shared features can satisfy our same-track spatial screen. A particularly clear example is S0-target-0000: its selected negative-drift path intersects a brighter, positively drifting feature present in both beams rather than tracing a separate persistent line.

For **every selected maximum, the two strongest time bins account for 63.7–91.0% of the positive target-minus-reference contribution** (or the reversed difference for controls). Thus the odd/even split does not establish persistence: two adjacent bright integrations can populate both subsets. This is a demonstrated weakness of our exploratory screen.

We made 40 adjacent-scan comparisons: linear continuation and constant rest-frequency Doppler predictions, for each candidate and each available adjacent scan. **None passed the spatial and differential thresholds at its exact predicted continuation.** Fourteen comparisons found a passing track somewhere within the much looser ±250 Hz, ±0.1 Hz/s window. Those window matches are retained in the table; they are not exact recurrence, and do not override the shared-feature evidence.

Post-inspection diagnostics also show that small frequency displacements in the other beam can substantially change the inferred beam contrast. For example, S0-target-0002's other-beam score rises from 4.78 to 10.49 when shifted by two channels; the resulting selected-to-other score ratio is 1.39. These are descriptive checks, not a newly validated rejection rule. Displaced reference tests at ±1, ±5 and ±10 kHz are also saved; they do not supply a survey-wide false-alarm rate.

The defensible finding is **no convincing target-specific persistent line in this sample**, with visible failure modes preserved. It is not a claim that every feature's transmitter has been identified, or that a weaker signal could not coexist with the shared structure.

## Planted-signal recovery

We ran **81 local tests**, separately injecting into untouched recorded backgrounds: three scans × three fixed frequencies × three nominal strengths × three beam conditions. Frequencies were approximately 1074.820, 1075.140 and 1075.600 MHz, spanning both retained and blanked regions. Drift was +0.15 Hz/s. Equal-beam injections test intended rejection; target-only and 1/8 reference-leakage injections test localization recovery.

| Injection condition | Nominal strength | Matched local recovery | Exact planted trajectory passed |
|---|---:|---:|---:|
| Target only | 15 | 1/9 | 0/9 |
| Target only | 30 | 9/9 | 9/9 |
| Target only | 100 | 9/9 | 9/9 |
| 1/8 reference leakage | 15 | 0/9 | 0/9 |
| 1/8 reference leakage | 30 | 9/9 | 9/9 |
| 1/8 reference leakage | 100 | 9/9 | 9/9 |
| Equal signal in both beams | 15, 30, 100 | 0/27 | 0/27 |

All successful local recoveries also met the tighter four-channel, two-grid-step matching diagnostic. None of the unmodified injection neighborhoods had a pre-existing matched detection. Weak injections were mostly missed; this detector has a real sensitivity floor.

Nominal strength is an input amplitude calibration: total per-time Gaussian-line amplitude in robust background-noise units is strength/√19, integrated over 32 sub-times per sample. It is **not** the recovered score, flux, EIRP, or bliss SNR; it should not be numerically equated with the differently defined strengths in our earlier audit. Recovery searches used 8,192-channel crops and the full drift grid, then matched near the known injection. They were not 81 blind reruns of the complete 1 MHz discovery search. No original-survey completeness estimate follows from these tests.

## The signed Doppler discrepancy

The accepted manuscript states a retained signed interval of **+0.05 to +1.5 Hz/s**. Its Figure 4 (`D3.png`) places the retained histogram only at positive drifts [2]. The manuscript derives its acceleration from the time derivative of Horizons `deldot`.

Horizons defines `deldot` as positive for recession and negative for approach [3]. For constant rest frequency and first-order radial Doppler,

\[
f_{obs}\simeq f_{rest}(1-v_r/c),\qquad
\dot f_{obs}\simeq-\frac{f_{obs}}{c-v_r}\frac{dv_r}{dt}.
\]

We queried Horizons at the ATA geodetic position from the archived telescope metadata. During these scans the object is approaching, but its radial range rate increases: approximately −51.426 to −51.395 km/s at the first sample centers. The corresponding positive radial acceleration is approximately 3.484–3.498 ×10⁻⁵ km/s². Therefore the approach blueshift is decreasing, giving a **negative frequency drift**:

| Scan | Predicted drift at 1075 MHz, first sample center |
|---|---:|
| 0 | −0.124894 Hz/s |
| 1 | −0.125220 Hz/s |
| 2 | −0.125401 Hz/s |

The cited archived bliss source [4] reads the file's frequency spacing without a sign flip. For these positive-spacing files, its CPU, CUDA and array integration paths associate positive reported drift with increasing physical frequency; the DAT writer retains that sign. Thus the inspected code does not supply an explanation in which positive reported drift means decreasing received frequency.

**Assessment:** The manuscript and retained-hit figure appear to describe a wrong-signed filter for the baseline constant-rest-frequency emitter model. The original instruction in our frozen protocol calling the positive interval “original-motion-compatible” was consequently corrected in a separate interpretation note, before new candidate inspection. Numerical discovery thresholds were unchanged.

The exact executed blanking script, run commands and complete before/after hit catalogs have not been obtained. This prevents claiming that we have reproduced the authors' executed filter or proved that a real signal was discarded. The journal website was inaccessible to the retrieval tools; the sign finding is specifically documented against the authors' accepted arXiv v2 manuscript and figure. Intrinsic frequency changes or rotation can alter an emitter's drift; they do not make the positive-only interval encompass the baseline negative prediction.

The saved Horizons response uses JPL solution #55, dated 21 October 2026, described as a temporary nonstandard solution supporting JWST, with a later observational arc. It is a present-day reconstruction, not the ephemeris used by the original analysts. Its acceleration magnitude agrees with the manuscript's stated range. Requests and responses are preserved so another orbit solution can be substituted and the calculation checked.

A secondary, post-inspection search used one physically specified Doppler template per scan to expose weaker fits hidden by a higher-scoring drift winner. The template's maximum departure from the sampled first-order Doppler curve across this band is below 0.020 Hz, versus 1.907 Hz channels. It finds two target-favored maxima and one reversed-beam maximum, all in the same 1075.010 MHz complex. Waterfalls again show intersection with the shared curved feature, not a separate persistent negative-drift line. This check does not produce a convincing candidate.

The concrete unresolved question is: **why does the documented positive-only filter exclude the negative drift predicted by the same range-rate convention?** The decisive materials would be the executed blanking code, signed pre/post-filter hit tables, and recovery tests at the predicted negative rates in frequency intervals that were otherwise retained.

## Reproduction and contents

The accompanying bundle contains the six extracted power/mask arrays, all source manifests and chunk hashes, protocol and interpretation note, analysis scripts, numerical tables, full winning-score profiles, paired waterfalls, injection examples, Horizons request/response, and selected licensed bliss source files. Scientific conclusions above concern only these spectra and this search.

To reproduce from the bundled arrays, install `requirements.txt`, then run, in order:

```bash
python search_tracks.py
python recovery_tests.py
python context_checks.py
python additional_diagnostics.py
python plot_results.py
```

`extract_three_scans.py` can re-fetch the fixed public source selection. `repair_extracted_archives.py` verifies arrays and rebuilds only failing archives. `SHA256SUMS.txt` covers the bundle contents other than itself. `results/all_candidates.csv`, `results/adjacent_scan_checks.csv`, `results/injection_recovery.csv`, and `results/ephemeris_by_scan.csv` contain the main inspectable results.

## Primary references

1. Berkeley public ATA archive: https://bldata.berkeley.edu/ATLAS/ATA_ATLAS/ . Exact six file URLs and byte-range hashes are in `data/*_manifest.json`.
2. Sheikh et al., *A Search for Radio Technosignatures from Interstellar Object 3I/ATLAS with the Allen Telescope Array*, accepted manuscript, arXiv:2512.18142v2, 20 May 2026, https://arxiv.org/html/2512.18142v2 . Journal DOI: https://doi.org/10.3847/1538-3881/ae6651 . Saved manuscript source and figures are from https://arxiv.org/src/2512.18142v2 , CC BY 4.0; attribution remains with the paper's authors.
3. NASA/JPL Horizons manual, observer quantity 20: https://ssd.jpl.nasa.gov/horizons/manual.html ; API documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html . The exact query, site coordinates, solution and response are in `aux/`.
4. Cited bliss archive, version 2025-05-22: https://doi.org/10.5281/zenodo.19131179 . Selected source files, hashes, archive hash and BSD license are in `aux/bliss-sign-evidence/`.
