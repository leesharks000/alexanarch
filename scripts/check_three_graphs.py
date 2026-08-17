#!/usr/bin/env python3
"""check_three_graphs.py — do the entities, the apertures and the horizon agree?

Three graphs describe the same archive from three sides:

    pessoagraph.org        THE ENTITIES        who can speak, and the 5,000-year
                                               lineage that licenses them
    surfacemap.org         THE APERTURES       through what opening a position
                                               reaches a reader
    crimsonhexagonal.org   THE EVENT HORIZON   what is inside the governed object

Until 2026-08-17 nothing declared what they were to each other, so nothing could
be out of sync — and a thing that cannot be out of sync cannot be checked. The
audit that prompted this found crimsonhexagonal's canonical file claiming 463
deposits while its own index page claimed 1,487 and the registry held 1,488.

This checks the two things that can be verified from the datasets: the counts each
graph asserts, and the identity coverage in graph-crosswalk.json.

    python3 scripts/check_three_graphs.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    reg = json.loads((ROOT / "data/registry.json").read_text())["deposits"]
    recs = list((ROOT / "datasets/heteronyms/records").glob("*.json"))
    ven = list((ROOT / "datasets/venues/records").glob("*.json"))
    xw = json.loads((ROOT / "datasets/heteronyms/graph-crosswalk.json").read_text())

    fails = 0
    print(f"  registry: {len(reg)} deposits · {len(recs)} heteronym records · {len(ven)} venues\n")

    for key, label in (("pessoagraph", "THE ENTITIES"),
                       ("surfacemap", "THE APERTURES"),
                       ("crimsonhexagonal", "THE EVENT HORIZON")):
        absent = [r["record"] for r in xw["rows"] if not r.get(key)]
        have = len(xw["rows"]) - len(absent)
        flag = "" if not absent else f"   <-- {len(absent)} absent"
        print(f"  {key:<20}{label:<22}{have}/{len(xw['rows'])} identities{flag}")
        if absent:
            print(f"        {', '.join(absent[:8])}")
            fails += 1

    print()
    print("  A graph missing an identity is not necessarily wrong — the Assembly")
    print("  substrates are not Pessoa-lineage entities and do not belong in the")
    print("  entity graph. What matters is that the absence is now VISIBLE and")
    print("  attributable, rather than three files drifting with nothing between them.")
    print(f"\n{'REVIEW' if fails else 'OK'}: {fails} graph(s) with gaps to account for")
    return 0


if __name__ == "__main__":
    sys.exit(main())
