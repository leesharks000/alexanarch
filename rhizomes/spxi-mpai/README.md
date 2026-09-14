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

# EA-RHIZOME-SPXI-01 — spxi mpai

The archive's documentary technologies: SPXI and its protocol family, MPAI packets, conformance instruments, disambiguation matrices, entity-definition blocks, compression kernels and inscription surfaces. AN INVENTORY, NOT AN ARGUMENT — and the distinguishing field is whether a technology is deployed, specified-and-dormant, or superseded.

## Counts

**256** nodes · **159** core · **97** neighbour · **113** edges · **7** stolons

## Roles

**Order is the classifier** — `role_for` returns on first match, so a broad pattern above a narrow one swallows it.

| role | what it names |
| --- | --- |
| `protocol` | what a conforming surface must carry. Specifies; does not measure. |
| `instrument` | what tests whether a surface carries it. #143: 'a standing protocol that cannot be checked is a wish.' |
| `packet` | an inscription placed at an address so an entity is legible there. Constructs positively and negatively at once. |
| `identifier` | what makes a thing referenceable across surfaces that do not share a registry |
| `kernel` | a fragment carrying enough structure to regenerate the whole. #76's apparatus, deployed. |
| `surface` | where a technology is actually placed, and the report that it was |
| `disambiguation` | distinguishing a thing from what shares its letters. #63 distinguishes SPXI from a TSX-listed ETF, the S&P 500 Index, the Society of Saint Pius X, SEO and GEO. |
| `unroled` | the honest floor; its count is this grammar's error bar |

ORDER SEPARATES SPECIFICATION FROM MEASUREMENT, which is the distinction #143 exists to hold: 'It is NOT the protocol itself; the protocol specifies, the instrument measures.' A body that filed both as `protocol` would lose the only thing that tells a wish from a fact.

A node matching nothing falls to `unroled`, whose count is this grammar's own error bar.

## Where it points and does not go

**Advertised, not included.** The outside stays outside and stays reachable.

- **`machine-mediated-reception`** — `measured_in` from `concept:inscription`
  whether an inscription was received is not answerable from the inscription. The capture registry holds the observations; this body holds the instruments that made them placeable.
- **`semantic-economy`** — `priced_in` from `concept:documentary-authority`
  these are documentary technologies, and #623 §4 maps standards to semantic infrastructure — what everyone builds on and nobody is paid for. Who bears the cost of inscription discipline is that body's question.
- **`model-collapse-anti-collapse`** — `specified_in` from `concept:reconstructive-compression`
  the holographic kernel is deliverable eight here and a formal apparatus there. THIS BODY DEPLOYS IT; that body defines what it must satisfy.
- **`revelation-first`** — `contested_in` from `concept:retrieval-settlement`
  the Revelation work plan's stated aim is that its argument enter the composition layer, and these are the technologies by which an argument is made enterable. WHETHER THEY WORK ON THAT ARGUMENT IS UNTESTED.
- **`provenance-erasure`** — `scored_in` from `concept:inscription`
  Whether an inscription survived is measured there; whether it was placed well is specified here. Deliverable ten — the declared SIM set — is an anti-erasure technology whose effect is scored by that body's instruments.
- **`heteronyms`** — `inscribed_for` from `concept:byline`
  the inscription technologies that make a byline legible to a machine. Deliverable five — disambiguation and negative tags — is what keeps two heteronyms from resolving to one entity.
- **`poetics`** — `carried_by` from `concept:seated-original`
  EA-CORPORA-03/02, the one seat that is the archive's own and the only one whose licence lets both objects ship.

## Reproducing it

```
RHIZOME_GRAMMAR=rhizomes/_grammars/spxi-mpai.json \
  python3 scripts/build_rhizome_mc.py
```

`spore.json` carries the recipe and the commit of the ledger it came from. The grammar is read, not carried: every determining rule above lives in `rhizomes/_grammars/`, and a different body means a different grammar file, not a fork of the generator.

Emitted from the [Crimson Hexagonal Archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive) · [alexanarch.org](https://www.alexanarch.org/)
