# PLAN-M4b: the drift search, from the M4/M4b boundary on

Written 2026-11-19, before any M4b product exists; DRAFT until the calibration below is run and its outcome written here, then frozen with its hashes in PLAN-M4b.sha256. Operator, 15:05 EST: "should we adjust to check for signal that drifts across frequency as we go?"; 15:11: "and agreed, we'll make the change at the transition boundary".

## Why

M4 has two blind spots, both of its design, neither of its execution.

1. **Misses.** M4 stacks power along the comet's own Doppler track and along 100 false tracks offset by constant velocities. A signal drifting at any other rate is smeared across bins and weakens. And mv.py normalises each bin by its median over the scan's rows, which removes any tone that stays in one bin for more than about half the scan: a stationary or slowly drifting tone (|rate| below about 0.02 Hz/s) is invisible to M4 by construction.
2. **False passes.** M4's veto compares the OFF scans bin by bin in the comet frame. A drifting emitter sits in different bins in the OFF scans and passes. Every M4 nomination so far is of this kind or closed (cc03 radiosondes, cc30 GLONASS L1).

## The boundary

M4 keeps its channels as recorded: cc00–cc32 and cc34, cc40, cc63 (the workers stopped at the end of cc31 and cc34, 2026-11-19). From the boundary, every channel is downloaded once and yields both M4's products (unchanged) and M4b's. The channels M4 finished are then downloaded again for M4b alone; their M4 results are not recomputed.

## What runs

`mvb.py CC SCAN`: mv.py's code, byte for byte below its marked lines (the diff is kept with this plan), plus, on the same in-memory power:

1. **Normalisation across frequency.** The bandpass is the median over the scan's on-target rows, smoothed as the median of 1024-bin blocks and interpolated; each row is divided by it and by its own median. A stationary tone survives. The channel centre ±4 bins is zeroed, as the hit rule zeroes it.
2. **Drift search** (`M4b/mdrift.py`). Rows padded to 64; Taylor's tree sums power along straight lines for every drift of 0 to ±63 cells over the 63 row intervals (383 s), at three resolutions: 1, 4 and 16 bins per cell (2.79, 11.2 and 44.7 Hz). The rates reached: |r| ≤ 0.46, 1.8 and 7.3 Hz/s; steps 0.0073, 0.029 and 0.117 Hz/s. Each drift's sum is z-scored by median and MAD across the band; per cell the largest z over drifts and its drift are kept, with the cells z ≥ 6 listed.
3. `out3/ccNN_SCAN.npz` holds these.

`mdhits.py CC`: the events. **Revised after calibration round 1 (cc30, M4b/cal/CALIBRATION-cc30.md): the hit statistic is local.** Each resolution's per-cell maximum over drifts is rescaled by the median and MAD of that maximum in blocks of 1024 cells, because one MAD across the coarse channel made broadband occupancy (GLONASS) into about 10⁵ hits. Hits and vetoes are read on the local statistic.
- **Hit**: a cell in an ON scan with z ≥ Z_HIT, the strongest within ±2 cells.
- **Track**: its drift extrapolated linearly to each other scan's first row. Window: ±(3 + ⌈|Δt|/383 s⌉ + ⌈K·|rate·Δt|⌉) cells, at the hit's resolution.
- **Veto**: in any OFF scan, the largest z (any drift) inside the window ≥ Z_VETO.
- **Class A**: not vetoed, and z ≥ Z_VETO inside the window in both other ON scans. **Class B**: not vetoed, single-scan.
- **Control**: the same rule with the roles exchanged (OFF scans as ON, ON scans as vetoes). Its counts are the rate at which pointing away from the comet produces events.
- One event per signal: the same scan within 134 Hz at any resolution is one event.

`m4b.sh PARITY`: per channel, mvb.py over the six scans; for a channel M4 has not finished, M4's mhits.py and mvolt.py as frozen; mdhits.py → `M4b/events/ccNN.json`; the stacks hashed into `M4b-PRODUCTS.sha256` and deleted.

## Calibration (before freezing)

On cc30, which holds the GLONASS L1 carriers M4 nominated:
1. **Injection.** Synthetic linear chirps added to both feeds before the FFT in the ON scans: rates 0, +0.1, −0.3, +1, −2, +4, −6 Hz/s, each at two strengths (r = 0.2 and 0.8: the tone's power over its bin's mean noise power, per frame). Recovery is read per rate and strength. The voltages are already quantised; the injection is added after quantisation.
2. **Persistent sources.** Two tones continued across all six scans (0 and +0.05 Hz/s, r = 0.8): they must be vetoed.
3. **GLONASS.** The carriers at 1599.96 and 1600.31 MHz must be vetoed.
4. **Control rate.** The role-exchanged counts on cc30.

Z_HIT, Z_VETO and K are set from these (provisional 10, 5, 0.5) and written here with the outcome before the plan is frozen.

**Round 1 done (cc30).** The class-A rule and the veto work. Slow strong tones (r = 0.8, |rate| ≤ 0.3 Hz/s) are found at local z 17–67; drifts of 1 Hz/s and above and r = 0.2 are not reliably found in that channel; GLONASS and the persistent tones are vetoed; the role-exchanged control gives B 270 against 32. **Round 2, before freezing:** a quiet channel, with injections continuous across the ON scans at 0.05–4 Hz/s and r = 0.4, 0.8 and 1.6, for the sensitivity curve and the thresholds. Nothing after freezing changes them.

## What counts

Class A is a lead for a closer voltage look; class B is reported, ranked by z, and read against its channel's control. Any class-A event is reported with its channel, scan, frequency, rate and z before anything else is done with it.

## Limits

- Straight lines only within a scan; across scans, the window allows K of the rate as curvature.
- Drifts beyond 7.3 Hz/s are not searched. At the coarser resolutions sensitivity falls by up to √L against a matched filter for a tone that drifts less than L bins per row.
- The bandpass smoothing (1024 bins, 2.86 kHz) passes structure narrower than that. Broad features are taken as bandpass.
- 64 coarse channels × 6 scans: about a day and a half at the M4 rate (about 30 channels in 17 hours with two workers).
