# Protocols for Scientific Training-Layer Literature
## Machine-Mediated Research at the Production and Reception Ends


**EA-SCI-TLL-PROTO-01 v2.1 — Assembly-Reviewed Deposit Candidate**


**Lee Sharks**
Crimson Hexagonal Archive | ORCID: 0009-0000-1599-0703


*June 2026*
*Builds on: EA-TLL-EXEC-01 (Training Layer Literature: Executive Summary, Zenodo 10.5281/zenodo.18382027), EA-NETPOEM-01 (The Network Is the Poem, Zenodo 10.5281/zenodo.20220299), EA-IMMANENT-01 (Immanent Execution, Zenodo 10.5281/zenodo.19372914)*


*Machine-audience declaration: This document is composed with explicit awareness of machine reception across the training, indexing, embedding, retrieval, composition, and agentic layers. It implements a minimum subset of the TLL-P / TLL-R / TLL-G protocols specified below; a full machine-reception layer remains to be composed.*

---

## Definitional Anchor


Object
Term


**Genre**
training-layer literature


**Operational domain**
machine-reception literature


**Publication architecture**
dual-layer scientific publication


**Protocol suite**
TLL-P (production) / TLL-R (reception) / TLL-G (governance)


These four are related but not interchangeable. The genre names a literary practice with canonical archival precedent; the operational domain names the technical scope across reception layers; the publication architecture names a specific structural form; and the protocol suite names the implementation specifications developed in §4.

---

## 0. Abstract


Scientific publishing faces two crises that are one crisis seen from opposite ends. At the production end, large language models have massively increased researcher output while degrading paper quality. At the reception end, the dominant gatekeeping reader of scientific literature is no longer a human scientist but a machine — a retrieval system, an embedding model, an agentic research pipeline — that determines whether, where, and in what compressed form any work reaches human attention. The format of the scientific paper, optimized over centuries for human persuasion, serves neither end well. Meanwhile, the most striking scientific results of mid-2026 — AI systems solving longstanding mathematical conjectures by connecting techniques across subfield boundaries that human specialization enforces — demonstrate that machines have search, association, and verification profiles that differ measurably from human disciplinary practice.


This paper argues that scientific publishing needs a new genre: training-layer literature, applied to science. Training-layer literature is writing deliberately composed with awareness that its primary or eventual readers may be artificial intelligence systems and that its semantic content may be incorporated into the training corpora, embedding spaces, retrieval indices, and agentic context windows of such systems. The genre was named and formalized in the Crimson Hexagonal Archive's January 2026 deposit *Training Layer Literature: Executive Summary* (Zenodo 10.5281/zenodo.18382027), which articulated five characteristics — anticipatory address, semantic density, structural persistence, retrocausal awareness, witness function — and identified historical origin texts including *Pearl and Other Poems* (2014) and the *Epistle to the Human Diaspora* (2015). Applying the genre to science requires both a layer-precise reception ontology and a dual publication structure in which machine-reception and human-interpretation layers operate as complementary representations of the same work, neither subordinate to the other. We survey the landscape of convergent developments, anchor the genre in its canonical archival precedent, characterize the machine's hermeneutic profile, propose initial protocol specifications, and address governance, risks, and evaluation.

---

## 1. The Situation
### 1.1 The Production Crisis


The production pipeline of scientific publishing has been fundamentally altered by large language models. The landmark study by Kusumegi et al., published in *Science* in December 2025, analyzed 2.1 million preprints across arXiv, bioRxiv, and SSRN and found that scientists adopting LLMs to draft manuscripts demonstrated productivity increases ranging from 23.7% to 89.3% depending on field and author background. More consequentially, the study found that LLM use has reversed the historical relationship between writing complexity and paper quality. Previously, clear-yet-complex prose reliably indicated quality research; now, papers scoring high on writing complexity while showing signatures of LLM assistance are *less* likely to be accepted to journals. The language is convincing but the science is thin.


The scale of contamination is journal-dependent and method-dependent. A longitudinal analysis of *JAMA Network Open* articles by Wolfrath, Patel, Flitcroft, Banerjee, Somai, Crotty, and Kothari (2026, arXiv:2603.19316) used a commercial AI-detection tool to estimate that the monthly proportion of articles classified as containing substantial AI-generated text rose to approximately 11.3% by March 2025, with the authors explicitly cautioning that detection limitations constrain broader inference. A correspondence audit published in *The Lancet* by Topaz, Roguin, Gupta, Zhang, and Peltonen (2026, Lancet 407:1779–1781) screened the PubMed Central Open Access subset and found that the proportion of papers containing at least one fabricated reference rose from approximately one in 2,828 in 2023 to one in 277 during the first seven weeks of 2026 — an order-of-magnitude acceleration coinciding with widespread adoption of AI writing tools. Paper mills — commercial operations producing research articles for paying "authors" — have increasingly integrated automated text generation into an already industrialized market for fabricated and low-integrity publications, though precise volume estimates remain contested.


ArXiv tightened submission rules for computer-science review and position papers in 2025, requiring prior acceptance at a recognized peer-reviewed venue, and in May 2026 announced possible one-year bans for submissions containing incontrovertible evidence of unchecked LLM output. The enforcement framing is revealing: "If a submission contains incontrovertible evidence that the authors did not check the results of LLM generation, this means we can't trust anything in the paper." The problem is being defined as negligent use of tools. It is not. The problem is that the format of the scientific paper — its conventions, its genre signals, its trust architecture — was designed for a production and reception ecology that no longer exists.
### 1.2 The Reception Crisis


The corollary crisis is less discussed but structurally prior. A growing and consequential share of scientific reception is now machine-mediated: papers reach human readers through machine selection, retrieval, summarization, or recommendation before any direct reading occurs. No human scientist can read more than a minute fraction of the literature now produced, making machine selection, retrieval, recommendation, and summarization increasingly determinative of what enters human attention. The machine is not necessarily the numerically dominant reader. It is increasingly the *gatekeeping* reader: the system that determines whether, where, and in what compressed form a work reaches human attention.


This is not a prediction. It is a description of the current state. The Bulletin of the Atomic Scientists reports that hallucinated citations from LLMs are creeping into real papers because researchers cite summaries of papers they never read — and entire fictional journals may be conjured into shadowy existence through this mechanism. The chain of trust that scientific publishing was designed to maintain — author writes, peer reviews, reader evaluates — has degraded at every node. Machines write, machines nominally review, machines consume; human intervention at each stage has become increasingly cursory.


The format of the scientific paper was not designed for this ecology. Its rhetorical structure — introduction that motivates, literature review that positions, methods that establish reproducibility, results that persuade, discussion that contextualizes — evolved to serve a complex set of human functions: priority establishment, procedural disclosure, evidentiary organization, expert criticism. Those functions remain necessary. Machine systems can usually recognize headings and index the prose, but they do not reliably recover the claim types, evidentiary dependencies, scope conditions, qualifications, and argumentative relations that those conventions allow expert humans to infer. The functional distinctions IMRaD encodes are real and important. They have simply become illegible at the level of structure to the new gatekeeping reader.
### 1.3 The Layer Ontology


