# Atlas v1.9 addendum — Browse sections beside the monolith — 2026-09-03

## What was added
`s/browse/family/<F>/`, `s/browse/month/YYYY-MM/`, `s/browse/venue/<slug>/` (+ three index pages): 103 paginated, self-canonical browse pages of ≤60 records with abstracts. Producer: `scripts/build_browse_sections.py`, invoked by `regenerate_surfaces.py` as surface `browse-sections`. URL list: `data/browse-sections-urls.json`, consumed by `regenerate_sitemap`.

## The dataflow
registry.json + datasets/journals/assignments.jsonl → build_browse_sections.py → s/browse/{family,month,venue}/**/index.html + data/browse-sections-urls.json → sitemap.xml.

## Rule carried
The monolith `s/browse/index.html` keeps its machine contract unchanged (numberOfItems, END-OF-BROWSE-ROWS, browse-index.json pointer; gates `check_surface_synchrony`, `capability_register`). The sections are an additional crawl surface for record-level discovery (ASSEMBLY-WORKPLAN-RECORD-VISIBILITY WS1), never a replacement. Gate: `build_browse_sections.py --check` — every ACTIVE deposit in exactly one family and one month section.

## Governing plan
ASSEMBLY-WORKPLAN-RECORD-VISIBILITY.md §2 WS1.
