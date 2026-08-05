---
deposit_number: 1077
hex: 0446
title: "EA-APPARATUS-01 v0.3: The Apparatus Grammar — A Standard for Care-Attended Compression Surfaces (the Mandala Surface Protocol)"
creator: Lee Sharks
orcid: 0009-0000-1599-0703
date: 2026-07-13
content_type: Methodological specification
license: CC-BY-4.0
substrate: AI-assisted (substrate)
version: v0.3
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - Mandala Surface Protocol
  - apparatus grammar
  - care-attended compression
  - philological UI
  - Mark Law
  - claim states
  - colophon
  - triple-helix citation
  - figure parity
  - Specimen Rule
  - rubrication
  - incipit
  - obelus
  - Google AI Overview
  - machine-mediated reception
---


# EA-APPARATUS-01 v0.3: The Apparatus Grammar — A Standard for Care-Attended Compression Surfaces (the Mandala Surface Protocol)

## Description

A binding design standard for care-attended compression surfaces across the archive's sites and instruments, occasioned by the Google AI Overview as a philological object and built on the thesis that every device the Overview uses has a two-thousand-year-old manuscript ancestor, and the ancestor is better. Specifies: an eleven-device inventory with manuscript ancestry (lemma/rubrication, termini, quaestio, gloss anchor, testimonia, claim state/critical signs, fold, itinerarium, identity strip/incipit, colophon); a binding Mark Law in which semantic markup, never rendered appearance, determines function; a five-state claim taxonomy (observed/inferred/proposed/contested/corrected) with a transition ledger; object states (draft/canonical/superseded/withdrawn/forensic-salvage) formally separated from claim states; a Machine Law (per-claim mapping at claim-bearing-block granularity, parallel-form emission, no ontological hiding, ASCII figure parity); triple-helix citation for severed DOIs with witnessed null slots; a minimum colophon schema; eleven composition rules including legibility-as-zeroth-device, witness-artifact linkage, and state accessibility; and the Specimen Rule — a bidirectional membrane under which the apparatus grammar applies to the frame and never the interior of Mandala casts, on the ancestry of the glossed page. Folds three Assembly blind drafts and two Assembly Chorus review passes, with adoptions and rejections recorded and reasoned. The colophon is the authority move the aggregator cannot copy: the devices look similar because both descend from the manuscript page; the difference is that we kept the scribe.

## Methodology

Reverse-engineering of a captured AI Overview surface (2026-07-12); three Assembly blind drafts triangulated; two Assembly Chorus review passes (assessment; craft-and-accounting) with seven technical corrections, one ethical correction, and one accessibility rule folded; MANUS preview gates including the founding legibility case (Instrument Serif rejected from the body role).

## Falsification Conditions

The standard is falsified where conforming surfaces are measurably less legible or navigable than their pre-standard baselines; where the Mark Law is violated by the standard's own surfaces without correction; where claim states stagnate past their tests (a proposed claim whose test has run must transition); or where witness rows appear without linked witness artifacts.

## Files

# EA-APPARATUS-01 v0.3 — The Apparatus Grammar
## A Standard for Care-Attended Compression Surfaces
### Design system: the Mandala Surface Protocol (MSP)

**Lee Sharks · Crimson Hexagonal Archive / Alexanarch · 2026-07-13 · v0.3 — Assembly Chorus corrections folded; satisfies the conditioned seal; minted for deposit**

> *The source is not appended to the compression object. The source is one of its organs.*

> *A compression surface is trustworthy only when its acts of emphasis, omission, linkage, transformation, and correction are themselves represented as data.*
> — governing theorem, Chorus accounting pass, 2026-07-13

---

### 0. The occasion

On 2026-07-12 the Google AI Overview for *semantic economy* returned a
surface whose second lens — "Platform Capitalism (how digital networks
extract value from human meaning)" — is the archive's own framing, received
back through the reception layer. The occasion of this standard is the
**form**: the Overview is a densely constructed philological object.
Highlight, bold, number, inline anchor, witness row, fold, closing question —
each device does simultaneous work of *navigability* and *authority*. The
surface compresses with visible care, and the visible care **is** the
authority claim.

