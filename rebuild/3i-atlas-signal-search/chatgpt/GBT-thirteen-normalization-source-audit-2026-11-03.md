# Green Bank thirteen: normalization, trajectory specificity, and source audit

3 November 2026. Exploratory continuation on the same six December 2025 Green Bank observations, not a new observing-epoch confirmation. No source is identified as an artificial transmission.

**Main findings:** changing the baseline axis explains the 13-versus-6 population change; row whitening does not explain it. A denser trajectory bank contains a different 15-cluster population. C03 is the only original candidate passing all four tested normalizations at its original paths, and its local comparison and motion-model checks preserve its priority. The scan0017 header has a plausible return-slew geometry, but actual pointing remains unresolved.

## 1. Controlled normalization experiment

The prior comparison changed both baseline and row weighting. We crossed them while retaining the original tracking, rounding, cross-scan alignment, ±1-bin maxima, nine DC-bin zeroing, ON≥2.5/OFF<2 gates and 10 Hz clustering.

T divides each frequency channel by its median over the 49 time integrations, then subtracts one. F divides each row by an interpolated frequency baseline from 1024-channel median blocks. Row whitening additionally removes the row median and divides by 1.4826 MAD. T0 reproduces the original method; F1 reproduces the previous alternative. T1 and F0 isolate the bundled changes. All scores remain empirical detector units, not Gaussian significances or physical fluxes.

| Method | Baseline | Row whitening | Object-frame clusters | Mean of original40 comparisons | Comparison maximum | Comparisons ≥ object count |
|---|---|---|---:|---:|---:|---:|
| T0 | Time median | no | 13 | 3.750 | 8 | 0/40 |
| T1 | Time median | yes | 13 | 3.750 | 8 | 0/40 |
| F0 | Frequency baseline | no | 6 | 3.400 | 9 | 7/40 |
| F1 | Frequency baseline | yes | 6 | 3.425 | 9 | 7/40 |

The T1 cluster coordinates match all thirteen original clusters. F0 and F1 select the same six coordinates. Those six include C03, a different path about 6.985 Hz from C01 in its known contaminated complex, and four other frequencies. They are not six original survivors. At the fixed original paths, only C03 passes F0/F1; the ±5 Hz original-coordinate window test also retains only C03.

The controlled count result isolates baseline choice, rather than row whitening, as the source of the population change. It does not establish which baseline has better sensitivity to every possible real signal. No new GBT injection-completeness curve was measured in this pass.

## 2. Where the individual scores change

All 78 original paths were reconstructed under each method: 312 scan/method scores. The stored per-time contributions reproduce every cached path score exactly. A symmetric algebraic decomposition of T0→F0 separates changes in tracked residual sum, global tracked median, and global MAD scale.

For ON scans13/15/17, the frequency-baseline global MAD is respectively about 5.35%, 5.01%, and 4.77% larger. This produces a modest downward standardized-score change. Changes in the tracked residuals themselves supply most of the mean loss across C03–C13; global-center changes are small. This is an exact accounting of the calculation, not a physical identification of the residuals' sources. The decomposition CSV preserves every term and its reconstruction error.

Twenty original ON paths cross below2.5 under F0/F1. Failures at the original native choices are:

