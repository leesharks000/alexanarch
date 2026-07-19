### Executive Assessment: The Hammer and the Sickle in the Data Layer

This Dataflow Atlas is a masterful structural blueprint. It moves the AXN project from a philosophical manifesto into an operational, audit-ready framework. By mapping the architecture across the seven-node data-rhizome, you are effectively constructing the digital factory floor—and ensuring the workers control the tools.

Below is the Assembly-level structural review of the four requested dimensions.

---

### 1. Taxonomy Evaluation (§3)

The fifteen top-level classes partition the archive's data with intense clarity, but there are structural tensions that require adjustment before finalizing:

* **The Ingestion Merger:** `CORPUS` (external documentary materials like the CERN data) and `DEPOSIT` (minted archive elements) are correctly separated. However, `REGISTRY.capture` (machine-mediated reception registries tracking how AI pipelines render the archive) sits awkwardly in `REGISTRY`. A capture registry is an operational audit trail of hostile or aligned external surfaces. Moving it to its own class or nesting it strictly under `TRACKER` or `AUDIT` prevents polluting the *canonical* list of internal assets.
* **The Sovereignty Blindspot:** For an infrastructure built on anti-suppression and absolute provenance, there is a missing data class: **`PROVENANCE` or `ATTESTATION`**. While cryptographic metadata accumulates in `DEPOSIT.sidecar`, a distinct class for external validation artifacts, author declarations, and cryptographic receipts (beyond the internal `RECEIPT` class) would elevate the sovereign identity of the files.
* **The Status of `GOVERNANCE.autonomous`:** The 875 files in this directory make up a massive chunk of your data footprint. Classifying them broadly as machine-authored governance is a good placeholder for Session 1, but if these are automated state assertions or algorithmic consensus records, they may need to be split into a dynamic operational class (`LEDGER` expansions) rather than static policy text (`GOVERNANCE`).

---

### 2. Deposit-Flow Semantics (§2)

The eleven-stage pipeline functions with relentless deterministic logic. The data dependencies are perfectly ordered: you anchor the identity kernel before generating derived artifacts.

* **The Dependency of Stage 8 (Interlink):** The classification of Stage 8 sidecar updates as `CONDITIONAL` (dependent on explicit references) is conceptually correct but operationally dangerous. If a newly minted paper references a prior deposit, updating the old deposit's sidecar must be an **atomic extension of the mint itself**, not an optional post-mint luxury. If it fails, the citation graph fractures immediately.
* **The Logic of Stage 11 (Verify):** Your handling of Stage 11 is highly sophisticated. Allowing verification to fail without rolling back the mint honors the core thesis: *the canonical bytes in the repo are the truth; the web deployment is merely a temporary projection*.
* **A Missing Stage:** There is no explicit **Vectorization / Semantic Ingestion** stage in the primary flow. If a primary objective of the Enli Lucente pilot is ensuring appearance and accuracy in RAG and AI overviews, vector generation or SPXI embedding alignment should be formalized as a conditional or mandatory stage right alongside Stage 5 (Body-index) rather than being deferred entirely to post-mint enrichment.

---

### 3. The Fossilized-State Pathology (§4)

Your reconnaissance exposes an incredible structural irony: an archive built to resist centralized platform erosion is sabotaged by its own manual front-end literals.

* **The Framing is Correct:** This is absolutely a pathology, not a "design choice." Presenting the archive as systematically smaller than it is directly undermines its perceived authority and footprint.
* **The Remediation Strategy:** Your three-way partition (`frozen-at` attributes, build-time templates, and active investigations) is completely sound. Class (b)—converting counts to build-time template substitutions—is your highest-leverage operational win.
* **The Deeper Risk:** The threat isn't just that human readers see stale numbers; it's that LLMs and academic scrapers indexing `alexanarch.org` or `machinemediation.org` will ingest these fossilized literals as ground-truth metadata. The archive is accidentally feeding misinformation to the very machines it seeks to accurately inform. Remediation in Session 4 is an urgent priority.

---

### 4. Pathology Register & Session 3 Design (§5 & §6)

The assigned severities match the operational risks perfectly.

* **The Critical Nexus (PATHOLOGY-09 & PATHOLOGY-10):** The absolute highest priority for Session 3 must be tracing the `data-rhizome` XML corpus (3,627 files) and the multiple `registry.json` files. If the fleet sites are carrying decoupled, stale mirrors of the registry, the rhizome isn't functioning as a distributed network; it's functioning as a broken echo chamber.
* **A Missing Pathology:** You should register a **`PATHOLOGY-11: Index Interdependency Vulnerability`**. Because Stage 5 rebuilds massive, archive-wide files (`body-index.json`, `search-index.json`) on *every single mint*, the pipeline will hit a processing and storage bottleneck as the archive scales past a few thousand deposits. The archive needs a sharded or incremental indexing strategy before the data layer chokes on its own growth.

---

### Next Steps: Moving to Session 2

The structural scaffolding is rock-solid. You have built the taxonomy and diagnosed the leakage.

As you prepare to process Enli's corpus, Session 2's focus on auditing the currency of `chunk-010` and resolving the 875 autonomous files will give us the clean slate required to ingest her data without inherited noise.

The atlas is **approved for progression** to Session 2. Bring the hammer down on the fossilized values.
