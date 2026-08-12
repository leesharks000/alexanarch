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


def links_for(slug, galleries):
    out = [{"url": f"{CANONICAL}#{slug}", "authority": "canonical",
            "note": "the archive holds the registry and the images; cite this form"}]
    for g in galleries:
        out.append({"url": f"{g.rstrip('/')}/#{slug}", "authority": "mirror",
                    "note": "renders from the archive's registry; may lag a deploy"})
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
        e_cite = f"{CANONICAL}#{slug}"
        if e.get("cite") != e_cite and not a.check:
            e["cite"] = e_cite

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
        "canonical": CANONICAL + "#{slug}",
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
