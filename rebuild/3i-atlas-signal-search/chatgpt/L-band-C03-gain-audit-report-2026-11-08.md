# C03 and the shared L-band power excursions

8 November 2026 · completed gain/normalization audit of the original six Green Bank scans

## Result

The measured shared-power excursions do not remove C03’s strict matched-profile statistic under the tested corrections. A row-level gain division leaves the result unchanged, as the detector’s local normalization predicts. Accounting approximately for variation within an integration changes the scores only slightly.

The first OFF pointing remains consequential: removing the two integrations affected by the deep OFF14 dip raises its score from **1.821 to 2.121**. The dip is therefore not the source of its positive support in this statistic. No tested branch produces a qualifying three-ON/three-OFF recurrence.

This is a robustness/mechanism test on the same previously inspected observations. It does not establish a celestial source, identify a particular human emitter, or replace the earlier tolerance-dependent C03 discovery screen.

## What was aligned

We restored the six saved full fine-resolution arrays and six saved high-time cutouts, checking their original hashes. The new reproducible package preserves exact smaller fine-frequency cutouts and the full derived shared-power curves; original full arrays remain at their existing persistent identities.

For each high-time reference channel, power is divided by that channel’s scan median. The timewise median over fifteen neighboring channels—48–55 and 65–71, excluding target/boundary channels 56–64—defines a shared-power proxy. It can contain receiver, interference or sky variability. It is not a calibrated gain measurement or an identified instrumental cause.

Headers align the high-time and fine-resolution products. Each 6.084537-second fine integration spans 17,408 samples at 349.525 microseconds, or 17 groups of 1,024 high-time samples. The 49 fine integrations cover 852,992 high-time samples. Another 5,120 high-time samples (~1.790 seconds) lie beyond the completed fine product and were not used in its exposure model. Their original data remain preserved.

The fixed quality rule flags any fine integration overlapping a complete ~0.1-second shared-proxy bin outside [0.8,1.2] of the scan reference. It flags only OFF14 integrations 26 and 27 (zero-based), spanning approximately 158.198–170.367 seconds. All ON integrations remain.

## Why scalar gain cancels

The local background is a median of nearby block means, calculated separately for every integration. It scales with a positive factor applied to that entire spectral row. Writing the normalized residual as

\[R_{tf}=\frac{P_{tf}}{B_t}-1,\]

division by a shared row factor gives

\[\frac{P_{tf}/g_t}{B_t/g_t}-1=R_{tf}.\]

The raw-bin test confirms this on all target and control profiles. The largest whole-scan score difference from row division is **1.02e-14**. This is numerical roundoff, not a physical change. A purely frequency-independent factor constant within each integration cannot create this normalized feature by itself.

The calculation does not exclude frequency-dependent artifacts, additive processes, or effects of time variation during the voltage-level Fourier transform. Those are different mechanisms.

## Five fixed branches

The inherited rest coordinate is 1665633776.6172388 Hz, with Gaussian sigma 1.6763806343 Hz and 100 unchanged neighboring spectral controls. There is no frequency or width optimization. Background-window indices are held to the inherited 16-position path so that template comparisons are not driven by an index-rounding shift.

- **Original16:** exactly reproduces the prior strict physical mean-power profile.
- **Row-scalar:** divides every spectral row by its mean shared-power proxy and repeats the same normalization.
- **Uniform17:** changes only the exposure quadrature to seventeen evenly weighted positions.
- **Power-weighted17:** weights those positions by measured block-average shared power. This is an approximate intensity exposure model, not a coherent-voltage correction.
- **Quality-mask16:** omits the two flagged OFF14 integrations and repeats the original fit. This is a secondary exclusion diagnostic, not an automatic improvement.

| Scan | Pointing | Original | Power-weighted17 | Quality-mask |
|---|---|---:|---:|---:|
| 13 | ON | +2.6670 | +2.6665 | +2.6670 |
| 14 | OFF | +1.8209 | +1.8231 | +2.1209 |
| 15 | ON | +2.3982 | +2.3985 | +2.3982 |
| 16 | OFF | -0.0629 | -0.0630 | -0.0629 |
| 17 | ON | +1.8489 | +1.8487 | +1.8489 |
| 18 | OFF | -0.9581 | -0.9583 | -0.9581 |

