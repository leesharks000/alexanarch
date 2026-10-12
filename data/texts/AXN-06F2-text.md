---
deposit_number: 1676
hex: 06F2
title: AI Overview Capture Registry — EA-WG-CAPTURES-01 v12.167 — 633 semantic addresses, 811 captures, 2026-06-07 to 2026-10-12
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-10-12
content_type: Longitudinal dataset snapshot
license: CC-BY-4.0
substrate: AI-assisted (substrate). Snapshot assembled, counted and written in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction, from the canonical store at v12.167. The captures themselves were taken by the operator on the surfaces named in each record.
version: v12.167
related_ids: "AXN deposit #1461 — EA-WG-CAPTURES-01 v10.9, superseded by this record\nAXN deposit #936 — EA-WG-CAPTURES-01 v8.9 (superseded by #1461)\nAXN deposit #1459 — EA-MMRS-AIOCR v1.1, the priority packet defending this instrument\nAXN deposit #1084 — EA-SEMANTIC-ADDRESSES-01, the address framework\nAXN deposit #1612 — What Enters Composition Through the Cards (source admission, June–September)\nAXN deposit #1614 — transcript coverage audit and the monotone gate\nAXN deposit #833 — The Summarizer as Horizon of Reception (a paper about the registry; not an edition)\nRegistry gallery: https://www.alexanarch.org/captures/"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - AI Overview Capture Registry
  - EA-WG-CAPTURES-01
  - machine-mediated reception
  - provenance erasure rate
  - semantic address
  - capture registry
  - longitudinal dataset
  - AI Overview
  - ChatGPT
  - record-page prompt
  - composition layer
  - entity resolution
  - adoption
  - versioned snapshot
  - MMRS
---

# AI Overview Capture Registry — EA-WG-CAPTURES-01 v12.167 — 633 semantic addresses, 811 captures, 2026-06-07 to 2026-10-12

# AI Overview Capture Registry — EA-WG-CAPTURES-01 v12.167

**633 semantic addresses · 811 captures · 84 dates · 2026-06-07 to 2026-10-12**

