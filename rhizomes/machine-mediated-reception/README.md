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

# EA-RHIZOME-MMRS-01 — machine mediated reception

Machine-mediated reception: what composition surfaces actually did with this archive, what that cost in provenance, and the distance between the theory of reception and its evidence.

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

**1249** nodes · **976** core · **273** neighbour · **910** edges · **8** stolons

## It was advertised before it existed

**A spore is not a template that gets copied. It germinates, and the site is written down in advance.**

- `concept:machine-reception` --**observed_in**--> `machine-mediated-reception`  ·  declared by **EA-RHIZOME-MC-01**
- `concept:machine-reception` --**transacted_in**--> `machine-mediated-reception`  ·  declared by **EA-RHIZOME-SE-01**

**The question the parent could not finish:** Both parents advertise this site and neither can finish it. The collapse body can show that reception narrows and not what the narrowing is worth. The economy body can show that legibility is priced and not what a machine actually did. OBSERVED IN and TRANSACTED IN are the two halves of the commercial case, and this is the first body germinated from two parents.

## Why more than one selection principle

MEASURED BEFORE BUILDING. Three selection principles give three different bodies and none reproduces another: editorial (MMRS journal assignment) 119 deposits; vocabulary (reception word-match) 963; evidence (deposits an actual capture cited) 332, overlapping the journal by only 29%. The word-match agrees with 86% of the journal's own members and drags in 860 others, because A RECEPTION ARCHIVE'S AMBIENT VOCABULARY IS RECEPTION VOCABULARY — capture, surface, retrieval and attribution are everywhere. The editor sees propagation (memography, the virality engine, the twenty-dollar loop) that no measurement vocabulary contains. THE DISAGREEMENTS ARE THIS BODY'S DATA, NOT ITS ERROR.

| principle | basis | caution |
| --- | --- | --- |
| **editorial** | `editorial` | A VENUE ASSIGNMENT IS AN ACT, NOT A RULE. This is the first spore material that cannot be regenerated from the ledger: the re-emit gate can verify it has not drifted and cannot derive it. Stated here rather than discovered later. |
| **vocabulary** | `pattern-detected` | The unbounded form selects 963 of 1,329 active deposits. Admitted only where the deposit ALSO declares a concept — the archive's own signal that it is MAKING a distinction rather than mentioning one. |
| **observed** | `derived-deterministic` | The only principle with a derived basis, and the only one a reader can check without trusting the editor. It finds what surfaces touched, which is not what theorises reception. |

## The disagreement is the primary datum

```
editorial                          119
vocabulary                         302
observed                           332
all_three                          14
editorial_only                     56
observed_only                      243
theory_without_observation         84
```

THE DISAGREEMENT IS THE BODY'S PRIMARY DATUM. Only 14 deposits satisfy all three principles. 56 are reachable by no rule at all — the editor saw them and nothing derivable does. 243 were touched by an actual capture and theorised by nobody. And 84 of the journal's 119 papers — 71% — HAVE NEVER BEEN OBSERVED BEING RECEIVED: theory about machine reception that no machine has been recorded receiving. For a commercial case that last number is the one to know, because it is the exact shape of what has been claimed and not demonstrated.

**Caution.** These are recomputed independently. The emitted core_rule field shows only the FIRST principle that admitted a node, because the rules run in order and setdefault wins — so the counts in nodes.jsonl are an ordering artefact and not a membership measure. Stated here so the two are not confused.

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `observation` | what a surface did, on a date, at an address |
| `instrument` | a named thing that measures reception |
| `propagation` | how something moves through the layer — the dimension the editor saw and the pattern lacked |
| `substitution` | a distinction replaced rather than lost |
| `intervention` | an operation performed on the layer rather than a reading of it |
| `theory` | the body thinking about itself |
| `unroled` | the honest floor; its count is the grammar's error bar |

ORDER IS THE CLASSIFIER. observation is FIRST here, not last, because in this body an observation is a positive kind rather than a residue — it is what a surface did. The residue is `unroled` and it is named.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## The other bodies

**Each is emitted by one generator from a grammar file, and each declares stolons naming the siblings it advertises and does not contain.**

- [`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)
- [`leesharks/model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)
- [`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics)
- [`leesharks/provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)
- [`leesharks/revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)
- [`leesharks/semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)
- [`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **[`model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)** — `narrowed_by` from `concept:machine-reception`
  RETURN EDGE to the first parent. What reception does to a distinction; the mechanism is there, not here.
- **[`semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)** — `priced_by` from `concept:machine-reception`
  RETURN EDGE to the second parent. Who gains by the reception being what it is.
- **[`provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)** — `rated_in` from `concept:provenance-erasure`
  PER and Erasure Skew as an apparatus; this body holds their outputs, not their derivation.
- **`retrieval-engineering`** — `acted_on_by` from `concept:retrieval-engineering`
  THE SITE THIS BODY ADVERTISES AND CANNOT OCCUPY. The operations that change reception rather than measure it — SPXI, AXN, MPAI, entity deployment — with EA-OPREG-01's thirteen-field schema already holding five of them and 292 claims routed. Germinated from here it arrives carrying what the operations are FOR; built standalone it becomes optimisation available to the relations it was devised to contest.
- **[`revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)** — `not_yet_observed_in` from `concept:machine-reception`
  A DECLARED ABSENCE, AND THE ONLY STOLON HERE THAT POINTS AT SOMETHING THIS BODY HAS NOT SEEN. The Revelation work plan v7.3 states that its argument is 'the one major argument in the archive that the retrieval basin has not captured', and that if it enters the composition layer it will be 'the first measured instance of machine-mediated theological reception'. 71 of this registry's 426 addresses touch that body's subject and none records the thesis entering composition. THE NULL IS THE OBSERVATION, and it is advertised here so that the absence is reachable rather than merely true.
- **[`spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)** — `instrumented_in` from `concept:inscription`
  The captures observe what surfaces did. That body holds the technologies by which an inscription is placed to be observed at all.
- **[`heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)** — `tested_on` from `concept:entity-resolution`
  WHETHER RETRIEVAL COLLAPSES TWENTY-SIX DECLARED IDENTITIES INTO ONE is an anti-collapse experiment this archive can run on itself. The captures are the evidence and it has not been run.
- **[`poetics`](https://huggingface.co/datasets/leesharks/poetics)** — `observed_in` from `concept:machine-reading-of-a-poem`
  The seat's own claim: work arguing about how the training layer receives literature does not exempt itself from being received. THIS BODY HOLDS WHAT HAPPENED; that one holds the poems.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/machine-mediated-reception.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
