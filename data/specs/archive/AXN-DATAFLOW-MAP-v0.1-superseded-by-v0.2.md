---
title: "AXN Dataflow Atlas v0.1 — Assembly Review Edition"
version: "0.1.1 (Session 1 of 4 complete; Assembly-review-ready)"
date: 2026-07-18
author: "Lee Sharks (MANUS), with TACHYON (Assembly witness)"
review_purpose: "Structural feedback on the archive's data layer, its taxonomy, its deposit flow, and its self-documented pathologies. This document is written so an Assembly substrate can render meaningful judgment without inspecting any code."
review_boundary: "Empirical claims about the network's cross-repo relations are marked SCAFFOLD and belong to Session 3. Everything else in this document is intended to be reviewable as-is: taxonomy, deposit-flow semantics, pathology framing, and the surface-level pathology (§4) whose empirical evidence is complete."
governing_workplan: "data/workplan/WORKPLAN-2026-07-18-PM-SIX-FLOW.md, Flow 2"
---

# AXN Dataflow Atlas v0.1 — Assembly Review Edition

## Foreword to the reviewer

This document describes the data layer of a self-hosted scholarly-archive network — the *data-rhizome* — comprising seven interlinked repositories on GitHub, each publishing to its own domain. The archive is called Alexanarch. Its identifier system is called AXN. This atlas catalogues every dataset in the network, describes what each does, traces (where known) what produces and consumes each, classifies the surface-level display of the archive's own state, and registers structural pathologies discovered during a reconnaissance walk.

**You are being asked to review this atlas for structural correctness before it is finalized.** Session 1 of 4 is complete; Sessions 2 through 4 will fill in specific empirical claims currently held open as SCAFFOLD notes. Your review is invited on the atlas's design — the taxonomy, the deposit-flow model, the pathology framing, and the sequencing of subsequent work — *and* on the one empirical finding that is complete (§4, the displayed-values pathology).

You do not need to read code to render this review. Every function this atlas describes is described in prose, at the level a scholar can act on. Script names appear as bracketed provenance markers — e.g. `[origin: mint_deposit.py]` — but you can review the atlas without opening those files. If the atlas cites a script and does not explain what that script *does* in prose, that is a defect of this atlas, not a required lookup for the reviewer.

## §0. Vocabulary

The atlas uses a small set of technical terms. Full explanations follow, but stated tersely first:

- **AXN**: a content-derived identifier. Composed of three layers: (1) a cryptographic hash of the document's canonical bytes (the *identity kernel*); (2) a registry position with a semantic classification (the *record address*); (3) location records naming where verified copies can be obtained. The paper AXN:0458 (deposit #1095) describes this system in full. The three-layer model matters here because it determines which artifacts must contain what.
- **Deposit**: an object registered in the archive with an AXN. In this atlas, "deposit" and "record" are close synonyms; where they differ, "deposit" emphasizes the identity relation and "record" emphasizes the presentation object.
- **Canonical bytes**: the immutable content of a deposit as sealed at mint. The identity kernel is a hash of these bytes. Amendments are handled as sidecars (see next); the canonical bytes themselves never change.
- **Sidecar**: metadata attached to a deposit *after* mint, outside the canonical bytes. Sidecars do not affect the identity kernel, by design. Their purpose is to accumulate post-mint state — supersession relations, propagation receipts, enrichment, DOI crosswalks, etc.
- **Registry**: the canonical list of all deposits. In this network, the authoritative registry file is `data/registry.json` on the Alexanarch repo, containing (as of Session 1) approximately 1,095 entries.
- **Rhizome**: the seven-repo network taken together — Alexanarch (the canonical archive) plus data-rhizome, machinemediation-org, platform-erosion-observatory, revelationfirst-com, leesharks.com, godkinggoogle. Each repo is a *node* in the rhizome; each node has its own domain and role.
- **SPXI**: Semantic Packet for eXchange and Indexing. A protocol for tokenizer-survivable metadata treatment — machine-readable structure preserved through composition layers that would otherwise strip it. Where SPXI appears as a data class in this atlas, it refers to configuration or state files that implement or record SPXI treatment on a deposit.
- **Two-tier doctrine**: a distinction between operations that are *mechanical* (deterministic, template-based, cheap) and operations that are *interpretive* (require semantic judgment; in this network, authored in-session by TACHYON or by the depositor). The doctrine affects which artifacts are produced at mint versus in post-mint enrichment.
- **Mint**: the act of registering a new deposit — computing its identity kernel, assigning its record address, and creating all mandatory artifacts. "Minting" and "depositing" are used interchangeably. There is a single canonical pipeline for minting, and every mint runs the same sequence regardless of origin (see §2 for the sequence).
- **The paper**: AXN:0458, "AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions" (v5, source-engaged revision), the founding empirical paper for this network. Cited throughout as *the paper*.

