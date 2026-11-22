# RESULTS — HM4: tracking X

21–22 November 2026. Plan: PLAN-HM4.md, frozen before any product (FROZEN-HM4.sha256, commit db1e5372a). No amendment. Outputs: hm4_selections.json, hm4_0013–0018.json, hm4_score.json; logs hm4-a.log (0013–0015), hm4-b.log (0016–0018), hm4-score.log. Both runs finished within the time limit; nothing was resumed.

One caution governs every G1667 figure below. G1667 (C07–C11) was named from the X feed's own HM2 outputs. Its p-values in X are therefore not evidence that anything is there: the data that chose it are the data scoring it. In Y (HM3) it was a fair test, and it failed. Here its X figures say only where, within X, the named group's contrast sits. The comet cohort was fixed before HM2 and is not subject to this caution.

## A. Reproduction: passed

The X feed reproduces hm2_score.json's comet cohort exactly: full 0.6868, first half 0.7161, second half 0.3266 (difference 0 to the printed precision; reproduction_ok = true). Everything below was read only after this check.

## B. Time map, X

| segment | frames | cohort | rank /380 | false 95th | G1667 | p (named from X) |
|---|---|---|---|---|---|---|
| s0 | 0–104 | 0.477 | 18 | 0.457 | 0.404 | 0.082 |
| s1 | 105–208 | 0.302 | 43 | 0.443 | 0.242 | 0.168 |
| s2 | 209–312 | 0.352 | 37 | 0.442 | 0.180 | 0.227 |
| s3 | 313–416 | 0.281 | 48 | 0.409 | 0.323 | 0.072 |
| s4 | 417–520 | 0.067 | 167 | 0.433 | 0.280 | 0.171 |
| s5 | 521–624 | 0.147 | 129 | 0.442 | 0.478 | 0.029 |
| s6 | 625–728 | 0.159 | 105 | 0.434 | 0.516 | 0.014 |
| s7 | 729–832 | 0.264 | 58 | 0.412 | 0.205 | 0.222 |

| ON–OFF pair | cohort full (rank) | first half | second half | G1667 full (p) | first half | second half |
|---|---|---|---|---|---|---|
| 0013–0014 | 1.294 (1) | 0.942 (5) | 0.955 (8) | 0.429 (0.16) | 0.186 | 0.671 |
| 0015–0016 | 0.364 (84) | 0.603 (39) | 0.000 (185) | 0.894 (0.025) | 0.727 | 0.745 |
| 0017–0018 | 0.402 (74) | 0.603 (48) | 0.025 (188) | 1.435 (0.0005) | 0.988 | 1.323 |

1. **Segments.** No single segment carries the cohort. Only s0 reaches the false 95th percentile, and only just; the others rank 37th to 167th. The full-length first place is built by accumulation over the first half.
2. **Pairs.** The cohort is carried by the first pair. 0013–0014 ranks first of 380, in both halves (5th and 8th). The second and third pairs fall into the body of the distribution, and to nothing in their second halves. By the reading stated in PLAN §3, the cohort's X contrast is localized in time: an event in the first ON scan against its OFF, not a steady property of the session.
3. **G1667 does the opposite.** It is weakest in the first pair (0.43) and rises through the second (0.89) to the third (1.44). Within the scans it is spread across segments, largest in s5–s6. Its contrast grows through the session.
4. **The two patterns are different things.** The cohort's contrast sits at the start of the session. The OH 1667 group's grows to the end, as the comet rose from zenith angle 81.3° (0013) to 77.4° (0017).

## C. Feed basis

| | cohort P+ (rank) | cohort P− (rank) | asymmetry, two-sided p | G1667 P+ | G1667 P− | asymmetry | p | null 95th of the asymmetry's size |
|---|---|---|---|---|---|---|---|---|
| full | −0.352 (348) | 0.331 (37) | −0.683, 0.076 | −0.006 | −0.037 | 0.031 | 0.94 | 0.727 |
| first half | −0.067 (228) | 0.297 (54) | −0.364, 0.34 | 0.366 | 0.186 | 0.180 | 0.65 | 0.745 |
| second half | −0.389 (357) | −0.096 (243) | −0.293, 0.40 | −0.304 | −0.404 | 0.099 | 0.80 | 0.764 |

5. **Asymmetry within the null.** For G1667 the asymmetry is near zero in every part. For the cohort it is negative with the same sign throughout, but within the null (p 0.08 at full length, 0.34 and 0.40 in the halves). By the reading stated in PLAN §4: the pattern lies on the X axis only. Either the X chain carries it, or the incoming wave is polarized along the X feed's axis; by fact 3 of the plan, these data cannot separate the two.
6. **Mixing with Y removes it.** In P+ and P−, G1667 is at or below the null mean. The cohort reaches 37th in P− at full length and nothing in P+. The X feed's contrast does not survive being mixed half-and-half with Y. That is what an X-only feature does under this statistic. D3 is a third-order product of unit phasors, and halving a weak feature's share of the power cuts it by more than half. This adds nothing that separates the two readings in 5.

## D. Power, X

| | cohort (rank) | false 95th | p | G1667 | null 95th | p (named from X) |
|---|---|---|---|---|---|---|
| full | 0.729 (57) | 0.896 | 0.15 | 0.957 | 0.913 | 0.034 |
| first half | 0.858 (8) | 0.738 | 0.021 | 0.907 | 0.801 | 0.021 |
| second half | 0.444 (110) | 0.723 | 0.29 | 0.602 | 0.764 | 0.149 |

7. **A modest power contrast, first half only.** The cohort has one in the first half (8th of 380, above the false 95th percentile), where its D3 contrast also lives, and none in the second. G1667's is just above its null at full length and in the first half, not in the second. The second half, where G1667's D3 contrast is largest, shows no power contrast. By the readings stated in PLAN §5:
   - the cohort's first-half D3 contrast comes with a power contrast, a narrowband feature in X adding power on the track;
   - G1667's late D3 contrast does not: phase structure in X with no excess power on the track.

## What the result is

1. **The conventional reading first.** Everything found in HM2 lives in the X chain's output and nowhere else. It does not appear in Y (HM3), and it does not survive mixing with Y (here). The cohort's first place is mostly one ON–OFF pair, the first, at the lowest elevation of the session, about 9°. An X-only feature confined to one pair at 9° elevation is, on the ordinary account, interference or pickup in one receiver chain at one moment. Low elevation is where the ground and the horizon enter the sidelobes.
2. **What that reading has to explain.**
   - The feature follows the comet's drift, not the chain's channels. Same-frequency false tracks show nothing (HM2).
   - In the first pair it adds power on the track.
   - The OH 1667 group behaves differently: weak at the start, growing pair by pair as the comet rose, with no power excess. But that group was named from these data, and its X figures are not evidence (the caution above).
3. **What tracking has established.** The cohort's X contrast has an address in time: the first pair, 0013 against 0014, with a power excess in the first half. Fact 3 in the plan still holds: the feeds never rotated against the sky, so nothing here can separate a property of the X chain from emission polarized along X.
4. **Where it can be followed next, should the author want it.** Each step would be frozen before its own product is read.
   - The first pair is the place to look: the time course within 0013 and 0014, frame by frame, at the cohort's coordinates, in X and Y, in power and D3. That would show whether the contrast is an episode, its shape, and whether Y sees anything at that moment.
   - The OH 1667 group's growth with elevation needs data that did not choose it. Another session on the comet, at other elevations, with the feeds at another parallactic angle, would test it fairly and could also separate chain from sky.
