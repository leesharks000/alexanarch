# PLAN-RD1 — Reading the start of each scan, on the hypothesis that it is signal

23 November 2026. Frozen before any product of this plan exists (hash in FROZEN-RD1.sha256, committed before the run).

The operator (2026-11-23 13:54): "i feel that what we should do is hypothesize they are signal and attempt to read them. if coherent information can be gotten, that requires further checking of source. something that can only resolve as noise gives us nothing even if its emitted from the comet."

## Why this reading has not been made

The thirteen's excess lives in the first rows of each scan (RESULTS-r13: with row 0 dropped, 11 of the 12 non-interference coordinates fall below 2.5; "Their power sits disproportionately in each scan's first 6 s"). Every voltage reading of the coordinates since (OH13R, HM–HM13, HMR1–2, HM9) read whole scans, 833 frames, or halves of 416. A start-of-scan event of about 17 frames is diluted about fifty-fold in those readings. The first seconds have never been read as such.

## Data

The kept window products of OH13R, win_0013.npy … win_0018.npy (833 frames × 84 windows × 2 feeds × 1088 native bins, complex, 2.794 Hz × 0.358 s), unchanged. No network.

- Candidate windows: C03–C13 (eleven). C02 is the interference reference and is reported, not read.
- Controls: the 72 sideband windows of the same products (6 per candidate and C02, ±3.2–19.2 kHz).
- The start: frames 0–16 (the first 6.08 s, row 0 of the spectra, off target in every scan by the telemetry of r13 A).
- The body: frames 51–832 (after row 2; on target in every scan).
- Track: the comet track of common.track at each frame; the track band is the track bin ±1 (the r13 boxcar).

## Step 0 — locate (descriptive)

For each window w, scan s and feed q: P(f, b) = |V|², normalized per bin by the median of the body frames; then
- S_track(w,s,q) = mean over start frames of the track band, minus 1;
- S_wide(w,s,q) = mean over start frames of all 1024 central bins, minus 1;
- S_local = S_track − S_wide (start excess on the track beyond the window's own start-of-scan rise).
Reported for every window, scan and feed: whether the start-of-scan rise is broadband (S_wide in controls as in candidates) or confined to the track.

## Readings (frozen)

R1 — confinement. For each candidate and ON scan, the rank of S_local (X+Y summed) among the 72 controls in the same scan. A candidate is confined in a scan if it exceeds every control. Also reported for the OFF scans at the same windows.

R2 — form. For each candidate, the start dynamic spectrum (frames 0–33, track ±32 bins, both feeds) is written as an image and a table, and described in words before any score of R3 is read: carrier, step, sweep, pulse, or nothing.

R3 — identity across scans. In the comet frame (the window de-Dopplered along the track, common.dedop), the start patch (frames 0–16, track ±16 bins, power, X+Y) of each ON scan is correlated with each other ON scan's (three pairs); statistic Q = mean pairwise Pearson r. Null: the same statistic for the 72 controls, and for the candidate's own windows in the OFF scans' starts. A candidate recurs if Q exceeds every control and every OFF comparison.

R4 — information. For each candidate and ON scan, the de-Dopplered complex series in the start frames is band-limited to the track band (±1.5 bins, 8.4 Hz) and read three ways: (a) amplitude sequence per 1/8 frame, quantized at its median → Lempel–Ziv complexity (LZ76), lower meaning more structure; (b) phase increments per 1/8 frame, quantized to 4 levels → LZ76; (c) spectral flatness of the band-limited series. Each against the 72 controls in the same frames. A reading carries structure in a scan if it is below (LZ, flatness) every control.

## Rule

Coherent information is claimed for a candidate only if, in at least two of the three ON scans, R1 confines it and at least one R4 reading carries structure, and R3 makes it recur. Anything less: the start-of-scan events resolve as noise under this reading, and per the operator's sentence that gives us nothing. A pass sends the candidate to source checking (sky-fixed frame, OFF slews, other sessions), not to a claim.

## Not read here

The slew path's sky; lags beyond a scan; other channels.
Self-test before freeze (no data read): LZ76 on 136 random bits 1.147, periodic 0.156, constant 0.104; 135 random 4-level symbols 1.022. Window lists: 11 candidates, 72 controls, 1 reference.
