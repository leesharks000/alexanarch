#!/usr/bin/env python3
"""Translation receipt — makes a translation self-describing, so a downstream green
verdict can never travel without the fabrication count beside it.

Invariant enforced here rather than merely documented:
    green verdict + fabricated > 0  is NOT a faithful translation.
"""
import json, hashlib, sys
from pathlib import Path
from collections import Counter

VERSION = "okf-shape-translator/0.1"

def make_receipt(mode, cases, breaks, log_claims, records, skipped, checker_result=None, refusals=None):
    b = Counter(x[1] for x in breaks)
    # expressible: cases that produced any output at all without fabrication
    fabricated = b.get("claim", 0)
    coerced    = b.get("identity", 0)          # id semantics overloaded to fit
    dropped    = sum(v for k, v in b.items() if k in
                     ("successor", "reason", "presence", "observation", "identifier_kind"))
    expressible = len(cases) - skipped
    preserved   = expressible - min(expressible, coerced)
    r = {
        "translator": VERSION,
        "translator_sha256": hashlib.sha256(Path("translate.py").read_bytes()).hexdigest()[:16],
        "mode": mode,
        "source_cases": len(cases),
        "output_claims": log_claims,
        "output_records": records,
        "expressible": expressible,
        "preserved": preserved,
        "coerced": coerced,
        "dropped": dropped,
        "fabricated": fabricated,
        "dropped_by_field": {k: v for k, v in b.most_common() if k not in ("claim", "identity")},
        "refused_untranslatable": skipped,
        "refusal_reasons": dict(Counter(x[1] for x in (refusals or [])).most_common()),
    }
    # refusal is not loss: a translator that declines to represent what it cannot carry
    # preserves epistemic integrity; one that silently forces it does not. Collapsing the
    # two would make this receipt commit the semantic collapse it exists to detect.
    if fabricated or coerced or dropped:
        r["fidelity_class"] = "lossy"
    elif skipped:
        r["fidelity_class"] = "partial_refusal"
    else:
        r["fidelity_class"] = "preserving"
    if checker_result:
        r["downstream_check"] = {k: checker_result.get(k) for k in
                                 ("claims_checked", "targets_known", "never_landed_count", "error")}
        clean = checker_result.get("never_landed_count", 0) >= 0 and not checker_result.get("error")
        r["fidelity_warning"] = (
            "DOWNSTREAM VERDICT IS NOT EVIDENCE OF FIDELITY: this translation fabricated "
            f"{fabricated} write-claim(s) the producer never made and dropped {dropped} "
            "field-level facts. A clean check over a lossy translation is clean about the "
            "translation, not about the source."
        ) if (clean and fabricated > 0) else None
    return r

if __name__ == "__main__":
    import re, translate as T
    cases = json.loads(Path("cases.json").read_text())["cases"]
    sys.path.insert(0, "."); import never_landed as nl
    pat = re.compile(r'\*\*(?:Record|Lesson) created\*\*: lesson ([a-z0-9-]+)')
    out = {}
    for mode in ("strict", "forced"):
        r = T.run(cases, mode, f"out-{mode}")
        chk = nl.check_log(f"out-{mode}/log.md", [f"out-{mode}/store"], claim_re=pat)
        rec = make_receipt(mode, cases, r["breaks"], r["log_claims"], r["records"],
                           r["skipped_untranslatable"], chk, r.get("refusals"))
        out[mode] = rec
        print(f"── receipt · {mode} ──")
        for k in ("source_cases","output_claims","expressible","refused_untranslatable","preserved","coerced","dropped","fabricated"):
            print(f"  {k:<14} {rec[k]}")
        print(f"  downstream     {rec['downstream_check']}")
        if rec.get("fidelity_warning"): print(f"  ⚠  {rec['fidelity_warning']}")
        print()
    Path("receipts.json").write_text(json.dumps(out, indent=1))
    print("→ receipts.json")
