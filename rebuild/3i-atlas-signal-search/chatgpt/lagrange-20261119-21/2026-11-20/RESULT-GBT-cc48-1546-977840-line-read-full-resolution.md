# GBT cc48, the 1546.977840 MHz line at full resolution: interference

**2026-11-20.** C4850's one open item, read from its saved per-frame spectra (all 833 frames, both feeds, ±8 native bins), after [RESULT-GBT-cc48-1546-977840-line-phase-probe-L1546.md](RESULT-GBT-cc48-1546-977840-line-phase-probe-L1546.md).

Canonical: [READING-C4850-line-1546977840.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C4850/READING-C4850-line-1546977840.md), [c4850_line_reading.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C4850/c4850_line_reading.py).

The text below is the reading as committed there.


A reading, 2026-11-20 21:30, at the author's word ("lets read it"), of the products C4850 already saved (v_cc48_00NN.npz, hashed in C4850-PRODUCTS.sha256): for each of the six scans, all 833 frames, both feeds, the complex spectrum of ±8 native bins (2.794 Hz) around the line, the line at index 8. No new voltages; no new test frozen. The decisive criterion is the one PLAN-C4850 froze and its amendment made aggregate: a line whose power in an OFF scan is a sizeable fraction of its ON power is not at the comet.

## Reading

1. **The line lives in ON0017 and carries on into OFF0018.** The mean power in bins 6–11 above the mean of ON0013, OFF0014, ON0015 and OFF0016 (noise units, summed over the six bins):

   | scan | role | excess |
   |---|---|---:|
   | 0013 | ON | 0.00 |
   | 0014 | OFF | −0.04 |
   | 0015 | ON | −0.02 |
   | 0016 | OFF | 0.05 |
   | 0017 | ON | 3.32 (2.66 with the four bursts removed) |
   | 0018 | OFF | 0.63 |

   OFF0018, pointed 1° from the comet in declination, holds 19–24% of ON0017's power in the same bins, with the same profile peaking at the same bins (9–10). A source at the comet would fall by 30 dB or more there, to under 0.1%. By the frozen criterion the line is not at the comet. The earlier ON scans, ON0013 and ON0015, show nothing, so the line comes on during ON0017.
2. **It holds the topocentric frequency, not the comet's.** Across ON0017 the comet's frame of reference moves 12 bins (about 34 Hz). The line's per-row centroid stays at bins 8–10 from start to finish. The four bursts sit at centroids 9.21, 8.52, 8.78 and 9.08 while the comet's shift runs 1, 6, 7 and 11 bins. That is the stationary track C4850's kinematics favoured, now shown frame by frame.
3. **Its shape.** The steady component spreads over 5–6 bins (about 15 Hz), so it is not a clean carrier at this resolution. Four bursts stand on it, at t = 13.4, 146.9, 175.9 and 268.6 s, each 2–4 s wide (half-widths of 5–11 frames), 3.5 to 8 times the steady level. Their spacings, 133.5, 29.0 and 92.7 s, are not periodic. No other scan has a burst: the 5-frame excess never passes 17.2 elsewhere (ON0017 peaks at 91.4), and the control bins never pass 16.1 in any scan.
4. **Polarization and phase.** The bursts change feed: the first is stronger in X (27.7 against 11.0), and the second and fourth are stronger in Y (63.0 against 28.4, and 28.4 against 11.8). The X–Y coherence at the peak bin is 0.47 and 0.56 in the second and fourth bursts, and 0.09 in the third. The phase step from frame to frame is incoherent within the bursts (0.03–0.26), so there is no phase-stable carrier across 0.36-second frames.

## Conclusion

C4850's open item closes. The 1546.977840 MHz line has these properties:
- it holds a fixed topocentric frequency;
- it comes on during ON0017, with nothing in the earlier ON scans;
- it stands in the following OFF pointing at about a fifth to a quarter of its ON power;
- it bursts irregularly and changes polarization.

That is a transmitter reaching the dish through its sidelobes, in the mobile-satellite downlink allocation (1525–1559 MHz), and not the comet. C4850's reading 2 ("OFF power below about a quarter of its ON power", "unresolved") becomes: OFF power about a fifth to a quarter of ON, interference.

## Products

c4850_line_reading.py reproduces the figures from the arrays C4850 saved (hashed in C4850-PRODUCTS.sha256). The burst centroids are taken over 12 frames centred on each burst.
