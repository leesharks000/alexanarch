#!/usr/bin/env python3
"""build_capture_links.py — every capture carries its own citation and its mirrors.

WHY THIS RUNS ON EVERY CAPTURE ADDED
Until 2026-08-07 the deep link `gallery/#slug` was assembled at RENDER TIME by
each gallery independently, from a list of gallery URLs, in JavaScript. That
meant three things, all bad: the registry could not tell you where a capture was
reachable without running a browser; a gallery added to the fleet inherited
nothing; and — the reason this exists — nobody noticed for months that the
anchors those links point at were never set anywhere.

So the links are now DATA, written into the registry when the capture is added,
not inferred later by whoever happens to be rendering. The registry states where
each capture can be found, and a gate can check it. An address that only exists
inside a renderer is not published.

CANONICAL vs MIRROR
The archive is the canonical citation target because the archive is the
authority. Mirrors deploy separately and may lag, so a mirror link is recorded
as a convenience and explicitly marked `authority: mirror`. A citation always
uses the canonical form.

Usage:
    python3 scripts/build_capture_links.py            # write links for all captures
    python3 scripts/build_capture_links.py --check    # fail if any are missing/stale
"""
import json, sys, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
CANONICAL = "https://www.alexanarch.org/captures/"
# THE RECORD PAGE IS THE CITATION (ruling, Lee Sharks, 2026-10-01: "b"). Until then a capture was cited at
# captures/#{slug}, an anchor inside one page that had grown past 8 MB. A fetcher drops the fragment and requests
# the whole page, and the fetch interfaces composition surfaces use refuse a response above about 4 MiB, so no
# citation in the registry resolved for a machine (diagnosed by ChatGPT, 2026-10-01: "Content length is too
# large: 4,194,305+ bytes"). Each capture now has its own page, captures/{slug}/, written by
# build_capture_records.py; an observation is cited at captures/{address_slug}/#{observation_slug} on that page,
# and captures/{observation_slug}/ resolves to it. The gallery anchors remain and still resolve in a browser.
RECORD = CANONICAL + "{slug}/"


def record_url(slug):
    return RECORD.format(slug=slug)


def links_for(slug, galleries):
    out = [{"url": record_url(slug), "authority": "canonical",
            "note": "the capture's own record page; cite this form"}]
    for g in galleries:
        g = g.rstrip('/')
        if g + '/' == CANONICAL:
            out.append({"url": f"{CANONICAL}#{slug}", "authority": "gallery",
                        "note": "the canonical gallery, anchored by slug"})
        else:
            out.append({"url": f"{g}/#{slug}", "authority": "mirror",
                        "note": "a window that renders from the archive's registry; may lag a deploy"})
    return out


def main():
    if not REG.exists():
        print("SKIP: the Capture Registry is withdrawn from publication (quarantine/capture-registry-20260812/) and under reconstruction; nothing to process.")
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    r = json.loads(REG.read_text())
    galleries = r.get("galleries", [])
    stale, missing = [], []

    for e in r["entries"]:
        slug = e.get("slug")
        if not slug:
            missing.append("(no slug)")
            continue
        want = links_for(slug, galleries)
        have = e.get("links")
        if have != want:
            (stale if have else missing).append(slug)
            if not a.check:
                e["links"] = want
        e_cite = record_url(slug)
        if e.get("cite") != e_cite and not a.check:
            e["cite"] = e_cite

        # OBSERVATIONS ARE CITABLE UNITS TOO (2026-08-27). This loop set `cite`
        # on the entry and stopped, so every entry carrying an `observations`
        # list left those observations without the canonical anchor the citation
        # grammar declares — 22 of 511 at the time this was found, and the
        # citability audit had been failing on them through three consecutive
        # deposit pipelines. The anchor is derived, not authored: an observation
        # with a slug has exactly one canonical form, and withholding it means
        # the registry advertises a unit no one can cite.
        for o in (e.get("observations") or []):
            o_slug = o.get("slug")
            if not o_slug:
                continue
            o_cite = record_url(slug) + ("" if o_slug == slug else f"#{o_slug}")
            if o.get("cite") != o_cite and not a.check:
                o["cite"] = o_cite

    if a.check:
        bad = missing + stale
        print(f"captures: {len(r['entries'])} · galleries declared: {len(galleries)}")
        if bad:
            for s in bad[:8]:
                print(f"  FAIL  {s} — links absent or not matching the declared galleries",
                      file=sys.stderr)
            print(f"\n{len(bad)} capture(s) without current links. Run without --check.",
                  file=sys.stderr)
            print("An address that only exists inside a renderer is not published.",
                  file=sys.stderr)
            return 1
        print("EVERY CAPTURE CARRIES ITS CANONICAL CITATION AND ITS MIRRORS")
        return 0

    r["link_policy"] = {
        "canonical": RECORD,
        "observation": RECORD + "#{observation_slug}",
        "ruled": "2026-10-01 (Lee Sharks): the capture's record page is the citation (option b); gallery anchors remain",
        "rule": "Links are DATA, written when a capture is added — not assembled at render "
                "time by whichever gallery happens to be running. The archive is canonical "
                "because it is the authority; mirrors are marked as mirrors and may lag.",
        "on_adding_a_gallery": "Add it to `galleries`, then re-run scripts/build_capture_links.py "
                               "so every existing capture gains the new mirror. A gallery that is "
                               "not in `galleries` is not part of the fleet, whatever it serves.",
        "on_adding_a_capture": "scripts/build_capture_links.py runs and writes the link set; "
                               "scripts/audit_capture_citability.py --check gates it.",
    }
    REG.write_text(json.dumps(r, ensure_ascii=False, indent=1))
    print(f"links written for {len(r['entries'])} captures across "
          f"{len(galleries)} declared galleries + the canonical archive form")
    if missing:
        print(f"  first-time links: {len(missing)}")
    if stale:
        print(f"  refreshed: {len(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
