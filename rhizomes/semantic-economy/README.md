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

# EA-RHIZOME-SE-01 — semantic economy

The archive's political economy of meaning, seeded at the stolon the collapse body left open. Its roles are NOT the collapse roles: where that body asks what narrows, this one asks who gains by the narrowing.

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

**512** nodes · **353** core · **159** neighbour · **424** edges · **7** stolons

## It was advertised before it existed

**A spore is not a template that gets copied. It germinates, and the site is written down in advance.**

- `concept:semantic-economy` --**situated_in**--> `semantic-economy`  ·  declared by **EA-RHIZOME-MC-01**

**The question the parent could not finish:** the political economy in which contraction is profitable

## The vocabulary is the archive's, not the emitter's

REBUILT FROM THE DEFINING PAPERS, 2026-09-12. v0.1 scoped this body to the ten numbered extraction operators of #27 Operative Architecture. Those are ONE REGION — §3.2, the extraction problem — of a framework that has three (§3.1 labor, §3.2 extraction, §3.3 enclosure) and six economic forms. The scoping was done by pattern-matching vocabulary rather than by reading what the framework says it covers.

#623 SEMANTIC INFRASTRUCTURE: FROM TIM BERNERS-LEE TO THE SEMANTIC ECONOMY is the bridge paper and its §4 IS the filter — a mapping from technical operations to economic forms: ontology engineering as semantic LABOR, knowledge graphs as semantic CAPITAL, standards as semantic INFRASTRUCTURE, knowledge-panel and API use as semantic RENT, model ingestion as semantic LIQUIDATION, maintenance failure and recursive degradation as semantic EXHAUSTION.

#255 SEMANTIC LIQUIDATION: AN EXECUTIVE SUMMARY supplies the operation's internal structure — three properties (irreversibility, value transfer, invisibility) and five stages (tokenization, stripping, attribution relocation, value capture, closure).

#24 MIND-CONTROL POEMS supplies the counter-operation: alienation extended into the symbolic infrastructure through which labor, recognition and desire become thinkable, and the liberatory poem as a symbolic counter-operation that interrupts conditioning and restores contact with relation and historical possibility.

| principle | basis | caution |
| --- | --- | --- |
| **vocabulary** | `pattern-detected` | ADDED 2026-09-12 AFTER THE GRID LIED. The organized grid reported that semantic_rent had NO INSTRUMENT AND NO MEASUREMENT, and I wrote that up as the body's largest gap and its most commercial one. It was an artifact. #1462 'Semantic Rent, Measured: Use, Acknowledgment, Discount, Supply', #1470 'One Transcript, Whole Stack: The Full Measurement of the SPXI Rent Event', #1479 its computation record and #1465 'Position Is Not Class' were all ACTIVE, all matched the select pattern on their titles, and all were ABSENT — because this grammar declared no core_principles, so rule V never ran and the body was selected by rule A alone, which matches DECLARED CONCEPTS rather than titles. A paper called 'Semantic Rent, Measured' whose declared concepts do not use the phrase was invisible to a body about semantic rent. |
| **title** | `pattern-detected` | ADDED AFTER #137 WAS FOUND ABSENT. The Semantic Commodity Form — the framework's own Marx extension, the paper this grammar was rebuilt from — was excluded because rule V requires a deposit to ALSO declare a concept, and #137 declares none. So do #140 its metadata packet, #150 the Assembly Chorus act, and #765 its ratification record.

The concept requirement was bounding over-selection that came from DESCRIPTION matching: title plus description selects 272, TITLE ALONE SELECTS 107. A title is the author's declaration of subject and needs no second signal. Rule V keeps its bound for description matches; a title match admits on its own. |

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `semantic_commodity_form` | #137 — THE GENERAL CASE, not one of the six. The six forms of #623 §4 are forms OF this: 'the meaning is preserved as retrievable, the authorship is negated as presence. The said survives; the act of saying is the lifted-and-cancelled term.' Sublation performed on meaning rather than labor-time, 'though the two were never separable, because the saying WAS labor.' It sits first because a deposit that names the general case is about the general case, whichever form it discusses. |
| `semantic_labor` | #623 §4.1 — ontology engineering as semantic labor. Who does the work the value is taken from. |
| `semantic_capital` | #623 §4.2 — knowledge graphs as semantic capital. Accumulated structured meaning, owned. |
| `semantic_infrastructure` | #623 §4.3 — standards as infrastructure. What everyone builds on and nobody is paid for. |
| `semantic_rent` | #623 §4.4 — knowledge-panel and API use as rent. Charging for access to what was given. |
| `semantic_liquidation` | #623 §4.4 and #255 — conversion of situated meaning into retrievable units, destroying context or authorship. Five stages, three properties. |
| `semantic_exhaustion` | #623 §4.5 — maintenance failure and recursive degradation. 'Model collapse is not a metaphor.' |
| `counter_operation` | #24 — the symbolic counter-operation. Not compensation alone; commons repair. |
| `accounting` | the instrument that makes the accounting possible — PER, tau, Omega, the registry |
| `instance` | an observed occurrence in the composition layer. Evidence that the operation ran, not a claim about which form it took. |
| `analysis` | the body thinking about itself |
| `unroled` | the honest floor; its count is this grammar's error bar |

ORDER IS THE CLASSIFIER. semantic_commodity_form is FIRST because it is the general case and the six are forms of it; a paper naming it is about it, whichever form it discusses. Then the six in #623 §4's own order — labor, capital, infrastructure, rent, liquidation, exhaustion — which runs from what is produced to what is destroyed. counter_operation and accounting follow because they act on the six rather than being among them.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## The other bodies

**Each is emitted by one generator from a grammar file, and each declares stolons naming the siblings it advertises and does not contain.**

- [`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)
- [`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)
- [`leesharks/model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)
- [`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics)
- [`leesharks/provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)
- [`leesharks/revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)
- [`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **[`model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)** — `narrowed_by` from `concept:semantic-economy`
  THE RETURN EDGE. The collapse body advertised this one; this one advertises it back. What contraction looks like from the side of the ledger — the question the parent could not finish is answered here only in part, and the part it cannot finish is what contraction does to meaning itself.
- **[`provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)** — `priced_in` from `concept:provenance-erasure`
  erasure as a cost borne by the provenance-bearer and never by the composer — the asymmetry is the operation's economic form
- **[`machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)** — `transacted_in` from `concept:machine-reception`
  the captures are where the economy is observable; 425 of them are not reproduced here
- **[`heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)** — `laboured_by` from `concept:heteronymic-plurality`
  who does the work when the author is twelve
- **[`revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)** — `settled_in` from `concept:documentary-authority`
  A DOCUMENTARY-AUTHORITY SETTLEMENT AT SCALE. The Domitianic consensus is a claim about which witness counts, decided by whom, and at what point it stopped being questioned — the same four powers this body measures, applied to a chronology rather than a form. Its primary external anchor is a late and ambiguous reception-history witness, and that is an admissibility question. This body does not adjudicate it.
- **[`spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)** — `built_in` from `concept:semantic-infrastructure`
  #623 §4.3 maps standards to semantic infrastructure — what everyone builds on and nobody is paid for. That body is this archive's own stock of them, and 91% of its specified protocols carry no deployment marker.
- **[`poetics`](https://huggingface.co/datasets/leesharks/poetics)** — `made_in` from `concept:semantic-labour`
  the writing the apparatus exists for. WHO PRODUCES is this body's question and a poem is an answer to it.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/semantic-economy.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
