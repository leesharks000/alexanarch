#!/usr/bin/env python3
"""withdraw_duplicate_seatings.py — the same capture seated twice.

THE DEFECT. Fifteen observations are BYTE-IDENTICAL transcripts on the SAME DATE
at the same address, seated twice. In thirteen of the fifteen, one copy carries
`auth: null` and the other carries a value — residue of the blanket auth rule
that assigned "signed in" to 161 observations. One capture, counted twice.

THE RULE, following the corpus's own withdrawal convention: withdrawn, not
deleted, and held with their data intact beside the record that covers each.

  - one copy null, one valued  -> the NULL copy is withdrawn
  - both null                  -> the later copy is withdrawn
  - neither null               -> the record CONTRADICTS ITSELF about a single
                                  capture's auth state. The duplicate is
                                  withdrawn and the survivor's auth is set to
                                  UNDETERMINED, because two attestations for one
                                  capture are not evidence for either.
"""
import json, pathlib, collections, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    p = json.loads(PROJ.read_text())
    withdrawn, contradicted = [], []
    for e in p["entries"]:
        obs = e.get("observations")
        if not obs or len(obs) < 2:
            continue
        groups = collections.defaultdict(list)
        for o in obs:
            t = str(o.get("transcript") or "")
            if len(t) > 200:
                groups[(o.get("date"), t)].append(o)
        drop = []
        for (date, _t), v in groups.items():
            if len(v) < 2:
                continue
            nulls = [o for o in v if o.get("auth") in (None, "null", "")]
            valued = [o for o in v if o not in nulls]
            if nulls and valued:
                loser, keeper, why = nulls[0], valued[0], "null-auth copy of a valued capture"
            elif not valued:
                loser, keeper, why = v[1], v[0], "both copies null; the later is withdrawn"
            else:
                loser, keeper = v[1], v[0]
                why = ("two DIFFERENT auth attestations for ONE capture: %r and %r. The duplicate is withdrawn "
                       "and the survivor set to UNDETERMINED — two attestations for one capture are not evidence "
                       "for either." % (v[0].get("auth"), v[1].get("auth")))
                keeper["auth"] = "UNDETERMINED"
                keeper["auth_basis"] = ("CONTRADICTED. The registry held this capture twice with different auth "
                                        "values; both are withdrawn as evidence. NULL is not zero and a "
                                        "contradiction is not a reading.")
                contradicted.append(e.get("q"))
            drop.append(id(loser))
            withdrawn.append({"q": e.get("q"), "date": date, "slug": loser.get("slug"),
                              "obs_id": loser.get("obs_id"), "auth_was": loser.get("auth"),
                              "per": loser.get("per"), "covered_by": keeper.get("obs_id"),
                              "why": why})
        if drop:
            e["observations"] = [o for o in obs if id(o) not in drop]
            e["n_observations"] = len(e["observations"])
            e["dates"] = sorted({o["date"] for o in e["observations"] if o.get("date")})
            e["surfaces"] = sorted({o["surface"] for o in e["observations"] if o.get("surface")})
            e["other_slugs"] = [o["slug"] for o in e["observations"]
                                if o.get("slug") and o["slug"] != e.get("slug")] or None
            e["series"] = len(e["observations"])
    p["withdrawn_duplicate_seatings"] = {
        "_rule": ("ONE CAPTURE, COUNTED ONCE. Each entry here is a byte-identical transcript on the same date at "
                  "the same address, seated a second time. Withdrawn, not deleted, and held with the observation "
                  "that covers it. Thirteen of fifteen were a null-auth copy beside a valued one — residue of the "
                  "blanket rule that assigned an auth state to 161 observations without observing any of them."),
        "_withdrawn_at": NOW, "count": len(withdrawn), "records": withdrawn}
    p["observation_count"] = sum(len(x.get("observations") or [x]) for x in p["entries"])
    PROJ.write_text(json.dumps(p, indent=1, ensure_ascii=False))
    print(f"withdrawn {len(withdrawn)} duplicate observations")
    for w in withdrawn:
        print(f"   {w['date']}  auth_was={w['auth_was']!r:<14} «{str(w['q'])[:40]}»")
    if contradicted:
        print(f"\nCONTRADICTED auth, survivor set to UNDETERMINED: {contradicted}")
    print(f"\nobservations now: {p['observation_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
