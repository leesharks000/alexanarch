#!/usr/bin/env python3
"""check_capture_page_current.py — fail when the captures page is behind the registry.

THE DEFECT THIS CLOSES (2026-08-15). Twelve captures were seated, committed and
pushed; the registry read 343 and the live page read 331 for hours. Nothing
failed. Three separate gaps, each silent:

  1. build_capture_gallery.py is NOT part of regenerate_surfaces.py, so the
     standard post-seating regeneration never rebuilt the cards.
  2. `dynamic-counts` is a regenerate_surfaces surface that has to be NAMED in
     --only, and every invocation this session named other surfaces instead.
  3. The gallery build CRASHED on schema drift in the new entries and the
     crash was invisible — the page simply kept its previous bytes, which are
     valid HTML, correctly served, and wrong.

A stale page is worse than a broken one: broken gets noticed. This check makes
the mismatch loud, and belongs in the post-seating sequence next to the
supersession gate.

Exit 0 when the page matches the registry, 1 when it does not.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
PAGE = ROOT / "captures/index.html"


def main():
    reg = json.loads(REG.read_text())
    n_entries = len(reg["entries"])
    declared = reg.get("address_count")
    page = PAGE.read_text()
    cards = page.count('class="cap-card"')
    m = re.search(r"complete list of ([\d,]+) captures", page)
    noscript = int(m.group(1).replace(",", "")) if m else None

    rows = [("registry entries", n_entries), ("registry address_count", declared),
            ("rendered cap-cards", cards), ("noscript count", noscript)]
    width = max(len(r[0]) for r in rows)
    for label, val in rows:
        print(f"  {label:<{width}}  {val}")

    bad = []
    if declared != n_entries:
        bad.append(f"registry address_count ({declared}) != entries ({n_entries})")
    if cards != n_entries:
        bad.append(f"page has {cards} cards for {n_entries} entries — run scripts/build_capture_gallery.py")
    if noscript != n_entries:
        bad.append(f"noscript says {noscript} for {n_entries} entries — run scripts/build_capture_gallery.py")

    # a surface must never be a section
    surfaces = {str(e.get("surface") or "") for e in reg["entries"]}
    sections = {str(e.get("s") or "") for e in reg["entries"]}
    collide = sorted(s for s in sections & surfaces if s)
    if collide:
        bad.append("SECTION/SURFACE COLLISION — s is the section, sf is the surface descriptor: "
                   + ", ".join(collide))
    unsectioned = sum(1 for e in reg["entries"] if not e.get("s"))
    if unsectioned:
        bad.append(f"{unsectioned} entries carry no section")

    if bad:
        print("\nCAPTURE PAGE IS NOT CURRENT:")
        for b in bad:
            print("  ✗ " + b)
        return 1
    print("\nCAPTURE PAGE MATCHES THE REGISTRY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
