# PLAN-HM9: reading for coherence

Frozen 22 November 2026, before any HM9 product is read, at the author's word (16:19 EST): "lets read for coherence. with the same provisions that we may not know in advance what form coherence takes."

**What is looked for.** As in the whole series, in the author's words: "we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning." Reading is kept apart from attribution.

**Why coherence.** HM6 found X power at C08–C11 rising with the comet's drift in the first pair. HM8 found the same ordering in the later pairs, but no longer standing out from the false cohorts' drift bias. The ordinary account is a property of the X chain in ON acting on drifting windows. It covers the later pairs, but it does not explain the first pair's rank (20th of 380 in power, 1st in D3). Every reading so far has measured power or phase statistics frame by frame. None has asked whether the excess behaves as one source: whether it holds its phase from frame to frame, whether it appears in both feeds at once, and whether the coordinates move together. Receiver noise does none of these. A source may do any of them, or something else.

**The provision.** We may not know in advance what form coherence takes. So the plan has readings of named forms (H1–H3), one open reading that assumes no form (H4), and two stages. Stage 1 reads ON 0013 and OFF 0014 only. Anything seen in stage 1 that no reading names can be frozen as an amendment and tested on the hold-out (0015–0018) before the hold-out is read.

## 1. Data

- HMR2's kept products, read without recomputation. These are, per frame and window, the de-Dopplered complex spectrum's central 33 bins (SP, ±16 bins, ±44.7 Hz) and the X/Y power ratio (P, the centre bin over the mean of 129 bins).
- The comet cohort's 95 windows: the 11 coordinates C03–C13 and their 84 sidebands, 833 frames, both feeds, scans 0013–0018.
- The products were made with continuous de-Doppler (the carry of PLAN-OH13R §1 is in hmr2.py), so a tone fixed in the comet's frame holds a fixed frequency in its window across frames.
- hm9.py checks every product's SHA-256 against HMR2/RESULTS-HMR2.sha256 before reading it. If any differs, nothing is read.
- HMR2's own score read SP for its envelope reading (R4) and nothing else. Nothing below was set from that.

