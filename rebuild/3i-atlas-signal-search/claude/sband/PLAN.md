# Frozen plan: the comet-frame property in another band (written 2026-11-03 ~16:05 EST, before any S-band power is read)

Question: does a beam-sided comet-frame excess, the property of the GBT 1667 MHz thirteen, appear in a band chosen before reading?

Data: GBT blc23 S-band cadence of 2025-12-18, scans 0029 (ON), 0030 (OFF), 0031 (ON), 0032 (OFF), 0033 (ON), 0034 (OFF), rawspec .0000.h5. Coarse channel: the one containing 2500.000 MHz (chosen by round number, before reading).

Procedure: identical to cometframe_raw.py / swapnull.py: per-channel time-median division minus one; 3-channel boxcar; rows summed along the comet path (Horizons range-rate for C/2025 N1 at the GBT site, 1-minute grid); robust z per scan; 9 DC bins zeroed; scans aligned in the comet rest frame; ON z >= 2.5 in all three, OFF z < 2.0 in all three, +-1 channel; 10 Hz clusters. Beam swap counted the same way. Null: true frame plus 40 false range-accelerations, seed 11, 0.03-1 (x C/1.42e9) km/s^2, exactly as in swapnull.py.

Outcomes, stated now: REPLICATES if the true frame's ON count exceeds every false frame and its ON-minus-swap difference exceeds every false frame's. BOUNDS if the true frame's ON count lies inside the false-frame range. Anything between is reported as it falls. No threshold, channel or null changes after reading.
