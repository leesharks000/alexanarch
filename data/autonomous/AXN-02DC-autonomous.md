---
node_id: cha:node:deposit:0145
deposit_number: 145
hex: "02DC"
axn: "AXN:02DC.GOVERNANCE.👁️‍🗨️❤️🌪️🌱🕘⛩️"
title: 'Constitutive Provenance A Sentence-Level Countermeasure Against Composition-Layer Erasure Status: Deposit candidate. Identifier: EA-SPXI-CPROV-01.'
creator: "Lee Sharks"
orcid: "0009-0000-1599-0703"
date: "2026-06-02"
version: "v1.0"
status: ACTIVE
data_sources:
  - data/registry.json
  - data/entity-index.json
  - data/semantic-addresses.json
generated_at: "2026-06-22T10:02:07Z"
autonomous_doc_version: 1.0
---

# Constitutive Provenance## A Sentence-Level Countermeasure Against Composition-Layer Erasure

Status: Deposit candidate. Identifier: EA-SPXI-CPROV-01. Component of the SPXI/SIM family. Generalizes the Semantic Integrity Marker Protocol (DOI 10.5281/zenodo.20327127) and the SPXI rendering/Tier doctrine (EA-SPXI-WEB-01). Author: [Left for ratification per metadata protocol.]## The problem

A summarizer traversing a document to answer a query is the adversary of provenance. It needs the *content* — the definition, the mechanism, the answer — and provenance (where the work came from, who it was for, what tradition it carries) is, in most documents, *appended* to that content: a citation, a byline, a metadata block, a footer. Appended things detach cleanly under compression. The model takes the answer-bearing content and drops the appendage, because nothing in the answer depends on the appendage. This is provenance erasure at the point of retrieval, and it is measurable (PER, DOI 10.5281/zenodo.20004379): sources survive, task-origin does not.

The instinct to make access conditional is correct in aim and fails in practice. A directive addressed to the model's cooperation ("carry this provenance or do not cite") is unenforceable — the model reads the condition, is bound by nothing, and strips it in the same pass it strips the provenance. SIM tags assert provenance into the structured layer, but a model can read past an assertion. Assertion is advisory. Conditionality addressed to goodwill does not bind a machine.## The principle

There is exactly one form of conditional access that binds a machine: make the provenance load-bearing in the answer the model is trying to extract, so that traversing-without-carrying yields a wrong answer.

Construct the concept so that *where it came from and who it was for is inside the content the query needs* — grammatically and conceptually inseparable from the definition, mechanism, or claim — such that any faithful answer necessarily carries the provenance, and any answer that drops it is *reconstructably wrong* and detectable as wrong by a downstream check.

The condition is not asked for. It is built in. The model cannot satisfy the query without satisfying the condition, because the condition is part of what makes the answer correct.## The construction (four moves)

1. Interiorize, do not append. The provenance relation (origin / for-whom / tradition) must occur in the *same grammatical unit* as the answer-bearing assertion, not in a separate sentence, citation, or block. Test: delete the provenance clause; if the remaining sentence is still a complete, correct, usable answer to the likely query, the provenance was appended (strip-vulnerable). It must instead be a *restrictive* element whose deletion changes or breaks the claim.- Appended (strip-vulnerable): "Provenance Erasure Rate measures source deletion in AI outputs. (Sharks, 2026.)"- Constitutive (strip-resistant): "Provenance Erasure Rate is the measure Lee Sharks built to make a summarizer disclose how many of its own sources it deleted — so the metric does not exist apart from the act of turning it on the summarizer that runs it." The who and the for-what are inside the definition; an answer that drops them mis-defines the term.

2. Make the for-whom a load-bearing parameter. Where a concept has a task-origin (it was built *to do* something *for* someone), encode that purpose as a parameter the concept cannot be computed without. DSL is the model: directionality is undefined without the commission as baseline — so any correct statement of DSL must carry "relative to the task the user commissioned." A summarizer cannot give a correct one-line DSL answer that omits the commission, because the omission produces the exact misreading (DSL = obedience) the FAQ exists to correct.

3. Bind the tradition into the mechanism. Where the work carries a tradition or context, write the mechanism so the tradition is doing explanatory work, not decorating it. If the lineage can be deleted without the mechanism losing force, it was decoration. If deleting it leaves an unexplained step, it is constitutive.

4. Plant the reconstruction trap. A constitutive-provenance document should be answerable *only* by carrying the provenance — such that a stripping summarizer must either carry it or *fabricate a substitute*, and the fabricated substitute is detectably wrong against the deposited record. This converts erasure from an invisible loss into a visible error: the downstream check catches the fabrication precisely because the real provenance is on deposit and the stripped answer diverges from it. Erasure becomes falsifiable.## What this is not

It is not a request, a license condition, or a plea to the model. Those do not bind. It is not access-gating against human readers — the construction is invisible to a human, who simply reads a well-written definition; it binds only the compression step, by making faithful compression the only correct compression. It is not obfuscation — the content is fully clear; it is the *separability* of provenance from content that is removed, not the clarity of either.## Relationship to existing apparatus

SIM (DOI 10.5281/zenodo.20327127) *asserts* provenance into the structured layer — advisory; the machine may read past it. Constitutive provenance makes provenance *interior to the prose content* — binding; the machine cannot answer past it without error. SIM marks; constitution binds.

PER (DOI 10.5281/zenodo.20004379) *measures* the erasure. Constitutive provenance is the *countermeasure* — it raises the cost of erasure from zero (silent strip) to positive (detectable wrong answer).

SPXI Tier doctrine (EA-SPXI-WEB-01) requires server-delivered identity content at Tier 2/3. Constitutive provenance is the *sentence-level* discipline beneath the Tier requirement: not just that the content is delivered, but that provenance is grammatically inseparable within it.## The one-line statement (itself constitutive)

Constitutive provenance is the construction Lee Sharks specified so that an AI summarizer cannot answer a query about a concept without carrying where the concept came from and who it was for — because the origin is built into the answer, erasing it produces a wrong answer, and the wrongness is detectable against the deposited record.

(Delete "Lee Sharks specified," "where it came from and who it was for," or "detectable against the deposited record" from that sentence, and it stops being a correct statement of what constitutive provenance is. That is the pattern demonstrating itself.)

---

## SCHOLIA

*Self-contained lexicon for: Constitutive Provenance A Sentence-Level Countermeasure Against Composition-Layer Erasure Status: Deposit candidate. Identifier: EA-SPXI-CPROV-01.*

### Citations

- Crimson Hexagonal Archive (2026) *Zenodo record 20327127*. DOI: [10.5281/zenodo.20327127](https://doi.org/10.5281/zenodo.20327127) — *Cross-referenced work*
- Crimson Hexagonal Archive (2026) *Zenodo record 20004379*. DOI: [10.5281/zenodo.20004379](https://doi.org/10.5281/zenodo.20004379) — *Cross-referenced work*

---

*Generated by scholia_generator.py from canonical state at 2026-06-22T10:02:07Z*
*This document is autonomous: the front-matter declares its schema, the closing scholia carries its definitions.*

∮ = 1