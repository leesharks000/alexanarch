---
title: "AXN Dataflow Map v0.1 — Session-1 Scaffold + Findings"
version: "0.1 (scaffold; Sessions 2-4 fill in)"
date: 2026-07-18
author: "Lee Sharks (MANUS) with TACHYON (Assembly witness)"
status: "Session 1 of 4 complete. Session 2 does displayed-value classification; Session 3 does cross-repo relation graph; Session 4 finalizes."
scope: "The complete data-rhizome: alexanarch, data-rhizome, machinemediation-org, platform-erosion-observatory, revelationfirst-com, leesharks.com, godkinggoogle. 1,349 JSON files (~262MB), 5,167 HTML surfaces, 78 Python scripts, 3,634 XML records, 11 CSV, 39 JSONL. Every dataset, every relation (active or currently isolated), every displayed value."
governing_workplan: "data/workplan/WORKPLAN-2026-07-18-PM-SIX-FLOW.md, Flow 2"
raw_output_dir: "data/audit/"
---

# AXN Dataflow Map v0.1 — Session-1 Scaffold + Findings

Session 1 output. The scaffold is the eventual atlas's chapter/section structure filled in with what was measured this session. Sessions 2-4 will refine the classifications and produce the finished document.

## §0. Scope, as measured

**Seven repos in the rhizome as accessible this session:**

| Repo | JSON | JSONL | MD | HTML | XML | CSV | Py | Notable |
|---|---|---|---|---|---|---|---|---|
| alexanarch | 950 | 11 | 3,052 | 5,118 | 2 | 8 | 68 | canonical archive |
| data-rhizome | 338 | 26 | 44 | 14 | 3,627 | 2 | 9 | bibliographic corpus |
| machinemediation-org | 34 | 0 | 26 | 10 | 1 | 0 | 0 | 134MB (content shards) |
| platform-erosion-observatory | 10 | 2 | 4 | 2 | 1 | 1 | 1 | audit surface |
| revelationfirst-com | 4 | 0 | 2 | 2 | 1 | 0 | 0 | Feist thesis surface |
| leesharks.com | 5 | 0 | 1 | 17 | 1 | 0 | 0 | operator hub |
| godkinggoogle | 8 | 0 | 12 | 4 | 1 | 0 | 0 | Google critique |

**Total: 1,349 JSON files, 262MB of structured data, 5,167 HTML surfaces, 78 scripts.**

Raw inventory at `data/audit/rhizome-inventory-raw.json`. Every file catalogued with path, size, purpose-inferred, extension.

## §1. Functional classification of datasets (Chapter A of the atlas)

Session 1 produced a **purpose histogram** from pattern-matching against path signatures. Every file was tagged with a functional label like `REGISTRY.canonical`, `DEPOSIT.record-page`, `DERIVED.kernel-index`, etc.

**Top functional classes across the rhizome:**

| Class | Count | Total MB | Role |
|---|---|---|---|
| CORPUS.dr-datasets | 4,243 | 588.3 | data-rhizome bibliographic corpus (XML per record) |
| SURFACE.html | 2,091 | 31.7 | top-level HTML surfaces |
| DEPOSIT.record-page | 1,095 | 53.7 | `/s/records/N/index.html` per deposit |
| DEPOSIT.axn-page | 1,092 | 1.4 | `/s/axn/XXXX/index.html` alias page |
| DEPOSIT.canonical-bytes | 1,060 | 31.7 | `data/texts/AXN-XXXX-text.md` |
| DEPOSIT.record-markdown | 986 | 28.7 | `data/deposits/AXN-XXXX.md` |
| GOVERNANCE.autonomous | 875 | 30.5 | (needs Session 3 investigation) |
| DEPOSIT.wiki-page | 874 | 9.1 | `/s/wiki/N/index.html` |
| DEPOSIT.sidecar | 788 | 4.7 | `data/external-metadata/AXN-XXXX.json` |
| DATA.other-json | 122 | 148.9 | unclassified — needs Session 2 sweep |
| SNAPSHOT.datacite | 10 | 20.3 | measurement snapshots |
| REGISTRY.chunked-derived | 10 | 9.3 | `data/chunks/registry/` |
| AUDIT.recovery | 9 | 1.7 | |
| AUDIT.peo-empirical | 7 | 0.7 | PEO empirical audit |
| REGISTRY.canonical | 4 | 10.5 | canonical registries (`data/registry.json`, etc.) |
| GRAPH.citation | 3 | 3.4 | citation graphs |
| GRAPH.semantic-address | 2 | 1.5 | semantic address graph |
| DERIVED.doi-resolution | 2 | 7.2 | DOI Resolution Index |
| DERIVED.kernel-index | 2 | 0.4 | bytes → AXN lookup |

