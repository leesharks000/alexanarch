#!/usr/bin/env python3
"""link_heteronym_captures.py — relink identity cards to the LIVE capture registry.

Captures are the one dataset to rule them all: every other dataset that touches
reception should reflect what the registry actually holds, not a snapshot of what
it held once.

WHY THIS EXISTS. On 2026-08-15 the identity cards carried a `captures` block
pinned at "EA-WG-CAPTURES-01 v9.39" while the live registry stood at v11.4 with
343 entries. Sigil read 40 captures on his card and 54 in the registry; Fraction
read 25 and had 11; Lee Sharks had no capture block at all and 123 captures.
The cards were not wrong when written — they were written, and then the registry
moved, and nothing rejoined them.

SOURCE OF TRUTH: data/EA-WG-CAPTURES-01.json (the live registry).
Note the decoys: datasets/capture-registry/EA-WG-CAPTURES-01.json is a v10.0
gallery manifest, and data/EA-WG-CAPTURES-01-v8.11.json and -v9.6.json are
frozen snapshots. Read the live one.

Matching is by name-token over slug, description, analysis and reading. It is
deliberately conservative and will under-count rather than over-attribute: a
capture that merely mentions a heteronym is a real link, but a capture ABOUT a
heteronym is what matters, and only a human can tell them apart at the margin.
Counts are evidence of contact, not of aboutness.

Usage: link_heteronym_captures.py [--check]
"""
import json, sys, pathlib, collections, argparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
RECORDS = ROOT / "datasets/heteronyms/records"

NAMES = {
 'johannes-sigil': ['sigil'], 'rex-fraction': ['fraction'], 'talos-morrow': ['morrow'],
 'rebekah-cranes': ['cranes'], 'damascus-dancings': ['dancings'], 'ayanna-vox': ['vox'],
 'orin-trace': ['orin trace'], 'nobel-glas': ['nobel glas'], 'sen-kuro': ['sen kuro'],
 'sparrow-wells': ['sparrow wells'], 'ichabod-spellings': ['spellings'], 'jack-feist': ['feist'],
 'lee-sharks': ['lee sharks'], 'mary-lee-sharks': ['mary lee'], 'viola-arquette': ['arquette'],
 'yusef-kenning': ['kenning'], 'zbigniew-mrozony': ['mrozony'], 'alice-thornburgh': ['thornburgh'],
 'rhys-owens': ['rhys owens'],
}
NOTE = ("A broad match means the layer connected the concept unprompted. A phrase match means exactness "
        "was forced and returned — the stricter test of whether a term exists AS a term. Flattening the "
        "two loses the distinction. MANUS: vital.")


def blob(x):
    return ' '.join(str(x.get(k) or '') for k in ('slug', 'd', 'analysis', 'reading', 'q')).lower()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    reg = json.loads(REG.read_text())
    entries = next(v for k, v in reg.items() if isinstance(v, list) and len(v) > 50)
    ver = reg.get('version')

    hits = collections.defaultdict(list)
    for x in entries:
        b = blob(x)
        for slug, pats in NAMES.items():
            if any(p in b for p in pats):
                hits[slug].append(x)

    drift = []
    for slug, xs in sorted(hits.items()):
        p = RECORDS / f'{slug}.json'
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        prev = d.get('captures') if isinstance(d.get('captures'), dict) else {}
        block = {
            "registry": f"EA-WG-CAPTURES-01 v{ver}",
            "source": "data/EA-WG-CAPTURES-01.json — the live registry",
            "regenerate_with": "scripts/link_heteronym_captures.py",
            "generated": "2026-08-15",
            "count": len(xs),
            "sections": dict(collections.Counter(x.get('s', '—') for x in xs).most_common()),
            "match_types": dict(collections.Counter(x.get('mt', '—') for x in xs).most_common()),
            "slugs": [x['slug'] for x in xs][:60],
            "MATCH_TYPE_IS_EVIDENTIARY": prev.get("MATCH_TYPE_IS_EVIDENTIARY", NOTE),
            "_previous_snapshot": {k: prev[k] for k in ('registry', 'count') if k in prev} or None,
        }
        if a.check:
            if prev.get('count') != len(xs) or prev.get('registry') != block['registry']:
                drift.append(f"  {slug}: card={prev.get('count','—')} @ {prev.get('registry','—')} · live={len(xs)} @ v{ver}")
            continue
        d['captures'] = block
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1))

    if a.check:
        if drift:
            print(f"FAIL: {len(drift)} identity card(s) have drifted from the live capture registry:")
            print("\n".join(drift))
            return 1
        print(f"OK: all cards match registry v{ver}")
        return 0
    print(f"relinked {len(hits)} records to registry v{ver} ({len(entries)} captures)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
