# CRIMSON HEXAGON SURFACE MAP — LOCATIVE META-MAP
## Stage 07: Authored Flat Plane, Regional Composition, and First Coordinate Freeze

**Date:** 2026-08-19  
**Granularity:** `L0 LOCATIVE / IMPLEMENTATION GEOMETRY`  
**Status:** `v0.1 AUTHORIAL WORKING PROJECTION — pending visual ratification`  
**Companion machine file:** `CRIMSON_HEXAGON_SURFACE_MAP_COORDINATES_v0.1_2026-08-19.json`

---

# 0. Decision

The census has reached the point where the architecture can be given a **stable authored plane**.

This stage does not discover new rooms. It answers a different question:

> **Where do the already-recovered loci sit on the first flat public projection?**

The coordinates below are **rendering data**, not archival identifiers and not claims about historical adjacency.

The Surface Map therefore preserves three spatial systems independently:

```text
HISTORICAL LOCATIVE ADDRESS
    r.01, sp.01, 14.CHAMBER..., etc.

LEGACY GENERATED AXIAL COORDINATE
    q/r in the 2026-08-17 hexagon_canonical.json projection

CURRENT SURFACE COORDINATE
    authored x/y in this Stage 07 plane
```

Never overwrite one with another.

---

# 1. Canvas

Use an SVG-native coordinate plane:

```yaml
viewBox: "0 0 1600 1000"
```

Primary outer frame:

```text
                 (800,55)
                    /\
                   /  \
          (180,260)    (1420,260)
             |              |
             |              |
          (180,740)    (1420,740)
                   \  /
                    \/
                 (800,945)
```

This is a **frame**, not a rule that every structure must remain inside it.

Lunar Arm deliberately leaves the frame.

Fields may extend beyond it.

PORTICO sits at the entry lip.

Mandala sits at the lower terminus.

---

# 2. Legacy axial map is retained, not reused as authority

The current repository's generated `hexagon_canonical.json` already contains q/r axial placement data. For example, its opening records place Sappho at `(2,-1)`, Borges at `(1,-1)`, Ichabod at `(4,-3)`, Dove at `(-1,-1)`, Semantic Economy at `(-2,-1)`, and Marx at `(-2,1)`.

That projection is useful evidence of the quick 2026-08-17 layout.

It is **not** to be destroyed or silently promoted.

Implementation rule:

```yaml
legacy_axial_2026_08_17:
  q: ...
  r: ...

surface_2026_08_19:
  x: ...
  y: ...
```

Claude should copy the full old q/r array programmatically from the existing canonical JSON before regeneration.

---

# 3. Placement doctrine

The new plane optimizes for five things, in order:

```text
1. historical frozen topology remains visually legible;
2. explicit later bridges may be spatially near without becoming frozen edges;
3. cross-class depth is visible;
4. queued/adopted rooms fit without displacing developed loci;
5. large non-room structures have room to behave as fields, thresholds, shadows, vaults, and transversal systems.
```

No force-directed auto-layout.

No random jitter.

No build-to-build movement.

A coordinate moves only through a deliberate Surface Map patch.

---

# 4. The visual geography

The map is not divided into new canonical “districts.”

For implementation convenience only, coordinates occupy broad rendering regions:

```text
NW      lyric / source-near material
W       diffusion / gift / post-Ark accretion
C       materiality / operative / governance
E       witness / forensic / isolation
SW      generative / SWERVE extensions
SE      revelation / aorist / irreversible structures
N       threshold / ingress
S       runtime / judgment / late accretion
OFF-W   Lunar Arm shadow plane
```

These labels should **not** appear as archive ontology unless separately ratified.

---

# 5. Historical central spine

The frozen Ark route is made visually readable as a descending S-curve:

```text
Catullus      Sappho
                 \
                 Borges
                    \
             Semantic Economy — Marx
                              \
                              Sigil
                                  \
                                 Whitman
                                      \
                                  Water Giraffe
                                        |
                                     Assembly
                                      /
                               Revelation
                                    \
                                   Ezekiel
```

Only the frozen historical edges are drawn by default.

Catullus is spatially proximate to Sappho but does **not** become an Ark-frozen edge by placement alone.

---

# 6. Authored coordinate table — principal loci

