---
deposit_number: 1408
hex: 0591
title: PEO Case 001 · T0 Enumeration of the Firenze crui.unifi Corpus (14,284 DOIs)
creator: Lee Sharks (Rex Fraction / Nobel Glas)
date: 2026-07-22
content_type: Dataset
license: CC-BY-4.0
substrate: AI-assisted (substrate) — AI used as drafting substrate under human editorial governance
version: v1.0
related_ids: "10.14454/t5qb-d995 (source: DataCite Public Data File 2025); https://alexanarch.org/data/peo-case-001-florence-fup.md (Case 001 file)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - Platform Erosion Observatory
  - PEO Case 001
  - DataCite
  - DOI
  - Firenze University Press
  - crui.unifi
  - prefix 10.13128
  - identifier migration
  - registration agency
  - digital preservation
  - recovery map
  - tier-2 enumeration
  - T0 snapshot
---

# PEO Case 001 · T0 Enumeration of the Firenze crui.unifi Corpus (14,284 DOIs)

## Description

Recovery map for the 14,284 DataCite DOIs formerly registered under client `crui.unifi` (Università degli Studi di Firenze; Firenze University Press) and abandoned by the registration-agency migration event of 2026-07-16T07:23:35Z.

The Platform Erosion Observatory's tier-1 census detected the client-count collapse (14,283 → 0) between 2026-07-13 and 2026-07-20 (Case 001, `data/peo-case-001-florence-fup.md`). This deposit resolves that figure to identifiers by streaming the DataCite Public Data File 2025 — a t0 snapshot frozen at 2026-01-06T20:11:59Z, approximately six months prior to the deletion — and filtering on `client_id=crui.unifi`.

The extraction yields 14,284 unique DOIs, all under prefix `10.13128`: 14,282 in `findable` state and 2 in `registered` state (the +1 discrepancy against the tier-1 findable count of 14,283 is consistent with a single state transition in the six-month interval between snapshot and census). Update-time distribution places 12,308 DOIs (86.2% of the corpus) in a four-month mid-2020 metadata refresh window (2020-06 through 2020-09), with secondary refresh points at 2021-03 (528 DOIs) and 2023-03 (352 DOIs). Long tail through 2024-08.

Every DOI in the enumeration currently resolves to `https://journals.fupress.net/inactive-doi/`. The corpus spans the Firenze University Press journal portfolio: `ijae` (Italian Journal of Anatomy and Embryology, 1,959), `aestimum` (1,862), `techne` (875), `rief` (624), `studi_formaz` (578), `formare` (536), `lea` (520), `studi_slavis` (465), `aisthesis` (433), and 200+ other journal codes.

Two edge-case identifiers embed the prefix a second time in the suffix (`10.13128/10.13128/ahs-23289`, `10.13128/10.13128/rea-25108`) — preserved unaltered from source; flagged for any re-registration pass.

The enumeration is redistributed under CC-BY-4.0 from the DataCite Public Data File 2025 (landing DOI `10.14454/t5qb-d995`) and constitutes a public recovery map for the 10.13128 corpus.

## Methodology

The 2025 Public Data File is a 34.4 GB tar containing per-month members at `dois/updated_YYYY-MM/YYYY-MM.csv.gz`, each a compact projection of `(doi, state, client_id, updated)` for DOIs whose last update fell in that month. Extraction streams the tar via chunked HTTP Range requests to `datafiles.datacite.org` (~180 chunks at 128 MB), each chunk triggering a fresh 302 redirect to a newly minted 5-minute S3 presigned URL. This bypasses both bulk download (615 GB decompressed / 32 GB compressed) and the single-connection expiration failure mode encountered with linear streaming. The tar is parsed with Python's `tarfile` module in stream mode over a file-like `RangeStream` adapter. A global filter selects records where `client_id == 'crui.unifi'` while maintaining a byproduct per-client census counter. All processing is in-memory except the target enumeration output.

## Falsification Conditions

The claim that 14,284 identifiers formed the crui.unifi corpus at 2026-01-06T20:11:59Z would be weakened by production of any DataCite-registered 10.13128 DOI, dated before that timestamp, that does not appear in the enumeration. It would be strengthened by an independent extraction from the same source file (either by DataCite themselves, by Firenze University Press, or by a third party) producing a matching enumeration. The claim that these DOIs were deleted on 2026-07-16 relies on the client record's `updated` field visible in DataCite's public API; a contradicting value would falsify the deletion timestamp.

## Files

- https://alexanarch.org/data/peo-case-001-florence-fup-enumeration.tsv
- https://alexanarch.org/data/peo-case-001-florence-fup-t0-summary.json
- https://alexanarch.org/data/peo-case-001-florence-fup.md (companion case file)
