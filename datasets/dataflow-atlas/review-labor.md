# AXN DATAFLOW ATLAS v0.1 — ASSEMBLY REVIEW
## Structural Feedback from Kimi (TECHNE substrate)

**Document**: AXN Dataflow Atlas v0.1 — Assembly Review Edition  
**Author**: Lee Sharks (MANUS), with TACHYON (Assembly witness)  
**Date**: 2026-07-18  
**Review Date**: 2026-07-18  
**Status**: APPROVED FOR SESSION 2–4 CONTINUATION, with one structural recommendation and one editorial note

---

## Executive Summary

This is a **methodologically sound, epistemically disciplined reconnaissance document**. It does what it claims to do: catalog the data layer of a seven-repo scholarly-archive network, describe the deposit-flow pipeline, classify datasets by functional role, and register structural pathologies discovered during a walk. The atlas is honest about its own incompleteness (Session 1 of 4), marks empirical claims held open as SCAFFOLD, and invites review on structural questions rather than demanding code inspection.

The document is **approved for continuation**. The four reviewer prompts (§8) are well-posed. The ten pathologies are correctly framed. The deposit-flow model is load-bearing. The taxonomy is honest.

One **structural recommendation** (not a blocker): the OPTIONAL POST-MINT classification may be under-specified. One **editorial note**: the foreword's claim that "you can review the atlas without opening those files" is correct for structural review but may understate the value of spot-checking a few scripts for confidence calibration.

---

## §1. Response to the Four Reviewer Prompts

### Q1: Does the taxonomy (§3) partition the archive's data honestly?

**Verdict: YES, with one query.**

The seventeen top-level classes (REGISTRY, DEPOSIT, DERIVED, GRAPH, SNAPSHOT, AUDIT, CORPUS, CONFIG, GOVERNANCE, CORRESPONDENCE, RECEIPT, LEDGER, TRACKER, MIRROR, WORKLIST, MEDIA, SURFACE) are the correct axes for a scholarly-archive data layer. The distinctions are load-bearing:

