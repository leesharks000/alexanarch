# Results: the comet frame under satellite clutter, GBT 1609.9–1630.4 MHz (plan PLAN-sat.md, sha256 5c817090…; run 2026-11-05)

Verdict: CLEARS. None of the seven coarse channels exceeds its false frames, trimmed or untrimmed: trimmed, 0 of 7 EXCEEDS (a lead needed 2). Nothing steady in the comet's frame stands above chance under the satellite power of 1609.9–1630.4 MHz in the Green Bank cadence of 2025-12-18, at this detector's gate.

| Channel | Centre (MHz) | Untrimmed true | Untrimmed false frames | Trimmed true | Trimmed swap | Trimmed false frames | False max ON−swap | Verdict (trimmed) |
|---|---:|---:|---|---:|---:|---|---:|---|
| blc23_cc20 | 1628.906 | 6 | 3.25 ± 1.59 (max 8) | 4 | 1 | 3.23 ± 1.54 (max 7) | 6 | BOUNDS |
| blc23_cc21 | 1625.977 | 281 | 283.88 ± 22.89 (max 369) | 82 | 106 | 80.47 ± 15.9 (max 148) | 31 | BOUNDS |
| blc23_cc22 | 1623.047 | 187 | 165.88 ± 18.28 (max 214) | 16 | 385 | 16.1 ± 5.69 (max 32) | -272 | BOUNDS |
| blc23_cc23 | 1620.117 | 153 | 135.47 ± 14.17 (max 164) | 232 | 279 | 205.72 ± 30.28 (max 348) | -27 | BOUNDS |
| blc23_cc24 | 1617.188 | 254 | 246.38 ± 17.92 (max 293) | 108 | 515 | 90.0 ± 19.79 (max 166) | -363 | BOUNDS |
| blc23_cc25 | 1614.258 | 4 | 2.95 ± 1.75 (max 8) | 5 | 3 | 3.02 ± 1.75 (max 8) | 6 | BOUNDS |
| blc23_cc26 | 1611.328 | 3 | 3.17 ± 2.04 (max 8) | 3 | 7 | 3.75 ± 1.95 (max 8) | 7 | BOUNDS |

What the trim did. In the Iridium channels it removed most of the clutter in three (1626.0, 1623.0 and 1617.2 MHz: the false-frame means fall from about 284, 166 and 246 to 80, 16 and 90) and left the comet frame inside the false frames each time. At 1620.1 MHz the trimmed counts rise in the true and false frames alike (153 to 232 true; 135 to 206 false mean): there the five largest rows do not carry the satellite power, which is spread more evenly through the scans, and the robust scale of the trimmed sums is narrower. The comparison stays within frame and stays bounded. In 1623.0 and 1617.2 MHz the trimmed swap counts (385 and 515) far exceed the ON counts: after trimming, features steady through the reference scans and absent from the ON scans dominate those channels; they are recorded here and belong to the OFF pointings, whatever their source. The channels outside Iridium's 1616–1626.5 MHz (1628.9, 1614.3, 1611.3 MHz) are quiet in every frame.

Every trimmed true-frame cluster is listed in sat.json with its rest and topocentric frequencies, its six scans' z (trimmed and untrimmed) and its offset from the nearest Iridium channel centre; as description only, none lies within 590 Hz of a channel centre.

Deviations. The plan's header gives its time as about 14:25 EST; it was written at 14:08 EST (file time), before the first fetch at 14:13; recorded in the commit that froze it. No other deviation: channels, procedure, null, trim and decision ran as frozen.

Out of reach, as the plan records: the Starlink direct-to-cell downlink at 1990–1995 MHz (Parkes blc12 is empty in the public directory; the GBT L-band nodes end at 1688.97 MHz) and burst timing (no public raw voltages).

Files: PLAN-sat.md, run_sat.py, cf.py, fetch_cc.py (as in lheld/), sat.json (per channel, per frame, untrimmed and trimmed counts and every trimmed true-frame cluster), run.log. Raw spectra were fetched by name from the public directory and deleted after each channel; their header JSON files stay in raw/, outside the tree.
