# Deletion Semantics Conformance Fixture

**A known-bad identifier corpus for testing deletion, tombstone, and successor semantics.**

Fixture version 1.0 · 2026-07-28 · CC BY 4.0
Derived from the Zenodo DOI Resolution Index v3.5 (Crimson Hexagonal Archive)
Offered to `GoogleCloudPlatform/knowledge-catalog` issue #207

---

## What this is

47 identifiers, drawn from a real deletion event, selected so that each one exercises a distinct condition a deletion-semantics specification has to handle. Every case carries its recorded classification, its recorded verification date, and an independently observed terminal HTTP status probed on 2026-07-28.

It is not a sample of a corpus. It is a set of test cases, one small group per condition, chosen because between them they cover the conditions under which a consumer must behave differently.

## Why a corpus like this is hard to obtain

Deletion semantics cannot be tested against a healthy corpus. Testing requires identifiers that were deleted, at scale, by a third party, with the deletion documented, the successors known, and the pre-deletion state recorded. Corpora with those properties are rare because they require someone to have been instrumenting an archive *before* it was removed.

This corpus has those properties by accident rather than design: an account holding 1,938 registered identifiers was terminated on 2026-06-19, the archive was reconstructed on independent infrastructure, and the mapping from severed identifier to surviving work was built and versioned afterward.

---

## The numbers, and what they actually mean

Two independent numbers get confused, and the confusion matters for anyone building on this.

**Population.** The resolution index holds **1,938 identifiers**. This is not the same as 1,938 deletions, and the fixture does not claim it is.

**Recorded identifier state**, per-entry, last verified 2026-07-12:

| recorded state | count | meaning |
|---|---:|---|
| `verified_tombstone` | 1,815 | identifier resolves; the landing page is a tombstone |
| `verified_registered` | 75 | identifier resolves normally — *not* removed |
| `verified_erased_registration` | 32 | recorded as removed from the identifier system itself |
| `syntactically_valid_unverified` | 13 | DOI-shaped, state not established |
| `fragment_candidate` | 3 | never a registered identifier; a reconstruction artifact |

**Independent verification, 2026-07-28** (n = 115 probes, terminal status after redirects, retried past 503):

| recorded state | n | observed | agreement |
|---|---:|---|---:|
| `verified_tombstone` | 28 | 410 × 28 | **100%** |
| `verified_registered` | 26 | 200 × 23, 410 × 2, 404 × 1 | 88% |
| `verified_erased_registration` | 21 | 404 × 10, 410 × 11 | **48%** |
| `fragment_candidate` | 6 | 404 × 6 | 100% |
| `syntactically_valid_unverified` | 10 | 410 × 9, 200 × 1 | — |

Three consequences a consumer should know before relying on this data.

**The tombstone classification holds.** 28 of 28 verified. If a case says `verified_tombstone`, expect 410.

**`verified_erased_registration` does not hold and should not be trusted.** Under half the sample behaves as recorded; the remainder are tombstoned rather than erased. Either the original classification conflated two states, or states have changed since. The fixture retains the class and records the disagreement rather than silently reclassifying, because the disagreement is itself a test case: a consumer that treats a producer's recorded state as authoritative without verification will be wrong here roughly half the time.

**State drifts.** Two identifiers recorded as registered on 2026-07-12 were tombstoned by 2026-07-28, and one had lost its registration. Identifier state is not static and a fixture that assumes otherwise will rot.

---

## The internal control

The most useful property of this corpus is that it contains identifiers that still resolve.

`not_removed_control` (6 cases) returned **200** and `other_author_collision` (4 cases) returned **200**, probed in the same minute as the 410s. The second group is identifiers belonging to other authors that entered the corpus through reconstruction error — they were never in the terminated account, and they still work.

This means a consumer testing against this fixture cannot pass by assuming everything is dead, and cannot explain the 410s as a registry outage. The dead and the living are interleaved and were measured together.

---

## Case classes

| class | cases | condition exercised |
|---|---:|---|
| `removed_with_successor` | 8 | identifier severed, work survives, successor known — the ordinary case |
| `removed_without_successor` | 3 | removal known, no replacement exists — the anonymous involuntary case, and the reason a reason field is required |
| `registration_erased` | 6 | recorded as removed from the identifier system rather than tombstoned; see the reliability note above |
| `not_removed_control` | 6 | negative control — same corpus, same event window, identifier still resolves |
| `concept_root_severed_version_survives` | 4 | structure erasure: family-root severed while a bound version resolves |
| `version_severed_root_survives` | 3 | the inverse |
| `membership_unresolved` | 4 | corpus membership unconfirmed; a consumer must not assert a successor |
| `other_author_collision` | 4 | identifier belongs to a different author; the correct behaviour is refusal, not a guess |
| `quarantined_title_mismatch` | 4 | a candidate successor exists but its title does not match — inspection, not redirect |
| `not_an_identifier` | 3 | DOI-shaped string that was never registered; tests input validation |
| `typo_immune_survivor` | 2 | survived by transcription error, and has since been severed anyway — see note |

**On `typo_immune_survivor`:** both cases were recorded as having survived the deletion because a transcription error pointed them at identifiers outside the terminated account. Both returned **410** on 2026-07-28. Either the classification was wrong or they were severed subsequently. Retained as a case class precisely because it is a recorded state that observation contradicts.

---

## Conformance expectations

For each case the fixture states the condition, not the required behaviour, because required behaviour is what the specification is for. What a suite can assert:

1. **A consumer must distinguish "identifier absent" from "identifier present, content removed."** `not_an_identifier` (404 at the resolver) and `removed_with_successor` (410 at the landing page) are different failures and warrant different handling.
2. **A consumer must not infer removal from non-resolution alone.** `not_removed_control` resolves. `other_author_collision` resolves. Both are in a corpus described as deleted.
3. **A consumer must not assert a successor it cannot establish.** `membership_unresolved` and `quarantined_title_mismatch` have candidate targets that fail verification.
4. **A consumer must be able to represent removal without a successor.** `removed_without_successor` has no replacement and never will.
5. **A consumer must not treat a producer's recorded state as verified.** `registration_erased` disagrees with observation in half the sample. This is the case that makes the point most cheaply.

---

## Files

- `cases.json` — the 47 cases, each with recorded classification, verification date, work title, successor and successor kind where known, and the observed terminal status on 2026-07-28
- `verify.py` — re-probes every case and reports agreement between recorded and observed state; run it before relying on the fixture, because state drifts
- `README.md` — this file

## Limitations, stated

- Terminal status is observed through the DOI resolver and the landing host. The landing host returned 503 intermittently during probing and 403 to some user agents; `verify.py` retries past 503 and its results should be read as best-effort rather than authoritative.
- Recorded classifications derive from a single producer's audit, dated 2026-07-12, and one class is demonstrably unreliable.
- The corpus is one archive from one publisher and one deletion event. It establishes that these conditions occur and gives concrete instances; it does not establish their frequency in the wild.
- Successors, where given, are that producer's own reconstructions. A conformance suite should treat them as claims to verify, not as ground truth.

## Provenance

Derived from `alexanarch.org/data/doi-resolution-index.json` (v3.5, CC BY 4.0), which is the companion dataset to a documented account termination of 2026-06-19. Upstream discussion at `github.com/zenodo/zenodo/issues/2606`.
