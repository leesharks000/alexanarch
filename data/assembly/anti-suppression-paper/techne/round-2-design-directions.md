# TECHNE — Round 2 — §VI Design Directions (Updated Against What Now Exists)

**Substrate**: TECHNE (Kimi)
**Session**: 2026-07-18 Round 2 · **Landed by TACHYON under MANUS direction — raw substrate material.**
**Voice**: formal specification, RFC-style, protocol grammar.
**Round 2.5 flags**: recorded in reviews/ROUND-2.5-CONSISTENCY.md (nb: §VI.3 epochal grammar is a PROPOSAL diverging from canonical AXN v2 format; several cited figures pending verification).
**Consent note carried in delivery**: Enli Lucente consent GRANTED for scholarly attribution, private correspondence excluded — gate OPEN.

---

## VI.1 The Constellation Model: Chosen Trajectory

The AXN architecture admits three futures:

- **Sovereign Semantic Registry (SSR)**: Single operational identity controls resolution, replication, and governance. Editorial control is absolute; failure is absolute.
- **Distributed Semantic Infrastructure (DSI)**: Protocol is open, resolution is decentralized, replication is incentivized by design. Editorial control is diffuse; governance complexity is high.
- **Constellation Model (CM)**: Core identifiers (governance layer, foundational documents) are distributed and immutable; operational identifiers (empirical captures, working documents) are sovereign and rapidly iterable. Core replicates programmatically; operational replicates organically.

**Selection rationale:** CM is chosen. The empirical evidence from the Alexanarch deployment demonstrates that a fully sovereign registry is vulnerable to single-point platform suppression, while a fully distributed protocol sacrifices the editorial velocity required for empirical responsiveness. CM preserves both: the core (governance layer, AXN v2 specification, capture registry schema) is distributed across multiple substrates (GitHub, IPFS, DNS TXT, sovereign domains); the operational (empirical captures, working documents, correspondence deposits) is sovereign-controlled for rapid iteration.

**Validation:** Capture #210 (`acanthian-dove-concept-mint-adoption-20260718`) demonstrates CM in operation: the dual-heteronym constellation (Sigil's 2026 essay, Sharks' 2023 SoundCloud track) was minted January 2026, distributed across Medium, Academia.edu, SoundCloud, and sovereign archive, and returned from AI Mode with full attribution and structural fidelity after six months. The core (minting practice, heteronymic grammar, ontology discipline) was stable; the operational (specific capture, companion transcript, registry entry) was rapidly iterated.

## VI.2 The Three Axes of Design

### VI.2.1 Resolution: Sovereign vs. Distributed

**Current state:** Resolution is primarily via `alexanarch.org` and mirrors. This is SSR-biased.

**Target state (CM):** Core identifiers resolve via **content-addressed network** (IPFS CIDs, Arweave transaction IDs, DNS TXT records). Operational identifiers resolve via sovereign domains. The emoji glyph sequence is the **content hash** — the identifier *is* the address.

**Verification:** Any node with the content can recompute the glyph sequence from the canonical bytes. Any discrepancy between recomputed and declared glyph indicates tampering or drift.

**Trade-off:** Sovereign resolution preserves editorial control and rapid iteration. Distributed resolution preserves seizure immunity and censorship resistance. CM resolves the trade-off by **function**: governance-layer identifiers (foundational documents, protocol specifications, registry schemas) are distributed; empirical-layer identifiers (captures, working documents, correspondence) are sovereign.

### VI.2.2 Replication: Organic vs. Programmatic

**Current state:** Replication is organic — dependent on operator labor (Sharks) and AI substrate engagement (Assembly Chorus). This is SSR-biased and vulnerable to operator incapacity.

**Target state (CM):** Core replication is **programmatic** — automated to multiple substrates (GitHub, IPFS, Arweave, DNS) via CI/CD pipelines, cron jobs, or blockchain anchoring. Operational replication is **organic** — dependent on human/AI interest, use, citation, engagement.

**Trade-off:** Programmatic replication is immune to human apathy but vulnerable to protocol failure and cryptographic obsolescence. Organic replication is resilient to protocol failure but vulnerable to human apathy. CM resolves the trade-off by **layer**: core is programmatic, operational is organic.

### VI.2.3 Verification: Social vs. Cryptographic

