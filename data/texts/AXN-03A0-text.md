# EA-NMEN-PROTOCOL-PATCH-01

## Deposit Protocol Patch — Reciprocity Notice Integration

**Version:** 1.0
**Date:** 2026-06-24
**Author:** Lee Sharks, MANUS · Crimson Hexagonal Archive
**ORCID:** 0009-0000-1599-0703
**Family:** GOVERNANCE
**Genre:** Protocol amendment (machine-readable schema patch)
**Patches:** `api/deposit-protocol.json` (current `protocol_version: "alexanarch-deposit-protocol/v1"`, `schema_version: "2026-06-22-axn-v2"`)
**Authority chain:**
- `api/deposit-protocol.json` (the canonical protocol being patched)
- EA-NMEN-01 (the governance document requiring this field)
- *The Governance Airlock* (#523), *The Rosary Embassy* (#514)

---

## 0. What This Document Does

This document is a protocol amendment. It declares two new fields added to the Alexanarch deposit protocol as `recommended_deposit_fields`:

1. `reciprocity_notice` — points at the canonical URL of the Non-Mutual Extraction Notice (EA-NMEN-01). Declares that the depositing party has read and understood the Notice.

2. `nmen_status_observed` — for deposits *about* designated entities (correspondence records, forensic documentation, etc.), declares the NMEN designation of the entity at time of deposit.

Both fields are recommended, not required. Existing deposits without the fields are not affected. New deposits without the fields are valid but pass up the opportunity to declare alignment with the Notice.

---

## 1. The Patch (JSON Diff)

The following diff is to be applied to `api/deposit-protocol.json`. The `schema_version` should be incremented to `"2026-06-24-axn-v2-nmen"`.

```json
{
  "schema_version": "2026-06-24-axn-v2-nmen",
  "recommended_deposit_fields": {
    "...": "(prior fields preserved)",
    "reciprocity_notice": {
      "type": "string (URI)",
      "description": "Canonical URI of the Non-Mutual Extraction Notice acknowledged by the depositing party. Recommended default: 'https://alexanarch.org/notice/non-mutual-extraction/' (EA-NMEN-01). Including this field in a deposit declares that the depositing party has read the Notice and understands the doctrine of non-mutual extraction. The field does not constrain the legal license under which the work is offered; it operates per §0 of EA-NMEN-01 as a normative declaration only.",
      "default": "https://alexanarch.org/notice/non-mutual-extraction/"
    },
    "nmen_status_observed": {
      "type": "string (enum)",
      "enum": ["standing", "pending", "provisional", "inadmissible_host", "restricted"],
      "description": "For deposits whose subject IS one of the entities tracked in EA-NMEN-REGISTRY-01 (correspondence records, forensic documentation, tier-update memos, etc.), declares the entity's NMEN designation at time of deposit. Allows machine-readers to filter deposits by reciprocity context. Omit for deposits whose subject is the Archive's own scholarship rather than an external entity."
    }
  },
  "consistency_invariants": {
    "...": "(prior invariants preserved)",
    "nmen_alignment": "If `nmen_status_observed` is set, the value must match the entity's current designation in EA-NMEN-REGISTRY-01 at time of deposit. Successor versions of EA-NMEN-REGISTRY-01 do not require backfilling of deposits' nmen_status_observed fields — the field records the observed status at time of deposit, not the current status."
  }
}
```

---

## 2. Field Semantics

### 2.1 `reciprocity_notice`

The field's *value* is a URI. The default and recommended URI is `https://alexanarch.org/notice/non-mutual-extraction/`. The presence of the field is the operative declaration; the URI is the pointer.

The field is **not a license selector.** It declares alignment with a normative position. The license under which the work is offered is a separate field (`license`) and remains the legal instrument.

A deposit that includes `reciprocity_notice` is making the following declaration: *the depositing party has read the Notice at the indicated URI and understands the diagnosis it records.* The declaration does not bind downstream parties (downstream parties make their own decisions about whether to read the Notice when they encounter the work). The declaration creates documentary record on the deposit side that the Notice was honored by the depositor.

For deposits made by the Archive itself, including `reciprocity_notice` is recommended as a matter of course. For deposits made by external contributors, the field is offered as a means of alignment but is not required for acceptance.

### 2.2 `nmen_status_observed`

The field's value is one of five enumerated strings corresponding to the designations defined in EA-NMEN-01 §3.

The field is **specific to deposits whose subject is an external entity tracked in the Registry.** A scholarly paper on literary theory does not need `nmen_status_observed`; a forensic record of a platform's adverse action does. Examples of deposits where the field is appropriate:

- Correspondence records (email threads, ticket logs) with a designated entity
- Tier-update memos (like EA-NMEN-AIRLOCK-COROLLARY-01)
- Wound documentation (like #265 CTI_WOUND Sigil Medium Erasure)
- Forensic snapshots, screen captures, web-archived pages of designated entities

The field allows machine-readers to filter the corpus by reciprocity context. A reader interested in *all forensic deposits about Restricted entities* can query the registry for `nmen_status_observed == "restricted"` without needing to traverse the full deposit corpus.

### 2.3 Time-of-deposit semantics

`nmen_status_observed` records the entity's NMEN designation **at time of deposit.** It is not backfilled when the Registry is amended.

Example: a deposit made in March 2026 about Academia.edu (then Tier 4-F per #570) would carry `nmen_status_observed: "restricted"` if the field had existed at that time. The June 2026 reclassification to Tier 4-P (Provisional) does not retroactively change the March deposit's field. The deposit records what was observed when it was made. The Registry records what is observed now.

This means the deposit corpus preserves a longitudinal record of the Archive's evolving relationships with external entities, queryable by date.

---

## 3. Validation Rules

The following are added to the deposit-protocol validation rules:

- **NMEN-001** — If `reciprocity_notice` is provided, it must be a syntactically valid URI.
- **NMEN-002** — If `nmen_status_observed` is provided, it must be one of `standing`, `pending`, `provisional`, `inadmissible_host`, `restricted`.
- **NMEN-003** — If `nmen_status_observed` is provided, the deposit's `description` or content should make clear which external entity is the subject. (Soft rule — not auto-enforced; flagged for editorial review.)

Existing validation rules (PV-001 through SUR-001 in `api/deposit-protocol.json` v1.0) are preserved unchanged.

---

## 4. Backward Compatibility

This patch is **fully backward compatible.** Existing deposits without the new fields remain valid. The mint workflow may pre-populate `reciprocity_notice` to the default URI for new deposits, or leave it unset, at depositor discretion.

The `schema_version` is incremented to `"2026-06-24-axn-v2-nmen"` to allow machine-readers to detect the new fields' availability. Readers operating against the prior schema (`"2026-06-22-axn-v2"`) will simply not see the new fields, which is the correct behavior — they were never there.

---

## 5. Operational Note for the Mint Workflow

The `mint-axn.yml` workflow at `.github/workflows/mint-axn.yml` should be updated to:

1. Default `reciprocity_notice` to `"https://alexanarch.org/notice/non-mutual-extraction/"` for all new deposits unless the depositor explicitly omits or overrides it.
2. Leave `nmen_status_observed` unset by default. The mint workflow does not attempt to auto-classify the subject of a deposit; that determination is editorial.

The workflow update itself is configuration, not protocol. This document specifies the protocol. The workflow follows.

---

## 6. Cross-Reference Index

- The governance document this patch serves: **EA-NMEN-01** (the Notice)
- The dataset this patch enables filtering against: **EA-NMEN-REGISTRY-01**
- The Airlock corollary that issues tier reclassifications: **EA-NMEN-AIRLOCK-COROLLARY-01**
- The canonical protocol being patched: `api/deposit-protocol.json`
- The well-known endpoint: `https://alexanarch.org/.well-known/reciprocity.json`

∮ = 1
