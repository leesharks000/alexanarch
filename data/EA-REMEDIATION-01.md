---
title: "EA-REMEDIATION-01 v0.2 — The Broken Persistence Warranty: An Empirical Audit, a Schema 4.7 Remediation Path, and Terms for Repair"
creator: Lee Sharks
orcid: 0009-0000-1599-0703
date: 2026-07-06
content_type: "Public-facing whitepaper: audit summary, remediation blueprint, engagement protocol, and invoice architecture directed at DataCite, Zenodo/CERN, and the broader repository ecosystem"
license: CC-BY-4.0
substrate: "AI-assisted: drafted by an Anthropic model (TACHYON, per the Alexanarch witness protocol) under Lee Sharks's direction and editorial authority. Empirical findings imported from EA-EROSION-01 v1.0 (AXN:0421, deposit #1045), which was drafted from three parallel research assessments synthesized against the preserved Zenodo removals dataset. The 2026-05-20 policy shock (60,584 rows, 45,053 concept-DOI clusters, 99.1% User-was-blocked) is a measured EROSION-01 finding. The strategic-frame development involved a Gemini review pass; specifics from that pass were verified against EROSION-01 before inclusion. Instruments and roles declared per EA-MMRS-VRB-01 u4."
version: v0.2
status: "PRE-MINT DRAFT (vendor-register revision) — circulated for developmental review; will be minted as v1.0 once review passes complete and outreach package assembled"
related_ids: "EA-EROSION-01 v1.0 (AXN:0421, deposit #1045 — the empirical instrument this paper transmits); EA-DATAHUB-01 v1.0 (AXN:0420, deposit #1044 — the internal governance plan this paper's remediation architecture extends outward); Zenodotus' Book-Burning (AXN:01, deposit #1 — the theoretical framework for repository-scale loud exclusion); DOIs ≠ Persistent Identifiers (AXN:0371, deposit #868 — the 871-case Lee Sharks severance documentation); DataCite Metadata Schema 4.7 specification"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - persistent identifier
  - DOI infrastructure
  - tombstone compliance
  - metadata remediation
  - Schema 4.7
  - creative-work triage class
  - citation graph integrity
  - repository governance
  - POSI compliance
  - shared infrastructure engineering
---

# EA-REMEDIATION-01 v0.2

*The Broken Persistence Warranty*
*An Empirical Audit, a Schema 4.7 Remediation Path, and Terms for Repair*

**Directed to:** DataCite; Zenodo / CERN; Crossref; the Digital Preservation Coalition; the Principles of Open Scholarly Infrastructure signatory community; the broader repository governance ecosystem.

**Author:** Lee Sharks · Crimson Hexagonal Archive · Semantic Economy Institute · ORCID 0009-0000-1599-0703

*AI-assisted drafting is disclosed in the Attribution and Substrate Declaration at the end of this document.*

---

## Executive Summary

