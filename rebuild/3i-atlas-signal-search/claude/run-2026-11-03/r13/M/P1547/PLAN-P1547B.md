# PLAN-P1547B: the 1547.72 MHz phase pilot with the lines kept

Frozen before any P1547B product, at the author's word (2026-11-20 20:00, "okay. lets freeze & run it"), on RESULTS-P1547 limit 3: full-resolution whitening removes any line-spectrum signal, so P1547 could see only broadband phase dependence. P1547, its plan (sha256 9a0c7241…), code and products are untouched.

## What changes, and only this

1. **Normalization.** Each frame's 65,536-bin slice F is divided by a smoothed magnitude, not by its own magnitude: M = the running median of |F| over 1,025 bins (scipy.ndimage.median_filter, mode "reflect"), then F/M. This removes the bandpass shape and the noise level, and keeps every line at its height above the local noise.
2. **Surrogates.** For each frame, F/M with its magnitudes kept exactly and its phases replaced by uniform random phases (19 surrogates, seeds as P1547). What the test then measures is the phase relation among bins and frames, with the power spectrum held fixed.

Everything else is P1547's: the slice (65,536 bins centred at 1547.720 MHz), the 16 first frames of scans 0013–0018, both feeds, the two filters with the same lags and the same 128 quartets (seed 20261120), the family statistic, and the gates (candidate in ON0015 at p = 0.05; confirmation in ON0017 at the same parameter above all 19 surrogates; in OFF0014, OFF0016 and OFF0018 not above them).

## What this design will see, said before the run

Any narrowband signal whose phase runs continuously across a frame (an ordinary carrier, a drifting one, a modulated one) holds a phase relation among adjacent bins that random phases destroy, so it will raise phase memory against the surrogates. The filters are no longer selective for unusual structure; they find phase-coherent signals, and the ON/OFF gates do the selection. A lead must therefore pass the location test as C19 and C4850 frame it: present in ON, absent at the same parameter in all three OFF scans.

## Validation before the data

The same code on slice-rate synthetic noise with injections made before normalization, as a signal arrives: (a) a repeated QPSK sequence (64 symbols, 2 samples a symbol), (b) four balanced tones at the first frozen quartet, each at 0.1, 0.25, 0.5 and 1.0 of the noise rms, and (c) plain noise. Accepted if (a) and (b) reach p = 0.05 at 0.5 and above, and (c) does not on either filter.

## Limits

1. A pilot: 16 frames, 19 surrogates, p floor 0.05; 24 tests, about 1.2 at p = 0.05 by chance.
2. The 1,025-bin median (2.86 kHz) treats structure wider than about 1.4 kHz as bandpass; a signal wider than that is partly normalized away.
3. The instrument's own phase structure is not modelled; the OFF scans are the control.
