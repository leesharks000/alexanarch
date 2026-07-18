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

**3.2 Content-agnosticism (MANUS ruling, 2026-07-18, full rejection of core-content restrictions).** The canonical form is whatever gets minted. The core carries NO content restrictions: citations, apparatus, prior identifiers — including the document's own previously assigned identifiers (a recovered deposit's legacy DOI, a prior AXN from a superseded mint) — are all admissible core content, because they existed before these bytes were sealed. Any typological restriction on core content violates the archive's content-agnosticism principle and would render the recovered corpus non-conforming (rescued deposits carry their own legacy DOIs in frontmatter). The distinction between core and sidecar is **temporal, not typological**: what exists at mint may be in the core; what arrives after mint attaches beside it. The sole surviving constraint is the original mathematical one — the not-yet-derived kernel and address cannot occur in the bytes they are derived from (fixed-point instability), which is an impossibility, not a policy.

**3.3 Amendment routing.** Every post-mint addition — DOI assignments, crosswalk entries, propagation receipts, citation-graph participation, legal-entity records, provenance — MUST attach as sidecar or index data and MUST NOT alter core bytes. Verifiers MUST compute kernels over core bytes alone; a container whose sidecar payloads enter the kernel derivation is non-conforming.

**3.4 Sidecar structure.** Current deployed form: one JSON sidecar per record (`data/external-metadata/AXN-<HEX>.json`), amendable, versioned by git history. STAGED target form: typed entries {type, target_kernel, sequence, prior_hash, payload, timestamp, signature}, validated by signature against the node's published key, kernel match, and chain continuity. The staged fields land with the ledger operator signature (same key infrastructure, same honest current-status scoring).

**3.5 Manifest [STAGED].** A signed, versioned document binding {core_kernel, core_hash, sidecar hashes, container_hash, timestamp}. New manifest per sidecar addition; superseded manifests retained. Until staged issuance lands, the registry entry + git history serve the manifest function, and conformance claims are qualified accordingly.

**3.6 Index.** The index maps external identifiers to containers, is mutable and multi-valued (one DOI to many containers; one container to many DOIs), and is a service, never part of the kernel. The existing DOI Resolution Index and doi-axn-map are the deployed index layer.

**3.7 Remint and stratification (autonomous minting).** The temporal rule is recursive: a container MAY be sealed as a new core at any time, and the new core may contain anything that pre-exists the new mint — the prior core's bytes, its accumulated sidecars, and the prior AXN itself (assigned earlier, therefore admissible). Each mint is a stratum; the fixed-point constraint applies per-mint and excludes only the not-yet-derived kernel. Reminting NEVER invalidates the prior AXN: both addresses remain valid for their respective byte-states (non-destruction; no-silent-reassignment). Lineage MUST be recorded at the registry/index layer via relation entries (supersession, aggregation, derivation) — never mandated inside core bytes, which remain content-agnostic. **Nested verifiability (property, not requirement):** where a prior core's bytes are contained intact within a new core, any holder can extract that byte range and recompute the prior kernel from inside the new core — lineage becomes independently checkable arithmetic rather than asserted metadata. Every container is thereby an autonomous minting point: any custodian holding a container can re-seal it into their own registry under registry-relative addressing, permissionlessly, with lineage verifiable where bytes are preserved intact. Remint is the mechanism by which another custodian's reconstruction becomes their own sovereign registration.

**3.8 Roles, not kinds (MANUS, 2026-07-18): core and sidecar are determined fully by the operative mint.** No byte stream is intrinsically core or intrinsically sidecar. Relative to a given mint, the core is whatever bytes that mint seals, and a sidecar is whatever attaches to that seal afterward. The same bytes may be a sidecar relative to one mint, core content within a later mint that contains them, and a sealed core of their own if minted directly — any sidecar may itself be minted, since minting is ungated. All conformance language in this specification is indexed to the operative mint: "verifiers compute kernels over core bytes alone" means *this mint's* sealed bytes; the §VIII.16 falsifier ("sidecar payload enters kernel derivation") is enforced by ordering, not content inspection — nothing attached after a mint's seal can occur in that mint's derivation. The container is not a privileged object; it is the view from a mint.

## 4. Falsification (paper §VIII.16)

**Core integrity under amendment.** Claim: adding a sidecar never alters the core kernel. Falsifier: any sidecar payload included in kernel derivation, or any manifest hashing sidecars into the kernel. Current status: routing rule deployed as practice and now as norm; typed chaining, signatures, and manifests staged; test vectors for container conformance to be published with the staged features.

## 5. What is NOT claimed

Containerization does not retain what never reached the container: content lost to a substrate's engineered non-persistence (the production-loss case) was never in any custodian's bytes, and no container format on the archive's side could have held it. The loss notice's lesson — no durable export means preservation responsibility falls entirely on the operator — is unchanged by this specification.
