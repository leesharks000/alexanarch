# Atlas addendum v1.3 — the record API projection, and a near-miss the atlas caught

**2026-08-15.**

## New derived surface: api/records/<n>.json

One canonical store (`data/registry.json`), one new projection: a per-record
JSON file for every deposit, emitted by `scripts/build_record_api.py` and
registered as regenerate_surfaces surface `record-api`. The files are DERIVED
and never hand-edited — each is the registry entry verbatim plus computed URLs,
deterministic (registry bytes in → identical bytes out; the build's second run
writes zero files). A defect in an emitted file is a defect in the registry or
the script. Origin: an external machine-retrieval audit found "GET one record"
required downloading the whole registry; this closes that.

## The near-miss, recorded because the atlas is why it stayed a near-miss

The companion change — rel=alternate links and `version` inside the JSON-LD of
EXISTING record pages — would have required re-rendering pages through
`wire_deposit.regenerate_static_page`. Per this atlas's own rule ("REPAIR
touches a record that already exists" / "no gate catches did-not-look"), ONE
unchanged record (#1400) was re-rendered as a test before any batch. The diff
showed the renderer STRIPS post-render surgical layers it does not know about:
the superseded-record retirement apparatus (noindex, `axn:retired`, canonical
repointed to the terminal record, the cite-instead banner) and the richer
supersession banner. A bulk re-render would have un-retired every superseded
record in the archive in one commit. The test render was reverted from git and
the HTML change is DEFERRED until the post-render layer stack is either folded
into the renderer or applied by a re-application pass that runs after it.

Rule restated for the next instance: **record pages are not a pure projection.**
They are renderer output PLUS surgical layers applied by later scripts. Until
that is unified, any re-render of an existing record page destroys information.
