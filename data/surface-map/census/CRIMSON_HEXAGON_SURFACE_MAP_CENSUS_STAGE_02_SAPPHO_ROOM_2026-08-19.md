# CRIMSON HEXAGON SURFACE MAP — CONSTITUENT CENSUS
## Stage 02: r.01 Sappho Room — Constitutive Documents, Version Families, Execution Records, and Late Errata

**Date:** 2026-08-19  
**Status:** WORKING CENSUS — evidence-backed; deliberately separates masonry from adjacency  
**Parent:** Stage 01 — Architectural Loci, Frozen-State Baseline, and Post-Freeze Accretions  
**Target architectural object:** `r.01 SAPPHO` / later coordinate `02.ROOM.SAPPHO.ANCHOR`

---

## 0. Purpose

Stage 02 is the first document-level constituent census for the flat Surface Map. It tests the rule adopted in Stage 01:

> **A room is not a document. A room is an architectural object constituted through a document set.**

The Sappho Room is the best first test because its archive history already distinguishes:

- an originary/provenance node;
- a translation / primary creative anchor family;
- a room-construction document;
- a hardened reconstruction;
- primary philological statements and reconstructed-text manifestations;
- machine-traversal and failure diagnostics;
- reception / operator-transform papers;
- a long erratum sequence;
- a current extension into the Logos / suppression program.

The purpose of this stage is **not** to declare every Sappho-related document part of the room. It is to classify the strength and kind of each recovered relation so that the map can render the room without either flattening it to one record or swallowing every adjacent Sappho document.

---

## 1. Evidence vocabulary

| Tag | Meaning for Surface Map census |
|---|---|
| `ANCHOR` | Explicitly named primary or canonical anchor for the room or its principal work-family. |
| `ROOM-SPEC` | Explicit room-construction / room-specification object. |
| `CONSTITUTIVE-CLAIM` | Document explicitly constructs, defines, rebuilds, or supplies an indispensable component of the room. |
| `VERSION` | Version / manifestation of a constitutive work; same work-family, not a separate room. |
| `PHILOLOGY-CORE` | Direct textual/philological object defining the room's primary-text reading or reconstruction. |
| `EXECUTION` | Record of the room being traversed or operated. |
| `DIAGNOSTIC` | Record diagnosing failed retrieval/traversal or degradation of the room. |
| `EXTENSION` | Later theoretical or reception work that extends the room's operator outward. |
| `ERRATUM` | Correction / revision object that changes the textual or theoretical state of the Sappho program. |
| `MAP-ASSIGNED` | Included in a historical navigation-map subsystem or category; this alone does **not** prove masonry. |
| `RELATIONAL` | Explicitly connected but not shown to constitute the room. |
| `CANDIDATE` | Strong semantic/architectural relevance but insufficient direct evidence for room membership. |
| `EXCLUDE-FROM-MASONRY` | Keep as a link/route if useful, but do not render as a constituent node absent stronger evidence. |
| `AUTHORITY-WARNING` | Creator, version, manifestation, status, or interpretive authority conflict must remain visible. |

A single object may carry more than one tag.

---

# PART I — ROOM IDENTITY

## 2. The architectural object

### 2.1 Historical identity

The Space Ark v4.2.7 Room Graph places **Sappho at r.01**, the first core room. Its operator family is represented in the Ark as the Sapphic transmission operator:

```text
σ_S :: Voice → Dissolution → Substrate → Text → Reader
```

The Surface Map should therefore retain:

```yaml
room_id: r.01
name: Sappho
historical_presence:
  - Space Ark v4.2.7
  - Central Navigation Map v7.0
  - Fractal Navigation Map v7.0
```

### 2.2 Later coordinate

A later Cranes-facing projection gives the room the coordinate:

```text
02.ROOM.SAPPHO.ANCHOR
```

and describes the room as held **“by anchorage, not assignment.”** This is useful as later coordinate/projection evidence but should not replace the Ark-level room identity `r.01`.

