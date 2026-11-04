# Parkes 2025-07-31 full-band search, results (plan: pks/PLAN-fullband.md)

Node summaries as logged in pks/fullband.log:

- blc07 SUMMARY {'true': 2197, 'swap': 746, 'false_mean': 2679.65, 'false_sd': 943.3305504964842, 'false_max': 5482, 'false_minus_swap_max': 1926, 'lead': False}
- blc06 SUMMARY {'true': 10168, 'swap': 8585, 'false_mean': 6634.8, 'false_sd': 1411.2837276749137, 'false_max': 9532, 'false_minus_swap_max': 3554, 'lead': False}
- blc05 SUMMARY {'true': 269, 'swap': 281, 'false_mean': 273.35, 'false_sd': 35.527841195321734, 'false_max': 384, 'false_minus_swap_max': 55, 'lead': False}
- blc10 SUMMARY {'true': 2933, 'swap': 2500, 'false_mean': 810.15, 'false_sd': 350.29776976167005, 'false_max': 1782, 'false_minus_swap_max': 350, 'lead': True}
- blc04 SUMMARY {'true': 3015, 'swap': 3152, 'false_mean': 1294.75, 'false_sd': 354.8309280488385, 'false_max': 2164, 'false_minus_swap_max': 566, 'lead': False}
- blc03 SUMMARY {'true': 3412, 'swap': 6970, 'false_mean': 3667.75, 'false_sd': 5419.10242452567, 'false_max': 25572, 'false_minus_swap_max': 7906, 'lead': False}
- blc11 SUMMARY {'true': 974, 'swap': 2157, 'false_mean': 689.9, 'false_sd': 138.86500639109912, 'false_max': 1206, 'false_minus_swap_max': -191, 'lead': False}
- blc02 SUMMARY {'true': 997, 'swap': 1777, 'false_mean': 580.8, 'false_sd': 221.5449390078681, 'false_max': 1389, 'false_minus_swap_max': -625, 'lead': False}
- blc01 SUMMARY {'true': 8758, 'swap': 9698, 'false_mean': 6871.55, 'false_sd': 1095.6135484284594, 'false_max': 9107, 'false_minus_swap_max': -77, 'lead': False}
- blc00 SUMMARY {'true': 11941, 'swap': 12837, 'false_mean': 9663.55, 'false_sd': 686.8385163195204, 'false_max': 11174, 'false_minus_swap_max': 795, 'lead': False}
- blc13 SUMMARY {'true': 602, 'swap': 659, 'false_mean': 486.05, 'false_sd': 107.25505815578117, 'false_max': 695, 'false_minus_swap_max': 79, 'lead': False}
- blc14 SUMMARY {'true': 4095, 'swap': 2340, 'false_mean': 2417.5, 'false_sd': 417.46191443052624, 'false_max': 3553, 'false_minus_swap_max': 375, 'lead': True}

## Flags

- blc10 (lead True under the rule). Driven by block 1730.242 MHz (true 493, swap 151, false max 150); leaving that block out kills the lead. Per-sample band power there varies by up to ±29% in both S and R scans: wideband bursty interference. Not a candidate.
- blc14 (lead True under the rule: true 4095, swap 2340, false max 3553). Driven by blocks 2307.2–2317.7 MHz; the top block 2315.600 MHz alone has true 687, swap 10, false max 256, and leaving it out kills the lead (true 3408 against false max 3535). Its 687 candidates are spread densely across the whole 2.1 MHz block. Per-sample band power (pks/bandpow.py, 50k-channel slices) at 2310.0, 2314.5, 2316.9 and 2330.0 MHz swings from −24% to +279% in both S and R scans, with the largest excursions in R1; at 2360.0 MHz it holds within ±3%. Wideband time-variable interference across about 2307–2330 MHz, the same pattern as blc10. Not a candidate.
