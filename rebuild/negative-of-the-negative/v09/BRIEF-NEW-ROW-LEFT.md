# Brief addendum: a new /non row for one entity of the maryleelabor left-and-labor census, under EA-NEGONT-02 v0.9 (#1690)

Read rebuild/negative-of-the-negative/v09/BRIEF-NEW-ROW-AGGREGATOR.md first and in full, then rebuild/negative-of-the-negative/v09/BRIEF-NEW-ROW-LABOR.md. The AGGREGATOR brief governs this row (rules, build steps, validation, final message, the shapes the page builder needs); the LABOR addendum's substitutions apply with the further substitutions below. Nearest exemplars: datasets/negative-of-the-negative/v2/rows/turkopticon.json, fairwork-cloudwork.json, data-workers-inquiry.json (rows built from the Labor Vector census on 2026-10-29). Repository /home/claude/alexanarch. Do not run git. Never use pkill. Use python3.12 for scripts. Create only new files at the paths named for YOUR row. Do not edit panel.json; the session seats the panel entry, mints the AXN and builds the pages.

## What these rows are
The maryleelabor left-and-labor census (maryleelabor.org/aggregators/, editor Lee Sharks, compiled 2026-10-31, anchored on #1725, *Ils ne sont pas marxistes*, AXN:0B50, data/texts/AXN-0B50-text.md) formalizes archives, editions, trackers and organizing records of left politics and labor as entities. Its organizing question: "Whose record does it keep, who holds it, and does it keep the losing side in a form that could be taken up later?" Its record fields keeps, holder and losing_side answer it; ml_reading is the archive's reading, ledgered as such. On 2026-10-31 (18:44 EDT) the operator ran each census name and the captures were seated in the Capture Registry the same evening. Operator ruling of 2026-10-29 stands for these rows: they are built "as against their wikipedia articles if they exist, their own pages, etc." Each row is type C unless the reading says otherwise.

## Substitutions
1. **The record.** For "the Labor Vector census record" read "the maryleelabor census record": /home/claude/fleet/maryleelabor-org/data/left-census/census.json, rows[slug == CENSUS] (fields, evidence {src, q}, record {keeps, holder, losing_side}, ml_reading, relations, negative_tags, unchecked; organizing_question, anchor, areas and schema_note at the top). The row files the census is built from: data/left-census/rows/CENSUS.py. Rendered: /home/claude/fleet/maryleelabor-org/aggregators/CENSUS/index.html, at https://www.maryleelabor.org/aggregators/CENSUS/.
2. **Ledger ids.** The record's claims are "ML-NN", dated 2026-10-31, editor Lee Sharks; locus = the field name; surface and record url https://www.maryleelabor.org/aggregators/CENSUS/. The census was composed in session on 2026-10-31 from sources saved that day; say so in the ledger's note for ML claims.
3. **Own pages already saved.** /home/claude/fleet/maryleelabor-org/data/left-census/sources/<CENSUS>--<id>.html.gz and .txt, with url, http, sha256 and fetch time in sources/manifest.json. Copy into your intake folder as Bn.html (gunzipped) and Bn.txt with the manifest's url, sha256 and read date. Sources the manifest records as refused or empty are unread; record them so.
4. **Fetching.** Fetch cards and Wikipedia with the census's agent string, "Mozilla/5.0 (compatible; maryleelabor-left-census)". A refusal (403, a bot check) is recorded as unreachable with what was tried; do not retry it with another agent string or by any other route around it.
5. **Surface.** Twelve captures are Google AI Overview, expanded. Three are Google AI Mode by the operator's report (the Marxists Internet Archive, the IISH, Labor Notes): write surface "Google AI Mode" for those and quote his note from the capture's head. Auth: signed out, incognito.
6. **The homonym row.** "MEGAdigital" composes Mega Digital JSC, a marketing agency in Vietnam; no card concerns the edition. For that row the field B is the edition's own pages and its Wikipedia article (the Marx-Engels-Gesamtausgabe; record what the name redirects to); the seven cards are recorded as the homonym's, with their sense, and the delta records the substitution. Homonyms stay distinct entities in the disambiguation.
7. **The archive's own row.** Labor Vector (laborvector.org) is the archive's own site (Lee Sharks; deposit #771 on its home page). Read the case for it as the archive's own entity (rows/spxi.json is the exemplar of that case; rows/the-final-time.json and rows/marx-as-identity.json are this day's archive-case rows). Its field holds the site's own card and the VectorStock homonym. The operator: "labor vector pulled up totally unrelated, so laborvector"; the spaced run is not pasted or seated, and is recorded in notes as the operator states it.
8. **The archive's left work.** Admission to A is by reading (§3.4). #1725 is the census's anchor and is read at the passages that name the entity or its kind (archives of the left, organs, holders, splits); other deposits enter only where they say something of the entity, by locus.
9. **Capture records.** The CAP- claims are the Capture Registry's findings and analysis for your capture (dated 2026-10-31), quoted verbatim from data/EA-WG-CAPTURES-01.json; surface url https://www.alexanarch.org/captures/<slug>/.
10. **Epoch** 2026-10-31; intake folder datasets/negative-of-the-negative/v2/intake/ROW-20261031/.

## The rows (the coordinator names ONE in your task)

| ROW | entity | CENSUS | capture slug (T) | AXN | surface |
|---|---|---|---|---|---|
| marxists-internet-archive | Marxists Internet Archive | marxists-internet-archive | marxists-internet-archive-aimode-20261031 | 0B65 | Google AI Mode |
| megadigital | MEGAdigital (the online MEGA, BBAW) | mega-digital | megadigital-aio-20261031 | 0B66 | Google AI Overview (expanded) |
| bannedthought | BannedThought.net | bannedthought | bannedthought-net-aio-20261031 | 0B5B | Google AI Overview (expanded) |
| erol | Encyclopedia of anti-Revisionism On-Line | erol | encyclopedia-of-anti-revisionism-on-line-aio-20261031 | 0B5D | Google AI Overview (expanded) |
| amiel-melburn-trust-archive | Amiel Melburn Trust Archive | banmarchive | amiel-melburn-trust-archive-aio-20261031 | 0B5A | Google AI Overview (expanded) |
| libcom-collections | libcom.org Collections | libcom-library | libcom-org-collections-aio-20261031 | 0B64 | Google AI Overview (expanded) |
| irish-left-archive | Irish Left Archive | irish-left-archive | irish-left-archive-aio-20261031 | 0B60 | Google AI Overview (expanded) |
| iish | International Institute of Social History | iish | international-institute-of-social-history-aimode-20261031 | 0B5F | Google AI Mode |
| reuther-library | Walter P. Reuther Library, Archives of Labor and Urban Affairs | reuther-library | walter-p-reuther-library-aio-20261031 | 0B68 | Google AI Overview (expanded) |
| labor-action-tracker | Labor Action Tracker | cornell-labor-action-tracker | labor-action-tracker-aio-20261031 | 0B61 | Google AI Overview (expanded) |
| crowd-counting-consortium | Crowd Counting Consortium | crowd-counting-consortium | crowd-counting-consortium-aio-20261031 | 0B5C | Google AI Overview (expanded) |
| unionstats | Union Membership and Coverage Database | unionstats | union-membership-and-coverage-database-aio-20261031 | 0B67 | Google AI Overview (expanded) |
| gnad | Global Nonviolent Action Database | gnad | global-nonviolent-action-database-aio-20261031 | 0B5E | Google AI Overview (expanded) |
| labor-notes | Labor Notes | labor-notes | labor-notes-aimode-20261031 | 0B62 | Google AI Mode |
| labor-vector | Labor Vector (laborvector.org) | labor-vector | laborvector-aio-20261031 | 0B63 | Google AI Overview (expanded) |

## Prose
No "not X but Y" or "X, not Y" constructions; no "rather than" or "instead of" outside quotations; third person; quotations verbatim; no hard line breaks inside strings; analyse mechanics, never motive.

## Final message
As the AGGREGATOR brief says, plus: the panel entry fields the session should seat (entity, name, type, homonym_names, homonym_basis, ontology {composition, E_F, rho}); any census field a fetched source contradicts or shows out of date; any capture finding your field ledger shows wrong (report; do not fix). Run python3.12 scripts/build_non.py --check only (it will report your row's pages missing until the session builds; that is expected).
