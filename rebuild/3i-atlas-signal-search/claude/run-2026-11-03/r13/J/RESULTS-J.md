# RESULTS-J: part J of PLAN-r13, the voltage test that can reach significance

Plan: PLAN-J.md, hashed with jv.py and janalyze.py in PLAN-J.sha256 before any J product existed (2026-11-18T17:06Z). The products are 1.1 GB and are not kept in the repository; their hashes are in J-PRODUCTS.sha256, and the statistics are in J.json. Run 2026-11-18, 17:06–17:53Z, six scans, no failures.

## The gate

J1 for m = 1, V0, comet frame gives **11**, delaymod's count, reproduced exactly. Passed.

## Result

**The comet frame beats all 400 false frames in the all-rows voltages, and the decision rule is not met.**
- With all rows (V0), the plain-power count (J1, m = 1) is 11 against 400 false frames: mean 3.33, maximum 9, p = 1/401.
- The co-moving pair statistic (J2) also exceeds its 99th percentile, at p = 0.005.
- Neither replicates in the ON scans separately: no single ON scan exceeds its own 99th percentile.
- With the off-target integrations dropped (V2), both fall to the null: J1 5 (p = 0.29), J2 p = 0.39.
- The suppressed-carrier products are at or below the null in both variants: x², J1 m = 2, gives 0; x⁴, J1 m = 4, gives 4 and 3.

| Variant | Statistic | True | False μ ± σ | p99 | Max | p (of 400) | p (40 nearest) | Each ON scan | Counts |
|---|---|---|---|---|---|---|---|---|---|
| V0 | J1_m1 | 11 | 3.33 ± 1.77 | 8.01 | 9 | 0.0025 | 0.024 | 0013: p 0.055 · 0015: p 0.249 · 0017: p 0.090 | no |
| V0 | J1_m2 | 0 | 3.36 ± 1.74 | 8.00 | 9 | 1.0000 | 1.000 | 0013: p 0.057 · 0015: p 0.052 · 0017: p 0.324 | no |
| V0 | J1_m4 | 4 | 3.23 ± 1.84 | 8.00 | 8 | 0.3990 | 0.488 | 0013: p 0.142 · 0015: p 0.135 · 0017: p 0.958 | no |
| V0 | J2 | 2.32 | 1.51 ± 0.25 | 2.22 | 2.38 | 0.0050 | 0.024 | 0013: p 0.097 · 0015: p 0.100 · 0017: p 0.112 | no |
| V2 | J1_m1 | 5 | 3.51 ± 1.95 | 8.01 | 10 | 0.2943 | 0.439 | 0013: p 0.047 · 0015: p 0.157 · 0017: p 0.125 | no |
| V2 | J1_m2 | 0 | 3.40 ± 1.82 | 8.00 | 9 | 1.0000 | 1.000 | 0013: p 0.182 · 0015: p 0.042 · 0017: p 0.304 | no |
| V2 | J1_m4 | 3 | 3.37 ± 1.90 | 9.01 | 10 | 0.6334 | 0.659 | 0013: p 0.172 · 0015: p 0.047 · 0017: p 0.803 | no |
| V2 | J2 | 1.49 | 1.48 ± 0.26 | 2.40 | 3.03 | 0.3890 | 0.585 | 0013: p 0.097 · 0015: p 0.117 · 0017: p 0.120 | no |

## Reading under the plan's rule

No J statistic counts. The voltages reproduce, with a null that can reach p = 1/401, what the spectra showed in r13:
- the comet-frame excess is real against the false frames when all rows are kept;
- it is carried by the off-target start of each scan;
- it does not replicate scan by scan.

J2 adds that the same rows also carry an excess of tone pairs moving together in the comet frame, and that it too vanishes under the cut. Neither a suppressed BPSK or QPSK carrier nor a delayed copy follows the comet.

The null is not exchangeable (r13 F). Against the 40 false frames nearest the comet's track, V0's J1 and J2 give p = 1/41 = 0.024: above every one of them. The excess against the nearest frames does not change the reading, because it does not survive the off-target cut.
