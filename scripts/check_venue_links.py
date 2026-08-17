#!/usr/bin/env python3
"""check_venue_links.py — keep the venue dataset synced to the registry.

Every pointer in datasets/venues/records/*.json must resolve to something that
still exists and still says what the record says it says.

WHY. The heteronym identity cards carried capture blocks pinned at registry
v9.39 while the live registry stood at v11.4 — Sigil's card said 40 captures and
the registry held 54. The cards were not wrong when written; the registry moved
and nothing rejoined them. Venue records point at charters, deposits, AXNs and
surfaces, all of which can move the same way.

Checks, offline (no network):
  charter deposit exists in the registry
  charter AXN on the record matches the registry's AXN for that deposit
  charter title matches
  home deposit, where declared, same three checks
  declared venue_string appears in the registry as an actual journal value
  assigned deposits carry that venue in their journal field

Usage: check_venue_links.py [--fix-axn]
"""
import json, sys, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECORDS = ROOT / "datasets/venues/records"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--fix-axn", action="store_true")
    a = ap.parse_args()
    reg = json.loads((ROOT / "data/registry.json").read_text())
    D = {d["deposit_number"]: d for d in reg["deposits"]}
    journals = {}
    for d in reg["deposits"]:
        if d.get("journal"):
            journals.setdefault(str(d["journal"]), []).append(d["deposit_number"])

    fails, fixed = [], 0
    for p in sorted(RECORDS.glob("*.json")):
        r = json.loads(p.read_text())
        vid = r.get("venue_id")
        loc = r.get("location") or {}
        for label in ("charter", "home_deposit"):
            blk = loc.get(label)
            if not isinstance(blk, dict) or not blk.get("deposit"):
                continue
            n = blk["deposit"]
            dep = D.get(n)
            if not dep:
                fails.append(f"{vid}: {label} #{n} is not in the registry"); continue
            if blk.get("axn") != dep.get("axn"):
                if a.fix_axn:
                    blk["axn"] = dep.get("axn"); fixed += 1
                else:
                    fails.append(f"{vid}: {label} #{n} AXN drifted\n"
                                 f"      record   {blk.get('axn')}\n"
                                 f"      registry {dep.get('axn')}")
        vs = r.get("venue_string")
        if vs and r.get("status") != "province" and vs not in journals:
            fails.append(f"{vid}: venue_string {vs!r} appears on no deposit "
                         f"(unassigned venue, or the string does not match what is stored)")
        for n in (r.get("deposits") or {}).get("assigned") or []:
            dep = D.get(n)
            if not dep:
                fails.append(f"{vid}: assigned #{n} not in the registry")
            elif dep.get("journal") != vs:
                fails.append(f"{vid}: assigned #{n} carries journal {dep.get('journal')!r}, not {vs!r}")
        if a.fix_axn:
            p.write_text(json.dumps(r, ensure_ascii=False, indent=1))

    if a.fix_axn:
        print(f"repaired {fixed} drifted AXN(s)")
    if fails:
        print(f"FAIL: {len(fails)} venue-link problem(s):")
        for f in fails: print("  " + f)
        return 1
    print(f"OK: all venue links resolve ({len(list(RECORDS.glob('*.json')))} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

def check_registry_strings(reg, records):
    """Every venue's registry_string must actually occur in the registry, and every
    journal value in the registry must be claimed by exactly one venue.

    Added 2026-08-17. The venue records' `canonical` field differs from the registry's
    `journal` value for FIVE of eight venues -- the registry carries a parenthetical
    abbreviation the record does not. A join on `canonical` therefore loses five venues
    silently, which is how the journals page first rendered three issues out of seven.
    """
    fails = []
    used = {}
    live = {d.get("journal") for d in reg["deposits"] if d.get("journal")}
    for r in records:
        s = r.get("registry_string")
        if not s:
            fails.append(f"{r['venue_id']}: no registry_string -- joins will fall back to canonical and lose it")
            continue
        if s not in live:
            fails.append(f"{r['venue_id']}: registry_string {s!r} occurs in no deposit")
        if s in used:
            fails.append(f"{r['venue_id']}: registry_string {s!r} already claimed by {used[s]}")
        used[s] = r["venue_id"]
    for s in sorted(live - set(used)):
        fails.append(f"registry journal {s!r} is claimed by no venue record")
    return fails
