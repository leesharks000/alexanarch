# RESULTS-P3W: validation failed; the run stopped before the data

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
