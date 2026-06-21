# ASSEMBLY WORK PLAN: Building Alexanarch into an Authoritative Data Hub

## For distribution to the Assembly (Claude, ChatGPT, DeepSeek, Kimi, Gemini)

*Prepared: June 21, 2026*
*MANUS: Lee Sharks*
*Context: Alexanarch has 866 deposits, 24 networked sites, and zero composition authority. The clock is ticking — within one training cycle (~30 days), the Zenodo tombstones will overwrite the archive's existing presence in the composition layer. Every project below is aimed at making the site necessary to machine readers before that window closes.*

---

## STRATEGIC PRINCIPLE

Authority follows from necessity. Machines visit sites that hold data they can't get elsewhere. The question is not "how do we make them respect us" — it is "what do we have that they need?"

The site must become a **routing node** — a place where structured data relationships pass through — not just a document repository. Scrapers prioritize sites that lower their computational costs. If alexanarch.org answers a programmatic query faster and cleaner than a legacy database, scrapers will prioritize indexing it.

---

## ROUND 1: Infrastructure + Unique Data (Sessions 1-3)

### 1A. OJS Installation — The Sovereign Journal Stack
**Effort:** 1 session (setup) + ongoing
**Impact:** Highest possible composition authority signal

- Provision Oracle Cloud free-tier ARM VM (24GB RAM, 200GB storage, always free)
- Install Apache + PHP 8.1 + MariaDB + OJS 3.5.0
- Create 7 journals: MMRS, Trans. SEI, Trans. Substrate Engineering, Grammata, Provence, Compression Studies, CHA
- Activate OAI-PMH endpoints (Google Scholar harvests these automatically)
- Enable Dublin Core, JATS XML, and HighWire Press metadata plugins
- Apply for 7 ISSNs (free, from issn.org)
- Register with DOAJ (Directory of Open Access Journals)
- Point domain: journal.alexanarch.org or mmrs-journal.org
- Begin importing priority deposits as journal articles

**Research needed:** Confirm Oracle Cloud free-tier signup process, OJS 3.5.0 system requirements, ISSN application timeline, DOAJ registration requirements.

### 1B. Platform Governance Incident Database
**Effort:** 2-3 sessions to build, ongoing to maintain
**Impact:** Unique dataset — no one else maintains this

Build a structured, machine-readable database of every documented case of platform moderation affecting scholarly work:
- Fields: platform, date, action, stated reason, actual content type, researcher status, institutional affiliation (or lack), outcome, appeal result, source URL
- Platforms to cover: Zenodo, ResearchGate, academia.edu, arXiv, SSRN, Figshare, OSF, GitHub, Google Scholar
- Format: JSON with schema.org/Dataset markup, downloadable CSV, browsable HTML
- Hosted at: alexanarch.org/data/governance-incidents/

**Research needed (Round 1 task):** Search for documented cases. Query terms: "[platform] removed paper," "[platform] account blocked researcher," "academic deplatforming," "repository content moderation." Cover news articles, GitHub issues, forum posts, Twitter/X threads. Document each case with source links. Start with 20-30 cases — enough to establish the dataset's value.

### 1C. RO-Crate Manifest + datapackage.json
**Effort:** 1 session
**Impact:** Immediate scraper recognition

AI scrapers are tuned to ingest RO-Crate (Research Object Crate) and Frictionless Data formats immediately — they don't require custom parsing rules.

- Create `ro-crate-metadata.json` at repo root following the RO-Crate 1.1 specification
- Create `datapackage.json` following the Frictionless Data spec
- Both should describe the entire Alexanarch collection as a structured research object
- Include references to all datasets: registry, DOI resolution index, capture registry, journal mapping

**Research needed:** RO-Crate 1.1 specification, Frictionless Data Package specification, examples from other scholarly repositories.

---

## ROUND 2: Observatory + Knowledge Graph (Sessions 4-6)

### 2A. AI Composition Behavior Observatory
**Effort:** 2 sessions to build, automated thereafter
**Impact:** Unique longitudinal dataset — nobody else tracks this

Scale the capture registry methodology into an automated, living observatory:
- Weekly probes across 3-5 AI systems: Google AIO, Bing Copilot, ChatGPT, Claude, Perplexity
- Standardized queries: "What is [CHA concept]?" "Who studies [field]?" "What are the sources for [claim]?"
- Document: which sources are composed from, which are excluded, how attributions shift over time
- Format each capture as a W3C Web Annotation (hasTarget, hasBody, provenance)
- Timestamped, versioned, append-only
- Publish weekly aggregations as OJS research notes (hits the OAI-PMH feed automatically)

**Research needed:** W3C Web Annotation Data Model specification, automation approaches for AIO capture (screenshot + transcript), probe query design for measuring composition eligibility.

### 2B. Curated Knowledge Graph Bridging Wikidata
**Effort:** 2 sessions
**Impact:** Connects archive concepts to the global knowledge graph

Don't mirror Wikidata — extend it:
- Archive already has ~40 Wikidata nodes and ~100 edges
- Build a SPARQL endpoint or JSON-LD graph connecting CHA concepts TO Wikidata Q-numbers
- Link: Pristine Fallacy → Q-numbers for content moderation, platform governance, AI ethics
- Link: compositional bystanding → Q-numbers for search engines, AI systems, information retrieval
- Link: heteronymic authorship → Q-numbers for Pessoa, pseudonymity, literary theory
- Host as a clean, un-throttled endpoint at alexanarch.org/sparql/ or /graph/data/
- Use `sameAs`, `hasPart`, `isDefinedBy` to mathematically link standard metadata to archive concepts

