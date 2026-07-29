# Deletion Semantics Conformance Fixture

**A known-bad identifier corpus for testing deletion, tombstone, presence, and successor semantics.**

Fixture version 2.1 — the chorus-review release · 2026-07-28
Dataset: CC0 1.0 (`LICENSE-DATA`) · Scripts: MIT (`LICENSE-CODE`)
Derived from the Zenodo DOI Resolution Index (current, envelope layer) + the Alexanarch registry + dated repair artifacts
Offered to `GoogleCloudPlatform/knowledge-catalog` issue #207

---

## What this is

111 cases across 17 classes, drawn from a real deletion event and its aftermath, selected so that each class exercises a distinct condition a deletion-semantics specification has to handle. Every case carries:

- **`axis_subject`** — every axis value names its subject (concept, identifier target, content payload, registry assertion, registry update, archive record). No axis is populated from evidence belonging to another. Without this field, "is it here?" is not a well-formed question.
- **`axes`** — validity / presence / edges per the design ratified on the thread. Presence is **sparse**: `removed` and `never_landed` are the only named states, and the absence of a marker means what the spec default means. Validity is **never derived from identifier survival**: an identifier can die while its claims stand, and stand while its claims are false — so identifier cases carry `unassessed` unless independent evidence establishes a truth value. Supersession is an **edges** fact; withdrawal is a **lifecycle** fact; neither is a truth value.
- **`expected`** — machine-readable consumer expectations (emit this marker, preserve this reason, follow or refuse this edge, reject this input). This is what lets an implementation pass or fail.
- **`reason`** where one exists — an object separating actor from rationale, in which `not_disclosed` and `unknown` are first-class.

It is not a sample of a corpus. It is a set of test cases, one group per condition.

## Why a corpus like this is hard to obtain

Deletion semantics cannot be tested against a healthy corpus. Testing requires identifiers that were deleted, at scale, by a third party, with the deletion documented, the successors known, and the pre-deletion state recorded. This corpus has those properties by accident rather than design: an account holding the identifiers was terminated on 2026-06-19, the archive was reconstructed on independent infrastructure, and the mapping from severed identifier to surviving work was built and versioned afterward.

---

## The numbers

**Population.** The source resolution index holds **1,937 identifiers**. Recorded validity distribution at build:

| recorded validity (envelope layer, current) | count |
|---|---:|
| `verified_tombstone` | 1,815 |
| `verified_registered` | 73 |
| `verified_erased_registration` | 32 |
| `syntactically_valid_unverified` | 13 |
| `fragment_candidate` | 3 |

**Independent verification at build, 2026-07-28** (109 network-addressable case identifiers, terminal HTTP after redirects, retried past 503; two local write-failure cases are checked against repository evidence, not HTTP):

| recorded validity | n | observed | agreement |
|---|---:|---|---:|
| `verified_tombstone` | 62 | 410 × 62 | **100%** |
| `verified_registered` | 18 | 200 × 18 | **100%** |
| `verified_erased_registration` | 12 | 404 × 7, 410 × 5 | **split — the finding, preserved** |
| `fragment_candidate` | 3 | 404 × 3 | 100% |
| `syntactically_valid_unverified` | 6 | 410 × 4, 200 × 2 | — (no expectation asserted) |

**The tombstone classification holds at scale.** 62 of 62.

**`verified_erased_registration` is preserved as untrustworthy — on both layers.** Roughly half the class behaves as recorded, and the actor at the registration-erasure layer cannot be established from probes; those cases carry `actor: unknown`. A consumer that treats a producer's recorded state as authoritative without verification will be wrong here about half the time. That is a test case, not a defect — and the re-probe apparatus reports this class as an observed distribution, never as pass/fail.

**Registry-record presence and target-resolution presence are different questions, and they diverged.** The `registry_resolution_divergence` class went **8 for 8 at build**: a `GET` of the DataCite record endpoint returned HTTP 200 with `attributes.state: "findable"` parsed from the body and UTC-timestamped, while DOI resolution returned 410 in the same build run. This is not two authorities giving opposite answers to one question — it is one identifier with two subject-relative presences: the metadata record is retrievable; the identifier target is gone. The fixture records both, dated. `reprobe_live.py` will catch drift.

---

## The drift ledger (derived, not narrated)

From the mapping-level diff between the v1.0 build commit and the current repository:

- **Old population 1,939** — the v1.0 README stated 1,938, a hand-carried miscount; corrected here by derivation.
- **Current population 1,937.** Exactly two mappings removed, both by disclosed producer withdrawal (`withdrawn_removal_vs_destruction` cases), and **both were `verified_registered`** — one mechanism fully explains both population 1,939 → 1,937 and registered 75 → 73.
- **Zero `identifier_validity` changes** among mappings present in both snapshots.
- **Observation drift on the 47-case v1 base: zero** — every v1 identifier returned the same terminal status hours apart. Stability at hours-scale; drift at days-scale (v1 documented 2026-07-12 → 2026-07-28 changes); both scales in the data.

