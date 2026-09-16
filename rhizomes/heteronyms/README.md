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

# EA-RHIZOME-HET-01 — heteronyms

Non-singular authorship: twenty-six declared identities, what each claims, what each wrote, and how unevenly the archive's own apparatus covers them.

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

**493** nodes · **326** core · **167** neighbour · **279** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `dodecad` | the twelve. The only identities the apparatus fully covers. |
| `mantle` | seven Assembly Chorus mantles. A mantle is worn rather than inhabited — a witness position, not a person. THE NAMES ARE COMMON WORDS and a bare match on them filed 237 nodes including 'availability surface' and 'Brazilian editorial labor', so a mantle name counts only in a mantle context. |
| `aperture` | one. Lee Sharks, recorded as the aperture through which other voices emerge — itself a heteronym, per the profile. |
| `orthonym_collaborator` | two real collaborators, held in the same roster. Their presence is what makes the roster a record of relations rather than a cast list. |
| `provenanced_figure` | figures with an external provenance — an adjacent heteronym and two provenanced historical figures, one external. |
| `non_human` | one. Mary Lee Sharks, the heteronymy of non-human entities — biolabor. |
| `attribution_machinery` | the apparatus that assigns work to a name, and whose coverage stops at twelve. Named by its own field names rather than by the word `claims`, which appears in every record and filed 285 nodes as machinery. |
| `theory` | the account of why authorship is non-singular here |
| `unroled` | the honest floor; its count is this grammar's error bar |

ORDER IS THE ROSTER'S OWN TAXONOMY, most-specific-first. The Dodecad leads because it is named individually and the names are unambiguous; the broader kinds follow. A classifier that put `attribution_machinery` first would file every heteronym record as machinery, since every record contains a claims block.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## The other bodies

**Each is emitted by one generator from a grammar file, and each declares stolons naming the siblings it advertises and does not contain.**

- [`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)
- [`leesharks/model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)
- [`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics)
- [`leesharks/provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)
- [`leesharks/revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)
- [`leesharks/semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)
- [`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **[`provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)** — `scored_in` from `concept:attribution`
  whether a byline survived a composition is scored there. THIS BODY HOLDS THE BYLINES; that one holds the instrument.
- **[`machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)** — `tested_in` from `concept:entity-resolution`
  THE EXPERIMENT THIS BODY EXISTS TO MAKE POSSIBLE: whether retrieval collapses twenty-six declared identities into one. The captures are the evidence and it has not been run.
- **[`model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)** — `narrowed_by` from `concept:heteronymic-plurality`
  collapsing distinct voices into one is the diversity loss that body measures, applied to authorship rather than to a distribution.
- **[`semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)** — `laboured_by` from `concept:semantic-labour`
  who does the work when the author is twelve — or twenty-six. That body asks who produces and who benefits; this one supplies the roster and does not answer it.
- **[`revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)** — `instantiated_by` from `concept:author-function`
  rung 5 is a heteronymy claim about a first-century corpus: John, James, Paul, Peter and Luke as author-functions in a fractured literary system. THE ARCHIVE RUNS ONE AND READS ONE, and does not argue from the first to the second.
- **[`spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)** — `inventoried_in` from `concept:book-length-work`
  which heteronym wrote which book is held in EA-BOOKS-01, and the inscription technologies that make a byline legible to a machine are specified there.
- **[`poetics`](https://huggingface.co/datasets/leesharks/poetics)** — `exercised_in` from `concept:authorship`
  the roster is here; the work is there. Antioch is Lee Sharks with Damascus Dancings and Jack Feist.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/heteronyms.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
