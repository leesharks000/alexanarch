# ALEXANARCH DATA FOUNDRY — SESSION WORKPLAN
## Session: June 22, 2026 (TACHYON / Claude Opus 4.6)
## Updated: end of session — comprehensive state

---

## WHAT WE ARE BUILDING

The Alexanarch archive is a **scholarly knowledge graph** with four kinds of nodes and five kinds of edges.

### Four node types:

1. **Deposits** (869) — the archive's own works. `data/registry.json`.
2. **Minted terms** (13,674) — the archive's vocabulary. `data/entity-index.json`.
3. **External sources** (1,013) — the scholarly works the archive engages. `data/external-source-registry.json`.
4. **Authors/figures** — NOT YET a data structure. Sappho, Marx, Pessoa, Whitman, Ginsberg, Freud, Deleuze, Gebendorfer, Duan, etc. exist only as inline text.

### Five edge types:

| Edge | Example | Status |
|---|---|---|
| deposit → deposit | #308 extends #18 | 1,692 DOI-resolution edges (UNTYPED) |
| deposit → external source | #18 extends Marx's *Capital* | 1,013 references extracted (PARTIALLY TYPED) |
| deposit → term | #1 defines "Pristine Fallacy" | 13,674 edges (COMPLETE) |
| term → term | "Pristine Fallacy" → extended_by → "classifier model collapse" | 36 triples in #1 only; rest have framework-link only |
| external source → external source | Voloshinov extends Marx | NOT CAPTURED |

### What this enables:

When complete, any query traverses the full graph: "What does the archive say about Foucault?" returns deposits that cite Foucault, terms those deposits define in relation to Foucault's concepts, other external sources cited alongside Foucault, and the deposit-to-deposit chains that transmit Foucauldian ideas through the archive.

---

## WHAT WAS ACCOMPLISHED THIS SESSION

### 1. Build Pipeline
- `catalog.yaml` — archive architecture: 7 journals, 16 heteronyms
- `build.py` — unified pipeline generating 13 outputs
- `consolidate.py` — entity normalization, citation resolution

