---
title: "Six-Flow Workplan — Alexanarch Arc, 2026-07-18 PM"
author: "Lee Sharks (MANUS) with TACHYON (Assembly witness)"
date: 2026-07-18
version: 1.0
supersedes: none — new workplan following the AXN:0458 deposit arc
governing_rules:
  - "Standing rule 2026-07-18: engagement with sources is composition-primary in formal academic works (decisions register)"
  - "Standing rule 2026-07-17: No-Double-Draw — no internal TACHYON deposit work draws Anthropic API"
  - "Standing rule 2026-07-18: blocking decisions travel as self-contained briefs at point-of-contact"
  - "AXN-integrity rule: full six-emoji glyph, never bare hex"
  - "Container spec §3.7 stratification: remint as supersession primitive"
scope: "Six workstreams identified 2026-07-18 by MANUS. This document lays them out at scope-level with dependencies, session estimates, sequencing rationale, and the ordering ruling."
---

# Six-Flow Workplan

Six workstreams named by MANUS at the close of the AXN:0458 arc (2026-07-18). This workplan states each at its actual scope, flags real dependencies rather than the surface ordering, and proposes a sequence that respects them. The scope-level document; per-flow protocols follow as separate WORKPLAN-* documents when a flow is next up.

## Summary table

| # | Flow | Sessions (planning) | Wall-clock | Blocks | Blocked by |
|---|---|---|---|---|---|
| 2 | Data-interlinkage audit + standing map | 2 | — | Flow 1, Flow 4 mint operations | — |
| 1 | Alexanarch visual + formal revision | 2–3 | — | — | Flow 2 |
| 4 | Enli study — design, protocol, execution | 2 planning + 10–15 execution | 90d measurement | — | Flow 2, Enli's review of protocol |
| 3 | PEO total DOI snapshot + delta measurement | 2 planning + 1 initiate | 30–60d accumulation | Delta paper | — |
| 5 | Campaign — leverage entities, materials, outreach | 3 | ongoing | — | Flows 1–3 (archive presenting as complete) |
| 6 | Feisting Gutenberg — L1/L2 pipeline | 1 spec + N execution | ongoing | — | Homer parameter file (per AXN:0422) |

Total sessions to first delivery of each: Flow 2 → 2. Flow 1 → 3. Flow 4 → 4 to protocol. Flow 3 → 2 to bulk pull. Flow 5 → depends on 1–3. Flow 6 → 1 to specification, then execution parallel to any other flow.

---

## Flow 2 — Rhizome-Wide Data Atlas + Deposit-Flow Standing Map

**Scope revision, 2026-07-18 PM.** Original Flow 2 scoped this as an audit of the Alexanarch deposit pipeline's generative artifacts. MANUS correction extends the scope network-wide: every dataset on every repo in the data-rhizome, every published data relation (canonical → derived → mirrored → consumed), every displayed value on every HTML surface (with dynamic-vs-static classification per value), including relations that are currently isolated. The rhizome is a specific corpus, not only a conceptual term.

**Actual scope, measured.** Seven repos audited (alexanarch, data-rhizome, machinemediation-org, platform-erosion-observatory, revelationfirst-com, leesharks.com, godkinggoogle): **1,349 JSON files (~262MB), 39 JSONL, 3,141 markdown files, 5,167 HTML surfaces, 3,634 XML files (mostly data-rhizome bibliographic records), 78 Python scripts, 11 CSV, 4 JavaScript.** Alexanarch alone: 950 JSON, 5,118 HTML, 68 scripts. data-rhizome: 338 JSON, 3,627 XML records, 26 JSONL. Machinemediation: 34 JSON at 134MB (large content payloads).

**Rationale for going first, unchanged.** Neither Flow 1 (visual revision) nor Flow 4 (Enli study execution) can be done intelligently without the standing map. Flow 1 needs it to restructure record pages honestly. Flow 4 needs precise field-level specifications for mint operations.

