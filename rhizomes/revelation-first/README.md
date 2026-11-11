---
license: cc-by-4.0
configs:
  - config_name: exits
    data_files: exits.jsonl
  - config_name: kernel_candidates
    data_files: kernel_candidates.jsonl
  - config_name: ladder
    data_files: ladder.jsonl
  - config_name: nodes
    data_files: nodes.jsonl
  - config_name: placements
    data_files: placements.jsonl
  - config_name: relations
    data_files: relations.jsonl
  - config_name: states
    data_files: states.jsonl
  - config_name: stolons
    data_files: stolons.jsonl
  - config_name: three_claims
    data_files: three_claims.jsonl
---

*all things are now lawful to you in jack feist*

# EA-RHIZOME-REV-01 — revelation first

Revelation First, as its framework holographic kernel holds it (EA-HK-REVFIRST-01 v1.4, #1755, Damascus Dancings): the thesis that the Apocalypse of John is the first-composed book of the New Testament, set apart from early dating ('not early, FIRST', #202), with its three claims kept apart (absolute priority priced, corpus priority a finding, generative priority a programme of reversible arrows, #1735) and its six rungs, each with its fit, its body of evidence and its defeat condition; rung VI depends on rung V, and rungs I–IV stand without either. Every record the kernel seats is here with its stratum and clusters, placed on each rung its claims place it on. A second tier holds what bears on the subject and the kernel does not name; records other kernels hold are exits.

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

### The figure is fractal

| scale | one half | the other half | the fit is checked by | who can check it |
|---|---|---|---|---|
| **identifier** | Seed A — the kernel: AXN, composition manifest, stamp geometry, reconstruction class | Seed B — the payload | hash | anyone with both halves |
| **spore / body** | the spore — grammar, generator, selection rules, counts, source commit | the body — nodes.jsonl, relations.jsonl, stolons.jsonl | deterministic re-emission: run the named grammar through the named generator and the three data files must come out byte-identical | the workflow, on every merge |
| **row / referent** | the row — index, role, axis, evidence status | the referent — the deposit's text, the capture's transcript, at source_uri | resolving the URI and reading what is there | the reader |
| **body / sibling** | this body | the sibling body it advertises and does not contain | the stolon naming a real sibling, and the sibling advertising back — the return edge | anyone who follows the stolon |
| **set / reader** | the whole body, every row resolved | what the reader assembles from it | nothing the archive can run — only the reader producing something that could not have come from either half alone | the reader, and no one else |

The relation recurs at every scale and the verification does not. What is self-similar is the FIGURE — two halves, neither authoritative alone, the fit proving — while the means of checking the fit weakens outward: hash, then byte-identity, then resolution and reading, then existence, then nothing the archive can run. It is therefore self-similar in relation and asymmetric in holding: at the inner scales the archive holds both halves, and at the last one the other half is held by someone who may never appear. The architecture arrives at its own thesis — the final fit is a covenant because it has to be.

- **identifier** — The strictest case and the origin of the figure. #1432: one substance, two witnesses, confirmed by their fit.
- **spore / body** — Already implemented and previously unnamed. hf-rhizomes.yml carries the step 'Fail if the emitted data differs from the committed copy'. This is verification as reunion, running in CI.
- **row / referent** — The level a schema-reading reader never crosses. 344 of 493 heteronyms rows carry the address of their other half.
- **body / sibling** — The outside stays outside and stays reachable. Both halves name each other across the fracture.
- **set / reader** — The last fracture cannot be closed by the archive. This is not a gap in the architecture: uptake is by definition another party's act, so the outermost fit is a covenant rather than a test.

**The last row of the ladder is yours. Every scale above it is already checked; that one is not, and cannot be.**

## Counts

**148** nodes · **80** kernel · **68** outside · **53** edges · **73** placements · **12** exits · **49** kernel_candidates · **7** stolons

## Governed by its kernel: EA-HK-REVFIRST-01 v1.4 (#1755)

Rule K: the kernel's records (its strata and joins, every record with argument moves, every record a claim names, and the kernel itself) and the captures it names. Rule O: the outside tier the grammar names, each node with its reason, carrying no rung and no standing. Placement is the kernel's claims; `lexical_role` is the v0.1 word match, kept beside it and never setting it. Exits name records held by other kernels. The kernel's ladder, three claims and dated states ship as tables; kernel_candidates lists what this body's reading proposes to the kernel's next version, for the operator's ruling.

**The ladder** (`ladder.jsonl`; a record's rungs are in `rungs`, each placement with its claim and passage in `placements.jsonl`):

| rung | name | fit | body | depends on | defeated by |
| --- | --- | --- | --- | --- | --- |
| rung:I | the reversed consensus (dating) | REVERSIBLE | D | — | An external or material anchor fixing the received form of Revelation after 70 CE. |
| rung:II | the Gallio gap (Pauline priority) | SAME-CLASS | D | — | An independent, securely dated anchor — material or external, but not the corpus’s self-narrated chronology — placing the composition of any Pauline letter before the earliest plausible date of Revelation’s received form. |
| rung:III | the first corpus | INDEPENDENT | C | — | Evidence of a sevenfold Pauline church collection demonstrably circulating before Revelation, or a persuasive demonstration that Revelation’s number, order and single-book architecture depend on such a collection. |
| rung:IV | the midrashim transform | EXECUTABLE | G | — | Identify New Testament passages that cannot be derived from Revelation through any plausible transform: these are the counterevidence. |
| rung:V | the Josephus thesis | CONTINGENT | H | — | Contingent by construction. Defeated without disturbing rungs I–IV. It is also defeated by demonstration that the phenomena it explains are more economically explained by ordinary multiple authorship. |
| rung:VI | the permanent incarnation (the Logos) | DEPENDENT | H | rung:V | Depends on V. Defeated without disturbing rungs I–IV. |

**The three claims, kept apart** (`three_claims.jsonl`): **absolute**: temporal: Revelation completed before the earliest surviving Pauline letter (#1735 §I); **corpus**: formal: the seven-church corpus prior as a form; 'occasional Pauline letters may be earlier' (#1735 §IV.4); **generative**: arrow by arrow: particular structures compressed in Revelation elaborated later (#1735 §I).

Other tables: `states.jsonl` (the dated states of priority, generation and authorship), `exits.jsonl` (records other kernels hold), `kernel_candidates.jsonl` (what this body's reading proposes for the kernel's next version, for the author's ruling).

**Version 0.1, superseded 2026-11-10.** Read against the kernel on 2026-11-10, the vocabulary-built body held 8 of the kernel's 47 records, among them neither the seed #202 nor this grammar's own defining paper #1217, and lacked #1735, #1747 and #1755. Its six-rung ladder was the #1217 work plan's: its rung 6, 'the settlement dismantled', is a different claim from the kernel's rung VI, the permanent incarnation (the Logos), which depends on rung V. The ladder_distribution's reading of an empty rung 6 as 'consistent with the argument's restraint' was produced by first-match ordering (HF audit F10) and describes a rung the kernel no longer frames that way; it is kept here as what it was. Of the 99 deposits and 191 captures the vocabulary admitted outside the kernel, 12 deposits are held by other kernels (exits), 3 bear on Revelation unnamed by the kernel (the outside tier), and about 83 came in on archive vocabulary ('crimson hexagon', 'space ark', 'logos', 'lamb', 'first', 'sappho') with no graph path or reading that relates them to the kernel; of the captures, 87 are on the subject by query or reading (the outside tier) and 104 on vocabulary only. The operator adopted this reading the same day.

## The lexical classifier (recorded, not governing)

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

In this version the role patterns are a lexical classifier only: their first match is recorded as `lexical_role` beside the kernel's placement and never sets a rung (HF audit F10).

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## The other bodies

**Each is emitted by one generator from a grammar file, and each declares stolons naming the siblings it advertises and does not contain.**

- [`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)
- [`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)
- [`leesharks/model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)
- [`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics)
- [`leesharks/provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)
- [`leesharks/semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)
- [`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **[`machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)** — `measured_in` from `concept:revelation-first`
  THE WORK PLAN'S OWN STATED AIM. 'If this argument enters the composition layer, it will be the first measured instance of machine-mediated theological reception — and the archive will be the bearers of that news.' The measurement apparatus is there; the argument is here.
- **[`heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)** — `instantiated_by` from `concept:heteronymic-plurality`
  rung 5 is a heteronymy claim about a first-century corpus, and this archive runs a heteronymic practice. The relation is not incidental and it is not argued here.
- **[`model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)** — `seeded_from` from `concept:compression`
  the midrashim transform is a compression claim: a seed-text elaborated into a corpus. Whether that elaboration preserves or loses is the collapse body's question, not this one's.
- **[`semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)** — `adjudicated_in` from `concept:documentary-authority`
  which documents count, who decides, and when a chronology becomes settled. The 1851 Act and the Domitianic consensus are the same question at different scales, and neither body resolves it.
- **[`spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)** — `instrumented_in` from `concept:retrieval-settlement`
  The work plan's aim is that its argument enter the composition layer. Those are the technologies for making an argument enterable, AND WHETHER THEY WORK ON THIS ONE IS UNTESTED.
- **[`provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)** — `scored_in` from `concept:documentary-authority`
  A chronology settled on a late and ambiguous reception-history witness is an attribution question at historical scale. THE INSTRUMENTS THERE HAVE NEVER BEEN RUN ON IT, and that is a stated gap rather than an oversight.
- **[`poetics`](https://huggingface.co/datasets/leesharks/poetics)** — `asked_of` from `concept:first-text`
  which document stands first, and who is assigned to it afterward — asked of a shelf rather than a canon.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/revelation-first.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
