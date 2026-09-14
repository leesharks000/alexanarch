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

**247** nodes · **158** core · **89** neighbour · **124** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `poem` | the made thing |
| `art_object` | the book as an object whose page is load-bearing. Nothing derived from it replaces it. |
| `machine_score` | the score. Not the piece. |
| `poetics` | the account of how the thing works |
| `seated_source` | the poets on the shelf beside it |
| `reception` | what happened when a machine read a poem |
| `apparatus` | what surrounds a work and is not the work |
| `unroled` | the honest floor |

ORDER PUTS THE MADE THING FIRST AND THE APPARATUS LAST, WHICH INVERTS EVERY OTHER BODY HERE. Elsewhere the instrument leads because the instrument is the contribution. Here the poem leads and a navigation map is what surrounds it — which is the whole reason this body was built.

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
