# Dataflow Atlas — v1.2 addendum (2026-08-11)

## The capture registry acquires a canonical intake flow, and the transcript becomes a join key

Prior head: `atlas-v1.1-addendum.md` (2026-08-11, same tether).
Deposited under tether **#1448 · AXN:05D9.ARCHIVAL.🍄🔎💡🝊🔙🏗️**.

The atlas has mapped the capture registry as a *dataset* since Session 1. It has never
mapped the registry's **intake** — the path a screenshot travels from Lee's phone to a
cited, linked, addressed card on `captures/index.html`. That path had been performed
ad hoc, differently each batch. As of registry v9.40 (285 entries, 19 added this
session) it is a fixed seven-step pipeline, and the atlas records it here because a flow
that runs the same way every time is the only kind the map can hold.

---

## §1 · NEW FLOW — the seven-step capture intake

Adopted this session as the single path. Order is load-bearing: each step reads what the
prior step wrote.

| # | instrument | reads | writes |
|---|---|---|---|
| 1 | `scripts/build_capture_links.py` | `data/EA-WG-CAPTURES-01.json` | per-gallery link maps (3 galleries + canonical) |
| 2 | `scripts/build_capture_gallery.py` | registry + link maps | `captures/index.html` (285 anchored cards) |
| 3 | `scripts/audit_capture_citability.py` | gallery + registry | assertion only — **every capture is citable** or the run fails |
| 4 | `scripts/audit_orphan_captures.py` | mirror-host image dirs + registry | orphan report (assertion, not mutation) |
| 5 | `scripts/resolve_capture_links.py` | registry + `data/registry.json` full bodies | `data/capture-deposit-links.json` |
| 6 | `scripts/build_semantic_addresses.py` | registry + links | `data/semantic-addresses.json` |
| 7 | `scripts/regenerate_surfaces.py --only dynamic-counts`, then `scripts/sync_capture_dataset.py` | everything above | fleet surfaces; `datasets/capture-registry/` (published dataset + manifest from disk) |

Two placements were decided, not inherited: **the resolver is step 5** (links must exist
before addresses are computed over them) and **dataset sync is last** (the published copy
is a projection of a finished state, never a working file). The audits at 3 and 4 are
gates — they mutate nothing, and a failure stops the run before anything propagates.

**Direction of flow:** strictly downstream from `data/EA-WG-CAPTURES-01.json`. Nothing
in the pipeline writes back to the registry. Intake (the composition of entries) is
upstream of step 1 and remains a read-and-decide act, not an instrument.

---

## §2 · RECORD STANDARD — what a capture entry now carries

Formalized this batch and applied to all 19 new entries; the standard is additive, so the
266 prior entries remain valid without it.

- **`meta` object** — capture circumstances as data: device, surface, auth state, query
  mode (`exact:true` for quoted queries), locale.
- **`transcript`** — the full text of the retrieval-layer output as copied, not
  paraphrased. This field is the substrate of §4 below.
- **`overview_at_capture` + `divergence`** — present only on **regeneration pairs**
  (§3). The first holds the AI Overview as screenshotted; the second states, in the
  archive's own words, how the transcript-copy differs from the screenshot.
- **`d` longitudinal linkage** — recaptures **never supersede**. A recapture is a new
  entry whose description names its priors in backticks
  (e.g. `water-giraffe-probe-self-report-20260809`). Time-series live in prose linkage,
  not in versioned overwrites; the earlier observation remains a first-class record.

The supersession rule is the custody-relevant part. A capture is an observation of a
volatile layer at a moment; replacing it would convert an instrument into a mirror of
whatever the layer says today — the exact failure the registry exists to measure.

---

## §3 · NEW SUBTYPE — the regeneration pair

Observed at least six times this batch: the retrieval layer regenerated its output
between the screenshot and the transcript copy, sometimes within one minute. The
`feist-function-alexanarch` / `-regen` pair is the type specimen — three distinct,
individually correct compositions of the same material inside ~15 minutes.

The subtype exists because the divergence **is the datum**. A single-state capture
records what the layer said; a regeneration pair records that the layer's statement is a
draw from a distribution, and bounds the distribution with two samples. The
`divergence` field keeps the comparison inside the record instead of leaving it to a
reader with two tabs open.

---

## §4 · FINDING — the transcript is a join key

The reason `transcript` is worth its bytes: **hard links now come out of it.** The
resolver's top tiers match AXN glyph-hexes, DOIs, and series identifiers found *inside
the captured text*. This batch, the SERP itself displayed the archive's own identifiers —
`revelationfirst-org` carried AXN:0349's six-glyph string in a result title and
hard-joined to deposit #202; `heteronym-dodecad` carried a Zenodo DOI and hard-joined
through it; `platform-erosion-observatory` and `axn-distributed-identifiers` joined on
glyph-hex.

Before transcripts were stored, these joins were impossible — a screenshot's identifier
content was locked in pixels. Glyph survival in retrieval surfaces, previously a
qualitative observation, is now a **mechanical link between a capture and the deposit the
layer was quoting**. 153 of 285 captures are linked (424 edges); the 132 unresolved are
unresolved *by design* — the ladder requires the query string to substring-match archive
text under strict fan-out caps, and coined-term queries exceed the body-tier caps.
Conservatism is the feature: a missing link is recoverable, a wrong one poisons the
graph.

---

## §5 · SURFACE FEATURE — the expandable transcript

`captures/index.html` cards now carry a statically pre-rendered
`<details class="cap-transcript">` block: the overview-as-screenshotted (labeled), the
divergence note where one exists, and the full transcript (`itemprop="text"`). Rendered
at build time by `transcript_block()` in the gallery builder — no client fetch, no
script dependency; filtering hides whole cards, so the block survives every UI state.
This closes a P-31 exposure preemptively: the transcript lives in the dataset, and the
surface provably renders what the dataset holds.

---

## §6 · MANIFEST CORRECTION

The dataset manifest had drifted (P-28 class): it declared v0.7 / 13 files while the
directory held addenda through v1.1. Regenerated this session from disk — every file
present is registered with measured size and SHA-256, version advanced to v1.2. The
correction is noted here so the gap in the manifest's own history is legible rather than
silent.

∮ = 1
