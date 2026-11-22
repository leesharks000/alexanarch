# READ — HM5's per-frame series at the comet's coordinates (path 3)

22 November 2026, at the author's word (10:42: "lets begin working through tests 1-4"). Descriptive: hm5_0013.npz and hm5_0014.npz read with no new computation on the voltages, no test and no threshold (read_frames.py → READ-HM5-frames.json, read-frames.log). C08–C11 were named from X, so nothing here is evidence that they are special.

Measure: each frame's power at the coordinate (centre bin over the mean of 129 bins, as HM4 §D) over the mean of its own sidebands at the same frame. ON is 0013, OFF 0014.

1. **The conventional reading first.** The power excess at C08–C11 in X is a shift of the whole distribution, not a few strong frames.
   - Medians move with the means. C08: median 0.746 in ON against 0.653 in OFF. C10: 0.812 against 0.693.
   - The frames where a coordinate stands above every sideband come at about the rate chance gives (C10 X: 117 frames in ON against 92.6 expected; C11 X: 120; C09 X: 125 against 119). The longest run above every sideband is 2 to 5 frames, about 0.7 to 1.8 s.
   - The strongest single frames (ratios 8 to 24) fall within the spread every coordinate shows in ON and OFF alike.
   This is how a small, steady added power looks. A steady property of the X chain at the ON pointing would look like this; so would steady faint emission.
2. **C08–C11 do not move together frame by frame.** Their pairwise correlations of per-frame excess in X ON average r = 0.04, against 0.01 for C03, C05, C12 and C13. Four coordinates rising together on one cause (a burst, a sweep, a gain step) would show a positive correlation. They show none beyond the comparison.
3. **The halves differ by coordinate.** In X ON, C08's excess is larger in the first half (ratio 1.25 against 1.15), while C09 and C11 grow in the second (1.14 → 1.26; 1.17 → 1.37) and C10 holds (1.26, 1.32). Rank by 11.5 s bin scatters in both directions for each coordinate, as HM5 §B found for D3.
4. **C08 is seen in Y as well.** HM5 reported Y as nothing for D3 and for the cohort's power. Coordinate by coordinate, the full-series ON − OFF power rank in Y is +0.625 at C08 (X: +1.00), and −0.33, +0.25, +0.25 at C09–C11 (X: +0.83, +0.63, +0.75). The per-frame ratio at C08 is 1.199 in ON against 1.058 in OFF in Y, close to X's 1.200 against 1.068.
   - C08's OFF ratio is the lowest of the eleven in both feeds.
   - So at C08 the power contrast is not X-only. C09–C11 remain X-only.
   - Stated as description: C08 was named from X, and Y's +0.625 is one coordinate among eleven.

**What this sends forward.** HM6 tests whether the C08–C11 power and the cohort's D3 follow the comet's drift or stay fixed at the dish, and looks for the OH line in each feed. It was designed from RESULTS-HM5 and frozen before its own product was read; this note changes nothing in it.