| Candidate | F1 minimum ON | F1 maximum OFF | Failed scans | Source-evidence assessment |
|---|---:|---:|---|---|
| C01 | 4.943 | 2.708 | OFF 0014 | Known shared line-complex contamination; no transmitter ID |
| C02 | 4.751 | 6.296 | OFF 0014,0018 | Direct known shared-line contamination; no transmitter ID |
| C03 | 2.546 | 1.623 | none | Passes all four; highest-priority original case |
| C04 | 1.251 | 0.800 | ON 0013,0015 | Loses ON support; source unresolved |
| C05 | 1.090 | 0.726 | ON 0013,0015 | Loses ON support; source unresolved |
| C06 | 1.645 | 1.855 | ON 0015,0017 | Loses ON support; source unresolved |
| C07 | 2.100 | 0.803 | ON 0015,0017 | Loses ON support; source unresolved |
| C08 | 1.558 | 1.177 | ON 0013,0015,0017 | Loses ON support; source unresolved |
| C09 | 2.081 | 2.943 | ON 0013; OFF 0014 | Loses ON support and exceeds OFF gate; source unresolved |
| C10 | 2.309 | 0.800 | ON 0013,0017 | Loses ON support; source unresolved |
| C11 | 1.649 | 0.718 | ON 0013,0015,0017 | Loses ON support; source unresolved |
| C12 | 1.014 | 1.186 | ON 0015,0017 | Loses ON support; source unresolved |
| C13 | 2.011 | 1.615 | ON 0017 | Loses ON support; source unresolved |

C01/C02's source evidence comes from the previously documented shared spectral complex, supported by the preserved contextual spectra. An OFF-threshold failure alone does not identify an emitter. C04–C13's normalization failures do not establish that each is interference or a statistical fluctuation. No new specific human transmitter was identified. Thirteen common-frequency, six-scan context figures and their normalized crops are preserved; scans remain separate, and OFF pointings are sequential rather than simultaneous beams.

## 3. A denser trajectory bank changes the population comparison

We retained the exact original forty acceleration perturbations and added sixty nearby probes: received-frequency drift errors −0.150…+0.150 Hz/s in0.005 steps at1667MHz, omitting duplicate zero. The corresponding radial-acceleration addition is −error×c/1667MHz. These are correlated model-specificity probes, potentially retaining real features, not independent noise samples.

| Method | Object count | Largest dense-probe count | Dense probes ≥ object count |
|---|---:|---:|---:|
| T0 | 13 | 15 | 1/60 |
| T1 | 13 | 14 | 1/60 |
| F0 | 6 | 11 | 21/60 |
| F1 | 6 | 11 | 22/60 |

T0 reaches15 at +0.125Hz/s error; T1 reaches14 at the same probe. Its net received drift is roughly +0.0003 to +0.0170Hz/s across the three ON scans, close to stationary. Thus the physical frame is still a local response peak under T, but it is not the largest count in this specified bank.

The competing fifteen occupy different frequency neighborhoods from the original thirteen. Their complete ledger is retained as D95-01…D95-15. An explicitly post-result crosscheck shows none passing F0/F1 within±5Hz of its selected coordinate; all lose the required ON support. This strengthens the diagnosis of baseline dependence in this count statistic. It does not identify those fifteen as interference. They remain a separate exploratory population, not an unrecorded discarded control.

No global p-value is assigned. Neither the original1/41 rank nor a rank combining these correlated, explored banks settles the full trial burden. Changing normalization also changes which structures and real signals can be retained.

## 4. C03 survives the tested baseline choices

Nominal first-order coordinate: **1665.633776617MHz**. Its precision is an exported analysis coordinate on a2.794Hz native grid, not physical millihertz accuracy.

| Method | Fixed-path minimum ON | Fixed-path maximum OFF | Best ±5Hz gate margin | Nearby comparison windows ≥ that margin |
|---|---:|---:|---:|---:|
| T0 | 2.6394 | 1.5052 | 0.1394 | 0/100 |
| T1 | 2.6405 | 1.4919 | 0.1405 | 0/100 |
| F0 | 2.5452 | 1.6214 | 0.0452 | 0/100 |
| F1 | 2.5463 | 1.6233 | 0.0463 | 0/100 |

The comparison centers are ±250, ±500, …, ±12500Hz; every center has the same±5Hz frequency freedom and three-ON/three-OFF requirements. The gate margin is min(ONscores−2.5, 2−OFFscores), maximized within the window. Zero of the100comparison windows passes the gate near C03 under any method. Complete local ledgers exist for all13candidates, not just C03.

