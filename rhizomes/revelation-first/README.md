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

# EA-RHIZOME-REV-01 — revelation first

The Revelation First thesis and everything it draws: the pre-70 argument, the midrashim transform, the Josephus heteronym cluster, and the Sappho material that bears on the same question of what stands first and who is assigned to it. Six rungs, and the body marks which rung a node sits on rather than treating the whole ladder as one claim.

## Counts

**271** nodes · **162** core · **109** neighbour · **170** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `dating_argument` | rung 1. When the text was composed, and how confident that answer is. |
| `priority_argument` | rung 2. Which document stands first, and whether the received answer is fact or reconstruction. |
| `material_witness` | rung 3. What the material record actually contains, as distinct from what the chronology asserts. |
| `midrashim_transform` | rung 4. The later corpus read as elaboration of a compressed seed. |
| `author_function` | rung 5. Who is assigned to a text, and when. AVAILABLE READING — the thesis does not require it. |
| `settlement_dismantled` | rung 6. The furthest claim, and the one the work plan is most careful about. |
| `operative_document` | Workstream 5. Revelation used rather than only read. |
| `reception_measure` | the work plan's own measurement arm. Its stated aim is the first measured instance of machine-mediated theological reception. |
| `experimental` | Workstream 6. Radical experimentalism, and the Sappho material that bears on the same question. |
| `unroled` | the honest floor; its count is this grammar's error bar |

ORDER IS THE LADDER. The six rungs run first, in order, so a node lands on the lowest rung it argues for rather than the most dramatic one available. That ordering is deliberate: the work plan's whole method is to distinguish claims that are usually collapsed, and a classifier that reached for rung 6 first would collapse them in the body.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **`machine-mediated-reception`** — `measured_in` from `concept:revelation-first`
  THE WORK PLAN'S OWN STATED AIM. 'If this argument enters the composition layer, it will be the first measured instance of machine-mediated theological reception — and the archive will be the bearers of that news.' The measurement apparatus is there; the argument is here.
- **`heteronyms`** — `instantiated_by` from `concept:heteronymic-plurality`
  rung 5 is a heteronymy claim about a first-century corpus, and this archive runs a heteronymic practice. The relation is not incidental and it is not argued here.
- **`model-collapse-anti-collapse`** — `seeded_from` from `concept:compression`
  the midrashim transform is a compression claim: a seed-text elaborated into a corpus. Whether that elaboration preserves or loses is the collapse body's question, not this one's.
- **`semantic-economy`** — `adjudicated_in` from `concept:documentary-authority`
  which documents count, who decides, and when a chronology becomes settled. The 1851 Act and the Domitianic consensus are the same question at different scales, and neither body resolves it.
- **`spxi-mpai`** — `instrumented_in` from `concept:retrieval-settlement`
  The work plan's aim is that its argument enter the composition layer. Those are the technologies for making an argument enterable, AND WHETHER THEY WORK ON THIS ONE IS UNTESTED.
- **`provenance-erasure`** — `scored_in` from `concept:documentary-authority`
  A chronology settled on a late and ambiguous reception-history witness is an attribution question at historical scale. THE INSTRUMENTS THERE HAVE NEVER BEEN RUN ON IT, and that is a stated gap rather than an oversight.
- **`poetics`** — `asked_of` from `concept:first-text`
  which document stands first, and who is assigned to it afterward — asked of a shelf rather than a canon.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/revelation-first.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
