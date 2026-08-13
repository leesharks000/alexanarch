# Data Atlas — current statement

**2026-08-13.** Twelve addenda accumulated (v0.1 → v1.2) with no consolidated
statement of main versus mirror. They are superseded as a *current* description
and retained as history: an addendum records what was true when it was written,
which is the point of keeping them.

## The capture registry across the fleet

| node | role | stores | renders | state |
|---|---|---|---|---|
| **alexanarch** | **canonical store + projection** | `rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json` — the only thing written to | `data/EA-WG-CAPTURES-01.json`, derived | v10.0 · 300 addresses · 395 observations |
| leesharks.com | renderer | **nothing** | fetches the projection at render | store retired 2026-08-13, bytes kept as `registry-v7_2-2026-06-15.json` |
| godkinggoogle.com | renderer | **nothing** | fetches the projection at render | store retired 2026-08-13, bytes kept as `registry-v9_4-2026-07-13.json` |
| machinemediation.org | **hosted mirror — role unresolved** | `data/registry.json`, a copy | its own pages | v9.55 · 288 · **stale, and declares the old source of truth** |

## What was wrong

Four nodes, four regimes, diverging by **169 records and two minor versions**
with nothing reporting it. Two of them held stores **nothing read**: both gallery
pages already fetched the live projection, so a human saw 300 records while a
crawler reading either repository found 131 or 202, at versions two months old,
with no statement that they were superseded.

That is the v9.6-fallback failure at fleet scale — **a stale representation
masquerading as a current measurement** — except no one was even reading it.

## The rule now

**One canonical store. One projection. Renderers render. Retired stores are
versioned, never deleted.**

> "retired stores keep their bytes as dated snapshots. we are versioning, not
> tombstoning." — MANUS, 2026-08-13

A retired store keeps a pointer to canonical, an **empty** entries array, and a
note saying why it is empty, with its last contents beside it under their own
version and date. A snapshot is a record of what a node published at a version.
It is not a measurement and must not be read as one.

## Intake

One contract, canonical at `rebuild/capture-registry/INTAKE-CONTRACT.md`. Nodes
**reference** it; none restates it. Minimum for a new capture: transcript, date,
surface, and both auth dimensions. Exact-string address match — **quotation marks
significant** — decides observation versus new record.

## Gates

`capture_intake.py` refuses an unreadable capture · `check_gallery_js.js`
executes the page scripts, because `node --check` is a syntax check and passed
for a day while the page was broken · `check_render_determinism.py` requires two
builds to be byte-identical · `check_fleet_sync.py` fails on any node declaring a
count or version divergent from canonical.

## Open

**machinemediation.org's role.** It is the only mirror that *hosts* rather than
fetches, and it is the MMRS editorial layer rather than a gallery. It currently
declares the superseded source of truth. Awaiting a ruling: renderer, or hosted
mirror with a sync step and a staleness banner. Untouched until then.

Freeze of all four nodes with counts, versions and SHA-256 before normalization:
`fleet-freeze-20260813.json`.
