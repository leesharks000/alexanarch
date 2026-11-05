# PLAN-ata36: the comet frame in 3648–3688 MHz, ATA 2025-07-03 (the strip no other public dataset covers)

Frozen 2026-11-04 before any power of this strip is read. The sha256 of this file is recorded in the runner and the results.

## Question

The ATA paper (Sheikh et al., arXiv:2512.18142v2) kept hits with drift +0.05 to +1.5 Hz/s; a tone fixed on 3I/ATLAS drifts negative in every session (§5.1 of the draft), so the paper's filter removed that class at every frequency it searched. Elsewhere in the public ATA band that class has a second look: the GBT (2025-12-18; 939–2064, 1651–2776, 3939–8251, 7689–12376 MHz), Parkes (2025-07-31; 704–1984 and 2112–3648 MHz, searched with the correct sign in pks/PLAN-fullband.md), MeerKAT (856–1712 MHz) and FAST (1050–1450 MHz). In 3648–3688 MHz, the top 40 MHz of the July 3 session, no other public 3I/ATLAS data exist: Parkes's public nodes end at 3648 MHz and the GBT's C band begins at 3939 MHz (headers mapped 2026-11-04, ata/ata_map.json and p17/headers_0002.json). This test asks whether the strip holds a beam-sided comet-frame excess, with a held-out half of the session.

## Data

ATA 2025-07-03, tuning LoD.C1504 (3591.75–3687.75 MHz, 1.9073 Hz channels, 19 samples of 16.777 s per scan), the session's 16 scans, beam0000 (on-source) and beam0001 (reference, offset 0.262°, recorded simultaneously): 32 files, read by HTTP range reads of the channels covering 3648.0–3687.75 MHz plus margins, in blocks of 524,288 channels overlapped by 4,096 on each side. Discovery: the first eight scans in time order. Held out: the last eight. No held-out power is read before the discovery result and the nominee list are written and hashed.

## Procedure

Per file and block: each channel divided by its median over the scan's 19 samples, minus one; 3-channel boxcar; rows summed along the comet path (constant rest frequency, Horizons range-rate at the ATA site −121.4733, 40.8178, 1.019 km, per sample centre); robust z; the scans aligned in the comet rest frame of the first discovery scan, ±1 channel max filter. Gate (discovery): beam 0 z ≥ 2.5 in at least 6 of the 8 scans and the mean of its 8 z ≥ 3.0; beam 1 z < 2.0 in all 8; 10 Hz clustering. Count T (true frame), the beam swap (beam 1 tested, beam 0 reference), and the 40 false range-accelerations of seed 11 (cf.py's family, 0.03–1 × C/1.42e9 km/s², random sign), each with its swap. A check before counting: the robust scatter of x/median − 1 in 3648–3688 MHz against 3600–3640 MHz of the same files, per beam and scan, recorded; if the strip's scatter departs by more than a factor of 1.5 the strip is reported block by block with that ratio.

## Rule

- Discovery: E = (T − μ)/max(σ, 0.5) over the false frames; FLAG = T above every false frame and T − swap above every false frame's difference.
- Nominees: the true-frame clusters, at most ten, ranked by mean beam-0 z; written with rest frequencies and hashed before the held-out scans are read.
- Held out: for each nominee, the eight held-out scans along the same path at the nominee's rest frequency ±5 Hz: beam 0 mean z ≥ 2.5 and beam 1 mean z < 2.0, where each scan's z is computed by the discovery procedure in a window of ±2,500 channels around the path, the mean is taken over the eight scans channel by channel in the rest frame, beam 0 takes its largest mean within ±5 Hz and beam 1 its largest mean within the same ±5 Hz. Control: 100 frequencies drawn uniformly over the strip (seed 37), at least 1 kHz from every nominee, tested the same way. A nominee continues if it passes and fewer than 5 of the 100 controls pass.
- Reported as measured: E, FLAG, every nominee with its held-out scores and control rank, and the allocations at each nominee's received frequency (US CBRS 3550–3700 MHz terrestrial; fixed-satellite downlink allocations internationally).

## Deviations

Recorded in RESULTS-ata36.md with their reasons.
