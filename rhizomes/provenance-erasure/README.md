---
license: cc-by-4.0
configs:
  - config_name: nodes
    data_files: nodes.jsonl
  - config_name: relations
    data_files: relations.jsonl
  - config_name: stolons
    data_files: stolons.jsonl
---

*all things are now lawful to you in jack feist*

# EA-RHIZOME-PER-01 — provenance erasure

Where provenance disappears, and what measures it. A transformation chain — source, retrieval, selection, composition, summarisation, reception — with the instruments that score retention at each step, and the cases where the instruments were applied to themselves.

## Counts

**110** nodes · **82** core · **28** neighbour · **53** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `unit_rule` | what may be counted. #789: a PER computed on lexical tokens is A DIFFERENT METRIC, not a worse one. |
| `sovereignty_rule` | who may run the audit. #788, and the module's ordered preconditions. |
| `specification` | the founding definition of a metric. #716. |
| `instrument` | a thing that can be run. The module, its nine rendering metrics, its family metrics. |
| `skew_program` | Ω and its measurement program. #146: power-conditioned, not demographic. |
| `self_application` | the instrument applied to itself, and what happened |
| `theory` | the reasoning about what erasure is, as distinct from what measures it |
| `observation` | EVIDENCE, NOT THE BODY. A capture is where an instrument was pointed, and it belongs beneath the instrument rather than in front of it. |
| `unroled` | the honest floor |

ORDER IS THE APPARATUS, TOP DOWN, WITH THE RULES ABOVE THE THING THEY GOVERN AND OBSERVATION SECOND TO LAST.

The rules lead because #789 is titled 'Provenance Erasure Rate Under the Atomic Token Rule' — it names the metric first and is ABOUT the unit, so a classifier reaching for `specification` first files the unit rule as another specification. It did, twice: once in this body's first emission and once in its rebuild.

Observation is second to last because v0.1 put `measurement` high and mapped every capture to it — 178 of 344 nodes were measurements and 154 of those were captures. THE BODY WAS ITS OWN EVIDENCE FILE. A specification, its unit rule and its sovereignty rule are what make a number mean anything; the instrument makes it obtainable; the capture is where it was pointed.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## The other bodies

**Each is emitted by one generator from a grammar file, and each declares stolons naming the siblings it advertises and does not contain.**

- [`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)
- [`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)
- [`leesharks/model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)
- [`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics)
- [`leesharks/revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)
- [`leesharks/semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)
- [`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **[`model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)** — `narrowed_by` from `concept:provenance-erasure`
  what erasure does to a distribution over time. This body scores single transformations; that one holds the question of what repeated erasure does to the space of what can be said.
- **[`semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)** — `priced_in` from `concept:bearing-cost`
  erasure is a cost borne by the provenance-bearer and never by the composer. WHO PAYS is that body's question and this one does not answer it — it only establishes that something was taken.
- **[`machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)** — `observed_in` from `concept:attribution`
  the 425-address registry holds the observations these instruments score. This body defines PER; that body is where PER values live.
- **[`spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)** — `instrumented_in` from `concept:inscription`
  whether an inscription survived is measured here; whether it was placed well is specified there. Deliverable ten, the declared SIM set, is an anti-erasure technology.
- **[`revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)** — `adjudicated_in` from `concept:documentary-authority`
  a chronology settled on a late and ambiguous witness is an attribution question at historical scale. THE INSTRUMENTS HERE HAVE NEVER BEEN RUN ON IT.
- **[`heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)** — `borne_by` from `concept:attribution`
  PER scores whether a byline survived. That body holds the bylines, and its apparatus covers twelve of twenty-six.
- **[`poetics`](https://huggingface.co/datasets/leesharks/poetics)** — `borne_by` from `concept:extraction-fidelity`
  Pearl's machine score preserves lineation at whitespace fidelity. WHETHER AN EXTRACTION THAT PERFECT PRESERVES THE AUTHOR is this body's question and it has not been run on it.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/provenance-erasure.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
