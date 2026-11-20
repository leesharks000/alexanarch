# 3I/ATLAS BRIDE D19 — recovery handoff (2026-11-19)

**Status: partial recovery, NOT the complete BRIDE payload.** This note records results recovered from the preceding ChatGPT analysis after its thread reached its length limit. The complete ~2.55 MB prepared packet, calibration, scripts, compressed trace data, and original checksums have **not** been uploaded or verified here. Do not treat this note as a computational replication.

## D19 BRIDE candidate: recovered statistics

The search explored **positive temporal correlation among separated frequency groups**, using 16 groups. The maximum reported correlation by scan:

| GBT scan | Reported maximum correlation |
|---|---:|
| 0013 (ON) | 0.4246836150 |
| 0014 (OFF) | 0.2951484343 |
| 0015 (ON) | 0.3388315948 |
| 0016 (OFF) | 0.2875054038 |
| 0017 (ON) | 0.2877469876 |
| 0018 (OFF) | 0.2759581109 |

In the original nomination, the maximum ON value (0.4246836150) exceeded the maximum OFF value (0.2951484343). The reported contrast was **2.8937503536** against envelope cutoff **1.9729156985**. These are *search-stage* figures, not independent confirmation: the nominated fixed frequency-group pair **7/15 did not repeat** in the subsequent checks. The data do **not** identify an emitter or an extraterrestrial signal.

## Underlying trace specification (recovered, payload absent)

- 6 recordings × 2 group traces × 64 rows, float32 = **3072 uncompressed bytes** for the D19 compact excerpt.
- Previous session described an embedded base64/zlib decoder and a SHA-256 digest whose recovered prefix/suffix were `e16488f0…a6e86ca`. **The digest is incomplete here and MUST NOT be used to verify a payload.**
- Full reconstruction depends on original Green Bank Telescope raw data at https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/ .
- Recovered voltage selection: **blocks 1634–1641**, **source file 12 / local blocks 98–105**, **coarse channel 7**, approximately **16 MiB per scan**.
- Earlier session reported preparing a ~2.55 MB packet containing 16 group traces, D19 power/voltage excerpt, analysis code, calibration, provenance and checksums. This packet **was not committed** before thread cutoff and is not available in this recovery environment.

## Related work to preserve separately

The operator also authorized direct GitHub transfer of the later **Mandala, beam-audit, random-form, and phase-analysis** experiment packages because chat file downloads were failing. Those files are **not included** here; their numerical results and payloads should be transferred only if recovered, with original plan/version distinctions preserved.

The earlier 13 GBT spectral features remain unresolved. In a separate full-cadence raw-header audit, ON17 changed to `TRACK` near the comet at 1.610613 s, with its remaining 1,667 raw blocks in TRACK; an initial anomalous position therefore does not justify treating the entire scan as off target. This pointing correction does not confer artificial origin on the features.

## Recovery tasks

1. Recover the original 2.55 MB packet and copy **its exact bytes** into versioned research storage, checking the original complete SHA-256 manifest.
2. Upload run code, calibration assumptions, trace tables, null construction, contrast/envelope computation, and provenance as separate reviewable files.
3. Transfer the later Mandala/beam-audit/random-form/phase-analysis files without inventing results.
4. Independently rerun D19 and held-out fixed-pair 7/15 tests before any detection claim.

**Interpretive constraint:** BRIDE is a named Mandala operator; its symbolic role is distinct from the radio-statistical BRIDE experiment. A suggestive correspondence cannot by itself serve as a radio detection statistic.
