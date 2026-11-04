# Wow!-guided intermittent search — frozen plan (2026-11-03, written before any data in this window is read)

Question. Does public 3I/ATLAS data near the hydrogen line hold a Wow!-like event: narrowband (<= 10 kHz), intermittent (present in one scan or one stretch of one scan), on-source only? Every earlier detector in this search required the signal in all ON scans; this one does not.

Anchors (MHz). A1 1420.405752 (HI rest), A2 1420.4556 (Ehman 1977), A3 1420.726 (Mendez et al. 2025). Each is mapped two ways: (c) emitted at the anchor in the comet's frame, observed at A(1 - deldot/c) with deldot from JPL Horizons at the site and time; (t) received at the anchor, topocentric. Anchor tolerance: +-15 kHz (the 5 kHz Wow! frequency error, the 10 kHz Wow! bandwidth).

Window. Target window 1419.4-1421.8 MHz (covers every anchor under both mappings with the 1977 frame spread). Control windows: the other non-overlapping 2.4 MHz windows inside the protected band 1400.0-1427.0 MHz (1400.2-1402.6, ..., stepping 2.4 MHz, excluding any that overlap the target window).

Data.
- P: Parkes UWL 2025-07-31, node blc05 (.fil, 2 Hz x 15 s, 20 samples, cadence S R S R S R).
- G: GBT 2025-12-18 node blc24 .0002.h5 (2.861 kHz x 1.07 s), all four cadences (0013-0018, 0029-0034, 0045-0050, 0061-0066), ON/OFF alternating.
Both verified open (HTTP 200) before this plan.

Normalisation. Per scan, each channel divided by its median over time, minus 1.

Detector P (Parkes). Frequency boxcars W in {1, 5, 50, 500, 5000} channels (2 Hz to 10 kHz). For each scan, sample and W: robust z across channels of that window (median, 1.4826 MAD). Event: z >= 7 in one sample of an S scan. Veto: any sample of any R scan with z >= 4 at the same W within +-(W + 2) channels (topocentric). Second detector P2 (within-scan persistence): the 20 samples of one S scan summed along the comet's Horizons range-rate path, z >= 6, and in every R scan the same sum < 3 within +-(W + 2) channels. Events within W + 2 channels of each other at the same W and scan count once.

Detector G (GBT). Channel widths W in {1, 2, 4} (2.9-11.4 kHz); time boxcars L in {1, 10, 67} samples (1.07 s, 10.7 s, 72 s, the Wow! transit envelope). For each scan, L and W: robust z across channels of the window per time step. Coarse-channel edges and DC masked as in pulsed.py (channel index mod 1024 >= 1020, <= 3, or within 2 of 512). Event: z >= 7 in an ON scan; veto: any OFF scan of the same cadence with z >= 4 at the same L, W within +-(W + 1) channels at any time. Events within W + 1 channels at the same L, W and scan count once.

Controls. (1) Swap: the same rule with R/OFF as target and S/ON as veto. (2) Every control window, same rule. (3) Injection before reading results: P, a 2 Hz tone at 1420.0 MHz in one sample of one S scan, and a 10 kHz-wide burst in one sample, each at amplitude giving z ~ 10; G, a 1-channel 10.7-s burst and a 4-channel 72-s burst in one ON scan. Each must be recovered; the injection run's counts are not results.

Lead. A lead requires all of: target-window event count (summed over widths) above every control window and above the swap; and at least one surviving target event within the anchor tolerance of an anchor under either mapping. Anything short of that is reported as no lead, with every surviving event listed with its offsets from the six anchor positions.

Outputs. wow/wow_pks.json, wow/wow_gbt.json; code wow/wow_pks.py, wow/wow_gbt.py; this plan's sha256 recorded in each output.
