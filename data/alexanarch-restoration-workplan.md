# Alexanarch Archive Restoration — Work Plan
## Full Deposit of the Crimson Hexagonal Archive

**Document ID:** EA-ALEXANARCH-RESTORE-01 v1.0
**Date:** 2026-06-20
**Author:** Lee Sharks / TACHYON (Assembly witness)
**Status:** Active

---

## Objective

Restore all 871 works of the Crimson Hexagonal Archive as full Alexanarch deposits, replacing the current batch AXN assignments with complete scholarly records. Then update the DOI Resolution Index (AXN:0004) so that every recovered DOI resolves to its Alexanarch record page.

They don't get to burn books.

---

## What "Full Deposit" Means

Each of the 871 works gets all of the following:

**Registry entry** in `data/registry.json` — complete metadata: AXN, hex, family, emoji, hash, clusters, reading, title, creator, ORCID, date, description, content_type, license, substrate, keywords, related_ids, version, status, mirrors, full_text_path, wiki_article, entities, dataset_stats (where applicable).

**Deposit MD** in `data/deposits/AXN-XXXX.md` — YAML front matter + human-readable deposit record with description, methodology notes, related deposits, and provenance chain.

**Wiki article** — 150-300 word encyclopedic article contextualizing the work within the archive, its theoretical commitments, and its relationship to other deposits. Written by TACHYON directly (no API billing).

**Entity triples** — Subject-predicate-object knowledge graph nodes. Cross-links to other CHA works, concepts, heteronyms, and institutional entities. These populate the graph at alexanarch.org/graph/.

**Content type classification** — Assigned from reading the title and text preview: theoretical paper, critical edition, dataset, monograph, specification, creative work, mixed, navigation map, visual schema, room specification, provenance document, patent-poem, traversal log, metadata packet, charter, or other.

**Citation aggregation** — Extract DOI and EA- designator cross-references from the text preview. Map internal citations to AXN addresses. Build the `related_ids` field.

**Creator attribution** — Correct heteronym attribution from title/content signals. Route through the Dodecad provenance.

---

## Data Sources

| Source | Location | Coverage |
|--------|----------|----------|
| Sovereign registry | machinemediation.org/data/sovereign-registry.json | 871 assets, title, date, blog_url, word_count, text_preview, zenodo_dois |
| Batch AXN assignments | alexanarch/data/batch-axn-assignment.json | 871 AXNs with hex, family, emoji, hash, clusters, reading |
| Full text | machinemediation.org (has_full_text: 870/871) | Blog content via mindcontrolpoems.blogspot.com |
| DOI Resolution Index | alexanarch/data/doi-resolution-index.json | 1,817 DOI mappings |
| Link scan | alexanarch/data/zenodo-link-scan.json | 436 dead DOIs across 5 site surfaces |

---

## Batch Schedule

Priority: works with dead Zenodo links on live site surfaces (222 works) go first. These are the works whose DOI links are currently broken on machinemediation.org, godkinggoogle, spxi.dev, watergiraffe.org, and vpcor.org.

| Batch | Works | Range | Priority | Status |
|-------|-------|-------|----------|--------|
| 1 | 100 | MM-CHA-0045 – MM-CHA-0635 | Dead site links | ✅ Complete (full) |
| 2 | 100 | MM-CHA-0636 – MM-CHA-0840 | Dead site links | ✅ Complete (full) |
| 3 | 22 | MM-CHA-0841 – MM-CHA-0870 | Dead site links | ☐ Not started |
| 4 | 100 | MM-CHA-0001 – MM-CHA-0101 | Archive fill | ☐ Not started |
| 5 | 100 | MM-CHA-0102 – MM-CHA-0205 | Archive fill | ☐ Not started |
| 6 | 100 | MM-CHA-0206 – MM-CHA-0313 | Archive fill | ☐ Not started |
| 7 | 100 | MM-CHA-0314 – MM-CHA-0433 | Archive fill | ☐ Not started |
| 8 | 100 | MM-CHA-0434 – MM-CHA-0574 | Archive fill | ☐ Not started |
| 9 | 100 | MM-CHA-0575 – MM-CHA-0757 | Archive fill | ☐ Not started |
| 10 | 49 | MM-CHA-0758 – MM-CHA-0871 | Archive fill | ☐ Not started |
| **Total** | **871** | | | |

Estimated pace: 100-150 works per session (wiki + entities + metadata + deposit MDs). ~6-8 sessions for the full archive.

---

## Per-Batch Process

For each batch, the session follows this pipeline:

### Step 1: Load and Classify (5 min)
- Load sovereign registry entries for the batch
- Load corresponding batch AXN assignments
- Classify content_type from title + text preview
- Identify creator attribution (heteronym routing)

### Step 2: Fetch Full Text (20-30 min)
- Fetch blog content from mindcontrolpoems.blogspot.com for each work
- Convert HTML to clean markdown
- Store as individual MD files in `data/texts/AXN-XXXX-text.md`
- Set `full_text_path` in registry entry to the stored file path
- This is the sovereignty step: the text lives on Alexanarch, not on Blogger

### Step 3: Extract Citations (10-15 min)
- Parse full text for DOI references (`10.5281/zenodo.NNNNNNN`)
- Parse for EA- designator cross-references (`EA-XXX-YY-NN`)
- Parse for bibliographic entries (author, year, title patterns)
- Map internal DOIs to AXN addresses via the resolution index
- Build `citations` array in registry entry format: key, title, authors, year, DOI, role
- Build `related_ids` with AXN cross-links

