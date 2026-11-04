# PLAN-comb: does receiver-frame structure explain the thirteen? (cadence/comb test)

Frozen 2026-11-04 before the data of this test were read in this run. The six input files were read in earlier runs (the thirteen were found in them, §7.1 of the draft); the structure measurement, masks, controls and rules below are fixed here before any of them is computed. The sha256 of this file is recorded in the runner and the results.

## Hypothesis

H_comb: the comet-frame excess in GBT blc23 coarse channel 7 (13 clusters against a false-frame null of about 3.75 ± 2.05) is produced by structure fixed in the receiver's frame: a comb, stationary lines with time-varying amplitude, or channels of excess temporal variability, including the radiosonde allocation edge at 1668.4 MHz. A comet-frame path drifts about 32 Hz through each scan and its topocentric position moves between scans as the comet's range-rate changes, so ON and OFF paths at one rest frequency cross different topocentric channels. If ON paths cross such structure and OFF paths miss it, the tracked sum yields ON-only coincidences without any source on the comet. C01 and C02 are known instances (the 1665.61512 MHz complex, teeth at about 60.35 Hz).

## Data

Breakthrough Listen GBT, 2025-12-18, blc23 rawspec.0000.h5, scans 0013–0018 (ON 0013, 0015, 0017; OFF 0014, 0016, 0018), coarse channel 7 (1665.53–1668.46 MHz, 1,048,576 channels of 2.794 Hz, 49 steps of 6.08 s), read by HTTP range reads with lheld/fetch_cc.py (copied unchanged). Range-rate from JPL Horizons as in lheld/cf.py.

## Step A: measure the receiver-frame structure from the OFF scans only

For each OFF scan k: the raw time-median spectrum M_k(j); a running median over 1025 channels as baseline; R_k(j) = M_k/baseline − 1. Line strength S(j) = median over the three OFF scans of R_k(j). Variability V(j) = for each OFF scan the per-channel temporal robust scale (1.4826 × MAD over the 49 steps) of x/median − 1, then the mean over the three OFF scans. Each of S and V is converted to a robust z over the coarse channel (median, 1.4826 × MAD), the nine DC channels excluded. Structure channels: z_S ≥ 5 or z_V ≥ 5, dilated by ±1 channel (the boxcar width). If this mask exceeds 25% of the channels, the threshold rises to 8 for both, fixed now.

Comb measurement: the Fourier power of z_S across the coarse channel (DC channels set to 0), reported as spacings in Hz between 8 Hz and 3 kHz, top ten peaks with power over the median; the local comb at 1665.61512 MHz (C01/C02) measured as tooth positions in S within ±500 Hz. Reported: the mask fraction, the structure channels within 1668.40–1668.46 MHz (the radiosonde edge).

## Step B: the main test (masking)

The lheld procedure (lheld/cf.py and the align/hits/cluster code of lheld/run_lheld.py, z_on 2.5, z_off 2.0, ±1 channel tolerance, 10 Hz clustering, 40 false range-acceleration frames from seed 11, swap counted) is run three ways on the same data:
- B0 unmasked: sanity; the true count should reproduce 13.
- B1 masked: in every scan, normalized values (x/median − 1) at structure channels are set to 0 before the boxcar and the path sum.
- B2 ten random masks: the structure mask circularly shifted by ten offsets drawn uniformly (seed 23) between 10,000 and 1,038,576 channels; true frame and swap only.

## Step C: supporting predictions

- P1 overlap. For each of the thirteen and each scan, the path's channels (per step, from the Horizons range-rate, ±1 channel) and the fraction O of steps whose window touches a structure channel. ΔO = mean over ON scans − mean over OFF scans. Controls: 13,000 rest frequencies uniform over the coarse channel, excluding ±10 Hz of the thirteen and the DC region; the thirteen's mean ΔO compared with 10,000 random 13-subsets of the controls. Supportive if at or above the 95th percentile.
- P2 prediction of per-scan contributions. W = the sum over steps of the largest z_V in the path's window. Spearman ρ between the 78 per-scan z_tracked values (oh13_candidates.csv) and W; null from 10,000 permutations of W within each scan. Supportive if ρ > 0 and p < 0.05.
- P3 descriptive: for each structure comb spacing s found in Step A with power ≥ 10 × the median, each candidate's per-scan topocentric mid-path phase relative to the nearest tooth (from S), ON against OFF. For C03, the distance of its per-scan path from the nearest structure channel, set beside ChatGPT's finding that the middle ON prefers a frequency about one channel off the shared track.

## Verdict (B1 against B0, B2)

- EXPLAINS: the masked true count is at most the masked null mean + 2 sd, and it is below at least 9 of the 10 random-mask true counts.
- DOES NOT EXPLAIN: the masked true count exceeds the masked null maximum.
- PARTIAL: anything else.
P1 and P2 are reported beside the verdict and do not change it. If B0 does not reproduce 13, the difference is reported and the verdict is computed against B0 as found.

## Deviations

Any departure from this plan is recorded in RESULTS-comb.md with its reason.
