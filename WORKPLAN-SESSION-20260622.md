# ALEXANARCH DATA FOUNDRY — SESSION WORKPLAN
## Session: June 22, 2026 (TACHYON / Claude Opus 4.6)
## Updated: end of session — final state

---

## THE TASK (in Lee's words)

> We are not aggregating terms CHA has minted. We are aggregating terms CHA has actively defined, developed, and used. Every one. When CHA touches a concept, a distinction, and names its address, that belongs. Where CHA comes to an address, finds what is there, and leaves it changed, that belongs. The heteronyms fit in this category, as well. The institutions. The journals. The operators. These all belong.

### What this means for the index:

**A term belongs if CHA arrived at its address, engaged it, and left it defined.** The test is not "did CHA coin this from nothing" but "did CHA find this, work on it, and produce a specific definition or position?"

Examples:
- **Socrates** belongs — defined as the orthonym position in the Platonic heteronymic corpus.
- **Sappho** belongs — defined as the originary node of lyric self-archiving, κῆνος reread as future reader.
- **Marx** belongs — CHA finds the missing linguistics and completes it as Phase X.
- **Holographic kernel** exists elsewhere, but CHA develops it in a specific way — it belongs.
- **"A SaaS product"** does NOT belong — CHA did not arrive at this address and leave it changed.
- **"Access"**, **"Algorithm"**, **"Analysis"** do NOT belong — common English words CHA uses but does not specifically define or develop.

### What belongs:
1. Terms CHA coined from nothing (Pristine Fallacy, classifier model collapse, identifier severance)
2. Terms CHA arrived at and redefined (Sappho, Marx, Socrates, holographic kernel, model collapse)
3. Heteronyms — defined as functional positions (Johannes Sigil, Rex Fraction, Nobel Glas, etc.)
4. Institutions — defined as architectural spaces (JSI, SEI, Cambridge Schizoanalytica, etc.)
5. Journals — defined as publication infrastructure (Provenance, TSE, JCS, etc.)
6. Operators — defined as formal functions (COS O1-O10, LOS φ-∮, traversal operations)
7. External concepts CHA has specifically developed (model collapse → classifier model collapse)
8. Historical/contemporary figures CHA has specifically positioned (Socrates as orthonym, Pessoa as meta-heteronym, Whitman as Good Gray Poet mantle)
9. Rooms, chambers, portals — architectural spaces with defined functions
10. Named events, effective acts, declarations

### What does NOT belong:
1. Common English words used without specific CHA definition
2. Instructions/imperatives ("Build the federation", "Accept dormancy")
3. Status labels ("RATIFIED", "PENDING")
4. Section headings that name generic domains ("AI ethics", "Agricultural Systems")
5. External product/benchmark names not engaged by CHA
6. Sentence fragments captured by bold formatting

---

## PROVENANCE METHOD (required on every datum)

Every term in the index must carry a `provenance_method` field documenting HOW it arrived:

