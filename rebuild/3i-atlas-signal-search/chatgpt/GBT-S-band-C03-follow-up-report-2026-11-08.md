# Later Green Bank S-band comparison of C03

8 November 2026 · completed public-data follow-up · no celestial sensitivity calibration at the candidate frequency

## Result

Neither the frozen comet-tracking model nor the frozen receiver-frequency model passed the three-ON/three-OFF recurrence screen in the later S-band cadence. The comet-track scores do retain a weak directional tendency: all three ON values are positive and all three OFF values negative. Five of 100 neighboring control tracks show at least as large an ON-minus-OFF contrast. This is an exploratory comparison selected after viewing the signs, not a detection probability.

**This result does not exclude a C03-strength source.** The numerical data cells cover its frequency, but the public receiver specifications and retrieved calibration do not establish usable celestial response there. Recorded spectral coverage and calibrated sky sensitivity are distinct.

## What was measured

The public node blc27 S-band cadence comprises scans 0029–0034 on 18 December 2025, beginning at 06:03:37 UT, about 76.5167 minutes after the first L-band scan. These are different scans on the same telescope/night. ON=29,31,33; OFF=30,32,34.

For receiver feasibility, we extracted 20 prespecified middle-product time rows per scan: every 16th row plus first/middle/last, across all 65,536 frequency bins. Sampling is 1.073741824 s and 2.861022949 kHz. This is a bandpass diagnostic, not a full intermediate-product timing search.

For the descriptive C03 comparison, we extracted all 49 native fine-product integrations in a 130-kHz cutout around the fixed coordinate and its controls. Sampling is 6.084537003 s and 2.793967724 Hz. Each cutout contains 46,531 frequency bins; the original HDF5 compression required reading one 2.93-MHz coarse chunk per time row. We retained only the smaller native cutouts, plus byte-range hashes and source metadata.

The selected fine compressed-source chunks total 956.8 MB. No entire node file was downloaded, and no download was required from the user. The 12 native NPZs (six bandpass and six fine) are included in the evidence package.

## Receiver-response finding

Official GBT documentation gives the nominal S-band receiver range as 1.73–2.60 GHz and its widest selectable RF filter as 1.68–2.65 GHz. The C03 observer frequency near 1.66564 GHz is below both lower limits. The original GBT study itself describes S-band observing coverage as 1.8–2.7 GHz. The retrieved public noise-diode/receiver calibration table, measured in 2008, begins at 1.72 GHz; it is not a calibration of the 2025 observation or a gain measurement at 1.665 GHz.

The recorded target-band powers are nonzero: approximately 0.605–0.619 times the recorded 1750–1760 MHz reference level in the sampled scans. The bandpass rises substantially toward the upper end of this node. These are ratios of recorded system power, not measured antenna-gain ratios or SEFD penalties. Post-filter receiver/backend noise can remain present where celestial response is attenuated.

No supported out-of-band celestial sensitivity was established. Consequently, no physical faint-source upper limit, calibrated EIRP fit or C03-strength exclusion is reported. A fixed raw-feature comparison remains possible and was completed separately. The check does not establish that the receiver has literally zero response at the candidate frequency.

## Frozen coordinates and models

- Comet rest coordinate: 1665633776.617238760 Hz, inherited from the prior physical C03 fit.
- Intrinsic Gaussian sigma: 1.676380634 Hz, integrated across each exposure with 16 subtimes. The initial staged-plan one-bin width was corrected from the actual inherited plan before fine powers were inspected.
- Receiver-fixed coordinate: 1665644304.702512 Hz, anchored to the modeled observed RF at the original L-band ON 13 midpoint. It is not the bare rest-frame coordinate.
- New JPL Horizons ephemeris uses the GBT geodetic site. Its overlap with the saved earlier ephemeris differs by at most 0.002119 Hz at C03; an orbit/velocity revision is not driving the comparison.
- The 100 inherited spectral-control offsets are +/-1 to 50 kHz in 1-kHz steps. Local baseline parameters and inverse-control-variance temporal weighting are inherited without tuning. The matched frequency is not maximized per scan.
- This narrow cutout tests C03 and controls. It does not retest all thirteen original candidate coordinates.

## Fixed-coordinate results

