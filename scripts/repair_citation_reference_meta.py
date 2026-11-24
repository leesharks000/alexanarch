#!/usr/bin/env python3
"""repair_citation_reference_meta.py — bring every record page's citation_reference tags to the renderer's form, in place.

The author, 2026-11-23 20:40: "we have to keep standard works cited lists alongside axn citations - aggregators read
citations as authority. full stop. google scholar wont index without it." No record page carried citation_reference
tags. The renderer (wire_deposit.citation_reference_tags) now writes one per entry of the record's standard list
(scripts/references_lib.py). This repairs the pages already rendered, touching only that block, placed directly after
citation_language, so no other layer of a page moves (the method of repair_scholar_meta.py). Not a record modification:
the page is brought to what the record already says. Idempotent; prints what changed.

    python3 scripts/repair_citation_reference_meta.py [--check] [N ...]"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
import os
os.chdir(ROOT)
import wire_deposit as W

OLD = re.compile(r'(?:<meta name="citation_reference" content="[^"]*">\n?)+')
LANG = '<meta name="citation_language" content="en">\n'


def main(argv):
    check = "--check" in argv
    only = {int(a) for a in argv if a.isdigit()}
    reg = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
    changed = pages_with = tags = 0
    for n, d in sorted(reg.items()):
        if only and n not in only:
            continue
        p = ROOT / f"s/records/{n}/index.html"
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        block = W.citation_reference_tags(d)
        t = OLD.sub("", s)
        if block:
            if LANG not in t:
                continue
            t = t.replace(LANG, LANG + block, 1)
            pages_with += 1; tags += block.count("<meta")
        if t != s:
            changed += 1
            if not check:
                p.write_text(t, encoding="utf-8")
    print(f"record pages {'to change' if check else 'changed'}: {changed}; pages with a list: {pages_with}; tags: {tags}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