**Code check before freezing.** hm9.py was run on synthetic data only (`selftest`: complex Gaussian noise, with sources added at three coordinates). No HMR2 product was opened. Noise passed none of the readings. Each added source was caught by its own reading:
- a steady carrier 0.3 bin off centre at 0.25 of the noise rms per bin (about 6% of the bin's power) by H2;
- a noise-like source common to both feeds at 0.4 of the noise rms by H1 (γ = 0.144) and H4;
- one series spread over nine X bins with a phase slope by H4, whose form named those bins.

The thresholds this implies: H1 resolves a cross-feed coherence of about γ ≥ 0.11 at the centre bins. H2 resolves a steady carrier carrying about 3% or more of its bin's power. HM8's X excess is 5–7%. H1 is weak for a source polarized wholly along X, which would also leave Y without excess, as observed. This is stated now.

## 2. The readings

Each reading is stated for every scan, feed, coordinate and sideband. "At the comet" means ON 0013 at a coordinate. Each is read against the same measure on that coordinate's own sidebands, against OFF 0014, and against Y. "Centre bins" are bins −2 to +2 (±5.6 Hz).

- **H1. Do the feeds agree?** The cross-feed coherence γ = |Σ X·Y*| / √(Σ|X|²·Σ|Y|²) over frames, at each centre bin; the reading takes the largest. Its p is analytic, for complex Gaussian noise, corrected for five bins. It is also compared with 2,000 circular shifts of Y against X (by 20 to 813 frames). The phase of the cross term is reported.
  - **Coherent across feeds:** p < 1e-4, none of the 2,000 shifts as high, and γ above every one of the coordinate's sidebands.
- **H2. Does the carrier hold its phase across frames?** Per feed:
  - (a) the lag coherence ρ(τ) between frame k and frame k + τ, for τ = 1–8 frames (0.36–2.9 s), at each centre bin, taking the largest, with an analytic p corrected for 40 trials;
  - (b) the frame-axis periodogram at each centre bin, its peak over its mean, which concentrates a carrier coherent over the whole scan, with p corrected for 5 × 833 trials.

  Each is compared with 2,000 surrogates that give every frame an independent random phase. That keeps each frame's spectrum and breaks any carrier across frames.
  - **Carrier:** (a) or (b) at p < 1e-4, none of the 2,000 surrogates as high, and above every one of the coordinate's sidebands.
- **H3. Do the coordinates move together?** The mean pairwise correlation of the per-frame X power ratio P among C08–C11, raw and as first differences, against 10,000 random four-sets drawn from the 84 sidebands. Y is the same. The 11 × 11 correlation matrix of the coordinates and each coordinate's mean correlation with its own sidebands are reported. Gain variation in the chain is broadband and largely cancels in P (centre over mean). A common rise in P among the four beyond the sidebands' is narrowband co-variation.
  - **Common mode:** none of the 10,000 four-sets as high, raw or differenced.
- **H4. The open reading.** It names no form.
  - Each window's frames are taken as vectors of 66 complex values (the 33 bins of X, then of Y), each element normalized by its rms over frames.
  - The reading takes the leading eigenvalue of their coherence matrix at lag 0, and the leading singular value of their cross-coherence between frame k and k + τ, τ = 1–8.
  - Any coherent structure, across bins, feeds or frames, whatever its shape, raises one of these above the noise and leakage that the sidebands share.
  - The leading eigenvector is reported as the form: its share in X and in Y, and the bins and feeds that carry it.
  - Surrogates (200 per coordinate): for lag 0, each of the 66 element series circularly shifted independently; for the lags, an independent random phase per frame and element.
  - **Open structure:** the statistic above all 200 surrogates and above every one of the coordinate's sidebands.

## 3. Reading what passes

1. A reading that passes at the comet in ON 0013, and does not pass as strongly in OFF 0014 or in the other feed, is carried to the hold-out. For H1 and H4 the feeds are read together, so they are read against OFF only.
2. **Hold-out:** the same reading at the same coordinate in ON 0015 and ON 0017, against their OFFs (0016, 0018). Passing in either ON under the same rule confirms it; failing in both leaves it found in one scan.
3. H4's hold-out holds the form fixed. The stage-1 leading eigenvector at that coordinate is applied to the hold-out frames, as the quadratic form u†Γu, against 200 independently shifted surrogates and against the sidebands' values under the same u. So the hold-out tests the form found, not a fresh search.
4. A reading that passes in OFF, or at a comet coordinate in a feed without the excess, counts as the procedure finding structure where the comet is not. The sidebands' pass rates are reported for every reading, scan and feed.
5. **Amendments (the provision).** After stage 1 is read, any structure seen in its reports that no reading names, at the comet and not in OFF, may be frozen as a stated test in AMEND-HM9.md: form, statistic, rule and hold-out. It is hashed and committed before stage 2 is run. Nothing seen in stage 1 changes H1–H4 or their rules.
6. **What a pass means, stated now.**
   - H1 passing says the excess is in the sky, or in whatever the two feeds share, and not in the X chain alone.
   - H2 passing says it is a carrier holding phase longer than a frame.
   - H3 passing says the four OH coordinates co-vary narrowband.
   - H4 passing says there is structure of the form it names.

   None of these is by itself meaning. None, by itself, separates a sender from a natural line or from interference that shares the comet's drift. The OFF scans are the not-interference test.

## 4. What stays fixed

No other bins, lags, windows, surrogate counts, thresholds or measures within H1–H4, and nothing tuned after a score. The seed is 20261123. A run stopped by the time limit is resumed from the start of the unfinished stage and marked in the log. Failing a frozen test bars nothing.

FROZEN-HM9.sha256 hashes this plan and hm9.py.