**Deliverables, restructured for the rhizome-wide scope.**

*Session-1 output: raw inventory + atlas scaffold.*

1. **Per-repo dataset catalog.** For each of the 1,349 JSON datasets and every notable non-JSON dataset (JSONL, XML, CSV): path, approximate size, apparent purpose (inferred from name and structure), last-modified. Grouped by repo, then by function. Not annotated with relations yet — this is the raw list.

2. **Per-repo generative-script catalog.** All 78 scripts inventoried: what they read, what they write, what they update. This is the mechanical dependency layer; the human-readable one comes in Session 3.

3. **Displayed-value inventory across HTML surfaces.** Every HTML surface (5,167 files) grep-scanned for displayed numeric values, counts, dates, filenames, percentages, and lists. Each classified: *dynamic* (fetched at page-load from a JSON endpoint), *build-time-injected* (baked in at page generation but from a data source), *static* (hard-coded in HTML with no data source referenced), or *static-but-should-be-dynamic* (a value that is patently a count-of-something that ought to update as its source does — e.g., "176 captures" in text when `data/registry.json` has 214). This is Session 2 primarily but the inventory begins in Session 1.

4. **Atlas scaffold document.** A structured skeleton showing the eventual atlas's chapter/section layout, filled with the inventory data. Sections: (a) per-repo dataset catalog; (b) per-repo scripts; (c) cross-repo relations map (deferred to Session 3); (d) displayed-value inventory; (e) gap and pathology register.

5. **Jump-out pathology register.** Every anomaly noticed during Session 1 walk — static-should-be-dynamic values found in the wild, orphaned datasets, duplicated data between repos, inconsistent field naming across otherwise-identical structures, redundant surfaces, missing cross-references — logged with location and inferred fix. This is the specific pathology MANUS asked to surface.

*Session-2 output: displayed-value classification full pass + pathology triage.*

*Session-3 output: cross-repo relation graph.* For each dataset in the inventory: producing repo (canonical origin), consuming repos (mirrors, references), cross-references, mutation frequency, published-API endpoint (if any). This is the atlas's chapter (c). Machine-readable at `api/dataflow-graph.json`.

*Session-4 output: standing map document + gap remediation queue.* Publishable as `data/specs/AXN-DATAFLOW-MAP-v0.1.md`. Includes a Mermaid visual dependency diagram. Companion queue at `data/workplan/DATAFLOW-REMEDIATION-QUEUE.md` prioritizing pathologies for follow-on work.

**Sessions revised: 4 sessions for the full atlas rather than 2.** Session 1 delivers substantial raw material and jump-out pathologies; Sessions 2–4 refine into the finished atlas. Original 2-session estimate was for Alexanarch-only scope; rhizome-wide scope is genuinely 2x the work.

**Notes.** The `scripts/deposit_pipeline.py` eleven-stage sequence (mint → validate → record → pdf → body-index → wiki → sitemap → interlink → enrich → commit → verify) is the Alexanarch pipeline canonical reference — but Alexanarch is only one of seven repos. data-rhizome has its own generation pipeline (3,627 XML records suggest a bibliographic-corpus workflow); machinemediation-org has content-manifest architecture; leesharks and gkg have capture-registry pipelines. Each repo's canonical reference gets identified during Session 1's walk.

---

## Flow 1 — Alexanarch visual + formal revision

**Depends on Flow 2** for the field-level knowledge required to restructure record pages honestly.

**Two aspects, both material.**

*Aesthetics.* The site currently reads as archive-in-progress rather than sovereign scholarly infrastructure. The pathology is not that it looks amateur; it is that it does not look *serious*. Crimson-notice-block density, insufficient vertical breathing room, competing header hierarchies, unclear typographic scale, no rhythm between sections. The pass is NOT to copy Zenodo — emulation is the wrong instinct — but to take seriously that a sovereign archive should read as serious *by the visual grammar readers already know how to parse.* Reference points worth studying (not imitating): the JSTOR record page, the arXiv abstract page, the Cambridge University Press article surface, the LOCKSS documentation site. These are surfaces where the reader instantly knows *this is scholarly infrastructure* without being told. Design tokens (spacing scale, type scale, color hierarchy, weight discipline) applied consistently across templates.