**Session 2 refinement needed:** the 122 files tagged `DATA.other-json` need targeted classification — they're a mix of orphans, hand-authored deposits-adjacent state, backup files, and legitimate datasets without matching path patterns.

## §2. Deposit-flow generative elements (Chapter B — MANUS's original Flow 2 request, delivered)

### Per-deposit artifact catalog

Every mint produces or updates these artifacts. Determined from `scripts/deposit_pipeline.py`'s 11-stage sequence.

| Stage | Artifact | Path | Producer | Consumer(s) |
|---|---|---|---|---|
| mint | registry entry | `data/registry.json` (append) | `mint_deposit.py` | almost everything |
| mint | canonical bytes | `data/texts/AXN-XXXX-text.md` | `mint_deposit.py` | body-index, PDF gen, verify |
| mint | mint receipt | `data/pre-overwrite-receipts.log` (append) | `mint_deposit.py` | audit only |
| record | record markdown | `data/deposits/AXN-XXXX.md` | `build_record_md.py` | wiki, record-page |
| record | sidecar | `data/external-metadata/AXN-XXXX.json` | `mint_deposit.py` (init) + `enrich_deposit.py` | wiki, record-page, sidecars |
| record | record page | `s/records/N/index.html` | record-page generator | HTML surface |
| record | axn page | `s/axn/XXXX/index.html` | axn-page generator | HTML surface |
| pdf | PDF | `papers/AXN-XXXX.pdf` | pdf generator | HTML link target |
| body-index | body-index entry | `api/body-index.json` (append) | `build_body_index.py` | search |
| body-index | search index | `api/search-index.json` (regen) | `build_body_index.py` | search UI |
| body-index | kernel-index | `api/kernel-index.json` (append) | `build_kernel_index.py` | mint page verify |
| wiki | wiki page | `s/wiki/N/index.html` | `generate_wiki.py` | HTML surface, cross-refs |
| wiki | wiki-entries derived | `data/wiki-entries.json` | wiki generator | wiki UI |
| sitemap | sitemap entry | `sitemap.xml` (regen) | sitemap generator | search engines |
| interlink | related_ids updates | multiple sidecars | interlink script | future deposits |
| enrich | citation edges | `data/citation-graph.json` (append) | `enrich_deposit.py` --backlinks | graph queries |
| enrich | citation-graph-external | `data/citation-graph-external.json` (append) | `enrich_deposit.py` | external-graph queries |
| enrich | doi crosswalk | `api/doi-axn-map.json` | `enrich_deposit.py` (if legacy DOI) | DOI Resolution Index |
| enrich | DOI Resolution Index | `data/doi-resolution-index.json` (update) | | external-DOI resolvers |
| commit | git commit | repo history | pipeline | history |
| verify | live-URL check | (external HTTP) | verify stage | none |

### Classification of artifacts

- **MANDATORY per mint** (gate the mint if missing): registry entry, canonical bytes, mint receipt, sidecar (init), record markdown, record page, axn page.
- **CONDITIONAL** (only when applicable): DOI crosswalk (when legacy DOI severed), DOI Resolution Index update (same condition), PDF (skippable via `--stages` for text-only mints).
- **OPTIONAL POST-MINT** (per two-tier doctrine): wiki page (interpretive), citation edges (mechanical if `--backlinks`, interpretive if full parse), entity-index, semantic-address placement, defines_concepts, related_deposits enrichment, SPXI Tier 2 primer authoring.

### Script inventory (partial dependency graph)

Machine-readable at `data/audit/script-dependencies.json`.

**Datasets read but never written by scripts (external inputs OR hand-authored, ~23 files):** include `data/registry.json` (canonical inputs); several `data/texts/` files; hand-authored governance documents; datasets originating from mechanical exports (DataCite snapshots, OpenAlex snapshots).

