# The census of Classical Philology (EA-CORPORA-40/16)

The census of Classical Philology (ISSN 0009-837X), pulled from Crossref on 16 November 2026: 11,206 records, 1906–2026. Crossref holds no abstracts for the journal. Reach coding is therefore from titles, and the notebook (§4) states the limits; the early volumes are seated whole in EA-CORPORA-40/01 so that the text question can be read on the page.

Files, under original/:
- census-cp.json: the Crossref works, as census_cp.py keeps them (DOI, year, type, title, subtitle, authors, volume, issue, page, citation count). The raw response is recorded by its SHA-256.
- cp-items.json: the 4,252 items kept (journal articles; reviews, front and back matter, and untitled items removed), ids CP0001–CP4252 in date order.
- cp-titles-all.csv, cp-titles-sample390.csv, sample390-ids.json: the files for the blind parallel run (a stratified sample, 30 per decade, seed 31) and its ids, so that both coders' work can be joined.
- d3-candidates.json: the 35 titles the corpus-grain lexicon flagged, all read by hand.
- census_cp.py: the script.
- PHILOLOGY-CENSUS-notebook-v0.1.md: the working notebook, not deposited.
- EA-CORPORA-philology-inventory.md: what the archive held, what was missing, and what this seating gathers.
