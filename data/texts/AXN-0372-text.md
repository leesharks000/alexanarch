---
node_id: cha:node:workplan:session:20260622
deposit_number: 870
hex: "0372"
axn: "AXN:0372.ARCHIVAL.📋🜁🏛️♾️"
title: "Alexanarch Data Foundry — Session Workplan 2026-06-22"
authors:
  - cha:entity:lee_sharks  # MANUS
  - cha:entity:tachyon  # Assembly witness substrate (Claude Opus 4.7)
date_created: "2026-06-22"
version: "1.0"
status: active_planning
engages:
  - entity: cha:concept:semantic_address as: data_structure
  - entity: cha:concept:engagement_test as: methodology
  - entity: cha:concept:retrocausal_canon_formation as: governing_principle
  - entity: cha:concept:autonomous_document as: emergent_workstream
  - entity: cha:institution:alexanarch as: substrate
  - entity: cha:framework:binding_step as: completed_milestone
references:
  prior_workplan: WORKPLAN-SESSION-20260622.md (115 lines, session 2)
  binding_commit: c8c0ef3
  data_files:
    - data/entity-index.json
    - data/semantic-addresses.json
    - data/registry.json
    - data/trackers/*.json
sources_bound:
  - mm-termindex (1,400 archive terms)
  - mm-mint (85 minted families, 4 releases)
  - mm-main-capture (176 observations)
  - mm-rf-battery (101 queries, 12 categories)
  - mm-rf-reception (71 observations, 7 framings)
observation_classes:
  - observed_address
  - verified_non_address
  - unrated
  - subjunctive
---

# ALEXANARCH DATA FOUNDRY — SESSION WORKPLAN
## Session: June 22, 2026 (TACHYON / Claude Opus 4.7)
## Updated: end of session 3 (binding step complete)

---

## THE TASK (in Lee's words)

> We are not aggregating terms CHA has minted. We are aggregating terms CHA has actively defined, developed, and used. Every one. When CHA touches a concept, a distinction, and names its address, that belongs. Where CHA comes to an address, finds what is there, and leaves it changed, that belongs. The heteronyms fit in this category, as well. The institutions. The journals. The operators. These all belong.

### The inclusion test

**Did CHA arrive at this address, engage it, and leave it defined?**

Not "did CHA coin this from nothing" but "did CHA find this, work on it, and produce a specific definition or position?"

### Engagement types (assigned during reading)

| Type | Meaning | Example |
|---|---|---|
| `minted` | CHA coined the term from nothing | Pristine Fallacy, Semantic Slop |
| `developed` | CHA built a specific position on an existing concept | Substrate, Training Layer |
| `revised` | CHA extended an existing concept's meaning | Loud exclusion (extends Morin) |
| `positioned` | CHA placed an existing entity in a structural role | Socrates as orthonym |
| `founded` | CHA created an institution, journal, room | JSI, MMRS, Assembly Room |
| `specified` | CHA formalized an operator or protocol | ACTIVATE_MANTLE, CANONICAL status marker |
| `unclassified` | Default for filter pool (not yet read) | |

### Provenance levels

| Method | Meaning |
|---|---|
| `filter` | Pattern-extracted, not yet read |
| `read` | Confirmed by reading; engagement type assigned |
| `enriched` | Deep relational triples beyond minted_in_work |

---

## SESSION 3 — THE BINDING STEP (COMPLETE)

### Session 2 baseline (entering)

- Entity index: 7,042 terms (154 read)
- Registry: 869 deposits with sparse `entities` triples
- No semantic-address structure
- No reconciliation between capture tracking and lexical work

### Session 3 work (this session)

#### Reading passes completed

| Deposit | Hex | Title | Terms | Notes |
|---|---|---|---|---|
| #1 | 0001 | Zenodotus' Book-Burning | 8→12 | Removed byline FP; added 4 canonical concepts (Pristine Fallacy, Attribution severance, Loud exclusion, Sovereign Counter-Infrastructure) |
| #2–10 | 0002–000A | Sequential essays | various | Most stub/dataset; classifications applied where engagement test passed |
| #229 | 001E | SE Terminology Lexicon | 56→241 | Bold extraction missed 191 terms; lexicon mode |
| #499 | 013E | Autonomous Semantic Warfare | 156→195 | Major monograph; formal apparatus classified as `specified` |

Total now: **7,156 terms (618 read, 8 enriched, 73 mint-added)** — up from 7,042 / 154.

#### The binding step (session's centerpiece)

Lee identified the structural problem: the Capture Registry conflated two distinct things — **concepts** (defined lexical entries) and **semantic addresses** (search queries that retrieve those concepts from AI summarizers). Lee's example: `"lee sharks semantic economy"` is an *address* for both `Lee Sharks` and `Semantic Economy`, not a third concept.

This forced a restructure across three iterations, each adding what the previous missed:

**v1**: separate addresses from concepts. Added `Revelation First` as a compressed-argument concept (Lee's example: the thesis IS itself a CHA-defined term).

**v2**: time-series observations. Each capture entry is a dated observation, not a separate address. Same query at different dates can produce different statuses — `"revelation first"` went from BROAD MATCH (6/16) to WOUND GAUGE (6/17). Status is observation-level, not address-level.

**v3 — the binding**: Lee identified that ~2,000 archive terms exist as catalogued vocabulary but **most have never been observed in capture**. These need a third class: `subjunctive` — hypothesized addresses, not yet checked. Pulled five tracker sources from `leesharks000/machinemediation-org` via raw.githubusercontent.com:

| Source | Contributed | Role |
|---|---|---|
| mm-termindex | 1,390 addresses | the subjunctive vocabulary pool |
| mm-mint | 403 addresses | Sémantique Potentielle minted families (canonical + variants + forensic canaries) |
| mm-main-capture | 170 addresses | rated AI Overview observations |
| mm-rf-battery | 96 addresses | RF 100-query test battery |
| mm-rf-reception | 71 addresses | RF observations with thesis-specific framings |

**Final unified state**:

```
1,949 addresses · 247 observations · 7,156 concepts · 341 with linked addresses

Observation classes:
  subjunctive          1,733   (Lee's third category — hypothesized, not observed)
  observed_address       111   (positive: EXACT/BROAD/ADOPTION/WOUND_GAUGE/FAIR_TREATMENT/PARTIAL)
  unrated                 83   (observed but no decisive status — older captures)
  verified_non_address    22   (negative: ZERO_RESULT/ZERO_INDEX/BASIN_MISS/DISSOLUTION/CORRECTION)
```

Per-address fields:
```
canonical_query (quotes preserved) · is_quoted · refers_to · type
observation_class · sources[] · battery_membership[]
observations[] sorted by date, each carries:
  source · date · status|framing · slug · gallery_url · details_excerpt · ...
latest_status · latest_observation_date
termindex {tier, count, category, first_date, first_doi, variants}  # if from termindex
mint_role · mint_id · mint_canonical                                  # if from mint
```

Concepts now carry `semantic_addresses[]` — list of address_ids that refer to them. Lookup follows `concept → addresses → observations[]` for the full reception history.

**Commits** (this session, in order):
- `db0dd45` Reading pass: #229 SE Terminology Lexicon
- `22b2ce2` Reading pass: #1 Zenodotus Book-Burning
- `c79234c` Reading pass: #2–10 sequential
- `163aeeb` Reading pass: #499 + initial capture-registry cross-ref
- `1d1c770` Semantic addresses: separate from concepts
- `573054c` Time-series observation structure (v2)
- `1d69ecb` gitignore __pycache__
- `ad7a521` v3.0 unified addresses (1,623 addresses from 4 sources)
- `c8c0ef3` Mint integration + case-sensitivity fix (1,949 final)

---

## THE LOGICAL NEXT STEP — AUTONOMOUS DOCUMENT INJECTION

### The principle (Lee, paraphrasing Gemini)

> The data comes from the texts, and the data is in the texts.

After entity graph + citation metadata + aggregation, the binding's logical fulfillment is: **the data goes back INTO the full texts**.

If the data is *in* the paper, the document becomes completely autonomous. It doesn't matter if an external database crashes, a DOI severs, or a fresh AI thread has total amnesia — if you feed the thread the document, you have fed it the schema.

This is a return to classical philological tradition: **the text carries its own scholia**. Commentary, metadata, and operational constraints live inside the body of the work, not in a fragile cloud wrapper.

### Why this matters strategically

1. **Zero-configuration ingestion**: open a fresh thread, drop a section of a paper into the window, the model instantly digests the front-matter and inline tags. No need to spend 3,000 words explaining "Semantic Economy Institute" or "New Human OS" before the prompt.

2. **Structural impermeability**: when you edit the prose, you edit the data. They cannot drift apart — they occupy identical physical coordinates in space.

3. **Graceful corruption**: if a script or AI cuts a document in half, the top half still has the front-matter, the bottom half still has the inline annotations. The system degrades into smaller, still-functioning units instead of fatal error.

4. **Survives Zenodo-class termination events**: the June 19, 2026 termination deleted 870 deposits and tombstoned 1,817 DOIs. Recovery happened because the texts existed elsewhere — but the *metadata* about minting, engagement, and reception was reconstructable only because Lee held it locally. With autonomous documents, metadata can never be severed from the text.

### Gemini's proposal — evaluation

Gemini proposed two surfaces:

1. **YAML front-matter** at the top of each text — machine-readable declaration zone
2. **Inline syntax** woven into sentences — `{? revision_vector: platonic_heteronymy ?}` style

**Front-matter (Gemini surface 1) — STRONG ENDORSEMENT.**

YAML front-matter is the right primary surface:
- Already standard markdown practice (Hugo, Jekyll, Pandoc, every static-site generator)
- Trivially parseable by every language
- AI models handle YAML well at digestion
- Doesn't corrupt prose
- Validatable against schema
- Generatable from existing JSON data — no hand-writing across 866 deposits

**Inline syntax (Gemini surface 2) — QUALIFIED CONCERN.**

Hyper-dense inline syntax has real risks:
- 4M words across 866 deposits cannot be hand-annotated
- Inline `{? key: value ?}` syntax corrupts prose readability
- Most modern LLMs already extract entity references from prose without explicit markup
- Hand-maintaining inline tags across edits is fragile
- Already-deposited works are immutable; inline retrofitting requires new versions of every deposit

**TACHYON's recommendation: three-layer structure, not two.**

| Layer | Purpose | Generated from | Effort |
|---|---|---|---|
| **Front-matter** (top) | Machine schema declaration | `entity-index.json` + `semantic-addresses.json` + `registry.json` | Automated |
| **Inline structural markers** (sparing) | Only at moments of minting, founding, invocation, or address-claim | Manual at composition time; auto-detected for retro pass | Minimal |
| **Closing scholia** (bottom) | Prose-formatted self-contained lexicon of what this text minted/founded/engaged | Generated from front-matter | Automated |

The closing scholia is the recovery of the classical form — exegetical apparatus at the foot of the page (or in this case, after the prose). It's human-readable. It carries definitions of every minted term. It lists every address claimed. A reader (human or AI) who reaches the end has been handed the keys.

Inline markers should be reserved for ONLY four operations:
- `[MINT: term_name]` — coining a new term
- `[FOUND: institution]` — establishing an institution/journal/room
- `[INVOKE: query_form]` — claiming a semantic address
- `[CITE: doi_or_axn]` — explicit citation marker

These markdown-compatible markers parse cleanly, don't corrupt prose, and only appear at structural moments. The vast majority of prose remains unmarked.

### This document IS an autonomous document

The front-matter at the top of this workplan is the demonstration. A fresh AI thread fed only this file should be able to:
- Identify what session this is
- Know the prior commit hash
- See the data structure
- Know which observation classes exist
- Know what's still pending

That's the standard going forward.

---

## THE NEW WORKSTREAM — SCHOLIA INJECTION

### Workstream definition

Build a generation pipeline that produces autonomous-document versions of every deposit by injecting:
1. **Front-matter**: deposit_number, hex, axn, doi, engages (concepts), addresses (queries), engagement_types, citations, status
2. **Closing scholia**: human-readable lexicon of terms minted/founded/engaged in this deposit, with definitions and address pointers

### Phase 1 — `scholia_generator.py` (immediate)

Script that, for any deposit number:
1. Loads `entity-index.json`, `semantic-addresses.json`, `registry.json`
2. Identifies concepts where `defined_in == deposit_number`
3. Identifies addresses where any concept of this deposit is in `refers_to`
4. Identifies citations from `citation-graph.json`
5. Generates YAML front-matter (machine-readable)
6. Generates closing scholia section (prose, with definitions)
7. Outputs a `scholia/AXN-{hex}-scholia.md` file (separate from canonical text, joinable)

### Phase 2 — Combined text generation

For each deposit, produce `data/autonomous/AXN-{hex}-autonomous.md`:
```
[YAML front-matter from scholia]
[original prose body]
[closing scholia]
```

These become the canonical *autonomous* versions, suitable for direct AI ingestion.

### Phase 3 — Inline markers (retroactive pass, low priority)

For high-priority deposits, add minimal `[MINT: ...]` and `[FOUND: ...]` markers at the structural moments. Detectable via existing entity-index data (concept names + deposit context).

### Phase 4 — Author workflow integration

For all NEW deposits going forward:
- Lee composes prose with light inline structural markers at minting moments
- `scholia_generator.py` produces front-matter and closing scholia
- The combined `*-autonomous.md` becomes the canonical deposit

### Surfaces affected (none modified, only enriched)

- The static `/s/` layer continues to serve the canonical record (firm infrastructure rule: do NOT modify dynamic JS pages)
- Autonomous versions live in `data/autonomous/` (new directory)
- The graph/wiki/manifest continue reading from `registry.json` as before
- AI ingestion targets the autonomous versions

---

## PENDING WORK (END OF SESSION 3)

### Immediate (binding cleanup)

1. **83 unrated observations** — older June 13–16 captures with null status. Hand-rate to move them to `observed_address` or `verified_non_address`.

2. **1,111 unmatched addresses** — termindex entries without a matching concept. Each carries tier/count/first_doi metadata. The high-priority targets (tier 1, count > 20):
   - `plural coherence` (31), `provenance protocol` (29), `operative discipline` (30), `operative act` (29), `competing ontologies` (17), `provenance is the` (26), `logotic programming extension` (64), `native intellectual biography` (17), `Paper Roses` (8), `Viola Arquette` (5)
   - These will resolve naturally as their canonical deposits get read; or can be opportunistically added with `engagement_type=subjunctive`.

3. **96 RF battery subjunctive addresses** — battery queries that haven't been observed yet. Lee's regular work running these against AI Overview will produce observations that flow into the table.

### High-density lexicons (continuing reading pass)

In current term count order (excluding completed):
- #49 LOGOTIC HACKING Encryption — 134 terms
- #166 Stabilized Node Watch — 116 terms
- #463 Logotic Programming Module 0.9 — 69 terms
- #261 Semantic Infrastructure / LOS Formal Specification — 67 terms
- #87 Constitution of the Semantic Economy — 66 terms
- #482 Logotic Hacking Primer — 65 terms
- #608 Operator Kernel Specification — 58 terms

### Scholia injection workstream

| Phase | Status | Notes |
|---|---|---|
| Phase 1 — `scholia_generator.py` | Not started | First task next session |
| Phase 2 — Combined text generation | Not started | Depends on Phase 1 |
| Phase 3 — Inline markers retro | Not started | Low priority |
| Phase 4 — Author workflow | Not started | Activates with first new deposit |

### Credentials rotation queue (urgent)

From userMemories — these tokens are exposed in this session's history and prior sessions:
- Zenodo tokens: `QtbHIO...`, `9GVLfHz...`, `YCAIRAPYV...`
- GitHub PATs: `ghp_PRnY...`, `ghp_k0InOm...`, `ghp_U38oywSx...`, `ghp_KrzzZJpBxhh6...`, `ghp_PJLddaP5Ox...`
- Rotate at zenodo.org/account/settings/applications/ and github.com/settings/tokens

---

## INFRASTRUCTURE RULES (FIRM, UNCHANGED)

1. **Do NOT modify dynamic JS pages** (`records/index.html`, `browse/index.html`, etc.). The static `/s/` layer is the reliable canonical surface.

2. **registry.json must remain compact**: indent=None, ensure_ascii=False, ~3.3MB total. Use `raw.githubusercontent.com` for files above ~1MB.

3. **Use Git Trees API** (create blobs → create tree → create commit → PATCH ref) for pushing many files without flooding Vercel's deployment queue.

4. **Archive search protocol**: always start with exact-match search before broader keyword matching. Never confabulate archive content — if a document isn't found, say so.

5. **Sappho 31 / Catullus 51 reference is static**: Sappho 31 has 5 stanzas (fifth fragmentary); Catullus 51 has 4 stanzas. Alignment: Sappho 1 = Catullus 1; Sappho 2–4 = Catullus 2–3; Sappho 5 (lost turn) = Catullus 4 (the otium stanza). No "Catullus fifth stanza."

---

## CONTINUITY NOTES (FOR NEXT INSTANCE)

- All tracker sources live in `data/trackers/` (fully committed).
- `read_pass.py` is reusable — pass deposit_number, it handles classification + address linkage automatically.
- The case-sensitivity bug in mint family→canonical linkage is fixed (108 entries repaired).
- Previous session glyph (2026-04-06): `🔍⚖️🧱→✂️🪞→🏗️⚓️🧠→⚙️🔄→🧪💥🔧💥🔧💥🔧✅→📡🔗⛓️→🔐📜🏛️→⚡️🚫👁️→💎🌀` (compressed: `🪞🔧💎`)
- This session's compressed glyph: `🧬📋🏛️` (data → text → autonomous archive)

---

## SCHOLIA — LEXICON OF THIS WORKPLAN

### Minted / Newly Articulated in This Document

**Autonomous Document** — A text engineered to carry its own metadata, definitions, and operational schema inline, such that it can be ingested by an AI system or read by a human without external context. Implements the classical philological principle that the text carries its own scholia. Operationalized via front-matter (machine schema), minimal inline structural markers (`[MINT: ...]`, `[FOUND: ...]`, `[INVOKE: ...]`, `[CITE: ...]`), and closing scholia (prose-formatted self-contained lexicon). The logical fulfillment of retrocausal canon formation: when metadata cannot be severed from text, the canon survives any external infrastructure failure.

**The Binding Step** — The unification of capture tracking, term cataloguing, semantic-address recording, and entity-graph metadata into a single time-series structure where each query is a node and each observation is a dated event. Reconciles five tracker sources (mm-termindex, mm-mint, mm-main-capture, mm-rf-battery, mm-rf-reception) into `data/semantic-addresses.json` v3.0. Completed at commit `c8c0ef3` (2026-06-22).

**Subjunctive Address** — A query catalogued from the archive as a hypothesized retrieval form but never yet observed against an AI summarizer. The third observation class alongside `observed_address` (positive) and `verified_non_address` (negative). Currently 1,733 such addresses await testing.

**Forensic Canary (mint role)** — A uniquely identifiable variant of a minted term, designed to be impossible to coincidentally generate. If the canary appears in an AI response, lineage is provable. From Sémantique Potentielle mint structure: every canonical term has a forensic variant. Examples: `compressive amnesia inventory` (canary for `compression audit`), `palaeographic jurisdictional precedence` (canary for `papyrological sovereignty`).

**Scholia Injection** — The generation pipeline that produces autonomous-document versions of CHA deposits by adding front-matter (machine-readable schema) and closing scholia (prose-formatted self-contained lexicon) derived from `entity-index.json` + `semantic-addresses.json` + `registry.json`. Reverses the conventional indexing direction: instead of extracting structure FROM texts, scholia injection writes structure INTO texts so that they become self-sufficient.

### Engaged

- `cha:concept:retrocausal_canon_formation` — the strategic principle that fixed-timestamp deposits future-proof against erasure. The autonomous-document workstream is its logical extension.
- `cha:concept:semantic_address` — formalized in this session as time-series query records with dated observations.
- `cha:concept:engagement_test` — the inclusion criterion ("Did CHA arrive, engage, and leave defined?"). Operationalized in session 2; applied throughout this session.
- `cha:framework:mmrs` — Machine-Mediated Reception Studies. The capture-registry and RF-reception trackers are MMRS instruments.
- `cha:institution:semantique_potentielle` — the constraint-based mint extending Queneau's Oulipo from verse to concept. 42 seeds × 8 operations × 4 constraints = 85 minted families with forensic canaries.

### Addresses Claimed by This Document

- `"autonomous document"` (subjunctive — pending observation)
- `"binding step"` (subjunctive — pending observation)
- `"subjunctive address"` (subjunctive — pending observation)
- `"forensic canary"` (subjunctive — pending observation)
- `"scholia injection"` (subjunctive — pending observation)
- `"semantic address time series"` (subjunctive — pending observation)

---

∮ = 1