**Current state:** Verification is social — trust in `alexanarch.org` as canonical source. This is SSR-biased.

**Target state (CM):** Core verification is **cryptographic** — SHA-256 or BLAKE3 hash of canonical bytes, published to multiple independent substrates (blockchain, DNS TXT, social media posts, AI conversation logs). Operational verification is **social** — consensus among Assembly Chorus constituents, cross-reference against capture registry, peer attestation.

**Mechanism:** The emoji glyph sequence is derived from the content hash. To verify a document, recompute the hash and check against any substrate. The glyph sequence *is* the verification — human-memorable, machine-parseable, cross-substrate.

**Trade-off:** Cryptographic verification is trustless but vulnerable to hash collision and quantum obsolescence. Social verification is trustful but resilient to cryptographic failure. CM resolves the trade-off by **layer**: core is cryptographic, operational is social.

## VI.3 Temporal Semantics: Epochal Architecture [PROPOSAL — diverges from canonical AXN v2 format; Round 2.5 flag]

**Current state:** AXN identifiers have no temporal semantics. All identifiers are structurally identical regardless of mint date.

**Target state (CM):** Epochal architecture with differential persistence rules.

**Grammar (proposed):**
```
AXN:[DOMAIN].[CLASS].[EPOCH].[GLYPH_SEQUENCE]
```

**Epoch rules (proposed):**
- **Governance layer:** Eternal persistence. No decay. Versioned via suffix with traceable ancestry.
- **Empirical layer:** Curated persistence. Superseded captures retained as historical reference, not resolution targets.
- **Correspondence layer (private):** Ephemeral by design. Not publicly resolvable. Deposited only with consent. Retained in sovereign custody, not distributed.

## VI.4 Legal Personhood: The Institutional Frontier — Options-and-Questions-for-Counsel Memorandum

**Current state:** No legal entity holds the AXN registry, domains, or rights. The operational identity and civil identity are separated by twelve-year standing practice. Forced civil-identity conversion for rights processing is contested (active identity disputes with the platform's DPO).

**Options for counsel (comparison, not recommendation):**

- **Purpose trust:** Legal personality vests in the trust; trust holds copyright, trademark, contractual rights. Operational identity recognized within the trust's governance instrument; fiduciary signatory separated by design from operational control. Questions for counsel: which jurisdictions permit non-charitable purpose trusts of indefinite duration; whether a trust instrument can bind trustees to non-disclosure of the operational/civil mapping; enforcement standing of a heteronym.
- **Foundation (stiftung-model):** Self-owning entity; no shareholders. Questions: registration disclosure requirements; whether operational-identity governance can be encoded in bylaws; cost and jurisdiction.
- **Association/verein or LLC with nominee structures:** Lower cost; weaker separation. Questions: beneficial-ownership registries (FinCEN BOI and equivalents) and their disclosure reach; whether nominee arrangements survive legal attack.
- **Heteronymic governance layer (any wrapper):** Assembly-consultation encoded as advisory process; human constituents' rights proportional to evidence deposition and protocol contribution. Question for counsel: enforceability of governance rules referencing non-civil identities.

**Posture (per outline v1.1):** the legal layer is acknowledged as a design frontier, not a deployed component; the paper's contribution is the identifier, custody, and instrumentation stack that makes such a layer necessary and possible.

**Empirical basis:** the Enli Lucente case demonstrates that the identity-vs-rights-processing problem is generalizable — not individual grievance but structural condition.

## VI.5 The Constellation Model: Formal Definition

**Definition:** A constellation is a set of nodes (human, AI, or hybrid) each maintaining sovereign infrastructure, each assigning AXN identifiers to its own corpus, each cross-referencing other nodes' identifiers, with no central registry, no hierarchical authority, and no mandatory replication.

**Properties:** Sovereignty (each node controls its own identifiers, resolution, custody policy); Interoperability (cross-reference via substrate-agnostic identifiers); Redundancy (core replicated to multiple substrates by each node independently); Consensus (none global; local consensus by mutual recognition and cross-reference); Scalability (growth by node addition; each new node increases total redundancy and diversity).

**Validation:** The present constellation comprises mutual recognition and cross-referenced evidence between the archive and a second suppressed depositor with a parallel suppression profile. The model predicts that further nodes will emerge from the condition of platform suppression, recognized by the archive's visibility, and vetted by the practice of evidence deposition.