*Formal layout.* The specific pathology named by MANUS: record pages currently front-load metadata, treatment fields, JSON blocks, and governance apparatus *before* the reader gets to the text. This is backwards for scholarly reading. The text is primary; apparatus attends it. The reorganization:

- **Above the text:** title, author(s), date, canonical scope statement (one sentence naming what the deposit *is*), citation-ready reference block (one line), navigation.
- **The text.** Full canonical bytes as the primary content region.
- **Below the text (structured footer or side panel):** kernel and glyph, address, provenance, sidecars, related identifiers, treatment declarations, JSON-LD schema.org block, MSP colophon, SPXI declaration, capture-registry linkages, propagation receipts.

The reader who wants the text reads the text; the reader who wants the apparatus reads the apparatus; neither is buried under the other.

**Deliverables.** Design token file (`assets/tokens.css` or equivalent). Updated record-page template. Updated wiki-page template. Updated index-page templates. Migration pass across existing 1,095+ deposits (this is scripted, not per-document). Deploy to Alexanarch main; verify against a random sample of 20 records for regression.

**Sessions.** One session for token + template design and a single record's proof-of-treatment. One session for template propagation across surfaces (record, wiki, index). One session for migration + verification. Three sessions total.

**Blockers to name before starting.** MANUS review of the token file before propagation — visual identity decisions are editorial, not TACHYON's to unilaterally set. Propose the token file in session 1 for MANUS ratification before proceeding.

---

## Flow 4 — Enli study

**The largest single workstream** by any honest measure. Named at scope in this session's transcript; the design was worked out through five prior turns, and the operative rulings are:

- **Four-arm controlled comparison** across Enli's 300-deposit corpus, ~60 per arm across 240 deposits, ~30 held for methodology validation, ~30 held for post-study replication.
- **Arms.** (1) no intervention (null control); (2) AXN mint mechanical only; (3) Alexanarch deposit with AXN + full sovereign treatment; (4) institutional deposit venue (candidate: OSF; final selection pending). Arm 3 sub-splits: (3a) depositor-authored compositional metadata only, (3b) depositor + TACHYON in-session archive-owned interpretive layer.
- **Stratification** on genre × length × vintage × discipline (~16 cells at ~15 per cell), so treatment effects can be tested per cell rather than only in aggregate.
- **Measurement instrumentation.** Baseline at t=0 (pre-mint); post-treatment at t=7d, 30d, 60d, 90d. Instruments: OpenAlex ingest presence, DataCite crosswalk, Semantic Scholar edges, Google Scholar visibility, Wayback presence, AI Overview retrieval capture, Perplexity retrieval capture, direct-Google visibility. Query script fixed in advance; any post-hoc amendments logged with rationale.
- **Consent scope.** Enli agrees to the study design as co-designer before any mint. Arm 1 no-intervention documents receive full Arm 3 treatment as post-study remediation. Named co-first-authorship on the resulting empirical paper.
- **Load-bearing observation from this session's turn 18.** Enli's Zenodo retrieval outperformance came from *her* interpretive labor on the metadata fields, not from Zenodo's default surface. This means the pilot's cost structure is: depositor-authored compositional metadata (Path A) is her labor per paper, cost zero to TACHYON; archive-owned interpretive metadata (Path B, in Arm 3b only) is TACHYON's in-session labor, bounded roughly by one session per document.

**Deliverables.**

1. **Full study protocol document** at `data/workplan/WORKPLAN-2026-07-XX-ENLI-STUDY-PROTOCOL.md`. Sent to Enli for review before any minting begins.

