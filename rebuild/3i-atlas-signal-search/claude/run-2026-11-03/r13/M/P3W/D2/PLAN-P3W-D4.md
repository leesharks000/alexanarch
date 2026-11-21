# PLAN-P3W-D4: ON0015 Y+ 422–440, the pair in every scan and every family

Frozen before any P3W-D4 product, at the author's word (2026-11-21 13:21, "lets tie up those loose ends"), on PLAN-P3W-D3's decision: gate 4 passed at full length (p3wd3_gate.json), so ON0015 Y+ 422–440 has passed all four of P3W-D's gates, and the plan named this follow-up.

**What the pair is.** In the target slice's 512-point segment spectra (358 Hz bins, unshifted FFT order), bins 422 and 440 are baseband −32.2 and −25.8 kHz, which is sky 1625.3258 and 1625.3194 MHz (the slice's frequency axis runs opposite to baseband). The sum form Y+ locks φ₄₂₂ + φ₄₄₀; its third would sit at baseband −58.0 kHz, sky about 1625.3516 MHz.

1. **Every scan.** For each of the six scans, at the full length already stored (ser_00NN.npy), the pair's A in each of the six families at (422, 440), with the full-length no-wrap shift null at that pair (lean.at_pair_lean, 39 surrogates, seed 557). Reported: A, the surrogate median and maximum, and the rank of A among the surrogates.
2. **Reading, fixed now.**
   - A source at the comet would show the pair, in some family, in ON scans above the null and not in OFF scans. Replication across ON scans is not required (the author's rule), but an OFF scan at the pair above its surrogate maximum sets the candidate aside as not at the comet.
   - Only Y, or Y and X? A sky source seen by both linear feeds would usually couple in X too (X+) or across (XY+); a Y-only relation, like the X-only features in channel 7, points to the instrument or to strongly linear interference.
3. **The aggregate rule stands.** The author's standing rule requires an aggregate family test for any lead; P3W-D2's aggregate is 2 of 36 (chance). Whatever this follow-up shows, this candidate is reported as passing P3W-D's four gates and failing the aggregate requirement unless the aggregate changes, which this plan does not test.
