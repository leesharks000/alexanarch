# RESULTS-P3W-C: validation failed; the run stopped before the data

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
