# RESULTS-sib: below-threshold siblings of the thirteen (frozen test)

Plan: sib/PLAN-sib.md, sha256 86bc3bb30f2a088c6e156f480c7e95d88d10116e5eb64c7f45366a65625f8338, frozen before the counts were computed. Data: GBT blc23 rawspec.0000, 2025-12-18, scans 0013–0018, coarse channel 7, re-read 2026-11-04 by sib/fetch_cc.py (fetch.log). Runner sib/run_sib.py (sha256 4d87a062…), output sib.json (sha256 24205670…), log run.log. Run 2026-11-04, 16:18–16:19 EST, one pass, no errors.

**Verdict (S1, 2.0 ≤ min ON < 2.5): NONE.** The comet frame holds 98 near-miss clusters against 105.6 ± 9.9 in the forty false frames (range 86–130; 80% of false frames reach 98). There is no excess just under the gate.

| band (min ON z; all OFF < 2.0) | true | swap | false mean ± sd | false min–max | fraction of false ≥ true |
|---|---:|---:|---|---|---:|
| S1: 2.0 ≤ min ON < 2.5 | 98 | 116 | 105.6 ± 9.9 | 86–130 | 0.80 |
| S2: 2.25 ≤ min ON < 2.5 | 15 | 26 | 18.2 ± 3.9 | 11–29 | 0.85 |
| ≥ 2.0 | 107 | 117 | 108.1 ± 10.0 | 89–134 | 0.63 |
| ≥ 2.25 | 25 | 27 | 21.5 ± 4.9 | 14–35 | 0.20 |
| ≥ 2.5 (the thirteen) | 13 | 1 | 3.75 ± 2.05 | 0–8 | 0.00 |
| ≥ 2.75 | 2 | 0 | 0.6 ± 0.9 | 0–3 | 0.10 |
| ≥ 3.0 | 1 | 0 | 0.1 ± 0.4 | 0–2 | 0.05 |

Clusters are counted after 10 Hz merging, so band counts do not add.

## Reading

The excess sits in one narrow slice of the score: at ≥ 2.5 the comet frame has 13 against 3.75, at ≥ 2.75 it has 2 against 0.6, so eleven of the thirteen lie between 2.5 and 2.75. Below the gate the comet frame is at or under the false frames (S1 98 against 105.6; S2 15 against 18.2), and the swap exceeds the true frame in both bands. A population of weak lines fixed in the comet frame leaves members under any gate it crosses: ChatGPT's injections (2026-11-04) recover a weak steady line at the tolerant gate in 118 of 256 placements, the rest falling below it. The near-miss band shows none.

Limit: the false-frame spread in S1 (sd 9.9) is about the size of the thirteen themselves. The band would show a sibling population several times larger than the thirteen and cannot exclude one of their own size. Within that limit, the comet-frame excess has no tail under the gate and almost none above it. That is the shape a fluctuation at the 2.5 cut takes; a real population would need its scores confined to the slice just above the gate, which the injected weak lines do not show. Post hoc, outside the plan: in ChatGPT's trial ledger (chatgpt/evidence/, results/all-trials.csv), the 356 weak steady-line injections (level 2.8, broad and local) have minimum ON scores of <2.0 in 78, 2.0–2.5 in 107, 2.5–2.75 in 50 and ≥2.75 in 121. Scaled to the eleven of the thirteen at 2.5–2.75, a population of such lines would put about 24 clusters in 2.0–2.5 and about 27 at ≥2.75; the comet frame shows no excess in the first and 2 against 0.6 in the second. The ledger scores use ChatGPT's F1 normalization and its own gate, so the comparison is approximate.

## Later (2026-11-04, 16:50 EST)

The reading above calls the shape that of a fluctuation at the 2.5 cut. The background models of bg/RESULTS-bg.md (frozen, b8fd193a…) bear on it: in 139 draws across four nulls (false accelerations, time-shuffled rows, role partitions, phase-randomized rows) none reaches 13, so a fluctuation of the data at that cut, which the nulls would show as often as the true frame, does not account for it. The measurement of this file stands: no siblings under the gate, the excess confined to 2.5–2.75.

## Deviations

One post hoc comparison, labelled (the injected weak lines' score distribution from ChatGPT's ledger). The raw spectra were deleted after the run; fetch_cc.py re-reads them by name.
