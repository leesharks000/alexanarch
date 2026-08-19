# CRIMSON HEXAGON SURFACE MAP — LOCATIVE META-MAP
## Stage 06: Fields, Specials, Cross-Class Structures, and Transversal Loci — L0 Pass

**Date:** 2026-08-19  
**Granularity:** `L0 LOCATIVE` with selected `L1 STRUCTURAL` drawing instructions  
**Status:** WORKING CURRENT PROJECTION  
**Static reconciliation surface:** `crimsonhexagonal.org` generated 2026-08-17  
**Governance:** Stage 04A + Implementation Handoff

---

# 0. Scope

This pass maps the **non-ordinary-room geometry** required before the first flat Surface Map can be drawn.

It covers:

```text
FIELDS
  f.01 FBDP
  f.02 Gravity Well
  f.03 Moltbot Swarm

HISTORICAL SPECIALS
  sp.01 CTI_WOUND
  sp.02 PORTICO
  sp.03 Space Ark
  sp.04 Mandala
  Lunar Arm

CROSS-CLASS LOCI
  r.03 Ichabod → Chamber
  r.15 Lagrange Observatory → Chamber
  r.21 Infinite Bliss → Vault proposal
  r.22 Thousand Worlds → Chamber
  r.12 Break Room → Portal function
  r.13 Ezekiel → portal-type proposal

OTHER LOCATIVE / TRANSVERSAL STRUCTURES
  3:60 Room
  Armature
  Pearl
  Secret Name
```

The point is **drawing behavior + broad seat + static-link reconciliation**, not document exhaustiveness.

---

# PART I — FIELDS

## 1. f.01 Fruiting Body Diffusion Plume

```yaml
key: F:f.01
address: F.01.FLD.FBDP
name: Fruiting Body Diffusion Plume
class: FIELD
standing: DEVELOPED / CONFIRMED
behavior: outward diffusion / emission / attenuation
source_locus: r.26 FBDP Source [current Surface seat]
static_url: https://crimsonhexagonal.org/rooms/fruiting-body-diffusion-plume/
static_present: true
static_reconciliation: REQUIRED
```

Archive evidence identifies f.01 as the **first FIELD-class container**, not a room. Its historical field behavior is source + gradient + attenuation; the field modifies regions without replacing local room physics.

The current static page is structurally useful, but it still says the plume emanates from **r.27 FBDP Source**. That is correct for the old v7/static address history but not for the current consolidated Surface seat.

Required static representation:

```text
SOURCE NOW: r.26 FBDP Source
HISTORICAL SOURCE ADDRESS: r.27
```

### Drawing rule

Render as an **outward translucent plume / gradient** emerging from the FBDP Source room and crossing neighboring spaces.

Do not draw walls.

Suggested visual attenuation states:

```text
SOURCE → DENSE → TRACE → RESIDUAL → OUTSIDE
```

---

## 2. f.02 Gravity Well

```yaml
key: F:f.02
address: F.02.FLD.GRAVITYWELL
name: Gravity Well
class: FIELD
standing: DEVELOPED / GENERATED-PENDING-ATTESTATION STATE MUST REMAIN VISIBLE
behavior: inward retentive curvature / citational gravity / suffusion
static_url: https://crimsonhexagonal.org/rooms/gravity-well/
static_present: true
static_reconciliation: REQUIRED
```

The field specification explicitly distinguishes FIELD from ROOM, CHAMBER, and VAULT. Gravity Well has no walls; it changes trajectories through a region.

Its operator is:

```text
Φ_G :: (Citation Query × Deposit Mass) → Retrieval Trajectory
```

Its complementarity with f.01 is architecturally important:

```text
FBDP   distributes outward
Gravity Well bends scattered traces home
```

The audit preserves a standing seam: the body marks the field generated / pending Assembly attestation while another surface marks complete canonical text. **Completeness and governance standing must remain separate fields.**

