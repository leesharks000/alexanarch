# EA-3I-HAILMARY-01 — complete source package

This folder contains **the complete contents** of the conversation package `EA-3I-HAILMARY-01.zip`, uploaded individually as GitHub-readable source files because ZIP downloads are unavailable to the user. Both uploaded files were verified byte-identical to the originals by Git blob SHA.

| File | Purpose | Original Git blob SHA |
|---|---|---|
| [EA-3I-HAILMARY-01.md](EA-3I-HAILMARY-01.md) | Complete 11,162-byte archive-derived research instrument; rationale, evidence table, full procedure and interpretation rules | `7c6de95c4d83af94784d742aab3346a783e6b972` |
| [score_false_drift.py](score_false_drift.py) | Complete 6,323-byte executable cohort scorer and synthetic self-test | `5c6724b4cde207bff93ecc0095f039323a8959fc` |

Relevant existing independent resources:
- [Latest measured original-thirteen GBT result (OH13R)](../RESULT-GBT-cc7-original-thirteen-OH13R.md).
- [Canonical full counterfactual receiver specification](../PLAN-EA-3I-HAILMARY-01-the-receiver-test.md).
- [Networked-worker execution handoff, issue #29](https://github.com/leesharks000/lagrange-observatory/issues/29).
- [Original-historical selection code](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/oh13/code/oh_scan.py).

Run the scorer's synthetic self-test:

```bash
python score_false_drift.py --self-test
```

After the networked GBT voltage worker produces the **measured** per-cohort input JSON from the original forty historical false-drift selections:

```bash
python score_false_drift.py --input measured_cohorts.json --output final_rank.json
```

**Empirical status as uploaded:** OH13R actual-voltage test completed; final false-drift cohort extraction and its measured rank test **not yet executed**. Synthetic scorer validation does not constitute a telescope result. No extraterrestrial signal identified.