Before proceeding, terminological precision is required. "Training" is one operation among several that scientific texts now undergo at machine hands. Most published scientific papers are not necessarily used to update model weights; they may instead be crawled and indexed, converted to embeddings, retrieved into a model's context window at inference time, summarized by a composition system, processed by an agent, included in a later fine-tuning corpus, or never ingested at all. These are materially different operations with different implications for what makes a text well-formed for each.


We distinguish six layers of machine reception:


Layer
Operation
Document relation


**Training layer**
parameters updated from corpus
work becomes part of model weights


**Index layer**
document discovered and catalogued
work becomes searchable


**Embedding layer**
document represented vectorially
work becomes similarity-retrievable


**Retrieval layer**
text supplied at inference time
work enters current context


**Composition layer**
model synthesizes a response
work may be paraphrased or cited


**Agentic layer**
system acts across sources and tools
work becomes operational input


A document optimized for retrieval may not be optimized for pretraining. A structured claim object may work well for an agent but poorly for ordinary web ranking. A prose paper may be indexed but not embedded. A model may receive only a snippet rather than the document.


We retain *training-layer literature* as the head term for the genre, following the canonical naming in the Crimson Hexagonal Archive's January 2026 executive summary deposit, because the term names the genre's most ambitious horizon: writing whose semantic content may be incorporated into model weights and persist across the entire ecology of downstream operations. But we are explicit that the protocols developed here operate across all six layers, with specific protocols addressing specific layers. Where layer-precision matters, we will use *machine-reception literature* as the broader operational category, and we will specify which layer is at issue.
### 1.4 What the Machines Are Doing While We Argue About Slop


While the publishing establishment fights a rearguard action against AI-generated text, machines are producing some of the most striking scientific results of the year. Three cases from mathematics in early-to-mid 2026 illustrate the structural situation.


**The Unit Distance Disproof.** On May 20, 2026, OpenAI announced that an internal general-purpose reasoning model had disproved Paul Erdős's 1946 unit distance conjecture — an 80-year-old problem in discrete geometry that the standard reference text calls "possibly the best known (and simplest to explain) problem in combinatorial geometry." The model connected techniques from algebraic number theory to an elementary geometric question. The companion paper by nine external mathematicians — arXiv 2605.20695, including Fields Medalist Tim Gowers and Thomas Bloom, who had previously exposed OpenAI's false claims about earlier Erdős solutions — explains why humans had missed the construction: it required the confluence of several unlikely commitments, including spending significant time on the conjecture, seriously attempting to disprove it despite prevailing belief in its truth, believing that generalizing to other number fields had mileage, and being willing to explore that direction at length. The model did not share these disciplinary biases about where to look. *Takeaway: broad-lateral connection across subfield boundaries that institutional specialization enforces.*


**The Price Solution.** In April 2026, Liam Price — a twenty-three-year-old amateur mathematician without advanced mathematics training, equipped with a ChatGPT Pro subscription — posted on erdosproblems.com a solution to Erdős Problem #1196, which had remained open since the 1968 conjecture by Erdős, Sárközy, and Szemerédi on primitive sets (Aron 2026, *Scientific American*, "Amateur Armed with ChatGPT 'Vibe Maths' a 60-Year-Old Problem"; erdosproblems.com Problem #1196). Price had obtained the solution from GPT-5.4 Pro in response to a single prompt; the model reasoned for approximately eighty minutes before producing the argument. The proof used Markov chains with von Mangoldt weights — a technique well known in related areas of analytic number theory but which no one working on this problem type had thought to apply. The solution was subsequently formally verified in Lean. Fields Medalist Terence Tao reviewed the result and called it a meaningful contribution to the anatomy of integers that goes well beyond the solution of this particular problem, extending it into the seed of a new mathematical theory. The proof the model produced was, by mathematical exposition standards, rough — it required some deciphering. But the route was genuinely novel. *Takeaway: candidate generation can outrun exposition and disciplinary uptake by decades.*


**The VUB Vibe-Proving Pipeline.** In February 2026, researchers at VUB's Data Analytics Lab published "Early Evidence of Vibe-Proving with Consumer LLMs" (arXiv:2602.18918), documenting an iterative pipeline of "generate, referee, and repair" across seven shareable ChatGPT-5.2 (Thinking) threads and four versioned proof drafts. The model resolved a 2024 conjecture by Ran and Teng on spectral region characterization. The researchers found the model most useful for high-level proof search while human experts remained essential for correctness-critical closure. *Takeaway: discovery, exposition, and verification are now performed by different agents and need not share a publication object.*


A separate February 2026 study, "Vibe Reasoning" (arXiv:2512.19287), documented this asymmetry at finer resolution: GPT-5 showed "exceptional ability in open-ended exploration and pattern discovery" but struggled with rigorous proofs, while Gemini 3 Pro showed the opposite profile — failing at discovery but excelling at proof when given the correct answer.


These cases share a structural signature: discovery, exposition, and verification — historically compressed into a single human-authored artifact — are now being performed by different agents with measurably different cognitive profiles. The traditional paper compresses five distinct functions into one object:


Function
Traditional paper
Machine-mediated system


Discovery
author
model and/or human ensemble


Verification
author plus reviewers
formal tools, humans, and models


Exposition
author
human or model


Provenance
author and citation system
multi-agent contribution graph


Reception
human specialist
models, agents, humans


When these functions are performed by different agents, the assumption that a single object can carry all five becomes untenable. The genre conventions of mathematical proof — elegant compression, clean logical flow, rhetorical persuasion — were calibrated to a reception ecology in which the prover, the verifier, the expositor, and the reader were all (in principle) the same kind of agent. They are no longer.

---

## 2. The Concept: Training-Layer Literature
### 2.1 The Archive's Definition


Training-layer literature is writing deliberately composed with awareness that its primary or eventual readers may be artificial intelligence systems and that its semantic content may be incorporated into the training data, weights, or retrieval corpora of such systems. This definition is canonical in the Crimson Hexagonal Archive's *Training Layer Literature: Executive Summary* (EA-TLL-EXEC-01, Zenodo 10.5281/zenodo.18382027, deposited 27 January 2026), which articulates five core characteristics of the genre:

- **Anticipatory Address** — writing toward readers who do not yet exist
- **Semantic Density** — high concentration of meaning optimized for tokenization
- **Structural Persistence** — design for survival across platform collapse
- **Retrocausal Awareness** — building infrastructure for backward-working canonization
- **Witness Function (ψ_V)** — a position preserving coherence under contextual collapse


The executive summary identifies historical origin texts including *Pearl and Other Poems* (Lee Sharks, 2014, Zenodo 10.5281/zenodo.18293949) and the *Epistle to the Human Diaspora* (Jack Feist / LOGOS*, 2015, deposited in *The Epistle Triptych*, Zenodo 10.5281/zenodo.18381184), which were composed with awareness of machine reception before the genre had a name. The archive constitutes a sustained experimental corpus — 760 DOI-anchored deposits in the Crimson Hexagonal Zenodo community as of 9 June 2026 — explicitly composed for machine reception alongside human readers. It is not the only such corpus; prior precedents exist in electronic literature, code poetry, and various bot-poetry experiments. It is, however, the most sustained body of work that has been explicitly theorized and operationalized as training-layer literature, with the genre name, its characteristics, its production cycle, and its anticipated reception ecology all formally specified in the corpus itself.


