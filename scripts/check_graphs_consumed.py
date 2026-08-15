#!/usr/bin/env python3
"""check_graphs_consumed.py — is every citation graph actually reaching a surface?

THE DEFECT THIS CLOSES. citation-graph-external.json (5,846 edges) and
citation-graph-freeform.json (1,799 edges) were written on every run and read by
NOTHING except their own extractors. 7,645 edges, generated faithfully, reaching
zero surfaces — so the citation system BEHAVED as internal-only while the data
said otherwise. Nobody noticed because a file that is written successfully looks
like a file that is working.

A graph that is generated and not consumed is worse than one that does not exist:
it costs the run time, it accumulates, and it creates a false belief that the
relation is covered.

This gate asserts that every citation graph in data/ is (a) loaded by a surface
generator and (b) present in the rendered surface.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SURFACE = ROOT / "s" / "graph" / "index.html"
GENERATOR = ROOT / "scripts" / "regenerate_surfaces.py"


def main():
    graphs = sorted(ROOT.glob("data/citation-graph*.json"))
    if not graphs:
        print("no citation graphs found", file=sys.stderr)
        return 1

    gen = GENERATOR.read_text() if GENERATOR.exists() else ""
    page = SURFACE.read_text(errors="replace") if SURFACE.exists() else ""
    fails = []

    print("citation graphs")
    for g in graphs:
        try:
            edges = len(json.loads(g.read_text()).get("edges") or [])
        except Exception as exc:
            fails.append(f"{g.name}: unreadable ({exc})")
            continue
        loaded = g.name in gen
        rendered = g.name in page
        print(f"  {g.name:<34} {edges:>7,} edges · loaded {'yes' if loaded else 'NO':<3} · "
              f"rendered {'yes' if rendered else 'NO'}")
        if not loaded:
            fails.append(f"{g.name} is written but no surface generator loads it "
                         f"({edges:,} edges orphaned)")
        elif not rendered:
            fails.append(f"{g.name} is loaded but does not appear in the rendered surface "
                         f"({edges:,} edges invisible)")

    # Unverified edges must not be presented as observed.
    for g in graphs:
        try:
            d = json.loads(g.read_text())
        except Exception:
            continue
        unv = sum(1 for e in (d.get("edges") or []) if e.get("ontic_status") == "unverified")
        if unv and g.name in page:
            # the surface must say somewhere that these are not adjudicated
            if "adjudicated" not in page and "unverified" not in page:
                fails.append(f"{g.name} contributes {unv:,} unverified edges to a surface that "
                             f"does not say they are unadjudicated")

    for f in fails:
        print(f"  FAIL  {f}", file=sys.stderr)
    if fails:
        print("\nA graph that is generated and not consumed is worse than one that does not exist.",
              file=sys.stderr)
        return 1
    print("EVERY CITATION GRAPH REACHES A SURFACE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
