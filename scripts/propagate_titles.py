#!/usr/bin/env python3
"""
propagate_titles.py — push canonical titles from the registry into every derived
dataset that carries a copy of them.

WHY THIS EXISTS. Deposit titles are copied into at least eight datasets. The
registry is the source of truth, but the regenerators do not refresh a title they
already hold: build_concept_map, build_mirror_map, generate_wiki, and the
browse/resolution index builders preserve the title recorded when the entry was
first created. Editing data/registry.json alone therefore does not correct the
corpus — it creates competing sets of deposit names, one per dataset, with no
signal to a consumer about which is current.

Discovered 2026-07-28 while repairing 152 titles whose frontmatter had been
concatenated into the title field and truncated at a character ceiling. After
running regenerate_surfaces.py, build_concept_map.py and build_mirror_map.py,
five datasets still carried the superseded strings: doi-resolution-index (125),
wiki-entries (113), browse-index (83), mirror-map (58), concept-map (21),
capture-deposit-links (21).

WHAT IT DOES. For each dataset, walks its records, resolves each to a registry
deposit by deposit_number or AXN, and replaces the title field with the registry
value. It never invents a title, never edits a record it cannot resolve, and
reports both what it changed and what it could not match.

Usage: python3 scripts/propagate_titles.py [--apply]
"""
import json, re, os, argparse

REGISTRY = 'data/registry.json'
HEX = re.compile(r'AXN:([0-9A-Fa-f]{4})')

# dataset path -> how to find its record list, and which keys identify/carry the title
# data/doi-resolution-index.json is DELIBERATELY EXCLUDED. Its title field records the
# title a work carried AT ZENODO, not the current deposit title — historical metadata
# about a severed identifier. Some rows are mapping_type=misclassified_other_author and
# name works by other authors entirely. Overwriting those from the registry would destroy
# the record of what each dead DOI was called, which is the index's whole purpose.
TARGETS = [
    ('data/concept-map.json',           None),
    ('data/mirror-map.json',            None),
    ('data/wiki-entries.json',          None),
    ('data/capture-deposit-links.json', None),
    ('data/browse-index.json',          None),
    ('datasets/set.json',               None),
]

ID_KEYS = ('deposit_number', 'deposit', 'record', 'n', 'number')
AXN_KEYS = ('axn', 'AXN', 'axn_full', 'identifier')
TITLE_KEYS = ('title', 'name', 'headline')


def load_registry():
    reg = json.load(open(REGISTRY, encoding='utf-8'))
    by_num, by_hex = {}, {}
    for d in reg['deposits']:
        t = str(d.get('title') or '')
        if not t:
            continue
        by_num[d['deposit_number']] = t
        m = HEX.match(str(d.get('axn') or ''))
        if m:
            by_hex.setdefault(m.group(1).upper(), t)
    return by_num, by_hex


def resolve(node, by_num, by_hex):
    """Return the canonical title for a record node, or None if unresolvable."""
    for k in ID_KEYS:
        v = node.get(k)
        if isinstance(v, int) and v in by_num:
            return by_num[v]
        if isinstance(v, str) and v.isdigit() and int(v) in by_num:
            return by_num[int(v)]
    for k in AXN_KEYS:
        v = node.get(k)
        m = HEX.match(str(v or ''))
        if m and m.group(1).upper() in by_hex:
            return by_hex[m.group(1).upper()]
    # a record path such as /s/records/1234/
    for v in node.values():
        if isinstance(v, str):
            m = re.search(r'/s/records/(\d+)/', v)
            if m and int(m.group(1)) in by_num:
                return by_num[int(m.group(1))]
    return None


def walk(obj, by_num, by_hex, stats):
    """Recursively find dicts that carry a title and an identifier, and correct them."""
    if isinstance(obj, dict):
        tk = next((k for k in TITLE_KEYS if isinstance(obj.get(k), str)), None)
        if tk:
            canon = resolve(obj, by_num, by_hex)
            if canon is None:
                stats['unresolved'] += 1
            elif obj[tk] != canon:
                obj[tk] = canon
                stats['corrected'] += 1
            else:
                stats['already'] += 1
        for v in obj.values():
            walk(v, by_num, by_hex, stats)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, by_num, by_hex, stats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    by_num, by_hex = load_registry()
    print("registry: %d titles\n" % len(by_num))
    print("%-42s %10s %10s %12s" % ("dataset", "corrected", "already", "unresolved"))
    total = 0
    for path, _ in TARGETS:
        if not os.path.exists(path):
            print("%-42s %s" % (path, "(absent)"))
            continue
        data = json.load(open(path, encoding='utf-8'))
        stats = {'corrected': 0, 'already': 0, 'unresolved': 0}
        walk(data, by_num, by_hex, stats)
        total += stats['corrected']
        print("%-42s %10d %10d %12d" % (path, stats['corrected'], stats['already'], stats['unresolved']))
        if a.apply and stats['corrected']:
            json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print("\ntotal titles corrected: %d" % total)
    if not a.apply:
        print("[dry-run] nothing written. re-run with --apply")


if __name__ == '__main__':
    main()
