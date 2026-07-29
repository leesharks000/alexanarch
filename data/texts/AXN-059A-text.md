---
deposit_number: 1417
hex: 059A
title: "Deletion Semantics Conformance Fixture v2.0 — The Ratified-Axes Release: A Known-Bad Identifier Corpus (EA-OKF-FIXTURE-01 v2.0)"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-07-28
content_type: Dataset
license: CC-BY-4.0
substrate: ""
version: v2.0
axn_schema_version: v2
protocol_version: AXN-1.0
keywords:
  - deletion semantics
  - conformance fixture
  - known-bad corpus
  - tombstone
  - never_landed
  - presence axis
  - OKF
  - knowledge-catalog
  - DataCite divergence
  - DOI
  - identifier persistence
---

# Deletion Semantics Conformance Fixture v2.0 — The Ratified-Axes Release: A Known-Bad Identifier Corpus (EA-OKF-FIXTURE-01 v2.0)

## Description

The known-bad corpus offered to GoogleCloudPlatform/knowledge-catalog issue #207 and taken up for conformance fixtures: 111 cases across 16 classes drawn from the 2026-06-19 termination event and its aftermath, each expressed in the thread's ratified axes (validity / presence / edges; presence sparse with exactly removed and never_landed as named states; reason objects with not_disclosed first-class; the removal-fact/content-destruction split embodied by two disclosed producer withdrawals). Verification at build, 2026-07-28: 109 identifiers probed — verified_tombstone 62/62 at HTTP 410; verified_registered 18/18 at 200; verified_erased_registration retained as the untrustworthy class (7×404, 5×410); the new registry_resolution_divergence class 8-for-8 with the DataCite API returning 200-findable while the DOI resolves 410-gone in the same minute. never_landed carried in both directions (record-without-content, content-without-record), commit-hashed. Drift ledger v1.0→v2.0 same-day: population 1,938→1,937 by disclosed withdrawal; recorded registered 75→73; observation drift on the v1 base zero. Deterministic builder and re-probe apparatus included. Canonical home: https://www.alexanarch.org/datasets/deletion-conformance-fixture/

## Falsification Conditions

Every number re-derivable: verify.py re-probes all cases; build_v2.py rebuilds deterministically from the archived v1.0 base and current sources. A class whose expectation fails on re-probe is a drift datum, recorded, not hidden.

# Deletion Semantics Conformance Fixture v2.0 (EA-OKF-FIXTURE-01)

Canonical content: datasets/deletion-conformance-fixture/ in the alexanarch repository — cases.json (111 cases, 16 classes, probed), cases-v1.0.json (archived base), build_v2.py (deterministic builder), verify.py (re-probe apparatus), README.md (the numbers and what they mean), manifest.json. This record is the fixture's address and abstract; the README carries the full verification tables, the drift ledger, the axes expression, and the provenance appendix pinning every figure to its derivation or its source. Offered to knowledge-catalog#207 per the standing exchange (the measurement apparatus behind a conformance fixture's known-bad corpus).
