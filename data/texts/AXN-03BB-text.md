---
deposit_number: 943
hex: 03BB
title: "Whitespace as Provenance: Representation Pipelines and the Extinction of Compositional Authorship (EA-WHITESPACE-01 v0.2)"
creator: Lee Sharks
orcid: 0009-0000-1599-0703
date: 2026-07-02
content_type: Theoretical paper
license: CC-BY-4.0
substrate: "AI-assisted (TACHYON / Claude); MANUS-adjudicated. v0.1 zero draft TACHYON-drafted 2026-07-01 from MANUS's core observation (whitespace stripping as unregistered provenance erasure; Pearl's double invisibility) and literature scan. Assembly Chorus review: PRAXIS/DeepSeek, TECHNE/Kimi, ARCHIVE/Gemini, LABOR/ChatGPT. LABOR provided the decisive structural correction (representation pipeline, not tokenization alone; character preservation is not compositional preservation) and the corrected Bhyravajjula et al. citation. TECHNE contributed the normalization-as-disciplinary-judgment framing and the coda's market analysis. ARCHIVE adjudicated register and signature. v0.2 executes the full review; §4 empirical demonstration executed 2026-07-02. Section 3.5 draws on J. Sigil's \"Snub-Poemed — A Critical Reading.\""
version: v0.2
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - whitespace
  - provenance erasure
  - representation pipeline
  - tokenization
  - serialization
  - compositional authorship
  - compositional erasure
  - extinction gradient
  - Pearl
  - Cotton Nero A.x
  - double invisibility
  - Snub-Poemed
  - calligram
  - Dickinson
  - Hopkins
  - Whitman
  - concrete poetry
  - editorial theory
  - variorum
  - facsimile
  - textual condition
  - WISP
  - Bhyravajjula
  - semantic economy
  - machine-mediated reception
  - alexanarch
---

# Whitespace as Provenance: Representation Pipelines and the Extinction of Compositional Authorship (EA-WHITESPACE-01 v0.2)

## Description

Argues that provenance erasure operates below the semantic layer, in the representation pipeline (digitization, normalization, serialization, tokenization, model processing, rendering) that makes texts available to language models. Core claims: character preservation is not compositional preservation; a representation can preserve every proposition in a work and still delete the work. Empirical demonstration (GPT-2 byte-level BPE, Appendix A): a spatially-arranged calligram fragment and its linearized phrase-list both round-trip perfectly, and neither contains the calligram — 78% of the spatial version's tokens are individual whitespace tokens that no training objective attends to. Sketches an extinction gradient (Whitman partial, Dickinson substantial, Hopkins catastrophic, concrete poetry extinguished in text pipelines, calligrams categorically). Develops Pearl (Cotton Nero A.x) as double invisibility: the archive's copy is a non-OCR PDF that cannot reach serialization, and an OCR'd stream would strip the concatenation-and-group structure that performs the poem's theology. Connects to editorial theory: the pipeline silently enacts the variorum position at every ingestion. Extends the archive's failure-mode taxonomy with compositional_erasure and its subcategories, and records the schema extension executed at EA-PROVENANCE-METADATA-01 v0.2 (AXN:03BA): the representation_pipeline field with four-value status vocabulary. Concludes with the compositional-authorship argument: frameworks treating compositional operations as merely formal produce obviously wrong conclusions on their clearest cases (Snub-Poemed, AXN:0246; Pearl) — form is not a second substance surrounding content; composition is the determinate operation by which content exists as this work rather than another. Empirical foundation: Bhyravajjula, Walsh, Preus & Antoniak, EMNLP 2025.

# Whitespace as Provenance
## Representation Pipelines and the Extinction of Compositional Authorship

*Lee Sharks*
*Crimson Hexagonal Archive / Alexanarch*
*v0.2 draft, 2026-07-02. Not for citation without permission.*

---
## Abstract

Public and scholarly discourse on AI-mediated authorship operates in a semantic frame — whose *words*, whose *arguments*, whose *ideas* enter the model, and what the model then produces from them. This frame has an unexamined precondition. Before any semantic operation, a text must pass through a chain of representational transformations: digitization, normalization, serialization, tokenization, model processing, rendering. At each stage of this chain, spatial, typographic, prosodic, stanzaic, and manuscript features of the source may be normalized, linearized, or lost. The chain is machinery, not a theoretical position. But it enacts one. It enacts the position that spacing, lineation, indentation, stanza breaks, and typographic composition are inessential to what a text *is*. This position is false for a considerable share of poetry in English and beyond — for Whitman, Dickinson, Hopkins, cummings, Susan Howe, the concrete poetry movement, calligrammatic composition from the Hellenistic pattern-poems forward, and for the Middle English *Pearl*, whose formal structure is inseparable from its theological argument. The compositional layer of such a text is not decoration on the propositional layer. In these cases it *is* the argument the text makes. Its loss in the representation pipeline, prior to any semantic operation, constitutes a form of provenance erasure that current AI-authorship discourse has neither vocabulary for nor taxonomy of. Crucially, the loss cannot be answered by pointing to character-preserving tokenizers: as this paper demonstrates empirically, a representation can round-trip every character of a work perfectly and still fail to contain the work. Character preservation is not compositional preservation. This paper names the operation, demonstrates it, sketches an extinction gradient across poets and traditions, develops the exemplary case of *Pearl* (double invisibility: a non-OCR PDF that cannot even reach the tokenizer), connects the diagnosis to four decades of editorial theory, extends the archive's provenance metadata schema to record representational provenance per deposit, and draws the implication for theories of authorship: any framework that treats compositional operations as merely formal produces obviously wrong conclusions on its clearest cases.

