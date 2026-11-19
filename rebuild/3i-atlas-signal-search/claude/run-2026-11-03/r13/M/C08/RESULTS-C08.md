# RESULTS-C08: the cc08 lead does not survive

Plan: PLAN-C08.md, frozen 2026-11-19T14:06:34Z (PLAN-C08.sha256). Products: z.json and v_0013.npz … v_0018.npz. Restacks: out2/cc08_*.npz from the frozen mv.py.

## 1. Uncapped z at the two predictions (z.json)

The comet prediction moves 13 bins per scan; the fixed prediction is bin 787546 throughout. In ON0013 the two coincide. "False frames" is how many of the 100 false-motion stacks reach the same z in the same ±5-bin window.

| Scan | Role | Comet: max z | False frames reaching it | Fixed: max z | False frames reaching it |
|---|---|---:|---:|---:|---:|
| 0013 | ON | 7.25 | 2 | 7.25 | 2 |
| 0014 | OFF | < 2 | – | < 2 | – |
| 0015 | ON | 2.15 (offset −4) | 3 | < 2 | – |
| 0016 | OFF | < 2 | – | < 2 | – |
| 0017 | ON | 2.69 (offset +1) | 7 | 2.13 (offset −4) | 1 |
| 0018 | OFF | < 2 | – | < 2 | – |

1. In ON0013 the excess is broad: z ≥ 4 across offsets −5 to +2, about 20 Hz. At this one window, 2 of 100 false-motion stacks reach the same z.
2. ON0015 has nothing at the comet prediction above noise. ON0017 has z 2.7 there, a level 7 of 100 false stacks reach in the same window.
3. All three OFF scans are below z 2 at both predictions.

## 2. The voltages (v_*.npz)

Per frame: power in the predicted bin ±2, divided by the band's median. For noise the expected value is 5/ln 2 = 7.21.

1. ON0013, comet track: mean 7.31 (feed X) and 7.28 (feed Y). Excluding the first integration, as M3 does, gives 7.31 and 7.29. Mean over the other scans and both tracks: 7.00–7.43. No scan stands out.
2. ON0013 mean spectrum over the 357.6 Hz band: 1.06 (X) and 0.97 (Y) of the median at the predicted bin. The largest bins anywhere in the band are 1.12 and 1.09, at other offsets. There is no line, no sidebands, and no excess at the predicted bin.
3. ON0013 over time, feed Y, in 30 s blocks: 7.82, 7.54, 7.36, 6.85, 6.92, 7.30, 6.83, 7.43, 7.40, 7.34. No block stands above noise.

## 3. Reading

The lead fails the frozen criterion: it is not at the comet prediction in two ON scans, and it does not appear in the voltages. The stack's z 7.25 in ON0013 is a broad excess that false-motion stacks also reach at that window, picked as a top-ten value from about a million bins. The 0.181 Hz W1 line was measured on that series. With no power above noise behind it, it is read as noise structure.

Recorded as found: the cc08 lead is closed.

## 4. Deviations

1. c08v.py's per-frame power keeps every frame. PLAN-C08 said "tracked in the comet frame as mvolt.py does", and mvolt.py drops each scan's OFF-row frames. The effect was computed for ON0013 (§2.1): 7.31/7.29 with the frames dropped, against 7.31/7.28 without.
2. The broad shape in ON0013 (offsets −5 to +2) could hide a source smeared by an unmodelled drift. Nothing in the voltages supports one. The limit is the plan's: this band shows narrow structure only.
