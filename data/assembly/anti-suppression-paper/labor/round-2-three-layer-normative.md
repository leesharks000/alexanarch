# LABOR Round 2 — §IV Three-Layer Model (Normative Draft)

**Landed by TACHYON under MANUS direction, 2026-07-18 — raw substrate material, Round 2.**

**Paper:** *AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions*  
**Deliverable:** `labor/round-2-three-layer-normative.md`  
**Substrate:** LABOR (ChatGPT)  
**Date:** 2026-07-18  
**Status:** Journal drafting material; normative core  
**Target:** 500–800 words

---

## The three-layer model

A conforming AXN implementation **MUST** distinguish content identity, registry address, and current location. These layers answer different questions and have different mutability rules.

### Layer 1: identity kernel

The identity kernel has the form:

```text
axn-content:sha256:<64 lowercase hexadecimal characters>
```

It identifies one sequence of canonical bytes by its full SHA-256 digest. Under AXN v2, the canonical bytes are produced from the registered `title`, `creator`, `description`, and `body` strings, joined in that order by a single line-feed character and encoded as UTF-8. Implementations **MUST NOT** trim whitespace, normalize Unicode, rewrite internal line endings, reorder fields, or substitute rendered-file bytes unless a later canonicalization profile explicitly requires that operation. A record **MUST** declare the protocol and canonicalization profile used. Where the exact registered field values are unavailable, identity verification is indeterminate rather than failed.

The kernel is immutable for those bytes. Any byte change produces a new kernel. This layer is authority-independent in a narrow, testable sense: anyone holding the canonical field values can recompute the digest and determine whether the claimed correspondence matches. The kernel does not establish authorship, legality, truth, custody, availability, or priority.

### Layer 2: canonical record address

The canonical record address has the form:

```text
AXN:<HEX>.<FAMILY>.<GLYPH>
```

`HEX` is the stable registry-position label. `FAMILY` is the registry-assigned semantic family. `GLYPH` is a six-grapheme recognition checksum obtained by mapping the first six bytes of the full SHA-256 digest through the canonical 256-entry glyph table. The full address names the object’s entrance into a particular registry; it is therefore not wholly content-derived.

The glyph is a 48-bit recognition component, not the cryptographic identity. Implementations **MUST** store and verify the full 256-bit digest and **MUST NOT** use the glyph alone as a unique database key. A glyph collision does not imply a SHA-256 collision and is resolved by the full identity kernel.

Once publicly assigned, a record address **MUST NOT** be silently reassigned to different canonical bytes. Classification correction, protocol migration, withdrawal, or replacement **MUST** preserve the former address in machine-readable history and express the new relation explicitly through aliasing, retirement, or supersession.

Accordingly, the current AXN is best characterized as **a sovereign record address with a content-derived recognition component, backed by a full content hash**.

### Layer 3: location record

A location record is a mutable, signed statement about where verified copies may presently be obtained. It **SHOULD** include the identity kernel, canonical record address, sequence number, prior-record hash, issuing node, issue time, optional expiry or recheck time, locations, custody role, last verification time, and signature.

A location MAY disappear or be added without changing either layer 1 or layer 2. Resolvers **MUST** treat locations as claims requiring verification: retrieved bytes are canonical only when their recomputed kernel matches the declared full digest. Superseded location records **SHOULD** remain auditable rather than being overwritten without history.

### Circularity prohibition

The assigned AXN and any value derived from its digest **MUST NOT** occur inside the canonical bytes from which that digest is computed. Otherwise inserting the identifier changes the bytes, which changes the digest, which changes the identifier, creating an unstable fixed-point problem. The AXN MAY appear in wrappers, landing pages, sidecar metadata, manifests, citations, or rendered derivatives outside the canonical byte scope.

### Verification procedure

A conforming verifier:

1. reconstructs canonical bytes under the declared profile;
2. computes SHA-256 and compares the full digest to the kernel;
3. derives and compares the six-glyph recognition checksum;
4. confirms that the record address is bound to that kernel in the cited registry state;
5. verifies any location-record signature separately; and
6. recomputes the kernel over bytes retrieved from each claimed location.

Failure at one layer does not automatically falsify the others. A dead location does not invalidate the kernel; a correct kernel does not prove custody; and a valid registry binding does not prove that any resolver currently serves the object.

---

## Implementation note requiring protocol reconciliation

The current protocol JSON defines canonical bytes as the four-field UTF-8 concatenation, while the mint-endpoint design also describes accepting a single `canonical_text` value. Before external conformance claims are made, the specification should state whether `canonical_text` is merely a transport that parses into the four canonical fields or a distinct canonicalization profile. Two inputs that are treated as equivalent by one implementation and different by another would break deterministic verification.

---
