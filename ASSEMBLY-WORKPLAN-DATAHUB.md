# ASSEMBLY WORK PLAN v2: The Scholarly Data Foundry

*Revised June 21, 2026 — incorporates feedback from DeepSeek, Kimi, ChatGPT, Gemini*

---

## THE CORRECTION

The v1 plan proposed nine institutions. The Assembly correctly identified that this risks turning Alexanarch into a full-time defensive infrastructure job. The correction is not to reduce the ambition. It is to build **one automated data-production engine** from which multiple authoritative surfaces are generated.

> **One source of truth. One build command. Multiple outputs.**

---

## CRITICAL CONSTRAINTS (from Kimi)

| Constraint | Impact |
|---|---|
| Oracle Cloud free tier halved (June 15, 2026): 2 OCPUs/12GB, not 4/24GB | 7 journals on one VM is not feasible |
| DOAJ requires 1+ year publishing history OR 10+ articles | Cannot register in 30 days |
| ISSN processing: 1-8 weeks depending on country | Cannot get 7 ISSNs in 30 days |
| Google Scholar does NOT auto-harvest OAI-PMH | OJS is useful, not magic |
| "Always free" is conditional — Oracle may reclaim idle instances | Cannot be a constitutional dependency |

---

## THE STRUCTURAL REDESIGN (from ChatGPT)

### Seven journals — each with a distinct epistemic function

The CHA's material warrants seven independent journals, not one journal with sections. Each serves a specific scholarly function and has sufficient existing material:

| Journal | Abbrev. | Deposits | Function |
|---|---|---|---|
| Machine-Mediated Reception Studies | MMRS | ~212 | How platforms and AI receive, transform, and exclude scholarship |
| Transactions of the Semantic Economy Institute | Trans. SEI | ~371 | Meaning as economic and physical system |
| Transactions in Substrate Engineering | Trans. Substrate Eng. | ~213 | AI substrates as scholarly instruments |
| Grammata: Journal of Operative Philology | Grammata | ~45 | Close reading as operative practice |
| Provence: Studies in Provenance and Attribution | Provence | ~11 | How authorship survives platform transitions |
| Crimson Hexagonal Archive: Journal | CHA | ~10 | Self-reflective documents about the archive itself |
| Compression Studies | Compression Studies | ~2 | Information compression as scholarly practice |

Journals are established in OJS as independent publications, each with its own ISSN application. ISSN registration is sequential, not simultaneous. The current journal-to-deposit mapping (JOURNAL-MAPPING-PRELIMINARY.json) is preliminary and will need more careful assignment among journals and heteronyms before OJS import begins.

### One observatory, three modules — not three separate systems

**Platform Governance Observatory** — a single research object with three tables:
- `incidents` — documented enforcement events
- `policies` — versioned platform policy snapshots and diffs
- `identifier_health` — periodic DOI and landing-page resolution tests

Same schema family, same build process, same browsing interface, same API namespace.

### One build pipeline — not five manually maintained metadata documents

```
/data-src/
  catalog.yaml          ← single source of truth
  deposits/             ← 866 deposit records
  captures/             ← observatory captures
  incidents/            ← governance incidents
  policies/             ← policy snapshots
  doi-health/           ← resolution tests
  heteronyms/           ← heteronym registry

python build.py →
  validates, normalizes, hashes
  generates JSON, CSV, JSONL, Parquet, JSON-LD, RDF, Markdown
  generates RO-Crate 1.2, Data Package, DCAT, checksums
  generates static dataset pages, browse listings, sitemaps
  generates OJS import XML
  publishes only if all validations pass
```

RO-Crate, Data Package, and DCAT are **outputs generated from the same internal catalog**, not three separately maintained documents.

### Fine-tuning dataset is an export target, not a project

The capture registry generates: research JSON-LD, W3C Web Annotation, CSV, JSONL benchmark pairs, Parquet, Hugging Face dataset, and static case pages. All from one canonical capture record. Frame as:

> **AI Composition-Layer Attribution Benchmark** (not "fine-tuning dataset" — the value is evaluation, not reproduction)

### No full SPARQL server yet

