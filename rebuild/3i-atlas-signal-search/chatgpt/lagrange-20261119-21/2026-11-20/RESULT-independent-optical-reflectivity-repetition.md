# Independent optical 3I/ATLAS anomaly sweep — executed 2026-11-20

## Data provenance
Public measured reflectivity data: [3I-ATLAS/discovery-paper, 3I-Reflectivity_JN_edit.csv](https://github.com/3I-ATLAS/discovery-paper/blob/main/src/data/3I-Reflectivity_JN_edit.csv), read directly via connected GitHub API (no instrument sample reconstruction). **1603 wavelength/reflectivity pairs**, 340.048–856.648 nm, nominal sampling **0.300 nm**. A **36.3 nm gap** lies between 491.848 nm and 528.148 nm; analyze separate segments (507 and 1096 samples). The CSV header labels wavelength merely `wave`; wavelength unit nm follows interpretation of values as micrometers, and should be checked against the originating paper.

## Hypothesis/filter
Do not assume temporal radio modulation or Doppler. Search for an *unanticipated spectral repetition* after robust local-median detrending, separately in both arms: clip residuals to ±4 local MAD-normalized units; scan positive Pearson autocorrelation over lags 8–120 bins (2.4–36.0 nm). Three half-window sizes: 15,30,60 bins (4.5,9,18 nm). Primary within-scale statistic is **the maximum across both arms and all lags**. Generate 249 seeded nulls permuting 16-bin contiguous blocks within each arm separately; each surrogate rescans all lags and both arms. Pseudorandom seed 20261120, 32-bit linear congruential generator. The null preserves short-range block structure but not broad wavelength-dependent response. This is a *structural null*, not a quantitative instrument model.

## Executed scores
| Smoothing half-width | blue-arm best | red-arm best | max-over-arms p |
|---|---|---|---|
| 4.5 nm | lag 24.3 nm, r=0.17293 | lag 28.2 nm, r=0.10493 | **0.172** |
| 9.0 nm | lag 24.3 nm, r=0.19806 | lag 17.1 nm, r=0.10709 | **0.124** |
| 18 nm | lag 30.9 nm, r=0.17118 | lag 4.5 nm, r=0.12366 | **0.528** |

No within-smoothing-family maximum survives block-order controls, **even before** considering the three post hoc scales as additional multiplicity. No evidence of repeated anomalous spectral fine structure was established. No claim regarding extraterrestrial technology can be inferred from this single spectrum. The test cannot detect a complex broadband signal with no repeated spectral envelope, nor any *time-domain* structure.

## Reproducibility
`scan_3i_optical_repetition.mjs` is a self-contained Node.js script that fetches the source CSV, asserts source shape, executes exactly the original tests and prints JSON. No data were modified or rehosted. Recorded tool calculation used the same formulas on the retrieved GitHub CSV.

## Next independent modality
NASA/TSSC dedicated 3I/ATLAS TESS fast 20-second photometry, 2026-01-15–22, is published as a **1.2 MB FITS light-curve product** at [Zenodo 19697668](https://zenodo.org/records/19697668), with official [MAST documentation](https://stdatu.stsci.edu/hlsp/tess-3i). Raw TESS bytes are not currently in ChatGPT's runtime; attempted Zenodo/Raw-GitHub direct downloads failed DNS. Do not claim a TESS light-curve test has run. Analyze comet-light curve with background and image-systematic control series and a held-out time interval once bytes are available.