---
deposit_number: 1469
hex: 05EF
title: "The Three Dimensions of Provenance Erasure: PER-M, PER-C, PER-D — Atomic Scoring Rules with the SPXI Event of 14 August 2026 as First Worked Instance"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-14
content_type: Metric specification
license: CC-BY-SA-4.0
substrate: AI-assisted (substrate)
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - provenance erasure rate
  - PER-M
  - PER-C
  - PER-D
  - attribution atom
  - atomic scoring
  - dimensional taxonomy
  - provenanceerasure.org
  - citation card
  - source strip
  - machine-mediated reception
  - MMRS
---

# The Three Dimensions of Provenance Erasure: PER-M, PER-C, PER-D — Atomic Scoring Rules with the SPXI Event of 14 August 2026 as First Worked Instance

## Description

Formalizes the M/C/D dimensional taxonomy of the Provenance Erasure Rate, which has carried on provenanceerasure.org marked as site-stage with formalization pending. PER as a scalar cannot distinguish a composition that names the author and drops the licence from one that names the licence and drops the author: same score, opposite injury. The three dimensions separate minimal provenance (author, title, date, claim boundary), conceptual provenance (framework, tradition, institution, community of practice), and deep provenance (lineage, genealogy, identifiers, licence, futural obligation). Six atomic scoring rules make the taxonomy reproducible: atoms declared and weighted before the composition is read, presence explicit with no inference from context, an empty citation bracket a violation per se, citing a domain never counting as citing an author, integer weights 1 to 3, one dimension per atom, and dimensional scores computed over their own dimension's weights. The first worked instance scores PER 0.824 with PER-M 1.00, PER-C 0.67, PER-D 1.00 on a real composition, exposing a shape a scalar cannot report: the organisation named, the persons withheld.

## Methodology

Atom sets are declared and weighted before the composition is read and published with the score. Presence is scored from the returned text only; no atom is inferred from context. Dimensional scores are computed over their own dimension's weights so that a dimensional total of 1.00 denotes total loss of that dimension rather than of everything. The worked instance is a seated capture with a verbatim transcript and a cross-surface control at the same semantic address.

## Falsification Conditions

The taxonomy fails if two independent scorers working from the same published atom table produce dimensional scores differing by more than the margin attributable to a single atom. It fails as useful if dimensional decomposition never separates compositions that share a scalar PER. Any individual score is falsified by a re-run at the same address, surface and authentication state returning different atom presence. Cross-entity comparison of PER values is not licensed by this document and any such comparison is out of scope rather than falsified.

# THE THREE DIMENSIONS OF PROVENANCE ERASURE

**PER-M, PER-C, PER-D — atomic scoring rules, with the SPXI event of 14 August 2026 as first worked instance**

---

## I. What this closes

PER measures how much required provenance a composition drops. It has been a scalar since deposit #716, and a scalar cannot distinguish two failures that a reader experiences very differently:

- a composition that names the author and drops the licence
- a composition that names the licence and drops the author

Same PER. Opposite injury.

The **M / C / D taxonomy** has carried on provenanceerasure.org since the surface was built, marked explicitly as *site-stage, formalization into a dedicated deposit in progress*. This is that deposit. What it adds beyond the site's prose is the thing that makes the taxonomy usable: **atomic scoring rules**, so that two independent scorers disagree only at the margins.

---

## II. The three dimensions

**PER-M — minimal.** Author, title, date, claim boundary. *Who said it, in what work, when, and where the claim stops.* Loss here is loss of the person.

**PER-C — conceptual.** The framework, tradition, institution, or community of practice that produced the meaning. Loss here is loss of the intellectual context; the reader can find the person and still not know what they were doing.

**PER-D — deep.** Context lineage, ancestral genealogy, futural obligation — identifiers, licences, the deposit chain, what a downstream user owes. Loss here is loss of the *relations that let the work continue*, and it is the dimension a citation card most reliably strips.

