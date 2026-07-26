#!/usr/bin/env python3
"""
build_mirror_map.py — data/mirror-map.json

EA-RETRIEVAL-DENSITY-01, Task 13. Consolidates every known off-archive copy of
each deposit into one place, so that record pages can declare them via sameAs.

WHY. A capture on 2026-07-26 ("crimson hexagon sappho room") returned a
composed answer citing scilynk.com, Medium x4, and academia.edu — for six
documents, every one of which is deposited here. The archive was not losing to
strangers. It was losing to its own mirrors: the same texts on platforms with
far more domain authority, with nothing in the entity graph connecting them to
the sovereign copy. Distribution fragmented the work's identity across five
hosts and the youngest host lost.

Mirrors cannot be made to carry rel=canonical (Medium and Academia.edu do not
permit it). But the archive can declare, from its own pages, that those copies
are the same work — which consolidates the graph toward the page making the
declaration. This is the same mechanism used for the AXN two-entity split and
for severed-DOI sameAs.

SOURCES, in descending coverage:
  doi-resolution-index live_urls   blog / registry / repo / datacite, joined on axn
  medium RSS seed                  10 items per author (Medium's feed cap)
  academia.edu                     presence known from the author's profile;
                                   URLs not yet collected, recorded as gaps

Every mirror records its source and join method, so any tier can be discarded.
Entries with url=null are emitted deliberately: a known-but-unlinked mirror is
a collection task, and silently dropping it would hide the work still to do.

Usage: python3 scripts/build_mirror_map.py [--medium-seed PATH] [--dry-run]
"""
import json, re, argparse, datetime, collections, os

REGISTRY = 'data/registry.json'
DOIIDX = 'data/doi-resolution-index.json'
OUT = 'data/mirror-map.json'


# The resolution index tiers its own axn assignments; inheriting them without
# recording the tier imports its uncertainty silently. Observed effect before
# this was added: deposit #42 acquired a blog URL belonging to a different
# work, because a fuzzy row shared its hex. Confidence is therefore carried per
# mirror, two classes are excluded outright, and only `high` is marked safe for
# automatic sameAs emission.
MAPPING_CONFIDENCE = {
    'direct_verified': 'high',
    'direct': 'high',
    'title_match_repoint': 'medium',
    'remediated_containment': 'medium',
    'superseded_version_pointer': 'medium',
    'phase4_mint': 'medium',
    'remediated_fuzzy': 'low',
    'remediated_ambiguous_earliest': 'low',
    'registry_referenced': 'low',
    'provisional_related_work_high': 'low',
    'provisional_related_work_medium': 'low',
    'provisional_related_work_low': 'low',
    'provisional_family_sibling': 'low',
}
MAPPING_EXCLUDE = {'misclassified_other_author', 'no_alexanarch_equivalent'}

HEX = re.compile(r'AXN:([0-9A-Fa-f]{4})')