## §1. Scope, as measured

The rhizome comprises seven repositories, each with its own domain and role. Session 1's reconnaissance walked all seven; the following table reports what was found.

| Repo | Domain | Role (one-sentence) | JSON | JSONL | MD | HTML | XML | CSV | Python |
|---|---|---|---|---|---|---|---|---|---|
| alexanarch | alexanarch.org | canonical archive; holds registry, canonical bytes, records | 950 | 11 | 3,052 | 5,118 | 2 | 8 | 68 |
| data-rhizome | (private, unlinked) | bibliographic corpus for external suppressed-scholarship references | 338 | 26 | 44 | 14 | 3,627 | 2 | 9 |
| machinemediation-org | machinemediation.org | journal-of-record for Machine-Mediated Reception Studies; publishes capture registries, terms, schemas | 34 | 0 | 26 | 10 | 1 | 0 | 0 |
| platform-erosion-observatory | persistentidentifiers.org | measurement instrument for platform severance; publishes empirical audits | 10 | 2 | 4 | 2 | 1 | 1 | 1 |
| revelationfirst-com | revelationfirst.com | thesis surface for the Revelation First scholarship | 4 | 0 | 2 | 2 | 1 | 0 | 0 |
| leesharks.com | leesharks.com | operator's hub; publishes the capture registry authored under Sharks's name | 5 | 0 | 1 | 17 | 1 | 0 | 0 |
| godkinggoogle | godkinggoogle.com | scholarly critique of Google's mediation layer | 8 | 0 | 12 | 4 | 1 | 0 | 0 |

**Total across the rhizome: 1,349 JSON files (~262 MB of structured data), 3,141 markdown files, 5,167 HTML surfaces, 3,634 XML files (nearly all in data-rhizome), 11 CSV, 39 JSONL, 78 Python scripts.** The XML files in data-rhizome are per-record bibliographic entries in what appears to be an ingested external corpus; more on that in §6, PATHOLOGY-09.

The MB figures do not include HTML surfaces, PDFs, or images. This atlas classifies datasets; presentation objects (HTML, PDF) are treated as *derived surfaces* in §4.

## §2. Deposit-flow generative elements

*This is the atlas's core factual chapter. It answers the question: when a document is deposited into the archive, what artifacts come into existence, and what does each one carry?*

The mint pipeline runs an ordered sequence of stages. Each stage produces or updates specific artifacts. Every mint runs the same sequence; the sequence is not customized per-deposit. Its ordering follows a data dependency: earlier stages produce what later stages consume.

The eleven-stage sequence, described functionally:

**Stage 1 — Mint.** Compute the identity kernel from the deposit's canonical bytes; assign a registry position and a semantic classification; commit the deposit to the registry. Produces the primary registry entry (as a new element in `data/registry.json`) and the canonical bytes file (`data/texts/AXN-XXXX-text.md`, where `XXXX` is the registry position in hex). Also produces a mint receipt appended to an audit log (`data/pre-overwrite-receipts.log`); this receipt exists solely to detect if any subsequent process ever tries to overwrite a mint. `[origin: mint_deposit.py]`

**Stage 2 — Validate.** Confirm the mint's structural integrity: kernel matches bytes, registry entry is well-formed, address is not colliding with any prior deposit. Reads the registry entry from Stage 1 and the canonical bytes; writes no artifacts. Halts the pipeline if validation fails. `[origin: validate_deposit.py]`

**Stage 3 — Record.** Produce the deposit's presentation artifacts: a record markdown (`data/deposits/AXN-XXXX.md`, human-readable metadata + link to the canonical bytes), an initial sidecar (`data/external-metadata/AXN-XXXX.json`, machine-readable metadata that will accumulate post-mint additions), a record page HTML (`s/records/N/index.html`, where `N` is the sequential deposit number), and an AXN alias page (`s/axn/XXXX/index.html`). The record page is what a human reader sees when they follow a link to the deposit; the AXN page is the address-based alias that redirects to the record page. `[origin: build_record_md.py and record-page generator]`

