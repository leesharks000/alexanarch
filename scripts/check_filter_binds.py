#!/usr/bin/env python3
"""check_filter_binds.py — does the list filter actually bind to the rows?

THE DEFECT THIS CLOSES
On 2026-08-14 the filters on /s/browse/ and /s/wiki/ were inert. Every part
looked right: the widget was present, the row selector matched 1,460 elements,
the count and full-search targets existed, the logic was correct, and both
`node --check` and the runtime gate reported clean.

The script ran DURING PARSE, above the list it filters — which is where a filter
bar belongs. `document.querySelectorAll` therefore returned an empty list, and
the guard `if (!rows.length) return;` fired. The guard written to protect the
page from blanking is what disabled it.

WHY NEITHER EXISTING GATE CAUGHT IT
`node --check` is a syntax check; this is legal syntax. And
check_gallery_js.js's stub DOM returns rows from querySelectorAll
unconditionally, so it exercised a function that on the real page never ran —
it reported "none threw" about code that was never reached.

WHAT THIS CHECKS
Document order: the script that queries the rows must not execute before the
rows exist. Either it defers (DOMContentLoaded / readyState / defer attribute)
or it sits after the last row. Anything else is an inert filter.
"""
import re, sys, pathlib

SURFACES = [
    ("s/browse/index.html", r'<a[^>]+href="/s/records/\d+/"', "browse"),
    ("s/wiki/index.html",   r'class="entry-row"',             "wiki"),
]
ROOT = pathlib.Path(__file__).resolve().parent.parent


def check(path, row_pat, label):
    p = ROOT / path
    if not p.exists():
        return [f"{label}: {path} missing"]
    t = p.read_text(errors="replace")
    fails = []
    rows = [m.start() for m in re.finditer(row_pat, t)]
    if not rows:
        return [f"{label}: no rows matched {row_pat!r} — selector and markup have diverged"]
    # Scope the deferral test to THE SCRIPT THAT QUERIES THE ROWS. A page-wide
    # search for DOMContentLoaded passes as soon as any unrelated script mentions
    # it, which is a gate that can be fooled by a neighbour.
    blocks = [(m.start(), m.group(1), m.group(2))
              for m in re.finditer(r'<script([^>]*)>([\s\S]*?)</script>', t)]
    owner = next(((pos, attrs, body) for pos, attrs, body in blocks
                  if "querySelectorAll" in body and "axnflt" in body), None)
    if owner is None:
        return [f"{label}: no script queries the rows — filter behaviour absent"]
    q, attrs, body = owner
    defers = ("DOMContentLoaded" in body) or ("readyState" in body) or re.search(r'\bdefer\b', attrs)
    if q < rows[0] and not defers:
        fails.append(
            f"{label}: filter queries rows at byte {q:,} but the first row is at {rows[0]:,} "
            f"and nothing defers execution — querySelectorAll returns 0, the length guard "
            f"fires, and the filter never binds ({len(rows):,} rows present and unfilterable)")
    for need in ("axnflt", "axnfltcount", "axnfltfull"):
        if f'id="{need}"' not in t:
            fails.append(f"{label}: #{need} missing — apply() dereferences it")
    print(f"  {label:<7} rows {len(rows):>6,} · query at {q:>9,} · first row at {rows[0]:>9,} · "
          f"deferred: {'yes' if defers else 'NO'}")
    return fails


def main():
    print("filter binding")
    fails = []
    for path, pat, label in SURFACES:
        fails += check(path, pat, label)
    for f in fails:
        print(f"  FAIL  {f}", file=sys.stderr)
    if fails:
        print("\nA filter that never binds is indistinguishable from a filter that finds nothing.",
              file=sys.stderr)
        return 1
    print("EVERY LIST FILTER BINDS TO ITS ROWS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