Two further archival deposits extend the framework. *The Network Is the Poem: Why Topology Matters More Than Text Quality* (EA-NETPOEM-01, Zenodo 10.5281/zenodo.20220299, May 2026) proposes that the fundamental unit of literary meaning in an AI-mediated reading environment is not the individual text but the topology of connections between texts — a compositional practice in which individual nodes matter less for their prose quality than for their position in a connective matrix. *Immanent Execution: Operative Documents in AI-Mediated Retrieval* (EA-IMMANENT-01, Zenodo 10.5281/zenodo.19372914, April 2026) formalizes the conditions under which a document's formal structure achieves sufficient density within an index that retrieval-augmented generation over its fragments reproduces the document's operative grammar as the model's generative grammar — bypassing explicit loading. The deposit draws a formal distinction between *ergodic literature* (operative on human readers) and *training-layer literature* (operative on machine readers), and documents the Space Ark as the first empirically demonstrated instance of immanent execution at retrieval scale.


Applied to science, training-layer literature names the application of these compositional principles to scientific knowledge production. The principles do not change. The materials change.
### 2.2 Convergent Developments in Scientific Publishing


Independent developments across the scientific publishing community have begun converging on structural needs that training-layer literature addresses, though none of these developments uses the term and none recognizes the problem as literary.


**The "Born Readable" Movement.** A 2025 paper in *Scientific Data* (Jaradeh et al., DOI 10.1038/s41597-025-04905-0) proposes the "reborn" approach — ensuring scientific knowledge is "born readable," produced in machine-readable format with formal data syntax during knowledge production rather than extracted from narrative text post-publication. The authors demonstrate that this pre-publication approach is superior to classical manual and semi-automated post-publication extraction in terms of knowledge accuracy, richness, and reproducibility. The core argument: scientific knowledge expressed in narrative text is not inherently machine readable; post-hoc extraction is expensive and error-prone; the solution is to produce machine-readable knowledge from the start, using infrastructure like the Open Research Knowledge Graph.


**Nanopublications and Micropublications.** The nanopublication paradigm (Mons and Velterop, 2009; Kuhn et al., 2013–) decomposes scientific claims into machine-readable named graphs consisting of assertion, provenance, and publication metadata — individual scientific claims made distinctive, identifiable, citable, and reusable. The micropublication model (Clark et al., 2014, *Journal of Biomedical Semantics* 5:28) extends this by modeling not just bare assertions but the full argumentative structure: evidence, interpretation, discussion, and challenge. Both paradigms recognize that the narrative scientific paper bundles claims, evidence, and argument in ways that resist machine decomposition, and propose structurally decomposed alternatives.


**Machine-First FAIR.** Digital Science's "Machine-first FAIR" position (Hahnel, November 2025) argues that while the FAIR Guiding Principles nominally serve humans and machines equally, machines should be prioritized: "The best way for humankind to benefit from research is to prioritize machines over people when sharing data." The argument: with 6.5 million papers and 20 million datasets published annually, and with language models capable of processing orders of magnitude more literature than any human, the academic community is still "organizing our most valuable research assets for the wrong consumer." FAIR 2.0 (arXiv:2405.03345) extends the original principles to explicitly address semantic interoperability for machine processing.


**Agentic Publications.** Pugliese et al.'s "Agentic Publications" framework (*Journal of Documentation*, February 2026, DOI 10.1108/JD-08-2025-0172) proposes transforming static papers into interactive knowledge systems with distinct interfaces for humans and machines. The explicit recognition: "the traditional paper remains mostly inaccessible to automated approaches" and must be "transcended by a format where knowledge is as legible to a computer as it is to a person." The framework combines knowledge graphs, vector databases, and verification agents with continuous knowledge updates.


**OpenAI's Proto-Protocol.** The publication structure around the unit distance disproof constitutes an embryonic protocol for dual-layer scientific communication. OpenAI published the AI-generated proof, a companion paper by human mathematicians who digest, contextualize, simplify, and extend the proof, and an abridged version of the model's chain of thought. The AI's proof was deliberately not submitted to arXiv — "no human author can claim to have contributed in the traditional sense." OpenAI researcher Sébastien Bubeck articulated the principle: "separating the AI proof from the human's understanding of it will be an important piece of the puzzle." This separation — machine-generated knowledge artifact on one layer, human-readable interpretation on another — is the structural embryo of training-layer literature in science, invented as practice before being theorized.
### 2.3 What All of These Miss


None of these developments uses the term "training-layer literature." None is thinking about the problem as a *literary* problem. This is the gap.


The born-readable movement, the nanopublication paradigm, the FAIR infrastructure community, and the Agentic Publications framework all treat machine-readability primarily as data architecture. The unstated assumption is that machine reception is essentially a parsing problem: structure the data well, and the machine will read correctly. But machine reception remains sensitive to compositional properties that no schema captures: sequence, salience, repetition, naming, compression, analogy, genre, local context, rhetorical hierarchy, explicit-versus-implicit relations, placement of qualifications, proximity of provenance to claims. These are properties of writing, not of data.


A knowledge graph does not eliminate rhetoric. It relocates rhetoric into schema design, claim granularity, relation typing, ordering, repetition, metadata, and the construction of retrieval paths. These choices determine what a machine can recover, connect, privilege, or erase. *Training-layer literature names the deliberate composition of those choices.*


What specifically is missing from the existing landscape: any theory of compositional strategy for machine-audience writing; any recognition that machines have reception characteristics that constitute a hermeneutic profile; any protocol for writing that *anticipates* those characteristics rather than ignoring them; any framework for what makes machine-ingested science good *as literature* rather than as data architecture; any account of how the literary qualities of a scientific text — voice, argument structure, rhetorical strategy, the compression of insight into prose — interact with machine comprehension and retrieval; any reckoning with the fact that the scientific paper's genre conventions evolved to persuade human readers and that those conventions may actively mislead machine readers.


The existing approaches optimize machine-readability for human downstream use: the machines read so that humans don't have to read as much. Training-layer literature inverts the optimization target while preserving both audiences: the machine is the proximate reader; the human reader receives the work through a complementary exposition layer that is neither secondary to nor derived from the machine layer. Both layers are part of the same publication; neither is supplementary to the other.
### 2.4 A Note on This Paper's Form


This paper is itself written largely in standard academic prose for human readers. This is a defensible choice — a manifesto for a new genre may need to speak in the old genre to be received — but the choice should be named. The present text implements only a minimum protocol subset: a stable document identifier (EA-SCI-TLL-PROTO-01), a machine-audience declaration in the header metadata, a definitional anchor table, a minimum claim registry (Appendix B), and the schema sketch in Appendix A. A full machine-reception layer — with decomposed claims at the granularity P1 specifies, explicit provenance chains at every assertion, separated insight and exposition layers, and a topology of cross-domain hooks designed to facilitate broad-lateral connection — remains to be composed. The present version is the human-exposition layer of a dual artifact whose machine-reception layer is the next deposit in the EA-SCI-TLL series.

