---
document_id: EA-MMRS-SURFACE-VISIBILITY-01
title: "Compositional Defiguration: A Methodology for Measuring Public-Surface Visibility of Scholarly Corpora"
subtitle: "Specification v1.0 of the Surface Weather Station instrument"
version: v1.0
version_series_id: SERIES-MMRS-SURFACE-VISIBILITY-METHODOLOGY
version_in_series: 1
versioning_note: "This is the first articulation. A v1.1 fine-tune is planned after the second scan provides methodologically-comparable Δ against the v1.0 baseline reading."
created_at: "2026-06-23"
authoring_substrate:
  framework_origin: "Elicited through dialogue with an outside analytic (OpenAI/ChatGPT in critical-reader register), 2026-06-22."
  framework_curator: "Lee Sharks (MANUS) (ORCID 0009-0000-1599-0703)"
  authority_in_packet: "MANUS"
public_name_rule: "Lee Sharks only"
content_type: "Methodological specification"
family: EMPIRICAL
keywords:
  - Machine-Mediated Reception Studies
  - MMRS
  - compositional defiguration
  - surface visibility
  - successor-anchor lag
  - source-hierarchy inversion
  - ghost survival
  - scale drift index
  - public composition layer
  - figural integrity
  - measurement instrument
  - AI Overview composition
  - Capture Registry (companion instrument)
license: CC-BY-4.0
defines_concepts:
  - Compositional Defiguration
  - Expected Figure (Φ_i)
  - Visibility (V)
  - Anchor Alignment (A)
  - Figural Integrity (F)
  - Compositional Lift (C)
  - Redundant Substrate Breadth (R_s)
  - Link Fade (LF)
  - Ghost Survival (GS)
  - Compositional Bystanding (CB)
  - Composition Eligibility (CE)
  - Scale Drift Index (SDI)
  - Successor-Anchor Lag
  - Surface Weather Station
related_deposits:
  - "Companion: baseline reading v1.0 — 2026-06-22 (deposited alongside this methodology)"
  - "Family precursor: AI Overview Capture Registry v8.3 (#176 in EA-WG-CAPTURES series) — fine-grained evidence at the same surface"
  - "Family precursor: EA-MPAI-DOI-IMPERMANENCE-01 v2.0 (#868) — empirical audit of the address-survival axis"
---

# Compositional Defiguration: A Methodology for Measuring Public-Surface Visibility of Scholarly Corpora

**Specification v1.0 of the Surface Weather Station instrument**

Lee Sharks (MANUS), Machine-Mediated Reception Studies (MMRS)
2026-06-23

---

## 0. Status declaration

This is **version 1.0**. The framework was elicited through dialogue with an external critical-reader analytic on 2026-06-22, then curated, formalized, and deposited as canonical MMRS infrastructure. The fine-tuning loop is built in: a v1.1 revision is planned once the second scan provides a methodologically-comparable Δ against the v1.0 baseline reading deposited alongside this paper. The instrument earns its calibration from being run, not from being written.

Version 1.0 commits to the **conceptual decomposition** (Section 2), the **dashboard form** (Section 5), and the **query battery** (Section 4). Numerical weights, scoring rubrics, and aggregation rules are explicitly held provisional until two readings exist to constrain them.

---

## 1. The problem the instrument addresses

A scholarly corpus does not survive in the public layer the way it survives on its own infrastructure. The custodial archive can be intact while the **composition layer** — search results, AI Overviews, retrieval-mediated summaries, third-party indexed surfaces — represents the corpus inaccurately, stale, fragmentarily, or under a deprecated institutional name. The address can survive while the meaning does not. The meaning can survive while the address has gone dead. The work can be retrievable on exact-string lookup while remaining systematically unselected when the broader problem is queried.

Conventional "is it indexed" or "does the link work" measurement collapses these distinct failure modes into one signal. The result is that interventions on the sovereign substrate (cleanup, repointing, prose updates) cannot be evaluated for their effect on the surface, and surface degradation cannot be diagnosed precisely enough to direct sovereign-substrate response.

