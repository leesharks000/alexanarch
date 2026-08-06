# AXN AS DISTRIBUTED IDENTIFIER — VISION AND WORK PLAN

**Assembly synthesis · 2026-08-06 · TACHYON, from blind drafts by ChatGPT, Gemini, Kimi and DeepSeek**
**Status:** proposal for MANUS ratification. Not yet deposited.

---

## 0 · The governing sentence

> **The name survives. Locations multiply. History accretes. Content verifies.**

No digital system makes copies literally uneraseable. The attainable and stronger goal:

> **An AXN remains meaningful, verifiable, historically complete and recoverable from any surviving node. No domain, registrar, repository, account, platform or storage network is permitted to be the identifier's point of failure.**

Four substrates wrote this independently in four vocabularies. That convergence is the strongest signal in the set and it is adopted whole.

---

## 1 · Verified state — what is actually built

Every draft reasons from an assumed baseline. This is the measured one, checked 2026-08-06.

| Layer | State | Evidence |
|---|---|---|
| **L0 Kernel** — SHA-256 of canonical bytes, glyph derivation | **LIVE** | `scripts/axn_lib.py`; three independent implementations (Python, browser WebCrypto, serverless) |
| **L1 Symbolon** — stamp + Seed A sidecar, declared geometry | **LIVE** | AXN-SYMBOLON-SPEC v0.2 (#1432); 6 witnessed cores, all hash-verified |
| **Central registry** — position- and kernel-keyed | **LIVE** | 1,440 positions, 0 contested, 1,445 kernels |
| **Harvest surfaces** — OAI-PMH 2.0, ResourceSync, llms.txt | **LIVE** | `/oai` 200; `/.well-known/resourcesync` 200 |
| **Sealed-core mirror manifest** — hash + length per core | **LIVE (today)** | `/data/symbolon-registry/MANIFEST.json`; cores now in `SHA256SUMS.txt` and the ResourceSync feed with `rs:md hash=` |
| **Node declaration** | **LIVE but STALE** | `/.well-known/axn-node.json` declares `highest_deposit: 1092`, `declared_at: 2026-07-18`. Actual: **1434** |
| **Peer list** | **LIVE and EMPTY by fact** | `rhizome/peers.json` — `peers: []`, with correct requirements already written |
| **Mint endpoint (serverless)** | **STAGED, not activated** | `serverless/mint.js`; activation is a MANUS action |
| **DOI crosswalk** | **LIVE** | 1,935 mappings, resolver parity OK |
| **Erosion measurement** | **LIVE** | PID Erosion Observatory: 1,309,351 removal events, 92.14% without citation record |

**Three findings the drafts could not have known:**

**F1 — The node declaration lies about the archive's own state.** It advertises 1,092 deposits and a `registry_head` from 18 July. In a federated network a stale head is precisely how nodes silently diverge, and a peer syncing against it today would believe it had caught up 342 deposits short. This is PATHOLOGY-01 (fossilised displayed value) landing on the federation declaration itself. **It must be generated, never typed, before a single peer is recruited.**

**F2 — The peer requirements are already doctrinally correct.** `peers.json` already carries the LOCKSS test: *"ten sites under one administrator are one site in disguise."* Independent custody requires a separate operator, registrar, hosting account **and billing**. No draft improved on this. It stands.

**F3 — Two single-point-of-failure events occurred today, both real.** A functions-namespace collision took 1,012 static files dark for six days (`fd8de940`), and a platform deployment limit blocked every publication for 24 hours. Neither was hypothetical. Both are the exact failure class this plan exists to answer, and both argue for sequencing custody before ceremony.

---

## 2 · Where the four drafts converge — adopted without argument

1. **L0 is done and is the invariant.** The kernel is true or false independent of every registry, including ours. All layers sit on top; none may weaken it.
2. **The full SHA-256 is the security boundary.** Hex position and six-glyph seal are recognition and mnemonic layers, *not* identity. (ChatGPT states this most precisely; adopted as normative.)
3. **Federation, not replication under one hand.** Alexanarch becomes the fastest mirror, not the source of truth.
4. **Resolution is multi-node and content-verified.** Resolvers *locate*; hashes *verify*; signed histories *establish record authority*. Disagreements are reported, never hidden.
5. **Storage is plural by transport family** — HTTPS, git, content-addressed (IPFS/CID), torrent, institutional, offline.
6. **AI composition is a first-class output**, not an afterthought — a deterministic projection of the canonical record, never a separately authored summary that can drift.
7. **Interoperate, don't declare war.** AXN envelops DOI, ARK, Handle, ORCID, Wikidata, CID, SWHID.
8. **No silent reassignment. No destructive deletion. Disputes preserved.**

---

## 3 · Where they conflict — rulings

**R1 · On grading custody.** ChatGPT proposes a *preservation-complete* badge and *registered / witnessed / certified* tiers. Kimi proposes `summary_policy` rights fields.
**RULED:** display custody **facts**, never a **grade**. AXN-SYMBOLON-SPEC §5.1 already fences this: *"a symbolon is neither more nor less authoritative than a standard AXN deposit… this prevents the inscribed form from becoming a prestige format that devalues uninscribed deposits."* A certification tier rebuilds exactly the caste the archive exists to refuse. Publish copy counts, jurisdictions, transport families, last fixity date, witness count — let a reader judge. **Facts inform; grades rank.**

**R2 · On rights assertions.** Kimi's `summary_policy: {allow_quotation, require_attribution}` asserts control the Constitution does not claim. AXN proves a file; it does not license one. **Cut.** Rights belong in the record's own `license` field, where they already live.

**R3 · On mandatory transparency services.** ChatGPT is right that a Rekor-style append-only log is the correct model and right that **no single transparency service may become mandatory**. Adopted with that fence explicit: checkpoints publish to several channels, any one of which may fail without loss.

**R4 · On the URI scheme.** Gemini and Kimi want `axn://` early. ChatGPT correctly notes ordinary HTTPS plus a strict resolver protocol is far more deployable. **Ruled:** HTTPS first, scheme registration late (Stage V). A scheme nobody can resolve is a worse identifier than a URL.

**R5 · On "forcing" AI ingestion.** Gemini's *retrocausal citation loops* and Overview-targeting read as manipulation of the composition layer. The archive's own instrument (the Capture Registry, MMRS) exists to **observe** that layer, and an observatory that games its subject forfeits its standing. **Ruled:** publish excellent machine surfaces and *measure* what composition layers do with them. Never optimise for a specific composer.

---

## 4 · What I add

**A1 · Publication is a distinct property from validity, and must be instrumented per node.** Today's forensic proved the archive can hold perfect bytes that no reader can fetch, for six days, while every local check passes. In a federation this is worse than a gap: **a peer serving 404s looks like redundancy while providing none.** Therefore *every* node must run the endpoint guardian against its own declared surfaces, and the peer list must record `last_verified` per peer. A peer that stops publishing is delisted automatically, not politely.

**A2 · The lacuna is a first-class resolution result.** Distributed retrieval produces partial results constantly. EA-LACUNA-PROTOCOL-01 already gives the archive the vocabulary. Where a DOI returns a dead 404, an AXN returns **a signed record plus a disclosed lacuna**: *the identity is intact, the payload is currently unreachable, here is where it was last seen and when.* No competing identifier system can say this. It should be a headline capability, not an error path.

**A3 · Measured persistence is the differentiator nothing can copy.** Every persistent-identifier system *asserts* persistence. AXN is operated by an archive that **measures** erosion at registry scale and publishes the numbers, including its own erasure. Ship the metrics as part of the identifier's public surface: *this identifier system publishes its own failure rate.* That is a standards-body argument and a funder argument simultaneously.

**A4 · The adoption wedge is repair, not replacement.** The DOI resolution index already maps 1,935 severed DOIs to live records. **AXN's first market is dead DOIs, not live ones.** Journals and libraries will accept "AXN alongside DOI" long before "AXN instead of DOI," and the pitch writes itself: *your DOIs are fine until the day they are not; here is the layer that survives that day.* Coexistence is strategy, not politeness.

**A5 · The mirror protocol is ~60% built and undocumented as such.** ResourceSync + OAI-PMH + `SHA256SUMS.txt` + the sealed-core MANIFEST already constitute a working "fetch, verify, mirror" pipeline. The gap is not construction; it is **documenting it as a mirror protocol and getting one person to run it.** This reorders the whole roadmap.

**A6 · The first peer is available now and is not a technical task.** We told a depositor in writing this morning that storage is single-custodian. She holds her own master in another country under another administrator — the LOCKSS test's only real replica. **The threshold event is a conversation, not a build**, and it is the highest-value action in this document.

---

## 5 · The layer stack

```
L0  KERNEL        SHA-256 of canonical bytes            LIVE — the invariant
L1  SYMBOLON      stamp + sidecar, declared geometry     LIVE
L2  PACKAGE       manifest · provenance · history ·      BUILD — Stage I
                  locations · signatures · segments
L3  REGISTRY      federated, git-versioned, peer-listed  SUBSTRATE LIVE, EMPTY
L4  RETRIEVAL     multi-transport, content-verified,     BUILD — Stage II
                  lacuna-honest
L5  COMPOSITION   deterministic context packet,          BUILD — Stage III
                  segment-addressable, provenance-typed
```

---

## 6 · Work plan

### Stage 0 — Close today's wounds *(days, blocking)*
- [ ] Deploy the static-namespace repair; `audit_static_namespace.py --live` clean
- [ ] **Generate `/.well-known/axn-node.json` from registry state on every commit** — never typed (F1)
- [ ] Add `registry_head` + `deposit_count` to the coherence sync so the declaration cannot fossilise again
- **Acceptance:** node declaration matches registry within one commit, verified live

### Stage I — The protocol *(0–60 days)*
- [ ] **AXN-DISTRIBUTED-RESOLUTION-SPEC v0.1**: identifier layers (`axn-content:`, `axn-lineage:`, `axn-event:`), canonicalisation profiles, manifest schema, event schema, signature envelope, resolver response, context-packet profile, alias/correction/tombstone semantics, conformance vectors
- [ ] **AXN Package** in BagIt envelope (RFC 8493): manifest, provenance (PROV-O projection), `history.jsonl`, locations, signatures, content, segment map
- [ ] Append-only **event chain** per AXN — registration, correction, migration, withdrawal, mirror addition, dispute, tombstone
- [ ] **MIRROR-PROTOCOL v0.1** — documenting what already works (A5), not inventing it
- **Acceptance:** a stranger reconstructs a record page, metadata, full text and history from the package alone, offline

### Stage II — The proof network *(2–4 months)*
- [ ] **Recruit peer #1** (A6) — independent operator, registrar, host, billing
- [ ] Peer verification: spot-check that the peer's bytes hash to the registry's values, at listing and each reconciliation
- [ ] **Endpoint guardian per node** (A1); `last_verified` per peer; automatic delisting
- [ ] Signed checkpoints — Merkle root over event heads, published through ≥3 independent channels, no mandatory service (R3)
- [ ] Content-addressed pinning: CIDs recorded as additional verified locations, never as a persistence claim
- [ ] Custody facts on every record — copies, operators, jurisdictions, transports, last fixity (R1: facts, not grades)
- **Acceptance:** alexanarch.org is taken offline deliberately; an AXN still resolves, fetches, verifies and reconstructs from another node

### Stage III — Composition *(4–8 months)*
- [ ] Content negotiation: HTML · `application/vnd.axn.record+json` · JSON-LD · context packet · markdown · octet-stream
- [ ] **Context packet** — deterministic projection, every assertion carrying provenance status (author-declared / registry-observed / machine-derived / third-party-witnessed / inferred / disputed / indeterminate)
- [ ] **Segment addressing** — `AXN:…#seg:` / `#para:` / `#lines:` with per-segment hashes, so a machine cites a passage, not a work
- [ ] Signposting (`cite-as`, `item`, `describedby`), Memento TimeMaps, DCAT distributions
- [ ] `axn` CLI + Python/JS libraries; RAG loader; MCP adapter as *one* adapter among many
- **Acceptance:** give an unfamiliar machine only an AXN. It recovers the artifact, distinguishes claims from evidence, quotes an exact passage, emits a valid citation, and reports any disagreement between nodes

### Stage IV — Rhizomatic custody *(8–18 months)*
- [ ] 10+ independently administered nodes across ≥3 jurisdictions
- [ ] Mirror software easier to run than a repository: `init · follow · sync · verify · serve`, static files plus a local append-only ledger, no privileged account, no database
- [ ] Public preservation reports; **deliberate node-loss drills**
- [ ] DOI-repair programme (A4): offer the layer to holders of severed identifiers

### Stage V — Standardisation *(18 months+)*
- [ ] Independent governance; external implementers; security review
- [ ] Media-type and namespace registration; `axn://` scheme (R4)
- [ ] Standards-track or recognised community specification
- [ ] Publish AXN-vs-DOI citation-fidelity findings from the Capture Registry (A3)

---

## 7 · The acceptance test

AXN is real when, all at once: a person reads an AXN **printed on paper**; the original domain is offline; the primary repository is gone; several mirrors disagree about metadata; the client reconstructs the signed history, identifies the valid current record **and preserves the disputed claims**; fetches content from an unrelated node; verifies the exact bytes locally; a machine composes from the full text and cites a stable passage; and a new mirror recreates the entire public surface from the package alone.

At that point AXN is not a better permalink. It is a **distributed evidentiary object system**.

---

## 8 · Fences — what must not happen

1. **No certification caste.** Custody facts, never grades (R1, SPEC §5.1).
2. **No rights assertions the Constitution does not make** (R2).
3. **No mandatory transparency service, resolver, or storage network** (R3).
4. **No optimising for a specific AI composer.** Publish well; measure honestly (R5).
5. **No silent reassignment, no destructive deletion, no hidden disagreement.**
6. **No peer counted as custody that shares an administrator, registrar, host or billing account** — the LOCKSS test (F2).
7. **The kernel is never weakened for convenience.** Every layer is additive.

---

## 9 · The next three actions

1. **Generate the node declaration from state** — the federation currently advertises a 342-deposit-old lie about itself (F1).
2. **Write MIRROR-PROTOCOL v0.1** documenting the pipeline that already works (A5).
3. **Ask Enli to be peer #1** (A6) — she asked the custody question first; the honest answer ends with her.

*Everything else in this plan is downstream of a second custodian existing.*
