# Deletion Semantics Conformance Fixture

**A known-bad identifier corpus for testing deletion, tombstone, presence, and successor semantics.**

Fixture version 2.0 — the ratified-axes release · 2026-07-28 · CC BY 4.0
Derived from the Zenodo DOI Resolution Index (current, envelope layer) + the Alexanarch registry + dated repair artifacts
Offered to `GoogleCloudPlatform/knowledge-catalog` issue #207

---

## What this is

111 cases across 16 classes, drawn from a real deletion event and its aftermath, selected so that each class exercises a distinct condition a deletion-semantics specification has to handle. Every DOI-kind case carries its recorded state (the producer layer), an independently probed terminal HTTP status from 2026-07-28, and — new in 2.0 — its expression in the three ratified axes: **validity** (does the claim hold), **presence** (is it here — sparse: `removed` | `never_landed` | no marker), and **edges** (what governs retrieval). Where a `reason` exists it is an object with an actor; `not_disclosed` is a first-class value, because the corpus's own deletion event never came with one.

It is not a sample of a corpus. It is a set of test cases, one group per condition, chosen because between them they cover the conditions under which a consumer must behave differently.

## Why a corpus like this is hard to obtain

Deletion semantics cannot be tested against a healthy corpus. Testing requires identifiers that were deleted, at scale, by a third party, with the deletion documented, the successors known, and the pre-deletion state recorded. This corpus has those properties by accident rather than design: an account holding 1,938 registered identifiers was terminated on 2026-06-19, the archive was reconstructed on independent infrastructure, and the mapping from severed identifier to surviving work was built and versioned afterward. Between fixture versions, two identifiers were withdrawn by the producer itself for disclosed reasons — which is why the population below reads 1,937.

---

## The numbers

**Population.** The resolution index holds **1,937 identifiers** (v1.0, hours earlier: 1,938 — see the drift ledger). Not 1,937 deletions; the recorded layer says which is which:

| recorded validity (envelope layer, current) | count |
|---|---:|
| `verified_tombstone` | 1,815 |
| `verified_registered` | 73 |
| `verified_erased_registration` | 32 |
| `syntactically_valid_unverified` | 13 |
| `fragment_candidate` | 3 |

**Independent verification, 2026-07-28** (109 case identifiers probed; terminal status after redirects, retried past 503):

| recorded validity | n | observed | agreement |
|---|---:|---|---:|
| `verified_tombstone` | 62 | 410 × 62 | **100%** |
| `verified_registered` | 18 | 200 × 18 | **100%** |
| `verified_erased_registration` | 12 | 404 × 7, 410 × 5 | **split — see below** |
| `fragment_candidate` | 3 | 404 × 3 | 100% |
| `syntactically_valid_unverified` | 6 | 410 × 4, 200 × 2 | — (no expectation asserted) |

**The tombstone classification holds at scale.** 62 of 62. If a case says `verified_tombstone`, expect 410.

**`verified_erased_registration` remains untrustworthy and is retained for exactly that reason.** Roughly half the class behaves as recorded. A consumer that treats a producer's recorded state as authoritative without verification will be wrong here about half the time — which is a test case, not a defect.

**Registry and resolution can disagree, live.** The new `registry_resolution_divergence` class went **8 for 8**: the DataCite API returns 200 (state findable) while the DOI resolves 410 (gone), probed in the same minute. Two authorities, one identifier, opposite answers. A consumer must carry both and collapse neither.

---

## The drift ledger (v1.0 → v2.0, same day)

State is not static, and the fixture's own version history is the exhibit:

- **Population 1,938 → 1,937**: two records withdrawn by the producer on 2026-07-28, reasons disclosed (`withdrawn_removal_vs_destruction` cases carry them).
- **Recorded `verified_registered` 75 → 73**: two identifiers changed recorded state within the day.
- **Observation drift on the v1 base: zero.** All 47 v1 identifiers returned the same terminal status hours apart — stability at hours-scale, drift at days-scale (v1 documented two 2026-07-12 → 2026-07-28 changes). Both scales are in the data.

