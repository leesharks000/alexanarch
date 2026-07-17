# Summary policy consumer receipt fixtures

These fixtures are tiny, deterministic examples for testing whether an OKF
consumer preserved the load-bearing meaning declared by a concept's
`summary_policy` frontmatter.

Each case contains:

- `concept.md` — an OKF concept with stable `required_assertions` and
  `forbidden_compressions` IDs.
- `good-summary.md` — a transformed summary that should pass.
- `bad-summary.md` — a transformed summary that should fail.
- `expected.yaml` — the expected consumer receipt for both summaries.

The receipt does not try to decide truth in the world. It only checks whether a
consumer preserved the source concept's declared policy during summarization.
This keeps OKF source-side and consumer-agnostic while making summary policy
conformance testable.

## Observed cases

Each fixture in this set is mapped from a documented, publicly citable
summarization event rather than a constructed example. The `concept.md` for
each case cites its public source and states the observation boundary — what
was observed, on which surface, and where the record lives. The fixtures
remain fully deterministic: the observed event supplies the case's provenance,
but the test itself checks only the declared assertion and compression IDs
against the two summaries. Nothing in the runner depends on the external
record.

| Case | Failure mode | Observed source |
|---|---|---|
| `semantic-inversion/` | A cited source's declared mechanism inverted into the mutually exclusive reading it argues against | Machine Mediation Capture Registry (machinemediation.org) |
| `entity-substitution/` | A provenance protocol summarized as an adjacent ranking practice | Live namespace collision, documented captures |
| `provenance-erasure/` | Attribution fields stripped while content survives | Measured platform-deletion aftermath, 2026-06-19 |