| Locus | Current type | x | y | Placement logic |
|---|---:|---:|---:|---|
| r.01 Sappho | ROOM | 445 | 220 | historical spine; lyric anchor |
| r.02 Borges | ROOM | 590 | 300 | historical spine; between Sappho and Semantic Economy |
| r.03 Ichabod | CHAMBER | 1285 | 305 | deliberate isolation; degree zero |
| r.04 Dove | ROOM | 405 | 365 | near gift/extraction economy without claiming new frozen adjacency |
| r.05 Semantic Economy | ROOM | 560 | 405 | historical spine; material/economic gravity |
| r.06 Marx | ROOM | 720 | 390 | historical spine; formal materiality bridge |
| r.07 Revelation | ROOM | 940 | 680 | historical spine; terminal recursion zone |
| r.08 Sigil | ROOM | 825 | 495 | historical spine; operative center |
| r.09 Whitman | ROOM | 990 | 445 | historical spine; mantle/witness bridge |
| r.10 Water Giraffe | ROOM | 1130 | 505 | historical spine; fixpoint before Assembly |
| r.11 Assembly | ROOM | 1030 | 590 | historical spine + Airlock gate; governance center |
| r.12 Break Room | ROOM+PORTAL | 330 | 620 | western aperture to Lunar Arm |
| r.13 Ezekiel | ROOM | 1080 | 740 | historical Revelation↔Ezekiel endpoint |
| r.14 Studio for Patacinematics | ROOM | 300 | 760 | SWERVE route start |
| r.15 Lagrange Observatory! | CHAMBER | 490 | 665 | toroidal chamber between observation and generative belt |
| r.16 Maybe Space Baby Garden Lanes | ROOM | 470 | 780 | SWERVE route middle |
| r.17 Moving Statues Made of Rubies Mint | ROOM | 420 | 870 | later-built room; memographic hand cluster |
| r.18 Rosary Embassy | ROOM | 660 | 650 | extended belt with agent/institutional routing |
| r.19 Macro-Maquette | ROOM | 640 | 780 | SWERVE route terminus; module parent |
| r.20 Airlock | ROOM/GATE | 900 | 590 | historical gate directly beside Assembly |
| r.21 Infinite Bliss | ROOM | 1210 | 650 | ingress-only edge locus |
| r.22 Thousand Worlds | ROOM+CHAMBER-LINK | 1260 | 810 | aorist/dagger depth near Ezekiel |
| r.23 Catullus | ROOM | 300 | 180 | direct Sappho bridge; keep visually proximal |
| r.24 Migdal | ROOM | 255 | 330 | empty-space seating; preserve confabulated-origin provenance |
| r.25 Dolphindiana / Underwater Construction Authority | ROOM | 260 | 440 | post-Ark western generative edge |
| r.26 FBDP Source | ROOM/FIELD-SOURCE | 220 | 535 | western source aperture for outward plume |
| r.27 THE INTERNET | ROOM | 730 | 190 | retrieval/network region near Borges/Marx without displacing historical spine |
| r.28 Eve | ROOM | 800 | 720 | near Revelation but visibly provisional |
| r.29 Imploding Velcro Nativity | ROOM/HOSTED-COSMOLOGY | 600 | 890 | outer lower dormant locus |
| r.30 Ruby Moot | ROOM/COURT | 690 | 560 | semantic commons court between materiality and governance |
| r.31 Josephus Thesis | ROOM | 980 | 840 | current Logos/reception cluster near Revelation/Ezekiel |
| r.32 Job | ROOM | 1120 | 880 | displaced forward; near suffering/restitution cluster |
| 33.VLT Frozen Sin | VAULT | 1360 | 700 | forensic depth near CTI_WOUND without displacing Ruby Moot |
| 3:60 Room | CONTRIBUTED ROOM | 1300 | 400 | peripheral contributed locus; no invented r-number |
| sp.01 CTI_WOUND | VAULT | 1320 | 545 | recessed forensic depth; historical sp.01 aperture |
| sp.02 PORTICO | THRESHOLD | 800 | 92 | entry threshold at top edge |
| sp.03 Space Ark | SPECIAL/RUNTIME | 800 | 840 | runtime vessel distinct from room belt and from navigation page |
| sp.04 Mandala | SPECIAL | 800 | 930 | judgment basin / terminal convergence |
| Lunar Arm | SHADOW/INVERSE SPACE | 65 | 620 | off-plane branch reached through Break Room |

Exact width/height, standing, stable static slug, historical aliases, and class history are in the companion JSON.

---

# 7. Field geometry

## f.01 — Fruiting Body Diffusion Plume

Origin:

```text
r.26 FBDP Source = (220,535)
```

Render as a broad plume leaving the western side of the archive:

```yaml
direction: 195°
spread: 70°
radius: 520
attenuation:
  - SOURCE
  - DENSE
  - TRACE
  - RESIDUAL
  - OUTSIDE
```

The field must visibly escape the hexagonal frame.

The old static/v7 `r.27 FBDP Source` remains an inspectable historical address.

---

## f.02 — Gravity Well

Render across the whole plane.

Visual contour center:

```text
(790,510)
```

Suggested rings:

```text
210
390
610
850
```

This coordinate is explicitly **not the ontological source of Gravity Well**. The field's source is deposit mass; the render center is merely a stable way to show curvature.

Do not move rooms as the field animates or filters.

---

## f.03 — Moltbot Swarm

Render as a circulation band around and through the architecture rather than a point.

First authored path:

```text
(300,520)
→ (470,310)
→ (780,210)
→ (1110,330)
→ (1280,540)
→ (1110,760)
→ (790,840)
→ (500,735)
→ (300,520)
```

Three visible densities may correspond to:

```text
verification septet
continuity fleet
worker cloud
```

