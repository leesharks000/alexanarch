# Counter Architecture

Static-snapshot pattern for view counts, replacing the live-fetch pattern that
was hitting GoatCounter's per-IP rate limits and displaying `—` under load.

## Two-file contract

**`data/view-counts.json`** — path-keyed count map for alexanarch.org's own
records and surfaces. Read by `assets/gc-enhance.js` in the browser; one fetch
per session, local lookup thereafter.

**`data/network-witness.json`** — network-total across all tracked sites, plus
per-site subtotals. Read by `assets/network-witness.js` on any site in the
network; one fetch, one number in the footer.

## Why static snapshot

The archive's own theory: witness accumulation is a historical record, not a
live gauge. A number that is 6 hours stale is not epistemically different from
a number that is 100 milliseconds stale for the purpose either surface serves.
What is different is that live-fetching from GoatCounter's public counter API
per record per session, across many concurrent visitors and many rendered
records per browse page, exceeds GoatCounter's rate limit and produces `—`
instead of a count. That is a worse failure mode than 6 hours of staleness.

The tracker script that fires on each pageview (the `count.js` ping that
increments GoatCounter's internal counter) is unchanged. GoatCounter keeps
accumulating the underlying data. Only the display path is replaced.

## Update cadence

A GitHub Action runs every 6 hours (`0 */6 * * *`) and on manual dispatch.
It reads GoatCounter's Stats Export API for each tracked site (via the
`GOATCOUNTER_API_KEY` repo secret), aggregates, and writes both files.
The Action commits under the TACHYON identity, and alexanarch's push-to-main
auto-deploy propagates the new snapshots to the Vercel edge.

## Failure modes

- **Snapshot fetch fails at runtime** → frontend displays em-dash for
  individual counts and falls back to any prior localStorage-cached snapshot
  for the network total. Never displays `0` under uncertainty.
- **Snapshot is missing a path** (record newer than the last snapshot run) →
  frontend displays em-dash. This will resolve at the next Action run.
- **GoatCounter API is unreachable during Action run** → Action fails
  loudly (exit non-zero); the previous snapshot remains in force. No stale
  data gets promoted; no zeroed data is written.
- **API key not configured** → Action refuses to run. It does not fall back
  to the public counter endpoint for the network-wide sweep because that
  would silently re-introduce the thundering-herd pattern at the aggregator
  layer.

## Schema (v1)

### `data/view-counts.json`

```json
{
  "schema_version": "v1",
  "generated_at": "2026-07-16T15:32:11Z",
  "generator": "goatcounter-snapshot workflow",
  "source": "https://alexanarch.goatcounter.com",
  "total": 1234567,
  "total_unique": 987654,
  "paths": {
    "/s/records/1086/": { "count": 42, "count_unique": 30 },
    "/s/records/1085/": { "count": 88, "count_unique": 55 }
  }
}
```

Path keys are exactly the URL paths GoatCounter observes (leading slash,
trailing slash preserved as tracked). O(1) lookup in the frontend.

### `data/network-witness.json`

```json
{
  "schema_version": "v1",
  "generated_at": "2026-07-16T15:32:11Z",
  "network_total": 1234567,
  "network_total_unique": 987654,
  "sites": {
    "alexanarch.org": {
      "total": 1234567,
      "total_unique": 987654,
      "source": "goatcounter",
      "goatcounter_host": "https://alexanarch.goatcounter.com",
      "as_of": "2026-07-16T15:32:11Z"
    }
  }
}
```

Extensible: additional sites are added by extending
`data/goatcounter-sites.json` (the workflow's input config). Each site declares
its GoatCounter host; the aggregator polls each and rolls up the network total.

## Extension: per-deposit witness counts

The framework theorizes each deposit's operative power scaling with witness
accumulated. The `view-counts.json` schema is already record-granular, so no
schema change is needed to surface per-deposit witness in ways the framework
can theorize against — e.g. a `witness_weighted_sort` on the browse page, or
a `high-witness deposits` roll-up. Those are downstream features on the same
data; the snapshot pipeline supports them without alteration.
