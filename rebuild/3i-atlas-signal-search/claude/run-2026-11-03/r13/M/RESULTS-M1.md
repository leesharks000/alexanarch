# RESULTS-M stage 1: single-pass leads by drift tuning

Run 2026-11-18 under PLAN-M (PLAN-M.sha256, frozen before the run) on r13 part J's V2 products. Leads are in M1.json.

## Counts

| Scan | Role | Comet-tuned leads | Pseudo-target mean | Pseudo max | p (of 41) |
|---|---|---|---|---|---|
| 0013 | ON | 30 | 22.3 | 48 | 0.073 |
| 0014 | OFF | 34 | 27.2 | 47 | 0.122 |
| 0015 | ON | 32 | 24.0 | 58 | 0.098 |
| 0016 | OFF | 31 | 23.5 | 34 | 0.122 |
| 0017 | ON | 25 | 21.9 | 34 | 0.244 |
| 0018 | OFF | 35 | 22.5 | 43 | 0.049 |

The OFF passes, which point away from the comet, give as many comet-tuned leads (31–35) as the ON passes (25–32). Across all six scans the comet frame gives slightly more leads than the average pseudo-target, but no more than the false drifts' range. **No pass has more comet-tuned structure than chance and the OFF control give.**

## The strongest leads are one receiver-frequency complex

dm.py's bin convention puts frequency at FC − (bin − N/2)·Δ.

- **The C02 complex.** The leading comet-tuned feature in five of six scans is bins 1017145–1017153: 1665.6152 MHz topocentric, rest 1665.6046 MHz, within 9 Hz of C02. Its comet z is 58.9 in ON0013, 18.4 in ON0015 and 16.3 in ON0017, but also 8.8 in OFF0016 and 7.2 in OFF0018. It is the receiver-frequency line complex near 1665.615 MHz that the ChatGPT voltage report resolves (external/chatgpt-20261118) and r13 holds as interference.
- **Two more, the same way.** Bins near 1024957 (1665.593 MHz) and 968835 (1665.750 MHz) recur in ON and OFF passes alike.
- **Why they tune near the comet.** Their tuning peaks near the comet's drift, so drift alone does not single out the comet. That this complex drifts at a comet-like rate is itself a property to record: a moving filter crossing several fixed lines, as the ChatGPT report describes, can mimic it. The OFF control catches it.

## Reading

Stage 1 produces no lead that stands out against its controls. The screen does what it should, and finds the brightest comet-like structure in the channel first. That structure is the known interference, and the OFF passes show it as such. Under the author's method a standing-out lead would set the next look. None does in coarse channel 7, so the next look is the screen itself, run on coarse channels not yet read.
