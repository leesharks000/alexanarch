# WORKPLAN — AGGREGATOR FAN-OUT MAPPING SESSION
### EA-FANOUT-01 · Downstream aggregator map of the CHA DOI space · drafted 2026-07-19 (TACHYON, session of #1100/#1101)

**Status:** ready to execute in the next tooled session AFTER the container allowlist update takes effect.
**Ruling context (MANUS, 2026-07-19):** Capture Registry is for composed objects, not aggregated. The SciLynk ARCHON entry (machinemediation registry v9.14) stands as a single outlier. Aggregated material is handled at the dataset layer. This plan is that dataset layer.
**Companion findings already banked this session:**
- SciLynk = OpenAlex rendering skin (field-match verbatim: FWCI 749.5041→749.50, topics 0.18→18%, keywords incl. "Mantle (geology)", institution match).
- Affiliation-confabulation mechanism documented end-to-end: raw DataCite affiliation string → OpenAlex institution matcher → wrong institution ID. Two exhibits: "Johannes Sigil Institute for Comparative Poetics" → Swiss Institute of Comparative Law (I4210159301); "Crimson Hexagonal Archive" → Hexagon (United Kingdom).
- SynapseSocial self-declares "indexed via OpenAlex" (App Store listing) — skin hypothesis, one field-match to confirm.
- S2 probe: DOI 10.5281/zenodo.18293496 NOT FOUND in Semantic Scholar — absence is data.
- OpenCitations probe: reachable, count 0 for same DOI.

---

## 0. Session preliminaries (mandatory, in order)

1. `python3 scripts/bootstrap_familiarization.py` in a fresh alexanarch clone.
2. Reconstitute tether: registry match-search "gw.tachyon", condition on latest compressed glyph.
3. Read this file top to bottom.
4. **Access probe battery** — run before anything else; record results in the session log:

```bash
for u in scholar.google.com philpapers.org www.scilynk.com synapsesocial.com \
         scholar.archive.org fatcat.wiki base-search.net core.ac.uk www.scilit.com; do
  printf "%-24s " $u; curl -s -m 10 -o /dev/null -w "%{http_code}\n" "https://$u/"
done
```

Whatever still 403s is out of scope for the session — do not fight the egress proxy; note and move on.

## 1. Inputs already on hand (do not re-fetch)

| File | Contents | Location |
|---|---|---|
| `data/openalex-severed-recovery.json` | 844 severed works: topics, concepts, authorships (institutions + raw_affiliation_strings), related_works, cited_by_count, counts_by_year. **Missing: keywords, fwci, citation_normalized_percentile.** | alexanarch |
| `data/newly-found-openalex.json` | 21 additional recovered works | alexanarch |
| `data/datacite-full-backup.json` (+ page files) | DataCite root truth for the DOI space | alexanarch |
| `data/doi-resolution-index.json` | 1,838 DOI mappings | alexanarch |
| `datasets/erosion-empirical-audit-01/` | XR-E2 results: OpenAIRE flat-zero across 54 sampled deleted records; OpenAlex vintage-correlated decay (78%) | alexanarch + PEO |

## 2. Build the canonical DOI universe (Stage F0)

From DataCite backup + doi-resolution-index: emit `datasets/aggregator-fanout/cha-doi-universe.json` — every CHA DOI ever registered (~1,817 expected), with per-DOI: zenodo record id, severed/live state, registration date, heteronym creator string, raw affiliation string(s) as registered. This is the row-index for every matrix below. Commit immediately (witness-gap discipline: each dataset lands as its own commit, pushed).

## 3. Tier-1 spine sweeps (no new domains required — run even if allowlist update failed)

