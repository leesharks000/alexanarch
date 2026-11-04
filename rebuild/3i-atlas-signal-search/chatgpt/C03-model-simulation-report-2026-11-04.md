# C03: can one line imitate a changing emitter or a swarm?

4 November 2026. Completed bounded exploratory simulation using the six previously examined Green Bank spectra; no new observing epoch.

**Yes: a single steady weak injected line can produce C03's tolerance-dependent pass and apparent peak displacement.** Single changing-frequency lines and two-/three-component mixtures can also do so. These observables do not identify a swarm. Multiple spectral components themselves could come from one radio, so even resolving several lines would not establish multiple vehicles.

## What was reproduced

All six baseline calibrations and the previously saved F1 local C03 profiles reproduce exactly (maximum profile error 0). The strict shared-frequency gate fails, margin -0.326978; allowing ±one native channel independently per scan passes, margin 0.148516. Three independent ON peaks are 1665633774.8646162, 1665633779.0555410, and 1665633774.8646162 Hz. The span and middle-versus-outers displacement are 4.190924883 Hz. These are grid-based peak estimates, not precise measured velocities or individual tracks of moving objects. One native channel is 2.793967723846 Hz.

## Experiment and denominators

The design was saved before scoring as C03-model-simulation-plan-2026-11-04.md. There are 53 fixed emitting configurations, 100 reused local backgrounds and 256 metadata-chosen broad-band backgrounds, with three equal-total-power levels: **56,604 injected trials plus 356 uninjected placements**. All use actual scan times and gaps, 16 sub-times per exposure, bin-integrated Gaussian power lines of sigma 0.6 native channels and the original first-order rest-frequency model. Only ON scans receive injected power; OFF backgrounds are unchanged. This tests target-only signal compatibility, not real astronomical localization.

The normalized amplitude at each placement is common to every alternative. Levels 2.8, 5.6 and 11.2 describe the mean noiseless steady-line increment in ON peak score; they are not observed flux, EIRP, or per-scan fitted strengths. Mixture powers sum to that same injected power at every exposure sub-time. Broad backgrounds span the common ~2.93 MHz band and include interference-contaminated positions; none were rejected by observed power. Models use q=1/2 channel offsets, periods 900/2700 s and four equally weighted fixed phases, as detailed in the plan. No phase was optimized to C03.

Equal power here means normalized model power, without a physical flux calibration. These are deterministic mean-power additions with an assumed Gaussian spectral response; source self-noise, coherent voltage phases, detailed receiver response and beam coupling are not simulated. Thus the experiment is a detector-behavior benchmark, not a complete radio-propagation model.

**Primary C03-like pattern:** tolerant gate passes, strict gate fails, and independent ON peak span ≥4.191 Hz. The **secondary pattern** additionally requires outer-peak difference ≤one native channel and absolute middle displacement ≥4.191 Hz. This secondary test permits either displacement sign and finite outer mismatch, so it is less specific than reproducing C03's exact signed triplet.

## Weakest-level results: broad placements

| Injected model | Configurations × placements | C03-like outcomes | Outer-aligned secondary | Recovered by tolerant gate |
|---|---:|---:|---:|---:|
| One steady line | 256 | 8 (3.1%) | 3 | 118 |
| One changing line | 4096 | 684 (16.7%) | 105 | 1308 |
| Two fixed, equal lines | 512 | 26 (5.1%) | 8 | 149 |
| Two lines, changing weights | 4096 | 342 (8.3%) | 63 | 1285 |
| Three fixed, equal lines | 512 | 24 (4.7%) | 8 | 80 |
| Three lines, changing weights | 4096 | 463 (11.3%) | 97 | 946 |

Counts are across configurations × reused placements. The one-line family has one configuration, changing and handoff families each have 16, and fixed mixtures each have two. These fractions describe this fixed benchmark, with its chosen models and thresholds. They are neither independent-trial probabilities nor posterior odds of source type.

Configuration choices matter: at this weak level, the 16 changing-single configurations individually produce 27–60 primary matches out of 256; two-line handoff configurations produce 9–34 and three-line handoffs 18–51. All configurations, including the less successful ones, are retained in `configuration-summary.csv` and the full trial ledger.

The critical result is the **8/256 steady-line cases**, including **3/256 secondary matches**. Frequency structure is therefore unnecessary to produce this defined C03-like behavior. Changing-frequency single-line models produce the broad phenotype more often than the tested mixture families at this equal power; that is model compatibility, not evidence selecting a transmitter model for C03.

## Conditioning on comparable recovered weakness

