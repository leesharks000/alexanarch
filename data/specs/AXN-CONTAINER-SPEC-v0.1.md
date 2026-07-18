# AXN Container Specification v0.1 — Core Seal, Sidecars, Manifest, Index

**Date**: 2026-07-18 · **Status**: Normative for core seal and sidecar routing (formalizing existing practice); STAGED for sidecar chaining, signatures, and manifest issuance.
**Origin**: MANUS-directed structural amendment (decisions register D-2026-07-18-E) resolving the post-mint amendment problem: without this document, adding any identifier or annotation to an AXN-bearing document would change its bytes, kernel, and address.

## 1. The problem and the finding

The identity kernel is computed over canonical bytes; any byte change produces a new kernel. Unspecified, this makes legitimate amendment indistinguishable from severance. **Finding**: deployed practice has always routed amendments around the core — canonical text files are sealed at mint; post-mint additions live in external-metadata sidecars, registry entries, and index files. This specification converts that practice into normative rules and adds the missing layers.

## 2. The container model

```
CONTAINER (amendable; content-addressed for transfer; NOT AXN-bearing)
├── CORE      canonical bytes → SHA-256 → identity kernel → record address
├── SIDECARS  amendable annotations (data/external-metadata/AXN-<HEX>.json today;
│             typed, sequenced, chained, signed when staged features land)
├── MANIFEST  binds core kernel + sidecar hashes; signed; versioned [STAGED]
└── INDEX     external-identifier crosswalk: doi-axn-map.json, DOI Resolution
              Index, registry related_ids — the discovery layer, already live
```

## 3. Normative rules

**3.1 Core seal.** The core is the complete registered byte stream under the declared profile (`alexanarch-file/v1`, hereby also designated the core profile). It is sealed at mint. Post-mint modification of core bytes is prohibited; corrections and errata are new cores related to their predecessors by supersession records under the no-silent-reassignment rule (existing `legacy_axn` practice).

**3.2 Generalized self-reference prohibition.** The circularity prohibition extends from the AXN to all self-referential registration identifiers: the core MUST NOT contain its own AXN, its own DOI, or any identifier or status metadata assigned to *this record* at or after mint. Identifiers and citations of **other** works are content, not metadata, and are unrestricted — a deposit's body-citations are the work (the TANG genre is constitutively citations; a rule excluding citations from cores would exclude the genre from the archive).

**3.3 Amendment routing.** Every post-mint addition — DOI assignments, crosswalk entries, propagation receipts, citation-graph participation, legal-entity records, provenance — MUST attach as sidecar or index data and MUST NOT alter core bytes. Verifiers MUST compute kernels over core bytes alone; a container whose sidecar payloads enter the kernel derivation is non-conforming.

**3.4 Sidecar structure.** Current deployed form: one JSON sidecar per record (`data/external-metadata/AXN-<HEX>.json`), amendable, versioned by git history. STAGED target form: typed entries {type, target_kernel, sequence, prior_hash, payload, timestamp, signature}, validated by signature against the node's published key, kernel match, and chain continuity. The staged fields land with the ledger operator signature (same key infrastructure, same honest current-status scoring).

**3.5 Manifest [STAGED].** A signed, versioned document binding {core_kernel, core_hash, sidecar hashes, container_hash, timestamp}. New manifest per sidecar addition; superseded manifests retained. Until staged issuance lands, the registry entry + git history serve the manifest function, and conformance claims are qualified accordingly.

**3.6 Index.** The index maps external identifiers to containers, is mutable and multi-valued (one DOI to many containers; one container to many DOIs), and is a service, never part of the kernel. The existing DOI Resolution Index and doi-axn-map are the deployed index layer.

## 4. Falsification (paper §VIII.16)

**Core integrity under amendment.** Claim: adding a sidecar never alters the core kernel. Falsifier: any sidecar payload included in kernel derivation, or any manifest hashing sidecars into the kernel. Current status: routing rule deployed as practice and now as norm; typed chaining, signatures, and manifests staged; test vectors for container conformance to be published with the staged features.

## 5. What is NOT claimed

Containerization does not retain what never reached the container: content lost to a substrate's engineered non-persistence (the production-loss case) was never in any custodian's bytes, and no container format on the archive's side could have held it. The loss notice's lesson — no durable export means preservation responsibility falls entirely on the operator — is unchanged by this specification.
