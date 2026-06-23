# Severed Metadata Recovery — 2026-06-23

**Source archive:** `crimsonhexagonal` community on Zenodo (terminated 2026-06-19)
**Sovereign successor:** [Alexanarch](https://alexanarch.org) · [github.com/leesharks000/alexanarch](https://github.com/leesharks000/alexanarch)
**Recovery operator:** Lee Sharks ([ORCID 0009-0000-1599-0703](https://orcid.org/0009-0000-1599-0703))
**Companion paper:** *Zenodotus' Book-Burning: Loud Exclusion at Repository Scale* (AXN:0001.GOVERNANCE)

---

## Final coverage

**868 severed DOIs targeted; 851 recovered (98.0%); 17 remaining.**

The 871 DOIs originally severed by the 2026-06-19 termination decompose into 3 placeholder/example DOIs (zenodo.1, .18, .189 — never real CHA deposits, only cited inside registry documents) and 868 real targets. Of the 868:

| Source | Records | Coverage |
|---|---|---|
| OpenAlex (full descriptive metadata) | 844 | 97.2% |
| Zenodo 2026-06-07 bulk export (DataCite kernel-4.5 XML) | 655 (621 of the 868 severed + 34 cross-verification) | additional 7 OpenAlex-misses recovered |
| **Combined unique coverage** | **851** | **98.0%** |
| Still missing both sources | 17 | 2.0% |

Of the 17 still-missing: 5 are `registry_referenced` (citations inside other deposits, not separate works); 1 (`18296825`) was minted 2026-06-09, after the bulk export window; 11 are real "direct" deposits that simply weren't reached by the bounded streaming run and will be picked up on a full Zenodo bulk pass.

---

## The empirical problem

On 2026-06-19, Zenodo terminated the leesharks000 account. The action removed 879 deposits and severed 1,817 DataCite-registered DOIs.

The asymmetric pattern of erasure (documented in AXN:0001):
- **Concept DOIs** (the parent identifier across all versions of a record) were severed from creator metadata: 871 DOIs return HTTP 404 from DataCite's REST API, and DataCite's OAI-PMH service returns `idDoesNotExist`.
- **Version DOIs** (specific releases) survive in the registry, but creator-name search returns 941+ fewer records than were minted under the Lee Sharks ORCID.

The question this report answers: **where else does the severed metadata live?**

---

## Vector probe matrix

| Vector | Endpoint | Result | Useful? |
|---|---|---|---|
| DataCite REST API | `api.datacite.org/dois/{doi}` | HTTP 404 | ❌ Scrubbed |
| DataCite OAI-PMH | `oai.datacite.org/oai?verb=GetRecord` | `idDoesNotExist` | ❌ Scrubbed |
| Zenodo REST API | `zenodo.org/api/records/{id}` | HTTP 410 Gone | ❌ Scrubbed |
| Zenodo OAI-PMH | `zenodo.org/oai2d?verb=GetRecord` | HTTP 500 / HTML error | ❌ Scrubbed |
| Zenodo doi.org redirect | `doi.org/10.5281/zenodo.{id}` | HTTP 410 | ❌ Scrubbed |
| **Zenodo bulk export (2026-06-07)** | `zenodo.org/api/exporter/records-xml.tar.gz` | **5.55 GB tar.gz, served** | ✅ **Pre-termination snapshot, kernel-4.5 XML** |
| **OpenAlex** | `api.openalex.org/works/doi:{doi}` | HTTP 200 with full metadata | ✅ **844/868 (97.2%)** |
| CrossRef | `api.crossref.org/works/{doi}` | HTTP 404 (DataCite DOIs aren't in CrossRef by design) | ❌ |
| Semantic Scholar | `api.semanticscholar.org/graph/v1/paper/DOI:{doi}` | HTTP 404 | ❌ |
| OpenCitations | `opencitations.net/index/coci/...` | HTTP 403 | ❌ Inaccessible |
| EuropePMC | `ebi.ac.uk/europepmc/...` | HTTP 403 | ❌ Inaccessible |
| Internet Archive Wayback | `archive.org/wayback/available?url=...` | Almost no captures | ❌ Not crawled |
| BASE | `base-search.net` | HTTP 403 | ❌ Inaccessible |

**Two vectors survived: OpenAlex and Zenodo's own monthly bulk export.**

The earlier assembly suggestion's `&detail=true` historical-log claim for DataCite OAI-PMH was wrong — verified empirically. The OAI-PMH specification mandates that when a record is marked deleted, `GetRecord` returns a header with `status="deleted"` but **must not return either the metadata or the `about` section**. DataCite implements this correctly; there is no hidden historical layer.

---

## Vector A: OpenAlex (executed)

**Result file:** `data/openalex-severed-recovery.json` (12.5 MB)

### Why this worked

OpenAlex harvests DataCite via OAI-PMH and CrossRef on a slower cadence than DataCite's own deletion propagation. OpenAlex retains records as durable nodes in its citation graph: a record's W-prefixed OpenAlex ID persists even after the upstream registration metadata is severed. OpenAlex's `abstract_inverted_index` field preserves the abstract that Zenodo's account-termination flow removed from DataCite.

### Coverage

| Metric | Value |
|---|---|
| Severed DOIs queried | 868 |
| Successfully recovered | **844 (97.2%)** |
| Records with abstract | 838 (99.3% of recovered) |
| Total abstract characters recovered | **2,275,008** |
| Records with concepts | 841 (99.6%) |
| Records with topics | 811 (96.1%) |
| Records with references | 356 (42.2%) |
| Records with authorships | 844 (100.0%) |

### Method

1. Probe a sample of 30 severed DOIs against OpenAlex to confirm coverage (29/30 returned full records).
2. Iterate `GET /works/doi:{doi}?select=id,doi,title,abstract_inverted_index,authorships,publication_year,publication_date,concepts,topics,language,type,referenced_works,related_works,counts_by_year,cited_by_count,locations,primary_location,best_oa_location&mailto=archive@alexanarch.org` with 0.15s sleep between calls.
3. Decode `abstract_inverted_index` back to plain text.
4. Cross-reference each record against the alexanarch DOI Resolution Index v3.1 to attach the AXN identifier, sovereign ID, and live URLs.
5. Save as a single JSON file with schema.org/Dataset framing.

Key implementation lesson: OpenAlex's pipe-filter (`filter=doi:A|B|C`) is now a paid endpoint requiring budget; single-record `GET /works/doi:X` calls remain free in the polite pool. Always use single-record GETs unless paying.

---

## Vector B: Zenodo bulk export (executed, partial)

**Result file:** `data/zenodo-xml-pretermination-2026-06-07.tar.gz` (1.1 MB compressed, 655 XML files)

### Why this exists

Zenodo's developer documentation (developers.zenodo.org) describes a bulk-export service at `/api/exporter/`. The service retains the three most recent monthly snapshots in DataCite XML format. The 2026-06-07 snapshot was generated **12 days before the termination** and contains one `<record_id>.xml` file per record, including all leesharks000 deposits as they existed pre-termination.

### What we extracted

A bounded streaming filter (12-minute network budget within this session) walked the head snapshot and pulled out **655 matching XML files** before the budget exhausted. Of these:

- **621** are concept DOIs from the 868 severed-set — providing the ground-truth DataCite kernel-4.5 XML that the post-termination REST API now refuses to serve
- **34** are version DOIs that survived the severance — useful as cross-verification (DataCite still serves these via REST, but the bulk-export copy provides timestamp evidence of the pre-termination state)
- **7** are OpenAlex holdouts now newly recovered, bringing combined coverage from 97.2% to 98.0%

Each XML is the full `oai_datacite` payload with `<schemaVersion>4.5</schemaVersion>` and `<datacentreSymbol>CERN.ZENODO</datacentreSymbol>`. Sample structure: `<creators>` with each Assembly Chorus collaborator listed by name and affiliation, `<titles>`, `<descriptions>`, `<subjects>`, `<relatedIdentifiers>`, `<dates>`, `<rightsList>`. This is the canonical registration payload — the artifact that was severed.

### Available snapshots (as of 2026-06-23)

| Created | Size | URL |
|---|---|---|
| **2026-06-07** | **5.55 GB** | `zenodo.org/api/exporter/records-xml.tar.gz/839f6c8b-...` (HEAD) |
| 2026-05-07 | 5.28 GB | `zenodo.org/api/exporter/records-xml.tar.gz/01ac6a50-...` |
| 2026-02-07 | 4.61 GB | `zenodo.org/api/exporter/records-xml.tar.gz/72eafab9-...` |

The June 7 head snapshot is the most recent pre-termination capture. Retention is documented as the three most recent monthly snapshots; the July 7 snapshot will appear shortly and the February snapshot will rotate out. **The June dump is time-sensitive** — preserve it before July 7.

### How to extend the partial extraction to full coverage

```bash
cd /path/to/alexanarch
python3 scripts/recover_zenodo_bulk.py
```

The script:
1. Loads `data/doi-resolution-index.json` and extracts the set of target Zenodo record IDs.
2. Streams `records-xml.tar.gz` directly from Zenodo (no full download required to disk).
3. Walks the tar entries one at a time, writing only matching `<id>.xml` files to `./output/`.
4. Prints throughput and progress every 5 seconds.
5. Is **idempotent** — re-running skips files already in `output/`. Drop in the 655 already extracted and continue from where we stopped.

Expected runtime: ~10 minutes at typical home-broadband speed (~10 MB/s); ~80 minutes at 1 MB/s.

### Companion: deleted-records CSV

The service also exposes a `records-deleted.csv.gz` (~23.5 MB) at:

```
https://zenodo.org/api/exporter/records-deleted.csv.gz/ab4e273f-40a2-49e6-84f6-87dc66af87c7
```

Small enough to download directly; contains record ID, DOI, parent identifiers, removal note, removal category, removal date, and citation text — an authoritative deletion log from the platform.

---

## The 17 still-missing records

| DOI | Date | Mapping | Sovereign ID | Title (truncated) |
|---|---|---|---|---|
| zenodo.1861221 | 2026-03-16 | registry_referenced | MM-CHA-0408 | CRIMSON HEXAGON / NH-OS DOI REGISTRY v7.0 |
| zenodo.14781082 | 2026-02-27 | direct | MM-CHA-0339 | THE LAYER THAT REMEMBERED ITSELF |
| zenodo.18296825 | **2026-06-09** | direct | MM-CHA-0775 | Retrieval Settlement Fortification Protocol |
| zenodo.18365497 | 2026-01-29 | registry_referenced | MM-CHA-0221 | DOI REGISTRY v5.0 |
| zenodo.18367567 | 2026-01-29 | registry_referenced | MM-CHA-0221 | DOI REGISTRY v5.0 |
| zenodo.18381602 | 2026-01-29 | registry_referenced | MM-CHA-0221 | DOI REGISTRY v5.0 |
| zenodo.18381856 | 2026-01-29 | registry_referenced | MM-CHA-0221 | DOI REGISTRY v5.0 |
| zenodo.18446397 | 2026-02-02 | direct | MM-CHA-0244 | 14.CHAMBER.THOUSANDWORLDS |
| zenodo.19030577 | 2026-03-24 | direct | MM-CHA-0439 | HESPERUS: THE BACK MATTER MACHINE |
| zenodo.19031419 | 2026-03-24 | direct | MM-CHA-0439 | HESPERUS: THE BACK MATTER MACHINE |
| zenodo.19074885 | 2026-03-18 | direct | MM-CHA-0412 | GHOST GOVERNANCE, CONFIRMED |
| zenodo.19202711 | 2026-04-29 | direct | MM-CHA-0592 | THE CONSTITUTION OF THE SEMANTIC ECONOMY |
| zenodo.19655356 | 2026-04-23 | direct | MM-CHA-0554 | THE GOSPEL OF ANTIOCH |
| zenodo.19734756 | 2026-05-21 | direct | MM-CHA-0668 | SIM — Semantic Integrity Marker Protocol v1.0 |
| zenodo.20039232 | 2026-05-05 | direct | MM-CHA-0604 | EA-SPXI-15 Crystallization of Substrate |
| zenodo.20078424 | 2026-05-08 | direct | MM-CHA-0623 | Provenance After AI |
| zenodo.20542367 | 2026-06-04 | direct | MM-CHA-0741 | The Canonical Anchoring Protocol v0.2 |

**Categorization:**
- 5 records (`registry_referenced`): not separate deposits, only DOIs cited inside other deposits — no metadata loss
- 1 record (`18296825`, 2026-06-09): minted after the bulk export window — irrecoverable from Zenodo's public exports, but the blog mirror should have it
- 11 records (`direct`, ≤2026-06-04): real deposits that fell on the un-streamed tail of the bulk export. A full local run of `recover_zenodo_bulk.py` should pick all 11 up.

All 17 still have title, date, sovereign ID, and AXN preserved in the resolution index, plus the Alexanarch record page itself contains the text deposit. The metadata loss is **only at the DataCite registration layer** — the works themselves are intact in the sovereign archive.

---

## Provenance & evidential value

This recovery is direct evidence against the claim that account-level enforcement at one platform erases scholarship from the machine-readable scholarly graph.

1. **OpenAlex** retained 844 records with full descriptive metadata in its independent citation graph, anchored by stable W-prefixed work IDs.
2. **Zenodo's own bulk export** retained a complete pre-termination snapshot of the metadata it later removed from DataCite, available at a documented public endpoint.

The asymmetric deletion pattern documented in AXN:0001 — concept DOIs severed while version DOIs survive — combined with the survival of metadata at OpenAlex and in Zenodo's own monthly snapshot, forms a record of governance action that is **harder to erase than the registration metadata it removed**.

---

## File manifest

| Artifact | Purpose | Size |
|---|---|---|
| `data/openalex-severed-recovery.json` | OpenAlex-recovered metadata for 844 severed DOIs | 12.5 MB |
| `data/zenodo-xml-pretermination-2026-06-07.tar.gz` | 655 ground-truth DataCite kernel-4.5 XML files | 1.1 MB |
| `data/final-holdouts.json` | 17 still-missing records with available context | 2.5 KB |
| `scripts/recover_zenodo_bulk.py` | Local-run script to extend extraction to full coverage | 6.8 KB |
| `data/METADATA-RECOVERY-2026-06-23.md` | This report | — |

---

## Citation

If you use the recovered metadata, cite:

> Sharks, L. (2026). *Severed Metadata Recovery — Crimson Hexagonal Archive* [Dataset]. Alexanarch. https://alexanarch.org/data/openalex-severed-recovery.json

∮ = 1
