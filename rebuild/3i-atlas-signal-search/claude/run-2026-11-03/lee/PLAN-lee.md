# PLAN-lee: the global look-elsewhere count for the thirteen

Frozen 2026-11-04 before any channel of this survey was computed. The sha256 of this file is recorded in the runner and the results.

## Question

Every null so far (false range-accelerations, time-shuffled rows, role partitions, phase-randomized rows, §7.1 and §7.18) shares coarse channel 7 of blc23 and the 2.5/2.0 cut. They measure how unusual 13 is in that channel. They do not measure how often a channel of the same cadence gives a comet-frame excess of that size when the procedure is run across the band. This survey runs it across the band and places coarse channel 7 among all channels.

## Data

Breakthrough Listen GBT, 2025-12-18, rawspec.0000.h5, scans 0013–0018 (ON 0013, 0015, 0017), nodes blc22, blc23, blc24 and blc25: 256 coarse channels of 2.93 MHz covering about 1126–1876 MHz, the L-band receiver's range. blc21 (1876–2064 MHz) and blc26 (939–1126 MHz) lie outside it and are not surveyed. Each channel is read by HTTP range reads (the reads of lheld/fetch_cc.py, held in memory).

## Procedure

Per channel, the procedure of lheld/run_lheld.py unchanged: x/median − 1, 3-channel boxcar, comet path sum (JPL Horizons range-rate at the GBT), robust z, the nine DC channels zeroed, rest-frame alignment, ±1 channel tolerance, min ON ≥ 2.5 and all OFF < 2.0, 10 Hz clustering; the true frame, the swap, and the 40 false range-accelerations of seed 11. The sixteen channels already computed with this procedure and seed are taken from their results without recomputation: blc23 coarse channel 7 (comb/comb.json B0) and the fifteen of lheld/lheld.json.

Per channel: T (true count), swap, null mean μ, sd σ, maximum, the largest false ON−swap difference, E = (T − μ)/max(σ, 0.5), and FLAG = T above every false frame and T − swap above every false frame's difference (the lheld replication condition).

## Rule

- p_LEE = the fraction of the 256 channels whose E is at least coarse channel 7's E (4.52), coarse channel 7 included; its smallest possible value is 1/256.
- N_FLAG = the number of channels flagged, against a chance expectation of about 256/41 ≈ 6.2 if each channel's true frame were exchangeable with its forty false frames.
- The flagged channels are listed with their frequencies and the allocations they fall in.

Reported as measured; no verdict word is attached to p_LEE beyond its value. If the survey cannot finish all channels, the completed ones are reported with the count, and p_LEE is computed over them.

## Deviations

Recorded in RESULTS-lee.md with their reasons.
