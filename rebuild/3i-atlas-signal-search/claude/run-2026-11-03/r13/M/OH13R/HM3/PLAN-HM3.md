# PLAN-HM3 — the HM2 measurement on the Y feed

Frozen 21 November 2026, before any Y product is read, at the author's word (18:37: "lets run those next tests").

**What is looked for, in the author's words.** "what were looking for, is something with meaning - and we do not know that that looks like. we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning, and the idea that we would not know what that looked like, that the reading it would be part of the meaning itself." The criteria below decide only whether a result counts as signal under them. They do not close the inquiry, and they do not forbid further tests; every later test is frozen before its own product is read.

**Why.** HM2 (X feed, frozen) ranked the comet cohort first of 380 at full length (p 0.0026) and second in the first half, and retired on the second half (45th). Reading its outputs afterwards (no new computation): the coordinates around the OH 1667 line, C07–C11 (1667.0–1668.0 MHz in the comet frame), held or strengthened in the second half (mean contrast +0.28 first half, +0.41 second), while false coordinates at the same frequencies averaged near zero in both halves. That group was named after seeing the X scores. The Y feed has not been read: it sees the same sky through an independent receiver chain, so it is a test of the X pattern, not a rescoring of it.

1. **Data.** The six scans, all 833 frames, the Y feed only. Everything else exactly as HM2 (hm2.py with Amendment 1): selections (hm2_selections.json, copied as hm3_selections.json), windows, reference windows skipped, six-sideband rule, D3 at d = 2, continuous comet- or false-frame de-Doppler, halves at frame 417.
2. **The full comet cohort.** Scored as HM2: cohort score = mean contrast × √n against the non-empty false cohorts; p_full = (1 + #false ≥ comet) / (1 + #non-empty false); both halves against the false 95th percentile. The HM2 rule is reported as stated.
3. **G1667, named now.** C07, C08, C09, C10, C11. Score = mean contrast × √5. Null: the false coordinates scored in HM2's windows with comet-frame-equivalent rest frequency in [1667.0, 1668.0) MHz and at least six sidebands; 10,000 random sets of five (numpy default_rng, seed 20261121); p = (1 + #draws ≥ G1667) / 10,001, and the null's 95th percentile in each half.
4. **X and Y together.** Reported, not gated: the Spearman correlation, over the eleven comet coordinates, of the X (HM2) and Y contrasts, full and each half.
5. **Reading the outcomes.** Each is stated so that it can be read as what it is:
   - G1667 counts as signal under these criteria if p_full ≤ 0.01 and both halves are at or above the null's 95th percentile. That says: the pattern found in X is present, on the comet's track, through an independent receiver chain, at frequencies where false tracks show nothing. It is still not a source, and it is not yet a meaning.
   - If G1667 does not reproduce in Y, the X pattern is not shared by the second chain at these criteria. That is information about where the pattern lives; it is recorded and read, not discarded.
   - The full cohort is reported against the HM2 rule either way.
6. **What stays fixed.** No other lag, statistic or frame within HM3; nothing tuned after the score. Any amendment is recorded before results.
