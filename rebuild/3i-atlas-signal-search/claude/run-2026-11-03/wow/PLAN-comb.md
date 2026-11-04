# Comb search across the Parkes 2025-07-31 band — frozen plan (2026-11-03, before any node other than blc05 is read for it)

Question. Does the 31.360 kHz comb seen at 1417-1426 MHz (RESULTS-wow.md) appear elsewhere in 704-3648 MHz during the same episode, or at other times?

Data. Every node of PKS_Jul_31_2025 with six .fil files (blc00-07, 10, 11, 13-17, 20-26). Episode: first S scan, samples 10-11. Baseline: samples 3, 4, 15, 16 of the same scan. r = mean(episode) / median(baseline) - 1, per channel.

Statistic. Per 4 MHz chunk, fold r at the period P channels (P = 31.360 kHz / 2 Hz = 15680, phase measured from absolute frequency so phases agree across chunks), smooth the folded profile with a 7-phase boxcar, take its maximum robust z and the phase of the maximum (Hz offset from the 1420.402360 MHz tooth grid). Controls: the same at periods for 31.250, 30.000 and 33.333 kHz.

Call. A chunk carries the comb if its fold z >= 6 and exceeds every control fold in that chunk by >= 2. Validation: blc05 1420-1424 MHz must pass.

Follow-up (only for chunks that pass): the same statistic in scan 2 samples 7-8 and scan 4 samples 10-11 (the other two episodes), and in every R scan at samples 10-11.
