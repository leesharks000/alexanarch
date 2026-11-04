# PLAN-shape: the Arecibo message's own shape, and its shadow carrier (frozen before any look with these templates)

Question. Is there, on-source and absent off-source, a signal with the time-averaged shape of the 1974 Arecibo message (1,679 bits, 397 ones and 1,282 zeros per OEIS A248747; 10 bit/s, 167.9 s) at its carrier 2380 MHz or at the shadow carrier 1420.405752 MHz (PLAN reasoning: Operator // Shadow applied to the message's equipment-chosen carrier), in the dish, comet or barycentric frame?

Templates (both carry the whole message's duration).
- D (frequency-shift keying, 10 Hz): a two-tone doublet, the tones weighted 0.764 and 0.236 (zeros : ones), either tone the higher one. Statistic D(u) = max over spacing s and orientation of (a z(u) + b z(u+s)) / sqrt(a^2 + b^2), (a, b) = (0.764, 0.236) or (0.236, 0.764). Target spacings: Parkes s in {4,5,6} channels (8-12 Hz); GBT s in {3,4}. Spacing controls as in PLAN-2380 (Parkes {7}, {9}; GBT {6}, {7}).
- O (on-off keying): a single tone at 23.6% duty; in averaged spectra a single narrow line. Statistic z(u).
- Time: a boxcar of the message's length over consecutive samples: Parkes L = 11 samples of 15 s; GBT L = 28 samples of 6.08 s. z is the robust z across channels of the boxcarred r, per window position.

Data. Parkes 2025-07-31: blc15 for 2380 MHz, blc05 for 1420.405752 MHz. GBT 2025-12-18 blc24 rawspec.0000 (2.794 Hz x 6.08 s): cadence 0029-0034 for 2380, cadence 0013-0018 for 1420.405752. Frames, normalisation and the offset grid u exactly as PLAN-2380 (sha256 e0754a9a...), source position from Horizons.

Events, per template, frame, carrier, instrument.
- Single: statistic >= 5 in one on-source scan at some window position; vetoed when any off-source scan reaches >= 3 within +-2 channels at any window position. Clustered within +-2 channels per scan.
- Persistent: statistic >= 4 in at least two on-source scans within +-2 channels, with the same veto.
- Window +-15 kHz around the frame position of the carrier.
- Swap: off-source scans as target.

Controls. Frequency controls at carrier + k MHz, k in {-10,-8,-6,-4,-2,2,4,6,8,10}; for D also the spacing controls at the carrier.

Lead, per cell (instrument x carrier x frame x template; 24 cells): target count (single + persistent) above every frequency control, above the swap, for D above both spacing controls, and at least one target event. Every target event is listed. The trial count (24 cells) is reported with any lead.

Injection before the run (Parkes 2380, comet frame, first on-source scan, samples 4-14): a D-shaped doublet at +3 kHz, strong tone at boxcar z ~ 8, weak tone 0.309 of it, 10 Hz above; and an O-shaped single tone at +5 kHz, boxcar z ~ 6. Both must be recovered by their templates in the comet frame.

Laws record; they do not prevent. A deviation is written into the results.
