# ALEXANARCH DATA FOUNDRY — SESSION WORKPLAN
## Session: June 22, 2026 (TACHYON / Claude Opus 4.6)
## Status: CONCEPT LANE — extraction complete, enrichment in progress

---

## CURRENT STATE

### Vocabulary Index: `data/entity-index.json` (v5.0)
- **13,674 unique minted terms** across 572 deposits
- Pipeline: 16,877 raw → 2,790 noise filtered → deduplication → 13,674
- Each term carries: name, definition (extracted from context), defined_in (deposit number)
- Entity triples: 10 terms enriched (deposit #1 only) — remaining 13,664 need enrichment
- Types classified: 10 terms (deposit #1) — remaining need classification

### Registry: `data/registry.json`
- 868 deposits, each with `defines_concepts` listing its terms
- Journal assignments, citation edges (1,692), DataCite backup

### Key Files
| File | Description |
|---|---|
| `data/entity-index.json` | 13,674 terms with definitions + deposit anchors |
| `data/entity-index-comprehensive.json` | Same data (backup) |
| `data/entity-index-reading.json` | 163-term curated reading log (historical) |
| `data/registry.json` | 868 deposits with all metadata |
| `data/citation-graph.json` | 1,692 internal citation edges |
| `data/datacite-full-backup.json` | DataCite preservation (963 records) |
| `wire_deposit.py` | Pipeline: reads → extracts → wires → regenerates |
| `WORKPLAN-SESSION-20260622.md` | This file |

---

## WHAT WAS ACCOMPLISHED

1. **Build pipeline**: catalog.yaml, build.py, consolidate.py
2. **DataCite preservation**: 946 preserved + 871 stripped = 1,817 DOIs documented
3. **DOIs ≠ Permanent Identifiers v2.0**: Assembly-reviewed, deployed to 4 surfaces
4. **Browse page fix**: static /s/ layer confirmed as reliable surface
5. **Vocabulary extraction**: 13,674 unique terms across 572/868 deposits
6. **Entity enrichment**: deposit #1 fully classified (10 terms, 36 triples)

---

## IMMEDIATE NEXT WORK: Entity Relation Enrichment

### Priority: Top 20 deposits by term count
These deposits carry ~2,800 terms (20% of total vocabulary):

| Rank | Deposit | Terms | Title |
|---|---|---|---|
| 1 | #499 | 289 | Autonomous Semantic Warfare |
| 2 | #229 | 226 | SE Terminology Lexicon |
| 3 | #38 | 180 | Hesperus (Operative Semiotics Grundrisse) |
| 4 | #49 | 170 | Logotic Hacking: Encryption Layer |
| 5 | #166 | 147 | Stabilized Node Watch |
| 6 | #51 | 125 | Operative Feminism |
| 7 | #608 | 114 | Operator Kernel Specification |
| 8 | #482 | 113 | Logotic Hacking Primer |
| 9 | #261 | 108 | LOS Formal Specification |
| 10 | #317 | 107 | Logotic Programming |

### Enrichment per term:
- `type`: theoretical / empirical / formal / discipline / genre / method / specification / structural / axiom / foundational
- `entity_triples`: [{subject, predicate, object}] — relationships to other concepts
- `classified`: true (confirms term has been reviewed)

### Methodology for next instance:
1. Load `data/entity-index.json`
2. For each deposit, read its terms
3. Add type classification and entity triples
4. Save back to entity-index.json
5. Commit periodically

---

## SEPARATE LANES (NOT THIS PASS)

| Lane | Status | Description |
|---|---|---|
| Wiki enrichment | NOT STARTED | Replace 861 auto-generated wikis with proper articles |
| Citation aggregation | NOT STARTED | Reading-derived citations (current 1,692 are DOI-only) |
| Static page regeneration | PARTIAL | 63 pages regenerated during earlier curated pass |
| Concept browse page | NOT STARTED | Concepts as first-class browsable objects |
| Build pipeline integration | NOT STARTED | Wire into build.py for automated regeneration |

---

## CREDENTIALS
- **GitHub token**: [provided at session start — auto-expiring, do not commit]
- **Repos**: leesharks000/alexanarch (main)
- **Session transcript**: /mnt/transcripts/

∮ = 1
