# PLAN-P3W-C: the two-part signal, third plan — a null that keeps steady tones

Frozen before any P3W-C product and before any telescope data were read, at the author's word (2026-11-21 09:33, "yup lets freeze & run it"), on RESULTS-P3W-B. PLAN-P3W (sha256 bd3d128b…) and PLAN-P3W-B (sha256 eca84bad…), their code and their validations stand as they are.

## Why P3W-B failed, from its own construction

The five-tone control put all five tones at the same fractional bin, bin + 0.37 (p3wb.py). A steady tone's phase advances by 2π times its fractional bin from one segment to the next, so every leakage bin of all five tones advances by the same amount. Two bins that advance together hold a fixed difference phase, which is what the difference families test. In the sum families the two advances add, the pair keeps rotating, and nothing locks. This is why only X−, Y− and XY− flagged. P3W-B's per-bin exclusion removed the strong bins, but not the many faint leakage bins whose pairs the family statistic sums. RESULTS-P3W-B gave this mechanism as "most likely, not tested here"; the control's construction settles it.

The null of P3W and P3W-B, a fresh random phase per segment and bin, destroys a steady tone's advance along with everything else. Steady tones therefore stand as excess against it.

## What changes from PLAN-P3W, and only this

1. **The null.** Each surrogate shifts each bin's sequence of segment phasors circularly in time, by its own random lag, drawn uniformly from 64 to S − 64 segments (S = 4,096). X and Y bins draw independent lags.
   - It keeps each bin's sequence exactly: its power, its self-coherence and its steady advance.
   - A steady tone survives it: a shift changes only the constant phase offset of a locked pair, not the size of the lock. So the null holds the stationary locks.
   - The searched-for signal does not survive it: its components are random in each segment and lock only segment by segment.
   - It is used everywhere the null is used: the family p, the surrogate values at the pair, and the location and control tests at a candidate's pair.
2. **P3W-B's steady-bin exclusion is removed.** The 2× power mask of PLAN-P3W stays.
3. **Acceptance.**
   - Each of the four forms (sum and difference, within X and across feeds) reaches family p ≤ 0.05 at the injected pair at per-bin amplitude ratio 0.5. 0.25 is reported, not required.
   - In 20 noise-only trials, at most 10% of family tests reach p ≤ 0.05 (at most 12 of 120).
   - No family is flagged at p ≤ 0.05 for any of five controls: one stationary tone; five stationary tones at the same fractional bin (P3W-B's control, kept); five stationary tones at mixed fractional bins (0.11, 0.37, 0.52, 0.68, 0.90); an uncoupled pair at 0.5.
   - Reported, not required: a tone at 0.5 switched on and off in step across its bins, in blocks of 32 segments chosen at random. Bursts align bins in time, so this null flags them by construction. A burst is told from the signal by the location test, not by the null: the C4850 and N1625 bursts stand in the OFF scans.
4. Everything else is PLAN-P3W's: data (C21's first 32 frames saved by N1625, scans 0013–0018, slices target, ctrl25k and hidrift), segments of 512, the six families, pair exclusions, 39 surrogates, family p = (1 + surrogates ≥ real)/40, seeds of the form PLAN-P3W gives, gates (candidate, holdout in time, location against the adjacent OFF scans with the 4× excess rule, the control slices) and limits. If not accepted, the run stops at validation.
