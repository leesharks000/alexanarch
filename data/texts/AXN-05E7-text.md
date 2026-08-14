---
deposit_number: 1461
hex: 05E7
title: AI Overview Capture Registry — EA-WG-CAPTURES-01 v10.9 — 328 semantic addresses, 470 captures, 2026-06-07 to 2026-08-14
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-14
content_type: Longitudinal dataset snapshot
license: CC-BY-4.0
substrate: AI-assisted (substrate)
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
  - AI Mode
  - composition layer
  - entity resolution
  - adoption
  - compositional entity liquidation
  - citation grammar
  - versioned snapshot
  - MMRS
---

# AI Overview Capture Registry — EA-WG-CAPTURES-01 v10.9 — 328 semantic addresses, 470 captures, 2026-06-07 to 2026-08-14

## Description

Versioned snapshot of the AI Overview Capture Registry (EA-WG-CAPTURES-01) at v10.9, continuing the deposit chain from v6.0 through v8.9. A longitudinal instrument for recording dated machine-mediated reception events: what composition layers make of a named entity when asked for it at a specific semantic address, on a specific date, in a specific authentication state. 328 semantic addresses carrying 470 captures across 41 distinct dates and thirteen surfaces, 451 of them with a verbatim transcript and 287 with a frame; 290 scored for Provenance Erasure Rate at a mean of 0.603. The citable unit is the CAPTURE — one surface, one semantic address, one date — independently anchored at captures/#slug, with the address separately citable across its surfaces and dates. 428 files totalling 193.5 MB are manifested with SHA-256: the core data as an attached bundle, the 420 capture frames referenced at their canonical paths under data/captures/slug/ per the registry's own rule that galleries display images rather than host them.

## Methodology

Each capture records the exact issued string, the surface, the date, the authentication state, the evidence class (paste, frame, or both), the returned source strip, a verbatim transcript where obtainable, and a finding. Surfaces are established from operator attestation with the frame as corroboration. Match type and Provenance Erasure Rate are recorded per capture, never per address. Addresses may carry several captures; each is anchored and citable on its own terms. The canonical store is the rebuild; the published projection is derived from it and no surface writes back to it.

## Falsification Conditions

Any capture is falsified by a re-run at the same address, surface, authentication state and date returning materially different composition, which is why the exact issued string and the rerun URL are recorded. The snapshot is falsified if the attached bundle's SHA-256 does not match, or if any manifested file's SHA-256 does not match the file at its stated path. PER scores are falsified by a source strip inconsistent with the recorded count.

# AI Overview Capture Registry — EA-WG-CAPTURES-01 v10.9

**328 semantic addresses · 470 captures · 2026-06-07 to 2026-08-14**

A longitudinal instrument for recording and analysing dated machine-mediated reception events: what composition layers make of a named entity when asked for it at a specific semantic address, on a specific date, in a specific authentication state.

This deposit is a **versioned snapshot** of that instrument, continuing the chain from v6.0.

---

## The citable unit

**ONE SURFACE + ONE SEMANTIC ADDRESS + ONE DATE = ONE CAPTURE.** Every capture is independently citable at `captures/#{observation_slug}`. The ADDRESS is separately citable at `captures/#{address_slug}` and is the right unit when the claim concerns the address across surfaces or over time.

Cite the CAPTURE for what a named system did. Cite the ADDRESS for what the address does. An address slug is inherited from whichever capture was seated first and is never renamed, so it names only that one — the address «who is lee sharks?» is anchored at a slug naming Bing Copilot while carrying ChatGPT, Perplexity and Google AI Overview captures too.

## State at v10.9

**Sections** — Captures 198 · Frameworks 55 · Heteronyms 21 · People 12 · Sites 10 · Institutions 9 · Projects 8 · Coinages 7 · Works 4 · Semantic Economy 2 · Archive 1 · Cold-start traversal 1

**Surfaces** — Google AI Overview 343 · UNDETERMINED 63 · UNRESOLVED 50 · ChatGPT 3 · Google Knowledge panel 2 · Google Search results page (no AI surface) 2 · Google AI Mode (native) 1 · Google Scholar 1

**Evidence** — 451 captures carry a verbatim transcript; 287 carry a frame. 290 are scored for Provenance Erasure Rate, mean **0.603**. 41 distinct capture dates.

## The data flow

The canonical store is `rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json`. The published projection at `data/EA-WG-CAPTURES-01.json` is DERIVED from it; galleries render FROM the projection and nothing renders TO it. Exactly one writable authority.

Intake adds a capture and is safe. Repair touches an existing record and is not: on 2026-08-13, forty captures were seated without incident and every destructive act that day was a fix. The repair posture is stated in `PIPELINE.md` — state the belief and its evidence, search the archive against it, one operation per commit, verify against the rendered page and say what was not verified.

## Files

**428 files, 193.5 MB**, each with a SHA-256 in the manifest below.

The **core data** — projection, canonical store, pipeline documents, the capture→deposit join, the semantic
addresses, the published dataset mirror and the rendered gallery — is attached as a single bundle,
`EA-WG-CAPTURES-01-v10.9.tar.gz`, 8.7 MB,
`sha256 7e6f3d77ebba1a6579020f2361664f494616e30064fbf8d41b329ac855ec20c8`.

The **420 capture frames** (152.5 MB) are
manifested at their canonical paths under `data/captures/{slug}/` rather than duplicated into the deposit.
That is the registry's own rule — *images are held there; galleries display them, they do not host them* — and
they are already versioned in the repository. Each carries a SHA-256 here, so the deposit can verify them
without holding a second copy. PNG frames do not meaningfully compress: bundling them would add 143 MB to
every version bump and recover nothing.

## Version chain

v6.0 (#1397) → v7.x (#1396, #1398, #1401, #825) → v8.3 (#3) → v8.9 (#936) → **v10.9 (this deposit)**

Between v8.9 and v10.9: the registry was rebuilt from its canonical store, the observation was established as the citable unit, a citation grammar was declared, per-capture anchors were repaired, the reading canon was marked, and PIPELINE.md was restored. The intervening versions are recorded in the projection's own `_what_changed_since_v9.6` block rather than as separate deposits.

## What this instrument has measured

Compositional entity liquidation at its own address, documented in EA-MMRS-AIOCR v1.1 (#1459): the exact proper name «AI overview capture registry» received as a common noun, the entity replaced by its semantic neighbourhood, no returned source identifying it.

A measured reclamation, 2026-08-14: «"semantic exhaustion"» returning the archive's definition and citing EA-MPAI-SEMEX-01 by name, against 2026-07-06 when the coinage was absorbed by semantic satiation across seven of seven third-party sources.

Three unprimed cold-start traversals (#1460), and an unprimed ChatGPT session that recovered the archive's
transmission thesis without being told it.
