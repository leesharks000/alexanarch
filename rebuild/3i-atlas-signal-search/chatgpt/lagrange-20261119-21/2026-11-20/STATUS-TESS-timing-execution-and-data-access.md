# TESS 3I/ATLAS 20-second photometry — execution checkpoint, 2026-11-20

**The telescope light curve has NOT been analyzed.** Verified source: [Zenodo v2.2 record](https://zenodo.org/records/19697668), [NASA/TSSC project](https://github.com/tessgi/tess-3i). The 1.2 MB fast-cadence product is `hlsp_tess-3i_tess_tpf_3iatlas-s1751-cam2-ccd3_tess_v2.0_fast-lc.fits`. Attempts to download from Zenodo in this execution environment failed with DNS error; no local photometry bytes exist. Do not imply a negative TESS observation or an astronomical period.

## Implemented and actually run
A full executable Python screening script `tess_scan.py`, source included in the conversation ZIP [TESS-3I-timing-pilot.zip], uses the actual FITS table schema, quality=0 where supplied, segments at time gaps, median detrends within contiguous sequences, and runs normalized Lomb–Scargle power at 240 periods from 120 to 18,000 seconds. It compares a maximum over all periods against a 12-cadence-block-reordering null with 199 surrogates, and reports early/late evidence at the *frozen winner*, without refit. It is a pilot; comparison to jitter/background-star controls and alternate apertures remains necessary before any astrophysical claim.

Synthetic injection self-test executed on three independent 900-sample simulated light-curve sequences with 20-second cadence. Planted 600 s modulation recovered at **602.927 s**; p=**0.025** against 39 surrogate controls; scores in frozen-period halves 0.646/0.645. Noise-only simulation strongest fluctuation p=**0.05** with 39 surrogates—one borderline noise example emphasizes why independent replication matters. These are *synthetic*, not observations.

## To run with actual NASA data
```bash
pip install numpy scipy astropy
curl -fL 'https://zenodo.org/records/19697668/files/hlsp_tess-3i_tess_tpf_3iatlas-s1751-cam2-ccd3_tess_v2.0_fast-lc.fits?download=1' -o tess_fast_lc.fits
OPENBLAS_NUM_THREADS=1 python tess_scan.py --fits tess_fast_lc.fits --nsurr 199 --output tess_real_result.json
```

The script first prints available FITS columns and auto-selects a flux series; **verify the chosen flux type** and contamination flags. The TSSC authors explicitly warn of bright saturated-star contamination near BTJD 4056.4 and stellar-background-model edge effects, so an apparent modulation must be checked against instrument and stellar controls. The output of this run is solely an executable validation and a documented network-access block.