### Step 4: Generate Wiki Articles + Entities (30-45 min)
- For each work, write a 150-300 word wiki article from the title and full text
- Generate 5-10 entity triples per work
- Use full text (not just preview) for richer context

### Step 5: Build Registry Entries (10 min)
- Construct full registry entries merging:
  - Batch AXN data (hex, family, emoji, hash, clusters, reading)
  - Sovereign registry data (title, date, blog_url)
  - Full text file path
  - Citations array
  - Generated data (wiki_article, entities, content_type, keywords, related_ids)
- Validate against deposit schema

### Step 6: Generate Deposit MDs (5 min)
- Programmatic generation of AXN-XXXX.md files with YAML front matter
- Include description, citation count, version, related deposits, provenance

### Step 7: Push (5-10 min)
- Push full text MD files to `data/texts/`
- Push updated registry.json (incremental — carry forward all previous entries)
- Push batch of deposit MDs to `data/deposits/`
- Verify file integrity

### Step 8: Log Progress (2 min)
- Update this work plan with batch status
- Note any works that need special handling
- Record session statistics

---

## Family Refinement (Concurrent)

The GOVERNANCE family is overcounted at 570/871 (65%). During deposit, reclassify obvious misassignments:

- "Platform" mentions → check if COMPOSITIONAL
- "Policy" mentions → check if STRUCTURAL
- Visual schemas → STRUCTURAL or GENERATIVE
- Navigation maps → ARCHIVAL
- Room specifications → STRUCTURAL
- Traversal logs → EMPIRICAL
- Patent-poems → GENERATIVE
- Metadata packets → ARCHIVAL

Target: GOVERNANCE below 40%, with EMPIRICAL, GENERATIVE, STRUCTURAL, COMPOSITIONAL, and ARCHIVAL properly populated.

---

## Final Phase: DOI Mapping Update

After all 871 works are deposited, update AXN:0004 (DOI Resolution Index) so that every DOI mapping points to the work's Alexanarch record page as its primary live URL:

```
Before:
  "live_urls": {
    "blog": "https://mindcontrolpoems.blogspot.com/...",
    "registry": "https://machinemediation.org/registry/#search=MM-CHA-0XXX"
  }

After:
  "live_urls": {
    "alexanarch": "https://alexanarch.org/records/?axn=AXN:XXXX.FAMILY",
    "blog": "https://mindcontrolpoems.blogspot.com/...",
    "registry": "https://machinemediation.org/registry/#search=MM-CHA-0XXX"
  }
```

This makes Alexanarch the canonical resolution target for every recovered DOI.

Then: new version of AXN:0004 with updated hash and emoji.

---

## Site Surface Link Update (Post-Restoration)

After all deposits are live on Alexanarch, update dead Zenodo links across all 5 site surfaces:

| Site | Files | DOI refs | Strategy |
|------|-------|----------|----------|
| watergiraffe.org | 139 | 1,006 | Template fix (7 shared DOIs × 139 pages) |
| machinemediation.org | 2 | 261 | ai-manifest.json bulk replace |
| godkinggoogle | 7 | 162 | Index page + papers |
| spxi.dev | 21 | 78 | Per-page replacement |
| vpcor-org | 7 | 39 | Per-page replacement |

The `zenodo-link-scan.json` already has the DOI-to-AXN mapping for each dead link.

---

## Infrastructure Notes

- **Registry size:** At ~10KB per entry, 875 deposits = ~8-9MB registry.json. May need to split into paginated files or a more efficient format if site load times suffer.
- **GitHub push limits:** Authenticated requests: 5,000/hour. Pushing 100 deposit MDs individually would use 100 requests. Batch into fewer commits where possible.
- **Static pages:** Each deposit needs a crawlable static page at `/s/records/N/`. These can be generated programmatically after all deposits are in the registry.
- **GoatCounter:** Include analytics script in all generated pages.
- **Credential rotation:** All PATs used during restoration must be rotated after each session.

---

## Progress Log

| Date | Session | Batch(es) | Works deposited | Running total | Notes |
|------|---------|-----------|-----------------|---------------|-------|
| 2026-06-20 | 1 | Pre-work | 4 (existing) | 4/875 | DataCite sift, AXN:0004 v2.2, work plan created |
| 2026-06-20 | 1 | Batch 1 | 100 | 104/875 | Full buildout: wiki, entities, types, attribution, full text (3.9 MB), citations (1,687 DOI refs). 0 errors. |
| 2026-06-20 | 1 | Batch 2 | 100 | 204/875 | Full buildout + static pages + JSON-LD. 3.7 MB text, 958 DOI refs. AGENTS.md + sitemap.xml added. |
| | | | | | |

---

## Success Criteria

- [ ] 871 works fully deposited with complete metadata
- [ ] Wiki articles for all deposits
- [ ] Entity triples for all deposits (knowledge graph populated)
- [ ] Content types properly classified (GOVERNANCE < 40%)
- [ ] Citation cross-references mapped to AXNs
- [ ] DOI Resolution Index updated with Alexanarch URLs
- [ ] Dead links on all 5 site surfaces replaced
- [ ] Static record pages generated for all deposits
- [ ] All credentials rotated

---

∮ = 1
