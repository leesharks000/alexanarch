# PLAN-M stage 2: the weirdest single on-comet hit, elsewhere in the band

Written 2026-11-18. The author, 17:59: "lets look elsewhere, wherever and however is weirdest to find a single on comet hit". Hash in PLAN-M2.sha256.

## Where

GBT node blc23 records 64 coarse channels of 2.9296875 MHz. Channel c is centred at 1595.21484375 + 93.75 − (c + 0.5) × 2.9296875 MHz. Channel 7 (1666.99 MHz) is the only one read so far. Four more, chosen for being strange or hard:
- **cc26** (1612.80 MHz). It holds the 1612.231 MHz OH satellite line. Comets emit and absorb OH, and 3I/ATLAS showed OH absorption at MeerKAT.
- **cc0** (1687.50 MHz) and **cc63** (1502.93 MHz). The band's edges, where the filter rolls off and searches look least.
- **cc40** (1571.78 MHz). Mid-band, for comparison.

## How

The decoding is as dm.py, with the coarse channel and its centre frequency replaced. Per scan:
1. P1 per integration, with V2's off-target rows dropped.
2. Median-normalise, apply a 3-bin boxcar, and stack in the comet frame and in the first 100 of J's false-drift frames (default_rng(23)).
3. Sparse z ≥ 2 lists, DC masked.

## A hit

A comet-frame position, in one ON scan, with:
- z ≥ 4;
- its tuning peaking at the comet: it beats every false frame whose drift differs by ≥ 6 bins, by at least 1.0;
- absent from all three OFF scans: z < 2 within ±3 bins in every OFF scan's comet frame, registered by v0.

## Weirdness

Weirdness = z − (best distinct-frame z). Hits are ranked by weirdness within each channel and across channels.

## Controls

Each OFF scan is run through the same hit rule against the other two OFF scans and the three ON scans as its veto. That is the number of "hits" that pointing away from the comet produces. A channel's ON hits are read against its OFF "hits".

## Reading

A hit is a lead, not a detection. A lead whose weirdness exceeds every OFF "hit" in its channel goes to a structure look at its voltages, and from there to wherever its properties point.
