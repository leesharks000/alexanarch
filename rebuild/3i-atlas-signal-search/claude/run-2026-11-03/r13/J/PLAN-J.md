# PLAN-J: part J of PLAN-r13, made exact before any of its products is read

Written 2026-11-18, before any J product exists. It fixes the statistics that PLAN-r13 part J names (v2, sha256 16236a7d…) and changes nothing that plan states. Hash in PLAN-J.sha256.

## Data and decoding

As voltages/delaymod (PLAN.md v1, dm.py hash 190992d5…).
- GBT blc23 GUPPI raw voltages, scans 0013–0018, coarse channel 7: 2^20-sample frames, 49 integrations of 17 frames per scan.
- The frames are streamed again and only products are kept.
- Products computed: P1 = |FFT x|² + |FFT y|², P2 the same on x², y², and P4 the same on x⁴, y⁴.

## Frames

- **True frame:** the comet frame (JPL Horizons deldot at GBT, as delaymod).
- **False frames:** 400 false-drift frames. Each adds an acceleration offset dv·(t − T0), with dv drawn as in delaymod: default_rng(23), uniform(0.03, 1.0), random sign, × c / 1.42 GHz.
- Frame 0 is the comet frame; frames 1–400 are the false frames.

## Variants

- **V0:** all 49 integrations.
- **V2:** the integrations whose rows the pointing telemetry marks off-target are dropped, as r13 part A found: 0013 [0]; 0014 [0, 1]; 0015 [0, 1]; 0016 [0, 1, 2]; 0017 [0, 1]; 0018 [0]. One integration is one rawspec row (17 frames, 6.085 s).
- V2 is added because r13 found the L-band excess in those rows. It is computed by the same code path.

## J1, suppressed carrier, and P1 as control

For each product m ∈ {1, 2, 4}, variant and frame, delaymod's M1 procedure is applied unchanged:
- median-normalise each integration and apply a 3-bin boxcar;
- shift by m·FC·(v − v0)/c/Δ and stack;
- compute the robust z and mask DC;
- keep a sparse list of z ≥ 2.

Scans are registered to 0013's rest coordinate by v0. The count is the number of clusters (gap 4) of positions with z ≥ 2.5 in all three ON scans and < 2.0 in all three OFF scans (±1 bin).

## J2, a delayed copy of a comet-tracking tone

Per scan, variant and frame:
- The stacked P1 z, clipped at zero, is Y(f).
- The pair product is Q(Δ) = Σ_f Y(f)·Y(f + Δ), for Δ = 5 … 2000 bins (14 Hz to 5.6 kHz). Lags of 4 bins or fewer are excluded because the boxcar correlates them. ±Δ are the same pair.
- q(Δ) is Q's robust z across the 1,996 lags.

A copy pair moving together accumulates only in the frame it tracks. The combined statistic is T2 = max over Δ of min over the ON scans of q(Δ), at lags where all three OFF scans have q < 2.0.

## Decision

A J statistic counts if its comet-frame value exceeds the 99th percentile of its 400 false frames and replicates in each ON scan separately:
- For J1, each ON scan's own count of positions with z ≥ 2.5 and that scan's OFF partner < 2.0 (pairs 0013/0014, 0015/0016, 0017/0018), ranked among the 400.
- For J2, each ON scan's max q, ranked among the 400.

p is reported as (1 + number of false frames ≥ true)/401. The decision is applied to V0 and V2 separately and both are reported.

## Gate

Before any J statistic is read, J1 for m = 1, V0, frame 0 must reproduce delaymod's comet-frame count of 11 (results.json, m1 at 2.5/2.0). If it does not, nothing in J is read and the discrepancy is reported.

## Known limit, stated before the result

r13 part F found the false-frame null non-exchangeable: frames with small offsets rank higher. The rank is therefore also reported against the 40 false frames with the smallest |dv|.

## Storage

- Sparse z ≥ 2 lists per scan, m, variant and frame, compressed.
- Q(Δ) arrays per scan, variant and frame.
- Hashed in J-PRODUCTS.sha256. Nothing raw is kept.
