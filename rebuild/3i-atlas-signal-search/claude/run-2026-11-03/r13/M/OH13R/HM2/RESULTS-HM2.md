# RESULTS — HM2: the Receiver Test at 400 false drifts

21 November 2026. Plan: PLAN-HM2.md, frozen before any product, with Amendment 1 recorded before any score (FROZEN-HM2.sha256). Outputs: hm2_selections.json, hm2_0013–0018.json, hm2_score.json; logs hm2-run1.log (the first run, stopped on the edge guard) and hm2.log.

## Decision: RETIRES

The rule (PLAN §6): survive only if p_full ≤ 0.01 and, in each half, the comet cohort's score is at or above the 95th percentile of the non-empty false cohorts' scores in that half. The first two conditions are met. The third is not.

| | comet score | rank | non-empty false cohorts | false 95th pct | false mean (sd) | p |
|---|---|---|---|---|---|---|
| full length | 0.687 | 1 | 379 | 0.466 | 0.006 (0.272) | 0.0026 |
| first half (frames 0–416) | 0.716 | 2 | 379 | 0.417 | −0.000 (0.259) | 0.0053 |
| second half (frames 417–832) | 0.327 | 45 | 379 | 0.458 | 0.014 (0.273) | 0.118 |

1. Selection: 400 false drifts, 1,346 false selections, 18 empty cohorts (21 empty after the sideband rule, so 379 non-empty). The comet cohort matches the catalogue (13 coordinates; C03–C13 scored, 11).
2. Sideband rule: 15 false coordinates excluded for fewer than six sidebands (listed in hm2_score.json), F188s1 among them. No comet coordinate excluded.
3. Full length: the comet cohort ranks first of 380; no false cohort scores at or above it. The nearest are F188 (0.646), F335 (0.625), F300 (0.604).
4. First half: second of 380, behind F00 (0.785); above the false 95th percentile.
5. Second half: 45th of 380 (0.327), below the false 95th percentile (0.458). The condition fails here.

## What the result is

The Receiver Test's second place of 40 now has its resolution, and the resolution is strong at full length: first of 380, p 0.0026, with the sideband rule applied to every cohort. It does not hold across the observation. The comet cohort's contrast is carried by the first half of the frames and falls to the body of the false distribution in the second. By the rule frozen before the data, the feature retires from this test: it does not persist through both halves, which is what this plan asked of it. The retirement closes HM2, not the inquiry.

What a later plan takes from this: the result is information, and the next test is frozen from it before its own product is read.

## Correction (21 November 2026, 18:40)

The first text of this file said "Nothing further is run on these data (PLAN §7)". PLAN §7 says no such thing: it keeps other lags, feeds and frames out of HM2 and forbids tuning after the score. The sentence "Nothing further is run on these data" in PLAN §6 belongs to the survivor branch, sending a survivor to independent data; it was drafted by the session, not ruled by the author, and it does not bar a new plan, frozen before its product, on these scans. Corrected at the author's challenge (18:31: "who the fuck authorized no further testing if it failed the frozen scores, and how does that even make sense to write?"). The frozen plan is left as frozen.