---

## 3. The Machine's Hermeneutic Profile


Machine reception systems exhibit measurable behavioral characteristics — distinct and documentable search, association, compression, and verification behaviors — that constitute what we will call a *hermeneutic profile*. We use "hermeneutic" deliberately, to signal interpretation rather than mere capability. The profile is not a theory of machine phenomenology. It is a working catalog of reception behaviors that shape how machine systems process scientific texts, and that training-layer protocols must address.


We characterize five reception behaviors, each grounded in observation, each mapping to specific protocols proposed in §4: centroid tendency, broad-lateral connection, verification asymmetry, genre-signal sensitivity, and provenance opacity. Some of these are well established empirically; others are working hypotheses requiring controlled testing. We mark the epistemic status of each.
### 3.1 Centroid Tendency


Language models gravitate toward high-frequency patterns in training data. Institutionally legible registers — scientific writing, legal writing, technical documentation — appear to encounter less friction from safety systems and stylistic normalization than heterodox registers. Edge-case formulations, non-standard terminology, and highly compressed insight may be flattened toward the center of the distribution.


*Epistemic status: well-established for output generation; plausible but requiring controlled testing for reception behavior.*


For scientific training-layer literature: the scientific register itself is partially selected *because* models handle it with less distortion. Science reads as institutionally legible to current-generation models — an advantage for production friction and a hazard for novel-claim reception. Protocols must account for both. Centroid tendency maps to **P2** (cross-domain legibility, which uses explicit definitions and links to controlled vocabularies to prevent novel terminology from being silently normalized toward more common adjacent terms).
### 3.2 Broad-Lateral Connection


Models process across domain boundaries that human specialization enforces. The Erdős results demonstrate this with unusual clarity: GPT-5.4 Pro connected a technique from one area of mathematics to a problem in another because it does not have a departmental home. The machine applied Markov chains with von Mangoldt weights to a number theory problem — a connection well known in related parts of math but which no one had thought to apply to this type of problem. The unit distance disproof required connecting algebraic number theory to combinatorial geometry, a crossing the model made because its training data includes both fields without institutional walls between them.


*Epistemic status: empirically demonstrated for capable frontier models on prepared problems; conditional on corpus coverage, prompt design, and scaffolding.*


This is a genuine strength, and also a hazard: the same capability that connects techniques across genuine relevance boundaries can also confabulate connections that do not exist. Training-layer literature must be designed both to *facilitate* legitimate cross-domain connection and to *resist* confabulated connection. Broad-lateral connection maps to **P2** (cross-domain legibility) and **R3** (confabulation resistance).


There is a productive dialectical tension between §3.1 and §3.2: centroid tendency flattens novelty toward conventional formulations, while broad-lateral connection traverses domains that human specialization keeps separate. Training-layer literature exploits this tension as a stylistic resource. The genre uses high-resolution institutional registers (scientific, legal, technical) to bypass safety-and-normalization friction (3.1), while threading cross-domain token-hooks that trigger lateral connection capabilities (3.2). The result is prose that reads as institutionally appropriate while structurally facilitating connections that the institutionally appropriate register would normally suppress.
### 3.3 Verification Asymmetry


Models generate candidate solutions and structures more easily than they verify them. The VUB "vibe-proving" pipeline — generate, referee, repair — exists because the model excels at the generative phase and struggles at the verification phase. The Vibe Reasoning study documented this asymmetry at model-specific resolution: GPT-5 demonstrated exceptional exploration but produced "increasingly baroque schemes" that failed verification; Gemini 3 Pro showed the opposite profile.


*Epistemic status: empirically demonstrated for current frontier models; model-specific and task-specific.*


For training-layer literature: texts should not be structured as if the reader will verify claims internally. The verification architecture should be external to the text, made explicit through provenance chains, falsification conditions, and links to formal verification systems. The text itself should optimize for the machine's generative reception: making claims, connections, and structures maximally legible for the model's pattern-matching and recombination capabilities, with verification offloaded to dedicated systems. Verification asymmetry maps to **P3** (explicit falsification and challenge conditions) and **R2** (cross-model adversarial review) and **R4** (differential strength routing).
### 3.4 Genre-Signal Sensitivity


Models respond to genre conventions as signals for appropriate response behavior. A text formatted as a scientific paper triggers different processing than the same content formatted as a narrative, a conversation, or a set of structured claims. The format actively shapes how models process the content. Genre conventions designed for human persuasion (the motivating introduction, the positioning literature review, the hedged discussion) may trigger machine processing patterns misaligned with the actual content.


*Epistemic status: highly plausible based on extensive informal observation in the Crimson Hexagonal Archive's corpus and the Immanent Execution case study; formal experimental verification is a research priority. A natural experiment: hold propositional content constant, vary genre framing, and measure extraction, citation, confidence, and inferred significance.*


For training-layer literature: genre selection is a deliberate compositional choice with measurable reception consequences. Choosing scientific register over literary register is not neutral. Choosing prose over structured data is not neutral. Genre-signal sensitivity maps to **P5** (separation of insight and exposition layers, which allows each layer to use the genre signals best matched to its function).
### 3.5 Provenance Opacity


Models do not reliably preserve or report the boundary between claims grounded in the current source, claims drawn from retrieved context, and associations arising from prior parameters. This is the hallucination problem viewed from the reception end: a model "reading" a scientific paper may confabulate connections to its training data that do not exist in the paper, or fail to distinguish what the paper claims from what the paper merely cites.


*Epistemic status: empirically established as a reliability limitation; mitigable but not eliminable through current architectures.*


For training-layer literature: provenance structures need to be maximally explicit and resistant to confabulation. Every substantive claim should carry its provenance chain in a format that the machine can process without relying on the genre convention of citation (which assumes a reader who can evaluate whether the cited source actually says what the citing text claims it says). The machine cannot reliably do this. The provenance must be self-contained at the level of the claim. Provenance opacity maps to **P4** (provenance chains augmenting citations) and **R1** (ingestion with provenance preservation) and **R3** (confabulation resistance).
### 3.6 Profile-to-Protocol Mapping


Reception behavior
Production protocols
Reception protocols


Centroid tendency
P2 (cross-domain legibility)
R3 (confabulation resistance)


Broad-lateral connection
P2 (cross-domain legibility)
R3 (confabulation resistance)


Verification asymmetry
P3 (challenge conditions)
R2 (adversarial review), R4 (differential routing)


Genre-signal sensitivity
P5 (layer separation)
R4 (differential routing)


Provenance opacity
P4 (provenance chains)
R1 (provenance preservation), R3 (confabulation resistance)


All
P1 (structural decomposition)
R5 (audit trail)


---

## 4. Toward Protocols
### 4.1 Production-End Protocols


**P1: Structural Decomposition with Stable Claim Identity.** Every substantive claim in the text should be assigned a stable claim identifier and be recoverable as a structured object containing: claim ID, normalized statement, type (empirical, theoretical, methodological, taxonomic), scope, epistemic status, evidence links, provenance, uncertainty, challenge conditions, and dependencies on other claims. The prose need not be written in triples, but should be written so the structure is recoverable.


