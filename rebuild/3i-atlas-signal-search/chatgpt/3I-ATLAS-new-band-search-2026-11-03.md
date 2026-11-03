# 3I/ATLAS: a new ATA band search and fixed-frequency follow-up

Analysis date: 3 November 2026. This pass uses new public ATA observations to follow six GBT frequency locations, searches the retained band for new features, and tests the selected new features in later observations. Candidate IDs below are ours; they are not authenticated entries from the published surveys' rejected-hit catalogues.

## Outcome

**No candidate passes this batch's fixed continuation test.** Six previously selected GBT frequency locations fail their independent-epoch ATA screen. A new full-band search produces four additional weak features; all four then fail the fixed-frequency test in the next three ATA scans. This supplies no confirmed persistent tone and no new emitter identification.

The full-band count itself supplies no excess: the physical frame has four clusters, while forty comparison frames average 4.475, with a maximum of thirteen. Twenty-two comparison frames have at least four. The four locations remain individually inspectable objects; this population comparison does not identify their sources.

## Six previously selected GBT locations

The earlier GBT frequency-baseline detector found six clusters. These are its own selected set, not six survivors of the original thirteen. They include the C01 vicinity, C03, and four additional locations. We froze all six before inspecting the new ATA frequency powers.

The new scans begin on 3 July 2025 at **07:50:48, 07:57:32 and 08:04:16 UTC**. Each contributes both simultaneous beams, nineteen 16.777216-second integrations, 1.907348633-Hz channels, and the full masks. The receiver-frame cutout is 1665.750000954–1667.249999046 MHz, three contiguous 0.5-MHz storage chunks.

The model is a constant first-order rest frequency, received as `f(t)=F×(1−v_radial(t)/c)`, with observer-site JPL Horizons velocities at integration centers. The half-native-channel grids and ±5 Hz / ±100 Hz windows were fixed. Each window is scored under frequency-baseline normalization and the original-style time-median normalization, using three-bin smoothing and exact per-frequency paths. Each observation is calibrated against the complete 0.5-MHz chunk containing that target. A flag requires all three target scores ≥2.5 and all three reference scores <2 at one common frequency. These are empirical MAD scores, not Gaussian significance units.

| ID | Nominal rest MHz | Primary best target minimum, ±5 Hz | Primary best target minimum, ±100 Hz | Flags, either window or normalization |
|---|---:|---:|---:|---:|
| GBT-FB01 | 1665.604564 | −0.194 | 1.038 | 0 |
| GBT-FB02 / C03 | 1665.633777 | 0.248 | 0.867 | 0 |
| GBT-FB03 | 1665.750096 | 0.568 | 0.696 | 0 |
| GBT-FB04 | 1666.049173 | 0.436 | 1.387 | 0 |
| GBT-FB05 | 1666.529380 | 0.347 | 0.777 | 0 |
| GBT-FB06 | 1666.598233 | −0.345 | 1.714 | 0 |

“Best target minimum” means the strongest common frequency after taking the weakest of the three target scans. All twenty-four combinations of six locations, two windows and two normalizations fail the screening rule. One hundred matched frequency comparison windows were retained per location and window width; all their score cubes and summaries are saved.

This independently observed July epoch is less sensitive than the December GBT observations. The result does not refute a faint December source, an intermittent source, or an arbitrary modulated source. It is also not an independent-epoch test of every original GBT candidate: the remaining original thirteen-candidate locations were not all included in this six-location set. The reproduced original 13-versus-3.750 result and the alternate 6-versus-3.425 result remain preserved separately.

## Searching for new features across the band

A supplemental plan specified a full-band search after acquisition had begun but before inspecting the new scores or spectral patterns. It did not change the six-location test. This was an internal dated specification, not a public preregistration.

The new search uses frequency-baseline normalization only, exact physical Doppler paths, one native-channel rest-frequency grid, the same three-target/reference gate, and 10-Hz clustering. It adds no intrinsic drift fit, RFI-band veto, neighboring-bin maximum filter, or assumed instrumental-DC veto at storage-chunk centers.

The comparison population is the physical model plus forty seed-11 acceleration perturbations, with magnitudes corresponding to 0.03–1 Hz/s at 1.42 GHz and random signs. Each frame uses its own per-observation, per-chunk track-distribution median and MAD. These are deliberately different hypotheses on the same data, not forty independent observations.

Frequency coverage is fixed by an intersection calculated from ephemeris and frequency metadata across all forty-one frames and all six inputs, with a 100-native-channel source-edge margin. This retains **781,966 of 786,432** native rest-grid points. Every counted frame searches the same retained frequencies. The exact retained intervals and edge exclusions are in `metadata-coverage.json`.

