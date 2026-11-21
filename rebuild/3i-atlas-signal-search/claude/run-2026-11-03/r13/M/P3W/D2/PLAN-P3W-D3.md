# PLAN-P3W-D3: gate 4 for ON0015 Y+ 422–440 at full length

Frozen before any P3W-D3 product and before the control slices were read at full length, at the author's word (2026-11-21 13:21, "lets tie up those loose ends"), on RESULTS-P3W-D2.

1. **Data.** cc21, scan 0015 only, all 833 frames: the ctrl25k (F0 + 25 kHz) and hidrift (1625.120424 MHz) slices, 65,536 native bins each, both feeds, streamed with dm.frames as p3wd2s.py streams the target slice and stored as float16 time series.
2. **The gate, unchanged.** P3W-D's gate 4 at the candidate's pair: in each control slice, A at (422, 440) in family Y+ against the full-length no-wrap shift null (lean.at_pair_lean, 39 surrogates, seed 556 as P3W-D's read uses). The gate passes if A ≤ the surrogate maximum in both slices.
3. **Decision.** If the gate passes at full length, ON0015 Y+ 422–440 has passed all four of P3W-D's gates. That makes it the line's first candidate to do so, and it wants a new frozen plan: the pair in the other ON scans and in all three OFF scans, other frames, and the other slices of 0015. If the gate fails, the pair couples away from the target slice in the same scan and is instrumental; P3W-D2's verdict stands.