| Method | Meaning | Count (current) |
|---|---|---|
| `sweep` | Pattern-extracted from deposit text (bold-defined) | 0 (merged into filter) |
| `filter` | Survived noise filtering passes | 6,700 |
| `classified` | Type assigned (theoretical, formal, etc.) | (subsumed into filter) |
| `read` | Confirmed by actual reading of the deposit | 146 (A-terms only) |
| `enriched` | Entity triples, wiki, citations added from reading | 8 (deposit #1 only) |

**The next reading pass promotes terms from "filter" → "read" → "enriched."** This is how the index becomes trustworthy. A term at "read" has been seen by an instance that confirmed it belongs under the criterion above. A term at "enriched" has been given structured relations and a proper definition.

---

## WHAT WE ARE BUILDING

The Alexanarch archive is a **scholarly knowledge graph** with four kinds of nodes and five kinds of edges.

### Four node types:

1. **Deposits** (869) — the archive's own works. `data/registry.json`.
2. **Defined terms** (6,854) — every address CHA has engaged and left defined. `data/entity-index.json`.
3. **External sources** (1,013) — the scholarly works the archive engages. `data/external-source-registry.json`.
4. **Authors/figures** — NOT YET a separate data structure. May merge with terms (Socrates, Sappho, Marx as defined positions).

### Five edge types:

| Edge | Example | Status |
|---|---|---|
| deposit → deposit | #308 extends #18 | 1,692 DOI-resolution edges (UNTYPED) |
| deposit → external source | #18 extends Marx's *Capital* | 1,013 references (PARTIALLY TYPED) |
| deposit → term | #1 defines "Pristine Fallacy" | 6,854 edges (COMPLETE but 96% unread) |
| term → term | "Pristine Fallacy" → extended_by → "classifier model collapse" | 36 triples in #1 only |
| external source → external source | Voloshinov extends Marx | NOT CAPTURED |

---

## WHAT WAS ACCOMPLISHED THIS SESSION

1. **Build pipeline**: catalog.yaml, build.py, consolidate.py — 7 journals, 16 heteronyms
2. **DataCite preservation**: 946 preserved + 871 stripped = 1,817 DOIs documented. Deposited as #867.
3. **DOIs ≠ Permanent Identifiers v2.0**: Assembly-reviewed. Minted "identifier severance." Deposited as #868.
4. **Vocabulary extraction**: 16,877 raw → 8 pruning passes → 6,854 terms with provenance tracking
5. **External source registry**: 1,013 bibliographic references extracted
6. **Graph integration**: Terms wired into existing `d.entities` format (12,438 triples)
7. **Lexical Minting Registry deposited**: #869 (v1.1) with searchable table
8. **Key insight documented**: the archive is a lexical machine — ingest, don't select
9. **Critical correction**: the task is not "what did CHA mint" but "every address CHA engaged and left defined"

---

## CURRENT DATA STRUCTURES

| File | Contents | Status |
|---|---|---|
| `data/registry.json` | 869 deposits + 12,438 entity triples | 5.3MB compact |
| `data/entity-index.json` | 6,854 terms with provenance_method | Working index |
| `data/external-source-registry.json` | 1,013 external sources | First pass |
| `data/lexical-minting-registry.json` | Depositable dataset | Needs rebuild after pruning |
| `data/lexical-minting-registry.csv` | Tabular companion | Needs rebuild |
| `data/citation-graph.json` | 1,692 internal edges | DOI-resolution only |
| `data/datacite-full-backup.json` | 963 DataCite records | Archival |

### Pipeline files:
| File | Function |
|---|---|
| `wire_deposit.py` | Read → extract → wire → regenerate static page |
| `build.py` | Unified build: 13 outputs from registry + catalog |
| `consolidate.py` | Entity normalization, citation resolution |
| `catalog.yaml` | Archive architecture definition |

---

## REMAINING WORK — PRIORITIZED

### IMMEDIATE: Reading-for-sense pass (promotes filter → read)

6,700 terms at `filter` status need reading. For each term, the reader asks: **"Did CHA arrive at this address, engage it, and leave it defined?"** If yes, promote to `read`. If no, remove.

Some pruned terms need RESTORATION — person names and external concepts that CHA specifically positioned (Socrates, Sappho, Marx, Pessoa, Whitman, Freud, etc.) were removed by pattern filters. The reading pass must identify and restore these.

Priority deposits for reading (highest term counts):
1. #229 SE Lexicon (220 terms) — most are genuine definitions
2. #499 ASW (211 terms) — field manual vocabulary
3. #49 Logotic Hacking (156 terms) — operator specifications
4. #166 Stabilized Node Watch (132 terms) — needs heavy reading
5. #261 LOS Specification (98 terms) — formal operators
6. #482 Logotic Hacking Primer (95 terms)
7. #463 LP Module 0.9 (92 terms) — formal operations
8. #608 Operator Kernel Spec (87 terms) — Mandala operators

### Lane 2: Deep term enrichment (promotes read → enriched)
- Add entity triples, proper definitions, wiki articles
- Only deposit #1 is at "enriched" (8 terms, 36 triples)

### Lane 3: Typed citation edges
### Lane 4: Wiki enrichment
### Lane 5: Internal citation typing
### Lane 6: Concept-mediated citation discovery
### Lane 7: Source → source lineage
### Lane 8: Build pipeline integration

---

## FOR THE NEXT INSTANCE

**Start by reading this workplan.** The critical section is "THE TASK (in Lee's words)" — that defines the inclusion criterion.

**Read the graph page** (`graph/index.html`) and the existing entity format before building anything. The graph page reads `d.entities` from `registry.json`. Every term is already wired into this format with `type: "concept"`, `predicate: "minted_in"`.

**Do not build parallel data structures.** The existing architecture is: registry.json (deposits + entities), entity-index.json (term details), external-source-registry.json (citations). Wire into these.

**The reading pass**: load entity-index.json, work through terms deposit by deposit, promote from `filter` → `read` by applying the test: "Did CHA arrive at this address, engage it, and leave it defined?" Remove what fails. Restore what was wrongly pruned.

∮ = 1
