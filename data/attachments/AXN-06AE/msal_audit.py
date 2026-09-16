#!/usr/bin/env python3
"""msal_audit.py — validate a Monetary Substrate Audit Ledger and recompute its score vector.

Checks the schema, recomputes every rate from its own numerator and denominator (a rate that
disagrees with its counts is a defect of the ledger, not a finding about the object), runs the
integrity heuristics the specification names, and REFUSES to emit a scalar audit score.

    python3 msal_audit.py MSAL-0001-sappho.yaml [--check]
"""
import sys, json, argparse, pathlib
import yaml
try: import jsonschema
except ImportError: jsonschema = None

ap = argparse.ArgumentParser(); ap.add_argument("ledger"); ap.add_argument("--check", action="store_true")
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parent
d = yaml.safe_load(open(a.ledger, encoding="utf-8"))
schema = json.load(open(ROOT / "msal-schema.json", encoding="utf-8"))
breaches = []

if jsonschema:
    for e in jsonschema.Draft202012Validator(schema).iter_errors(d):
        breaches.append("schema: " + "/".join(map(str, e.path)) + ": " + e.message[:140])

# rates must equal their own counts
S = d.get("audit_scores", {})
for k, v in S.items():
    if isinstance(v, dict) and "rate" in v:
        nums = [x for x in v.values() if isinstance(x, int)]
        if len(nums) == 2:
            n, den = nums[0], nums[1]
            want = round(n / den, 4) if den else None
            if want is not None and abs((v["rate"] or 0) - want) > 1e-6:
                breaches.append(f"score {k}: rate {v['rate']} disagrees with {n}/{den} = {want}")

# integrity heuristics from the specification
for var in d.get("monetary_inscription", {}).get("variables", []):
    if var.get("denominator_belongs_to") == "the observer":
        cls = {x.get("class") for x in d.get("inscription_integrity", {}).get("defects", [])}
        if "observer_denominator" not in cls:
            breaches.append(f"variable {var.get('name')} has an observer denominator and no observer_denominator defect is recorded")
    if var.get("source") in ("asserted", "chosen") and not var.get("derivation"):
        breaches.append(f"variable {var.get('name')} is {var.get('source')} with no derivation stated")

ii = d.get("inscription_integrity", {})
ca = d.get("closure_audit", {})
if ii.get("assessment") == "unassessed":
    breaches.append("inscription_integrity is unassessed: the ledger cannot classify without it")
if ii.get("defects") and ii.get("assessment") == "sound":
    breaches.append("defects recorded but assessment is 'sound'")
if d.get("irrecoverable_remainder", {}).get("explicit_nonzero_remainder") is not True:
    breaches.append("remainder must be explicitly non-zero; zero remainder is a claim requiring its own evidence")
if d.get("audit_result", {}).get("semantic_account_closed") is not False:
    breaches.append("semantic_account_closed must be false")

# the prohibition, enforced
if any(k in S for k in ("score", "total", "overall", "composite", "grade")):
    breaches.append("a scalar audit score is present; the specification prohibits it")

print(f"MSAL audit — {d.get('id')}  ({d.get('protocol')} v{d.get('version')})")
print(f"  closure classification : {ca.get('classification')}   (pointer {ca.get('audit_pointer')}, semantic settlement claimed {ca.get('semantic_settlement_claimed')})")
print(f"  inscription integrity  : {ii.get('assessment')}   ({len(ii.get('defects') or [])} defects, amount survives: {ii.get('amount_survives_audit')})")
print(f"  2x2 classification     : {d.get('audit_result',{}).get('audit_classification')}")
print("  score vector (never summed):")
for k, v in S.items():
    if isinstance(v, dict) and "rate" in v:
        nums = [x for x in v.values() if isinstance(x, int)]
        print(f"    {k:38s} {v['rate']}   ({nums[0]}/{nums[1]})" if len(nums) == 2 else f"    {k:38s} {v['rate']}")
print(f"    {'integrity_defect_count':38s} {S.get('integrity_defect_count')}   (a count; defects do not average)")
print("  defect classes:", ", ".join(sorted({x.get("class") for x in (ii.get("defects") or [])})))
if breaches:
    print("\nBREACHES:")
    for b in breaches: print("  -", b)
else:
    print("\nno breaches: the ledger is internally consistent and its own assessment stands")
sys.exit(1 if (a.check and breaches) else 0)