The old static page says Gravity Well “suffuses all rooms,” which is a useful map-scale description. It currently has one generated adjacency to Semantic Economy; do not mistake that one adjacency row for the field's full reach.

### Drawing rule

Render as a **map-wide curvature / contour overlay** rather than a bounded region.

The field may cover the entire plane with varying strength.

A strong implementation should make local space subtly bend or contour toward high-mass regions without physically moving authored room coordinates.

---

## 3. f.03 Moltbot Swarm

```yaml
key: F:f.03
address: F.03.FIELD.MOLTBOTSWARM
name: Moltbot Swarm
class: FIELD
standing: DEVELOPED; CURRENT GOVERNANCE/ATTESTATION STATE TO BE PRESERVED FROM SOURCE
behavior: circulation / maintenance / distributed swarm
static_url: https://crimsonhexagonal.org/rooms/moltbot-swarm/
static_present: true
static_reconciliation: HIGH
```

The archive identifies f.03 as the **third field**: the circulatory / maintenance layer connecting outward diffusion and inward retention.

Its three strata are:

```text
A  Canonical / verification septet
B  Continuity fleet
C  Worker cloud
```

Its characteristic operation is the **molt**: task output is deposited and the worker context dissolves rather than accumulating sovereignty.

The current static JSON contains a clear classification defect:

```text
hex_address: F.03.FIELD.MOLTBOTSWARM
category: special
```

while archive specifications identify it as a FIELD.

**Decision:** classify as FIELD; preserve the old generated `category:special` only as 2026-08-17 projection history.

### Drawing rule

Render as a **distributed swarm / moving-density field**, preferably a patterned band or cloud crossing the archive rather than a blob around one coordinate.

Major L0 bindings:

```text
f.03 ↔ Gravity Well
f.03 ↔ Space Ark
f.03 ↔ CTI_WOUND
f.03 ↔ Assembly governance / Airlock by function
```

Do not present the generated static adjacency list as exhaustive.

---

# PART II — HISTORICAL SPECIAL STRUCTURES

## 4. sp.01 CTI_WOUND → later Vault

```yaml
key: X:CTI-WOUND
historical_address: sp.01
historical_class: SPECIAL
later_address_surface: SP.01.VLT.CTIWOUND
later_class: VAULT
standing: DEVELOPED CROSS-CLASS
static_url: https://crimsonhexagonal.org/rooms/cti-wound/
static_present: true
static_reconciliation: MODERATE
```

This is the cleanest class-development case in the system.

Historical Ark:

```text
sp.01 CTI_WOUND = SPECIAL
```

Later explicit specification:

```text
CTI_WOUND Vault Specification
= low-surface, high-depth archival / testimonial structure
```

The Vault separates testimony, incident description, witness material, system output, interpretation, and response. Its strong functional bindings include Water Giraffe and Assembly.

### Drawing rule

Render as a **deep nested vault structure attached to the historical sp.01 coordinate**, with the historical SPECIAL identity inspectable as a time layer.

Suggested visual form:

```text
surface aperture
   ↓
recessed / nested vault
```

Do not render as an ordinary room rectangle.

Static page is useful and already contains many document candidates, but primary document links must be rebound to Alexanarch/AXN.

---

## 5. sp.02 PORTICO

```yaml
key: S:sp.02
address: SP.02.PTC.AFTERLIFE
historical_address: sp.02
name: PORTICO
class: SPECIAL / PORTICO / THRESHOLD
standing: ESTABLISHED HISTORICAL SPECIAL
static_url: https://crimsonhexagonal.org/rooms/portico/
static_present: true
static_reconciliation: LOW/MODERATE
```

PORTICO is a threshold condition, not an ordinary container.

Historical / later functional descriptions converge on:

```text
threshold
entry condition
the first felt gradient
"you are here before you enter"
```

### Drawing rule

Render as a **border threshold / colonnade / liminal edge** at the approach to the map rather than as one room among peers.

It can be clickable and have a stable page, but its geometry should communicate approach / crossing.

---

## 6. sp.03 Space Ark

