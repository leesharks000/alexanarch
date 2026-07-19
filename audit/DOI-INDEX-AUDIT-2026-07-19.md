# DOI Resolution Index Audit — 2026-07-19

**Method:** local join of `data/doi-resolution-index.json` mappings against `data/openalex-severed-recovery.json`
(844 OpenAlex-captured titles), keyed on exact DOI. Titles normalized ([SUPERSEDED] prefixes stripped, lowercased);
mismatch = fewer than 2 shared tokens in the first 8 words. No API calls; No-Double-Draw respected.

**Result: 468 of 844 checkable mappings (55.5%) carry a title/target that does not match the OpenAlex record for the same DOI.**
Full list: `DOI-INDEX-AUDIT-2026-07-19.json` (dead_doi, index title, OpenAlex title, current alexanarch target).

**Observed corruption patterns:**
1. **Off-by-one / shifted assignment** — e.g. "A Primer in How to Read the Crimson Hexagon" sits at 10.5281/zenodo.18187481
   per OpenAlex, but the index places that title on 18185996 and gives 18187481 the adjacent record's title.
2. **Many-to-one collapse** — five distinct DOIs (18156781, 18157917, 18158108, 18158140, 18158159) all mapped to
   "THE LAW AS MEANING ECONOMY" / record #239, while OpenAlex shows five distinct works.
3. **Cross-family misassignment** — 10.5281/zenodo.19013315 (THE SPACE ARK v4.2.7) mapped to THE SPLICE (#561);
   surfaced 2026-07-19 by a user-facing 404 report and the revelationfirst link check. The row's own
   `title_verification` note attributes it to a "2026-07-06 correction … exact_title_match" pass.

**Root cause class:** title-similarity matching used as a join key during batch construction/correction.
Titles are not keys. The DOI is the key, and the OpenAlex snapshot + DataCite backup both index by exact DOI.

**Fixed this session (surgical, OpenAlex-verified):** 19013315, 18969405, 18928855 → /s/records/558/
(THE SPACE ARK EA-ARK-01 v4.2.7, AXN:0184.GOVERNANCE.🎵💛🌙♅🕚🏷️); resolver map re-derived via sync_resolver.py.
Registry #561 zenodo_dois cleaned. 18908080 (possible concept-DOI ambiguity vs the Math/Formal doc, #557) left
untouched pending remediation.

**Remediation plan (MANUS scheduling):** regenerate all 844 checkable rows by exact-DOI join from
openalex-severed-recovery.json + datacite-full-backup.json; DOIs absent from both sources stay as-is with an
`unverified` flag; every corrected row gets a title_verification note citing its OpenAlex work ID; sync_resolver +
full validation in the same commit. Estimated one focused session. The remaining 1,094 mappings (not in the OpenAlex
snapshot) get verified against the DataCite backup in the same pass.


---

## Remediation executed same session (index v3.4 → v3.5)

`scripts/remediate_resolution_index.py` — DOI-keyed truth union (DataCite backup 963 + OpenAlex snapshot 844 +
newly-found 21 + tombstone citation_texts), exact-title constraint with tiered fallback (full-token Jaccard ≥0.9 or
≥0.7 with 0.15 gap; containment ≥0.9 for truncated titles), two-pass supersession-pointer resolution, non-Latin/short
title guard. All prior values preserved per-row in `remediation_2026_07_19`.

Final distribution: A exact-unique 164 · C fuzzy 556 · D containment 266 · S superseded-pointer 10 ·
already-correct 280 · ambiguous-earliest 2 (duplicate-deposit pairs #238/#886, #282/#324 — flagged for MANUS) ·
no-candidate 614 (titles corrected, prior targets retained flagged; includes works never restored and known
foreign-DOI rows) · no-truth 34 · unmatchable non-Latin 12. 40 envelopes advanced no_successor_known →
same_work_title_matched with evidence entries. Gates: validate_resolver PASS, parity OK (1938 keys, 1269 live),
registry --strict 0 failures.

**New identity artifact:** `datasets/doi-work-identity/doi-identity-map.json` — the DOI→work identity map that never
previously existed; registered as 9th member of the dataset set. G10's member_count 7-vs-8 was itself a live
PATHOLOGY-01 (the 2026-07-18 atlas pin added the member without bumping the count) — corrected in set.json v1.2,
which also wires every member's `map` field to /datasets/dataflow-atlas/ per MANUS ruling 2026-07-19.