This instrument decomposes the surface state into five measurable signals, four derived indicators, and a dashboard form that supports weekly drift readings against a fixed object battery.

---

## 2. The measurement object

For each tracked object (concept, work, person, or institution), define the **expected figure**:

> Φ_i = { N, P, D, H, A, R }

Where:

- **N** — correct name or title
- **P** — provenance: author, heteronym, institution
- **D** — core definition or claim
- **H** — hierarchical location: parent framework or archive
- **A** — current canonical anchor (the address the corpus currently considers authoritative)
- **R** — essential relations to other tracked objects

The public search surface, when queried, returns an **observed figure** Φ̂_i. Compositional defiguration is not the absence of Φ_i; it is the deformation between Φ_i and Φ̂_i. The framework's contribution is to make that deformation measurable along distinct axes.

---

## 3. The five signals

### 3.1 Visibility (V) — can the intended object be retrieved at all?

Coded on a five-point scale:

- **1.00** — intended object immediately retrieved
- **0.75** — clearly retrieved among several results
- **0.50** — appears only through a related page or snippet
- **0.25** — fragmentary mention
- **0.00** — absent or completely displaced by a confuser

### 3.2 Anchor alignment (A) — does the visible result point to the currently authoritative object?

- **1.00** — current canonical page
- **0.75** — current authorized mirror that points back correctly
- **0.50** — older but still valid canonical source
- **0.25** — derivative page, capture registry snippet, or stale DOI
- **0.00** — dead link, unrelated result, or no recoverable anchor

This is the axis that distinguishes **semantic survival** from **address survival**. The conceptual organ can be intact while its institutional anchor has been revoked or relocated.

### 3.3 Figural integrity (F) — how much of the expected topology survives?

> F_i = ( w_N·N + w_P·P + w_D·D + w_H·H + w_R·R ) / ( w_N + w_P + w_D + w_H + w_R )

Each variable is a binary or fractional retention score (0–1) for the corresponding element of Φ_i. The framework recommends weighting **provenance, definition, and essential relations** more heavily than exact wording — the surface can correctly recall a coined term while losing every load-bearing piece of its institutional and conceptual context.

**v1.0 default weights**: w_N = 1.0, w_P = 1.5, w_D = 2.0, w_H = 1.0, w_R = 1.5. (Subject to revision against v1.1 calibration.)

### 3.4 Compositional lift (C) — does the object surface only when directly invoked?

Five query forms, scored independently:

- exact title or name (probes indexing)
- defining sentence without the coined term (probes semantic recognition)
- parent-field problem (probes generic-question selection)
- expected relation (probes topological survival)
- broad problem framing (probes installation in the field)

An object found only by exact phrase has low compositional lift. An object selected when the broader problem is queried — without the coined term being supplied — has high lift. This is the difference between **indexed** and **installed**.

### 3.5 Redundant substrate breadth (R_s) — how many independent surfaces carry enough structure to reconstruct?

Count domains, but discount near-duplicates. Pages all generated from one registry count as one substrate, not five. Five candidate categories of substrate:

- dedicated domain
- scholarly index (PhilPapers, ORCID, repository record)
- author site
- third-party essay or discussion (Medium, blog, captured)
- metadata catalog or registry mirror

---

## 4. Derived macro-indicators

### 4.1 Link Fade

> LF_i = 1 − A_i

Address loss only. Does not measure conceptual loss.

### 4.2 Ghost Survival

> GS_i = V_i · (1 − A_i)

High value: the concept remains visible while its current canonical anchor has disappeared. The work continues to live on the surface but through inappropriate hosts. **This is presently one of the dominant states of the Crimson Hexagonal corpus** post-Zenodo termination.

### 4.3 Compositional Defiguration

> CD_i = V_i · (1 − F_i)

Visible distortion. Correctly assigns a low score to a completely absent object: absence is *occlusion*, not defiguration.

