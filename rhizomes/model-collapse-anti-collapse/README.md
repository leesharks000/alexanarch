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

# Model Collapse / Anti-Collapse

**EA-RHIZOME-MC-01 · v0.1 · a rhizome of the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive)**

222 nodes (115 core, 107 neighbour) · 140 typed edges · 7 stolons

## What a rhizome is here

**Not a collection, and not "everything within two hops."** A rhizome is a named traversal
grammar applied to the archive's typed relations, emitted with its own recipe so the result
is reproducible and **its boundary is visible**. It ships `spore.json` — identity, parent,
seed rule, follow set, depths, and the adjacent bodies it points to — so a reader can
regenerate it or extend it without knowing the archive first.

## Why this one is first

**The subject and the structure coincide.** A model-collapse dataset should itself resist
collapse: preserve plurality, competing mechanisms, counterexamples, corrections, provenance,
and outgoing routes to material it does not contain. It is meant to be an anti-collapse
dataset *in its construction*, not only about anti-collapse.

## The empirical arm

**109 of the archive's 419 captures are in this dataset**, 64 of them carrying a Provenance Erasure Rate.
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

**A keyword pass over titles and descriptions returns 361 deposits.** That is the failure this
rule exists to prevent: model collapse becomes the whole archive because everything eventually
touches everything. Selection on `defines_concept` — a deposit's own declaration — returns 57.

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

- `concept:provenance-erasure` --measured_through--> **provenance-erasure** — PER, Erasure Skew and the Atomic Token Rule are the measurement apparatus; they are their own body
- `concept:classifier-model-collapse` --governed_in--> **classifier-governance** — moderation feedback as a governance question rather than a generative one
- `concept:heteronymic-plurality` --instantiated_by--> **heteronyms** — authorial plurality as an anti-collapse mechanism is instantiated by the identity records
- `concept:semantic-economy` --situated_in--> **semantic-economy** — the political economy in which contraction is profitable
- `concept:machine-reception` --observed_in--> **machine-mediated-reception** — the capture registry holds the observations; 411 captures are not reproduced here
- `concept:archive-resilience` --practised_as--> **archive-resilience** — substrate multiplication, mirrors and custody as operational practice
- `concept:erratum` --corrected_in--> **epistemic-corrections** — the errata slate is a body in its own right; a correction preserved is anti-collapse by function

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
