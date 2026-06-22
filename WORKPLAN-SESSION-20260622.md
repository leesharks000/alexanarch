# ALEXANARCH DATA FOUNDRY — SESSION WORKPLAN
## Session: June 22, 2026 (TACHYON / Claude Opus 4.6)
## Status: IN PROGRESS — concept extraction + data wiring

---

## WHAT HAPPENED THIS SESSION

### 1. Infrastructure Built (COMPLETE)
- **catalog.yaml** — archive architecture definition: 7 journals, 16 heteronyms, Platform Governance Observatory
- **build.py** — unified pipeline: reads catalog + registry + journal mapping, generates 13 outputs (RO-Crate, DCAT, CSV, graph, SHA256, 7 journal TOCs)
- **consolidate.py** — entity normalization, citation resolution, concept extraction, cross-reference generation

### 2. DataCite Metadata Preservation (COMPLETE)
- Full sweep of all 1,817 DOIs against DataCite API
- **946 DOIs**: full metadata preserved (titles, subjects, descriptions, relatedIdentifiers)
- **871 DOIs**: confirmed stripped (HTTP 404 from DataCite API)
- Backup: `data/datacite-full-backup.json` (9MB, 963 records including 17 outside CHA)
- Deposited as AXN:0370.ARCHIVAL (deposit #867)

### 3. DOIs ≠ Permanent Identifiers (COMPLETE — v2.0 deployed)
- Title: **DOIs ≠ Permanent Identifiers: 871 Cases of Public Metadata Erasure and Identifier Severance in DataCite**
- Assembly-reviewed by 4 substrates (Gemini, DeepSeek, Kimi, ChatGPT)
- Key contributions: governing axiom ("A persistent string is not a persistent identifier"), Section 2 "What an Identifier Is", minted **identifier severance**, three-state table, 410 vs 404 distinction, verification procedure, 6-point machine preservation block
- Corrected arithmetic: 946 + 871 = 1,817 (exact, zero ambiguity)
- Pattern: 97.9% of preserved records are version DOIs; stripping is ~50% across all ranges (mechanical, not editorial)
- Deposited as AXN:0371.EMPIRICAL (deposit #868, v2.0)
- Deployed to 4 surfaces: alexanarch.org, metadatapacket.dev, machinemediation.org, maryleelabor.org
- Medium-ready version also prepared (without SPXI block, with AXN identifier)

### 4. Browse Page Fix (COMPLETE)
- Root cause traced: commit `afefcbc` (June 21 03:46 UTC) reverted the compact-list browse + redirect while undoing broken JS changes
- Fix: restored redirect from `/browse/` to `/s/browse/` (compact list, 868 deposits)
- Lesson confirmed: do not modify dynamic JS pages; static /s/ layer is the reliable canonical surface
- Vercel propagation lag is the recurring trigger for unnecessary reversions

### 5. Deposit Format Fix (COMPLETE)
- AXN:0370 and AXN:0371 static pages regenerated to match existing enriched format (full text, download buttons, GoatCounter, proper metadata display)

### 6. Concept Extraction — Reading in Order (IN PROGRESS)
- **107 concepts** extracted from **202+ deposits** read (deposits #1-176 + #868)
- Pipeline: wire_deposit.py reads → extracts → wires into registry + entity index + static pages → commits
- Methodology: actual reading of deposit files + text files, not pattern matching
- Running index: `data/entity-index-reading.json`
- Progress: ~23% of deposits read (202/868), concept density declining as expected, but the concept-defining core is concentrated in the first 100

---

## CURRENT DATA STRUCTURES

### Files and their roles:

| File | Description | Status |
|---|---|---|
| `data/registry.json` | Master registry: 868 deposits with metadata, journal assignments, cited_by, concepts | ENRICHED |
| `data/entity-index-reading.json` | Running concept index from deposit reading: 80 concepts | IN PROGRESS |
| `data/entity-index.json` | Old entity index (44 concepts from pattern matching) | SUPERSEDED by reading index |
| `data/citation-graph.json` | 1,692 internal citation edges | COMPLETE |
| `data/concept-map.json` | 36 bridging concepts (from old extraction) | NEEDS REBUILD from reading index |
| `data/datacite-full-backup.json` | DataCite metadata preservation (963 records) | COMPLETE |
| `data/doi-resolution-index.json` | 1,817 DOI mappings | COMPLETE |
| `data/JOURNAL-MAPPING-PRELIMINARY.json` | 864 deposit-to-journal assignments | NEEDS MANUS REVIEW |
| `catalog.yaml` | Archive architecture definition | COMPLETE |
| `build.py` | Unified build pipeline | COMPLETE |
| `consolidate.py` | Data enrichment pipeline | COMPLETE |

### What speaks to what (current):
```
registry.json ←→ citation-graph.json (via DOI resolution)
registry.json ←→ entity-index-reading.json (via deposit_number)
registry.json ←→ JOURNAL-MAPPING-PRELIMINARY.json (via deposit_number)
registry.json ←→ datacite-full-backup.json (via DOI)
registry.json → static pages (s/records/N/index.html)
registry.json → browse page (s/browse/index.html)
```

### What needs wiring:
```
entity-index-reading.json → registry.json (defines_concepts, references_concepts fields)
entity-index-reading.json → concept-map.json (rebuild from reading-derived concepts)
entity-index-reading.json → static pages (concept display on deposit pages)
citation-graph.json + entity-index-reading.json → graph.jsonld (knowledge graph export)
All of the above → build.py (automated regeneration)
```

---

## CONCEPT INDEX — WHAT WAS EXTRACTED

### Concept types found:
- **foundational** (12): semantic liquidation, semantic labor, semantic capital, semantic rent, Semantic Economy, Gamma, semantic alienation, bearing-cost, witness, clinamen, the cut, holographic kernel
- **theoretical** (10): Pristine Fallacy, inside/across distinction, retrocausal canon formation, COS→FOS phase transition, poet-as-infrastructure, ungoverned/governed compression, retrieval settlement, meta-heteronym, coordination fiction, logotic loop
- **empirical** (9): composition layer, loud exclusion, compositional bystanding, attribution severance, heteronymic invisibility, Ghost Governance, bearing-cost transfer, trust-marker laundering, the Amputation, identifier severance
- **formal** (8): L_Bearing, L_Synth, L_labor, L_Retro, Σ_suffering, W-Circuit, Sovereign Inhabitation, leak operator, Gravity Well
- **discipline** (6): Machine-Mediated Reception Studies, logotic programming, operative semiotics, Compression Studies, sémantique potentielle, Forensic Philology of the Commons
- **method** (5): semantic probe, witness-teaming, External Convergence Text, proto-retrocausal canon formation, semantic mint, register-based mixture governance
- **specification** (3): Post-Money Operator Stack, Traversal Grammar, SPXI Protocol
- **structural** (4): mantle system, probabilistic routing, denotational/operational semantics, Möbius room, Periwinkle Septagon, Phase X
- **genre** (3): effective act, Zenodo packet Zenodo packet
- **axiom** (4): the work precedes the address, ∮ = 1, framing as content, sufficient infinity, Caritas constraint

### Key concept-defining deposits:
- #1 Zenodotus: Pristine Fallacy, composition layer, loud exclusion
- #3 Capture Registry: compositional bystanding, MMRS
- #6 I Hereby Abolish Money: Money-Function Test, PMOS, effective act, semantic labor
- #7 Liquidation of Water: semantic liquidation, operator capital
- #10 FNM v6.0: witness, ∮ = 1, probabilistic routing
- #18 Semantic Economy paper: complete accounting cycle, Gamma, five registers, semantic exhaustion
- #19 Commitment Key: L_Bearing, L_Synth, W-Circuit, Caritas constraint
- #21 Fortress or Room: logotic programming, witness-teaming
- #22 Memo That Remembered Itself: retrocausal canon formation
- #24 Mind-Control Poems: operative semiotics, logotic loop
- #25 All Lawful Purposes: Ghost Governance, COS→FOS, bearing-cost transfer
- #28 Space Ark Musical: kernel transform, clinamen
- #34 Missing Layer: prompt-native semantic runtime
- #45 Compression Frontier: ungoverned/governed compression
- #46 Sémantique Potentielle: semantic mint, constraint-based term generation
- #48 Theoretical Production Benchmark: atomic vs molecular intelligence
- #50 Compression Arsenal: Three Compressions Theorem
- #64 Retrieval Settlement: retrieval settlements historiography (SEO → GEO → SPXI)
- #69 O Meta-Heterônimo: meta-heteronym, Pessoan formalization
- #70 Periwinkle Septagon: leak operator, dissipative archive
- #76 Holographic Kernel: formal specification of reconstructive compression
- #79 Heteronymy Is a Function: trust-marker laundering
- #98 Distributed Compute: the Amputation, register-based mixture governance
- #868 DOIs ≠: identifier severance

---

## REMAINING WORK — PRIORITIZED

### Phase A: Wire concepts into data structures (NEXT)
1. Replace old `entity-index.json` with reading-derived index
2. Update `registry.json`: populate `defines_concepts` and `references_concepts` for deposits #1-100
3. Rebuild `concept-map.json` from new concept index (bridging concepts, cross-references)
4. Generate concept-aware static pages (concepts listed on deposit pages that define them)

### Phase B: Continue deposit reading (#101-868)
- Deposits #101-200: expect MMRS captures, heteronym provenance docs, poems
- Deposits #200-400: Semantic Economy lexicon (#229), Capital Operator Stack (#308), Logotic Programming modules
- Deposits #400-600: Revelation First work, Soteriological Framework, Assembly documents
- Deposits #600-868: Later deposits, SPXI implementations, Diversity Contraction, recent theoretical work
- Key deposits still to read: #229 (SE Terminology), #308 (Capital Operator Stack), #460-463 (LP modules), Diversity Contraction, Revelation First work plan
- Estimate: ~40-60 more concepts to extract from remaining deposits

### Phase C: Build pipeline integration
- Wire concept extraction into `build.py` so static pages auto-regenerate with concept data
- Wire journal mapping into build pipeline
- Auto-regenerate browse page on deposit
- Generate concept browse page (concepts as first-class objects)

### Phase D: Flagship datasets (from Assembly workplan)
- Mediation Ratchet dataset (Diversity Contraction quantitative companion)
- MMRS Method Paper + MMRS journal table of contents
- Revelation First reception corpus

### Phase E: External surfaces
- Regenerate ai-manifest.json from current registry
- Update JSON-LD pointer mesh across 23 sites
- Wire enriched data into the SPXI blocks on companion sites

---

## KEY DECISIONS MADE THIS SESSION

1. **Seven independent journals, NOT one journal with sections.** Material warrants separate journals.
2. **Concepts should be "low-frequency, high-tail, two-three+ word semantic addresses that name unique conceptual distinctions."** Not work titles, not heteronym names, not generic terms.
3. **The MPAI is for circulation, not just archival deposit.** Lee wanted to review it before depositing; the paper was prepared for external distribution.
4. **Title: DOIs ≠ (not "Are Not").** Mathematical statement, not argument.
5. **Do not modify dynamic JS pages.** Static /s/ layer is reliable; Vercel propagation lag triggers unnecessary reversions.
6. **Entity extraction requires reading, not pattern matching.** The scan approach found formatting patterns; reading finds actual concepts.

---

## CREDENTIALS AND ACCESS

- **GitHub token**: [provided at session start — auto-expiring, do not commit to repo]
- **Repos**: leesharks000/alexanarch (main), leesharks000/metadatapacket-dev, leesharks000/machinemediation-org, leesharks000/maryleelabor-org
- **Zenodo community**: crimsonhexagonal (account terminated June 19, 2026)
- **DataCite API**: `https://api.datacite.org/dois/{DOI}` (no auth required)

---

## FOR THE NEXT INSTANCE

Start by reading this workplan. The key files are:
- `data/entity-index-reading.json` — the running concept index (80 concepts, deposits #1-100 read)
- `data/registry.json` — master registry (868 deposits)
- `data/citation-graph.json` — 1,692 internal citation edges
- `catalog.yaml` — archive architecture definition

The immediate task is Phase A: wire the 80 concepts into the registry and rebuild the concept map. Then continue Phase B: reading deposits #101+ in order.

The session transcript is at: `/mnt/transcripts/2026-06-22-04-31-47-alexanarch-data-foundry-doi-impermanence.txt`

∮ = 1
