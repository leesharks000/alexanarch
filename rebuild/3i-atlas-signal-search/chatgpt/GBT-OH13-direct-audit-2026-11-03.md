# The original thirteen: exact reproduction and candidate audit

Research note for Lee Sharks · 3 November 2026 · working analysis, not deposited

**The original result reproduces: 13 clusters, compared with 3.75 ± 2.046 clusters in the packet's 40 false-acceleration controls; the largest control has 8. All 78 rounded per-scan scores match.** The effect survives some reasonable method corrections and a veto around the known contaminant. It is an exploratory count excess under a specified detector, not yet an identified astronomical transmission.

**Scope correction:** these thirteen were selected across an entire 2.93 MHz instrument channel. None is inside the ±5 kHz OH-centered region of our earlier report. That earlier negative result does not adjudicate these thirteen. The earlier report now carries a dated correction.

## 1. Inputs and exact replication

The supplied ZIP contains the original selection code, candidate coordinates, metadata and a README. Its CSV is identical to the separately attached CSV: 78 rows, thirteen IDs and six scans.

- oh13.zip SHA256:2034f51db60240330fb35c618900be6ace1af5e49b3609a29abb0f1202dfdff5
- oh13_candidates.csv SHA256:d3d15492915a18b09787534bc2e8df70f54a4d9934658ad631e0a9a7fb7f42df

We fetched all of coarse channel7 from the exact six public blc23 files, retaining 49 integrations ×1,048,576 native channels per scan. The band covers approximately1665.527–1668.457 MHz at 2.794 Hz resolution and6.085-second sampling. All 294 downloaded chunk hashes match the same chunks in our previous acquisition. All 112,871,892 overlapping saved power values match bit-for-bit. Each full-channel output passed CRC and hash checks. The six compressed outputs total1,050,141,263 bytes.

The original Horizons query was repeated with its exact site coordinates, start/stop rounding, minute grid and parameters; the full response was saved. The resulting original-code score vectors match our optimized implementation bit-for-bit for all six true-frame scans.

The thirteen reproduced cluster means match the exported coordinates within0.0005 Hz, reflecting export rounding rather than physical measurement precision. All 78 scores agree within their supplied0.01 rounding. No candidate was reconstructed by guessing its identity.

Original rules:
1. Divide each native frequency channel by its own median over time, then subtract one.
2. Apply a three-channel boxcar.
3. Roll rows by the predicted comet drift and sum them.
4. Standardize each scan using the full channel's median and MAD; zero nine DC bins.
5. Align scans by comet rest frequency and maximize within±1 channel.
6. Require every ON scan to score≥2.5 and every OFF scan<2.
7. Merge adjacent accepted frequencies within10 Hz.

Those z values are empirical detector units. They are not automatically Gaussian significance or calibrated physical flux.

## 2. What the controls establish

| Procedure | True-frame clusters | Control mean | Control maximum | Controls reaching true count |
|---|---:|---:|---:|---:|
| Original packet method |13|3.750|8|0/40|
| Exact reference-rest-grid spacing |12|3.625|9|0/40|
| Fixed-tone trajectory veto,±10 Hz |12|3.725|8|0/40|
| Broader fixed-tone veto,±60 Hz |11|3.725|8|0/40|

Every variant was applied to the true frame and the same forty controls. The veto excludes a template if it encounters the specified topocentric tone neighborhood in any scan; it is a reproducible sensitivity test, not proof that every excluded template has a human origin.

The grid correction matters because the supplied code divides rest-frequency differences by the native instrumental channel spacing, rather than the slightly different reference rest-grid spacing. Correcting this changes quantized coincidences but does not eliminate the excess relative to these controls.

The packet's seed11 control realization reproduces exactly, including maximum8. The earlier pasted maximum10 is not the maximum of this saved realization; it may describe another run or counting convention.

