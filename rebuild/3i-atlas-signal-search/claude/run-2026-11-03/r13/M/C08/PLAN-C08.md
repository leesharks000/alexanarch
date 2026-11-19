# PLAN-C08: tracking the cc08 lead

Frozen before any C08 product. The M4 run and its code are untouched; cc08 is already complete there, so m4.sh skips it.

## The lead

M4 cc08, hit 0013#1, feed Y: comet-frame bin 787546, 1663.3270 MHz topocentric at the scan's first kept row, z 7.25, W1 29.7 at 0.181 Hz, k4 2.19. In ON0013's top ten only. Its absence from ON0015 and ON0017 is censored: those scans keep only ten hits each, and only z ≥ 2 is stored.

## Questions

1. Is it in ON0015 and ON0017 below the cap, at the bin a comet source would occupy?
2. Is it in the OFF scans at that bin, or at a fixed topocentric frequency (the terrestrial hypothesis)?
3. When within ON0013 is it on: steady, intermittent at about 5.5 s, or a transient?
4. What is its shape in a 357.6 Hz band: line width, sidebands?

## Steps

1. Re-stack cc08 for all six scans with the frozen mv.py (hash 895e3ceb…). This regenerates out2/cc08_*.npz identically to M4's.
2. `c08z.py`: for every scan, read the stored z (frame f0) in ±5 bins around two predictions, with no cap.
   - Comet: p + round(FC·(v0_s − v0_0013)/C/DF), the mapping mhits.py and mvolt.py use.
   - Fixed: bin p in every scan. A stack bin is the topocentric frequency at that scan's first kept row, so a fixed emitter recurs at the same bin, smeared within a scan by the comet-frame tracking.
   - The same windows in the 100 false frames give the reference: the fraction of false frames reaching the same z.
3. `c08v.py`: stream each scan once. Extract ±64 bins per frame around both predictions, tracked in the comet frame as mvolt.py does. Save per-frame power at the predicted bin ±2, and the band's mean spectrum, for both feeds. Save the complex series for ON0013.
4. Read-off goes in RESULTS-C08.md. A finding needs the same feature at the comet prediction in at least two ON scans and absent from all three OFF scans at both predictions. Anything else is recorded as what it is.

## Limits

1. Only the shapes this band can show (357.6 Hz, 2.794 Hz resolution). Wideband structure is outside it (external/inscription-20261119).
2. Only z ≥ 2 is stored in the stacks: below that, absence means z < 2, not zero.