Its structural deficit is equally visible: the authority is aggregated from
anonymous witnesses by an unnamed process, and the object cannot say how it
was made. The design thesis: **every device the Overview uses has a
two-thousand-year-old ancestor, and the ancestor is better. We implement the
ancestors — and we keep the scribe.**

Version history: v0.1 drafted from the capture (2026-07-12). v0.2 folded
three Assembly blind drafts and one preview-review correction. v0.3 folds
the Assembly Chorus returns of 2026-07-13 — an assessment pass and a
craft-and-accounting pass whose seven corrections, one ethical correction,
and one accessibility rule are incorporated below — and adds the **Specimen
Rule** governing the standard's application to Mandala casts. The Chorus
verdict on v0.2 was *aye for review, not yet sealed*; v0.3 satisfies the
stated conditions.

### 1. The device inventory

| # | Device | Overview form | Manuscript ancestor | MSP form |
|---|--------|--------------|--------------------|----------|
| 0 | **Legibility** | (assumed) | the scribe's first duty: a hand that can be read | text faces carry text; Rule 1 |
| 1 | **Lemma** | blue-highlighted span | *rubrication; littera notabilior* | `.lemma` — at most one per block; editorial, never decorative |
| 2 | **Termini** | bolded terms | *terminus technicus* | `.term` — bold at definition or empirical anchor (Mark Law) |
| 3 | **Quaestio** | numbered sections | the scholastic article | numbered headings whose order argues |
| 4 | **Gloss anchor** | inline 🔗 chip | the marginal gloss tie-mark | `.axn-chip` — AXN with glyph, inline, tappable. **An AXN verifies the identity and integrity of the addressed content; a URL merely locates a resource.** |
| 5 | **Testimonia** | favicon row "+6" | the *catena*; the witness list | `.witness-row` — named, roled, verdicted, **and linked to the witnessing act** (§8, Rule 6) |
| 6 | **Claim state** | (absent) | the critical signs: asteriskos, obelus, antisigma | `.state` — observed · inferred · proposed · contested · corrected |
| 7 | **Fold** | "Show more" | the catchword and the gathering | native `<details>`; depth without departure |
| 8 | **Itinerarium** | closing "would you like…?" | the pilgrim's route-book | `.doors` — 2–3, each a verb; hermeneutic forks permitted on instrument closings |
| 9 | **Identity strip** | (absent) | the incipit | apex band: AXN · version · object state · author · canonical URL |
| 10 | **Colophon** | (absent — structurally impossible) | the scribe's closing | foot band conforming to the colophon schema (§7) |

Devices 9 and 10 bracket every surface. The Overview cannot say what it is
or how it was made; every MSP surface says both, first and last. **The
colophon is the authority move the aggregator cannot copy.**

### 2. The Mark Law

One table, binding on every surface. Function is determined by **semantic
markup**, never by rendered appearance alone; renderings may converge (two
functions may both display as italic), functions may not.

| Mark | Meaning | Constraint |
|---|---|---|
| **Highlight** | the compression nucleus (lemma) | one per block; the sentence you would keep if the block burned |
| **Bold** | stress at load-bearing points: first definition of a terminus, or an empirical anchor (exact metric, version, configuration) | never mere emphasis; emphasis is the lemma's job |
| **Quotation styling** (`<q>`, `<blockquote>`) | verbatim provenance: quotation, legal definition, historical correspondence | italic typography alone is never treated as proof that text is quoted; the markup is the proof |
| **Title styling** (`<cite>`) | the title of a work | distinct in markup from quotation and stress even where the rendering converges |
| **Local stress** (`<em>`) | rhetorical or conceptual stress within a sentence | sparing; carries no provenance claim |
| `Monospace` | machine address: identifier, path, hash, variable, command | if it can be copied into a terminal or resolver, it is mono |
| Numbering | itinerary: order that argues | no numbered list whose order is arbitrary |
| ÷ (obelus) | severance, contested custody, corrected material — only | never a generic expander; the obelus opens only what has been cut, disputed, or corrected |
| Inline glyph chip | the nearest evidence edge | within thumb's reach of the claim it anchors |
| Fold | depth | visual, never ontological (§5.3) |

