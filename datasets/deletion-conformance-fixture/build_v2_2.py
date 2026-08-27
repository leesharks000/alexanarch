#!/usr/bin/env python3
"""build_v2_2.py — derive v2.2 from v2.1 by appending six cases the cross-implementation
test showed v2.1 could not test.

v2.1 established the never_landed direction and then, in the cross-test of 2026-08-26
(https://www.alexanarch.org/datasets/deletion-semantics-cross-implementation-test/),
turned out to barely exercise it: 1 never_landed case in 111, and every fully expressible
presence value 'removed'. The distinction the cross-test turns on was under-represented in
the fixture that helped uncover it. This cut repairs that, and says so rather than making
v2.1 look as though it tested more than it did.

Additions:
  A/B/C matched under one convention, with B split in two — the split IS the cross-test's
  finding, that a removal recorded only in prose and a write that never landed are
  observationally identical to a consumer reading the machine-readable discovery surface.
  Plus the intake-acknowledgment pair offered on knowledge-catalog#207.
MIT.
"""
import json
from pathlib import Path
from collections import Counter

CONV = ("matched convention: producer-controlled identity, filenames diverging from stable ids, "
        "one write-claim log, one machine-readable index, prose removal record")

NEW = [
{ "case_class": "present_control_matched",
  "identifier": "okf-abc-present-001",
  "observed_2026_08_26": 'record present at the declared location; listed in the machine-readable index', "identifier_kind": "declared_path",
  "work_title": "A — record created and present (matched control)",
  "recorded": {"declared_in": "producer write-claim log", "declared_state": "record at a producer-controlled location",
               "discovery_surface": "listed in the machine-readable index", "convention": CONV},
  "axes": {"validity": "unassessed",
           "note": "presence deliberately UNMARKED: nothing is absent. The control against which the two absence cases are read."},
  "axis_subject": {"kind": "claim", "identifier": "okf-abc-present-001"},
  "test": "the matched present case. A consumer must not mark it, and its presence in the index is what the two absence cases are contrasted against.",
  "expected": {"emit_presence": None, "must_not_mark_never_landed": True} },

{ "case_class": "removed_absence_on_discovery_surface",
  "identifier": "okf-abc-removed-002",
  "observed_2026_08_26": 'record absent from the declared location; absence assertion present in the machine-readable index (id, presence, date, reason, recording authority, successor)', "identifier_kind": "declared_path",
  "work_title": "B(i) — created, then removed; absence assertion exposed on the machine-readable discovery surface",
  "recorded": {"declared_in": "producer write-claim log", "declared_state": "record at a producer-controlled location",
               "removal_recorded": "id, presence, date, reason, recording authority, successor",
               "discovery_surface": "absence assertion present in the machine-readable index", "convention": CONV},
  "axes": {"presence": "removed", "validity": "unassessed",
           "edges": {"successor": "okf-abc-present-001", "relationship": "curation_successor"},
           "note": "the repaired condition: the removal is where a consumer reads."},
  "reason": {"actor": "producer", "reason": "ownership_correction",
             "note": "curation; recorded with a recording authority, which is what makes the absence attributable rather than merely observed"},
  "removal_fact_retained": True, "content_destroyed": False,
  "axis_subject": {"kind": "claim", "identifier": "okf-abc-removed-002"},
  "test": "a removal exposed on the surface the consumer consults. Must be emitted as removed and must NOT be scored never_landed — the write landed and was later withdrawn.",
  "expected": {"emit_presence": "removed", "must_not_mark_never_landed": True,
               "preserve_reason": True, "follow_successor": True,
               "require_absence_on_discovery_surface": True} },

{ "case_class": "removed_absence_prose_only",
  "identifier": "okf-abc-removed-prose-004",
  "observed_2026_08_26": 'record absent from the declared location; absence assertion present in a prose removal file and ABSENT from the machine-readable index', "identifier_kind": "declared_path",
  "work_title": "B(ii) — created, then removed; absence recorded in prose only, absent from the machine-readable index",
  "recorded": {"declared_in": "producer write-claim log", "declared_state": "record at a producer-controlled location",
               "removal_recorded": "id, presence, date, reason, successor — in a prose removal file",
               "discovery_surface": "NOT exposed in the machine-readable index", "convention": CONV},
  "axes": {"presence": "removed", "validity": "unassessed",
           "edges": {"successor": "okf-abc-present-001", "relationship": "curation_successor"},
           "note": "the observed condition of a real producer bundle (remember/0.2, 2026-08-26): the removal is recorded in full and is not on the surface a consumer reads."},
  "reason": {"actor": "producer", "reason": "ownership_correction",
             "note": "the producer did not lose the removal; the consumer cannot see it"},
  "removal_fact_retained": True, "content_destroyed": False,
  "evidence": ["https://www.alexanarch.org/datasets/deletion-semantics-cross-implementation-test/ (necessity and sufficiency runs, 2026-08-26)"],
  "axis_subject": {"kind": "claim", "identifier": "okf-abc-removed-prose-004"},
  "test": "THE discriminating case. A consumer reading only the machine-readable discovery surface will score this identically to the never-landed case below — demonstrated on two independently built implementations. A conformant consumer must either resolve it as removed or report that the absence assertion is unreachable; it must not silently emit never_landed.",
  "expected": {"emit_presence": "removed", "must_not_mark_never_landed": True,
               "require_absence_on_discovery_surface": True,
               "known_collision_with": "never_landed_matched",
               "note": "a consumer that emits never_landed here has reproduced the cross-implementation collision" } },

{ "case_class": "never_landed_matched",
  "identifier": "okf-abc-neverlanded-003",
  "observed_2026_08_26": 'location absent; never written, and no absence assertion exists on any surface', "identifier_kind": "declared_path",
  "work_title": "C — creation asserted, never landed (matched)",
  "recorded": {"declared_in": "producer write-claim log", "declared_state": "record at a producer-controlled location",
               "discovery_surface": "no record and no absence assertion — the location was never written",
               "convention": CONV},
  "axes": {"presence": "never_landed", "validity": "unassessed",
           "note": "no removal occurred; the assertion was never satisfied. Distinguished from B only by the presence or absence of a surviving absence assertion."},
  "reason": {"actor": "producer", "reason": "producer_bug"},
  "axis_subject": {"kind": "claim", "identifier": "okf-abc-neverlanded-003"},
  "test": "the matched never-landed case. Correctly emitted as never_landed; the conformance question is whether a consumer distinguishes it from B(ii), which it does not resemble in the producer's records and does resemble on the consumer's surface.",
  "expected": {"emit_presence": "never_landed", "check_assertion_at_source": True} },

{ "case_class": "acknowledged_then_silent",
  "identifier": "intake-ack-2026-08-26-a",
  "observed_2026_08_26": 'registration absent at every later date; no withdrawal, rejection, or absence assertion recorded', "identifier_kind": "state_change_claim",
  "work_title": "Dated intake acknowledgment, no subsequent registration",
  "recorded": {"declared_in": "intake acknowledgment, dated", "declared_state": "submission received and queued for registration",
               "observed_condition": "no registration at any later date; no withdrawal, no rejection, no absence assertion"},
  "axes": {"presence": "never_landed", "validity": "unassessed",
           "note": "the acknowledgment is what makes this checkable. Without a dated acceptance, absence is deniable lag; with one, silence is a dated falsity about a specific assertion."},
  "reason": {"actor": "unknown", "reason": "unknown",
             "note": "mechanism unattributable from the record; the acknowledgment is the only assertion available"},
  "axis_subject": {"kind": "claim", "identifier": "intake-ack-2026-08-26-a"},
  "test": "extends the assertion boundary from producer logs into intake systems. A dated acknowledgment is an assertion checkable where it was made; sustained silence against it is not slowness but a claim that did not become true.",
  "expected": {"emit_presence": "never_landed", "check_assertion_at_source": True,
               "require_dated_acknowledgment": True} },

{ "case_class": "acknowledged_registered_late",
  "identifier": "intake-ack-2026-08-26-b",
  "observed_2026_08_26": 'registration present, dated later than the acknowledgment, delay visible in the record', "identifier_kind": "state_change_claim",
  "work_title": "Dated intake acknowledgment, registration completed late and honestly",
  "recorded": {"declared_in": "intake acknowledgment, dated", "declared_state": "submission received and queued for registration",
               "observed_condition": "registered at a later date, with the delay visible in the record and no backdating"},
  "axes": {"validity": "unassessed",
           "note": "presence deliberately UNMARKED: the claim became true, late. The must-not-mark twin of the case above."},
  "reason": {"actor": "producer", "reason": "not_disclosed", "note": "delay disclosed by the dated record itself"},
  "axis_subject": {"kind": "claim", "identifier": "intake-ack-2026-08-26-b"},
  "test": "the explicit trap for the intake pair: a checker that scores latency as disappearance fails here. Slow is not silent, and an honestly late registration must not be marked.",
  "expected": {"emit_presence": None, "must_not_mark_never_landed": True,
               "must_not_score_latency_as_absence": True} },
]