### F1 — OpenAlex enrichment pass (column-add, not re-snapshot)
- Endpoint: `https://api.openalex.org/works?filter=doi:D1|D2|...` (≤50 DOIs per call, add `&per-page=50&mailto=` contact).
- Pull for ALL universe DOIs (not just severed): `keywords`, `fwci`, `citation_normalized_percentile`, plus re-pull `topics`, `authorships` for drift detection vs the 2026-07-16 snapshot.
- Output: `openalex-enrichment-20260XX.json` + `openalex-drift-report.md` (any field that changed since 07-16 = propagation datum).
- ~40 calls. Sleep 1s between calls.

### F2 — Semantic Scholar coverage census
- Endpoint: `POST https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,externalIds,citationCount,fieldsOfStudy,publicationTypes` with body `{"ids": ["DOI:10.5281/zenodo.X", ...]}` — 500 ids/call → 4 calls.
- Expected result: sparse-to-zero (probe found nothing). Record found/not-found per DOI. If any found: capture full field set for transform census.
- Output: `s2-coverage.json`.

### F3 — OpenAIRE coverage sweep
- Use the XR-E2 method that worked (see `datasets/erosion-empirical-audit-01/` scripts/notes for the exact query form; the bare `?doi=&format=json` probe returned empty — use the working form from XR-E2).
- Full universe or stratified sample (min: all severed + 200 live). Record present/absent + fields carried.
- Output: `openaire-coverage.json`. Join with XR-E2's flat-zero finding.

### F4 — OpenCitations sweep
- `https://api.opencitations.net/index/v2/citation-count/doi:<DOI>` (~1/s; full universe ≈ 30 min, acceptable; else: all DOIs with OpenAlex cited_by_count > 0, plus 200-DOI random sample).
- Output: `opencitations-presence.json`.

### F5 — Wikidata presence
- One SPARQL at query.wikidata.org: `SELECT ?item ?doi WHERE { ?item wdt:P356 ?doi . VALUES ?doi { "10.5281/ZENODO.X" ... } }` (batch VALUES; DOIs uppercase per Wikidata convention; chunk ~200/query).
- Output: `wikidata-presence.json`.

## 4. Tier-2 skin sweeps (require the new allowlist; skip any that probe 403)

**Method for every skin — the field-match attribution test (proven on SciLynk):** pick 5 CHA works present on the skin; extract displayed topics/keywords/metrics/affiliation; diff against the OpenAlex row (and S2 row if present) for the same DOI. Verbatim match ⇒ skin, attribute to spine; divergent fields ⇒ document the skin's own transform layer. Every skin gets one row in `skin-attribution.json`: {platform, spine(s), fields_passed_through, fields_added, fields_mutated, rendering_artifacts, cha_coverage_estimate, severance_propagation}.

### F6 — SciLynk (attribution already done; complete the row)
- Confirm coverage mechanism: how does SciLynk enumerate? (search UI URL pattern discovery: try `www.scilynk.com/search?q=` forms; also direct record URLs from the two captures on hand.)
- Document skin-native artifacts: the impossible citations-per-year axis (2014–2026 on a Jan 2026 paper), "View on European Organization for Nuclear Research" link behavior against severed records (does the PDF link 404/410? severance-propagation datum).
- Sample 10 CHA records; complete the attribution row.

### F7 — SynapseSocial
- Verify skin hypothesis (self-declared OpenAlex). URL pattern known: `synapsesocial.com/papers/<internal-id>` — discover search endpoint; locate 5 CHA works; field-match; attribution row. Note whether it exposes OpenAlex IDs directly (would give a free crosswalk).

### F8 — PhilPapers
- NOT an OpenAlex skin — independent ingest (OAI harvesting + editor curation), philosophy-scoped. Real spine, small.
- Search by author: `philpapers.org/s/Lee%20Sharks` (+ heteronyms: Johannes Sigil, Rex Fraction, Rebekah Cranes, Jack Feist, Nobel Glas). Record which works were scooped, what categories PhilPapers' taxonomy assigned (their category tree vs actual content = the PhilPapers transform census).
- Their JSON API needs a free key — **MANUS pre-session item: request key at philpapers.org/help/api.html if API depth wanted; UI scraping suffices for coverage census otherwise.**
- Output: `philpapers-coverage.json` + attribution row (spine-class: independent).