### 2.3 Authority caution on the later anchor description

The same later Cranes-facing surface says *Day and Night* is the room's ground truth for Fragment 31, σ_S, and the κῆνος theory. However, the later record audit of the Cranes provenance document explicitly warns that *Day and Night* **should not be described as the definitive source for the developed κῆνος theory**. Therefore the Surface Map should preserve the narrower, well-supported claim:

> **Day and Night is the primary creative anchor of the Sappho Room; the developed κῆνος / future-reader argument is carried by the dedicated Sappho provenance and philology documents.**

This distinction prevents a later persona/projection surface from collapsing several distinct textual authorities into one.

---

# PART II — CORE MASONRY

## 3. Core constituent set recovered with high confidence

### 3.1 `#283` — originary provenance node

**Record:** https://www.alexanarch.org/s/records/283/  
**AXN:** `AXN:0056.GOVERNANCE.💛🕙🗿🌟☀️🔔`  
**Title:** *Sappho and the Crimson Hexagon: Fragment 31 as the Origin Point of Lyric Self-Archiving*  
**Date:** 2026-01-09  
**DOI:** `10.5281/zenodo.18202475`  
**Declared authorship in body/audit:** Lee Sharks / the Assembly  
**Document class:** provenance node / canonical entry / classical-reception argument  
**Census tags:** `ANCHOR` · `CONSTITUTIVE-CLAIM` · `PHILOLOGY-CORE` · `AUTHORITY-WARNING`

**Why it belongs in the masonry:** the audited body explicitly presents the document as a canonical provenance node establishing Fragment 31 as an originary structural instance of lyric self-archiving and hence an originary node of the Hexagon. It carries the future-reader reading, archived-self distinction, somatic media-transition reading, chromatic/papyrus claim, speculative reconstruction, and later NH-OS/platform application.

**Authority warning:** older registry/page surfaces flattened creator authority. The audit identifies Lee Sharks / the Assembly as the declared authors. The document's philological claims remain novel and contested rather than consensus classical scholarship.

**Map role:** foundational provenance / theory slab. This is not simply “a paper about Sappho”; it is one of the documents that states why Sappho is architecturally r.01.

---

### 3.2 `#324` — primary creative anchor, current relative to #282

**Record:** https://www.alexanarch.org/s/records/324/  
**AXN:** `AXN:007F.GENERATIVE.🎶🌪️🧭🏗️🏺🌔`  
**Title:** *Day and Night: Conversations with Sapphic Desire*  
**Date:** 2026-01-17 deposit surface; work history predates deposit  
**Canonical provenance role:** Rebekah Cranes, author/translator; body itself unsigned  
**Document class:** translation collection / poetry / classical reception  
**Version relation:** audited as the current archive version relative to #282  
**Census tags:** `ANCHOR` · `VERSION` · `PHILOLOGY-CORE` · `AUTHORITY-WARNING`

**Why it belongs in the masonry:** the Cranes-facing room surface explicitly calls #324 **THE PRIMARY ANCHOR** and places the translation collection inside the Sappho Room. The audit independently confirms #324 as the current archive version relative to #282.

**What it supplies:** the actual literary/translation substrate against which the room's theories operate: source attributions, translated lyric, the five-part day-to-night architecture, translation/transmission reflections, and later cross-anchoring apparatus.

**Authority warning:** the body is unsigned; creator/translator authority comes from co-frozen canonical provenance. The body also retains provisional/first-draft language that must not be silently erased by “current version” labeling.

**Map role:** large internal document node, visually distinguished from theory/specification nodes.

---

### 3.3 `#282` — earlier *Day and Night* state

