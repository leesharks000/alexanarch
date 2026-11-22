# RESULTS-HM8: the X power excess, in the other pairs and on Parkes's scale

Scored 22 November 2026, after all four scans finished, against PLAN-HM8.md as frozen. `sha256sum -c FROZEN-HM8.sha256` printed OK for PLAN-HM8.md and hm8.py before the score was run. Nothing below was set after the score.

**Reproduction (plan §2).** For each new scan, track c power at every comet window matches HMR2's stored per-frame power, averaged over frames. The largest relative difference was 1.04e-7 (0015), 1.10e-7 (0016), 1.19e-7 (0017) and 0.97e-7 (0018), against the frozen 1e-4. A is read.

**Separability.** The comet's drift across the scan is 11.65–11.67 native bins in 0013, 12.38–12.40 in 0015 and 13.10–13.12 in 0017, at every coordinate. The three tracks separate in every pair.

## A. The three tracks in the other two pairs

C08–C11 mean ON − OFF rank, X power (the plan's rule, §3):

| pair | track c (comet drift) | track d (dish-fixed) | track f (drift mirrored) | by the rule |
|---|---|---|---|---|
| 0013/0014 (HM6) | 0.80 | 0.31 | −0.39 | follows the comet |
| 0015/0016 | 0.39 | 0.15 | −0.16 | follows the comet |
| 0017/0018 | 0.14 | −0.10 | −0.21 | follows the comet |
| mean of three | 0.44 | 0.12 | −0.25 | |

1. **By the frozen rule, HM6's finding extends.** Track c is greater than both d and f in 0015/0016 and in 0017/0018. Plan §4 asked for at least one; both pairs meet it.
2. **The excess fades from pair to pair.** On track c the C08–C11 mean falls from 0.80 to 0.39 to 0.14.
3. **Against the false cohorts on the same track, the comet's power no longer stands out.** This is reported, not ruled; the plan's rule is the C08–C11 ordering. The cohort power score on track c ranks 20th of 380 in the first pair, 101st in the second and 205th in the third. In the third pair the comet's score (0.39) is below the false cohorts' mean (0.44). The false cohorts' upward bias on track c, which RESULTS-HM6 item 4 recorded as a property of drifting windows in ON, is there in every pair (false mean 0.44, 0.41, 0.44 on c; about 0 on d and f). A c > d, f ordering is what any drifting cohort tends to show. In the second and third pairs, the comet's ordering is not distinguishable from that bias.
4. **C09, per track** (reported): 0.83 / 1.00 / −0.67 in the first pair, 0.17 / 0.83 / −0.50 in the second and 0.67 / −0.17 / −0.33 in the third. C09 is stronger fixed at the dish in the first two pairs and follows the drift in the third. It holds no consistent side.
5. **D3 and Y** (reported, not ruled):
   - X D3, cohort rank on c: 1st in the first pair, 84th in the second, 74th in the third. In the second pair d ranks better (52nd), and in the third f ranks better (25th).
   - Y power: the comet's rank on c is 226th, 318th and 236th; Y shows nothing in any pair.
   - Y D3 in 0017/0018 is low on all three tracks (364th, 359th, 362nd of 380).

## B. The Green Bank excess on HM7's scale

The excess e (plan §5), X, mean of the three pairs, in units of the local system power per native bin, and the predicted Parkes a over the whole SEFD range (plan §6):

| coordinate | mean e, X | predicted a: Jul 31 | Sep 12 | Oct 5 |
|---|---|---|---|---|
| C03 | −0.003 | −0.003 to −0.002 | −0.003 to −0.002 | −0.004 to −0.002 |
| C04 | 0.002 | 0.001 to 0.002 | 0.001 to 0.002 | 0.002 to 0.003 |
| C05 | 0.030 | 0.016 to 0.026 | 0.020 to 0.032 | 0.021 to 0.033 |
| C06 | 0.005 | 0.003 to 0.005 | 0.003 to 0.006 | 0.004 to 0.006 |
| C07 | 0.049 | 0.027 to 0.043 | 0.033 to 0.053 | 0.035 to 0.056 |
| C08 | 0.065 | 0.036 to 0.057 | 0.043 to 0.070 | 0.046 to 0.073 |
| C09 | 0.054 | 0.030 to 0.048 | 0.036 to 0.058 | 0.038 to 0.061 |
| C10 | 0.056 | 0.031 to 0.049 | 0.038 to 0.060 | 0.040 to 0.063 |
| C11 | 0.074 | 0.041 to 0.065 | 0.050 to 0.080 | 0.052 to 0.084 |
| C12 | −0.007 | −0.005 to −0.003 | −0.007 to −0.004 | −0.007 to −0.004 |
| C13 | 0.020 | 0.011 to 0.018 | 0.013 to 0.022 | 0.014 to 0.023 |

6. **HM7's null does not constrain the Green Bank excess at any coordinate.** By plan §7, a coordinate is constrained at a ≥ 1.5 and unconstrained below 1. The largest predicted a is 0.084 (C11, October, at the low SEFD), about eighteen times below HM7's floor. Steady and comet-borne, the excess would have been invisible at Parkes. Parkes neither confirms it nor rules it out.
7. This carries the plan's stated assumption: a steady source between July and December. The SEFDs are from memory, so they are carried as a range; the reading holds across the whole range.

## Reading

- The first pair's X power excess on the comet's drift passes the frozen test in both later pairs, and HM6's finding extends by its own rule.
- Read against the false cohorts on the same track, it does not hold up. The excess falls by half and then by half again. By the third pair the comet's cohort sits in the body of the false cohorts, where the drifting-window bias that HM6 recorded would put any cohort. The ordinary account, a property of the X chain in ON acting on drifting windows, now covers the second and third pairs as well as it covers any cohort. It does not explain the first pair's rank of 20th of 380 in power, or 1st in D3.
- Parkes cannot speak to it at this size. That is a fact about HM7's sensitivity, not about the excess.
- Failing a frozen test bars nothing, and passing one claims no more than the rule says. The first pair stays what HM6 found. HM8 adds that the later pairs pass the rule without standing out from what drifting windows do.

Outputs: hm6_0015–0018.json and .npz (about 2.4 MB each, committed as HM6 committed its own), hm8-0015–0018.log, hm8-score.log, hm8_score.json. RESULTS-HM8.sha256 hashes this file and the score.
