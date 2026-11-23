# Recovered archive verification — 2026-11-19

Two prior research archives were recovered from the user's saved Library, materialized, and inspected in this session. These SHA-256 hashes are for the **original ZIP bytes in the local recovered copies**; they do not assert the original upstream data were re-downloaded or independently reanalyzed.

| Archive | Size, bytes | ZIP entries | SHA-256 | ZIP CRC integrity |
|---|---:|---:|---|---|
| ATA-3664-association-progress-2026-11-17.zip | 8,374,141 | 30 | `5ff10be4daf0b88138c10a4abb6a451e0698ab7897af2ec9c87d0cbe3047529e` | PASS |
| GBT-full-cadence-acquisition-checkpoint-2026-11-16.zip | 1,366,866 | 21 | `3774f71b959cda1a5530c4cf4e95ef8f1465ad30e46ac0ab8be4fd02690cb18d` | PASS |

For the GBT checkpoint, all **19 entries in its own MANIFEST.json** match their stored SHA-256 hashes (0 failures). It reports 10,056 source blocks checked, a per-scan 1,676-block header audit, no reported drop counters and calibration off. ON17 first TRACK occurs at 1.610612736 s with 1,667 TRACK blocks and 9 UNKNOWN initial blocks. These are recorded status/pointing fields; they do not verify celestial origin of the radio features.

The ATA 3664-MHz archive contains plan, code, an old-scan association result, saved windows and forecast inputs. Its original plan explicitly reserved scans 6–8 for prospective validation; those reserve data **have not been decoded here**. This archive is **not** the 1631.75–1632.08 MHz six-event dataset. Do not conflate the two experiments or treat its already-exposed first-six-scan outputs as held-out evidence.

These ZIP files remain preserved in the user's Library. **Their binary bytes have not been pushed to GitHub** in this commit. The original 2.55 MB BRIDE D19 and later Mandala packages remain unverified/missing in the resumed workspace.

Reference protocols:
- [1632 MHz discrimination v1](PLAN-MSS-1632-discrimination-v1.md)
- [Mandala held-out v1](PLAN-MANDALA-multiview-heldout-v1.md)

**Current outcome:** research protocols frozen; archive integrity verified; no new emitter detection claimed.
