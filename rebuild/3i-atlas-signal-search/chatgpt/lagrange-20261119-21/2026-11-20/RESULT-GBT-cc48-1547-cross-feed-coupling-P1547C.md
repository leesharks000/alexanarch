# GBT cc48, 1547.72 MHz, cross-feed coupling: nothing in the closure; the lag-0 coupling stands in the OFF scans; no lead

**2026-11-20.** The third of the 1547.72 MHz phase pilots, after [P1547](RESULT-GBT-cc48-1547-phase-pilot-P1547.md) and [P1547B](RESULT-GBT-cc48-1547-phase-pilot-lines-kept-P1547B.md): signal that resolves only in the coupling of the two feeds, X at one frequency in phase relation with Y at another, against a null that keeps each feed's spectrum and each bin's X–Y relation.

Canonical run, frozen plan, code, hashes: [PLAN-P1547C.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/PLAN-P1547C.md), [RESULTS-P1547C.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/RESULTS-P1547C.md), [P1547C-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/P1547C-PRODUCTS.sha256), [p1547c.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P1547/p1547c.py).

The text below is RESULTS-P1547C as committed there.


Run 2026-11-20 under PLAN-P1547C (sha256 504b6b21…, frozen at the author's word, 20:08). GBT 3I/ATLAS scans 0013–0018, coarse channel 48, the first 16 frames, 65,536 bins centred at 1547.720 MHz, each feed normalized by its 1,025-bin running median (P1547B), against 19 shared-rotation surrogates: one random phase per bin applied to both feeds, which keeps each feed's spectrum and each bin's X–Y relation and destroys every relation across bins. Products and hashes in P1547C-PRODUCTS.sha256.

## Reading

1. **Cross-feed closure: nothing.** No scan reaches the family test: ON0015 p = 0.75, and across all six scans p = 0.25–0.75, real scores 0.96–1.08 times the median surrogate maximum. A coupling of X at one frequency to Y at another, in phase across the 2,048 segments of a scan, is absent at this frequency in these frames down to the validated level (a coupled signal at 0.1 of the noise rms gave 7.1× the surrogate maximum).
2. **Cross-feed phase memory: no lead.** ON0015 gives a candidate at lag 2 (27.4 ×10⁻⁴ against a surrogate median of 6.9 and maximum of 23.4; p = 0.05), the lag of P1547B's within-feed candidate in the same scan. ON0017 does not reproduce it (1.5, below every surrogate). The confirmation gate fails.
3. **The lag-0 coupling is in the OFF scans.** At lag 0, the instantaneous coupling of the two feeds' phase increments, three scans stand above all their surrogates: ON0015 (26.1), OFF0016 (27.3) and OFF0018 (27.3), against surrogate medians of 8.2–9.3. ON0017 does not (11.2). A coupling as strong in two OFF pointings as in an ON is not at the comet. It is a relation across bins between the feeds that both feeds receive, or that the receiver chain makes; this run does not separate the two.
4. **The ON0015 phase relation, both runs.** P1547B found phase memory at lag 2 within each feed in ON0015; this run finds it between the feeds at lag 2, and between them at lag 0, in the same scan. Whatever carries it reaches both feeds together. It is not reproduced in ON0017, and at lag 0 the same coupling stands in OFF0016 and OFF0018.

## Validation (before the data, synthC.json)

A coupled signal built to be invisible to every earlier test (within each feed, tone phases that jump at random every segment; X and Y on different bins; the cross-feed closure fixed at zero):

| amplitude (of noise rms) | cross closure | cross memory | P1547B within-feed closure, X / Y |
|---:|---|---|---|
| 0 | p 0.95, 0.91× | p 0.20 | p 0.55 / 0.45 |
| 0.1 | **p 0.05, 7.1×**, injected quartet | p 0.55 | p 0.65 / 0.35 |
| 0.25 | **p 0.05, 18.3×**, injected quartet | p 1.00 | p 1.00 / 0.90 |
| 0.5 | **p 0.05, 20.5×**, injected quartet | p 0.25 | p 0.80 / 0.05 |
| 1.0 | **p 0.05, 19.0×**, injected quartet | p 0.05 | p 0.30 / 0.85 |

The cross-feed closure is accepted; the within-feed tests do not see the signal (one p = 0.05 in eight, at chance), which is the case the plan was made for. The cross-feed memory filter had no designed injection and is read as exploratory.

## Family scores

| scan | role | cross memory p | lag | score/surr. max | cross closure p | quartet | score/surr. max |
|---|---|---:|---:|---:|---:|---:|---:|
| 0013 | ON | 0.35 | 64 | 1.08 | 0.30 | 104 | 1.08 |
| 0014 | OFF | 0.30 | 16 | 1.13 | 0.70 | 44 | 0.96 |
| 0015 | ON | 0.05 | 2 | 1.48 | 0.75 | 120 | 0.97 |
| 0016 | OFF | 0.05 | 0 | 1.45 | 0.25 | 124 | 1.04 |
| 0017 | ON | 0.95 | −512 | 0.78 | 0.55 | 5 | 0.98 |
| 0018 | OFF | 0.10 | 0 | 1.45 | 0.50 | 70 | 1.03 |

## Cross-feed phase memory at lags 0 and 2 (×10⁻⁴)

| scan | role | lag 0 real | surr. median | surr. max | lag 2 real | surr. median | surr. max |
|---|---|---:|---:|---:|---:|---:|---:|
| 0013 | ON | 5.8 | 6.9 | 14.6 | 6.6 | 5.9 | 20.1 |
| 0014 | OFF | 15.1 | 9.4 | 20.7 | 13.2 | 5.1 | 16.3 |
| 0015 | ON | 26.1 | 8.2 | 19.6 | 27.4 | 6.9 | 23.4 |
| 0016 | OFF | 27.3 | 9.1 | 18.4 | 12.4 | 8.7 | 22.0 |
| 0017 | ON | 11.2 | 9.3 | 22.5 | 1.5 | 8.1 | 22.1 |
| 0018 | OFF | 27.3 | 9.3 | 20.2 | 6.9 | 10.4 | 21.8 |

## Limits

1. A pilot: 16 frames and 19 surrogates; 12 tests, about 0.6 at p = 0.05 by chance (three reached it).
2. The coupling closure tested is of the form X_k Y_l X*_m Y*_n with k + l = m + n over 128 frozen quartets of 512-sample segments; other coupling forms (other quartet sets, X_k X_l Y*_m Y*_n, longer segments) are not tested.
3. Whether the lag-0 cross-feed coupling is the sky's or the receiver's is not established; the OFF scans place it away from the comet either way.
