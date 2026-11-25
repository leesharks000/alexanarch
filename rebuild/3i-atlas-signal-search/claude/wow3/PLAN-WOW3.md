# PLAN-WOW3: seven further readings of the Wow! signal as filtering procedure

**2026-11-24, 20:58 EST, at the author's word:** "yes, lets freeze and run what we can", after the question of 20:22: "in what ways could the wow signal be translated into a filtering procedure in the 3i signal search that we have not yet considered." Frozen before any product (FROZEN-WOW3.sha256). Standing rules: a failed test forbids nothing further; it only withholds the word *signal* under the readings tested.

Earlier readings: the 3 November intermittent search (run-2026-11-03/wow), PLAN-WOW (W1–W5: the frequency, the width, the profile in time, the ON/OFF rule), PLAN-SYMBOLON (K1–K4: the profile reversed and inverted, the frequency mirrored, the halves joined). The Wow! as recorded: PLAN-WOW §1.

## R1. The offset read as a velocity, and the comet's own velocity in 1977

320 ± 5 kHz above the hydrogen line is a blueshift of 67.54 ± 1.06 km/s; Ehman's 49.8 kHz is 10.51 km/s.

- **Query.** JPL Horizons, C/2025 N1 (3I/ATLAS), observer at Big Ear (Delaware, Ohio: 83.0489° W, 40.2513° N, 0.282 km), 1977-08-16 03:16 UT: range-rate (deldot), range, RA/Dec (ICRF).
- **Test.** deldot within ±1.06 km/s of −67.54, or of −10.51 (approach is negative).
- **Control.** deldot once a day from 1970 to 1985: the fraction of days inside each window. A match counts only if that fraction is under 5%.
- **Also reported, not tested:** the angle between the comet's 1977 position and the Wow's two horn positions (J2000 RA 19h25m31s and 19h28m22s, Dec −26°57′), and the same angle's daily distribution.
- **Caution recorded before the query.** The orbit is integrated 48 years back from a 2025 arc; Horizons' own uncertainty is not propagated here.

## R2. The same velocities on the OH lines, in the comet's frame

Targets: each of 1612.2310, 1665.4018, 1667.3590 and 1720.5300 MHz multiplied by (1 + v/c) for v = 67.54 and 10.51 km/s (blueshift, the Wow's sign): eight targets. Read as PLAN-WOW stage 2 read the hydrogen line: public rawspec .0000 (2.79 Hz × 6.08 s), the coarse channel holding each target (blc23, and blc22 for 1720), scans 0013–0018, tracked in the comet frame, a band of ±5 kHz × (line/1420.4), ON/OFF contrast per pair, peak-bin z. Controls: 200 random targets in the same coarse channel, more than 50 kHz from every target and from the line at rest. A target counts above 95% of its controls.

## R3. One horn of two read as polarization, at the R2 targets

Polarization has been read blind in the two OH coarse channels and at the thirteen candidates (voltages/README, findings 1–3). It has not been read at the Wow's velocities. Voltages of blc23 coarse channels 7, 8 and 26 (voltreduce.py, 5.59 Hz, scan-integrated full Stokes), scans 0013–0018. At each R2 target in those channels (the comet frame at scan mid-time; ±5 kHz scaled as in R2): the largest |z| of V/I, Q/I and U/I and the largest z of I inside the band (blind_pol.py's normalisation), per scan. Controls: 200 random windows of the same width in the same coarse channel. Counts if an ON scan's value exceeds 95% of the controls in all three ON scans and in no OFF scan. The polarization fractions are uncalibrated (no calibrator solution), comparable within the data only.

## R4. The profile transposed from time to frequency

Six adjacent channels whose powers stand as 6:14:26:30:19:5, at one time. Public rawspec .0002, blc21–26, per scan: the time-mean spectrum, divided by its running median (101 channels), in robust sigma units; at channel widths 2.86 kHz and 8.58 kHz. Score: correlation with the unit template along frequency, both orders (ascending and descending frequency). Detection: score ≥ 6 in an ON scan and < 3 at the same place in the OFF after it. Controls: 200 smooth single-peaked shapes (PLAN-WOW amendment 1's generator and seed) and 200 random six-value sequences. Rank against the smooth controls is the test.

## R5. The cadence read as a period

Big Ear integrated 10 s and was blind for 2. Public rawspec .0002 (1.07 s), blc21–26, 8.58 kHz channels: each channel's time series within a scan, correlated with a 12 s square wave, 10 on and 2 off, over twelve phases; the maximum over phase, in sigma units of that channel. Detection: ≥ 6 in an ON scan, < 3 in the OFF after it. Controls: 200 periods drawn uniformly from 7–20 s, excluding 11–13 s, same duty (5/6), same phases. The count of ON-only detections at 12 s is ranked within the controls.

## R6. The direction read as a rest frame

A tone steady in the Sun's frame along the line of sight to the comet. From Horizons vectors (GBT site): the unit vector to the comet and the velocity of the site relative to the Sun; the radial velocity of a Sun-rest source in that direction. Targets: the hydrogen line, the line + 320 kHz, the line + 49.8 kHz, each at rest in that frame; blc24 .0000, ±5 kHz, ON/OFF contrast, peak-bin z, as PLAN-WOW stage 2. Controls: 200 random targets tracked in the same frame. The Wow's own sky direction is not a frame for data pointed at the comet and is not used.

## R7. Big Ear rebuilt on the Green Bank data

blc24 .0002: fifty channels of 8.58 kHz centred on the hydrogen line (topocentric, as Big Ear recorded), 10 s integrations every 12 s, each channel's samples in units of its own scan sigma above its scan median, truncated to an integer and printed in Big Ear's alphabet (blank for 0, 1–9, A–Z). Statistic per scan: the number of characters ≥ 5, and the longest run of consecutive characters ≥ 5 in one channel (the Wow's run is six). Controls: 200 other fifty-channel blocks of blc24. The printouts of the six scans are kept in the result.

## Not run, and why

- **The profile as Big Ear's beam.** Green Bank tracked the comet; a steady source on axis shows no envelope. Under tracking this reading reduces to "steady through an ON scan and absent from the OFF", which is the search's standing test.
- **W5 and its mirror** (PLAN-WOW §2, PLAN-SYMBOLON §2): still open, with their cost.
- **A 72 s fold:** four cycles in a 300 s scan; not enough to rank.

## Code and products

`r1_horizons.py`, `r2_r6_lines.py`, `r3_pol.py`, `r457_stream.py`; products hashed in WOW3-PRODUCTS.sha256.
