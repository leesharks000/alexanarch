# Dataflow Atlas — v1.1 addendum (2026-08-11)

## The heteronym dataset acquires a join, and the archive draws itself

Prior head: `atlas-v1.0-addendum.md` (2026-08-06).
Deposited under tether **#1448 · AXN:05D9.ARCHIVAL.🍄🔎💡🝊🔙🏗️**.

The atlas has not previously covered `datasets/heteronyms/`. It does now, because that
dataset stopped being a standing description of twelve positions and became a **join** —
and because four artefacts were added that are *generated from the corpus* rather than
authored about it, which is a flow the map has no other instance of.

---

## §1 · NEW NODE — `datasets/heteronyms/crosswalk.json`

**Inputs, all read and none written:**

| source | what is taken |
|---|---|
| `data/registry.json` | the creator field of every deposit |
| `data/citation-graph.json` | 9,453 deposit-level edges |
| `data/lexical-minting-registry.json` | 12,073 terms, keyed on `defined_in_deposit` |
| `data/concept-map.json` | 63 concepts, current record and prior versions |
| `data/wiki-entries.json` | 1,445 entries, keyed on creator |

**Output:** one object per position carrying authored-deposit count, minted-term count and
sample, concept membership, wiki-entry count, and directed citation degrees in and out.

**The join rule is the load-bearing part.** A position owns a deposit **only if it is named
in the creator field**. *Names X* and *is by X* are different claims and the crosswalk keeps
them apart: 458 deposits qualify, and the orthonym-signed majority is **excluded rather than
assigned to a default**. Any downstream figure inherits this rule, so a reader can always
ask what a colour means and get an answer.

**Direction of flow:** strictly downstream. The crosswalk never writes back to the
registry, the citation graph or the lexicon. Its summary *is* copied into the twelve
records under `crosswalk`, which is a projection, not a source.

---

## §2 · A CLASS OF ARTEFACT THE MAP HAS NOT HELD — the derived figure

Every other figure in the fleet is **composed**: a person read a record and decided what to
draw. These four are **projections**. The distinction matters for custody, so it belongs on
the map:

> A composed figure is an argument about the archive. A derived figure is a **view** of it.
> Disagreement with a derived figure is disagreement with the corpus rather than with its
> renderer.

**All four are deterministic.** Jitter, where present, is a SHA of the term or slug rather
than a random draw, so *the same corpus always paints the same picture* — and therefore
**a change in an image is evidence of a change in the archive**. That property is what makes
them instruments rather than decoration.

| artefact | reads | states |
|---|---|---|
| `dodecad-graph.svg` | crosswalk | positions as nodes; in-degree sets radius, citation count sets edge weight. Edges below weight 12 omitted, **and the figure says so on its face** |
| `citation-field.svg` | registry + citation graph | all 9,136 edges among 1,447 deposits, nothing filtered; chord curvature from endpoint distance, so chords crossing the centre are **late work citing early work** |
| `lexical-field.svg` | registry + lexical registry | 12,073 terms as motes in the sector of the coining position; **5,056 in a voice, 7,017 in the ground** |
| `capture-field.svg` | `EA-WG-CAPTURES-01.json` | 261 dated reception events across twelve section bands; larger motes are phrase-matched |

**Generators:** `scripts/build_dodecad_graph.py --write`,
`scripts/build_citation_field.py --write`. Both regenerate from current data; neither takes
an argument that could bias the output.

---

## §3 · WHAT THE JOIN SHOWED THAT NO SINGLE NODE COULD

Collapsing the citation graph from deposits to positions is a lossy operation, and it is
worth doing because the loss is exactly the noise:

- **Sigil ↔ Fraction at 167 and 147.** Near-symmetric, which is a *dialogue* and not a
  hierarchy — and not a shape anyone would hand-author, since an author would make one
  primary.
- **Ichabod Spellings: 100 out, 2 in.** A substrate cites and is not cited. **Nobody wrote
  this into the data.** A noise floor was specified, deposits accumulated over months, and
  a citation graph was built for unrelated purposes; the theory came back out.
- **Sigil minted 2,556 terms of 12,073; Fraction 1,638.** Two positions, a third of the
  vocabulary.
- **7,017 terms belong to no position.** The heteronyms did not build the lexicon. They
  inflected it.

---

## §4 · PATHOLOGY REGISTER — additions

**P-31 · SURFACE-ONLY FINDING.** Work performed on a published surface and never folded
back into the dataset the surface is generated from. Observed three times in one session:
traversal logs, capture links, and five heteronym records built as HTML with no dataset
entry. **Detection:** for any generated surface, assert that every claim on it resolves to
a field in its source. **Consequence:** the next generation of the surface silently drops
the finding.

**P-32 · UNTESTED UNIFORMITY.** A pattern written once and propagated without a single
instance being exercised. Observed as 144 dead grid squares — twelve pages of twelve links
each, all pointing at a path that does not exist, none ever clicked. **Detection:** test one
instance per propagated pattern, not one per pattern.

**P-33 · CANONICAL SOURCE TAKEN TOO LITERALLY.** A field read correctly from the source of
truth and reported without asking whether the source is *right*. Observed as
`crimshexagonal.org`, a typo in `data/fleet-domains.json` reported as a dead domain.
**Detection:** when a canonical value fails an external check, test the value's neighbours
before reporting the world wrong.

---

## §5 · WHAT THE MAP NOW SAYS ABOUT THE HETERONYM LAYER

Before this addendum the twelve positions were **described** in a dataset and **rendered**
on twelve surfaces, with no path between the description and the archive's other data.
There is now a single downstream join, and four instruments that read it.

The consequence for custody is small but real: **the heteronym layer is now falsifiable
against the corpus.** If a position's page claims a shape the citation graph does not
support, the graph says so, and it says so in a picture that regenerates on every change.

∮ = 1