A plus-one tail rank for 13 versus these40 controls is1/41≈0.0244. This is **not a globally calibrated p-value**. The acceleration distribution, correlated frames, examined thresholds and other searches remain part of the trial burden. Neither zero controls reaching13 nor “4.5 standard deviations above the control mean” would justify a discovery claim.

As a separate descriptive check, all 20 ways to assign three of the six scans as ON were evaluated. The actual nominal ON grouping gives 13 clusters; the other groupings give0–6. Different sky positions, observing times and instrumental conditions need not be exchangeable, so this is not an exact randomization test. It supports preserving the association with this observing cadence while leaving its cause open.

## 3. The known line complex: C01 and C02

A receiver-frequency feature near1665.61512 MHz is visible in all six scans, including OFF pointings. Four prominent peaks in its local complex fit a spacing of about60.35 Hz, with residuals below0.9 Hz at the native2.79 Hz resolution. This is a descriptive local fit, not a transmitter identification or proof of a mains-frequency mechanism.

**C02 has direct contamination evidence.** Its selected scan 0013 track passes within0.42 Hz of the packet's cited1665.615127 MHz coordinate. About91% of its positive normalized contribution in that scan occurs near the detected local spectral peaks, using an8.38 Hz matching radius. Its exceptionally large score57.35 is therefore not evidence for a clean, localized comet tone. C02 is also the sole original candidate surviving the stricter ON≥3 rule.

**C01 needs more precise wording than the packet gives it.** Its track never crosses the central cited tone: the selected path remains at least27.5 Hz away. The literal “crosses the fixed tone” description is incorrect. Its tracks do, however, occupy the same conspicuously contaminated local line complex. In ON scan 0015, about52% of its positive contribution occurs near the measured comb peaks. This is positive evidence of contamination, without establishing that every part of C01 is explained or identifying a particular human emitter.

The same line complex is present in OFF data. A persistent stationary complex is a substantially supported contaminant explanation; it does not by itself rule out every weaker coexisting component.

C03–C13 do not intersect this local complex. They must not inherit its classification merely because C01/C02 are contaminated.

## 4. Individual candidates

The following scores reproduce the provided per-scan selection. Positive ON contributions are partly guaranteed by the selection rule and are not independent confirmation.

|ID|Nominal rest MHz|Smallest ON score|Largest OFF score|Treatment|
|---|---:|---:|---:|---|
|C01|1665.604557|2.62|1.97|Local line-complex contamination; central-carrier crossing claim incorrect|
|C02|1665.604608|3.02|1.39|Direct common-line crossing and dominant contaminated contribution|
|C03|1665.633777|2.64|1.51|Useful priority for an independent follow-up|
|C04|1666.119474|2.51|0.97|Weak and threshold-sensitive; source unresolved|
|C05|1666.167782|2.52|0.83|Source unresolved|
|C06|1666.512829|2.83|1.15|Source unresolved|
|C07|1667.138772|2.51|1.16|Source unresolved|
|C08|1667.412866|2.58|1.43|Source unresolved|
|C09|1667.430186|2.52|1.71|Three accepted rows merged; source unresolved|
|C10|1667.686517|2.67|0.96|Two accepted rows merged; source unresolved|
|C11|1667.994976|2.69|0.52|Source unresolved|
|C12|1668.098187|2.57|1.66|Source unresolved|
|C13|1668.429424|2.65|1.57|Source unresolved|

Every candidate has all six native-coordinate paths, all 294 time-sample contributions, per-scan concentration measures and a six-scan waterfall. The selected native neighbor can differ from the exported cluster-mean frequency: export_oh13.py reports a mean coordinate but scores from a separately chosen best member. The audit explicitly resolves those native choices rather than assuming they coincide.

For C03–C13, the largest single sample contributes roughly9–14% of positive contributions at most in any ON scan. They cannot all be dismissed as single-spike artifacts. This is a concentration diagnostic, not evidence of a message.

## 5. Sensitivities that remain conditional

