# Work plan — individual record visibility to search, retrieval, and composition

Opened 2026-09-03. Owner: Lee Sharks; execution: Claude (Anthropic) in session. Status lines are appended, never rewritten.

## 0. The finding this plan answers

Machine surface healthy (200, self-canonical, no x-robots, full text inline, all 1,576 in sitemap, robots open, 7–14 record→record links per page). Search layer failing at record granularity: four exact-title probes (#27 Mar, #311 Jan, #1038 Jul, #1546 Aug) returned **zero record pages**; what returned was the browse page (cached 2026-06-25, "1435 deposits"), the wiki index (cached, "1451 entries"), and third-party copies (Medium, academia.edu, Zenodo tombstones). Phenotype: collection-level legibility, record-level loss. Composition sits on that index and composes at collection granularity, citing copies.

Causes in play, by weight: (1) one ~940 KB browse page holding every record link, the only thing the index reliably keeps; (2) crawl staleness — index snapshots two months old; (3) the legacy `/records/?id=` canonical collapse (FIXED 2026-09-03, PRs #55/#56; ~900 pre-June records affected); (4) duplicate competitors older/stronger than the domain.

Current external guidance (checked 2026-09-03): Google AI Overviews/AI Mode eligibility = indexed + snippet-eligible + technical requirements + site included in the Search Console "Search generative AI" control; no special files (llms.txt not processed for AI features); internal linking named as a lever. ChatGPT search retrieves primarily from Bing's index (+OAI-SearchBot); IndexNow (already in the fan-out) is Bing's ingestion path.

## 1. Rules that keep this grounded

- **The atlas governs.** `s/browse/index.html` carries a machine contract (numberOfItems, END-OF-BROWSE-ROWS, browse-index.json pointer) and is read by `check_surface_synchrony` and `capability_register`. It is not modified. New surfaces are added beside it, each with a `--check` gate.
- **No new machine-facing files as remedies.** Nothing in current guidance rewards them; the remedies are pages, links, and freshness.
- **Freeze before repair, measure after.** Every change lands after the cohort baseline is recorded, and the cohort is re-probed on a cadence. No "wait and see."
- **One PR per workstream.** Record re-renders (1,576 pages) are their own PR, through `wire_deposit` and `check_rendered_record`.
- **Search Console truth beats inference.** Where Search Console can answer (selected canonical, indexing state, the generative-AI control), it is consulted before the next architectural change.

## 2. Workstreams

### WS0 — Baseline (before anything else)
- Record today's four title probes verbatim (done above) and the pre-fix legacy state (records/index.html at eb139eb0; live capture 200 + canonical=/records/).
- Build `scripts/probe_record_search.py`: 20-record cohort (5 pre-June with legacy URLs; 5 mid; 5 recent; 5 with strong external duplicates), exact-URL fetch + exact-title search via the same engine, which surface ranked, dated JSON to `data/probes/record-search/YYYY-MM-DD.json`. Run weekly by workflow.
- Done when: first baseline file committed. **Gate:** the probe is idempotent and never mutates expectations.

### WS1 — Paginated browse sections (new surface)
- `regenerate_surfaces.py` gains `browse-sections`: `/s/browse/family/<F>/`, `/s/browse/month/YYYY-MM/`, `/s/browse/venue/<slug>/` — each ≤ ~60 records with title, date, description, links to record, prev/next section, and back to `/s/browse/`. Self-canonical. In sitemap. Linked from the monolith header and from each record page ("in this family · this month · this venue").
- `--check` gate: every ACTIVE deposit appears in exactly one month page and one family page; counts match the registry head.
- Done when: live, gated, in the atlas binding (v3.3 addendum).

### WS2 — Citation-graph anchors on record pages
- `wire_deposit` renders "Cites" and "Cited by" as real anchors from `data/citation-graph.json` (10,474 edges), capped at 25 each with a link to the graph surface for more. Also "Series" prev/next where `version_series_id` exists.
- Re-render all records (retired pages excluded by the surgical-layer guard). One PR.
- Done when: `check_rendered_record` passes and median record→record links ≥ 20.

### WS3 — Search Console and Bing (Lee)
- Add `alexanarch.org` as a **Domain property** (DNS TXT at the registrar — one record, covers www/non-www/http/https). Submit `sitemap.xml` and `sitemap-axn.xml`. Confirm Settings → "Search generative AI" is on.
- URL-inspect #27, #311, #1038, #1546: read *Google-selected canonical* and the indexing verdict. Record the four answers in this file.
- Bing Webmaster Tools: verify the same domain; import from Search Console if offered; confirm IndexNow key is recognised.
- On the persistent indexing issues on the other properties: capture the exact verdict strings ("Discovered – currently not indexed", "Crawled – currently not indexed", "Duplicate, Google chose different canonical", "Alternate page with proper canonical") per property. Those strings name different causes and the plan for each differs; they go in §3 when known.

### WS4 — Duplicate policy
- Inventory the copies: GitHub raw `data/texts/*.md`, Medium reposts, academia.edu PDFs, Zenodo tombstones, HF dataset. Decide per class: keep (with canonical pointing home where the platform allows — Medium supports canonical on import), demote, or leave. GitHub raw is the strongest competitor and cannot carry a canonical; consider `X-Robots-Tag`-equivalent via a `robots.txt` on the pages branch or moving raw texts behind the site (they are already served at `/data/texts/`).
- Done when: a written policy per class and any platform-side canonicals set.

### WS5 — Re-probe and decide
- Two weeks after WS1+WS2 land: run the cohort; compare to baseline; read Search Console for the four. Decide whether the browse/link shape was the mechanism, and what remains.

## 3. Search Console verdicts (fill in)

| record | indexing verdict | Google-selected canonical | date |
|---|---|---|---|
| #27 | | | |
| #311 | | | |
| #1038 | | | |
| #1546 | | | |

## 4. Sequence

WS0 → WS3 (Lee, in parallel) → WS1 → WS2 → WS4 → WS5. WS3's answers can reorder WS1/WS2 if the selected canonical turns out to be a copy rather than the aggregate.

## 5. Status
- 2026-09-03 — plan opened; legacy canonical collapse fixed (#55/#56); baseline probes recorded in §0; atlas constraint on browse recorded in §1.
