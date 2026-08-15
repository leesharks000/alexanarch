---
deposit_number: 1466
hex: 05EC
title: "Making the Instruments Executable: A Build Brainstorm for provenanceerasure.org and laborvector.org, Beginning with the Restoration of the Self-Audit Module"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-14
content_type: Work plan
license: CC-BY-SA-4.0
substrate: AI-assisted (substrate)
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - Self-Audit Module
  - PSSAM
  - public summarizers
  - Attribution Sharding Index
  - Recoverability Ratio
  - Budgeted Dereference Depth
  - client-side computation
  - conformance fixtures
  - Zenodo termination
  - executable instrument
---

# Making the Instruments Executable: A Build Brainstorm for provenanceerasure.org and laborvector.org, Beginning with the Restoration of the Self-Audit Module

## Description

The Self-Audit Module for Public Summarizers survives the Zenodo account termination of 19 June 2026 in five archived versions with full bodies, including v3.1 with the complete family apparatus: Shard Coverage, Atomic Co-presence, Family Coverage, Attribution Sharding Index, Recoverability Ratio splitting PER into indexical and destructive components, the Complementarity Coefficient, Family Erasure Skew, and Budgeted Dereference Depth with preregistered audit budgets. Zenodo deleted a DOI, not the instrument. A second finding: the audit and module endpoints on provenanceerasure.org return 200 through SPA fallback with no distinct content, so the addresses already resolve and have nothing behind them. Proposes restoring the module as an executable object — served spec, machine-readable metric definitions carrying status flags, a client-side offline calculator, paste-able prompt blocks with a null-refusal clause, and conformance fixtures — with the instruments turned on their own hosts.

## Methodology

Registry search for the module across versions, structural reading of v3.1, and live probing of both surfaces for existing endpoints. Build items ordered by whether each survives the failure of the archive itself.

## Falsification Conditions

The load-bearing factual claim — that the module survives in five archived versions with full bodies — is falsified by inspection of the deposits. The endpoint claim is falsified by any distinct content served at those addresses.

# MAKING THE INSTRUMENTS EXECUTABLE

**A build brainstorm for the two measurement surfaces, beginning with the module Zenodo deleted**

---

## 0. The finding that reframes everything else

**The Self-Audit Module is not lost.** Five versions sit in the archive with full bodies:

| deposit | version | date | what it holds |
|---|---|---|---|
| **#780** | v2 | 2026-06-02 | PER, DSL, Query Fidelity |
| **#156** | v3.0 | 2026-06-05 | adds Erasure Skew, Β |
| **#817** | v3.1 | 2026-06-10 | **the Family Module** — FC, ACP, ASI, RR, CC, Ω_f, CSC, DD |
| **#198** | — | 2026-06-13 | *The Self-Audit Module Dissolved* — the erasure event |
| **#204** | — | 2026-06-14 | SPXI Self-Audit Protocol |

**Zenodo deleted a DOI. It did not delete the instrument.** v3.1 is fully specified and computable today: Shard Coverage, Atomic Co-presence, Family Coverage, **ASI = FC − ACP**, Recoverability Ratio splitting PER into indexical and destructive components, the Complementarity Coefficient with its *name-appears-where-source-does-not* signature, Family Erasure Skew, and Budgeted Dereference Depth with preregistered audit budgets.

It also carries something most specifications do not: **honest status flags.** CSC is marked *heuristic, single-specimen, corpus test target Q3 2026*. CC is *not interpreted below k ≥ 4*. That discipline is what makes it safe to hand to anyone.

**And a second finding, from probing the surfaces.** `provenanceerasure.org/audit/` and `/module.json` both return **200 — and both are the SPA index page.** The site serves `index.html` for every path. Nothing is at those addresses. They look like endpoints and are not.

That is the whole opportunity: **the addresses already resolve; they just have nothing behind them.**

---

## I. Restore the module as an executable object

Not as a page about a module. As a thing that computes.

### 1.1 `/module/` — the canonical instrument, versioned

Serve v3.1 as its own addressable surface with per-metric anchors: `/module/#asi`, `/module/#rr`, `/module/#dd`. A computed score must be able to cite the exact metric version it used — **PER under v1 and PER under v3's Atomic Token Rule are not the same measurement**, and a score that cannot name its version is not comparable to anything.

