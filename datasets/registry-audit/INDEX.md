# Registry Audit — Living Package INDEX
**State: AUDIT COMPLETE at frozen corpus boundary (#1–#1426, 100%, zero gaps) · snapshot 055429ac**
**Regenerated from live state 2026-08-04 (supersedes all prior INDEX figures; earlier internal contradictions — 928/74.89% era — retired).**

## Current live figures (regenerate from files; prose figures rot — §13 mode 3)
- Ledger: alexanarch_audit_merged_ledger_through_0001-0018_v1.0.json (1,426 rows, contiguous, sha in MANIFEST)
- Dispositions: data/audit/registration_dispositions.json **v5.1** (re-derived against current record state, then corrected: clearance requires the AUDIT'S recommendation satisfied, not merely the conflict tidy) — HARVEST 992 · HARVEST_WITH_WARNING 385 · **WITHHOLD 56**
- OAI feed: 1,373 records · dc:relation live · dc:source + per-record dc:publisher live (MECH-BATCH-1) · ResourceSync = doctrine site 10
- Venue truth: journal canonical corpus-wide (W6 COMPLETE); dc:publisher on all 1,426 frozen records; NH2/NHP creative-venue ruling applied (venues.json v1.2)
- Type vocabulary: **v1.2 RATIFIED (41 values)** — GENRE BURN-DOWN COMPLETE; only #1168/#1170 remain transitional (identity-blocked)
- In-history sweep: CLOSED with clean negative (repo history exhausted for the 68-target recovery queue); 6 version-label defects fixed; RF chain completed to v7.3 head; #1242/#1243 composing thread located (recovery_queue_R1b v1.9 tail governs)
- **STATE: one canonical derivation — `scripts/record_state.py`. Every emitter consumes it; `scripts/check_state_conformance.py` (state + page + OAI + BODY + FRONTMATTER) and `scripts/check_body_hygiene.py` (ENTITIES/RUNON/GLUED/HARDWRAP/SUBJECT/ESCAPED) are mandatory propagation gates (§5c). Current: state 0 divergences / 1,433; hygiene 128 records (GLUED 81, RUNON 31, SUBJECT 9, ESCAPED 7, HARDWRAP 2, ENTITIES 1); SUBJECT candidates are identity adjudications in §11, never auto-repaired.**
- Repair ledger: repair_ledger.json — **1187 rows** (R-0001 → current; tail governs)
- DW verified-clean register: DW-VERIFIED-REGISTER.json — **#1-#204 of 1,433 (14.2%)**, 0 rejects
- **AUDIT EXECUTION: AUDIT-DIRECTIVE-QUEUE.json is the work queue** (the audit's own `recommendation` field, grouped). Status: **52/127 satisfied, 75 open**. Of the open: **25 have NO TEXT** (external recovery only — MANUS exports, academia, threads, audio/video), **40 HAVE THEIR TEXT** and are metadata/normalization directives executable now, 10 other. Satisfaction is evidence-tested on the record, never asserted in prose.
- Audit-derived record fields now in use: `creator_roles` (role projection, strings preserved) · `version_basis` (ruling + prior claim + directive) · `date_semantics` (publication vs deposit) · `body_status.audit_disposition` (the audit's verdict travelling with the record)
- Workplan: WORKPLAN_OAI_REMEDIATION_v2.0.md — **decisions log is the authoritative running record**
- WRONG_OBJECT program: wrong-object-workup-2026-08-04.json v1.2 (match graph, recovery channels, adjudication findings)
- Recovered bytes: recovered/2026-08-04/ (SHA256SUMS sealed)

## Continuation state
- alexanarch_audit_continuation_state_v3.1.json: **RETIRED — nothing to continue.** Preserved as historical artifact of the 928-row era.
- Forward-audit rule for deposits #1427+: **RATIFIED (MANUS 2026-08-04).** New mints audited AT MINT via method_core v0.4; audit row appended at mint; no standing audit:pending. Catch-up batch for the post-freeze backlog queued as the rule's first act.

## Reading order for a fresh session
1. WORKPLAN §5b + decisions log (bottom-up)  2. This INDEX  3. wrong-object-workup v1.2  4. repair_ledger tail
