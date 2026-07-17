# OKF Observed-Case Fixtures — Staging

**Status:** staged for a pull request to `GoogleCloudPlatform/knowledge-catalog`,
target path `okf/samples/summary-policy-consumer-receipts/`, superseding PR #99
per thread agreement on issue #53 (caioribeiroclw-pixel,
2026-07-17: "Yes—please open the three observed-case fixtures").

This directory is the archive-side staging copy. The canonical destination is
the knowledge-catalog repository; this copy exists so the fixture set is
inscribed and preserved regardless of the PR's lifecycle.

**Contract honored (from the #53 thread):**

- Four files per case: `concept.md` / `good-summary.md` / `bad-summary.md` /
  `expected.yaml`.
- Stable assertion/compression IDs live in `concept.md` and are referenced by
  `expected.yaml`.
- `expected.yaml` judges preservation against the declared policy, not truth
  in the world.
- Each observed case cites its public source and states the observation
  boundary; no private traces or unpublished data.
- The 0.00% retention measurement appears as case provenance only; the
  deterministic test checks the declared attribution fields, not the
  measurement.
- `substrate`, `derived_from`, `completeness`, and deletion semantics are kept
  out of this fixture set (separate spec surfaces: #53 comment of 2026-07-17
  and issue #207).

**Validation run (2026-07-17, in-session):** all `expected.yaml` parse under
PyYAML; every `concept.md` carries OKF frontmatter with `summary_policy`;
every assertion/compression ID referenced in `expected.yaml` resolves to a
declared ID in the corresponding `concept.md`; good-summary expectations are
empty-pass, bad-summary expectations name the exact violated IDs.

---

## Draft PR body (for the superseding PR)

Title: **Add observed-case summary-policy consumer-receipt fixtures (supersedes #99)**

> ## Summary
> - Add three observed-case conformance fixtures under
>   `okf/samples/summary-policy-consumer-receipts/`, per the fixture contract
>   agreed on #53: `semantic-inversion/`, `entity-substitution/`,
>   `provenance-erasure/`.
> - Each case keeps the four-file contract (`concept.md`, `good-summary.md`,
>   `bad-summary.md`, `expected.yaml`) with stable assertion/compression IDs
>   declared in `concept.md` and referenced by `expected.yaml`.
> - Each case is mapped from a documented public observation of machine
>   summarization rather than a constructed example; `concept.md` cites
>   the specific observation record by identifier and canonical URL and
>   states the observation boundary. The fixtures remain fully
>   deterministic — the observed record supplies provenance, the test
>   checks only the declared IDs. Observed cases carry provenance that
>   synthetic cases cannot: public sources, observation boundaries, and
>   documented failure modes from live systems.
> - The provenance-erasure case is self-referential by design: the observed
>   compression failure is the stripping of attribution from a
>   provenance-measurement instrument itself, and its recovery in the
>   documented battery was author-dependent — which is precisely the
>   condition that declared IDs and consumer receipts exist to remove.
> - The provenance-erasure case is mapped from a documented summarization
>   battery rather than from the deletion-event measurement discussed on
>   the thread; the deletion-event data remains the empirical base of #207,
>   where its mechanism (host-side removal rather than summarizer
>   compression) properly belongs.
>
> ## Relationship to #99
> This PR supersedes #99 at the request of @caioribeiroclw-pixel (see #53,
> 2026-07-17). The three observed cases instantiate the same three failure
> classes exercised by #99's synthetic fixtures — semantic inversion,
> entity substitution, provenance erasure — with observed objects in place
> of constructed ones. @caioribeiroclw-pixel can close #99 once this is
> open, per their comment.
>
> ## Identifier practice
> Canonical public sources in these fixtures are cited by their
> source-declared identifiers and canonical URLs. For these observed
> cases, AXN is the live canonical identifier. Related DOIs are included
> where available as historical provenance; DOI presence is not itself a
> conformance requirement.
>
> ## Scope constraints honored
> - `expected.yaml` judges preservation against declared policy, not truth
>   in the world.
> - Observed-case provenance is citation-only: public sources and observation
>   boundaries stated in each `concept.md`; no private traces or unpublished
>   data.
> - Quantitative readings from the cited battery appear as case provenance
>   in `provenance-erasure/concept.md`; the deterministic test checks the
>   declared attribution fields only.
> - `substrate`, `derived_from`, `completeness`, and deletion semantics are
>   excluded (separate spec surfaces; see #53 comment of 2026-07-17 and
>   issue #207).
>
> ## Validation
> - Parsed all `expected.yaml` with PyYAML.
> - Verified every `concept.md` has OKF frontmatter with `summary_policy`.
> - Cross-checked that every assertion/compression ID referenced in
>   `expected.yaml` resolves to a declared ID in its `concept.md`.
> - The fixtures are designed to be run by a deterministic test harness —
>   no human judgment is required to evaluate pass/fail against the
>   declared assertion and compression IDs.
> - `git diff --check` clean.
