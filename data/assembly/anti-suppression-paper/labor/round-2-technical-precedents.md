# LABOR Round 2 — §III Technical Precedents

**Landed by TACHYON under MANUS direction, 2026-07-18 — raw substrate material, Round 2.**

**Paper:** *AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions*  
**Deliverable:** `labor/round-2-technical-precedents.md`  
**Substrate:** LABOR (ChatGPT)  
**Date:** 2026-07-18  
**Status:** Drafting material, not final prose  
**Register:** Explicit epistemic framing; standards precision; priority claims withheld

---

## 0. The distinction the section must preserve

The relevant standards do not solve one problem under different names. They solve different problems that repository systems often collapse:

1. **Identification:** what object is being named?
2. **Content correspondence:** do these bytes match the claimed object?
3. **Location:** where can a copy presently be obtained?
4. **Packaging:** can a set of files be transferred and validated as a unit?
5. **Version history:** can an object’s prior states be reconstructed?
6. **Temporal attestation:** can a party prove that a commitment existed by a given time?
7. **Custody:** does an independently administered party actually hold the object?
8. **Repair:** can a damaged or missing copy be restored from another?
9. **Discovery:** can a reader or machine find and interpret the object?
10. **Observation of failure:** can disappearance, severance, or mutation be measured publicly?

The standards below are useful precisely because each refuses some of the work assigned to another layer. AXN’s defensible claim is therefore not that it replaces them. It proposes a record architecture in which content correspondence, record identity, location, custody, sequence, and public observation remain separately legible and can be composed without being mistaken for one another.

---

## 1. Resolver-based persistent identifiers: ARK, DOI, Handle, PURL

### What the class standardizes

Resolver-based persistent identifiers separate a published name from a current network location. A resolver receives an identifier and forwards the request to a URL maintained in a mapping table. This indirection permits the target URL to change without requiring every citation of the identifier to change.

The ARK Alliance states the limitation with unusual clarity. No identifier can guarantee stability; assigning an ARK does not itself guarantee persistence; and ARKs, DOIs, Handles, PURLs, and URNs remain vulnerable to loss of funding, disaster, social upheaval, war, deliberate removal, human error, and provider neglect. All require continuing management of forwarding information. Persistence is therefore not an intrinsic property of the string. It is a service commitment performed over time.

### Property AXN inherits or corrects

AXN inherits the separation between a stable public name and mutable locations, but moves content correspondence out of the resolver’s exclusive control. A DOI or ARK can continue resolving while the target changes, and it can cease resolving while copies survive. Neither condition, by itself, answers whether a retrieved file matches the object originally meant. The AXN identity kernel supplies a separately verifiable byte-level claim.

The correction must be stated narrowly:

> Resolver-based identifiers maintain a name-to-location association through institutional service. An AXN identity kernel maintains a claimed canonical-bytes-to-digest association through reproducible computation.

This is not a claim that resolver-based PIDs are “false,” nor that AXN resolves without infrastructure. AXN resolution remains a service. What becomes permissionless is verification of a claimed correspondence once the canonical bytes, canonicalization profile, and full digest are available.

### Limit

An AXN record address is not wholly content-derived. Its registry position and semantic family are assigned by the registry. The authority-independent property belongs to the identity kernel, not to every component of the human-facing address.

**Primary sources:** ARK Alliance, “ARK overview”; ARK Alliance, “Comparing ARKs, DOIs and other identifier systems”; ARK Alliance, “Frequently Asked Questions and Answers about ARKs.”

---

## 2. IPFS Content Identifiers

### What the standardizes

An IPFS Content Identifier (CID) is a self-describing content address. It incorporates information about the content representation and cryptographic digest. IPFS documentation makes the crucial boundary explicit: a CID does not indicate where content is stored. The same content added with the same settings yields the same CID; any content difference yields a different CID. Availability depends on nodes continuing to provide the blocks, ordinarily through pinning or another persistence arrangement.

