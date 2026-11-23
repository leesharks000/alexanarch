# Search elsewhere: independent 3I/ATLAS signal opportunities outside the GBT voltage run
Date: 2026-11-20. Status: external-source audit plus numerical re-evaluation of published FAST event rates, not new telescope-data reduction.

## 1. FAST seven January 5 chirps: actual reported records and numerical test
Primary source (full text): https://arxiv.org/abs/2603.19023 , Table 5, IV Results, III Table 2.

FAST observed on 2025-10-03, 2025-10-29, 2025-12-19 and 2026-01-05 in its L-band 19-beam configuration. Seven visually retained chirp-up event records from 2026-01-05 occur at **four unique frequencies**:
| event ID | MHz | drift Hz/s | polarization | expected comet drift magnitude at MHz, Hz/s | measured / expected |
|---|---:|---:|---|---:|---:|
|244|1431.9978|0.045|I|0.2371|0.190|
|250|1431.9978|0.045|XX|0.2371|0.190|
|3703|1250.0126|0.055|YX|0.2070|0.266|
|5965|1333.3168|0.135|YY|0.2208|0.611|
|47992|1250.0126|0.047|YY|0.2070|0.227|
|225671|1066.6534|0.115|YY|0.1766|0.651|
|250224|1066.6534|0.107|I|0.1766|0.606|

Recalculation explicitly uses the paper's Table 2 comet expected drift **0.207 Hz/s at 1250 MHz on 2026-01-05**, scaled by frequency: `expected(f)=0.207*(f_MHz/1250)`. This is a magnitude comparison, not a reconstruction of the exact signed ephemeris over the observation. Every measured rate is below the expected rate by 0.062–0.192 Hz/s. Rates are fitted linear values while the observed features chirp-up (curved), so these numbers cannot fully reject alternative non-linear trajectory models; they validate the paper's statement that the reported fitted rates are not the comet-predicted rates.

The paper additionally detects a similar chirp-up in a reference beam at 1312.5502 MHz, and finds combinations of hardware ROACH2 oscillator frequencies reproduce frequencies to <=0.03 MHz, an exploratory instrumental-intermodulation explanation. This is a serious mundane alternative, not positive ET evidence. **Seven records do not mean seven independent signals.**

## 2. MeerKAT public catalogue — available, but archive already analyzed most of it
Breakthrough Listen official: https://seti.berkeley.edu/atlas/
Directory verified: https://bldata.berkeley.edu/ATLAS/MeerKAT/
Files currently listed:
- `atlas_hits.json.gz` 70M
- `atlas_hits_2025_11.json.gz` 75M
- `atlas_hits_2025_11_dups.json.gz` 90M
- `atlas_hits_2025_12.json.gz` 197M
These are *compressed size labels* in Apache directory listing, not row counts.

Earlier archive research #1742 already examined ~6 million MeerKAT hits on six dates in Nov/Dec 2025, and established essentially no hit occupancy in the C03 1663–1667 MHz region; do **not** repeat the same thresholded hit census or present it as new.

A useful *different* test, if unthresholded multibeam dynamic spectra are separately retrievable: compare continuous simultaneous central-beam versus side-beam power **below** the seticore threshold, and use beam sensitivity calibration. A hit catalogue alone cannot reconstruct subthreshold powers or modulation phase.

Direct data download in this environment was attempted and failed with temporary DNS resolution, so no new MeerKAT census is claimed here.

## 3. TESS optical transient/periodicity experiment (new signal modality)
Official MAST: https://archive.stsci.edu/hlsp/tess-3i
Public v2.0 Zenodo dataset: https://zenodo.org/records/19697668
Observing span: 2026-01-15 to 2026-01-22. Products specifically:
- `hlsp_tess-3i_tess_tpf_3iatlas-s1751-cam2-ccd3_tess_v2.0_fast-lc.fits` **1.2 MB**, 20-s cadence TESS lightcurve.
- `hlsp_tess-3i_tess_ffi_3iatlas-s1751-cam2-ccd3_tess_v2.0_lc.fits` **648 kB**, lower cadence.
- `...fast-tp.fits` 218.2 MB, image stamps with background correction.

The 1.2 MB time series is the best *low-compute* genuinely new search substrate: test residuals against smooth comet brightening, TESS instrumental cycles, aperture/background artifacts, and known rotational variability; apply a prespecified robust periodicity + pulse search with comparison stars and correct multiple trials. Such anomalies would not be radio technosignatures and are not evidence of artificial origin without further specificity.

## 4. ALMA/ACA December 22 2025 millimeter-wave spectra
Public source: https://pmc.ncbi.nlm.nih.gov/articles/PMC13391348/
The study reports ALMA ACA CO and HCN emission observed on 2025-12-22, and locates the underlying ALMA dataset in the observatory's archive. These observations offer high-resolution comet-rest-frame *natural line controls*, and potentially permit inspection for unexplained spectral emission/temporal variation, but they are targeted spectral windows (not an unconstrained broad-spectrum communications search). Need dataset/project identifiers and public status validated before pipeline work.

## 5. Accessible alternative: TESS route vs raw large radio files
The GBT raw-voltage work is already delegated to Claude. No point duplicating its acquisition. TESS fast light curve is ~1.2 MB compared with MeerKAT catalogue >75 MB and GBT voltages 1.35 TB. The TESS route gives an independently designed experiment against *optical* nonstandard activity, while FAST already provides a published control for misleading curved chirps.
No new extraterrestrial signal or artificial optical event was identified in this audit.

## Data access
Verified online primary source pages and file lists. Container DNS lookup for bldata.berkeley.edu failed; no actual MeerKAT, FAST raw, TESS FITS or ALMA measurement-set bytes were transferred or analyzed in this checkpoint.
