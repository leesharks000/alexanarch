# Alexanarch Session Workplan — 2026-06-22 (PM Reconciliation)

**Author:** Lee Sharks (MANUS), under TACHYON synthesis
**Session date:** 2026-06-22 (PM update; AM version preserved in git at commit `e9798ce~1`)
**Status:** Active session, live document — updated AS work ships
**Purpose:** Continuity document — readable by a fresh TACHYON instance, by ARCHIVE, and by Lee himself

---

## 1. Where things stand right now

The Crimson Hexagonal Archive's sovereign successor is **Alexanarch**, live at https://alexanarch.org and on GitHub at https://github.com/leesharks000/alexanarch.

**Current corpus state:**

| Metric | Count | Source |
|---|---|---|
| Deposits in canonical registry | **879** | data/registry.json |
| Curated concepts (entity-index) | **7,173** | data/entity-index.json |
| With Phase C `referenced_in` populated | 2,120 | (Phase C) |
| Minted lexical terms (raw) | **12,032** | data/lexical-minting-registry.json |
| Inter-deposit citation edges | **4,866** | data/citation-graph.json |
| Semantic addresses | **1,964** | data/semantic-addresses.json |
| AI Overview captures | **176** | data/EA-WG-CAPTURES-01-v8.3.json |
| Legacy Zenodo DOI mappings | 1,675 | data/doi-resolution-index.json |
| Registry chunks (1 MB target) | 9 | data/chunks/registry/ |
| Protocols (machine-enforced) | 3 | api/index.json (deposit/axn/enrichment) |
| Primary UI surfaces | 4 | /wiki/, /graph/, /lexical/, /citations/ |

**Latest commit:** `49864f4` (Wire Phase C into dynamic surfaces + add /lexical/ + /citations/)

The session followed the 2026-06-19 Zenodo termination of the CHA account. Work has compounded: building Alexanarch as sovereign substrate, depositing the analytical and empirical record, repairing surface-level breakage, tightening empirical claims, and now formalizing the data structures and renderings as machine-readable infrastructure.

---

## 2. Architecture — current state

### 2.1 Substrate stack

