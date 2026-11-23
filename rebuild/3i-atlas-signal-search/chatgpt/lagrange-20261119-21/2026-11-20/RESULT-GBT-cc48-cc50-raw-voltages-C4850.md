# GBT cc48 and cc50 in the raw voltages: not the comet; one faint cc48 line unresolved

**2026-11-20.** Executed on the public GBT voltages, all six scans of coarse channels 48 and 50, both polarizations: the next targets after cc19 in [PLAN-occupied-bands-comet-matched-discrimination.md](PLAN-occupied-bands-comet-matched-discrimination.md). Companion to [RESULT-GBT-cc19-raw-voltages-C19.md](RESULT-GBT-cc19-raw-voltages-C19.md).

Canonical run, frozen plan, code, hashes: [PLAN-C4850.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C4850/PLAN-C4850.md) (frozen before any product), [RESULTS-C4850.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C4850/RESULTS-C4850.md), [C4850-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C4850/C4850-PRODUCTS.sha256), extractor [c4850v.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C4850/c4850v.py), analyses [c4850a.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/C4850/c4850a.py).

The text below is RESULTS-C4850 as committed there.

---


Run 2026-11-20 under PLAN-C4850 (sha256 c2fd6d45…), GBT 3I/ATLAS scans 0013–0018 (2025-12-18), coarse channels 48 (FC 1546.875 MHz) and 50 (FC 1541.015625 MHz), all 833 frames per scan, both polarizations, streamed from bldata.berkeley.edu. Products and hashes in C4850-PRODUCTS.sha256.

## Reading

1. **cc50: not the comet.** The channel's ON-favoured lines are one emitter, and it is off-target. About 93 narrow lines with irregular spacing fill 1540.23–1540.38 MHz, strong in ON0013, present at the same topocentric bins in ON0015, faint in ON0017. They share one envelope: frame-to-frame correlation among the 16 saved cluster lines is 0.17 in ON0013 and 0.30 in ON0015, against 0.006 for random positions. Taken together they stand in the OFF scans: shared variation persists in OFF0014 (0.13), and their power there is 6–8% above the controls, against 29–54% in ON0013. The OFF power is about 15–20% of the ON power; a source at the comet would be under 0.1%. The band also carries a broadband excess of 2–4% in every scan, OFF included. On the comet track from ON0013, ON0015 sits at noise (median excess 0.25 against 2.57 at the fixed bin).
2. **cc48: one small open item.** A single line at 1546.97784 MHz (M4b Class B, ON0017, z 22.9 at 16 bins, drift 0) is present in ON0017 alone: per-frame power at the fixed bin 1.49 against controls 1.05 ± 0.10 (about 4σ), on the comet track 1.17. It is bursty (6-second rows from 0.92 to 2.95) and partly polarized (X–Y coherence 0.11 against 0.01–0.08 elsewhere). OFF0016 sits at 1.02 and OFF0018 at 1.12 (controls 1.04–1.07). It is too faint for the OFF scans to reach the 1% bound: they say only that its OFF power is below about a quarter of its ON power. It favours the fixed topocentric frequency over the comet track. Unresolved.
3. **The saved Class A events.** Of each channel's saved events, the median OFF/ON power ratio at the fixed bin is 0.81 (cc48) and 0.88 (cc50); for cc48's 9 saved Class A it is 0.74, minimum 0.57. None is at the comet.

## The frozen analyses

1. **Location per saved event.** 55 targets per channel (40 ON events, 15 role-reversed). Leads by the frozen rule: cc48 1, cc50 4. All four cc50 event leads are lines of the 1540.23–1540.38 MHz cluster (reading 1); the cc48 lead is the 1546.97784 MHz line (reading 2).
2. **Catalogue-free lines.** cc48: 23,568 line entries over the three ON scans, two frames and two resolutions; 4 leads, all the 1546.97784 MHz line. cc50: 22,839 entries; 350 leads in 142 frequency groups, every one inside 1540.229–1540.382 MHz (307 in ON0013, 43 in ON0015).
3. **Families.** The two-sequence search on each scan's 60 strongest lines reaches at most 6 in either channel, the random level. Neither channel holds a comb like cc19's.
4. **Kinematics, polarization and voltage** for the leads as above.

## Error recorded and amendment

1. The frozen lead rule tested each line alone against the noise in each OFF scan. For lines a few times above the noise, that cannot see an OFF component at 15–20% of the ON power. The cc50 cluster passed it line by line and failed it in aggregate (reading 1). The aggregate test over a shared-envelope family is an amendment after the freeze, recorded as such; it is the test any future lead must pass.
2. The first read-off ran out of time: c4850a.py re-read each compressed product from disk at every access. It now loads each array once. No result depends on the change.

## Pointing (telemetry.json, per scan, tracking rows)

| scan | role | az | el | offset |
|---|---|---|---|---|
| 0013 | ON | 88.5–89.3° | 8.7–9.7° | comet |
| 0014 | OFF | 88.5–89.3° | 10.3–11.3° | Dec +1° |
| 0015 | ON | 90.2–90.9° | 10.8–11.8° | comet |
| 0016 | OFF | 90.4–91.1° | 11.0–12.0° | RA +1° |
| 0017 | ON | 91.8–92.6° | 12.9–13.9° | comet |
| 0018 | OFF | 93.5–94.3° | 13.3–14.3° | Dec −1° |

The comet was low in the east. From Green Bank the geostationary belt lies below the horizon at these azimuths; its nearest visible stretch is about 10° away (az 98–103°, el 1–7°). No downlink satellite was in or near the main beam. Low elevation puts the far sidelobes on the horizon, where ground and airborne transmitters are.

## Limits

1. Narrowband, 2.794 Hz.
2. Direction is not measured beyond ON against OFF.
3. The v_ccNN_00NN.npz products (about 27–33 MB each) are hashed and kept outside git; c4850v.py regenerates them from the public voltages.

## Next

1. The cc48 line at 1546.97784 MHz: its time structure within ON0017 at full resolution (the per-frame complex spectra are saved), and whether it recurs anywhere in the band at another frequency on the comet track.
2. cc21–cc23 (the Iridium band), ChatGPT's next targets.
