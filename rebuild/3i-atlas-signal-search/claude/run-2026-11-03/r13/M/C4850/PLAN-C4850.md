# PLAN-C4850: cc48 and cc50 in the raw voltages

Frozen before any C4850 product. M4, M4b, C19 and their code are untouched.

## The lead

1. M4b's full band gave 287 Class A on the three ON scans against 506 with the roles reversed. Channels whose Class A count exceeds their role-reversed count include cc48 (1546.875 MHz; A 58 against 8) and cc50 (about 1541.0 MHz; A 34 against 3) (RESULTS-M4b.md).
2. Both lie in the mobile-satellite downlink allocation (1525–1559 MHz). Allocation is a prior on interference, not a cut.
3. M4b saved at most 40 events and 15 role-reversed events per channel. In cc48 only 9 of the 58 Class A are among the saved 40. The catalogue cannot carry the question alone.
4. ChatGPT's list puts these two next after cc19 (Lagrange Observatory, PLAN-occupied-bands-comet-matched-discrimination.md, 2026-11-20).

## The criterion (the author, 2026-11-18)

In the comet, not interference, and weird as voltage. Replication is not required; the OFF scans are the interference test.

## The test that drift cannot evade (from C19)

A source at the comet's position falls by 30 dB or more in the OFF pointings, 60′ off, about 8 beamwidths at these frequencies. A line whose OFF power is a sizeable fraction of its ON power is not at the comet, whatever its transmitter does with frequency. This holds for a Doppler-compensating transmitter too (ChatGPT, 2026-11-20 15:08).

## Data

Coarse channels 48 and 50, scans 0013–0018, both polarizations, all 833 frames, streamed by dm.frames. FC = 1688.96484375 − (cc + 0.5) × 2.9296875 MHz. Bin b = N/2 + (FC − f)/DF − 0.5.

## Targets (fixed before streaming)

1. Every saved M4b event of the channel, ON (events) and role-reversed (control_top), at its recorded topocentric frequency.
2. Sixty random positions per channel, seed 4850, none within 500 Hz of a target.

## Products (c4850v.py, one stream per channel and scan)

As C19's c19v.py, with one addition:
1. S: the scan-mean power spectrum, both polarizations.
2. Sc: the scan-mean power spectrum in the comet's frame, each frame shifted by FC·(v(t) − v0)/C/DF before it is summed (v0 at the scan's first frame).
3. R (per-row windows ±128 bins, stored normalized by the window median, with RM), Pf and Pc (per-frame power ±2 bins at the fixed and the comet-tracked bin), V (per-frame complex spectra ±8 bins) for every target.
4. Hashes in C4850-PRODUCTS.sha256.

## Analyses (c4850a.py)

1. Location, per target. Line power above the local median in each scan, at the fixed bin and on the comet track (from Pf and Pc and from S and Sc). For every ON event: the ratio of each OFF scan's power to the ON scan's.
2. Catalogue-free lines. In each ON scan's S and Sc, every peak above z 8 at 1 and 16 bins (z from the local median and MAD in 4,096-bin blocks), within the central 92% of the channel. For each: its power in all three OFF scans at the same topocentric bin and, from Sc, on the comet track; and in the other ON scans on the comet track.
3. Kinematics. Each ON event fitted in its own ON scan; its stationary and comet tracks scored without refit in the other five scans (C19 analysis 4).
4. Polarization and voltage for the ON events as C19 analyses 5–6.
5. Families. The two-sequence search of c19n.py on each scan's catalogue-free line list.

## Reading

1. A lead: an ON line whose power in every OFF scan, at both the fixed bin and the comet track, is below 1% of its ON power (the beam allows far less), and which is at noise in the OFF Sc. Where it appears in another ON scan it should be on the comet track; it need not appear.
2. Interference: OFF power at a sizeable fraction of ON. Then the products say what they can of its mechanism.
3. Anything else is recorded as what it is. A negative is a negative for narrowband lines in these two channels.

## Limits

1. Narrowband, 2.794 Hz; wideband structure is outside it.
2. A source that fades or switches can mimic an ON-only line in one scan pair. A lead is checked against both neighbouring OFF scans and its time structure in Pf before it is called one.
3. Direction is not measured beyond ON against OFF.

## Inputs (sha256)

b77d23008668e9ee100cf4dd780cfa38706494d402697d4ec78c86c7fb0cb455  M4b/events/cc48.json
21944c678d479f34f4b6133190bc0db0c710a6b775c51aa7be70242a9e200c0d  M4b/events/cc50.json
d40047c7c0bb8e8a187623cf554648a5b2d4716b41b7eef59e98231a00cbabf8  C19/c19v.py
e8e0f6db92ee20a11e77187146d1192a045c49158faab15a27f80e6132342549  C19/c19n.py
0f412b86146c91578ce4560decd395d780480bdeb4cf89019bb5ffbf7e4466d2  C19/RESULTS-C19.md
190992d522927fdef300252dadffa75584104c59297e79f5584c825a10b93acb  voltages/delaymod/dm.py
1bf4b7ffc4cefb4edff55c7a3ce2253676e9543526544589859503fb3e940354  voltages/delaymod/horizons-gbt-20251218.txt
