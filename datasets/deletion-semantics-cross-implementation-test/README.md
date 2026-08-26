# Deletion Semantics — Cross-Implementation Test v1.0

**A recorded removal and a never-landed write are observationally identical at the consumer
boundary. Exposing the absence assertion on a machine-readable discovery surface is necessary and
sufficient to separate them.**

Reproducibility package for a cross-implementation test run 2026-08-26, fulfilling the cross-test
offered on [knowledge-catalog#207](https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/207).
Three artifacts, none modified, none authored by the same party:

| | artifact | role |
| --- | --- | --- |
| producer | [andrewcrenshaw/remember-okf-sample-bundle](https://github.com/andrewcrenshaw/remember-okf-sample-bundle) @ `ea18185f` | remember/0.2 emitted shape |
| consumer | [inkxel/throughline](https://github.com/inkxel/throughline) @ `c512e8b9` `scripts/never_landed.py` | assertion-consistency checker |
| corpus | [deletion-conformance-fixture v2.1](https://www.alexanarch.org/datasets/deletion-conformance-fixture/) | 111 cases, built before either implementation existed |

**Read [`reports/FINDINGS.md`](reports/FINDINGS.md) first.** Reproduce from clean clones with
[`commands/reproduce.sh`](commands/reproduce.sh); pins in [`sources/source-lock.json`](sources/source-lock.json).

## Results in brief

- Both published baselines reproduce exactly (third independent reproduction of each); bundle integrity verified against its own `SHA256SUMS`, 0 mismatches.
- **Representation portability is 1/111** while checker portability holds on two flags — these are different properties.
- **A clean downstream verdict is not evidence of translation fidelity**: a forced translation fabricated 110 write-claims and dropped 451 facts, and produced the same clean result. The translation receipt makes that inseparable from the verdict.
- **The decisive collision**: `A present · B removed-with-tombstone · C never-landed` → the consumer returns `present · never_landed · never_landed`. The producer recorded the removal; the machine index does not carry it.
- **The repair**, tested both ways: with the absence record in the index, `A present · B removed · C never_landed`. Strip it and leave the prose tombstone intact, and B and C collide again.

## Normative form of the requirement

> A surviving absence assertion must be exposed on a machine-readable discovery surface that
> ordinary consumers consult. Preserving the same information only in prose is insufficient.

Not "put tombstones in `.manifest.json`" — that is one producer's carrier, not a format primitive.

## Layout

    sources/       pinned third-party artifacts + source-lock.json
    translator/    translate.py, receipt.py, repair.py, tomb.py (+ the checker, as run)
    receipts/      translation receipts, strict and forced
    profiles/      field-level break profiles
    fixtures/abc/  the three-record fixture, source and repaired
    runs/          01 baselines · 02 strict · 03 forced · 04 collision · 05 necessity · 06 sufficiency · 07 corpus
    reports/       FINDINGS.md
    commands/      reproduce.sh

Credit: the `--id-key` resolution path and the empty-log guard are @andrewcrenshaw's contributions
to @inkxel's checker; the checker and the bundle are their work. This package composes them and
adds the translation, the receipt, the fixture, and the repair test.

CC BY 4.0 · Crimson Hexagonal Archive
