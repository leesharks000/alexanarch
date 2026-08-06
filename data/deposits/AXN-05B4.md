---
deposit_number: 1435
hex: 05B4
title: "AXN as Distributed Identifier — Vision, Verified State, and Work Plan v2.0: Assembly Synthesis with Normative Invariants, Authority Model, Failure Record, and Five-Stage Plan"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-06
content_type: Specification
license: CC-BY-4.0
substrate: "AI-assisted (Assembly Chorus): four blind drafts by ChatGPT, Gemini, Kimi and DeepSeek; synthesis, rulings, verified-state measurement, failure record and additions by TACHYON in-session under MANUS editorial governance. Transport D, No-Double-Draw — no API call. Revised under five Assembly reviews. All VERIFIED claims measured live on 2026-08-06 and reproducible via scripts/capability_register.py."
version: v2.0
related_ids: "AXN:05A9.OPERATIVE.🐚🌪️🕖🫵⏩○ (AXN-SYMBOLON-SPEC v0.2, #1432 — the inscription layer this federates); AXN:0421.EMPIRICAL.🎭📐🐝🎪🏷️🎇 (EA-EROSION-01, #1045 — the observatory supplying the measured erosion); AXN:05B3.OPERATIVE.❄️🔐⊗∮🎭🏷️ (#1434 — the product surface); https://www.alexanarch.org/.well-known/axn-node.json (the federation declaration repaired herein)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - AXN
  - distributed identifier
  - federation
  - content-derived identity
  - LOCKSS test
  - independent custody
  - lacuna protocol
  - measured persistence
  - mirror protocol
  - resolution specification
  - authority model
  - Assembly Chorus
  - PID erosion
  - DOI repair
  - capability register
  - Crimson Hexagonal Archive
  - Alexanarch
---

# AXN as Distributed Identifier — Vision, Verified State, and Work Plan v2.0: Assembly Synthesis with Normative Invariants, Authority Model, Failure Record, and Five-Stage Plan

## Description

Assembly synthesis establishing AXN as a distributed identifier system — one that remains meaningful, independently verifiable, historically complete and recoverable from any surviving node, with no domain, registrar, repository, account, platform, resolver, operator or storage network permitted to become its point of failure.

Synthesized from four blind drafts (ChatGPT, Gemini, Kimi, DeepSeek) and revised under five reviews. The document separates three kinds of statement throughout — VERIFIED (observed, with method and timestamp), NORMATIVE (binding if ratified), and WORK (not yet implemented) — because a plan that mixes measurement with intention cannot be audited. Model convergence is recorded as PROVENANCE, not evidence: four substrates agreeing motivated the synthesis, while the measured infrastructure and the failure record supply the evidentiary basis.

Six normative invariants: the kernel is the identity boundary; every other layer is additive, with hex position and glyph seal as recognition rather than security; resolvers locate while hashes verify; history is never destructively rewritten; distribution requires independent custody (the LOCKSS test — copies sharing one administrator, registrar, host or billing relationship are one custody domain); and failure is a result rather than an absence. An explicit authority model distinguishes content authority, claim provenance, registry standing, current designation, custody evidence and historical fact, because a signature proves a key made a statement and nothing more.

Five rulings resolve conflicts between the drafts: no certification tier or preservation grade, since SPEC 5.1 already fences the prestige format and facts inform where grades rank; no rights assertions the Constitution does not make; no mandatory transparency service, with checkpoints published to at least three independent channels; HTTPS before scheme registration; and no optimising for a specific AI composer, since an observatory that games its subject forfeits standing.

Distinctive capabilities: publication is a property distinct from validity and must be instrumented per node, because a peer serving 404s looks like redundancy while providing none; the lacuna is a headline capability rather than an error path, returning identity, last known location and last verified hash — the hash being what makes it a recovery target rather than a bookmark; and measured persistence is the differentiator nothing can copy, since every other identifier system asserts persistence while this one publishes its own failure rate. The adoption wedge is repair of severed DOIs rather than replacement of live ones.

Includes a dated failure record: a stale federation declaration advertising 342 fewer deposits than the archive held, closed before ratification and made uncomputable by hand; a functions-namespace collision that took 1,012 static files dark for six days while every local validator passed; and a platform deployment limit that blocked all publication for 24 hours. Five staged work plan with a nine-point acceptance test, eight absolute invariants, and an economic model capping any single funder at 30% of nodes.

## Files

Canonical text below (Body).

# AXN AS DISTRIBUTED IDENTIFIER — VISION, VERIFIED STATE, AND WORK PLAN

