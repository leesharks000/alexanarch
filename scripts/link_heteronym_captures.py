#!/usr/bin/env python3
"""link_heteronym_captures.py — attribute captures to heteronyms BY CLAIM.

Captures are the one dataset to rule them all. Every dataset touching reception
must reflect what the registry holds now, not what it held once.

ATTRIBUTION IS BY CLAIM, NOT BY NAME.
An earlier version matched heteronym NAMES against capture text. That was the
same error as the June journal batch: matching strings instead of reading claims.
Rex Fraction does SPXI, so every SPXI capture is his whether or not it names him.
Nobel Glas holds SPXI Framework 15, so some SPXI captures are also his.

ATTRIBUTION IS MANY-TO-MANY.
One heteronym's claim does not exhaust a capture. A capture on "SPXI Lee Sharks"
belongs to Sharks AND to Fraction. Any model that assigns each capture to exactly
one owner will be wrong about most of the interesting ones.

EVERY ATTRIBUTION CARRIES ITS BASIS.
`by` records which claim-term matched and where. Attribution without a stated
basis is what produced 371 deposits in one journal; it is not repeated here.

Claims live in each record's `claims.terms`. To change what a heteronym owns,
edit the record — not this script.

SOURCE OF TRUTH: data/EA-WG-CAPTURES-01.json (live; v11.4, 343 captures).
Decoys: datasets/capture-registry/EA-WG-CAPTURES-01.json is a v10.0 gallery
manifest; data/EA-WG-CAPTURES-01-v8.11.json and -v9.6.json are frozen snapshots.

Usage:
  link_heteronym_captures.py            reattribute
  link_heteronym_captures.py --check    fail if any card has drifted
  link_heteronym_captures.py --orphans  list captures no heteronym claims
"""
import json, sys, pathlib, collections, argparse, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
RECORDS = ROOT / "datasets/heteronyms/records"
FIELDS = ('slug', 'd', 'analysis', 'reading', 'q', 's', 'cites')


def load_claims():
    out = {}
    for p in sorted(RECORDS.glob('*.json')):
        d = json.loads(p.read_text())
        terms = ((d.get('claims') or {}).get('terms')) or []
        if terms:
            out[p.stem] = {'name': d.get('name'), 'terms': [t.lower() for t in terms]}
    return out


def blob(x):
    return ' '.join(str(x.get(k) or '') for k in FIELDS).lower()


# Word-boundary matching. A first pass used plain substring containment and
# attributed 271 captures to Rex Fraction because his claim-term "PER"
# (Provenance Erasure Rate) matched inside "paper", "person" and "operative".
# An acronym is only a claim when it stands as a word.
_CACHE = {}


def claim_hits(term, text):
    rx = _CACHE.get(term)
    if rx is None:
        rx = _CACHE[term] = re.compile(r'(?<![a-z0-9])' + re.escape(term) + r'(?![a-z0-9])')
    return bool(rx.search(text))


def attribute(entries, claims):
    hits = collections.defaultdict(list)
    claimed = set()
    for i, x in enumerate(entries):
        b = blob(x)
        for slug, c in claims.items():
            matched = [t for t in c['terms'] if claim_hits(t, b)]
            if matched:
                hits[slug].append((x, sorted(matched, key=len, reverse=True)[:4]))
                claimed.add(i)
    return hits, claimed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--orphans', action='store_true')
    a = ap.parse_args()

    reg = json.loads(REG.read_text())
    entries = next(v for k, v in reg.items() if isinstance(v, list) and len(v) > 50)
    ver = reg.get('version')
    claims = load_claims()
    hits, claimed = attribute(entries, claims)

    if a.orphans:
        orph = [entries[i] for i in range(len(entries)) if i not in claimed]
        print(f"{len(orph)} of {len(entries)} captures claimed by no heteronym:\n")
        for x in orph[:40]:
            print(f"  [{x.get('s','—'):<22}] {x.get('slug','')[:64]}")
        print("\nAn orphan is a gap in the claims data, not a capture that belongs to nobody.")
        return 0

    drift = []
    for slug, xs in sorted(hits.items()):
        p = RECORDS / f'{slug}.json'
        d = json.loads(p.read_text())
        prev = d.get('captures') if isinstance(d.get('captures'), dict) else {}
        block = {
            "registry": f"EA-WG-CAPTURES-01 v{ver}",
            "source": "data/EA-WG-CAPTURES-01.json — the live registry",
            "attribution": "BY CLAIM (claims.terms), many-to-many; a capture may belong to several heteronyms",
            "regenerate_with": "scripts/link_heteronym_captures.py",
            "count": len(xs),
            "sections": dict(collections.Counter(x.get('s', '—') for x, _ in xs).most_common()),
            "match_types": dict(collections.Counter(x.get('mt', '—') for x, _ in xs).most_common()),
            "attributions": [{"slug": x['slug'], "by": m} for x, m in xs][:80],
            "MATCH_TYPE_IS_EVIDENTIARY": prev.get("MATCH_TYPE_IS_EVIDENTIARY",
                "A broad match means the layer connected the concept unprompted. A phrase match means "
                "exactness was forced and returned — the stricter test of whether a term exists AS a term. "
                "Flattening the two loses the distinction. MANUS: vital."),
        }
        if a.check:
            if prev.get('count') != len(xs) or prev.get('registry') != block['registry']:
                drift.append(f"  {(d.get('name') or slug):<20} card={prev.get('count','—')} live={len(xs)}")
            continue
        d['captures'] = block
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1))

    if a.check:
        if drift:
            print(f"FAIL: {len(drift)} card(s) drifted from registry v{ver}:")
            print("\n".join(drift)); return 1
        print(f"OK: all cards match registry v{ver}"); return 0

    total = sum(len(v) for v in hits.values())
    print(f"registry v{ver}: {len(entries)} captures · {len(claimed)} claimed · "
          f"{len(entries)-len(claimed)} orphaned")
    print(f"{total} attributions across {len(hits)} heteronyms (many-to-many)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
