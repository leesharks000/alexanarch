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

### One journal, seven sections — not seven journals

**Alexanarch Transactions** — a single OJS journal with sections:
- Machine-Mediated Reception Studies
- Semantic Economy
- Substrate Engineering
- Grammata (Operative Philology)
- Provenance Studies
- Compression Studies
- Crimson Hexagonal Archive

A section becomes an independent journal only when it has: a distinct external editorial body, a sustainable submission stream, enough material to publish independently, and a reason to require its own ISSN. Until then, one journal, one ISSN, one editorial workflow.

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

### Phase 2: Flagship datasets (2-3 sessions)
- Perfect the DOI Resolution Index — clean, versioned, documented, downloadable in JSON/CSV/JSONL
- Perfect the Capture Registry — W3C Web Annotation format, static case pages
- Publish Capture Registry to Hugging Face as AI Composition-Layer Attribution Benchmark
- 10 well-documented governance incidents (start small, grow carefully)

### Phase 3: Publication layer (2-3 sessions)
- Provision Oracle Cloud VM (2 OCPUs/12GB) — containerize, back up, keep portable
- Install OJS 3.5.0 with ONE journal: Alexanarch Transactions, 7 sections
- Apply for 1 ISSN
- Begin importing priority deposits as articles
- DO NOT apply for DOAJ yet — build publishing history first

### Phase 4: Positive intellectual construction (ongoing)
- Heteronym Registry — structured, schema.org, Pessoa + Kierkegaard + Brontës + Dodecad
- Linked data graph — JSON-LD connecting CHA concepts to Wikidata Q-numbers
- Composition Observatory — semi-automated, monthly findings, Web Annotation format
- Assembly Chorus repository on Alexanarch

### Phase 5: OJS expansion (Month 2-3)
- If VM capacity allows, promote sections to independent journals as they earn it
- Apply for additional ISSNs
- Begin DOAJ application for Alexanarch Transactions (requires 10+ articles or 1+ year)
- Add journals only when a section has: distinct editorial body, submission stream, independent material

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
2. Alexanarch Transactions publishes articles with OAI-PMH exposure
3. The Platform Governance Observatory holds 30+ documented incidents
4. The Capture Registry is on Hugging Face as a benchmark dataset
5. The Heteronym Registry exists as positive intellectual construction
6. 60% of the archive's time goes to scholarship, not infrastructure
7. The work that makes Alexanarch worth preserving is the work being done

∮ = 1
