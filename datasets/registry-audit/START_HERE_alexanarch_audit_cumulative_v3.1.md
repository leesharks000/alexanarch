# START HERE — Alexanarch Audit Cumulative v3.1

This package supersedes the v3.0 cumulative handoff for active continuation.

## Current position

- **928 / 1,426 unique records audited**
- **65.08% complete**
- **Contiguous coverage: #499–#1426**
- **Remaining: #1–#498 (498 records)**
- **Frozen commit:** `055429ac82edc967f09c4640ffd0b049cff78e6e`
- **Method:** v0.4
- **Repair performed:** No

## Primary files

1. `alexanarch_audit_ledger_v1.1.json` — authoritative 928-record cumulative ledger.
2. `alexanarch_audit_ledger_v1.1.csv` — flat review/export surface.
3. `alexanarch_audit_report_v1.1.md` — cumulative findings and upper-tail stop-lines.
4. `alexanarch_audit_batch_13_upper_tail_1399-1426_v1.0.json` — all 28 upper-tail adjudications.
5. `alexanarch_audit_boundary_validation_v3.1.json` — independent range/count/hash/package checks.
6. `alexanarch_audit_continuation_state_v3.1.json` — exact resume state.
7. `alexanarch_audit_method_core_v0.4.md` — governing method.

## Resume instruction

Audit **#1–#498** under method v0.4. Every record receives `FRONTMATTER_AND_IDENTITY_READ`. Preserve raw lifecycle uncertainty as `UNKNOWN`. Do not repair records until the full 1,426-record ledger has been merged and independently validated.

## Upper-tail result

The #1399–#1426 boundary contributed 25 net-new records after replacing three previously audited overlap rows (#1400, #1401, #1403). Newly discovered P0: #1417's v2.0 dataset record seats v2.1 primary files.