| Quantity | Result |
|---|---:|
| Physical-frame clusters | 4 |
| Forty comparison frames: mean | 4.475 |
| Comparison standard deviation | 3.074 |
| Largest comparison count | 13 |
| Comparisons with at least four clusters | 22/40 |

There is no count excess here. The conditional plus-one rank is 23/41, about 0.561; it is not a global p-value incorporating all past or current exploratory trials.

The plan retained at most the five strongest physical-frame clusters, ranked by their minimum target score. There are four, so all four were carried forward. Each occupies one eligible grid point; that is the thresholded footprint, not a measured intrinsic linewidth.

| Full ID, prefix `ATA-BAND-` | Nominal rest MHz | Discovery target scores | Discovery reference scores |
|---|---:|---|---|
| F00-0001 | 1665.646564 | 2.858, 3.443, 2.529 | 1.116, 1.067, 1.459 |
| F00-0002 | 1665.737026 | 2.897, 4.012, 3.372 | 0.954, 0.641, 1.474 |
| F00-0003 | 1665.766814 | 3.265, 2.665, 2.627 | −0.335, 1.906, −1.064 |
| F00-0004 | 1666.484638 | 2.681, 3.411, 2.985 | 0.719, 1.105, −0.727 |

The printed coordinates describe the analysis grid and should not be mistaken for physical precision finer than the native channels. Exact frozen coordinates are preserved in the target file. Separate fixed-frequency calculations reproduce all twenty-four discovery target/reference scores with zero numerical discrepancy.

The largest two positive integration contributions account for about 24–41% in each target scan. This describes concentration; it does not establish noise, a transmitter, or persistent illumination. Aligned target/reference powers, mean residual profiles and all per-integration contributions are preserved for each feature. Visual inspection alone supplies no source identification.

## Held-out continuation of all four new features

The four selected best-frequency coordinates were frozen before reading the next three chronological scan pairs. The follow-up retained the ±5 Hz window, selecting normalization, physical Doppler model, smoothing, calibration rule and three-target/reference gate. No wider frequency window or new drift fit was introduced after inspection.

| ID, prefix `ATA-BAND-` | Discovery minimum target score | Best continuation minimum target score | Continuation flag | Eligible comparisons at least as high |
|---|---:|---:|---:|---:|
| F00-0001 | 2.529 | -0.323 | 0 | 65/100 |
| F00-0002 | 2.897 | -0.061 | 0 | 51/100 |
| F00-0003 | 2.627 | -0.099 | 0 | 66/100 |
| F00-0004 | 2.681 | 0.800 | 0 | 7/69 |

The continuation scans begin at **08:11:01, 08:17:46 and 08:24:30 UTC on 3 July 2025**. Every candidate has eleven valid trial points in its fixed ±5 Hz window. The strongest common point of any candidate has a minimum target score of only 0.800. All four fail the target-strength requirement itself; no reference-beam identification is needed to explain their failure.

Comparison eligibility follows the saved ephemeris/frequency-coverage rule. F00-0004 lies near its 0.5-MHz storage-chunk edge, leaving 69 eligible comparison windows; the other features each have 100. All 369 eligible comparison windows have zero continuation flags. The excluded windows and reasons are retained. This is a descriptive comparison, not an independent global significance calculation.

The result weakens persistent constant-rest-frequency interpretations of these four features. It does not establish that they were human transmitters or fluctuations alone, and it does not exclude an intermittent component. In particular, a gate requiring all three target scans will miss a source present in only one of them.

The held-out observations test temporal persistence in the same ATA session. They are new powers, but not an independent instrument or a different night's calibration environment. Their result must be interpreted at that scope.

## GBT scan0017: header provenance is clearer; pointing is still unresolved

The existing scalar source header is separated from the midpoint comet prediction by 16.108 arcmin under an ICRF interpretation, or 9.827 arcmin under an apparent-coordinate interpretation. Repeated header values in multiple products do not independently measure the beam position.

The inspected public code supplies a concrete provenance chain:

1. The hpguppi status loop reads the current GBT status fields `j2000_major` and `j2000_minor`, formats them as `RA_STR` and `DEC_STR`, and by default polls once per second.
2. Rawspec parses those strings as RA hours and Dec degrees.
3. Within its first-input-file initialization, rawspec copies those scalar coordinates into each output product's header.

The HDF5 products report rawspec 3.2.0. The inspected source supports a first-header snapshot interpretation; the exact executed build and status configuration have not been established. It also makes a J2000 source path more concrete than treating the header as an unspecified apparent position. It still cannot say whether the telescope was settled on target through the scan. A snapshot captured while status was changing is one possible explanation, not an observed fact.

The public schedule places the relevant interval in the Breakthrough Listen project GBT25B-999. The public NRAO metadata query returns no GBT execution blocks for the tested 18–19 December 2025 interval; a control query without dates returns 8,797 GBT records, validating the instrument-filter route. The BL directory contains 1,296 linked HDF5 products and no linked raw/header/FITS/log products. The operator-log route requires sign-in. Those are tested access results, not evidence that GBO has no underlying records.