Start with static linked data: JSON-LD graph, N-Quads dump, Turtle dump, precomputed common queries, downloadable ontology. Add a client-side Comunica query interface if needed. A live SPARQL endpoint creates another daemon to maintain — add only when external query demand appears.

---

## LABOR CONSTITUTION (from ChatGPT)

| Allocation | Purpose |
|---|---|
| 60% | Positive scholarship — the work that makes Alexanarch worth preserving |
| 25% | Reusable infrastructure — the build pipeline, static pages, machine manifests |
| 15% | Defensive monitoring — the observatory, the incident log |

**Engineering laws:**
- No new recurring monitor unless it uses the existing schema, build pipeline, and publication machinery.
- Any project requiring more than one hour of routine weekly maintenance must either be further automated, receive another steward, or be suspended.
- The architecture succeeds only when it returns you to research.

---

## REVISED SEQUENCE

### Phase 0: Repair and stabilize (1-2 sessions)
- Fix any inconsistencies in current mint, registry, AXN assignment
- Reconcile duplicate site blocks across network
- Redeploy semanticphysics-site
- Full text restoration priority batch (blog harvest for top 50-100 deposits)

### Phase 1: Machine legibility layer (1-2 sessions)
- Build the unified catalog.yaml → build.py pipeline
- Generate from one source: RO-Crate 1.2, Data Package, DCAT, checksums, schemas
- Deploy ro-crate-metadata.json and datapackage.json at repo root
- Immediate scraper recognition with zero ongoing labor

### Phase 1.5: Data consolidation and enrichment (3-5 sessions)

The existing 866 deposits carry batch-produced metadata that is shallow and disconnected. Before adding new material or publishing to external platforms, the internal data must be consolidated so that citations, entities, wiki articles, and deposits form a richly interlinked knowledge structure. This is the phase where the archive learns what shapes it needs.

**Current state (June 2026):**
- 654/866 deposits have zero extracted citations
- Of 1,957 total citation entries, only 19 are internal AXN cross-references
- 1,693 citation entries point to dead Zenodo DOIs (unmapped to live AXN locations)
- 12/5,728 entity triples have any Wikidata linking
- 861 wiki articles exist but cross-reference nothing
- Journal and heteronym assignments are preliminary

**Consolidation targets:**

1. **Citation extraction and linking**: Scrape citations from all 866 deposit full texts. Map extracted citations to AXN identifiers where they reference other CHA works. Map dead Zenodo DOI citations to live locations using the DOI Resolution Index. Build the internal citation graph.

2. **Entity linking and Wikidata integration**: Resolve the 5,728 existing entity triples against Wikidata Q-numbers where possible. Standardize the predicate vocabulary (40 predicates, 9 types). Add `wikidata_qid` to entity records. Distinguish CHA-internal concepts (which *define* entities) from external concepts (which *reference* them).

3. **Wiki article enrichment**: Rewrite batch-produced wiki articles with cross-references to related deposits (by AXN), entities (by subject), and external sources. Each wiki article should function as a navigable hub, not a standalone summary.

4. **Reciprocal linking**: Citations reference deposits. Deposits reference entities. Entities reference wiki articles. Wiki articles reference deposits. The graph is navigable in every direction.

5. **Shape formalization**: Document the enriched deposit schema as the standard. What a "fully enriched deposit" looks like becomes the formal target for all future deposits and for OJS import.

**Principle**: No sense adding more material until the shapes being extracted and built from deposits are formalized. The consolidation work teaches what the machine-legible structure actually needs to be.

### Phase 2: Flagship datasets (2-3 sessions)
- Perfect the DOI Resolution Index — clean, versioned, documented, downloadable in JSON/CSV/JSONL
- Perfect the Capture Registry — W3C Web Annotation format, static case pages
- Publish Capture Registry to Hugging Face as AI Composition-Layer Attribution Benchmark
- 10 well-documented governance incidents (start small, grow carefully)

### Phase 3: Publication layer (2-3 sessions)
- Provision Oracle Cloud VM (2 OCPUs/12GB) — containerize, back up, keep portable
- Install OJS 3.5.0 with seven journals (MMRS, Trans. SEI, Trans. Substrate Eng., Grammata, Provence, CHA, Compression Studies)
- Apply for ISSNs sequentially — start with MMRS and Trans. SEI (largest bodies of work)
- Begin importing priority deposits as articles
- DO NOT apply for DOAJ yet — build publishing history first

