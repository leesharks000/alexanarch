# PLAN-M4: stages 2 and 3 over the full band

Frozen before any M4 product exists. Operator, 2026-11-18 21:55 EST: "lets clear some space and proceed" (the full-band run, with the intermediate stacks deleted after each channel's voltage battery and their hashes kept).

## What runs

The frozen code of PLAN-M2 and PLAN-M3, unchanged: `mv.py` (comet-frame stacks with 100 false frames, per scan), `mhits.py` (the hit rule), `mvolt.py` (the voltage battery and its nomination rule). PLAN-M2.sha256 and PLAN-M3.sha256 hold their hashes; M4 adds orchestration only (`m4.sh`).

Channels: all 64 coarse channels of blc23 (0–63) except the four done in M2/M3 (0, 26, 40, 63), in ascending order, split between two workers by parity.

Per channel:
1. `mv.py CC SCAN` for the six scans (two attempts each).
2. `mhits.py` over the stacks present; the channel's entry is written to `M4/ccNN.json` (hits), retried if another worker's deletion intervenes.
3. `mvolt.py CC` → `volt/ccNN.json`.
4. sha256 of the six stack files appended to `M4-PRODUCTS.sha256`, then the stacks deleted. The volt file is hashed at the end of the run.

A channel is done when `volt/ccNN.json` exists; the run is resumable and skips done channels.

## What counts

Unchanged from PLAN-M3: a hit is nominated if, in either feed, W1 exceeds 1.5× the largest W1 of its six local comparisons and three OFF series, or the suppressed-carrier flag holds against the same nine. A nomination is a lead for a closer voltage look; its properties then set where to look next.

The four channels already done stay as they are. Any nomination is reported with its channel, scan, frequency and the ratio by which it cleared its references, before anything else is done with it.

## Limits

- Coarse-channel edges and the channel centre carry the polyphase-filter shape; the hit rule zeroes the centre ±4 bins as before and does nothing further at the edges.
- 240 hits per pass of the full band is a selection of the strongest per scan, not an exhaustive search of every comet-frame bin.