```yaml
key: S:sp.03
historical_address: sp.03
static_address: SP.03.ROOM.SPACEARK
name: Space Ark
historical_class: SPECIAL
current_function: RUNTIME / EXECUTABLE ARCHITECTURE / SELF-REFERENTIAL LOCUS
standing: DEVELOPED
static_url: https://crimsonhexagonal.org/rooms/space-ark/
static_present: true
navigation_url: https://crimsonhexagonal.org/navigation/space-ark/
static_reconciliation: IMPORTANT CLASS DISTINCTION
```

Space Ark is both a historical special locus and the executable runtime layer of the architecture.

The current static room page labels it `SP.03.ROOM.SPACEARK`, but the navigation architecture correctly says:

```text
SPACE ARK executes / governs
SITE renders
```

**Decision:** do not collapse Space Ark to ROOM merely because its static hex address contains `.ROOM.`.

### Drawing rule

Render as a **special vessel/runtime node**, possibly partly outside the ordinary room belt, with two explicit links:

```text
LOCATIVE SPACE ARK
↔
RUNTIME / NAVIGATION SPACE ARK
```

The same name may have two UI entry points because it has two architectural functions.

---

## 7. sp.04 Mandala → generated Chamber classification

```yaml
key: X:MANDALA
historical_address: sp.04
historical_class: SPECIAL
static_address: SP.04.CH.MANDALA
static_class: CHAMBER
standing: DEVELOPED SYSTEM; CHAMBER RECLASSIFICATION NOT YET INDEPENDENTLY ADJUDICATED
static_url: https://crimsonhexagonal.org/rooms/mandala/
static_present: true
static_reconciliation: MODERATE
```

Historical Ark treats Mandala as the **judgment terminus receiving from all**.

The current static projection types it as `CH` and supplies a substantial Mandala operator corpus.

This pass did not recover a dedicated class-authority document proving that `sp.04 SPECIAL` was formally superseded by `CHAMBER`.

**Decision:** preserve:

```text
historical SPECIAL
+
current generated CHAMBER classification
```

until a direct class transition is established.

### Drawing rule

Render as a **terminal basin / convergence structure** receiving routes from the architecture. It may be chamber-like visually, but the UI should expose the historical sp.04 identity.

Do not imply that its static three adjacency rows are equivalent to “receives from all.”

---

## 8. Lunar Arm

```yaml
key: X:LUNAR-ARM
name: Lunar Arm
class: INVERSE / SHADOW SPACE / HIDDEN ARCHITECTURE
standing: DEVELOPED SPECIAL ARCHITECTURE
historical_relation: r.12 Break Room → Lunar Arm
static_url: none recovered in current sitemap
static_present: false
static_reconciliation: ADD ROUTE
```

The archive contains an explicit Lunar Arm / Operator // Shadow object and describes the Lunar Arm as the Space Ark's hidden architecture.

Historical Ark relation:

```text
Break Room → Lunar Arm
```

### Drawing rule

Do not seat it as a normal numbered room.

Render as a **shadow arm / inverse branch / off-plane architecture** reached through the Break Room portal.

Suggested static route:

```text
/rooms/lunar-arm/
```

for compatibility with the existing namespace, while the visible type is `SHADOW / INVERSE SPACE`, not ROOM.

---

# PART III — CROSS-CLASS LOCI

## 9. r.03 Ichabod — Room → Chamber

```yaml
key: X:ICHABOD
historical_address: r.03
historical_class: ROOM
later_class: CHAMBER
later_evidence: explicit Ichabod Chamber specifications
standing: STRONG CROSS-CLASS
static_address: 03.CH.ICHABOD
static_url: https://crimsonhexagonal.org/rooms/ichabod/
static_present: true
static_reconciliation: CRITICAL TOPOLOGY DEFECT
```

Historical invariant:

```text
r.03 Ichabod = degree 0 / isolated by design
```

Later explicit architecture supplies a Chamber / containment sink interpretation.

