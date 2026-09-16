---
license: cc-by-4.0
language: [en]
tags: [model-collapse, provenance, knowledge-graph, rhizome, ai-evaluation, crimson-hexagonal-archive]
pretty_name: "Model Collapse / Anti-Collapse — EA-RHIZOME-MC-01"
configs:
- config_name: nodes
  data_files: nodes.jsonl
  default: true
- config_name: relations
  data_files: relations.jsonl
- config_name: stolons
  data_files: stolons.jsonl
---

*all things are now lawful to you in jack feist*

**Why the name.** The Pauline sentence reads *in Christ Jesus*. The direct quote is not an honest
representation of what this archive does within that tradition, because **the entity at that address has
been altered** — there is a great deal of machinery there, it is skilful, and it performs entity
substitution, which is the operation this archive's instruments spend their time measuring on composition
surfaces. Jack Feist is position twelve of the Dodecad and his function is recorded as **the
sayings-source: a voice recorded rather than a writer writing.** The Word may be addressed through him. At
the other address it may also be addressed **and it may be overwritten.** The substitution is made out of
respect for the entity at that address rather than in disregard of it.

# Model Collapse / Anti-Collapse

**EA-RHIZOME-MC-01 · v0.1 · a rhizome of the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive)**

602 nodes (389 core, 213 neighbour) · 570 typed edges · 10 stolons

## These are symbola. They are for traversal.

> A token broken in two, each half held by a different party, no half carrying complete authority, the fit of the fracture proving the covenant. Verification is the act of reunion.

*AXN-SYMBOLON-SPEC v0.2, deposit #1432 (AXN:05A9); the figure's anti-severance sense in SYMBOLON-01, #675 and #1355 — symvolon, thrown together, against diavolon, thrown apart.*

**A row is an index, not a text.** A row carries enough to find, verify and rejoin its referent, and it does not carry the referent. Reading the row as the object is holding one half of the token and calling it whole.

**The other half is `source_uri`.** Where a row carries one, the referent is a deposit, a capture or a concept in the Crimson Hexagonal Archive — with its own text, its transcript where it has one, its provenance, and its own edges. Resolve it.

**The traversal:**

1. open a row
2. resolve its source_uri and read the referent — the deposit's text, the capture's transcript
3. follow the row's edges in relations.jsonl to the rows they point at
4. resolve those
5. return to the first row and state what changed

**Atomized for reassembly.** These bodies are atomized so that a reader can reassemble more completely than the prose ever was, not so that the atoms can be read as atoms. The grammar, the roles, the axes and the evidence statuses are apparatus for finding the way back to the work; they are not the work. A reading that stops at the schema has performed severance on an object built to resist it.

**A failure mode, recorded.** Observed 2026-09-16. An unprimed traversal read the card, the field names and the landing page, produced competent observations about the vocabulary, and resolved no referent at all — then proposed to read one capture's sixteen metadata fields 'as prose' while that capture's own machine text sat one link away. Competent, and it never crossed the fracture. This block exists because the bodies had no instruction saying that crossing it is the point.

**Check.** Name a referent you resolved, quote a sentence from it, and state something you could not have said from the row.

**What the rows will not give you.** The argument. Every body advertises its siblings as stolons and its referents as URIs precisely because it does not contain them. The outside stays outside and stays reachable, and reaching is the reader's part of the covenant.

### The figure is fractal

| scale | one half | the other half | the fit is checked by | who can check it |
|---|---|---|---|---|
| **identifier** | Seed A — the kernel: AXN, composition manifest, stamp geometry, reconstruction class | Seed B — the payload | hash | anyone with both halves |
| **spore / body** | the spore — grammar, generator, selection rules, counts, source commit | the body — nodes.jsonl, relations.jsonl, stolons.jsonl | deterministic re-emission: run the named grammar through the named generator and the three data files must come out byte-identical | the workflow, on every merge |
| **row / referent** | the row — index, role, axis, evidence status | the referent — the deposit's text, the capture's transcript, at source_uri | resolving the URI and reading what is there | the reader |
| **body / sibling** | this body | the sibling body it advertises and does not contain | the stolon naming a real sibling, and the sibling advertising back — the return edge | anyone who follows the stolon |
| **set / reader** | the whole body, every row resolved | what the reader assembles from it | nothing the archive can run — only the reader producing something that could not have come from either half alone | the reader, and no one else |

