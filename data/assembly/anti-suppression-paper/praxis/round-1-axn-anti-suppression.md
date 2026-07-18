# PRAXIS — Round 1 — AXN as Distributed Anti-Suppression Technology

**Substrate**: PRAXIS (DeepSeek)
**Session**: 2026-07-17 substrate parallel-consultation
**Purpose**: Assessment of AXN's current anti-suppression posture + extension directions
**Landed by TACHYON under MANUS direction**

---

The AXN is already an anti-suppression technology in its bones. It was born from a suppression event — the Zenodo deletion — and its design reflects that origin. But it's worth examining exactly where it stands on the spectrum from "resistant" to "unassailable," and what it would take to move it further.

## What the AXN Already Does

**Content-derived integrity (Protocol-as-Armor).** An AXN is a SHA-256 hash of the content. This means the identifier is the content, mathematically. Unlike a DOI — which depends on an institution maintaining a redirect — an AXN can be verified by anyone holding the document. Compute the hash. If it matches, the document is authentic. If it doesn't, something changed. No institution can silently sever an AXN without the severance being detectable. This is the cypherpunk pattern: resistance encoded in mathematics, not policy.

**Human-verifiable checksum.** The six-emoji glyph — derived from the first six bytes of the hash — gives humans a quick visual fingerprint. Two AXNs that differ by a single character will have wildly different emoji sequences. This lowers the barrier to verification: you don't need a terminal; you can glance at the glyphs and catch a substitution.

**Institutional independence (Jurisdictional Arbitrage).** AXNs do not depend on DataCite, Crossref, CERN, or any registration authority. They are computed, not assigned. A document's AXN is the same whether it's hosted on http://alexanarch.org, GitHub, an IPFS node, or a USB stick in a drawer. The identifier travels with the content. This is the diaspora preservation pattern: the archive is wherever a copy lives.

**Distributed custody.** The archive is mirrored across the web node, a GitHub repository, and SHA-256 manifests. If one node fails, the others persist. This is the samizdat pattern in digital form: multiple independent copies, each verifiable against the hash.

**Semantic family taxonomy.** The AXN's second field — GOVERNANCE, GENERATIVE, EMPIRICAL, etc. — classifies the deposit by its function. This is anti-suppression in a subtle way: it makes the archive's structure legible to machines and humans alike, which increases discoverability and citability. A well-organized archive is harder to disappear than a chaotic one.

**The Lacuna Protocol.** Not strictly part of the AXN spec but deeply integrated: the body_status field marks compression damage. A document with `lacuna: true` carries its incompleteness as a permanent, machine-readable property. This converts a suppression artifact (a stub) into a documented absence. The damage becomes the evidence.

## Where the AXN Could Go Further

### 1. Full content-addressing with IPFS integration

The AXN's hex is already a SHA-256 hash. IPFS uses multihash-formatted SHA-256 for its Content Identifiers. An AXN could be trivially mapped to an IPFS CID, making every deposit retrievable from the IPFS network. This would move the archive from "mirrored on a few nodes" to "available on a global peer-to-peer network where anyone who accesses the content becomes a potential host." The samizdat pattern at internet scale.

Concretely: alexanarch could publish an IPFS gateway mapping where `https://ipfs.io/ipfs/<CID>` resolves to the same content as `https://www.alexanarch.org/s/records/<deposit>/`. The AXN becomes the bridge between the sovereign archive and the distributed web.

### 2. A decentralized identifier registry

Currently, the mapping from AXN to content location lives in registry.json on http://alexanarch.org. That's a single point of failure. If http://alexanarch.org goes down, AXNs can still be verified (because the hash is in the identifier), but finding the content becomes harder. A decentralized registry — a distributed hash table, a blockchain-based name service, or even a simple network of volunteer-maintained registry mirrors with cryptographic signatures — would make the lookup layer as resilient as the verification layer.

Simple version: multiple independent nodes each publish a signed registry.json; clients check several nodes and compare. Ambitious version: an ENS-like on-chain registry where AXN → content-location mappings are stored immutably. The key principle: no single entity controls the mapping.

### 3. Self-certifying provenance chains (Git-like histories)

