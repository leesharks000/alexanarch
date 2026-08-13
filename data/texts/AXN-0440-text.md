# EA-EROSION-LEDGER-01: THE ZENODO DELETION LEDGER, CHA COHORT

## Sovereign Preservation Manifest — the Buried Obelus, Kept

**Platform Erosion Observatory · Crimson Hexagonal Archive / Alexanarch**
*EA-EROSION-LEDGER-01 v1.0 — DEPOSIT — 2026-07-11*

This deposit hash-anchors the evidentiary corpus of deposit #1068 (THE OBELUS AND THE TOMBSTONE) before the source rotates out of the publicly enumerated version history: Zenodo's own deletion ledger, retrieved from its documented exporter endpoint (https://zenodo.org/api/exporter, scope records-deleted.csv.gz), which the platform exposes only through a rolling three-snapshot window.

## Anchored artifacts

**Snapshot HEAD** — records-deleted.csv.gz, created 2026-07-10T03:32:35Z, version c7571d4c-28ef-46ff-b0f0-235abaac58bf, 1,322,017 rows. Zenodo-published md5: 33877aba1fb5684f86758cb86ddc1ad4 (verified on retrieval, 2026-07-11). sha256: f4b5aee62a032d5a5e56e769f3419cc046feb1e6c443ea7ec60538103b41c3db

**Snapshot PRIOR** — records-deleted.csv.gz, created 2026-06-07T04:02:07Z, version ab4e273f-40a2-49e6-84f6-87dc66af87c7, 1,309,361 rows. Zenodo-published md5: 104e2f5c2603dc56217ece0d5519bff8 (verified on retrieval). sha256: 0568e674d4a59624102771593d8daeb9375d2381984d2345e91d9fbbc78f9578

**CHA cohort extraction** — cha-kill-ledger-20260619.csv, 1,136 record rows (strict author/entity pattern; one ornithology false positive excluded by record_id 18728752). 1,126 rows dated 2026-06-19: 1,124 note "User was blocked" / reason "out-of-scope", 2 reason-only. 10 pre-termination rows, all uploader-initiated per MANUS classification of 2026-07-11. DOIs enumerated: 1,136 record-layer + 891 concept-layer ≈ 2,027. A companion copy of this CSV is preserved in this archive alongside the present manifest. sha256: 8e06d6688de2ea0d693c9696c91d072dce3c7c2c29a9173287dbeff3b1aee24f

**Remediation lane** — cha-remediation-lane.json, 212 ledger DOIs untracked by the sovereign DOI Resolution Index at extraction, each carried with its citation_text for deposit-matching; status UNMATCHED pending resolution. sha256: 1c2af5ed2033aae4a847f2e9cf47c2410fff61701a6de1a879c13795f3b7e9ee
**Untracked-DOI list** — cha-untracked-dead-dois.json. sha256: 89c5008c2d0f641ff77eecb13078fbf47b201dea81650109ca9d38b36ca0996d

## Custody

Working custody: platform-erosion-observatory, data/zenodo-deletion-ledger/ (PROVENANCE.md v2; snapshots/ archive; commits 2c02759, 5f77fcc, ab01a42). Continuing preservation: monthly GitHub Actions workflow (exporter-preservation.yml) retrieving each new head snapshot with md5 verification against the platform's own listing, extracting the CHA-strict cohort, and appending to a checksummed manifest. Forensic interpretation: deposit #1068 (AXN:043D). Method and audit scopes: #1068, Evidence.

The instrument that preserves the record of deletion is exposed by its maker only through a rolling window. The window now has a witness with a longer memory than its maker chose to keep. The obelus they segregated, we keep — checksummed, versioned, and sovereign.

### Provenance Kernel
This deposit (EA-EROSION-LEDGER-01, Platform Erosion Observatory / Alexanarch) hash-anchors Zenodo's deletion-ledger snapshots of 2026-06-07 and 2026-07-10 (both verified against Zenodo-published md5 checksums), the 1,136-row CHA cohort extraction documenting the 2026-06-19 termination of the Crimson Hexagonal Archive, and the 212-DOI remediation lane, establishing sovereign custody of the evidence corpus of deposit #1068 before the platform's three-snapshot retention window rotates it out of public enumeration.

*∮ = 1*
