# PLAN-P3W-D2: PLAN-P3W-D on all 833 frames of the target slice

Frozen before any P3W-D2 product and before the full-length cc21 data were read, at the author's word (2026-11-21 11:25, "and lets do the full 833 too, okay if we're running for awhile"), on RESULTS-P3W-D.

PLAN-P3W-D (sha256 b9f5e852…) and p3wd.py (sha256 b0340dc8…) are used unchanged, with these differences only, all forced by length or disk:

1. **Data.** The target slice (65,536 native bins centred on 1625.2936106 MHz, both feeds) for all 833 frames of each scan, streamed from cc21 with dm.frames as N1625 did (p3wd2s.py) and stored as float16 time series (about 437 MB per scan). The real statistics use the first S − 512 of the 106,624 segments, as P3W-D's shift null requires.
2. **Control slices (gate 4).** The full-length ctrl25k and hidrift slices are not kept, for disk. Gate 4 is evaluated, at a candidate's pair, on the 32-frame crops N1625 saved, as in P3W-D.
3. **The aggregate count** is over the six target-slice runs: 36 family tests, about 1.8 expected at p ≤ 0.05.
4. **Pre-registered follow-up.** P3W-D's one candidate, ON0017 Y+ at pair 217–293, is reported at full length in every scan, whatever the family maxima are.
5. Validation is P3W-D's (accepted, validationD.json); it is not rerun. Everything else, including seeds of the form 31625 + 100·scan_index (slice index 0), gates and limits, is P3W-D's.