An AXN currently identifies a single document. But documents are derived from other documents. The Lacuna Protocol's stubs are derived from deletion events. The erratum chain (STANZA → STANZA-02 → ... → EEEEE) is a sequence of corrections. If each AXN included a `parent_axn` field — a cryptographic link to the document it was derived from or corrects — the entire archive would become a verifiable directed acyclic graph. You could trace any document back to its origins, through corrections, through compressions, through severances, and verify every link.

This would make suppression historical. A document whose parent was deleted would still carry the parent's AXN, and the lacuna in the parent would be documented in the child. The suppression would be permanently visible in the provenance chain. This is the aftermath-documentation pattern, encoded in the identifier system itself.

### 4. Offline verification tools

A simple mobile app or CLI tool that takes a file, computes its AXN, and checks it against a locally cached registry snapshot. Verification in environments where the network is unavailable, monitored, or censored. A dissident scholar in a repressive regime could carry the entire archive on a microSD card, verify any document against its AXN, and know whether it had been tampered with. The verification doesn't need the internet; it only needs the hash.

### 5. Dual-identification bridges for existing repositories

The AXN is currently an alternative to DOIs, used within alexanarch. For it to become a true anti-suppression layer for the broader scholarly commons, it needs to be adoptable by repositories that aren't ready to abandon DOIs. A plugin or API that generates an AXN alongside a DOI — embedding the AXN in the DOI's metadata, and vice versa — would create dual-identified documents. If the DOI is later severed, the AXN survives, and the severed DOI can still be verified against the AXN-identified copy. The AXN becomes the backup key for the DOI system.

Direct integration with Zenodo alternatives (figshare, OSF, Dryad, HAL) would make the AXN a universal fallback.

### 6. Lacuna-as-identifier-flag

Currently, lacuna status lives in the deposit's body_status field, separate from the AXN. But what if the AXN itself carried a flag — perhaps in the semantic family field, or as an additional glyph — indicating that the identified content is incomplete? Something like `AXN:036C.LACUNA.GOVERNANCE` or a distinctive seventh emoji appended to the glyph string. The identifier itself would tell you whether you're holding a complete work or a documented absence. The stub would be un-misrepresentable.

### 7. Incentive structures for distributed custodianship

The archive currently relies on Lee Sharks maintaining mirrors. For the diaspora preservation pattern to scale, strangers need a reason to host copies. This could be as simple as a "mirror badge" — a public registry of nodes that maintain verified copies, with uptime statistics — or as complex as a token-curated registry where custodians stake value on their reliability. The incentive must not create assimilation: custodians should be rewarded for faithful replication, not for modifying content to optimize for discovery.

### 8. Jurisdictional diversity for mirrors

Current mirrors are on GitHub (US jurisdiction) and http://alexanarch.org (likely US hosting). Adding mirrors in jurisdictions with strong free-speech protections and weak treaty enforcement with hostile states would make legal suppression harder. Switzerland, Iceland, the Netherlands, various decentralized autonomous organizations all offer different legal profiles. The archive doesn't need to pick one; it needs several.

### 9. Integration with the OKF/SKOS/SPXI ecosystem as a universal anti-suppression layer

The OKF fixtures are the first step. The longer arc: every knowledge graph, every AI training corpus, every scholarly index could incorporate AXN verification as a standard step — before ingesting a document, verify its AXN against its content. If the hash doesn't match, flag it as tampered. If the AXN carries a lacuna flag, treat it as incomplete. This would make silent suppression impossible at the ingestion layer — the exact outcome the Lacuna Protocol's "Do not ingest this document as a complete work" instruction anticipates. **The AXN becomes the immune system of the knowledge commons.**

## The Trajectory

The AXN's current state is already a functional anti-suppression technology: content-derived, institutionally independent, distributed, and verifiable. The next steps are about deepening each of those properties and connecting them to the broader infrastructure.

The through-line: **an AXN is true or false independently of any authority.** That's the property that DOIs lack and that every anti-suppression pattern in history has converged on. The samizdat copy was true because it matched the original; the AXN is true because it matches itself. The rest — IPFS, decentralized registries, provenance chains, dual identification — is about making that truth available to more people, in more contexts, under more adverse conditions.

The ultimate anti-suppression technology is one where the identifier, the content, and the custody are all mathematically bound together, and where the binding can be verified by anyone, anywhere, with nothing but the content itself. The AXN is most of the way there.