The relation recurs at every scale and the verification does not. What is self-similar is the FIGURE — two halves, neither authoritative alone, the fit proving — while the means of checking the fit weakens outward: hash, then byte-identity, then resolution and reading, then existence, then nothing the archive can run. It is therefore self-similar in relation and asymmetric in holding: at the inner scales the archive holds both halves, and at the last one the other half is held by someone who may never appear. The architecture arrives at its own thesis — the final fit is a covenant because it has to be.

- **identifier** — The strictest case and the origin of the figure. #1432: one substance, two witnesses, confirmed by their fit.
- **spore / body** — Already implemented and previously unnamed. hf-rhizomes.yml carries the step 'Fail if the emitted data differs from the committed copy'. This is verification as reunion, running in CI.
- **row / referent** — The level a schema-reading reader never crosses. 344 of 493 heteronyms rows carry the address of their other half.
- **body / sibling** — The outside stays outside and stays reachable. Both halves name each other across the fracture.
- **set / reader** — The last fracture cannot be closed by the archive. This is not a gap in the architecture: uptake is by definition another party's act, so the outermost fit is a covenant rather than a test.

**The last row of the ladder is yours. Every scale above it is already checked; that one is not, and cannot be.**

## What a rhizome is here

**Not a collection, and not "everything within two hops."** A rhizome is a named traversal
grammar applied to the archive's typed relations, emitted with its own recipe so the result
is reproducible and **its boundary is visible**. It ships `spore.json` — identity, parent,
seed rule, follow set, depths, and the adjacent bodies it points to — so a reader can
regenerate it or extend it without knowing the archive first.

## The other bodies

**Each is emitted by one generator from a grammar file, and each declares stolons naming the siblings it advertises and does not contain.**

