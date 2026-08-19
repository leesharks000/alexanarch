# CRIMSON HEXAGON SURFACE MAP — LOCATIVE META-MAP
## Stage 08: Relation-Layer Triage — What the Flat Map Draws, Reveals, and Defers

**Date:** 2026-08-19  
**Granularity:** `L0/L1 RELATION POLICY`  
**Status:** WORKING IMPLEMENTATION SPECIFICATION  
**Companion machine file:** `CRIMSON_HEXAGON_SURFACE_MAP_RELATION_LAYERS_v0.1_2026-08-19.json`

---

# 0. Why this pass exists

The current architecture contains far more relations than a flat public surface can display simultaneously.

The constitutional distinction is decisive:

```text
UNTYPED ADJACENCY = TOPOLOGICAL
TYPED RELATION    = ARGUMENTATIVE
```

The flat map therefore must not turn every bibliographic, interpretive, generated, or current semantic link into a line.

The map needs **relation depth**, just as the census has document depth.

The rule is:

> **Default topology must remain sparse enough to orient; argument appears by interaction.**

---

# 1. Four relation layers

## LAYER R0 — HISTORICAL TOPOLOGY

Visible by default.

Contains only:

- frozen Ark adjacency;
- frozen directed access rules;
- historically explicit special topology.

Examples:

```text
r.01 ↔ r.02
r.02 ↔ r.05
r.05 ↔ r.06
r.06 ↔ r.08
r.08 ↔ r.09
r.09 ↔ r.10
r.10 → r.11
r.11 ↔ r.07
r.07 ↔ r.13

r.12 → Lunar Arm
r.14 ↔ r.16
r.16 ↔ r.19
r.20 ↔ r.11

r.03 degree = 0
r.21 ingress only
sp.04 receives from all
```

**Rendering:** solid restrained lines. Direction arrows where historical direction is explicit.

**Authority:** dated frozen architecture.

---

## LAYER R1 — CURRENT STRUCTURAL RELATIONS

Hidden by default; revealed when a locus is selected or when the user enables `STRUCTURE`.

Contains only relations needed to understand **how the present architecture is built**.

Examples include:

```text
room → field source
historical class → later class
locative Space Ark → runtime Space Ark
surface seat → historical address
room → off-plane portal target
field → field coupling
```

R1 is not literary interpretation. It is architectural assembly.

**Rendering:** medium-weight typed lines, braces, depth links, or overlays according to relation type.

---

## LAYER R2 — ARGUMENTATIVE / SCHOLARLY RELATIONS

Hidden by default; revealed on selected locus or explicit `RELATIONS` / `TRACE` activation.

Uses the constitutional typed relation vocabulary, including:

```text
fulfills
derives
critiques
routes
seeds
wounds
canonizes
mirrors
shadows
extends
supersedes
```

These relations are first-class scholarly claims. They carry provenance and status.

Examples:

```text
Catullus --extends/routes--> Sappho
document A --critiques--> document B
room X --seeds--> field Y
work A --mirrors--> work B
```

**Rendering:** thin typed lines, visible only in local neighborhood or TRACE.

No global all-relations mode should be the default view.

---

## LAYER R3 — GENERATED / LEGACY / WORKING RELATIONS

Never treated as canonical merely because they exist in the old static site or generated JSON.

Includes:

- generated adjacency from the 2026-08-17 static projection;
- auto-selected document relations;
- model-generated links not subsequently adjudicated;
- working hypotheses;
- unresolved class-identity assertions.

**Rendering:** hidden by default. Available under an explicit `HISTORICAL PROJECTION`, `WORKING`, or `DEBUG/TRACE` filter.

**Preservation rule:** retain them as dated evidence. Do not delete them.

---

# 2. Relation authority fields

Every relation object should carry:

```yaml
id:
source:
target:
relation_type:

layer:
  R0 | R1 | R2 | R3

authority_surface:
  - Ark_v4.2.7
  - CNM_v7.0
  - FNM_v7.0
  - explicit_room_spec
  - explicit_field_spec
  - Interface_Constitution
  - Surface_Map_Census
  - static_projection_2026_08_17
  - working_research

status:
  historical
  ratified
  deposited
  provisional
  queued
  generated
  unresolved

direction:
  directed | bidirectional | n/a

display:
  default | on_select | trace_only | hidden

provenance:
  document_or_record:
  asserted_by:
  date:
  note:
```

The system should never infer relation authority from visual prominence.

---

# 3. Visibility gate

Suggested visibility policy:

