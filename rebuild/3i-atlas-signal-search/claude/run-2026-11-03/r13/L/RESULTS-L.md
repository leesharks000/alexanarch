# RESULTS-L: the return (r13 part L)

Run 2026-11-18 under PLAN-L (PLAN-L.sha256, frozen 22:19:40Z before any L statistic was computed), on r13 part J's saved products; no new data read. Statistics in L.json.

**Gate.** J1, m = 1, V0, comet frame: 11. Passed.

**Result: neither statistic counts.**

| Statistic | Variant | Comet frame | False-frame mean ± sd | p99 | max | p (of 401) | Nearest 40 |
|---|---|---|---|---|---|---|---|
| L1, absent middle | V0 | 10 | 8.84 ± 3.17 | 18.0 | 21 | 0.35 | 0.61 |
| L1, absent middle | V2 | 9 | 8.72 ± 3.08 | 17.0 | 18 | 0.50 | 0.68 |
| L2, displaced middle | V0 | 10 | 8.78 ± 3.18 | 18.0 | 21 | 0.34 | 0.61 |
| L2, displaced middle | V2 | 9 | 8.67 ± 3.08 | 17.0 | 18 | 0.50 | 0.68 |

- **L1.** Comet-frame positions strong in ON0013 and ON0017, absent from ON0015 and from every OFF scan, number 9–10 clusters, about what any false drift gives (8.7–8.8 on average). The comet frame is not preferred.
- **L2 adds nothing.** Almost every L1 position finds some ON0015 position 5–2,000 bins away, in false frames as in the comet frame, so L2 equals L1 less a few. The plan named this risk; at single-scan z ≥ 3 a window that wide cannot discriminate. A displaced return would need a stated displacement, or a stronger per-scan threshold, to be tested.
- **Positions.** The comet frame's L1 positions, registered, are in L.json. Several recur in both variants (74617, 83831, 131649–50, 196919, 483120–21, 707375–76, 773258–60). Recurrence across variants is expected, because V2 only drops rows. They are recorded, not read.

**What this rules out, at its sensitivity.** In coarse channel 7, there is no comet-tracking tone, steady within each look, that appears in the first and third ON scans and is absent from the second beyond what false drifts produce. This is a single-scan z ≥ 3 in the 49-integration stack. Weaker returns, returns displaced by a stated amount, returns that switch within a look (part K's object), and other coarse channels are untested.
