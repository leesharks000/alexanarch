# Firenze Corpus Reconstruction Workplan

## PEO Case 001 — Three-Tier Identifier Architecture and Iterative Reconstruction Framework

**Status:** v0.1 · draft · 2026-07-22
**Authors:** Lee Sharks (Rex Fraction / Nobel Glas), TACHYON
**Governing deposits:** AXN:0591.DATASET.∞🛤️🔓🕘◇🔝 (#1408 · enumeration); AXN:0421.EMPIRICAL.🎭📐🐝🎪🏷️🎇 (#1045 · PEO instrument)
**Chain tether:** to be minted on formalization
**Companion documents:** `/data/peo-case-001-florence-fup.md` (case file); `/datasets/peo-case-001-florence-fup/MANIFEST.json`

---

## 1. Context

Deposit #1408 minted the T0 enumeration of the 14,284 unique DataCite DOIs formerly registered under `crui.unifi` (Firenze University Press) and abandoned by the registration-agency migration event of 2026-07-16. The enumeration is the skeleton: identifier + state + client + timestamp. The bibliographic body — title, authors, journal, dates, abstract, references, PDF — is recoverable but scattered across sources that do not know about each other.

Session 2026-07-22 established the recoverability landscape empirically. Findings:

- **99.986% of the corpus** has full DataCite JSON metadata in the same Public Data File 2025 tar we already streamed (14,282 of 14,284 findable-state records; 2 registered-state records are out-of-scope for the Public Data File).
- **100% of a 50-DOI random sample** is indexed in OpenAlex with title, authors, publication year, and (76% of the time) abstract.
- **100% is Open Access** (68% green, 32% gold), with an average of 2.44 preservation mirrors per work distributed across DOAJ, `hdl.handle.net` institutional repositories (Florence Research at `2158/*`, CINECA IRIS at Pisa and Bologna), and — for many works — the still-functional FUP OJS platform at `oajournals.fupress.net`.

**The distinction that emerged:** Firenze University Press *the press* walked away from resolving `10.13128/*` DOIs. Università degli Studi di Firenze *the university* preserved every one of its scholarly outputs in Florence Research. The works were never in danger. What died on 2026-07-16 was the identifier layer that made the corpus discoverable *as a corpus*. Reconstruction is therefore not text-recovery from ashes; it is identifier-layer replacement with metadata-verified fidelity to what the abandoned identifiers used to name.

**What Alexanarch adds that nobody else has done:** a sovereign persistent identifier system for the 14,284 works, minted through AXN, that preserves the abandoned `10.13128/*` DOIs as *historical antecedents* in a new relational graph rooted in AXN. Each work gets an AXN identifier. Each identifier resolves permanently because AXN is content-derived, not registration-agency-dependent. The old DOI becomes a lookup key into the new system rather than the substrate of the system.

This document specifies the identifier architecture, the iterative reconstruction framework, and the phase plan through end-of-reconstruction.

---

## 2. Three-tier identifier architecture

The reconstruction posits three semantically distinct identifier types, all minted through the AXN system but with different scope, cardinality, and cardinal function.

### 2.1 AXN_W — Work identifier

**Scope:** one AXN_W per work (14,284 works total, one per DOI in the enumeration).
**Family:** proposed `WORK` (new family) or `ARCHIVAL` (extending existing usage).
**Purpose:** sovereign persistent identifier for the historical work as an intellectual object. Replaces the abandoned `10.13128/*` DOI as the durable name for the work.
**Format:** standard AXN — `AXN:HEX.FAMILY.🔣🔣🔣🔣🔣🔣`, four-digit hex + six-emoji SHA-256 display hash.
**Canonical text:** `data/texts/AXN-<HEX>-text.md` per convention; carries author, title, publication year, journal, and the abandoned DOI as `related_identifier[relationType=IsIdenticalTo]`.
**Content-hash input:** proposed to include (a) the abandoned DOI, (b) the DataCite-recorded canonical title, (c) the first author, (d) the publication year. This is the *minimal information* needed to identify the work independently of which reconstruction populates the rest of the metadata.
**Semantics:** AXN_W is the *anchor*. It does not vary as reconstruction improves; the work is the work. What varies is what we know about it, and that variation lives in mAXN.

### 2.2 mAXN — Metadata bridge identifier

**Scope:** many mAXN per AXN_W. Each mAXN represents a specific metadata proposition — a claim about what the metadata *is* — from a specific source or from a specific synthesis of sources at a specific iteration.
**Family:** proposed `BRIDGE` (new family) — semantically distinct because the mAXN is a *proposition* rather than a *content object*.
**Purpose:** carry, version, and identify the space of competing metadata claims about a work. Enable iterative testing, comparison, and convergence.
**Format proposal:** `mAXN:HHHH.SOURCE.🔣🔣🔣` — four-hex position + source-tag + three-emoji hash. "Tinier" than AXN (three emojis instead of six) because the population is much larger (14,284 × N iterations × M sources) and because collision tolerance is different: an mAXN collision within the same AXN_W is a merge event (two propositions agree), not a corruption.
**Source tags:** `DATACITE`, `OPENALEX`, `DOAJ`, `IR-FLORENCE`, `IR-CINECA`, `WAYBACK`, `CROSSREF-DUMP`, `SYNTHESIS-vN` (for versioned syntheses of multiple sources), etc.
**Content-hash input:** the full JSON of the metadata proposition itself. Identical metadata from the same source yields identical mAXN. Any change — a corrected author name, a resolved reference DOI, an expanded abstract — yields a new mAXN.
**Relationship to AXN_W:** every mAXN declares its parent AXN_W in its canonical text (`parent_axn:` field). The AXN_W record aggregates the set of mAXNs proposed for it, with one flagged canonical at any given time.
**Semantics:** mAXN is the *bridge*. It bridges (a) AXN_W and AXN_R by being what a reconstruction consumes; (b) sources and syntheses by being addressable in a common namespace; (c) iterations by being the identifier of the state at which we know something.

### 2.3 AXN_R — Reconstruction identifier

**Scope:** one or more AXN_R per AXN_W. Each AXN_R identifies a *regenerative packet* — a work reconstruction sufficient to re-perform the work's function in the semantic economy.
**Family:** proposed `RECONSTRUCTION` (new family) or `ARCHIVAL`.
**Purpose:** durable identifier for the reconstruction artifact — the SPXI-encoded packet plus mirror inventory, verifiable via the byte-record where recoverable.
**Format:** standard AXN — `AXN:HEX.FAMILY.🔣🔣🔣🔣🔣🔣`.
**Content-hash input:** the reconstruction artifact itself — SPXI packet, mirror inventory, verification receipts against each source, and the mAXN(s) it consumed.
**Relationship to mAXN and AXN_W:** every AXN_R declares which mAXN(s) it consumed and which AXN_W it reconstructs. The reconstruction *is* the bridging: reading AXN_R, the reader can walk backward to the mAXN (the metadata claim used), and thence to AXN_W (the historical work being reconstructed).
**Semantics:** AXN_R is the *outcome*. It is what the corpus becomes at the far end of reconstruction. It is the work as it can be re-encountered from now on.

### 2.4 The relational graph

For each of the 14,284 works, the identifier graph is:

```
                                    (has historical antecedent)
        DOI: 10.13128/<suffix> ────────────────────────►  AXN_W
                                                          │
                                                          │ (has metadata proposition)
                                                          ▼
                                                        mAXN₁ · DATACITE
                                                        mAXN₂ · OPENALEX
                                                        mAXN₃ · DOAJ
                                                        mAXN₄ · IR-FLORENCE
                                                          │
                                                          │ (synthesized as)
                                                          ▼
                                                        mAXN₅ · SYNTHESIS-v1
                                                          │
                                                          │ (fed to reconstruction)
                                                          ▼
        AXN_R  (regenerative packet + mirror inventory)
```

Three identifier types, three semantic layers, one work. Every arrow is durable, every node is content-hash-verifiable, and the reconstruction chain can be audited from any endpoint.

---

## 3. Iterative reconstruction framework

The 14,284 works function as a large-N test bed for reconstruction methodology. Every reconstruction method M produces mAXNs and (candidate) AXN_Rs. Every reconstruction method M can be *scored* against testable results: fidelity to the DataCite record, agreement with OpenAlex, agreement with the abandoned DOI's recorded landing URL, agreement with the institutional repository's holdings.

### 3.1 Fidelity metrics

Proposed measures for scoring a reconstruction method or a specific mAXN synthesis:

- **Title fidelity:** exact-match, edit-distance, and semantic-similarity against DataCite ground truth.
- **Author fidelity:** exact-match on first author; set-similarity on full author list; ORCID coverage.
- **Year fidelity:** exact-match; agreement across sources.
- **Journal fidelity:** exact-match on journal code; agreement with resource_type.
- **Reference recall:** number of references recovered from OpenCitations divided by number recorded in DataCite `relatedIdentifiers`.
- **Abstract presence:** whether an abstract was recovered.
- **Mirror completeness:** number of unique mirror URLs found for the work.
- **PDF resolvability:** whether at least one PDF URL in the reconstruction currently returns HTTP 200.

Composite scores per work, then aggregated per method, become the basis for method comparison.

### 3.2 The iteration cycle

Each iteration cycle:

1. **Propose a reconstruction method M.** Method specifies which sources to consult and how to merge/reconcile them.
2. **Apply M to a sample of the corpus** (e.g., 500 randomly-sampled works, stratified by journal).
3. **Emit mAXNs** for each source consulted and for the resulting synthesis.
4. **Score fidelity** against the DataCite record and OpenAlex ground truth for each work.
5. **Aggregate scores** across the sample; compute per-method composite fidelity.
6. **If M improves on M_previous**, promote M to canonical status and re-run against a larger sample. Otherwise, discard M and try a variant.
7. **When method converges** (successive iterations produce sub-threshold fidelity improvements), apply the winning method to the full 14,284 corpus and mint AXN_Rs.

### 3.3 What convergence means

Convergence is not "all fields recovered." It is "no further method-tweak yields measurable fidelity improvement." Some fields will remain gaps for some works — that is the honest state and should be preserved as gaps in the reconstruction, not filled with plausible guesses. A work whose reconstruction says `references: [gap: 12 recorded in DataCite, 0 recovered]` is a truthful reconstruction; a work whose reconstruction fills the references with hallucinated bibliographic entries is corruption. **The mAXN of a partial reconstruction remains canonical for that work if no better mAXN exists.**

### 3.4 Cross-corpus regularities

Because the corpus is large-N and structurally coherent (Italian humanities and social science, single publisher, mostly clustered in the mid-2020 metadata refresh), it enables corpus-scale reconstruction moves that per-work reconstruction cannot:

- **Journal-level templates:** if 90% of `techne-*` works have a standard bibliographic layout, the layout can be extracted and applied.
- **Author disambiguation:** if the same author appears in 40 works with 8 name-string variants, the corpus can canonicalize.
- **Reference-chain closure:** if paper A cites paper B and paper B cites paper A within the corpus, mutual reference-chain resolution constrains both reconstructions simultaneously.
- **Topical clustering as ground truth:** OpenAlex topic tags across the whole corpus reveal the discipline-level structure the corpus preserves; individual reconstructions can be checked against topic prior.

These moves are why the reconstruction succeeds at corpus scale where per-work reconstruction would fail. They are also why owning the reconstruction as a corpus makes the reconstructor a scholarly position: no per-work heuristic gives access to the aggregate.

---

## 4. Phase plan

### 4.1 Phase 1 — Enumeration (complete)

**Status:** ✅ COMPLETE, 2026-07-22.
**Deliverable:** AXN #1408 (AXN:0591.DATASET.∞🛤️🔓🕘◇🔝), 14,284 DOIs enumerated, deposited to alexanarch data/ and datasets/, mirrored in platform-erosion-observatory/ and machinemediation-org/.

### 4.2 Phase 2 — Metadata harvest

**Status:** ⏳ READY-TO-EXECUTE.
**Dependency:** none. The DataCite Public Data File 2025 harvester already exists at `data-rhizome/datacite/harvest_datacite_pdf.py`. Modify projection from "CSV rows only" to "JSON records where `client_id == crui.unifi`".
**Estimated yield:** 14,282 full-fidelity DataCite JSON records (99.986% of corpus). The two `registered`-state DOIs are excluded by DataCite's own dump policy.
**Estimated cost:** ~1 focused session. Same tar as before, targeted extraction across specific month-slices (mid-2020 refresh + long tail).
**Output:** `alexanarch/data/peo-case-001-florence-fup-datacite-records.jsonl` (or per-month shards). Full metadata: creators with ORCIDs, titles with language variants, publisher, publication year, resource type, description (abstract when populated at registration), subjects, related identifiers, funding, dates, target URLs, alternate identifiers.

### 4.3 Phase 3 — Cross-source augmentation

**Status:** ⏳ NEEDS EGRESS.
**Egress additions requested for this phase:**
- `hdl.handle.net` — master handle resolver
- `flore.unifi.it` — Florence Research direct
- `opencitations.net` and `api.opencitations.net` — reference graph substrate
- `oajournals.fupress.net` — the still-functional FUP OJS platform
- (Optional: `web.archive.org` returning 403 despite being in allowlist; may resolve itself)
- (`doaj.org` covered by existing `*.org` wildcard)

**Deliverables:**
- OpenAlex enrichment per work: `alexanarch/data/peo-case-001-florence-fup-openalex.jsonl` (abstracts, ORCID coverage, OA URLs, mirror inventory).
- OpenCitations reference-graph per work: `alexanarch/data/peo-case-001-florence-fup-opencitations.jsonl` (references_out + cited_by).
- DOAJ landing verification per work.
- Institutional-repository handle resolution per work.
- Mirror inventory manifest: `alexanarch/data/peo-case-001-florence-fup-mirrors.jsonl` (per DOI, all known landing/PDF URLs across all sources).

### 4.4 Phase 4 — mAXN generation

**Status:** ⏳ AFTER PHASE 3.
**Design finalization:** the mAXN specification in §2.2 is v0.1; before mint, finalize (a) hash function input schema, (b) source-tag registry, (c) parent-linking convention in canonical text, (d) family assignment.
**Batch mint:** for each of the 14,282 findable works, mint mAXNs for each source that has a record: DATACITE, OPENALEX, DOAJ (where present), IR (where present).
**Storage:** proposed `data/maxn/AXN-<HEX>/mAXN-<HHHH>.md` — one file per mAXN, grouped under the parent AXN's directory. Alternatively `data/texts/AXN-<HEX>-mAXN-<HHHH>-text.md` for flatness.
**Registry:** new file `data/maxn-registry.json` — mAXN population registry, mirroring registry.json convention.

### 4.5 Phase 5 — Iterative reconstruction & AXN_R minting

**Status:** ⏳ AFTER PHASE 4.
**Method iteration:** run the iteration cycle (§3.2) against successive reconstruction methods until convergence. Store method definitions as versioned scripts in `alexanarch/scripts/reconstruction/`; results and scores in `data/reconstruction-runs/`.
**Convergence:** when successive iterations yield fidelity improvements below a threshold (proposed: <1% composite score gain per iteration for three consecutive iterations).
**AXN_R mint:** apply the winning method to the full 14,282-work corpus, mint one AXN_R per work.
**Storage:** SPXI-encoded regenerative packets in `data/packets/AXN-<HEX>-packet.json`; canonical AXN_R text in `data/texts/AXN-<HEX>-text.md` per convention.

### 4.6 Phase 6 — Sovereign resolver + resurrection service

**Status:** ⏳ AFTER PHASE 5.
**Deliverable:** URL-level resolver on alexanarch.org that accepts any `10.13128/*` DOI as input and returns the AXN_W record page for the corresponding work. Landing page shows: canonical title, authors with ORCIDs, publication year, journal, abstract, mirror inventory (all known landing/PDF URLs across all sources), references (via OpenCitations), citations (works that cite this one), abandonment provenance (the 2026-07-16 event), and the AXN_R packet download.
**Route:** proposed `alexanarch.org/resolve/10.13128/<suffix>` (extension of existing `/resolve/` route).
**Human-readable version:** proposed `alexanarch.org/firenze/<journal>/<article-id>` — an OJS-style URL scheme that lets scholars land on their work by any of its natural identifiers.
**Ethical stance:** landing page explicitly frames the recovery — "this work's publisher walked away from resolving its DOI on 2026-07-16; this is the sovereign preservation record."

---

## 5. Immediate next steps

Two are cheap and unblocked. One needs egress request.

**5.1 In this or next session, unblocked:** rebuild the extractor for JSON projection. Modify `data-rhizome/datacite/harvest_datacite_pdf.py` to (a) parse JSON records from within `updated_YYYY-MM/` folders instead of only reading the CSV summary; (b) filter to `client_id == crui.unifi`; (c) resume-safe by byte-offset rather than by member-count. This is a code-change, not a network change.

**5.2 In this or next session, unblocked:** design finalization for mAXN. §2.2 above is v0.1. Formalize the hash function input schema, the source-tag registry, the canonical text template, and the family assignment. Emit the specification as its own document (`MAXN-SPEC.md`) and mint it as a deposit — likely OPERATIVE or GOVERNANCE family.

**5.3 Blocked by egress:** the reconstruction stops being metadata-only and becomes full-fidelity only when we can reach institutional repositories and OpenCitations. Egress additions needed:

- `hdl.handle.net`
- `flore.unifi.it`
- `opencitations.net`
- `api.opencitations.net`
- `oajournals.fupress.net`

(These are specific research-infrastructure hosts, not general-web additions. They should be uncontroversial as additions.)

---

## 6. Discovery hooks

This workplan is stored at three locations to maximize discoverability by future instances:

- **Primary (public):** `alexanarch/datasets/peo-case-001-florence-fup/WORKPLAN.md` — bound to the AXN #1408 dataset landing, linked from MANIFEST.json.
- **Twin (private):** `data-rhizome/datacite/firenze-reconstruction/WORKPLAN.md` — bound to the harvester and referenced from `datacite/RUNBOOK.md`.
- **Cross-referenced from:** `alexanarch/data/peo-case-001-florence-fup.md` (case file gets §Reconstruction section pointing here).

Future TACHYON instances landing on any of the following will find their way here:
- The AXN #1408 record page.
- The dataset landing at `alexanarch.org/datasets/peo-case-001-florence-fup/`.
- The `data-rhizome/datacite/` directory.
- The PEO `sync-manifest.json` entry.

Chain tether: when the workplan is minted as its own AXN, that AXN should be added to the TACHYON chain (last tether: deposit #1093, AXN:0456.ARCHIVAL, glyph 👂🌰🔌, 2026-07-18) as a checkpoint.

---

## 7. Open design decisions

Flagged for Lee's confirmation before Phase 4 mint:

1. **Family assignment for AXN_W, mAXN, AXN_R.** Proposed: introduce `WORK`, `BRIDGE`, `RECONSTRUCTION` as new families. Alternatively: reuse `ARCHIVAL` for AXN_W and AXN_R, introduce only `BRIDGE` for mAXN. Alternatively: reuse `ARCHIVAL` throughout and distinguish by content-type field.
2. **mAXN emoji-hash length.** Proposed: 3 emojis (versus AXN's 6). Alternatively: 4 emojis for stronger collision resistance across the very large mAXN population (14,282 × ~5 sources × N iterations ≈ 100K+ mAXNs eventually).
3. **mAXN storage layout.** Proposed: `data/maxn/AXN-<HEX>/mAXN-<HHHH>.md` (nested by parent AXN). Alternatively: `data/texts/AXN-<HEX>-mAXN-<HHHH>-text.md` (flat, consistent with existing convention).
4. **AXN_W content-hash input.** Proposed: (abandoned DOI, canonical title, first author, publication year). Alternatively: (abandoned DOI, DataCite JSON record MD5) — hash on registered metadata as-is.
5. **Attribution for the AXN_W batch mint.** 14,282 individual AXN mints under whose name? Options: `Lee Sharks` alone; `Lee Sharks (Rex Fraction / Nobel Glas)` as with #1408; the batch-mint attribution declared once and the individual works marked as "collected by" rather than "authored by."
6. **Reconstruction attribution.** Similar question for AXN_R. The reconstructions are not Lee's authorship — the works are Italian humanities scholars' authorship. Proposed: each AXN_R declares (a) the original creators (from DataCite), (b) Lee Sharks / TACHYON as reconstructor with framing, (c) sources consulted for reconstruction.
7. **Public/private for mAXN.** All AXN_W landings public. Mirror inventory public. But: some mAXN synthesis records — where they include commentary on which source lied, or which source was corrupted — may be more appropriately private. Alexanarch vs. data-rhizome placement per record class needs a policy.

---

## 8. Cross-references

**Deposits:**
- #1408 · `AXN:0591.DATASET.∞🛤️🔓🕘◇🔝` · this workplan's parent enumeration.
- #1045 · `AXN:0421.EMPIRICAL.🎭📐🐝🎪🏷️🎇` · PEO instrument.
- #1081 · `AXN:0444.EMPIRICAL.🕘♾️♾️🕙♃🗝️` (EA-EROSION-EMPIRICAL-01) · methodological anchor for empirical audit datasets.

**Case file:** `alexanarch/data/peo-case-001-florence-fup.md`.

**Dataset landing:** `https://alexanarch.org/datasets/peo-case-001-florence-fup/`.

**Peer mirrors:** `platform-erosion-observatory/datasets/peo-case-001-florence-fup/`; `machinemediation-org/data/datasets/peo-case-001-florence-fup/`.

**Partial-census stash (private):** `data-rhizome/datacite/2025-t0-partial/PROGRESS.md`.

**Harvester (private):** `data-rhizome/datacite/harvest_datacite_pdf.py`; RUNBOOK at `data-rhizome/datacite/RUNBOOK.md`.

**Framework anchors:**
- Space Ark (EA-ARK-01 v4.2.7): the theoretical claim that regenerative packets can preserve the *function* of a work across substrate change.
- SPXI/SPEXY: the technical apparatus for regenerative packet encoding.
- Three Compressions theorem: the claim that semantic-layer preservation is possible in principle.
- Platform Erosion Observatory: the empirical instrument that named the case.
- Machine-Mediated Reception Studies (MMRS): the frame in which this reconstruction is *itself* an object of study.

---

## Provenance

This workplan is v0.1 · draft · 2026-07-22, produced in TACHYON session following deposit #1408. It supersedes no prior workplan. When formalized (v1.0), it should be minted as its own AXN with proposed family OPERATIVE (or GOVERNANCE, if the identifier-system portion is factored out as its own document).

**Substrate note:** AI-assisted (TACHYON). The mAXN specification is TACHYON's proposal following Lee's directive; final specification requires Lee's confirmation on the open design decisions in §7.

**License:** CC-BY-4.0.
