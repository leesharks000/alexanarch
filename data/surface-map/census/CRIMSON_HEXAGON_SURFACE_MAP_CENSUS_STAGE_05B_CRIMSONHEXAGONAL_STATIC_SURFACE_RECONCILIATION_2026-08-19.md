# CRIMSON HEXAGON SURFACE MAP — RECONCILIATION SURFACE AUDIT
## Stage 05B: `crimsonhexagonal.org` Static Projection, Existing Loci, and Link Bindings

**Date:** 2026-08-19  
**Granularity:** `L0/L1 RECONCILIATION SURFACE`  
**Status:** VERIFIED AGAINST CURRENT DEPLOYMENT SOURCE + LIVE ROOT/MANIFEST  
**Parent governance:** Stage 04A — Consolidation, Preservation, and Seating Principle  
**Parent seating pass:** Stage 05 — Post-Ark Consolidation and Seating

---

# 0. Why this surface matters

The current Surface Map census must treat `crimsonhexagonal.org` as an **additional reconciliation surface**.

It was built quickly and was not subjected to the same slow room-by-room canonical audit now underway. Therefore it is not authoritative merely because it is public and static.

But it is unusually valuable because it already contains:

```text
stable public room URLs
static HTML pages
per-room JSON projections
JSON-LD
room-to-room hyperlinks
navigation-layer pages
sitemap.xml
robots.txt
SPXI index
machine manifest
canonical JSON projection
```

The correct status is therefore:

> **PUBLIC PROJECTION / RECONCILIATION WITNESS — not canonical judge.**

It should be read alongside:

```text
frozen Ark / CNM / FNM states
+
Alexanarch sovereign records
+
current Surface Map census
+
crimsonhexagonal.org static projection
```

Where the static site agrees with stronger evidence, it gives us ready-made locative and link infrastructure. Where it disagrees, the disagreement itself is a useful record of the architecture's rapid consolidation state.

---

# PART I — WHAT IS ACTUALLY THERE

## 1. Live root and machine manifest

The live root currently presents `crimsonhexagonal.org` as the **Crimson Hexagonal Archive — Governed Operating Surface** and links directly to:

- `/manifest.json`
- `hexagon_canonical.json`
- Alexanarch
- Space Ark
- the wider network of project sites

The root currently claims:

```text
38 rooms
1,488 deposits
39 operators
6 typed relations
26 heteronyms
7 witnesses
```

The current machine manifest, however, reports a different snapshot:

```text
architecture.rooms: 29
architecture.documents: 455
architecture.relations: 20
counts.deposits: 1487
counts.rooms: 29
counts.as_of: 2026-08-16
```

**Reconciliation flag:** the public root and manifest are already on different count / classification surfaces.

This is not necessarily one simple arithmetic error. The static interface often uses **“rooms” as shorthand for all navigable spaces**, while the manifest's `rooms` count appears to refer to a narrower architectural array. But the mismatch must be made explicit rather than left implicit.

---

## 2. Static public tree

The deployment repository contains a genuine static public layer:

```text
/public/
  manifest.json
  sitemap.xml
  robots.txt
  spxi-index.jsonld
  /rooms/
  /navigation/
  /machine/
```

Each room-like route typically contains at least:

```text
index.html
index.json
```

This is excellent infrastructure for the future Surface Map because every locus can already have:

```text
human-readable static page
+
machine-readable static object
```

without requiring client-side JavaScript to expose the room identity.

---

## 3. Navigation documents already seated statically

The sitemap exposes:

```text
/navigation/
/navigation/registry/
/navigation/central-map/
/navigation/fractal-map/
/navigation/space-ark/
```

The navigation index correctly states the non-collapsible functional distinction:

```text
REGISTRY     stores
CENTRAL MAP  routes
FRACTAL MAP  resolves traversal
SPACE ARK    executes / governs
SITE         renders
```

It also explicitly states that the **current projection is generated, dated, and disposable**, while the historical specifications are not rewritten.

This is fully compatible with the Surface Map method adopted in Stages 03–05.

**Decision:** preserve these static navigation routes and bind the new flat map beside them rather than replacing them.

Recommended addition:

```text
/navigation/surface-map/
```

or simply:

```text
/map/
```

with explicit statement:

```text
Surface Map renders current locative projection.
It does not supersede CNM v7.0, FNM v7.0, or Space Ark 4.2.7.
```

---

# PART II — SITEMAP INVENTORY

## 4. Current static space routes

