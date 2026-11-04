# RESULTS-comb: receiver-frame structure and the thirteen (frozen test)

Plan: comb/PLAN-comb.md, sha256 75a991d4cc60fdbd45aa7e9c718b6902f9c1cb5269fa01f1c2d4961aedd1e08e, frozen before the structure measurement. Data: GBT blc23 rawspec.0000, 2025-12-18, scans 0013–0018, coarse channel 7 (1665.53–1668.46 MHz), read 2026-11-04 by comb/fetch_cc.py (lheld's, unchanged; fetch.log). Runner comb/run_comb.py (sha256 2e6b522c…), output comb.json (sha256 75e67c5e…), log run.log. Run 2026-11-04, 15:33–15:37 EST, one pass, no errors.

**Verdict: DOES NOT EXPLAIN.** With every receiver-frame structure channel masked, the comet frame keeps 12 clusters against a masked false-frame null of 3.78 ± 2.09 (maximum 9; no false frame reaches 12). The mask removes C02 and nothing else.

## Step A: the structure in the OFF scans

- Structure channels (z ≥ 5 in line strength S or in variability V, three OFF scans): 15 core channels, 31 after the ±1 dilation, 0.003% of the coarse channel. Line strength gives 11, variability 9. The threshold stayed at 5 (the 25% fallback did not apply).
- Nearly all of them sit in the 1665.61512 MHz complex of C01 and C02: within ±500 Hz of 1665.61512, S and V reach 66.6 and 35.0 at 1665.615119 MHz, with further structure at 1665.615116–1665.615181 and 1665.615060–1665.615063 MHz.
- The radiosonde edge (1668.40–1668.46 MHz, 20,413 channels) holds no structure channel; its maxima are z_S 3.96 and z_V 4.20.
- No comb across the channel. The ten strongest Fourier peaks of z_S between 8 Hz and 3 kHz spacing stand 15.4–18.4 times the median power (9.69, 18.58, 23.24, 15.47, 8.38, 103.26, 24.28, 17.73, 1685.67 and 94.12 Hz). For about 365,000 independent bins of noise the expected maximum is ln N / ln 2 ≈ 18.5 times the median, so all ten are at the noise expectation. The 60.35 Hz teeth of the C01/C02 complex are local to it.

## Step B: masking

| run | true ON | swap | false ON mean ± sd (40) | false max | fraction of false ≥ true |
|---|---:|---:|---|---:|---:|
| B0 unmasked | 13 | 1 | 3.75 ± 2.05 | 8 | 0.0 |
| B1 structure masked | 12 | 1 | 3.78 ± 2.09 | 9 | 0.0 |
| B2 ten random masks (same mask shifted) | 13 in all ten | 1 in all ten | — | — | — |

B0 reproduces the original count and null exactly. B1 removes C02 (1665.604608 MHz) and keeps the other twelve, C01 among them: C01 crosses the complex's side structure without its masked core channels. The masked count stays above every masked false frame, which is the plan's DOES NOT EXPLAIN condition. The drop of one cluster is below all ten random-mask counts, so the mask acts where it was expected to, on C02, and nowhere else.

## Step C: supporting predictions

- P1 overlap. The mean ON-minus-OFF overlap of the thirteen is 0.011, at the 99.88th percentile of 10,000 random 13-subsets of 13,000 control rest frequencies (control mean 0.000 ± 0.003; 0.05% of controls touch a structure channel at all). The whole of it comes from C01 (−0.116) and C02 (+0.259). C03–C13 have an overlap of 0 in every scan, ON and OFF.
- P2 per-scan contributions. Spearman ρ between the 78 per-scan z values and the summed variability W along each path is 0.104, one-sided permutation p 0.039 (within-scan permutations, 10,000). It is carried by C02 (0013 z 57.35, W 380.8). Post hoc, outside the plan (posthoc_p2.py, posthoc_p2.log): without C01 and C02, ρ 0.069, p 0.11, and none of the remaining 66 rows touches a structure channel.
- P3 phases. The plan's rule (Fourier power ≥ 10 × median) admitted all ten Step A peaks, which are at the noise expectation; the per-scan phases against them are recorded in comb.json and carry no comb. C03's paths lie 10,350–10,418 channels (about 29 kHz) from the nearest structure channel in all six scans, with no step within one channel. ChatGPT's finding, that C03's middle ON prefers a frequency about one channel off the shared track, has no receiver-frame structure nearby to come from.

## Reading

Receiver-frame structure in this coarse channel is one line complex at 1665.615 MHz. It accounts for C02, touches C01, and does not reach C03–C13 in any scan. The cadence alias it would take for ON paths to sample comb teeth and OFF paths to fall in gaps has no comb to work with: the channel holds no periodic structure above noise. The comet-frame excess survives the mask at 12 against a maximum of 9 in forty false frames. Structure fixed in the receiver's frame, as these OFF scans measure it (median-line strength and temporal variability at 2.8 Hz and 6.1 s), is excluded as the source of C03–C13. Interference whose structure is absent from the OFF scans, or present only at scales finer or coarser than this measurement, remains open, as do the other items of the work plan (below-threshold siblings, background models, injection with the original detector).

## Deviations

- One post hoc computation, labelled and kept separate (P2 without C01 and C02).
- The raw spectra (raw/, six files, about 1.2 GB) were deleted after the run; fetch_cc.py re-reads them by name from the public directory.