These are control-normalized profile statistics, not Gaussian detection significances. The inherited diagnostic screen requires all ON scores ≥ 2.5 and all OFF scores < 2.0. It fails in every branch. The original strict ON values remain approximately 2.667,2.398 and 1.849.

After isolating the quadrature change, the largest score change due to the measured within-integration weighting is **0.002215**. The largest modeled spectral-center shift is **0.013408 Hz**, compared with 2.794-Hz native channels. No qualifying recurrence appears or disappears through this small template effect.

## What the OFF14 exclusion shows

The two flagged integrations contain negative target-profile amplitudes at the fixed C03 track. Removing them raises the control-centered whole-scan line amplitude from 0.066381 to 0.077714; its control MAD changes only from 0.036456 to 0.036642. The higher score is not merely a large shrinking of the noise scale.

The dip therefore does not explain away the off-target support under this estimator. The masked OFF14 score also exceeds the inherited OFF-screen threshold 2.0. Actual antenna tracking for ON17 and the physical origin of the features remain unresolved; this audit does not supply those missing measurements.

## Injected lines and validation

The audit contains 1,020 model-matched mean-power injection trials: 990 steady lines at the target and ten fixed neighboring coordinates, plus 30 one-integration tests at the most depressed shared-power interval. Three dimensionless line amplitudes (0.03,0.1,0.3) are used for steady tests; the transient uses 0.3. Local normalization is applied to actual raw power bins and control comparison weights are frozen. These are prescribed-coordinate recovery checks, not a global completeness or new EIRP calibration.

An additional 90 tests inject the **same original16 signal** and fit it with each branch. The per-row response ratios range from **0.99964081 to 1.00007148**: the tested template changes preserve this conditional weak-line signal to about 0.04%.

The masking exception is explicit: a real one-integration line injected into the removed OFF14 interval is completely discarded by that branch. The all-row original and weighted branches retain that interval. Masking cannot be advertised as universally preserving unknown transient signals.

All six smaller input archives pass their recorded hashes. All six cadence/grouping reconstructions agree exactly. Independent Python median/fsum calculations reproduce all 30 whole-scan scores to maximum difference 9.99e-16. Selected original-bin sums and template normalization are checked in each branch, and the original 101-by 49 strict profile arrays reproduce the prior saved outputs. The maximum raw injected-amplitude increment error is 6.66e-16.

## Interpretation and remaining test

The shared row-level power variation is already normalized out of this detector. The measured sub-integration intensity-weighting model also has negligible effect. These particular mechanisms do not resolve C03. The stronger OFF14 support after excluding the dip gives no cleaner ON-only localization.

We did not reconstruct voltage phase or how rapid variation could alter the coherent FFT window and spectral leakage. The weighted Gaussian intensity model cannot substitute for those calculations. A voltage-level analysis would test that remaining mechanism directly, if the relevant recordings survive and can be obtained. Frequency-specific interference and instrumental effects likewise remain possible.

The published voltage-retention evidence is preserved with this audit: Berkeley’s 3I/ATLAS page says raw voltages were being transferred from Green Bank. That supports a retention/transfer intention for this dataset; it does not confirm the current inventory, successful transfer or access conditions. No external message was sent.

## Source statements

- [Berkeley 3I/ATLAS observations](https://seti.berkeley.edu/atlas/overview.html): raw voltages described as being transferred from Green Bank. Saved HTML and hashes are in sources/.
- [General Green Bank retention policy](https://seti.berkeley.edu/bl_gbo.html): many recordings are reduced and deleted; selected voltage observations are retained. This general policy does not establish the present status of these scans.

## Reproduction

The evidence archive includes native fine cutouts, full derived shared-power curves, seventeen-block weights and quality masks, inherited model/ephemeris inputs, original strict reference profiles, all branch profiles/scores, injection ledgers, independent validation, plots and source statements. CHECKPOINT.md and README-reproduce.md provide recovery and offline reconstruction steps. Original full native archive IDs and hashes remain in the input ledgers.