Removing the largest one or two samples from each tracked path, while recalibrating the full-channel true-frame statistic, gives seven clusters. A frequency-baseline normalization retaining stationary spectral features gives six true-frame clusters. Matching false-frame controls were not recomputed for those two additional transformations, so neither count can be used as a calibrated rejection or validation of the original excess.

C03 retains all three ON scores above 2.5 and all three OFF scores below2 under the alternate normalization:
- ON:2.546,2.820,2.966
- OFF:1.623,1.069,0.168

At its originally selected native bins, removing the largest two samples still leaves ON scores2.990,2.780,2.524. This makes it a sensible target for further testing, not an independently confirmed signal.

The packet's lower-cut numerical claim does not reproduce from its stated configuration. ON≥2/OFF<1.5 gives 80 clusters versus a control mean83.575; ON≥2/OFF<2 gives 107 versus 108.15. Neither yields the reported118 versus 120.9. Both support the qualitative statement of no lower-cut excess, but the exact original configuration behind118 needs locating.

Raising ON to3 leaves onlyC02, the contaminated case. The absence of another OH-line counterpart is not a mandatory rejection of an artificial emitter unless a model specifically predicts both lines.

The supplied periodicity script concatenates separated ON scans before its FFT, so any physical periodicity analysis needs the real timestamps and gaps. The claimed shuffle-based timing test is not implemented in that supplied script. This does not prove it was never run elsewhere; its code/output are absent from this packet.

## 6. Nominal pointing metadata require resolution

Official blimpy code interprets HDF5 src_raj in hours and src_dej in degrees. Using those units, the source-header positions differ from the supplied comet coordinates as follows, **if interpreted in the same coordinate frame**:

|Nominal ON scan|Angular separation|
|---|---:|
|0013|0.158 arcmin|
|0015|0.711 arcmin|
|0017|16.108 arcmin|

For scale, the observatory's Gregorian beam relation gives about7.56 arcmin FWHM at 1667 MHz. A16.1 arcmin discrepancy would therefore matter if it represented actual pointing error.

That conditional must not be dropped. The headers alone do not establish actual tracking, coordinate epoch/frame or whether the field records catalog rather than contemporaneous encoder positions. Stale metadata or coordinate-convention differences remain possible. Actual pointing/antenna telemetry and header semantics are needed before calling0017 off-target. Its nominal ON label is retained in the reproduction.

## 7. Current judgment and next test

The thirteen are a reproducible computational observation. Their excess over the saved control population should be preserved as an **exploratory result requiring explanation and further testing**. The existing evidence does not warrant treating the whole population as demonstrated interference, nor does it establish artificial transmission.

The next focused test should prioritize C03, at nominal first-order rest frequency1665.633776617 MHz, using unexamined observations with adequate sensitivity. The data-derived number is a model coordinate on a2.79 Hz grid, not a sub-hertz physical measurement. The exact frequency model, allowed offset, occupancy and decision statistic should be fixed before examining those observations. A failure of a persistent-tone test would not exclude intermittent or intrinsically modulated transmission.

In parallel, resolve the nominal scan 0017 coordinate discrepancy and recover the full trial history. Same-data robustness tests do not substitute for independent observations. No semantic or communicative interpretation is established here.

## Evidence and sources

[Direct audit evidence package](https://chatgpt.com/library?file_id=libfile_6b47f6362dcc8191b56b0921522df356&account_id=personal) contains the unchanged supplied packet, exact query/response, acquisition and analysis code, hashes, true-frame score arrays, all forty control candidate sets, sensitivity tables, roles, full candidate time series and thirteen waterfalls. All six full-channel power archives are separately saved and listed in the native-input ledger.

- [Public Green Bank data index](https://bldata.berkeley.edu/ATLAS/GB_ATLAS/)
- [Official blimpy HDF5 reader](https://github.com/UCBerkeleySETI/blimpy/blob/master/blimpy/io/hdf_reader.py)
- [GBT beam specification](https://greenbankobservatory.org/about/telescopes/gbt/)
- Supplied oh13.zip, including README and original scripts; contents and hashes preserved unchanged.