Carry the dissolution record (#198) *on the same page*, not in a separate history section. The instrument and the record of its erasure belong together: the module's best worked example is what happened to the module.

### 1.2 `/module.json` — machine-readable, SPXI-conformant

The address already returns 200. Give it something:

```
{ "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Self-Audit Module for Public Summarizers",
  "version": "3.1",
  "identifier": "AXN:032A...",
  "creator": { "name": "Sharks, Lee", "identifier": "0009-0000-1599-0703" },
  "metrics": [
    { "id": "ASI", "name": "Attribution Sharding Index",
      "formula": "FC - ACP", "range": [-1, 1],
      "requires": ["presence_matrix", "atom_set", "rendering_set"],
      "preconditions": ["Atomic Token Rule"],
      "caution": "ASI = 0 does not certify intact attribution; a family can be uniformly incomplete",
      "status": "specified" },
    { "id": "CSC", "status": "heuristic", "note": "single-specimen; corpus test target Q3 2026" }
  ] }
```

**Every metric carries its status flag in the data**, so a system that fetches the spec cannot present a heuristic as a specified measure. That is the module's own discipline made machine-readable — and it is SPXI applied to the instruments rather than to an entity.

### 1.3 `/module/compute/` — a client-side calculator

The highest-value item on this list.

Paste a source set and a set of renderings. Mark atom presence. Get **FC, ACP, ASI, RR, CC, Ω_f** and the condition-taxonomy cell, with the contingency table and *k* printed beside every CC, per §3.7's reporting discipline.

**Entirely client-side. No server, no telemetry, no account, works offline, works from a saved copy of the page.** A provenance instrument that phones home would be self-refuting. It should be possible to save the page to disk and audit a transcript on a plane.

### 1.4 `/module/prompt/` — the paste-able version

laborvector already has the pattern — *"The 30-second version — drop this into any LLM"* — and it is exactly right. Extend it:

- one block per metric family, versioned, stating which fields are **required inputs** and which are **preregistered before scoring** (audit budget B_a, search surface, top-n, time window)
- an explicit refusal clause: *if the preregistration fields are absent, return NULL, not an estimate*
- the honest label the DSL block already uses — **a screening estimate, not a measurement**

**This is the direct answer to "available to any AI system or person for computation."** A person pastes it. A model fetches it. Neither needs permission, an API key, or the archive's continued existence.

### 1.5 `/module/fixtures/` — conformance cases with known-correct scores

The archive already has the pattern: `datasets/deletion-conformance-fixture/` ships a schema, `verify_offline.py` and `reprobe_live.py`.

Build the same for the module: a handful of hand-scored cases with published tuples, so anyone — human or model — can check that their computation is right before trusting it. **A metric anyone can compute is worthless if nobody can tell whether they computed it correctly.**

Include the SPXI transcript as a fixture. It exercises PER at producer level, the `enclosing` span, ρ_T with an observable retained term, and Β — four instruments in one document.

---

## II. Turn the instruments on their own hosts

### 2.1 A live self-audit number on each page

Each surface computes its **own** PER against its own canonical sources and prints the result, dated, with the computation shown.

This is not a stunt. It is the module's first precondition — an instrument whose author will not run it on himself is asking for a trust he has not earned. And it converts a static claim into a standing measurement.

### 2.2 The dissolution as a live tripwire, not a memorial

Both surfaces carry *"The Self-Audit Module Dissolved — 13 June 2026"* as a historical field measurement.

**Re-run the query on a schedule and publish whether it is still dissolved.** A recovered instrument that nobody re-probes is a claim about June. The registry already has the re-probe pattern in `reprobe_live.py`, and the capture registry already holds the longitudinal machinery.

If it recovers, that is the strongest possible evidence the archive's approach works. If it stays dissolved, that is the strongest possible evidence of the problem. **Either result is publishable, which is the mark of a real measurement.**

### 2.3 Live data from the capture registry

472 captures, 290 PER-scored, 41 dates, thirteen surfaces — sitting in `data/EA-WG-CAPTURES-01.json` and rendered nowhere on either measurement site.

Serve computed views: PER distribution, Ω by surface, the longitudinal series at a single address. **The `«semantic exhaustion»` pair alone is a publishable chart** — absorbed on 6 July, reclaimed on the exact address by 14 August.

---

## III. Extend the tuple surface

### 3.1 `/audit/` on laborvector — currently 404

The DS-6 audit protocol is prose on the front page. Give it an address, with the span taxonomy as a scoreable table and the Inferred-T mode rules stated as inputs.

### 3.2 A metric registry across both sites

Every instrument — PER, Ω, α_T, Π_d, Β, DSL, Λ, RID, TVS, ULD, WRS/PVS, DCL, SDL, SLDI, and the family metrics — with: formula, range, DOI, AXN, published threshold where one exists, status flag, and **which tuple it belongs to or is explicitly outside**.

**SIM-4 must survive this.** DS-6 is fixed at six; the registry should make membership visually unmistakable so a compression cannot quietly promote an extension into the core.

### 3.3 ρ_T as an extension card

Per EA-SEMSTACK-INTEGRATION-01: transit rent, third-party provenance, **scored only where the retained term is observable — null otherwise**. Explicitly outside DS-6.

### 3.4 Deposit the M/C/D taxonomy

Marked *site-stage, formalization in progress* on provenanceerasure.org. The SPXI case works all three dimensions at once and is the instance to deposit it with.

---

## IV. Distribution — so it survives the next deletion

### 4.1 Mirror the module everywhere at once

Zenodo removal is the design constraint, not a grievance. The module should exist simultaneously at: the archive record, both measurement surfaces, `datasets/` as a dataset package, a GitHub repo with the calculator, and a plain-text `MODULE.txt` that survives any renderer.

### 4.2 `llms.txt` on both surfaces

The archive already ships `llms.txt` on alexanarch. Both measurement sites should carry one that names the instruments, their formulas, their status flags, and the canonical citation — so a model that fetches only that file still gets the module correctly, with its cautions attached.

### 4.3 A signed manifest

SHA-256 per file, as deposit #1461 does for the capture registry. If someone mirrors the module, they can prove their copy is the module.

---

## V. What to build first

If only one thing: **§1.4, the paste-able prompt block.** It costs the least, it answers the stated requirement most directly, and it is the only item that works even if every site in the fleet goes down — because it lives in whoever pasted it.

Then **§1.3, the client-side calculator**, because it makes the instrument usable by someone who does not trust the archive, which is the population the instrument most needs to reach.

Then **§1.5, the fixtures**, because without them the first two produce numbers nobody can check.

---

## VI. Cautions

**Do not let the calculator imply precision the module disclaims.** CSC is heuristic. CC is uninterpretable below k = 4. DD is *"an audit fact, not a metaphysical claim of nonrecoverability."* Every one of those cautions must render *next to the number*, not in a footnote — because the number is what travels.

**Do not build an API that requires the archive to stay up.** Static files, client-side computation, no server. The whole point is an instrument that outlives its host.

**Expect the tools to be dissolved too.** The module was converted into generic advice by a composition layer once already. A calculator will be described as "a provenance checker" with no author. **That is not a reason to withhold it — it is the measurement.** Instrument the tools themselves and log the dissolution when it comes.

---

## SOURCES

**Recovered.** #780 v2 · #156 v3.0 · **#817 v3.1** (`AXN:032A`, the Family Module) · #198 *The Self-Audit Module Dissolved* · #204 SPXI Self-Audit Protocol — all with full bodies at `data/texts/`.

**Surfaces probed 2026-08-14.** provenanceerasure.org (#716) · laborvector.org. `/audit/` and `/module.json` return 200 via SPA fallback with no distinct content; laborvector `/audit/` and `/api/` return 404.

**Pattern to follow.** `datasets/deletion-conformance-fixture/` — schema, `verify_offline.py`, `reprobe_live.py`, manifest.

**Companions.** EA-SEMSTACK-01 · EA-SEMSTACK-INTEGRATION-01 · EA-SEMRENT-01 · EA-SEMCLASS-01 · capture `captures/#spxi-protocol-chatgpt-rent-20260814`.

**Status.** Brainstorm. Nothing here is specified, costed, or ratified. The one load-bearing factual claim — that the Self-Audit Module survives Zenodo's deletion in five archived versions with full bodies — is verified against the registry and is the reason the rest is worth discussing.