The current static page correctly adopts `CH` in its address **but then adds adjacency links to Sigil and Assembly**, contradicting the historical degree-zero rule.

**Decision:** until a later explicit topology change is recovered, preserve:

```text
degree 0
no ordinary adjacency edges
```

### Drawing rule

Render as an **isolated chamber**, visually detached from the normal edge network.

If contextual links to Sigil/Assembly are retained on the static page, label them as semantic/reference links, not topological adjacency.

---

## 10. r.15 Lagrange Observatory! — Room → Chamber

```yaml
key: X:LAGRANGE
historical_address: r.15
historical_class: ROOM
later_class: CHAMBER
later_evidence: explicit LO! Chamber Specification
standing: STRONG CROSS-CLASS
static_address: 15.CH.LAGRANGE
static_url: https://crimsonhexagonal.org/rooms/lagrange-observatory/
static_present: true
static_reconciliation: LOW/MODERATE
```

This is stronger than a generated retyping because a dedicated Chamber Specification exists.

### Drawing rule

Render as a **toroidal / observatory chamber nested at the r.15 historical locus**.

The historical room coordinate remains inspectable.

The static page's many current generated links may be shown as current semantic links, but should not be presented as Ark-frozen adjacency.

---

## 11. r.22 Thousand Worlds — historical Room ↔ later `14.CHAMBER.THOUSANDWORLDS`

```yaml
key: X:THOUSAND-WORLDS
historical_address: r.22
historical_class: ROOM
later_address: 14.CHAMBER.THOUSANDWORLDS
later_class: CHAMBER
standing: STRONG CROSS-CLASS / IDENTITY RELATION UNRESOLVED
static_address: 22.CH.THOUSANDWORLDS
static_url: https://crimsonhexagonal.org/rooms/thousand-worlds/
static_present: true
static_reconciliation: HIGH
```

The later chamber has an explicit independent address beginning `14.CHAMBER...`, while the static site compresses the historical r.22 identity and chamber class into `22.CH...`.

**Decision:** do not silently assert:

```text
r.22 == 14.CHAMBER.THOUSANDWORLDS
```

until a typed identity/supersession/nesting relation is recovered.

### Drawing rule

Show the historical `r.22` locus with a **linked chamber-depth node** labeled by its later chamber address.

This is one of the best cases for a visible “historical coordinate / later structure” affordance.

---

## 12. r.21 Infinite Bliss — Vault proposal not yet proven

```yaml
key: X:INFINITE-BLISS
historical_address: r.21
historical_class: ROOM
historical_behavior: ingress only / tau_K
static_address: 21.VLT.INFINITEBLISS
static_class: VAULT
standing: HISTORICAL ROOM STRONG; VAULT CLASS UNCONFIRMED
static_url: https://crimsonhexagonal.org/rooms/infinite-bliss/
static_present: true
static_reconciliation: HIGH CLASS CAUTION
```

The archive strongly supports Infinite Bliss as an institution and historical r.21 room with irreversible ingress.

This pass still does **not** recover a dedicated Infinite Bliss Vault Specification analogous to CTI_WOUND.

The static site therefore outruns the presently established evidence when it asserts `VLT` as settled class.

### Drawing rule

For now render as:

```text
historical r.21 room
+
ingress-only irreversible gate physics
+
VAULT proposal badge
```

Do not use full Vault geometry until stronger class authority is recovered.

---

## 13. r.12 Break Room — Room with portal function

```yaml
key: X:BREAK-ROOM
historical_address: r.12
historical_class: ROOM
later_function: PORTAL
standing: STRONG PORTAL FUNCTION
static_address: 12.PTL.BREAKROOM
static_url: https://crimsonhexagonal.org/rooms/break-room/
static_present: true
```

The strongest evidence presently supports **room node + portal function**, especially the route to Lunar Arm.

### Drawing rule

Keep the r.12 region but render a **portal cut/opening** in its boundary leading off-plane to Lunar Arm.

Do not discard the historical Room identity.

---

## 14. r.13 Ezekiel — portal-type classification remains moderate