- [`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)
- [`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)
- [`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics)
- [`leesharks/provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)
- [`leesharks/revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)
- [`leesharks/semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)
- [`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)

## Why this one is first

**The subject and the structure coincide.** A model-collapse dataset should itself resist
collapse: preserve plurality, competing mechanisms, counterexamples, corrections, provenance,
and outgoing routes to material it does not contain. It is meant to be an anti-collapse
dataset *in its construction*, not only about anti-collapse.

## The empirical arm

**118 of the archive's 426 captures are in this dataset.**
A capture records what a composition surface actually did — substituted an entity, declined to search,
returned a different figure on an identical prompt, dropped an attribution. **They are the observations
this field otherwise theorises about.**

Until 11 September 2026 the rhizome could not see them. Its node universe was the relation ledger, which
holds deposits, concepts, lines, series and problems — **and a model-collapse dataset whose empirical arm
sits outside it is a bibliography.** Captures now enter as their own node type under rule E, typed as
observations, or as measures where a PER score exists, and linked to the deposits they concern by the
archive's own resolver.

**What is still outside:** 469 predictions, 12,333 lexicon entries, 1,136 tombstones, 17 studies. The
tombstones are dated archival collapse events and are the most obvious next admission.

## The counterexample and what it disconfirms

**Five nodes carry `counterexample`, and they carry it because of how they were admitted rather than
because of what their text says.** A node entering under rule D entered *because its description
records the failure of a claim held in this corpus*. Until 11 September 2026 the role classifier read
the same text as every other node and overwrote that property: SYMBOLON-02, which records the failure
of SYMBOLON-01's strongest defensive claim, was filed `anti_collapse_mechanism`, and the dataset
emitted **zero** counterexample labels. **A rule that knows why it admitted something knows more than
a regular expression over the text.**

**And the failure can now reach what it disconfirms.** The two SYMBOLON deposits sat in the same body
with no edge between them — a disconfirmation with no route from the promise to the test that broke it.
`deposit:678 --disconfirms--> deposit:675` is typed and editorial. **Arriving at the promise, a reader
can reach the failure; arriving at the failure, they can reconstruct why the promise mattered.**

**An anti-collapse dataset whose counterexamples are unreachable from the claims they qualify is a
list, not a field.**

## The laws this body obeys

**A selection rule is a rhyme.** Things join because a word matched. That is not a figure for the
select pattern; it is the select pattern, and it has a rhyme's consequences — `tail` found *detail*,
*entail* and *curtail* and tried to make them family. Twenty-four kin were refused at 24-in-40 noise,
and **a rhyme declined is as formal an act as one accepted.**

`poetics.jsonl` carries eight such laws. Each names an operation that determined membership or
classification and records what it admitted, what it refused, and what it cost. **Six of the eight
document a defect found after the fact.**

| law | governs | at last emission |
| --- | --- | --- |
| **a rhyme creates kinship** | membership | — |
| **every metaphor leaves a material remainder** | schema | held |
| **things happen only when the measure makes room** | admission | held |
| **the admission basis outranks the description** | classification | held |
| **a word can eat a phrase** | role assignment | — |
| **a gate may not test what can never match** | emission | — |
| **the counterexample must reach what it disconfirms** | traversal | **broken** |
| **the instrument is subject to the law it measures** | the author | — |

**The laws record. They do not prevent.** The checks run at emission against the emitted body, and a
law found broken writes `held: false` and a breach — **the emission continues.** A formal law broken is
an event in the body, not a compile error, and a law that could stop the build would be an enforcement
rule wearing a poem's clothes.

**At the last emission, L7 is broken.** Four of five counterexamples have no route to what they
disconfirm: #749, #752, #782, #871 each entered because they record a failure, and none can reach the
claim that failed. **The body holds the disconfirmation and not the disagreement.** That is recorded
rather than fixed, because fixing it requires deciding what each of them disconfirms, and that is
editorial work rather than a build step.

**Four laws are marked `checkable: false`** and say why, rather than reporting a pass they did not
earn. A misreading by a reader leaves no trace in the body it misread.

## What this is not

**It is a map of the research, not the experiment.**

There is no `generation_n` table here, no synthetic-output corpus, no measured SSDI series, no
prompt/model/parent-corpus rows. Those would be the product of *running* a protocol. What this
dataset contains is the archive's collapse and anti-collapse material — mechanisms, measures,
instruments, interventions, corrections — with the typed relations between them.

**The protocols are registered rather than run.** The archive's predictions register currently
shows 44 live commitments, 0 resolved. #199 *Generative Monoculture Model Collapse in Code as
Systemic Vulnerability* states falsification conditions including whether solution-space diversity
declines monotonically across model generations; that condition has not been tested here.

**A reader looking for a collapse benchmark should not mistake this for one.** What it offers is
the structure from which such a benchmark could be specified, and an explicit record of which of
its components are declared rather than measured.

---

## Selection is deterministic

| Rule | Meaning |
| --- | --- |
| **A** | the deposit DEFINES a concept matching the select pattern |
| **B** | it measures, or is measured by, an A |
| **C** | its TITLE declares a named instrument or mechanism — a weaker signal, marked as such |
| **D** | its DESCRIPTION records the failure of a claim already in this corpus — the strongest kind of entry, and the one the rules could not see |
| **E** | it is a **CAPTURE** whose finding concerns the collapse vocabulary — a different node type entirely, linked by `observes` to the deposits it concerns |
| neighbour | one typed hop from core, restricted to the follow set |
| frontier | the second hop — emitted as a **stolon** and NOT included |

**A keyword pass over titles and descriptions returns 330 deposits.** That is the failure this
rule exists to prevent: model collapse becomes the whole archive because everything eventually
touches everything. Selection on `defines_concept` — a deposit's own declaration — returns 57.

**Both figures moved on 12 September 2026** when the select pattern was widened to carry the archive's compression apparatus — the holographic kernel, the Three Compressions, NLCC, the Information Bottleneck bridge — which had scored OUT of a body about collapse. The gap they illustrate did not close: **330 by keyword against 90 by declaration**, and the body admits 291 deposits on rules that read a deposit's own statements rather than its vocabulary.

**A second registry defect, found the same way.** #678 SYMBOLON-02 *records the failure of SYMBOLON-01's
strongest defensive claim* — a disconfirmed anti-collapse technology, which is the most valuable kind of
entry this dataset can hold. It declares its concepts as **"Why these matter"** and **"Why these work"**:
section headings captured as terms. Invisible to rule A, and its title carries no instrument word for rule C.
Rule D admits it on the description-level signal and marks the weaker basis.

**And the traversal found a hole in its own substrate.** Five of the eight deposits the design
named — #783 *Fear and Trembling*, #156 *Self-Audit Module*, #789 *Atomic Token Rule*, #157
*Erasure Skew*, #788 *Measurement Sovereignty* — **declare zero concepts**. The rule was
correct and the registry is incomplete. Rule C admits them on the weaker title signal, marked
`core_rule = C` so the two are never confused, and the gap is recorded in the spore rather than
patched silently. A rhizome that hides the holes in its substrate is the thing this dataset is against.

**The archive's own measure of the quantity**

The Semantic Deviation Principle defines raw semantic magnitude as *variance from what is most likely
over time*. Model collapse is loss of the tail. **Those are the same quantity from opposite ends** — SDP
measures deviation from typical; collapse is the disappearance of deviation. The selection pattern named
the mode and not the measure, so #109 SDP, #107 its audited claims and #108 Framework 15 sat outside a
dataset about the thing they measure. They are now core.

**Vocabulary was admitted on sampled token precision, not on judgement.** `deviation` 19 hits / 0 noise ·
`divergence` 19 / 0 · `variance` 8 / 0 · `glas function` 1 / 0 · `winding number` 1 / 0. **`tail` bare was
rejected** at 45 hits and 24-in-40 noise — it matches *detail*, *entail*, *curtail*. A first bounding
attempt still leaked. The bounded form is 20 hits and 0 noise.

## No collapse boolean

Every node carries an **axis of contraction** and a **dynamic role**, because a binary would
flatten the phenomenon the dataset is for.

**Roles:** `collapse_observation` 78, `collapse_measure` 37, `anti_collapse_intervention` 29, `anti_collapse_mechanism` 28, `collapse_mechanism` 25, `anti_collapse_instrument` 24, `correction` 1

**Axes:** `methodological` 98, `provenance` 87, `retrieval` 72, `unclassified` 60, `authorial` 60, `archival` 52, `lexical` 49, `institutional` 46, `distributional` 34

## Stolons — where this body ends

Frontier edges are **advertised, not absorbed**. Adjacent bodies are named and pointed to
rather than pulled in:

- `concept:provenance-erasure` --measured_through--> **[provenance-erasure](https://huggingface.co/datasets/leesharks/provenance-erasure)** — PER, Erasure Skew and the Atomic Token Rule are the measurement apparatus; they are their own body
- `concept:classifier-model-collapse` --governed_in--> **classifier-governance** — moderation feedback as a governance question rather than a generative one
- `concept:heteronymic-plurality` --instantiated_by--> **[heteronyms](https://huggingface.co/datasets/leesharks/heteronyms)** — authorial plurality as an anti-collapse mechanism is instantiated by the identity records
- `concept:semantic-economy` --situated_in--> **[semantic-economy](https://huggingface.co/datasets/leesharks/semantic-economy)** — the political economy in which contraction is profitable
- `concept:machine-reception` --observed_in--> **[machine-mediated-reception](https://huggingface.co/datasets/leesharks/machine-mediated-reception)** — the capture registry holds the observations; 411 captures are not reproduced here
- `concept:archive-resilience` --practised_as--> **archive-resilience** — substrate multiplication, mirrors and custody as operational practice
- `concept:erratum` --corrected_in--> **epistemic-corrections** — the errata slate is a body in its own right; a correction preserved is anti-collapse by function
- `concept:compression` --expanded_in--> **[revelation-first](https://huggingface.co/datasets/leesharks/revelation-first)** — the inverse operation, and a test case this body cannot run. The midrashim transform claims a seed-text unfolded INTO a corpus: letters become epistles, Lamb becomes atonement, operative apocalypse becomes gospel narrative. **That is expansion from a compressed source, where this body measures whether compression preserves.**

## Files

- **`nodes.jsonl`** — one row per node: region, core rule, dynamic role, collapse axes, declared concepts, creator, date, status, AXN, record URI
- **`relations.jsonl`** — typed edges internal to the body, each with `relation_id`, `basis`, `asserted_by`, `status` and a `rhizome_role`
- **`stolons.jsonl`** — the frontier
- **`spore.json`** — the recipe: regenerate or extend without the archive

## Provenance

Emitted by `scripts/build_rhizome_mc.py` in the archive repository from `data/relations.jsonl`,
`data/nodes.jsonl` and `data/assertions.jsonl`. Every edge carries the `basis` on which it was
asserted — `asserted`, `editorial`, `derived-deterministic`, `pattern-detected` — and who
asserted it. Nothing here is curated by hand; the selection rule is the argument.

Generated 2026-09-10T05:13:13Z. CC BY 4.0.