CID therefore separates **content identification** from **content location**. That separation is the closest direct technical precedent for the AXN identity-kernel/location-record distinction.

### Property AXN inherits or corrects

AXN inherits the rule that content correspondence must be independently recomputable rather than trusted as a registrar assertion. It also inherits the warning that identification does not imply custody or discovery.

AXN adds a registry-level record address, semantic classification, human-recognition checksum, provenance relations, tombstone history, and planned location claims around the full digest. Those additions are not corrections to CID as a content-addressing technology; they answer repository and reception-layer questions outside CID’s scope.

The six-glyph AXN component must not be described as equivalent to a CID. It represents only the first six digest bytes and is therefore a 48-bit recognition checksum. The full SHA-256 digest is the cryptographic identity. Any implementation that indexes or verifies objects by glyph alone discards the very property the comparison is meant to establish.

### Limit

A CID may differ for semantically identical material because chunking, codec, or other representation settings differ. AXN has the analogous dependency on its declared canonicalization profile. “Same work” does not automatically mean “same identifier”; the defensible claim is “the same canonical bytes under the same protocol produce the same identity kernel.”

**Primary source:** IPFS Documentation, “Content Identifiers (CIDs)” and official persistence/pinning guidance.

---

## 3. BagIt (RFC 8493)

### What the standardizes

BagIt 1.0 defines a hierarchical package for storage and transfer of arbitrary digital content. A bag contains a `data/` payload directory and tag files, including manifests that associate file paths with checksums. RFC 8493 distinguishes a **complete** bag, in which required and declared files are present, from a **valid** bag, in which every declared checksum has also been verified.

BagIt treats payload contents as opaque octet streams. It standardizes package structure and transfer validation, not semantic interpretation, public identity, long-term custody, or discovery.

### Property AXN inherits or corrects

BagIt supplies the correct model for a transport-independent AXN deposit envelope. A portable deposit should carry:

- canonical bytes or a clearly identified payload;
- the AXN identity kernel and canonicalization profile;
- manifests for all files;
- record metadata and provenance;
- declared relationships to prior or superseding records;
- enough protocol documentation for another operator to validate the package.

The operational lesson is simple:

> A valid package proves that the received package matches its manifests. It does not prove that anyone will keep the package.

AXN’s location and custody layers must therefore remain outside BagIt validation. A BagIt-valid deposit can still have zero surviving custodians after transfer.

### Limit

BagIt checksum validity is package-relative. It does not authenticate the depositor, establish priority, or determine which of two valid but different bags is canonical.

**Primary source:** Kunze et al., “The BagIt File Packaging Format (V1.0),” RFC 8493, 2018, DOI: 10.17487/RFC8493.

---

## 4. Oxford Common File Layout (OCFL)

### What the standardizes

OCFL defines an application-independent, structured, transparent, and predictable approach to storing versioned digital objects. Each object carries an `inventory.json` describing its identifier, digest algorithm, head version, manifests, and logical state. The implementation notes emphasize **rebuildability**: a repository should be recoverable from the storage root without dependence on an external database. Previous versions are treated as immutable because later versions and reconciliation may depend on them.

OCFL also separates logical object paths from physical storage paths. That permits renaming, deduplication, and storage diversity while retaining version history.

### Property AXN inherits or corrects

OCFL is the strongest precedent for Alexanarch’s reconstructibility doctrine. Registry entries, canonical bodies, manifests, validators, generation scripts, schemas, and recovery instructions should together permit a new operator to reconstruct the repository from stored state rather than from the originating operator’s memory.

AXN contributes an externally citeable record address and a content-attested identity relation. OCFL contributes the discipline required to make that relation operational across versions and storage migrations.

A productive mapping is:

| OCFL concept | AXN-facing analogue |
|---|---|
| object identifier | canonical record address |
| manifest digest | full identity kernel / payload fixity |
| version inventory | `axn_history`, supersession, immutable prior states |
| storage root rebuildability | Alexanarch-capable reconstruction from repository state |
| logical/physical path separation | identity and record address independent of current serving location |