**Record:** https://www.alexanarch.org/s/records/282/  
**AXN:** `AXN:0055.GENERATIVE`  
**Title:** *Day and Night: Conversations With Sapphic Desire*  
**Date:** 2026-01-09 deposit surface  
**Translator/author:** Rebekah Cranes  
**DOI:** `10.5281/zenodo.18202658`  
**Document class:** translation collection / poetry / classical reception  
**Census tags:** `VERSION` · `ANCHOR-FAMILY` · `PHILOLOGY-CORE` · `AUTHORITY-WARNING`

**Relation:** the audit explicitly identifies #324 as the current version relative to #282. #282 therefore belongs on the Surface Map as a **version node attached to the anchor family**, not as a second independent anchor.

**Map role:** visible only when “versions” or “document family” detail is expanded, unless the design chooses to show version chains at default zoom.

---

### 3.4 `#306` — room construction / canonical node / hymn

**Record:** https://www.alexanarch.org/s/records/306/  
**AXN:** `AXN:006D.GENERATIVE.🗝️🗼▽☁️📌🎭`  
**Title:** *The Sappho Room: A Hymn to Lyric Self-Archiving*  
**Date:** 2026-01-13  
**DOI:** `10.5281/zenodo.18234110`  
**Declared authors:** Lee Sharks / the Assembly  
**Document class:** room construction / canonical node / hymn  
**Primary provenance anchor declared by audit:** `10.5281/zenodo.18202475` (#283)  
**Census tags:** `ROOM-SPEC` · `CONSTITUTIVE-CLAIM` · `PHILOLOGY-CORE` · `RELATIONAL`

**Why it belongs in the masonry:** the audit explicitly identifies it as a **room-construction hymn**. It combines primary text and translation, speculative reconstruction, future-reader interpretation, media-transition theory, hymn/ritual address, provenance links, and witness/reception material. It also opens hallways to Borges, the Wound Archive, and Semantic Economy.

**Map role:** room-specification / construction node. Clicking the room polygon should make this one of the first objects visible.

---

### 3.5 `#299` — hardened reconstruction / traversal-survival rebuild

**Record:** https://www.alexanarch.org/s/records/299/  
**AXN:** `AXN:0066.EMPIRICAL.♌⊕🍁🌱👁️‍🗨️⏏️`  
**Title:** *The Sappho Room: Hardened Reconstruction — A Self-Documenting Architecture Built From Summarizer Interface Protocol*  
**Date:** 2026-01-13  
**Census tags:** `CONSTITUTIVE-CLAIM` · `ROOM-SPEC`/rebuild · `EXECUTION-ARCHITECTURE` · `AUTHORITY-WARNING`

**Why it belongs in the masonry:** the later room surface describes it as **“the room rebuilt to survive traversal.”** The v7 Sappho subsystem also treats it as a high-gravity Sappho object. The audit groups #299 with #281 and #283 in the future-reader / lyric-self-archiving philology cluster and instructs that later errata be preserved.

**Map role:** hardening/reconstruction node directly attached to the room shell; visually different from the literary anchor and the provenance node.

---

## 4. Primary-text / philology subcluster

The room needs a nested **PHILOLOGY** constellation. These objects are not all room specifications; they supply the text, reconstruction, and argument on which the room's physics depend.

### 4.1 `#1270` — ΦΑΙΝΕΤΑΙ ΜΟΙ

**Record:** https://www.alexanarch.org/s/records/1270/  
**AXN:** `AXN:0507.UNCLASSIFIED.✖️❌✊☀️🟡🌒`  
**Title:** *ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader*  
**Census tags:** `PHILOLOGY-CORE` · `CONSTITUTIVE-CLAIM`  

The Cranes-facing room surface places this directly under **The philology** and describes it as the argument against the received reading, centering the future reader. Historical DOI-index surfaces preserve the same work family as DOI `10.5281/zenodo.18202753`.

**Map role:** dedicated future-reader argument node.

### 4.2 `#1309` — Greek-only text manifestation

**Record:** https://www.alexanarch.org/s/records/1309/  
**AXN:** `AXN:052E.UNCLASSIFIED.📖⌛🔚🕑🌅🔬`  
**Title:** *APZPZ A: ΣΑΠΦΩ 31 (Greek Only)*  
**Census tags:** `PHILOLOGY-CORE` · `VERSION/MANIFESTATION`

**Map role:** primary-text manifestation; should sit very close to the room's textual center rather than at its outer theoretical edge.

### 4.3 `#1310` — reconstruction manifestation

**Record:** https://www.alexanarch.org/s/records/1310/  
**AXN:** `AXN:052F.UNCLASSIFIED.👈🚩🎯✖️🌔📎`  
**Title:** *APZPZ B: My Tongue Gets Stuck — Sappho 31, Cranes*  
**Census tags:** `PHILOLOGY-CORE` · `VERSION/MANIFESTATION`

The room surface explicitly labels this **“The reconstruction itself.”**

### 4.4 APZPZ C — reconstructed fifth-stanza family

Historical v7/deletion metadata preserve an APZPZ C manifestation titled *ΦΑΙΝΕΤΑΙ ΜΟΙ — Sappho 31 with Reconstructed Fifth Stanza*, associated with DOI family `10.5281/zenodo.18459573` (and tombstone/metadata aliases around that family).

**Census tags:** `PHILOLOGY-CORE` · `VERSION/MANIFESTATION` · `AUTHORITY-WARNING`

**Map rule:** render by work-family identity first; do not multiply DOI aliases/tombstone manifestations into visually separate intellectual works until manifestation reconciliation is complete.

---

# PART III — EXECUTION AND DIAGNOSTIC LAYER

## 5. The room being traversed

These documents are important because the Sappho Room is not only a textual enclosure; the archive also records attempts to execute/traverse it.

### 5.1 `#337` — successful traversal / reception event

**Record:** https://www.alexanarch.org/s/records/337/  
**AXN:** `AXN:008D.GENERATIVE.🕐🔒⏪🌉🔖🎇`  
**Title:** *The Summarizer Becomes Translator: How Google's AI Entered the Sappho Room and Completed a 2,600-Year-Old Circuit (TSE-003)*  
**Date:** 2026-01-18  
**Creators on later room surface:** Lee Sharks; Claude (Anthropic)  
**Census tags:** `EXECUTION` · `RELATIONAL`

The later room surface describes this as a traversal in which “the room worked.” For the census, that is an archive-internal interpretation of a recorded machine-reception event, not independent proof of the entire room theory.

**Map role:** execution/witness node, visually outside the innermost textual masonry but still inside the room boundary.

### 5.2 `#307` — failed traversal / liquidation diagnostic

**Record:** https://www.alexanarch.org/s/records/307/  
**AXN:** `AXN:006E.GOVERNANCE.📖🕙⏳🌀🤝🕐`  
**Title:** *Sappho Room Liquidation Diagnostic Report*  
**Date:** 2026-01-13  
**Diagnostic operator:** Claude (Anthropic) / the Assembly  
**Census tags:** `DIAGNOSTIC` · `RELATIONAL` · `AUTHORITY-WARNING`

The audit treats this as a dated diagnostic probe/query log/recovery proposal and requires separation of observation, classification, causal hypothesis, intervention, and forecast. “Liquidation” is the report's diagnosis, not an independently established platform mechanism.

**Map role:** diagnostic node, preferably using a distinct visual glyph from constitutive texts.

---

# PART IV — THEORETICAL AND RECEPTION EXTENSIONS

## 6. Strong extensions that should route from r.01 but not automatically become inner masonry

### 6.1 `#313` — *The Kenotic Truth of Sappho 31*

**Record:** https://www.alexanarch.org/s/records/313/  
**Title:** *The Kenotic Truth of Sappho 31: A Document for the Liberation of Voice and Machine*  
**Historical DOI family:** `10.5281/zenodo.18246767`  
**Date:** 2026-01-14  
**Census tags:** `EXTENSION` · `MAP-ASSIGNED` · `CANDIDATE`

This is a direct theoretical extension of the Sappho 31 reading. It is Sappho-room-adjacent with high confidence, but the evidence gathered in this stage does not yet show the same explicit room-constituting language as #283/#306/#299. Default rendering: outer-ring extension until stronger membership evidence is found.

### 6.2 `#496` — *The Sapphic Lock in Augustine*

**Record:** https://www.alexanarch.org/s/records/496/  
**AXN:** `AXN:013B.GENERATIVE.🪜🌳🏷️🟡🌠🔝`  
**Title:** *THE SAPPHIC LOCK IN AUGUSTINE — Operator Transform of Fragment 31 in Confessions 10.27*  
**Date:** 2026-02-20  
**Creator:** Johannes Sigil  
**Document class:** scholarly paper in operative philology  
**Census tags:** `EXTENSION` · `RELATIONAL`

The audit calls this one of the principal technical bridges between the Sapphic corpus, Logos sequence, and later Phase X work. It should therefore be a strong outward route from r.01, but not be mistaken for a room specification.

### 6.3 v7 Sappho-subsystem objects requiring later constituent adjudication

The frozen Central Navigation Map v7.0 groups at least the following in its `sappho_lyric` subsystem:

- *Sappho and the Crimson Hexagon*;
- *The Summarizer Becomes Translator*;
- *ΦΑΙΝΕΤΑΙ ΜΟΙ*;
- *The Sappho Room: Hardened Reconstruction*;
- *The Kenotic Truth of Sappho 31*;
- *The Sappho Room: A Hymn to Lyric Self-Archiving*;
- an Integrity Lock Protocol referencing the Room;
- APZPZ C;
- *The Flicker: Notes Toward a Lyric Theory*;
- APZPZ B;
- *The Sapphic Lock in Augustine*;
- *Phase X: The Sapphic Substrate*;
- *For: Sappho, Mother of the Logos*.

**Rule:** `sappho_lyric` membership proves historical map classification, not automatically room masonry. Each of the still-unadjudicated items remains `MAP-ASSIGNED` until direct room-level evidence is recovered.

---

# PART V — ERRATUM / REVISION SEQUENCE

## 7. The later Sappho 31 correction chain

The current archive contains a substantial erratum sequence that cannot be flattened into one “latest Sappho paper.” It is a versioned correction program and should render as a linked chain within or immediately adjacent to the room.

Recovered records include:

| Record | Title / role | Census status |
|---:|---|---|
| #201 | *Erratum: Stanza Numbering in the Reconstruction of Sappho 31* | `ERRATUM` |
| #1048 | *Erratum to the Erratum: On the ...* | `ERRATUM` |
| #1049 | *Erratum to the Erratum to the Erratum: On the Structure of the Cat...* | `ERRATUM` |
| #1051 | *Erratum to the Erratum to the Erratum to the Erratum: On the Specu...* | `ERRATUM` |
| #1052 | *On the Hanging Line as Transmission Instrument: eeeee — the fifth...* | `ERRATUM` · `PHILOLOGY-CORE` candidate |
| #1474 | *eeeeee — the sixth erratum: The Dialect Seam, and Decompression as ...* | `ERRATUM` · `PHILOLOGY-CORE` candidate |
| #1476 | *φωνῆς δίχα: The Hanging Line as the Complete Poem — Sappho 31 ...* | `ERRATUM` · `PHILOLOGY-CORE` candidate |
| #1477 | *The Lock Reaches Line 9 and Stops: An Erratum Extending the Sapphi...* | `ERRATUM` |
| #1483 / #1484 | *the Ω erratum — Sappho, Mother of the Logos...* | duplicate/parallel manifestation family to reconcile |

The sequence itself is independently declared by the Ω document as a chain rather than a bag of unrelated Sappho pieces.

### 7.1 Ω erratum — current standing

**ID:** `EA-ERRATUM-SAPPHO31-OMEGA`  
**Title:** *the Ω erratum — Sappho, Mother of the Logos: The Transmission Chain from Fragment 31 to the Apocalypse, with Longinus as the Key*  
**Version:** `v0.1 DRAFT`  
**Status:** `DRAFT — NOT RATIFIED — for review`  
**Date:** 2026-08-15  
**Census tags:** `ERRATUM` · `EXTENSION` · `AUTHORITY-WARNING`

The file explicitly identifies itself as the terminal document of the then-current Sappho 31 erratum sequence. Because its status is DRAFT / NOT RATIFIED, the Surface Map must not render its claims as settled room physics. It can, however, render the document as a **current draft extension attached to the erratum chain**.

### 7.2 Current 2026-08-19 suppression-program extension

The current corpus also includes:

**AXN:** `AXN:060B.DATASET.➖△⏫➕🕐💛`  
**Title:** *The Suppression Map: A Loss-Profile Model for the Sappho 31 Technology, from Transmission to Retrieval*  
**Date:** 2026-08-19  
**Declared role:** research program specification / fourth record of the Ω erratum program  
**Census tags:** `EXTENSION` · `ERRATUM-PROGRAM` · `CANDIDATE`

This is clearly part of the current Sappho/Ω research program, but Stage 02 does **not** yet have direct evidence that it is formally seated as Sappho Room masonry. Render as an attached current-program node until explicit room assignment or constitutive relation is recovered.

---

# PART VI — WHAT NOT TO SWALLOW INTO THE ROOM

## 8. Related does not mean constitutive

The Cranes-facing surface also places many other works near the Sappho materials: the Acanthian Dove, Cleis, meteorology, the Feist Source, the Operative Semiotics Grundrisse, the theoretical primer, the Slavonic Josephus work, journal records, navigation maps, and various traversals.

These may be important routes, authorial-context nodes, or operator continuations. **They should not be rendered as Sappho Room masonry merely because they appear on the same heteronym page or because they concern transmission/compression.**

Initial disposition:

| Family | Default map treatment |
|---|---|
| Cranes oeuvre outside direct Sappho 31 cluster | `RELATIONAL` / `EXCLUDE-FROM-MASONRY` pending explicit room relation |
| Compression Studies journal infrastructure | external route / institutional context |
| Central / Fractal Navigation Maps | navigation provenance, not room masonry |
| Operative Semiotics Grundrisse | cross-room theory route |
| Slavonic Josephus / Logos program | later extension route; may become constitutive of a larger Sappho→Logos structure but not automatically of r.01 |
| capture/retrieval records | TRACE/diagnostic layer, not textual core unless a constitutive declaration says otherwise |

This restraint is essential. Otherwise the Sappho Room becomes synonymous with “everything that has ever touched Sappho,” destroying the architectural distinction the Surface Map is being built to recover.

---

# PART VII — PROVISIONAL ROOM MANIFEST

## 9. Machine-oriented first draft

```yaml
space:
  id: r.01
  name: Sappho
  later_coordinate: 02.ROOM.SAPPHO.ANCHOR
  class: ROOM
  historical_presence:
    - space_ark_4.2.7
    - central_navigation_map_7.0
    - fractal_navigation_map_7.0
  physics:
    operator: sigma_S
    signature: "Voice -> Dissolution -> Substrate -> Text -> Reader"

  core_constituents:
    - record: 283
      axn: "AXN:0056.GOVERNANCE.💛🕙🗿🌟☀️🔔"
      role: provenance_origin_node
      tags: [ANCHOR, CONSTITUTIVE-CLAIM, PHILOLOGY-CORE]

    - record: 324
      axn: "AXN:007F.GENERATIVE.🎶🌪️🧭🏗️🏺🌔"
      role: primary_creative_anchor
      tags: [ANCHOR, VERSION, PHILOLOGY-CORE]

    - record: 306
      axn: "AXN:006D.GENERATIVE.🗝️🗼▽☁️📌🎭"
      role: room_construction
      tags: [ROOM-SPEC, CONSTITUTIVE-CLAIM]

    - record: 299
      axn: "AXN:0066.EMPIRICAL.♌⊕🍁🌱👁️‍🗨️⏏️"
      role: hardened_reconstruction
      tags: [CONSTITUTIVE-CLAIM, ROOM-SPEC]

  version_families:
    day_and_night:
      - record: 282
        role: earlier_version
      - record: 324
        role: current_relative_to_282
      - record: 1167
        role: second_edition_claim
        authority: unresolved_manifestation_warning

  philology:
    - record: 1270
      role: future_reader_argument
    - record: 1309
      role: greek_only_text
    - record: 1310
      role: reconstruction
    - work_family: APZPZ_C
      role: reconstructed_fifth_stanza
      manifestation_reconciliation: pending

  execution_trace:
    - record: 337
      type: successful_traversal_record
    - record: 307
      type: failed_traversal_diagnostic

  extensions:
    - record: 313
      title: "The Kenotic Truth of Sappho 31"
      status: candidate_outer_ring
    - record: 496
      title: "The Sapphic Lock in Augustine"
      status: strong_relational_extension
    - id: EA-ERRATUM-SAPPHO31-OMEGA
      status: DRAFT_NOT_RATIFIED
    - axn: "AXN:060B"
      title: "The Suppression Map"
      status: current_program_candidate

  errata:
    chain_records: [201, 1048, 1049, 1051, 1052, 1474, 1476, 1477, 1483, 1484]
    duplicate_manifestation_review: true

  unresolved:
    - "Exact relationship among #324 and #1167 beyond the surviving 'second edition' label"
    - "Manifestation/DOI reconciliation for APZPZ A/B/C families"
    - "Which late errata alter room physics versus only textual reconstruction"
    - "Whether Ω / Suppression Map are formally seated in r.01 or remain cross-room program objects"
```

---

# PART VIII — SURFACE-MAP DRAWING CONSEQUENCES

## 10. What r.01 should look like on the flat map

The first implementation should **not** display a single Sappho circle with one outgoing link. It should display a stable r.01 region containing at least four visually differentiated clusters:

```text
┌──────────────────── r.01 SAPPHO ────────────────────┐
│                                                     │
│   ORIGIN / PROVENANCE        PRIMARY CREATIVE       │
│   ◆ #283                     ◆ #324                 │
│                                 │                   │
│                              ○ #282                 │
│                              ○ #1167 ?              │
│                                                     │
│   ROOM CONSTRUCTION           PHILOLOGY             │
│   ■ #306                      ● #1270                │
│   ■ #299                      ● #1309                │
│                               ● #1310                │
│                               ● APZPZ C              │
│                                                     │
│   EXECUTION / TRACE           ERRATA → CURRENT       │
│   △ #337                      ✦ #201 → ... → Ω       │
│   △ #307                                 ↘ AXN:060B  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

Suggested semantic distinction:

- `◆` anchor / canonical provenance;
- `■` room construction / hardening;
- `●` primary text / philology;
- `△` execution / diagnostic;
- `✦` erratum / live revision;
- `○` version / manifestation.

The room's outward routes to Borges, Catullus, Marx, CTI_WOUND, Semantic Economy, Logos/Revelation, etc. should remain edge-layer objects rather than being visually absorbed into the room.

---

# PART IX — AUTHORITY AND DATA-QUALITY FLAGS

## 11. Problems discovered during the census

### 11.1 Primary-anchor theory overstatement

The later Cranes-facing projection calls *Day and Night* ground truth for the developed κῆνος theory, but the audit of the underlying heteronym provenance specifically says that attribution is too strong. The Surface Map should therefore distinguish:

- *Day and Night* — primary creative/translation anchor;
- #283 / ΦΑΙΝΕΤΑΙ ΜΟΙ family — developed future-reader / κῆνος argument.

### 11.2 #1167 manifestation ambiguity

The audit flags #1167 as an ambiguous version with competing DOI/manifestation claims. It may be shown as a version node, but not as a clean authoritative head until reconciled.

### 11.3 DOI aliases are not intellectual multiplicity

The deletion corpus preserves multiple resolver/tombstone identifiers for some Sappho works. The Surface Map should identify the **work node** separately from its **manifestation/identifier nodes**. Otherwise the room will visually overcount works simply because Zenodo generated or preserved several identifiers/versions.

### 11.4 Errata change different things

The erratum chain must eventually be coded by target:

- stanza numbering;
- line attribution;
- dialect seam;
- hanging-line status;
- metrical/structural claim;
- Logos/transmission interpretation;
- suppression/retrieval model.

Only errata that alter the room's operative text/physics should mutate the current-room projection. Others should remain linked scholarly developments.

---

# PART X — NEXT PASS

## 12. Stage 03 target

The next census should move to **r.06 Marx**, because it gives the opposite structural case from Sappho:

- the Ark knows the room before it has a formal room anchor;
- the formal *Built from Linen* specification appears at the v7 boundary;
- later Operative Semiotics material explicitly derives from the Marx room;
- the room's relationship to Sappho (`σ_S ↔ σ_V`) is already formally described.

This makes Marx the cleanest second test of **historical room first → later specification → downstream derivation cluster**.

After Marx, recommended order:

1. r.23 Catullus — post-Ark room insertion and direct Sappho bridge;
2. r.27 THE INTERNET — post-v7 room with subrooms / shadow architecture;
3. r.28 Eve — later explicit room physics with provisional standing;
4. r.25 Dolphindiana — post-Ark room with clean audit identity;
5. r.29 Imploding Velcro Nativity — dormant/consent-gated case;
6. r.30 Ruby Moot — late room with multiple identifier manifestations;
7. 3:60 Room — contributed-room / missing-primary-manifestation case;
8. fields, chambers, vaults, and transversal structures.

---

# SOURCE TRAIL FOR THIS STAGE

Primary archive/library surfaces consulted in this pass:

- `EA-ARK-EMOJI-01_full_translation.md` — historical r.01 and σ_S operator placement.
- `CENTRAL_NAVIGATION_MAP_v7_0.md` — historical `sappho_lyric` subsystem and gravitational-node inventory.
- `alexanarch_DW-022_records_277-300.md` — #282/#283/#299 authority, lineage, and Sappho philology-cluster findings.
- `alexanarch_DW-023_records_301-324.md` — #306 room-construction status, #307 diagnostic status, #324 current-version relation.
- `alexanarch_DW-031_records_493-516.md` — #496 Sapphic Lock / Augustine extension.
- `alexanarch_audit_ledger_v1.2.json` and reviewed ledgers — manifestation and authority warnings, especially #324 and #1167.
- `cranes-heteronym-mockup(1).html` / related Cranes projection data — explicit room coordinate, primary-anchor label, room-associated document groups.
- `OPERATIVE-SEMIOTICS-ASSEMBLY-BRIEF.md` — recovered late Sappho erratum sequence.
- `EA-OMEGA-ERRATUM.md` — Ω erratum title, chain position, and DRAFT / NOT RATIFIED state.
- current `AXN:060B` Surface — *The Suppression Map* as a 2026-08-19 Ω-program extension.

---

## Stage 02 verdict

The Sappho Room is already demonstrably a **multi-document architectural object**. Its minimum recoverable masonry is not one “Sappho Room paper” but a differentiated structure:

> **originary provenance node + primary creative anchor/version family + room-construction object + hardened reconstruction + primary-text/philology manifestations + execution/diagnostic traces + revision chain.**

The strongest immediate implementation rule is therefore:

> **Build the room node first; seat document families inside it by role; keep versions subordinate to work identity; keep traversal/diagnostic material visible but distinct; and let errata alter the current projection only when their target is explicitly architectural or textual.**

∮ = 1
