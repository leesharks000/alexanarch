# RESULTS-ratio (plan ratio/PLAN-ratio.md, sha256 1cd2fef8...)

Injection (5/3 topocentric, scan 0): tone recovered z 6.30 at offset 0.00 kHz (P, W1, sample 7); burst recovered z 6.63 at +3.00 kHz (P, W50, sample 12). Deviation, recorded: the first burst calibration used single-channel sd and gave z 3.5 at W50 (adjacent 2 Hz channels correlated); recalibrated to the sd of the W50 boxcar. Detector unchanged. Background at z >= 5 is heavy-tailed: hundreds of in-tolerance events per frequency in S and in R; about half the window vetoed at W1.

GBT (cadence 0029, 2214-2401 MHz): alpha 5/3 true 0 swap 0; ctrl 11/7 true 0 swap 0. Other cadences hold no list frequency.

Parkes, in-tolerance events (true = S scans, swap = R scans):
- alpha 5/3 2367.3429 MHz blc14: true 480, swap 441
- alpha 15/8 2663.2608 MHz blc17: true 152, swap 191
- alpha 7/4 2485.7101 MHz blc15: true 1792, swap 854
- alpha 3/2 2130.6086 MHz blc13: true 93, swap 77
- alpha 7/5 1988.5681 MHz None: true 0, swap 0
- alpha sqrt2 2008.7571 MHz None: true 0, swap 0
- alpha 2 2840.8115 MHz blc20: true 85, swap 93
- alpha 4/3 1893.8743 MHz blc11: true 77, swap 76
- alpha 8/7 1623.3209 MHz blc07: true 1108, swap 333
- alpha 7/6 1657.14 MHz blc07: true 94, swap 92
- alpha 7/8 1242.855 MHz blc04: true 268, swap 120
- alpha 1/2 710.2029 MHz blc00: true 559, swap 441
- alpha 4/7 811.6604 MHz blc00: true 75, swap 94
- ctrl 11/4 3906.1158 MHz blc32: true 107, swap 104
- ctrl 11/5 3124.8927 MHz blc22: true 88, swap 80
- ctrl 6/11 774.7668 MHz blc00: true 341, swap 316
- ctrl 11/6 2604.0772 MHz blc16: true 66, swap 78
- ctrl 7/11 903.8946 MHz blc01: true 97, swap 103
- ctrl 11/7 2232.0662 MHz blc13: true 1058, swap 65
- ctrl 13/5 3693.055 MHz blc27: true 88, swap 77
- ctrl 8/11 1033.0224 MHz blc02: true 78, swap 81
- ctrl 11/8 1953.0579 MHz blc11: true 77, swap 80
- ctrl 13/6 3077.5458 MHz blc22: true 77, swap 87
- ctrl 7/13 764.8339 MHz blc00: true 289, swap 472
- ctrl 9/11 1162.1502 MHz blc03: true 250, swap 937
- ctrl 11/9 1736.0515 MHz blc10: true 79, swap 76

Summary under the frozen rule: alpha rate 434.8 per covered frequency (11 covered; 7/5 and sqrt2 fall in 1984-2112 MHz, held by no node), control rate 207.3 (13), alpha swap rate 255.6, multi-scan criterion met. lead = True.

Diagnosis.
- The alpha rate is carried by two frequencies: 7/4 (1792 vs 854; 1564 of 1792 in scan 0, samples 9-19) and 8/7 (1108 vs 333; scans 0 and 2, samples 2-7 and 14-18). Without them the alpha rate is 154.8, below the control rate.
- 7/4 x HI = 2485.710 MHz (comet position 2485.91) lies in 2483.5-2500 MHz, a mobile-satellite downlink allocation (Globalstar). 8/7 x HI = 1623.321 MHz (comet position 1623.45) lies in 1616-1626.5 MHz, the Iridium allocation. 7/8 x HI = 1242.855 MHz: its strongest events sit at 1242.9446 MHz, inside the GLONASS L2 FDMA channel at 1242.9375 MHz (k = -7). These are allocations; that these particular events are those satellites is not checked.
- The control list carries the same pattern: 11/7 x HI = 2232.066 MHz (true 1058, swap 65, z to 452, 990 of 1058 in scan 0) lies in 2200-2290 MHz, a space-research and space-operations downlink allocation. An on-source excess at a satellite-band frequency occurs on both lists.
- The multi-scan criterion is met by noise at this threshold: with hundreds of events per window, many 100 Hz bins hold events from two S scans on every list.
- Post-hoc (not in the plan): label-permutation test over the 24 covered frequencies, 20000 draws. Plan statistic (difference of mean true counts) p = 0.107; per-frequency log(true/swap) mean difference p = 0.299.

Reading. The lead fires under the frozen rule and the rule does not survive its own controls: the excess follows which list frequencies happen to land in satellite downlink allocations, and a control frequency in such an allocation shows the largest on/off contrast of all 26. Not a candidate. The rule's mean-rate statistic and its multi-scan clause are too weak at z >= 5 in this data; a future plan needs a rank statistic and a per-frequency persistence test at a fixed frame frequency.