Scores are control-normalized matched-profile statistics; they are not Gaussian significances. The inherited diagnostic gate requires all ON scores>=2.5 and all OFF scores<2.0.

| Scan | Pointing | Comet-track score | Receiver-fixed score |
|---|---|---:|---:|
| 29 | ON | +0.128 | +1.802 |
| 30 | OFF | -0.282 | -0.022 |
| 31 | ON | +1.523 | +0.368 |
| 32 | OFF | -0.203 | -0.055 |
| 33 | ON | +1.202 | +1.319 |
| 34 | OFF | -0.595 | +0.833 |

No ON scan reaches 2.5 under either model. Both complete recurrence gates fail. This says that the specified raw-feature recurrence screen was not met; it is not a calibrated null at the earlier conditional 26 mW source strength.

## Retained weak ON/OFF tendency

The comet model has all ON scores above all OFF scores, and the all-positive-ON/all-negative-OFF sign pattern. Three of 100 controls share the latter sign pattern, six share complete ON/OFF ordering, and 5 have at least as large an ON-minus-OFF mean-score contrast. The target contrast is 1.974 robust control units.

The receiver-fixed contrast is weaker (1.140 robust control units; 12/100 controls at least as high), but that difference is not a demonstrated preference between physical source models.

This contrast analysis is explicitly adaptive: it was added after inspecting the per-scan signs. The controls share a receiver and have correlated spectral/background structure. The control counts are descriptive ranks, not a global p value. The pattern is retained in full; a threshold failure is not evidence that every amplitude is exactly zero. No frequency was shifted to improve it.

## Recovery and independent reconstruction

660 mean-power Gaussian line injections were made in the actual native arrays at the frozen target and ten prespecified neighboring coordinates, under both track models. Injected dimensionless line amplitudes were 0.01,0.03,0.1,0.3 and 1.0, using frozen background weights. These characterize recorded-data recovery, not response to a transmitter with stated EIRP.

All twelve native-array hashes were checked; 42 source-HDF5 scalar comparisons match the decoded cutouts. Independent Python median/fsum reconstructions reproduce all twelve scan/model scores to maximum error 8.88e-16. Raw-power injections change the recovered line amplitude by the intended amount to maximum error 1.79e-07. The 12 selected-row scalar profile checks use three source rows per model per scan (36 row comparisons), and exposure-integrated template mass is verified.

## What this changes

The initial header audit correctly established recorded frequency coverage but did not establish useful astronomical response. This follow-up qualifies the proposed later-cadence test: the data permit a descriptive raw-feature comparison, but not a strong physical absence claim at this out-of-spec frequency.

C03 remains unresolved. The later data offer a weak aligned ON/OFF tendency, with several neighboring controls as strong or stronger and no qualifying recurrence. We have not identified a human transmitter or an extraterrestrial one. The earlier L-band results remain unchanged.

The next useful public-data test is the original L-band gain-variation audit: align the already-measured shared excursions with the original 6.085-second narrowband integrations and check whether the apparent feature or ON/OFF contrast changes, using injected lines to test preservation. A suitable voltage or intermediate-resolution product would address candidate-resolved modulation. More uncalibrated S-band threshold cuts would not supply the missing physical sensitivity.

## Reproduction and sources

The evidence archive includes the native samples/cutouts, scripts, saved JPL queries/responses, original C03 plan/coordinate source, receiver documentation, calibration table, byte-range hashes, per-row profiles, all spectral-control scores and all injection trials. README-reproduce.md and CHECKPOINT.md give clean recovery steps. No external message was sent.

- Public observation listing: https://bldata.berkeley.edu/ATLAS/GB_ATLAS/
- GBT receiver ranges/filter choices: https://www.gb.nrao.edu/electronics/GBTelectronics/Receivers/greg.html
- S-band filter documentation: https://gbtdocs.readthedocs.io/en/latest/references/receivers/s-band.html
- Public calibration table: https://www.gb.nrao.edu/electronics/GBTelectronics/Receivers/tcal/tcalrcvr2_3.txt
- Original observation paper: https://seti.berkeley.edu/atlas/Breakthrough_Listen_Observations_of_3I_Atlas_with_the_GBT.pdf
- JPL Horizons response and query: inputs/sband-horizons-response.json and inputs/sband-horizons-query.json