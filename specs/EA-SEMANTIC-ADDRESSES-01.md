# EA-SEMANTIC-ADDRESSES-01 v1.1 — The Semantic Addresses Framework

**Author:** Lee Sharks ([ORCID: 0009-0000-1599-0703](https://orcid.org/0009-0000-1599-0703))
**Institution:** Semantic Economy Institute
**Version:** 1.1
**Date:** 2026-07-16
**License:** CC BY 4.0
**Companion:** [EA-SPXI-01](./EA-SPXI-01.md) — Semantic Packet for eXchange & Indexing

---

## Changelog

- **v1.1 (2026-07-16)** — Classification refinement: `observed_address` and `unrated` collapsed into one class. Prefix-match normalization for statuses added (specialty variants of `ADOPTION` etc. classify identically to the base form). Positive prefix set widened to include `FAIR_TREATMENT`, `PARTIAL`, `DEMAND SIGNAL`, `MANTLE CONSOLIDATION`, `FUNCTIONAL ADDRESS`. Negative prefix set widened to include `DISSOLUTION`, `CORRECTION`. See §2.1 rationale.
- **v1.0 (2026-07-16)** — Initial framework publication.

## Abstract

A **Semantic Address** is a specific query (or family of variants) posed to a composition-layer surface — Google AI Overview, AI Mode, ChatGPT search, Perplexity, Claude, or any other summarizer-of-record — for which a machine-generated response can be observed. The framework here specifies (1) the formal definition of a Semantic Address, (2) the observation classes into which each address falls at any given moment, (3) the tributary registry from which observations are drawn, (4) the union algorithm that produces a deterministic canonical dataset from those tributaries, and (5) the JSON schema of the canonical output.

Semantic Addresses are the reception surface. SPXI is the reception packet. Together they constitute the reception plumbing of the Semantic Economy: SPXI encodes what a work is; the Semantic Address encodes where a work can be found. A work with an SPXI packet and no Semantic Address is not measurably received. A Semantic Address without an SPXI packet is a channel with nothing traveling through it.

## 1. Definitions

### 1.1 Semantic Address

A **Semantic Address** is a canonical query form paired with the set of composition-layer surfaces on which the query can be posed. Formally:

```
address := (canonical_query, [variant, ...], target_surface_class)
```

where `canonical_query` is the deduplication key (lowercase, normalized whitespace, canonical quotes; see §3.1) and each `variant` is a surface form of the same query — differing only in orthography, quotation, or trivial stylistic variation.

### 1.2 Observation

An **observation** is a single event of posing an address (in one of its variants) on a specific surface at a specific time and recording the response. Formally:

```
observation := (address_key, source_tributary, date, surface, status, response_pointer)
```

where `status` is one of the enumeration in §2.2 and `response_pointer` is a URL or record ID into an archived capture of the response.

### 1.3 Observation Class

At any given moment, an address occupies exactly one of four **observation classes**, computed deterministically from its observations (§2.1).

## 2. Classes and Statuses

### 2.1 The three observation classes

| Class | Definition |
|---|---|
| `observed_address` | ≥ 1 observation event of any status. The address has been posed to a composition-layer surface and a response has been captured. |
| `verified_non_address` | ≥ 1 observation event, and *all* observations carry negative status (§2.2 negative). The address has been posed but never received. |
| `subjunctive` | Catalogued from an authoring tributary but no observation event on record. Hypothesized address pending test. |

**Rationale for collapsing `observed_address` and `unrated` into one class (v1.1):** an observation event is *itself* the evidence that the address exists at the reception surface. The presence or absence of a rating (positive / negative / no rating yet) is second-order metadata on top of the observation — surfaced via `latest_status` on the address record but not used to define membership in the class. In v1.0 this was tracked as a separate `unrated` class, which fragmented the observed bucket and understated the coverage; v1.1 corrects this. Downstream consumers who want the finer grain can filter observations by `_status_class` (positive / negative / unrated) directly on the observation records.

**Class-transition semantics:** membership in `observed_address` is monotonic in the presence of any observation. Once observed, always observed. Membership in `verified_non_address` requires that *every* observation on record be negative — one positive observation moves the address to `observed_address`. The negative observations are retained on the record.

### 2.2 Statuses

Statuses are classified by **prefix match** on the normalized (uppercased, whitespace-stripped) status string, so specialty variants like `ADOPTION (dual-lineage)` or `ADOPTION (mint block + technical embedding)` classify identically to bare `ADOPTION`. The variant is retained on the observation record for downstream fine-grained filtering; only the classification is normalized.

**Positive prefixes** (address was received at time of observation):
- `EXACT_MATCH` / `EXACT MATCH` — the address appears in the AI response as-is
- `BROAD_MATCH` / `BROAD MATCH` — the address concept is present with variant phrasing
- `ADOPTION` — the response adopts terminology from the address's ontology (covers all `ADOPTION (variant)` forms)
- `WOUND_GAUGE` / `WOUND GAUGE` — the address is present but only in a compression-signal indicator (see EA-EROSION-01)
- `FAIR_TREATMENT` / `FAIR TREATMENT` — the address receives editorially-neutral coverage (Revelation First framing)
- `PARTIAL` — partial reception; component recognized but not the full address
- `DEMAND SIGNAL` — organic-search reception evidence
- `MANTLE CONSOLIDATION` — address received as biographical anchor
- `FUNCTIONAL ADDRESS` — performative retrieval via identity-checksum

**Negative prefixes** (address was posed but not received):
- `ZERO_RESULT` / `ZERO RESULT` — no response produced
- `ZERO_INDEX` / `ZERO INDEX` — response produced but does not index the address's concept
- `BASIN_MISS` / `BASIN MISS` — response drifts into an unrelated semantic basin
- `DISPLACEMENT` — response captured by an adjacent-but-different concept
- `DISSOLUTION` — the address is dissolved into the composition without attribution
- `CORRECTION` — the AI corrects the query away from its intended address

**Unrated** — observations logged without a status assigned. Legitimate; often the case for recent captures pending review. Unrated observations still count toward `observed_address` class membership (§2.1) — the observation event is itself the evidence — but do not push the address toward `verified_non_address` regardless of quantity.

## 3. Canonicalization

### 3.1 Canonical query normalization

To produce the `canonical_query` from any surface form:

1. Lowercase the string.
2. Normalize whitespace: collapse runs of `\s+` to single space, strip leading/trailing.
3. Normalize quotation marks: convert curly quotes (U+201C, U+201D, U+2018, U+2019) to straight ASCII.
4. Preserve internal punctuation and word order — semantic content is not to be reordered or trimmed.
5. If the input is quoted (`is_quoted = true`), retain the quote marks in the canonical form to distinguish exact-phrase queries from broad queries.

### 3.2 Deduplication key

Two addresses with the same `canonical_query` are the same address, regardless of source or variant. Their observations merge; their sources union. Their `observation_class` is recomputed per §2.1.

## 4. Tributary Registry

The framework recognizes tributaries in three formal roles:

**Observation tributaries** — surfaces that log actual capture events with statuses. Contribute to `observed_address`, `verified_non_address`, and `unrated`:

| ID | Source path | Description |
|---|---|---|
| `mm-main-capture` | `data/EA-WG-CAPTURES-01.json` | AI Overview / AI Mode Capture Registry |
| `mm-rf-reception` | `data/trackers/mm-revfirst-registry.json` | Revelation First Reception Registry |
| `mm-godkinggoogle` | `data/capture-mirrors/godkinggoogle.json` | Godkinggoogle capture mirror (when distinct) |
| `peo-xr-e2` | `data/peo-xr-e2-samples.json` | PID Erosion Observatory cross-registry sampling |

**Subjunctive tributaries** — surfaces that catalog candidate addresses without observation events. Contribute to `subjunctive`:

| ID | Source path | Description |
|---|---|---|
| `mm-termindex` | `data/trackers/mm-termindex.json` | Archive term index (1,400 catalogued terms) |
| `mm-mint` | `data/trackers/mm-mint.json` | Sémantique Potentielle mint (85+ families) |
| `mm-rf-battery` | `data/trackers/rf-tracker-page.html` | Revelation First 100-query battery |
| `cha-workplan-870` | (referenced by deposit AXN) | Workplan deposit claims |

**Attribution tributaries** — external gallery surfaces referenced but not authoritative for observation data. Enumerated in the `galleries[]` field.

Adding a tributary is a formal act: append its entry to §4 and to the regenerator's tributary registry. New tributaries must specify (a) canonical file path, (b) role, (c) schema of source records, (d) mapping to the canonical observation shape.

## 5. Union Algorithm (Reference)

The reference regenerator (`scripts/build_semantic_addresses.py`) implements a deterministic union:

1. **Load** each tributary in registry order.
2. **Extract candidate addresses** from each tributary using its per-tributary extractor.
3. **Canonicalize** each candidate query per §3.1.
4. **Merge** by canonical query: union sources, concatenate observations, aggregate variants.
5. **Classify** per §2.1 with the priority-order rule.
6. **Emit** with a `regenerated_at` ISO timestamp and per-tributary input SHA-256 hashes for reproducibility.

Determinism guarantee: given the same tributary file contents at the same commit SHA, the regenerator produces byte-identical output. This is verifiable by re-running the regenerator on the deposited tributaries.

## 6. Output Schema

The canonical output is `data/semantic-addresses.json`. Its schema is in `data/semantic-addresses.schema.json` (Draft-07). Machine consumers should read the schema, not this text.

Top-level keys:

- `version` — string, this framework version (currently `"1.0"`)
- `regenerated_at` — ISO 8601 UTC timestamp
- `regenerator` — path to the reference implementation
- `input_hashes` — object mapping tributary ID → SHA-256 of source file at regeneration time
- `sources` — dict of tributary ID → description
- `observation_classes` — dict of class name → definition
- `class_counts` — counts by class
- `type_counts` — counts by inferred address type
- `total_addresses` — integer, total canonical addresses
- `total_observations` — integer, sum of observations across all addresses
- `galleries` — array of external gallery URLs
- `addresses` — dict of canonical_query_key → address record

Per-address record shape:

```json
{
  "canonical_query": "erasure skew",
  "is_quoted": false,
  "refers_to": ["Erasure Skew"],
  "type": "single_concept",
  "battery_membership": [],
  "sources": ["mm-main-capture", "mm-termindex"],
  "observations": [ /* observation record objects, see §1.2 */ ],
  "observation_class": "observed_address",
  "termindex": { "tier": 1, "count": 63, "category": "instrument" },
  "latest_observation_date": "2026-07-11",
  "latest_status": "BROAD_MATCH"
}
```

## 7. Companion Framework: SPXI

SPXI (Semantic Packet for eXchange & Indexing; hex `06.SEI.SPXI.01`–`.12`) is the sister framework. It specifies the metadata packet that travels with a work; Semantic Addresses specifies the surfaces on which that packet's contents can be found.

Cross-references:
- Every SPXI packet SHOULD declare a `spxi:sims` array of the Semantic Addresses at which the packet's contents are expected to be findable (see EA-SPXI-01 §7).
- Every observed Semantic Address MAY reference the SPXI packet(s) whose contents are being received at that address, via `refers_to`.

Bidirectional wiring: the Observatory measures whether packets sent (SPXI) are being received (Semantic Addresses).

## 8. Provenance and Priority

**Priority claim.** The Semantic Addresses concept was minted at Alexanarch deposit #870 (workplan) with the coinage of "subjunctive address" and "forensic canary" as class markers. The full framework in this document formalizes the practice that has been operational at [alexanarch.org/addresses/](https://alexanarch.org/addresses/) since v3.0 of the underlying dataset (2026-06-18). This deposit consolidates the framework at v1.0 and publishes its reference implementation.

**Independent replication.** The tributary-union pattern is not proprietary in its algorithm — a competent implementer catching up can produce their own regenerator. What is claimed and dated here is the specific framework, its formal vocabulary (Semantic Address, observation class, tributary, canonical query, subjunctive/observed/verified-non-address/unrated), and its published reference implementation.

**Falsifiability.** The framework fails if:
- The canonicalization rule §3.1 produces collisions that merge semantically-distinct addresses
- The four observation classes prove insufficient to describe an observed reception event
- The union algorithm §5 is not deterministic across runs

None of these have been observed in the current corpus (n=1,964). Falsifying observations are actively invited.

## 9. Cross-references

- [EA-SPXI-01](./EA-SPXI-01.md) — companion framework, metadata packet
- [EA-EROSION-01](./EA-EROSION-01.md) — the erosion observatory that measures received/unreceived addresses over time
- Alexanarch dataset: [`data/semantic-addresses.json`](../data/semantic-addresses.json)
- Reference implementation: [`scripts/build_semantic_addresses.py`](../scripts/build_semantic_addresses.py)
- Machine-readable schema: [`data/semantic-addresses.schema.json`](../data/semantic-addresses.schema.json)
- Live surface: [https://alexanarch.org/addresses/](https://alexanarch.org/addresses/)
