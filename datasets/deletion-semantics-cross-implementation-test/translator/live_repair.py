#!/usr/bin/env python3
"""08 — the producer's own repair, live (2026-09-03).

Run 06 tested a CONSTRUCTED repair: prose tombstones lifted into the machine index by this
package's translator. On 2026-09-01 the producer shipped its own repair at
55e6493945a51c77e8a002630dc4890e90d7123e (knowledge-catalog#207). This run reads the
producer's real .manifest.json at that commit and re-asks the three questions of runs
04–06 against it, with no translation layer in between:

  1. Are A (present), B (removed), C (never landed) separable from the machine surface alone?
  2. Necessity: strip the absences map — do B and C collapse again?
  3. One level up: does the manifest say whether the absence pass RAN (absenceReconciliation)?

Usage: python3 translator/live_repair.py <path-to-bundle-checkout>   (stdlib only)
"""
import json, sys
from pathlib import Path

A = "remember://lesson/okf-conformance-fixture-001"
B = "remember://lesson/okf-conformance-tombstoned-000"
C = "remember://lesson/okf-conformance-never-landed-999"

def bare(rid): return rid.rsplit("/", 1)[-1]

def classify(m, rid):
    # FINDING (08): entries are keyed by bare lessonId ("okf-conformance-fixture-001"),
    # absences by full URI ("remember://lesson/okf-conformance-fixture-001"). The two maps
    # use different identifier forms for the same stable identity; a consumer must
    # normalise before it can test exclusivity or look one id up in both. Recorded as
    # 4_key_form_mismatch below; classification here normalises on the bare id.
    if rid in (m.get("entries") or {}) or bare(rid) in (m.get("entries") or {}): return "present"
    ab = (m.get("absences") or {}).get(rid)
    if ab: return ab.get("presence")
    rec = m.get("absenceReconciliation") or {}
    return "unwritten(default)" if rec.get("status") == "ok" else "unknown(pass not run)"

def main(root):
    mpath = Path(root)/"bundle"/".manifest.json"
    m = json.loads(mpath.read_text())
    out = {"manifest_keys": list(m.keys()), "commit_expected": "55e6493945a51c77e8a002630dc4890e90d7123e"}
    out["1_separability_live"] = {"A": classify(m, A), "B": classify(m, B), "C": classify(m, C)}
    out["1_B_record"] = (m.get("absences") or {}).get(B)
    out["1_exclusive_with_entries_after_normalisation"] = all(bare(k) not in (m.get("entries") or {}) for k in (m.get("absences") or {}))
    out["4_key_form_mismatch"] = {"entries_keys": list((m.get("entries") or {}).keys()), "absences_keys": list((m.get("absences") or {}).keys()),
                                  "note": "entries keyed by bare lessonId, absences by full remember:// URI; same identity, two forms. Exclusivity is only testable after normalisation."}
    stripped = dict(m); stripped.pop("absences", None)
    out["2_necessity_strip_absences"] = {"A": classify(stripped, A), "B": classify(stripped, B), "C": classify(stripped, C)}
    out["2_B_C_collapse_when_stripped"] = classify(stripped, B) == classify(stripped, C)
    out["3_reconciliation_key"] = m.get("absenceReconciliation")
    no_rec = dict(stripped); no_rec.pop("absenceReconciliation", None)
    out["3_without_reconciliation"] = {"B": classify(no_rec, B), "C": classify(no_rec, C)}
    out["verdict"] = {
        "separable_from_machine_surface": out["1_separability_live"] == {"A": "present", "B": "removed", "C": "never_landed"},
        "key_forms_uniform_across_maps": False,
        "absences_necessary": out["2_B_C_collapse_when_stripped"],
        "reconciliation_distinguishes_empty_from_unexamined": (m.get("absenceReconciliation") or {}).get("status") == "ok" and out["3_without_reconciliation"]["B"].startswith("unknown"),
    }
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "remember-okf-sample-bundle")
