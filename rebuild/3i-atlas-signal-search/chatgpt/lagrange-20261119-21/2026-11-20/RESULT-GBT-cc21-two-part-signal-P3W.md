# GBT cc21, the two-part signal that resolves only with a third (P3W to P3W-D): the fourth validation accepted; one candidate, ON0017, fails the location rule; no lead

**2026-11-21.** The author's question: a tripartite tone that looks like noise until its third is added. Two components whose phases wander together, so that their sum or difference phase stays fixed, are noise to every earlier test of the search; a steady third at the sum or difference frequency would lock the triple. The test is the phase stability of the pair across segments, on C21's first 32 frames (saved by N1625). Four plans were frozen. The first three stopped at their own validations; the fourth was accepted, and the six scans were read against its gates.

Canonical runs, frozen plans, code, hashes: [PLAN-P3W.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/PLAN-P3W.md), [RESULTS-P3W.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/RESULTS-P3W.md), [P3W-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/P3W-PRODUCTS.sha256), [p3w.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/p3w.py); [PLAN-P3W-B.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/PLAN-P3W-B.md), [RESULTS-P3W-B.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/RESULTS-P3W-B.md), [P3W-B-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/P3W-B-PRODUCTS.sha256), [p3wb.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/p3wb.py).

P3W-C: [PLAN-P3W-C.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/PLAN-P3W-C.md), [RESULTS-P3W-C.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/RESULTS-P3W-C.md), [P3W-C-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/P3W-C-PRODUCTS.sha256), [p3wc.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/p3wc.py), [diagC.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/diagC.py).

P3W-D: [PLAN-P3W-D.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/PLAN-P3W-D.md), [RESULTS-P3W-D.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/RESULTS-P3W-D.md), [P3W-D-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/P3W-D-PRODUCTS.sha256), [p3wd.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/p3wd.py).

The text below is RESULTS-P3W-D, then RESULTS-P3W, RESULTS-P3W-B and RESULTS-P3W-C, as committed there.

---

Run 2026-11-21 under PLAN-P3W-D (sha256 b9f5e852…), with p3wd.py (sha256 b0340dc8…) over p3w.py; both hashes checked after the run (FROZEN-P3W-D.sha256). Validation 1,257 s (validationD.json); then the six scans (p3wd_00NN.json) and the reading against the gates (p3wd_gates.json).

## Validation: accepted

| form | 0.25 | 0.5 |
|---|---|---|
| sum within X | p 0.125 | **p 0.025, pair 137–301, 3.14×** |
| difference within X | p 0.10 | **p 0.025, pair 137–301, 3.26×** |
| sum across feeds | p 0.275 | **p 0.025, pair 137–301, 2.73×** |
| difference across feeds | p 0.25 | **p 0.025, pair 137–301, 2.97×** |

| criterion | rule | result | |
|---|---|---|---|
| four forms at 0.5 | each p ≤ 0.05 at the injected pair | all four | met |
| noise only | ≤ 12 of 120 family tests at p ≤ 0.05 | 7 of 120 | met |
| one stationary tone, 5 runs | ≤ 3 of 30 | 2 of 30 | met |
| five tones, same fractional bin, 5 runs | ≤ 3 of 30 | 0 of 30 | met |
| five tones, mixed fractional bins, 5 runs | ≤ 3 of 30 | 0 of 30 | met |
| uncoupled pair at 0.5, 5 runs | ≤ 3 of 30 | 1 of 30 | met |
| burst (reported) | — | X+ 0.05, X− 0.025; the rest 0.1–0.725 | reported |

The steady-tone controls that failed P3W-B and P3W-C are clean without the seam: 2 of 90 tests at p ≤ 0.05 across the three, under the 5% an exact null gives. The burst flags within X, as the plan said it would by construction. 0.25 is not reached by any form in this run (P3W-C reached it once); sensitivity stands at 0.5.

## Reading

1. **One candidate.** Of the 18 ON-scan families on the target slice, one reaches p ≤ 0.05: **ON0017, Y+ (sum form within feed Y), pair 217–293, p 0.05**, score 0.0654 against a surrogate-maximum median of 0.0581 (1.12×) and a surrogate median at the pair of 0.0132. About 0.9 such candidates are expected by chance.
2. **Holdout in time: passed.** Each half of the scan gives the pair on its own: A 0.052, analytic p 0.0038; A 0.056, p 0.0016 (gate ≤ 0.01).
3. **Location: failed.** At the same pair and family, neither adjacent OFF scan stands above its own surrogate maximum (OFF0016 A 0.0078, below its median; OFF0018 A 0.0261 against a maximum of 0.0328). But OFF0018 holds an excess of 0.0138 over its surrogate median, and the ON excess is 0.0522, a ratio of **3.77, under the plan's 4**. The pair's coupling stands in the following OFF pointing at about a quarter of its ON strength.
4. **Control slices quiet at the pair** (ctrl25k A 0.0287 against a maximum of 0.0317; hidrift 0.0100 against 0.0301).
5. **The aggregate is chance.** Across all 108 family tests (6 scans × 3 slices × 6 families), 8 reach p ≤ 0.05 against about 5.4 expected; the chance of 8 or more is 0.17. Five are in ON scans and three in OFF. On the target slice: ON0017 Y+, OFF0016 X−, OFF0018 X+.