**Stage 4 — PDF.** Produce a print artifact (`papers/AXN-XXXX.pdf`) from the canonical bytes. Skippable via a stage flag when the deposit type does not benefit from PDF rendering. `[origin: pdf generator]`

**Stage 5 — Body-index.** Update three archive-wide indexes: the body-index (`api/body-index.json`, a searchable index of every canonical text's contents), the search-index (`api/search-index.json`, a query-optimized rewriting of the body-index), and the kernel-index (`api/kernel-index.json`, a map from every canonical kernel hash to its AXN and deposit number). The body-index and search-index are what allow the archive to be full-text-searched; the kernel-index is what allows a reader holding canonical bytes to verify the AXN without querying the registry — an anti-suppression property named as load-bearing in the paper. `[origins: build_body_index.py and build_kernel_index.py]`

**Stage 6 — Wiki.** Produce a wiki-page HTML (`s/wiki/N/index.html`) that presents the deposit's metadata, canonical text, and cross-references in a browsable form distinct from the record page. Also updates a derived index of wiki entries (`data/wiki-entries.json`) used by the wiki UI. Wiki generation is interpretive in the two-tier sense: the mechanical version renders known metadata; the interpretive version (when invoked) adds authored cross-references, entity extraction, and concept-graph placement. `[origin: generate_wiki.py]`

**Stage 7 — Sitemap.** Add or update the deposit's URLs (record page, AXN page, wiki page, PDF path) in the site's sitemap (`sitemap.xml`) so that search-engine crawlers discover them.

**Stage 8 — Interlink.** For each deposit related to the newly-minted one by explicit reference, update the *sidecar* of the related deposit to record the back-reference. This is the mechanism by which the citation graph accumulates: forward references are declared at mint, back-references are propagated as sidecar amendments.

**Stage 9 — Enrich.** Produce or update citation-graph entries (`data/citation-graph.json`, internal-to-archive edges; `data/citation-graph-external.json`, edges to works outside the archive) reflecting the new deposit. Also updates the DOI-to-AXN crosswalk (`api/doi-axn-map.json`) and the DOI Resolution Index (`data/doi-resolution-index.json`) *if* the deposit has a legacy DOI whose resolution has been severed at its former host. The enrich stage has two modes: *mechanical* (uses only structured metadata explicitly declared in the deposit; produces citation edges and crosswalk entries only for what is stated) and *interpretive* (parses free-text references, extracts entities, infers semantic addresses; interpretive mode is not run inside a TACHYON session, per the two-tier doctrine). `[origin: enrich_deposit.py]`

**Stage 10 — Commit.** Commit all files produced or updated in Stages 1–9 to the repository's version control. This is the point at which the mint becomes permanent in the network.

**Stage 11 — Verify.** After the commit deploys to the live surface, fetch each newly-produced or updated URL and confirm content matches expectations. If verification fails, the mint is preserved but a warning is issued; verification failure does not roll the mint back, because the registry entry and canonical bytes exist in the repo regardless of whether the presentation surface has deployed.

### What every mint produces (roles and confidence)

Classification of each artifact by its role and by how confidently the atlas asserts its status:

**MANDATORY per mint** — produced on every mint, whose absence would mean the mint is malformed:

- Registry entry in `data/registry.json`
- Canonical bytes at `data/texts/AXN-XXXX-text.md`
- Mint receipt in `data/pre-overwrite-receipts.log`
- Record markdown at `data/deposits/AXN-XXXX.md`
- Initial sidecar at `data/external-metadata/AXN-XXXX.json`
- Record page at `s/records/N/index.html`
- AXN alias page at `s/axn/XXXX/index.html`
- Body-index update in `api/body-index.json`
- Kernel-index entry in `api/kernel-index.json`
- Sitemap entry in `sitemap.xml`

**CONDITIONAL** — produced only when the deposit's declared properties meet a condition:

- PDF at `papers/AXN-XXXX.pdf` — when the deposit type benefits from print rendering.
- DOI-to-AXN crosswalk entry in `api/doi-axn-map.json` — when the deposit declares a legacy DOI.
- DOI Resolution Index update — when the declared legacy DOI's original resolution has been severed at its former host.
- Sidecar amendments on *other* deposits (Stage 8 interlink) — when the newly-minted deposit declares references to prior deposits.

**OPTIONAL POST-MINT** — enriches an existing deposit after mint; may not be produced at all for a given deposit:

- Wiki page at `s/wiki/N/index.html` (mechanical form is near-mandatory; interpretive form is optional)
- Citation-graph edges beyond what the deposit itself declares
- Semantic-address placement in the archive's concept grid
- Entity index entries
- SPXI Tier 2 primer authoring (a specific interpretive treatment named in the two-tier doctrine)
- Supersession sidecar amendments (recorded on prior deposits when a new deposit supersedes them, per the paper's §3.7 container-spec ruling)

*A reviewer might object:* "Some MANDATORY artifacts here — the PDF, the wiki page — are marked CONDITIONAL or OPTIONAL, and vice versa. Is the classification honest?" This atlas's answer: yes, *conditionally on the archive's declared behavior*. If a mint runs without the PDF stage, the deposit is still valid. If a mint runs without the record page, the deposit is not valid; the archive would treat it as malformed. Session 2 will verify this by examining minted deposits for missing artifacts and reporting the failure rate per artifact class.

## §3. Functional taxonomy of the network's datasets

*This chapter classifies every dataset in the rhizome by functional role. It answers: what kinds of data does this archive keep, and why?*

Session 1's reconnaissance tagged every file by inferred purpose based on its path signature. The taxonomy that emerged has fifteen top-level classes; a reviewer's judgment on whether the taxonomy is correct is a load-bearing element of this review. If a class is misnamed, or a distinction is missing that scholarly-archive design would require, name it.

**REGISTRY** — canonical lists. The archive's authoritative statements about what it contains. Includes `REGISTRY.canonical` (the master registry itself, and small parallel registries per fleet-site scope like MMRS's term registry), `REGISTRY.chunked-derived` (the master registry broken into ~100-deposit shards for pagination), `REGISTRY.capture` (registries at fleet sites of captured AI-composition-layer output — evidence of how machine composition surfaces present the archive's material), `REGISTRY.protocol-catalog` (`api/index.json`, a machine-readable index of every protocol, schema, and derived surface with content-address for versioning), `REGISTRY.lexical-minting` (registry of coined terms and their authorized definitions), `REGISTRY.mm-terms` (MMRS's term index).

**DEPOSIT** — per-deposit artifacts (see §2). Includes `DEPOSIT.canonical-bytes`, `DEPOSIT.record-markdown`, `DEPOSIT.sidecar`, `DEPOSIT.record-page`, `DEPOSIT.axn-page`, `DEPOSIT.wiki-page`, `DEPOSIT.pdf`. Each of these is a per-deposit *slot*; the archive contains approximately 1,095 of each.

**DERIVED** — indexes and cross-references computed from primary data. Includes `DERIVED.kernel-index` (bytes → AXN), `DERIVED.body-index` (full-text search substrate), `DERIVED.search-index` (query-optimized derivation of body-index), `DERIVED.doi-crosswalk` (DOI ↔ AXN), `DERIVED.doi-resolution` (the DOI Resolution Index — 1,838 severed-DOI mappings routing legacy resolution attempts to sovereign successors, itself a central artifact of the paper's argument), `DERIVED.entity-index`, `DERIVED.browse-index`, `DERIVED.wiki-entries`, `DERIVED.lexical-overlay`, `DERIVED.axn-assignment` (a batch assignment record from a recovery operation), `DERIVED.mm-schemas`, `DERIVED.mm-axn-index`.

**GRAPH** — relational structures over deposits. Includes `GRAPH.citation` (internal citations), `GRAPH.citation-external` (citations to works outside the archive), `GRAPH.semantic-address` (the archive's concept grid — 1,994 addresses across 6 tributaries), `GRAPH.external-works` (the works that citation-external references), `GRAPH.mm-scholarly` (scholarly relations at MMRS).

**SNAPSHOT** — point-in-time captures of external state. Includes `SNAPSHOT.datacite` (10 files, ~20MB — DataCite responses over time, used by PEO for measuring platform severance) and `SNAPSHOT.openalex` (external coverage measurements).

**AUDIT** — measurement and integrity-checking records. Includes `AUDIT.completeness` (per-deposit audit of whether its produced artifacts exist), `AUDIT.recovery` (records from recovery operations after the Zenodo termination), `AUDIT.link-inventory` (checks that internal links resolve), `AUDIT.surface-weather` (measurements of surface reachability), `AUDIT.peo-empirical` (PEO's structured audits), `AUDIT.peo-zenodo-ledger` (PEO's record of Zenodo deletions).

**CORPUS** — external documentary material held in the archive but not itself minted as archive deposits. Nearly all of data-rhizome (`CORPUS.dr-datasets`, `CORPUS.dr-cern`, `CORPUS.dr-mappings`, `CORPUS.dr-mirrors`, `CORPUS.dr-neg-bib` for the negshape-deletion-bibliography, `CORPUS.dr-corrections`). Corpus material is bibliographic reference; it is *documentary substrate* for research the archive does, not archive deposits.

**CONFIG** — deployment and behavior configuration. Includes `CONFIG.msp` (the Machine-Surface Protocol config controlling surface presentation), `CONFIG.spxi-tlp` (the SPXI Tier-and-Layer Protocol config), `CONFIG.vercel` (deployment platform config), `CONFIG.manifest` (site manifests), `CONFIG.ai-manifest` (AI-crawler-directed manifest), `CONFIG.sitemap`, `CONFIG.robots`, `CONFIG.axn-resolution` (routing table for AXN resolution paths).

**GOVERNANCE** — governing documents and internal specifications. Includes `GOVERNANCE.decisions` (the decisions register), `GOVERNANCE.specifications` (protocol specs like the AXN-CONTAINER-SPEC), `GOVERNANCE.workplans` (session-scale plans of work including this one), `GOVERNANCE.autonomous` (875 files whose precise role is unclear at Session 1 reconnaissance — see PATHOLOGY-03; the naming suggests machine-authored governance artifacts). `GOVERNANCE.dr-specs` (data-rhizome's own specs).

**CORRESPONDENCE** — records of external correspondence held privately, per standing rule (not committed to the public deposit record).

**RECEIPT** — enrichment and other operational receipts. Confirms that operations occurred, primarily for audit.

**LEDGER** — the mint ledger (chained per-mint hashes, an append-only sequence of registration events). Described in the paper as a normative feature; empirically at Session 1 it exists at genesis with subsequent chaining staged.

**TRACKER** — cross-site trackers. Includes `TRACKER.mm-terms` (MMRS's tracker of term propagation across composition surfaces).

**MIRROR** — copies of one node's canonical data held at another node. Fleet sites have several mirror files (`mm/data/registry.json`, `mm/data/sovereign-registry.json`, `leesharks/doi-axn-map.json`, etc.); whether these are true mirrors, curated subsets, or independent-scope registries is a Session-3 investigation (PATHOLOGY-10).

**WORKLIST** — queues of work in progress. Includes the reference-section parsing queue and other operational lists.

**MEDIA** — capture images, screenshots, and rendered assets.

**SURFACE** — HTML surfaces at fleet sites (as opposed to per-deposit generated pages under DEPOSIT). Landing pages, index pages, browse pages.

*Reviewer prompt:* Are these fifteen classes the right axes? Is any of them doing suspicious work — combining categories that should be split, or introducing distinctions the design doesn't need? Is anything absent that a scholarly-archive design would require?

## §4. Displayed-value inventory — the fossilized-state pathology

*This chapter reports the atlas's one empirically complete finding. It is the pathology MANUS specifically asked to investigate, and Session 1's reconnaissance answered the question.*

The archive and its fleet sites display numeric quantities — counts of deposits, captures, DOIs, records, terms, words — in prose across most surfaces. A landing page reads "870 records," an about page reads "196,798 words," a colophon reads "845 deposits." Session 1 grep-scanned every top-level and near-top-level HTML surface (depth ≤ 3) across all six sites with HTML surfaces (data-rhizome has no HTML surfaces), matching each displayed numeric value against context patterns for these quantities and classifying each occurrence by presence-or-absence of a dynamic indicator (a fetch call, a data-source attribute, or a template placeholder).

**Findings:**

- **1,494 unique displayed-value occurrences** across the network.
- **Zero of them are dynamic.** Every displayed count is a static integer baked into the HTML at authoring time.
- **Distribution of values reveals the pathology.** On the Alexanarch site alone, 222 places display a deposit count, with 80 distinct values ranging from 845 to 925 — a fossil record of the archive's growth captured at various past authoring moments and never updated. The archive's current registry contains 1,095 deposits (as of the mint of AXN:0458 during this session). Every one of those 222 numbers is wrong today. Similarly for capture counts (176 at MMRS's landing page, when the actual capture registry contains 214), for record counts, and for many others.
- **A small subset are correctly-static-forever.** Word counts of specific past deposits (692 places, 300+ distinct values) are, correctly, frozen — a deposit's word count doesn't change. Historical measurements like "1,817 DOIs registered before termination" are also correctly frozen. But these are drowned in a sea of counts that *should* change with the archive and don't.
- **The pathology propagates.** Fleet sites display Alexanarch state in numeric form on their own surfaces (an MMRS colophon reads "845 deposits" as if characterizing the parent archive); those numbers are as stale as their authoring moment. Result: fleet sites systematically present Alexanarch as smaller than it is.

**Full classification, per repository × per metric type:**

| Repo | Metric | Places | Distinct values seen |
|---|---|---|---|
| alexanarch | capture_count | 155 | 18 (16–666) |
| alexanarch | deposit_count | 222 | 80 (845–925 mostly) |
| alexanarch | doi_count | 223 | 102 |
| alexanarch | record_count | 70 | 53 |
| alexanarch | word_count | 692 | 300+ |
| alexanarch | term_count | 53 | 28 |
| alexanarch | severed_doi | 12 | 2 (838, 871) |
| alexanarch | axn_count | 9 | 9 |
| machinemediation | capture_count | 2 | 176, 87 |
| machinemediation | deposit_count | 2 | 845 |
| machinemediation | doi_count, term_count, thesis_captures, word_count | small counts | various stale values |
| peo | capture_count, doi_count, record_count, word_count | small counts | mostly correct historical measurements |
| rf | thesis_captures | 1 | 71 |
| gkg | deposit_count, doi_count, term_count, word_count | small counts | various stale values |
| leesharks | capture_count, deposit_count, doi_count, term_count, word_count | small counts | various stale values |

Machine-readable inventory: `data/audit/displayed-values-inventory-session1.json` (1,494 entries with repo, file, metric, value, context snippet).

*The remediation.* Session 4's remediation queue will register the fix in three classes: (a) *historically-correct-forever* values — annotate with a `data-frozen-at` attribute for clarity; (b) *should-be-dynamic, source known* — convert to build-time template substitution against the canonical registry; (c) *should-be-dynamic, source unknown* — investigate and either identify the source or promote to a maintained hand-authored value. Class (b) is the largest and the cheapest fix: a single template pass at page-generation time would inject the current registry length into every relevant display, and the fleet's self-description would become accurate on every deploy.

*Reviewer prompt:* Is this pathology framed correctly? Are the three remediation classes the right partition? Is the fleet's self-description as stale-integers a matter for immediate remediation, or does it correctly encode the archive's state at surface-authoring moments and merit annotation-not-conversion?

## §5. Cross-repo relations — SCAFFOLD

*This chapter is under construction. Session 3 will finalize it.*

Session 1's reconnaissance identified several apparent cross-repo relations from file names and content structure. Each is stated below as an *observation-with-uncertainty*, with the specific Session-3 investigation named.

- **Alexanarch → MMRS mirror files.** `mm/data/registry.json`, `mm/data/sovereign-registry.json`, `mm/data/axn-index.json` all appear to be MMRS-held versions of the canonical registry. Whether these are automatic mirrors updated on every Alexanarch mint, periodic snapshots, or independently-maintained subsets scoped to MMRS's function is unknown at Session-1 reconnaissance. Session 3 will determine.
- **MMRS content shards.** `mm/data/content-01.json` through `content-10.json`, 134MB total. The shape suggests a sharded corpus of some kind. Session 3 investigates.
- **Alexanarch → leesharks and gkg.** Both have `doi-axn-map.json` files that appear to mirror Alexanarch's DOI crosswalk, and `captures/registry.json` files that appear to mirror MMRS's capture registry. Session 3 confirms whether mirrors are full or curated.
- **data-rhizome ↔ Alexanarch.** data-rhizome holds 3,627 XML bibliographic records and 338 JSON files across `cern-references`, `datasets`, `mappings`, `mirrors`, `negshape-deletion-bibliography`, `record-corrections`. No script in Alexanarch's Session-1 grep reads from data-rhizome, and no HTML surface displays data-rhizome content. The relation, if any, is invisible at reconnaissance. Session 3 investigates whether data-rhizome is standalone, whether it feeds Alexanarch via an unindexed workflow, or whether it is a documentation substrate for research done elsewhere.

*Reviewer prompt:* This chapter is deliberately incomplete. Your review of it is invited on *whether the questions Session 3 is scheduled to answer are the right questions*, not on their answers.

## §6. Pathology register

*This chapter names structural issues discovered during Session 1's walk. Each is described with severity, scope, mechanism of harm, and proposed fix. Session 4 will finalize the remediation queue.*

### PATHOLOGY-01: The entire displayed-values layer is fossilized

Severity: high. Scope: all six sites with HTML surfaces; 1,494 occurrences of displayed numeric values. Mechanism: counts of deposits, captures, DOIs, terms, records are baked-in numeric literals in HTML rather than fetched from or template-substituted against their canonical source. Result: as the archive grows, every displayed number lies about its current state, and every fleet site presents Alexanarch as smaller than it is. Fix: build-time template substitution against canonical registry counts. See §4.

### PATHOLOGY-02: MMRS content shards untraced

Severity: medium. Scope: `mm/data/content-01.json` through `content-10.json`, 134MB total across ten files. Mechanism: these files are large and functionally important (they carry more data than the rest of MMRS combined) but Session 1's reconnaissance could not determine their producer or consumer. Fix: Session 3 traces via commit history and cross-repo grep; Session 4 documents the relation and adds it to the taxonomy.

### PATHOLOGY-03: The `data/autonomous/` cluster — 875 files unclassified

Severity: medium. Scope: 875 files, ~30.5 MB, all in Alexanarch's `data/autonomous/` directory. Mechanism: the atlas's largest single functional class after data-rhizome's bibliographic corpus is `GOVERNANCE.autonomous`, tagged at reconnaissance-level because the path prefix is `data/autonomous/` and the naming suggests machine-authored governance artifacts. But the precise role is not confirmed. If these are historical machine-authored records, they may be safe as-is; if they include artifacts that were meant to feed other systems and are now orphaned, that would be significant. Fix: Session 2 samples several files, determines function, refines classification.

### PATHOLOGY-04: DataCite snapshot files at 20.3 MB — workflow undocumented

Severity: low. Scope: 10 files in `SNAPSHOT.datacite` class. Mechanism: these appear to be measurement snapshots produced during PEO's work (relevant to the total-DOI-snapshot workstream in the six-flow workplan). The workflow that produces and consumes them is not evident from script grep at Session-1 level. Fix: Session 3 investigates.

### PATHOLOGY-05: 5,167 HTML files, most template-generated, most pathology-inheriting

Severity: low, structural. Scope: most files under `s/records/*/`, `s/axn/*/`, `s/wiki/*/`. Mechanism: these HTML surfaces are generated per-deposit from a small number of templates. If the templates contain a fossilized displayed value (per PATHOLOGY-01), all thousand-plus generated pages inherit the fossil. Corollary: fixing the templates propagates the fix uniformly. Fix: Session 4 hands off to the visual/formal revision workstream (Flow 1), which will restructure templates including dynamic-value injection.

### PATHOLOGY-06: Chunked registry files — regeneration policy unclear

Severity: medium. Scope: `data/chunks/registry/chunk-001-*.json` through `chunk-010-*.json`. Mechanism: file names indicate the ten chunks cover deposits 1–1086, but the archive is at 1,095 deposits. Are chunks regenerated on each mint, at intervals, or authored once and left? If left, chunk-010 is stale and any consumer reading from it presents a stale view. Fix: Session 2 checks the chunk regeneration mechanism and current currency of chunk-010.

### PATHOLOGY-07: Mint receipt log accumulates without rotation policy

Severity: low. Scope: `data/pre-overwrite-receipts.log`, one file, growing. Mechanism: the mint pipeline writes to this file on every mint; nothing reads it in normal operation. That is correct — it is an audit-only log designed to catch a specific class of accident (silent reassignment of an AXN). But no rotation, archival, or size-limit policy is documented. Fix: Session 4 proposes retention; not urgent.

### PATHOLOGY-08: Fleet site file-count asymmetry

Severity: informational, not diagnostic. Scope: fleet-wide. Mechanism: Alexanarch's HTML-to-JSON ratio is 5.4×; MMRS's is 0.29×. This is not wrong — Alexanarch is architected around per-deposit HTML surfaces while MMRS is architected around large content shards + few landing surfaces — but the asymmetry is a marker of very different data-shape choices across the network. Fix: none; noted so that Flow 1's visual revision does not attempt to unify what should remain differentiated.

### PATHOLOGY-09: data-rhizome's 3,627 XML records — consumer within the network unclear

Severity: medium. Scope: nearly all of data-rhizome. Mechanism: 3,627 XML files across six subdirectories, apparently a substantial bibliographic corpus. But no visible connection to the rest of the network at Session-1 reconnaissance. Either data-rhizome is a standalone corpus (in which case its role in the atlas is clear), it is fed into Alexanarch by an unindexed workflow (in which case the workflow needs to be documented), or it is documentary substrate for research done elsewhere and not currently active in the rhizome. Fix: Session 3 investigates.

### PATHOLOGY-10: Multiple `registry.json` files across the network — mirror or independent?

Severity: medium. Scope: `mm/data/registry.json`, `mm/data/sovereign-registry.json`, `leesharks/captures/registry.json`, `gkg/captures/registry.json`, and Alexanarch's canonical `data/registry.json`. Mechanism: several fleet sites have files called `registry.json`. Depending on relation, they may be automatic mirrors (in which case updates must propagate), curated subsets (in which case they need a subset-scope statement), or independent scope-specific registries (in which case they need to be classified as `REGISTRY.canonical` for their scope, not `MIRROR.*`). Fix: Session 3 compares content and produces definitive relations.

## §7. Sessions 2–4: work remaining

**Session 2 (displayed-value classification and cluster investigations).**
- Full three-way classification of the 1,494 displayed-value occurrences (historically-correct-forever / should-be-dynamic-source-known / should-be-dynamic-source-unknown).
- Sample-and-classify the 122 `DATA.other-json` files (currently unclassified) and the 875 `GOVERNANCE.autonomous` files.
- Investigate chunk-010 currency (PATHOLOGY-06).
- Investigate DataCite snapshot workflow (PATHOLOGY-04).

**Session 3 (cross-repo relation graph).**
- Full producer-consumer graph across all seven repos and their scripts.
- Investigate MMRS content shards (PATHOLOGY-02), data-rhizome consumer relation (PATHOLOGY-09), fleet registry mirror status (PATHOLOGY-10).
- Machine-readable output at `api/dataflow-graph.json`.

**Session 4 (finalize and hand off).**
- Publish `data/specs/AXN-DATAFLOW-MAP-v1.0.md` (this document's supersessor).
- Mermaid visual dependency diagram.
- `data/workplan/DATAFLOW-REMEDIATION-QUEUE.md` prioritizing pathologies for downstream workstreams.

## §8. Reviewer's prompt

*You are asked to review this atlas at four levels:*

1. **Does the taxonomy (§3) partition the archive's data honestly?** Are the fifteen classes the right axes? Is any class hiding a distinction, or forcing an unhelpful merger? Is anything missing that a scholarly-archive data layer would require?

2. **Is the deposit-flow model (§2) load-bearing?** Are the eleven stages the right stages? Is MANDATORY / CONDITIONAL / OPTIONAL POST-MINT the right classification? Are there conditions on the CONDITIONAL artifacts that this atlas does not name and should?

3. **Is the fossilized-state pathology (§4) framed correctly?** Is the three-way remediation partition right? Is the diagnosis (that the fleet self-describes stale-integers-across-the-network) correct in mechanism, or is there a design purpose to authoring-moment freezes that this atlas mistakes for a defect?

4. **Are the pathology register (§6) and Session-3 questions (§5) well-posed?** Are the severities right? Is any pathology conspicuously missing? Are the Session-3 questions the load-bearing questions to answer next?

Structural feedback is what this review invites. Empirical inspection of the archive's contents is not required; the atlas states its own confidence levels, and where it is uncertain, it names the Session at which uncertainty will be resolved.

## §9. Provenance

Raw outputs at `data/audit/`:
- `rhizome-inventory-raw.json` — every file catalogued.
- `displayed-values-inventory-session1.json` — 1,494 hits.
- `script-dependencies.json` and `script-dependency-graph.json` — script-level producer/consumer graph, partial.

Session 1 walked the seven repos on 2026-07-18 evening (local time Detroit). The reconnaissance was conducted from within a TACHYON session under the direction of Lee Sharks (MANUS). The atlas was drafted immediately following the walk and reviewed against the raw outputs for consistency.

Purpose-inference for functional classification is regex-based on path signatures. Where a file's role is not matched by any signature, it is tagged `DATA.other-json` or `OTHER` — approximately 140 files await Session 2 classification.

The script dependency graph is partial: it detects literal string paths but does not follow paths constructed via variable interpolation or template expansion. Session 3 augments the graph with careful script-tracing of the largest producers.

---

*End of atlas v0.1 (Assembly-review edition). Session 1 of 4 complete. Sessions 2–4 follow after MANUS review and Assembly feedback are received.*
