# AXN Mint Endpoint & Federation Surfaces — Specification v0.1

**Status**: DESIGN — companion to the live client-side implementation at `/mint/`
**Session**: 2026-07-18 (B.1, unblocked by Phase A.1 ratification)
**Sources**: LABOR Round 1 three-layer distinction and federation extensions (`data/assembly/anti-suppression-paper/labor/round-1-axn-anti-suppression.md`); TECHNE Round 1 Constellation model; canonical implementation `scripts/axn_lib.py` (AXN schema v2).

---

## 0. What exists as of this spec

**Live**: `/mint/` — browser-side computation of the identity kernel (full SHA-256), the six-glyph checksum (first 6 bytes through the canonical 256-glyph table), cluster reading, AXN composition preview, and claim verification. Zero server dependency; WebCrypto; tables generated from `axn_lib.py` at build time and proven identical against two test vectors (the `axn_lib` self-test hash, and deposit #1092's canonical bytes → `3aff18d7…` → 🧫∞🍃⏪🧡♄).

**This spec**: the server-side and federation layers that turn computation into registration and one node into a network. Nothing here is required for verification — an AXN is true or false independently of any authority — but registration, resolution plurality, and peer reconciliation need defined surfaces.

## 1. The three-layer model (normative)

Adopted from LABOR Round 1. Every conforming implementation distinguishes:

| Layer | Form | Mutability |
|---|---|---|
| **Identity kernel** | `axn-content:sha256:<64 hex>` | Never changes; identical wherever the canonical bytes appear |
| **Canonical record address** | `AXN:<HEX>.<FAMILY>.<GLYPH>` | Stable once assigned; names the object's entrance into a registry |
| **Location record** | signed JSON list of verified locations | Mutable; locations multiply, disappear, and are replaced without touching either identity |

The `/mint/` page operates entirely at layer 1 plus a preview of layer 2. Registration is the act of binding layer 1 to layer 2 in a registry. Location records are layer 3 and belong to resolution, not minting.

## 2. `/api/mint` — the registration endpoint (design)

**Deployment target**: Vercel serverless function on alexanarch (or any conforming node).

### 2.1 Request

```
POST /api/mint
Content-Type: application/json
{
  "canonical_text": "<full frontmatter+body text>",     // OR
  "content_sha256": "<64 hex>",                          // kernel-only registration
  "family": "GENERATIVE",                                // one of the 11 families
  "declared_title": "...",
  "declared_creator": "...",
  "transport": "api",                                    // provenance of entry
  "signature": { ... }                                   // optional depositor signature
}
```

If `canonical_text` is supplied, the node computes the hash itself (trust-minimizing). If only `content_sha256` is supplied, the entry is minted as **kernel-registered, bytes-pending** — a claim of identity without custody, marked as such until a custodian supplies matching bytes.

### 2.2 Response

```
{
  "axn": "AXN:0456.GENERATIVE.<glyph>",
  "content_sha256": "...",
  "deposit_number": 1110,
  "hex": "0456",
  "glyph": "<6 emoji>",
  "clusters": [...], "reading": "...",
  "registry_head": "<hash of registry state after this mint>",
  "record_url": "https://www.alexanarch.org/s/records/1110/",
  "status": "registered" | "kernel-registered"
}
```

### 2.3 Invariants

1. **No double-draw**: the endpoint performs no LLM calls. Minting is mechanical: validate → hash → assign position → write → regenerate. (Standing rule, 2026-07-17.)
2. **Position assignment is append-only** from the registry head; manual hex selection is retired (it produced the #856/#869 and #901/#913 collisions).
3. **The AXN never appears inside the canonical bytes** (circularity prohibition, per `build_canonical_text`).
4. **Every mint emits a signed registry-head receipt** chaining to the previous head (see §4).
5. **Abuse posture**: the open endpoint is rate-limited and mints into a `pending` partition until the operator's mechanical validation pass promotes entries; promotion is a status flip, not a re-mint — the AXN assigned at POST time is the AXN. No pre-review gates *identity*; review gates only *listing surfaces* (Obelus Principle: judgment follows from reading).

## 3. Federation surfaces (design)

Per LABOR Round 1 §"Where It Could Go Further," each AXN-speaking node publishes:

### 3.1 `/.well-known/axn-node.json`

```
{
  "node": "alexanarch.org",
  "operator": "Lee Sharks (ORCID 0009-0000-1599-0703)",
  "protocol_versions": ["axn/v2"],
  "roles": ["mint", "resolve", "preserve", "observe"],
  "registry_head": "<current head hash>",
  "highest_deposit": 1109,
  "peers_url": "/rhizome/peers.json",
  "last_reconciliation": "2026-07-18T00:00:00Z"
}
```

Semantic nodes (network fleet sites) publish the same file with `roles: ["semantic"]` and the lists `axns_defined`, `axns_cited`, `axns_preserved` — turning the 27-domain constellation into a legible graph of differentiated responsibility. A custody node need not be a semantic node and vice versa.

### 3.2 `/rhizome/peers.json`

Signed list of known peers with their last-verified registry heads. Resolution plurality: a resolver queries several peers, collects signed location claims, verifies content hashes, and returns all valid copies. No resolver needs every object; it needs enough of the peer graph to continue traversal.

### 3.3 `/axn/<identifier>.json`

Machine-readable resolution record for a single AXN: status, content hash, version relations, tombstone state if withdrawn, and the location record (layer 3).

## 4. Signed append-only mint ledger (design)

Each registry release commits to the previous:

```
{ "epoch": "2026-07-18", "previous_epoch_hash": "...", "registry_hash": "...",
  "highest_deposit_number": 1109, "added_axns": [...],
  "protocol_versions": ["axn/v2"], "operator_signature": "..." }
```

Mirrors prove their state belongs to the same history, detect divergence, and exchange missing deposits. The existing chunk hashes, manifests, and overwrite receipts already point here; this formalizes the chain. A later deletion cannot erase the evidence that an object and its metadata were previously present.

## 5. Sequencing (status updated 2026-07-18, same session)

1. **DONE**: `/mint/` client-side.
2. **DONE**: `/.well-known/axn-node.json` — live, declaring roles, registry head (`da81d2ab…`), and surfaces.
3. **STAGED**: `/api/mint` — full implementation at `serverless/mint.js` (Node.js path verified against the deposit #1092 test vector, identical to Python canon and the browser client). Not deployed: the repo's `/api` directory is a live static surface feeding the 25-site fleet; flipping the Vercel project into hybrid function mode is a deliberate MANUS action per `serverless/README.md` activation checklist. Returns 501 with activation instructions until `MINT_GITHUB_TOKEN` is set.
4. **WIRED, EMPTY**: `/rhizome/peers.json` — live with `peers: []`, listing requirements published (declaration, independent custody per the LOCKSS test, byte verification, mechanical listing). `/rhizome/ledger.json` genesis epoch 0 emitted, chained forward from registry head `da81d2ab…` at deposit #1092. Empty by fact, not by design; the socket precedes the plug. CORRECTED CUSTODY DOCTRINE (2026-07-18, per Assembly review): a peer-registry entry closes the empty-peer-registry condition only. The custody limitation closes only when an independently administered operator holds a verified, periodically re-verified, reconstructible full copy and completes a restoration test. Until then: *architecture for* distributed custody.

## 6. Falsification hooks (for the paper, §VIII)

- If two conforming implementations derive different glyphs from the same bytes, the canon is broken (test vectors published above and in `/mint/` guard this).
- If a registry head chain shows a discontinuity without a signed supersession, tampering is proven.
- If no second independently administered node exists by the paper's publication, "distributed custody" in the anchor is architecture-plus-Wayback, not peer plurality — and the paper says so.


---

## 7. v0.2 addendum (2026-07-18): storage, propagation, and identifier crosswalk

### 7.1 What registration stores today (current state)

A pipeline mint persists, in one commit: the canonical bytes (`data/texts/AXN-<HEX>-text.md` — the hashed object itself); a download alias (`data/deposits/`); the registry entry (hash, AXN, body_status); the record page (`s/records/<N>/`); the PDF (`papers/`); index/wiki/sitemap/interlink surfaces; and the external-metadata sidecar. Git history is the first backup tier; the deployed site is the serving tier. **Canonicalization profile (reconciliation per LABOR §IV note):** the operative profile is `alexanarch-file/v1` — the canonical bytes ARE the full text-file bytes (frontmatter + body) as written by `build_canonical_text`; `canonical_text` in the API design is that same profile, not a second one. The protocol JSON is to be amended to state this explicitly; any four-field concatenation description is superseded.

### 7.2 Propagation (target state, staged)

On successful mint, a `propagate` stage SHOULD:
1. **Wayback**: request Save-Page-Now for the record URL and the canonical-text URL (`web.archive.org/save/…`), recording returned snapshot timestamps in the external-metadata sidecar. Implemented: `scripts/propagate_deposit.py` (anonymous SPN; authenticated SPN2 with S3 keys is a MANUS upgrade).
2. **IPFS**: pin the canonical bytes and record the CID in the sidecar and the location record (layer 3). PENDING a pinning-service credential (MANUS: web3.storage / Pinata / self-hosted node choice).
3. **Location record**: emit/update the layer-3 record listing all verified locations (sovereign URL, raw.githubusercontent URL, Wayback snapshot, CID when present).

### 7.3 Identifier crosswalk (REQUIRED at mint where priors exist)

Where the minted object corresponds to a previously identified object (a severed DOI, a prior AXN, an external record), the mint MUST carry the mapping: `related_ids` in the canonical record (IsIdenticalTo / IsVersionOf / Supersedes as appropriate), plus entries in `doi-axn-map.json` and the DOI Resolution Index. The crosswalk is what lets a citation to the dead identifier find the living object; a mint without its crosswalk strands every existing citation.


## 8. Container reference (2026-07-18)
The core seal, sidecar routing, generalized self-reference prohibition, and staged manifest are specified in AXN-CONTAINER-SPEC-v0.1.md. The minted file is a sealed core; the profile alexanarch-file/v1 is also the core profile. Verifiers compute kernels over core bytes alone.