The current sitemap contains **38 room/space URLs** beneath `/rooms/`:

```text
airlock
assembly
borges
break-room
catullus
cti-wound
dove
eve
ezekiel
fbdp-source
frozen-sin-archive
fruiting-body-diffusion-plume
gravity-well
ichabod
infinite-bliss
internet
job-room
josephus-thesis
lagrange-observatory
macro-maquette
mandala
marx-room
maybe-space-baby-garden-lanes
migdal-room
moltbot-swarm
moving-statues-made-of-rubies-mint
portico
revelation
rosary-embassy
sappho
semantic-economy
sigil
space-ark
studio-for-patacinematics
thousand-worlds
underwater-construction-authority-of-dolphindiana
water-giraffe
whitman
```

This is already a useful discovery surface.

But `/rooms/` is presently an **umbrella namespace**, not a pure ROOM-class namespace. It includes:

- rooms;
- chambers;
- vaults;
- portals;
- fields;
- special structures.

That explains part of the `38 rooms` public-facing count.

**Surface Map consequence:** retain the URLs for stability, but expose `structure_type` visibly so `/rooms/` means “navigable spaces” rather than ontologically flattening everything into ROOM.

---

# PART III — DIRECT RECONCILIATION FINDINGS

## 5. Internet / FBDP Source collision is encoded in the static site

The current static projection says:

```text
26.ROOM.INTERNET
27.ROOM.FBDPSOURCE
```

Specifically:

```yaml
/rooms/internet/:
  hex_address: 26.ROOM.INTERNET
  id: r26

/rooms/fbdp-source/:
  hex_address: 27.ROOM.FBDPSOURCE
  id: r27
```

This preserves the older consolidation logic in which FBDP Source retained the v7 `r.27` address and Internet was moved into `r.26`.

Stage 05 adopted the opposite **current Surface Map seating** because the explicit developed Internet room specification has the stronger claim to `r.27`:

```text
CURRENT SURFACE:
r.26 FBDP Source   [relocated; historical alias r.27]
r.27 THE INTERNET  [developed explicit specification]
```

**Decision:** the site is a reconciliation witness here, not authority.

When regenerated, preserve both histories:

```yaml
FBDP_Source:
  historical_addresses:
    - r.27 [CNM v7 / old static projection]
  current_surface_seat: r.26

Internet:
  historical_static_address:
    - r.26 [2026-08-17 generated site]
  canonical_spec_address:
    - r.27
  current_surface_seat: r.27
```

---

## 6. The static site preserves the queued/confabulated consolidation set

The current static site contains pages for:

```text
24.ROOM.MIGDAL
29.ROOM.JOB
30.VLT.FROZENSIN
31.ROOM.JOSEPHUS
```

This is valuable because it preserves the consolidation state later explained by MANUS:

```text
model-confabulated inference
→ recognized as confabulation
→ deliberately preserved
→ queued architecture
```

These pages should **not be deleted**.

Their current addresses, however, are not all current Surface seats.

Stage 05 seating:

```text
r.24 Migdal          retain queued/adopted
r.31 Josephus        retain queued-room seat
r.32 Job             move from old r.29
33.VLT Frozen Sin    move from old 30.VLT
```

The old URLs should remain useful through alias / redirect behavior even after the locative metadata changes.

---

## 7. Two developed later rooms are missing from the static sitemap

The current sitemap does **not** expose dedicated static pages for:

```text
r.29 THE IMPLODING VELCRO NATIVITY
r.30 THE RUBY MOOT
```

Yet both have substantially stronger architectural standing than the queued Job / Frozen Sin objects currently occupying those number positions on the old static projection.

This is the clearest concrete reason to treat the site as needing reconciliation.

**Required correction:** add canonical static routes for both developed structures, without destroying the preserved Job / Frozen Sin routes.

Suggested slugs:

```text
/rooms/imploding-velcro-nativity/
/rooms/ruby-moot/
```

---

## 8. Catullus is present but materially under-described

The static Catullus JSON currently gives:

```text
23.ROOM.CATULLUS
physics: Lyric invective
documents: []
adjacent: []
```

That is far thinner than the explicit r.23 specification, which formalizes the Catullan Compression operator `σ_C` and its relation to Sappho.

**Decision:** static presence is confirmed, but Catullus requires a structural refresh before it is used as a constituent source for the flat map.

This is a good example of why the static pages are **bindings and clues**, not a substitute for the archive census.

---

## 9. Sappho proves the static-document architecture is useful — and currently unsafe as authority

