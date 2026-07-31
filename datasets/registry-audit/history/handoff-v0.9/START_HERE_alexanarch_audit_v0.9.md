# START HERE — Alexanarch Audit, Fresh Thread

Continue the Alexanarch pre-registration audit.

## Exact state

- Frozen commit: `055429ac82edc967f09c4640ffd0b049cff78e6e`
- Corpus: 1,426 deposits
- Fully merged audit: v0.8
- Unique records adjudicated: 539
- Resume at deposit: **#999**
- Next macro-batch: **#999–#1198**
- Use 40-record immutable shards:
  - #999–#1038
  - #1039–#1078
  - #1079–#1118
  - #1119–#1158
  - #1159–#1198

## Read only these first

1. `alexanarch_audit_method_core_v0.1.md`
2. `alexanarch_audit_resume_card_v0.5.md`
3. `alexanarch_audit_continuation_state_v0.9.json`
4. `alexanarch_audit_master_index_v0.9.json`
5. `alexanarch_recommended_record_schema_v0.1.json`

Do **not** read the old conversation. Do **not** load the full v0.8 ledger unless:
- a deposit appears in `audited_deposits`; or
- the macro-batch is ready to merge.

## Method

For every record, compare the frozen structured catalog entry with the actual work-bearing body or declared manifestation. Audit title, creator roles, version, lifecycle, type, work locus, manifestations, identifiers, dates, license, and relations.

Review depth: `FRONTMATTER_AND_IDENTITY_READ`.

Do not adjudicate by grep, body length, word count, title alone, or generic metadata defaults.

## Storage

Seal each 40-record shard as an immutable JSON file with SHA-256. Persist immediately after every P0. Merge only after all five shards validate deposits #999–#1198 exactly once.

At merge:
- use the full v0.8 JSON ledger;
- update overlaps and preserve prior rows in `audit_history`;
- publish v0.9;
- advance to #1199.
