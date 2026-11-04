# Frozen plan: comet-frame search across the Parkes band, 2025-07-31 (written 2026-11-03 ~17:55 EST, before any full-band power is read)

Access (checked 2026-11-03 before this plan): PKS_Jul_31_2025 nodes blc00-07, 10, 11, 13-17, 20-26 each list all six .0000.fil scans and serve byte ranges to
the end of every file (22 nodes, 704-1984 and 2112-3648 MHz; blc12, 1984-2112 MHz, is empty; blc08, 09, 18, 19 do not exist). PKS_Sep_12_2025 and
PKS_Oct_05_2025 return HTTP 403 on every node. Public companions for any lead: ATA 2025-07-03 to 07-30 (spectra), GBT 2025-12-18 (spectra), MeerKAT
2025-11-06 to 12-19 (hit lists).

Order: blc07 (1600-1728), blc06 (1472-1600), blc05 (1344-1472) first; then the remaining nodes.

Detector: the oh13 rule on 2 Hz x 15 s data. Blocks of 1,048,576 channels, overlapped by 600; per channel divide by its median over the scan's 20
samples, minus one; 3-channel boxcar; rows summed along the comet path (constant rest frequency, Horizons range-rate at Parkes, per sample centre; the
block centre frequency sets the shifts); robust z per scan per block; scans aligned in the rest frame; source scans z >= 2.5 in all three, reference scans
z < 2.0 in all three, +-1 channel; only the block core (300 channels in from each edge) counted; clusters merged at 10 Hz (5 channels).

Null: the same procedure with (a) the beams swapped (R as target, S as reference) and (b) 20 false range-accelerations (seed 11, the first 20 of the oh13
set: 0.03-1 Hz/s at 1.42 GHz). Per node: true count, swap count, false-frame mean, sd and max, and every true-frame cluster with its six scores.

A node shows a lead only if its true count exceeds every false frame and its true-minus-swap difference exceeds every false frame's. Every cluster is kept
whatever the count. No threshold, block, null or ordering changes after reading.