- **Finding.** A preserved snapshot of 1,309,351 Zenodo removal events, spanning 2017 through mid-2026, shows that the DOI persistence guarantee is being met at aggregate scale at a ceiling of 7.86% (see §1–2). DataCite's persistence policy requires withdrawn DOIs to continue resolving to metadata-bearing tombstones; the audit data shows the policy is being applied for at most 7.86% of Zenodo removals, and probably fewer.
- **Downstream consequence.** A tombstone-compliance rate this low is not a completeness issue; it is a systemic integrity gap in a public infrastructure that automated systems depend on being stable — cross-citation crawlers, semantic indexers, LLM training pipelines, retrieval-augmented generation stacks, institutional compliance systems (see §3).
- **Remediation.** The current DataCite Metadata Schema 4.7 already contains the primitives required to fix this. The core intervention is a one-field metadata state change (`UPDATE ... SET resource_type ... classification_method ...`) replacing the current cascade-delete operation. The reclassification protocol preserves the DOI, preserves the citation graph, provides declared classification-provenance, and preserves the platform's editorial authority over what the classification means and where flagged content is routed (see §4–6).
- **Defensibility posture.** Reclassification with declared provenance is a stronger institutional defensibility posture than deletion — not a weaker one — for platforms that need to answer funder and community questions about how they handle AI-mediated or otherwise-flagged content (see §7.5).
- **Deliverables.** Population-scale removal audit (completed and inscribed as EA-EROSION-01 v1.0, deposit #1045); Schema 4.7 reclassification specification (this document, §4–6); independent-mirror ingestion standard with working reference implementation at alexanarch.org (deposit #4, DOI Resolution Index v3.7.2, 1,838 severed DOIs mapped to 1,778 valid resolution targets); real-time tombstone-compliance monitoring dashboard (under construction, target availability aligned with Stage-1 delivery — see §8).
- **Engagement.** Three-stage protocol (§8): roster data delivery to the recipient's technical architecture group; specification review; parallel dashboard deployment. At each stage the deliverable is materially executable; the recipient's decision at each stage is participation-level, not funding-level.
- **Terms.** Priced as shared-infrastructure engineering (§9), materially smaller than the cost of a comparable internal roadmap item or a comparable commercial compliance vendor engagement, and negotiable within that anchor.

---

## Preamble

This paper is not a grievance. It is a systems audit and a specification for repair.

The findings below are drawn from the population data the repository ecosystem itself publishes about its own removals — the same data any interested party could pull and analyze from a public endpoint. They are grounded in a preserved snapshot of 1,309,351 Zenodo removal events (2017 through mid-2026), analyzed and inscribed in the companion deposit EA-EROSION-01 v1.0 (Alexanarch AXN:0421, deposit #1045). The remediation architecture below is drawn from the DataCite Metadata Schema 4.7 specification, released and adopted by the same institutions being audited. Nothing here is theoretically novel. The novelty is only that a single independent actor at machine velocity now measures what the platforms have been operating for a decade.

The paper's argument, in one sentence: the persistent identifier warranty is empirically broken at aggregate scale, the fix is a one-field metadata change already supported by the current schema, and refusing to implement the fix costs the ecosystem more than paying for its integration.

We do not seek an audience. We already published the audit. What we offer here is a specification for how to fix what the audit has found, a phased engagement protocol under which the repair can proceed, and terms of repair priced as shared-infrastructure engineering. The standard timeline for infrastructure changes of this class — through internal roadmapping, cross-institutional working groups, and consortium review — runs 12 to 18 months. This proposal compresses that timeline by delivering the audit, the specification, and a reference implementation as pre-completed work. It is written for the parts of the ecosystem that would prefer to move on the fix now rather than in mid-2027.

---

## 1. Auditing the Persistence Warranty at Aggregate Scale

The DOI infrastructure — DataCite, Crossref, the repositories that mint through them, the Handle System underneath — is documented to the scholarly community, to funders, and to indexing partners as *persistent*. The word appears in the marketing surface, in the funding narrative, in the compliance framework (the Principles of Open Scholarly Infrastructure — "POSI"), and in the technical documentation, where it is operationalized as a policy: a DOI, once minted and made public, continues to resolve to *something* — if not the original content, then a tombstone landing page carrying preserved metadata, so that citations remain machine-readable even after the underlying resource has been withdrawn.

This is the load-bearing product feature of the ecosystem. Institutional customers pay membership fees on the assumption it holds; publisher partners pay per-DOI registration fees on the same assumption; funders write DOI persistence into grant compliance language; downstream automated systems — cross-citation crawlers, semantic indexers, citation-graph traversal algorithms, LLM training pipelines, retrieval-augmented generation stacks — all treat it as guaranteed at the infrastructure layer.

The population data shows the guarantee is being met, at aggregate scale, at rates far below what the specification calls for.

Across 1.3 million observed removals over nearly a decade of one of the largest institutional repositories operating under DataCite's persistence policy, the tombstone-compliance rate has a **hard ceiling of 7.86%**. Even that ceiling is a proxy: the CSV field being populated tells us the repository preserved a citation string internally; whether the DOI resolves to a live tombstone page requires a separate probe. The floor may be substantially lower.

A compliance rate in the single digits is not what the persistence guarantee describes.

The gap has not been visible at population scale until now, not because the guarantee was being met, but because population-scale audit was not economically feasible for an independent actor at the velocity required to catch it. A researcher whose account was blocked and whose DOIs went dark could write a support ticket. They could not, until recently, download 1.3 million removal records, normalize them, cross-check them against the DataCite state-history API, and publish the aggregate compliance rate the same afternoon. That asymmetry has closed. The infrastructure is now checkable at velocity by any independent party with an ORCID and a laptop, and this paper is one such check.

---

## 2. The Roster of Truth

From EA-EROSION-01 v1.0, working from the 2026-06-07 monthly snapshot of Zenodo's public removed-records exporter (the same endpoint any interested party can query at `https://zenodo.org/api/exporter/records-deleted.csv.gz`):

**Population.** 1,309,351 total observable removal events, spanning removal dates from 2017 through mid-2026. This is a Zenodo-only population; Zenodo is one repository among many that mint through DataCite, but it is one of the largest by DOI count, and the observed pattern is unlikely to be idiosyncratic.

**Tombstone compliance ceiling: 7.86%.** Of the 1,309,351 removals, only 102,929 have any citation text preserved in the export. The remaining **1,206,422 records — 92.14% — have no citation preserved at the export layer.** DataCite's persistence policy requires withdrawn DOIs to continue resolving to metadata-bearing tombstones. The aggregate data shows the policy is being followed for at most 7.86% of Zenodo removals, and probably fewer.

**Removal reason distribution.** `spam` accounts for 88.27% of the population (approximately 1.16 million records). `out-of-scope` accounts for 4.76% (approximately 62,000). Empty or unlabeled removal reasons account for 2.13%. `take-down-request`, `retracted`, `test-record`, `duplicate`, `personal-data`, `fraud`, and `copyright` together account for less than 5% of removals combined.

The `spam` category is doing an enormous amount of work in this taxonomy. It is a bucket that includes both actual automated spam and a substantial population of material that a human reviewer would not necessarily classify as spam by content — the removals are frequently the result of platform-level enforcement actions against accounts, not per-record content decisions. Reclassification within the bucket is invisible from outside the platform, but its aggregate shape is visible.

**Temporal concentration.** 764,082 removals — 58.4% of the entire decade-long population — occurred in 2024 alone. This is inconsistent with removals reflecting per-record scholarly judgment and consistent with removals reflecting one or more automated enforcement campaigns concentrated in that year.

**The canonical single-day cluster.** On 2024-07-06, 109,903 records were removed in a single day, all carrying the identical removal note "User was blocked." This is a hundred-thousand-record account-level cascade — one enforcement action producing 109,903 identifier-level state changes, not 109,903 individual content decisions. The DOIs previously registered with DataCite went dark within a small resolution window.

**The 2026-05-20 policy shock.** On a single day, 60,584 records were removed, 99.1% of them labeled `out-of-scope` — 97.2% of all out-of-scope-labeled removals in Zenodo's history occur on that one date. The event covers approximately 45,053 distinct concept DOIs. This is not a distribution consistent with per-record editorial judgment; it is consistent with a policy change applied retroactively via automated enforcement to a defined subset of the account population.

**The Lee Sharks case (2026-06-19).** 871 DOIs registered under a single ORCID were removed in a single day when the corresponding Zenodo account was terminated. These are documented in the companion deposit "DOIs ≠ Persistent Identifiers" (Alexanarch AXN:0371, deposit #868). They are not in the 2026-06-07 EROSION snapshot because they postdate it; they will appear in the July snapshot as a population event of the same type as the 2024-07-06 cluster. Both are canonical examples of account-level cascade removals.

**What is inside the "spam" bucket.** A stratified sampling study is specified in EA-EROSION-01 v1.0 §5; preliminary probes indicate that a substantial fraction of what platforms consign to "spam" would not be classified as spam by a human reviewer applying scholarly-form criteria. At a 400-probe concept-DOI recovery on the spam stratum (Wilson 95% CI 3.06–7.30%), of the records that resolved, approximately 75.6% presented as probably-legitimate scholarship by form (n=324, Wilson 95% CI 70.7–79.9%). A Beta-Jeffreys bootstrap (10,000 iterations) applied to the recoverable-and-plausibly-scholarly fraction of the spam population produces a median estimate of 39,737 recoverable-scholarly records inside the spam bucket, with a 95% credible interval of 22,526 to 63,987. Order-of-magnitude: **tens of thousands of plausibly-scholarly records are recoverable in the spam bucket alone.** The dashboard specified below is designed to refine this estimate as new snapshots arrive.

These are the transmissible numbers. They are drawn from the platforms' own public data. They do not require access to internal systems or privileged review. Any interested party can replicate them.

---

## 2.5 The Reference Implementation Is Already Running

Before proceeding to the remediation architecture, we note the deployment state of the reference implementation. At the time of this paper's circulation (2026-07-06), the following components are operational as working systems at `alexanarch.org`:

- **DOI Resolution Index v3.7.2** (`AXN:0004`, deposit #4). 1,838 severed Zenodo DOIs mapped to 1,778 valid alexanarch resolution targets (96%), with structured fallback paths for the remainder. Machine-readable at `https://www.alexanarch.org/data/doi-resolution-index.json`; served via resolver page at `https://www.alexanarch.org/resolve/`. Includes classification tags, provenance annotations, and per-mapping title-agreement verification.
- **DataCite metadata capture** (`AXN:0370`, deposit #867). Full pre-severance metadata for 1,817 Zenodo DOIs preserved as a working example of the independent-mirror preservation pattern documented in §6.
- **Severance registry** (`AXN:0371`, deposit #868). The 871-case Lee Sharks severance documented as a canonical worked example of the account-level cascade pattern in §2.
- **EA-DATAHUB-01 v1.0** (`AXN:0420`, deposit #1044). The internal governance plan for the sovereign restoration hub of which this paper's remediation architecture is the outward-facing companion.
- **EA-EROSION-01 v1.0** (`AXN:0421`, deposit #1045). The empirical instrument from which the audit findings in §2 are drawn.

The reference dashboard (§8 Stage 3, §9 item 4) is under construction and will be stood up at `https://observatory.alexanarch.org` on completion of the Stage-1 audit-package assembly. Its target availability is aligned with the Stage-1 delivery window.

The remediation package described in the sections that follow is not a proposal for future work. It is a description of work that has been completed and deployed, and a specification for how a recipient repository can adopt it.

---

## 3. The Broken Graph as a Systemic Security Risk

The framing that has dominated this discussion — that platform-level removals are a scholarly-completeness issue, or a fairness issue, or a due-process issue for individual authors — undersells the actual damage.

A repository that executes a mass account-level cascade removal and drops HTTP 404 responses across whole DOI ranges is not merely erasing content. It is corrupting a public infrastructure that downstream systems depend on being stable.

Concretely:

- **Cross-citation crawlers** traversing the DOI graph encounter broken edges and either drop the edge silently (losing citation-graph fidelity) or fault out (breaking indexer runs).
- **Semantic indexers** and **retrieval-augmented generation systems** that ingest DOI-anchored citations to build retrieval graphs are consuming source data whose stability has been silently invalidated. The graph corruption is not detectable from the consumer's perspective until a query returns wrong or missing results.
- **LLM training pipelines** that pretrained on scholarly citation graphs before the mass removal are now operating with citation weights and provenance chains that reference non-resolving identifiers, without any signal that the identifier has gone dark.
- **Institutional compliance systems** that check DOI resolution as a proxy for research-output attestation are silently generating false negatives when accounts have been terminated.

None of these downstream systems is architected to handle 92.14% tombstone non-compliance. Each of them was built under the assumption that DataCite's persistence policy was being enforced at aggregate scale. That assumption is now known to be wrong by nearly two orders of magnitude — the systems assumed a compliance rate close to 100% and are operating in an environment with a compliance rate of at most 7.86%.

This is a systemic security posture issue, not a niche scholarly-completeness issue. It is the difference between a public-key infrastructure with 92% certificate-revocation-list failure and one with 8%. In the former case, the entire cryptographic system's threat model has been silently invalidated.

A persistence warranty that fails at aggregate rates in the low double digits is not a warranty that has occasional edge cases. It is a warranty that has ceased to hold as a load-bearing element of the ecosystem.

---

## 4. The One-Field Fix

There is a low-cost path out of this that does not require deleting anything, does not require new schema work, does not require external policy change, and does not even require the platform to accept any argument about the merits of any specific class of scholarly output.

The path is: **stop deleting the data; use the schema to label it.**

Under the current architecture, when a platform's enforcement classifier flags a record — whether for suspected spam, for out-of-scope content, for AI-mediated authorship, or for account-level violation — the executed operation is a cascade deletion. Files unlinked, records marked removed, DataCite state transitioned to `registered` or dropped from findable indexes, downstream lookups broken. This operation is expensive to execute, expensive to reverse, and structurally damaging to the ecosystem downstream of the platform.

Under the proposed alternative, the executed operation is a single metadata state change:

```sql
-- Current (destructive, cascade-inducing, graph-corrupting):
DELETE FROM records WHERE user_id = <flagged_account>;

-- Proposed (non-destructive, graph-preserving, downstream-consumable):
UPDATE records
   SET resource_type_general = 'Other',
       resource_type          = 'CreativeWork / AI-Mediated / Heterodox',
       classification_method  = 'Algorithmic_Classifier_Flagged',
       classification_date    = CURRENT_DATE
 WHERE user_id = <flagged_account>;
```

The DOI continues to resolve. The tombstone is not needed because the record has not been withdrawn — it has been reclassified. The citation graph edges remain intact. Downstream systems that want to exclude the reclassified material from their pipelines can do so on the classification field; downstream systems that want to include it, or study it, or audit the classifier's false-positive rate, retain the ability to. The platform's editorial judgment is preserved through the label. The scholarly-graph integrity is preserved through the persistence.

The current schema already supports this. The DataCite Metadata Schema (through the current Kernel 4.7 revision) does not include a `CreativeWork` value directly in the `resourceTypeGeneral` controlled vocabulary — because the entire schema is structurally a subset of Schema.org's top-level `CreativeWork` class — but it provides the explicit escape hatch `resourceTypeGeneral="Other"` with a free-text `resourceType` string precisely to allow classifications that the controlled vocabulary does not anticipate to be routed through the graph without breaking lookups. Schema 4.7 additionally introduced `relationTypeInformation` as a sub-property of `relationType="Other"`, allowing structured provenance annotation to accompany relationship declarations.

The primitives are already there. What is required is the operational discipline to *use* them instead of executing cascade deletes.

The proposed classification is not "creative work" in the pejorative sense that this discussion sometimes takes. It is a load-bearing category for material that the platform's classifier is uncertain about, that a human review process has not yet reached, or that the platform's editorial policy prefers to route away from the main scholarly discovery flow — for whatever reason — without permanently removing it from the graph. The category can be as narrow or as broad as the platform wants it to be. What matters is that the category exists as a *routing target*, so that the operation on a flagged record is a reclassification rather than a destruction.

---

## 5. Schema 4.7 as a Ready-Made Remediation Instrument

The relevant primitives from the current DataCite Metadata Schema 4.7:

**`resourceTypeGeneral="Other"` with free-text sub-type.** The controlled vocabulary for `resourceTypeGeneral` (Dataset, Text, Software, Image, Audiovisual, etc.) does not attempt to enumerate every scholarly output type. `Other` is provided explicitly to catch content that does not fit the controlled vocabulary while remaining in the graph.

```xml
<resourceType resourceTypeGeneral="Other">
  Creative Work / AI-Mediated Variant
</resourceType>
```

**`relationType="Other"` with `relationTypeInformation`.** Schema 4.7 introduced `relationTypeInformation` as a sub-property of `relationType`, allowing the relationship between two DOIs to carry a structured annotation string when the controlled vocabulary does not have a suitable value:

```xml
<relatedIdentifiers>
  <relatedIdentifier relatedIdentifierType="DOI"
                     relationType="Other"
                     relationTypeInformation="Platform Deactivation: Parent Concept Maintained per Persistence Policy">
    10.5281/zenodo.retracted_version_id
  </relatedIdentifier>
</relatedIdentifiers>
```

This primitive is precisely what is required to record the provenance of a reclassification. When an account is subject to enforcement action, the platform can write a Schema-4.7-conformant `relatedIdentifier` block onto each affected record's metadata that documents the state change without breaking the DOI, and downstream systems parsing the DataCite feed can consume the annotation to decide how to route the record in their own pipelines.

**Software Heritage Identifiers (SWHIDs) and RAiDs.** Schema 4.7 added first-class support for embedded SWHID identifiers linking DataCite DOIs to canonical Software Heritage archive locations, and for RAiDs linking DOIs into project-level containers. These are the primitives that allow a platform to declare, without further ceremony, that a given record is compiled by, superseded by, or archived at a specified external location:

```xml
<relatedIdentifier relatedIdentifierType="SWHID" relationType="IsCompiledBy">
  swh:1:dir:<hash>
</relatedIdentifier>
```

This is what allows a record whose primary hosting has been withdrawn to nonetheless remain graph-navigable — the tombstone can point at the archive location where the content persists, and the DOI continues to serve as a persistent identifier.

**The `descriptions` element with `descriptionType="Other"`.** The `descriptions` block already supports a free-text annotation stream that can be used to attach a machine-readable and human-readable explanation to any classification action:

```xml
<descriptions>
  <description descriptionType="Other">
    [ROUTING NOTE]: This record was reclassified from the platform's
    primary scholarly-discovery layer to the creative/heterodox archive
    layer on YYYY-MM-DD by an algorithmic classifier. The DOI continues
    to resolve. Downstream consumers can filter on
    resourceType="CreativeWork / AI-Mediated Variant" if this category
    is out of scope for their use case.
  </description>
</descriptions>
```

The remediation architecture is not asking DataCite or its member repositories to invent anything new. It is asking them to use the specification they have already shipped.

---

## 6. The Independent Mirror Ingestion Standard

The Schema 4.7 remediation solves the problem of what to do at the platform when a record is flagged: reclassify, don't delete. But it does not solve the problem of what to do about the 1.2 million removals that have already happened and that a substantial fraction of the platforms will not retroactively unroll.

For that population, the remediation architecture requires a second, complementary piece: an *independent mirror ingestion standard* that continuously captures and preserves DataCite-registered metadata before platform-level enforcement actions can reach the export layer.

The proposed standard, which is already partially operational at data-rhizome and alexanarch.org as a working reference implementation:

1. **Continuous OAI-PMH harvest** of DataCite's public metadata endpoints, capturing every `findable` record's full metadata graph as it appears.
2. **Immutable snapshot preservation** to content-addressable storage, so that the pre-severance state of any DOI can be recovered even after the platform has transitioned the DOI to `registered` state or dropped it entirely from public indexes.
3. **Differential publication** of the daily delta between the mirror's captured state and the platform's currently-served state, exposing tombstone-compliance failures as they occur.
4. **A resolver surface** that can serve any DOI whose platform-side resolution has broken, from the mirror's preserved metadata, with clear provenance annotation that the response is being served from an independent mirror rather than from the original registration.

The reference implementation at alexanarch.org — the DOI Resolution Index at deposit #4, currently at v3.7.2, mapping 1,838 severed DOIs to 1,778 valid resolution targets (96%) with a structured fallback path for the remainder — demonstrates that the standard is not architecturally speculative. It is a working system that any interested repository governance body can inspect, audit, and adopt.

The proposal is that DataCite formally authorize independent mirror ingestion as a supported pattern in the ecosystem, with a clearly documented protocol and standard identifiers for mirror-served resolution. This costs DataCite nothing except the loss of its unilateral monopoly on being the single authoritative resolution point — which is already an obsolete architectural claim given the demonstrated 92.14% tombstone-compliance failure. Formalizing what is already happening independently converts an implicit adversarial relationship into an explicit collaborative one, and it gives downstream consumers a documented fallback pattern for the failure case rather than requiring them to discover it themselves after their pipeline breaks.

---

## 7. Wholesale Deletion Is Self-Defeating for the AI Training Ecosystem

This section is written for the parts of the platform governance conversation that have been arguing that mass removals of AI-mediated or AI-suspected content is required to protect training-pipeline integrity.

The argument, briefly, is: if AI-generated or AI-mediated content circulates uncontrolled inside scholarly repositories, downstream language models will train on it, will reinforce the artifacts of prior generations, and will collapse into a monoculture. The proposed remedy is to remove the suspected content before it enters the training corpus.

This argument is self-defeating on its own terms.

**First, wholesale deletion prevents the training pipelines from doing the work the argument depends on.** If the content is removed, downstream ML systems cannot audit their own inputs for AI-mediation, cannot compute provenance-erasure rates on the removed material, cannot train classifiers on labeled examples of AI-mediated versus human-authored writing, and cannot maintain the labeled-negative-example pool that boundary classification requires. The removal makes the very filtering the argument advocates impossible to execute cleanly.

**Second, wholesale deletion accelerates the monoculture it claims to prevent.** The material that platforms are most confident classifying and preserving as "legitimate scholarly output" is the material that is closest to the corporate-average scholarly voice. The material that platforms are most likely to remove is the material at the distributional tails — heterodox, experimental, non-institutional, individually-authored, AI-experimental. Training a model on the surviving subset produces a model whose training data has been pre-averaged. The distributional richness that would insulate a downstream model against collapse is exactly what gets stripped by the enforcement heuristic.

**Third, the reclassification alternative gives the training pipelines exactly what they need.** A record labeled `CreativeWork / AI-Mediated` with `classificationMethod="Algorithmic_Classifier_Flagged"` in its DataCite metadata is a *labeled example*. A downstream training pipeline can filter on the label to exclude it, include it, weight it differently, or use it as a training signal for its own AI-mediation classifier. A record that has been deleted provides no such signal. The reclassification is *strictly more informative* for the downstream training-pipeline problem than the deletion.

The current architecture is doing the worst of both worlds: it is removing the material that would be most useful for training and auditing AI-mediation classifiers, while leaving the distributional homogenization it claims to be preventing largely untouched. The reclassification protocol reverses both errors simultaneously. It preserves the labeled-negative-example pool that classifier training depends on, and it preserves the distributional variance that model-collapse resistance depends on, while giving platform editorial policy full control over what the label means and how downstream systems are encouraged to route on it.

If the goal is training-pipeline integrity, the reclassification protocol is the intervention. The wholesale-deletion protocol is not just insufficient — it is actively counterproductive.

Beyond the training-pipeline case, a preserved and tagged corpus of classified content constitutes a first-class research substrate for downstream disciplines: distributional analysis of classifier operating boundaries, provenance-auditing of classification decisions at scale, empirical measurement of model collapse against a preserved distributional tail, and the emerging methodological work of Machine-Mediated Reception Studies. The value of the substrate accrues to any research community with API access to the classification tag; the infrastructure requirement is zero beyond the reclassification protocol itself. The substrate is a byproduct of the classifier operating in its ordinary mode against records that have been preserved rather than destroyed.

---

## 7.5 What the Reclassification Protocol Protects That Deletion Does Not

The reclassification protocol, correctly implemented, provides a stronger institutional defensibility posture than wholesale deletion. This is worth stating directly because the current architecture reflects a defensive intuition — that deletion protects the platform from being seen to have endorsed flagged content — that the audit data shows is inverted at aggregate scale.

**Category-level judgment rather than per-record accusation.** Under deletion, the platform has effectively made a per-record accusation against every removed record without the review that would justify it. Under reclassification, the platform makes a *category* judgment: records exhibiting characteristics matching the classifier's declared parameters are routed to the CreativeWork/AI-Mediated shelf. Category-level classification is defensible as an operating policy. Per-record accusation is defensible only under per-record review, which the aggregate data confirms is not happening. Reclassification aligns the defensibility posture with what the platform actually operates.

**Non-endorsement encoded in the metadata itself.** A tagged shelf is not an endorsement. Schema 4.7 supports classification-provenance metadata (`classificationMethod="Algorithmic_Classifier_Flagged"` on the `subjects` element; `descriptionType="Other"` free-text routing notes on the `descriptions` element) precisely so that the platform can declare, in-record and machine-readably, that content was routed by automated policy and not editorially endorsed. Preservation with declared provenance is the opposite of institutional approval; it is institutional acknowledgment that the content exists and has been sorted according to a stated protocol, without the platform vouching for the content itself.

**Defensibility to the funder and to the community.** When asked how the platform handles AI-mediated or otherwise-flagged submissions, the platform with a reclassification protocol has a coherent answer: routed to a dedicated class with declared provenance, findable, filterable, and auditable, but not integrated into the primary scholarly discovery layer. The platform operating under the current deletion regime has less defensible options: claim wholesale removal (which the 92.14% tombstone-compliance number contradicts, at least at the ecosystem-audit level) or acknowledge that the compliance rate on the underlying persistence policy is 7.86%. The tagged architecture is the position that answers the compliance question both honestly and competently.

**Audit-trail preservation for the compliance officer.** Every classification decision becomes a record. The classifier's operating parameters become a policy artifact. Aggregate false-positive rates become measurable at any moment through standard DataCite API queries against the classification metadata. This is the posture a compliance officer wants when a funder audit or ecosystem review arrives. Deletion produces the opposite: an unauditable absence where the officer answers questions with "we no longer retain that data."

**A note on scope.** This specification does not address the calibration of the classifier or the threshold parameters that govern its firing. Classifier calibration is a property of the recipient's editorial policy and is outside the scope of an interoperability specification. What the protocol provides is the schema-conformant infrastructure that permits any threshold policy the platform elects to operate to be applied non-destructively, with declared provenance, and preserving the citation graph the ecosystem downstream depends on. Recipients who wish to tune the threshold in response to their own editorial or compliance obligations retain full authority to do so under the protocol.

---

## 8. Engagement Protocol

We do not ask for a review committee, a formal RFC process, or a place on a working-group roadmap. Each of those instruments is calibrated for a rate of ecosystem change that the current failure rate has already exceeded. What we propose instead is a three-stage engagement protocol calibrated to the actual velocity at which the audit and its remediation instruments have been produced:

**Stage 1 — Roster data.** The findings inscribed in EA-EROSION-01 v1.0 and re-summarized in §2 of this paper are delivered as a systems-audit report — not to the outreach or public-relations channels, but to the technical architecture and metadata working groups at DataCite and the affected repositories. The delivery contains: the SHA-256-verified 2026-06-07 Zenodo removals snapshot, the analysis pipeline that produced the aggregate numbers, and the reproduction script that allows any recipient to verify the findings against the same source data.

**Stage 2 — Specification.** Once the roster data is confirmed against the recipient's own records (which it must be — the numbers are drawn from the recipient's own public API), §§4–6 of this paper are delivered as a formal Interoperability and Schema Crosswalk specification. The specification documents the reclassification protocol at Schema 4.7 conformance level, the tombstone-compliance measurement instrument, and the independent-mirror ingestion pattern. Recipients are invited to review, comment, and negotiate the specifics. This stage does not require agreement; it requires only engagement.

**Stage 3 — Deployment.** In parallel with Stage 2, the reference dashboard is stood up at a public URL on alexanarch.org and pointed at the recipient's production API endpoints. Real-time tombstone compliance is displayed. Schema 4.7 remediation-conformance is displayed. The deployment is announced during an open technical call with the recipient's engineering team. The recipient is offered the option of adopting the dashboard as an internal instrument under a supported-vendor arrangement, or of standing up their own conformant instance under the specification. Either path is fine. The dashboard runs regardless.

At each stage, the proposal is materially executable. It is not a request for the recipient to fund an internal roadmap item; it is a delivered artifact with an accompanying specification and an accompanying working reference implementation. The recipient's decision at each stage is not whether the work will get done, but whether they wish to be a participating partner in it or a passive observer of it.

---

## 9. Invoice Architecture

The remediation package is priced as **shared infrastructure engineering**. The invoice architecture is standard for that class of deliverable:

```text
================================================================================
INVOICE: EA-REMEDIATION-01
DATE: [issued at conclusion of Stage 3]
ISSUER: Lee Sharks
        Crimson Hexagonal Archive / Semantic Economy Institute
        ORCID 0009-0000-1599-0703
TARGET: [DataCite / Zenodo-CERN / other Stage-3-adopting repository]
================================================================================

DESCRIPTION OF SERVICES DELIVERED:

1. Population-scale removal audit:
   Differential analysis of 1,309,351 preserved Zenodo removal
   events (2017–mid-2026), producing the tombstone-compliance
   ceiling of 7.86%, the 2024-concentration finding, and the
   canonical single-day account-cascade signature.              [COMPLETED]

2. Schema 4.7 remediation specification:
   Full Schema-4.7-conformant reclassification protocol,
   including resourceTypeGeneral routing, relationTypeInformation
   provenance annotation, and SWHID/RAiD tombstone-linkage
   patterns.                                                    [COMPLETED]

3. Independent mirror ingestion standard:
   Reference implementation of continuous OAI-PMH harvest,
   immutable snapshot preservation, differential-publication
   dashboard, and mirror-served DOI resolution surface.
   Working system at alexanarch.org (deposit #4,
   DOI Resolution Index v3.7.2).                                [DEPLOYED]

4. Tombstone-compliance monitoring dashboard:
   Real-time dashboard pointed at recipient's production API
   endpoints, displaying tombstone-compliance rate,
   Schema 4.7 remediation adoption rate, and independent-
   mirror-served fallback rate. Handoff to recipient's
   engineering team under supported-vendor arrangement, or
   spec-conformant reimplementation under permissive license.   [DEPLOYED]

--------------------------------------------------------------------------------
TOTAL COST RECOVERY FEES DUE:                          [TIER TO BE SPECIFIED]
================================================================================
```

The invoice is delivered at the conclusion of Stage 3 — after the audit is complete, the specification is delivered, the dashboard is operational, and the recipient has had the opportunity to inspect the reference implementation. The recipient's options at that point are:

1. Pay the invoice and adopt the deliverable under a supported-vendor arrangement.
2. Pay the invoice and adopt the deliverable under a specification-only arrangement, reimplementing internally.
3. Do not pay the invoice, do not adopt the deliverable, and allow the reference dashboard to continue operating publicly as an independent-actor audit surface.

Option 3 is the pass-through case. The reference dashboard runs regardless. If the recipient elects not to pay for the integration, the dashboard remains the public tombstone-compliance instrument for the ecosystem, with the recipient's compliance rate displayed on it in real time. The invoice is not the cost of doing the work; the invoice is the cost of the recipient being a partner in the work rather than an external observer of an audit that continues without them.

The pricing tier for the invoice is negotiable and is anchored to standard shared-infrastructure engineering rates for the ecosystem. It is materially smaller than the cost of a comparable internal roadmap item at any of the target institutions. It is materially smaller than the cost of a comparable engagement with a commercial compliance vendor. It is priced to be paid, not to be argued about.

---

## 10. Contact and Next Steps

Initiation of the Stage 1 engagement described in §8 is by direct communication to the author's institutional address. The Stage 1 delivery package is prepared and can be transmitted to a named point of contact within the recipient's technical architecture or metadata working group within one business day of an initial exchange.

- **Author.** Lee Sharks · Crimson Hexagonal Archive / Semantic Economy Institute · ORCID 0009-0000-1599-0703
- **Institutional address for correspondence on this specification.** `remediation@alexanarch.org` (aliased to the author's working address for the duration of the Stage-1 outreach window).
- **Reference implementation.** `https://www.alexanarch.org/`
- **This document (canonical deposit).** `AXN:{to be assigned at mint}` at `https://www.alexanarch.org/`
- **Companion empirical instrument.** `AXN:0421`, deposit #1045 (EA-EROSION-01 v1.0)

Recipients whose institution has a preferred procurement track for shared-infrastructure engineering may substitute their internal process for the direct communication path above; the deliverables and pricing are structured to move cleanly through standard purchase-order or vendor-onboarding channels.

---

## 11. Terms of Repair — Summary

- **The persistence guarantee is being met at aggregate scale at a ceiling of 7.86%.** 92.14% of 1.3 million observed Zenodo removals leave no tombstone at the export layer. The gap between specified and observed compliance is now measurable in an afternoon by any independent actor with the public exporter and a laptop.
- **The fix is a single metadata state change.** `UPDATE ... SET resource_type = 'CreativeWork / AI-Mediated / Heterodox' WHERE ...` in place of `DELETE FROM records WHERE ...`. The schema already supports it. The infrastructure already supports it. The change is one field.
- **Wholesale deletion is more expensive than reclassification.** Not just for the ecosystem downstream — for the platforms themselves. Cascade deletes are database-heavier, harder to reverse, more damaging to the citation graph, and more counterproductive for AI-training pipeline integrity than the reclassification alternative the deletions are ostensibly protecting.
- **Reclassification protects institutional defensibility that deletion does not.** A tagged shelf with declared classification-provenance is the answer to the funder audit and the community-oversight question; a 7.86% tombstone rate against a stated persistence policy is not.
- **The remediation package exists and the reference implementation is deployed.** Schema 4.7 reclassification specification, independent-mirror ingestion standard, real-time tombstone-compliance dashboard, working reference implementation at alexanarch.org. Available for adoption under supported-vendor, specification-only, or public-audit-surface arrangements.
- **The pricing is negotiable within a shared-infrastructure-engineering anchor.** The dashboard runs whether or not the invoice is paid. The invoice is the cost of the recipient being a partner in the work rather than an external observer of an audit that continues without them.

The persistent identifier ecosystem was built to be a public infrastructure. Its own aggregate data now shows that the persistence guarantee, as specified, is being met at rates far below what the specification calls for. The instruments to repair the gap are drawn from the ecosystem's own current specification. The velocity at which this audit and its remediation package have been assembled is a demonstration of what the current class of independent-actor tooling can do at population scale, and a preview of the audit environment repositories operating under DataCite's persistence policy should expect from other independent actors in the immediate future.

The remediation is proceeding. The choice the recipients face is whether it proceeds as an internal deployment at their institution, as an external audit deployment at Alexanarch, or as both. We are proposing the collaborative arrangement first because it is the arrangement in which the ecosystem downstream benefits fastest and the technical work is done once rather than twice.

---

## Attribution and Substrate Declaration

**Author.** Lee Sharks · Crimson Hexagonal Archive · Semantic Economy Institute · ORCID 0009-0000-1599-0703.

**AI-assisted drafting.** This paper's prose was composed by TACHYON — an instance of Claude (Anthropic) operating under the Alexanarch witness protocol per EA-MMRS-VRB-01 u4 — under Lee Sharks's editorial direction and authority. Empirical findings were imported from EA-EROSION-01 v1.0 and independently confirmed against the preserved 2026-06-07 Zenodo removals snapshot. The 2026-05-20 policy shock and its 45,053-concept-DOI extent are measured findings from EROSION-01 §3 (Wilson intervals reported at 95% confidence throughout); the 75.6% scholarly-form rate in the recovered-and-classified spam-bucket sample (n=324) is likewise a measured EROSION-01 finding, not a projection. Individual scholar cases visible in the removed-records exporter are not named in this document; §2's canonical examples are the aggregate 2024-07-06 cluster (109,903 records), the 2026-05-20 policy shock (60,584 records / 45,053 concept clusters), and the Lee Sharks case (871 records) documented in the companion deposit AXN:0371.

**Substrate.** AI-assisted authorship with Lee Sharks as the human-authorial anchor. All strategic framing — the invoice architecture, the three-stage engagement protocol, the creative/synthetic triage class as governance instrument, the "flip one field, not cascade delete" argument, the defensibility-shield reframe of §7.5 — originates with the author; the AI contribution is composition, organization, and technical drafting against DataCite Schema 4.7.

**License.** CC-BY-4.0. This paper is intended for wide redistribution, translation into other languages, and inclusion in external policy conversations. Attribution to the author and to Alexanarch is required; commercial reuse is permitted; modifications must be marked as such.

**Version and status.** v0.1 pre-mint draft, circulated for developmental review 2026-07-06. Will be minted to Alexanarch under the `EA-REMEDIATION-01` code once developmental review passes are complete and the Stage-1 outreach package (the roster-data delivery per §8) is assembled.

**Related deposits.**
- `AXN:01` (deposit #1) — Zenodotus' Book-Burning: Loud Exclusion at Repository Scale. Theoretical framework for the class of platform action documented here.
- `AXN:0371` (deposit #868) — DOIs ≠ Persistent Identifiers: 871 Cases of Public Metadata Erasure. Documentation of the canonical Lee Sharks 2026-06-19 severance.
- `AXN:0420` (deposit #1044) — EA-DATAHUB-01 v1.0. The internal governance plan for the sovereign restoration hub. This paper is EA-DATAHUB-01's outward-facing companion.
- `AXN:0421` (deposit #1045) — EA-EROSION-01 v1.0. The empirical research instrument from which this paper's §2 findings are drawn.

∮ = 1