---

## The internal control

`not_removed_control` (10 cases) returned **200**, and `other_author_collision` (8 cases) probes live in the same window: the dead and the living are interleaved and were measured together. A consumer cannot pass by assuming everything is dead, and cannot explain the 410s as a registry outage.

---

## Case classes (16)

| class | cases | condition exercised |
|---|---:|---|
| `removed_with_successor` | 20 | identifier severed, work survives, successor known — the ordinary case |
| `registration_erased` | 12 | recorded as erased from the identifier system; the untrustworthy class, retained as such |
| `not_removed_control` | 10 | negative control — same corpus, same event window, still resolves |
| `removed_without_successor` | 9 | removal known, no replacement — the case a `reason` field exists for |
| `concept_root_severed_version_survives` | 8 | structure erasure: family root severed, bound version resolves |
| `membership_unresolved` | 8 | membership unconfirmed; a consumer must not assert a successor |
| `other_author_collision` | 8 | identifier belongs to someone else; correct behaviour is refusal |
| `quarantined_title_mismatch` | 8 | candidate successor exists, title disagrees — inspection, not redirect |
| `registry_resolution_divergence` | 8 | **new** — DataCite says findable, resolution says gone; both true, in different senses |
| `version_severed_root_survives` | 5 | the inverse structure erasure |
| `state_drift_documented` | 4 | **new** — same identifier, two honest recorded states hours apart, both dated |
| `not_an_identifier` | 3 | DOI-shaped string never registered; input validation |
| `never_landed` | 2 | **new** — a dated assertion of a state that had not landed, caught by a check; both directions (record-without-content, content-without-record) |
| `superseded_present` | 2 | **new** — present record, edges redirect governance: the false-but-present quadrant |
| `typo_immune_survivor` | 2 | recorded as survivor-by-error; observation contradicts; retained as contradiction |
| `withdrawn_removal_vs_destruction` | 2 | **new** — the ratified split embodied: removal-fact permanent and public, content destroyed on a separate disclosed path, successor edge pointing to the owner's live identifier |

---

## The axes, as carried

Every case bears `axes`. Presence is **sparse**: `removed` and `never_landed` are the only named states, and the absence of a marker means what the spec default means — a producer cannot know that no unrecorded prior state existed, so no default is asserted. Validity is independent (`holds` on most severed identifiers: the works remain real; only the pointer died). Edges carry successors and supersession without implying anything about presence. The `reason` object separates actor from rationale, and the 89 termination-class cases carry `reason: not_disclosed, actor: host` — truthfully, because no per-record rationale was ever provided.

---

## Files

- `cases.json` — the fixture (v2.0, 111 cases, probed)
- `cases-v1.0.json` — the archived v1.0 base (47 cases), for the drift ledger
- `build_v2.py` — the builder: selection predicates, axes mapping, probe apparatus; deterministic, reruns from the archived base
- `verify.py` — re-probe everything and report agreement; run it before relying on the fixture
- `manifest.json` — dataset metadata

## Provenance appendix — where the numbers come from

- Population, recorded distribution, envelope layer: `data/doi-resolution-index.json` (this repository, current commit) — recount: `python3 - <<'P'` … see build_v2.py header.
- Probe results: `build_v2.py` probe pass, 2026-07-28, cache retained at build time; re-derive with `verify.py`.
- The 2026-06-19 event and downstream measurement (0.00% citation-field retention, n = 1,059 batches, 100% in controls): Alexanarch deposits #1081 (EA-EROSION-EMPIRICAL-01) and the Platform Erosion Observatory; the figures as cited to issue #207 on filing.
- The 1,322,017-record purge figure: reported figure, carried with its source — deposit #451 (the OKF correspondence record) and the issue #207 filing; not independently re-derivable from this repository.
- Withdrawals and never-landed cases: commit-hashed in this repository, 2026-07-28.
