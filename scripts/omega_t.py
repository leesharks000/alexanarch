#!/usr/bin/env python3
"""omega_t.py — compute Ω_t, the time axis of Erasure Skew.

WHY THIS EXISTS. PER measures how much provenance was dropped. Ω measures on whom
it fell. Neither carries time — so neither can distinguish erasure as ATTRITION
(a thing dissolving because nothing holds it) from erasure as RESPONSE (power
arriving because a thing became legible enough to answer).

    attrition  → as legibility rises, erasure FALLS
    response   → as legibility rises, erasure RISES

TWO CONSTRUCTIONS FAILED FIRST AND ARE REFUSED HERE BY DESIGN.

  Regression on source count is AMBIGUOUS IN SIGN. `gravity well protocol` moved
  0.00 → 0.75 while sources fell 3 → 2; the slope is negative and the naive
  classifier returned "attrition" for a case where erasure doubled.

  Field-level mean PER by date MEASURES THE SAMPLER, NOT THE FIELD. 2026-06-17
  shows n=46 at mean 0.880 — that was a coined-term battery, and coined terms
  erase heavily. Corpus mean is 0.621 before August and 0.588 after: flat, and
  meaningless either way.

SO Ω_t IS DEFINED ONLY OVER MATCHED PAIRS — same semantic address, SAME SURFACE,
two dates. Everything else is discarded. A cross-surface difference is a surface
difference, not a time difference.

AND A DIFFERENCE ALONE STILL CANNOT ATTRIBUTE. If archive addresses rise while
the rest of the surface also rises, Ω_t recorded a platform change. The
difference-in-differences arm exists so that a rise can be assigned to the
archive rather than to Google.

    python3 omega_t.py                  # matched pairs and regimes
    python3 omega_t.py --did            # difference-in-differences by arm
    python3 omega_t.py --baseline       # pre-registration snapshot for a trial
"""
import json
import pathlib
import statistics
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAP = ROOT / "data" / "EA-WG-CAPTURES-01.json"
TRIALS = ROOT / "data" / "omega-t-trials.json"

SCOPE = ["framework", "discipline", "method", "subcategory", "technique",
         "product-feature", "absent"]


def load():
    return json.loads(CAP.read_text())


def matched_pairs(cap, surface=None):
    """Same address, same surface, two or more dates. The only valid axis."""
    out = []
    for e in cap["entries"]:
        obs = [o for o in (e.get("observations") or [e])
               if isinstance(o.get("per"), (int, float)) and o.get("date")]
        by = defaultdict(list)
        for o in obs:
            by[o.get("surface")].append(o)
        for s, v in by.items():
            if surface and s != surface:
                continue
            v.sort(key=lambda o: o["date"])
            if len(v) >= 2 and v[0]["date"] != v[-1]["date"]:
                out.append({"q": e.get("q"), "surface": s,
                            "t0": v[0]["date"], "per0": v[0]["per"],
                            "t1": v[-1]["date"], "per1": v[-1]["per"],
                            "omega_t": round(v[-1]["per"] - v[0]["per"], 3),
                            "n": len(v),
                            "composed_as_0": v[0].get("composed_as"),
                            "composed_as_1": v[-1].get("composed_as")})
    return out


def drift(p):
    """Ω_d — definitional drift. Independent of Ω_t: an entity can be fully
    attributed and fully liquidated in the same composition."""
    a, b = p.get("composed_as_0"), p.get("composed_as_1")
    if not (a and b):
        return None
    d = {}
    if a.get("scope") in SCOPE and b.get("scope") in SCOPE:
        d["scope_descent"] = SCOPE.index(b["scope"]) - SCOPE.index(a["scope"])
    if a.get("term_returned") != b.get("term_returned"):
        d["term_substituted"] = {"was": a.get("term_returned"), "now": b.get("term_returned")}
    if a.get("binding_relation") != b.get("binding_relation"):
        d["binding"] = f"{a.get('binding_relation')} → {b.get('binding_relation')}"
    if a.get("organic_presence") != b.get("organic_presence"):
        d["organic"] = f"{a.get('organic_presence')} → {b.get('organic_presence')}"
    return d or None


