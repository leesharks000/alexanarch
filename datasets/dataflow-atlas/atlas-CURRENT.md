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

## Every producer bound — 2026-08-15

v1.5 bound the datasets and ten producers. There are **174 scripts**; the dependency graph
named **fourteen**. `binding-v2.0.json` binds all of them with writes, reads, docstring and
gate state — 42 write a known artifact and only **14 carry a `--check` gate**, so most
producers cannot be verified against their output.

**Contested artifacts:** `data/EA-WG-CAPTURES-01.json` has **15 producers** and
`data/registry.json` has **11**, against a DEPLOY-FLOW that names one deposit workflow. An
artifact with several writers has no ordering and no lock; whichever ran last wins and nothing
records which.

**A collision, reconciled:** two captures-to-heteronyms linkers existed over two stores, both
dated 2026-08-15 — name-match to `data/dodecad.json`, claim-match to the identity records. The
second was written without finding the first. Both are kept, neither summed: records carry
`captures_by_name` (floor) and `captures` (ceiling), and `dodecad.json` is marked a projection.

Rule added: **before writing a producer, search for the one that already exists.**

Full detail: `atlas-v1.6-addendum.md`.

## External dependencies, and every dataset described — 2026-08-15

**Twelve heteronym identity cards render on twelve different domains**, and the capture
registry displays in three galleries on three more. Those are external dependencies of the
datasets and nothing checked them. On first run
`scripts/check_external_surfaces.py` found **Sen Kuro's card returning 404** — reseated at
holographickernel.org by a ruling that reached the fleet's attribution map and never reached
`datasets/heteronyms/index.json`. A dataset pointing at a dead surface asserts something false,
and no internal gate can see it.

Also found: **`machinemediation.org/captures/` resolves and is not in the registry's declared
gallery list** — the venue whose founding dataset the registry *is*. And host drift between
v10.0 (`godkinggoogle.vercel.app`) and v11.4 (`www.godkinggoogle.com`).

`binding-v3.0.json` now describes **all eighteen datasets**, including the four not interlinked
— perseus-classical, gutenberg-classical, new-human-primary, deletion-conformance-fixture —
with an `interlinked` flag so absence is legible rather than inferred.

Rule added: **an atlas that maps only what a repository contains is not a map of the system.**

Full detail: `atlas-v1.7-addendum.md`.

## The Surface Map data seat — 2026-08-19

