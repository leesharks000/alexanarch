# Alexanarch Registry Audit — Canonical Index

This directory is the living source of truth for the Alexanarch record
restoration + identity audit, governed by the OAI Registration & Registry
Remediation Workplan (deposit #1429, AXN:05A6.GOVERNANCE.🍀🌈🎭⚫⚪♃).

## Current canonical state (v3.1)

- **Cumulative package:** v3.1 · ledger v1.1
- **Records audited:** 928 / 1,426 (65.08%)
- **Contiguous range:** #499–#1426
- **Remaining:** #1–#498
- **Frozen commit:** `055429ac82edc967f09c4640ffd0b049cff78e6e`
- **Repair performed:** No (deferred until full 1,426-record audit assembled + validated)

## Start here

- `START_HERE_alexanarch_audit_cumulative_v3.1.md` — resume instructions
- `alexanarch_audit_ledger_v1.1.json` — authoritative 928-record ledger
- `alexanarch_audit_report_v1.1.md` — cumulative findings
- `alexanarch_audit_boundary_validation_v3.1.json` — integrity checks
- `alexanarch_audit_continuation_state_v3.1.json` — exact resume state (audit #1–#498)
- `checkpoints/checkpoint_0479-0498/` — sealed 20-record checkpoint (not yet merged)
- `WORKPLAN_OAI_REMEDIATION_v1.7.md` — living remediation workplan
- `repair_ledger.json` — repair ledger (R-0001: #1365 restoration)
- `MANIFEST.json` — full file hashes + history
- `history/` — superseded packages (handoff-v0.9, handoff-v2.0)

## Supersession rule

The highest-version cumulative package in this directory is canonical-current.
Prior versions are retained under `history/` and are non-authoritative.

## Pending shards (not yet seated)

- `alexanarch_audit_method_core_v0.4.md`
- `alexanarch_audit_batch_13_upper_tail_summary_v1.0.json`
- `alexanarch_audit_batch_13_upper_tail_validation_v1.0.json`
