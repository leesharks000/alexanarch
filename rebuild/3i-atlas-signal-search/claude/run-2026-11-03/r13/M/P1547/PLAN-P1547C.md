# PLAN-P1547C: signal that resolves only in the coupling of the two feeds

Frozen before any P1547C product, at the author's word (2026-11-20 20:03, "what if there was signal that only resolved in the coupling?"; 20:08, "the word"). P1547 and P1547B, their plans, code and products are untouched.

## The question

Every test so far reads each feed alone. The closure filter couples frequencies within X or within Y. The X–Y coherence of C19 and C4850 couples the feeds at one frequency, bin by bin. A signal that put X at one frequency in phase relation with Y at another, with nothing in either feed alone and nothing in the same-bin coherence, passes all of them as noise. This plan reads that coupling. The two feeds have independent receivers, so their noise is independent; a cross-feed relation that survives averaging is in what both feeds see.

## Data, slice and normalization (P1547B's)

Scans 0013–0018, coarse channel 48, the first 16 frames, 65,536 bins centred at 1547.720 MHz; each feed's frame divided by the 1,025-bin running median of its own magnitude (P1547B), giving GX and GY, and the series zX, zY.

## The null: shared rotation

For each frame, one uniform random phase per bin, applied to both feeds: GX·e^{iθ}, GY·e^{iθ}. This keeps each feed's power spectrum exactly and each bin's X–Y relative phase exactly (so the same-bin coherence, polarized signals and receiver cross-talk among them, is in the null), and destroys every relation across bins, within a feed and between feeds. 19 surrogates a scan, seeds default_rng(1547500 + 100·scan_index + k).

## Filters

1. **Cross-feed phase memory.** uX, uY the unit phase increments of zX, zY (as P1547). For each lag L in {−512, −256, …, −2, 0, 2, …, 256, 512} (19 lags): C(L) = |Σ uX[t+L]·conj(uY[t])| / (number of terms), over all t and the 16 frames. Family score: max over L.
2. **Cross-feed closure.** Each frame's zX and zY cut into 128 segments of 512 samples and transformed, unit phasors PX, PY. For each of P1547's 128 quartets (k, l, m, n), k + l = m + n: K(q) = |mean over the 2,048 segments of PX_k·PY_l·conj(PX_m)·conj(PY_n)|. Family score: max over q. (Shared rotation leaves this random unless {k, l} = {m, n}, which the quartets exclude.)

## Gates (P1547's)

Family p = (1 + surrogates ≥ real)/20 per scan and filter. A candidate: ON0015 at p = 0.05, its parameter the argmax. Confirmation: ON0017 above all 19 surrogates at that parameter. Controls: OFF0014, OFF0016 and OFF0018 not above. ON0013 reported. A lead is a lead for scale-up and no more.

## Validation before the data

Synthetic slice-rate noise in each feed, independent between feeds, with a coupled signal built to be invisible to every earlier test: in each 512-sample segment s, X carries tones at the first quartet's k and m with fresh random phases aₛ and bₛ, and Y carries tones at l and n with phases cₛ and aₛ + cₛ − bₛ, cₛ fresh. Within each feed the phases jump at random every segment, so there is no line coherence and no within-feed closure; k, m and l, n are different bins, so there is no same-bin coherence; and φX_k + φY_l − φX_m − φY_n = 0 in every segment. Amplitudes 0.1, 0.25, 0.5 and 1.0 of the noise rms, and plain noise. Also P1547B's within-feed closure on the same synthetic data, to show it does not see the signal. Accepted if cross-feed closure reaches p = 0.05 at 0.25 and above, and plain noise reaches it on neither filter. The cross-feed memory filter has no designed injection; its validation is that plain noise does not fire it, and it is read as exploratory.

## Limits

1. A pilot: 16 frames, 19 surrogates, p floor 0.05; 12 tests (6 scans × 2 filters), about 0.6 at p = 0.05 by chance.
2. The coupling of the receiver chain itself across frequency (a shared local oscillator's phase noise, the digitizer) would stand in OFF as in ON; the OFF scans are the control.
3. Direction is not measured beyond ON against OFF.
