# Atlas v1.8 addendum — The Surface Map data seat — 2026-08-19

## What was added

A new canonical data seat: `data/surface-map/`. It holds the Crimson Hexagon Surface Map — `COORDINATES_v0.1.json` (39 loci on the authored 1600×1000 plane, hexagonal boundary, three fields, three transversal structures) and `RELATION_LAYERS_v0.1.json` (13 R0 default edges, R1/R2 whitelists, R3 trace-only including the two Ichabod legacy retypes), plus the eight-stage census derivation record under `census/` and the preserved pre-reconciliation static projection under `snapshots/static-projection-2026-08-17.tar.gz`.

## The dataflow

Authority stack: Ark / CNM / FNM > Alexanarch > Census > static site. The archive owns the data; crimsonhexagonal.org projects it. The projection surfaces are `surface_map.json`, `surface_relations.json`, and `surface_aliases.json` at the site root, rendered by `/map/`. The projection carries per-locus history (legacy axial coordinates from the 2026-08-17 canonical, class drift as separate fields, confabulation-origin flags) that derives from, and must remain reconcilable with, this seat.

## External dependency stated

Per the v1.7 rule — an atlas that maps only what a repository contains is not a map of the system — the crimsonhexagonal.org projection is an external dependency of this seat. Divergence between seat and projection is a defect of the projection, never grounds to amend the seat silently: the seat versions (`v0.1` in filename), and supersession is by new version, not edit.

## Governing deposit

AXN:0620.ARCHIVAL.🌗⚡📌🧭🌠💧 — *The Surface Map: Authored Flat Projection of the Crimson Hexagon v0.1* (deposit #1517).

## Rule carried

Locate first. Preserve history. Bind sovereignly. Draw sparsely. Deepen later.
