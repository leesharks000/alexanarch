# ALEXANARCH DATA FOUNDRY — SESSION WORKPLAN
## Session: June 22, 2026 (TACHYON / Claude Opus 4.6)
## Updated: end of session — final state

---

## THE TASK (in Lee's words)

> We are not aggregating terms CHA has minted. We are aggregating terms CHA has actively defined, developed, and used. Every one. When CHA touches a concept, a distinction, and names its address, that belongs. Where CHA comes to an address, finds what is there, and leaves it changed, that belongs. The heteronyms fit in this category, as well. The institutions. The journals. The operators. These all belong.

### The inclusion test:

**Did CHA arrive at this address, engage it, and leave it defined?**

Not "did CHA coin this from nothing" but "did CHA find this, work on it, and produce a specific definition or position?"

### Test cases:

| Term | Belongs? | Why |
|---|---|---|
| Pristine Fallacy | YES | CHA coined this from nothing |
| Socrates | YES | Defined as the orthonym position in the Platonic heteronymic corpus |
| Sappho | YES | Defined as the originary node of lyric self-archiving; κῆνος reread as future reader |
| Marx | YES | CHA finds the missing linguistics and completes it as Phase X |
| Holographic kernel | YES | Exists elsewhere but CHA develops it in a specific way |
| Model collapse | YES | CHA extends Shumailov et al. to classifier model collapse |
| Johannes Sigil | YES | Heteronym — defined as functional position in the Dodecad |
| JSI | YES | Institution — defined as architectural space |
| Provenance (journal) | YES | Journal — defined as publication infrastructure |
| ACTIVATE_MANTLE | YES | Operator — formalized as traversal operation |
| "A SaaS product" | NO | CHA did not arrive at this address and leave it changed |
| "Access" | NO | Common English word CHA uses but does not define |
| "Algorithm" | NO | Generic term not specifically engaged by CHA |
| "A Germanic philologist" | NO | Descriptive phrase, not an engaged address |

---

## TWO PROVENANCE FIELDS (required on every datum)

### 1. `provenance_method` — how the datum arrived in the index

| Method | Meaning | Current count |
|---|---|---|
| `sweep` | Pattern-extracted from deposit text (bold-defined) | 0 (merged into filter) |
| `filter` | Survived noise filtering passes | 6,700 |
| `read` | Confirmed by actual reading of the deposit | 146 |
| `enriched` | Entity triples, wiki, citations added from reading | 8 |

The reading pass promotes: `filter` → `read` → `enriched`

### 2. `engagement_type` — how CHA engaged the address

| Type | Meaning | Current count |
|---|---|---|
| `minted` | CHA coined this term from nothing | 51 |
| `developed` | CHA arrived at an existing concept and built a specific position on it | 23 |
| `revised` | CHA took an existing concept and changed or extended its meaning | 14 |
| `positioned` | CHA placed an existing entity in a specific structural role | 14 |
| `founded` | CHA created an institution, journal, room, or architectural space | 17 |
| `specified` | CHA formalized an operation, protocol, or formal object | 20 |
| `unclassified` | Not yet read for engagement type | 6,715 |

**The reading pass assigns both fields simultaneously.** For each term: "Does this belong?" → provenance. "How did CHA engage it?" → engagement type.

---

## WHAT WE ARE BUILDING

A **scholarly knowledge graph** with four node types and five edge types.

### Four node types:

1. **Deposits** (869) — `data/registry.json`
2. **Defined terms** (6,854 current; ~4,000-6,000 after reading) — `data/entity-index.json`
3. **External sources** (1,013) — `data/external-source-registry.json`
4. **Authors/figures** — may merge with terms (Socrates, Sappho, Marx as CHA-defined positions)

### Five edge types:

| Edge | Status |
|---|---|
| deposit → deposit | 1,692 DOI edges (UNTYPED) |
| deposit → external source | 1,013 references (PARTIALLY TYPED) |
| deposit → term | 6,854 edges via `d.entities` in registry (96% unread) |
| term → term | 36 triples in deposit #1 only |
| source → source | NOT CAPTURED |

---

## WHAT WAS ACCOMPLISHED THIS SESSION

