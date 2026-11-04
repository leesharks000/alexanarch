# Frozen plan: C03 (and the other twelve) at Parkes, 2025-07-31 (written 2026-11-03 ~17:35 EST, before any Parkes power is read)

Data: Breakthrough Listen Parkes UWL, PKS_Jul_31_2025/blc07 (1600-1728 MHz, 2 Hz channels, 15 s samples, 20 per scan), cadence
S 50760, R 51102, S 51442, R 51782, S 52123, R 52472 (S = on 3I/ATLAS, R = reference), product .0000.fil.

Targets: the thirteen frozen rest frequencies of oh13 (C01-C13). Primary: C03, 1665.633777 MHz. C01 and C02 carry the GBT contamination labels.

Model: constant rest frequency, received f(t) = F (1 - v(t)/c), v the comet's range-rate from Parkes (Horizons, site 148.2635 E, -32.9984, 0.415 km),
at each sample centre.

Detector (the oh13 rule, adapted only for the sample count): per channel, divide by its median over the scan's 20 samples, minus one; 3-channel boxcar;
sum along the path; robust z (median, 1.4826 MAD) over the extracted +-16 kHz window of that scan. Score of a target in a scan: the largest z within
the window (strict +-5 Hz; secondary +-100 Hz) at one common rest frequency. Flag: z >= 2.5 in all three S scans and < 2.0 in all three R scans at one
rest frequency (+-1 channel). Controls: 100 windows centred at F +- 250k Hz, k = 1..50, same widths and rule; report how many controls reach each
target's minimum S score.

Outcomes, stated now: a flag at C03 under the strict window is a CONTINUATION; no flag is NOT CONTINUED (Parkes is a 64 m dish against the GBT's
100 m, and the object was farther in July, so a null bounds a source only at Parkes's sensitivity). No window, threshold or model changes after reading.
