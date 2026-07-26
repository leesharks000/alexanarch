#!/usr/bin/env python3
"""
build_concept_map.py — data/concept-map.json

EA-RETRIEVAL-DENSITY-01, Task 12. Restores the function lost with the Zenodo
account: a stable identifier per *work* that resolves to that work's current
version, distinct from the per-version identifier.

Alexanarch mints a fresh hex for every deposit, including every version of the
same work (1,405 distinct hexes across 1,410 deposits). So a reader arriving at
DOI REGISTRY v3.0 has no way to learn that v5.0 exists, and the retrieval layer
sees four unrelated documents where there is one work in four states.

TWO FAMILY TYPES, DELIBERATELY SEPARATED
The corpus contains two things that look alike to a naive grouper and must not
be conflated:

  VERSION family  same work, successive states. Needs a concept pointer to the
                  current version. (DOI Registry v2 -> v3 -> v4 -> v5.)
  PROGRAM family  distinct works sharing a programme identifier. Needs a
                  collection, NOT a version pointer. (EA-SEI-PHASEX covers
                  three different papers; pointing one at another would be
                  worse than no resolver at all.)

Grouping on EA identifiers alone produces the second and labels it the first.
This script therefore keys on normalised title base, uses EA identifiers only
as corroboration, and emits programme families separately and explicitly.

DETECTION TIERS (recorded per family so any tier can be discarded)
  version/explicit   shared title base AND >=2 members carry version tokens
  version/superseded shared title base AND a member is marked SUPERSEDED
  version/implicit   shared title base, no version tokens (possible duplicates)
  program/ea         shared EA identifier, divergent title bases

CURRENT-VERSION SELECTION
  highest parsed version tuple; ties broken by date, then by deposit number
  (later mint wins). Families where selection is ambiguous are flagged
  `needs_review` rather than resolved silently.

Usage: python3 scripts/build_concept_map.py [--dry-run]
"""
import json, re, argparse, datetime, collections

REGISTRY = 'data/registry.json'
OUT = 'data/concept-map.json'

VP = re.compile(r'\bv\.?\s*(\d+)\.(\d+)(?:\.(\d+))?\b', re.I)
EA = re.compile(r'\b(EA-[A-Z]{2,12}-[A-Z0-9]{1,12}(?:-\d{2})?)\b')
SUPERSEDED = re.compile(r'\bsuperseded\b', re.I)
HEX = re.compile(r'AXN:([0-9A-Fa-f]{4})')


def norm_title(t):
    """Strip version tokens, supersession notes, identifiers, punctuation."""
    t = str(t or '')
    t = SUPERSEDED.sub(' ', t)
    t = re.sub(r'10\.5281/zenodo\.\d+', ' ', t)
    t = re.sub(r'AXN:[0-9A-Fa-f]{4}[^\s]*', ' ', t)
    t = EA.sub(' ', t)
    t = VP.sub(' ', t)
    t = re.sub(r'\b(version|draft|final|rev|edition)\s*\d+[\.\d]*\b', ' ', t, flags=re.I)
    t = re.sub(r'[^a-z0-9 ]', ' ', t.lower())
    return re.sub(r'\s+', ' ', t).strip()


def vtuple(t):
    m = VP.search(str(t or ''))
    if not m:
        return None
    return tuple(int(g) for g in m.groups() if g is not None)


def slug(s, n=60):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s[:n].rstrip('-')


