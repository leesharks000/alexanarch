# C03: equal transmitter strength across telescopes, and its measured time profile

Completed 5 November 2026. **The earlier ATA nondetection is expected for a transmitter as faint as the amplitude fitted to C03 under this model. The Green Bank time profile does not resolve a distinctive burst or a clean switching event.** These conclusions do not establish that C03 is a physical emitter or identify its source.

The same Earth-directed transmitter power was injected into actual Green Bank December and ATA July backgrounds, accounting for distance, instrumental sensitivity, native channel width and exposure smearing. This replaces the earlier comparisons in arbitrary raw-MAD or score units. It remains conditional on representative published calibration values, a fixed Gaussian line and unit on-axis target response.

## Equal-power result

With nominal GBT SEFD 12.5 Jy, the descriptive common-power fit to the three ON amplitudes is **26.36 mW**. The assumed 10–15 Jy GBT range changes that to **21.09–31.63 mW**. These are calibration scenarios, not a confidence interval or an independently measured transmitter power. The feature was selected before this analysis; the fit is selection-biased. It assumes the source is at 3I/ATLAS's distance and on axis.

The combined empirical spectral-control MAD of the nominal fit is 6.07 mW, which is descriptive scatter, not an unconditional significance. Per-ON fitted values are 28.01, 31.24, 20.82 mW; their respective control MADs are 10.50, 13.03, 11.26 mW. The third scan's actual antenna tracking remains unresolved, so these cannot be interpreted as three established on-axis flux measurements.

At nominal ATA SEFD 390 Jy, the same 26.36 mW model adds only **0.0155–0.0175 detector-score units** per July scan, against a target screen of 2.5. Recovery is **0/100 backgrounds**. Across all 15 combinations of GBT calibration-derived fitted strength and ATA 200–800 Jy scenarios, the added ATA score ranges from 0.0060 to 0.0409, and every projection has 0/100 target recoveries.

The score response per watt in these data is approximately 131–156 times greater at GBT than ATA under nominal calibration. This includes receiver sensitivity, distance, sampling and the empirical matched-control scatter; it is not an intrinsic universal telescope ratio.

| Equal EIRP | GBT target recovery | GBT joint screen | ATA target recovery | ATA joint screen |
|---|---:|---:|---:|---:|
| 0.003 W | 0/100 | 0/100 | 0/100 | 0/100 |
| 0.01 W | 0/100 | 0/100 | 0/100 | 0/100 |
| 0.03 W | 12/100 | 11/100 | 0/100 | 0/100 |
| 0.1 W | 100/100 | 94/100 | 0/100 | 0/100 |
| 1 W | 100/100 | 94/100 | 0/100 | 0/100 |
| 3 W | 100/100 | 94/100 | 7/100 | 3/100 |
| 10 W | 100/100 | 94/100 | 100/100 | 87/100 |

The primary recovery location is known and fixed; there is no frequency search. The target-only rule requires all three ON scores >=2.5. The joint rule additionally requires all three reference scores <2. Strong-source joint recovery can plateau below 100 because some background placements have reference power above that veto. Counts describe reused empirical backgrounds and deterministic mean-power additions; they are not independent Bernoulli probabilities, calibrated Gaussian significances, or source-origin odds. Zero-power baselines produce no three-ON recoveries in either instrument.

## Temporal profile

The CSV retains all 49 native integrations in each GBT scan (approximately 6.08 seconds), all six original scan times and real gaps. Fixed five-integration bins are about 30.4 seconds, with the final partial bin kept explicitly. No averaging crosses a scan gap. OFF pointings view different sky positions: their lower values cannot establish that a celestial source switched off during those intervals.

Primary extraction follows one common C03 rest-frequency track. A separate plot/CSV branch uses the three already-selected per-ON peak frequencies; a third holds received frequency fixed at the first ON midpoint. None chooses a new frequency peak per integration. Signed, including negative, line-amplitude estimates are retained.

The fixed-track scan scores are:

| Scan | Role | Common-track score | Equivalent power proxy, nominal SEFD | One control MAD |
|---|---|---:|---:|---:|
| 13 | ON | 2.667 | 28.01 mW | 10.50 mW |
| 14 | OFF | 1.821 | 21.08 mW | 11.58 mW |
| 15 | ON | 2.398 | 31.24 mW | 13.03 mW |
| 16 | OFF | -0.063 | -0.85 mW | 13.43 mW |
| 17 | ON | 1.849 | 20.82 mW | 11.26 mW |
| 18 | OFF | -0.958 | -10.69 mW | 11.16 mW |