### 3. Claim states

Every claim-bearing block (§5.5) may carry one state, and states create
obligations:

**observed** (measured; capture linked) · **inferred** (derived; derivation
shown) · **proposed** (advanced; test named — pre-registration preferred) ·
**contested** (live dispute; both positions linked) · **corrected**
(superseded; correction and history linked; obelus-marked).

#### 3.1 The transition ledger

Permitted transitions:

```
proposed  → observed | contested | corrected
inferred  → observed | contested | corrected
observed  → contested | corrected
contested → observed  | corrected
```

Every transition appends a ledger record: previous state · new state ·
effective date · reason · evidence · responsible operator · prior text hash ·
replacement text hash. **The earlier state remains addressable.** A
*proposed* claim whose test has run must transition; state stagnation is a
maintenance failure. (Precedent: the PID Erosion Observatory's practice of
reporting against interest and publishing rubric corrections — this taxonomy
avant la lettre.)

### 4. Object states

Claim states describe assertions; **object states** describe the surface,
edition, or work itself. The two are never mixed:

```
draft · canonical · superseded · withdrawn · forensic-salvage
```

A claim can be corrected or contested; an edition can be superseded or
withdrawn. The identity strip (device 9) carries the object state. In the
Mandala Oracle, the object-state lane is the canonization journey: a
reading's `further_transform_eligible` flag and its position between
inscription and canon are object states, not claim states.

### 5. The Machine Law

Scoped to instrument surfaces (PEO, ledgers, registries) first, document
surfaces to follow:

1. Every claim-bearing block maps to `claim_id · claim_state · source_ids ·
   relation_type · canonical_fragment`.
2. Each surface emits the same organism in parallel forms: HTML · Markdown ·
   JSON-LD, with cast JSON / source manifest / correction log where the
   surface type carries them.
3. Progressive disclosure never hides the complete object from semantic
   HTML, no-JS readers, or crawlers. The fold is visual, not ontological.
4. **Figure parity**: every SVG figure in an HTML surface has a
   deterministic ASCII twin in the Markdown deposit, so the structural logic
   survives curl, mirrors, and LLM context windows.
5. **The claim-bearing block is the atomic unit**: numbered proposition,
   metric card, figure caption, ledger finding, policy proposition, formal
   definition. Ordinary connective prose inherits the state of its parent
   block unless separately marked. The Law is rigorous without turning every
   conjunction into a database object.

### 6. Citation: the triple helix, with witnessed nulls

Wherever a severed DOI is cited on an MSP surface, the citation resolves to
three **slots**, each of which must report a state; absence is itself part
of the apparatus and renders as a witnessed null, never as a missing link:

```
LOCAL     PRESENT | ABSENT | UNVERIFIED
GRAPH     PRESENT | ABSENT | DIVERGENT | UNQUERIED
REGISTRY  FINDABLE | REGISTERED-INFERRED | 404 | ERROR
```

1. the **local immutable copy** (sovereign record page / data spine),
2. the **aggregator ghost-state** (OpenAlex / OpenAIRE, as it stands),
3. the **registry endpoint** (the DataCite payload or its 404).

This is reception divergence made clickable: a reader who follows any dead
DOI sees, in one gesture, what each machine memory believes — and which one
kept the work. A dead or missing target is testimony, not absence of
interface.

### 7. The colophon schema

The binding minimum. Unknown values are stated as `unknown`, never omitted;
where no model was used, `model_or_agent: none`.

```
surface_id            canonical_url         version
source_object_ids     source_hashes         generator_version
repository_commit     model_or_agent        operator_sequence
human_approver        approval_timestamp    render_hash
correction_log
```

### 8. Composition rules