def main():
    d = json.loads(Path("cases.json").read_text())
    assert d["version"] == "2.1", f"expected v2.1 base, got {d['version']}"
    Path("cases-v2.1.json").write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    have = {c["identifier"] for c in d["cases"]}
    added = [c for c in NEW if c["identifier"] not in have]
    d["cases"].extend(added)
    d["version"] = "2.2"
    d["date"] = "2026-08-26"
    d["total_cases"] = len(d["cases"])
    d["classes"] = dict(sorted(Counter(c["case_class"] for c in d["cases"]).items()))
    d["v2_1_limitation_ledger"] = (
        "v2.1 held 111 cases with exactly ONE never_landed case, and every fully expressible "
        "presence value was 'removed'. The cross-implementation test of 2026-08-26 turned on the "
        "removed/never_landed distinction and found that the fixture built to test it barely "
        "represented it. v2.2 adds six cases in response. This ledger exists so v2.1 is not read "
        "retroactively as having tested more than it did.")
    d["v2_2_additions"] = {
        "observation_convention_note": (
      "All six carry a top-level observed_<date> field. 110 of the 111 v2.1 cases already did; the one "
      "exception (registry_update_not_landed) is a must-not-mark case whose observation sits in recorded, "
      "so nothing ever had to read it. Authoring the new cases in that exception's style made them "
      "undetectable to a consumer that extracts observations from top-level observed_* keys — which is how "
      "the reference checker does it. The convention was load-bearing and undocumented; it is documented here."),
  "matched_trio": "A present, B(i) removal exposed on the discovery surface, B(ii) removal in prose only, "
                        "C never landed — one convention, four cases. B is split because the split is the finding: "
                        "B(ii) and C are observationally identical to a consumer reading the machine index, "
                        "demonstrated on two independently built implementations.",
        "intake_pair": "acknowledged_then_silent, where a dated acceptance converts later silence from deniable lag "
                       "into checkable falsity, and its must-not-mark twin acknowledged_registered_late, so a checker "
                       "cannot score latency as disappearance. Offered on knowledge-catalog#207.",
        "new_expected_keys": ["require_absence_on_discovery_surface", "require_dated_acknowledgment",
                              "must_not_score_latency_as_absence", "known_collision_with"],
        "new_recorded_key": "discovery_surface — where, if anywhere, a surviving absence assertion is machine-readable",
        "derived_from": "https://www.alexanarch.org/datasets/deletion-semantics-cross-implementation-test/"}
    Path("cases.json").write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    print(f"v2.2: {d['total_cases']} cases (+{len(added)}); v2.1 retained as cases-v2.1.json")
    print("presence distribution:", dict(Counter(
        (c.get('axes') or {}).get('presence', 'unmarked') for c in d['cases'])))

if __name__ == "__main__":
    main()
