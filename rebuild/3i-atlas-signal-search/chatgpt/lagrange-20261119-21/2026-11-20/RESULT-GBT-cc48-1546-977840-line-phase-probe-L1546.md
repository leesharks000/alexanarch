# GBT cc48, 1546.977840 MHz line-centred phase probe: no lead; the magnitude-preserving null cannot see periodic structure

**2026-11-20.** Executed on the public GBT voltages from [PLAN-1546-977840-line-phase-injection-validated.md](PLAN-1546-977840-line-phase-injection-validated.md), after [STATUS-1546-977840-phase-probe-execution.md](STATUS-1546-977840-phase-probe-execution.md). line_phase_probe.py is not in this repository, so the run is an independent implementation of the plan's text, with a second frame window (401–416, the line's strongest in ON0017 by C4850) declared before the run.

Canonical run, frozen plan, code, hashes: [PLAN-L1546.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/L1546/PLAN-L1546.md), [RESULTS-L1546.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/L1546/RESULTS-L1546.md), [L1546-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/L1546/L1546-PRODUCTS.sha256), [l1546.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/L1546/l1546.py).

The text below is RESULTS-L1546 as committed there.


Run 2026-11-20 under PLAN-L1546 (sha256 87476462…, with amendment 1, recorded before any voltage), an independent implementation of ChatGPT's frozen plan (Lagrange Observatory, PLAN-1546-977840-line-phase-injection-validated.md, sha256 a15946fd…). GBT 3I/ATLAS scans 0013–0018, coarse channel 48, 8,192 bins centred on 1546.977840 MHz and a control 8 kHz above, both feeds, 39 magnitude-preserving surrogates. Set A is the plan's first 16 frames of each scan. Set B is frames 401–416, declared before the run as the window where C4850 found the line strongest in ON0017. Products and hashes in L1546-PRODUCTS.sha256.

## Reading

1. **No lead.** Set A gives one candidate: ON0017 Y, lag 128, family p = 0.025, score 2.68. The +8 kHz control does not fire (p = 0.275). At lag 128 the two halves of ON0017 give p = 0.175 and 0.025, so the candidate fails the held-half rule. At that lag the OFF scans stand at ratios 0.32–0.65 of their surrogate medians. Set B, the line's strongest frames, gives no candidate in either feed (ON0017 p = 0.525 X, 0.30 Y).
2. **Across the 24 family tests on the line** (6 scans × 2 feeds × 2 sets), one reaches p ≤ 0.05: the Set A candidate above. About 1.2 are expected by chance. Of the 24 control tests, one does (ON0013 Y, Set A, p = 0.05).
3. **What the test can see.** The frozen self-test fails in this implementation. A repeated period-256 code at 0.65 of the noise rms raises the phase-increment memory at lag 256 to 59.3 ×10⁻³ against 6.1 for noise. But its magnitude-preserving surrogates reach 47.6, because a periodic code is a line spectrum, and its period is carried by the very magnitudes the null keeps (amendment 1). The family test therefore sees only phase dependence beyond what the power spectrum implies, and is blind to periodic structure. ChatGPT reports p = 0.025 for its own self-test. This run does not reproduce that, and the difference is not resolved.
4. **The raw comparison (amendment 1).** In every scan, feed and set, the raw phase-increment memory at the line lies at 0.3–6.4 ×10⁻³ at every lag, as at the +8 kHz control (0.2–5.7). ON0017 stands no higher than the OFF scans. A repeated code carrying 0.65 of the slice's noise power would give about 59. So no such code is present in these 22.9 kHz at that level, in either set. This bounds only strong coded signals spread over the slice. The observed line holds a few bins of 8,192, and a carrier at its strength is far below what this comparison can register.

## Family results

| set | scan | role | feed | line p | lag | score | +8 kHz p |
|---|---|---|---|---:|---:|---:|---:|
| A | 0013 | ON | X / Y | 0.40 / 0.925 | 256 / 512 | 1.80 / 1.06 | 0.175 / 0.05 |
| A | 0014 | OFF | X / Y | 0.75 / 1.00 | 128 / 256 | 1.52 / 0.74 | 0.475 / 0.60 |
| A | 0015 | ON | X / Y | 0.85 / 1.00 | 128 / 512 | 1.44 / 0.84 | 0.95 / 0.15 |
| A | 0016 | OFF | X / Y | 0.90 / 0.25 | 128 / 64 | 1.05 / 1.94 | 0.45 / 0.35 |
| A | 0017 | ON | X / Y | 0.225 / **0.025** | 32 / 128 | 2.20 / 2.68 | 0.475 / 0.275 |
| A | 0018 | OFF | X / Y | 0.175 / 0.075 | 128 / 512 | 1.95 / 2.46 | 0.425 / 0.40 |
| B | 0013 | ON | X / Y | 0.30 / 0.125 | 512 / 32 | 2.32 / 2.36 | 0.575 / 0.70 |
| B | 0014 | OFF | X / Y | 0.075 / 0.85 | 64 / 256 | 2.60 / 1.29 | 0.15 / 0.45 |
| B | 0015 | ON | X / Y | 0.325 / 0.625 | 64 / 256 | 1.99 / 1.51 | 0.70 / 0.275 |
| B | 0016 | OFF | X / Y | 0.70 / 0.50 | 256 / 32 | 1.50 / 1.56 | 0.425 / 0.525 |
| B | 0017 | ON | X / Y | 0.525 / 0.30 | 128 / 32 | 1.65 / 1.95 | 0.325 / 0.45 |
| B | 0018 | OFF | X / Y | 0.50 / 0.925 | 512 / 256 | 1.80 / 1.22 | 0.825 / 0.625 |

## Limits

1. A pilot: 16 frames a set, 39 surrogates, p floor 0.025; trials across scans, feeds, sets and controls are not corrected.
2. The family test cannot see periodic structure (reading 3). The raw comparison sees only strong coded signals (reading 4).
3. The line itself, C4850's open item, stays where C4850 left it: a faint, bursty, partly polarized line in ON0017, with OFF power below about a quarter of its ON power, not resolved. Its time structure at full resolution, which C4850's saved spectra allow, remains the next reading.
