# PLAN-ocad: the comet frame in the other three cadences of 2025-12-18 (S, C, X)

Frozen 2026-11-17 (about 22:20 EST) before any spectrum of this survey is read. Only the headers have been read (`headers.py`, `headers.json`, sha256 ca07c823…). The sha256 of this file is recorded in the runner and the results.

## Question

The comet-frame detector of §7.15 has been run on the night's L-band cadence (64 of 256 channels, §7.19), on one S-band channel (§7.8) and on the deep-space downlink band in X band (18 channels, §7.21). The rest of the night has never been read in the comet's frame: the S-band cadence (scans 0029–0034, 6 nodes, 1651–2776 MHz), the C-band cadence (scans 0045–0050, 29 nodes, 3939–8251 MHz, never read at all) and the X-band cadence (scans 0061–0066, 31 nodes, 7689–12376 MHz) outside 8398–8451 MHz. Does anything stand in the comet's frame there above chance?

## Data

Breakthrough Listen GBT, 2025-12-18, rawspec.0000.h5 (2.79 Hz × 6.085 s, 49 rows), fetched by name from https://bldata.berkeley.edu/ATLAS/GB_ATLAS/ by HTTP range reads of one coarse channel at a time, held in memory and not stored. Cadences: S ON 0029/0031/0033, OFF 0030/0032/0034; C ON 0045/0047/0049, OFF 0046/0048/0050; X ON 0061/0063/0065, OFF 0062/0064/0066.

Pool. For each cadence, every node's 64 coarse channels. Where two nodes carry the same frequency range (same fch1 in `headers.json`), the node first in name order is the pool's and the other is kept as its twin. Excluded as already run with this detector: S blc23 coarse channel 30 (the 2500 MHz channel, §7.8) and X blc72 coarse channels 60–63 and blc73 0–13 (§7.21).

## Channels

1. Named lines, run first. The channel containing each line's topocentric frequency in the comet frame at the cadence's middle, f_rest × (1 − v/c) with v the Horizons range-rate at the GBT:
   - methanol 6668.5192 MHz (C);
   - OH 6035.0932 and 6030.7485 MHz (C);
   - formaldehyde 4829.6594 MHz (C);
   - OH 4765.562, 4750.656 and 4660.242 MHz (C);
   - methanol 12178.597 MHz (X).
   If two lines fall in one channel, it is run once.
2. Random. The rest of the pool in one fixed random order (numpy default_rng(41) permutation of the pool listed in cadence S, C, X order, node by descending fch1, coarse channel by index), until 64 channels are complete in all.

Stopping rule, fixed here by sample size alone (the operator's ruling of 2026-11-04: "a healthy random sampling is enough, and others can check the rest if theres something worth checking"): 64 channels. The order is written to `order.json` before the first channel is read. Each channel's result is written before the next is read, so a stopped run is a prefix of the order.

## Procedure

Identical to `lee/run_lee.py` (itself `lheld/run_lheld.py` unchanged): x/median − 1; 3-channel boxcar; rows shifted along the comet path (JPL Horizons range-rate at the GBT, 1-minute steps); robust z per scan; 9 DC bins zeroed; scans aligned in the comet rest frame; ON z ≥ 2.5 in all three and OFF z < 2.0 in all three, ±1 channel; 10 Hz clusters; the swap counted the same way; the true frame and 40 false range-accelerations, seed 11, 0.03–1 (× C/1.42e9) km/s². The two changes are the cadence lists and the time origin of the false accelerations: T0 is the cadence's first ON scan start (the deviation recorded for §7.21).

Per channel: T, swap, the false mean μ and sd σ, the false maximum, the largest false ON−swap difference, E = (T − μ)/max(σ, 0.5), and every true-frame cluster's rest frequency.

## Decision

- A channel EXCEEDS if T is above every false frame and T − swap is above every false frame's difference (chance about 1/41 per channel).
- Random channels: with n complete, a lead is a count of exceeding channels whose Poisson chance at mean n/41 is below 2 percent (for n = 56, 5 or more).
- Named-line channels: each one that exceeds is reported by name and gets a replication test, frozen before it is read: its twin node where one exists; for 7689–8251 MHz, the other cadence (C and X both carry it, about 1.5 hours apart); otherwise the next held-out route that can be named.
- Nothing exceeds: those channels are bounded at this detector's gate.
- Every true-frame cluster is listed. Interference-filled channels, with false means above 8, are reported as such and not argued.

## Not covered

The other ~3,400 channels of these cadences; drifts other than the comet's own (apart from the false frames); bursts shorter than 6.085 s; anything below the gate; the delayed-copy and modulation tests, which need voltages these cadences do not have publicly.

## Deviations

Recorded in RESULTS-ocad.md with their reasons.
