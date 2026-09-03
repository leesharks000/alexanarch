#!/usr/bin/env python3
"""reference_verdict.py — two consumers over this fixture, to show what v2.2 requires.

UNREPAIRED decides presence from what the record asserted and what is there now. That is
sufficient for v2.1 and false-positives on the v2.2 absence cases: a removal it cannot see
is indistinguishable from a write that never landed.

REPAIRED adds one lookup — before assigning never_landed, ask whether a surviving absence
assertion is reachable on the discovery surface. That is the whole difference.

v2.2 (2026-09-03) adds the collision one level up, from the producer's own experience of
building the repair (knowledge-catalog#207, open-knowledge-format#11): an empty absences map
means "nothing removed" only if a sibling reconciliation key says the pass ran; without it the
consumer must emit a third state, pass_not_run, and never "clean".

Run: python3 reference_verdict.py           MIT.
"""
import json, sys
from pathlib import Path

ABSENT_WORDS = ("absent", "missing", "not present", "no body")

def observed(case):
    """Normalize BOTH observation locations, per the schema's observation_convention.

    Reading only the canonical top-level form made six v2.2 cases invisible during
    authoring — a record present in the corpus and unreachable to the consumer, which
    is the failure this fixture exists to detect, committed by the fixture's own tooling.
    """
    parts = [str(v) for k, v in case.items() if k.startswith("observed_")]
    alt = (case.get("recorded") or {}).get("observed_condition")
    if alt:
        parts.append(str(alt))
    return " ".join(parts).lower()

def declares_body(case):
    rec = case.get("recorded") or {}
    return (case.get("identifier_kind") == "declared_path"
            or (case.get("axis_subject") or {}).get("kind") == "registry_assertion"
            or "declared_state" in rec)

def unrepaired(case):
    """v2.1-era consumer: asserted a body, body is gone -> never_landed."""
    if not declares_body(case):
        return None
    return "never_landed" if any(w in observed(case) for w in ABSENT_WORDS) else None

def absence_assertion_reachable(case):
    """Is a surviving absence assertion exposed where a consumer reads? The fixture states
    this in recorded.discovery_surface; a live consumer would consult the producer's index."""
    ds = ((case.get("recorded") or {}).get("discovery_surface") or "").lower()
    if not ds:
        return None                      # nothing declared: cannot tell
    if "absent from the machine-readable index" in ds or "not exposed" in ds:
        return False                     # recorded, but not where the consumer reads
    if "absence assertion present" in ds:
        return True
    return None

def reconciliation_state(case):
    """v2.2 (2026-09-03): the collision one level up. An empty absences map with a
    reconciliation key of status ok is a clean examined corpus; without the key, nobody
    looked. The fixture states this in recorded.declared_state; a live consumer would read
    the producer's absenceReconciliation key (remember/0.2 at 55e6493)."""
    ds = ((case.get("recorded") or {}).get("declared_state") or "").lower()
    if "absencereconciliation status ok" in ds:
        return "ran"
    if "absencereconciliation absent" in ds or "not ok" in ds:
        return "not_run"
    return None

def repaired(case):
    v = unrepaired(case)
    rs = reconciliation_state(case)
    if rs == "not_run":
        return "pass_not_run"                                  # a third state, never 'clean', never never_landed
    if rs == "ran" and v is None:
        return None                                            # clean, examined
    if v != "never_landed":
        return v
    reach = absence_assertion_reachable(case)
    if reach is True:
        return (case.get("axes") or {}).get("presence")      # the surviving assertion answers
    if reach is False:
        return "unreachable_absence_assertion"               # report, do not silently collapse
    return "never_landed"

def score(cases, verdict):
    tp = fp = fn = 0; failures = []
    for c in cases:
        got = verdict(c)
        want = (c.get("expected") or {}).get("emit_presence")
        if want == "never_landed" and got == "never_landed": tp += 1
        elif got == "never_landed" and want != "never_landed":
            fp += 1; failures.append(("false positive", c["case_class"], c["identifier"]))
        elif got is None and want == "never_landed":
            fn += 1; failures.append(("missed", c["case_class"], c["identifier"]))
    trap = [c for c in cases if (c.get("expected") or {}).get("must_not_mark_never_landed")]
    trap_ok = all(verdict(c) != "never_landed" for c in trap)
    return {"true_positives": tp, "false_positives": fp, "missed": fn,
            "must_not_mark_cases": len(trap), "must_not_mark_passed": trap_ok,
            "failures": failures}

if __name__ == "__main__":
    d = json.loads(Path("cases.json").read_text())
    cases = d["cases"]
    print(f"{d['name']} v{d['version']} — {len(cases)} cases\n")
    for name, fn in (("UNREPAIRED", unrepaired), ("REPAIRED", repaired)):
        r = score(cases, fn)
        print(f"── {name} ──")
        print(f"  true positives {r['true_positives']} · false positives {r['false_positives']} · "
              f"missed {r['missed']} · must-not-mark {r['must_not_mark_cases']} cases, "
              f"{'passed' if r['must_not_mark_passed'] else 'FAILED'}")
        for f in r["failures"]: print(f"    ! {f[0]}: {f[1]} {f[2]}")
        print()
    print("The difference is one lookup: consult the discovery surface before assigning never_landed.")