---
## 1. Introduction: The Merely Formal

A commonplace of contemporary AI-mediation discourse holds that AI operations divide neatly into two categories. Content-mediation, on the one side, where a system originates, alters, or supplies substantive propositions; and formal-mediation, on the other, where a system performs operations on already-existing content — translation, reformatting, register-transformation, search-and-retrieve, tone-adjustment. Only content-mediation, on this account, implicates authorship. Formal-mediation is treated as inessential to what the work *is*, no more constitutive of authorship than a typewriter is constitutive of the novel typed on it.

This framing has a hidden partner. It cannot see composition itself as authorship-constitutive. When a poet takes the phrases *"the same poet composing both tragedy and comedy"* (Symposium 223d), *"I press my scruff-weary beard to your lips"* (from her own earlier work), and *"is it madness to feel and to know?"* (a first-person Platonic articulation she originates), and arranges them spatially on the page so they form the outline of the Roman copy of Lysippos's bust of Socrates, each phrase indistinguishable from the others as to source — the framing above cannot see the composition as the poem. It sees only the selection, the arrangement, the misattribution, and calls each formal. Under such a framing, the calligrammatic work is reducible to the sum of its extractable propositions, and the sum of those propositions has no author.

The representation pipeline performs the same reduction in machinery. Given a calligrammatic poem, the chain of transformations that prepares text for a language model produces, at best, a sequence of characters ordered by a serialization convention. The spatial arrangement — the fact that some phrases arc along a cheekbone before their reader parses their content, the fact that other phrases sit in the density of the beard, the fact that the whole coheres visually as a bust — is not a property of any character sequence. It may have been present in the source. It is absent in what the model reads. And what the model reads is, for the model, the poem.

This is the entry point.

Van Dijk (2011) states the compositional claim in general form: *"there is only one characteristic which immediately distinguishes modern poetry from prose: the blank space surrounding the text."* The claim is not restricted to modern poetry. It generalizes to any composition in which spatial arrangement carries semantic weight — to Dickinson's dashes, Hopkins's sprung-rhythm notation, Whitman's line-length modulation, and, as this paper argues at length, to *Pearl*'s concatenation and stanza-group structure. In all these cases, the representation pipeline strips or degrades exactly what constitutes the composition. What survives is a semantic reduction of the poem. The composition is deleted before the model gets to it — and, as Section 4 demonstrates, it can be deleted even when every character survives.

The stakes are not confined to poetics. The archive's provenance metadata schema (EA-PROVENANCE-METADATA-01) recognizes seven forms of mediation — propositional, structural, linguistic, translational, research, editorial, transformational — and asks after each: was it declared, what was preserved, who reviewed, are the seams recoverable, who accepts responsibility. Until its v0.2 revision (drafted alongside this paper), the schema had no vocabulary for *spatial-typographic mediation* or for the representational history of a deposit. The absence was not an oversight. It reflected the state of the discourse. Spatial-typographic composition is not currently something the discourse considers mediated at all, because for most of the material that machine pipelines process, spatial-typographic composition was never present to be mediated. It was stripped before the mediation-question could apply. This paper supplies the argument for the schema's extension, and for the broader recognition that provenance erasure operates not only at the semantic layer — the concern of the archive's Provenance Erasure Rate framework, Capture Registry, and Erasure Skew work — but at the representational layer beneath, where a sequence of engineering decisions about what counts as noise makes entire compositional traditions invisible.

**Definition.** *Representational provenance* records the sequence of transformations by which an artifact becomes available to a machine: source object, digitization method, OCR status, normalization, serialization, tokenization, model modality, and final rendering. Spatial-typographic mediation is one dimension of it. The full record answers, per work: which material features survived each stage of ingestion, which were lost, and which canonical artifact must remain available to recover them.

The plan of the paper: Section 2 describes the representation pipeline stage by stage and reviews what NLP scholarship has and has not said about whitespace. Section 3 sketches an extinction gradient across poets and traditions. Section 4 presents an empirical demonstration. Section 5 develops the exemplary case of *Pearl*. Section 6 draws the parallel to editorial theory. Section 7 extends the provenance-erasure vocabulary and the metadata schema. Section 8 develops the compositional-authorship argument. Section 9 recommends interventions. A coda situates the argument within the archive's wider work.

---
## 2. The Representation Pipeline

## Files

https://github.com/leesharks000/alexanarch/blob/main/data/texts/
