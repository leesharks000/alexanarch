#!/usr/bin/env python3
"""audit_capture_citability.py — a capture that cannot be cited is not published.

WHY THIS EXISTS
The registry has always BUILT deep links of the form `gallery/#slug`, and no
gallery has ever set the anchor those links point at. Every "Screenshot →" the
registry advertised landed a reader on the top of a gallery page with 230
captures beneath it and no indication which one was meant. The links were not
broken in any way a status code would reveal; they resolved, and told you
nothing.

Two duplicate slugs were also found at the moment citability was introduced —
two pairs of captures on the same query at different dates. They were
disambiguated by date, which was free precisely because no anchor had ever
resolved: nothing could have cited the ambiguous form. **After that moment,
slugs are permanent.** A renamed slug silently breaks every citation made to it,
and unlike a dead URL it leaves no error behind — the reader simply lands
somewhere else and is not told.

WHAT THIS ENFORCES
  1. Every capture has a slug.
  2. Slugs are unique.
  3. Slugs are stable: any slug present in a published snapshot must still exist.
  4. Slug characters are anchor-safe.
  5. The registry declares its citation grammar, so consumers need not infer it.

Usage:
    python3 scripts/audit_capture_citability.py
    python3 scripts/audit_capture_citability.py --live   # + resolve a sample
"""
import json, re, sys, pathlib, argparse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
SAFE = re.compile(r"^[a-z0-9][a-z0-9\-]{2,119}$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    a = ap.parse_args()
    r = json.loads(REG.read_text())
    entries = r["entries"]
    fails = []

    slugs = [e.get("slug", "") for e in entries]
    for e in entries:
        s = e.get("slug", "")
        if not s:
            fails.append(f"capture dated {e.get('date')} has no slug — it cannot be cited")
        elif not SAFE.match(s):
            fails.append(f"slug '{s}' is not anchor-safe (lowercase, digits, hyphens; 3–120 chars)")
    dupes = sorted({s for s in slugs if s and slugs.count(s) > 1})
    for d in dupes:
        fails.append(f"slug '{d}' is used by {slugs.count(d)} captures — a citation to it is ambiguous")

    cit = r.get("citation") or {}
    if "canonical_form" not in cit:
        fails.append("the registry declares no citation grammar; consumers would have to infer it")

    # stability: every slug a published snapshot carries must still exist
    snap = ROOT / "datasets/capture-registry/EA-WG-CAPTURES-01.json"
    if snap.exists():
        try:
            old = {e.get("slug") for e in json.loads(snap.read_text()).get("entries", [])}
            gone = sorted(x for x in old - set(slugs) if x)
            hist = {h["was"] for e in entries for h in e.get("slug_history", [])}
            gone = [g for g in gone if g not in hist]
            for g in gone[:10]:
                fails.append(f"slug '{g}' was published and is now absent — every citation to it "
                             f"now lands elsewhere with no error shown")
        except Exception as e:
            fails.append(f"could not read the published snapshot: {e}")

    # DISCOVERABILITY. Citable-by-people and citable-by-machines are different
    # properties. The gallery was client-rendered for months, so a crawler saw 717
    # characters and none of the captures — a registry ABOUT machine reception,
    # unreadable by machines. The static list is what makes an anchor mean
    # something to a reader that does not execute JavaScript.
    page = ROOT / "captures/index.html"
    if page.exists():
        pg = page.read_text(errors="replace")
        static = pg.count('class="cap-card" id=')
        if static < len(entries):
            fails.append(f"the gallery pre-renders {static} of {len(entries)} captures; the rest "
                         f"exist only after JavaScript runs, so their anchors are invisible to "
                         f"any reader that does not execute it")
        if "application/ld+json" not in pg:
            fails.append("the gallery declares no JSON-LD; the registry is undescribed to machines")
        if 'rel="describedby"' not in pg:
            fails.append("the gallery carries no Signposting to the registry JSON")

    if a.live and not fails:
        try:
            with urllib.request.urlopen(
                    "https://www.alexanarch.org/captures/", timeout=30) as resp:
                page = resp.read().decode("utf-8", "replace")
            if "gotoSlug" not in page:
                fails.append("the live gallery cannot resolve a fragment: no deep-link resolver "
                             "is present, so every citation lands on the page top")
        except Exception as e:
            fails.append(f"live gallery unreachable: {e}")

    print(f"captures: {len(entries)} · unique slugs: {len(set(slugs))} · "
          f"citation grammar: {'declared' if cit else 'ABSENT'}")
    for f in fails:
        print(f"  FAIL  {f}", file=sys.stderr)
    if fails:
        print("\nA capture that cannot be cited is not published, it is only stored.",
              file=sys.stderr)
        return 1
    print("EVERY CAPTURE IS CITABLE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
