# PEO CASE 001 — The Florence Severance (crui.unifi / Firenze University Press)
## Platform Erosion Observatory case file · opened 2026-07-20 · TACHYON, MANUS directing

## Finding (as of 2026-07-20 ~05:30Z)
14,283 DataCite DOIs under prefix 10.13128 — substantially the journal corpus of
Firenze University Press, registered since 2012 under DataCite client CRUI.UNIFI
(Università degli Studi di Firenze; domains unifi.it, fupress.net) — are currently:
1. **Unfindable in DataCite**: client count 14,283 → 0 between census epochs 2026-07-13
   and 2026-07-20; client record still ACTIVE; prefixes relationship EMPTIED; client
   record last updated **2026-07-16T07:23:35Z** (the event window, to the hour).
   Prefix record absent from DataCite; prefix census (any client): 0.
2. **Unregistered in Crossref**: prefix 10.13128 ownership now shows Crossref member
   21822 "Firenze University Press" — but works under the prefix: **0** (member's
   41,157 Crossref DOIs live under other prefixes; issuing ~4.6K/yr).
3. **Tombstoned at resolution**: sample DOI 10.13128/annali_dip_filos-8672
   (Annali del Dipartimento di Filosofia) resolves to
   https://journals.fupress.net/inactive-doi/ — "Inactive DOI … no longer active or
   could not be resolved." A publisher-side catch-all tombstone.

**Classification (provisional): registration-agency migration with abandoned identifier
layer.** Prefix ownership crossed DataCite→Crossref on ~2026-07-16; the registered corpus
did not cross with it. As of tonight the 14,283 have public machine-readable metadata in
NEITHER registration agency and resolve to a deletion notice. Every citation ever made to
a 10.13128 DOI currently dead-ends. Whether this is transitional breakage (re-registration
pending) or permanent abandonment (content re-minted under FUP's other prefix, legacy
identifiers orphaned) is the open question the observatory now tracks.

## Method note
Detected by tier-1 census delta (per-client findable counts) within 7 days of the event,
against +956,807 net registry growth; diagnosed to the hour from the client record's
updated timestamp; classified via prefix census, Crossref prefix/member records, and
handle-resolution probe. Public signals only; no privileged access.

## Significance
- Validates EA-EROSION-01 end-to-end: count-deltas detect; drill-down classifies.
- Demonstrates the CHA pattern at university-press scale and third-party distance:
  the PID layer failing silently while both registries' public surfaces show nothing
  amiss (an "active" client with zero DOIs; a prefix owner with zero works).
- The tombstone genre generalizes: "Inactive DOI" (FUP) = "Record no longer available"
  (Zenodo). Naming the genre is MMRS work.

## Recovery instrument
The DataCite Public Data File 2025 (harvest staged in data-rhizome/datacite/, next
session) predates the event and contains the complete DataCite metadata for all 14,283 —
titles, creators, URLs, relations. It is the BEFORE-snapshot and the recovery map:
old DOI → bibliographic identity → locate at journals.fupress.net → a Florence
DOI Resolution Index, built exactly as the CHA's own was built, for a third party.

## Tracking plan
Weekly: crui.unifi count; prefix 10.13128 findable (DataCite) and works (Crossref);
sample-DOI resolution class. Milestones: first Crossref registration under the prefix
(repair begins) / 90 days of zeros (abandonment hardens). All readings appended here.

## Open decisions (MANUS)
1. Responsible disclosure: courteous notification to FUP / CRUI / DataCite with findings
   and the offer of the recovery map (Ayanna Vox register; service posture).
2. Publication timing of the case study relative to disclosure.
3. Whether Florence recovery-index construction is in-scope for the harvest session.

## Reading log
- 2026-07-20T05:30Z — state as above (DataCite 0 / Crossref 0 / tombstone). Baseline.

## T0 enumeration (2026-07-22)

