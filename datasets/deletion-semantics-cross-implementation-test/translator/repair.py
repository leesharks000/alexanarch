#!/usr/bin/env python3
"""Repair probe — the minimum machine-readable surviving-absence record, and its effect.

Spec-level requirement under test: an absent concept needs SOME machine-readable
surviving record keyed to stable identity. Implementation-level repair: expose it in
the producer's machine index (here .manifest.json) rather than in prose only.

Payload under test:
  id, presence (removed|never_landed), date, reason, recorded_by, successor?, successor_kind?
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, ".")
import never_landed as nl

TOMB_LINE = re.compile(r"^\*\s+\*\*(?P<id>[^*]+)\*\*\s+—\s+presence:\s*(?P<presence>\S+)\s+—\s+"
                       r"tombstoned\s+(?P<date>\S+)\s+—\s+reason:\s*(?P<reason>[^—]+?)"
                       r"(?:\s+—\s+successor:\s*(?P<successor>\S+))?\s*$")

def repair_manifest(store, recorded_by="remember/0.2"):
    """Lift prose tombstones into the machine index. Idempotent; adds nothing else."""
    store = Path(store); mpath = store/".manifest.json"
    m = json.loads(mpath.read_text()); m.setdefault("absent", {})
    tomb = store/"tombstones.md"
    if tomb.is_file():
        for line in tomb.read_text().splitlines():
            g = TOMB_LINE.match(line)
            if not g: continue
            d = g.groupdict()
            m["absent"][d["id"]] = {"id": d["id"], "presence": d["presence"],
                "date": d["date"], "reason": d["reason"].strip(),
                "recorded_by": recorded_by,
                **({"successor": d["successor"]} if d.get("successor") else {})}
    mpath.write_text(json.dumps(m, indent=1))
    return len(m["absent"])

def repaired_check(log, store, claim_re, id_key="id"):
    """The consumer, with one added lookup: before calling a claim never-landed, ask
    the machine index whether an absence record survives for it."""
    out = nl.check_log(log, [store], claim_re=re.compile(claim_re), id_key=id_key)
    absent = json.loads((Path(store)/".manifest.json").read_text()).get("absent", {})
    verdicts, still = {}, []
    for n in out["never_landed"]:
        a = absent.get(n["target"])
        if a: verdicts[n["target"]] = a["presence"]
        else: verdicts[n["target"]] = "never_landed"; still.append(n)
    out["verdicts"] = verdicts
    out["never_landed"] = still
    out["never_landed_count"] = len(still)
    return out

if __name__ == "__main__":
    store, log = "abc/store", "abc/log.md"
    pat = r'\*\*Lesson created\*\*: lesson ([a-z0-9-]+)'
    n = repair_manifest(store)
    print(f"repair applied: {n} absence record(s) lifted into .manifest.json\n")
    print(json.dumps(json.loads(Path(store,'.manifest.json').read_text())["absent"], indent=1))
    r = repaired_check(log, store, pat)
    print("\n════ REPAIRED CONSUMER ════")
    for rid,label in [("okf-abc-present-001","A created and present"),
                      ("okf-abc-removed-002","B created, then removed; tombstone exists"),
                      ("okf-abc-neverlanded-003","C asserted, never landed")]:
        v = r["verdicts"].get(rid, "present")
        print(f"  {rid:<28} → {v:<13} {label}")
    b, c = r["verdicts"].get("okf-abc-removed-002"), r["verdicts"].get("okf-abc-neverlanded-003")
    print(f"\n  B={b}  C={c}  →  {'DIVERGE' if b!=c else 'still collide'}")
    print(f"  other cases disturbed: {'no' if r['claims_checked']==3 and r['targets_known']>=1 else 'CHECK'}"
          f"  (claims={r['claims_checked']}, known={r['targets_known']})")
