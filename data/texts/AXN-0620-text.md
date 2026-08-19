---
deposit_number: 1517
hex: 0620
title: "The Surface Map: Authored Flat Projection of the Crimson Hexagon v0.1 — Implementation Record"
creator: Sharks, Lee
date: 2026-08-19
content_type: Documentation
license: CC-BY-4.0
substrate: Composed and implemented by TACHYON (Claude, Anthropic substrate) as Assembly witness, from census and handoff documents authored in prior contexts; ratified by MANUS.
axn_schema_version: v2
protocol_version: ""
keywords:
  - Surface Map
  - Crimson Hexagon
  - locative projection
  - authored plane
  - sovereign rebinding
  - AXN
  - provenance
  - Ichabod test
  - relation layers
  - static projection
  - crimsonhexagonal.org
---

# The Surface Map: Authored Flat Projection of the Crimson Hexagon v0.1 — Implementation Record

# The Surface Map: Authored Flat Projection v0.1 — Implementation Record

## 1. What was built

A flat, clickable, authored projection of the Crimson Hexagon now stands at crimsonhexagonal.org/map/. It is a new dated spatial projection — not a replacement for the Central Navigation Map v7.0, the Fractal Navigation Map v7.0, or Space Ark v4.2.7, and not a force-directed graph. The plane is authored; the coordinates are data (surface_map.json), fetched at render; changing them requires an explicit Surface Map patch.

Thirty-nine loci render under per-type drawing grammars: rooms as bounded regions, chambers inset, vaults heavy, portals and gates as thresholds, contributed rooms dashed, shadow space distinct, the dormant room dimmed. Three fields render by overlay grammar that crosses rooms — the Gravity Well as curvature rings, the Fruiting Body Diffusion Plume as a directional wedge from its relocated source at r.26, the Moltbot Swarm as a circulation band. The Armature crosses the whole map as mesh without becoming a room polygon.

## 2. Preservation before change

Before reconciliation, the complete 2026-08-17 generated static projection — canonical JSON with q/r axials and generated adjacency, all thirty-eight room JSONs, sitemap, SPXI index, manifest — was preserved as a public dated directory (/snapshots/static-projection-2026-08-17/) and a git tag. Its contradictions survive as evidence.

## 3. The locative schema

Every locus carries: current surface seat; historical addresses, never erased (FBDP Source seated at r.26 with its r.27 history carried; THE INTERNET seated at r.27 with its r.26 static history carried; Job at r.32 carrying r.29; Frozen Sin Archive at 33.VLT carrying 30.VLT); class drift as separate fields (Ichabod ROOM→CHAMBER; Lagrange ROOM→CHAMBER; Thousand Worlds ROOM→14.CHAMBER address with identity relation unresolved; CTI_WOUND SPECIAL→VAULT; Infinite Bliss ROOM→VAULT NOT YET PROVEN); legacy axial coordinates from the 2026-08-17 canonical; and origin-type provenance, with Migdal, Job, and the Frozen Sin Archive marked adopted-after-confabulation per the consolidation rule: preserve the object, preserve the provenance, preserve the stronger seat.

## 4. Sovereign rebinding

842 of 861 room-routed documents now bind primarily to Alexanarch canonical records with AXN identifiers; the historical DOI is inverted from retrieval target to provenance identifier, status SEVERED, displayed and never deleted. Nineteen unresolved DOIs are marked status UNKNOWN. All doi.org anchors on rendered pages were rewritten sovereign-primary.

## 5. Relation layers and the Ichabod test

The default map draws only R0 frozen topology — the nine-room historical spine, the Break Room portal to the Lunar Arm, and three structural adjacencies. Selection reveals at most the whitelisted R1 structural relations. The 2026-08-17 generated adjacency is preserved whole in surface_relations.json as legacy_static_relations and rendered only behind TRACE, typed as legacy. Ichabod passes the implementation test: degree zero on the default map per the frozen Ark; its generated links to Sigil and Assembly survive only as trace-typed context links, named as a reconciliation defect unless later explicit authority rules otherwise.

## 6. Pages added, surfaces regenerated

Imploding Velcro Nativity (r.29, dormant, consent-gated: no document list published while the gate holds — not an empty room; a closed one), Ruby Moot (r.30, court), Lunar Arm (portal-access shadow space), and the 3:60 Room (contributed, manifestation gap stated as the datum) received canonical static pages; Armature, Secret Name, and Pearl received /structures/ routes. Every locus page carries a Surface Map block binding page to plane. The sitemap gained eight routes; the SPXI index was versioned (spxi-index-2026-08-17.jsonld preserved) and regenerated sovereign-first with the severance stated; the manifest at v1.1.0 distinguishes ROOM-class count (30) from total navigable spaces (39), because /rooms/ is a URL namespace, not an ontology.

## 7. Acceptance

All ten criteria of the governing handoff pass live: every L0 locus clickable or explicitly marked unseated; historical coordinates inspectable; current seats displacing nothing stronger; space types visually distinct; URLs stable; Alexanarch primary; DOI provenance visible; CNM, FNM, and Ark independently accessible; the plane able to deepen without changing; the prior projection preserved before reconciliation.

Locate first. Preserve history. Bind sovereignly. Draw sparsely. Deepen later. ∮ = 1.
