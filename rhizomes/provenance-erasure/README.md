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

**190** nodes · **123** core · **67** neighbour · **99** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `magnitude` | PER and its M/C/D dimensions — HOW MUCH IS LOST. With the unit rule that says what may be counted, because a PER on the wrong unit is a different metric. |
| `orientation` | Ω — WHICH WAY IT FALLS. Not a programme beside the metric: the second axis of one framework. 'A rate without an orientation cannot tell you who was erased.' |
| `precondition` | what runs before any metric, in an order the module calls load-bearing. ABN is rank zero. |
| `instrument` | the module and its metrics. Five versions; v3.2 self-complete, 'because a module that cannot be run from one document is a changelog rather than a module.' |
| `process_provenance` | the third dimension the site adds to C2PA and PER. 'Fluency can be generated. Provenance must be borne.' |
| `before_the_machines` | Domain 2. Erasure is older than the composition layer, and the site argues it at Sophistical Refutations 183b. |
| `reception` | what surfaces did with the instruments. Named shapes rather than generic loss — including the battery where a surface fabricated replacement metrics, ran them on itself, and gave itself perfect scores across all dimensions. |
| `self_application` | the instrument applied to itself. The Self-Audit Module Dissolved, PER 1.00. The Empty Bracket. |
| `theory` | the reasoning about what erasure is |
| `evidence` | where an instrument was pointed. Beneath the apparatus, not in front of it. |
| `unroled` | the honest floor |

ORDER IS THE SITE'S, AND MAGNITUDE AND ORIENTATION LEAD TOGETHER because the site says they are the two moments of one loss. Preconditions next, because the module runs them before any metric and calls the order load-bearing. Then the instruments that produce a number, then the domains the framework claims, then the named pathologies, then self-application, then evidence.

TWO EARLIER GRAMMARS PUT MY OWN CATEGORIES HERE AND BOTH MISSED THE FRAMEWORK'S CENTRAL PAIR.

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