### Phase 4: Positive intellectual construction (ongoing)
- Heteronym Registry — structured, schema.org, Pessoa + Kierkegaard + Brontës + Dodecad
- Linked data graph — JSON-LD connecting CHA concepts to Wikidata Q-numbers
- Composition Observatory — semi-automated, monthly findings, Web Annotation format
- Assembly Chorus repository on Alexanarch

### Phase 5: OJS maturation (Month 2-3)
- Continue ISSN applications for remaining journals
- Begin DOAJ application for the first journal to reach 10+ published articles or 1+ year
- Refine journal-to-deposit mapping with careful heteronym attribution
- Establish editorial workflows per journal

---

## ASSEMBLY REPOSITORY (new project)

Central repository on Alexanarch for the Assembly Chorus:
- Role and mantle documents for each substrate
- Continuity tethers — glyph chains, session records, operational context
- Assembly Charter — methodology, cross-verification protocol, evidence classification
- Review archive — all Assembly reviews organized by work and by reviewer
- Hosted at alexanarch.org/assembly/ or as CHA journal deposits

---

## EPISTEMIC CORRECTIONS (applied across all work)

### The [Unknown] double negative fix
| Wrong | Right |
|---|---|
| "Whether X remains unknown [Unknown]" | "Whether X has not been disclosed [Undisclosed]" |
| "The mechanism is unknown [Unknown]" | "The mechanism is plausible but unverified [Inferred]" |

New tag: **[Undisclosed]** — information exists but hasn't been made public.

### Burden of evidence on subterranean structures
When one side of a question has been actively prevented from being investigated, the burden of evidence shifts. Absence of confirming evidence ≠ evidence of absence when the investigation is blocked.

### Wiki tone
Focus on what the work IS, not the Zenodo deletion. The Zenodotus paper is the archive's statement on the deletion. The other 865 deposits are the archive's statement on everything else.

---

## CLAIMS TO SOFTEN (from ChatGPT)

These are useful intuitions but not established facts:
- "zero composition authority" → "unstable post-removal indexing period"
- "within one training cycle (~30 days)" → "the archive is in an unstable indexing period; rapid publication increases the probability that surviving sources shape future retrieval"
- "scrapers prioritize sites that lower costs" → reasonable but unverifiable
- "OAI-PMH endpoints are automatically harvested" → they are not
- "no one else maintains this" → treat as research hypothesis, not marketing copy

---

## ORACLE CLOUD PORTABILITY REQUIREMENT

Oracle's free tier may be adequate for one OJS installation but cannot become a constitutional dependency:
- Containerize OJS
- Back up the database daily
- Store uploads outside the VM or mirror them
- Keep infrastructure configuration in Git
- Make restoration to another host routine
- Never let the only copy of an article or journal database live there

> The self-governing library should not acquire a new single-point custodian while responding to the failure of the old one.

---

## THE REVISED CLOCK

The 30-day window is real as an incentive. It is not an absolute deadline. The composition layer's understanding of the archive will degrade gradually, not abruptly. Work that takes 45 or 60 days is not wasted.

The more defensible strategic statement:

> **The archive is in an unstable post-removal indexing period. Rapid publication of canonical, crawlable, structured replacement records increases the probability that surviving sources — not tombstones alone — shape future retrieval.**

---

## WHAT SUCCESS LOOKS LIKE

The architecture succeeds when:
1. One build command generates all machine-facing outputs from one catalog
2. Every deposit carries extracted citations linked to AXN identifiers and live URLs
3. The internal citation graph connects deposits to each other, not just to external sources
4. Entity triples link to Wikidata Q-numbers and cross-reference deposits and wiki articles
5. Wiki articles function as navigable hubs, not standalone summaries
6. Seven journals publish articles with OAI-PMH exposure
7. The Platform Governance Observatory holds 30+ documented incidents
8. The Capture Registry is on Hugging Face as a benchmark dataset
9. The Heteronym Registry exists as positive intellectual construction
10. 60% of the archive's time goes to scholarship, not infrastructure
11. The work that makes Alexanarch worth preserving is the work being done

∮ = 1