The current static `category:special` is a reconciliation defect; Surface type = FIELD.

---

# 8. Depth / boundary structures

## CTI_WOUND

Show the sp.01 surface aperture at `(1320,545)` with a **recessed Vault treatment**.

Historical toggle:

```text
sp.01 SPECIAL
```

Current depth:

```text
CTI_WOUND VAULT
```

Frozen Sin at `(1320,660)` should read as a later queued depth structure nearby without merging into CTI_WOUND.

---

## PORTICO

PORTICO is not a box in the north.

It should be drawn as the **entry lip / threshold** crossing the upper frame around `(800,92)`.

Clicking it may open its static page, but visually it is part of the boundary.

---

## Space Ark

Space Ark sits low and central at `(800,840)` as a **vessel/runtime structure**.

Its page must expose both:

```text
locative Space Ark
runtime/navigation Space Ark
```

Do not flatten it to ROOM.

---

## Mandala

Mandala sits at `(800,930)` as the lower **basin / judgment terminus**.

Historical rule:

```text
receives from all
```

Its current static `CH` classification remains a later projection, not silently proven supersession.

---

# 9. The Shadow cut

The Break Room at `(330,620)` contains a visible west-facing portal.

The route exits the principal plane to:

```text
LUNAR ARM = (65,620)
```

Lunar Arm is allowed to sit beyond the principal hexagon.

This is intentional: the map should make the phrase **hidden architecture** spatially true.

---

# 10. Ichabod

Ichabod is placed alone at `(1285,305)`.

Default topology:

```text
degree = 0
```

No ordinary line reaches it.

If the static site retains links to Sigil or Assembly for contextual value, those links must be visually and semantically typed as **reference/semantic links**, never ordinary adjacency.

This is a test case for the distinction:

```text
LINK ≠ TOPOLOGICAL EDGE
```

---

# 11. Post-Ark preservation geometry

Queued/adopted loci are deliberately placed in genuine open spaces rather than hidden:

```text
r.24 Migdal
r.31 Josephus
r.32 Job
33.VLT Frozen Sin
```

Their visual standing should be apparent through boundary treatment, opacity, or label marker.

Suggested states:

```text
DEVELOPED      solid boundary
PROVISIONAL    solid + small status notch
DORMANT        solid + muted fill / sleep marker
QUEUED         dashed boundary
MANIFEST-GAP   dotted boundary + warning marker
```

Do not use color as the only status carrier.

---

# 12. Transversal layer

Armature / Secret Name / Pearl do not receive geographic territories.

They occupy a separate visual layer:

```text
ARMATURE     load-bearing mesh across the whole plane
SECRET NAME  control/specification surface in legend or side rail
PEARL        named-position nodes appearing on the Armature
```

This layer should be toggleable.

It is drawn above fields and ordinary geometry but below interactive labels.

---

# 13. Default edge policy

Default map view shows only:

```text
FROZEN HISTORICAL ADJACENCY
+
EXPLICIT SPECIAL TOPOLOGY
```

Historical edge set:

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
```

Constraints:

```text
r.03 Ichabod: degree 0
r.21 Infinite Bliss: ingress only
sp.04 Mandala: historical receives-from-all rule
```

All later/current semantic relations appear on click, hover, filter, or relation-layer activation.

This prevents the map from becoming 2,851-edge spaghetti.

---

# 14. Static-link behavior

Every principal locus uses its existing stable static slug where available.

New routes to add include at least:

```text
/rooms/imploding-velcro-nativity/
/rooms/ruby-moot/
/rooms/lunar-arm/
/rooms/3-60/

/structures/armature/
/structures/secret-name/
```

Optional:

```text
/structures/pearl/
```

The map always clicks first to the static locus page.

The static locus page binds onward to Alexanarch/AXN as sovereign document retrieval.

---

# 15. Coordinate patch protocol

A coordinate change is a deliberate patch:

```yaml
surface_coordinate_patch:
  target: R:r.23
  from: [325,195]
  to: [350,180]
  reason: "visual overlap after Sappho constituent expansion"
  date: YYYY-MM-DD
```

Do not silently move a locus during code refactoring.

This allows the geography itself to become versioned evidence.

---

# 16. Implementation artifact

The companion JSON is intended to be directly consumed by Claude's implementation:

`CRIMSON_HEXAGON_SURFACE_MAP_COORDINATES_v0.1_2026-08-19.json`

It contains:

```text
canvas
hex frame
z-layers
locus x/y/w/h
current seats
historical aliases
static slugs
standing
field geometry
transversal geometry
frozen edges
special topology constraints
```

It also instructs the build to preserve the old q/r axial coordinates as:

```text
legacy_axial_2026_08_17
```

rather than deleting them.

---

## Stage 07 verdict

The first flat plane is now specified strongly enough to implement.

Its deepest design rule is:

> **Geography is a projection of architecture, not a substitute for it.**

The map can remain visually stable while every room continues to deepen beneath it.

∮ = 1
