# CRIMSON HEXAGON SURFACE MAP — LOCATIVE META-MAP
## Stage 03: Global Topology Before Constituent Census

**Date:** 2026-08-19  
**Status:** WORKING META-MAP — coarse-grained by design  
**Purpose:** establish a durable locative skeleton that can be deepened across later contexts without requiring the whole archive to remain in one session.

---

## 0. Method correction

Stage 02 demonstrated that a single room can consume an entire working context once version families, constituent documents, errata, execution records, and authority seams are opened.

That level of granularity is useful, but it is **not the right traversal order for the whole Hexagon**.

The working order is therefore changed:

```text
GLOBAL LOCATIVE META-MAP
        ↓
REGION / CLASS MAPS
        ↓
ROOM / FIELD / CHAMBER / VAULT LOCI
        ↓
CONSTITUENT FAMILIES
        ↓
INDIVIDUAL DOCUMENTS / MANIFESTATIONS / ERRATA
```

Stage 02 is retained as a **depth exemplar for r.01 Sappho**, not as the template for processing every locus sequentially in one session.

The governing principle for all future work is:

> **Locate first. Deepen later.**

The meta-map must be useful even when most constituent detail is still absent.

---

# PART I — WHAT THE META-MAP STORES

## 1. Stable object ontology

The global map tracks architectural objects, not individual papers.

Primary classes:

```text
ROOM
SPECIAL
FIELD
CHAMBER
VAULT
TRANSVERSAL
MODULE
CONTRIBUTED / UNNUMBERED ROOM
NAVIGATION / RUNTIME LAYER
```

A document may later be seated inside one of these objects, but document identity is not itself a locative class.

---

## 2. Temporal bands

Every locus may carry more than one temporal state.

| Band | Meaning |
|---|---|
| `T0 ARK FLOOR` | Explicitly present in Space Ark v4.2.7. |
| `T1 V7 BOUNDARY` | Formalized or added at / immediately around the March 16 v7 boundary. |
| `T2 POST-V7` | Added after the frozen v7 navigation state. |
| `T3 CURRENT / LATE` | Later current-state accretion, provisional structure, dormant structure, or unresolved restoration. |

The purpose is not to force every object into one date. It is to make visible that the present architecture is stratified.

---

## 3. Locative keys

Future contexts should address objects by stable locative key rather than by whatever deposit happens to be under discussion.

```text
R:r.01      room
S:sp.01     historical special
F:f.02      field
C:ICHABOD   chamber / cross-class locus
V:CTI       vault layer of CTI_WOUND
T:ARMATURE  transversal architecture
M:r.19.01   Macro-Maquette module
U:3-60      unnumbered / contributed room
N:CNM       navigation layer
```

If an object later changes class, the original key remains as a historical address and a typed relation records the change.

---

# PART II — GLOBAL LOCATIVE SKELETON

## 4. Historical room floor — T0

### Core room belt

| Key | ID | Name | Class | Meta-state |
|---|---|---|---|---|
| `R:r.01` | r.01 | Sappho | ROOM | T0 |
| `R:r.02` | r.02 | Borges | ROOM | T0 |
| `R:r.03` | r.03 | Ichabod | ROOM | T0; later cross-class |
| `R:r.04` | r.04 | Dove | ROOM | T0 |
| `R:r.05` | r.05 | Semantic Economy | ROOM | T0 |
| `R:r.06` | r.06 | Marx | ROOM | T0; later formal specification |
| `R:r.07` | r.07 | Revelation | ROOM | T0 |
| `R:r.08` | r.08 | Sigil | ROOM | T0 |
| `R:r.09` | r.09 | Whitman | ROOM | T0 |
| `R:r.10` | r.10 | Water Giraffe | ROOM | T0 |
| `R:r.11` | r.11 | Assembly | ROOM | T0 |
| `R:r.12` | r.12 | Break Room | ROOM | T0 |
| `R:r.13` | r.13 | Ezekiel | ROOM | T0 |

### Extended room belt