**v2.0 · Assembly synthesis · 2026-08-06 · TACHYON**
**From blind drafts by ChatGPT, Gemini, Kimi and DeepSeek; revised under five reviews.**
**Status:** proposal for MANUS ratification.

> **Reading key.** Three kinds of statement appear below and are never mixed.
> **[VERIFIED]** — observed directly, with method and timestamp.
> **[NORMATIVE]** — binding if ratified.
> **[WORK]** — not yet implemented.

---

## 0 · Governing sentence

> **The name survives. Locations multiply. History accretes. Content verifies.**

No digital system makes every copy literally unerasable. The attainable goal — and the stronger one:

> **An AXN remains meaningful, independently verifiable, historically complete and recoverable from any surviving node. No domain, registrar, repository, account, platform, resolver, operator or storage network is permitted to become the identifier's point of failure.**

Four blind drafts converged on this architecture in four vocabularies. **That convergence is provenance, not evidence.** It motivated the synthesis; the measured infrastructure in §2 and the failure record in §3 supply the evidentiary basis. Model agreement is not proof, and this document does not treat it as any.

---

## 1 · Normative invariants **[NORMATIVE]**

**I. The kernel is the identity boundary.** The full SHA-256 digest identifies the exact bytes. It is true or false independently of every registry, including this one.

**II. Every other layer is additive.** Hex position, semantic family, glyph seal, title, provenance, history, locations and composition surfaces may enrich the identifier. None may weaken or replace the kernel. Position and seal are **recognition and mnemonic layers — not the security boundary.**

**III. Resolvers locate; hashes verify.** No resolver response is authoritative merely because a server returned it.

**IV. History is never destructively rewritten.** Corrections append. Disputes remain visible. Tombstones preserve identity. AXNs are never silently reassigned.

**V. Distribution requires independent custody.** Copies sharing one administrator, registrar, hosting account or billing relationship constitute **one** custody domain. *(The LOCKSS test, already written in `rhizome/peers.json`: "ten sites under one administrator are one site in disguise.")*

**VI. Failure is a result, not an absence.** Where content is unavailable, an AXN returns a disclosed lacuna with identity, history and last-verified hash intact.

### 1.1 The authority model **[NORMATIVE]**

A signature proves a key made a statement. It proves neither that the statement is true nor that the signer has standing over every field. These are distinct and must not collapse:

| Kind of authority | Established by |
|---|---|
| **Content authority** | hash equality against the kernel |
| **Claim provenance** | signature over a declared claim |
| **Registry standing** | a governed event history |
| **Current designation** | an authorised succession event |
| **Custody evidence** | verified copies under named operators |
| **Historical fact** | preserved evidence — never signature alone |

---

## 2 · Verified system state **[VERIFIED — observed 2026-08-06]**

