# PLAN-P3W: a two-part signal that resolves only when a third is added

Frozen before any P3W product, at the author's word (2026-11-21 07:33: "what if it was a tripartite tone that looked liked noise until its third were added, but we had to add the third"; 07:55: "yup, lets freeze & test").

## The target

Two components, at frequencies f₁ and f₂, whose phases wander at random from segment to segment but always so that φ₁ + φ₂ (the sum form) or φ₁ − φ₂ (the difference form) stays constant. Each component alone is noise. Their powers are noise, and they share no frequency, so their same-bin coherence is nothing. Supplied with a third, a steady reference at f₁ + f₂ (or f₁ − f₂) whose phase is constant, the triple X_{f₁}·X_{f₂}·conj(R) holds a fixed phase. Since a constant R only rotates the product, the test needs no reference phase: it is the phase stability of X_{f₁}·X_{f₂} (sum form) or X_{f₁}·conj(X_{f₂}) (difference form) across segments. Every earlier test of the search passes such a signal as noise. P1547 and P1547B were within one feed. P1547C's closure was four-wave, k + l = m + n, all within the data. The C19 and C4850 coherence was same-bin.

## Data

- C21's first 32 frames, saved by N1625 (crops_00NN.npz, hashed in N1625-PRODUCTS.sha256): scans 0013–0018, both feeds, three slices of 65,536 native bins:
  - target, centred at 1625.2936106 MHz;
  - +25 kHz;
  - the high-drift control at 1625.1204237 MHz.
- Each frame's crop is inverse-transformed and the 32 frames concatenated: 2,097,152 samples, cut into 4,096 segments of 512 samples.
- Each segment is transformed with a rectangular window, so that white-noise bins are independent. That gives 512 bins of 357.6 Hz, unit phasors P[s, k] = X/|X|.

## Statistics (six families per scan and slice)

For pairs (k, l):
- sum: A⁺(k, l) = |mean over segments of P[s,k]·P[s,l]|;
- difference: A⁻(k, l) = |mean of P[s,k]·conj(P[s,l])|.

These are taken within X, within Y, and across feeds (X at k, Y at l).

Pairs are excluded:
- with |k − l| < 2, against leakage between neighbours;
- containing a tonal bin, one whose mean power exceeds twice the median bin power of that slice and feed (or of either feed, for cross pairs). The target is coupling among bins that look like noise.

The family score is the maximum of A over the allowed pairs.

## Null

39 surrogates per scan and slice. Each draws one uniform random phase per segment and bin and applies it to both feeds. That keeps every power exactly and every same-bin X–Y relation exactly, and destroys every relation across bins, within a feed and between feeds. Family p = (1 + surrogates ≥ real)/40, floor 0.025. Seeds: default_rng(31625 + 100·scan_index + 10·slice_index + k).

## Gates

1. A candidate: a family in an ON scan (0013, 0015, 0017) at p ≤ 0.05, with its argmax pair (k, l). There are 18 ON-scan families on the target slice; about 0.9 pass by chance.
2. Holdout in time: the same pair, in the same family and scan, in each half of the scan (segments 0–2047 and 2048–4095). Each half must give an analytic p = exp(−S·A²) ≤ 0.01 at that pair, where S is the half's segment count.
3. Location: at the same pair and family in the OFF scans adjacent to the candidate's scan, A is not above that OFF scan's surrogate maximum at the pair. The candidate's excess over its surrogate median must also be at least four times the OFF scans' excess. A coupling as strong in an OFF pointing is not at the comet.
4. Controls: the same bin pair in the two control slices does not pass its own surrogates. A coupling at fixed bin offsets in every slice is instrumental.
5. Whatever passes 1–4 is a lead for scale-up (all 833 frames, the 1547 and 1632 bands) and nothing more.

## Validation (before the data)

- Synthetic: complex noise, independent between feeds, 2,097,152 samples per feed.
- Coupled tones at segment bins f₁ = 137 and f₂ = 301, constant within each segment, with fresh random phases every segment. Four forms:
  - sum within X;
  - difference within X;
  - sum across feeds (f₁ in X, f₂ in Y);
  - difference across feeds.
- Amplitudes in each bin: 0.1, 0.25 and 0.5 of the noise's per-bin amplitude, so each tone is at or below the noise in its own bin.
- Also: 20 noise-only trials, a stationary tone, and an uncoupled pair with independent phases.
- Accepted if:
  - each form reaches family p ≤ 0.05 at the injected pair at 0.25 and above;
  - at most 3 of the 20 noise trials pass on any family;
  - the stationary tone and the uncoupled pair are not flagged.

If not accepted, the run stops at validation.

## Limits

1. A pilot: 32 frames (11.5 s) of one channel, 39 surrogates.
2. Only couplings constant over the scan's 32 frames. A pair whose coupled phase drifts (a Doppler-shifted third) is outside it.
3. The third is a pure tone. Any other third is a key this test does not hold, and a third known only to the sender cannot be found by any test.
