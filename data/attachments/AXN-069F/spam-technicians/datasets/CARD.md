---
license: cc-by-4.0
pretty_name: Spam Technicians — the source-admission ontology cluster, translated out of prose (argument as dataset)
language:
- en
tags:
- argumentation
- claim-evidence
- epistemic-status
- knowledge-graph
- retrieval
- crimson-hexagonal-archive
size_categories:
- n<1K
configs:
{configs}
---

# Spam Technicians

*{maxim}*

> Blessed are the telemarketers, and spam technicians, and those whom no one wants to talk to on the phone, or over email.
>
> — *I Am X, Be Y, Blessed is the Z*, "BLESSED IS…" (Crimson Hexagonal Archive #328, [AXN:0083](https://www.alexanarch.org/s/axn/0083/), sha256 0137fd4b09443f91…; also in *Antioch: A Volume of Poems*, #331, AXN:0086; and the Prophetic Catalog's gloss, #83, AXN:0255: "the spam technician and the archive builder share a structural position")

**Why the name.** The cluster this dataset decomposes shows a fleet of twenty-nine hosts under one author scoring, on every link-topology feature computable from outside, where the web-spam literature's positive class scores, and a poem deposited in January had already blessed the position. The name is the poem's; the provenance link is above; the dataset is the argument.

**What this is.** A paper cluster translated out of prose. The documents — EA-MIRROR-01 (*What Not Reading Did to Its Own Ontology*), the fleet topology report of 2026-09-15, #1612 (*What Enters Composition Through the Cards*, AXN:069D), #1611 (*The Negative of the Negative*, AXN:069B), and the records they cite — survive here only as provenance: `source_document`, `source_version`, `source_section`, `source_locus`, `deposit`, `axn`. The primary units are the argument's own: {n_claims} atomic claims, {n_evidence} evidence objects (including measurement gaps recorded as data), {n_relations} typed relations, {n_tests} specified tests, {n_terms} defined terms, and a derived `support_topology` with one row per claim. Built {built}.

**The discipline it preserves.** Every claim carries an `epistemic_status` from a controlled vocabulary — measured_internal · measured_external · literature_claim · model_implication · hypothesis · model_consequence · specified_test · strategic_corollary · structural_reading · definition · falsified_in_test · ruling — and a `level` (measured · classical_model · contemporary_hypothesis · model_consequence · strategic · structural · definitional · self). This is the three-level separation the source papers keep: what the audit measures, what classical trust-graph models imply, what is hypothesised of contemporary retrieval. No claim carries a confidence score. The `support_topology` config shows, per claim, what supports it at which level, what contradicts or qualifies it, what measurement is missing, and which tests bear on it.

**What a consumer can ask.** *What exactly is measured about the source-relative update barrier?* — the topology shows: nothing directly; tied/untied behaviour is consistent with it; the negative-bleed trace and the gate-reception test are the discriminating experiments, specified and not run. *What would falsify the topology explanation?* — walk from C-FLEET-VECTOR to its measurement gaps and to T-WEBSPAM-SCORE. *Did the mirror survive its own test?* — C-ADMITTED-LIKE-FLEET is falsified_in_test, superseded by C-TOPOLOGY-DISCRIMINATES, with T-VF-VA run and its result evidence attached.

**Configs.** `claims` (claim_id, claim, claim_class, epistemic_status, scope, conditions, level, provenance, superseded_by, note) · `evidence` (evidence_id, evidence_type, statement, variable, value, unit, measurement_date, status, capture_ids, provenance) · `relations` (subject_id, relation ∈ supports · constrains · depends_on · entails_under_model · contradicts · qualifies · illustrates · operationalizes · formalizes · tests · falsifies_if · revises · analogizes · instantiates · scopes · measures_gap_of · reads_against · names, object_id) · `tests` (test_id, name, tests_claims, input, prediction, falsifies_if, status ∈ specified_not_run · run · partially_run · blocked, result, result_date, result_evidence) · `terms` (term_id, term, definition, introduced_in, prior_articulation, status_kind) · `support_topology` (derived).

**Seating rule.** A claim enters only with a section and, where the sentence can be located, a locus; evidence enters with its measurement date and status, and a measurement that was not made enters as `measurement_gap`; a relation enters only between ids that exist; a test that has been run carries its result and the evidence ids that constitute it; a term that names something the archive had already named carries `prior_articulation`. The builder rejects dangling ids and any claim marked measured without a supporting evidence relation.

**Provenance.** Source of truth `datasets/argument-as-dataset/rows.json` in `leesharks000/alexanarch` (proposed), validated against `schema.json`, built by `scripts/build_argument_as_dataset.py`. Companion datasets: `leesharks/negative-of-the-negative` (concept-keyed intervention); proposed Hub name for this dataset `leesharks/spam-technicians`, `leesharks/crimson-hexagonal-archive` (the records). Author: Lee Sharks, ORCID 0009-0000-1599-0703. License CC BY 4.0.
