# Results: two-epoch match, Parkes 2025-07-31 against Green Bank 2025-12-18 (plan PLAN-epoch.md, sha256 1b3234fa…; run 2026-11-05)

Verdict: NO MATCH. No Green Bank comet-frame cluster in the primary set, and none of the thirteen, has a Parkes comet-frame candidate within 10 Hz of its rest frequency. The thirteen have no Parkes candidate within 50 Hz.

Inputs: 62,864 Parkes true-frame candidates (22 nodes); Green Bank clusters merged at 10 Hz: 1026 in all 64 surveyed channels, 295 in the primary set (channels with 50 or fewer true-frame clusters), 13 in coarse channel 7. Inside Parkes coverage: 858, 250 and 13. Dense channels set aside from the primary set: blc23_cc23, blc23_cc39, blc23_cc44, blc23_cc49, blc25_cc01.

| Set · tolerance | M (true) | Shift null, mean ± sd | Null max | p |
|---|---:|---:|---:|---:|
| primary · d 10 Hz | 0 | 0.185 ± 0.448 | 3 | 1.0 |
| primary · d 50 Hz | 1 | 0.792 ± 0.908 | 5 | 0.545 |
| all · d 10 Hz | 2 | 0.762 ± 0.917 | 5 | 0.17 |
| all · d 50 Hz | 5 | 3.765 ± 2.1 | 11 | 0.3325 |
| thirteen · d 10 Hz | 0 | 0.003 ± 0.05 | 1 | 1.0 |
| thirteen · d 50 Hz | 0 | 0.005 ± 0.1 | 2 | 1.0 |

The null is 400 rigid shifts of the Green Bank list (seed 5, 1–50 kHz either way). Decision rule: a lead needs p ≤ 0.01 in the primary set at 10 Hz, or for the thirteen at least one match at 10 Hz with p ≤ 0.01. Neither holds.

Every pair within 50 Hz (rest frequencies in MHz; Parkes scores are the six scans' robust z, S source, R reference):

| GBT channel | GBT f_rest | Parkes node | Parkes f_rest | Parkes − GBT (Hz) | Set | Parkes scores |
|---|---:|---|---:|---:|---|---|
| blc23_cc39 | 1574.495207 | blc06 | 1574.495165 | -42.0 | dense | S0 4.71 R1 1.09 S2 12.07 R3 -0.14 S4 3.08 R5 1.27 |
| blc23_cc39 | 1574.596106 | blc06 | 1574.596135 | +29.0 | dense | S0 5.98 R1 -0.48 S2 48.45 R3 -0.67 S4 2.9 R5 1.97 |
| blc23_cc55 | 1527.102024 | blc06 | 1527.102065 | +41.5 | primary | S0 3.78 R1 1.58 S2 4.17 R3 0.61 S4 3.62 R5 0.71 |
| blc23_cc44 | 1557.534879 | blc06 | 1557.534887 | +8.0 | dense | S0 4.02 R1 1.47 S2 4.18 R3 -1.57 S4 7.88 R5 -1.15 |
| blc23_cc44 | 1557.762370 | blc06 | 1557.762368 | -2.0 | dense | S0 3.38 R1 1.5 S2 3.01 R3 0.19 S4 9.02 R5 1.82 |

All five pairs lie in mobile-satellite and navigation-satellite allocations (1525–1559 and 1559–1610 MHz); the all-channel count at 10 Hz, 2, sits inside the shift null (p 0.17). Recorded here, read as nothing.

Scope and limits. The test reads stored candidates only: what Parkes found at its own gate (z ≥ 2.5 in all three source scans, 2 Hz channels) and what Green Bank found at its own (2.794 Hz channels). A line fixed in the comet's frame but weaker than either gate at one epoch is not tested. A transmitter whose frequency changed between July and December is not tested. Parkes coverage is taken as each node's 128 MHz span, as the plan says; block edges are not reconstructed. 192 Green Bank L-band channels remain unsurveyed (lee/RESULTS-lee.md), and their clusters do not enter here.

Files: PLAN-epoch.md, run_epoch.py, epoch.json (every pair within 50 Hz, the null draws' summaries), run.log.