1. **Build pipeline**: catalog.yaml, build.py, consolidate.py — 7 journals, 16 heteronyms
2. **DataCite preservation**: 946 preserved + 871 stripped = 1,817 DOIs. Deposited as #867.
3. **DOIs ≠ Permanent Identifiers v2.0**: Assembly-reviewed. Minted "identifier severance." Deposited as #868.
4. **Vocabulary extraction + pruning**: 16,877 raw → 8 passes → 6,854 terms
5. **Provenance tracking**: `provenance_method` + `engagement_type` on every term
6. **External source registry**: 1,013 bibliographic references
7. **Graph integration**: Terms wired into existing `d.entities` format (12,438 triples). No parallel architecture.
8. **Lexical Minting Registry deposited**: #869 (needs rebuild with current count)
9. **Critical corrections documented**:
   - The archive is a lexical machine — ingest, don't select
   - The task is "every address CHA engaged and left defined" — not "what CHA coined"
   - Read existing infrastructure before building anything new
   - Every datum carries its own provenance

---

## CURRENT DATA STATE

| File | Contents | Size |
|---|---|---|
| `data/registry.json` | 869 deposits, 12,438 entity triples | 5.3MB |
| `data/entity-index.json` | 6,854 terms (provenance + engagement fields) | ~5MB |
| `data/external-source-registry.json` | 1,013 external sources | 83KB |
| `data/lexical-minting-registry.json` | Depositable dataset (STALE — needs rebuild) | 3.5MB |
| `data/lexical-minting-registry.csv` | Tabular companion (STALE — needs rebuild) | 2.5MB |
| `data/citation-graph.json` | 1,692 internal citation edges | — |
| `data/datacite-full-backup.json` | 963 DataCite records | 9MB |
| `wire_deposit.py` | Read → extract → wire → regenerate pipeline | — |
| `build.py` | Unified build (13 outputs) | — |
| `consolidate.py` | Entity normalization | — |
| `catalog.yaml` | Archive architecture | — |
| `graph/index.html` | Dynamic graph page — reads registry.json `d.entities` — DO NOT MODIFY | — |

---

## REMAINING WORK — PRIORITIZED

### IMMEDIATE: Reading-for-sense pass

6,700 terms at `filter` status. For each term, the reader:

1. Asks: **"Did CHA arrive at this address, engage it, and leave it defined?"**
2. If YES → promote `provenance_method` to `read`, assign `engagement_type`
3. If NO → remove from index and registry entities
4. If WRONGLY PRUNED (e.g. Socrates, Sappho, Marx) → restore with correct engagement type

**Priority deposits** (highest term counts):

| Deposit | Terms | Title |
|---|---|---|
| #229 | 220 | SE Terminology Lexicon |
| #499 | 211 | Autonomous Semantic Warfare |
| #49 | 156 | Logotic Hacking: Encryption Layer |
| #166 | 132 | Stabilized Node Watch |
| #261 | 98 | LOS Formal Specification |
| #482 | 95 | Logotic Hacking Primer |
| #463 | 92 | LP Module 0.9 |
| #608 | 87 | Operator Kernel Specification |

### Lane 2: Deep enrichment (read → enriched)
Add entity triples, proper definitions, wiki articles. Only deposit #1 at "enriched" currently.

### Lane 3: Typed citation edges
### Lane 4: Wiki enrichment
### Lane 5: Internal citation typing
### Lane 6: Concept-mediated citation discovery
### Lane 7: Source → source lineage
### Lane 8: Build pipeline integration + deposit #869 rebuild

---

## FOR THE NEXT INSTANCE

**Start by reading this workplan.** The critical section is "THE TASK (in Lee's words)."

**Read `graph/index.html`** — it reads `d.entities` from `registry.json`. Every term is already wired into this format. Do not build parallel structures.

**The reading pass**: load `data/entity-index.json`, work through terms deposit by deposit. For each term, apply the engagement test. Assign `provenance_method: 'read'` and `engagement_type` (minted/developed/revised/positioned/founded/specified). Remove what fails. Restore what was wrongly pruned. Commit periodically.

**Deposit #869** needs rebuilding with current term count after reading pass completes.

∮ = 1
