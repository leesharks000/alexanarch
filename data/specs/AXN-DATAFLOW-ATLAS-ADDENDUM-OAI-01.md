# Dataflow Atlas Addendum — the OAI-PMH Harvesting Surface

**Addendum to AXN Dataflow Atlas v0.2 (deposit #1097). Folds into v0.3 at next version-mint.**
Recorded 2026-07-30. Author: Lee Sharks. Substrate: AI-assisted (TACHYON, in-session).

## Why this is an Atlas matter, not a deploy note

The Atlas exists because a deposit can exist in the registry while being invisible on derived
discovery surfaces unless those surfaces are regenerated after registry changes. The OAI-PMH
endpoint is a new derived surface with exactly that property, and it introduces a new failure
mode: a record absent from `data/oai-index.json` is invisible to every aggregator that harvests
incrementally — which is all of them. That is a discovery-layer severance produced by the
archive against itself, and it belongs in the pathology register's frame of reference.

## New generative element

| Element | Path | Producer | Consumer |
|---|---|---|---|
| OAI index | `data/oai-index.json` | `scripts/build_oai_index.py` | `api/oai.js` |
| OAI endpoint | `/oai` (rewrite → `/api/oai`) | Vercel function | external harvesters |

Compiled rather than served from `data/registry.json` (≈12 MB) because a harvester walking the
corpus in 100-record pages would pay that load on every cold start. Index at recording: 1,427
records, 1.58 MB, 16 sets.

## Pipeline position

`stage_oai` runs immediately after `sitemap` in `scripts/deposit_pipeline.py`, on the same
principle: a record that never enters the discovery index is not published, only stored.

STAGE_ORDER: mint · validate · record · pdf · body-index · wiki · sitemap · **oai** ·
interlink · enrich · identity · commit · verify · announce

## Field derivation

`datestamp` derives from `date_modified` (see `scripts/record_modification.py`) falling back to
`date`. This is the first consumer of that field, and it is the one that makes the field
consequential: selective harvesting keys on datestamp, so a record whose modification was never
recorded will not be re-harvested after repair.

Sets are compiled on two axes — `family:*` from the AXN semantic family, `completeness:full` vs
`completeness:metadata-capture` from `body_status.class` — so the completeness distinction the
archive maintains internally is visible to harvesters rather than flattened at the boundary.

## Declared deletion policy

`deletedRecord: persistent`, the strongest of the three OAI-PMH options. The repository
undertakes to disseminate a `status="deleted"` header permanently rather than dropping a record
silently. The protocol has a field for the difference between *removed* and *never written*;
this archive declares the strong form of it in metadata every harvester reads at `Identify`.

## Known gaps

1. `oai_dc` only. No `datacite` or `oai_datacite` prefix yet; OpenAIRE prefers richer formats
   for full compliance and will accept `oai_dc` at basic level.
2. No `WITHDRAWN`-status records exist at recording, so the persistent-deletion undertaking is
   declared but not yet exercised. First exercise should be verified rather than assumed.
3. Registration with the OpenArchives repository list and OpenAIRE is pending; until then the
   endpoint is harvestable but not advertised.
