# PLAN-lheld: the thirteen's property in held-out L-band channels of the same scans (frozen before any of these channels is read)

Question. The thirteen (GBT blc23 coarse channel 7, 1665.53-1668.46 MHz, scans 0013-0018) are a beam-sided comet-frame excess. With scan 0017 now argued to be on target (p17/RESULTS-0017.md), does the same property appear in other L-band coarse channels of the same six scans, read for the first time here?

Channels, by rule: in both L-band nodes of the cadence (blc23, 1501.465-1688.965 MHz; blc24, 1313.965-1501.465 MHz), every coarse channel whose index is 7 modulo 8 (indices 7, 15, 23, 31, 39, 47, 55, 63), excluding blc23 index 7 (the original): 15 channels, 2.93 MHz each. No exclusion for interference.

Procedure: identical to the S-band held-out test (sband/PLAN.md, sha256 ca251bf3...) and to cometframe_raw.py / swapnull.py: per-channel time-median division minus one; 3-channel boxcar; rows summed along the comet path (Horizons range-rate at the GBT); robust z per scan; 9 DC bins zeroed; scans aligned in the comet rest frame; ON z >= 2.5 in all three (0013, 0015, 0017), OFF z < 2.0 in all three, +-1 channel; 10 Hz clusters; beam swap counted the same way; null of the true frame plus 40 false range-accelerations, seed 11, 0.03-1 (x C/1.42e9) km/s^2.

Per channel, as in the S-band plan: REPLICATES if the true ON count exceeds every false frame and its ON-minus-swap difference exceeds every false frame's; BOUNDS if the true ON count lies inside the false-frame range; anything between reported as it falls.

Overall. Under no signal each channel replicates with probability about 1/41 or less; across 15 channels about 0.37 expected. The property replicates in held-out L band if 3 or more of the 15 channels replicate (binomial chance about 0.6 percent); 1 or 2 is reported as consistent with chance; 0 bounds it. Every channel's true-frame candidate frequencies are listed.