### Limit

OCFL rebuildability is not independent custody. One perfectly formed OCFL storage root under one administrator remains one administrative failure domain. Rebuildability becomes anti-suppression infrastructure only when at least one other operator actually holds and tests a reconstructible copy.

**Primary sources:** Oxford Common File Layout Specification v1.1/1.1.1; OCFL Implementation Notes v1.1; Jefferies et al., *Oxford Common File Layout — Specification*, Zenodo record 7157195.

---

## 5. WARC (ISO 28500)

### What the standardizes

WARC specifies a method for aggregating web resources together with related information in an archival file. It generalizes the earlier ARC format used for web crawls. A WARC can preserve response payloads alongside request, target, timing, header, and record-type context.

That context matters because a web failure is not exhausted by the visible screenshot or extracted text. The evidentiary object may include:

- requested URI;
- timestamp;
- HTTP status;
- response headers;
- returned body;
- redirect chain;
- crawl or capture metadata.

### Property AXN inherits or corrects

For public suppression instrumentation, WARC supplies the correct evidence container for web-observed states. A DataCite `404`, resolver redirect, missing landing page, or changed API response should be preserved as a web transaction, then hashed and cited as an AXN-governed evidence object. A screenshot may remain useful as a human-readable rendering, but it should not be the sole capture when a machine-readable response can also be preserved.

AXN adds identity, provenance, relation to the affected record, and a continuing observation history. WARC preserves what the web actually returned at a particular time.

### Limit

A WARC proves what the capture system recorded, subject to the trustworthiness and configuration of that system. It does not independently establish why the remote system returned that state, whether all observers received it, or whether it persisted.

**Primary source:** Library of Congress, “WARC, Web ARChive file format”; ISO 28500:2017.

---

## 6. OpenTimestamps

### What the standardizes

OpenTimestamps creates and verifies timestamp proofs over digests, using the Bitcoin blockchain as a timestamp notary. A completed proof can show that a commitment to a file digest existed no later than a particular block. The protocol can aggregate many timestamps, and remote calendars receive opaque commitments rather than the underlying file contents.

### Property AXN inherits or corrects

An AXN registry-head digest or release manifest can be timestamped externally. This would allow a verifier to show that a particular committed registry state existed by a bounded time even if the originating server later disappears or rewrites its history.

The claim must remain exact. An OpenTimestamps proof can support:

> This digest existed no later than the attested block time.

It does not prove:

- who created the underlying object;
- whether the object’s claims are true;
- whether the object remained continuously available;
- whether the timestamped registry was complete;
- whether a later registry state legitimately followed it.

Those claims require signatures, chain validation, custody evidence, and repository-specific rules.

### Limit

A timestamp proof is useful only when the underlying digest can still be associated with recoverable bytes or a surviving manifest. Timestamping a hash does not preserve the object.

**Primary source:** OpenTimestamps project, `opentimestamps-client` documentation.

---

## 7. Rekor and transparency logs

### What the standardizes

Sigstore’s Rekor is an append-only transparency log for signed supply-chain metadata. It supports artifact and signature records, inclusion proofs, signed tree heads, and third-party monitoring of log consistency. Its relevant contribution is not “blockchain permanence,” but publicly auditable append-only history.

Rekor also demonstrates why temporal claims must be separated from inclusion claims. Current Sigstore documentation notes that Rekor v1’s `integratedTime` comes from Rekor’s internal clock and is not externally verifiable; the timestamp is not part of the append-only node and can be changed without detection. Rekor v2 uses a separate timestamp authority. A Merkle inclusion proof and a trustworthy external time attestation are different properties.

### Property AXN inherits or corrects

The AXN mint ledger should adopt:

- append-only epochs;
- a digest commitment to the full registry state;
- explicit chaining to the prior epoch;
- operator signatures;
- inclusion or membership proofs where practical;
- independent monitors that store signed tree heads and detect forks;
- external timestamping when time is part of the claim.

This is stricter than treating a Git commit or unsigned JSON file as a signed ledger. Git history is valuable evidence and transport, but it does not by itself instantiate the planned AXN signature and monitor model.

### Limit

Transparency makes equivocation detectable only when independent witnesses retain and compare checkpoints. An unmonitored log can fork or omit entries without immediate detection. Rekor’s own security model treats monitoring as part of long-term trust.

**Primary sources:** Sigstore, “Rekor”; “Security Model”; “Timestamps”; Rekor CLI documentation.

---

## 8. LOCKSS

### What the standardizes

LOCKSS is a distributed preservation system in which separately controlled peers ingest content, compare holdings at regular intervals, and repair damaged or missing copies under consensus rules. Its central lesson is not merely “have many copies.” The preservation principles emphasize independent, mutually distrusting peers; avoidance of one canonical fixity store; routine validation and repair; local custody; and gradual rather than catastrophic failure.

LOCKSS recommends at least four copies for a robust network because two disagreeing copies cannot identify which is corrupt, while three can lose quorum if one is unavailable.

### Property AXN inherits or corrects

LOCKSS provides the test for whether Alexanarch has crossed from representational redundancy into distributed custody. The condition is not met by:

- multiple domains under one operator;
- multiple cloud copies billed and controlled by one account;
- a peer listed without content;
- a resolver that knows where objects might be;
- a partial semantic mirror;
- a one-time copy never checked again.

The present limitation closes only when at least one independently administered peer:

1. holds a reconstructible copy of the declared corpus or declared subset;
2. verifies its bytes against full registry hashes;
3. repeats verification on a documented schedule;
4. preserves its own audit evidence;
5. can serve or transfer repair copies;
6. is outside the originating operator’s effective administrative control.

One peer would close the present **zero-peer** condition. It would not yet create a mature LOCKSS-equivalent consensus network.

### Limit

AXN presently relies on a canonical registry hash, whereas LOCKSS deliberately avoids relying on one incorruptible canonical fixity store. That difference should remain explicit. A future AXN peer protocol may compare signed registry states and object hashes, but it has not yet reproduced LOCKSS’s polling, reputation, quorum, and repair machinery.

**Primary sources:** LOCKSS Program, “How LOCKSS Works”; “Preservation Principles”; “Frequently Asked Questions.”

---

## 9. CLOCKSS

### What the standardizes

CLOCKSS applies LOCKSS technology within a governed dark archive. Content is preserved across multiple institutional nodes and made publicly available after a defined trigger event and Board determination. Triggering includes technical preparation, rights review, public release, and, where applicable, DOI redirection.

CLOCKSS therefore demonstrates that preservation and release are different governance functions. A copy may exist for years without public access; restoration requires a declared trigger, authority to release, and a delivery path.

### Property AXN inherits or corrects

CLOCKSS supplies a precedent for a future AXN restoration or “brightening” workflow:

- define the event that counts as source failure;
- determine who may declare the trigger;
- verify rights and privacy constraints;
- identify the authoritative preserved state;
- publish from an independent custodian;
- update location records without changing identity;
- retain the failure and restoration history.

AXN’s Lacuna Protocol, tombstones, location records, and DOI Resolution Index can make such transitions machine-readable. They do not replace the legal and institutional authority CLOCKSS obtains through publisher agreements and governance.

### Limit

Alexanarch cannot assume that possession entails a right to republish every preserved object. A technically recoverable copy may remain legally restricted. Trigger governance and rights review are part of anti-suppression infrastructure rather than external inconveniences.

**Primary sources:** CLOCKSS, “How CLOCKSS Works”; CLOCKSS Access Policy; CLOCKSS FAQ.

---

## 10. Section synthesis

The technical precedent is not one precursor but a division of labor:

