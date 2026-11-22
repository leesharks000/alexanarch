# RESULTS-HM10: the comet's OH line, measured and calibrated

Scored 22 November 2026 against PLAN-HM10.md as frozen (71b15a71e). `sha256sum -c FROZEN-HM10.sha256` printed OK before the run. All six public rawspec.0000 files were read remotely, scans 0013–0018 in order. All flux values assume a system equivalent of 10 Jy (absorb-calib's assumption; the product is uncalibrated), so mJy are approximate.

## The measurement

Pooled over the three pairs, at the comet's rest velocity. A is the 1667 MHz peak as a fraction of system power (×10⁻³); negative is absorption. σ is the scatter of the same fit at 72 line-free offsets.

| | FWHM 1 km/s | 2 km/s | 3 km/s |
|---|---|---|---|
| joint 1665 + 1667 (5:9): A, σ, z | −0.31, 0.81, −0.38 | −0.29, 0.55, −0.51 | −0.17, 0.52, −0.32 |
| 1667 alone: A, z | −0.41, −0.71 | −0.53, −1.27 | −0.41, −1.31 |
| 1665 alone: A, z | +0.01, +0.02 | +0.28, +0.47 | +0.35, +0.48 |
| 1612 (satellite): A, z | +0.74, +0.44 | +0.47, +0.27 | +0.52, +0.33 |
| voltages, 1667, X: A, z | +0.36, +0.60 | −0.18, −0.39 | −0.32, −0.72 |
| voltages, 1667, Y: A, z | −0.76, −1.25 | −0.27, −0.47 | +0.26, +0.70 |

1. **No line.** The joint statistic is within ±0.51σ at every width, against the rule's |z| ≥ 4. The comet's value sits in the middle of its 72 controls (23rd to 27th from the bottom). 1665 and 1667 disagree in sign. Per pair at 2 km/s, 1667 reads −1.5, −1.3 and +0.3σ, and 1665 reads −0.4, +0.9 and +1.9σ. In the voltages X and Y also disagree in sign at two of the three widths.
2. The 1667 line alone leans to absorption (−1.3σ at 2 and 3 km/s), the side MeerKAT saw in October. At that size it is noise. It agrees with absorb-calib's −0.35 and with HM6's first-pair reading.

## The calibration (new)

Absorption pairs (5:9) injected into the ON spectra at 12 line-free offsets, recovered by the same joint filter:

| injected 1667 peak | ≈ mJy | detected at z ≤ −3, of 12: 1 km/s | 2 km/s | 3 km/s | recovered / injected (2 km/s) |
|---|---|---|---|---|---|
| 0.5 × 10⁻³ | 5 | 0 | 0 | 1 | 0.84 |
| 1.0 × 10⁻³ | 10 | 0 | 1 | 1 | 0.93 |
| 1.5 × 10⁻³ | 15 | 1 | 4 | 5 | 0.96 |
| 2.0 × 10⁻³ | 20 | 3 | 9 | 9 | 0.97 |
| 3.0 × 10⁻³ | 30 | 9 | 12 | 12 | 0.99 |

3. **The calibrated floor** is the smallest depth found in at least 11 of 12. It is 3 × 10⁻³ of system power, about 30 mJy, for lines 2–3 km/s wide. For 1 km/s it is above 3 × 10⁻³, since 9 of 12 is under the bar. The filter does not eat the line: 93–99% of an injected depth is recovered at 1 × 10⁻³ and above.
4. **Against MeerKAT's October depths** (−14.2 ± 3.4 mJy at 1667, −8.4 ± 3.1 at 1665): a 1667 line of October strength, about 1.4 × 10⁻³, would have been found in about 4 of 12 placements at 2 km/s. The December data could not reliably have seen the comet's OH even had it held its October strength. The floor is about twice that depth.
5. This revises absorb-calib's reading. Its "three-sigma floor about 11–12 mJy" was a scatter-based limit. Measured by injection, the depth found reliably is about 30 mJy. A line at 11–12 mJy is found about one time in three.

## Reading

- The search cannot see the one natural signal the comet is known to make at these frequencies, at the strength it was last measured. For a line a few kHz wide, the floor of what these data find reliably is about 3 × 10⁻³ of the system power. A kilohertz-scale absorber or emitter on the comet weaker than about 30 mJy would be missed.
- This bears on the narrowband readings differently. They concentrate on single 2.8 Hz bins, where HM9's self-test puts the carrier floor near 3% of a bin's power, and HM8's excess is 5–7%. Those readings are sensitive to narrow features the OH test is not.
- The two calibrations together say what the series could and could not have found. It could find:
  - a narrow carrier at a few percent of a bin;
  - a cross-feed coherence above 0.11;
  - a kilohertz-wide line above about 30 mJy.

  It could not find the comet's own OH at its October depth.
- Failing a frozen test bars nothing.

Outputs: hm10.json, hm10.log. RESULTS-HM10.sha256 hashes them and this file.