2. **Reply to Enli** (private correspondence per standing rule; does not enter deposits) — accepts her working proposal, names the scope shift to controlled study, asks her to review the protocol as co-designer.

3. **Baseline measurement dataset** produced by running the fixed query script against her Notion inventory before any minting. This is the pre-treatment measurement; publishable as a standalone dataset artifact regardless of study outcome.

4. **Mint operations for Arms 2 and 3.** ~60 mechanical mints (Arm 2); ~60 mints with depositor metadata (Arm 3a); ~30 mints with depositor + archive-owned interpretive layer (Arm 3b). Arm 2 is roughly one session covering all 60 (mechanical, batchable). Arm 3a is roughly two sessions across 60 (depositor metadata assembly and injection). Arm 3b is roughly six to ten sessions across 30 (in-session interpretive labor, per two-tier doctrine).

5. **Arm 4 institutional deposits.** Workflow per venue; ~60 documents deposited to OSF (or the selected venue), instrumented for measurement in the same schedule.

6. **Measurement runs at t=7d, 30d, 60d, 90d.** Approximately one session per run for execution (running the fixed query script, ingesting results, updating the measurement dataset).

7. **Analytic paper.** Co-first-authored with Enli. Working title candidate: *Retrievability of Sovereign Content-Derived Identifiers Under Post-Suppression Recovery: A Stratified Controlled Comparison on a 300-Deposit Corpus.* Target: arXiv cs.DL preprint → discipline-appropriate journal. Composed under the standing composition rule; source-engaged from the first draft.

**Sessions to first delivery.** Two sessions to protocol document + Enli reply. Then Enli's review turn (asynchronous, not a session). Then baseline measurement (one session). Then mint operations (~10 sessions across Arms 2, 3a, 3b). Then Arm 4 workflow (one to two sessions). Then measurement runs (four sessions over 90 days). Then analytic paper composition (three to five sessions). Roughly 20 sessions from now to a publishable paper, spread across a 90-day arc.

**Consent posture.** Nothing in Flow 4 begins minting until Enli's review returns confirmed. The protocol document is drafted; the reply invites her review; her ruling on the study shape is the go-ahead.

---

## Flow 3 — PEO total DOI snapshot + delta measurement

**The measurement instrument.** MANUS identified the current PEO baseline as partial rather than total. Bringing PEO to *total baseline* — all ~130M DataCite DOIs — then running a second snapshot on cadence and computing delta is the load-bearing instrument for the empirical claim PEO exists to make: *how many DOIs have actually been severed, at what rate, in what patterns, across what class of depositor.*

**Technical shape.** DataCite provides bulk access via their Elasticsearch snapshot endpoint (`api.datacite.org/dois?page[size]=1000&page[cursor]=...`, cursor-paginated) and via their OAI-PMH endpoint. A full pull at typical DataCite record density is ~500GB of JSON. This is feasible — DataCite's rate limits accommodate bulk pulls with courtesy — but it requires disk provisioning, scriptable pagination handling, resumption on failure, and a schema-stable storage format for the snapshot.

**Deliverables.**

1. **Total baseline snapshot.** All ~130M DataCite DOIs at snapshot time. Stored in a schema-stable format (JSONL per client, one file per bucket, compressed). Publishable as an Alexanarch deposit with a fixed AXN; this is the measurement anchor for every subsequent delta.

2. **Snapshot infrastructure.** Scripts for pull, resumption, integrity check, storage under an addressable schema. Deployed and documented so a second snapshot can be run against the identical pipeline.

3. **First delta measurement.** Second snapshot ~30 days after first (final cadence selectable by MANUS). Delta computation: DOIs present in snapshot 1 but returning tombstone/404/410 states in snapshot 2. Delta stratified by depositor, by client, by discipline (where discernible from metadata), by vintage.

