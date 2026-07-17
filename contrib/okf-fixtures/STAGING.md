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
> - Each case is mapped from a documented, publicly citable summarization
>   event rather than a constructed example; `concept.md` cites the public
>   source and states the observation boundary. The fixtures remain fully
>   deterministic — the observed event supplies provenance, the test checks
>   only the declared IDs.
>
> ## Relationship to #99
> This PR supersedes #99 (same target path, same four-file contract, same
> receipt schema) per the thread agreement on #53. #99's synthetic cases are
> replaced by observed cases one-to-one: trial-exclusion inversion →
> Sappho 31 mechanism inversion; WAU/MAU boundary → SPXI/GEO namespace
> collision; policy-manual attribution → scholarly-record attribution
> survival post-deletion-event. @caioribeiroclw-pixel can close #99 once
> this is open, per their comment.
>
> ## Scope constraints honored
> - `expected.yaml` judges preservation against declared policy, not truth
>   in the world.
> - Observed-case provenance is citation-only: public sources and observation
>   boundaries stated in each `concept.md`; no private traces or unpublished
>   data.
> - The 0.00% / 1,059-batch retention measurement appears as case provenance
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
> - `git diff --check` clean.