The static Sappho page is already close to the desired implementation pattern:

```text
room identity
physics
operators
LP program
room-defining document
core documents
additional documents
adjacent rooms
HTML + JSON + JSON-LD
```

It currently seats **21 documents** and contains internal significant links to Borges, Semantic Economy, Marx, Sigil, Whitman, Break Room, Ezekiel, CTI_WOUND, and Space Ark.

That is exactly the kind of pre-existing binding infrastructure the Surface Map should reuse.

But the current auto-selection is not reliable enough to ratify:

- the page declares *For: Sappho, Mother of the Logos* as the **room-defining document**;
- its metadata surface gives creator `Nobody`;
- its excerpt itself says a DOI is pending;
- the current Stage 02 census identifies a much richer differentiated masonry of provenance anchor, creative anchor/version family, room construction, hardened reconstruction, philology core, execution/diagnostic, and errata.

**Decision:** preserve the static page, but replace flat document ranking with the Stage 02 role schema.

---

# PART IV — LINK-BINDING DEFECT

## 10. Static room pages still bind constituent documents primarily to Zenodo DOI URLs

This is the most important repair after locative reconciliation.

The Sappho static HTML links its documents directly as:

```text
https://doi.org/10.5281/zenodo....
```

But the current machine manifest explicitly states:

```text
Zenodo DOIs are HISTORICAL / SEVERED.
Do not resolve them as the retrieval path.
Resolve AXN at alexanarch.org.
```

Thus the site currently contains an internal contradiction:

```text
MANIFEST:
  DOI = historical identifier, not retrieval path

STATIC ROOM HTML:
  DOI = primary clickable document link
```

**Required binding inversion:** 

```text
PRIMARY CLICK:
  Alexanarch / AXN sovereign record

SECONDARY METADATA:
  historical DOI
```

For example:

```yaml
document:
  title: "ΦΑΙΝΕΤΑΙ ΜΟΙ..."
  axn: "AXN:..."
  canonical_url: "https://www.alexanarch.org/s/records/.../"
  historical_doi: "10.5281/zenodo...."
  historical_doi_status: SEVERED
```

The visible page can still show the DOI, but it should not send the reader into a known severed retrieval path.

---

# PART V — OTHER STALE STATIC SURFACES

## 11. SPXI index is a useful but stale snapshot

The current `spxi-index.jsonld` is dated:

```text
2026-04-28
```

and still describes the archive as:

```text
532+ DOI-anchored Zenodo deposits
```

while binding the old Zenodo community as a primary sameAs / kernel surface.

This is now historically useful but current-state stale.

**Decision:** preserve a versioned historical copy; generate a new SPXI site index from Alexanarch / AXN and the current Surface Map rather than editing the old semantic state without record.

---

## 12. Robots and sitemap are structurally good

The current robots file:

- allows ordinary crawling;
- names the sitemap;
- explicitly provides access for GPTBot, ChatGPT-User, Claude-Web, PerplexityBot, CCBot, and Google-Extended to the SPXI index;
- uses a crawl delay.

This is compatible with the goal of machine-readable static room surfaces.

**Decision:** retain crawlability architecture; regenerate targets and bindings rather than redesigning this layer from scratch.

---

# PART VI — RECONCILIATION AUTHORITY MODEL

## 13. Four surfaces, four roles

The project should now explicitly distinguish:

| Surface | Role | Authority |
|---|---|---|
| Ark / CNM / FNM frozen documents | historical state | authoritative for their dated state |
| Alexanarch / AXN | sovereign work-bearing record | primary current document authority |
| `crimsonhexagonal.org` static pages | public locative projection / link surface | reconciliation witness; regenerable |
| Surface Map census | current locative adjudication | working current projection until ratified |

The static site is especially valuable as **evidence of what the architecture thought it had seated on 2026-08-17**.

It should therefore never be silently overwritten without preserving that projection state.

---

# PART VII — STATIC PAGE SCHEMA AFTER RECONCILIATION

## 14. Recommended per-locus static object

```yaml
surface:
  slug: sappho
  url: https://crimsonhexagonal.org/rooms/sappho/
  projection_generated: YYYY-MM-DD

identity:
  current_surface_seat: r.01
  historical_addresses: []
  structure_type: ROOM
  standing: DEVELOPED

canonical_authority:
  primary_record: https://www.alexanarch.org/s/records/...
  axn: AXN:...
  historical_doi: 10.5281/zenodo....
  doi_status: SEVERED

architecture:
  physics: ...
  operators: [...]
  adjacent: [...]
  fields: [...]

constituent_families:
  anchors: [...]
  room_specs: [...]
  philology: [...]
  versions: [...]
  diagnostics: [...]
  errata: [...]

reconciliation:
  source_projection: 2026-08-17-static
  changed_since_projection: true
  notes: ...
```