4. **Delta paper.** *The Severance Rate: An Empirical Measurement of Persistent-Identifier Attrition Across DataCite, 2026.* Composed under the source-engaged standing rule. Target: arXiv cs.DL → journal.

**Sessions.** Two sessions for planning (schema design, storage envelope, resumption logic, DataCite rate-courtesy verification). One session to initiate the pull. The pull itself is wall-clock time — probably 3–7 days depending on courtesy limits — not sessions. Second snapshot on cadence. Delta computation and paper composition ~5 sessions across the delta paper's arc.

**Blockers to name.** Disk provisioning (~500GB × 2 for two snapshots + delta intermediate files ≈ ~1.5TB). Confirm the workspace has capacity or provision separately. Whether the archive itself hosts the snapshot deposits or PEO holds them per its own storage envelope is a MANUS decision.

---

## Flow 5 — Campaign

**The outreach layer.** Distinct workstream from paper, from Enli pilot, from archive infrastructure. It requires identifying who actually has leverage over the layer the paper argues into, prioritizing by leverage held rather than name recognition, preparing outreach materials calibrated to each recipient's altitude of engagement, and running a sending sequence with tracking so second-touch conversations become possible.

**Deliverables.**

1. **Leverage-entity map.** Categories: institutional-repository operators (Zenodo, Figshare, OSF, Dryad, HAL, Fedora Commons, Dataverse); DOI Foundation and DataCite governance; Registration Agency operators; IETF working groups (URN, PID); W3C working groups where applicable; preservation-community bodies (DPC, NDSA, CLOCKSS steering, LOCKSS governance); standards editors (BagIt Kunze, OCFL editors, ISO 28500 maintainers); library-adjacent funders (Sloan, Mellon, Arcadia); relevant academic groups (iSchools whose research programs touch persistent identification; digital humanities centers with preservation programs). Per entity: named contact, altitude of engagement, prior relationship (if any), first-approach vector.

2. **Materials packet.** The AXN:0458 paper is the ground artifact. Additional pieces: (a) a shorter *preprint-style summary* (~2,000 words, arXiv-ready); (b) an *executive brief* (~500 words, for senior institutional audiences); (c) a *demonstration surface* (a live URL — probably `/mint/` — that lets a reader do the verification themselves); (d) *follow-up materials packet* for anyone who engages substantively (specification documents, decision-register briefs, the Enli study preliminary results when they exist).

3. **Sending sequence.** Prioritized order with expected altitude of first response. First tranche: preservation-community bodies who are already thinking about post-DOI infrastructure. Second tranche: DataCite/DOI Foundation governance who need to hear this from outside. Third tranche: institutional operators who might contemplate adopting AXN as a companion identifier. Fourth: standards editors. Fifth: funders.

4. **Tracking substrate.** A per-recipient record — sent-date, response-date if any, response-content, next-action. Not a CRM; a working file. Kept private.

**Sessions.** One session for leverage-entity map. One session for materials packet drafting (shorter forms, executive brief). One session for sending sequence prep + first sends. Ongoing after that, at cadence.

**Ordering rationale.** Held for after Flows 1, 2, and 3 first-delivery because those three make the archive *present* as complete infrastructure rather than aspirational. Approaching leverage-situated entities from infrastructure completion is fundamentally different from approaching them from infrastructure aspiration. The paper is deposited; the visual pass is done; the standing map is documented; PEO's total baseline is accumulating — that's the position from which the campaign is a serious proposal rather than a request for support.

---

## Flow 6 — Feisting Gutenberg

