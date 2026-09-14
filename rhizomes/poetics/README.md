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

# EA-RHIZOME-POET-01 — poetics

The poems, the poetics, and what the archive has said about how a poem is read by a machine.

## Counts

**42** nodes · **0** core · **0** neighbour · **10** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `undersong` | a piece that elaborates another piece in the same book. Three Undersongs and a Footnote, all attached to PEARL. |
| `essay` | the appendix: essays, manifestos, minutiae |
| `apparatus` | front matter. Note that two of six are by heteronyms — Sigil introduces, Feist supplies from THE CRIMSON HEXAGON. |
| `poem` | the made thing. In this book, most of it. |
| `unroled` | the honest floor |

ORDER IS THE BOOK'S OWN. Undersong and Footnote before poem, because a piece that elaborates another is a different kind of thing and the generic pattern would swallow it. Apparatus last, because in this body the front matter is what surrounds the work.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **`machine-mediated-reception`** — `observed_in` from `concept:machine-reading-of-a-poem`
  THE SEAT'S OWN CLAIM is that work arguing about how the training layer receives literature does not exempt itself from being received. That body holds the evidence of what happened when these poems were read.
- **`provenance-erasure`** — `scored_in` from `concept:extraction-fidelity`
  the score preserves the lineation; WHETHER IT PRESERVES THE AUTHOR is scored there.
- **`model-collapse-anti-collapse`** — `measured_in` from `concept:two-objects`
  a score with perfect back-projection on the text and none on the artwork is a case the kernel apparatus has not been run on. AN EXTRACTION CAN BE LOSSLESS AND STILL NOT BE THE BOOK.
- **`heteronyms`** — `instantiated_by` from `concept:authorship`
  who wrote which poems. Antioch is Lee Sharks with Damascus Dancings and Jack Feist; Day and Night is Rebekah Cranes.
- **`spxi-mpai`** — `manifested_in` from `concept:seated-original`
  Pearl is EA-CORPORA-03/02. The one seat that is the archive's own, and the only one whose licence lets both objects ship.
- **`revelation-first`** — `contested_in` from `concept:first-text`
  which document stands first and who is assigned to it afterward — asked of a corpus rather than a shelf.
- **`semantic-economy`** — `priced_in` from `concept:unpaid-making`
  A POEM IS SEMANTIC LABOUR THAT NOBODY PAID FOR, which is that body's §4.1 exactly — ontology engineering as semantic labor, the work the value is taken from. Pearl was printed in 2014 by a press the author runs, and the question of who bears the cost of making it is not answered here.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/poetics.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