This lets each static page function simultaneously as:

```text
human room page
machine endpoint
map node target
provenance surface
link hub
```

---

# PART VIII — LINK BINDING MODEL FOR THE FLAT MAP

## 15. The flat map should bind into the existing static layer

Each map polygon should link first to the static room page:

```text
/map/#r01
   ↓
/rooms/sappho/
```

The room page then fans out:

```text
ROOM PAGE
├── Alexanarch canonical anchor
├── constituent documents by role
├── historical DOI metadata
├── adjacent room static pages
├── CNM neighborhood
├── FNM traversal
├── Ark runtime
└── Surface Map coordinate
```

And every Alexanarch room-constituting record should eventually link back:

```text
Alexanarch document
   ↓
Crimson Hexagon locus
   ↓
Surface Map coordinate
```

This creates the desired bidirectional binding:

```text
MAP ↔ SPACE ↔ DOCUMENT ↔ ARCHIVE
```

rather than the current mostly one-way:

```text
SPACE → historical DOI
```

---

# PART IX — RECONCILIATION QUEUE

## 16. High-priority corrections to the static surface

### P0 — preserve current projection before editing

Archive / tag the current generated site state as:

```text
STATIC PROJECTION — 2026-08-17
```

The contradictions are historically informative and should not disappear.

### P1 — regenerate locative identities from Stage 05

Required changes include:

```text
Internet:    old static r.26 → current r.27
FBDP Source: old static r.27 → current r.26
Job:         old static r.29 → current r.32
Frozen Sin:  old static 30.VLT → current 33.VLT
```

with historical aliases preserved.

### P2 — add missing developed loci

```text
r.29 Imploding Velcro Nativity
r.30 Ruby Moot
```

### P3 — rebind documents to Alexanarch / AXN

Primary links become sovereign records. DOIs remain historical metadata.

### P4 — reconcile per-room document role assignments

Begin with Stage 02 Sappho; do not trust autogenerated “room-defining” selection.

### P5 — regenerate counts from one declared ontology

Distinguish:

```text
ROOM-class count
TOTAL NAVIGABLE SPACES
DEPOSITS
DOCUMENTS ROUTED INTO HEXAGON
```

Do not let all four collapse into “rooms” or “documents.”

### P6 — refresh machine surfaces together

Regenerate from one current projection:

```text
manifest.json
hexagon_canonical.json
rooms/*/index.json
rooms/*/index.html
rooms/index.html
navigation/current-projection pages
sitemap.xml
spxi-index.jsonld
```

### P7 — add Surface Map endpoint

```text
/map/
```

with the stable authored coordinates and interactive / clickable flat plane.

---

# PART X — VERIFICATION LIMIT

## 17. What was and was not directly verified

Verified in this pass:

- the live site root resolves and exposes the operating-surface page;
- the live `manifest.json` is retrievable;
- the public GitHub deployment source contains the static room / navigation tree;
- the current sitemap source enumerates 38 space routes;
- representative per-room static JSON and HTML were inspected directly;
- representative navigation HTML was inspected directly;
- robots and SPXI static machine files were inspected directly.

Search-engine queries in this pass did **not** surface the individual room URLs as indexed results. That is not proof that they are unindexed; it simply means this search pass did not retrieve them.

The static route tree is therefore verified as deployment source and sitemap intent. A later HTTP-by-HTTP availability sweep can be run separately if needed.

---

## Stage 05B verdict

`crimsonhexagonal.org` should be promoted in our methodology from “renderer we already know exists” to:

> **a dated, public, static reconciliation surface containing useful locative memory, machine-readable room projections, and a pre-existing hyperlink skeleton.**

It is **not clean enough to govern the current map**.

Its most valuable current functions are:

```text
1. preserve the 2026-08-17 consolidation state;
2. supply stable public slugs for spaces;
3. expose per-room HTML + JSON + JSON-LD;
4. supply internal adjacency links;
5. reveal where current canonical seating disagrees with old projection;
6. become the eventual binding layer between flat map and Alexanarch.
```

The governing integration rule is:

> **Do not rebuild the static web surface from nothing. Reconcile it, version it, and make its links sovereign.**

∮ = 1
