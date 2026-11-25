# Look 3.2 — the Wow's frequency fixed in the Sun's frame, at Parkes (frozen before any read)

Reading: an emitter in the comet's beam that holds the Wow's frequency fixed relative to the solar-system barycentre, not to the comet.

Frequency: the Wow as received at Big Ear, 1977-08-16 03:16:06 UTC (revised 1420.726 MHz; Ehman 1420.4556 MHz), corrected for Big Ear's barycentric velocity along the Wow's direction (J2000 RA 19h25m31s and 19h28m22s, Dec -26d57m; mean of the two horns). Earth's barycentric velocity from JPL Horizons; site rotation added (Big Ear 83.0489 W, 40.2513 N). Received at Parkes, per 15 s row: f = f_emit * (1 - rr/c), rr = deldot - v_comet . u (Horizons, Parkes site; comet barycentric velocity, unit vector to comet).

Data: Parkes UWL blc05 product .0000 (2 Hz x 15 s), sessions 2025-07-31, 09-12, 10-05 (10-05: two days after the Mars passage). S scans on the comet, R reference.

Per window (+-6 kHz): each row shifted to the Sun frame; z-map as look2_parkes (row-normalised, 201-channel median shape, MAD scale); column mean x sqrt(nt) per scan; S scans stacked per session by summing columns / sqrt(n).

Statistic: the peak stacked S column within +-1 kHz of the prediction (frame uncertainty), per session and per frequency. Null: the same peak in 40 control windows, the prediction offset by +-(15 + 15k) kHz, k = 0..19.

Lead: the peak above all 40 controls in its session, and the R stack at the same column below 3. A lead then needs the same comet-frame... no: the same Sun-frame frequency within +-50 Hz in a second session.

Also reported: pixels >= 5 in S and R windows; every session's peak regardless.
