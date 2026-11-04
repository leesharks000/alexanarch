# PLAN-absorb-calib: can the public GBT data see the comet's own OH absorption? (written before the look)

Purpose. Calibrate a dip (absorption/notch) detector on a natural absorption known to exist: MeerKAT ATel #17473 reports OH absorption from 3I/ATLAS on 2025-10-24 in the 1665 and 1667 MHz lines, peaks -8.4 +- 3.1 and -14.2 +- 3.4 mJy, at about -15.6 km/s, 0.3 km/s channels.

Data. GBT blc23 rawspec.0000, 2025-12-18, cadence 0013-0018 (ON 0013, 0015, 0017; OFF 0014, 0016, 0018), 1501.465-1688.965 MHz, 2.794 Hz x 6.08 s, 49 samples. Lines: OH 1665.4018 and 1667.3590 MHz (main), 1612.2310 MHz (satellite, expected weaker), each in the comet frame (Horizons range-rate at the GBT).

Estimator. No per-channel time normalisation (it would erase a steady line). Per scan, average the 49 samples after shifting each to the comet frame. Fractional ON-OFF: ON / mean(OFF before, OFF after; 0017 uses 0016 and 0018) - 1. Baseline: a cubic fit over +-60 kHz excluding +-8 kHz around the line, subtracted. Rebin to 2.8 kHz (about 0.5 km/s). Average the three ON-OFF pairs (also reported without 0017, whose header position lies 16 arcmin from the comet).

Statistic. Depth at the line centre (mean of the bins within +-4 kHz) in units of the robust scatter of the rebinned spectrum outside +-8 kHz. Controls: the same statistic at 40 offsets spread evenly across +-15 to +-55 kHz, and at the same rest frequency in the dish frame (near closest approach the two frames lie close; both reported).

Reading. A dip at both main lines in the comet frame, deeper than every control, with 1667 deeper than 1665 (LTE ratio 9:5), is a recovery; anything less sets the sensitivity this data allows. Expected noise per 2.8 kHz bin, ON-OFF over three pairs, about 1e-3 of Tsys; MeerKAT's 14 mJy is about 1.4e-3 of Tsys at the GBT (2 K/Jy, Tsys 20 K), so recovery is marginal at best if the absorption held its October strength.