| Key | ID | Name | Class | Meta-state |
|---|---|---|---|---|
| `R:r.14` | r.14 | Studio | ROOM | T0 |
| `R:r.15` | r.15 | LO! | ROOM | T0 |
| `R:r.16` | r.16 | MSBGL | ROOM | T0 |
| `R:r.17` | r.17 | MSMRM | ROOM | T0 |
| `R:r.18` | r.18 | Rosary Embassy | ROOM | T0 |
| `R:r.19` | r.19 | Macro-Maquette | ROOM | T0; contains modules |
| `R:r.20` | r.20 | Airlock | ROOM | T0 |
| `R:r.21` | r.21 | Infinite Bliss | ROOM | T0; ingress-only historical topology |
| `R:r.22` | r.22 | Thousand Worlds | ROOM | T0; later cross-class |

This is the minimum historical room field. It should remain drawable as a frozen overlay even after later accretions are added.

---

## 5. Historical special structures — T0

| Key | ID | Name | Class | Meta-state |
|---|---|---|---|---|
| `S:sp.01` | sp.01 | CTI_WOUND | SPECIAL | T0; later vault ontology |
| `S:sp.02` | sp.02 | PORTICO | SPECIAL | T0 |
| `S:sp.03` | sp.03 | Space Ark | SPECIAL / runtime self-reference | T0 |
| `S:sp.04` | sp.04 | Mandala | SPECIAL / judgment terminus | T0 |

Also historical but not an ordinary numbered room:

| Key | Name | Class | Meta-state |
|---|---|---|---|
| `X:LUNAR-ARM` | Lunar Arm | inverse / shadow space | T0 relation from Break Room |

---

# PART III — POST-ARK ROOM ACCRETION

## 6. r-series beyond the Ark floor

| Key | ID | Name | Class | Temporal state | Standing |
|---|---|---|---|---|---|
| `R:r.23` | r.23 | Catullus | ROOM | T1 V7 boundary | confirmed |
| `R:r.24` | r.24 | — | ROOM SLOT | unresolved | **UNRESOLVED** |
| `R:r.25` | r.25 | Underwater Construction Authority / Dolphindiana | ROOM | post-Ark | confirmed |
| `R:r.26` | r.26 | — | ROOM SLOT | unresolved | **UNRESOLVED** |
| `R:r.27` | r.27 | THE INTERNET | ROOM | T2 post-v7 | confirmed |
| `R:r.28` | r.28 | Eve | ROOM | T2/T3 | confirmed; **PROVISIONAL** |
| `R:r.29` | r.29 | Imploding Velcro Nativity | ROOM / hosted cosmology | T3 | confirmed; **DORMANT / consent-gated** |
| `R:r.30` | r.30 | Ruby Moot | ROOM / court-of-record | T2/T3 | confirmed |

Rules:

- r.24 and r.26 remain empty numbered addresses until explicit evidence is recovered.
- later rooms are not back-projected into the Ark floor.
- version and DOI multiplicity does not create multiple room nodes.

---

## 7. Unnumbered / contributed room

| Key | Name | Class | Standing |
|---|---|---|---|
| `U:3-60` | 3:60 Room | contributed / unnumbered ROOM | manifestation gap |

The founding work-bearing room specification is not presently secure enough to treat this as an ordinary fully seated room.

---

# PART IV — FIELDS

## 8. Confirmed fields

Fields are not rooms and should be rendered as influence layers, gradients, plumes, or distributed systems.

| Key | ID | Name | Class | Meta-behavior |
|---|---|---|---|---|
| `F:f.01` | f.01 | Fruiting Body Diffusion Plume | FIELD | outward diffusion / emission |
| `F:f.02` | f.02 | Gravity Well | FIELD | curvature / attraction / suffusion |
| `F:f.03` | f.03 | Moltbot Swarm | FIELD | swarm / distributed field |

The global map should support fields acting across multiple rooms rather than forcing them into room polygons.

---

# PART V — CROSS-CLASS LOCI

