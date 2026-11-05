# Frozen plan: the comet frame under satellite clutter, GBT 1609.9–1630.4 MHz (written 2026-11-05 ~14:25 EST, before any of these channels is read at row level)

Question. The comet-frame test is blind where satellites fill every frame: blc23 coarse channel 23 (1620.1 MHz, inside Iridium's 1616–1626.5 MHz) gave 153 true-frame clusters against 135.5 ± 14.2 in the false frames (lheld/RESULTS-lheld.md), indistinguishable. A source keeping itself just below determinability would be hidden there. Does anything steady in the comet's frame sit under the satellite power in 1609.9–1630.4 MHz?

Why trimming separates them (computed in session before this plan, circular 780 km orbits at 86.4°, Earth rotation, the GBT site, 1,334 visible passes): an Iridium downlink's Doppler rate passes through zero near the horizon, so no minimum rate bounds it; but its frequency stays within 8.4 Hz (three fine channels) for at most 23.5 s, under four rows of 6.08 s. A steady tone at fixed rest frequency is present in every row of every ON scan, and the three ON scans span about 25 minutes, longer than any single pass's dwell.

Data. GBT blc23 rawspec .0000.h5, scans 0013–0018 (the cadence of 2025-12-18), coarse channels 20–26 (2.93 MHz each, 1609.87–1630.37 MHz), fetched by name from the public directory with fetch_cc.py, deleted after each channel.

Procedure. Identical to lheld (cf.py: per-channel time-median division minus one, 3-channel boxcar, rows shifted along the comet path, robust z per scan, 9 DC bins zeroed; rest-frame alignment; ON z ≥ 2.5 in all three, OFF z < 2.0 in all three, ±1 channel; 10 Hz clusters; swap; true frame plus 40 false range-accelerations, seed 11), computed twice per frame:
- untrimmed, exactly as lheld;
- trimmed: at every channel of every scan, the 5 largest shifted rows are dropped before the sum (a steady tone keeps 44 of 49 rows; a satellite crossing loses the rows that carry it).

Decision, on the trimmed count. A channel EXCEEDS if its true ON count exceeds every false frame's and its ON−swap difference exceeds every false frame's (chance about 1/41 per channel). Overall: a lead if 2 or more of the 7 channels exceed (chance about 1.2 percent); one is reported as a channel to hold out, not a lead; none clears the band. The untrimmed counts are reported beside, and do not decide.

Every trimmed true-frame cluster is listed with its rest and topocentric frequencies, its six scans' z, and its offset from the nearest Iridium channel centre (1616.0208333 MHz + k × 41.6667 kHz), as description only.

Out of reach. The Starlink direct-to-cell downlink (1990–1995 MHz): Parkes blc12, which would hold it on 2025-07-31, is empty in the public directory (pks/PLAN-fullband.md), and the GBT L-band nodes stop at 1688.97 MHz. Burst timing needs raw voltages; none are public for these scans.
