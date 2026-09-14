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

## Counts

**493** nodes · **326** core · **167** neighbour · **279** edges · **6** stolons

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

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **`provenance-erasure`** — `scored_in` from `concept:attribution`
  whether a byline survived a composition is scored there. THIS BODY HOLDS THE BYLINES; that one holds the instrument.
- **`machine-mediated-reception`** — `tested_in` from `concept:entity-resolution`
  THE EXPERIMENT THIS BODY EXISTS TO MAKE POSSIBLE: whether retrieval collapses twenty-six declared identities into one. The captures are the evidence and it has not been run.
- **`model-collapse-anti-collapse`** — `narrowed_by` from `concept:heteronymic-plurality`
  collapsing distinct voices into one is the diversity loss that body measures, applied to authorship rather than to a distribution.
- **`semantic-economy`** — `laboured_by` from `concept:semantic-labour`
  who does the work when the author is twelve — or twenty-six. That body asks who produces and who benefits; this one supplies the roster and does not answer it.
- **`revelation-first`** — `instantiated_by` from `concept:author-function`
  rung 5 is a heteronymy claim about a first-century corpus: John, James, Paul, Peter and Luke as author-functions in a fractured literary system. THE ARCHIVE RUNS ONE AND READS ONE, and does not argue from the first to the second.
- **`spxi-mpai`** — `inventoried_in` from `concept:book-length-work`
  which heteronym wrote which book is held in EA-BOOKS-01, and the inscription technologies that make a byline legible to a machine are specified there.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/heteronyms.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