Under this new physical-template detector, the strict three-ON screen does not pass at the observed C03 coordinate. This does not overwrite the earlier tolerance-dependent result obtained with a different detector. The primary amplitude profile is weak and does not establish a clean onset/termination. The first OFF pointing also has a positive fitted amplitude, comparable to the third ON pointing within the control scatter; it remains below the reference cut and does not identify an emitter.

A bounded temporal search tested every start for windows of 5, 10 and 20 samples, separately inside each ON scan, comparing each window with the remainder of that same scan. The strongest contrast is scan 15, samples 6–10, approximately 30.4 seconds. **74/100** matched spectral-control placements have at least as strong a maximum after the identical three-scan, 345-window search. This provides no exceptional temporal-structure result under that diagnostic. It is a conditional comparison, not a global p-value and not a measured physical burst duration.

The exported amplitude curve is therefore an estimated time profile with noise, not a recovered transmitter activation envelope. A weak steady line remains compatible; intermittent, instrumental and interference explanations remain unresolved.

## Physical model and calibration limits

The intrinsic rest-frame Gaussian sigma is 1.676380634 Hz, the same physical width at both telescopes. Each exposure integrates 16 sub-times and exact Gaussian fractions over signed native bins. Integrated flux follows P/(4 pi d^2); native-bin density divides by channel width. Raw increments use each row's local system-power baseline and assumed SEFD. The baseline is the median of twenty 128-channel block means away from the line, not the local raw MAD. JPL observer ephemerides supply distance and first-order radial Doppler tracks.

GBT uses the paper's 10–15 Jy SEFD range. ATA's published 1336 MHz tuning estimate is 390 +/-60 Jy; the 200/800 Jy endpoints used here are wider stress scenarios, not quoted uncertainty limits. The published ATA figure is averaged across antenna/sessions and is not a measured scan-specific calibration at C03's near-band-edge frequency. No new calibration-source observation, encoder tracking record, or beam-response measurement was obtained. ON17 remains unresolved. Changing emission direction, duty cycle, polarization, line width or frequency law is outside the steady equal-EIRP primary test. A full Doppler/clock/relativistic uncertainty budget is not supplied.

## Checks and recoverability

All six original GBT archives and their extracted NPY arrays matched their stored SHA-256 hashes, and their member reads passed ZIP CRC verification. All three paired ATA archives matched original hashes; arrays are finite/positive and masks zero. Independent scalar original-bin sums agree with the C03 path in all 24 observation/track products to the saved tolerance. Gaussian-bin quadrature covers both instruments' relative line widths.

All 36 actual float32 injection checks recomputed the local background baseline and matched-template estimate. The maximum score discrepancy from the fast conditional-calibration calculation was 4.7303e-06, below the fixed 0.05 guard. The maximum recovered total-injected-power relative error was 0.000219526. All zero-amplitude bitwise checks passed. The injections model deterministic Gaussian mean power; detailed channelizer/window response, source self-noise and coherent voltage phases are not simulated.

There are 7,200 fixed-grid trial rows covering 100 backgrounds, nine EIRPs and all calibration scenarios. All per-integration estimates, binned profiles, individual temporal-window scores, calibration factors, actual injection checks and code are retained. A descriptive supplement exports fixed-coordinate temporal profiles for all thirteen original candidates using twenty local spectral controls each; it performs no new selection or source classification.

The six GBT and three ATA native inputs stay at their existing saved identities in inputs/observations.json and inputs/native-input-ledger.json. The compact evidence contains the plan, proof of its save before scoring, all small dependencies, code and results. The shared resume record retains earlier branches. This work does not finish the full upper-strip search, resolve the older Wow branch, or inspect Parkes source powers.

## Sources

- GBT paper, 22 December 2025 draft: https://ora.ox.ac.uk/objects/uuid%3Ac8eed7f9-1108-4db5-90cf-6e08cb9ba0dd/files/rk06989777 — SEFD definitions accompanying equation 1.
- ATA paper, 18 December 2025 draft: https://seti.berkeley.edu/atlas/ATA_3IAtlas.pdf — page 10, beamformer SEFD table and derivation. Source version is explicit; the model does not silently substitute later revised values.
- Public programme/data description: https://seti.berkeley.edu/atlas/
- The saved JPL observer responses, original ATA request and original native source metadata accompany the evidence. The original GBT velocity-response request file was not recovered; its response header records the target, site, dates, cadence and units.