def build():
    reg = json.load(open(REGISTRY, encoding='utf-8'))
    deps = reg['deposits']

    # index by normalised title base
    bases = collections.defaultdict(list)
    for d in deps:
        b = norm_title(d.get('title'))
        if len(b) >= 12:                      # too-short bases over-merge
            bases[b].append(d)

    concepts, programs, review = [], [], 0
    claimed = set()

    for base, members in sorted(bases.items()):
        if len(members) < 2:
            continue
        vt = [m for m in members if vtuple(m.get('title'))]
        sup = [m for m in members if SUPERSEDED.search(str(m.get('title', '')))]
        if len(vt) >= 2:
            basis = 'version/explicit'
        elif sup:
            basis = 'version/superseded'
        else:
            basis = 'version/implicit'

        def sortkey(m):
            v = vtuple(m.get('title')) or (0,)
            return (v, str(m.get('date') or ''), m['deposit_number'])
        ordered = sorted(members, key=sortkey)
        current = ordered[-1]
        top = [m for m in ordered if sortkey(m)[0] == sortkey(current)[0]]
        ambiguous = len(top) > 1 and basis != 'version/implicit'
        if ambiguous:
            review += 1

        eas = sorted({e for m in members
                      for e in EA.findall(str(m.get('title', '')))})
        hexes = [HEX.match(str(m.get('axn', ''))) for m in ordered]
        root_hex = next((h.group(1).upper() for h in hexes if h), None)

        cid = slug(base)
        concepts.append({
            'concept_id': cid,
            'concept_url': f'https://www.alexanarch.org/s/concept/{cid}/',
            'title_base': base,
            'basis': basis,
            'root_axn_hex': root_hex,
            'ea_identifiers': eas,
            'member_count': len(members),
            'needs_review': ambiguous,
            'current': {
                'deposit_number': current['deposit_number'],
                'axn': current.get('axn'),
                'title': current.get('title'),
                'date': current.get('date'),
                'version': '.'.join(map(str, vtuple(current.get('title')) or [])) or None,
                'record_url': f"https://www.alexanarch.org/s/records/{current['deposit_number']}/",
            },
            'versions': [{
                'deposit_number': m['deposit_number'],
                'axn': m.get('axn'),
                'title': m.get('title'),
                'date': m.get('date'),
                'version': '.'.join(map(str, vtuple(m.get('title')) or [])) or None,
                'superseded_marker': bool(SUPERSEDED.search(str(m.get('title', '')))),
                'is_current': m['deposit_number'] == current['deposit_number'],
                'record_url': f"https://www.alexanarch.org/s/records/{m['deposit_number']}/",
            } for m in ordered],
        })
        claimed.update(m['deposit_number'] for m in members)

    # FUZZY TIER. Titles drift between versions ("Crimson Hexagonal
    # Architecture: FRACTAL NAVIGATION MAP v7.0" vs "The Crimson Hexagon:
    # Fractal Navigation Map"), so exact base matching misses the largest
    # families. Fuzzy grouping catches them but can over-merge, so it is gated
    # hard and NEVER auto-resolves: every fuzzy family is emitted with
    # needs_review=True and no current-version pointer is trusted until a human
    # signs it off. Requires version tokens in >=2 members, so that distinct
    # works are not merged merely for sharing a subject.
    import difflib
    remaining = [d for d in deps if d['deposit_number'] not in claimed
                 and vtuple(d.get('title'))]
    rem_bases = [(d, norm_title(d.get('title'))) for d in remaining]
    used = set()
    for i, (d1, b1) in enumerate(rem_bases):
        if d1['deposit_number'] in used or len(b1) < 16:
            continue
        group = [d1]
        for d2, b2 in rem_bases[i + 1:]:
            if d2['deposit_number'] in used or len(b2) < 16:
                continue
            r = difflib.SequenceMatcher(None, b1[:70], b2[:70]).ratio()
            if r >= 0.86:
                group.append(d2)
        if len(group) < 2:
            continue
        ordered = sorted(group, key=lambda m: ((vtuple(m.get('title')) or (0,)),
                                               str(m.get('date') or ''),
                                               m['deposit_number']))
        current = ordered[-1]
        eas = sorted({e for m in group for e in EA.findall(str(m.get('title', '')))})
        root_hex = next((h.group(1).upper() for h in
                         (HEX.match(str(m.get('axn', ''))) for m in ordered) if h), None)
        cid = slug(norm_title(d1.get('title')))
        concepts.append({
            'concept_id': cid,
            'concept_url': f'https://www.alexanarch.org/s/concept/{cid}/',
            'title_base': b1,
            'basis': 'version/fuzzy',
            'root_axn_hex': root_hex,
            'ea_identifiers': eas,
            'member_count': len(group),
            'needs_review': True,
            'current': {
                'deposit_number': current['deposit_number'],
                'axn': current.get('axn'),
                'title': current.get('title'),
                'date': current.get('date'),
                'version': '.'.join(map(str, vtuple(current.get('title')) or [])) or None,
                'record_url': f"https://www.alexanarch.org/s/records/{current['deposit_number']}/",
                'provisional': True,
            },
            'versions': [{
                'deposit_number': m['deposit_number'],
                'axn': m.get('axn'),
                'title': m.get('title'),
                'date': m.get('date'),
                'version': '.'.join(map(str, vtuple(m.get('title')) or [])) or None,
                'superseded_marker': bool(SUPERSEDED.search(str(m.get('title', '')))),
                'is_current': m['deposit_number'] == current['deposit_number'],
                'record_url': f"https://www.alexanarch.org/s/records/{m['deposit_number']}/",
            } for m in ordered],
        })
        used.update(m['deposit_number'] for m in group)
        claimed.update(m['deposit_number'] for m in group)
        review += 1

    # programme families: shared EA identifier spanning divergent title bases
    by_ea = collections.defaultdict(list)
    for d in deps:
        for e in set(EA.findall(str(d.get('title', '')))):
            by_ea[e.upper()].append(d)
    for e, members in sorted(by_ea.items()):
        if len(members) < 2:
            continue
        if len({norm_title(m.get('title')) for m in members}) < 2:
            continue                          # single work -> already a concept
        programs.append({
            'program_id': e,
            'program_url': f'https://www.alexanarch.org/s/program/{slug(e)}/',
            'note': ('Distinct works sharing a programme identifier. This is a '
                     'collection, not a version family: no current-version '
                     'pointer is asserted.'),
            'member_count': len(members),
            'members': [{
                'deposit_number': m['deposit_number'],
                'axn': m.get('axn'),
                'title': m.get('title'),
                'date': m.get('date'),
                'record_url': f"https://www.alexanarch.org/s/records/{m['deposit_number']}/",
            } for m in sorted(members, key=lambda x: str(x.get('date') or ''))],
        })

    basis_counts = collections.Counter(c['basis'] for c in concepts)
    return {
        '$schema': 'https://www.alexanarch.org/data/concept-map.schema.json',
        'name': 'Concept Map — work-level identity and current-version resolution',
        'description': (
            'Restores the concept-identifier function lost with the terminated '
            'Zenodo account. Alexanarch mints a fresh hex per deposit, so every '
            'version of a work is an independent object with no link to its '
            'siblings; a reader arriving at an old version cannot learn that a '
            'newer one exists. Each concept here names a work and points at its '
            'current version. Programme families — distinct works sharing an '
            'identifier — are listed separately and carry no version pointer, '
            'because conflating the two would resolve one work to another. '
            'Every family records the basis on which it was detected so any '
            'confidence tier can be discarded independently.'),
        'generated_by': 'scripts/build_concept_map.py',
        'generated_at': datetime.datetime.now(datetime.timezone.utc)
                        .isoformat(timespec='seconds').replace('+00:00', 'Z'),
        'totals': {
            'deposits': len(deps),
            'concepts': len(concepts),
            'deposits_in_concepts': len(claimed),
            'singletons': len(deps) - len(claimed),
            'needs_review': review,
            'program_families': len(programs),
        },
        'basis_counts': dict(basis_counts),
        'concepts': concepts,
        'program_families': programs,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    p = build()
    t = p['totals']
    print(f"concepts={t['concepts']}  deposits_in_concepts={t['deposits_in_concepts']}  "
          f"singletons={t['singletons']}  needs_review={t['needs_review']}  "
          f"program_families={t['program_families']}")
    for k, v in p['basis_counts'].items():
        print(f"   {k:22s} {v}")
    if a.dry_run:
        print('[dry-run] no write')
        return
    json.dump(p, open(OUT, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print(f'[ok] wrote {OUT}')


if __name__ == '__main__':
    main()
