# PLAN-HM7: the thirteen at Parkes

Frozen before any Parkes data product was read, only headers and directory listings. The author asked (2026-11-22) for "hmr2 and hm7 alongside". HM7 was test 4: the 1667 voltages at ATA or Parkes. The Parkes files were 403 until Matt Lebofsky opened them, which the author reported at 13:21 EST: "matt says it should be fixed now". Matt had already written that no Parkes voltages exist. HM7 is therefore redrawn for the products that do exist: it is a power test in an independent telescope on other dates. It is not a D3 test, which needs voltages.

## What exists (headers read 2026-11-22 13:2x EST)

1. Breakthrough Listen Parkes UWL, node blc07, covering 1600–1728 MHz, holding every candidate (1665.60–1668.43 MHz rest). Each scan has three products:
   - `.0000`: 64,000,000 channels of 2 Hz, 15 s integrations, total power only (nifs 1), float32;
   - `.0001`: 256 channels of 500 kHz at 0.1 ms, XX, YY, Re XY and Im XY;
   - `.0002`: 64,000 channels of 2 kHz, 1 s, nifs 4.
   Sep 12 and Oct 5 are HDF5 (chunks of 2^20 channels); Jul 31 is SIGPROC filterbank.
2. Cadence: the comet pointing (`_S_`) alternates with a reference pointing (`_R_`, 0.5° north in declination).
   - **2025-07-31**: three S and three R, 20 integrations each.
   - **2025-10-05**: three S and three R, 20 each.
   - **2025-09-12**: one empty stub; S scans of 9, 20 and 3 integrations; then S/R three times, 20 each.
   The scored pairs are the three S/R pairs of each session. Sep 12's three earlier S scans (17701, 18085, 18796) are scored and reported, but they enter no rule.
3. Range-rate of C/2025 N1 from the Parkes site (148.2635 E, −32.9984, 0.415 km), JPL Horizons, 1-minute steps, fetched 2026-11-22 and committed here:
   - Jul 31: −24.2 km/s, 2.82 au;
   - Sep 12: −3.7 km/s, 2.55 au;
   - Oct 5: −7.4 km/s, 2.48 au.
   The track drifts at most 2.35 Hz per 15 s integration.

## Windows

The candidates are the thirteen of `oh13/oh13_candidates.json`, at their comet-frame rest frequencies. C01 is folded into C02 (50 Hz apart), leaving twelve windows. C02 is scored as a candidate here; at Green Bank it was the reference window. Each candidate gets six matched controls: the first six of ±3.2, ±6.4, ±9.6, ±12.8, ±16.0 and ±19.2 kHz whose centre is more than 100 Hz from every candidate and from every control already taken. The same windows are used in every session.

## The statistic

For each window, scan and integration k at its mid-time:

- the track channel is the nearest 2 Hz channel to f_rest·(1 − v(t_k)/c), with fch1 taken as the centre of channel 0;
- the ±2.5 kHz strip (2,501 channels) around it is kept and aligned on the track;
- each row is divided by its median.

S(j) is the sum over integrations of channels j−1..j+1, so a 6 Hz width that absorbs the in-integration drift and the half-channel convention. **Z** is S(0) against S(j) for |j| ≥ 30 (60 Hz), excluding ±30 channels around every other window's track: (S(0) − median)/(1.4826·MAD). On synthetic noise Z has mean −0.04, sd 1.05, and 0.3% ≥ 2.5.

Windows whose track comes within 100 Hz of a coarse-channel centre (fch1 − (n + ½)·0.5 MHz, the DC bin) are flagged `dc` and kept out of every rule. They are still reported.

## Rules

- **R1, the Green Bank selection transposed**: in a session, Z ≥ 2.5 in all three S scans and Z < 2.0 in all three R scans.
- **R2, standing apart**: D = mean S Z − mean R Z exceeds D of all of the candidate's own unflagged controls. The percentile among all unflagged controls in the session is reported.
- **Family tests**:
  - the mean D of the scored candidates against 10,000 random equal-size draws of unflagged controls (seed 20261122);
  - the same for G1667 (C08–C11).
- **Replication**: a candidate replicates if R1 holds in at least two of the three sessions.
- **Sensitivity**: a tone on the track, a·σ_k in one channel per integration, is injected into every ON scan of every scored candidate for a in {0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32}. The fraction reaching Z ≥ 2.5 is reported, along with σ per channel as a fraction of the median, so that a threshold can be stated as a fraction of system power in 2 Hz.

## Descriptive, no rule

For G1667 and their controls, the tracked ±20 kHz strip of the 2 kHz product is stored in every IF. It is reported S against R per IF, because the Green Bank contrast was in the X feed. The IF order of the Parkes products is not stated in the headers, so the IFs are reported as IF0–IF3. At 2 kHz a 2 Hz tone is diluted about a thousandfold, so this is reported, not tested.

## What a result can and cannot say

The telescope, the dates and the distance all differ from Green Bank (2025-12-18, X feed, voltages). Nothing scales the Green Bank candidates' power into Parkes flux, so a failure to replicate bars nothing. It means that nothing at those rest frequencies stood above the noise floor HM7 measures. A pass in two sessions, in an independent telescope, on the comet's own track and not at the reference pointing, would be the first evidence for any candidate outside the Green Bank night.

## Files

- `hm7.py`: `extract SESSION`, then `score`.
- The three Horizons tables.
- Outputs `hm7_<session>_<scan>.npz` and `hm7_score.json`.

FROZEN-HM7.sha256 hashes this plan, the script and the ephemerides.