A separate file, `GBT-pointing-evidence-needed.md`, specifies the small packet that could resolve this: time-tagged antenna coordinates and frame/feed metadata around 05:08:17–05:13:15 UTC, the GO record, the original raw-header sequence, and build provenance. No request has been sent to anyone. Actual scan0017 pointing remains unresolved.

## Verification, saved work and limits

All six new paired native cutouts are saved separately, with CRC checks completed on acquisition and all input SHA256 hashes verified. Every mask value in all twelve beams is zero. Twenty-four ordinary HDF5 source slices—twelve from the first discovery pair and twelve from the first continuation pair—match extracted powers and masks bit for bit across all three storage chunks. The independent fixed-frequency calculation reproduces all twenty-four selected discovery scores exactly.

The saved evidence contains fixed plans, source indexes and headers, ephemeris requests/responses, source Range hashes, all frequency-score cubes, forty-one frame cluster ledgers, all comparison outcomes, per-integration contributions, code, validation receipts and figures. Native cutouts are referenced by their saved identities and checksums rather than duplicated inside the evidence ZIP. The read-only public-code snapshot redacts embedded connection parameters; none were used.

| Native pair | Saved powers and masks |
|---|---|
| Discovery pair 1 | [GBT-FB-six-ATA-powers-scan0-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_319b7ede4dac8191acbfe60758e0bc03&account_id=personal) |
| Discovery pair 2 | [GBT-FB-six-ATA-powers-scan1-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_c24907423ce48191b221c51b27bade31&account_id=personal) |
| Discovery pair 3 | [GBT-FB-six-ATA-powers-scan2-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_950e3d84e5d081918ab3f5ea722555b4&account_id=personal) |
| Continuation pair 1 | [ATA-band-holdout-powers-scan0-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_178d43182ad0819188c521f2a190d0e9&account_id=personal) |
| Continuation pair 2 | [ATA-band-holdout-powers-scan1-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_4c2a7b38abec8191b42c0372ca6370cd&account_id=personal) |
| Continuation pair 3 | [ATA-band-holdout-powers-scan2-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_005238e5d5b88191b05690e8766249ce&account_id=personal) |

[Complete evidence package](https://chatgpt.com/library?file_id=libfile_61cc8ebb901c81918cc2de8efa867237&account_id=personal) · [Current continuation record](https://chatgpt.com/library?file_id=libfile_349f1c1635808191b815fee10ce169d7&account_id=personal)


The user's five proposed conditions remain hypothetical search guides. This pass tests one finite class: narrow power concentrated along a constant first-order rest-frequency trajectory and present in all three target scans. It does not test every intermittent, relational or meaning-bearing organization, and does not define “near determinability” as “below an amplitude threshold.” These total-intensity spectrograms also average over 16.777216-second integrations; this pass does not resolve faster organization within each integration or recover voltage phase. No decoded content or artificial origin is established by these calculations. A new hypothesis would need a specified observable relation and a separately disclosed test.

Primary sources and earlier results:

- [Breakthrough Listen observations and public-data description](https://seti.berkeley.edu/atlas/)
- [Public ATA/GBT/Parkes data root](https://bldata.berkeley.edu/ATLAS/)
- [GBT public schedule for the relevant dates](https://dss.gb.nrao.edu/schedule/public/printerFriendly?days=2&start=12%2F17%2F2025&tz=ET)
- [NRAO public archive](https://data.nrao.edu/portal/), with exact read-only requests and responses retained
- [Pinned hpguppi GBT status code](https://github.com/UCBerkeleySETI/hpguppi_daq/blob/fe82cf0cc367350a1d59dab817417008036dd52a/src/hpguppi_gbtstatus_loop.rb)
- [Pinned rawspec output initialization](https://github.com/UCBerkeleySETI/rawspec/blob/a5cc3b08820b2959d0d4e281adc110abb959df17/rawspec.c)
- [Pinned rawspec coordinate parser](https://github.com/UCBerkeleySETI/rawspec/blob/a5cc3b08820b2959d0d4e281adc110abb959df17/rawspec_rawutils.c)
- [GBT indicated-position documentation](https://www.gb.nrao.edu/GBT/MC/dataproc/gbtPosHandling/gbtPosHandling/node4.html)
- [Previous C03 follow-up and GBT normalization controls](https://chatgpt.com/library?file_id=libfile_44f436fca71481918d3de5e73564797b&account_id=personal)
- [Original direct thirteen-candidate audit](https://chatgpt.com/library?file_id=libfile_ec087222fc5c8191a477c4289e631591&account_id=personal)
