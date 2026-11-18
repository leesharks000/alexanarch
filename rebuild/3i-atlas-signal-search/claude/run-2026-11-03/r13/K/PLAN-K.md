# PLAN-K: complementary frequency switching, made exact before any K product is read

Written 2026-11-18, before any K product exists. Proposed by a ChatGPT reading of ΦΑΙΝΕΤΑΙ ΜΟΙ v3.1 (pasted by the author, 14:16): receive the data in a declared frame, look for a relation among individually weak components, and make the relation answerable to another encounter. Hash in PLAN-K.sha256.

## What it tests that nothing before it tested

- r13 J1 and J2 stack the integrations and keep no time structure. J2's pair product Q(Δ) finds two tones present together.
- Part K looks for two comet-tracking tones that alternate in time: power rising at A as it falls at B. Their sum S(t) = P_A + P_B can stay flat, so neither tone stands out in a stack, while their difference D(t) = P_A − P_B carries the pattern.

## Data and decoding

As r13 J: voltages/delaymod dm.py (hash 190992d5…), GBT blc23, scans 0013–0018, coarse channel 7, 49 integrations of 17 frames per scan. Only P1 = |FFT x|² + |FFT y|² is formed, per integration, and only products are kept.

## Frames

- **The comet frame:** frame 0, the JPL Horizons deldot at GBT, as J.
- **The stationary frame:** no Doppler correction.
- **False frames:** the first 200 of J's 400 false-drift frames, the same default_rng(23) draw.

## Variants

V0: all 49 integrations. V2: the off-target rows dropped, as J (0013 [0]; 0014 [0, 1]; 0015 [0, 1]; 0016 [0, 1, 2]; 0017 [0, 1]; 0018 [0]).

## The relation

1. Per integration, median-normalise each channel across integrations and apply a 3-bin boxcar, as J. Shift each integration to the frame and mask DC (±4 bins).
2. Standardise each channel across the kept integrations: a(t).
3. For each separation Δ ∈ {8, 32, 128, 512, 2048} bins (22 Hz, 89 Hz, 358 Hz, 1.43 kHz, 5.72 kHz; bin 2.794 Hz), the complementarity of the pair (f, f+Δ) is ρ(f, Δ) = −mean_t a_f(t)·a_{f+Δ}(t). Two independent channels give ρ near 0, and complementary switching gives ρ near +1.
4. ρ is given its robust z across f within each Δ: ρz.
5. The same ρ is formed on the first half of the kept integrations (h1) and on the second (h2).

## Statistics

- **K1, replication.** Scans are registered to 0013's rest coordinate by v0, as J. The count is the number of clusters (gap 4) of positions f, for any Δ, where ρz ≥ 3 in all three ON scans and < 2 in all three OFF scans (±1 bin). For a single scan: ρz ≥ 3 in that ON scan and < 2 in its OFF partner.
- **K2, prediction from the edge.** In each scan and for each Δ, select the 20 pairs with the highest ρz on h1. The score is the mean of their h2 ρz, which is the relation the selection did not see. A scan's K2 is the largest of its five Δ scores. K2 combined is the minimum of the three ON scans' K2.
- **K3, a switching period.** In each scan and for each Δ, take the 50 pairs with the highest ρz and form D(t) = a_f − a_{f+Δ}. A pair's score is the largest normalised projection of D on a square wave of period p ∈ {2, 4, 8, 16} integrations, maximised over phase. A scan's K3 is its largest pair score over the five Δ. K3 combined is the minimum of the three ON scans' K3.

## Decision

A K statistic counts if all of the following hold:
- its comet-frame value exceeds the 99th percentile of the 200 false frames;
- it exceeds the stationary frame's value;
- it does so in each ON scan separately;
- for K1 and K2, it exceeds the same statistic in each ON scan's OFF partner.

p is (1 + number of false frames ≥ true)/201. V0 and V2 are reported separately. The 40 false frames with the smallest |dv| are reported as well, since r13 part F found the null non-exchangeable.

## Gate

Before any K statistic is read, the comet-frame stacked P1 z of 0013, V0, computed by K's own code, must give the same z ≥ 2 positions as J's m1_V0_f0 list. If it does not, nothing in K is read.

## An injection, before the data

kinject.py puts a complementary pair (Δ = 128, period 8 integrations, drifting 300 bins over the scan) into synthetic Gaussian noise of the same shape (47 × 2^20), and runs kcore on it in the true frame, the stationary frame and one false frame. It touches no real data. Result, in INJECT.json, run before any K product existed:
- at ±1.2 noise sd per integration, the pair has ρz 3.9 in the true frame, and K3 finds it with score 0.90 at period 8, against 0.46–0.53 as the largest noise score; in the stationary and false frames its ρz is −0.8 and −1.6;
- at ±0.9 sd its ρz is 2.8, below the K1 threshold and outside the K3 top 50; at ±0.6 sd it is 1.3.

So K is sensitive to a complementary pair whose two members each swing by about one noise sd from integration to integration. In a stack such a pair sums to nothing, so J and the earlier searches could not see it. In a single scan the largest noise ρz across 2^20 channels reaches 4.4, which is why K1 asks for all three ON scans.

## Known limits, stated before the result

- Frequency-switching interference is an ordinary source of complementary pairs. The OFF and stationary requirements are there for it.
- A gain change between integrations moves every channel together. That is the opposite sign to complementarity: it pushes ρ down everywhere, and the robust z across f absorbs the shift.
- Any pattern-shaped structure found outside the statistics is reported as found, under its own description, and is not counted.

## Storage

Sparse lists of ρz per scan, variant, frame and Δ: ρz ≥ 3 for ON scans and ρz ≥ 2 for OFF scans, which is what K1 reads; the h1 and h2 values at the top 20; and the K3 scores and phases at the top 50. Hashed in K-PRODUCTS.sha256. Nothing raw is kept.