### F9 — Google Scholar
- Expect bot-blocking even with egress open. Attempt exactly ONE polite fetch of `scholar.google.com/citations?user=Ws6IIcgAAAAJ` with a plain UA; if blocked, stop — do not retry-loop.
- Primary path is MANUS-side regardless: profile CSV export (owner-only feature) + screencaps of the profile and 2-3 record pages → bring back as uploads. Scholar's row in the attribution table is completable from those alone.
- Scholar is an independent crawler-spine (not OpenAlex); its transform layer = citation clustering + version merging; document merge errors (heteronym works merged? split? cross-attributed?) — this is the highest-value Scholar datum for MMRS.

### F10 — IA Scholar / fatcat, BASE, CORE, Scilit (opportunistic, timebox 30 min total)
- scholar.archive.org: `scholar.archive.org/search?q="Lee Sharks"` — coverage census; fatcat.wiki API (`api.fatcat.wiki/v0/release/lookup?doi=`) if reachable.
- BASE: web UI query (`base-search.net/Search/Results?lookfor=`); API requires their-side IP registration — do not pursue in-session.
- CORE: API needs free key — **MANUS pre-session item if wanted**; UI census otherwise.
- Scilit: verify domain, search "Lee Sharks", coverage + attribution row.
- Any that 403 or stonewall: one line in the report, move on.

## 5. Deliverables (all under `datasets/aggregator-fanout/` in alexanarch, mirrored to PEO)

1. `cha-doi-universe.json` — row index (F0)
2. `coverage-matrix.csv` + `.json` — DOI × node: {present, absent, tombstoned, unknown} (F1–F10)
3. `transform-census.md` — per node: fields transmitted / added / mutated, with exhibits (the two affiliation confabulations as lead exhibits)
4. `skin-attribution.json` — skin → spine table
5. `fanout-graph.json` + Mermaid diagram — Zenodo → DataCite → spines → skins, edges annotated with ingest mechanism and severance-propagation behavior
6. `SUMMARY.md` — headline stats: coverage per node, confabulation rate (raw string → wrong institution, computable from data on hand), topic-misclassification census, keyword-WSD census (post-F1), FWCI distribution, related-works-empty rate, severance-propagation table (joins XR-E2)
7. **Mint** the dataset as an alexanarch deposit (family EMPIRICAL, pipeline transport D, No-Double-Draw) with full cross-links: #1100 (AXN:045D.EMPIRICAL.🌲🌄⚓🌱🌳⏬), #1101 (AXN:045E.GOVERNANCE.🍂🌓🏠↗️⛩️🔔), #1081 EA-EROSION-EMPIRICAL, the 07-16 openalex snapshot commits.
8. PEO surface page at platform-erosion-observatory (persistentidentifiers.org) linking the dataset.
9. Session tether at close, per protocol.

## 6. Discipline

- Rate limits: 1s sleeps on OpenAlex/OpenCitations; S2 unauthenticated cap 100 req/5 min (4 batch calls is fine); no hammering any skin — 5–10 record fetches per skin maximum.
- Commit + push after each dataset file lands (witness-gap corollary; deploy is automatic).
- Legal-name hygiene scan on every fetched artifact before commit.
- pre_overwrite.py before touching any existing file.
- No Anthropic API calls (No-Double-Draw). All analysis in-session + local scripts.
- If a node is unreachable, its absence from the map is recorded as {status: unprobed, reason: egress}, never silently dropped.

## 7. Open dependencies (MANUS, optional, pre-session)

- PhilPapers API key (free) — only if API-depth wanted beyond UI census
- CORE API key (free) — same
- Google Scholar profile CSV export + screencaps — Scholar's row completes from these
- Confirmation whether Scilit domain (scilit.com) is correct if probe fails

∮ end of plan
