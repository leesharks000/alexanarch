# PLAN-r13: the thirteen again, under the cautions of 2026-11-18

Frozen 2026-11-18, before any spectrum of this rerun is read. The sha256 of this file is recorded in PLAN.sha256, in the runner and in the results. Requested by Lee Sharks, 2026-11-18 08:26 EST: "lets run the original 13 again with especially those cautions in mind... and did we run those with the metadata slew correction in mind?"

## What is already done and not repeated

- The pair test: two ON scans give no excess for any pair (§7.14).
- Siblings below the threshold (sib/).
- Three background models (bg/).
- Held-out L band (lheld/) and the look-elsewhere survey (lee/).
- The cadence comb (comb/) and the two-epoch match (epoch/).
- Raw-voltage delayed copy and modulation (voltages/delaymod/).
- The 0017 header geometry and settling check (p17/, §7.14).

## Data

- GBT blc23, 2025-12-18, coarse channel 7 (1665.5–1668.5 MHz), scans 0013–0018 (ON 0013/0015/0017, OFF 0014/0016/0018).
- Spectra: rawspec.0000.h5 (2.79 Hz × 6.085 s, 49 rows), fetched by HTTP range read, held in memory.
- Telemetry: the GUPPI block headers of the same scans' raw voltages (https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/, 6,800-byte header per 134 MB block, about 0.0447 s per block). Read are every 4th block of file 0000 (the first 128 blocks, about 5.7 s) and every 32nd block after. The fields used are RA, DEC, AZ, ZA, TRK_MODE, PKTIDX, STT_IMJD, STT_SMJD, TBIN.
- Coordinates: the thirteen of oh13_candidates.csv (C01–C13). C01 is known interference, kept and labelled.

## Procedure

The same as lheld/run_lheld.py and ocad/run_ocad.py:
- x/median − 1, then a 3-channel boxcar;
- shift along the frame path;
- robust z per scan, with the 9 DC bins zeroed;
- align in the frame's rest frequency;
- ON z ≥ 2.5 in all three, OFF z < 2.0 in all three, ±1 channel;
- 10 Hz clusters, and the swap counted the same way;
- 40 false range-accelerations about the frame, seed 11, 0.03–1 (× C/1.42e9) km/s², with T0 the first ON start.

## Parts

**Gate.** V0, all rows, comet frame, must give 13 true-frame clusters. If it does not, nothing else is read as a result and the discrepancy is reported.

**A. Telemetry and the row cut.**
- A1. Per scan, the time of the first TRACK block, and the scan's own path over its TRACK blocks: a straight line in RA and in DEC against time.
- A2. A row is off-target if any sampled block within its span is not TRACK, or lies more than 0.2 arcmin from that line. For the ON scans, the line's offset from the comet (Horizons topocentric RA/DEC, 1-minute steps) is also reported.
- Variants, each with its own 40 false frames:
  - V1: drop row 0 of every scan;
  - V2: drop the off-target rows of A2.
- Reading: if V1 or V2 brings T to or below its own false maximum, the excess depends on off-target time, and this is reported as such. Otherwise the excess stands without it.

**B. Strength.**
- B1. S = the largest, over rest-frequency positions where all three OFF are below 2.0, of the smallest of the three ON z (with the ±1-channel tolerance). It is ranked among the 40 false frames.
- B2. For each of C01–C13, the smallest ON z at its coordinate (±1 channel), in the true frame and at the same rest position in each false frame. Its rank is out of 41.
- B1 and B2 are computed for V0, V1 and V2.

**C. Injection calibration.**
- Twenty frequencies, numpy default_rng(13) uniform over the channel. Excluded are positions within 200 bins of DC, of any of the thirteen, and of the fixed tone at 1665.615127 MHz.
- At each, a tone one bin wide, following the comet path, is added to the raw power of every row of the three ON scans: amplitude A × the row's median × σ, where σ is the robust standard deviation of x/median − 1 over the channel in that scan.
- A runs over 0.25, 0.5, 1, 2 and 4, all twenty tones at once per A, each run with its 40 false frames.
- Reported, per A:
  - the count rule (T and whether it exceeds);
  - B1;
  - the injected tones recovered as clusters;
  - each tone's smallest ON z.
- From these:
  - the A at which half the tones are recovered;
  - the A at which the count rule and the strength rule trip;
  - for each of the thirteen, the A whose median smallest-ON z matches the coordinate's own.
- This calibrates; it does not decide.

**D. Other frames.**
- Each frame is run as V0 and V2, with its own 40 false frames about it:
  - comet (the original): f(1 − v/c), v the Horizons range-rate at the GBT;
  - flip: f(1 + v/c), the sign reversed;
  - geocentric: a frequency fixed at the Earth's centre, so the arrival drifts only by the GBT's rotation velocity along the line to the comet (astropy get_gcrs_posvel at the GBT; direction from Horizons topocentric RA/DEC);
  - barycentric: a frequency fixed in the solar-system barycentric frame at the Earth, so the arrival is shifted by the GBT's barycentric velocity along the line to the comet (astropy radial_velocity_correction, kind barycentric, toward the comet's position);
  - topocentric: zero drift. This is the interference frame, reported as reference and not read.