These are descriptive checks of a candidate already selected from a broad search. The same100neighborhoods and same data are reused across methods, so this is not400independent trials or an independently calibrated detection probability. The smallest F margins are only about0.045–0.046 above the threshold. C03 remains weak, despite being comparatively robust.

## 5. Physical background-motion controls

After initial factorial counts were visible, a separately saved exploratory addendum specified two ordinary context models: fixed receiver frequency; and a fixed-direction emitter stationary in the solar-system barycentric frame. The latter includes the observatory's orbital and rotational Doppler motion.

Horizons supplied geometric SSB-relative-to-GBT vectors, in equatorial ICRF, km/s and UT. SSB-relative velocity is minus observer barycentric velocity. We projected it onto the fixed ICRF comet direction at the cadence midpoint, then added one constant velocity offset to match the first reference frequency convention. This absorbs an unknown emission-frequency zero point, without fitting acceleration. These are first-order path models with an additive frequency-zero convention, without a complete relativistic/clock uncertainty budget. The full varying curves were used; the OFF scans were evaluated under the same model direction as ON, as in the legacy comparison.

| Method | Object model | Fixed receiver | Fixed-direction barycentric model |
|---|---:|---:|---:|
| T0 | 13 | 3 | 3 |
| T1 | 13 | 3 | 3 |
| F0 | 6 | 6 | 10 |
| F1 | 6 | 6 | 10 |

The population ranking again depends on baseline: T favors the object-frame count, while F gives more clusters under this particular barycentric model. These are different selected populations, not classifications of the original13.

At C03's initial frequency coordinate±5Hz, neither background model passes under any normalization. Whole-band background selections also produce no accepted cluster near C03: the nearest accepted cluster is at least about68kHz away in these runs. Forty-eight independent scalar rescores from native C03 powers reproduce the background-model scores exactly. Thus two simple stationary-source alternatives do not explain C03 under the stated model and gate. Variable interference, other intrinsic drifts, instrumental effects and selected noise remain open.

This extension was post-result exploratory and uses the same data. It does not identify the source, supply fresh confirmation, or show that an arbitrary background-motion model has been excluded.

## 6. What the header check adds

The six HDF-derived source positions reproduce their original metadata. Nominal OFF pointings are approximately30.48,60.09and60.18arcmin from the predicted ICRF target at their midpoints. The ON offsets are0.158,0.711and16.108arcmin. All six source_name strings read DIAG_3I_ATLAS despite their different positions and OFF filenames, so that string alone is not an ON/OFF role indicator.

Scan0017's scalar header lies **0.542arcmin from the tangent-plane segment joining the precedingOFF0016header and the predictedON0017position**, at26.68%of the segment's distance from the target toward the precedingOFF. This geometric relationship is compatible with a coordinate snapshot partway through a return slew. It is not a measured slew path and does not establish that the settled observation was off target or correctly on target. The inspected first-header copying chain makes a latched value plausible, while its exact deployed provenance remains unverified.

Actual antenna/GO records for approximately2025-12-18 05:08:17–05:13:15UTC, with settling margins, are still needed. No new tracking telemetry was obtained and no request was sent to another person. Known sign-in walls were not bypassed or repeatedly treated as new evidence.

## 7. Verification and scope

Six native NPZs pass their existing source-ledger SHA256 and CRC checks; restored NPYs match all six prior hashes. All156previous T0/F1selected-path scores reproduce exactly, and all six entire T0true-frame score vectors match the unchanged original function bitwise. The two reference population/control counts reproduce. All312fixed-path component scores and48C03background raw rescores have zero observed numerical discrepancy. Seventeen optimized local-index selections match full-array searches exactly. The78symmetric score decompositions reconstruct to floating-point precision.

The vector position derivative agrees with the supplied velocity to about6.5e-7km/s. Printed JD interval rounding initially tripped a stricter check; using the exact printed UT calendar intervals resolved that numerical-time subtraction issue without changing the check threshold or the signal models. The source query/response and check values are saved.