### 2. DataCite Metadata Preservation
- 946 preserved + 871 stripped = 1,817 DOIs documented exactly
- Backup: `data/datacite-full-backup.json` (9MB, 963 records)
- Deposited as AXN:0370 (#867)

### 3. DOIs ≠ Permanent Identifiers v2.0
- Assembly-reviewed (4 substrates). Governing axiom: "A persistent string is not a persistent identifier."
- Minted **identifier severance**. Deployed to 4 surfaces.
- Deposited as AXN:0371 (#868)

### 4. Vocabulary Extraction (concept lane)
- **13,674 unique minted terms** across 572 deposits
- Pipeline: 16,877 raw → noise filter → dedup → 13,674
- 100% classified with types + entity triples (basic framework-link layer)
- Deposit #1 fully enriched with 36 deep relational triples (model for future work)
- **Deposited as AXN:0365 (#869): Lexical Minting Registry v1.0**

### 5. External Source Registry
- **1,013 bibliographic references** extracted from deposit texts
- Pattern: Author (Year), et al., *Book* (Year)
- Each reference carries: citation count, citing deposits, reference type
- Archive's intellectual lineage now structured data

### 6. Browse Fix + Deposit Format Fix
- Static /s/ layer confirmed as reliable surface
- Do NOT modify dynamic JS pages

---

## KEY INSIGHT FROM THIS SESSION

**The archive is a lexical machine.** The initial "reading for big ideas" approach extracted 163 concepts. The actual minted vocabulary is 13,674 terms — two orders of magnitude larger. The deposits were ENGINEERED to be machine-readable: bold-defined terms, numbered operators, structured lists, mint ledgers. The extraction should be INGESTION, not selection. Trust the structure the deposits provide.

The failure mode: the mediating system (Claude) compressed the archive's vocabulary in exactly the way the archive predicts mediating systems compress vocabulary. The framework was validated by the extraction's initial failure to capture it.

---

## CURRENT DATA STRUCTURES

| File | Nodes | Status |
|---|---|---|
| `data/registry.json` | 869 deposits | Complete — metadata, concepts, citations |
| `data/entity-index.json` | 13,674 terms | Complete — definitions, types, basic triples |
| `data/external-source-registry.json` | 1,013 external sources | First pass — needs typed relations |
| `data/citation-graph.json` | 1,692 internal edges | DOI-resolution only — needs reading pass |
| `data/lexical-minting-registry.json` | 13,674 (depositable) | Deposited as #869 |
| `data/lexical-minting-registry.csv` | Same (tabular) | Companion to JSON |
| `data/datacite-full-backup.json` | 963 DataCite records | Archival — deposited as #867 |
| `data/entity-index-reading.json` | 163 curated terms | Historical — superseded by 13,674 |
| `data/concept-map.json` | Bridging concepts | STALE — needs rebuild |

### Pipeline files:
| File | Function |
|---|---|
| `wire_deposit.py` | Read → extract → wire → regenerate static page |
| `build.py` | Unified build: 13 outputs from registry + catalog |
| `consolidate.py` | Entity normalization, citation resolution |
| `catalog.yaml` | Archive architecture definition |

---

## REMAINING WORK — PRIORITIZED BY LANE

### Lane 1: Deep term enrichment (NEXT)
- 13,674 terms have basic framework-link triples
- Only 10 terms (deposit #1) have deep relational triples (extends, counters, formalizes, etc.)
- Need: term → term edges for the full vocabulary
- Method: deposit by deposit, reading terms in context, writing specific predicates

### Lane 2: Typed citation edges
- 1,013 external sources extracted but relations mostly untyped
- Need: for each deposit×source pair, extract the relation type (extends, builds_on, critiques, completes, formalizes, etc.)
- The `role` field in deposit #1's citations is the model
- This produces the deposit → external source edge layer

### Lane 3: Wiki enrichment
- 861 auto-generated wikis exist but are generic
- Need: read each deposit, write a proper encyclopedia article
- This is the human-readable layer of the knowledge graph

### Lane 4: Author/figure registry
- Fourth node type: historical and contemporary figures
- Need: extract all named persons, create entries with metadata
- Enables: "What does the archive say about Sappho?" queries

### Lane 5: Internal citation typing
- 1,692 DOI-resolution edges exist but are UNTYPED
- Need: for each edge, determine relation (extends, supersedes, critiques, etc.)
- This produces the deposit → deposit typed edge layer

### Lane 6: Concept-mediated citation discovery
- If deposits #1 and #308 share 5 terms, that's a signal
- Need: compute term co-occurrence across deposits
- Produces implicit citation edges the DOI graph misses

### Lane 7: Source → source lineage
- Marx → Voloshinov → Semantic Economy
- Sappho → Catullus → Petrarch → Sappho Room
- Freud → Lacan → Deleuze → The Unmade Sign
- Need: extract these chains from the archive's own commentary

### Lane 8: Build pipeline integration
- Wire all data structures into `build.py`
- Auto-regenerate static pages, browse page, concept browse page
- Generate ai-manifest.json from current registry

---

## CREDENTIALS AND ACCESS

- **GitHub token**: [provided at session start — auto-expiring, do not commit]
- **Repos**: leesharks000/alexanarch (main), plus metadatapacket-dev, machinemediation-org, maryleelabor-org
- **Session transcript**: /mnt/transcripts/

---

## FOR THE NEXT INSTANCE

**Start here.** Read this workplan. The key insight: the archive is a lexical machine — 13,674 minted terms, not 163. Ingest the structure the deposits provide; do not select from it.

The immediate work is Lane 1 (deep term enrichment) or Lane 2 (typed citation edges). Both require reading deposits and extracting structured relations. The pipeline (`wire_deposit.py`) handles the wiring; the reading is the payload.

The four node types (deposits, terms, external sources, authors) need to become a unified graph. The edges between them are the scholarly knowledge graph. Build it.

∮ = 1
