# RESULTS — HM5: the first pair through time

21–22 November 2026. Plan: PLAN-HM5.md, frozen before any product (FROZEN-HM5.sha256, commit bbbf8b76d). No amendment. Outputs: hm5_0013.npz/.json, hm5_0014.npz/.json (the per-frame series for the comet cohort's 95 windows are in the .npz), hm5_score.json; logs hm5-0013.log, hm5-0014.log, hm5-score.log. Both scans finished within the time limit.

The pair was chosen from HM4's result. Nothing below is evidence that the pair is special; it describes what the pair's contrast is made of.

## A. Reproduction: passed

X D3 over all frames: 1.29399, against HM4's pair 0013–0014 score of 1.29399 (exact). Everything below was read only after this check.

## Over all frames

| | cohort score | rank /380 | false 95th | false mean | comet mean rank in ON | in OFF |
|---|---|---|---|---|---|---|
| D3, X | 1.294 | 1 | 0.764 | 0.001 | 0.784 | 0.394 |
| D3, Y | 0.038 | 201 | 0.709 | 0.046 | 0.420 | 0.409 |
| power, X | 1.093 | 20 | 1.090 | 0.441 | 0.826 | 0.496 |
| power, Y | 0.188 | 226 | 1.010 | 0.316 | 0.587 | 0.530 |

## B. The time course: spread, not an episode

1. **The rule (PLAN §4).** The positive parts of the X D3 bin scores sum to 8.08. The best run of at most three bins holds 2.21 of it (bins 12–14, ON 04:49:23–04:49:46 UTC): 27%, under the half the rule asks. By the reading stated in advance, the contrast is spread through the pair.
2. **Where the strong bins fall.** Five of the 26 bins reach the top 5% of the false cohorts (chance alone gives about 1.3): bins 2, 9, 12, 13 and 23. They fall across the whole scan: 04:47:28, 04:48:49, 04:49:23, 04:49:34, 04:51:29 UTC in ON. Between them the bins scatter in both directions. The first place over all frames is built from a contrast present through the five minutes, not from a moment in them.

## C. ON or OFF: the comet scan rises

3. **D3, X.** The comet coordinates sit at a mean rank of 0.78 among their sidebands in ON and 0.39 in OFF. Both move, but ON moves further: +0.28 above the middle against −0.11 below it. By the reading stated in PLAN §5, this is both, with the comet scan rising as the larger part: a presence in ON more than an absence in OFF.
4. **Power, X.** This one is ON alone: 0.83 in ON, 0.50 in OFF.

## D. Y and power at the same moment

5. **Y: nothing.** Y D3 over all frames is 201st of 380 (0.04 against a false 95th of 0.71). Y's comet coordinates sit at the middle in both scans (0.42 and 0.41). One Y bin reaches the top 5%, as chance gives. By the reading stated in advance, this pair is X-only too.
6. **Power, X: at the threshold.** X power over all frames is 20th of 380, 1.093 against a false 95th of 1.090, so the D3 contrast comes with a power contrast on the track, just at the line.
   - The false cohorts' power contrast is itself biased upward (false mean 0.44): ON scan 0013 is brighter than OFF 0014 across the band, at the session's lowest elevation.
   - The comet's power excess stands at the edge of that general brightening, not far above it.
   - Three X power bins reach the top 5% (bins 4, 20, 22), and none of them is a top D3 bin.

## E. Coordinates

| | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rest frequency, MHz | 1665.634 | 1666.120 | 1666.168 | 1666.513 | 1667.139 | 1667.413 | 1667.430 | 1667.687 | 1667.995 | 1668.098 | 1668.429 |
| D3 X, ON − OFF rank | 0.50 | 0.50 | 0.75 | 0.38 | 0.13 | 0.00 | −0.17 | 0.88 | 0.13 | 0.38 | 0.83 |
| power X, ON − OFF rank | 0.00 | 0.38 | 0.13 | −0.38 | 0.13 | 1.00 | 0.83 | 0.63 | 0.75 | 0.00 | 0.17 |

7. **D3 is carried broadly.** Nine of the eleven coordinates are positive. The largest are C10 (0.88), C13 (0.83) and C05 (0.75); C08 and C09 contribute nothing.
8. **Power is concentrated on C08–C11**, the OH 1667 coordinates: C08 1.00 (the comet coordinate above every sideband in ON and below every one in OFF), C09 0.83, C11 0.75, C10 0.63. Elsewhere it is near zero.
9. **They are different coordinates.** D3 is strong where power is not (C05, C13). Power is strong where D3 is not (C08, C09). Only C10 carries both.

## What the result is

1. **The conventional reading first.** This pair's first place is a steady X-only excess on the comet's coordinates through the whole ON scan, against an OFF scan where they sit a little below the middle. Y sees nothing. ON is brighter than OFF across the band at this elevation, and the comet's power excess is at the edge of that general brightening. A steady X-chain property of the ON pointing, at the lowest elevation of the session, accounts for the time course, the Y absence and the power. Nothing in HM5 requires more.
2. **What it does not settle.** The excess follows the comet's drift on its coordinates and not the false drifts on theirs. The power excess falls on the four coordinates around the OH 1667 line, C08–C11, and nowhere else. C08 stands above all its sidebands in ON and below all of them in OFF.
   - Those four are the group HM3 tested in Y, where it failed. In X it grows through the session in phase (HM4).
   - Here, in the first pair, it carries power and not phase: a narrowband excess in X on the OH 1667 coordinates at the start of the session, ahead of the phase structure that appears on the same coordinates later.
   - This is a description of where things sit, not a finding. The coordinates were named from X.
3. **Where it can be followed next, should the author want it.**
   - The per-frame series kept for the 95 comet windows (hm5_0013.npz, hm5_0014.npz) can be read without new computation for the shape at C08–C11: power frame by frame, ON against OFF.
   - A fair test of the OH 1667 coordinates needs data that did not name them. That is another session on the comet, which is the step RESULTS-HM4 §4 already names.