The 14,283-figure lost between the 2026-07-13 and 2026-07-20 census epochs is now
resolved to identifiers. The DataCite Public Data File 2025 (landing DOI
`10.14454/t5qb-d995`), frozen at `2026-01-06T20:11:59Z` — approximately six months
prior to the deletion event — was streamed and filtered on `client_id=crui.unifi`.
The extraction yields **14,284 unique DOIs**, all under prefix `10.13128`:

- 14,282 in `findable` state (one below the tier-1 census's 14,283 figure, consistent with a single state-transition between the T0 snapshot and the 2026-07-13 tier-1 census)
- 2 in `registered` state (a state class DataCite's client-count APIs generally do not surface, hence the +2 versus tier-1)

Update-time distribution places 12,308 DOIs — 86.2% of the corpus — in a four-month window
of mid-2020 (June through September), consistent with a single sustained
metadata refresh event. Secondary refresh points at 2021-03 (528) and
2023-03 (352). Long tail through August 2024. Top source months:
2020-06 (4,939), 2020-08 (3,242), 2020-07 (2,392), 2020-09 (1,735), 2021-03 (528).

The enumeration is deposited at `data/peo-case-001-florence-fup-enumeration.tsv`
alongside this case file, and structured facts at
`data/peo-case-001-florence-fup-t0-summary.json`. The enumeration is
redistributed from the DataCite Public Data File under its CC-BY license and
constitutes a recovery map for the 10.13128 corpus that currently resolves to
`https://journals.fupress.net/inactive-doi/`.

### Sample identifiers

For scale reference, three DOIs spanning the alphabetical range:

- `10.13128/1970-9501-2450`
- `10.13128/ijae-16987`
- `10.13128/techne-9971`

### Data-quality note

Two DOIs in the corpus (`10.13128/10.13128/ahs-23289`,
`10.13128/10.13128/rea-25108`) embed the `10.13128` prefix a second time inside
the suffix. They resolve as valid DataCite identifiers in the T0 snapshot and
are preserved unaltered in the enumeration; any re-registration pass should
inspect them individually.

### Extraction method note

The 2025 Public Data File is a 34.4 GB tar containing per-month
`dois/updated_YYYY-MM/YYYY-MM.csv.gz` members, each a compact projection of
`(doi, state, client_id, updated)` for DOIs whose last update fell in that
month. Streaming the tar via chunked HTTP Range requests to
`datafiles.datacite.org` — each chunk triggering a fresh S3 presigned URL
through the DataCite 302 (5-minute presigned TTL, ~180 chunks at 128 MB) —
avoids both bulk download (615 GB decompressed, 32 GB compressed) and the
single-connection expiration failure mode. Global filter yields per-client
enumerations without materializing the full 108,468,906-record file.

---

## Reconstruction

Session 2026-07-22, following the T0 enumeration and its deposit as AXN #1408, established that this abandoned corpus is over-preserved by other actors: 100% of a 50-DOI random sample indexed in OpenAlex, 100% Open Access, 99.986% with full DataCite JSON metadata already in the Public Data File 2025 tar, average 2.44 preservation mirrors per work distributed across DOAJ, Florence Research (`hdl.handle.net/2158/*`), and CINECA IRIS. The University of Florence preserved every one of its scholarly outputs; Firenze University Press walked away from the identifier layer that made the corpus discoverable *as a corpus*.

A three-tier identifier architecture and phased reconstruction plan is specified in [WORKPLAN.md](../datasets/peo-case-001-florence-fup/WORKPLAN.md). The plan introduces:

- **AXN_W** — sovereign persistent identifier for each work, replacing the abandoned `10.13128/*` DOI.
- **mAXN** — metadata-specific bridge identifier, carrying and versioning competing metadata propositions from different sources.
- **AXN_R** — identifier for reconstructions (SPXI-encoded regenerative packets), verifiable against source records.

The corpus becomes a large-N testbed for iterative reconstruction methodology. Egress additions requested for institutional-repository access are enumerated in the workplan §5.3.
