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

**344** nodes · **254** core · **90** neighbour · **151** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `unit_rule` | what may be counted. #789: decomposing a query into lexical tokens is A DIFFERENT METRIC and a disqualifying error. |
| `sovereignty_rule` | who may run the audit. #788. The module expressly rejects self-certification. |
| `self_application` | the instrument applied to itself, and what happened. The body's distinguishing cases. |
| `skew_analysis` | #146: retention varies with retrieval capital rather than demographic position, and demographic categories are not variables in the estimator |
| `metric` | a defined quantity with a unit of analysis. #716, #141, #780. |
| `extraction` | erasure described as something taken rather than something lost |
| `measurement` | an instrument's output on a date, at an address |
| `analysis` | the body reasoning about its own instruments |
| `unroled` | the honest floor; its count is this grammar's error bar |

ORDER PUTS THE RULES ABOVE THE OUTPUTS, and a first emission got this backwards. With `metric` first, #789 'Provenance Erasure Rate Under the Atomic Token Rule' matched on PER and filed as a metric — leaving `unit_rule` with one node and `sovereignty_rule` with one, the two roles this grammar argues matter most.

A metric's unit rule and its sovereignty rule are what make its number mean anything. #789 exists because a PER computed on the wrong unit is 'A DIFFERENT METRIC', not a worse one, and #788 exists because a self-certified audit is not an audit. `self_application` and `skew_analysis` follow, because a case where the instrument was turned on itself is a finding rather than a reading, and Ω's power-conditioning is a property of the estimator rather than an output of it.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **`model-collapse-anti-collapse`** — `narrowed_by` from `concept:provenance-erasure`
  what erasure does to a distribution over time. This body scores single transformations; that one holds the question of what repeated erasure does to the space of what can be said.
- **`semantic-economy`** — `priced_in` from `concept:bearing-cost`
  erasure is a cost borne by the provenance-bearer and never by the composer. WHO PAYS is that body's question and this one does not answer it — it only establishes that something was taken.
- **`machine-mediated-reception`** — `observed_in` from `concept:attribution`
  the 425-address registry holds the observations these instruments score. This body defines PER; that body is where PER values live.
- **`spxi-mpai`** — `instrumented_in` from `concept:inscription`
  whether an inscription survived is measured here; whether it was placed well is specified there. Deliverable ten, the declared SIM set, is an anti-erasure technology.
- **`revelation-first`** — `adjudicated_in` from `concept:documentary-authority`
  a chronology settled on a late and ambiguous witness is an attribution question at historical scale. THE INSTRUMENTS HERE HAVE NEVER BEEN RUN ON IT.
- **`heteronyms`** — `borne_by` from `concept:attribution`
  PER scores whether a byline survived. That body holds the bylines, and its apparatus covers twelve of twenty-six.
- **`poetics`** — `borne_by` from `concept:extraction-fidelity`
  Pearl's machine score preserves lineation at whitespace fidelity. WHETHER AN EXTRACTION THAT PERFECT PRESERVES THE AUTHOR is this body's question and it has not been run on it.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/provenance-erasure.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
