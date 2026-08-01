# Alexanarch Record Restoration and Identity Audit — Cumulative Report v1.1

**Frozen source commit:** `055429ac82edc967f09c4640ffd0b049cff78e6e`  
**Method:** v0.4  
**Audit phase:** audit only; no record repair  
**Cumulative coverage:** **928 of 1,426 records (65.08%)**  
**Contiguous audited range:** **#499–#1426**  
**Remaining range:** **#1–#498**

## Upper-tail boundary completed

The final corpus boundary **#1399–#1426** received a fresh `FRONTMATTER_AND_IDENTITY_READ` at the frozen commit. Primary attachment or data loci were checked where the record's identity depended on them.

- Direct adjudications: **28**
- Prior overlap re-reads: **3** — #1400, #1401, #1403
- Net-new records: **25**
- Record repair performed: **No**

### Upper-tail severity

| Severity | Count |
|---|---:|
| P0 | 3 |
| P1 | 6 |
| P2 | 5 |
| P3 | 1 |
| OK | 13 |

### Upper-tail registration disposition

| Disposition | Count |
|---|---:|
| WITHHOLD | 3 |
| HARVEST_WITH_WARNING | 12 |
| HARVEST | 13 |

## Decisive upper-tail findings

### P0 — registration-blocking identity/version conflicts

1. **#1400 — Revelation First v7.1:** seats work-plan **v7.3**, not the named v7.1.
2. **#1403 — Revelation First v7.2:** seats work-plan **v7.3**, with concept/version DOI semantics unresolved.
3. **#1417 — Deletion Semantics Conformance Fixture v2.0:** the declared primary `cases.json` and `manifest.json` are **v2.1** at the frozen commit. The record also says 16 classes while the manifest reports 17.

### P1 — named primary manifestation absent or external

- **#1399, #1402:** truthful metadata-only restorations of the OKF proposal; the proposal text itself is absent.
- **#1414, #1415, #1416, #1418:** accurate address/abstract records whose full executable specifications live on linked external JSON/HTML surfaces rather than being seated self-contained in Alexanarch.

### Attachment and projection checks

- **#1407:** both the unrotated master and reading derivative of the handwritten Effective Act exist at the frozen commit. The payload remains image-borne and was not transcribed in this audit.
- **#1409:** the v1.0 PDF and HTML manifestations exist. The HTML masthead identifies the final form, but its document `<title>` still says `v1.0-rc1`; this is a P3 projection defect, not a wrong-object finding.
- **#1408:** the 14,284-row Firenze enumeration TSV and T0 summary JSON exist.
- **#1424:** the Sovereign Asset Registry and bidirectional crosswalk JSON files exist.

### P2 title/scope normalization

- **#1420:** general bookshelf/collection wrapper title seats a narrower Revelation-dating article.
- **#1421:** Jaussian-frame subtitle differs from the seated empirical-reception subtitle.
- **#1422:** machine-editions/two-marks wrapper differs from the seated machine-composition/interpretive-supply subtitle.
- **#1401:** v7.2 text aligns, but the relation to #1396 and the complete image set remain unmodeled.
- **#1407:** image-borne primary payload present but not semantically read in this text-centered pass.

## Cumulative ledger position

### Severity

| Severity | Count |
|---|---:|
| P0 | **121** |
| P1 | **175** |
| P2 | **344** |
| P3 | **35** |
| OK | **253** |

### Registration disposition

| Disposition | Count |
|---|---:|
| WITHHOLD | **128** |
| HARVEST_WITH_WARNING | **527** |
| HARVEST | **273** |

### Identity status

| Status | Count |
|---|---:|
| CONFIRMED_MATCH | **755** |
| WRONG_VERSION | **81** |
| WRONG_OBJECT | **39** |
| AMBIGUOUS_VERSION | **31** |
| PROBABLE_MATCH | **22** |

## Boundary result

The upper corpus boundary is now closed. The cumulative ledger is exactly contiguous from **#499 through #1426**, with no islands or gaps inside that range.

The remaining work is a single lower block:

> **#1–#498 — 498 records**

Repair remains deferred until the full 1,426-record audit has been assembled and validated.
