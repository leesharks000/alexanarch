# Repetition without a known code: completed experiment

**The search recovered some unknown repeated packets at 3% added filtered-background power. It has not produced a robust comet-associated signal.** Its first version failed interference challenges. One declared repair rejected all fresh synthetic negative challenges, but its only added-window nomination was strongly inflated by lag-range edge handling.

This is a method-development result from the 18 December 2025 UTC GBT observations, analyzed 18 November 2026. It should not be reported as a signal discovery or a blanket non-detection limit.

## What was done

We restored and hash-verified six phase-preserving two-feed voltage products, then searched complex-voltage self-similarity at delays of approximately 2–120 seconds. The detector was supplied no packet, preamble, symbol rate, carrier frequency or repetition period. It operated after the predicted comet Doppler correction, an 8 Hz low-pass filter and decimation to 44.70348 samples/s.

Frequency selection was frozen before calculating new waveform statistics: eleven legacy C03–C13 windows, twenty additional windows selected without the original brightness gate, forty threshold-setting windows, and forty reserved comparison windows. Every target also had eight local frequency comparisons. All observations had been used previously, so this was a new exploratory statistic on existing data. These are selected frequency comparisons, not independent astronomical observations.

## First version: sensitivity accompanied by failed controls

The primary raw ON-minus-OFF delayed-peak score recovered the true period or a harmonic at 3% added power in 12/12 random BPSK, 11/12 complex-packet and 3/12 intermittent-packet configurations. But at 30% added power it also nominated 6/12 nonrepeating controls, 12/12 pure-tone controls and 12/12 repeated signals present in both ON and OFF scans. Its absence of measured candidates does not rescue those failures. The primary version is retained in full as a failed candidate-selection method.

## One repair, checked with fresh waveform configurations

The secondary rule was explicitly declared after those failures and before its calculation. It normalized a peak by local lag-score variability and added requirements for a distinct ON peak and substantially weaker OFF prominence. Threshold-setting comparisons intentionally omitted the new gates, retaining conservative maxima. Detector rules and thresholds were not tuned again after the fresh checks.

Fresh test seeds 12–23 were separate from the original twelve configurations. They still used the same eleven selected measured backgrounds; new seeds do not supply independent astronomical data. At each power, twelve configurations were tested per waveform family.

| Added / filtered background power | Repeated BPSK: correct period | Repeated complex packet: correct period | Intermittent packet: correct period |
|---:|---:|---:|---:|
| 0 | 0/12 | 0/12 | 0/12 |
| 0.003 | 0/12 | 0/12 | 0/12 |
| 0.01 | 0/12 | 0/12 | 0/12 |
| 0.03 | 4/12 | 9/12 | 0/12 |
| 0.1 | 11/12 | 12/12 | 5/12 |
| 0.3 | 12/12 | 12/12 | 11/12 |
| 1 | 12/12 | 12/12 | 11/12 |

The repaired screen nominated **0/24 fresh nonrepeating controls, 0/24 fresh pure-tone controls, and 0/24 fresh equal-ON/OFF controls** at 30% added power. These finite configurations are useful implementation checks, not a calibrated global false-alarm probability. The packet families differ from the earlier modulation-screen benchmark, preventing a universal performance ranking. Recovered repetition periods are not recovered message contents.

Power fractions refer to the final filtered voltage stream, averaged over the statistical window including inactive periods. They are not published detection SNR, flux density, EIRP, or a demonstrated placement below the published inspected threshold. In the fresh configurations, no tested family was recovered at 0.3% or 1% added power. One original-seed intermittent configuration did recover at 1%; it did not generalize to the fresh cohort. The intermittent family remains especially incomplete, and recovery is not uniformly monotone with power under the screening heuristics.

## The actual-data flag and its boundary problem

The primary screen nominated zero legacy and zero expanded windows. The repaired screen nominated zero legacy windows and one of twenty expanded windows: `control-17000Hz`, rest frequency **1665.616776617 MHz**, at a delay of **119.811691861 seconds**. The threshold was 15.764629; its selected score was 24.474871.

Two of the forty reserved comparison windows also crossed the repaired cutoff, at delays 119.587996 and 2.236962 seconds. All three selected peaks lie near the searched-delay boundaries. Running medians and median absolute deviations with nearest-value padding can artificially lower a boundary's estimated variability. The reserved-window findings therefore materially limit an interpretation of the expanded-window flag.

We performed a declared fixed-peak sensitivity diagnostic: calculate the same autocorrelations with a larger delay context, approximately 0.0447–140 seconds, and evaluate only the three already selected delays. No new delays were nominated and the original flags were not erased.

| Window | Selected delay (s) | Original repaired score | Score with extended lag context |
|---|---:|---:|---:|
| control-17000Hz | 119.811692 | 24.475 | 4.971 |
| control+29000Hz | 119.587996 | 17.790 | 6.434 |
| control-42000Hz | 2.236962 | 16.342 | 3.775 |

The extended context changes the statistic near the boundaries, and the original cutoff is not recalibrated for that changed context. These numbers are a robustness diagnostic, not an independent validation test or a new calibrated rejection threshold. The strong score loss makes the flag unsuitable as robust evidence for a repeating comet source. The original delayed excess is still recorded. All four wrong-motion versions of this window, recomputed with the full secondary gates, fell below its original cutoff; that alone does not overcome the boundary sensitivity.

The repaired screen also produced three above-threshold wrong-motion scores before its new prominence gates; these are explicitly retained as unvetoed upper-bound checks. Only the sole observed nominee received the full wrong-motion gate recomputation. The forty reserved windows and the wrong-motion comparisons are not independent null trials or independently established interference sources.

## What to carry forward

There is demonstrated sensitivity to some repeated packets at 3% added filtered power without knowing their code. That gain is qualified by failed primary controls and a remaining boundary-handling problem. The next implementation must calculate sufficient lag context before taking running medians/MADs, freeze that implementation, and recalibrate all thresholds and recovery curves before new candidate selection. The present run does not silently substitute an improved boundary rule after observing its flags.

No bits or language were decoded from the measured observations. No claim of alien origin or a general absence of weak communication follows from these tests. No external messages or public deposits were made.

## Files and replay

- `REPORT.md`: complete primary experiment, thresholds, limits and recovery counts.
- `PLAN.md`, `SECONDARY-PLAN.md`, `BOUNDARY-DIAGNOSTIC.md`: ordered experiment definitions and changes.
- `results/`, `secondary/`, `diagnostic/`: all results, preserved failures, sufficient measured statistics, benchmark voltage backgrounds, recovery curves and fixed-peak diagnostic.
- `experiment.py`, `secondary.py`, `boundary_diagnostic.py`, `verify.py`: code. Primary and secondary benchmark/score replay uses the cached products in the bundle. Recomputing raw-derived feature products and the boundary diagnostic needs the six source voltage arrays named in `INPUTS.json`.
- `VALIDATION.json`: direct replay of selected original/fresh configurations, numerical and count checks. `source-verification.json`: hashes of the six restored source arrays. `freeze.json`: original selection and plan hashes.

The primary FFT autocorrelation matches independent direct complex sums; constant feed-phase invariance is tested. Three secondary configurations replay exactly, including scores and selected delays. All original and secondary trial denominators and constant-within-trial carrier assumptions were verified. This is reproducibility of an exploratory experiment, not an independent observation.