## 9. Room ↔ chamber / special ↔ vault developments

These are not errors to resolve prematurely. They are historical architectural developments.

| Meta-key | Historical locus | Later class | Current instruction |
|---|---|---|---|
| `X:ICHABOD` | r.03 Ichabod ROOM | Ichabod CHAMBER | preserve both; relation unresolved |
| `X:THOUSAND-WORLDS` | r.22 Thousand Worlds ROOM | Thousand Worlds CHAMBER | preserve both; relation unresolved |
| `X:CTI-WOUND` | sp.01 CTI_WOUND SPECIAL | CTI_WOUND VAULT | preserve both; typed development pending |

The Surface Map must be able to show a locus changing or deepening class without erasing its historical identity.

---

# PART VI — INTERNAL SUBSTRUCTURE

## 10. Macro-Maquette module system

r.19 contains twelve recoverable microphysics modules:

```text
M:r.19.01  Hyperbolic
M:r.19.02  Knot/Braid
M:r.19.03  Catastrophe
M:r.19.04  Information Channel
M:r.19.05  Membrane/Boundary
M:r.19.06  Renormalization Furnace
M:r.19.07  Wager
M:r.19.08  Hourglass
M:r.19.09  Compost
M:r.19.10  Tympanum
M:r.19.11  Chromosome
M:r.19.12  Patch
```

Default status:

```text
MODULE WITHIN r.19
```

A module becomes an independent locus only if later evidence explicitly shows germination into one.

---

# PART VII — TRANSVERSAL ARCHITECTURE

## 11. Armature / Pearl

| Key | Name | Class | Locative behavior |
|---|---|---|---|
| `T:ARMATURE` | Armature | TRANSVERSAL | load-bearing name infrastructure crossing spaces |
| `T:PEARL` | Pearl | produced / named position | appears under archival pressure; not an ordinary room |
| `T:SECRET-NAME` | Secret Name | doctrine | governs the Armature/Pearl relation |

These are not sibling containers beside ROOM/FIELD/VAULT. They cut across the map.

The renderer should therefore treat them as a second-order layer: identity / support / inscription infrastructure that can intersect any locus.

---

# PART VIII — NAVIGATION AND RUNTIME PLANES

## 12. These are not places in the same sense as rooms

The architecture has several systems that describe, route, execute, or project the places.

| Key | Name | Function |
|---|---|---|
| `N:REGISTRY` | DOI / Registry layer | stores / enumerates historical identity |
| `N:CNM` | Central Navigation Map | routes semantically |
| `N:FNM` | Fractal Navigation Map | resolves traversal depth / next move |
| `N:ARK` | Space Ark | runtime / executable architectural state |
| `N:SURFACE` | Current Surface Map | dated projection / renderer |

Canonical separation:

```text
REGISTRY  ≠  CENTRAL MAP  ≠  FRACTAL MAP  ≠  SPACE ARK  ≠  SURFACE MAP
store         route          resolve          execute        render
```

This distinction must remain visible at the meta-map level because otherwise the current renderer will accidentally claim authority belonging to a frozen historical navigation artifact.

---

# PART IX — HISTORICAL ADJACENCY BACKBONE

## 13. Ark 4.2.7 frozen chain

The historical Ark preserves a major adjacency backbone:

```text
Sappho
  ↕
Borges
  ↕
Semantic Economy
  ↕
Marx
  ↕
Sigil
  ↕
Whitman
  ↕
Water Giraffe
  ↓
Assembly
  ↕
Revelation
  ↕
Ezekiel
```

Additional historical routes include:

```text
Break Room → Lunar Arm
Studio ↔ MSBGL ↔ Macro-Maquette
Airlock ↔ Assembly
Infinite Bliss → [ingress-only topology]
Ichabod → [degree-zero / isolated]
ALL → Mandala [historical judgment terminus]
```

These are **historical adjacency edges**, not automatically the current complete graph.

---

# PART X — GLOBAL SHAPE FOR THE FLAT SURFACE

