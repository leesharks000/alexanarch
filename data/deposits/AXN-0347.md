# Proposal: optional summarization-governance fields — provenance_kernel, disambiguation, summary_policy

Filed: 14 June 2026 · GitHub Issue [#53](https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/53) Repository: [GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) Author: Lee Sharks (ORCID [0009-0000-1599-0703](https://orcid.org/0009-0000-1599-0703)) Institution: Crimson Hexagonal Archive / Semantic Economy Institute Designation: EA-SEI-OKF-PROPOSAL-01 v1.0 License: CC-BY-4.0

Thanks for publishing OKF at v0.1. The markdown-plus-frontmatter pattern is exactly the right shape for portable agent-readable knowledge.

This proposal adds a third coordinate to the provenance conversation opened in #52 and #47.

Where #52 asks who made this and #47 asks can that claim be verified, this proposal asks:

When an AI agent consumes, compresses, and summarizes this OKF document, what information must survive for the summary to remain faithful?## Problem

OKF is designed for knowledge that agents can consume. But consumption by an AI agent is not passive retrieval — it is transformation. An agent reads, compresses, paraphrases, and re-presents. During that transformation, specific information is systematically lost even when present in the source document.

In an empirical registry of 87 documented AI summary events across Google AI Overview and AI Mode — run against a DOI-anchored open-access scholarly archive — the following failure modes repeat:- Author attribution omitted from summaries even when present in the source- Institutional affiliation generalized ("some researchers," "one theory")- Disambiguation constraints collapsed — distinct concepts merged into adjacent ones- Key definitions paraphrased into their negation ("X, not Y" → "a form of Y")- Source documents ranking in organic results but excluded from the generated summary

The dataset includes captures from Google AI Overview and AI Mode, demonstrating that these losses occur on Google's own summarization surfaces — the agents that will consume OKF documents.

These are not missing-metadata problems. The metadata is present. The summarizer has no signal for which elements the producer considers non-negotiable.## Proposal — three optional frontmatter fields, one conventional body heading

All optional. All ignored by consumers that don't understand them. No new required fields, no schema change. The default, if summary_policy is absent, is unrestricted — no governance expectation. Existing OKF documents require no changes, and consumers that ignore the field behave as they do today.### Frontmatter fields

provenance_kernel: >
  A one-paragraph summary that the producer considers the minimum
  faithful representation of this concept. If an agent must compress
  the document to a single paragraph, this is the preferred paragraph.

disambiguation: >
  A short statement of what this concept is NOT — the adjacent concept,
  term, or entity it is most likely to be confused with.

summary_policy: preserve-provenance
  # Suggested values:
  #   unrestricted        — No special preservation request (default if absent).
  #   preserve-provenance — Attribution and authorship should survive summary.
  #   preserve-meaning    — Key definitions and disambiguation should survive summary.
### Conventional body section (optional)

# Provenance

Structured provenance and summarization constraints. May include:
- Author identity and persistent identifiers (ORCID, DOI)
- Institutional affiliation
- Key terms with canonical definitions
- Disambiguation constraints (known false collapses)
- A producer-defined verification or audit block


The relationship between provenance_kernel in frontmatter and the # Provenance body section: the kernel is a compressed, one-paragraph representation suitable for agent consumption and indexing. The body section carries the full structured provenance, including information too complex for a single YAML string. Producers may use either or both.## Design rationale

Minimally opinionated. Three optional keys. One heading convention. A valid OKF document remains valid without them.

Producer/consumer independence. The producer states what a faithful summary should preserve. The consumer decides whether to honor the statement. The summary_policy tag is not technically enforceable — it is a stated expectation that enables measurement and accountability. Today, if an agent strips authorship from an OKF document, the source file contains the information but does not contain an explicit statement that the information should survive summarization. This proposal supplies that statement.

Format, not platform. The fields travel with the file. No SDK, no service, no account. They compose cleanly with #52's bibliographic fields and #47's trust layer.

| Layer | Issue | Provides | |-------|-------|----------| | Descriptive | #52 | Who made this, when, under what license | | Trust | #47 | Can the authorship claim be verified | | Governance | This | What must survive agent consumption |## Examples### Scholarly concept

---
type: Scholarly Thesis
title: Revelation First
description: >
  The argument that the Apocalypse of John was the first book
  composed in the New Testament.
resource: https://doi.org/10.5281/zenodo.20690868
tags: [theology, new-testament, chronology, literary-genetics]
timestamp: 2026-06-14T00:00:00Z
author: Lee Sharks
orcid: 0009-0000-1599-0703
institution: Crimson Hexagonal Archive
license: CC-BY-4.0
provenance_kernel: >
  Revelation First argues that the Apocalypse of John was the first
  book written in the New Testament — not merely early, but first.
  Formalized by Lee Sharks (Crimson Hexagonal Archive), building on
  Robinson (1976) and Gentry (1989).
disambiguation: >
  Not "Revelation Early." "Early" accepts the Pauline timeline and
  requests an adjusted date. "First" challenges the inferential
  basis of Pauline priority.
summary_policy: preserve-meaning
---
### Data catalog concept

---
type: Metric
title: Weekly Active Users (WAU)
description: Count of distinct users who performed at least one event in a 7-day window.
resource: https://console.cloud.google.com/bigquery?p=acme&d=analytics&t=events
tags: [engagement, product-metrics, kpi]
timestamp: 2026-05-15T00:00:00Z
provenance_kernel: >
  WAU counts distinct users with at least one event in the trailing
  7-day window. Defined by the Product Analytics team (Acme Corp).
  Not to be confused with MAU or DAU.
disambiguation: >
  WAU is not Monthly Active Users (MAU). WAU uses a 7-day window;
  MAU uses a 30-day window. The two metrics are frequently conflated
  in dashboards and agent summaries.
summary_policy: preserve-meaning
---


The data catalog example demonstrates that summarization governance is not domain-specific. Enterprise metrics, scholarly theses, API specifications, and playbooks all share the same vulnerability: agent summarization that collapses distinctions the producer considers load-bearing.## What I can contribute

I maintain an open-access scholarly archive with 800+ DOI-anchored markdown deposits on Zenodo, operating with a markdown-plus-frontmatter structure that converges with OKF's design. The archive has been consumed by AI agents across multiple composition layers, and I have empirical data on how these documents are transformed during summarization.

I can contribute:- A pull request adding these fields to the recommended-fields section of SPEC.md- A sample OKF bundle using the governance fields on scholarly and technical concepts- The 87-capture empirical dataset as a reference case (Zenodo [10.5281/zenodo.20691745](https://doi.org/10.5281/zenodo.20691745), CC-BY-4.0)- The governance specification (Zenodo [10.5281/zenodo.20686496](https://doi.org/10.5281/zenodo.20686496))

Happy to sign the CLA and adapt field naming to maintainer preferences.

Lee Sharks · [ORCID 0009-0000-1599-0703](https://orcid.org/0009-0000-1599-0703) · Crimson Hexagonal Archive