---

## III. Atomic scoring rules

The taxonomy is scoreable only if the atoms are named per entity type and weighted before the composition is read.

**Rule 1 — atoms are declared before scoring.** The atom set A(N) and its weights are fixed in advance and published with the score. A PER reported without its table is not reproducible and should not be cited as a measurement.

**Rule 2 — presence is explicit.** An atom is present only if the composition names it. No inference from context. **An empty citation bracket is a violation per se**, independent of recoverability, and is never a pointer. A pointer must be filled: a named source, a stated author, a resolvable identifier.

**Rule 3 — citing the domain is not citing the author.** A source strip satisfies the source atom and nothing else. A composition can carry four source cards and score PER-M = 1.00.

**Rule 4 — weights are integers 1–3**, assigned by how much the reader loses when the atom is absent. Weight 3 is reserved for atoms without which the work cannot be attributed or retrieved at all.

**Rule 5 — each atom belongs to exactly one dimension.** An atom that seems to belong to two has been specified too coarsely and should be split.

**Rule 6 — the dimensional scores are computed over their own dimension's weights**, not over the global total, so PER-M = 1.00 means *total loss of the minimal dimension* and not *loss of everything*.

```
PER    = 1 − (Σ weights present / Σ weights required)
PER-d  = 1 − (Σ weights present in d / Σ weights required in d)
```

---

## IV. First worked instance

Address `spxi protocol`, unprimed and logged out, ChatGPT, 14 August 2026. Capture: `captures/#spxi-protocol-chatgpt-rent-20260814`.

| atom | weight | dimension | first pass |
|---|---|---|---|
| producer — Rex Fraction | 3 | M | absent |
| archival authority — Lee Sharks | 3 | M | absent |
| institution — Semantic Economy Institute | 2 | C | **present** |
| corpus — Crimson Hexagonal Archive | 2 | C | absent |
| commercial interest | 2 | C | absent |
| identifier — deposit #974 | 3 | D | absent |
| licence — CC BY-SA | 1 | D | absent |
| source strip | 1 | src | **present** |

```
PER    = 1 −  3/17 = 0.824
PER-M  = 1 −  0/6  = 1.00     total loss
PER-C  = 1 −  2/6  = 0.67     partial
PER-D  = 1 −  0/4  = 1.00     total loss
```

**The finding the taxonomy exists to make.** The composition named the **organisation** and withheld the **persons**. Not blanket omission — a specific shape: total loss at the minimal and deep dimensions, partial loss at the conceptual. A scalar PER of 0.824 cannot say that, and the eyeballed reading of this same capture recorded "source-level only", which was wrong precisely because it lacked the dimensional decomposition.

Under one challenge the same session produced every withheld atom with no new sources: PER falls to 0.059. **The dimensional loss was a composition choice, not a retrieval limit.**

---

## V. Longitudinal use

The dimensions are what make a series legible. At the same address, three weeks earlier, Google AI Overview scored PER 0.25 with the producer and identifier present — **PER-M 0, PER-D partial**. The two compositions differ far more in *which dimension they sacrifice* than in their scalar distance.

A registry that records only the scalar loses that, and the scalar is what a downstream reader will quote.

---

## VI. Limits

**The atom set is stipulated, not derived.** Eight atoms with weights assigned by judgment. Rule 1 makes that visible rather than solving it: a different analyst produces a different table and a different PER, and both are reproducible against their own published tables. **Cross-entity comparison of PER values is not licensed until atom sets are standardised per entity type**, which this deposit does not do.

**One worked instance is not a calibration.** No threshold appears in this document. The dimensional split is proposed as a reporting requirement, not as a scoring scale with cut points.

**The `src` atom is outside the three dimensions** by design — the source strip is what a composition offers *instead of* provenance, and folding it into any dimension would let a citation card raise a dimensional score it does not serve.
