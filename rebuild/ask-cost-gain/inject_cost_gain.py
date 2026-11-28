#!/usr/bin/env python3
"""Add the two 'cost' and 'gain' links to the 'Ask ChatGPT otherwise' row of every record page already rendered, by replacing that row with
the generator's own output (wire_deposit.ask_otherwise_html), and nothing else on the page. A full re-render was tried first and set aside:
on 63 of 64 sampled pages it also changed other blocks (blank lines, regenerated sections), which this change has no business touching.
    python3 rebuild/ask-cost-gain/inject_cost_gain.py"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
import wire_deposit as W
row = re.compile(r'<div class="ask-otherwise"[^>]*>.*?</div>', re.S)
done = same = norow = mismatch = 0
for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]:
    p = ROOT / f"s/records/{d['deposit_number']}/index.html"
    if not p.exists(): continue
    s = p.read_text(encoding="utf-8"); m = row.search(s)
    if not m: norow += 1; continue
    new = W.ask_otherwise_html(d)
    old_links = re.findall(r'href="([^"]+)"', m.group(0)); new_links = re.findall(r'href="([^"]+)"', new)
    if new_links[:len(old_links)] != old_links: mismatch += 1; continue          # the page's row is not the generator's earlier output: left alone, counted
    if m.group(0) == new: same += 1; continue
    p.write_text(s[:m.start()] + new + s[m.end():], encoding="utf-8"); done += 1
print(f"rows replaced {done}; already current {same}; pages without the row {norow}; rows that differ from the generator's earlier links, left alone {mismatch}")