**Lee Sharks** · ORCID 0009-0000-1599-0703 · 12 October 2026 · supersedes v10.9 (#1461)

## 1. The citable unit

**ONE SURFACE + ONE SEMANTIC ADDRESS + ONE DATE = ONE CAPTURE.**

- **The capture** is citable at `captures/{slug}/`. Cite it for what a named system did.
- **The address** is citable at `addresses/{slug}/`. Cite it for what the address does across surfaces or over time.

Each address has had its own page since 2026-09-25. That page is the unit a fetcher can read whole, which the gallery is not. An address's slug is inherited from the first capture seated at it and is never renamed.

## 2. State at v12.167

**Sections, by address count:**

| Section | Addresses |
|---|---|
| Machine Reception | 107 |
| Heteronyms | 77 |
| Frameworks | 63 |
| Archive | 56 |
| Coinages | 38 |
| Semantic Economy | 37 |
| Works | 35 |
| Revelation & Theology | 32 |
| Classics & Philology | 28 |
| Provenance & Erasure | 24 |
| Institutions | 23 |
| Valuation | 17 |
| Sites | 15 |
| ∮ = 1 | 15 |
| Reference & General Knowledge | 12 |
| Architecture | 11 |
| People | 11 |
| Projects | 11 |
| Operative Semiotics | 10 |
| Platform Erosion | 9 |
| Disciplines | 1 |
| Revelation First | 1 |

**Surfaces, by capture count:**

| Surface | Captures |
|---|---|
| Google AI Overview | 490 |
| ChatGPT (all recorded labels: 119 + 27 Luna 5.6 + 12 Luna + 8 chatgpt.com + 1 web, logged out) | 167 |
| Undetermined | 56 |
| Unresolved | 50 |
| Google AI Mode | 12 |
| Grok | 7 |
| Bing Copilot | 6 |
| Perplexity (one agentic) | 5 |
| Claude | 3 |
| Qwen | 2 |
| Google Knowledge panel | 2 |
| Single-capture surfaces (Gemini, Google Scholar, a Google results page with no AI surface, Bing Copilot Search popup, ScholaRef, SciLynk, TikTok Studio) | 7 |
| Surface not recorded at the capture | 4 |

**Authentication state:** signed in 223; signed out and incognito (both spellings) 251; incognito 124; signed out 74; unrecorded 91; other recorded states 48.

**Evidence:** 792 captures carry a verbatim transcript and 328 carry a frame. 505 are scored for PER, at a mean of 0.506; at v10.9 the mean was 0.603.

## 3. The data flow

**Since 2026-08-17 (ratified, MANUS), `data/EA-WG-CAPTURES-01.json` is the single writable authority.** The rebuild store (`rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json`) is sealed as the rebuild-era source, last written 2026-08-18. This corrects v10.9's account of the data flow, which named the rebuild as canonical; that was accurate at its date.

The seat runs in this order:

1. `scripts/capture_intake.py --seat`
2. `scripts/build_capture_gallery.py`
3. `scripts/seat_capture_postflight.py`, which links, bakes, gates (the runtime gate executes the page scripts), builds the semantic-address layer and publishes `addresses/{slug}/`, then syncs and cites.

Each batch of intake is kept as `rebuild/capture-registry/intake-YYYYMMDD-*/`.

## 4. Files

The **core data bundle** is `EA-WG-CAPTURES-01-v12.167.tar.gz` (18,662,466 bytes; SHA-256 `ce2c510cc2bd91926cebd71c094c5a13f1f14198a04ea44609477b2e40305548`). It holds:

- `data/EA-WG-CAPTURES-01.json`, the canonical store;
- `rebuild/capture-registry/`: the pipeline documents, the intake directories and the sealed rebuild store;
- `data/capture-deposit-links.json`;
- `data/semantic-addresses.json`;
- `datasets/capture-registry/`;
- `captures/index.html`.

`manifest.json` lists 478 files with SHA-256, bytes, media type and role: the eight core files, the bundle, and the **469 capture frames** (179.2 MB), which are manifested at their canonical paths under `data/captures/{slug}/` rather than duplicated. This follows the registry's rule: images are held there, and galleries display them rather than host them. Total manifested: 269.4 MB.

## 5. Version chain

v6.0 (#825) → v6.1 (#1397) → v7.0 (#1398) → v7.2 (#1396, #1401) → v8.3 (#3) → v8.9 (#936) → v10.9 (#1461) → **v12.167 (this deposit)**

Between v10.9 and v12.167 the registry went from 328 addresses and 470 captures to 633 and 811. The intervening minor versions are recorded in the canonical file, not as separate deposits.

## 6. What changed in the instrument since v10.9

1. **Canonical authority moved** from the rebuild store to the projection (2026-08-17).
2. **Address pages.** Every address has a page of its own (2026-09-25).
3. **Surfaces widened.** At v10.9, ChatGPT accounted for 3 captures; it now accounts for 167. The registry also holds Google AI Mode, Grok, Bing Copilot, Perplexity, Claude and Qwen.
4. **Source chips are data.** Each chip is recorded with its relation to the archive and carries into the PER notes. *What Enters Composition Through the Cards* (#1612) profiles source admission across June–September.
5. **The transcript is the capture.** #1614 audited transcript coverage and installed the gate that keeps the count monotone.
6. **The record-page run (2026-10-12).** 43 deposits, from #1421 to #1675, were captured at their own record pages' Ask ChatGPT prompts, signed out and incognito. The author was retained in all 43, the archive in 27, the identifier in 22. Mean PER was 0.22, with one score excluded (see §7).

## 7. Known defects at v12.167, recorded as data

**Defect counts, as the registry declares them:**

| Defect | Count |
|---|---|
| citations-null | 166 |
| analysis-without-finding | 152 |
| truncated-by-interface | 126 |
| surface-unresolved | 50 |
| unsupported-citations | 10 |
| date-unresolved | 3 |

**Declared but not held.** Two addresses declare more observations than they hold, so the registry counts 813 observations and holds 811:

- `operative-semiotics-20260610` declares 4 and holds 3.
- `operational-semiotics-bing-copilot-20260823` declares 2 and holds 1.

**PER against its markers.** Twelve captures carry all four PER markers true with PER 1.0:

- Ten were seated on 2026-08-13. The marker convention of that seating is not yet verified.
- Two were seated this month, under the convention where true means retained, and are inconsistent with it: `dedication-what-syllogizing-can-divide-chatgpt-20261011` and `missing-translator-ask-chatgpt-20261012`.

**Surface not recorded.** Four captures carry no surface label at the capture. They are counted here as unrecorded and not assigned.

None of these is repaired in this snapshot. Repair is its own mode.
