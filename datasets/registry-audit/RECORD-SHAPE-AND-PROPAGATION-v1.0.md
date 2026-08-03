# RECORD SHAPE & PROPAGATION DOCTRINE v1.0
**Ratified basis:** MANUS 2026-08-03 ("any record repair before understanding final fixed shape will have to be redone").
**Prompted by:** #1267 and #1308 — repairs that landed in the registry while the staged text, static page,
wiki article, chunks, and OAI feed kept declaring prior states. A record must declare ONE state, everywhere.

## 1 · The declaration sites (the SHAPE)
A single deposit's state is declared in NINE places. Every repair must reach all of them or it is a fracture.

| # | Site | Authority |
|---|------|-----------|
| 1 | `data/registry.json` entry — body_status.class + canonical_text_status | **AUTHORITATIVE** (per status_reconcile) |
| 2 | registry display fields — content_type, version, keywords, description, wiki_article | derived from (1) |
| 3 | `data/texts/AXN-XXXX-text.md` — frontmatter AND body-state blocks (Methodology/semi-restored notices) | must agree with (1); body bytes immutable EXCEPT tombstones/recoveries under sealed basis |
| 4 | `s/records/N/index.html` — static record page (banner, byline, Full Text) | rendered from (1)+(3) |
| 5 | `s/wiki/N/` + wiki surfaces | rendered from wiki_article |
| 6 | `data/external-metadata/AXN-XXXX.json` sidecar | must agree |
| 7 | `data/chunks/registry/*.json` mirror | regenerated from (1) |
| 8 | `data/axn-central-registry.json` | regenerated from (1) |
| 9 | `data/oai-index.json` (+ dispositions capsule) | regenerated from (1) + dispositions; **lifecycle_state=withdrawn_external is NEVER exposed** |

## 2 · The propagation order (one command)
`python3 scripts/propagate_record_state.py N [N …]` runs, in order:
1. **Tombstone text rewrite** (only if `lifecycle_state=withdrawn_external`): staged text replaced with the
   typed-tombstone document — foreign content removed, foreign-work frontmatter carries NO archive ORCID,
   rightful author + DOI named.
2. `status_reconcile --apply` — display fields derived from authoritative fields.
3. `wire_deposit.regenerate_static_page` for each N — the record page.
4. `regenerate_surfaces --only chunks,browse,browse-index,search-index,wiki,sitemap`.
5. `build_central_registry`.
6. `build_oai_index` — withdrawn_external excluded at the gate regardless of disposition.

## 3 · The rule
**No repair is complete until propagation has run.** The repair ledger row is inscribed at step 0;
the repair is DONE at step 6. Wave batches run propagation once per batch, not per row.

## 4 · MANUS rulings of 2026-08-03 (recorded here for the repair waves)
- **Controlled type vocabulary: YES** — draft to be ratified before the 159-row compound batch runs.
- **Creator-role projection: project declared roles as the audit recommends** (roles from sealed rows;
  no invention; consent-gated externals unchanged).