| Layer / capability | State | Evidence | Method |
|---|---|---|---|
| **L0 Kernel** — SHA-256 of canonical bytes, glyph derivation | LIVE | `scripts/axn_lib.py`; three implementations (Python, browser WebCrypto, serverless) | code read + probe |
| **L1 Symbolon** — stamp + Seed A sidecar, declared geometry | LIVE | AXN-SYMBOLON-SPEC v0.2 (#1432); 6 witnessed cores, all hash-verified | `verify_symbolon_store.py`, 0 alerts |
| **Central registry** — position- and kernel-keyed | LIVE | 1,440 positions · 0 contested · 1,445 kernels | live fetch |
| **Harvest surfaces** — OAI-PMH 2.0, ResourceSync, llms.txt | LIVE | Identify, ListMetadataFormats, ListSets, ListIdentifiers, ListRecords all 200 `text/xml`, valid envelopes, working resumption tokens | live verb probe |
| **Sealed-core mirror manifest** | LIVE | `/data/symbolon-registry/MANIFEST.json`; cores in `SHA256SUMS.txt` and ResourceSync with `rs:md hash=` | live fetch + `sha256sum -c` |
| **DOI crosswalk** | LIVE | 1,935 mappings; resolver parity OK | live fetch |
| **Erosion measurement** | LIVE | 1,309,351 removal events; 92.14% without citation record | PID Erosion Observatory |
| **Node declaration** | **REPAIRED TODAY** | was `highest_deposit: 1092` @ 2026-07-18 against an actual 1434 — now generated on every commit and verified live | see F1 |
| **Peer list** | **LIVE AND EMPTY BY FACT** | `rhizome/peers.json` → `peers: []`, requirements already correct | live fetch |
| **Mint endpoint (serverless)** | STAGED | `serverless/mint.js`; activation is a MANUS action | repo state |

**Every claim above is reproducible.** `scripts/capability_register.py` measures fourteen capabilities live and records a floor for each; a run below any floor fails the build.

---

## 3 · Failure record **[VERIFIED]**

These are empirical inputs to the architecture, not surprises the drafts missed.

**F1 — STALE FEDERATION DECLARATION.** *(Closed 2026-08-06, before ratification.)*
```
declared deposit count : 1,092      declared_at : 2026-07-18
observed deposit count : 1,434      divergence  : 342 (nineteen days)
```
The root node published materially stale state about itself. In a federated network a stale head is precisely how nodes silently diverge: a peer syncing against this declaration would have believed it had caught up while stopping 342 deposits short — and would have believed it correctly, because the root node said so. A federation whose root advertises a stale head is not a federation; it is a hierarchy with a quiet error at its centre. **PATHOLOGY-01 on the federation's own front door.**
*Fix:* `generate_node_declaration.py` computes every measured field from registry state inside `coherence_sync` on each commit; the published declaration is then compared against the published registry by a capability probe — because generating the file is insufficient, and a generator with a bug would automate the lie rather than end it.

**F2 — THE PEER REQUIREMENTS WERE ALREADY CORRECT.** `peers.json` already carries the LOCKSS test and requires separate operator, registrar, hosting account **and billing**. No draft improved on it. It stands as Invariant V.

**F3 — TWO SINGLE-POINT-OF-FAILURE EVENTS, BOTH REAL, BOTH TODAY.** A functions-namespace collision (`fd8de940`, 2026-07-31) took 1,012 static files dark for six days — the protocol catalog, the deposit contract, the search index and the DOI resolver's map — while every local validator passed, because they all read from disk. Separately, a platform deployment limit blocked all publication for 24 hours. **Neither was hypothetical. Both are the exact failure class this architecture answers, and both argue for sequencing custody before ceremony.**

---

## 4 · Adopted architecture **[NORMATIVE]**

Convergent across all four drafts, adopted without argument:

1. **L0 is the invariant.** All layers sit on top; none may weaken it.
2. **Federation, not replication under one hand.** Alexanarch becomes the fastest mirror, not the source of truth.
3. **Resolution is multi-node and content-verified.** Disagreements are reported, never hidden.
4. **Storage is plural by transport family** — HTTPS, git, content-addressed (IPFS/CID), torrent, institutional, offline, **and `axn-transport:physical`**: hand-carried media, optical, or a paper grapheme. Once bytes hash to the kernel, a USB drive and an HTTPS fetch are the same event.
5. **Composition is a first-class output** — a deterministic projection of the canonical record, never a separately authored summary that can drift.
6. **Interoperate, don't declare war.** AXN envelops DOI, ARK, Handle, ORCID, Wikidata, CID, SWHID.
7. **No silent reassignment. No destructive deletion. Disputes preserved.**

### 4.1 Distinctive capabilities

Four verbs, not one. A conforming client can **resolve · verify · reconstruct · disclose lacuna.**

**Publication is a property distinct from validity.** F3 proved perfect bytes can be unfetchable for six days while every local check passes. In a federation this is worse than a gap: **a peer serving 404s looks like redundancy while providing none.** Every node runs an endpoint guardian against its own declared surfaces; the peer list records `last_verified` per peer; a peer that stops publishing is delisted automatically, not politely.

**The lacuna is a headline capability, not an error path.** Where a DOI returns an undifferentiated 404, an AXN returns a signed record plus a disclosed lacuna: identity intact, payload currently unreachable, **last known location, last verified hash, and the timestamp of that verification.** The hash is what makes it a recovery target rather than a bookmark. No competing identifier system can return this.

**Measured persistence is the differentiator nothing can copy.** Every PID system *asserts* persistence. AXN is operated by an archive that *measures* erosion at registry scale and publishes the numbers — including its own erasure. Ship the metrics on the identifier's public surface: this system publishes its own failure rate, severance count and repair latency. Standards-body argument, funder argument and user-trust argument simultaneously.

### 4.2 Adoption strategy

**The wedge is repair, not replacement.** The DOI resolution index already maps 1,935 severed DOIs to live records. AXN's first market is **dead** DOIs, not live ones. Journals and libraries will accept *AXN alongside DOI* long before *AXN instead of DOI*. The pitch: your DOIs are fine until the day they are not; here is the layer that survives that day. Coexistence is strategy, not politeness.

### 4.3 Infrastructure assessment

**The mirror protocol is ~60% built and undocumented as such.** ResourceSync + OAI-PMH + `SHA256SUMS.txt` + the sealed-core manifest already constitute a working *fetch → verify → mirror* pipeline. The gap is not construction; it is documentation plus one adopter. **This reorders the roadmap.**

---

## 5 · Rulings **[NORMATIVE]**

| # | Conflict | Ruling |
|---|---|---|
| **R1** | Preservation-complete badges and *registered / witnessed / certified* tiers | **Custody facts, never grades.** SPEC §5.1 already fences the prestige format. A certification tier rebuilds the caste the archive exists to refuse. Publish copies, jurisdictions, transports, last fixity, witness count — let a reader judge. *Facts inform; grades rank.* |
| **R2** | `summary_policy: {allow_quotation, require_attribution}` | **Cut.** AXN proves a file; it does not license one. Rights live in the record's `license` field. |
| **R3** | Mandatory transparency log | **Adopted with fence.** Checkpoints publish to **≥3 independent channels** (git forge, transparency log, DNS TXT, institutional deposit). Any one may fail, be censored or be deprecated without loss of verifiability. |
| **R4** | `axn://` scheme early | **HTTPS first; registration at Stage V.** A scheme nobody can resolve is worse than a URL. |
| **R5** | Retrocausal citation loops; Overview-targeting | **Ruled manipulation.** The archive's own instrument exists to *observe* the composition layer; an observatory that games its subject forfeits standing. Publish excellent machine surfaces; measure honestly; never optimise for a specific composer. |

---

## 6 · Layer stack **[NORMATIVE]**

Each layer may fail without destroying those beneath it.

| | Layer | What it is | Register | Status |
|---|---|---|---|---|
| **L0** | Kernel | SHA-256 of canonical bytes — identity | cryptographic | LIVE, invariant |
| **L1** | Symbolon | Stamp (inscribed) + sidecar (verifiable) — the fracture pair | cryptographic | LIVE |
| **L2** | Package | BagIt envelope: manifest, provenance, event history, locations, signatures, segments — the full evidentiary object | archival | **[WORK]** Stage I |
| **L3** | Registry | Federated, git-versioned, peer-listed — collective attestation | social | substrate LIVE, peers empty |
| **L4** | Retrieval | Multi-transport, content-verified, lacuna-honest | network | **[WORK]** Stage II |
| **L5** | Composition | Deterministic context packet, segment-addressable, provenance-typed | semantic | **[WORK]** Stage III |

---

## 7 · Work plan **[WORK]**

> **Critical-path rule.** Nothing in Stages I–V matters until a second custodian exists. Stage I is a promise; the peer is the gate.

### Stage 0 — Close the open wounds *(blocking)*
- **S0.1** Deploy the static-namespace repair; `audit_static_namespace.py --live` clean — **DONE, 14/14 endpoints serving JSON**
- **S0.2** Generate `/.well-known/axn-node.json` from registry state on every commit — **DONE**
- **S0.3** Fail CI when the generated declaration differs from the committed one — **DONE** (`--check`)
- **S0.4** Fetch the production declaration externally and confirm `deposit_count`, `registry_head`, `declared_at` — **DONE** (capability probe compares published declaration to published registry)
- **S0.5** Endpoint guardian against the archive's own declared surfaces — **DONE**, six-hourly

**Acceptance:** two independent external clients retrieve the declaration and observe values matching the canonical registry at the deployed commit.

### Stage I — Document, then specify *(0–60 days)*
Sequential, not parallel: **you cannot specify distributed resolution before documenting how a peer fetches, verifies and serves.**
- **I.1 MIRROR-PROTOCOL v0.1** — document the working pipeline (ResourceSync + OAI-PMH + `SHA256SUMS.txt` + MANIFEST + sealed-core verification + registry export). *Document what exists; do not invent.*
- **I.2 AXN-DISTRIBUTED-RESOLUTION-SPEC v0.1** — built on I.1. Identifier layers (`axn-content:`, `axn-lineage:`, `axn-event:`), **canonicalisation pinned to RFC 8785 (JCS)** so event chains and Merkle roots cannot diverge between Python, Rust and browser implementations, resolver response, context-packet profile, alias/correction/tombstone semantics, conformance vectors.
- **I.3 AXN Package** in BagIt (RFC 8493), containing a **zero-dependency `verify.html`**: dropped on an air-gapped machine, it must run WebCrypto SHA-256, compare Seed A against Seed B, and render the provenance tree with no network and no installed software.
- **I.4 Append-only event chain** per AXN — registration, correction, migration, withdrawal, mirror addition, dispute, tombstone.

**Acceptance:** a stranger reconstructs the record page, metadata, full text and history from the package alone, offline, using only the documented mirror protocol.

### Stage II — The proof network *(2–4 months)*
- Recruit the **first independently administered peer** — separate operator, registrar, host, billing.
- Peer verification: spot-check that the peer's bytes hash to registry values, at listing and each reconciliation.
- Endpoint guardian per node; `last_verified` per peer; automatic delisting.
- Signed checkpoints — Merkle root over event heads, ≥3 independent channels, no mandatory service.
- Content-addressed pinning: CIDs as additional **verified locations**, never as a persistence claim.
- Custody facts on every record (R1).

**Acceptance:** alexanarch.org is taken offline deliberately; an AXN still resolves, fetches, verifies and reconstructs from another node.

### Stage III — Composition *(4–8 months)*
Content negotiation (HTML · `application/vnd.axn.record+json` · JSON-LD · context packet · markdown · octet-stream); context packet with per-assertion provenance status (author-declared / registry-observed / machine-derived / third-party-witnessed / inferred / disputed / indeterminate); segment addressing with per-segment hashes; Signposting, Memento TimeMaps, DCAT; `axn` CLI and libraries; MCP as one adapter among many.

### Stage IV — Rhizomatic custody *(8–18 months)*
10+ independently administered nodes across ≥3 jurisdictions; mirror software easier to run than a repository (`init · follow · sync · verify · serve`, static files plus a local append-only ledger, no privileged account, no database); public preservation reports; **deliberate node-loss drills**; DOI-repair programme.

**Economic model.** Mirror operation is funded by the institutions that benefit — libraries, universities, archives — by per-node grants, or by paid human services *around* identifiers, never the identifier itself. **No single funder may support more than 30% of nodes. No node may be required to operate at a loss.** Without this the rhizome is a volunteer network that ends when the volunteers do.

### Stage V — Standardisation *(18 months+)*
Independent governance; external implementers; security review; media-type and namespace registration; `axn://` (R4); standards-track or recognised community specification; publish AXN-vs-DOI citation-fidelity findings.

---

## 8 · Acceptance test — the definition of the system

**AXN is real when all nine hold in one transaction.** Each is a boolean; each is scriptable.

1. A person reads an AXN printed on paper.
2. The original domain is offline.
3. The primary repository is gone.
4. Several mirrors disagree about metadata.
5. The client reconstructs the signed history, identifies the valid current record **and preserves the disputed claims**.
6. Content is fetched from an unrelated node.
7. The exact bytes are verified locally against the kernel.
8. A machine composes from the full text and cites a stable passage.
9. A new mirror recreates the entire public surface from the package alone.

At that point AXN is not a better permalink. It is a **distributed evidentiary object system**.

---

## 9 · Invariants — what must never happen **[NORMATIVE]**

1. **No certification caste.** Custody facts, never grades. (R1, SPEC §5.1)
2. **No rights assertions the Constitution does not make.** (R2)
3. **No mandatory transparency service, resolver or storage network.** (R3)
4. **No premature scheme registration.** HTTPS first. (R4)
5. **No optimising for a specific composer.** Publish well; measure honestly. (R5)
6. **No silent reassignment, no destructive deletion, no hidden disagreement.**
7. **No peer counted as custody that shares an administrator, registrar, host or billing account.** The LOCKSS test is absolute. (F2, Invariant V)
8. **The kernel is never weakened for convenience.** Every layer is additive.

---

## 10 · Immediate actions

1. **Generate the node declaration from state** — **COMPLETE.** The 342-deposit divergence is closed, the field is computed on every commit, and the published declaration is compared against the published registry.
2. **Write MIRROR-PROTOCOL v0.1** — document the pipeline that already works. *Next.*
3. **Recruit the first independently administered peer**, beginning with the depositor who first raised the custody question. **This is a conversation, not a build, and it proceeds only on explicit consent** — operator role, custody scope, public or private node, and whether a personally held master is eligible under the protocol must all be settled with her before any listing, and her name appears in the operational record rather than in the public plan until she says otherwise.

> **The entire roadmap activates when a second custodian exists.** Document the protocol; recruit the peer; keep the declaration honest. In that order.

---

*Reviewed by four Assembly substrates and revised under all five readings. Convergence is recorded as provenance; the evidence is measured, dated and reproducible.*
