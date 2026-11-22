# RESULTS-HM9: reading for coherence

Scored 22 November 2026 against PLAN-HM9.md as frozen (b9304cfd4), in its two stages. `sha256sum -c FROZEN-HM9.sha256` printed OK before each stage. hm9.py verified every HMR2 product against RESULTS-HMR2.sha256 before reading it. Stage 1 (ON 0013, OFF 0014) was read first. AMEND-HM9.md, committed before stage 2 (07997ee5f), records that no amendment was frozen and why.

## Stage 1: ON 0013 against OFF 0014

| reading | at the comet, ON 0013 | OFF 0014 | sidebands' base rate (p < 1e-4) |
|---|---|---|---|
| H1, the feeds agree | no coordinate below p = 0.11 | C09 nearest, γ = 0.089, p = 0.0067 | 0 of 84, both scans |
| H2, carrier across frames, X | none below p = 0.07 (lag) or 0.14 (periodogram) | C10 periodogram p = 0.025 | 0 of 84 |
| H2, carrier across frames, Y | C10 periodogram nearest, p = 0.047 | none below 0.06 | 0 of 84 |
| H3, C08–C11 common mode, X | raw 0.034 (144 of 10,000 as high); differenced 0.049 (39) | −0.001 and 0.000 (about 5,000) | |
| H3, Y | −0.033 and −0.038 | 0.019 and 0.028 (940, 580) | |
| H4, open, lag 0 | **passes at C04 only**: 1.648, its sidebands' highest 1.617, 0 of 200 surrogates | C04 1.617, below its sidebands' 1.636 | |
| H4, open, lags 1–8 | none | none | |

1. Nothing at the OH coordinates C08–C11 passes any reading, in either feed or scan. Nor does anything at C03–C13 other than C04's open reading.
2. **C04's open reading.** Its form is diffuse: 0.36 in X and 0.64 in Y, with the largest element carrying 0.074 (Y+15). Its value is at the edge that noise gives for 66 elements over 833 frames, (1 + √(66/833))² ≈ 1.64, and inside the scan's range of sidebands (up to 1.666). It was carried to the hold-out with its form fixed (plan §3.3).
3. **H3 in X comes nearest of the readings that fail**: p ≈ 0.004 differenced, against the rule's p < 1e-4. OFF shows none, and Y shows none.

## Stage 2: the hold-out (ON 0015 and 0017, OFF 0016 and 0018)

4. **C04's form does not hold.** Applied to the hold-out frames, the stage-1 eigenvector gives u†Γu = 1.025 in ON 0015 and 0.966 in ON 0017, where 1 is what noise gives. 48 and 161 of 200 surrogates were as high (p ≈ 0.24 and 0.80). It does better in OFF 0016 (1.074, 4 of 200) than in either ON. By §3.2 it fails in both ONs, and stays found in one scan.
   - **A discrepancy with the plan.** §3.3 says the fixed form is also compared with the sidebands' values under the same u. hm9.py applies the fixed form only at the coordinates, so the sideband comparison was not computed. The surrogate test alone already fails in both ONs, so the outcome does not depend on it.
5. **H3 does not recur.** C08–C11's mean correlation in X is −0.019 raw and −0.022 differenced in ON 0015 (about 9,100 of 10,000 four-sets as high). It is 0.017 and 0.023 in ON 0017 (1,242 and 979). OFF 0016 and 0018 give similar values, and Y gives nothing in any scan.
6. **H1 and H2:** none passes anywhere, and the sidebands' base rate at p < 1e-4 is 0 of 84 in every scan. The single value below p = 0.01 in the hold-out is C09's X periodogram in ON 0017, p = 0.0076.

## Reading

- On every measure of coherence the plan names, and on the open one that names none, the X excess at C08–C11 behaves like receiver noise. It holds no phase from frame to frame, it shares nothing with Y, and the four coordinates do not move together beyond what their sidebands do.
- The one structure stage 1 found, at C04, is diffuse, at the noise edge, and absent on the hold-out.
- This is what the ordinary account predicts for the excess: a property of the X chain acting on drifting windows. The comet account in its coherent forms (a carrier, a polarized source seen by both feeds, a line shared by the four OH coordinates) predicts otherwise.
- The self-test bounds what these readings miss. A carrier holding more than about 3% of its bin's power would have been seen by H2, and HM8's excess is 5–7%. A cross-feed coherence of γ ≥ 0.11 would have been seen by H1. What remains possible is an incoherent excess polarized wholly along X, which no coherence reading can separate from the X chain.
- Failing a frozen test bars nothing. The first pair's rank (20th of 380 in power, 1st in D3) still stands as HM6 found it. HM9 says the power in it does not cohere.

Outputs: hm9_stage1.json, hm9_stage2.json, hm9-stage1.log, hm9-stage2.log. RESULTS-HM9.sha256 hashes them and this file.