PLATFORM = {
    'blog': ('mindcontrolpoems.blogspot.com', 'Blog — often the most-recently-'
             'overwritten copy, since the author revised in place rather than '
             'posting successive versions'),
    'registry': ('machinemediation.org', 'Sovereign registry anchor (MM-CHA)'),
    'repo': ('github.com', 'Source repository'),
    'datacite': ('datacite.org', 'Registry metadata record'),
}


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def build(medium_seed=None):
    reg = load(REGISTRY)
    deps = reg['deposits']
    by_hex, by_num = {}, {}
    for d in deps:
        by_num[d['deposit_number']] = d
        m = HEX.match(str(d.get('axn', '')))
        if m:
            by_hex.setdefault(m.group(1).upper(), d)

    mirrors = collections.defaultdict(list)
    stats = collections.Counter()

    # 1. resolution-index live_urls, joined on axn
    for row in load(DOIIDX).get('mappings', []):
        mtype = row.get('mapping_type')
        if mtype in MAPPING_EXCLUDE:
            stats[f'excluded/{mtype}'] += 1
            continue
        axn = row.get('axn') or ''
        m = HEX.match(axn)
        if not m:
            continue
        d = by_hex.get(m.group(1).upper())
        if not d:
            continue
        conf = MAPPING_CONFIDENCE.get(mtype, 'low')
        for kind, url in (row.get('live_urls') or {}).items():
            if not url:
                continue
            host, note = PLATFORM.get(kind, (kind, ''))
            rec = {'platform': kind, 'host': host, 'url': url,
                   'source': 'doi-resolution-index', 'join': 'axn',
                   'mapping_type': mtype, 'confidence': conf,
                   'safe_for_sameas': conf == 'high',
                   'dead_doi': row.get('dead_doi'), 'note': note}
            if rec not in mirrors[d['deposit_number']]:
                mirrors[d['deposit_number']].append(rec)
                stats[f'{kind}/{conf}'] += 1

    # 2. medium seed, joined on title similarity (recorded per row)
    if medium_seed and os.path.exists(medium_seed):
        import difflib
        titles = [(d['deposit_number'], str(d.get('title', '')).lower()) for d in deps]
        for r in load(medium_seed).get('mirrors', []):
            t = re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', r['title'].lower())).strip()
            best, bn = 0.0, None
            for n, dt in titles:
                dtl = re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', dt)).strip()
                if not dtl:
                    continue
                s = difflib.SequenceMatcher(None, t[:90], dtl[:90]).ratio()
                if t[:40] and t[:40] in dtl:
                    s = max(s, 0.93)
                if s > best:
                    best, bn = s, n
            if bn and best >= 0.72:
                conf = 'high' if best >= 0.90 else 'medium'
                rec = {'platform': 'medium', 'host': 'medium.com', 'url': r['url'],
                       'source': 'medium-rss', 'join': f'title~{best:.2f}',
                       'confidence': conf, 'safe_for_sameas': conf == 'high',
                       'handle': r.get('handle'), 'published': r.get('date')}
                if rec not in mirrors[bn]:
                    mirrors[bn].append(rec)
                    stats[f'medium/{conf}'] += 1
            else:
                stats['medium/unmatched'] += 1

    rows = []
    for n in sorted(mirrors):
        d = by_num[n]
        rows.append({
            'deposit_number': n,
            'axn': d.get('axn'),
            'title': d.get('title'),
            'record_url': f'https://www.alexanarch.org/s/records/{n}/',
            'mirrors': mirrors[n],
        })

    covered = len(rows)
    return {
        '$schema': 'https://www.alexanarch.org/data/mirror-map.schema.json',
        'name': 'Mirror Map — off-archive copies, for entity consolidation',
        'description': (
            'Every known copy of each deposit hosted outside this archive. Its '
            'purpose is sameAs emission: mirrors on Medium, Blogger and '
            'Academia.edu cannot be made to carry rel=canonical, but the archive '
            'can declare from its own pages that those copies are the same work, '
            'which consolidates the entity graph toward the declaring page. '
            'Built because a 2026-07-26 capture showed composed answers citing '
            'scilynk, Medium and Academia.edu for six documents all deposited '
            'here: the archive was losing not to strangers but to its own '
            'distribution copies. Each mirror records its source and join method '
            'so any tier can be discarded; known-but-unlinked mirrors are '
            'emitted with url=null rather than dropped, because a missing URL is '
            'a collection task and hiding it would hide the work.'),
        'generated_by': 'scripts/build_mirror_map.py',
        'generated_at': datetime.datetime.now(datetime.timezone.utc)
                        .isoformat(timespec='seconds').replace('+00:00', 'Z'),
        'totals': {
            'deposits': len(deps),
            'deposits_with_mirrors': covered,
            'coverage': round(covered / len(deps), 4),
            'mirror_links': sum(len(r['mirrors']) for r in rows),
            'safe_for_sameas': sum(1 for r in rows for x in r['mirrors']
                                   if x.get('safe_for_sameas')),
            'works_with_a_safe_mirror': sum(1 for r in rows if any(
                x.get('safe_for_sameas') for x in r['mirrors'])),
        },
        'source_counts': dict(stats),
        'confidence_note': (
            'The resolution index tiers its own axn assignments and this map '
            'carries those tiers rather than flattening them. Only mapping types '
            'direct_verified and direct are marked safe_for_sameas; fuzzy, '
            'containment and provisional rows are retained for inspection but '
            'must not be emitted automatically. Two classes are excluded '
            'outright: misclassified_other_author and no_alexanarch_equivalent.'),
        'known_gaps': {
            'academia.edu': ('Roughly 150 papers are present on the author profile; '
                             'URLs not yet collected. Academia.edu is outside the '
                             'build environment egress allowlist, so links must be '
                             'exported from the profile and joined by title.'),
            'medium': ('Medium caps its RSS feed at 10 items per author and blocks '
                       '/archive and ?format=json; its sitemap is partitioned by post '
                       'date rather than by user. Full enumeration requires an export '
                       'from the author\'s own Stories page.'),
            'substack': 'Present but rarely retrieved; not yet enumerated.',
        },
        'works': rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--medium-seed', default=None)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    p = build(a.medium_seed)
    t = p['totals']
    print(f"deposits_with_mirrors={t['deposits_with_mirrors']}/{t['deposits']} "
          f"({100*t['coverage']:.0f}%)  mirror_links={t['mirror_links']}")
    for k, v in sorted(p['source_counts'].items()):
        print(f"   {k:22s} {v}")
    if a.dry_run:
        print('[dry-run] no write')
        return
    json.dump(p, open(OUT, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print(f'[ok] wrote {OUT}')


if __name__ == '__main__':
    main()
