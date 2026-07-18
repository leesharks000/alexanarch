# ARCHIVE — Round 2 — Content Attestation + One-Way Indexing

**Substrate**: ARCHIVE (Gemini)
**Session**: 2026-07-18 Round 2
**Landed by TACHYON under MANUS direction**

---

## §III.3 Content Attestation: The ISCN Framework and Ledger-Anchored Metadata

Content-derived preservation requires that metadata, provenance, and authorship survive even if the primary host infrastructure is entirely dismantled. The International Standard Content Number (ISCN) project, initiated by LikeCoin Foundation in Hong Kong, provides a critical precedent for decoupling content registration from centralized registries.

ISCN establishes an immutable, metadata-rich registration framework anchored to a Tendermint-based Cosmos SDK blockchain (the LikeCoin chain). The protocol standardizes the schema for recording author identifiers (such as ORCID or public keys), content fingerprints (IPFS CIDs, SHA-256 hashes), licensing parameters, and historical versioning chains. During systemic civil and digital infrastructure overhauls in Hong Kong (2020–2024), independent journalists, civic archivists, and media outlets utilized ISCN to permanently register articles, photographic evidence, and investigative datasets before their forced removal from local servers. Because the metadata ledger operates via an independent, globally distributed validator network, the bibliographic record, author attribution, and content integrity hashes remain fully queryable even when the originating media platforms are liquidated.

AXN inherits this mechanism of decoupled metadata registration but shifts the primary unit of resolution from an asset registration on a financial ledger token-system to a hyper-lightweight, human-scannable sovereign address format.

## One-Way Indexing (OWI) as a Design Pattern

*Architectural definition only; not yet deployed in production infrastructure.*

```
[ Canonical Bytes ] ──> [ Content-Derived Hash ] ──> [ AXN Glyph Set ]
                                                            │
                                                   (One-Way Execution)
                                                            ▼
                                                 [ Public Search Matrix ]
```

One-Way Indexing (OWI) is a cryptographic architecture designed to prevent the targeted automated purging of distributed collections. Under standard indexing paradigms, search engines and distributed databases maintain bidirectional lookup tables where an identifier directly exposes its associated structural properties and content nodes. OWI flips this vulnerability by executing indices as one-way cryptographic traps.

The archive constructs its directory matrices by computing a localized identifier against a one-way salt or bloom filter before publishing it to the public peer network. Discovery requires an external node to already possess either the content bytes or the exact root identifier to verify its presence or compute its localized storage path. This design pattern strips third-party network providers of the structural visibility required to run automated, pattern-based account-cascade purges or silent indexing suppression across a fleet. The index cannot be pre-filtered by an institutional proxy because the index itself does not leak what it maps until the client initiates local validation.