The analysis retains legacy rounded tracks, coordinate-grid behavior, DC handling and circular shifts to isolate normalization effects. It is not a new fully corrected detector. Alignment collisions are logged rather than silently repaired. The original candidates are well inside the coarse-channel boundary. Source and clock/ephemeris uncertainties remain separate from numerical implementation checks.

No injected-signal sensitivity study of these new GBT factorial variants or calibrated flux/EIRP bound was produced. Previous ATA injection results cannot be transferred numerically to them. All six scans have already been examined; internal robustness does not furnish an independent observation. The earlier lower-sensitivity JulyATA nulls remain separate.

## 8. What this pass supports

C03 deserves the next individual-source investigation. Its baseline robustness, local specificity and failure under the two simple background models are positive same-data evidence to preserve. The thirteen-count population remains conditional on baseline treatment, with a competing count peak in another trajectory family. We have explained which computational operation drives the population change and documented the per-candidate threshold failures; we have not identified the physical source of C03–C13 or fully calibrated the count excess.

The next discriminating evidence would be adequately sensitive unused observations at the predicted frequencies, actual scan0017tracking records, and targeted recovery/background studies before preferring one normalization's physical interpretation. The receiver-aware hypothesis remains a guide to constructing tests; no encoded content or AI operator has been inferred.

## Reproduction

Place the six saved full-coarse NPZs in native/ using inputs/native-input-ledger.json (each has a persistent file ID and hash). Extract this evidence package in one directory. The required non-power inputs and original reference function are included. Deterministic score caches are omitted; allow roughly25GBtemporary space to regenerate them. Python/NumPy/Matplotlib versions are recorded in environment.json.

Run:

```bash
python restore_native.py
python experiment.py scores
python experiment.py counts
python candidates.py
python decompose.py
python pointing.py
python background_models.py
python background_candidate_checks.py
python verify_background.py
python competing_population.py
python plots.py
python make_report.py
```

The saved vector response is sufficient; get_background.py makes the separately recorded public query only if a fresh response is desired. Scoring can resume hash-checked completed batches. Small calibration/check receipts, complete404frame cluster/accepted-row ledgers, all5200local comparison rows plus52primaries, component/time tables, background curves, named competing15, source crops and13context figures accompany the code. Large native powers have their own persistent records.

- [Original thirteen audit](https://chatgpt.com/library?file_id=libfile_ec087222fc5c8191a477c4289e631591&account_id=personal)
- [Earlier normalization controls and ATA follow-up](https://chatgpt.com/library?file_id=libfile_44f436fca71481918d3de5e73564797b&account_id=personal)
- [This pass's fixed plan](https://chatgpt.com/library?file_id=libfile_f9380a0e02308191bea625654f65af19&account_id=personal)
- [This pass's executable evidence](https://chatgpt.com/library?file_id=libfile_067ebefc4a248191b17bb5a879331d1e&account_id=personal)
- [Continuation checkpoint](https://chatgpt.com/library?file_id=libfile_349f1c1635808191b815fee10ce169d7&account_id=personal)
- [Official Horizons API documentation](https://ssd-api.jpl.nasa.gov/doc/horizons.html)
- [Official Horizons manual](https://ssd.jpl.nasa.gov/horizons/manual.html)

- [GBT-OH13-full-scan0013-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_3dd4425a7aac8191ad7ba836e142d03e&account_id=personal)
- [GBT-OH13-full-scan0014-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_807421c1c4e08191932b2bf77c630eb9&account_id=personal)
- [GBT-OH13-full-scan0015-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_3f9eb1d00430819197d794acb6cb936a&account_id=personal)
- [GBT-OH13-full-scan0016-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_d5147211ae2c81919a76965755b847f9&account_id=personal)
- [GBT-OH13-full-scan0017-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_20e6af053e9481919fbf1257ef3d4af1&account_id=personal)
- [GBT-OH13-full-scan0018-2026-11-03.npz](https://chatgpt.com/library?file_id=libfile_ca0844003e6481919726c1ad604f8b15&account_id=personal)
