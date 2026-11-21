# PLAN-P3W-B: the two-part signal, second plan

Frozen before any P3W-B product and before any telescope data were read, at the author's word (2026-11-21 08:22, "the word"), on RESULTS-P3W. PLAN-P3W (sha256 bd3d128b…), its code and its validation stand as they are.

## What changes from PLAN-P3W, and only this

1. **Sidelobe exclusion.** A bin is excluded from every pair if its own segment-to-segment phase advance is steady: self-coherence c_k = |mean over segments of P[s+1,k]·conj(P[s,k])| with analytic p = exp(−(S−1)·c_k²) ≤ 10⁻³. This is in addition to the 2× power mask. A stationary tone's leakage, wherever it reaches, carries the tone's steady advance and is removed. A coupled pair's components, whose phases are fresh each segment, are not.
2. **Acceptance.**
   - Each of the four forms (sum and difference, within X and across feeds) reaches family p ≤ 0.05 at the injected pair at per-bin amplitude ratio 0.5. 0.5 is the sensitivity P3W's validation measured; 0.25 is reported, not required.
   - In 20 noise-only trials, at most 10% of family tests reach p ≤ 0.05 (at most 12 of 120).
   - No family is flagged for any of three controls: a stationary tone; a set of five stationary tones at non-integer bins; and an uncoupled pair at 0.5.
3. Everything else is PLAN-P3W's: data, segments, statistics, pair exclusions, null, seeds, gates and limits. If not accepted, the run stops at validation.