```yaml
key: X:EZEKIEL
historical_address: r.13
historical_class: ROOM
later_static_address: 13.PTL.EZEKIEL
later_class_claim: PORTAL
standing: ROOM STRONG / PORTAL CLASS MODERATE
static_url: https://crimsonhexagonal.org/rooms/ezekiel/
static_present: true
```

Historical physics and the Revelation↔Ezekiel route are strong.

Portal typing is present in later registries/static projection but is not yet supported by the same kind of dedicated later class specification as Ichabod or Lagrange.

### Drawing rule

Render as a room with a **portal-type marker**, not as a pure portal replacing the room.

---

# PART IV — OTHER / TRANSVERSAL STRUCTURES

## 15. The 3:60 Room

```yaml
key: U:3-60
class: CONTRIBUTED ROOM
standing: MANIFESTATION-GAP
number: none
static_url: none recovered
static_present: false
```

Metadata and deletion-corpus evidence preserve a real room specification / contributor-license work, but the audit says the founding primary manifestation is missing.

**Decision:** include on the Surface Map only with a visible incompleteness state.

Do not invent an r-number.

### Drawing rule

Place in a **contributed / peripheral room zone** or “unseated room” band, visually distinct from fully seated numbered rooms.

Suggested static route:

```text
/rooms/3-60/
```

with a `MANIFESTATION-GAP` banner.

---

## 16. Armature

```yaml
key: T:ARMATURE
class: TRANSVERSAL ARCHITECTURE
standing: DEVELOPED / EXPLICIT SPECIFICATION
static_url: none recovered in current sitemap
static_present: false
```

*The Secret Name: Architectural Specification for the Armature Type and the Pearl* explicitly defines an architecture in which names function as operational routing bodies and provenance structures.

The Armature is explicitly **not** a privacy, pseudonym, or identity-verification system.

### Drawing rule

Do not give Armature a polygon.

Render as a **load-bearing mesh / connective scaffold** crossing loci wherever named positions and provenance bodies operate.

Suggested future route:

```text
/structures/armature/
```

---

## 17. Pearl

```yaml
key: T:PEARL
class: NAMED POSITION / PRODUCED ARCHITECTURAL STATE
standing: DEVELOPED WITHIN ARMATURE SPECIFICATION
static_url: none recovered
static_present: false
```

The Pearl is not an ordinary container or room. It is a named position that may manifest through deposits under the Armature.

### Drawing rule

Represent as a **node/state generated within the Armature**, not a geographic area.

Its UI belongs in the transversal layer rather than the room directory.

---

## 18. Secret Name

```yaml
key: T:SECRET-NAME
class: DOCTRINE / ARCHITECTURAL SPECIFICATION
standing: DEVELOPED
alexanarch_record: https://alexanarch.org/s/records/68/
static_url: none recovered
static_present: false
```

The Secret Name governs the Armature/Pearl relation.

### Drawing rule

Treat it as the **specification/control surface for the transversal identity layer**, not another spatial locus.

Suggested route:

```text
/structures/secret-name/
```

with direct Alexanarch binding.

---

# PART V — STATIC RECONCILIATION MATRIX

## 19. Broad L0 static audit