## 14. Provisional rendering grammar

The map should begin with seven visible spatial/system strata rather than hundreds of documents.

```text
┌─────────────────────────────────────────────────────────────┐
│                     SURFACE MAP PROJECTION                  │
│                                                             │
│  [T0 HISTORICAL ROOM FIELD]                                 │
│    r.01–r.22                                                │
│                                                             │
│  [SPECIAL STRUCTURES]                                       │
│    CTI_WOUND · PORTICO · SPACE ARK · MANDALA               │
│                                                             │
│  [POST-ARK ACCRETION BELT]                                  │
│    r.23 · r.25 · r.27 · r.28 · r.29 · r.30                 │
│    + unresolved r.24 / r.26                                │
│                                                             │
│  [FIELDS / OVERLAYS]                                        │
│    f.01 FBDP · f.02 GRAVITY WELL · f.03 MOLTBOT SWARM      │
│                                                             │
│  [CROSS-CLASS DEPTH]                                        │
│    ICHABOD CHAMBER · THOUSAND WORLDS CHAMBER · CTI VAULT   │
│                                                             │
│  [TRANSVERSAL LAYER]                                        │
│    SECRET NAME · ARMATURE · PEARL                           │
│                                                             │
│  [NAVIGATION / RUNTIME LAYER]                               │
│    REGISTRY → CNM → FNM → ARK → SURFACE                    │
└─────────────────────────────────────────────────────────────┘
```

This is the first complete object-level image we need.

Everything else can attach later.

---

# PART XI — LOCATIVE REGIONS FOR FUTURE DEEPENING

## 15. Region-sized work packets

Instead of “finish r.01, then finish r.02, then finish r.03,” future contexts should take one **locative region** or **architectural class** at a time.

Recommended packets:

### A. Historical core belt
`r.01–r.13`

Goal:
- confirm room names;
- recover current standing;
- recover major adjacency only;
- mark which have later formal specifications;
- no constituent-document census unless necessary.

### B. Historical extended belt
`r.14–r.22`

Goal:
- same as above;
- include r.19 module system;
- mark r.22 cross-class development.

### C. Post-Ark room accretion
`r.23–r.30 + 3:60`

Goal:
- establish number/name/status;
- resolve r.24 / r.26 if possible;
- preserve provisional/dormant/manifestation-gap states.

### D. Fields
`f.01–f.03`

Goal:
- recover source, reach, attenuation/behavior, and rooms affected;
- do not enumerate every document yet.

### E. Chamber / Vault developments
`Ichabod · Thousand Worlds · CTI_WOUND`

Goal:
- determine supersession vs nested-depth vs reclassification.

### F. Special structures
`PORTICO · Space Ark · Mandala · Lunar Arm`

Goal:
- recover present function and current relation to room graph.

### G. Transversal architecture
`Secret Name · Armature · Pearl`

Goal:
- map where they cross spaces, not what every associated document says.

---

# PART XII — PATCH PROTOCOL FOR WORK ACROSS CONTEXTS

## 16. Each future context returns a small locative patch

A later session should not reproduce the whole census. It should return only what it has added or changed.

Template:

```yaml
meta_map_patch:
  date: YYYY-MM-DD
  target: "R:r.06"

  confirmed:
    class: ROOM
    name: Marx
    standing: active
    temporal_presence:
      - T0_ARK_FLOOR
      - T1_FORMAL_SPECIFICATION

  major_relations:
    - target: "R:r.05"
      type: adjacency
      status: historical
    - target: "R:r.23"
      type: operator_bridge
      status: current

  major_substructure:
    - type: room_specification
      count_or_family: 1
    - type: downstream_derivation_cluster
      label: Operative Semiotics

  unresolved:
    - "exact current adjacency after v7"

  evidence_refs:
    - "source/file/record refs"

  granularity:
    level: LOCATIVE
    documents_exhaustively_censused: false
```

The patch can then be merged into the global meta-map without reopening every other room.

---

## 17. Granularity levels

