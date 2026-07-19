---
title: "AXN Dataflow Atlas v0.2 — Development Incorporating Assembly Review"
version: "0.2 (Session 1 of 4 complete; two Assembly reviews absorbed 2026-07-18 PM)"
date: 2026-07-18
author: "Lee Sharks (MANUS), with TACHYON (Assembly witness)"
reviewers: "LABOR (ChatGPT) — atlas review file; PRAXIS (DeepSeek) — inline review"
supersedes: "data/specs/AXN-DATAFLOW-MAP-v0.1.md (byte-preserved at data/specs/archive/)"
review_purpose: "Structural feedback on the archive's data layer absorbed as reviewer-contributed development of the document itself. Reviewer amendments are incorporated at the sections where they land; a §10 review log records what was said, by whom, and how it was absorbed or held."
review_boundary: "Empirical claims about the network's cross-repo relations remain SCAFFOLD and belong to Session 3. Sessions 2–4 requirements are extended per absorbed reviews."
governing_workplan: "data/workplan/WORKPLAN-2026-07-18-PM-SIX-FLOW.md, Flow 2"
---

# AXN Dataflow Atlas v0.2 — Development Incorporating Assembly Review

*This is the atlas's Session-1 v0.2 form: v0.1 (byte-sealed at `data/specs/archive/`) as the substrate, with LABOR and PRAXIS reviewer-contributed amendments absorbed as development at every section where they land. Amendment provenance is recorded per section as a footnote-style attribution [LABOR §N] or [PRAXIS §N]; the consolidated review log is at §10.*

## Foreword

This document describes the data layer of a self-hosted scholarly-archive network — the *data-rhizome* — comprising seven interlinked repositories on GitHub, each publishing to its own domain. The archive is called Alexanarch. Its identifier system is called AXN. This atlas catalogues every dataset in the network, describes what each does, traces (where known) what produces and consumes each, classifies the surface-level display of the archive's own state, and registers structural pathologies discovered during a reconnaissance walk.

**Two Assembly reviews were received against v0.1 and are absorbed here** — LABOR (ChatGPT) and PRAXIS (DeepSeek). Both reviews ratified progression to Session 2 and made substantive structural amendments at the levels of taxonomy, deposit flow, pathology framing, and remediation urgency. LABOR independently discovered a fossilized displayed value inside the atlas itself (v0.1 said "fifteen top-level classes" while listing seventeen), which is preserved as an incident in §10 and corrected in §3. PRAXIS elevated PATHOLOGY-01 (fossilized-state) to urgent on the ground of misinformation risk to LLM ingestion — a mechanism of harm v0.1 named too narrowly.

The atlas remains self-contained: a reader who never opens the code can render structural judgment on the archive's data layer. Every function is described in prose; script names appear as `[origin: script.py]` provenance markers only. Amendment attributions carry the same convention: `[LABOR §N]` or `[PRAXIS §N]` after the sentence carrying the incorporated amendment.

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