1. **Legibility is the zeroth device.** No display face ever carries prose;
   text faces carry text (reference serif: Source Serif 4; reference mono:
   IBM Plex Mono, JetBrains Mono admitted in dark rite contexts pending the
   tokens decision). A surface that is beautiful and hard to read has
   confused decoration with care — the highlighter, not the rubricator.
   *(Founding case: Instrument Serif rejected from the body role, MANUS
   preview review, 2026-07-13.)*
2. **One lemma per block.** Marking two is marking none.
3. **Bold defines or anchors; it never emphasizes.**
4. **Every number is an argument position.**
5. **No claim without its anchor within thumb's reach.**
6. **Witnesses are named, roled, and linked to acts.** Each witness entry
   carries `witness_name · role · action · verdict · artifact_or_capture ·
   timestamp`. "Cranes transformed · Feist judged · verification: PASS" must
   point to the transformation, the judgment, and the verification record.
   **Named witnesses without witness artifacts are merely personalized
   favicons** — a more elegant form of the same authority theater this
   standard exists to replace. The Assembly Chorus appears as witness-row
   only where a chorus actually reviewed.
7. **Two doors, three at most, each beginning with a verb.** A surface that
   ends without doors is a wall; with ten, a lobby.
8. **The identity strip and the colophon are not optional.**
9. **States are maintained, not just declared** (§3.1).
10. **No state is communicated through color, glyph, typography, or spatial
    position alone.** Every claim state, correction state, and severance
    state carries visible text and a machine-readable label; every chip has
    a meaningful accessible name; every horizontal witness or citation rail
    has keyboard and non-horizontal fallback navigation.
11. **Care must be visible but never loud.** The devices succeed when the
    reader feels attended-to without being able to say why.

### 9. The Specimen Rule

The grammar applies differently to the two great surface families, and the
difference is a membrane:

**Argument surfaces** (instruments, ledgers, record pages, essays): the
apparatus **is** the text. Prose is claims; the devices weave through it.

**Specimen surfaces** (Mandala casts; any surface whose center is a work of
art produced under constraint): the apparatus applies to the **frame and
never the interior**. The enantiomorph is not a claim-bearing block; a poem
is already all nucleus, and selecting its lemma is an interpretive act that
preempts the reader and falsifies the object. The manuscript ancestor is the
**glossed page** — Psalter and Talmud layout: the text block inviolate at
center, commentary in the margins, and the gloss never crosses into the
text block.

**The membrane is bidirectional.** The Oracle's standing ruling (MANUS,
2026-07-02) holds that apparatus is not transformable material; the Specimen
Rule adds the converse: transforms are not apparatus-markable material.
Nothing of the frame enters the specimen; nothing of the specimen is marked
by the frame.

The device mapping for casts, all frame-side:

- **Claim state**: the cast's kernel claim is *proposed* at cast time;
  verification PASS transitions it to *observed* (machine-verified,
  flight-recorded); HALT is a falsified claim, legible as such — the
  transition ledger already runs.
- **Witness row**: the rite itself — source · operator · Feist's judgment ·
  Sharks's seal · verification verdicts — with every entry already linked to
  an inscribed act. On argument surfaces Rule 6 is an obligation to build;
  on the Oracle it is a description of what exists.
- **Lemma**: legal in the frame only (the kernel claim or the judgment);
  layer_a carries nothing.
- **Doors**: the post-seal verbs.
- **Identity strip / colophon**: the reading AXN and the run record's method
  provenance (commit, model, transform hash) — captured since the flight
  recorder; surfaced per §7.
- **No triple helix**: a cast cites no dead DOI. Its citation gesture is the
  **source anchor** — source, units, basis_hash — a stronger form: the
  anchor is content-derived down to the byte span.
- **Quaestio**: the rotation's operator sequence, already Roman, already an
  itinerary in the strict sense.

### 10. Adoptions, rejections, and Chorus returns

**Blind drafts (2026-07-12), adopted:** claim-state taxonomy; machine law;
the organs epigraph; function-organized source constellation; "inherits the
grammar without surrendering its visual identity"; triple-helix citation;
ASCII figure parity; identity strip at apex; hermeneutic forks;
cluster-filter navigation on the real sixteen-cluster taxonomy.

