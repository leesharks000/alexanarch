# RESULTS-absorb-calib (plan absorb/PLAN-absorb-calib.md, sha256 62d0a126...)

Data as planned: GBT blc23 rawspec.0000, 2025-12-18, scans 0013-0018. Comet range-rate at the GBT -1.898 to -1.858 km/s (one day before closest approach), so the comet and dish frames lie within about 10 kHz of each other at 1.6 GHz. Deviation, recorded: the first ON scan (0013) has no preceding OFF; its pair uses 0014 alone.

Depth at line centre (mean within +-4 kHz, 2.8 kHz bins, cubic baseline over +-60 kHz), in units of the off-line scatter; negative is absorption. Rank = controls (of 40 offsets at +-15 to +-55 kHz) at or below the centre value.
- OH 1665.4018, comet frame: +0.64 (rank 37/40); without 0017 +0.32. Dish frame +0.85.
- OH 1667.3590, comet frame: -0.35 (rank 18/40); without 0017 -1.18 (rank 6/40). Dish frame +0.78.
- OH 1612.2310, comet frame: +0.03; dish frame -0.21.
- Per pair, comet frame: 1665 (0013, 0015, 0017) -0.24, +0.83, +0.84; 1667 -0.58, -0.87, +0.60; 1612 +0.58, -0.26, -0.74.

Sensitivity. Off-line scatter 0.61-0.67 x 10^-3 of the system power per 2.8 kHz bin at the main lines; three-sigma limit on a line-centre dip 1.06 x 10^-3 (1665) and 1.17 x 10^-3 (1667). With an assumed GBT L-band system equivalent of about 10 Jy (Tsys about 20 K, gain about 2 K/Jy; the public product is uncalibrated, so this conversion is approximate), about 11-12 mJy. MeerKAT's October depths were -8.4 +- 3.1 and -14.2 +- 3.4 mJy.

Reading. The comet's OH absorption is not recovered on 2025-12-18. The data could have seen it only near its October strength (about 1667 at 14 mJy, near the three-sigma limit), and by mid-December, seven weeks past perihelion, the outgassing would be expected to have fallen. The calibration therefore sets the floor: a dip on the object has to be deeper than about 1 x 10^-3 of the system power over a few kHz to show in this data. Physically, a small body cannot dim a measurable share of a beam several arcminutes wide (the nucleus covers about 10^-11 of it); only gas spread across the coma can absorb at that level. A notch search on the narrowband products elsewhere is therefore a search for coma-scale absorbers, at a sensitivity this calibration shows to be below the known natural one.