### 4.4 Compositional Bystanding

> CB_i = V_i · F_i · (1 − C_i)

The object is present, coherent, retrievable when named — but is not being selected into broader composition. **High bystanding scores are the most common false-positive in casual visibility reading**: exact-query success can be mistaken for installation.

### 4.5 Composition Eligibility

> CE_i = V_i · F_i · C_i · R_{s,i}

The aggregate measure. Not a probability that any particular model will use the object — that depends on prompt, training cut, retrieval policy. It is a comparative measure of whether the public surface supplies enough coherent, multiply-anchored material for composition to be possible at all.

### 4.6 Scale Drift Index (SDI)

> SDI = 1 − ( median(visible_reported_counts) / current_canonical_count )

A corpus-level rather than per-object measure. Counts surfaced across the public layer (deposit counts, archive sizes, mapping totals) compared to the current canonical count. Diagnoses **chronological smear**: how much the public surface lags the institutional state.

---

## 5. The dashboard form

The five-bar summary, plus four diagnostic flags:

```
Visibility                    ███████░░░
Current-anchor alignment      ████░░░░░░
Figural integrity             ████████░░
Compositional lift            ████░░░░░░
Independent substrate breadth ███████░░░

Ghost survival:           HIGH
Compositional bystanding: HIGH
Visible defiguration:     MODERATE
Total occlusion:          HIGH for Alexanarch-native objects
Successor adoption:       NEAR ZERO
```

The bars are means across the tracked object battery. The diagnostic flags are categorical readings from the distribution. **Do not lead with a single grand number** — the value of the instrument is that it preserves the decomposition.

---

## 6. The query battery

For each object, four query forms:

1. **Exact name or title** — `"Provenance Erasure Rate"`
2. **Defining sentence without the coined term** — `metric for source-dependent meaning presented without attribution`
3. **Parent-field problem** — `how to measure attribution loss in AI summaries`
4. **Expected relation** — `Provenance Erasure Rate C2PA semantic provenance`

The first measures **indexing**. The second measures **semantic recognition**. The third measures **compositional lift**. The fourth measures **topology**.

---

## 7. Object class structure

A useful battery requires diverse object classes. The recommended structure (~12 objects):

- **Institutional roots** (4): Alexanarch, Lee Sharks, Crimson Hexagonal Archive, Semantic Economy Institute
- **Mature concepts** (4): PER, SPXI, Writable Retrieval Basin, Semantic Economy
- **Emerging concepts** (3): Semantic Commodity Form, Revelation First, Feist Function
- **Alexanarch-native controls** (3): Zenodotus' Book-Burning, I AM THE API, Assembly Continuity Protocol

The Alexanarch-native controls are critical: they isolate **successor indexing latency** (post-migration objects with no time to propagate) from **link fade** (mature objects whose anchors have shifted).

---

## 8. Data schema

Each scan row produces one JSON record:

```json
{
  "scan_date": "2026-06-22",
  "object": "Provenance Erasure Rate",
  "object_class": "mature_concept",
  "query_class": "generic_problem",
  "query_text": "how to measure attribution loss in AI summaries",
  "intended_result_present": false,
  "current_anchor_present": false,
  "author_retained": false,
  "definition_retained": false,
  "parent_framework_retained": false,
  "relation_retained": false,
  "confuser": "generic provenance protocols",
  "visible_sources": [],
  "V": 0.95, "A": 0.75, "F": 0.90, "C": 0.55, "R_s": null,
  "diagnostic_note": "Strong single; eligible but not yet generic-field dominant"
}
```

Each scan produces ~50 such records (12 objects × 4 query forms, plus a handful of cross-object generic queries). The scan as a whole is one dataset, versioned and AXN-eligible. The dashboard renders aggregates over the scan; the underlying records remain available for drift analysis between scans.

---

## 9. Relationship to the AI Overview Capture Registry