def arm_of(q, trial):
    ql = str(q or "").lower()
    for name, pats in trial["arms"].items():
        if any(pt.lower() in ql for pt in pats):
            return name
    return trial.get("default_arm", "field-control")


def report(pairs):
    rose = [p for p in pairs if p["omega_t"] > 0.01]
    fell = [p for p in pairs if p["omega_t"] < -0.01]
    flat = [p for p in pairs if abs(p["omega_t"]) <= 0.01]
    print(f"matched pairs (same address, same surface, two dates): {len(pairs)}")
    print(f"  erasure ROSE {len(rose)} · FELL {len(fell)} · unchanged {len(flat)}")
    if pairs:
        print(f"  mean Ω_t {statistics.mean(p['omega_t'] for p in pairs):+.3f}")
    print("\n  largest rises")
    for p in sorted(rose, key=lambda x: -x["omega_t"])[:10]:
        d = drift(p)
        mark = "  ← Ω_d " + json.dumps(d, ensure_ascii=False)[:60] if d else ""
        print(f"   {p['omega_t']:+.2f}  {str(p['q'])[:38]:<40} {p['t0']}→{p['t1']}{mark}")
    print("\n  largest falls")
    for p in sorted(fell, key=lambda x: x["omega_t"])[:6]:
        print(f"   {p['omega_t']:+.2f}  {str(p['q'])[:38]:<40} {p['t0']}→{p['t1']}")


def did(pairs):
    """Difference-in-differences. Without this, a rise cannot be assigned to the
    archive rather than to the surface."""
    if not TRIALS.exists():
        print("no trial registered — write data/omega-t-trials.json first", file=sys.stderr)
        return 1
    trials = json.loads(TRIALS.read_text())
    for trial in trials["trials"]:
        print(f"\n══ {trial['id']} — {trial['question']}")
        print(f"   intervention: {trial['intervention']}  on {trial['intervention_date']}")
        print(f"   PRE-REGISTERED {trial['registered']} · status {trial['status']}")
        byarm = defaultdict(list)
        for p in pairs:
            byarm[arm_of(p["q"], trial)].append(p["omega_t"])
        for arm in list(trial["arms"]) + [trial.get("default_arm", "field-control")]:
            v = byarm.get(arm) or []
            if not v:
                print(f"   {arm:<18} n=0   — no matched pairs yet")
                continue
            print(f"   {arm:<18} n={len(v):<3} mean Ω_t {statistics.mean(v):+.3f}")
        t = byarm.get(trial["treated_arm"]) or []
        c = byarm.get(trial.get("default_arm", "field-control")) or []
        if t and c:
            print(f"   DiD = {statistics.mean(t) - statistics.mean(c):+.3f}  "
                  f"(treated minus field control)")
        else:
            print("   DiD: NOT COMPUTABLE — both arms need matched pairs spanning the intervention")
    return 0


def baseline(pairs, cap):
    """The pre-intervention snapshot. Must be taken BEFORE the treatment fires,
    or the trial has no t0 and measures nothing."""
    print("BASELINE — latest Google AI Overview PER per address\n")
    rows = []
    for e in cap["entries"]:
        obs = [o for o in (e.get("observations") or [e])
               if o.get("surface") == "Google AI Overview" and isinstance(o.get("per"), (int, float))]
        if obs:
            last = max(obs, key=lambda o: o.get("date") or "")
            rows.append((last["date"], last["per"], e.get("q")))
    rows.sort(reverse=True)
    for d, p, q in rows[:24]:
        print(f"   {d}  {p:.2f}  {str(q)[:52]}")
    print(f"\n   {len(rows)} addresses carry a Google AI Overview baseline")


def main():
    cap = load()
    pairs = matched_pairs(cap)
    if "--did" in sys.argv:
        return did(pairs)
    if "--baseline" in sys.argv:
        baseline(pairs, cap)
        return 0
    report(pairs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
