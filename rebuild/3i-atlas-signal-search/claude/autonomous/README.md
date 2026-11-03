# 3I/ATLAS: signal classes for an autonomous sender, GBT 2025-12-18 cadence (analysis 2026-11-03)

Data: Breakthrough Listen, Green Bank, cadence scans 0013–0018 (ON 0013/0015/0017 on 3I/ATLAS, OFF 0014/0016/0018). Two products: blc23 `.0000.h5` coarse channel 7 (1665.53–1668.46 MHz, 2.794 Hz × 6.08 s, cached from the oh13 work) and blc23 `.0002.h5` (1501.5–1689.0 MHz, 2.861 kHz × 1.074 s, 279 samples per scan), from https://bldata.berkeley.edu/ATLAS/GB_ATLAS/.

The hypothesis under test is a sender supervised by a system that has monitored Earth's radio and read the published search pipelines. Such a sender can choose its frame and its time structure with Earth's receivers in mind. Four classes were tested; the ChatGPT ATA pass of the same date tested a fifth (a constant comet-frame rest frequency in a later ATA session).

## 1. Observer-compensated tones (`autonomous.py`)

A transmitter that removes its own Doppler for a receiver at point X arrives at the GBT on the path f(t) = F (1 − (v_topo − v_X)/c), with v_topo and v_X the comet's range-rate from the GBT site and from X (JPL Horizons). Four frames: X = none (the uncompensated comet frame of the oh13 search), X = GBT (zero drift at the telescope, the class turboSETI-style pipelines drop as terrestrial), X = geocentre, X = solar-system barycentre (the frame results are published in). Rule: z ≥ 2.5 in all three ON scans and z < 2.0 in all three OFF scans at one frame frequency (±1 channel), clustered at 10 Hz. Null 1: 24 false range-accelerations around each frame's path (0.03–1 Hz/s at 1.42 GHz, seed 7). Null 2: the beam swap (OFF scans as target, ON as reference).

| Frame | ON-target clusters | False frames: mean ± sd (max) | Fraction of false ≥ ON | Beam swap |
|---|---:|---:|---:|---:|
| comet (uncompensated) | 13 | 3.75 ± 1.76 (7) | 0.00 | 1 |
| GBT topocentric (zero drift) | 3 | 3.29 ± 1.54 (7) | 0.75 | 7 |
| geocentric | 7 | 3.96 ± 2.19 (9) | 0.08 | 7 |
| barycentric | 5 | 2.63 ± 1.44 (7) | 0.04 | 3 |

The zero-drift class, the one a familiar sender would know pipelines discard, gives nothing on-source: 3 clusters, fewer than the swap's 7. The geocentric and barycentric frames rise modestly above their false frames and show the same count, or near it, with the beams swapped, so the excess has no side.

## 2. Beam asymmetry in the comet frame (`swapnull.py`)

The comet frame's 13 against 1 was tested against 40 false frames (seed 11), each counted both ways.

| Quantity | True frame | 40 false frames: mean ± sd (max) | Fraction of false ≥ true |
|---|---:|---:|---:|
| ON-target clusters | 13 | 3.75 ± 2.05 (8) | 0.000 |
| Beam-swap clusters | 1 | 3.33 ± 2.07 (9) | (10% have ≤ 1) |
| ON minus swap | 12 | 0.42 ± 2.57 (6) | 0.000 |
| ON-singles minus OFF-singles (z ≥ 6 in one scan) | 6 | 3.08 ± 2.40 (8) | 0.125 |

The oh13 excess is specific to the on-source beam: no false frame produces it, and no false frame produces an ON-minus-swap difference above 6. The single-scan (intermittent) count shows no excess.

Natural reading checked: cometary OH would sit within about ±11 kHz (±2 km/s) of 1667.359 or 1665.402 MHz in the comet frame. The nearest of the 13 is C08 at 1667.412866 MHz, 54 kHz (about 10 km/s) from 1667.359; the rest lie 70 kHz to 1.75 MHz from either line. The 13 do not trace the comet's OH.

## 3. Time structure: periodic and pulsed (`pulsed.py`)

At 2.861 kHz the comet's Doppler change over a scan stays inside one channel, so each channel holds a comet-fixed tone for the whole scan. Periodic: power at the same channel and period (2.15–150 s) ≥ 12× the channel's median in all three ON scans and < 4× in all three OFF scans. Broadband: the same rule on the channel-summed series (a dispersion-free pulse train). Events: single 1.07-s samples at robust z ≥ 8 in one beam at channels quiet (|z| < 4) throughout the other beam.

| Test | ON target | Beam swap |
|---|---:|---:|
| Periodic (channel, period) pairs | 173 | 456 |
| — of which in radio-astronomy bands (1610.6–1613.8, 1660.5–1670 MHz) or 1501.5–1518 MHz | 0 | 0 |
| Broadband periods | 0 | 0 |
| Events, in channels | 1,161 in 107 | 8,967 in 3,285 |

All 173 ON-target periodic pairs fall in satellite allocations: 108 in GNSS (1559–1610 MHz), 61 in Inmarsat/MSS (1518–1559), 4 in Iridium (1616–1626.5). The on-source events sit in the same allocations (63 MSS/Inmarsat channels, 37 GNSS, 5 MSS, 2 Iridium). The OFF beam is busier in every test; its events include 516 channels in the 1612 MHz OH band, which belong to the OFF pointing. The broadband periodograms peak at 74.9, 149.8 and 299.6 s in ON and OFF alike: the scan length and its harmonics.

## Reading

Of the classes an autonomous, Earth-familiar sender would plausibly use, three return nothing on-source (zero-drift compensation to the telescope, single-scan intermittency, periodic or pulsed structure outside satellite bands). Two compensated frames rise modestly with no beam side. The one standing feature is the comet-frame excess at z 2.5 (13 clusters), now shown to belong to the on-source beam against 40 false frames. Its limits stand as before: it does not hold at 2.0 or 3.0; its candidates average about 0.35σ per step with no shared time pattern; and the ATA July session (lower sensitivity) did not continue six of its locations. Every test here was chosen after the oh13 result, so the trials are many and these fractions are descriptive. No content, origin or emitter is established.

## Next test the sidedness result specifies

The 1667 MHz channel has no second GBT cadence in the public directory: the same night's later cadences on blc23 (scans 0029–0034, 0045–0050, 0061–0066) are at 2.4–2.6, 7.7–7.9 and 11.6–11.8 GHz (headers read 2026-11-03). Two held-out routes remain. (a) The frequencies: the 13 rest frequencies and the 2.5/2.0 rule, frozen, on an ATA or Parkes session at 1667 MHz with sensitivity near the GBT's. (b) The property: the comet-frame procedure, the beam swap and the 40 false frames, frozen as here, run on one coarse channel of an S-, C- or X-band cadence chosen before reading. A beam-sided comet-frame excess in another band would replicate the class; its absence bounds it.

## Files

`autonomous.py`, `swapnull.py`, `pulsed.py` (code); `OH_autonomous.json`, `OH_swapnull.json`, `pulsed.json` (results, every hit listed with its per-scan scores).
