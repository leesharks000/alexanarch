# Alexanarch record audit — final completion report v1.0

## Verdict

The immutable record audit is complete for the frozen Alexanarch corpus at commit `055429ac82edc967f09c4640ffd0b049cff78e6e`.

- **Coverage:** #1–#1426
- **Records audited:** 1,426 / 1,426 (100.00%)
- **Records #1427 and later:** out of scope
- **Repository repairs performed:** none
- **Audit method:** Alexanarch Audit Method Core v0.4
- **Terminal geometry:** #19–#38 followed by the non-overlapping terminal checkpoint #1–#18

This completes the audit. It does **not** declare the registry remediated. The sealed rows preserve what was found at the frozen commit and separate registration disposition from later repair work.

## Cumulative outcome

| Severity | Records |
|---|---:|
| OK | 284 |
| P0 | 124 |
| P1 | 519 |
| P2 | 464 |
| P3 | 35 |

| Registration disposition | Records |
|---|---:|
| HARVEST | 304 |
| HARVEST_WITH_WARNING | 991 |
| WITHHOLD | 131 |

Severity and disposition are independent controlled fields; they should not be forced into a one-to-one equivalence. The inherited audit includes 131 WITHHOLD dispositions and 124 P0 severity findings.

## What the audit found

The dominant recurring failure was not loss of work identity. It was **flattening at the registration and projection layer**: authorial and contributor roles collapsed into a single creator field; explicit historical or draft versions projected as v1.0; bibliographic types generalized or changed; publication, revision, deposit, and restoration dates collapsed; and metadata packets or later manifestations seated as if they were the primary object.

Across the inherited defect-code vocabulary, the largest recurring labels include bibliographic-type conflict, standing/lifecycle ambiguity, creator-authority flattening, primary-creator conflict, missing primary manifestation, title projection, and uncorroborated or conflicting version fields. These labels were created across multiple audit phases and are not mutually exclusive; the authoritative unit remains the individual record row and its sealed checkpoint.

## Terminal checkpoint #1–#18

The terminal checkpoint produced **13 P1 and 5 P2 findings**, all `HARVEST_WITH_WARNING`; there were no P0 or direct-HARVEST rows.

The most consequential terminal conditions were:

- **#1:** the complete work survives on the static page, but registry/page v9 dated 2026-06-19, stale SPXI v8.1 dated 2026-06-20, and current body v9.1 FINAL dated 2026-06-20 conflict. The separately staged canonical Markdown is absent.
- **#2:** the complete prose poem survives on-page and its authorship is readable; the staged Markdown is absent, and the frozen registry itself distinguishes a historical frontmatter-hash claim from the current serialization.
- **#3–#4:** the pages explicitly say their JSON datasets are the canonical artifacts, but those datasets are absent from the frozen source bundle. #4 also projects v3.8.1 over v3.11.0 and collapses original and revision dates.
- **#6:** Claude is omitted from the declared two-author navigation map.
- **#10–#11, #13–#14, and #16:** explicit v5.0–v7.0, build 6.3, or v0.6 identities are projected as v1.0.
- **#12:** the Assembly Chorus is omitted and a declared meta-deposit/“Other” object is classified as a theoretical paper.
- **#15:** witness/traversal-event documentation is classified as the navigation map it documents.
- **#16:** Talos Morrow’s author role and Lee Sharks’s human-operator role are reversed.
- **#18:** Rebekah Cranes is added to a Lee Sharks/Johannes Sigil body byline, while a theoretical protocol paper is classified as creative work.

Twelve AXN sequence-discontinuity boundaries occur inside #1–#18. They are recorded as frozen custody facts only; no missing identifiers were reconstructed.

## Source completeness and custody

The frozen #1–#358 bundle contains 358 registry rows and 358 static pages, but 354 staged canonical texts. Deposits #1–#4 lack staged text files. That asymmetry is preserved as evidence:

- #1–#2 retain complete page-embedded bodies.
- #3–#4 retain metadata/descriptive pages but not the declared canonical JSON artifacts.

The structured source-discontinuity register is `alexanarch_audit_final_source_discontinuities_v1.0.json`.

## Required downstream work

### 1. Controlled lifecycle conversion: #1–#498

Lifecycle conversion remains deliberately deferred. For rows **#1–#498**, `lifecycle_state`, `lifecycle_basis`, and `lifecycle_confidence` remain null, with the standing note:

> Raw frozen lifecycle field was not converted into a controlled standing state; no lifecycle inference was made in this checkpoint.

A separate reviewed pass must convert the raw lifecycle language for **#1–#498** into the controlled standing model, preserving evidence basis and confidence. This conversion must not alter the sealed audit findings.

### 2. Registration remediation planning

Prioritize records currently marked WITHHOLD and P0, then warning-level creator, version, type, date, and manifestation defects. Repairs should be issued as new derived remediation artifacts or registry changes with their own custody trail, never by rewriting an immutable checkpoint.

### 3. Primary-manifestation recovery

Any absent, proxy, wrong-version, or unverified primary object requires separately authenticated recovery evidence. The frozen source state and the audit conclusion must remain unchanged even after recovery succeeds.

## Handoff architecture

The final cumulative ZIP contains:

- the governing inherited handoff for #359–#1426;
- the frozen source bundle for #1–#358;
- all 18 immutable thread checkpoints covering #1–#358;
- the merged 1,426-row JSON and CSV ledgers;
- Method Core v0.4;
- final completion summary and source-discontinuity register;
- chronology, manifest, validation record, and internal `SHA256SUMS.txt`.

The merged ledger is the navigation surface. Each nested immutable checkpoint is the authoritative source for its record adjudications.