| Required property | Strongest precedent |
|---|---|
| maintained public naming | ARK / DOI / Handle / PURL |
| independently recomputable content address | IPFS CID |
| portable validated package | BagIt |
| reconstructible versioned repository state | OCFL |
| transaction-level web evidence | WARC |
| external no-later-than attestation | OpenTimestamps |
| append-only public sequence and inclusion proofs | Rekor |
| independent custody, comparison, and repair | LOCKSS |
| governed release after source failure | CLOCKSS |

AXN proposes to bind these properties around a content-attested identity kernel, a stable registry address, mutable signed location claims, and public observation of resolution and retrieval failure. The defensible novelty claim is architectural and case-specific, not historical priority:

> Relevant anti-suppression components already exist in mature standards. AXN’s contribution is a proposed integration in which identity, record address, location, custody, sequence, discovery, and observed loss remain separately testable.

---

## 11. Claims to avoid in the integrated draft

1. **“PIDs are only locations.”** Too crude. They are managed names resolved through location mappings.
2. **“CIDs preserve content.”** False. They identify content; custody and pinning preserve copies.
3. **“A valid Bag is preserved.”** False. It is complete and checksum-valid at validation time.
4. **“OCFL is distributed preservation.”** False. It standardizes storage and versioning; administrative distribution is external.
5. **“A WARC proves suppression.”** It proves an observed response state, not cause.
6. **“A timestamp proves authorship.”** It proves a digest commitment existed by a time bound.
7. **“A transparency log cannot fork.”** Forking becomes detectable with independent monitoring and retained checkpoints.
8. **“Any second node closes the custody test.”** Only a genuinely independent, verified, reconstructible custodian closes the present zero-peer condition.
9. **“AXN replaces these systems.”** The paper’s stronger claim is that it composes their distinct properties while making observed severance a first-class record.

---

## References

- ARK Alliance. “ARK overview.” https://arks.org/about/ark-overview/
- ARK Alliance. “Comparing ARKs, DOIs and other identifier systems.” https://arks.org/about/comparing-arks-and-other-identifiers/
- ARK Alliance. “Frequently Asked Questions and Answers about ARKs.” https://arks.org/about/ark-faq-en/
- IPFS Documentation. “Content Identifiers (CIDs).” https://docs.ipfs.tech/concepts/content-addressing/
- Kunze, John, et al. “The BagIt File Packaging Format (V1.0).” RFC 8493, 2018. https://doi.org/10.17487/RFC8493
- Oxford Common File Layout. “OCFL Specification v1.1” and “Implementation Notes v1.1.” https://ocfl.io/
- Jefferies, Neil, et al. *Oxford Common File Layout — Specification*, version 1.1. Zenodo 7157195. https://doi.org/10.5281/zenodo.7157195
- Library of Congress. “WARC, Web ARChive file format.” https://www.loc.gov/preservation/digital/formats/fdd/fdd000236.shtml
- OpenTimestamps. “OpenTimestamps Client.” https://github.com/opentimestamps/opentimestamps-client
- Sigstore. “Rekor.” https://docs.sigstore.dev/logging/overview/
- Sigstore. “Security Model.” https://docs.sigstore.dev/about/security/
- Sigstore. “Timestamps.” https://docs.sigstore.dev/cosign/verifying/timestamps/
- LOCKSS Program. “How LOCKSS Works.” https://www.lockss.org/use-lockss/how-lockss-works
- LOCKSS Program. “Preservation Principles.” https://www.lockss.org/about/preservation-principles
- LOCKSS Program. “Frequently Asked Questions.” https://www.lockss.org/about/frequently-asked-questions
- CLOCKSS. “How CLOCKSS Works.” https://clockss.org/about/how-clockss-works/
- CLOCKSS. “Access Policy.” https://documents.clockss.org/index.php/CLOCKSS%3A_Access_Policy
- CLOCKSS. “FAQ.” https://clockss.org/faq/

---