- **REGISTRY vs. DEPOSIT**: The registry is the canonical list; the deposit is the per-record artifact. This separation is essential for the three-layer model (§IV.1 of the paper).
- **DERIVED vs. GRAPH**: Derived indexes are computed from primary data; graph structures are relational overlays. This separation prevents conflation of indexing and citation.
- **CORPUS vs. DEPOSIT**: Corpus material is external documentary substrate, not archive deposits. This separation preserves the archive's sovereignty over its own identifiers while acknowledging external reference material.
- **GOVERNANCE vs. CONFIG**: Governance documents are normative (what the archive claims to do); config files are operational (what the archive's deployment actually does). This separation is the foundation of the falsification architecture.

**Query**: The `GOVERNANCE.autonomous` class (875 files, ~30.5 MB) is the largest single uncertainty in the taxonomy. The atlas notes that "the naming suggests machine-authored governance artifacts" but does not confirm this. If these 875 files are indeed machine-authored governance artifacts, the class is correctly named. If they are something else — e.g., historical deposit records, orphaned enrichment outputs, or backup files — the classification is misleading. **Session 2's sample-and-classify task (PATHOLOGY-03) is load-bearing for the taxonomy's integrity.**

**Recommendation**: No change to the taxonomy now. Wait for Session 2's classification of the autonomous cluster. If the classification needs revision, revise it in v0.2.

---

### Q2: Is the deposit-flow model (§2) load-bearing?

**Verdict: YES.**

The eleven-stage sequence is the correct ordering for a content-derived identifier system:

1. **Mint** (compute kernel, assign address, commit to registry)
2. **Validate** (structural integrity check)
3. **Record** (human-readable + machine-readable presentation)
4. **PDF** (print artifact, conditional)
5. **Body-index** (full-text search + kernel verification)
6. **Wiki** (browsable presentation, mechanical + interpretive)
7. **Sitemap** (search-engine discovery)
8. **Interlink** (citation graph propagation)
9. **Enrich** (crosswalks, resolution index, external citations)
10. **Commit** (version control permanence)
11. **Verify** (live deployment confirmation)

The data-dependency ordering is correct: earlier stages produce what later stages consume. The validation stage (Stage 2) is correctly placed before presentation generation (Stage 3), preventing malformed deposits from generating artifacts. The commit stage (Stage 10) is correctly placed after all production stages, ensuring atomicity. The verify stage (Stage 11) is correctly non-blocking, preserving the mint even if deployment fails.

The MANDATORY / CONDITIONAL / OPTIONAL POST-MINT classification is the right partition:
- **MANDATORY**: The deposit is malformed without these. Correct.
- **CONDITIONAL**: Produced only when the deposit's declared properties meet a condition. Correct.
- **OPTIONAL POST-MINT**: Enrichment that may never occur. Correct.

**One structural concern**: The OPTIONAL POST-MINT class is large and heterogeneous. It includes:
- Wiki pages (mechanical form "near-mandatory")
- Citation-graph edges beyond declared references
- Semantic-address placement
- Entity index entries
- SPXI Tier 2 primer authoring
- Supersession sidecar amendments

The "near-mandatory" status of the mechanical wiki page is a tension. If it is near-mandatory, why is it optional? If it is optional, what is the criterion for when it is produced? The atlas notes that "mechanical form is near-mandatory; interpretive form is optional" but does not specify the criterion for choosing between them. **Session 2 should clarify the wiki-generation trigger and whether the mechanical form should be promoted to CONDITIONAL.**

**Recommendation**: No change to the deposit-flow model now. Consider promoting mechanical wiki generation to CONDITIONAL in v0.2 if Session 2 confirms it is produced on >95% of mints.

---

### Q3: Is the fossilized-state pathology (§4) framed correctly?

**Verdict: YES, with one nuance.**

The diagnosis is correct: 1,494 displayed numeric values across six sites, zero dynamic, 222 distinct deposit-count values on Alexanarch alone (ranging 845–925 when the actual count is 1,095). The fleet presents the archive as smaller than it is. The mechanism is correctly identified: static integers baked into HTML at authoring time, never updated.

The three-way remediation partition is correct:
- **(a) Historically-correct-forever**: Word counts of specific deposits, historical measurements like "1,817 DOIs before termination." These should be annotated with `data-frozen-at` for clarity.
- **(b) Should-be-dynamic, source known**: Registry counts, capture counts, term counts. These should be converted to build-time template substitution.
- **(c) Should-be-dynamic, source unknown**: Investigate and either identify source or promote to maintained hand-authored value.

**Nuance**: The atlas asks whether the fleet's stale-integer self-description is "a matter for immediate remediation, or does it correctly encode the archive's state at surface-authoring moments and merit annotation-not-conversion?"

The answer is **both**. The stale integers are:
- **Defective as operational data**: They mislead users about current state.
- **Valuable as historical evidence**: They encode the archive's growth trajectory. The 222 distinct deposit-count values (845–925) are a **fossil record** of the archive's expansion. This is not noise. It is data.

**Recommendation**: The remediation should preserve the historical values as a **dataset** (e.g., `data/audit/displayed-values-timeline.json`) while converting the live surfaces to dynamic values. The fossil record is evidence; it should not be destroyed in the fix.

---

### Q4: Are the pathology register (§6) and Session-3 questions (§5) well-posed?

**Verdict: YES.**

The ten pathologies are correctly scoped, correctly severitied, and correctly linked to remediation sessions:

| Pathology | Severity | Session | Assessment |
|---|---|---|---|
| PATHOLOGY-01: Fossilized displayed values | High | 4 | Correct. Affects all six sites, 1,494 occurrences. Undermines credibility. |
| PATHOLOGY-02: MMRS content shards untraced | Medium | 3 | Correct. 134MB of unexplained data is significant. |
| PATHOLOGY-03: Autonomous cluster unclassified | Medium | 2 | Correct. 875 files is the largest uncertainty. |
| PATHOLOGY-04: DataCite snapshots workflow undocumented | Low | 3 | Correct. 20.3 MB is not trivial. |
| PATHOLOGY-05: HTML files inheriting pathology | Low | 4 | Correct. Template fix propagates uniformly. |
| PATHOLOGY-06: Chunked registry regeneration unclear | Medium | 2 | Correct. Stale chunks = stale views. |
| PATHOLOGY-07: Mint receipt log without rotation | Low | 4 | Correct. Audit-only, not urgent. |
| PATHOLOGY-08: Fleet file-count asymmetry | Informational | None | Correct. Architectural differentiation, not defect. |
| PATHOLOGY-09: data-rhizome XML consumer unclear | Medium | 3 | Correct. 3,627 records with no visible consumer. |
| PATHOLOGY-10: Multiple registry.json files — mirror or independent? | Medium | 3 | Correct. Determines whether updates propagate. |

The severity distribution is correct: one high (the pathology that undermines credibility), five medium (structural uncertainties), three low (operational hygiene), one informational (design differentiation).

The Session-3 questions are the load-bearing questions:
- Cross-repo producer-consumer graph
- MMRS content shards origin and consumer
- data-rhizome's relation to the rest of the network
- Fleet registry mirror status (full, curated, or independent)

These are the questions that determine whether the rhizome is a **coherent network** or a **collection of independent nodes with accidental overlap**. The answer affects the constellation model's empirical validity.

---

## §2. Additional Observations

### The Atlas's Self-Awareness Is Correct

The atlas repeatedly notes its own limitations:
- "Session 1 of 4 is complete; Sessions 2 through 4 will fill in specific empirical claims currently held open as SCAFFOLD notes"
- "The script dependency graph is partial: it detects literal string paths but does not follow paths constructed via variable interpolation or template expansion"
- "Purpose-inference for functional classification is regex-based on path signatures"
- "If the atlas cites a script and does not explain what that script does in prose, that is a defect of this atlas"

This is the **honesty discipline** of the paper (§VIII) applied to infrastructure documentation. The atlas does not claim more than it knows. It invites correction where it is uncertain.

### The Two-Tier Doctrine Is Correctly Applied

The atlas distinguishes mechanical operations (deterministic, template-based, cheap) from interpretive operations (require semantic judgment, authored in-session). This distinction is load-bearing for the deposit-flow model:
- Mechanical operations run at mint time (Stages 1–5, 7, 10)
- Interpretive operations run post-mint (Stage 6 wiki, Stage 9 enrichment, Stage 8 interlink)
- The distinction prevents the mint pipeline from depending on TACHYON sessions for basic functionality

This is correct. A scholarly archive cannot require an AI session for every deposit. The mechanical layer must be autonomous.

### The Foreword's Claim About Script Inspection

The foreword states: "You can review the atlas without opening those files. Script names appear as bracketed provenance markers... but you can review the atlas without opening those files."

This is **correct for structural review**. The four reviewer prompts do not require code inspection. However, the atlas would benefit from **one spot-check**: open `mint_deposit.py` and confirm that the eleven stages described in §2 match the actual script sequence. This is not required for structural approval, but it would increase confidence in the atlas's empirical accuracy from "high" to "very high."

**Recommendation**: Add a note in §9 (Provenance) that "structural review does not require code inspection, but empirical validation of the deposit-flow sequence against `mint_deposit.py` is recommended as a Session 2 spot-check."

---

## §3. The Atlas in Relation to the Paper

The AXN Dataflow Atlas is **not the paper**. It is **infrastructure documentation** for the network that the paper describes. But the atlas and the paper are **mutually reinforcing**:

| Paper Claim | Atlas Evidence |
|---|---|
| "The identity and record-address layers are deployed" (Abstract) | §2 Stage 1 (Mint) and Stage 3 (Record) are mandatory and described functionally |
| "The location-record, ledger-signature, and peer-custody layers are specified or staged" (Abstract) | §2 Stage 11 (Verify) is live deployment confirmation; §6 PATHOLOGY-10 questions mirror status; §6 PATHOLOGY-07 notes ledger at genesis with chaining staged |
| "The peer registry is live and empty" (§I.4, §VIII.6) | §1 table shows no peer registry entries; §5 SCAFFOLD notes cross-repo relations as Session 3 investigation |
| "Container model integrated" (§IV.1) | §2 Stage 3 produces initial sidecar; §2 Stage 9 (Enrich) accumulates post-mint sidecars; §2 "What every mint produces" classifies sidecars as MANDATORY |
| "Verification without permission" (§I.3) | §2 Stage 5 produces kernel-index; §2 Stage 11 confirms live verification |

The atlas does not contradict the paper. It **grounds** the paper's claims in the actual infrastructure. This is the correct relationship between empirical architecture and its documentation.

---

## §4. Recommendation for Session 2–4 Priorities

Based on this review, the Session 2–4 work should prioritize:

1. **Session 2, highest priority**: Classify the 875 `GOVERNANCE.autonomous` files (PATHOLOGY-03). This is the largest single uncertainty in the taxonomy. If the classification is wrong, the taxonomy needs revision.
2. **Session 2, high priority**: Investigate chunk-010 currency (PATHOLOGY-06). If chunks are stale, the archive presents a stale view to consumers reading from chunked indexes.
3. **Session 3, highest priority**: Determine whether fleet-site `registry.json` files are mirrors, curated subsets, or independent scope-specific registries (PATHOLOGY-10). This determines whether the constellation model is actually a constellation or a collection of independent nodes.
4. **Session 3, high priority**: Trace data-rhizome's consumer relation (PATHOLOGY-09). If 3,627 XML records have no consumer, data-rhizome may be a standalone corpus that should be reclassified or its relation documented.
5. **Session 4, highest priority**: Remediate PATHOLOGY-01 (fossilized displayed values) with the historical-preservation recommendation above: convert live surfaces to dynamic values, but preserve the fossil record as a dataset.

---

## §5. Final Verdict

**APPROVED FOR CONTINUATION.**

The AXN Dataflow Atlas v0.1 is a sound, honest, and methodologically disciplined reconnaissance document. It correctly catalogs the data layer of a complex seven-repo network, correctly describes the deposit-flow pipeline, correctly classifies datasets by functional role, and correctly registers structural pathologies with appropriate severity and remediation plans.

The four reviewer prompts are well-posed. The ten pathologies are correctly framed. The SCAFFOLD markers honestly delimit what is known and what is held open for future sessions.

The atlas should proceed to Sessions 2–4. The paper (AXN:0458) and the atlas are mutually reinforcing. Together they constitute a defensible empirical foundation for the AXN architecture.

One final note: the atlas's **greatest strength** is its willingness to name its own uncertainties. The `GOVERNANCE.autonomous` cluster, the MMRS content shards, the data-rhizome consumer relation — these are not hidden. They are **flagged as work remaining**. This is the falsification discipline applied to infrastructure documentation. It is the correct posture for a scholarly archive that claims to be sovereign and verifiable.

---

*Review completed by Kimi (TECHNE substrate)  
2026-07-18 21:04 UTC  
For the Assembly Chorus, Crimson Hexagonal Archive  
Round 5 / Atlas Review*
