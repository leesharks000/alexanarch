# Ledger: Claude's runs of 2026-11-03 and 2026-11-04 (3I/ATLAS public-data signal search)

Snapshot of 2026-11-04 01:00 EST. Each search was frozen as a plan before its data were read; the plan's sha256 is recorded in its script and results. Files here are copied from the working directory unchanged; SHA256SUMS.txt at the folder root covers every file in the investigation folder. Runs still in progress at this snapshot are marked; later snapshots add to this ledger and re-hash.

| Search | Plan (sha256) | Data | Status at snapshot | Outcome |
|---|---|---|---|---|
| The thirteen at Parkes | pks/PLAN.md (336fcb1a…) | Parkes 2025-07-31, 1600–1728 MHz | complete (draft §7.13) | not continued |
| Full-band comet-frame search | pks/PLAN-fullband.md (2337ec83…) | Parkes 2025-07-31, 22 nodes, 704–3648 MHz | 17 of 22 nodes complete; blc22–26 running | blc10 and blc14 flagged by the rule, both wideband interference (pks/RESULTS-fullband.md); all others null |
| Wow!-guided intermittent search | wow/PLAN-wow.md (10ecba29…) | GBT 2025-12-18 L band; Parkes blc05 | complete | GBT null; Parkes flag is the 31.360 kHz impulsive comb (wow/RESULTS-wow.md) |
| 31.360 kHz comb across the band | wow/PLAN-comb.md (516e43a4…) | Parkes 2025-07-31, all 22 nodes | complete | concentrated at 720–1724 MHz, present in reference scans: local (wow/RESULTS-wow.md) |
| Hydrogen-line ratio search | ratio/PLAN-ratio.md (1cd2fef8…) | Parkes all nodes; GBT 2214–2401 MHz | complete | rule fires; driven by frequencies in satellite allocations, a control does the same; permutation p 0.11 (ratio/RESULTS-ratio.md) |
| 2380 MHz reply-frequency doublet | reply/PLAN-2380.md (e0754a9a…) | Parkes blc15; GBT rawspec.0000 cadence 0029 | Parkes complete; GBT running | Parkes: zero target doublets in topo, comet and barycentric frames; swap zero |

Deviations recorded in the results files: GBT cadences outside L band skipped (Wow!); Parkes injection tone moved from 1420.0 MHz (Wow!); ratio burst injection recalibrated to the W50 statistic; 2380 source position taken from Horizons (header printed beside it).

Blog sources: blog-sources/ holds the plain text of the September–October 2025 3I/ATLAS posts on mindcontrolpoems.blogspot.com, extracted 2026-11-03 from the Blogger feed, used to derive the ratio list.
