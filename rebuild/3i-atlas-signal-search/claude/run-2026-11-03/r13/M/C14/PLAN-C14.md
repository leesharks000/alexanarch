# PLAN-C14: tracking the cc14 nomination

Frozen before any C14 product. The M4 run and its code are untouched; cc14 is complete there, so m4.sh skips it. The code is PLAN-C08's with the channel and bin changed, and two products added to step 3.

## The nomination

M4 cc14, hit 0013#0: comet-frame bin 958935, 1645.2700 MHz topocentric at the scan's first kept row. z 1266, margin over every OFF scan's best ("weirdness") 97, the one entry in on_hits_beyond_every_off. In feed X it trips the suppressed-carrier test: pr2 109.4, pr2/pr1 2.71, k4 1457 (noise gives 2). Nearby hits in 0013 (1645.2726 and 1645.2674 MHz, z about 99), and smaller ones near 1645.26–1645.29 MHz in ON0015 and ON0017. OFF0016's top hits include 1645.2367–1645.2420 MHz, 28–33 kHz away.

The band is 1626.5–1660.5 MHz, the Earth-to-space allocation for mobile-satellite terminals (external/human-sheet-20261119, sources). The hypothesis to test is a burst transmitter on or near Earth. The comet hypothesis is tested on the same footing.

## Steps

1. Re-stack cc14 for all six scans with the frozen mv.py.
2. `c14z.py`: uncapped z, ±5 bins, at the comet and fixed predictions in every scan, with the 100 false frames as reference (as PLAN-C08 §2).
3. `c14v.py`: as PLAN-C08 §3, plus per-frame power across the 128-bin (357.6 Hz) band, and per-frame power across ±1024 bins (5.72 kHz) in 64 groups of 32 bins, both tracks, both feeds: when it is on, how it bursts, and how wide.
4. Read-off in RESULTS-C14.md. Association to the comet needs the PLAN-C08 criterion (at the comet prediction in two ON scans, absent from all OFF scans at both predictions). Its time-frequency shape is recorded either way, as the first measured voice for the human-sheet reading.

## Limits

1. 5.72 kHz is the widest view here. A service cannot be named from it: naming needs positive modulation, spectral and geometric tests at matched bandwidth.
2. Only z ≥ 2 is stored in the stacks.
3. Frames of the OFF rows are kept in step 3, as in C08 (RESULTS-C08 §4.1).