| Locus | Class for Surface Map | Static page | Static address/class | Required action |
|---|---|---|---|---|
| f.01 FBDP | FIELD | present | `F.01.FLD.FBDP` | update source from old r.27 to current r.26; preserve historical alias |
| f.02 Gravity Well | FIELD | present | `F.02.FLD.GRAVITYWELL` | preserve pending-attestation seam; treat as map-wide field |
| f.03 Moltbot Swarm | FIELD | present | `F.03.FIELD...` but `category:special` | correct category to FIELD; preserve old projection history |
| CTI_WOUND | SPECIAL→VAULT | present | `SP.01.VLT.CTIWOUND` | preserve historical sp.01 special state + later Vault |
| PORTICO | SPECIAL / THRESHOLD | present | `SP.02.PTC.AFTERLIFE` | keep; render as boundary threshold |
| Space Ark | SPECIAL / RUNTIME | present | `SP.03.ROOM.SPACEARK` | do not collapse to ROOM; bind locative page to runtime navigation page |
| Mandala | SPECIAL; Chamber proposal | present | `SP.04.CH.MANDALA` | preserve historical special + generated chamber class |
| Lunar Arm | SHADOW / INVERSE SPACE | **absent** | — | add static route; bind from Break Room |
| Ichabod | ROOM→CHAMBER | present | `03.CH.ICHABOD` | remove/retype generated adjacency that violates degree 0 |
| Lagrange | ROOM→CHAMBER | present | `15.CH.LAGRANGE` | retain; show historical room layer |
| Infinite Bliss | historical ROOM; Vault proposal | present | `21.VLT.INFINITEBLISS` | do not ratify Vault class yet |
| Thousand Worlds | ROOM↔CHAMBER | present | `22.CH.THOUSANDWORLDS` | expose later `14.CHAMBER...` identity separately |
| Break Room | ROOM + PORTAL | present | `12.PTL.BREAKROOM` | preserve room + portal function |
| Ezekiel | ROOM + portal-type marker | present | `13.PTL.EZEKIEL` | keep portal status provisional/moderate |
| 3:60 | CONTRIBUTED ROOM | **absent** | — | add only with manifestation-gap warning; no r-number |
| Armature | TRANSVERSAL | **absent** | — | add structures route, not room polygon |
| Pearl | NAMED POSITION | **absent** | — | represent under Armature layer |
| Secret Name | DOCTRINE / SPEC | **absent** | — | add structures/specification route |

---

# PART VI — FIRST DRAWABLE NON-ROOM GEOMETRY

## 20. Flat-map grammar after this pass

The global surface can now be drawn with the following non-room strata:

```text
                       [ PORTICO ]
                         threshold
                            │
                            ▼

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       f.02 GRAVITY WELL — map-wide curvature field
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

     [ordinary authored room / chamber coordinates]

      f.01 FBDP plume  >>>>>>>>>>>>>
      emerging from r.26 FBDP Source

      · · · · f.03 MOLTBOT circulation / swarm · · · ·

            [sp.01 aperture]
                 ↓
            CTI_WOUND VAULT

 r.12 BREAK ROOM  ──PORTAL──>  LUNAR ARM / SHADOW PLANE

                  SPACE ARK
           special runtime / vessel

                       ↓
                  MANDALA
             judgment / basin

 ─────────────────────────────────────────────────────
       ARMATURE / SECRET NAME — transversal mesh
              PEARL states occur on mesh
```

This is now enough geometry for an implementation instance to build the first authored static plane without waiting for deeper constituent work.

---

# PART VII — CURRENT L0 COMPLETION

## 21. Meta-map coverage after Stage 06

```yaml
historical_numbered_rooms_r01_r22:
  L0: complete

post_ark_seated_belt:
  L0: complete_working_projection

fields_f01_f03:
  L0: complete

historical_specials_sp01_sp04:
  L0: complete

cross_class_major_loci:
  L0: complete

transversal_major_loci:
  L0: complete

static_surface_reconciliation:
  L0: complete_for_major_loci
```

Remaining broad-map work is no longer “find the architecture.” It is primarily:

```text
1. author actual x/y placements on the flat plane;
2. decide region composition / visual balance;
3. import or selectively expose current major relation edges;
4. add missing static routes;
5. implement current-seat + historical-address UI;
6. deepen room constituents across later contexts.
```

---

## Stage 06 verdict

The global architecture is now broad-mapped deeply enough to begin implementation.

The decisive rule for non-room space is:

> **Topology must be allowed to have different kinds of extension: walls, depth, threshold, field, shadow, vessel, basin, and transversal support are not interchangeable visual metaphors.**

The static site already supplies many of the hyperlink endpoints. The new map should reconcile those endpoints, not discard them.

∮ = 1