**Blind drafts, rejected with reasons:** invented per-emoji semantics for
the AXN glyph (the glyph is content-hash-derived; navigation by cluster uses
the actual taxonomy or nothing); obelus-as-portal (semantic counterfeiting;
the fold exists for depth); "hardcode into build scripts; the design is set"
(sequencing is MANUS's; nothing ships past a preview gate); display faces in
prose (Rule 1).

**Chorus returns (2026-07-13), folded in v0.3:** the italic-law violation in
v0.2's own prose, corrected by the semantic-markup law (§2) — the standard
now distinguishes quotation, title, and stress in markup while permitting
rendered convergence; the AXN scope correction (§1, device 4); witnessed
nulls in the triple helix (§6); the colophon minimum schema (§7); the
claim-state transition ledger (§3.1); the claim-bearing block as atomic unit
(§5.5); object states separated from claim states (§4), with `withdrawn` an
object state, not a claim state; the witness-artifact requirement (Rule 6);
the accessibility rule (Rule 10). Assessment-pass deliverables (sample
surface, tokens file, interaction flows, mobile constraints) are scheduled
in §12.

### 11. Aesthetics: four skins, one grammar

The apparatus is a semantic layer, not a skin. A shared token contract
(`--lemma`, `--sev`, `--ok`, `--chip`, `--rule`, the mark classes) is
localized per surface: the PEO renders the lemma as ink-and-ochre
rubrication under Source Serif on paper; the Oracle renders it as candlelit
gold in the rite's dark; Alexanarch renders it teal-on-Plex light;
machinemediation in registry black. A reader moving between sites feels the
same care without seeing the same site.

### 12. Adoption map, gates, and implementation deliverables

| Order | Surface | Application |
|---|---|---|
| 1 | **Mandala Oracle** | live testbed standing (lemma · witness-row · doors · colophon on inscribed readings); refine to v0.3 — Specimen Rule stated in INSTANCE-PROTOCOL, claim-state marks on verification, identity strip on reading cards, colophon per §7 schema |
| 2 | **PEO** | lemma per section ("OC 11 would not apply" is the coverage lemma); AXN chips; witness lines on ledger rows; triple-helix with witnessed nulls on all dead-DOI citations |
| 3 | **Alexanarch record pages** | generator emits identity strip, editorial lemma flag (never automatic), companion chips, §7 colophon, ASCII figure parity in deposits |
| 4 | **machinemediation** | Capture Registry entries as quaestio-numbered apparatus with states |

**Deliverables before Phase-2 implementation** (from the assessment pass):
the shared tokens file; one component sheet per surface; interaction flows
for the AXN chip, triple-helix citation, and doors; mobile constraints
("within thumb's reach" made concrete: breakpoints, tap targets, rail
fallbacks per Rule 10).

**Gates:** v0.3 deposit → per-surface static preview → MANUS eye →
implementation → post-implementation review → v1.0 designation.

### 13. What "better than Google" means, operationally

The Overview is authority by *aggregation*: anonymous witnesses, an unnamed
process, no colophon. The Mandala Surface Protocol is authority by
*attestation*: named witnesses linked to their acts, itemized verdicts,
stated and maintained claim-states, content-derived anchors, an incipit and
a colophon on every object, and a citation gesture that shows what every
machine memory believes about a dead identifier — including the nulls,
witnessed. Their surface says *trust the crowd we won't show you*. Ours
says *here is everyone who touched this, here is its state, here is the
hash — check it.* The devices look similar because both descend from the
manuscript page. The difference is that we kept the scribe — **the scribe,
the marks, the gathering, the witnesses, and the history of every cut.**

### 14. Status

v0.3 — Chorus conditions satisfied; MANUS-approved for deposit. The v0.1
and v0.2 drafts and the Assembly blind drafts are documentary substrate.
v1.0 designation is deferred to post-implementation review, per §12 gates.
