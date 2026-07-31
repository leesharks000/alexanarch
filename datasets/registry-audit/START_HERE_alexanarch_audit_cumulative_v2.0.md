# START HERE — Alexanarch cumulative audit v2.0

## Frozen source
- Repository: `leesharks000/alexanarch`
- Commit: `055429ac82edc967f09c4640ffd0b049cff78e6e`
- Corpus: 1,426 deposits

## Canonical current state
- Cumulative unique audited records: **717**
- Coverage: **50.28%**
- Remaining: **709**
- Consecutive coverage: **#499–#1198** (700 records)
- Additional audited islands above #1198: **17 records**
- Batch 9 (#999–#1198): reassembled, validated, and merged
- Repair performed: **No**

## Current canonical files
1. `alexanarch_audit_ledger_v0.9.json` — complete normalized cumulative ledger
2. `alexanarch_audit_ledger_v0.9.csv` — regenerated flat projection of that ledger
3. `alexanarch_audit_report_v0.9.md` — cumulative human-readable report
4. `alexanarch_audit_master_index_v1.0.json` — lightweight overlap/resume index
5. `alexanarch_batch_9_reassembled_0999-1198_v1.0.json` — validated 200-record Batch 9 ledger
6. `alexanarch_batch_9_consolidated_summary_v1.0.json` — Batch 9 P0/P1 and totals
7. `alexanarch_audit_continuation_state_v2.0.json` — exact next operation
8. `PACKAGE_MANIFEST_v2.0.json` — file hashes and validation state

## Next exact operation
Audit **#1199–#1278** as an 80-record macroshard with four 20-record checkpoints. Eight deposits are known overlap re-reads: #1211, #1216, #1217, #1236, #1237, #1238, #1242, #1243.

## Packaging rule
At every completed batch boundary, replace the active handoff with one newly generated cumulative canonical set. Incremental prior START_HERE and resume-card chains are not carried into the active package.