The predeclared subset requires a tolerant pass with its selected minimum ON score from 2.5 to 3.25 and maximum ON ≤4.0. C03 itself has selected ON scores approximately 2.65, 2.87, 3.11. For broad backgrounds at level 2.8:

| Model | Strength-matched recovered cases | C03-like | Secondary |
|---|---:|---:|---:|
| One steady line | 50 | 5 | 2 |
| One changing line | 681 | 450 | 76 |
| Two fixed, equal lines | 79 | 17 | 4 |
| Two lines, changing weights | 680 | 249 | 48 |
| Three fixed, equal lines | 50 | 19 | 5 |
| Three lines, changing weights | 566 | 346 | 78 |

Thus 5/50 recovered, comparably weak steady-line cases meet the primary pattern, and 2/50 meet the secondary pattern. These are conditional denominators, not 5/256 or a 10% probability that C03 is one steady line. Conditioning changes the population and does not correct selection of C03 itself.

## Local-background check and stronger signals

At the same weak level in the 100 local backgrounds:

| Model | Trials | C03-like | Secondary |
|---|---:|---:|---:|
| One steady line | 100 | 5 | 0 |
| One changing line | 1600 | 301 | 45 |
| Two fixed, equal lines | 200 | 16 | 4 |
| Two lines, changing weights | 1600 | 161 | 29 |
| Three fixed, equal lines | 200 | 9 | 2 |
| Three lines, changing weights | 1600 | 190 | 28 |

The primary compatibility result repeats locally (5/100 steady-line placements), although none of those 100 steady cases meets the secondary alignment criterion. No uninjected placement passes the tolerant gate in either set (0/100 local; 0/256 broad). This is a limited reused-background control, not a calibrated C03 false-alarm probability or a noise exclusion.

At levels 5.6 and 11.2, steady lines yield 0/256 primary patterns in each broad set. Their strict recoveries are respectively 253/256 and 255/256. The weak-line frequency jitter diminishes as injection strength grows. Note tolerant recovery can be lower than strict recovery: widening the OFF maximum also makes the OFF veto stronger.

## Full preprocessing validation

All 30 modified ON scans (10 three-scan cases) completed the full F1 preprocessing and full-band score calibration. Maximum absolute local score discrepancy from the fast simulation was **0.022175**, against the predeclared 0.05 guard: **PASS**.

Strict/tolerant decisions agree in 10/10 three-scan validation cases. These checks cover two fixed broad placements and the predeclared representative models/strengths, not every one of the 56,604 trials. The main simulation adds powers to fixed normalized spectra with fixed full-band score calibration; report its rates as approximate conditional-normalization benchmark results, even when the guard passes. Small preprocessing errors can still change cases arbitrarily close to a threshold.

All six native input archives passed saved SHA/CRC and extracted NPY SHA assertions before scoring. 159 independent scalar integrations of individual native-bin powers reproduce the vector response to maximum absolute error 5.33e-15. Mixture weights sum to one, and zero-amplitude raw additions preserve the tested inputs bitwise. Every full raw validation case and score profile is retained.

## What this changes for the investigation

The tiny frequency offsets are insufficient to infer multiple emitters, internal relative motion, coordination, or AI operation. A steady weak carrier remains compatible with the tested pattern. This experiment also does not show that any injected-emitter hypothesis explains the real C03 source: it does not compare an adequate model of all instrumental artifacts, interference and no-emitter backgrounds, nor compute a likelihood for the full data.

To distinguish models, examine time-resolved evidence for two resolved components present together or a reproducible frequency trajectory, and test a frozen prediction in unused sensitive data. A changing single transmitter and a multi-carrier transmitter remain degenerate with multiple physical transmitters in power spectra alone. No drone-specific, extraterrestrial, or AI-operator signature was found here.

## Files and reproduction

`C03-model-simulation.png` shows the actual profile, one illustrative steady-line secondary match and descriptive benchmark rates. The example is the first broad steady case in ledger order meeting the strength-matched secondary criterion (broad index 105); it is selected after scoring for illustration, not validation.

The evidence archive contains executable code, frozen plan, all model configurations, exact backgrounds, integrated response arrays, all 56,960 trial rows, every raw validation result, integrity/calibration checks, run logs and the prior audit dependencies. Full native powers remain at the six unchanged Library IDs in `audit/inputs/native-input-ledger.json`; large deterministic caches are regenerable. `README.md` explains restoration and commands. Earlier unfinished Wow-guided work remains separately recorded in the continuity checkpoint and is not represented as finished by this pass.