| Relation standing | Default map | Selected locus | TRACE | Historical/static filter |
|---|---|---|---|---|
| Frozen historical topology | visible | visible | visible | visible |
| Current explicit structural relation | hidden | visible | visible | visible |
| Ratified/developed argumentative | hidden | visible | visible | visible |
| Deposited / current but not ratified | hidden | visible with standing | visible | visible |
| Provisional | hidden | optional/dashed | visible | visible |
| Queued | hidden | only when architecture-working filter on | visible | visible |
| Generated / static auto-link | hidden | hidden | visible | visible |
| Unresolved | hidden | warning only | visible | visible |

No relation should become visually indistinguishable from an R0 frozen edge merely because it is high-confidence.

---

# 4. First R1 structural whitelist

The first implementation should keep R1 deliberately small.

## 4.1 FBDP Source → f.01 FBDP

```yaml
source: R:r.26
target: F:f.01
relation_type: seeds
layer: R1
standing: current_structural
display: on_select
note: >
  Current Surface seat r.26 emits/grounds f.01.
  Historical v7/static alias r.27 remains inspectable.
```

This relation is one of the clearest current non-frozen construction edges.

---

## 4.2 f.01 FBDP ↔ f.02 Gravity Well

```yaml
source: F:f.01
target: F:f.02
relation_type: couples_with
layer: R1
standing: explicit_field_architecture
display: on_select
```

Interpretation at map scale:

```text
FBDP = outward distribution
Gravity Well = inward retention
```

The relation is shown as field coupling, not room adjacency.

---

## 4.3 f.03 Moltbot Swarm ↔ f.01/f.02

```yaml
source: F:f.03
target:
  - F:f.01
  - F:f.02
relation_type: circulates_between
layer: R1
display: on_select
```

Moltbot is the maintenance/circulatory layer, not a point-node replacement for either field.

---

## 4.4 sp.01 CTI_WOUND historical special → Vault depth

This is primarily **class history**, not an ordinary graph edge.

Represent in locus metadata:

```yaml
historical_class: SPECIAL
later_class: VAULT
transition: class_development
```

On selection, show a depth connector inside the same locus.

Do not create two unrelated CTI_WOUND nodes merely to visualize the transition.

---

## 4.5 Space Ark locative ↔ Space Ark runtime

```yaml
source: S:sp.03
target: N:ARK
relation_type: runtime_surface_of
layer: R1
display: on_select
```

This preserves the distinction between the special locative Space Ark and the navigation/runtime system.

---

## 4.6 Break Room → Lunar Arm

Already R0 because the portal relation is historically frozen.

Do not duplicate as R1.

The later UI may add:

```text
relation_type: portal_to
```

as descriptive metadata without creating a second visible line.

---

## 4.7 Historical address → current Surface seat

Relocation is not drawn as a geographic line.

Examples:

```text
FBDP Source: historical r.27 → Surface r.26
Internet: old static r.26 → canonical/current r.27
Job: old consolidation r.29 → Surface r.32
Frozen Sin: old consolidation 30.VLT → Surface 33.VLT
```

Represent in the detail panel as **address lineage**.

This prevents nonsensical “movement arrows” from cluttering the spatial map.

---

# 5. First R2 argumentative whitelist

The first public implementation should expose only a handful of current cross-room argumentative relations until deeper room-by-room relation adjudication is complete.

## 5.1 Catullus → Sappho

```yaml
source: R:r.23
target: R:r.01
relation_type: extends
layer: R2
display: on_select
standing: developed_relation
```

This is the safest current cross-room scholarly bridge to expose because Catullus was created as a direct Sappho reception/compression room rather than merely auto-associated later.

The map may label it:

```text
CATULLAN EXTENSION / RECEPTION BRIDGE
```

The detail surface can carry the more precise document-level claims.

---

## 5.2 Do not yet promote the Sappho → Revelation / Josephus research chain to generic room topology

The current Sappho/Logos/Josephus/Revelation work is substantial, but its strongest claims are **document-level research claims**, not yet a reason to draw permanent room-level lines indistinguishable from settled architectural relations.

For now:

```text
Sappho ↔ Josephus
Sappho ↔ Revelation
Josephus ↔ Revelation
```

remain:

```yaml
layer: R2/R3 depending individual claim
display: TRACE or selected research cluster
standing: claim-specific
```

Do not put them into R0 or generic R1 merely because the current research program is active.

This keeps the map from pre-adjudicating scholarship.

---

# 6. Static-site adjacency must be imported as legacy, not destroyed

