# Look 3.1 — off the comet, in the MeerKAT hit lists (frozen before any count)

Reading (Loeb, 2026-04-23): "gadgets" seeded from a hitchhiked comet. A body released near 3I/ATLAS shares, to first order, the comet's line-of-sight acceleration as seen from MeerKAT, but need not sit in the comet's beam. Every prior search used the 63 off-target beams only as background. This look reads them as the place to look.

Data: the four public seticore hit lists (S/N >= 6), 64-beam scans only (157 scans; 2025-11-06, 11-19, 11-20, 11-22, 12-19). 2025-11-27 is target-beam only and is excluded.

Predicted drift: JPL Horizons, 3I/ATLAS from MeerKAT (21.4430 E, -30.7110, 1.038 km), range-rate at 10-minute steps; acceleration by finite difference; drift = -f * a / c at each hit's frequency and scan midpoint.

Singleton: an off-target hit (beam != 0) with no hit in any other beam of the same scan within +-2 kHz. Many-beam hits are interference entering the array; a localized source reaches one beam.

Statistic N: singleton off-target hits whose drift lies within +-1.5 drift steps (one step = foff / (nt * tsamp)) of the prediction.

Null: the same count for 40 false accelerations, the prediction multiplied by 40 factors evenly spaced over [-1.5, -0.5] and [0.5, 1.5] with |factor - 1| >= 0.1 excluded (20 each side).

Lead: N above all 40 false counts. If a lead: list its hits; a hit counts toward recurrence if a singleton at comet drift appears within +-5 kHz of the same comet-frame frequency on another day. Recurrence across days is the second criterion.

Also reported, not tested: the same count in the target beam; the false-factor distribution; every singleton at comet drift by day and band. Oddities outside the criteria are logged, not dropped.
