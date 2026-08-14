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
    # 2026-08-12: the Capture Registry is WITHDRAWN from publication (see
    # quarantine/capture-registry-20260812/ and rebuild/capture-registry/).
    # There is nothing published to audit for citability, and this gate must
    # not block deposits of unrelated work while the rebuild proceeds. When the
    # registry returns, this resumes automatically.
    if not REG.exists():
        print("SKIP: %s is absent — the Capture Registry is withdrawn from "
              "publication and under reconstruction. Citability cannot be "
              "audited for a surface that is not published." % REG.name)
        return 0
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

    # THE FLOW MUST BE DISPLAYED where a writer will meet it. Declaring it in the
    # atlas was insufficient — every one of the three flow failures was committed by
    # someone with no reason to consult an atlas.
    if "_FLOW" not in r:
        fails.append("the registry does not declare its own data flow as its first key; a program "
                     "opening it to write meets data before it meets the rule")
    gal = ROOT / "captures/index.html"
    if gal.exists():
        g = gal.read_text(errors="replace")
        if 'id="capture-flow"' not in g:
            fails.append("the gallery does not display the data flow; a surface that renders FROM "
                         "the registry must say so where a reader or crawler will see it")
    ds = ROOT / "datasets/capture-registry/index.html"
    if ds.exists() and "capture-flow" not in ds.read_text(errors="replace"):
        fails.append("the published dataset surface does not display the data flow")

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
        # THE AFFORDANCE MUST BE WIRED. The cite control shipped as a bare anchor
        # to #slug with no handler class, so clicking it navigated to the card the
        # reader was already on. It looked functional and did nothing — the worst
        # of the three states, because a broken control that reports success is
        # not distinguishable from one that works.
        # MATCH THE CLASS, NOT THE ATTRIBUTE STRING. The control ships as
        # class="cap-cite cap-act" — it carries cap-act so ONE delegated
        # handler on the container serves every card. An exact-string check for
        # class="cap-cite" reported 0 of 316 on a control that renders twice per
        # card and works: verified 2026-08-14, 632 buttons, handler bound via
        # closest('.cap-act'), reading dataset.citation into navigator.clipboard.
        # A gate that fails a working affordance teaches the next reader to
        # weaken the affordance until the gate passes.
        n_btn = len(re.findall(r'class="[^"]*\bcap-cite\b[^"]*"', pg))

        # THE CITABLE UNIT IS THE OBSERVATION, NOT ONLY THE ADDRESS.
        # ONE SURFACE + ONE SEMANTIC ADDRESS + ONE DATE = ONE CAPTURE. The
        # gallery has always anchored each observation as
        # <details class="cap-obs" id="{observation_slug}">, but the declared
        # grammar named the ADDRESS as the citable unit, so a reader citing one
        # system's behaviour had to cite an address carrying several. The
        # address slug is inherited from whichever observation was seated first:
        # «who is lee sharks?» is anchored at a slug naming Bing Copilot while
        # holding ChatGPT, Perplexity and Google AI Overview captures too.
        # Observation slugs are anchors, so a collision silently resolves two
        # distinct captures to one. Checked here.
        obs = [o for e in entries for o in (e.get("observations") or [])]
        oslugs = [o.get("slug") for o in obs if o.get("slug")]
        odup = len(oslugs) - len(set(oslugs))
        n_oanchor = sum(1 for sl in set(oslugs) if f'id="{sl}"' in pg)
        n_ocite = sum(1 for o in obs if o.get("cite"))
        if odup:
            fails.append(f"{odup} observation slug collision(s); two captures would share one anchor")
        if n_oanchor < len(set(oslugs)):
            fails.append(f"only {n_oanchor} of {len(set(oslugs))} observations are anchored in the page")
        if n_ocite < len(obs):
            fails.append(f"only {n_ocite} of {len(obs)} observations carry a citation")

        # AN ANCHOR THAT APPEARS TWICE IS NOT AN ANCHOR. Duplicate ids are
        # invalid HTML and #slug becomes ambiguous — the browser jumps to
        # whichever element parsed first, so a citation lands somewhere the
        # citer did not choose. Two causes, both found 2026-08-14: the alias
        # span emitted alongside a <details> that already carried the id, and a
        # first observation whose slug is the card's own slug repeating it on
        # the inner <details>.
        import collections as _c
        _ids = _c.Counter(re.findall(r'id="([^"]+)"', pg))
        _dupe = [i for i, n in _ids.items() if n > 1]
        if _dupe:
            fails.append(f"{len(_dupe)} duplicate element id(s) — #{_dupe[0]} resolves ambiguously")

    # FIELD SHAPES THE RENDERER DEREFERENCES. A `collisions` value written as a
    # plain string instead of a list of {with, via, ev} dicts crashed the gallery
    # build on 2026-08-14 with AttributeError deep inside a generator — the data
    # was already written and committed before anything noticed. Checked here, in
    # the data, before a renderer meets it.
    for _e in entries:
        for _o in (_e.get("observations") or [_e]):
            _c = _o.get("collisions")
            if _c is not None and not isinstance(_c, list):
                fails.append(f"{_o.get('slug')}: collisions is {type(_c).__name__}, must be a list of objects")
            elif isinstance(_c, list):
                for _x in _c:
                    if not isinstance(_x, dict) or "with" not in _x:
                        fails.append(f"{_o.get('slug')}: a collisions entry lacks the 'with' key")
                        break
        if n_btn < len(entries):
            fails.append(f"{n_btn} of {len(entries)} cards carry a cite control; "
                         f"the rest offer no way to cite what they display")
        if not re.search(r"closest\(['\"]\.cap-(cite|act)['\"]\)", pg):
            fails.append("no delegated handler for the cite control: the button renders "
                         "and does nothing when clicked")
        if 'data-citation=' not in pg:
            fails.append("the cite control copies no citation, only a bare URL")
        if 'itemtype="https://schema.org/CreativeWork"' not in pg:
            fails.append("captures carry no machine-readable citation microdata; "
                         "a crawler can read the prose and not the attribution")

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

    n_obs = sum(len(e.get('observations') or [e]) for e in entries)
    print(f"addresses: {len(entries)} · captures: {n_obs} · unique slugs: {len(slugs)} · "
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