- Per frame: T, swap, the false mean, sd and maximum, the largest ON − swap difference, B1, and the true-frame clusters' rest frequencies.
- An alternate frame exceeds by the same rule as the comet frame: T above every false frame, and T − swap above every false difference.
- Whether the comet frame is the best of the four non-topocentric frames is reported. So is whether the thirteen's coordinates stand in any other frame.

**E. Ephemeris.**
- The JPL solution identifier and date of the Horizons result are recorded.
- Reported against the false frames' smallest acceleration (0.03 × C/1.42e9 km/s²): the range-acceleration error needed to move a tone one channel across the cadence.

**F. Aggregate rank (no new spectra).**
- Across the 64 surveyed L-band channels (lee/) and the 64 S/C/X channels (ocad/): the true frame's rank among its 41 frames in T, from the stored per-frame rows.
- Tested for uniformity (Kolmogorov–Smirnov, and the count in the top 10 percent). A weak, spread excess would show here although no channel exceeds.
- Ties are broken at random, seed 5. The thirteen's channel is reported apart.

**G. Twin independence (no new spectra).**
- For the S/C/X twin node pairs (ocad/order.json): from the headers, the bank, IF and polarisation fields, and whether the two nodes' data are the same.
- A twin is used for replication only if it is shown to be independent.

## v2 additions (2026-11-18 08:30 EST, before any spectrum of this rerun is read)

Lee Sharks, 08:30: "we need to measure strength, test outside l band, look for things beyond steady emission, check multiple frames, judge across channels, do voltage permutation tests that can reach significance, check replication routes, and so on; and the items you suggest as well, 5 and 7 etc." Version 1's sha256 stays in PLAN.sha256 as written; v2's is appended.

**I. Beyond steady emission** (comet frame, V0 and V2, each with its own 40 false frames):
- I1, single scan strong: positions where one ON scan has z ≥ 5, the other two ON are anything, and all three OFF are below 2.0.
- I2, two of three: positions where two ON scans have z ≥ 3 and all three OFF are below 2.0.
- I3, single-row bursts: each row of each scan is tracked alone and given a robust z. The count is positions where some ON row has z ≥ 6 and no OFF row reaches 4.
- Each count is ranked among its 40 false frames, by the same exceed rule as the main count.

**K. Wider signals.** The main count is repeated with boxcars of 9 and 33 channels (25 and 92 Hz) in place of 3, with the cluster tolerance widened to the boxcar. This is run for the comet frame, V0 and V2.

**H. Strength and injection outside L band.**
- Twelve channels of the S/C/X survey: the four named-line channels with the highest T, plus eight drawn by default_rng(17) from its random channels, at least two per band.
- Each is rerun with B1 (strength) and I1–I3.
- The injection of part C is applied at A = 0.5, 1 and 2 to four of them, one per band plus methanol 6668.5. This gives each band's detection floor in the same units as L band.
- Run after this file's L-band parts; procedure as ocad/run_ocad.py with the statistics added.

**J. A voltage test that can reach significance.**
- The scan-label permutation of voltages/delaymod has 20 labellings, so p cannot fall below 0.05. Here the voltage tests are made comet-referenced, so their null is false frames, as many as compute allows:
  - J1, suppressed carrier: the x² and x⁴ comet-frame stacks of delaymod M1, with 400 false-drift frames (seed 23) in place of 40.
  - J2, delayed copy of a comet-tracking tone: in each comet-tracked 2^20 spectrum, the power at rest frequency f is cross-multiplied with the power at f + Δ for Δ in ±1 … ±2000 bins. Copies are thereby sought as pairs that move together in the comet frame, against the same 400 false frames.
- p can reach 1/401.
- Decision: a J statistic counts if its true-frame value exceeds the 99th percentile of the 400 and replicates in each ON scan separately.
- Raw voltages of coarse channel 7 are streamed again (about 21 GB) and only products are kept. This is run last.

**F and G** stand as written (aggregate rank across channels; twin independence), and are run as soon as the S/C/X survey is complete.

**Replication routes, stated before any result:**
- For L band: the July 31 Parkes epoch (done, epoch/) and the ATA July sessions (ata-ontrack/).
- For S/C/X:
  - twins only where part G shows them independent;
  - 7689–8251 MHz between the C and X cadences;
  - cross-telescope, the ATA July 8 high band (6376–9064 MHz) at the same emitted frequency.

## Not covered

- Bursts shorter than 6.085 s in the spectra (the voltages see 0.36 s frames in J).
- Patterns spanning channels.
- Other raw-voltage channels.

## Deviations

Recorded in RESULTS-r13.md with their reasons.
