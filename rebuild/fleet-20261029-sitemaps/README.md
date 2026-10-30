# Fleet sitemap pass, 2026-10-29

At the operator's request ("let's check all sitemaps across the fleet, make sure theyre up to date").

## What was checked

`sitemap_audit.py` read every surface's sitemap(s) at origin/main against the indexable HTML pages at origin/main (pages that declare noindex or redirect excluded), and fetched each live sitemap. Every live sitemap answered 200 and matched its repository. `audit-before.json` is the result. `stale2.py` separated lastmods overtaken by a commit to the page from those overtaken only by fleet-wide stamping.

## What was done (24 repositories, one commit and one bundle each; `bundles.tsv`)

`sitemap_regen.py` regenerates a sitemap from the tree in the fleet's own semantics (`scripts/url_grammar.py`: pages from the tree, lastmod from the page's last git commit, pages whose canonical points to another site unlisted), writing the sitemap only. It keeps the existing host, URL form and priorities, and the PDF and Markdown files the sitemap already listed. Not listed: pages that declare noindex or redirect, and housekeeping pages (privacy, subscribed, search, the Oracle's shared-thread template /t).

- Pages added: traininglayerliterature.org 74 (the originals cards and rooms added since 2026-10-23); provenanceerasure.org /module (the Self-Audit Module); themandalaoracle.com /routing and /terms; survivethedeletion /who/spellings. Every URL added answered 200 live.
- Entries removed: leesharks.com /atlas (a redirect) and /captures (canonical at alexanarch); machinemediation.org /captures (canonical at alexanarch) and /data/specs/EA-SPXI-ANALOG-01/v1.0/EA-SPXI-ANALOG-01-v1.0 (removed on 2026-10-22; the URL no longer resolves); godkinggoogle.com /captures (canonical at alexanarch); spxi.dev /analog/v1.0 (declares noindex).
- lastmod brought to each page's last commit everywhere else.
- operativesemiotics.org: sitemap-predictions.xml lastmods set from git (2026-10-22, when the prediction pages' text changed). `scripts/index/build_index.py` was not rerun: it stamps the run date into every page's dateModified and lastmod, a modification claimed whether or not one happened.

## Not changed, reported

- **Four per-site `scripts/build_sitemap.py` (axn-identifiers, godkinggoogle, restoredacademy, spxi-dev) are out of date.** They emit the apex host, trailing slashes the live sites redirect, and (restoredacademy) `restoredacademy.com`. The committed sitemaps use the current form; rerunning those scripts would regress them.
- **restoredacademy:** its pages, sitemap and robots.txt name `www.restoredacademy.com` as canonical; the fleet manifest binds `restoredacademy.org`. Both hosts answer 200. A binding question for the operator.
- **metadatapacket.dev:** `public/sitemap.xml` is written by `scripts/build_site.py` with each packet's own date as lastmod; complete (108 URLs, the 78 packet pages included). The root `sitemap.xml` (5 URLs) is not served (the site's output directory is `public/`).
- **secretbookofwalt.org, livingarchitecturelab.org:** framework builds (Vite, Astro); their live sitemaps (10, 17 URLs) were read; not regenerated here.
- **alexanarch.org:** the sitemap is `regenerate_surfaces.py`'s, by its own documented rules (records by their own dates; stubs and withdrawn records unlisted; static URLs without lastmod). Its omissions are by those rules, with these candidates for the operator's ruling: /book/ (the Book, reopened 2026-10-27), the dataset landing pages under /datasets/ (about twenty; only /datasets/ is listed), /axn/constitution, /s/fleet. Saved source pages (the /non intakes, /data/corpora) are not candidates.
