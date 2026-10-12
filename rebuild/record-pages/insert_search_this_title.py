#!/usr/bin/env python3
"""Place (or replace in place) the 'Search this title' line, broad with an exact-match link beside it, on existing record pages without re-rendering them (2026-10-11).

A full re-render was tried and reverted: the renderer has moved on from many pages (titles, descriptions and DOI lines change), and
210 pages carry surgical layers the renderer refuses to strip. So the line is inserted at one point, immediately before the page's
single '<h2>Description</h2>', and nothing else on the page is touched. Idempotent: a page that already carries the line is left as
it is. The line itself comes from wire_deposit.search_this_title_html, the renderer's own function, so new and old pages agree."""
import json, pathlib, sys, collections, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); import os; os.chdir(ROOT)
import wire_deposit as w
reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
MARK = "<h2>Description</h2>"
c = collections.Counter(); skipped = []
for d in reg["deposits"]:
    n = d["deposit_number"]; p = ROOT / f"s/records/{n}/index.html"
    if not p.exists(): c["no page"] += 1; continue
    line = w.search_this_title_html(d, len(w._captures_for_deposit(n)))
    if not line: c["status " + str(d.get("status"))] += 1; continue
    h = p.read_text(encoding="utf-8")
    if 'class="search-this-title"' in h:
        # REPLACED IN PLACE (2026-10-11, broad first): the existing line is swapped for the current one; nothing else moves.
        new = re.sub(r'<div class="search-this-title"[^>]*>.*?</div>', lambda m: line, h, count=1, flags=re.S)
        if new == h: c["already current"] += 1; continue
        p.write_text(new, encoding="utf-8"); c["replaced"] += 1; continue
    if h.count(MARK) != 1: c["no single Description heading"] += 1; skipped.append(n); continue
    p.write_text(h.replace(MARK, line + "\n" + MARK, 1), encoding="utf-8"); c["inserted"] += 1
print(dict(c)); print("skipped (no single Description heading):", skipped[:40], len(skipped))