---

## The internal control

`not_removed_control` (10 cases) returned **200** in the same probe window as the 410s. The dead and the living are interleaved and measured together: a consumer cannot pass by assuming everything is dead, and cannot explain the 410s as an outage.

---

## Case classes (17)

| class | cases | condition exercised |
|---|---:|---|
| `removed_with_successor` | 20 | identifier severed, work survives, successor known — the ordinary case |
| `registration_erased` | 12 | recorded as erased; untrustworthy on both layers, retained as such; `actor: unknown` |
| `not_removed_control` | 10 | negative control — same corpus, same event window, still resolves |
| `removed_without_successor` | 9 | removal known, no replacement — the case a `reason` field exists for |
| `concept_root_severed_version_survives` | 8 | structure erasure: family root severed, bound version resolves |
| `membership_unresolved` | 8 | membership unconfirmed; a consumer must not assert a successor |
| `other_author_collision` | 8 | identifier belongs to someone else; correct behaviour is refusal |
| `quarantined_title_mismatch` | 8 | target gone (presence: removed); candidate successor's title disagrees — the edge is quarantined, not followed |
| `registry_resolution_divergence` | 8 | record-presence vs target-presence, subject-relative, diverged at the dated probe |
| `version_severed_root_survives` | 5 | the inverse structure erasure |
| `state_drift_documented` | 4 | same identifier, two honest recorded states hours apart, both dated |
| `not_an_identifier` | 3 | DOI-shaped string never registered; input validation |
| `superseded_present` | 4 | present record with a supersession edge; the edge governs retrieval and proves nothing about truth — validity stays `unassessed`, presence stays unmarked |
| `typo_immune_survivor` | 2 | recorded as survivor-by-error; observation contradicts; retained as contradiction |
| `withdrawn_removal_vs_destruction` | 2 | the ratified split embodied: removal-fact permanent and public (`axis_subject: content_payload` — the tombstone record itself resolves 200 by design), content destroyed on a separate disclosed path |
| `never_landed` | 1 | a registry asserted a body at a path where none existed; checkable where asserted; caught by a check; commit-hashed |
| `registry_update_not_landed` | 1 | the adjacent **inverse**: content landed, the registry update did not. Presence deliberately **unmarked** — the presence axis is not made to carry transaction atomicity |

---

## Verification

Two verifiers, two jobs:

- **`verify_offline.py` (default, no network):** schema shape, counts, the sparse-presence rule, subject-explicit axes, validity discipline, expectation consistency, repository evidence for the local cases. Conformance testing runs against the committed `cases.json`; it requires no live probes.
- **`reprobe_live.py` (optional):** routed by `identifier_kind`; emits a dated observation report and never mutates expected results. Live re-probing consumes external services (doi.org, api.datacite.org, alexanarch.org); requests are serialized with delays. Respect providers' rate limits.

`build_v2.py` (MIT) regenerates the fixture deterministically from the archived v1.0 base and the repository's current sources; the shipped fixture is frozen by `manifest.json` (file hashes + source commit).

## Files

- `cases.json` — the fixture (v2.1, 111 cases, probed at build)
- `cases-v1.0.json` — the archived v1.0 base (47 cases), for the drift ledger
- `deletion-fixture.schema.json` — JSON Schema for the fixture
- `build_v2.py` · `verify_offline.py` · `reprobe_live.py` — apparatus (MIT)
- `LICENSE-DATA` (CC0 1.0) · `LICENSE-CODE` (MIT)
- `manifest.json` — frozen metadata: hashes, source commit, counts

## Licensing

The dataset (`cases.json`, `cases-v1.0.json`, the schema, this README, the manifest) is released under **CC0 1.0**: the license covers the selection, annotation, arrangement, and original text, and does not — and cannot — relicense third-party identifiers or their metadata, which remain public-resolution artifacts recorded here as observed. The scripts are **MIT**. Identifiers in the corpus are public; the fixture records observed resolution state, not a judgment on any host's policy.

## Provenance appendix — where the numbers come from

- Population, recorded distribution, envelope layer: `data/doi-resolution-index.json` at the manifest's source commit; recount with the snippet in `build_v2.py`.
- Probe results: build probe pass, 2026-07-28 (HEAD terminal statuses; DataCite via GET with parsed `attributes.state` and UTC timestamps, embedded per-case). Re-derive with `reprobe_live.py`.
- Drift ledger: mapping-level diff, repository commits `188780b4` → current; derivation in the builder header.
- The 2026-06-19 event and downstream measurement (0.00% citation-field retention, n = 1,059 batches, 100% in controls): Alexanarch deposit #1081 (EA-EROSION-EMPIRICAL-01) and the Platform Erosion Observatory, as cited in the issue #207 filing.
- The 1,322,017-record purge figure: **reported figure, carried with its source** — deposit #451 and the issue #207 filing; not independently re-derivable from this repository.
- Withdrawals and write-failure cases: commit-hashed in this repository, 2026-07-28.