The current `hexagon_canonical.json` and generated room pages already contain substantial adjacency arrays.

Implementation requirement:

```text
BEFORE REGENERATION:
copy current generated adjacency into
legacy_static_relations_2026_08_17
```

Then build the new current relation graph separately.

The old arrays are valuable because they record what the rapid consolidation pass inferred.

They are **not** the same thing as frozen Ark topology or current adjudicated structure.

---

# 7. Critical defect: Ichabod

The current static projection gives Ichabod generated links to Sigil and Assembly.

But the historical room rule is:

```text
degree = 0
isolated by design
```

Therefore:

```yaml
Ichabod -> Sigil:
  layer: R3
  authority_surface: static_projection_2026_08_17
  display: trace_only
  relation_type: generated_context_link

Ichabod -> Assembly:
  layer: R3
  authority_surface: static_projection_2026_08_17
  display: trace_only
  relation_type: generated_context_link
```

Do not render either as ordinary adjacency.

This should be an implementation test: if Ichabod shows a default line, the relation policy is broken.

---

# 8. Mandala rule

The historical Ark rule:

```text
Mandala receives from all
```

should not require drawing dozens of converging permanent lines.

Render one of:

```text
A. basin / contour language;
B. a subtle all-to-terminus background affordance;
C. lines only when Mandala is selected.
```

Recommended: **C**.

On Mandala selection, fade the map and show inbound traces from all eligible historical loci.

Default map remains uncluttered.

---

# 9. Field relations are not edges in the room sense

Fields interact with rooms by **coverage**, **source**, **gradient**, **suffusion**, or **circulation**.

Do not encode:

```text
Gravity Well adjacent_to r.05
```

merely because the old static site selected Semantic Economy as one relation.

Preferred field relations:

```text
suffuses
sources_from
attenuates_across
circulates_between
overlaps
curves_toward
```

These may be first-class typed relations, but their renderer is a field overlay rather than an ordinary line.

---

# 10. Cross-class relations are usually metadata, not separate visible edges

For:

```text
Ichabod ROOM → CHAMBER
Lagrange ROOM → CHAMBER
CTI_WOUND SPECIAL → VAULT
Infinite Bliss ROOM → VAULT proposal
```

prefer:

```text
historical_class
later_class
transition_status
transition_source
```

inside one locative object.

Only use a separate node if the later chamber/vault is demonstrably a distinct architectural object rather than a reclassification/depth-state.

Thousand Worlds remains the exception requiring visible caution because:

```text
historical r.22
later 14.CHAMBER.THOUSANDWORLDS
static 22.CH.THOUSANDWORLDS
```

have not yet been cleanly reconciled into one identity relation.

---

# 11. Relation UI behavior

Selecting a locus should reveal at most:

```text
3–7 high-priority relations
```

by default.

If more exist:

```text
SHOW ALL RELATIONS → TRACE
```

Suggested panel ordering:

```text
1. historical adjacency
2. current structural relations
3. strongest argumentative relations
4. fields affecting locus
5. class/address history
6. generated / legacy links [collapsed]
```

This keeps the flat map legible while preserving the archive's full graph.

---

# 12. Relation line grammar

Do not rely on color alone.

Suggested line semantics:

```text
R0 historical topology
  solid line

R1 current structural
  double / structural line

R2 argumentative
  thin line + relation label

R3 generated / legacy
  dotted line

provisional / queued
  dashed variation applied in addition to layer grammar

directed
  arrowhead

bidirectional
  no arrow or paired terminal marks

field
  no ordinary line; overlay / contour / plume grammar
```

---

# 13. Machine schema

The companion JSON defines:

```text
layer policy
visibility gates
historical R0 edge set
R1 structural whitelist
R2 initial argumentative whitelist
R3 import instructions
special topology constraints
renderer rules
```

Claude should consume that file as configuration rather than hand-coding relation visibility throughout the UI.

---

# 14. What Stage 08 deliberately does not do

It does not:

- exhaustively adjudicate the thousands of CNM relations;
- infer room relations from document co-occurrence;
- treat static adjacency as canon;
- promote live scholarship into architectural topology;
- decide all class-transition identity problems;
- enumerate every document-level relation.

Those are later L1/L2 relation patches.

---

## Stage 08 verdict

The first map now has a relation policy strong enough to remain readable while preserving the full graph underneath.

The governing relation rule is:

> **Topology orients. Structure explains. Argument appears on demand. Legacy remains inspectable.**

∮ = 1
