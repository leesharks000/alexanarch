# PLAN-P3W-D: the two-part signal, fourth plan — the shift without wraparound

Frozen before any P3W-D product and before any telescope data were read, at the author's word (2026-11-21 10:44, "lets develop the fourth version"), on RESULTS-P3W-C. PLAN-P3W (sha256 bd3d128b…), PLAN-P3W-B (sha256 eca84bad…) and PLAN-P3W-C (sha256 12a06e36…), their code and their validations stand as they are.

The two changes below are the ones RESULTS-P3W-C names. The first was chosen after the diagnostic diagC (synthetic data only, not frozen), which compared the circular shift with a shift without wraparound on the two five-tone controls. That diagnostic is the only basis for the choice, and no telescope data have been read under any of the four plans.

## What changes from PLAN-P3W-C, and only this

1. **The null: a shift without wraparound.** Let S be a slice's segment count (4,096) and W = 512. The real statistics are computed on segments 0 to S − W − 1 (3,584 segments). Each surrogate reads each bin's sequence from its own offset, drawn uniformly from 0 to W, over the same 3,584 segments: bin k of a surrogate is P[L_k + s, k] for s = 0 … S − W − 1. X and Y bins draw independent offsets.
   - There is no seam. A steady tone's run of phases stays one run, so a locked pair's surrogate lock is the real lock with a different constant offset, of the same size.
   - The searched-for signal, whose components are random in each segment, is broken wherever two bins' offsets differ, which is all but about 1 in 513 pairs in any surrogate.
   - It is used everywhere the null is used: the family p, the surrogate values at the pair, and the location and control tests at a candidate's pair.
   - The cost is a shorter window, a sensitivity factor of about √(3584/4096) ≈ 0.94 in coupling.
2. **Controls judged as noise is judged.** Each control is run in five realizations with fresh noise and fresh seeds; a control passes if at most 10% of its family tests reach p ≤ 0.05 (at most 3 of 30). An exact null passes this with probability about 0.94.
3. **Acceptance.**
   - Each of the four forms (sum and difference, within X and across feeds) reaches family p ≤ 0.05 at the injected pair at per-bin amplitude ratio 0.5. 0.25 is reported, not required.
   - In 20 noise-only trials, at most 12 of 120 family tests reach p ≤ 0.05.
   - Each of four controls passes by the rule in 2: one stationary tone; five stationary tones at the same fractional bin (0.37); five at mixed fractional bins (0.11, 0.37, 0.52, 0.68, 0.90); an uncoupled pair at 0.5. Amplitudes as in PLAN-P3W-C.
   - Reported, not required: the burst control of PLAN-P3W-C, one realization.
4. **The holdout in time** (PLAN-P3W's gate 2) is unchanged: the two halves of the full scan, each with analytic p = exp(−S·A²) ≤ 0.01 at the candidate's pair.
5. Everything else is PLAN-P3W-C's, and through it PLAN-P3W's: data (C21's first 32 frames saved by N1625, scans 0013–0018, slices target, ctrl25k and hidrift), segments of 512, the six families, the 2× power mask and pair exclusions, 39 surrogates, family p = (1 + surrogates ≥ real)/40, gates and limits. If accepted, the six scans are run and read against the gates. If not accepted, the run stops at validation.
