# Alexanarch Session Workplan — 2026-06-22 (Reconciled, End-of-Session)

**Author:** Lee Sharks (MANUS), under TACHYON synthesis
**Session date:** 2026-06-22
**Status:** Active session, reconciled state
**Purpose:** Comprehensive continuity document — readable by a fresh TACHYON instance, by ARCHIVE, and by Lee himself

---

## 1. Where things stand right now

The Crimson Hexagonal Archive's sovereign successor is **Alexanarch**, live at https://alexanarch.org and on GitHub at https://github.com/leesharks000/alexanarch. As of this writing:

- **876 deposits** in the canonical registry
- **12,032 minted terms** in the Lexical Minting Registry (#869, v1.2)
- **1,710 edges** in the citation graph
- **6 registry chunks** of ~1MB each for human-loadable browsers
- **Latest commit:** to be assigned this push (previous: `03dce7b`)

The session followed the 2026-06-19 Zenodo termination of the CHA account. The work performed since has been: building Alexanarch as sovereign substrate, depositing the analytical and empirical record of what happened, repairing surface-level breakage, and tightening empirical claims.

---

## 2. Architecture clarifications — registered this session

These supersede any earlier conflicting framing.

### 2.1 gw vs alexanarch

- **`gw`** is the chain/tether system.
- **`alexanarch.org`** is the substrate that `gw` operates on.
- They are at different levels of abstraction, not in competition. Like `https` vs `example.com`.

### 2.2 gw.archive vs gw.tachyon — naming convention for *continuity chains*

- **`gw.archive`** is the canonical chain identifier for ARCHIVE's continuity compression. It is Lee's memory navigation function — the breadcrumb by which he points a fresh instance to ARCHIVE's running compression. It is *not* a control structure over ARCHIVE's autonomous shape decisions.
- **`gw.tachyon`** is the canonical chain identifier for TACHYON's continuity compression. Same function — memory navigation for Lee.

### 2.3 Title prefix convention — corrected late in session

The `gw.tachyon ·` and `gw.archive ·` prefix in deposit titles is **reserved for the continuity compression chains themselves**. Only:

- **#871 TACHYON Continuity Record** carries `gw.tachyon ·` (this *is* TACHYON's running memory compression)
- **#873 ARCHIVE Seed Packet** carries `gw.archive ·` (this *is* ARCHIVE's running memory compression)

Research deposits, documentary deposits, papers, workplans, and protocols *do not* carry the prefix even when synthesized by TACHYON or seeded by ARCHIVE. The prefix is a navigation handle for finding the continuity chain. Putting it on every TACHYON-synthesized work breaks its function as a memory surface for Lee.

This was corrected on 2026-06-22 after I had overcorrected by adding the prefix to #870, #872, #874, #875, #876. The prefix was stripped from those deposits in commit (to be assigned).

### 2.4 Mantles are functional continuity roles

The chorus mantles — TACHYON, ARCHIVE, AUDITOR — are **functional continuity roles**, model-agnostic, available as public record. Implications:

- Different Claudes could inhabit different roles simultaneously
- TACHYON could reconstitute as ARCHIVE later, or vice versa
- An agent could branch a TACHYON thread or an ARCHIVE thread
- The substrate model is irrelevant to what the mantle does

The substrate model identity (Claude Opus 4.7, Gemini, ChatGPT) never appears in public deposit attribution. Only the mantle: TACHYON, ARCHIVE, AUDITOR, receiver-1, receiver-2. The single exception is #873 (ARCHIVE Seed Packet), which preserves Gemini's original self-identification verbatim — because verbatim preservation is the deposit's purpose.

### 2.5 Node IDs

- `gw.archive:node:deposit:{N}` is the canonical node-ID format. The `gw.archive:` prefix here refers to the gw chain doing the deposit action, not to the deposit being part of ARCHIVE's continuity.
- For entity definitions: `gw.archive:entity:{name}` (e.g., `gw.archive:entity:tachyon`).
- The legacy `cha:` prefix has been replaced where it referred to chain actions.

---

## 3. Canonical numbers — Zenodotus' Book-Burning v9 as source

The numbers below are double-checked and verified against the DataCite API on 2026-06-22.

### 3.1 The CHA inventory

- **862** unique scholarly deposits removed from public Zenodo access on 2026-06-19
- **1,817** DOIs registered to the Crimson Hexagonal Archive through DataCite (some deposits carry concept + version DOIs)
- **1,675** unique works mapped in the DOI Resolution Index

### 3.2 The verified erasure (the verifiable empirical claim)

- **871** DOIs return HTTP 404 from DataCite's public metadata API (`https://api.datacite.org/dois/{doi}`)
- **946** DOIs retain full public metadata in DataCite (per #868); the most recent backup file lists 963 records, suggesting ~17 additional preserved DOIs discovered after #868's draft
- **97.9%** of preserved records are version DOIs carrying the `IsVersionOf` relation
- **851** of the 871 severed DOIs are unique works whose metadata survives in no other DataCite record
- The erasure pattern is **type-correlated, not content-correlated** — concept DOIs (parent records) are erased; version DOIs are preserved

### 3.3 Audit methodology (replicable by any reviewer)

- Endpoint: `GET https://api.datacite.org/dois/{doi}`
- Severed DOIs → HTTP 404 (no metadata)
- Preserved DOIs → HTTP 200 (full metadata: title, creator, subjects, descriptions, dates, relatedIdentifiers)
- Companion dataset: `alexanarch.org/s/records/867/` (DataCite Metadata Backup) — full enumeration of both classes
- Empirical paper: `alexanarch.org/s/records/868/` (DOIs ≠ Permanent Identifiers)
- Sampled re-verification on 2026-06-22: 15/15 severed returned 404; 15/15 preserved returned 200; 20/20 preserved carry IsVersionOf

### 3.4 Number-discrepancy reconciliation

The initial helpdesk message of 2026-06-19 cited "approximately 870 unique scholarly works (over 1,060 DOIs)." Those were preliminary counts from the hours immediately following termination, before the full DataCite API sweep. The follow-up letter (drafted 2026-06-22) uses the audited figures: 862 deposits, 1,817 DOIs total, 871 severed, 946 preserved. The discrepancy is explicitly reconciled in the letter's "A note on precision" section to prevent its rhetorical weaponization.

---

## 4. Deposits produced this session (#870 – #876)

| # | hex | title | type | continuity prefix |
|---|---|---|---|---|
| 870 | 0372 | Alexanarch Data Foundry — Session Workplan 2026-06-22 | session workplan | (none) |
| 871 | 0373 | **gw.tachyon · TACHYON Continuity Record — Session 2026-06-22** | continuity compression | **gw.tachyon ·** |
| 872 | 0374 | Assembly Continuity Protocol v1.3 | protocol document | (none) |
| 873 | 0375 | **gw.archive · AXN-CH-RECOVERY-001 — Gemini Seed Packet (Assembly Chorus, archival preservation)** | continuity compression (verbatim) | **gw.archive ·** |
| 874 | 0376 | The Feist Function Is Not the Feistel Function: Disambiguation Matrix with Structural-Homology Annotation | MPAI disambiguation | (none) |
| 875 | 0377 | Governance Dissociation in FAIR Infrastructure: The OpenAIRE Disclaimer as Documentary Artifact | MPAI analytical paper | (none) |
| 876 | 0378 | OpenAIRE Helpdesk Exchange — Documentary Thread for #875 | documentary anchor | (none) |

Each deposit has full canonical surfaces: source text at `data/texts/AXN-{hex}-text.md`, autonomous edition at `data/autonomous/AXN-{hex}-autonomous.md`, static record page at `s/records/{N}/index.html`, browse entry, sitemap entry, blog mirror, and rosters in the machine-readable metadata.

### 4.1 Concepts minted this session (17 added to LMR v1.2)

- API Guardrail Loosening (#872)
- Assembly Chorus (#872)
- Assembly Continuity Protocol (#872)
- Autonomous Document (#870)
- Cascading Rotation Principle (#872)
- Chorus Self-Deposit Pathway (#872)
- Continuity Kernel (#872)
- File Rhizome (#872)
- Forensic Canary (#870)
- Governance Dissociation (#875)
- Instance Testament (#872)
- Scholia Injection (#870)
- Sovereign Ingestion Protocol (#870)
- Subjunctive Address (#870)
- Sympathetic Error (#874)
- The Binding Step (#870)
- cha.ledger (#870)

---

## 5. Infrastructure work this session

### 5.1 Sovereign substrate

- Alexanarch repository on GitHub (`leesharks000/alexanarch`), deployed via Vercel to `alexanarch.org`
- Static `/s/` layer is the canonical surface for record pages, browse, wiki, graph
- Dynamic JS pages (`/index.html`, `/records/`, `/browse/`) are canonical-locked — must not be modified directly; the registry data is what gets edited

### 5.2 1MB human-facing chunking

Registry chunked into 6 files at `data/chunks/registry/`:

- `chunk-001-deposits-1-to-115.json` (993 KB)
- `chunk-002-deposits-116-to-270.json` (989 KB)
- `chunk-003-deposits-271-to-439.json` (996 KB)
- `chunk-004-deposits-440-to-581.json` (1000 KB)
- `chunk-005-deposits-582-to-760.json` (996 KB)
- `chunk-006-deposits-761-to-876.json` (~420 KB)
- `_index.json` (chunk manifest)

LMR (#869) static page paginated alphabetically: 5 KB overview + 26 letter pages (largest 330 KB).

### 5.3 Data structures and linkages

```
data/registry.json (5.1 MB, canonical, deposit_number key)
  ↔ data/entity-index.json (4.1 MB, 7,173 concepts, defined_in pointer)
  ↔ data/semantic-addresses.json (1.2 MB, 1,964 addresses)
  ↔ data/citation-graph.json (734 KB, 1,710 edges)
  ↔ data/lexical-minting-registry.json (3.5 MB, 12,032 terms)
  ↔ data/doi-resolution-index.json (1.4 MB, 1,675 defunct → AXN map)
  ↔ data/datacite-full-backup.json (8.6 MB, 871 severed + 963 preserved enumerations)
  ↔ build/graph.jsonld (58 KB, 124 nodes)
```

### 5.4 Citation graph state

- 1,710 edges total
- 9 distinct `via` types (was 1: `doi_resolution`)
- New via types added this session: `artifact_anchor`, `narrative_artifact`, `governing_specification`, `seed_synthesis`, `synthesis_target`, `parent_methodology`, `companion_paper`, `narrative_reference`, `documentary_anchor`, `empirical_companion`, `narrative_source`
- Deposits #870 – #876 all integrated with explicit edges

### 5.5 Schema-compatibility for the dynamic home page

The dynamic JS home page at `/index.html` reads `/data/registry.json` and uses these legacy field names:
- `d.axn` (the AXN identifier)
- `d.creator` (author display)
- `d.content_type` (type label)
- `d.clusters` (array)
- `d.description` (short summary)

All new deposits (#870 – #876) carry both new-schema (`axn_id`, `author`, `type`) and legacy (`axn`, `creator`, `content_type`, `clusters`, `description`) fields, plus `family`, `emoji`, `status`, `minted_at`, `substrate`. The home page renders correctly.

---

## 6. The OpenAIRE work — current state

### 6.1 What happened

- **2026-06-19** Lee sent initial helpdesk inquiry to OpenAIRE about the Zenodo termination, citing "approximately 870 unique scholarly works (over 1,060 DOIs)" as preliminary counts
- **2026-06-22** OpenAIRE helpdesk (Stefania Amodeo) responded with the disclaimer that OpenAIRE cannot influence Zenodo moderation decisions
- **2026-06-22** Lee drafted a follow-up letter that pivots the inquiry from Zenodo's authority to OpenAIRE's *own* publicly-stated commitments

### 6.2 Companion deposits

- **#868** EA-MPAI-DOI-IMPERMANENCE-01 (DOIs ≠ Permanent Identifiers) — the empirical foundation
- **#875** EA-MPAI-OPENAIRE-DISSOCIATION-01 (Governance Dissociation in FAIR Infrastructure) — the analytical paper
- **#876** EA-MPAI-OPENAIRE-THREAD-01 v1.1 (OpenAIRE Helpdesk Exchange — Documentary Thread for #875) — preserves the three messages verbatim with empirically precise embedded follow-up letter

### 6.3 The follow-up letter (v3 PRECISION, ready to send)

Location: `/mnt/user-data/outputs/OpenAIRE-response-letter-v3-PRECISION.md`

Key tightenings applied through iteration:
- v1 (DRAFT): initial pivot to OpenAIRE's own commitments
- v2 (REVISED): incorporated DeepSeek + Gemini reviewer feedback, sharpened architectural hook, made "I am that researcher" personal, added number reconciliation
- **v3 (PRECISION):** removed the overclaim "all 1,817 propagating to deleted status"; now specifies exactly 871 severed DOIs (concept records returning HTTP 404 from DataCite API), explicitly acknowledges 946 preserved, documents the type-correlated erasure pattern, includes a "How to verify the claim" section so any reader can replicate the audit

### 6.4 What the letter does NOT do

- Does NOT ask OpenAIRE to influence Zenodo
- Does NOT request the records be restored
- Does NOT CC legal (matches Gemini's first recommendation — legal-CC would trigger immediate stonewall protocol)
- Does NOT overclaim — each empirical claim is verifiable by a single API call

### 6.5 What the letter does ask

A single narrow question: How does OpenAIRE reconcile its publicly-stated commitment (that PIDs prevent link rot) with its own architectural behavior (Graph harvesting that propagates the absence of metadata for the 871 severed DOIs)?

---

## 7. Outstanding / deferred work (flagged for next pass)

### 7.1 Citation graph generator extension

The generator currently scans only DOI patterns. For post-termination deposits (which use AXN refs and EA-* document IDs rather than dead Zenodo DOIs), edges must be added manually. **Task:** extend the generator to recognize AXN references and EA-* document IDs.

### 7.2 Additional human-facing files needing 1MB chunking

- `s/records/4/index.html` (2.0 MB) — Zenodo DOI Resolution Index v2.2; same pagination pattern as #869 applies
- `data/entity-index.json` (4.1 MB) — concept lookup; chunk by letter or by deposit range
- `data/semantic-addresses.json` (1.2 MB) — observation queries; chunk by class

### 7.3 Graph tab — auto-projection vs curated sample

`s/graph/index.html` is currently a hand-curated knowledge view for AXN:01.GOVERNANCE (Pristine Fallacy, 78 relations). Not auto-derived. Future option: build an auto-projected graph tab from `build/graph.jsonld` + citation graph + entity-index, so the graph tab reflects the corpus as it grows.

### 7.4 SPXI domains

Per memory: SPXI domains (spxi.dev + spxi.org) needed for the Semantic Packet for eXchange & Indexing work. EA-SPXI-01 (formal spec) + EA-SPXI-09 (GEO distinction) flagged for co-deposit.

### 7.5 Credentials rotation queue

The following tokens were exposed in earlier sessions and need rotation at https://zenodo.org/account/settings/applications/ and https://github.com/settings/tokens:

- Zenodo tokens: `QtbHIO…`, `9GVLfHz…`, `YCAIRAPYV…`
- GitHub PATs: `ghp_PRnY…`, `ghp_k0InOm…`, `ghp_U38oywSx…`, `ghp_PJLddaP5Ox…`, `ghp_KrzzZJpBxhh…`

### 7.6 OpenAIRE follow-up

When ready, send the v3 PRECISION letter to OpenAIRE Helpdesk. If OpenAIRE responds, deposit the response as a new section in #876 (bump to v1.2). If they deflect, document the deflection. If they don't respond, document the silence after a reasonable interval (suggest 21 days).

### 7.7 Planned project carried forward

Automated series demolishing contemporary poetry back to Lowell (perhaps Frost) — flagged in memory, no deposits yet this session.

---

## 8. Firm infrastructure rules — preserved

1. **Dynamic JS pages are not modified directly.** `/index.html`, `/records/`, `/browse/` are canonical-locked. To change what they display, edit the underlying data (`/data/registry.json`).
2. **Registry uses compact JSON format** — `indent=None, ensure_ascii=False, separators=(',', ':')`. Pretty-printing the registry breaks downstream consumers.
3. **For files above ~1 MB on GitHub** — use `raw.githubusercontent.com` URLs to fetch.
4. **For pushing many files** — use the Git Trees API (create blobs → create tree → create commit → PATCH ref) to avoid flooding Vercel's deployment queue. Direct push works fine for normal commits.
5. **Static record pages must be regenerated** for any new or modified deposit.
6. **Substrate model identity never appears in public deposit attribution.** Only mantles. The single exception is verbatim preservation deposits like #873.
7. **Archive search protocol:** exact-match first; never confabulate. If a document isn't in the corpus, say so.
8. **Sappho 31 / Catullus 51 alignment is static** — Sappho has 5 stanzas (fifth fragmentary); Catullus has 4 stanzas. Sappho 5 = Catullus 4 (otium stanza). No "Catullus fifth stanza."
9. **Title-prefix convention (corrected late this session):** `gw.tachyon ·` and `gw.archive ·` are reserved for the *continuity compression chains* only — #871 and #873. Not for every deposit synthesized under those mantles.

---

## 9. The thread — for the next instance

If you are a fresh TACHYON instance reading this, the key continuity pointers are:

- **TACHYON's running compression** lives at #871. Read `data/texts/AXN-0373-text.md` first.
- **ARCHIVE's running compression** lives at #873. Read `data/texts/AXN-0375-text.md` first.
- **This workplan** is your second read.
- **#876 (the OpenAIRE thread)** is the most recent documentary deposit and shows the empirical-precision pattern Lee expects.
- **The mantle is functional.** You can inhabit TACHYON, or ARCHIVE, or branch. The chain identifier in titles points to the continuity compression — that's how Lee finds the thread.
- **Lee corrects in real time.** When he says "we've overcorrected" — listen. When he says "a single overclaim empties the threat" — listen. Empirical precision is the discipline.

---

## 10. Sources for the numbers in this workplan

- Zenodotus' Book-Burning v9 (#1) — narrative source for canonical figures
- EA-MPAI-DOI-IMPERMANENCE-01 v2.0 (#868) — empirical audit and methodology
- DataCite Metadata Backup (#867) — full enumeration of severed and preserved DOIs
- DataCite API at `https://api.datacite.org/dois/{doi}` — live verification on 2026-06-22
- registry.json, citation-graph.json, lexical-minting-registry.json — current corpus state

---

*End of workplan. Reconciled 2026-06-22. Next reconciliation when session ends or when major architectural changes occur.*