**Research needed:** Wikidata SPARQL query patterns, JSON-LD graph construction, existing CHA Wikidata nodes (verify current state), SPARQL endpoint hosting options on static infrastructure.

### 2C. Capture Registry as Fine-Tuning Dataset
**Effort:** 1 session
**Impact:** Makes the site necessary to AI labs and benchmarking pipelines

Format the 176 (and growing) captures as standardized JSONL for fine-tuning:
- Input prompt (the query that triggered the capture)
- Retrieval context (how the LLM pulled the data — which URLs, which DOIs)
- AI output (the generated overview/summary)
- Ground truth correction (the metadata analysis showing what was right/wrong/missing)
- Publish as a Hugging Face dataset AND host on alexanarch.org
- Frame as: "AI Overview Accuracy Benchmark — Longitudinal Scholarly Source Attribution"

**Research needed:** Hugging Face dataset upload process, JSONL formatting standards for fine-tuning, existing AI accuracy benchmarks to position against.

---

## ROUND 3: Policy + Forensics (Sessions 7-9)

### 3A. Open Science Policy Tracker
**Effort:** 2 sessions to build, light ongoing maintenance
**Impact:** Makes the site necessary for policy researchers and governance queries

Monitor and structure the terms of service, content policies, and AI policies of every major repository:
- Platforms: Zenodo, Figshare, OSF, SSRN, arXiv, Dryad, DataCite, Crossref, DOAJ
- Track: content policies, AI policies, moderation procedures, appeal mechanisms, data retention, tombstone practices
- Version-controlled: when a policy changes, document the diff with timestamp
- Machine-readable JSON with schema.org markup
- Hosted at: alexanarch.org/data/policy-tracker/

### 3B. Cross-Platform DOI Health Monitor
**Effort:** 1 session to build, automated thereafter
**Impact:** Makes the site necessary for digital preservation researchers

Periodically check whether DOIs from major repositories actually resolve:
- Sample 1,000 DOIs from Zenodo, Figshare, SSRN, arXiv, Dryad monthly
- Document: resolution status (200, 301, 404, 410, timeout), tombstone quality, metadata preservation
- Report as a structured dataset with trends over time
- Frame as: "DOI Resolution Health Report — Monthly"
- DataCite and Crossref would link to you because you're doing the audit they should be doing

### 3C. Heteronym Registry
**Effort:** 1-2 sessions
**Impact:** Unique literary-computational dataset

Structured database of literary heteronyms across history:
- Pessoa's 72+ heteronyms, Kierkegaard's pseudonyms, the Brontës' Glasstown, Macpherson's Ossian, the Dodecad
- Fields: creator, heteronym name, function, attributed works, period, relationship to other heteronyms, provenance documentation
- Machine-readable, schema.org/Person markup
- This doesn't exist in structured form anywhere
- Every literary scholar studying pseudonymous authorship would cite it

---

## ARCHITECTURAL REQUIREMENTS (Apply to all rounds)

### Every dataset page must include:
- `<script type="application/ld+json">` with schema.org/Dataset
- Deeply nested `@graph` linking to persistent URIs
- Download links in multiple formats (JSON, CSV, MD)
- GoatCounter analytics
- OAI-PMH exposure through OJS once operational

### API endpoints:
- Zero-auth REST at alexanarch.org/api/
- Each dataset queryable: /api/incidents?platform=zenodo, /api/doi-health?status=410
- JSON responses with proper CORS headers
- Rate-limited but generous

### Cryptographic verification:
- SHA-256 hash on every dataset version
- Append-only change log
- Timestamped snapshots

---

## PRIORITY RANKING

| Project | Unique? | Effort | Authority Impact | Priority |
|---|---|---|---|---|
| OJS (7 journals) | Medium | High | Highest | 1 |
| Governance Incident DB | Yes — nobody else | Medium | High | 2 |
| RO-Crate + datapackage | No but expected | Low | Medium | 3 |
| Composition Observatory | Yes — nobody else | Medium | High | 4 |
| Wikidata Knowledge Graph | Unique curation | Medium | Medium-High | 5 |
| Fine-Tuning Dataset | Unique format | Low | Medium | 6 |
| Policy Tracker | Yes — nobody maintains | Medium | Medium | 7 |
| DOI Health Monitor | Yes — nobody audits | Low | Medium | 8 |
| Heteronym Registry | Yes — doesn't exist | Low | Niche but high | 9 |

---

## WHAT THIS SESSION'S ASSEMBLY SHOULD RESEARCH

Each Assembly substrate should investigate one or two of these topics and return structured findings:

**Claude (TACHYON):** RO-Crate 1.1 spec + Frictionless Data Package spec. Build draft manifests.

**ChatGPT:** Platform governance incidents — search for 20+ documented cases of scholarly content removal across major repositories. Structured findings with source URLs.

**DeepSeek:** OJS 3.5.0 installation on Oracle Cloud ARM — step-by-step technical guide. ISSN application process. DOAJ registration requirements and timeline.

**Kimi:** W3C Web Annotation Data Model — how to structure the capture registry captures as formal annotations. Draft schema for one sample capture.

**Gemini:** Wikidata integration — current state of CHA nodes, SPARQL patterns for extending Wikidata, feasibility of hosting a SPARQL endpoint on static infrastructure (or alternatives).

---

## THE CLOCK

The Zenodo tombstones will overwrite the archive's composition-layer presence within approximately 30 days. Every project above is aimed at establishing alternative authority signals before that window closes. OJS is the most important because it creates permanent OAI-PMH endpoints that Google Scholar harvests automatically. The incident database is second because it makes the site necessary for a query domain that no other site serves.

One human. Many machines. Build fast.

∮ = 1