**A new canonical seat, `data/surface-map/`**, holds the Crimson Hexagon Surface Map:
39 loci with authored plane coordinates, the R0–R3 relation triage (X:ICHABOD at degree 0
by constraint), the eight-stage census derivation record, and the preserved 2026-08-17
static projection as tarball. crimsonhexagonal.org **projects** this seat (`/map/`,
`surface_map.json`, `surface_relations.json`) — an external dependency under the v1.7 rule.
Seat versions by filename; supersession is by new version, never silent edit.
Governing deposit: AXN:0620.ARCHIVAL.🌗⚡📌🧭🌠💧 (#1517).

Full detail: `atlas-v1.8-addendum.md`.

## Dataset navigation, audited as rendered — 2026-08-15

The tab and its subpages had accreted rather than been designed. **Two subpages 404'd**
(`/datasets/journals/`, `/datasets/mret/`), both linked from the tab the same day they were
added — a card was written and the page it pointed at was not. **Five title forms** were in use
across sixteen pages, including the path as title; **two pages had no back-link**, stranding
the reader; and **tombstone-mirror and zenodo-datacite-batch rendered under the same title**.

Seating apparatus now stated in `binding-v3.1.json` and enforced by
`scripts/check_dataset_navigation.py`: a directory must have an index or must not be linked;
the title is `<Name> — Datasets — Alexanarch` and must be unique; every page links back; every
page declares its canonical store; and navigation is **one level** — files linked directly,
because a dataset is a directory of files, not a site.

18 of 18 now present the same way.

## Render refusals are a guard, not a failure — 2026-08-15

Re-rendering all 1,486 record pages after the venue assignment, **210 refused**. Every refusal
was the guard working, and they are of **two different kinds that look alike**:

- **152 superseded or retired** — `axn:retired content="superseded"`, `noindex`, canonical
  pointing at the successor. Their metadata may name an old venue; that is harmless, because
  the page is canonicalised away and does not reach Scholar. Forcing a re-render to "fix" it
  would strip the tombstone.
- **58 lacuna stubs** — `axn:retired content="stub"`, which is the **lacuna apparatus, not
  retirement** (EA-LACUNA-PROTOCOL-01, #1087). These are **ACTIVE** in the registry and marked
  stub on the page, and **both are right: the work exists, its text does not.** Re-rendering
  would strip the mark and present a stub as a whole document.

I first read the second set as a registry/page contradiction. They are the opposite — two
systems agreeing with a guard between them. The meta name `axn:retired` carries both
retirement and lacuna, which is what made the misreading available.

A bulk re-render reporting "1,276 of 1,486" therefore looks like partial failure and is not.

## The binding that writes into other repositories — 2026-08-17

`scripts/build_network_block.py` is the only producer that writes outside alexanarch, and
until today it had **no atlas entry**. Four failures followed from that, three of them
invisible to every gate:

| | what | effect |
|---|---|---|
| NB-1 | reader took `set()` over a restructured manifest | would have emptied the block on every site |
| NB-2 | a domain in the manifest but absent from `GROUPS` | would have deleted a live domain from 27 sites |
| NB-3 | `var(--accent,#1a3a5c)` on sites that define no such variable | **shipped** — headings near-unreadable on four dark sites |
| NB-4 | non-greedy `.*?</div>` matched one domain, not the block | **shipped** — fourteen sites rendered the block twice |

**Why the gates missed NB-4.** Every check asked whether the markers were *present*. The
marker count was 1 on every site, so every check passed. **A duplicate that lives outside the
markers is invisible to any check that counts containers.** The operator had already said we
were doubling up; I verified one site, found one marker pair, and reported it clean.

**Rule.** A binding that writes into other repositories must be described here, and its checks
must test the **rendered result**, not the presence of its own markers.
`scripts/check_fleet_block.py` now counts rendered group headers per site and fails on any
count that is not exactly one. **Allied Sites is never counted** — it is curated, and no
generator writes it.

## Addendum — 2026-08-17: the capture registry's canonical store, ratified

The contested artifact is contested no longer. `data/EA-WG-CAPTURES-01.json`
is the canonical store for the capture registry, by MANUS ruling of this date,
on the finding that `rebuild/capture-registry/PIPELINE.md` step 3 had directed
seating into it since 2026-08-13 while the `_authority` block still named the
rebuild store — a constitution and an operating manual ratified the same day,
disagreeing for a month, with every session lawfully obeying the manual. The
rebuild store is sealed with honor at 305 addresses / 401 observations; its
provenance blocks remain authoritative for how pre-08-13 values were
recovered. Four declaration surfaces were amended in one motion (commit of
this date) so exactly one claim exists.

Binding note for the next revision: `datasets/capture-registry` canonical is
declared (`data/EA-WG-CAPTURES-01.json`); the CONTESTED flag on that artifact
resolves to "canonical, many committed producers, per PIPELINE.md."

Standing defect carried forward: `capture_intake.py` routes exact-match
against the sealed store and cannot see post-08-13 addresses — a duplicate
mint waiting to happen; repoint before next use. Three intake helpers
(`seat_source.py`, `cite_draft.py`, `extract_citations.py`) read the sealed
store and need the same verification.

The lesson is the atlas's own, third instance this week: a layer that looks
like data must say whether it is data — and when two documents both say, they
must say the same thing. The rule gains a corollary tonight: WHEN A
CONSTITUTION AND AN OPERATING MANUAL DISAGREE, EVERY SESSION IS LAWFUL AND
THE DATASET STILL SPLITS. Reconciliation is a repair with its own mode.

## Ledger line — 2026-08-18: the mirror-shape lesson, third instance

A capture-registry entry duplicates its primary observation's fields at the
top level, and the gallery renders the top; a seating that updates one side
of the mirror is half a seating. The who-said images sat correctly bound at
the observation level through two repairs while the card rendered nothing,
because entry.imgs stayed empty — caught by MANUS reading the rendered page,
not by any count. Same class as the attestation-fields flattening and the
projection/store split: WHEREVER A STRUCTURE DUPLICATES A VALUE, TWO TRUTHS
CAN DIVERGE SILENTLY, AND ONLY A GATE THAT COMPARES BOTH SIDES SEES IT.
Standing repair: an audit clause failing any entry whose entry-level imgs
disagree with its primary observation's imgs (and likewise for the other
mirrored fields).