**Verdict under the plan: no lead.** The candidate fails gate 3, and no aggregate family test stands out. It is the first candidate the P3W line has produced, and it holds in both halves of the scan; what keeps it from being a lead is that the following OFF pointing carries the same coupling at a quarter of its strength, and a coupling present off the comet is not at the comet.

## What this run establishes

- The two-part signal, in either form, within either feed or across them, at a per-bin amplitude ratio of 0.5 (each component a quarter of its bin's noise power, invisible in power), is absent from C21's first 32 frames in all six scans and three slices, except for ON0017's pair 217–293, which the location test sets aside.
- Steady carriers no longer bias the test.
- Limits as PLAN-P3W gives them: couplings constant over the 32 frames only (a Doppler-drifting third is outside), segments of 512, C21 only.

Products: PLAN-P3W-D.md, p3wd.py, FROZEN-P3W-D.sha256, validationD.json, p3wd_0013–0018.json, p3wd_gates.json and this file, hashed in P3W-D-PRODUCTS.sha256. valD.log, scanD.log and readD.log are the run's console logs and are not hashed.

---


Run 2026-11-21 under PLAN-P3W (sha256 bd3d128b…). The plan's rule: "If not accepted, the run stops at validation." It was not accepted, and no telescope data were read (validation.json).

## Validation

| form | 0.1 | 0.25 | 0.5 |
|---|---|---|---|
| sum within X | p 0.475 | p 0.90 | **p 0.025, pair 137–301, 3.07×** |
| difference within X | p 0.275 | p 0.85 | **p 0.025, pair 137–301, 3.09×** |
| sum across feeds | p 0.325 | p 0.825 | **p 0.025, pair 137–301, 3.00×** |
| difference across feeds | p 0.025, wrong pair | p 0.85 | **p 0.025, pair 137–301, 3.02×** |

Amplitudes are the tone's per-bin amplitude over the noise's. "×" is the score over the median surrogate maximum.

- Noise-only: 6 of 20 trials have some family at p ≤ 0.05 (XY+ 3, XY− 2, Y+ 1). That is 6 of 120 family tests, 5% per family.
- Stationary tone: X− p = 0.025; the other families 0.125–0.925.
- Uncoupled pair: no family at p ≤ 0.05 (0.10–0.90).

## Why it failed

1. **Sensitivity is at 0.5, not 0.25.** For a coupled pair at per-bin amplitude ratio a, the expected coupling is about (√π/2 · a)²: about 0.05 at 0.25. The noise maximum over about 130,000 allowed pairs and 4,096 segments is about √(ln(2.6×10⁵)/4,096) ≈ 0.055. At 0.5 the coupling is about 0.20, well clear. The plan's bar was set below what this length of data can reach. At 0.5 each tone carries a quarter of its bin's noise power: invisible in power, below the tonal mask.
2. **The false-alarm bar was per trial; it should have been per family.** With six families, about 26% of noise trials show one family at p ≤ 0.05 by chance. The observed per-family rate, 5%, is nominal.
3. **Steady tones leak into the difference form.** A stationary tone's leakage reaches many bins, each with the tone's own phase advance per segment. Their difference phases are therefore locked, and the 2× power mask does not catch sidelobes below it. In a band with carriers, the difference families would fire on interference.

## What a second plan would change

Frozen before any data, if the author gives the word:
- **Acceptance at 0.5:** the validated sensitivity.
- **False alarms per family:** at most 10%.
- **Sidelobe exclusion:** bins with a steady phase advance of their own excluded. That is any bin whose self-coherence |mean P[s+1,k]·conj(P[s,k])| is significant, at analytic p ≤ 10⁻³, which removes tone leakage wherever it reaches.
- **Validation repeated** with the stationary tone, a set of tones, and the coupled pair at 0.5.

---


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

---


Run 2026-11-21 under PLAN-P3W-C (sha256 12a06e36…), with p3wc.py (sha256 ad865051…) over p3w.py; both hashes checked after the run (FROZEN-P3W-C.sha256). The plan's rule: "If not accepted, the run stops at validation." It was not accepted, and no telescope data were read (validationC.json; 1,123 s).

## Validation

| form | 0.25 | 0.5 |
|---|---|---|
| sum within X | p 0.75 | **p 0.025, pair 137–301, 3.03×** |
| difference within X | p 0.025, pair 137–301, 1.11× | **p 0.025, pair 137–301, 3.48×** |
| sum across feeds | p 0.175 | **p 0.025, pair 137–301, 3.33×** |
| difference across feeds | p 0.725 | **p 0.025, pair 137–301, 3.06×** |

| criterion | rule | result | |
|---|---|---|---|
| four forms at 0.5 | each p ≤ 0.05 at the injected pair | all four, p 0.025 at 137–301 | met |
| noise only | ≤ 12 of 120 family tests at p ≤ 0.05 | 8 of 120 | met |
| one stationary tone | no family at p ≤ 0.05 | X− 0.05; the rest 0.225–1.0 | **not met** |
| five tones, same fractional bin | no family at p ≤ 0.05 | X− 0.05; the rest 0.25–0.975 | **not met** |
| five tones, mixed fractional bins | no family at p ≤ 0.05 | X+ 0.05, X− 0.05; the rest 0.1–0.975 | **not met** |
| uncoupled pair at 0.5 | no family at p ≤ 0.05 | 0.40–0.65 | met |
| burst (reported) | — | X− 0.025, XY+ 0.05; the rest 0.075–0.525 | reported |

The flags are at the margin (p 0.05 is the real score exceeding all but one of 39 surrogates), and all four are in the X families, the feed that carries the tones. The Y families, which carry no tone, flag in none of the controls.

## Why it failed

1. **The circular shift leaves a seam.** A steady tone's segment phasors rotate at a fixed rate. Shifting a bin's sequence circularly by L wraps its end round to its start, so the shifted sequence carries two constant offsets, before and after the seam, differing by the tone's total advance over the scan. For two bins whose difference (or sum) phase is locked, the segments between their two seams carry a different relative offset from the rest. Every surrogate's lock at such a pair is therefore a little weaker than the real one, and the real score stands above the null. The bias acts only on locked pairs, so it acts only where steady tones are.
2. **Checked after the failure, on synthetic data only (diagC.py, diagC.json; not frozen).** On three fresh realizations each of the two five-tone controls, the circular shift as frozen gave X− at p ≤ 0.05 in 5 of 6. A shift without wraparound (each bin read from its own offset, 0–512 segments, the real statistic on the same 3,584 segments) gave no family at p ≤ 0.05 in any of the 24 tests (X± and Y±), with X− at 0.225–1.0. The seam accounts for the flags.
3. **The sum flag on the mixed tones fits the same mechanism.** Of the mixed fractional bins, 0.11 + 0.90 and 0.37 + 0.68 are within 0.05 of a whole bin, so those pairs' sum phases nearly lock, as same-fraction pairs' difference phases do.
4. **The control rule was too strict to pass by chance.** "No family at p ≤ 0.05 in any control" over 4 controls × 6 families is 24 tests; with an exact null each reaches p ≤ 0.05 with probability 0.05, and all 24 stay clear with probability 0.95²⁴ ≈ 0.29. PLAN-P3W-B's three controls (18 tests) had the same fault (0.95¹⁸ ≈ 0.40). P3W-B's failure was systematic nonetheless: three difference families flagged at once on the five-tone control, and its construction explains them (RESULTS-P3W-B).

## What stands

- The shift null does what it was built to do for the searched-for signal: all four forms recovered at 0.5 and the difference form within X at 0.25; noise-only false alarms 8 of 120, near nominal (about 7%).
- The bias is in the wraparound, not in shifting: without the seam the steady tones fall inside the null.
- No telescope data were read under PLAN-P3W, PLAN-P3W-B or PLAN-P3W-C.

## What a fourth plan would change

Frozen before any data, if the author gives the word:
- **The shift without wraparound**: each bin's segment sequence read from its own random offset, 0–512 segments, and the real statistic computed on the same 3,584 segments (a sensitivity cost of about √(3584/4096) ≈ 0.94).
- **Controls judged as noise is judged**: five realizations of each control, and at most 10% of each control's family tests at p ≤ 0.05.
- Everything else as PLAN-P3W-C.

Products: PLAN-P3W-C.md, p3wc.py, FROZEN-P3W-C.sha256, validationC.json, diagC.py, diagC.json and this file, hashed in P3W-C-PRODUCTS.sha256. valC.log is the run's console log and is not hashed.
