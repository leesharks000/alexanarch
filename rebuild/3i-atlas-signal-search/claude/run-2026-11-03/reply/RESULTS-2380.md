# RESULTS-2380 (plan reply/PLAN-2380.md, sha256 e0754a9a...)

Injection (Parkes, before the run): a doublet 10 Hz apart at comet-frame 2380 MHz + 3 kHz, all samples of the three on-source scans, each tone z ~ 6 in the scan average. Recovered as one persistent doublet in the comet frame at the planted offset (D 5.39, 6.91, 5.03 in the three on-source scans); nothing in the topocentric or barycentric frames. No injection was run on the GBT data; the plan required it at Parkes only.

Deviation, recorded: the source position for the barycentric frame was taken from Horizons. Parkes header src 16:54:10.0 -17:34:59.9 against Horizons 253.174, -17.543 deg; GBT header src 10.8454 h, 6.706 deg against Horizons 162.680, 6.707 deg.

Parkes 2025-07-31, blc15 (2 Hz x 15 s): target count 0 in all three frames (topo, comet, bary), swap 0, persistent 0; spacing controls 0, 0. Frequency controls (2380 + k MHz, k = -10 ... +10): topo [13, 18, 15, 35, 14, 8, 9, 2, 3, 2]; comet [11, 4, 17, 26, 7, 0, 9, 0, 2, 3]; bary [22, 7, 13, 13, 13, 12, 12, 0, 3, 1]. lead False in every frame.

GBT 2025-12-18, blc24 cadence 0029, rawspec.0000 (2.794 Hz x 6.08 s, read by HTTP range): target 0 in all three frames, swap 0, persistent 0; spacing controls 0, 0; frequency controls all 0 apart from 2 (topo, 2384 MHz). lead False in every frame.

Reading. No two-tone signal with the Arecibo message's 10 Hz spacing appears within +-15 kHz of 2380 MHz at either telescope, in the dish frame, the comet frame or the barycentric frame, at the detection levels the plan sets. The Parkes target window is quieter than nine of its ten neighbouring controls. The null bounds a doublet persisting through on-source scans (or single-sample at D >= 5) at these sensitivities and dates; it says nothing on other modulations, other spacings, or signals shorter than a sample.