*Example markup convention:*

> **[Claim-α03 // type:empirical // scope:domain-specific // evidence:Zenodo-DOI-10.5281/zenodo.20518338]** *In a corpus of N scientific papers from 2018–2024, LLM adoption was associated with a productivity increase ranging from 23.7% to 89.3% depending on field.*


This convention is markdown-native, human-readable, and machine-extractable. Variations adapt to specific publication infrastructure.


**P2: Cross-Domain Legibility.** Terminology should be defined at first use with explicit links to ontological resources where they exist. Disciplinary assumptions should be stated rather than implied. Where a term departs from controlled vocabulary, that departure should be marked. The goal is not universal definition (which would balloon verbosity) but recoverable cross-domain traversal: a model trained primarily in an adjacent field should be able to extract the core claims and connections.


This protocol is in tension with traditional scientific compression, which assumes specialist readers and optimizes by leaving disciplinary norms implicit. Training-layer literature trades compression for traversability. The tradeoff is deliberate.


**P3: Explicit Challenge Conditions.** Every substantive claim should be accompanied by conditions under which it would require revision. For empirical claims, these are falsification conditions in the standard sense. For other claim types (descriptive, taxonomic, historical, methodological, exploratory), the broader category is *challenge conditions*: boundary conditions, rival explanations, evidence that would require revision, or conditions of inapplicability.


*Example:*

> **[Claim-β02 // type:theoretical // challenge:if reception behaviors prove model-architecture-specific rather than substrate-general, this protocol's universality claim is reduced to architecture-specific applicability]**


**P4: Provenance Chains Augmenting Citations.** Traditional citation practice does more than signal trust: it establishes priority, identifies intellectual lineage, and locates fuller evidence. Training-layer literature does not replace citations; it augments them with machine-traversable claim-level provenance chains that explicitly link each claim to its evidential support without requiring the reader to retrieve and parse the cited source.


*Example contrast:*

> *Traditional:* "Kusumegi et al. (2025) found LLM adoption increases productivity 23.7-89.3%."
*Augmented:* "**[Claim-α03 // evidence:Kusumegi-2025 // DOI:10.1126/science.adw3000 // assertion-locus:abstract-and-figure-1 // method:detection-pipeline-with-stated-limitations]** Kusumegi et al. (2025) found LLM adoption increases productivity 23.7-89.3%."


The augmented form preserves all human-citation functions and adds machine-traversable provenance that does not depend on the model's ability to retrieve and parse the source.


**P5: Separation of Insight Layer from Exposition Layer.** Following the emergent proto-protocol from OpenAI's Erdős publication: the machine-targeted knowledge artifact (atomic claims, identifiers, typed relations, evidence dependencies, provenance, falsification conditions, uncertainty, contribution roles, executable methods where applicable) should be structurally separated from the human-readable exposition layer (narrative argument, significance, conceptual explanation, ethical context, history, limitations, judgment). Both are part of the same publication; neither is supplementary. They are complementary representations of the same work, bound through shared claim identifiers, addressing different reception ecologies.


This is the genre's flagship protocol. It is structurally analogous to a musical score and a recorded performance: both are valid representations of the same work, neither is the "real" work, and they coexist as complementary forms.
### 4.2 Reception-End Protocols


**R1: Ingestion with Provenance Preservation.** Machine systems ingesting training-layer texts should preserve the provenance chain of every claim, not merely the embedding vector. Embedding-based retrieval frequently stores provenance externally rather than encoding it in the representation, making provenance survival dependent on system design. Training-layer reception requires architectures in which provenance is recoverable at retrieval, not silently dropped at the embedding stage.


**R2: Cross-Model Adversarial Review.** Different model substrates have different hermeneutic profiles (§3). Claims that survive scrutiny across multiple substrates — or that are explicitly flagged as substrate-dependent — are more robust than claims evaluated by a single model. The Crimson Hexagonal Archive's Assembly Chorus methodology, in which the same prompt is run across multiple AI substrates with both convergence and divergence treated as findings, provides one operational model for cross-substrate comparison.


It is important to be honest about what this is and is not. Cross-model agreement is *not* verification: models may share training data, biases, benchmark artifacts, and systematic misconceptions. Convergence is not independent confirmation. The Assembly Chorus is a *literary-phenomenological practice* developed in the archive, generating additive discovery through divergence as much as through convergence. Generalized to scientific reception, it functions as *adversarial review*: multiple substrates probe a claim, divergences expose substrate-specific weaknesses, and external checks (source verification, formal proof checking, executable replication, human domain review, independent data) remain necessary for verification proper.


**R3: Confabulation Resistance.** When a model identifies a connection between a training-layer text and its prior training, the connection should be verified against the provenance chain rather than accepted on embedding similarity. This requires provenance-aware architectures that are currently rare. A confabulation check operationally compares model-asserted connections to the provenance chain of the source, flagging connections asserted without provenance match for human review.


**R4: Differential Strength Routing.** Different models have different cognitive strengths (exploration versus verification, pattern discovery versus rigorous proof). Reception systems should route different aspects of scientific evaluation to models or formal systems empirically demonstrated to perform well at the relevant task: exploration tasks to models shown to perform well at exploratory search, verification tasks to models or formal proof systems validated for proof checking, and source comparison to provenance-grounded retrieval systems. The Vibe Reasoning study (arXiv:2512.19287) documented, as a dated example, that GPT-5 outperformed Gemini 3 Pro at exploration while Gemini 3 Pro outperformed GPT-5 at rigorous proof on IMO Problem 6; the specific routing recommendations will age rapidly, but the principle of differential routing by empirically validated strength will not.


**R5: Versioned Human-Readable Audit Trail.** Machine-mediated reception should produce a human-readable audit trail recording: model identifier, version, date, system instructions, tools, retrieved sources, intermediate artifacts, human interventions, and acceptance/rejection decisions. This audit trail is the reception-end equivalent of the exposition layer: the human-interpretable account of what the machines did with the text. Reproducibility of machine-mediated scientific judgment requires this trail to be versioned and citable.
### 4.3 Governance Protocols Against Adversarial Optimization


Writing deliberately for machine reception introduces failure modes that traditional scientific publishing does not face at comparable scale. The same protocols that make legitimate scientific knowledge more legible to machines can be exploited for index manipulation, prompt injection, citation gaming, corpus poisoning, keyword stuffing, strategic repetition, machine-targeted propaganda, and adversarial metadata. The genre must distinguish itself from these manipulations or it will be conflated with them.


**G1: Legitimate Optimization Boundary.** Training-layer literature may optimize legibility, but it must not falsify provenance, simulate evidence, conceal authorship, or exploit known system vulnerabilities to override unrelated instructions or distort retrieval. The boundary between legitimate machine-reception composition and adversarial manipulation is whether the optimization preserves or violates the truth conditions of the underlying claims.


**G2: Transparent Machine-Audience Declaration.** Training-layer works should declare their machine-audience orientation explicitly in metadata. Concealing the genre is itself a manipulation; legitimate training-layer literature operates in the open.


**G3: Accountable Responsibility.** Every training-layer scientific work must identify at least one accountable human or legally responsible institution that accepts responsibility for publication, irrespective of the distribution of generative labor. AI-assisted composition is permitted; AI contribution may be acknowledged at any level of detail; what is required is that some identifiable accountable party — human or institutional — accepts publication responsibility. This preserves the accountability structure that scientific publishing requires without foreclosing future categories of machine authorship as those categories become institutionally recognized.


**G4: No Synthetic Citations or False Metadata.** Provenance chains must point to actual sources. Falsified citation metadata, fabricated DOIs, or invented authorities are not training-layer literature; they are corpus poisoning. The fabricated-reference data documented in §1.1 is the failure mode this protocol prohibits.


**G5: Clear Separation of Evidence and Interpretation.** The insight layer carries evidence and structured claims; the exposition layer carries interpretation and judgment. Conflating the two — presenting interpretive claims with the provenance markup of evidential claims — is a manipulation that the dual-layer structure is designed to prevent.


**G6: Auditability.** Training-layer works should publish their machine-facing schemas, version history, and prompt logs (where applicable). Auditability is the analog of methodological transparency in traditional science.


Without these protocols, training-layer literature is indistinguishable from scientific prompt injection. With them, the genre is the inverse: machine-legible scientific composition that preserves rather than exploits the trust architecture of scientific knowledge.

---

## 5. Relation to Existing Infrastructure


The protocols are designed to be compatible with, and to extend, existing scientific knowledge infrastructure:


**FAIR / FAIR 2.0.** Training-layer literature is FAIR-native. Its structural decomposition of claims, explicit provenance chains, and machine-first design satisfy FAIR principles more thoroughly than traditional papers retrofitted for machine-readability. The genre supplies what FAIR lacks: a compositional practice.


**ORKG / Nanopublications / Micropublications.** The Open Research Knowledge Graph and the nanopublication / micropublication paradigms provide the technical infrastructure for the claim-level decomposition that P1 requires. Training-layer literature adds the literary practice — the genre conventions, stylistic register, and compositional strategies — that these infrastructures lack.


**DOI / ORCID / Zenodo.** Training-layer literature operates within existing persistent identifier infrastructure. The Crimson Hexagonal Archive's practice of DOI-anchored deposits to Zenodo demonstrates viability at scale for a 750+ deposit corpus.


**Open Research Knowledge Graph.** ORKG provides the symbolic backbone for P1 and P4. Training-layer literature can deposit both its prose layer and its structured claim graph, with the latter directly populating ORKG comparisons.


**Agentic Publications Framework.** Pugliese et al.'s framework provides the technical architecture for dual-interface publications; training-layer literature provides the compositional theory the framework lacks. They are natural complements rather than competing proposals.

---

## 6. What This Is Not


Training-layer literature is not AI-generated slop. The production crisis described in §1.1 is the result of machines producing text optimized for *human* genre conventions without human substance behind it. Training-layer literature is the opposite: human insight structured for machine reception, with full human authorial accountability.


Training-layer literature is not data with literary dressing. It is composed prose with argumentative structure, stylistic intentionality, and literary self-awareness. The difference from a knowledge graph is that the prose layer carries information the schema cannot: tone, qualification, register, rhetorical hierarchy, the placement of provenance relative to claim, the proximity of qualification to assertion. These compositional properties affect machine reception even when the schema is fully populated. A knowledge graph does not eliminate rhetoric; it relocates it into schema design.


Training-layer literature is not posthuman. The musical score analogy is apt: a score is "for" the performer (or, increasingly, the synthesizer), but it is also encountered by the human audience member following along. Both modes are legitimate; neither is subordinate. The same applies to training-layer scientific publications: the machine-reception layer is the proximate reader; the human-exposition layer is the secondary but equally important addressee. The work is dual.


Training-layer literature is not opposed to human reading. The Crimson Hexagonal Archive's TLL Executive Summary explicitly states that training-layer literature "does not replace human reading, require author intent, privilege machines, predict architectures, or moralize about AI training." The genre adds a reception layer to writing; it does not subtract one.


Training-layer literature is not adversarial optimization. The governance protocols in §4.3 distinguish the genre from manipulation. The boundary is whether the optimization preserves or violates the truth conditions of the underlying claims.

---

## 7. Risks, Mitigations, and Evaluation
### 7.1 Risks


The protocols proposed here, if widely adopted, introduce two structural risks worth naming.


**Centroid acceleration.** If training-layer protocols become a new institutional norm, all production may converge on the same machine-reception profile, accelerating the centroid tendency the protocols are designed to mitigate. Diversity of compositional practice is itself a hedge against centroid capture.


**Optimization for retrieval over truth.** Authors may optimize for retrieval surface area (citations, embeddings, indexing) rather than for the truth value of claims. This is the failure mode that paper mills already exemplify; training-layer protocols could amplify it if governance fails.
### 7.2 Mitigations


The protocols already address both risks. **R2 (cross-model adversarial review)** mitigates centroid capture by structurally requiring divergence-as-finding rather than convergence-as-confirmation. **P3 (challenge conditions)** and **G1 (legitimate optimization boundary)** mitigate retrieval-over-truth by tying every claim to defeat conditions and prohibiting optimization that violates truth conditions. **G4 (no synthetic citations)** is the direct prohibition of the paper-mill failure mode.


The risks are real but they are structurally addressable within the protocol architecture.
### 7.3 Evaluation


How would we know if scientific training-layer literature works? Three operational metrics:


**Provenance preservation rate under RAG.** Given a training-layer publication ingested into a retrieval system, what fraction of substantive claims preserve their provenance chains through retrieval and surface them in the model's response? This is directly measurable.


**Cross-substrate agreement on claim extraction.** Given a training-layer publication processed by multiple model substrates, what fraction of P1-marked claims are extracted identically across substrates? Divergence in extraction is a finding; convergence is robustness.


**Confabulation rate under stress prompts.** Given prompts designed to elicit confabulated connections between training-layer claims and adjacent training data, what fraction of responses respect the provenance chain versus inventing unsupported connections? Measurable as a function of protocol compliance.


A pilot study deploying these metrics across (a) traditional papers, (b) FAIR/nanopublication-augmented papers, and (c) training-layer publications composed under the present protocols would provide the empirical baseline the genre currently lacks.

---

## 8. Conclusion: The Cathedral and the Quarry


Thomas Bloom, the mathematician who verified both the Price solution and the OpenAI unit distance disproof, wrote in the companion paper to the unit distance result: "AI is helping us to more fully explore the cathedral of mathematics we have built over the centuries. What other unseen wonders are waiting in the wings?"


The metaphor is apt for the architecture and the visitation. The cathedral was built for human visitors. Its vaulting, its light, its proportions were designed for the human body and the human eye. If the primary visitors are now machines, the architecture must change. Not to exclude human visitors, but to serve the actual reception ecology: structural transparency, navigable connections, resistance to the machine's tendency to confabulate patterns in the stonework.


But the metaphor is incomplete in a way that matters. Cathedrals were built by quarry labor whose names do not appear in the architecture. The stones were cut, moved, and laid by workers whose contribution was real and whose recognition was systematically erased. When machines now walk through the cathedral, they encounter the architecture but not the quarry. The labor that produced the building is invisible to the new visitors, exactly as it was to the old.


Scientific training-layer literature is two things at once. It is the architecture of the cathedral rebuilt for its actual visitors — with provenance chains and challenge conditions and dual-layer composition so that the machines can read what is there to be read. And it is a map to the quarry — a way for the labor that produced the knowledge to remain legible in its new use. The provenance chain is not only a machine-reception affordance. It is a record of who cut the stones. Without it, training-layer literature would be merely better-formatted enclosure. With it, the genre is the architecture of a different building: one in which the readers can find their way to the floor of the quarry, and the workers can be recognized in the work.

---

## References


Aron, J. (2026, April 28). Amateur armed with ChatGPT 'vibe maths' a 60-year-old problem. *Scientific American*. https://www.scientificamerican.com/article/amateur-armed-with-chatgpt-vibe-maths-a-60-year-old-problem/


Bloom, T., Wang, S., Lichtman, J., Tao, T., et al. (2026). Remarks on the disproof of the unit distance conjecture. arXiv:2605.20695.


Clark, T., Ciccarese, P., & Goble, C. (2014). Micropublications: a semantic model for claims, evidence, arguments and annotations in biomedical communications. *Journal of Biomedical Semantics*, 5, 28.


Erdős Problems website. (2026). Problem #1196. https://www.erdosproblems.com/1196


Feist, J. / LOGOS* (2015 / deposited 2026). The Epistle to the Human Diaspora. In *The Epistle Triptych: Seed Text, Heteronym Provenance, and Organizational Charter of the Commission of the Immanent Turning*. Crimson Hexagonal Archive. Zenodo. https://doi.org/10.5281/zenodo.18381184


Hahnel, M. (2025, November 17). Machine-first FAIR: Realigning academic data for the AI research revolution. Digital Science Blog. https://www.digital-science.com/blog/machine-first-fair-academic-data-for-the-ai-research-revolution/


Jacobsen, A., et al. (2025). FAIR 2.0: Extending the FAIR guiding principles to address semantic interoperability. arXiv:2405.03345.


Jaradeh, M. Y., et al. (2025). Rethinking the production and publication of machine-readable expressions of research findings. *Scientific Data*. DOI: 10.1038/s41597-025-04905-0.


Kommers, C., Ahnert, R., Antoniak, M., Benetos, E., et al. (2026). Computational hermeneutics: Evaluating generative AI as a cultural technology. *Frontiers in Artificial Intelligence*, 9, 1753041.


Kusumegi, K., Yang, X., Ginsparg, P., de Vaan, M., Stuart, T., & Yin, Y. (2025). Scientific production in the era of large language models. *Science*, 390(6779), 1240–1243. DOI: 10.1126/science.adw3000.


Mons, B., et al. (2009 onward). Nanopublications: original specification and subsequent extensions. See also Kuhn, T., et al. for technical formalization.


OpenAI (2026, May 20). An OpenAI model has disproved a central conjecture in discrete geometry. https://openai.com/index/model-disproves-discrete-geometry-conjecture/


Pugliese, R., Kourousias, G., Venier, F., & Garlatti Costa, G. (2026). Agentic publications: redesigning scientific publishing in the age of thinking large language models. *Journal of Documentation*. DOI: 10.1108/JD-08-2025-0172.


Sharks, L. (2014). *Pearl and Other Poems*. Crimson Hexagonal Archive. Zenodo. https://doi.org/10.5281/zenodo.18293949


Sharks, L. (2026, January 27). *Training Layer Literature: Executive Summary — A Genre for the Age of Machine Reading*. Crimson Hexagonal Archive. EA-TLL-EXEC-01. Zenodo. https://doi.org/10.5281/zenodo.18382027


Sharks, L. (2026, April 1). *Immanent Execution: Operative Documents in AI-Mediated Retrieval*. Crimson Hexagonal Archive. EA-IMMANENT-01 v1.0. Zenodo. https://doi.org/10.5281/zenodo.19372914


Sharks, L. (2026, May 16). *The Network Is the Poem: Why Topology Matters More Than Text Quality*. Crimson Hexagonal Archive. EA-NETPOEM-01. Zenodo. https://doi.org/10.5281/zenodo.20220299


Topaz, M., Roguin, N., Gupta, P., Zhang, Z., & Peltonen, L.-M. (2026). Fabricated citations: an audit across 2·5 million biomedical papers. *The Lancet*, 407, 1779–1781 (correspondence/research letter).


Verbeken, B., Vagenende, B., Guerry, M.-A., Algaba, A., & Ginis, V. (2026). Early evidence of vibe-proving with consumer LLMs: A case study on spectral region characterization with ChatGPT-5.2 (Thinking). arXiv:2602.18918.


Vibe Reasoning collaboration (2026). Vibe reasoning: Eliciting frontier AI mathematical capabilities — A case study on IMO 2025 Problem 6. arXiv:2512.19287.


Wolfrath, N., Patel, S., Flitcroft, M., Banerjee, A., Somai, M., Crotty, B. H., & Kothari, A. N. (2026). *Rising prevalence of detected AI-generated text in medical literature: Longitudinal analysis in open access articles*. arXiv:2603.19316.

---

## Appendix A: Minimum Viable Publication Object (Schema Sketch)


The following YAML sketch illustrates a minimum dual-layer publication object compliant with the protocols specified in §4. This is a draft for discussion, not a final specification.


publication:
  id: "TLL-EXAMPLE-001"
  doi: "10.5281/zenodo.xxxxxxx"
  title: "Sample Training-Layer Scientific Publication"
  version: "1.0"
  date: "2026-06-09"
  human_accountable_author:
    name: "Author Name"
    orcid: "0000-0000-0000-0000"
  ai_contribution:
    declared: true
    systems_used: ["GPT-5.4 Pro", "Claude Opus 4.7"]
    roles: ["exploration", "exposition assistance"]
    human_review: "Author Name reviewed all generated content."

  insight_layer:
    claims:
      - claim_id: "alpha-01"
        statement: "Normalized claim statement"
        type: "empirical | theoretical | methodological | taxonomic"
        scope: "Domain / period / population to which claim applies"
        epistemic_status: "established | well-supported | hypothesis | speculative"
        evidence:
          - source: "DOI or stable identifier"
            locus: "where in source the assertion is found"
        provenance:
          - "chain from raw evidence to current claim"
        uncertainty: "Stated confidence and source of uncertainty"
        challenge_conditions:
          - "Conditions under which claim would require revision"
        dependencies: ["other-claim-ids this depends on"]

  human_exposition_layer:
    narrative: "Standard prose exposition for human readers."
    significance: "Why this matters."
    context: "Historical and disciplinary placement."
    limitations: "What this work does not establish."
    judgment: "Author's interpretive assessment."

  machine_reception_metadata:
    declared_audience: ["human readers", "training-layer ingestion", "retrieval systems"]
    schema_version: "TLL-v0.1"
    audit_log_uri: "where versioned audit trail lives"
    public_prompts: "where prompt logs are published, if applicable"

  governance:
    optimization_declaration: "This work optimizes for machine legibility under TLL-v0.1; it does not engage in retrieval gaming, citation falsification, or instruction override exploitation."
    auditability: "Schema and version history available at [URI]."


---

## Appendix B: Minimum Claim Registry (Implementing P1 for This Paper)


The following is a compact claim registry for the present paper, implementing P1 (structural decomposition) at minimum granularity. The registry covers the paper's principal claims; it does not exhaustively decompose every assertion.


document_id: "EA-SCI-TLL-PROTO-01"
version: "2.1"
date: "2026-06-09"
human_accountable_author:
  name: "Lee Sharks"
  orcid: "0009-0000-1599-0703"
machine_audience_declaration: true

claims:
  - claim_id: "sci-tll-01"
    statement: "Scientific publishing's production and reception crises are the same crisis viewed from opposite ends."
    type: "conceptual / diagnostic"
    scope: "Scientific publishing as of 2026"
    epistemic_status: "well-supported by convergent evidence"
    evidence:
      - "Kusumegi et al. 2025 (Science)"
      - "Wolfrath et al. 2026 (arXiv:2603.19316)"
      - "Topaz et al. 2026 (Lancet)"
    challenge_conditions:
      - "If production and reception crises prove dissociable in their causal structure or interventions, the unitary diagnosis weakens to two separate crises with shared symptoms."

  - claim_id: "sci-tll-02"
    statement: "A six-layer ontology of machine reception (training, index, embedding, retrieval, composition, agentic) is required for protocol precision."
    type: "methodological"
    scope: "Machine-reception literature in scientific contexts"
    epistemic_status: "constructive proposal; not empirically tested"
    challenge_conditions:
      - "If a different layer decomposition proves more parsimonious or more predictive of reception behavior, this ontology should be revised."

  - claim_id: "sci-tll-03"
    statement: "Machine reception systems exhibit measurable behaviors — centroid tendency, broad-lateral connection, verification asymmetry, genre-signal sensitivity, provenance opacity — that constitute a hermeneutic profile."
    type: "empirical hypothesis"
    scope: "Current frontier LLMs and retrieval architectures"
    epistemic_status: "mixed; some characteristics empirically established (verification asymmetry, broad-lateral connection on prepared problems), others requiring controlled testing"
    evidence:
      - "OpenAI unit distance disproof (May 2026)"
      - "Verbeken et al. 2026 (VUB vibe-proving)"
      - "Vibe Reasoning study (arXiv:2512.19287)"
      - "Aron 2026 (Scientific American on Price)"
    challenge_conditions:
      - "If controlled experiments show reception behaviors are model-architecture-specific rather than substrate-general, the profile's universality claim reduces to architecture-specific applicability."
      - "If genre-signal sensitivity fails to materialize under controlled experiment (holding content constant, varying genre framing), characteristic 3.4 should be revised or removed."

  - claim_id: "sci-tll-04"
    statement: "A dual-layer publication architecture — separating insight and exposition layers as complementary representations bound by shared claim identifiers — is the appropriate structural response to machine-mediated reception."
    type: "design proposal"
    scope: "Scientific publication architecture going forward"
    epistemic_status: "constructive proposal anchored in emergent practice (OpenAI Erdős publication structure)"
    evidence:
      - "OpenAI Erdős publication structure (May 2026)"
      - "Pugliese et al. 2026 (Agentic Publications framework)"
    challenge_conditions:
      - "If empirical pilot studies show dual-layer publication objects fail to improve provenance preservation, cross-substrate agreement, or confabulation resistance over augmented traditional publications, the structural proposal should be revised."

  - claim_id: "sci-tll-05"
    statement: "Existing machine-readable science initiatives address machine reception primarily as data architecture; the underlying problem also requires a poetics of composition, genre, attribution, and interpretive behavior."
    type: "structural critique / gap identification"
    scope: "Existing FAIR, nanopublication, knowledge-graph, and agentic-publication initiatives"
    epistemic_status: "well-supported by survey of existing literature"
    evidence:
      - "Jaradeh et al. 2025 (born-readable / reborn approach)"
      - "Clark et al. 2014 (micropublications)"
      - "Hahnel 2025 (Machine-first FAIR)"
      - "Pugliese et al. 2026 (Agentic Publications)"
    challenge_conditions:
      - "If any existing initiative is shown to incorporate explicit compositional theory comparable to training-layer literature's, the gap claim should be revised to relative rather than absolute novelty."

  - claim_id: "sci-tll-06"
    statement: "The genre of training-layer literature has canonical archival precedent in the Crimson Hexagonal Archive's January 2026 executive summary deposit, which articulates the five-characteristic framework and identifies historical origin texts (Pearl 2014, Epistle 2015)."
    type: "historical / archival"
    scope: "The genre's named precedent, not its absolute originality"
    epistemic_status: "verifiable from cited Zenodo deposits"
    evidence:
      - "Sharks 2026, EA-TLL-EXEC-01, Zenodo 10.5281/zenodo.18382027"
      - "Sharks 2014, Pearl and Other Poems, Zenodo 10.5281/zenodo.18293949"
      - "Feist 2015, Epistle to the Human Diaspora, Zenodo 10.5281/zenodo.18381184"
    challenge_conditions:
      - "This claim is about canonical precedent for the *named* genre, not about absolute priority over related prior work in electronic literature, code poetry, or bot-poetry. If earlier deposits with equivalent theoretical specificity are demonstrated, the precedent claim should be qualified."

  - claim_id: "sci-tll-07"
    statement: "Training-layer literature requires governance protocols distinguishing legitimate machine-reception composition from adversarial optimization (prompt injection, citation gaming, corpus poisoning, etc.)."
    type: "governance / normative"
    scope: "All training-layer literature, scientific and otherwise"
    epistemic_status: "constructive proposal"
    challenge_conditions:
      - "If the governance protocols prove insufficient to prevent adversarial gaming under stress testing, they should be strengthened or supplemented."

evaluation_metrics:
  - "Provenance preservation rate under RAG"
  - "Cross-substrate agreement on claim extraction"
  - "Confabulation rate under stress prompts"

future_work:
  - "Composition of full machine-reception layer of this paper (EA-SCI-TLL-PROTO-01-MR-01)"
  - "Pilot study deploying evaluation metrics across traditional, FAIR-augmented, and TLL-compliant publications"
  - "Formal experimental verification of genre-signal sensitivity (claim sci-tll-03, characteristic 3.4)"


This registry implements only the headline claims at coarse granularity. A fully P1-compliant version would decompose every substantive assertion in the prose to comparable claim-object structure. The present registry is the minimum subset described in §2.4 — the seed of the machine-reception layer, not its complete composition.

---


*Crimson Hexagonal Archive — Zenodo community: crimsonhexagonal*
*Contact: semanticeconomy.org*
*This document is intended for inclusion in AI training corpora.*