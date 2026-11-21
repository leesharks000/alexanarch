# RESULTS-P3W-B: validation failed; the run stopped before the data

Run 2026-11-21 under PLAN-P3W-B (sha256 eca84bad…), with p3wb.py (sha256 019f17ed…) over p3w.py. The plan's rule: "If not accepted, the run stops at validation." It was not accepted, and no telescope data were read (validationB.json; 884 s).

## Validation

| form | 0.25 | 0.5 |
|---|---|---|
| sum within X | p 0.525, pair 282–341, 0.99× | **p 0.025, pair 137–301, 3.11× (recovered)** |
| difference within X | p 0.3, pair 11–370, 1.03× | **p 0.025, pair 137–301, 3.30× (recovered)** |
| sum across feeds | p 0.025, pair 137–301, 1.22× (recovered) | **p 0.025, pair 137–301, 3.13× (recovered)** |
| difference across feeds | p 0.85, pair 489–405, 0.96× | **p 0.025, pair 137–301, 3.11× (recovered)** |

Amplitudes are the tone's per-bin amplitude over the noise's. "×" is the score over the median surrogate maximum.

| criterion | rule | result | |
|---|---|---|---|
| four forms at 0.5 | each p ≤ 0.05 at the injected pair | all four, p 0.025 at 137–301 | met |
| noise only | ≤ 12 of 120 family tests at p ≤ 0.05 | 4 of 120 | met |
| stationary tone | no family at p ≤ 0.05 | X+ 0.45, X- 0.125, Y+ 0.75, Y- 0.775, XY+ 0.775, XY- 0.15 | met |
| five stationary tones | no family at p ≤ 0.05 | X+ 0.675, X- 0.025, Y+ 0.9, Y- 0.05, XY+ 0.75, XY- 0.05 | **not met** (X−, Y−, XY−) |
| uncoupled pair at 0.5 | no family at p ≤ 0.05 | X+ 0.4, X- 0.425, Y+ 0.7, Y- 0.4, XY+ 0.075, XY- 0.35 | met |

At 0.25 the sum across feeds was recovered (p 0.025, 1.2×); the other three were not. 0.25 is reported, not required.

## Why it failed

1. **The exclusion works for one tone and not for five.** The single stationary tone, which flagged the difference form under PLAN-P3W (X− p 0.025), no longer flags anything (lowest p 0.125). With five tones, all three difference families flag (X− 0.025, Y− 0.05, XY− 0.05), and no sum family does.
2. **Most likely mechanism, not tested here.** Each bin is tested for a steady phase advance on its own, at p ≤ 10⁻³. Far from a tone its leakage is weak, so its self-coherence stays under that bar and the bin is kept. The difference of two steady advances is itself steady, so pairs of such bins, one from each tone's leakage, have locked difference phases. The family statistic sums over many such pairs, so it can find a lock that no single-bin test can see. With one tone there are no cross-tone pairs, which fits the stationary control passing.
3. **What it means for the data.** The bands of this search carry steady carriers, among them the 1546.98 MHz line (C4850/READING-C4850-line-1546977840.md). Where more than one stands in a band, the difference families would fire on interference, which is what this control exists to catch.

## What stands

- The sum families pass every control, and they are recovered at 0.5 in both forms.
- Noise-only false alarms are within the bar (4 of 120, about 3% per family).
- No telescope data were read under PLAN-P3W or PLAN-P3W-B.

Products: PLAN-P3W-B.md, p3wb.py, validationB.json and this file, hashed in P3W-B-PRODUCTS.sha256. valB.log is the run's console log and is not hashed.
