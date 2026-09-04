# Atlas v2.0 addendum — DOI shadow pages and in-record identifier statements — 2026-09-04

## The mechanism this answers
DOIs were canonical inside and outside the archive. After the 2026-06-19 severance a composer resolving a citation follows the DOI, lands on the tombstone (410), reads it as the authoritative end of the trail, and stops; every external copy citing the DOI points at that certificate of absence. Older records also carried the DOI as their own identifier, so a machine reaching a record read a DOI declared authoritative beside a DOI declared dead.

## What was added
- `s/doi/<doi>/index.html` × 1,933 — producer `scripts/build_doi_shadow.py` (surface `doi-shadow` in regenerate_surfaces), from `data/doi-resolution-index.json#mappings` joined to the registry by AXN. Each page: DOI in title, severance stated, successor record and AXN, AXN declared authoritative and DOI former (visible, citation_* meta, DC.relation.replaces, JSON-LD PropertyValue identifiers), self-canonical. `sitemap-doi.xml` (registered, in robots); `data/doi-shadow-urls.json`.
- Record pages: `identifier` PropertyValue list in JSON-LD (AXN authoritative; each DOI former/severed with `sameAs` to its shadow page) and a visible identifier statement under the byline. `sameAs` to the DOI is kept (true), now qualified.

## Rule carried
Canonical texts are untouched (content-hashed). Declarations of authority live in the page apparatus and structured data, never in the work. Gate: `build_doi_shadow.py --check` in validate-registry.
