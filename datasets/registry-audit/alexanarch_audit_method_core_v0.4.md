# Alexanarch Audit Method Core v0.4

## Governing invariants

- Audit against frozen repository commit `055429ac82edc967f09c4640ffd0b049cff78e6e`.
- Read the work-bearing body, not title metadata alone.
- Preserve every earlier adjudication verbatim in `audit_history` on overlap.
- Do not repair records during the audit. Repair begins only after all shards are reassembled and the merged ledger is validated.
- `registration_disposition` values are `WITHHOLD`, `HARVEST_WITH_WARNING`, `HARVEST`, and `PENDING_REVIEW`.
- Lifecycle is represented by controlled `lifecycle_status`, explanatory `lifecycle_note`, `standing_basis`, and typed relations.

## Checkpointed macroshards

The operational target is now an **80-record macroshard** composed of four immutable **20-record internal checkpoints**. The increase changes packaging and repeated administrative overhead; it does not reduce the required read depth for any record. Every record still receives `FRONTMATTER_AND_IDENTITY_READ`.

- 20 records: immutable internal checkpoint.
- 80 records: preferred macroshard when no stop-line condition occurs.
- 40 records: canonical fallback shard produced by a stop-line split or retained from the earlier cadence.
- Earlier sealed 20-record and 40-record shards remain `LEGACY_VALID` or canonical as already declared and are never rewritten merely to fit the new cadence.

## Stop-the-line split rule

The active macroshard stops and reverts to 40-record packaging when any of the following appears: a P0 wrong-object or wrong-version finding; a source discontinuity; a new defect class not represented in the schema; a dense unresolved version chain; more than four P1 findings inside one 20-record checkpoint; or evidence that preflight missed a recurring conflict. Completed 20-record checkpoints remain valid. The macroshard splits at the nearest 40-record boundary; no completed read is discarded.

For the attempted `#1079–#1158` macroshard, deposit `#1107` triggered the rule because full-volume identity and DOI metadata were bound to a body explicitly declaring itself an announcement/sampler. The first fallback shard is therefore `#1079–#1118`; the next is `#1119–#1158`.

## Deterministic preflight

Before adjudication, compare registry/page/body layers across the full intended interval for title, creator, version, lifecycle language, manifestations, attached artifacts, projection losses, duplicate authority, and typed predecessor/successor statements. Preflight prioritizes reading; it never substitutes for reading.

## Severity and disposition

- `P0`: wrong object, wrong historical version, or incompatible primary manifestation. `WITHHOLD`.
- `P1`: primary manifestation absent, complete claim materially false, or creator authority materially conflicted. `HARVEST_WITH_WARNING`.
- `P2`: lifecycle, duplicate, role, title, version-field, date, or projection normalization defect. `HARVEST_WITH_WARNING`.
- `P3`: minor non-blocking normalization.
- `OK`: no material registration conflict observed. `HARVEST` unless a declared draft state independently requires a warning.

## External custody

`EXTERNALLY_CUSTODIED` means intentionally omitted from the working context. It does not mean missing or discarded. Such an artifact must be supplied and hash-verified before final merge if it is a required merge input.

## Compact-evidence acceleration

Beginning with deposits `#1199–#1398`, the audit uses a compact-evidence recording mode to reduce administrative overhead without reducing source-reading depth.

- Every record still receives `FRONTMATTER_AND_IDENTITY_READ`.
- The frozen body or explicit static tombstone is still opened for every deposit.
- Routine metadata-only restorations receive a short decisive finding rather than repeated prose.
- Wrong-object, wrong-version, creator-authority, lifecycle, and completeness conflicts retain explicit record-level evidence.
- Source transport is not treated as adjudication: deterministic preflight and compact notes may prioritize reading, but may not replace it.
- Twenty-record checkpoints remain immutable. P0 and dense-P1 conditions force 40-record sealing even when an 80-record interval was initially planned.

This change reduces narration, repeated schema prose, and packaging work. It does not reduce the number of records read, the identity fields compared, or the stop-line protections.
