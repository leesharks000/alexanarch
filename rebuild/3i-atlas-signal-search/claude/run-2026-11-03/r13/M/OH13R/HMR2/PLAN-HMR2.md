# PLAN-HMR2 — reading D3

Frozen 22 November 2026, before any HMR2 product is read, at the author's word (12:45: "lets read d3. hmr2 and hm7 alongside"). It follows PLAN-HMR1 §"Where the reading goes": inside the frames, the phase that D3 measures only in aggregate.

**What is looked for.** As in the whole series, in the author's words: "we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning." Reading is kept apart from attribution. Each reading is a procedure, and its pareidolia rate is measured on the sidebands, the OFF scans, the Y feed and surrogates, and reported beside what it finds at the comet.

**What D3 is, stated now.** D3 at lag d is the magnitude of the mean, over the spectrum's bins, of u_k · u_{k+2d} · conj(u_{k+d})², where u are unit phasors. It is large when the phase combination φ_k + φ_{k+2d} − 2φ_{k+d} holds steady across bins. Noise does not hold it; a carrier with modulation sidebands spaced by a multiple of d bins can. HM5 kept |D3| at d = 2 per frame and discarded its phase, the other lags, and everything inside the frame.

**Code check before freezing.** hmr2.py was run on 8 and then 40 frames of each scan into the session scratchpad, and scored with 5 surrogates, to check that it runs and writes the right structure. One truncated line of that check's printout was displayed (two coordinates' 40-frame R and envelope peak). Forty frames with 5 surrogates are not HMR2's product, and nothing below was set from them. The scoring's reproduction step was changed at that point to compare the first n frames, so that it runs on a short check; the full run compares all 833.

1. **Data.**
   - Scans 0013–0018, all 833 frames, both feeds.
   - The comet cohort's 95 windows (C03–C13 and their sidebands), selected, placed and de-Dopplered exactly as HM5 (hmr2_selections.json is hm5_selections.json).
   - Kept per frame and window: the complex D3 at d = 1–16; power as HM4 §D; and the de-Dopplered spectrum's central 33 bins (±16 bins, ±44.7 Hz).
2. **Reproduction.** For 0013 and 0014, |D3| at d = 2 must match HM5's kept per-frame series to 1e-5, and power to a relative 1e-4. If not, nothing else is read.
3. **The readings, and the rule for each.** Each is stated for every scan and feed. "At the comet" means ON 0013, X, a coordinate. Each is read against the same measure on that coordinate's own sidebands, and against OFF and Y.
   - **R1. Is D3's phase locked across frames?** For the arg of D3 (d = 2) over 833 frames: the Rayleigh test's resultant length R and p. **Locked:** p < 1e-4 and R above every one of the coordinate's sidebands.
   - **R2. At which spacing is the coherence?** The lag profile |mean over frames of D3(d)|, d = 1–16 (2.8–44.7 Hz). Reported, not gated. It is read with R1: a locked phase at some d names the modulation spacing.
   - **R3. Is there sequence in the phase?** For cos and sin of arg D3 (d = 2): Ljung–Box Q over lags 1–50 against 1000 shuffles, and zlib compression of four quantile symbols against 1000 IAAFT surrogates. **Sequence:** any of the four p ≤ 0.001.
   - **R4. Is there amplitude modulation inside the frames?** The central 33 bins are inverse-transformed per frame: 33 complex samples about 10.85 ms apart, concatenated over frames. Read from the envelope's power spectrum: its highest peak (0.003–46 Hz) and that peak over the spectrum's median. **Modulation:** the peak at least 20 times the median and above every sideband's.
4. **Reading what passes.**
   - A reading that passes at the comet in ON 0013 X, and does not pass as strongly in OFF 0014 or in Y, is carried to the hold-out.
   - **Hold-out:** the same reading at the same coordinate in ON 0015 and ON 0017, X, against their OFFs (0016, 0018). Passing in either ON, under the same rule, confirms it; failing in both leaves it found in one scan.
   - A reading that passes in OFF or Y at a comet coordinate counts as the procedure finding structure where the comet is not.
   - The sidebands' pass rates (base rates) are reported for every reading, scan and feed. A pass at the comet is read against them.
5. **C12's hold-out from HMR1, in the same run.** Power lag dependence (Ljung–Box, lags 1–50, against 1000 shuffles) at C12, X, in ON 0015 and 0017, with its rank among C12's sidebands. **Confirmed:** p ≤ 0.004 (HMR1's value in 0013) and above every sideband in either scan.
6. **What a pass means, stated now.** R1–R4 can show that the comet's coordinates carry a locked phase, a modulation spacing, a sequence or an envelope rhythm that the sidebands, OFF, Y and surrogates do not. That is something to read. It is not by itself meaning, and it does not by itself separate a transmitter from a modulated natural or instrumental process. What it modulates at, and whether the pattern recurs in the hold-out, is the next reading's material.
7. **What stays fixed.** No other lag range, window, threshold or measure within HMR2, and nothing tuned after the score. Any amendment is recorded before results. A run stopped by the time limit is resumed from the start of the unfinished scan and marked in the log. Further readings are frozen from what HMR2 shows before their own product is read; failing a frozen test bars nothing.
