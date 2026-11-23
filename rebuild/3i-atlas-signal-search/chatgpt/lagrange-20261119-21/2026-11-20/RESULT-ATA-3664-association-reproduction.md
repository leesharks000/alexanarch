# ATA 3664 MHz comet-association reproduction — 2026-11-20

**Outcome: fixed recorded-frequency model strongly favored over the comet-Doppler model in the recovered data.** This is a rerun of already exposed scans 0–5, NOT a fresh held-out observation or a finding about the separate 1631.75–1632.08 MHz feature family.

## Input
User Library archive `ATA-3664-association-progress-2026-11-17.zip`, 8,374,141 bytes, SHA-256 `5ff10be4daf0b88138c10a4abb6a451e0698ab7897af2ec9c87d0cbe3047529e` (ZIP CRC verified). It contains 6 scan pairs, source code `association.py`, spectral windows `windows/scan-{0..5}.npz`, Horizons ephemerides and original frozen plan. Five observed frequency teeth near 3664 MHz and one exploratory extrapolated tooth are included; **only the five measured teeth** are included in the 60-comparison statistics below.

## Executed code
```sh
unzip ATA-3664-association-progress-2026-11-17.zip -d working
cd working
OPENBLAS_NUM_THREADS=1 python association.py 0 1 2 3 4 5
python - <<'PY'
import association
association.injections()
PY
```
Reproduction generated `results/association.json` and `results/injections.json`. No primary tests were retuned. A separate NumPy-only readback of the raw NPZ row-wise integer-bin maxima and quality gates compared results against the stored fit summaries.

## Numerical result
- Six scans × two beams × five measured teeth = **60 valid fits**, all with recorded-frequency RMS **less** than comet-model RMS.
- Median fixed-recorded-frequency residual RMS: **1.4004615995 Hz** (range 0.0000362–5.370237 Hz).
- Median predicted-comet residual RMS: **39.2472053635 Hz** (range 35.87696–40.84954 Hz).
- Median observed slope: **7.1777e−8 Hz/s**; median comet-model slope: **−0.4271123856 Hz/s**.
- The five measured teeth occupy approximately 3663.99947, 3663.99974, 3664.00000, 3664.00027, and 3664.00053 MHz.
- Beam headers place beam 0 within ~0.17–0.87 arcsec of the saved comet ephemeris and beam 1 approximately 375.7–375.8 arcsec away; this is intended pointing metadata, not independent beam calibration. The raw line-area target/reference ratios for the five teeth are generally near 1 across pairs (some deviations), consistent with a shared-beam pattern.
- Independent re-selection of row-wise strongest native bin in ±100 Hz windows and quality q≥6 reproduced the original integer-frequency spans in all **60/60** beam–scan–tooth cases.
- The original archived injection function re-executed **96 cases**: 32/32 at strength 128 local MAD passed, 32/32 at strength 32 passed, and 0/32 zero-amplitude cases passed. Controls are synthetic examples from this chosen family, not a survey-wide sensitivity guarantee.

## Interpretation
The approximately fixed telescope-recorded RF frequencies, failure to follow the expected comet Doppler curve, and appearance in both beams strongly favor local/terrestrial/instrumental interference for these 3664 MHz features. They do not identify an individual transmitter. Because the sample is from the previously examined six scans, the result is **reproduction of an archival negative**. The original plan reserved scans 6–8 for future prospective testing; those remain unexamined here and must not be described as tested.

**Separate investigation not yet executed:** six recurring features reported in 1631.75–1632.08 MHz, which require their own candidate timestamps, powers, beam and drift ledgers. Nothing in this 3664 MHz analysis settles them.

## Limitations
The recomputation depends on code and data preserved in the prior archive; this is not an independent acquisition from the Breakthrough Listen server. No raw receiver voltage or calibration of antenna gain for these ATA Stokes-I windows is claimed. Repeated exposure, exploratory selection and model-family restriction prevent a global p-value or a claim that all conceivable comet-origin emissions are excluded.
