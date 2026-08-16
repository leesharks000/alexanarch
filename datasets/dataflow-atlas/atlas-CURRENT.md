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

The path from screenshot to citable entry is `rebuild/capture-registry/PIPELINE.md`.
Both are now reachable from `AGENTS.md` — the STOP block and the catalog table —
because until 2026-08-13 they were referenced from nowhere and an instance
arriving at the front door could not find them.

## Two modes, and only one is dangerous — 2026-08-13

**INTAKE** adds an observation that did not exist. Forty captures were seated
across four sittings that day and intake broke nothing, twice.

**REPAIR** touches a record that already exists. Four repairs broke the dataset
the same day, and *every destructive act was a fix*: a projector that
reintroduced the doubling the projection had already resolved (60 surplus cards,
`"anti-suppression infrastructure"` rendering three times); a schema reseat in a
shape 406 seated observations do not use, blanking auth and PER on twenty cards;
six cards rendering blank titles because a display label sat in a key the gallery
does not read; and a correct citation note destroyed by a "correction" made
without searching the archive — twice, in both directions, over one SoundCloud
card.

None of these was a parsing failure. The doubling was stated plainly in the
commit that fixed it four rounds earlier. The blank titles came from a renderer
line already read. The schema divergence would have taken five records to see.
**No gate catches "did not look."**

What is in place now:

- **`reading_canon`** inside `data/EA-WG-CAPTURES-01.json` — six seated records,
  each teaching one thing a new instance otherwise gets wrong: the baseline shape
  and a collision held evenly; a longitudinal series across dates and auth
  states; a non-query address on a non-Google surface with a null citation count;
  absence as measurement; the collision register and its `via` mechanism; and a
  record that corrects itself.
- **The repair posture**, in PIPELINE.md and AGENTS.md §6: state the belief and
  its evidence, search the archive against it, one operation per commit, verify
  against the rendered artifact and state what was not verified.
- **One operation per commit** is the only property that actually saved the
  dataset that day — the revert was clean because intake and repair had not been
  mixed.

## The projector

**Still does not exist**, and its absence is a standing item rather than a
resolved one. Nothing in the repository derives `data/EA-WG-CAPTURES-01.json`
from the rebuild; nine scripts read it and none writes it. One was built on
2026-08-13, shipped three regressions, and was reverted with everything else.
Until it exists, the capture registry is maintained by seating directly into the
published projection, and the canonical store at
`rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json` is behind it.

**A carry-layer diff is the acceptance test when it is rebuilt** — regenerate the
published projection from canonical and compare only the fields that are carried
rather than computed. That test, run once, found that the previous builder had
been silently whitespace-collapsing transcripts at projection time: a cleaning
step inside a layer that must never clean, invisible to every other check.

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

## The heteronym substrate, and projections generally — 2026-08-15

A dataset can be a projection of another dataset, and a thin projection of a rich store is
indistinguishable from a poor store until you find the store. On 2026-08-15 an agent read
`datasets/heteronyms/heteronyms.jsonl`, found two heteronyms with empty roles, and recommended
against seating them as editors — while their full identity cards sat unread in
`datasets/heteronyms/records/`, carrying MANUS rulings no deposit contained.

**A layer that looks like data must say whether it is data.** `records/` is canonical;
`heteronyms.jsonl` is generated by `scripts/build_heteronym_index.py` and stamps `_derived_from`
on every row. Three tiers now hold archive-wide: deposits are **timestamps**, projections name
their **source**, canonical stores are declared **canonical**. And living does not mean correct —
the same day, the dataset had Spellings as active and the deposit had him dead, and the deposit
was right.

Captures are the one dataset to rule them all: the live registry is `data/EA-WG-CAPTURES-01.json`
(v11.4, 343). The identity cards were pinned at v9.39. Relinked, with
`scripts/link_heteronym_captures.py --check` as the gate.

Full detail: `atlas-v1.4-addendum.md`.

## The binding — 2026-08-15

The atlas is supposed to bind every connector, input, output and interlink to data. It named
**three datasets of eighteen**. Of those eighteen, 13 carry a manifest, **2 declare a canonical
store, and 1 names the script that rebuilds it** — and a dataset that says neither cannot be
checked for drift, which is the precondition for every silent failure recorded here.

`binding-v1.0.json` binds all eighteen: canonical store, producer, gate, and explicit
`binding_gaps` where missing. With **10 producers, 10 gates and 8 interlinks**, each interlink
declaring what it joins ON — because the join key is the claim. Three carry a must-not: a
mantle cannot be joined on a byline, the two capture routes must not be summed, and claim
counts are evidence of contact rather than of aboutness.

Rule added: **a dataset must declare on its own face what is canonical, what regenerates it,
and what gate detects its drift.** v1.4 said a layer must say whether it is data; this says it
must also say what keeps it true.

Full detail: `atlas-v1.5-addendum.md`.
