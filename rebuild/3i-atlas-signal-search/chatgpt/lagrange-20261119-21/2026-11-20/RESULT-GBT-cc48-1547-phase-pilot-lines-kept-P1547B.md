# GBT cc48, 1547.72 MHz, phase pilot with the lines kept: an ON0015 lag-2 candidate that ON0017 does not reproduce; not a lead

**2026-11-20.** The follow-up to [RESULT-GBT-cc48-1547-phase-pilot-P1547.md](RESULT-GBT-cc48-1547-phase-pilot-P1547.md): the same test with each frame normalized by a smoothed magnitude instead of whitened, so line-spectrum signals stay in view, against magnitude-preserving surrogates.

Canonical run, frozen plan, code, hashes: [PLAN-P1547B.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/PLAN-P1547B.md), [RESULTS-P1547B.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/RESULTS-P1547B.md), [P1547B-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/P1547B-PRODUCTS.sha256), [p1547b.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/p1547b.py), diagnostic [p1547b_diag.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/p1547b_diag.py).

The text below is RESULTS-P1547B as committed there.


Run 2026-11-20 under PLAN-P1547B (sha256 e579474b…, frozen at the author's word, 20:00), the follow-up to RESULTS-P1547 limit 3. GBT 3I/ATLAS scans 0013–0018, coarse channel 48, the first 16 frames, both feeds, 65,536 bins centred at 1547.720 MHz, each frame divided by a 1,025-bin running median of its magnitude, against 19 magnitude-preserving phase surrogates. Products and hashes in P1547B-PRODUCTS.sha256.

## Reading

1. **No lead.** ON0015, the discovery scan, gives a candidate in both feeds on the same parameter: phase-increment memory at lag 2 (X 30.3, Y 34.1, in units of 10⁻⁴, against surrogate medians of 10.0 and 8.0 and maxima of 16.8 and 15.5; p = 0.05 in each). At that lag, without retuning, ON0017 does not reproduce it (X 4.5, Y 14.9, below or within its surrogates). The confirmation gate fails, so by the frozen rule it is not a lead.
2. **It is not tied to the pointing.** At lag 2 the next scan, OFF0016, carries X 18.8 against a surrogate median of 6.3 (one surrogate higher), and OFF0018 carries X 10.2 and Y 18.6 against medians of 6.5 and 7.9 (Y: one surrogate higher). The excess is strongest in ON0015; after it, two OFF scans stand above their surrogate medians while the ON scan between them does not. It follows no ON/OFF pattern.
3. **It is not a line.** Post-freeze diagnostic (p1547b_diag.py, diagB.json, outside the plan's gates): the slice holds no strong line in ON0015 (the strongest bins stand 3.4–3.6 times the local noise, at the level of the noise's own extremes); setting the ten strongest lines (±8 bins) to random phase leaves the lag-2 memory where it was (X 47 → 52, Y 46 → 40, per-frame medians ×10⁻⁴). Per frame, the values sit inside the surrogates' range (ON0015 X median 47 against one surrogate's 33, 90th percentile 55). The family excess comes from a lag-2 phase relation that holds the same sign across the 16 frames, broadband across the slice, in both feeds.
4. **Elsewhere.** Of the 24 family tests, four reach p = 0.05: the two ON0015 candidates, closure in ON0013 Y (quartet 125, 1.28×) and phase memory in OFF0018 Y (lag 512, 1.48×). About 1.2 are expected by chance.

## Validation (before the data, synthB.json)

Injections made before normalization, as a signal arrives:
- Four balanced tones: four-frequency closure reaches p = 0.05 at every amplitude tried, 0.1, 0.25, 0.5 and 1.0 of the noise rms (3.8–5.3× the surrogate maximum), each time at the injected quartet. The closure filter is accepted.
- A repeated QPSK sequence: phase-increment memory reaches p = 0.05 only at 1.0 of the noise rms (1.41×); at 0.5 it does not (p = 0.60). The memory filter does not meet the frozen criterion (p = 0.05 at 0.5 and above), and is read under that limit.
- Plain noise: neither filter.

## Family scores

| scan | role | feed | memory p | lag | score/surr. max | closure p | quartet | score/surr. max |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 0013 | ON | X | 0.30 | 8 | 1.12 | 0.40 | 22 | 1.04 |
| 0013 | ON | Y | 0.55 | 2 | 1.00 | 0.05 | 125 | 1.28 |
| 0014 | OFF | X | 0.40 | 256 | 1.04 | 0.35 | 46 | 1.03 |
| 0014 | OFF | Y | 0.20 | 256 | 1.16 | 0.40 | 95 | 1.03 |
| 0015 | ON | X | 0.05 | 2 | 2.07 | 0.25 | 59 | 1.06 |
| 0015 | ON | Y | 0.05 | 2 | 2.20 | 0.70 | 99 | 0.94 |
| 0016 | OFF | X | 0.25 | 2 | 1.23 | 0.75 | 59 | 0.94 |
| 0016 | OFF | Y | 0.20 | 4 | 1.13 | 0.85 | 21 | 0.90 |
| 0017 | ON | X | 0.70 | 32 | 0.87 | 0.60 | 87 | 0.96 |
| 0017 | ON | Y | 0.50 | 16 | 1.05 | 0.35 | 31 | 1.07 |
| 0018 | OFF | X | 0.10 | 256 | 1.42 | 0.90 | 100 | 0.88 |
| 0018 | OFF | Y | 0.05 | 512 | 1.48 | 1.00 | 40 | 0.81 |

## The lag-2 memory across the scans (×10⁻⁴)

| scan | role | X real | X surr. median | X surr. max | Y real | Y surr. median | Y surr. max |
|---|---|---:|---:|---:|---:|---:|---:|
| 0013 | ON | 2.7 | 8.2 | 14.5 | 16.6 | 9.9 | 19.4 |
| 0014 | OFF | 2.1 | 8.5 | 16.7 | 12.3 | 8.4 | 17.4 |
| 0015 | ON | 30.3 | 10.0 | 16.8 | 34.1 | 8.0 | 15.5 |
| 0016 | OFF | 18.8 | 6.3 | 21.2 | 8.3 | 9.8 | 20.8 |
| 0017 | ON | 4.5 | 9.4 | 15.8 | 14.9 | 10.1 | 22.4 |
| 0018 | OFF | 10.2 | 6.5 | 12.8 | 18.6 | 7.9 | 20.0 |

## Limits

1. A pilot: 16 frames (5.7 s) a scan and 19 surrogates. The ON0015 lag-2 relation is the one item worth the plan's scale-up (all 833 frames, 199 surrogates), which would show whether it lasts through the scan and whether it is the start of a fade through the six; that is a new plan.
2. The memory filter's sensitivity to a repeated code is low (validation); a negative from it is weak.
3. A lag-2 relation among phase increments is also what a slight non-whiteness of the instrument's response within the normalization window would make; the OFF scans share it in part, which is consistent with that and with a time-varying source alike. Its mechanism is not established.