**Stage 5 — Body-index.** Update three archive-wide indexes: the body-index (`api/body-index.json`, a searchable index of every canonical text's contents), the search-index (`api/search-index.json`, a query-optimized rewriting of the body-index), and the kernel-index (`api/kernel-index.json`, a map from every canonical kernel hash to its AXN and deposit number). The body-index and search-index are what allow the archive to be full-text-searched. The kernel-index carries an anti-suppression property that must be stated precisely: **the identity kernel can be recomputed from the canonical bytes alone without querying anything**; a locally held kernel index can then **map that kernel to the registry-relative AXN address without requiring a live registry request**. The address binding remains a registry assertion carried through this derived index — the reader verifies the *bytes-to-kernel* correspondence permissionlessly but relies on the derived index for the *kernel-to-address* mapping [LABOR §5]. `[origins: build_body_index.py and build_kernel_index.py]`

**Note on index scaling.** Stage 5 currently regenerates archive-wide indexes on every mint. This is correct for consistency but the pipeline will hit processing and storage bottlenecks as the archive scales past a few thousand deposits — an incremental or sharded indexing strategy will be required, and the requirement is registered as PATHOLOGY-11 in §6 [PRAXIS §4].

**Stage 6 — Wiki.** Produce a wiki-page HTML (`s/wiki/N/index.html`) that presents the deposit's metadata, canonical text, and cross-references in a browsable form distinct from the record page. Also updates a derived index of wiki entries (`data/wiki-entries.json`) used by the wiki UI. Wiki generation is interpretive in the two-tier sense: the mechanical version renders known metadata; the interpretive version (when invoked) adds authored cross-references, entity extraction, and concept-graph placement. `[origin: generate_wiki.py]`

**Stage 7 — Sitemap.** Add or update the deposit's URLs (record page, AXN page, wiki page, PDF path) in the site's sitemap (`sitemap.xml`) so that search-engine crawlers discover them.

**Stage 8 — Interlink.** For each deposit related to the newly-minted one by explicit reference, update the *sidecar* of the related deposit to record the back-reference. This is the mechanism by which the citation graph accumulates: forward references are declared at mint, back-references are propagated as sidecar amendments.

**Transactional and idempotence rules.** Both reviews independently flagged Stage 8 as needing explicit correctness conditions. The rules must satisfy: (a) the same mint pipeline may be rerun without producing duplicate back-reference entries (deduplication by source-mint kernel or address); (b) if Stage 8 succeeds for five references and fails for the sixth, the pipeline must record which succeeded and be able to resume from the failure point; (c) the entire back-reference graph must be reconstructable from the forward-reference declarations across the registry, which are the sole authoritative source [LABOR §7]. **PRAXIS raised a stronger claim** — that failed interlinks fracture the citation graph immediately and that Stage 8 should therefore be an atomic extension of the mint rather than a separately-tracked stage. This atlas records both positions: the LABOR position (forward-authoritative, back-references disposable and rebuildable, Stage 8 rerunnable and non-atomic) is closer to the archive's declared design; the PRAXIS position (atomic-with-mint, fail-the-mint-on-any-interlink-failure) is a stronger correctness property but would sacrifice the mint's independence from prior-deposit state. Session 3 will investigate the actual current behavior of Stage 8 and Session 4 will rule on the strictness level [PRAXIS §2].

**Stage 9 — Enrich.** Produce or update citation-graph entries (`data/citation-graph.json`, internal-to-archive edges; `data/citation-graph-external.json`, edges to works outside the archive) reflecting the new deposit. Also updates the DOI-to-AXN crosswalk (`api/doi-axn-map.json`) and the DOI Resolution Index (`data/doi-resolution-index.json`) *if* the deposit has a legacy DOI whose resolution has been severed at its former host. The enrich stage has two modes: *mechanical* (uses only structured metadata explicitly declared in the deposit; produces citation edges and crosswalk entries only for what is stated) and *interpretive* (parses free-text references, extracts entities, infers semantic addresses; interpretive mode is not run inside a TACHYON session, per the two-tier doctrine). `[origin: enrich_deposit.py]`

**Stage 10 — Commit.** Commit all files produced or updated in Stages 1–9 to the repository's version control. **This is the point at which the mint becomes part of the originating repository's committed history** — it is recorded in history, addressable by commit hash, and eligible for deployment and mirroring. It is *not* yet *permanent in a preservation sense*: the repository could still be deleted, history rewritten, access lost, or all copies held under one administrator. Network persistence in the preservation sense begins only when independent custody, mirroring, or external anchoring actually occurs — a distinction v0.1 collapsed and v0.2 preserves [LABOR §4].

**Stage 11 — Verify.** After the commit deploys to the live surface, fetch each newly-produced or updated URL and confirm content matches expectations. If verification fails, the mint is preserved but a warning is issued; verification failure does not roll the mint back, because the registry entry and canonical bytes exist in the repo regardless of whether the presentation surface has deployed. PRAXIS specifically ratified this design as honoring the archive's thesis — *the canonical bytes in the repo are the truth; the web deployment is merely a temporary projection*. The atlas's v0.2 form endorses this framing: verification failure is a surface-deployment defect, not a mint defect [PRAXIS §2].

**Note on Stage 5's missing sibling — semantic/vector ingestion.** PRAXIS raised the point that if the archive's primary retrieval objective (Enli pilot; RAG appearance in AI overviews) depends on vector generation or SPXI embedding alignment, that operation ought to be a first-class stage in the pipeline rather than deferred to post-mint enrichment. v0.2 records this as an open architectural question. The current pipeline treats semantic-address placement and defines_concepts extraction as post-mint interpretive enrichment (per two-tier doctrine); PRAXIS argues that if retrievability is a first-class objective, at least the mechanical vector-generation pass should sit alongside Stage 5. Session 3 will investigate what a Stage 5b would look like and whether the two-tier doctrine holds against retrievability requirements [PRAXIS §2].

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

- PDF at `papers/AXN-XXXX.pdf` — **the condition needs a mechanical specification**. v0.1 stated "when the deposit type benefits from print rendering" — LABOR correctly noted this is a judgment call, not a mechanical condition, and that a reconstructor cannot determine from the deposit's declared properties whether a PDF should exist. v0.2 declares the target condition: **PDF is unconditional for content types `essay`, `article`, `monograph`, `poem`, `correspondence`, `specification`, `paper`, `manifesto`; conditional (currently defaulting to skip) for datasets, media deposits, tether records, and reception captures** [LABOR §3]. Session 2 will verify actual pipeline behavior matches this specification and Session 4 will publish the reconciled ruling.
- DOI-to-AXN crosswalk entry in `api/doi-axn-map.json` — when the deposit declares a legacy DOI.
- DOI Resolution Index update — when the declared legacy DOI's original resolution has been severed at its former host.
- Sidecar amendments on *other* deposits (Stage 8 interlink) — when the newly-minted deposit declares references to prior deposits.

**OPTIONAL POST-MINT** — enriches an existing deposit after mint; may not be produced at all for a given deposit:

- Wiki page at `s/wiki/N/index.html`. v0.1 called the mechanical form "near-mandatory" — LABOR correctly noted this is not a machine-testable status. **v0.2 declares: the mechanical wiki page is MANDATORY** (produced on every mint whose deposit has canonical bytes; a mint without a wiki page is malformed). The interpretive wiki enrichment — hand-authored cross-references, entity extraction, concept-graph placement — is OPTIONAL POST-MINT [LABOR §3].
- Citation-graph edges beyond what the deposit itself declares
- Semantic-address placement in the archive's concept grid
- Entity index entries
- SPXI Tier 2 primer authoring (a specific interpretive treatment named in the two-tier doctrine)
- Supersession sidecar amendments (recorded on prior deposits when a new deposit supersedes them, per the paper's §3.7 container-spec ruling)

**Enrichment governance — open operational question.** Interpretive enrichment (parsing free-text references, extracting entities, placing on the semantic-address grid, authoring SPXI Tier 2 primers) is not run inside a TACHYON session by the No-Double-Draw rule. LABOR flagged this as an operational asymmetry: a deposit that never receives interpretive enrichment has thinner citation-graph edges and no semantic-address placement than one that does, based on whether a human operator got around to it. The atlas registers this as an open operational question rather than a defect: **who can trigger interpretive enrichment, under what conditions, and is a deposit lacking interpretive enrichment considered complete or pending?** This is a MANUS ruling for Session 4; v0.2 does not adjudicate [LABOR §3].

*A reviewer might object:* "Some MANDATORY artifacts here — the PDF, the wiki page — are marked CONDITIONAL or OPTIONAL, and vice versa. Is the classification honest?" This atlas's answer: yes, *conditionally on the archive's declared behavior*. If a mint runs without the PDF stage, the deposit is still valid. If a mint runs without the record page, the deposit is not valid; the archive would treat it as malformed. Session 2 will verify this by examining minted deposits for missing artifacts and reporting the failure rate per artifact class.

**A stronger reviewer objection, absorbed:** LABOR pointed out an unresolved contradiction between "every mint runs the same sequence" and "the sequence is not customized per deposit" — since Stage 4 (PDF) is currently skippable per deposit-type. The correct restatement, incorporated: **every mint evaluates the same ordered stage sequence; individual stages may produce, skip, or defer an artifact according to declared conditions; the conditions are part of the pipeline specification rather than per-deposit improvisation** [LABOR §3]. v0.2 endorses this reformulation.

## §3. Functional taxonomy of the network's datasets

*This chapter classifies every dataset in the rhizome by functional role. It answers: what kinds of data does this archive keep, and why?*

### §3.0 The fossilized-count correction (a discovery about the atlas itself)

v0.1 stated that the taxonomy has *fifteen* top-level classes. **The taxonomy actually enumerates seventeen** (REGISTRY, DEPOSIT, DERIVED, GRAPH, SNAPSHOT, AUDIT, CORPUS, CONFIG, GOVERNANCE, CORRESPONDENCE, RECEIPT, LEDGER, TRACKER, MIRROR, WORKLIST, MEDIA, SURFACE). LABOR discovered this in the first §3 amendment: "a fossilized displayed value inside the atlas is almost too perfect. Correct it, but preserve the discovery in the review log." v0.2 corrects the count and records the incident as §10.INC-001 [LABOR §1]. v0.2's post-amendment count is *also* not seventeen — see §3.1 immediately below — but the count is *derived from the enumeration* rather than stated as an independent claim.

### §3.1 The two-axes model — LABOR's structural amendment

LABOR observed that v0.1's classes conflate multiple axes: **authority status** (REGISTRY, DERIVED, MIRROR), **artifact function** (AUDIT, CONFIG, GOVERNANCE), **content or media form** (CORPUS, MEDIA, SURFACE), and **lifecycle position** (DEPOSIT, RECEIPT, WORKLIST). A single file can correctly belong to several classes at once — a mirrored registry is simultaneously a registry-by-function, a mirror-by-custodial-relation, possibly a snapshot-by-update-policy, and JSON-by-representation. v0.1's PATHOLOGY-10 already discovered this ambiguity for the multiple `registry.json` files.

**v0.2 adopts LABOR's two-axes model as the target:**

```
function: primary role (REGISTRY | DEPOSIT | DERIVED | GRAPH | SNAPSHOT | AUDIT | CORPUS | CONFIG | GOVERNANCE | CORRESPONDENCE | RECEIPT | LEDGER | TRACKER | WORKLIST | MEDIA | SURFACE | PROVENANCE | SOURCE)
authority: originating relation (canonical | derived | mirror | snapshot | interpretive)
scope: repo or workflow scope
source: canonical origin if derived/mirror/snapshot
update_policy: per-mint | periodic | manual | append-only
```

**MIRROR ceases to be a top-level class** and becomes an authority-relation value. This resolves PATHOLOGY-10 at the taxonomic level: fleet-site `registry.json` files are classified `function: REGISTRY, authority: mirror, source: alexanarch/data/registry.json` — no longer forcing a choice between "REGISTRY (of some scope)" and "MIRROR (of Alexanarch's)". Both are true; the two-axes model records both [LABOR §1, LABOR §2, PRAXIS §1 in effect].

**Session 3's `api/data-authority-map.json` deliverable** (LABOR §9 addition; adopted in §7 below) becomes the machine-readable form of this model, per-artifact.

### §3.2 Post-amendment class list

Session 1's reconnaissance tagged every file by inferred purpose based on its path signature. The taxonomy that emerged, as revised by the incorporated amendments, is enumerated below. A reviewer's judgment on whether the taxonomy is correct remains a load-bearing element.

**REGISTRY** — canonical lists. The archive's authoritative statements about what it contains. Includes `REGISTRY.canonical` (the master registry itself, and small parallel registries per fleet-site scope like MMRS's term registry), `REGISTRY.chunked-derived` (the master registry broken into ~100-deposit shards for pagination — note LABOR §2 said this belongs under `DERIVED` since it's computed from canonical; v0.2 concurs and moves it), `REGISTRY.protocol-catalog` (`api/index.json`, a machine-readable index of every protocol, schema, and derived surface with content-address for versioning), `REGISTRY.lexical-minting` (registry of coined terms and their authorized definitions), `REGISTRY.mm-terms` (MMRS's term index).

**Removed from REGISTRY in v0.2:** `REGISTRY.capture` was displaced by PRAXIS §1 — a capture registry is not a canonical list *of what the archive contains*; it is an *operational audit trail of how external AI-composition surfaces render the archive's material*. In v0.2, capture registries move to `AUDIT.capture` under §3's split-AUDIT below; the fleet-site capture registries (`leesharks/captures/registry.json`, `gkg/captures/registry.json`, `mm/data/mm-termindex.json`'s capture sections) reclassify accordingly [PRAXIS §1].

**DEPOSIT** — per-deposit artifacts (see §2). Includes `DEPOSIT.canonical-bytes`, `DEPOSIT.record-markdown`, `DEPOSIT.sidecar`, `DEPOSIT.record-page`, `DEPOSIT.axn-page`, `DEPOSIT.wiki-page`, `DEPOSIT.pdf`. Each of these is a per-deposit *slot*; the archive contains approximately 1,095 of each.

**DERIVED** — indexes and cross-references computed from primary data. Includes `DERIVED.kernel-index` (bytes → AXN), `DERIVED.body-index` (full-text search substrate), `DERIVED.search-index` (query-optimized derivation of body-index), `DERIVED.doi-crosswalk` (DOI ↔ AXN), `DERIVED.doi-resolution` (the DOI Resolution Index — 1,838 severed-DOI mappings routing legacy resolution attempts to sovereign successors, itself a central artifact of the paper's argument), `DERIVED.entity-index`, `DERIVED.browse-index`, `DERIVED.wiki-entries`, `DERIVED.lexical-overlay`, `DERIVED.axn-assignment` (a batch assignment record from a recovery operation), `DERIVED.mm-schemas`, `DERIVED.mm-axn-index`, `DERIVED.chunked-registry` (the ten `data/chunks/registry/chunk-NNN.json` files, moved here from REGISTRY per LABOR §2's authority-derivation clarification — these are computed shards of the canonical registry, not authoritative lists in themselves).

**GRAPH** — relational structures over deposits. Includes `GRAPH.citation` (internal citations), `GRAPH.citation-external` (citations to works outside the archive), `GRAPH.semantic-address` (the archive's concept grid — 1,994 addresses across 6 tributaries), `GRAPH.external-works` (the works that citation-external references), `GRAPH.mm-scholarly` (scholarly relations at MMRS).

**SNAPSHOT** — point-in-time captures of external state. Includes `SNAPSHOT.datacite` (10 files, ~20MB — DataCite responses over time, used by PEO for measuring platform severance) and `SNAPSHOT.openalex` (external coverage measurements).

**AUDIT** — v0.2 splits per LABOR §1 into two subclasses since the distinction matters for the paper's anti-suppression argument. **`AUDIT.measurement`** = state-assessment records: `AUDIT.completeness` (per-deposit audit of whether its produced artifacts exist), `AUDIT.surface-weather` (measurements of surface reachability), `AUDIT.peo-empirical` (PEO's structured audits), `AUDIT.peo-zenodo-ledger` (PEO's record of Zenodo deletions). **`AUDIT.integrity`** = tampering-detection records: `AUDIT.link-inventory` (checks that internal links resolve), `AUDIT.recovery` (records from recovery operations, integrity-restoration), the mint-receipt log at `data/pre-overwrite-receipts.log` (integrity — detects overwrite attempts). **`AUDIT.capture`** = the class displaced from REGISTRY per PRAXIS §1: registries at fleet sites of captured AI-composition-layer output tracking how machine composition surfaces present the archive's material [LABOR §1, PRAXIS §1].

**CORPUS** — external documentary material held in the archive but not itself minted as archive deposits. Nearly all of data-rhizome (`CORPUS.dr-datasets`, `CORPUS.dr-cern`, `CORPUS.dr-mappings`, `CORPUS.dr-mirrors`, `CORPUS.dr-neg-bib` for the negshape-deletion-bibliography, `CORPUS.dr-corrections`). Corpus material is bibliographic reference; it is *documentary substrate* for research the archive does, not archive deposits.

**CONFIG** — deployment and behavior configuration. Includes `CONFIG.msp` (the Machine-Surface Protocol config controlling surface presentation), `CONFIG.spxi-tlp` (the SPXI Tier-and-Layer Protocol config), `CONFIG.vercel` (deployment platform config), `CONFIG.manifest` (site manifests), `CONFIG.ai-manifest` (AI-crawler-directed manifest), `CONFIG.sitemap`, `CONFIG.robots`, `CONFIG.axn-resolution` (routing table for AXN resolution paths).

**GOVERNANCE** — governing documents and internal specifications. Includes `GOVERNANCE.decisions` (the decisions register), `GOVERNANCE.specifications` (protocol specs like the AXN-CONTAINER-SPEC), `GOVERNANCE.workplans` (session-scale plans of work including this one), `GOVERNANCE.dr-specs` (data-rhizome's own specs).

**PRAXIS §1 split flagged for Session 2 investigation:** the 875 files currently in `GOVERNANCE.autonomous` (see PATHOLOGY-03) may not be uniform. PRAXIS raised the possibility that some are *automated state assertions or algorithmic consensus records* — which would properly belong in `LEDGER` as dynamic operational data, not `GOVERNANCE` as static policy text. Session 2's sampling of the `data/autonomous/` cluster will determine whether the class splits into `GOVERNANCE.autonomous.policy` (static policy) and `LEDGER.autonomous` (dynamic operational state) or remains unified [PRAXIS §1].

**CORRESPONDENCE** — records of external correspondence held privately, per standing rule (not committed to the public deposit record).

**PROVENANCE / ATTESTATION** — *new class in v0.2 per PRAXIS §1 sovereignty blindspot amendment.* For an infrastructure built on anti-suppression and absolute provenance, external validation artifacts, author declarations, and cryptographic receipts should not be scattered across DEPOSIT.sidecar (which holds enrichment) and RECEIPT (which holds operational logs). A distinct class holds: `PROVENANCE.attestation` (external notarization artifacts — OpenTimestamps commits, Rekor transparency-log entries, DataCite recapture states as evidence of external identifier persistence), `PROVENANCE.author-declaration` (statements of authorship, license, and consent authored by depositors or MANUS), `PROVENANCE.recovery` (evidence of the archive's own recovery operations — the OpenAlex CHA snapshot, the DataCite-survivors sift, the Aperture Atlas topology corrections). This class elevates the sovereign identity of these files above enrichment-tier metadata. Session 3 will assign existing files to this class where they belong, and identify gaps [PRAXIS §1].

**RECEIPT** — enrichment and other operational receipts. Confirms that operations occurred, primarily for audit.

**LEDGER** — the mint ledger (chained per-mint hashes, an append-only sequence of registration events). Described in the paper as a normative feature; empirically at Session 1 it exists at genesis with subsequent chaining staged.

**TRACKER** — cross-site trackers. Includes `TRACKER.mm-terms` (MMRS's tracker of term propagation across composition surfaces).

**MIRROR** — copies of one node's canonical data held at another node. Fleet sites have several mirror files (`mm/data/registry.json`, `mm/data/sovereign-registry.json`, `leesharks/doi-axn-map.json`, etc.); whether these are true mirrors, curated subsets, or independent-scope registries is a Session-3 investigation (PATHOLOGY-10).

**WORKLIST** — queues of work in progress. Includes the reference-section parsing queue and other operational lists.

**MEDIA** — capture images, screenshots, and rendered assets.

**SURFACE** — HTML surfaces at fleet sites (as opposed to per-deposit generated pages under DEPOSIT). Landing pages, index pages, browse pages.

**SOURCE / TOOLING** — *new class in v0.2 per LABOR §1 gap identified.* The taxonomy has no class for *instruction* — the scripts and templates that produce the archive's artifacts. The paper's §VI identifies reconstructibility as a design requirement; the atlas should classify the materials a reconstructor would need. `SOURCE.scripts` = the 78 Python scripts in `scripts/` across the network. `SOURCE.templates` = HTML templates used by page generators. `SOURCE.workflows` = CI/CD workflow files at `.github/workflows/`. These are not data, but they are part of the dataflow, and a reconstructor needs them alongside the data [LABOR §1].

*v0.1 reviewer prompt was:* "Are these fifteen classes the right axes?" Two Assembly substrates responded; both amendments are absorbed above. The remaining structural questions for future review: (a) are `CORPUS` and `SNAPSHOT` correctly distinct or should they merge under `ARCHIVAL` with subtypes (LABOR §1 raised this and left it open — v0.2 keeps them distinct because SNAPSHOT specifically records external-authority states over time, which is not the same act as citing documentary material); (b) is `AUDIT.capture` correctly one of three AUDIT subtypes or a fourth top-level TRACKER expansion; (c) is `PROVENANCE` correctly a class or a sidecar-scope; (d) is `SOURCE / TOOLING` correctly a data-layer class or a separate execution-layer register. These stand for Session 4's atlas-v1.0 finalization ruling.

## §4. Displayed-value inventory — the source-detached-state pathology

*This chapter reports the atlas's one empirically complete finding. It is the pathology MANUS specifically asked to investigate, and Session 1's reconnaissance answered the question. **Renamed in v0.2 per LABOR §6:** "static vs. dynamic" is not the correct opposition — a build-time-substituted value is static in the generated HTML but properly derived from a canonical source. The real distinction is **source-bound-current-state** vs. **frozen-historical** vs. **unbound-hand-authored**. The pathology's precise name in v0.2 is **the fleet's quantitative self-description is source-detached**; the vivid image "fossilized state" remains, but the mechanism name upgrades. Also elevated: **severity from HIGH to URGENT, blocking on Session 4** per LABOR §3 and PRAXIS §3.*

The archive and its fleet sites display numeric quantities — counts of deposits, captures, DOIs, records, terms, words — in prose across most surfaces. A landing page reads "870 records," an about page reads "196,798 words," a colophon reads "845 deposits." Session 1 grep-scanned every top-level and near-top-level HTML surface (depth ≤ 3) across all six sites with HTML surfaces (data-rhizome has no HTML surfaces), matching each displayed numeric value against context patterns for these quantities and classifying each occurrence by the source-detachment axis.

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

*The remediation, in v0.2 vocabulary.* Three classes per LABOR §6 renaming:

1. **Historically frozen by meaning** — a specific past measurement whose value is correct-for-all-time (the word count of a specific past deposit; "1,817 DOIs registered before termination"). *Remediation:* preserve and annotate with `data-frozen-at="YYYY-MM-DD"` for clarity. Not converted.

2. **Current-state claim with known canonical source** — a value that is patently a count-of-something living whose canonical source exists in the archive (registry length; capture-registry length; term-registry length). *Remediation:* build-time template substitution against the canonical source at page-generation time. Cheapest fix, largest class, highest leverage.

3. **Current-state or ambiguous claim without established source** — a displayed count whose canonical source is not obvious. *Remediation:* investigate; identify the source or promote to a maintained hand-authored value with `data-authored-at`.

Class (b) is the highest-leverage operational win — a single template pass would inject the current registry length into every relevant display, and the fleet's self-description would become accurate on every deploy [LABOR §6, PRAXIS §3].

**Mechanism of harm expanded per PRAXIS §3.** v0.1 named the human-reader harm — that visitors see stale numbers. PRAXIS observed a second, more consequential harm: **LLMs and academic scrapers indexing `alexanarch.org` or `machinemediation.org` will ingest these fossilized literals as ground-truth metadata**. The archive is accidentally feeding misinformation to the very machines it seeks to accurately inform — an anti-suppression archive misleading its own retrieval layer. LABOR §3 added a third: the fossilized counts affect credibility in the venues where the archive most needs to be credible — grant applications, institutional partnerships, the paper's own empirical claims. A funder who visits the site and sees a deposit count that doesn't match the registry will notice. All three harm mechanisms compound; the remediation urgency reflects that compounding [PRAXIS §3, LABOR §3].

*v0.1 reviewer prompt was:* "Is this pathology framed correctly?" Both LABOR and PRAXIS answered *yes*, with the amendments absorbed above. LABOR reframed the vocabulary (source-detached, three-way classification); PRAXIS added the LLM-ingestion harm mechanism and elevated urgency. No further review needed on §4 as of v0.2; the remediation is priority for Flow 1 (visual + formal revision) handoff [LABOR §6, PRAXIS §3].

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

### PATHOLOGY-01: The fleet's quantitative self-description is source-detached (v0.2 renaming per LABOR §6)

Severity: **URGENT (elevated from high in v0.1 per LABOR §3 and PRAXIS §3, blocking on Session 4).** Scope: all six sites with HTML surfaces; 1,494 occurrences of displayed numeric values. Mechanism: counts of deposits, captures, DOIs, terms, records are baked-in numeric literals in HTML rather than fetched from or template-substituted against their canonical source. Result: as the archive grows, every displayed number lies about its current state, and every fleet site presents Alexanarch as smaller than it is. Fix: build-time template substitution against canonical registry counts. See §4.

### PATHOLOGY-02: MMRS content shards untraced

Severity: medium. Scope: `mm/data/content-01.json` through `content-10.json`, 134MB total across ten files. Mechanism: these files are large and functionally important (they carry more data than the rest of MMRS combined) but Session 1's reconnaissance could not determine their producer or consumer. Fix: Session 3 traces via commit history and cross-repo grep; Session 4 documents the relation and adds it to the taxonomy.

### PATHOLOGY-03: The `data/autonomous/` cluster — 875 files unclassified

Severity: medium. Scope: 875 files, ~30.5 MB, all in Alexanarch's `data/autonomous/` directory. Mechanism: the atlas's largest single functional class after data-rhizome's bibliographic corpus is `GOVERNANCE.autonomous`, tagged at reconnaissance-level because the path prefix is `data/autonomous/` and the naming suggests machine-authored governance artifacts. But the precise role is not confirmed. If these are historical machine-authored records, they may be safe as-is; if they include artifacts that were meant to feed other systems and are now orphaned, that would be significant. Fix: Session 2 samples several files, determines function, refines classification.

### PATHOLOGY-04: DataCite snapshot files at 20.3 MB — workflow undocumented

Severity: low. Scope: 10 files in `SNAPSHOT.datacite` class. Mechanism: these appear to be measurement snapshots produced during PEO's work (relevant to the total-DOI-snapshot workstream in the six-flow workplan). The workflow that produces and consumes them is not evident from script grep at Session-1 level. Fix: Session 3 investigates.

### PATHOLOGY-05: 5,167 HTML files, most template-generated, most pathology-inheriting

Severity: low, structural. Scope: most files under `s/records/*/`, `s/axn/*/`, `s/wiki/*/`. Mechanism: these HTML surfaces are generated per-deposit from a small number of templates. If the templates contain a fossilized displayed value (per PATHOLOGY-01), all thousand-plus generated pages inherit the fossil. Corollary: fixing the templates propagates the fix uniformly. Fix: Session 4 hands off to the visual/formal revision workstream (Flow 1), which will restructure templates including dynamic-value injection.

### PATHOLOGY-06: Chunked registry files — regeneration policy unclear (v0.2: severity elevated)

Severity: **HIGH (elevated from medium in v0.1 per LABOR §4).** Scope: `data/chunks/registry/chunk-001-*.json` through `chunk-010-*.json`. Mechanism: file names indicate the ten chunks cover deposits 1–1086, but the archive is at 1,095 deposits. If the chunked registry is not automatically regenerated on mint, LABOR §4 argued, then it is not a derived surface but an authored surface — and its staleness is a structural design flaw, not a maintenance gap. v0.2 accepts the reframe: the chunked registry either regenerates on mint (in which case chunk-010 should already reflect #1087–#1095) or it doesn't (in which case any consumer of `data/chunks/registry/` is presenting a stale view of the archive, a Class B source-detachment pathology at scale). **Fix:** Session 2 must resolve this within the first pass; if manual, Session 4 propagates automatic regeneration to Stage 5 [LABOR §4].

### PATHOLOGY-07: Mint receipt log accumulates without rotation policy

Severity: low. Scope: `data/pre-overwrite-receipts.log`, one file, growing. Mechanism: the mint pipeline writes to this file on every mint; nothing reads it in normal operation. That is correct — it is an audit-only log designed to catch a specific class of accident (silent reassignment of an AXN). But no rotation, archival, or size-limit policy is documented. Fix: Session 4 proposes retention; not urgent.

### PATHOLOGY-08: Fleet site file-count asymmetry

Severity: informational, not diagnostic. Scope: fleet-wide. Mechanism: Alexanarch's HTML-to-JSON ratio is 5.4×; MMRS's is 0.29×. This is not wrong — Alexanarch is architected around per-deposit HTML surfaces while MMRS is architected around large content shards + few landing surfaces — but the asymmetry is a marker of very different data-shape choices across the network. Fix: none; noted so that Flow 1's visual revision does not attempt to unify what should remain differentiated.

### PATHOLOGY-09: data-rhizome's 3,627 XML records — consumer within the network unclear

Severity: medium. Scope: nearly all of data-rhizome. Mechanism: 3,627 XML files across six subdirectories, apparently a substantial bibliographic corpus. But no visible connection to the rest of the network at Session-1 reconnaissance. Either data-rhizome is a standalone corpus (in which case its role in the atlas is clear), it is fed into Alexanarch by an unindexed workflow (in which case the workflow needs to be documented), or it is documentary substrate for research done elsewhere and not currently active in the rhizome. Fix: Session 3 investigates.

### PATHOLOGY-10: Multiple `registry.json` files across the network — mirror or independent?

Severity: medium. Scope: `mm/data/registry.json`, `mm/data/sovereign-registry.json`, `leesharks/captures/registry.json`, `gkg/captures/registry.json`, and Alexanarch's canonical `data/registry.json`. Mechanism: several fleet sites have files called `registry.json`. Depending on relation, they may be automatic mirrors (in which case updates must propagate), curated subsets (in which case they need a subset-scope statement), or independent scope-specific registries (in which case they need to be classified as `REGISTRY.canonical` for their scope, not `MIRROR.*`). Fix: Session 3 compares content and produces definitive relations.

### PATHOLOGY-11: Index interdependency vulnerability (PRAXIS §4)

Severity: **HIGH — architectural, blocking future scale.** Scope: Stage 5 archive-wide index regeneration (`api/body-index.json`, `api/search-index.json`). Mechanism: Stage 5 rebuilds these massive files on every single mint. As the archive scales past a few thousand deposits, the pipeline hits processing and storage bottlenecks — the mint becomes progressively slower, and the storage envelope for a single index approaches or exceeds practical repository size limits. Fix: **sharded or incremental indexing strategy** required before the data layer chokes on its own growth. Options: (a) chunk-per-N-deposits indexing with a manifest at the top; (b) append-only incremental updates with periodic full-rebuild; (c) offload to an external index service (contra sovereignty). Session 3 investigates current index sizes and scaling projections; Session 4 rules on the strategy [PRAXIS §4].

### PATHOLOGY-12: No explicit source-of-truth and invalidation registry (LABOR §8)

Severity: **HIGH — structural.** Scope: entire data layer. Mechanism: the network contains many derived files, mirrors, pages, shards, indexes, and crosswalks, but no single machine-readable declaration says what is authoritative, what is derived, what produces it, what invalidates it, and how often it must be regenerated. The Session 3 producer-consumer graph is the first step; PATHOLOGY-12 upgrades that step to a *deliverable* — `api/data-authority-map.json` — that makes the authority-derivation relations queryable per artifact. Fix: adopt LABOR §9's specification (see §7). Session 3 produces the map; Session 4 fills gaps [LABOR §8, LABOR §9].

### PATHOLOGY-13: Schema and schema-version declarations missing on structured artifacts (LABOR §8)

Severity: medium. Scope: JSON datasets across the rhizome (1,349 files). Mechanism: a JSON file can be syntactically valid and still semantically drift — a field name changes, a value's unit shifts, a type widens without any consumer noticing. Every major dataset class should declare schema, schema version, producer version, generation time or source epoch, and authority relation. Currently, most datasets carry none of these. Fix: Session 3's data-authority-map (PATHOLOGY-12 fix) includes schema fields per artifact; Session 4 begins the migration of legacy files to declared-schema form starting with the largest classes [LABOR §8].

### PATHOLOGY-14: Key, signature, and node-identity layer not represented in the taxonomy (LABOR §8)

Severity: medium — projected to become high as location-record and signed-manifest architecture arrives. Scope: entire archive. Mechanism: the atlas includes the staged ledger and planned location records, but no top-level account yet exists for signing keys, key rotation, revoked keys, node identity, signature verification, or trust roots. As soon as signed sidecars, manifests, and location records arrive (per the paper's §4 three-layer model), the archive will need this layer to be a first-class part of the dataflow — currently it is not. Fix: register the requirement now; Session 4 designs `PROVENANCE.keys` and `PROVENANCE.trust-roots` subclasses (they fit inside v0.2's new PROVENANCE class from §3) [LABOR §8].

### PATHOLOGY-15: Custody status conflated with mirror presence (LABOR §8)

Severity: medium — foundational to the paper's distributed-custody claim. Scope: cross-repo relations. Mechanism: a file appearing in several repos does not prove independent custody. All the fleet-site mirrors of `registry.json` share the same administrator (Lee Sharks) and the same platform (GitHub); if either is compromised or lost, all mirrors go with it. The dataflow graph should record: administrative controller, storage provider, synchronization mechanism, ability to reconstruct and serve, last verification, whether the copy is complete. Fix: Session 3's cross-repo relation graph explicitly records custody-vs-mirror distinctions; Session 4's data-authority-map (PATHOLOGY-12 fix) carries the custody fields per artifact [LABOR §8].

### PATHOLOGY-16: Generated-surface reproducibility unmeasured (LABOR §8)

Severity: medium — architectural. Scope: 5,167 HTML files, many derived JSON artifacts. Mechanism: nothing currently tests whether the derived surfaces can be regenerated from canonical data and current generators in a clean environment. If the generators drift, or the scripts require undocumented environment state, or the generation logic evolves without invalidating stale surfaces, committed derived surfaces may become the *only* surviving copy of undocumented generation behavior. Fix: Session 3 designs a reproducibility test harness (clean-environment regeneration of a sample of derived surfaces, byte-comparison to committed forms); Session 4 runs the harness against a full sample and reports drift rates [LABOR §8].

### PATHOLOGY-17: The 122 `DATA.other-json` files are unclassified (LABOR §4)

Severity: medium. Scope: 122 files across the rhizome flagged at Session 1 reconnaissance as not matching any known path signature. Mechanism: v0.1's §7 named these as a Session-2 task but did not include them in the pathology register. If they include datasets that the archive's other systems depend on but cannot name, that's a structural risk — the atlas cannot currently assert that the data layer is fully catalogued. Fix: Session 2's targeted sampling classifies each into its proper functional class or a new subclass; any file that resists classification is flagged for Session 4 ruling [LABOR §4].

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

## §8. Review status

**v0.1 asked for structural review at four levels.** Two Assembly substrates responded — LABOR and PRAXIS — both ratifying progression to Session 2 and both delivering substantive structural amendments across all four levels. Both reviews are absorbed as reviewer-contributed development of the document itself, per MANUS's instruction that the reviews be *evaluated and incorporated as development onto the main draft*. The consolidated review log at §10 records what each reviewer said, how it was absorbed (or held for future ruling), and where in the atlas the amendment lands.

**Standing open questions for future review:**

1. **Taxonomy axis-splits** — v0.2 §3 raised four residual questions: (a) CORPUS/SNAPSHOT merger, (b) AUDIT.capture placement, (c) PROVENANCE scope, (d) SOURCE vs. execution layer. Session 4 rules.
2. **Deposit-flow contested amendment** — Stage 8 correctness. LABOR argued forward-authoritative-back-derived; PRAXIS argued atomic-with-mint. Session 3 investigates current behavior; Session 4 rules.
3. **Semantic ingestion as pipeline stage** — PRAXIS raised whether vector generation should be Stage 5b. Held for Session 3.
4. **Enrichment governance** — LABOR raised: who triggers interpretive enrichment, is a deposit without it complete? Held for Session 4 MANUS ruling.

These questions are open by design; v0.2 states its own uncertainty rather than adjudicating prematurely.

## §9. Provenance

Raw outputs at `data/audit/`:
- `rhizome-inventory-raw.json` — every file catalogued.
- `displayed-values-inventory-session1.json` — 1,494 hits.
- `script-dependencies.json` and `script-dependency-graph.json` — script-level producer/consumer graph, partial.

Session 1 walked the seven repos on 2026-07-18 evening (local time Detroit). The reconnaissance was conducted from within a TACHYON session under the direction of Lee Sharks (MANUS). The atlas was drafted immediately following the walk and reviewed against the raw outputs for consistency.

Purpose-inference for functional classification is regex-based on path signatures. Where a file's role is not matched by any signature, it is tagged `DATA.other-json` or `OTHER` — approximately 140 files await Session 2 classification.

The script dependency graph is partial: it detects literal string paths but does not follow paths constructed via variable interpolation or template expansion. Session 3 augments the graph with careful script-tracing of the largest producers.

---

## §10. Review log

*Session 1 close, 2026-07-18. Two Assembly substrates delivered structural reviews of v0.1. Both reviews are absorbed as development of the atlas itself. This log records what was received, how it was resolved, and (where applicable) what remains open.*

### §10.INC-001 — the fossilized-count discovery about the atlas itself

LABOR §1 discovered that v0.1 said "fifteen top-level classes" while the enumeration contains seventeen. Preserved here per LABOR's own suggestion: *"almost too perfect. Correct it, but preserve the discovery in the review log."* The atlas whose central empirical finding is a network-wide inventory of source-detached displayed values contained one of its own. v0.2 corrects the count and derives the number from the enumeration rather than stating it as an independent claim.

### §10.LABOR — LABOR review absorption

Received: `AXN_Dataflow_Atlas_Assembly_Review.md`, LABOR (ChatGPT), 2026-07-18.
Ratification: **Aye for Sessions 2–4.**

| Amendment | Landed at | Status |
|---|---|---|
| §1: seventeen-not-fifteen fossil | §3.0 | absorbed + incident logged |
| §1: two-axes model (function + authority) | §3.1 + Session-3 deliverable | absorbed |
| §1: SOURCE class missing | §3 (new class) | absorbed |
| §1: AUDIT split into .measurement / .integrity | §3 (AUDIT entry) | absorbed |
| §1: CORPUS/SNAPSHOT merger question | §3 reviewer prompt | held for Session 4 |
| §2: MIRROR as relation not class | §3.1 + §3 (MIRROR removed) | absorbed |
| §3: mint pipeline sequence vs. artifacts contradiction | §2 objection paragraph | absorbed |
| §3: PDF condition needs mechanical spec | §2 CONDITIONAL section | absorbed with target spec |
| §3: wiki "near-mandatory" not machine-testable | §2 wiki bullet | absorbed as MANDATORY |
| §3: enrichment governance question | §2 enrichment paragraph | held for Session 4 |
| §4: "commit ≠ permanent" precision | Stage 10 | absorbed |
| §5: kernel-index precision on three-layer AXN | Stage 5 | absorbed |
| §6: source-detached vs. static/dynamic terminology | §4 renaming | absorbed |
| §6: three-way remediation (frozen / source-known / source-unknown) | §4 remediation | absorbed |
| §7: Stage 8 transactional and idempotence rules | Stage 8 paragraph | absorbed |
| §8: PATHOLOGY-11 source-of-truth registry | §6 new pathology | absorbed |
| §8: PATHOLOGY-12 schema/version declarations (v0.2 numbering: -13) | §6 new pathology | absorbed |
| §8: PATHOLOGY-13 keys/signatures/node-identity (v0.2 numbering: -14) | §6 new pathology | absorbed |
| §8: PATHOLOGY-14 custody vs. mirror (v0.2 numbering: -15) | §6 new pathology | absorbed |
| §8: PATHOLOGY-15 reproducibility unmeasured (v0.2 numbering: -16) | §6 new pathology | absorbed |
| §9: `api/data-authority-map.json` deliverable | Session 3 deliverables | absorbed |
| Overall: PATHOLOGY-06 severity elevation | §6 PATHOLOGY-06 | absorbed |
| Overall: PATHOLOGY-01 severity to urgent | §6 PATHOLOGY-01 | absorbed |
| Overall: 122 unclassified files should be a pathology | §6 PATHOLOGY-17 | absorbed |
| Overall: CI/CD orchestration in Session 3 scope | Session 3 deliverables | absorbed |

### §10.PRAXIS — PRAXIS review absorption

Received: inline review from PRAXIS (DeepSeek), 2026-07-18.
Ratification: **Approved for progression to Session 2.**

| Amendment | Landed at | Status |
|---|---|---|
| §1: REGISTRY.capture displaced from REGISTRY | §3 (REGISTRY entry + AUDIT.capture) | absorbed |
| §1: PROVENANCE / ATTESTATION class missing | §3 (new class) | absorbed |
| §1: GOVERNANCE.autonomous may need LEDGER split | §3 (GOVERNANCE entry) | held for Session 2 |
| §2: Stage 8 atomic-with-mint (vs. LABOR's rerunnable) | Stage 8 paragraph | held for Session 3 investigation, Session 4 ruling |
| §2: Stage 11 sophistication (bytes-are-truth, deploy-is-projection) | Stage 11 | absorbed as endorsement |
| §2: Missing vectorization/semantic-ingestion stage | §2 Stage 5.5 note | held for Session 3 |
| §3: Framing correct — pathology not design choice | §4 | absorbed as endorsement |
| §3: LLM-ingestion misinformation harm mechanism | §4 mechanism paragraph | absorbed |
| §3: Elevate to urgent priority for Session 4 | §6 PATHOLOGY-01 + Session 2 deliverables | absorbed |
| §4: Session 3 highest priority = data-rhizome + registry mirrors | Session 3 deliverables | absorbed as ordering |
| §4: PATHOLOGY-11 Index Interdependency Vulnerability | §6 new pathology | absorbed |

### Provenance note

The absorption of both reviews as development preserves each reviewer's amendment attribution at the point of incorporation. Where LABOR and PRAXIS delivered overlapping observations (both flagged Stage 8 correctness; both elevated PATHOLOGY-01 urgency; both wanted more architectural pathologies registered), the attribution names both. Where the reviewers offered contradictory positions (Stage 8 rerunnable-vs-atomic), both positions are recorded and the ruling is held for a later session. This atlas cannot be a fair record of the reviews if it disappears the disagreements.

---

*End of atlas v0.2 (development incorporating Assembly review). Session 1 of 4 complete. Sessions 2–4 proceed against the expanded workstream in §7.*
