# PLAN-ratio: hydrogen-line ratio search, Parkes 2025-07-31 and GBT 2025-12-18 (frozen before any look at these frequencies)

Question. Do the ratio frequencies drawn from the blog's 3I/ATLAS posts (Sep–Oct 2025: "Numbers in the Void", "Treatise", "What Signal Looks Like", "Speculative Contact Protocols") carry more narrowband events in on-source scans than a rule-built control list, and more than the same frequencies in reference scans?

Anchor. HI rest frequency 1420.405752 MHz.

Alphabet list (13). f = r x 1420.405752 MHz for r in: 5/3, 15/8, 7/4, 3/2, 7/5, sqrt2, 2, 4/3, 8/7, 7/6, 7/8, 1/2, 4/7. (pi, 4462.336 MHz, is outside both instruments and is dropped.)

Control list (13), by fixed rule: reduced fractions p/q with p, q <= 16, at least one of p, q divisible by 11 or 13, f within 704–4032 MHz, more than 1 MHz from every alphabet frequency; sorted by (p+q, p); first 13: 11/4, 11/5, 6/11, 11/6, 7/11, 11/7, 13/5, 8/11, 11/8, 13/6, 7/13, 9/11, 11/9. No exclusions for known interference (11/9 at 1736.05 MHz lies near the blc10 interference block; it stays in).

Frames. Each frequency is tested at two positions: topocentric (f itself) and comet frame (f x (1 - v/c), v the Horizons range-rate of C/2025 N1 at the sample time). Tolerance +-15 kHz around each position.

Parkes data. PKS_Jul_31_2025, the node whose 128 MHz band contains the frequency, six 0000.fil files (S/R alternating), 2 Hz channels, 20 x 15 s samples. A frequency inside no node's band, or within 200 kHz of a band edge, is recorded as uncovered. Load a window spanning both positions +-200 kHz. Normalise r = X / median over the scan's samples - 1 per channel. Boxcars W in {1, 5, 50, 500, 5000} channels.
- Detector P (single sample): robust z over the window, z >= 5; veto any channel within +-(W+2) of a reference-scan channel with z >= 4 (any sample) at the same W.
- Detector P2 (one scan dedrifted to the comet frame and summed over its 20 samples): z >= 5; veto from reference-scan P2 z >= 3.
- Events are clustered within +-(W+2) channels per scan; an event counts for a frequency when its peak lies within tolerance of either position.
- Swap: the same with R scans as target and S scans as veto.

GBT data. blc24 .0002.h5 cadence covering 2214–2401 MHz (2.861 kHz x 1.07 s); detector G as in PLAN-wow (W in {1,2,4}, L in {1,10,67}, OFF veto 4) with z >= 5; same frames and tolerance; window both positions +-300 kHz. Applies to whichever list frequencies fall in that band (alphabet 5/3 at 2367.343 MHz; controls none expected); reported separately.

Statistic. Rate = in-tolerance events (P + P2, all W, all S scans) per covered frequency, for each list.

Lead. Alphabet rate > control rate AND alphabet rate > alphabet swap rate AND at least one alphabet event present in two or more S scans within tolerance of the same position. Every in-tolerance event is listed with frequency, offset, scan, sample, W and z whether or not the lead fires. Threshold z >= 5 is set for a list of 26 frequencies x 2 positions x 30 kHz (about 1.6 MHz total, 0.8 M channels at 2 Hz).

Injection check before the run: one 1-channel tone and one 50-channel burst, each at z ~ 7 in normalised r, added to scan 0 at the 5/3 topocentric position and 3 kHz off it; both must be recovered in tolerance.

Laws record; they do not prevent. A deviation is written into the results.
