# GBT cc21, the two-part signal at full length (P3W-D2): the 32-frame candidate does not persist; ON0015 Y+ fails only the control-slice gate; no lead

**2026-11-21.** P3W-D, unchanged in method, on all 833 frames of the target slice, at the author's word ('and lets do the full 833 too').

Canonical run: [PLAN-P3W-D2.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/D2/PLAN-P3W-D2.md), [RESULTS-P3W-D2.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/D2/RESULTS-P3W-D2.md), [lean.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/D2/lean.py), [P3W-D2-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/P3W/D2/P3W-D2-PRODUCTS.sha256).

The text below is RESULTS-P3W-D2 as committed there.


Run 2026-11-21 under PLAN-P3W-D2 with amendment 1 (FROZEN-P3W-D2.sha256; FROZEN-P3W-D2-amend1.sha256: plan 6e007b57…, lean.py 47979f31…, check_lean.json 63f4ad59…). The target slice of cc21 (65,536 native bins at 1625.2936 MHz, both feeds), all 833 frames, 106,624 segments of 512 per scan (ser_00NN.npy, hashed in SER.sha256, kept out of git for size); P3W-D's statistics and shift null computed block-wise in single precision (lean.py), checked against P3W-D's 32-frame result before use (all six families: same pair, same score to six decimals, same p).

## Reading

1. **The 32-frame candidate does not persist.** P3W-D's ON0017 Y+ pair 217–293 (0.065 over 32 frames) is at full length 0.0026 in ON0017, and 0.0008–0.0037 in the other five scans, all at the single-pair noise floor (about 1/√106,112 ≈ 0.003). It was a fluctuation of the first 32 frames.
2. **Two new candidates on the ON scans' target slice** (of 18 ON families; about 0.9 expected):
   - **ON0015 Y+, pair 422–440, p 0.025.** Both halves hold it (A 0.0105, p 0.0029; A 0.0133, p 0.0001). Both adjacent OFF scans sit below their own surrogate medians at the pair (OFF0014 0.0018, OFF0016 0.0010, against medians of 0.0026), so the location test passes. **It fails gate 4**: in the same scan's hidrift slice (173 kHz away), the pair stands above every surrogate (0.0295 against a maximum of 0.0236; ctrl25k quiet, 0.0028 against 0.0278). Gate 4 was read on the 32-frame crops, as the plan says, because the full-length control slices were not kept.
   - **ON0017 X−, pair 192–204, p 0.05.** Both halves hold it (p 0.0014, 0.0001); the control slices are quiet; it **fails location**: OFF0016 carries the same coupling at the pair (0.0058 against a surrogate median of 0.0027, a maximum of 0.0058), an ON-to-OFF excess ratio of 3.07, under the plan's 4.
3. **The aggregate is chance**: 2 of 36 family tests at p ≤ 0.05 (ON0015 Y+, ON0017 X−) against 1.8 expected.

**Verdict under the plan: no lead.** ON0015 Y+ 422–440 is the nearest the P3W line has come: it holds in both halves, is absent from both adjacent OFF scans, and fails only because the same bin pair couples in another slice of the same scan, which points to the instrument (a relation at a fixed position in the channelization, in a slice 173 kHz away) rather than the sky.

## What would settle ON0015 Y+ 422–440

Gate 4 at full length: stream the hidrift and ctrl25k slices of ON0015 alone (about 0.9 GB) and read the pair there with the full-length null. If the pair couples in the control slices at full length too, it is instrumental; if it does not, it stands as the line's first candidate to pass all four gates, and wants the other ON scans and the OFF scans at the same pair read again under a new frozen plan.

Products: PLAN-P3W-D2.md, p3wd2s.py, p3wd2.py (unused after amendment 1), lean.py, check_lean.json, the FROZEN files, SER.sha256, p3wd2_00NN.json, p3wd2_gates.json and this file, hashed in P3W-D2-PRODUCTS.sha256. The .log files are console logs and are not hashed.
