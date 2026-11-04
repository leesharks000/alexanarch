# RESULTS-lheld: the thirteen's property in fifteen held-out L-band channels (frozen test)

Plan: lheld/PLAN-lheld.md, sha256 e059db4e0b74828b…, frozen before any of these channels was read. Data: GBT blc23 and blc24, 2025-12-18, scans 0013–0018 (ON 0013, 0015, 0017), rawspec.0000 (2.794 Hz × 6.08 s), each coarse channel of index 7 mod 8 read over HTTP by lheld/fetch_cc.py; procedure lheld/cf.py (the S-band held-out procedure unchanged); runner lheld/run_lheld.py. Run 2026-11-04, resumed once at the background limit; each channel's result written before the next was read.

| channel | centre MHz | true ON | swap | false ON mean ± sd (40) | false max | false ON−swap max | fraction of false ≥ true | verdict |
|---|---:|---:|---:|---|---:|---:|---:|---|
| blc23_cc15 | 1643.555 | 1 | 3 | 3.2 ± 1.66 | 7 | 5 | 1.0 | BOUNDS |
| blc23_cc23 | 1620.117 | 153 | 555 | 135.47 ± 14.17 | 164 | -361 | 0.175 | BOUNDS |
| blc23_cc31 | 1596.680 | 7 | 7 | 4.65 ± 4.1 | 22 | 20 | 0.125 | BOUNDS |
| blc23_cc39 | 1573.242 | 259 | 196 | 135.85 ± 62.96 | 299 | 156 | 0.05 | BOUNDS |
| blc23_cc47 | 1549.805 | 18 | 44 | 16.05 ± 8.58 | 44 | 18 | 0.325 | BOUNDS |
| blc23_cc55 | 1526.367 | 5 | 25 | 24.75 ± 46.39 | 208 | 173 | 0.875 | BOUNDS |
| blc23_cc63 | 1502.930 | 4 | 5 | 2.98 ± 1.41 | 6 | 3 | 0.35 | BOUNDS |
| blc24_cc07 | 1479.492 | 1 | 42 | 2.92 ± 1.85 | 8 | -35 | 0.95 | BOUNDS |
| blc24_cc15 | 1456.055 | 4 | 3 | 3.92 ± 2.1 | 11 | 7 | 0.475 | BOUNDS |
| blc24_cc23 | 1432.617 | 6 | 4 | 3.55 ± 2.22 | 9 | 6 | 0.2 | BOUNDS |
| blc24_cc31 | 1409.180 | 0 | 2 | 3.4 ± 1.71 | 8 | 4 | 1.0 | BOUNDS |
| blc24_cc39 | 1385.742 | 4 | 5 | 3.7 ± 1.98 | 9 | 5 | 0.5 | BOUNDS |
| blc24_cc47 | 1362.305 | 5 | 3 | 2.83 ± 1.53 | 7 | 4 | 0.125 | BOUNDS |
| blc24_cc55 | 1338.867 | 3 | 4 | 3.12 ± 1.99 | 10 | 10 | 0.55 | BOUNDS |
| blc24_cc63 | 1315.430 | 5 | 4 | 3.23 ± 1.88 | 8 | 5 | 0.175 | BOUNDS |

Overall by the frozen rule: 0 of 15 channels replicate (3 or more needed for REPLICATES): **BOUNDS**.

Reading. In no held-out L-band channel of the same six scans does the true comet frame exceed every false frame, and in none does its ON−swap difference exceed every false frame's. The large counts sit in satellite downlink bands: 1620.1 MHz (Iridium, 1616–1626.5), 1573.2 MHz (the edge of GNSS L1), 1549.8 and 1526.4 MHz (Inmarsat), where the false frames are as large. The beam-sided comet-frame excess of coarse channel 7 (the thirteen) does not recur elsewhere in the cadence's L band. Every channel's true-frame candidate frequencies are in lheld.json.