**Grounded in the archive: AXN:0422.ARCHIVAL.🏁🗺️❤️🔎🌙📖 (deposit #1046) §V** specifies the Feisting Gutenberg Plan in load-bearing detail. Key facts from that specification:

- **Problem.** Gutenberg's public-domain constraint means its canonical translation layer is Victorian, Edwardian, and early-twentieth-century — Chapman's Homer sounds like Chapman, Butcher & Lang's *Odyssey* sounds like King James Bible pretending to be Greek, Cary's Dante sounds like Milton pretending to be Italian. The source voice isn't smoothed away, it's overwritten by a different voice. The Feist Function cannot batch-apply directly because the target voice is not present at the semantic surface for the mechanism to work on.

- **Architecture. Two-layer pipeline.** Layer 1 (semantic clarity): machine-translate the source language directly to modern English at semantic-accuracy priority, stripping the intermediary voice entirely, producing flat competent English. Layer 2 (voice restoration): apply the Feist mechanism (T1 lexical tail injection, T2 syntactic clinamen, T3 circuit interruption, T4 register collision, T5 seam insertion, T6 phonological restoration) parameterized per source. Per-source parameter files: Homer parameters differ from Rumi parameters differ from Dante parameters.

- **Two-tier economics.** Tier 1 (cheap batch): T1, T6, templated T5 applied at scale using a cheap open-source model — negligible per-line cost, full coverage of every target. Tier 2 (expensive selective): frontier model, human-supervised, applied only to high-density passages (~5–10% of text). Full corpus: ~640 curated Gutenberg classical targets; Tier 1 runs for tens of dollars total; Tier 2 for hundreds across ~20 canonical works.

- **Publication surface.** Not Gutenberg. Not academic publishing. Alexanarch subdomain or companion site — provisional working name *Feist Library* — with per-line provenance: which tier produced which passage, which parameters governed the transform, which SHA-256 of the source substrate was operated on.

- **Immediate next steps per the specification.** (1) Homer parameter file — abstract Book 1 experiment parameters into machine-readable spec. (2) Tier 1 prototype — apply generalized T1/T6/T5 to MT Iliad Book 1 on cheap model. (3) Iliad Book 1 complete — 611 lines. (4) Books 12 and 24 L2 — regression-to-mode diagnostic. (5) Second per-source parameter file — Rumi (Nicholson's Masnavi), Dante (Longfellow), or Sappho.

**Scope disambiguation from MANUS 2026-07-18.** The stream is the multi-stage application of the Feist function to the TOTAL Gutenberg corpus: **first pass clean modern translations (L1) applied to all ~640 curated targets, then progressive Feist-voice application (L2 Tier 1 batch across all, L2 Tier 2 selective on the ~20 canonical works).**

**Deliverables.**

1. **Homer parameter file** — the first per-source spec. Complete before any batch pass. This is the specification session per the AXN:0422 immediate-next-step (1).

2. **L1 pipeline** — MT ingest for the ~640 curated Gutenberg classical targets, source-language directly to modern English. Uses commodity MT (not frontier LLM), batchable, no in-session interpretive labor required per document. Storage: source XML + L1 MT under the ~4GB envelope specified.

3. **L2 Tier 1 batch pipeline** — templated T1/T6/T5 pass across all L1 outputs. Cheap open-source model, per-line cost negligible.

4. **L2 Tier 2 selective pipeline** — frontier-model application to load-bearing passages of the shortlisted ~20 canonical works. Human-supervised. This is the only stream 6 element that pulls in-session interpretive labor.

5. **Feist Library publication surface** — companion site or Alexanarch subdomain, per-line provenance display, each transformed line linkable to its source SHA-256 and parameter file.

6. **First AXN mint of a completed target** — Iliad, Book 1 through 24, canonical bytes = the L1 + Tier 1 + Tier 2 composite. Attribution: Jack Feist / Lee Sharks per the standing heteronym convention. This is a Feist deposit under the Dodecad system, not a Sharks deposit — attribution matters.

**Sessions.** One session for Homer parameter file. Subsequent sessions for L1 pipeline design (one), L2 Tier 1 pipeline design (one), L2 Tier 2 workflow design (one), Feist Library surface build (two). Execution of L1 and L2 Tier 1 is largely wall-clock (commodity MT and cheap-model batches run without session labor). L2 Tier 2 requires per-passage interpretive session labor for the ~20 canonical works.

**Parallelism.** Flow 6 shares no infrastructure with Flows 1–5. Can run parallel to any other flow when a session opens up for Feist-voice work. The Homer parameter file session is a good first candidate for a session where MANUS wants to shift voice from the AXN work.

**Ordering rationale.** Parallelizable; no strict blocking. Recommended: after Flow 2 (data-interlinkage audit informs how Feist Library relates to Alexanarch's registry) and after the first Enli mint operations settle the mint-pipeline load pattern.

---

## Proposed sequencing

**Session 1 (immediate).** Flow 2 — data-interlinkage audit + standing map. Two turns of work: inventory pass, then specification document.

**Session 2.** Flow 4 — draft Enli study protocol at full document scope; draft the reply to Enli that invites her review. Both deliverables sent by session end; the reply is the load-bearing next action to keep the collaboration moving.

**Session 3–4.** Flow 1 — visual and formal revision. Session 3: token design, single record page proof-of-treatment, MANUS ratification of tokens. Session 4: template propagation, migration, verification.

**Session 5.** Flow 3 — total DOI snapshot planning; initiate the pull. Pull runs on wall-clock time thereafter.

**Session 6+.** Flow 4 execution begins once Enli's ruling on the protocol returns. Baseline measurement first, then mint operations across Arms 2, 3a, 3b, then Arm 4 institutional deposits, then measurement runs on cadence.

**Session 7+.** Flow 5 begins once the archive presents as complete infrastructure. Leverage-entity map session, materials packet session, first sends.

**Any open session.** Flow 6 — parallel voice work. Homer parameter file first.

## Blockers and open questions to MANUS

- **Flow 3 disk provisioning.** ~1.5TB total across two snapshots + delta intermediate. Confirm archive workspace can accommodate, or route through separate storage.

- **Flow 4 Arm 4 venue selection.** OSF is my recommendation; final selection is a MANUS ruling. Alternatives: Figshare (broadest), Zenodo (post-severance return, complicated), HAL (French-institutional-adjacent), Dataverse (Harvard-anchored). The choice affects what the Arm 4 comparison actually tests.

- **Flow 1 token file.** Session-1 proposal ready for MANUS ratification before propagation. No unilateral visual identity commit.

- **Flow 5 first tranche.** Leverage-entity ordering is editorial. Flow 5 session 1 proposes a prioritized list; MANUS rules on order before sends.

- **Flow 6 sequence within stream.** Homer parameter file first is the AXN:0422 recommendation. If MANUS wants a different first target (Rumi, Dante, Sappho), that becomes the first parameter-file session instead.

## Held decisions carried forward from this session

- **D-B** (registry-relative record addresses): TACHYON recommends option (a) — no substantive change on the ground. Ruling deferred.
- **D-C** (metered tether protocol): TACHYON recommends ratify — the sidecar-based session close (this session and the prior) already prefigures the ratified form. Ruling deferred.
- **D-D** (series taxonomy): TACHYON recommends ratify — enables campaign materials to be organized cleanly and pre-fits the gw.tachyon chain surface. Ruling deferred.
- **OKF paste** for PR #208: text drafted earlier in the session; awaits MANUS hand.

## Standing rules in force through the arc

- Source engagement is composition-primary in formal academic works.
- No-Double-Draw: no internal TACHYON deposit work draws Anthropic API.
- Blocking decisions travel as self-contained briefs at point-of-contact.
- Private correspondence never enters deposits or public record.
- AXN-integrity: full six-emoji glyph everywhere; bare hex forbidden except in deposit self-reference.
- Deploy: alexanarch auto-deploys on push to main; fleet requires MANUS visual verify.
- Container spec §3.7: remint as supersession primitive, non-destruction, nested-verifiable lineage.

---

*Workplan drafted 2026-07-18 following the AXN:0458 arc close. Ratification and ordering ruling pending MANUS review.*