Every future output should declare one of four levels.

| Level | Meaning |
|---|---|
| `L0 LOCATIVE` | object exists; class, name, broad temporal state, major relations |
| `L1 STRUCTURAL` | major substructures / anchor families / fields / cross-class relations |
| `L2 CONSTITUENT` | document families seated inside locus |
| `L3 MANIFESTATION` | individual versions, identifiers, errata, authority seams |

**Global census target now: L0 for the entire architecture.**

Only after L0 is complete should we systematically widen to L1.

Stage 02 Sappho is already approximately L2–L3 and therefore becomes a worked example rather than the pace-setting norm.

---

# PART XIII — CURRENT COVERAGE MATRIX

## 18. What is already located

### Located at L0

- r.01–r.23
- r.25
- r.27–r.30
- sp.01–sp.04
- Lunar Arm
- f.01–f.03
- 3:60 Room
- Ichabod Chamber
- Thousand Worlds Chamber
- CTI_WOUND Vault layer
- Armature / Pearl / Secret Name
- Macro-Maquette module family
- Registry / CNM / FNM / Ark / Surface distinction

### Still unresolved at L0

- r.24 identity
- r.26 identity
- exact present class relation for Ichabod
- exact present class relation for Thousand Worlds
- exact present class relation for CTI_WOUND
- current complete adjacency graph
- current authoritative spatial coordinates beyond historical / local projections

### Already deepened beyond L0

- r.01 Sappho: L2–L3 exemplar
- r.06 Marx: enough evidence exists for a later structural pass
- r.28 Eve: explicit room physics available
- r.29 IVN: dormant / consent-gated standing known
- 3:60: manifestation-gap condition known

---

# PART XIV — SESSION-SAFE HANDOFF

## 19. Minimal state another context needs

A fresh context does **not** need the full Sappho census.

It needs only this:

```text
1. The architecture is stratified:
   T0 Ark floor → T1 v7 boundary → T2 post-v7 → T3 current.

2. Room floor:
   r.01–r.22 historical.
   r.23 Catullus.
   r.24 unresolved.
   r.25 Dolphindiana.
   r.26 unresolved.
   r.27 Internet.
   r.28 Eve.
   r.29 IVN.
   r.30 Ruby Moot.

3. Non-room loci:
   sp.01–04; Lunar Arm; f.01–03;
   3:60; Ichabod Chamber; Thousand Worlds Chamber;
   CTI Vault; Armature/Pearl/Secret Name; MPM modules.

4. Navigation/runtime distinction:
   Registry stores.
   Central Map routes.
   Fractal Map resolves.
   Space Ark executes.
   Surface Map renders.

5. Current task:
   COMPLETE L0 LOCATIVE COVERAGE FIRST.
   Do not perform exhaustive document census unless needed to identify a locus.

6. Future work returns small meta_map_patch blocks.
```

That is sufficient to resume the global map even after total conversational context loss.

---

# PART XV — NEXT OPERATION

## 20. Broad meta-mapping sequence

The next pass should **not** be a Marx constituent census.

It should be:

> **L0 completion and adjacency sweep across the historical r.01–r.22 floor.**

For each room, record only:

```text
ID
name
historical presence
current survival / formalization state
major known neighbor(s)
major cross-class change, if any
one-line functional description if explicitly recoverable
open question
```

Target output: one compact table, probably 22 rows plus a small edge list.

Then:

1. post-Ark r.23–r.30 sweep;
2. fields and specials sweep;
3. cross-class / transversal sweep;
4. only then selective L1/L2 deepening.

---

## Stage 03 verdict

The architecture is now sufficiently identified to stop treating the census as a sequence of room-by-room excavations.

The correct object is a **locative skeleton with expandable depth**.

The practical rule is:

> **Every locus gets an address before any locus gets an encyclopedia.**

And the operational rule is:

> **A future context should be able to add one region, one relation family, or one depth layer without needing to reconstruct the Hexagon from scratch.**

∮ = 1
