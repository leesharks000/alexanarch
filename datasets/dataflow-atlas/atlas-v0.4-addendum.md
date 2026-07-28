# AXN Dataflow Atlas — v0.4 Addendum

**Date:** 2026-07-28
**Author:** Lee Sharks (MANUS), with TACHYON (Assembly witness)
**Supplements:** `atlas-v0.2.md`, `atlas-v0.3-addendum.md`
**Occasion:** a corpus-wide title repair, and what it revealed about how field edits do and do not travel.

---

## PATHOLOGY-26 — Derived datasets copy titles; no regenerator refreshes them

**Class:** DERIVED.divergence
**Severity:** high — silently produces competing sets of deposit names with no signal to a consumer about which is current
**Status:** instrument built, corpus clean as of this addendum; the underlying flow is unchanged

### Statement

The registry is the source of truth for a deposit's title. The title is also **copied into at least eight datasets**, and the regenerators that rebuild those datasets **preserve a title they already hold** rather than re-reading it from the registry. A correction written to `data/registry.json` therefore does not correct the corpus. It creates one competing name per dataset, and a consumer reading any of them has no way to know which is current.

### Evidence

Discovered 2026-07-28 during the repair of 152 titles whose frontmatter had been concatenated into the title field and truncated at a character ceiling (see §PATHOLOGY-27). After writing the registry **and** running `regenerate_surfaces.py`, `build_concept_map.py`, and `build_mirror_map.py` — that is, after every regeneration step the archive provides — the following datasets still carried superseded titles:

| dataset | superseded titles remaining after full regeneration |
|---|---|
| `data/capture-deposit-links.json` | 99 |
| `data/wiki-entries.json` | 33 (in generated prose; title fields were current) |
| `data/concept-map.json` | 0 |
| `data/mirror-map.json` | 0 |
| `data/browse-index.json` | 0 |
| `api/search-index.json` | 0 |
| `datasets/set.json` | 0 |

`concept-map`, `mirror-map` and `search-index` were clean because their builders reconstruct entries from the registry wholesale. `capture-deposit-links` was not, because its builder writes a title at link-creation time and does not revisit it. `wiki-entries` carried current titles but stale **prose**, because the wiki generator quotes the title into an authored description and the description is not regenerated when the title changes.

That distinction is the pathology's real shape: **the archive has two kinds of derived dataset, and only one kind self-heals.** Nothing in the data layer marks which is which.

### Instrument

`scripts/propagate_titles.py`. Walks each derived dataset, resolves every record carrying a title to a registry deposit by deposit number, AXN, or embedded record path, and replaces the title with the registry value. It never invents a title, never edits a record it cannot resolve, and reports resolved / already-current / unresolvable counts per dataset. Dry-run by default.

### One dataset is excluded, and the exclusion is the point

`data/doi-resolution-index.json` carries a `title` field on all 1,939 mappings and is **deliberately not propagated to**.

Its title is not a copy of the deposit's name. It is the title the work carried **at Zenodo** — historical metadata describing a severed identifier. Some rows carry `mapping_type: misclassified_other_author` and name works by other authors that fell inside the DOI range. A first draft of the propagation instrument proposed rewriting **2,367 of these fields** from the registry, which would have destroyed the record of what each dead DOI was called — the index's entire purpose.

The general principle, which the atlas should carry forward: **a field named `title` in a derived dataset is not necessarily a copy of the canonical title.** Before any propagation, establish whether the field is a *replica* (should track the source) or a *record of a past state* (must not). The archive currently provides no way to tell these apart from the data alone, which is the residual defect this addendum leaves open.

### Residual

- No dataset declares whether its title field is a replica or a historical record. Proposed: a `field_semantics` block at the top of each derived dataset naming, per field, whether it tracks a source or records a state.
- No regeneration step is mandatory after a registry field edit. Proposed: fold `propagate_titles.py` into the deposit pipeline's identity stage, and extend it beyond titles to any field replicated across datasets.
- The wiki generator's authored prose quotes canonical values and is not invalidated when they change. Prose corrected in place this pass; the flow is unchanged.

---

## PATHOLOGY-27 — The title field absorbed the frontmatter block, then truncated

**Class:** REGISTRY.field-integrity
**Severity:** high — affected 15% of the corpus in every machine-facing surface
**Status:** 152 corrected, 21 held for a reading pass, 1 empty title outstanding (#125)

### Statement

At ingest, the title field of many deposits was populated with the document's frontmatter block concatenated after the title — author, affiliation, ORCID, hex address, date, document ID, version, license — and then cut at a **120- or 200-character ceiling**, landing mid-word. 138 titles sat at exactly 120 characters and 51 at exactly 200. The resulting strings appeared as the deposit's name in the `<title>` tag, the meta description, `citation_title`, and the JSON-LD `name` on every record page.

Representative: `…Author: Lee Sharks Affiliation: Crimson H` · `…Semantic Economy I` · `…First published: mindcontrolpoems.blogspot.com, 29 D` · `ERASURE SKEW: A Measurement Program … Composition Systems E`.

### Method, and why it matters

An earlier pass (2026-07-26) used a word list of section headers, found 212 titles ending in "Description" or "Abstract", corrected those, and reported the corpus clean. **It could not see this defect at all**, because a truncated frontmatter block does not end in any word a list can anticipate.

The present pass read all 1,411 titles in batches and derived the rule from what was observed. Four corrections to the rule emerged from reading successive batches, each of which a regex pass would have shipped as a success:

1. `Document:` fires only before a numeric identifier — it was cutting *Heteronym Provenance Document: Rebekah Cranes* to *Heteronym Provenance*.
2. `License:` removed from the marker set entirely — in this archive it names a document type, and the marker was truncating two contributor-license titles at their subject.
3. A bracketed `[SUPERSEDED …]` or `[DUPLICATE …]` prefix is preserved whole — the DOI marker was firing inside it and reducing thirteen titles to `[SUPERSEDED →`.
4. Trailing tree-drawing characters are trimmed — nine titles were left ending in a dangling `├──`.

**The methodological finding is worth recording as such:** at this corpus size, a title-level defect is *readable* — 1,411 titles is a bounded quantity — and a classifier written before reading will report the absence of its own class as the absence of defects. The rule should be derived from the reading, not the reading replaced by the rule.

### Held, not guessed

21 titles are held rather than corrected: their metadata runs on with no marker, so the boundary between title and byline is not visible in the string. These require the deposit's body heading to be read. #125 has no title at all and is held with them.