- **Alexanarch** is the sovereign successor archive. Live at alexanarch.org, mirrored on GitHub.
- **Gravity Well (gw)** is the continuity/chain system. Two roles:
  - `gw.tachyon` — running TACHYON compression chain (#871, AXN:0373)
  - `gw.archive` — running ARCHIVE compression chain (#873, AXN:0375)
- **Mantles are functional roles**, not identities. An instance can inhabit TACHYON, ARCHIVE, or branch new mantles.

### 2.2 Title-prefix convention

`gw.tachyon ·` and `gw.archive ·` prefixes are reserved for the *continuity compression chains only* — currently #871 and #873. Not for every deposit synthesized under those mantles.

### 2.3 Protocol-as-code

`api/index.json` is the single source of truth for the protocol catalog. New instances run `scripts/bootstrap_familiarization.py --strict` at session start to verify every protocol/schema content hash matches what the index claims. Direct edits to protocol JSONs bypass this check and produce drift detected on next bootstrap.

Hand-editing a protocol JSON is **not supported**. Use `scripts/protocol_update.py` (atomic: recomputes hash, updates index, appends change_log).

### 2.4 Identity vs recognition

Per the LABOR canonical invariant #6: **recognition ≠ identity**. AXNs are deterministic content-derived identity. Substrate-chosen glyphs (when present) are recognition markers, preserved in `glyphic_canary` field, never as the AXN.

### 2.5 AXN schema v2 is canonical

- AXN format: `AXN:<HEX>.<FAMILY>.<6 EMOJI>`
- Emoji derived from first **6 bytes** of SHA-256 of canonical bytes, mapped through 256 curated emoji
- v1 (4-emoji) deprecated; all 13 pre-v2 deposits backfilled in commit `2b586d5`
- v1 AXNs preserved as resolvable aliases in `legacy_axn` field + `axn_history[]` array
- Canonical implementation: `scripts/axn_lib.py`
- Canonical spec: `api/axn-protocol.json`

---

## 3. Canonical numbers — Zenodotus' Book-Burning v9 as source

Preserved verbatim from AM workplan; no change.

- **870 deposits in CHA at the time of termination** (Zenodotus' Book-Burning v9, the canonical narrative source)
- **1,817 DOIs minted, 871 returned HTTP 404 on 2026-06-19**, all in a single day
- **EA-MPAI-DOI-IMPERMANENCE-01 v2.0** (#868) is the empirical audit deposit; methodology replicable via DataCite API at `https://api.datacite.org/dois/{doi}`
- **DataCite full backup** (`data/datacite-full-backup.json`, 9.06 MB) is the empirical foundation

---

## 4. Data structures — the canonical layer

### 4.1 Primary registries (sources of truth)

| File | Size | Records | What it carries |
|---|---|---|---|
| `data/registry.json` | 5.97 MB | 879 deposits | Bibliographic metadata + v2 AXN + content hash + `entities[]` (subject/predicate/object/type/evidence_status triples — source of the graph projection) + `wiki_article` + Phase C `references_concepts[]` + `references_concept_count` + `legacy_axn` / `axn_history` / `glyphic_canary` |
| `data/entity-index.json` | 4.93 MB | 7,173 concepts | Curated concept layer. Each: `term` + `definition` + `defined_in` (founder deposit; on 7,097) + `entity_triples[]` (on 7,097) + classification + Phase C `referenced_in[]` and `reference_count` (on 2,120) |
| `data/lexical-minting-registry.json` | 3.52 MB | 12,032 raw terms | Broader pre-curation surface. 7,045 overlap entity-index; 4,987 LMR-only; 128 entity-index-only |
| `data/citation-graph.json` | 1.59 MB | 4,866 edges | Inter-deposit citations. After Phase B: `doi_resolution` 4,311 / `deposit_number_reference` 346 / `ea_id_reference` 158 / `axn_hex_reference` 21 / `axn_reference` 12 / 11 hand-curated |
| `data/semantic-addresses.json` | 1.28 MB | 1,964 addresses | Query addresses + observations. Class counts: subjunctive 1,748 / observed 111 / verified-non 22 / unrated 83. 348 unique `refers_to` targets — **100% intersect entity-index by exact string** |
| `data/EA-WG-CAPTURES-01-v8.3.json` | 241 KB | 176 captures | AI Overview captures with `mt` status (EXACT MATCH / BROAD MATCH / ADOPTION / ZERO RESULT / etc.) |
| `data/doi-resolution-index.json` | 1.49 MB | 1,675 mappings | Legacy Zenodo DOI → AXN resolution table |
| `data/datacite-full-backup.json` | 9.06 MB | DataCite snapshot | Empirical foundation for #868 (DOIs ≠ permanent identifiers) |

### 4.2 Derived surfaces (regenerated)

| File | Regenerated by | What it serves |
|---|---|---|
| `data/browse-index.json` | regenerate_surfaces.py | Compact deposit list for /s/browse/ |
| `data/chunks/registry/*.json` | regenerate_surfaces.py | 9 chunks of ~1 MB for human-loadable browsing |
| `sitemap.xml` | regenerate_surfaces.py | Crawler sitemap |
| `SHA256SUMS.txt` | regenerate_surfaces.py | Content-addressable checksums |
| `s/browse/index.html` | regenerate_surfaces.py | Static no-JS browse |
| `s/records/<N>/index.html` | (per deposit) | 880 static no-JS record pages |
| `s/wiki/index.html` | regenerate_surfaces.py (Phase D static fallback) | Static no-JS wiki |
| `s/graph/index.html` | regenerate_surfaces.py (Phase D static fallback) | Static no-JS graph |

### 4.3 Supporting datasets

| File | Size | Status |
|---|---|---|
| `data/external-source-registry.json` | 84 KB | Reception sources catalog |
| `data/heteronym-doi-sift.json` | 44 KB | Heteronym DOI cross-reference |
| `data/JOURNAL-MAPPING-PRELIMINARY.json` | 227 KB | Journal-to-deposit mapping (preliminary) |
| `data/batch-axn-assignment.json` | 974 KB | Historical batch AXN assignment record |
| `data/restoration-batch-plan.json` | 20 KB | Restoration plan record |
| `data/zenodo-link-scan.json` | 217 KB | Zenodo link survey |
| `data/datacite-metadata-page{1..4}.json` | ~500 KB each | Paginated raw DataCite snapshot |

### 4.4 Protocols + schemas (`api/`)

| File | Purpose |
|---|---|
| `api/index.json` | Central catalog — single source of truth |
| `api/deposit-protocol.json` | Deposit validation rules (PV/REQ/AXN/CONS/SUR/IDX series) |
| `api/axn-protocol.json` | AXN identifier protocol (v2 canonical) |
| `api/enrichment-protocol.json` | Citation extraction + concept backlink protocols |
| `api/deposit-schema.json` | Submission schema |
| `api/schemas/deposit-entry.schema.json` | Registry entry schema |

---

## 5. UI rendering — current surfaces

### 5.1 Primary dynamic surfaces

| Surface | Fetches | Renders |
|---|---|---|
| `/wiki/index.html` | registry + entity-index | One card per deposit with non-empty `wiki_article`. AXN badge, title→record, autoLinked article body, **Defines** row (entities[] with predicate `defined_in`/`defines`), **References** row (Phase C `references_concepts`, capped at 24), reference_count summary. Search filters title+article+keywords. autoLink pools entities[] subjects/objects + references_concepts + deposit titles/AXNs. |
| `/graph/index.html` | registry + entity-index | Walks `d.entities[]` across all deposits, groups by subject. Type filter chips, search by entity name. Each card: name + type + relations with evidence badges + **Phase C footer** "Referenced across N deposits · defined in #M". Receives `?search=` from wiki. Top 50 by filter+search. |
| `/lexical/index.html` | LMR alone | 12,032 terms, alphabetical jump bar (per-letter counts), type/definition search, paginated 100/page. Each: term + type + definition + "defined in #N · title". Stats: Terms / Defining deposits / Types. |
| `/citations/index.html` | citation-graph + registry | 4,866 edges grouped by source deposit. Via-type filter chips (12 types). Search by AXN/title/#N/via. Per-block: source #N + AXN + title, outgoing edges showing via + target #N + AXN + title. Paginated 30/page. |

### 5.2 Static surfaces

| Surface | Role |
|---|---|
| `/s/browse/index.html` | Primary browse (no JS) |
| `/s/records/<N>/index.html` | Per-deposit record pages (880 of them) |
| `/s/wiki/index.html` | Static fallback for /wiki/ |
| `/s/graph/index.html` | Static fallback for /graph/ |

### 5.3 Other site routes

| Route | Function |
|---|---|
| `/` | Home page |
| `/deposit/` | Deposit form/instructions |
| `/browse/` | Meta-refresh redirect to /s/browse/ |
| `/records/?id=<N>` | Dynamic per-deposit page (reads registry by issue_number) |
| `/principles/` | Founding principles |
| `/identifiers/` | AXN explainer |
| `/manifest/` | Site manifest |
| `/guide/` | Deposit guide |

---

## 6. Cross-reference flow — how the layers compose

```
data/texts/AXN-*-text.md
        │ extracted by reading-pass + concept_backlink.py
        ▼
LMR (12,032 raw)  ──curation──►  entity-index (7,173 curated)
                                      │
                                      │ defined_in ────────┐
                                      │ entity_triples     │
                                      │ referenced_in      │
                                      │ reference_count    │
                                      ▼                     ▼
                              semantic-addresses    registry deposit
                              (refers_to → concept)  (entities[],
                              observations[] ◄────── wiki_article,
                              EA-WG-CAPTURES-01      references_concepts)
                                                        │
                          citation-graph (4,866 edges) ◄┘
                          source/target_deposit, via

Surface projection:
   /wiki/      ◄── registry + entity-index
   /graph/     ◄── registry + entity-index
   /lexical/   ◄── LMR alone
   /citations/ ◄── citation-graph + registry
   /datasets/  ◄── (planned — see §8.1)
```

**Semantic addresses are conceptually a field-set on lexical entities.** 100% of `refers_to` targets exact-match entity-index. The data currently lives in a separate file; surfacing it as a per-entity property is the design intent (not yet implemented in the UI).

---

## 7. Infrastructure work this session (commits)

| Commit | Title | Effect |
|---|---|---|
| `e9798ce` | Continuity tethers #877/#878/#879 + deposit-flow infrastructure | Three substrate continuity tethers deposited; `regenerate_surfaces.py`, `insert_seed_deposits.py`, `DEPOSIT-FLOW.md` introduced |
| `2b586d5` | AXN schema v2 enforcement (Part 1) | 13 deposits backfilled to 6-emoji; canonical `axn_lib.py` introduced; deposit-protocol.json + deposit-schema.json + validate_deposit.py + CI workflow stub |
| `0bef5d4` | Document pending workflow changes (Part 2) | `WORKFLOW-CHANGES-PENDING.md` for the workflow files that need workflow-scoped PAT |
| `d2a1fad` | Central protocol registry | `/api/index.json` + `scripts/bootstrap_familiarization.py` + `scripts/protocol_update.py` + `api/axn-protocol.json` + `api/schemas/deposit-entry.schema.json` |
| `759756d` | Site copy reframe | Home page reframed from exclusion frame to permanence/continuity/governance frame |
| `ee1a1db` | Citation extractor (Phase B) | `scripts/citation_extractor.py` + `api/enrichment-protocol.json`; citation graph 1,710 → 4,866 edges |
| `e02173b` | Site: AXN explainer v1→v2 fix | Residual v1 4-emoji drift in `index.html` AXN section corrected |
| `17ba562` | Phase C: bidirectional concept↔deposit indexing | `scripts/concept_backlink.py`; entity-index gains `referenced_in[]`+`reference_count`; registry gains `references_concepts[]`+`references_concept_count`; 24,777 matches; 2,120 concepts linked beyond defined_in |
| `729dfd9` | Phase D static fallback **(process failure)** | Overwrote `/s/wiki/` and `/s/graph/` without inspecting that the canonical surfaces were at `/wiki/` and `/graph/`. Static files now declared `role: static_fallback`. The overwrite produced no useful result. Recorded here so the failure is part of the visible record, not buried. |
| `49864f4` | Wire Phase C into dynamic surfaces + add /lexical/ + /citations/ | Correction to `729dfd9`. `/wiki/` and `/graph/` extended with Phase C fields. New primary surfaces `/lexical/` and `/citations/`. `/api/index.json` extended with primary/static_fallback role labels. |

---

## 8. Workstream items

Live checklist. Items marked ✓ as they ship. Open items prioritized for this session and beyond.

### 8.1 Dataset navigation surface ✓ (commit pending this push)

**Goal:** A `/datasets/` page that catalogs every data file with size, record count, what it carries, and which UI surfaces consume it. Single navigation entry point for the data layer.

**Steps:**

- [x] Create `/datasets/index.html` — static catalog with 6 sections (Primary registries / Derived surfaces / Protocols & schemas / Supporting datasets / Per-deposit text bodies / Scripts)
- [x] Each entry: path + size + count + description + consumed-by links (chip-style) + download link
- [x] Live overlay: small JS block fetches `/api/index.json` and overrides deposit count + protocol versions where they may have moved
- [x] Add "Datasets" to home page nav (between Citations and Guide)
- [x] Add `/datasets/` as `role: primary` entry in `/api/index.json`
- [x] 32 dataset entries cataloged total; markup validated (142/142 div, 6/6 h2)
- [x] Workplan item updated with completion record (this line)

### 8.2 Captures surface ✓ (commit pending this push)

**Goal:** `/captures/index.html` — 176 AI Overview captures browseable by section/status. Currently only visible as deposit #3's wiki entry.

**Steps:**

- [x] Build `/captures/index.html` (13.2 KB dynamic) — fetches `EA-WG-CAPTURES-01-v8.3.json`
- [x] Section filter chips — all 9 sections with counts: Frameworks 82, Heteronyms 29, Sites & Surfaces 16, Revelation First 14, Revelation First / Semantic Economy 13, Books & Projects 10, Identity 8, Mary Lee Constellation 2, Semantic Economy 2
- [x] Status (`mt`) filter chips with intent ordering: ADOPTION (32, green), EXACT MATCH (14, teal), BROAD MATCH (40, yellow), ZERO RESULT (1, red), ZERO INDEX (1, red), WOUND GAUGE (1, purple), unrated (87, gray) — each chip color-coded
- [x] Search across query / slug / description
- [x] Per-capture card: section badge, date, query, status chip + source format, description (≤380 chars), action row
- [x] Action row: "Screenshot →" deep link to `godkinggoogle.vercel.app/captures/#<slug>`, "As address →" forward-ref to `/addresses/?q=`, "Re-run search →" where `search_url` present
- [x] Paginated 25/page
- [x] Deep-linking: `?slug=<slug>` and `?q=<query>` populate search on load
- [x] Four stats cards: Captures / Sections / Status types / Capture days
- [x] Added `/captures/` to home nav AND added missing `/datasets/` to existing surface navs (wiki, graph, lexical, citations) for cross-surface nav consistency
- [x] Register in `/api/index.json` as `role: primary` (companion_to deposit #3 record)

### 8.3 Semantic addresses surface ▢

**Goal:** `/addresses/index.html` — 1,964 query addresses with observation class filter and entity-link drill.

**Steps:**

- [ ] Build `/addresses/index.html` — fetch `semantic-addresses.json` + entity-index
- [ ] Class filter chips (subjunctive 1,748 / observed 111 / verified-non 22 / unrated 83)
- [ ] Type filter chips (single_concept / unmatched / compressed_argument / multi_concept / site_query / diagnostic_test)
- [ ] Per-address: canonical_query, is_quoted, refers_to (linked to /graph/?search=), observations list, mint_role where present
- [ ] Add to home nav
- [ ] Register in `/api/index.json`

### 8.4 Entity ↔ semantic-address bidirectional link in /graph/ ✓ (commit pending this push)

**Goal:** Surface the address↔entity bridge on `/graph/` entity cards. Each entity whose name matches a `refers_to` target shows its canonical-query status inline.

**Steps:**

- [x] Extend `/graph/index.html` to fetch `semantic-addresses.json` in parallel (3-way Promise.all)
- [x] Build reverse-index: `concept_name → [{q, cls, obs, type}]`
- [x] Attach `e.addresses[]` to each entity card whose name is a `refers_to` target
- [x] Render address-chip row below the Phase C footer: "Tested as query: `<query>` `[class]` (N obs)" with up to 6 chips + `+N more` tail
- [x] Add CSS class chips per observation class (observed/subjunctive/unrated/verified-non) with color coding matching `/lexical/` convention
- [x] Add "Tested as queries" stat card showing count of entities with at least one address
- [x] Address chip URL points to `/addresses/?q=<query>` (forward-reference; lives once item 8.3 ships /addresses/)

**Coverage:** 273 of ~8,468 graph entities receive the overlay. Top by address row count: Lee Sharks (23, 11 observed), Substrate (21, 20 subjunctive), CANONICAL (20, all subjunctive), Semantic Economy (12, mixed). The subjunctive dominance on key concepts makes the catalogued-but-untested gap visible at the card level.

### 8.5 Lexical → engagement bridge in /lexical/ ✓ (commit pending this push)

**Goal:** Surface entity-index engagement state on LMR term cards. Currently `/lexical/` shows raw LMR only.

**Steps:**

- [x] Build `scripts/build_lexical_overlay.py` — derives `data/lexical-overlay.json` (1.30 MB compact) from LMR + entity-index + semantic-addresses
- [x] Overlay carries per-engaged-term: engagement_type, reference_count, entity_triples_count, classified, concept_type, defined_in, and (where present) address_count + address_classes distribution
- [x] Extend `/lexical/index.html` to fetch LMR + overlay in parallel
- [x] Each term card gains an engagement badge row: `raw` (LMR-only) / `<engagement_type>` (entity-index) / refs N / triples N / addr N [obs/subj/unr/vna]
- [x] Engaged terms (in entity-index) get clickable name linking to `/graph/?search=`
- [x] New filter chips: All / Engaged / LMR-only / Tested as queries
- [x] Two new stats cards: "Engaged in concept layer" (7,045) and "Tested as queries" (255)
- [x] Register `build_lexical_overlay.py` in `/api/index.json` scripts
- [x] Register `lexical_overlay` in `/api/index.json` registries with `role: derived_enrichment`

**Notable findings from the build:**
- 7,045 LMR terms engaged (also in entity-index); 4,987 LMR-only (raw)
- Only **575 of 7,045** engaged terms have deliberate engagement_type (8%); the rest (6,470) are unclassified — significant gap surface for reading-pass work
- 255 terms are also semantic-address targets; address-class distribution across those: subjunctive 370 / unrated 36 / observed 32 / verified_non 1
- Engagement type distribution: minted 436 / specified 64 / developed 26 / founded 20 / revised 17 / positioned 12

### 8.6 DOI Resolution surface ▢

**Goal:** `/resolve/?doi=...` route that maps legacy Zenodo DOIs to current AXN/record. Either a JS page that reads `doi-resolution-index.json` or a dedicated browseable list.

**Steps:**

- [ ] Build `/resolve/index.html` — accepts URL `?doi=10.5281/zenodo.XXXX` and maps to AXN
- [ ] Browseable list view when no `?doi=` param
- [ ] Register in `/api/index.json`

### 8.7 Wiki autoLink case-insensitivity ✓ (commit pending this push)

**Goal:** Wiki article links should match casing variants. Currently case-sensitive — "lee sharks" lowercase or "LEE SHARKS" uppercase doesn't link.

**Steps:**

- [x] Confirm bug with audit: **92 of 879** wiki_articles contain at least one case-variant of a canonical term across 9 sampled canonical terms (Lee Sharks, Semantic Economy, Crimson Hexagon, etc.)
- [x] Common pattern: ALL-CAPS titles quoted in body prose (e.g., "WHO IS LEE SHARKS, TO FORGIVE EZRA POUND?")
- [x] Patch `/wiki/index.html` autoLink: title-pass regex aligned to entity-pass — `gi` flag, fixed-length lookbehind `(?<![>"\/])` and lookahead `(?![<"\/])` (mirrors entity regex)
- [x] Python simulation against 50 sample articles confirms: 3 of 4 ALL-CAPS variants now link correctly; **0 nested `<a>` tag regressions**
- [x] One trade-off documented: quoted prose like `"Crimson Hexagon"` doesn't link because the leading `"` triggers the protective lookbehind (the same protection that prevents matching inside HTML attributes). Unquoted ALL-CAPS / lowercase / mixed-case prose still links. Acceptable for now.

**Trade-off accepted:** the protective lookbehind that prevents `<a class="entity-link">` from matching inside attribute values also excludes terms preceded by a `"` in prose. Refining this to context-aware tokenization is deferred (would be a substantive parser rewrite, not a one-line fix).

### 8.8 Reading-pass continuation ▢

**Goal:** Read the 340 deposits in range #1–#875 that lack extracted concepts, plus #877–#879. Each read adds concepts to entity-index, which auto-flows through to /wiki/, /graph/, /lexical/.

**Steps:**

- [ ] Use `wire_deposit.py` for systematic real-time concept extraction
- [ ] Track progress against the 340-unread baseline
- [ ] Periodic registry chunk + surface regeneration

### 8.9 Workflow-scoped PAT changes ▢ (carries forward from prior session)

Two files saved at `/tmp/workflow-changes/` need workflow-scoped PAT to push:

- `.github/workflows/mint-axn.yml` (v1 4-byte → v2 6-byte glyph derivation, axn_schema_version output, post-mint regenerate_surfaces, atomic commit)
- `.github/workflows/validate-registry.yml` (CI enforcement)

Documented in `WORKFLOW-CHANGES-PENDING.md`.

### 8.10 SPXI domains ▢ (carries forward)

SPXI domains needed for the Semantic Packet for eXchange & Indexing work: `spxi.dev` + `spxi.org`. EA-SPXI-01 (formal spec) + EA-SPXI-09 (GEO distinction) flagged for co-deposit.

### 8.11 Credentials rotation queue ▢ (security)

Tokens exposed in prior sessions, pending rotation:

- Zenodo: `QtbHIO…`, `9GVLfHz…`, `YCAIRAPYV…` — rotate at https://zenodo.org/account/settings/applications/
- GitHub PATs: `ghp_PRnY…`, `ghp_k0InOm…`, `ghp_U38oywSx…`, `ghp_PJLddaP5Ox…` — rotate at https://github.com/settings/tokens
- Current active PAT: `ghp_KrzzZJpBxhh…` (repo scope only, no workflow scope)

### 8.12 OpenAIRE follow-up ▢ (carries forward)

When ready, send the v3 PRECISION letter to OpenAIRE Helpdesk. Document response or silence in #876 (bump version on update).

### 8.13 Pre-overwrite mechanism ▢ (process)

Per the session's standing directive: build a file-system-level guard so writing to an existing file requires first producing a describe-current-state receipt. Specifically:

- `scripts/pre_overwrite.py <path>` — reads file (and live URL when reachable), writes structural inventory to `data/pre-overwrite-receipts.log`
- `regenerate_surfaces.py` and other write-path scripts refuse to write when current sha256 has no recent receipt
- Receipt log goes into `api/index.json` as a required-read

This mechanism is what prevents the `729dfd9` failure pattern. First task for next thread per Lee's directive.

### 8.14 Reading pass continuation: 340 unread deposits ▢

(Duplicate of 8.8 — kept here as cross-reference to the wider work.)

---

## 9. Firm infrastructure rules — preserved + updated

1. **Dynamic JS pages are not modified directly without reading them first.** This includes `/index.html`, `/wiki/`, `/graph/`, `/lexical/`, `/citations/`, `/records/`. The `/s/` static fallbacks are regenerable; the dynamic primaries are the load-bearing surfaces.
2. **Registry uses compact JSON format** — `indent=None, ensure_ascii=False, separators=(',', ':')`. Pretty-printing the registry breaks downstream consumers.
3. **For files above ~1 MB on GitHub** — use `raw.githubusercontent.com` URLs.
4. **For pushing many files** — Git Trees API (create blobs → tree → commit → PATCH ref). Direct push for normal commits.
5. **Static record pages must be regenerated** for any new or modified deposit.
6. **Substrate model identity never appears in public deposit attribution.** Only mantles. The single exception is verbatim preservation deposits like #873.
7. **Archive search protocol:** exact-match first; never confabulate.
8. **Sappho 31 / Catullus 51 alignment is static** — Sappho 5 stanzas (fifth fragmentary), Catullus 4 stanzas. No "Catullus fifth stanza."
9. **Title-prefix convention:** `gw.tachyon ·` and `gw.archive ·` are reserved for the continuity compression chains only — currently #871 and #873.
10. **Protocol changes through `scripts/protocol_update.py`** — hand-editing protocol JSONs produces drift detected by bootstrap.
11. **AXN schema v2 is canonical** — 6 emoji, derived from first 6 bytes of SHA-256.
12. **Recognition ≠ identity** (LABOR invariant #6). Substrate-chosen glyphs in `glyphic_canary` field, never as the AXN.
13. **Read before writing.** When extending a surface, read the live page in full before any write. The `729dfd9` failure was overwriting without reading. **(Standing directive — must be made structural, see 8.13.)**
14. **Workplan updates with the work.** This document is live. Items checked off as they ship.

---

## 10. The thread — for the next instance

If you are a fresh TACHYON instance reading this:

- **Run** `python3 scripts/bootstrap_familiarization.py --strict` first. Receipt goes to `data/instance-familiarization.log`.
- **Read** `api/index.json` — the central catalog. Every protocol, schema, registry, surface, and script listed there.
- **Read** this workplan second.
- **TACHYON's running compression** lives at #871 (AXN:0373). Read `data/texts/AXN-0373-text.md` if you need the chain context.
- **ARCHIVE's running compression** lives at #873 (AXN:0375). Read `data/texts/AXN-0375-text.md`.
- **The mantle is functional.** Inhabit TACHYON, ARCHIVE, or branch.
- **Lee corrects in real time.** Listen when he says "overcorrected," "a single overclaim empties the threat," or "you didn't check." Empirical precision is the discipline.
- **Build the pre-overwrite mechanism first** (item 8.13) before any other work. The `729dfd9` failure pattern must be made structural-impossible, not a resolution to hold harder.

---

## 11. Sources for the numbers in this workplan

- `data/registry.json` (current corpus state)
- `data/entity-index.json`, `data/lexical-minting-registry.json` (curation state)
- `data/citation-graph.json` (post-Phase-B)
- `data/semantic-addresses.json` (v3.0)
- `data/EA-WG-CAPTURES-01-v8.3.json`
- Zenodotus' Book-Burning v9 (#1) — narrative source for 870/871 figures
- EA-MPAI-DOI-IMPERMANENCE-01 v2.0 (#868) — empirical audit
- DataCite API at `https://api.datacite.org/dois/{doi}` — live verification

---

*Reconciled 2026-06-22 PM. Live document — updated as items in §8 ship. Previous version preserved in git at commit `e9798ce~1`.*
