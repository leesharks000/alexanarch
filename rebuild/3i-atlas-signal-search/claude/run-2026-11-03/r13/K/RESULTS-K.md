# RESULTS-K: complementary frequency switching (r13 part K)

Run 2026-11-18 under PLAN-K (PLAN-K.sha256, frozen 19:24:30Z before any K product existed). Products are hashed in K-PRODUCTS.sha256; the statistics are in K.json.

## Gate

K's own comet-frame stack of 0013, V0, gives exactly J's m1_V0_f0 list: 25,552 positions with z ≥ 2, identical. **Passed.**

## Result: no K statistic counts, in either variant

| Statistic | Variant | Comet frame | Stationary | False-frame p99 | p (of 201) | Nearest 40 | Counts |
|---|---|---|---|---|---|---|---|
| K1 (replication) | V0 | 0 clusters | 0 | 1 | 1.00 | 1.00 | no |
| K1 (replication) | V2 | 0 | 0 | 1 | 1.00 | 1.00 | no |
| K2 (prediction) | V0 | 0.249 | 0.305 | 0.392 | 0.10 | 0.12 | no |
| K2 (prediction) | V2 | 0.146 | 0.246 | 0.373 | 0.50 | 0.54 | no |
| K3 (period) | V0 | 0.524 | 0.436 | 0.544 | 0.065 | 0.098 | no |
| K3 (period) | V2 | 0.465 | 0.488 | 0.549 | 0.86 | 0.90 | no |

- **K1.** No position, at any of the five separations, has a complementary pair at ρz ≥ 3 in all three ON scans with all three OFF scans below 2. That holds in the comet frame, the stationary frame and every false frame. Each ON scan alone, against its OFF partner, has about 3,700–4,300 clusters across the five separations, and each ranks inside its null (p 0.50–0.995). Those clusters are the noise tail of 2^20 channels.
- **K2.** A pair selected on the first half of a scan does not carry its complementarity into the second half better than in false frames. In the comet frame the combined score falls below the stationary frame in both variants, and no ON scan exceeds its p99.
- **K3.** The largest square-wave scores in the comet frame (0.46–0.55) lie inside the false frames' range (p99 0.544–0.549). The noise maximum in the synthetic injection was 0.46–0.53. The one repeated pair, scan 0015 at Δ = 2048 bins, f = 969,332, period 4 integrations, scores 0.53 in both variants and is unremarkable within its scan (single-scan p 0.30–0.39).

## What this rules out, at the sensitivity measured

By the injection (INJECT.json), K detects a comet-tracking complementary pair whose two members each swing about 1.2 noise standard deviations per integration, at the separations and periods searched. A pair at about 0.9 sd falls below K1's threshold. In these scans of coarse channel 7 there is no such pair in the comet frame beyond what false frames produce. Weaker pairs, other separations, other periods, and channels other than coarse channel 7 are not tested.

## Run notes

- K was queued behind part H and started when H ended (19:39Z).
- The queued run reached its two-hour background limit during scan 0018. 0013–0017 were complete. 0018 was restarted alone and finished in 1,244 s, and kanalyze ran after it. The restart is recorded in k.log.
- The products (out/, 4 files per scan) are kept outside git, as J's are, and hashed in K-PRODUCTS.sha256.
