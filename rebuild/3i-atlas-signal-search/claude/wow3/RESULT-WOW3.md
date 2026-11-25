# Seven further readings of the Wow! signal as filtering procedure: none finds anything in the 3I/ATLAS data, and the comet's 1977 velocity does not match the Wow's

**2026-11-24/25.** At the author's word (20:58 EST): "yes, lets freeze and run what we can". Plan frozen before any product: PLAN-WOW3.md, FROZEN-WOW3.sha256 (02:02 UTC); amendment 1 frozen before its rerun: AMENDMENT-1.md, FROZEN-WOW3-A1.sha256. Post-hoc checks are labelled as such. Products hashed in WOW3-PRODUCTS.sha256.

## R1. The offset as a velocity, and the comet in 1977: no match

- **The Wow's offset as a blueshift:** 67.54 km/s (revised) or 10.51 km/s (Ehman), each ± 1.06 km/s.
- **3I/ATLAS from Big Ear at 1977-08-16 03:16 UT (JPL Horizons):** range-rate −43.01 km/s, range 590.2 AU, RA 294.82°, Dec −19.09°.
- **Neither window holds it.** Across 1977 the comet's range-rate ran from −87.7 to −28.1 km/s with the Earth's motion; it lay inside the revised window on 2.4% of days from 1970 to 1985, and never inside Ehman's.
- **The sky position:** 8.47° and 8.25° from the Wow's two horn positions. The comet stood at least that close on 36% of those days, and never closer than 8.21°: at 590 AU it hardly moves, so the nearness is its incoming direction.
- **Caution.** The orbit is integrated 48 years back from a 2025 arc; its uncertainty is not propagated here.

## R2. The Wow's velocities on the OH lines, comet frame (amendment 1 for the two last groups)

| Target | MHz | Mean ON/OFF − 1 | Rank vs 200 controls |
|---|---|---|---|
| OH 1612 at 67.54 km/s | 1612.5942 | 0.0366 | 0.980 |
| OH 1612 at 10.51 km/s | 1612.2875 | 0.0351 | 0.200 |
| OH 1665 at 67.54 km/s | 1665.7770 | 0.0371 | 0.905 |
| OH 1665 at 10.51 km/s | 1665.4602 | 0.0413 | 0.985 |
| OH 1667 at 67.54 km/s | 1667.7346 | 0.0361 | 0.310 |
| OH 1667 at 10.51 km/s | 1667.4175 | 0.0357 | 0.050 |
| OH 1720 at 67.54 km/s | 1720.9176 | 0.0375 | 0.655 |
| OH 1720 at 10.51 km/s | 1720.5903 | 0.0373 | 0.495 |

- **Two targets rank above 95%.** Neither has a narrow core in any scan (peak-bin z 0.6–0.9, ON and OFF alike).
- **Both sit near a coarse-channel edge** (67 kHz and 199 kHz below the top), where the controls, drawn from the channel's interior, do not sit.
- **Post hoc, the same distance from the edge in neighbouring channels, with no Wow velocity involved:**
  - 67 kHz from the edge: 0.0414, 0.0411, 0.0414, 0.0405, 0.0402, against the target's 0.0413.
  - 199 kHz from the edge: 0.0373, 0.0339, 0.0365, 0.0336, 0.0359, against the target's 0.0366.
- **Reading.** The two excesses are the channel edge's, not the targets'.

## R3. Polarization at those targets (blc23 voltages, coarse channels 7, 8 and 26; 5.59 Hz; full Stokes)

- **No target counts** in I, V, Q or U: none is above 95% of its 200 control windows in all three ON scans and in no OFF scan. ON ranks run from 0.00 to 0.96.
- **The re-read of channels 7 and 8 reproduced the first read:** every recorded hash of the channel bytes matches (voltages/out/meta_*). The integrated spectra were hashed (INTEG-deleted-after-hashing.sha256) and deleted for disk.
- The polarization fractions are uncalibrated, as before.

## R4. The profile along frequency (blc21–26, 2.86 kHz and 8.58 kHz)

Pooled over the six nodes, ON-only detections against the 200 smooth controls:

| Width, order | Wow | Smooth median | Rank |
|---|---|---|---|
| 2.86 kHz, ascending | 2,450 | 2,756 | 0.100 |
| 2.86 kHz, descending | 2,464 | 2,756 | 0.135 |
| 8.58 kHz, ascending | 554 | 649.5 | 0.015 |
| 8.58 kHz, descending | 599 | 649.5 | 0.160 |

By node the ranks run from 0.04 to 0.95. The Wow's shape along frequency picks out less than an ordinary bump does.

## R5. The 12 s cadence, 10 on and 2 off (blc21–26, 8.58 kHz, 1.07 s)

1,153 ON-only detections at 12 s, against a median of 1,200 for the 200 other periods: rank 0.18. By node, 0.00 to 0.865.

## R6. The hydrogen targets at rest in the Sun's frame (blc24, 2.79 Hz)

The Sun-frame radial velocity along the line of sight was −29.6 km/s (the comet's own was −1.9), so the targets sit about 140 kHz above their rest values.

| Target | Mean ON/OFF − 1 | Per pair | Rank |
|---|---|---|---|
| S1, the hydrogen line | 0.0027 | 0.045, −0.037, 0.000 | 0.000 |
| S2, + 320 kHz | 0.0416 | 0.099, 0.013, 0.014 | 0.575 |
| S3, + 49.8 kHz | 0.0811 | 0.115, 0.032, 0.096 | 1.000 |

- **S3 is above all 200 controls and S1 below all of them.** The controls' median is 0.0416.
- **Post hoc, the contrast in 10 kHz steps across the line, topocentric:** the band's power peaks at 1420.57–1420.58 MHz, which is the Galaxy's hydrogen emission. Across that peak the contrast falls from 0.041 to 0.001 (1420.53–1420.57) and then rises to 0.087 at 1420.59, returning to 0.035 by 1420.63. Pair by pair the swing changes size and sign (at 1420.56: +0.091, −0.111, +0.033).
- **S1 (1420.546 topocentric) lies on the falling side and S3 (1420.596) on the rising side.**
- **Reading.** This is the Galactic hydrogen line seen at two pointings: the comet position and the OFF position have slightly different hydrogen profiles, and their ratio swings across the peak. It is some 50 kHz wide, with no narrow core (peak-bin z 0.8–2.9), and it changes from pair to pair.

## R7. Big Ear rebuilt on the hydrogen band (blc24, fifty channels of 8.58 kHz, 10 s every 12 s)

- **No character reaches 5 in any scan.** The largest are 1, 1, 2, 2, 2 and 3 in scans 0013–0018. The Wow ran 6, E, Q, U, J, 5.
- **The printouts are fields of 1s and blanks.** The first rows of the ON scans are solid 1s, a slow gain drift within the scan.
- With nothing at 5, the 200 control blocks have nothing to rank against.

## What this establishes

- **The Wow! was not the hydrogen line at rest in 3I/ATLAS's frame in 1977.** The comet approached at 43.0 km/s; the offset asks for 67.5 or 10.5.
- **No reading finds a comet-frame or ON-only feature.** The three targets that cleared 95% are accounted for: two by coarse-channel edges, one by Galactic hydrogen. Each account was checked after the fact and is marked post hoc.
- **Under the readings tested, the Wow! gives no filtering procedure that selects anything in these data.**
- **Still open:** W5 and its mirror; the profile as beam, which under tracking is the search's standing test.
