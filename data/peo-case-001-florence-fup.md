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
