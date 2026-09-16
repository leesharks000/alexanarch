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

Pearl and Other Poems as its own graph: 42 pieces across four sections, the edges the book makes between them, and the captures in which a machine read the book or a piece of it.

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

## Counts

**99** nodes · **42** core · **0** neighbour · **31** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `passage` | a located span; assigned by the passage layer, not by pattern |
| `undersong` | a piece that elaborates another piece in the same book. Three Undersongs and a Footnote, all attached to PEARL. |
| `essay` | the appendix: essays, manifestos, minutiae |
| `apparatus` | front matter. Note that two of six are by heteronyms — Sigil introduces, Feist supplies from THE CRIMSON HEXAGON. |
| `poem` | the made thing. In this book, most of it. |
| `unroled` | the honest floor |

ORDER IS THE BOOK'S OWN. Undersong and Footnote before poem, because a piece that elaborates another is a different kind of thing and the generic pattern would swallow it. Apparatus last, because in this body the front matter is what surrounds the work.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## The other bodies

**Each is emitted by one generator from a grammar file, and each declares stolons naming the siblings it advertises and does not contain.**

- [`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)
- [`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)
- [`leesharks/model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)
- [`leesharks/provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)
- [`leesharks/revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)
- [`leesharks/semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)
- [`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **[`machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)** — `observed_in` from `concept:machine-reading-of-a-poem`
  THE SEAT'S OWN CLAIM is that work arguing about how the training layer receives literature does not exempt itself from being received. That body holds the evidence of what happened when these poems were read.
- **[`provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)** — `scored_in` from `concept:extraction-fidelity`
  the score preserves the lineation; WHETHER IT PRESERVES THE AUTHOR is scored there.
- **[`model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)** — `measured_in` from `concept:two-objects`
  a score with perfect back-projection on the text and none on the artwork is a case the kernel apparatus has not been run on. AN EXTRACTION CAN BE LOSSLESS AND STILL NOT BE THE BOOK.
- **[`heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)** — `instantiated_by` from `concept:authorship`
  who wrote which poems. Antioch is Lee Sharks with Damascus Dancings and Jack Feist; Day and Night is Rebekah Cranes.
- **[`spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)** — `manifested_in` from `concept:seated-original`
  Pearl is EA-CORPORA-03/02. The one seat that is the archive's own, and the only one whose licence lets both objects ship.
- **[`revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)** — `contested_in` from `concept:first-text`
  which document stands first and who is assigned to it afterward — asked of a corpus rather than a shelf.
- **[`semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)** — `priced_in` from `concept:unpaid-making`
  A POEM IS SEMANTIC LABOUR THAT NOBODY PAID FOR, which is that body's §4.1 exactly — ontology engineering as semantic labor, the work the value is taken from. Pearl was printed in 2014 by a press the author runs, and the question of who bears the cost of making it is not answered here.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/poetics.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