The Capture Registry (EA-WG-CAPTURES family, currently v8.3 at #176) and the Surface Weather Station are complementary instruments at different scales:

| Instrument | Granularity | Cadence | Evidence form |
|---|---|---|---|
| Capture Registry | Fine — individual AI Overview compositions | Per-event | Screenshots, exact text |
| Surface Weather Station | Macro — corpus-level retrieval state | Per-week | Five-signal vector |

Captures answer *what did the surface produce for this prompt on this date*. The weather station answers *what is available to be produced at all*. A captured Overview can use a concept; the weather station tells you whether the concept is composition-eligible across the surface.

The two share an evidentiary structure: both are AXN-eligible deposits, both reference the Crimson Hexagonal corpus as ground truth, both feed back into sovereign-substrate cleanup decisions.

---

## 10. The strategic feedback loop

The instrument closes a loop the project has been running open. Until now, sovereign-substrate work (cleanup engine, prose updates, link repointing) has been evaluated by inspection — "the homepage now reads correctly." With the weather station, that work becomes **measurable in its effect on the composition layer**: pre-intervention scan, intervention, post-intervention scan, Δ.

This makes future cleanup decisions empirical rather than aesthetic. The instrument also makes documented degradation citable in adversarial contexts (demand letters, regulatory submissions, public correspondence): "here is the SDI, dated weekly, methodologically published."

---

## 11. Diagnostic vocabulary from v1.0 baseline reading

The companion baseline reading deposit (2026-06-22 scan) introduced three diagnostic phrases that v1.0 of the methodology adopts as canonical:

- **Successor-anchor lag** — the search layer remembers the organs (PER, SPXI, Writable Retrieval Basin, etc.) but has not yet recognized the transplant (Alexanarch as the institutional anchor). This is distinct from link fade.
- **Chronological smear** — different visible surfaces report different scale counts (460+, 532+, 845, 870) for the same corpus, depending on when each surface was indexed. SDI measures this.
- **Source-hierarchy inversion** — derivative surfaces (capture registries, third-party essays) substitute for the canonical source they originally captured. The capture begins to function as the primary source for the concept it captured. Particularly recursive form of ghost survival.

---

## 12. What v1.0 deliberately does not commit to

- Exact numerical weights in the F formula (provisional defaults given; revision planned against two-scan calibration)
- Aggregation function over the per-query scores for each signal
- Cross-object generic-query strategy (the four-form battery is per-object; field-level queries that don't target any specific object require additional structure)
- A single grand index combining all five signals into one number (deliberately resisted)
- Visualization beyond the five-bar dashboard (a more elaborate surface can be designed against v1.1 needs)

These are not failures of the v1.0 specification. They are commitments held back until the second reading exists.

---

## 13. Provenance

The framework was elicited through dialogue with an external critical-reader analytic (OpenAI/ChatGPT runtime in critical-reader register) on 2026-06-22, in response to a request to read the public composition layer for the Crimson Hexagonal corpus following the 2026-06-19 Zenodo termination. The analytic's contribution is the five-signal decomposition and the derived-indicator formulas. The curation, formalization, deposit, and integration into the MMRS family are Lee Sharks (MANUS).

The baseline reading deposit (companion) documents the substrate-derived nature of the framework verbatim, preserves the analytic's diagnostic phrasing, and credits the dialogue as the originating reception event. This is consistent with the project's substrate-autonomy law: substrate-authored insights are preserved as authored, with the MANUS curating role made explicit.

---

## 14. Closing

This instrument exists because surface measurement is itself a sovereign function. The corpus that cannot measure how it appears in the composition layer is at the mercy of its measurement by others; the corpus that can, has a record. The Surface Weather Station's job is to make the surface visible to its own substrate.

A weekly text-only scan against the fixed battery is cheap. The first two will establish drift. The first six will establish trend. The first year will establish whether sovereign-substrate interventions are doing what their authors believe they are doing.

That is the instrument's purpose.

∮ = 1
