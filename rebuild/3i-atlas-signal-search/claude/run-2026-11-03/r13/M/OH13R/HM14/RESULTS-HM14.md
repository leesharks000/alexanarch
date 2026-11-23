# RESULTS-HM14 — the Parkes pattern against 380 false drifts

23 November 2026. Plan PLAN-HM14.md, amendment 1 before any product (FROZEN-HM14.sha256). Code hm14.py. Output hm14.json; logs hm14-run2.log (the scored run, whose final file write failed on a float32 after every score had printed) and hm14.log (the same run repeated with `default=float` in the write, amendment 2, output only; identical figures).

**Gate passed** in all three sessions: the comet cohort at HM7's own reference range reproduces HM7's stored D for every candidate to 1e-3.

**Verdict under the plan: the Parkes pattern retires.**

| Session | family, comet | false mean ± sd | comet rank of 381 | C09 rank of 381 |
|---|---|---|---|---|
| 2025-07-31 | 0.103 | 0.040 ± 0.235 | 141 | 107 |
| 2025-09-12 | 0.122 | −0.033 ± 0.242 | 90 | 42 |
| 2025-10-05 | 0.329 | −0.016 ± 0.211 | 20 | 85 |
| combined (mean standardized) | | | 25 | 24 |

The rule asked the family to rank in the top 5% (≤ 19) in two sessions and ≤ 4 combined. It ranks in the top 5% in none (October, its strongest, is 20th) and 25th of 381 combined (about the top 7%). C09 meets neither part (ranks 107, 42, 85; 24th combined).

Unlike Green Bank, the false cohorts here carry no upward bias: their family mean is 0.040, −0.033 and −0.016, positive in 59%, 42% and 49% of cohorts. So HM7's positive sign is not the drifting-window property. It is a weak excess of consistent sign: the comet cohort sits at standardized 0.27, 0.64 and 1.63 in the three sessions. Three positives would come from a false cohort about one time in eight, and the combined standing from about one in fifteen. Neither is evidence, and the rule frozen before the run retires it.

**What this closes.** The one pattern in the record that ran the same way across two telescopes and four dates does not stand above false drifts at Parkes. It is weak and of consistent sign, not an artefact of tracking, and not a lead. With it, the voltage phase has no open lead on the comet. What could still revisit it is only another session at these rest frequencies, at a telescope as sensitive as Green Bank.
