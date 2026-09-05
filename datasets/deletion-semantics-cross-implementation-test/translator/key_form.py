#!/usr/bin/env python3
"""09 — the key-form repair, live (2026-09-05).

Run 08 found `entries` keyed by bare lesson id and `absences` by full remember:// URI — one identity in two
forms, so the exclusivity invariant was only testable after a consumer normalised, and held trivially before.
The producer repaired it at 3806111cad1a058585242f7ad78716c4a767c782: every entries and absences value carries
an `id` in the remember://lesson/<id> form, and the invariant is asserted over those values. This run checks,
from the document alone and with NO normalisation: one form, every value carries the field, disjoint.
It also states the producer's own note: the 2026-09-01 audit had stripped the URI prefix silently — a check
normalised by knowledge the document never stated — the same defect one layer up.

Usage: python3 translator/key_form.py <bundle-checkout>   (stdlib only)
"""
import json, sys, re
from pathlib import Path
def main(root):
    m = json.loads((Path(root)/'bundle'/'.manifest.json').read_text())
    E = m.get('entries') or {}; A = m.get('absences') or {}
    ids_e = [v.get('id') for v in E.values()]; ids_a = [v.get('id') for v in A.values()]
    form = re.compile(r'^remember://lesson/[^/]+$')
    out = {"commit_expected": "3806111cad1a058585242f7ad78716c4a767c782",
           "entries_keys": list(E.keys()), "entries_ids": ids_e, "absences_keys": list(A.keys()), "absences_ids": ids_a,
           "1_every_value_carries_id": all('id' in v for v in E.values()) and all('id' in v for v in A.values()),
           "2_one_identifier_form": all(isinstance(x, str) and form.match(x) for x in ids_e + ids_a),
           "3_exclusive_over_stated_ids_no_normalisation": not (set(ids_e) & set(ids_a)),
           "4_bare_keys_retained_as_addressing": all(k in E for k in E) and any('/' not in k for k in E),
           "reconciliation": m.get('absenceReconciliation')}
    out["verdict"] = {"key_form_uniform_and_checkable_from_document": out["1_every_value_carries_id"] and out["2_one_identifier_form"] and out["3_exclusive_over_stated_ids_no_normalisation"]}
    print(json.dumps(out, indent=1))
if __name__ == '__main__': main(sys.argv[1] if len(sys.argv) > 1 else 'remember-okf-sample-bundle')