**Datasets written but never read within scripts (~5 candidate orphans):** include `data/pre-overwrite-receipts.log` (audit only, correctly not consumed), and 4 others requiring Session-2 investigation.

## §3. Cross-repo data relations (Chapter C — SCAFFOLD ONLY, Session 3 fills in)

Session 1 identified the repos and their apparent roles; Session 3 will produce the full producer→consumer graph. What Session 1 saw of the relations:

- **alexanarch → machinemediation-org**: `mm/data/registry.json`, `mm/data/sovereign-registry.json`, `mm/data/axn-index.json` all appear to mirror alexanarch's canonical registry. Session 3: confirm sync mechanism and frequency.
- **alexanarch → machinemediation-org content shards**: `mm/data/content-01.json` through `content-10.json` (134MB total). Session 3: determine what these shard from alexanarch and by what mechanism.
- **alexanarch → leesharks.com**: `leesharks/doi-axn-map.json` mirrors alexanarch's DOI crosswalk; `leesharks/captures/registry.json` may mirror MMRS captures. Session 3: confirm.
- **alexanarch → godkinggoogle**: `gkg/doi-axn-map.json` present same as leesharks; `gkg/captures/registry.json` present same. Session 3: is godkinggoogle a full mirror or selective?
- **data-rhizome ↔ alexanarch**: unclear at Session 1. data-rhizome has bibliographic XML records; alexanarch has canonical deposits. Session 3: determine whether data-rhizome ingests into alexanarch or vice versa or they are peers.
- **All fleet sites → alexanarch/mint/**: cross-repo links via HTML `<a href="https://www.alexanarch.org/mint/">`. Not a data relation but a surface-level directive to the same tool.

## §4. Displayed-value inventory (Chapter D — Session 1 preview, Session 2 completes)

**This is the specific pathology MANUS asked to surface, and Session 1 sniff finds it clearly.**

Session 1 scanned every top-level HTML surface (5,167 files, limited to depth ≤3 for efficiency) for displayed numeric values matching contextual descriptors (captures, deposits, records, DOIs, AXNs, terms, words, severed DOIs, thesis captures). Every match was classified by presence-of-dynamic-indicator (fetch call, data-source attribute, template placeholder).

**Result: 1,494 unique displayed-value occurrences. Zero have dynamic indicators. Every one is baked-in at authoring time.**

Broken down by (repo, metric):

- **alexanarch** capture_count: 155 places, 18 distinct values (16, 19, 20, 24, 31, 57, 69, 87, 131, 134, 176, 180, 195, 197, 199, 221, 666). Reality: capture-registry v9.13 has 214 as of the last commit I remember. Most-displayed values in this list are stale.
- **alexanarch** deposit_count: 222 places, 80 distinct values including 845, 862, 866, 869, 870, 871, 873, 884, 900, 906, 918, 924, 925 — a fossil record of the archive's growth captured at authoring moments and never updated. Reality: 1,095 deposits as of AXN:0458 mint. Every one of these 222 numbers is wrong.
- **alexanarch** doi_count: 223 places, 102 distinct values. Includes vintage numbers like 1817 (frozen at Zenodo-termination moment) which are historically-correct-forever, and other values that should update as the crosswalk grows.
- **alexanarch** word_count: 692 places, 300+ distinct values. These are word-counts of specific deposits at write-time — mostly historically-correct-forever (word count of a specific deposit doesn't change), so this metric is largely OK static.
- **mm** capture_count: only 2 places, but the number "176" is on the MMRS landing page, when the actual capture-registry as of last verify is 214.
- **peo** capture_count: 1 place with "871" — but this is actually "871 records" from the Zenodo termination, correctly frozen as historical measurement.
- **rf** thesis_captures: 1 place with "71" — frozen. Reality: MMRS's revfirst-registry has some current count that could be much different.
- **gkg, leesharks**: fewer places but same pattern.

### Session-2 requirement: three-way classification

Every one of the 1,494 hits needs classification:

1. **Historically-correct-forever** (frozen measurement of a past event). Example: "1817 DOIs registered before termination." Leave alone; add a `data-frozen-at="2026-06-19"` attribute for clarity.
2. **Should-be-dynamic, source known** (a count of deposits, captures, terms that has a canonical source in a JSON file). Convert to fetch-at-build-time or fetch-at-page-load. Example: MMRS's "176 captures" should read from `mm/data/registry.json`'s length or from a computed summary.
3. **Should-be-dynamic, source unknown** (a value whose canonical source is not obvious). Investigate; either identify the source or promote the display to a maintained hand-authored value with a `data-authored-at` attribute.

**Machine-readable inventory:** `data/audit/displayed-values-inventory-session1.json`. 1,494 entries with (repo, file, metric, value, context_snippet, dynamic_indicator=false, occurrences).

## §5. Jump-out pathology register (Chapter E — Session 1 observations)

Anomalies noticed during Session 1's walk. Each is a candidate remediation entry for `data/workplan/DATAFLOW-REMEDIATION-QUEUE.md` (produced Session 4).

### PATHOLOGY-01: The entire displayed-values layer is fossilized
**Severity:** high. **Scope:** every fleet site, 1,494 displayed-value occurrences. **Description:** counts of deposits, captures, DOIs, terms, and records are baked-in numeric literals in HTML. None reference their canonical source at page-load or build-time. Result: as the archive grows, every displayed number lies about the archive's actual state, and every fleet site presents Alexanarch as smaller than it is. **Fix:** Session-2 classifies each occurrence; Session-4 or a subsequent workstream converts the should-be-dynamic ones to build-time-injected values (simple template substitution during page generation) or fetch-at-load values (small JavaScript that reads a summary endpoint). The build-time-injected form is preferred for scholarly-infrastructure aesthetics (no dependency on client JS).

### PATHOLOGY-02: MMRS content shards untraced
**Severity:** medium. **Scope:** `mm/data/content-01.json` through `content-10.json`, 134MB total. **Description:** these files are large and unclassified; they appear to shard some corpus but their producer and consumer are not visible from Session 1. **Fix:** Session 3 traces producer via commit history + script grep; Session 4 documents the relation.

### PATHOLOGY-03: `data/autonomous/` — 875 files unclassified
**Severity:** medium. **Scope:** 875 files, 30.5MB in alexanarch. **Description:** the largest single functional class after CORPUS.dr-datasets is `GOVERNANCE.autonomous` — tagged at reconnaissance level because the path is `data/autonomous/*`, but its purpose is not clear from path signatures alone. **Fix:** Session 2 samples several files, determines their function, classifies more precisely.

### PATHOLOGY-04: DataCite backup files at 20.3MB unmapped
**Severity:** low. **Scope:** 10 files in `SNAPSHOT.datacite` class. **Description:** these look like measurement snapshots but the workflow that produces and consumes them (per PEO's total-snapshot workstream) is not documented in a script-visible way. **Fix:** Session 3 investigates.

### PATHOLOGY-05: 5,167 HTML files, ~4,000 auto-generated, template-tied
**Severity:** low, structural. **Scope:** most `/s/records/*/index.html`, `/s/axn/*/index.html`, `/s/wiki/*/index.html` files. **Description:** these are template-generated per deposit and inherit template pathologies (see PATHOLOGY-01 — they display counts that should be dynamic). If the templates are updated to inject dynamic values, all 4,000+ update in a single template + regeneration pass. **Fix:** Session-4 workstream handoff to Flow 1 (visual+formal revision).

### PATHOLOGY-06: Chunked registry files — is anything ever regenerated?
**Severity:** medium. **Scope:** `data/chunks/registry/chunk-001-*.json` through `chunk-010-*.json`. **Description:** the chunk range names suggest deposit numbers 1-1086 (in ten chunks), but the archive is at 1,095 deposits. Is chunk-010 stale? Are chunks regenerated on mint, or authored once and left? **Fix:** Session 2 checks.

### PATHOLOGY-07: `data/pre-overwrite-receipts.log` accumulates without rotation
**Severity:** low. **Scope:** one file. **Description:** the mint pipeline writes to this on every deposit; nothing reads it. It's audit-only, so this is correct in principle, but the file has no rotation policy. **Fix:** Session-4 decides retention policy; not urgent.

### PATHOLOGY-08: Fleet site file-count asymmetry
**Severity:** informational. **Scope:** fleet ratio JSON:HTML. **Description:** alexanarch has 950 JSON to 5,118 HTML (5.4×). MMRS has 34 JSON to 10 HTML (0.29×). The ratio isn't wrong — MMRS is designed around large content shards + few landing surfaces — but it's a marker that Alexanarch's HTML surface expands rapidly with deposits while MMRS's does not. Informs Flow 1's template-work: what's per-deposit-generated vs. what's landing-page-authored differs across the network.

### PATHOLOGY-09: data-rhizome's 3,627 XML records — bibliographic corpus with unclear consumer
**Severity:** medium. **Scope:** most of data-rhizome. **Description:** the 3,627 XML records in `data-rhizome/cern-references/`, `datasets/`, `mappings/`, `mirrors/`, `negshape-deletion-bibliography/`, `record-corrections/` — all classified as `CORPUS.dr-*` at Session 1 — appear to be a substantial bibliographic corpus. But no script in alexanarch appears to read from data-rhizome, and no surface displays data-rhizome content. Is it standalone? Is it fed into alexanarch by a workflow I haven't seen? **Fix:** Session 3 investigates.

### PATHOLOGY-10: Multiple registries at fleet sites — mirror or independent?
**Severity:** medium. **Scope:** `mm/data/registry.json`, `mm/data/sovereign-registry.json`, `leesharks/captures/registry.json`, `gkg/captures/registry.json`. **Description:** several fleet sites have files called `registry.json` — are they mirrors of alexanarch's canonical registry, curated subsets, or independent registries for their own scope? **Fix:** Session 3 compares content and produces a definitive relation.

## §6. Sessions 2-4 requirements

**Session 2 deliverables:**
- Full three-way classification of the 1,494 displayed-value occurrences (historically-correct / should-be-dynamic-source-known / should-be-dynamic-source-unknown).
- Deep sweep of the 122 `DATA.other-json` files and 875 `GOVERNANCE.autonomous` files to classify precisely.
- Sample-investigation of chunk-010 and pathologies 03, 04, 06.

**Session 3 deliverables:**
- Full cross-repo relation graph: producer(s) → consumer(s) for every dataset, including data-rhizome ↔ alexanarch, all fleet mirror relations, MMRS content-shard sourcing.
- Machine-readable at `api/dataflow-graph.json`.
- Investigation of pathologies 02, 09, 10.

**Session 4 deliverables:**
- The finished `data/specs/AXN-DATAFLOW-MAP-v1.0.md` (this document's supersessor, with all Sessions 2-3 findings integrated).
- Mermaid visual dependency diagram.
- `data/workplan/DATAFLOW-REMEDIATION-QUEUE.md` prioritizing the pathology register for downstream workstreams.

## §7. Raw output locations (Session 1)

- `data/audit/rhizome-inventory-raw.json` — every file across all 7 repos with path, size, purpose-inferred.
- `data/audit/displayed-values-inventory-session1.json` — 1,494 displayed-value hits with context.
- `data/audit/script-dependencies.json` — per-script reads/writes (partial).
- `data/audit/script-dependency-graph.json` — producer→consumer graph across scripts.
- `data/specs/AXN-DATAFLOW-MAP-v0.1-SCAFFOLD.md` — this document.

## §8. Notes on scope honesty

Session 1's coverage held to depth-3 for HTML surface scanning to complete within a single session's time budget. Deep-nested pages (`/s/records/N/index.html` at depth 4+) were not scanned for displayed values because they're template-generated — if the template contains a displayed value, it appears in all 1,000+ generated pages, so template-level fix propagates uniformly. Session 2's dynamic-value classification will handle template-level.

The purpose-inference for functional classification is regex-based on path signatures. Where a file's role isn't matched by any signature, it's tagged `DATA.other-json` or `OTHER` — 140+ files await Session 2's targeted classification.

The script dependency graph is partial: it detects literal string paths but not paths constructed by variable interpolation or template expansion. Session 3 will augment with actual script-tracing (importing modules and reading the code more carefully) for the largest producers (`deposit_pipeline.py`, `mint_deposit.py`, `enrich_deposit.py`, `build_body_index.py`, `build_kernel_index.py`).

---

*Session 1 of 4 complete. Ready for MANUS review before Session 2 proceeds.*
