#!/usr/bin/env python3
"""
resolve_capture_links.py — build data/capture-deposit-links.json

EA-RETRIEVAL-DENSITY-01, Task 7. The Capture Registry (EA-WG-CAPTURES-01,
authored on machinemediation.org) and the deposit registry describe the same
objects with no edges between them: every capture-derived semantic address
carries refers_to = [], so all 198 of them classify as "unmatched". This
script computes the join.

Resolution ladder, highest confidence first. Each link records the method
that produced it so the map is auditable and any tier can be discarded.

  hard/axn      an AXN:XXXX string appears in the capture entry
  hard/doi      a Zenodo DOI appears; resolved via doi-resolution-index axn
  hard/series   an EA-*-NN series identifier appears and matches a deposit
  soft/title    the capture query appears verbatim inside a deposit title
  soft/keyword  the capture query matches a deposit keyword exactly

Deposit-number mentions (#1234) are deliberately NOT used: capture entries
cite their own registry numbers, footnotes, and page counts in the same form,
and the false-positive rate is unacceptable for a provenance instrument.

Usage:
  python3 scripts/resolve_capture_links.py [--captures PATH] [--dry-run]
"""
import json, re, os, argparse, hashlib, datetime

CAPTURES = 'data/EA-WG-CAPTURES-01.json'
REGISTRY = 'data/registry.json'
DOIINDEX = 'data/doi-resolution-index.json'
OUT = 'data/capture-deposit-links.json'

MIN_QUERY_LEN = 8          # below this, title substring matching is noise
MAX_SOFT_LINKS = 6
MAX_BODY_LINKS = 4         # body matching is the loosest tier; keep fan-out tight         # a query matching more than this is too generic


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


_BODIES = None


def _bodies(deps):
    """deposit_number -> lowercased body text. Loaded once (~39MB)."""
    global _BODIES
    if _BODIES is not None:
        return _BODIES
    out = []
    for d in deps:
        p = str(d.get('full_text_path') or '').lstrip('/')
        if not p or not os.path.exists(p) or not p.endswith('.md'):
            continue
        try:
            out.append((d['deposit_number'],
                        open(p, encoding='utf-8', errors='replace').read().lower()))
        except Exception:
            continue
    _BODIES = out
    return out


def build():
    caps = load(CAPTURES)
    reg = load(REGISTRY)
    deps = reg['deposits']

    by_axn, by_hex, by_num = {}, {}, {}
    titles, keywords, descs, series = [], [], [], {}
    for d in deps:
        n = d['deposit_number']
        by_num[n] = d
        a = str(d.get('axn') or '')
        if a:
            by_axn[a] = n
            m = re.match(r'AXN:([0-9A-Fa-f]{4})', a)
            if m:
                by_hex[m.group(1).upper()] = n
        t = str(d.get('title') or '').strip()
        if t:
            titles.append((n, t.lower()))
        for k in (d.get('keywords') or []):
            if isinstance(k, str) and len(k) >= MIN_QUERY_LEN:
                keywords.append((n, k.lower().strip()))
        desc = str(d.get('description') or '').strip()
        if desc:
            descs.append((n, desc.lower()))
        sid = d.get('series_id')
        if sid:
            series.setdefault(str(sid).upper(), n)
        ms = re.search(r'\b(EA-[A-Z]{2,10}-\d{2})\b', t)
        if ms:
            series.setdefault(ms.group(1).upper(), n)

    # DOI -> deposit, via the resolution index's axn join
    doi2dep = {}
    dep_doi_status = {}
    if os.path.exists(DOIINDEX):
        for row in load(DOIINDEX).get('mappings', []):
            axn, doi = row.get('axn'), row.get('dead_doi')
            if not (axn and doi):
                continue
            n = by_axn.get(axn)
            if n is None:
                m = re.match(r'AXN:([0-9A-Fa-f]{4})', axn)
                if m:
                    n = by_hex.get(m.group(1).upper())
            if n is not None:
                doi2dep[doi] = n
                st = row.get('status')
                rec = dep_doi_status.setdefault(n, {'dois': [], 'statuses': []})
                if doi not in rec['dois']:
                    rec['dois'].append(doi)
                if st and st not in rec['statuses']:
                    rec['statuses'].append(st)

    links, stats = {}, {'hard/axn': 0, 'hard/doi': 0, 'hard/series': 0,
                        'soft/title': 0, 'soft/keyword': 0,
                        'soft/description': 0, 'soft/body': 0}
    unresolved = []

    for e in caps.get('entries', []):
        slug = e.get('slug')
        if not slug:
            continue
        blob = json.dumps(e, ensure_ascii=False)
        found = {}   # deposit_number -> (method, evidence)

        for m in re.finditer(r'AXN:[0-9A-Fa-f]{4}', blob):
            n = by_hex.get(m.group(0)[4:].upper())
            if n is not None:
                found.setdefault(n, ('hard/axn', m.group(0)))

        for m in re.finditer(r'10\.5281/zenodo\.\d+', blob):
            n = doi2dep.get(m.group(0))
            if n is not None:
                found.setdefault(n, ('hard/doi', m.group(0)))

        for m in re.finditer(r'\b(EA-[A-Z]{2,10}-\d{2})\b', blob):
            n = series.get(m.group(1).upper())
            if n is not None:
                found.setdefault(n, ('hard/series', m.group(1)))

        q = (e.get('q') or '').strip().strip('"').strip().lower()
        if len(q) >= MIN_QUERY_LEN:
            tmatch = [n for n, t in titles if q in t]
            if 0 < len(tmatch) <= MAX_SOFT_LINKS:
                for n in tmatch:
                    found.setdefault(n, ('soft/title', q))
            kmatch = [n for n, k in keywords if q == k]
            if 0 < len(kmatch) <= MAX_SOFT_LINKS:
                for n in kmatch:
                    found.setdefault(n, ('soft/keyword', q))
            if not found and len(q) >= 12:
                dmatch = [n for n, s in descs if q in s]
                if 0 < len(dmatch) <= MAX_SOFT_LINKS:
                    for n in dmatch:
                        found.setdefault(n, ('soft/description', q))
            # Last tier: exact phrase in body text. Many captures test coined
            # terms that appear in prose and never in a title. Requires a
            # longer phrase and a tighter fan-out cap, since body matching is
            # the loosest evidence in the ladder.
            if not found and len(q) >= 14:
                bmatch = [n for n, b in _bodies(deps) if q in b]
                if 0 < len(bmatch) <= MAX_BODY_LINKS:
                    for n in bmatch:
                        found.setdefault(n, ('soft/body', q))

        if not found:
            unresolved.append({'slug': slug, 'q': e.get('q'), 'date': e.get('date')})
            continue

        PRIORITY = {'hard/series': 0, 'soft/title': 1, 'hard/axn': 2,
                    'soft/keyword': 3, 'soft/description': 4, 'soft/body': 5,
                    'hard/doi': 6}
        best = min(found.items(), key=lambda kv: (PRIORITY.get(kv[1][0], 9),
                                                  -len(str(kv[1][1])), kv[0]))[0]
        entries = []
        for n, (method, ev) in sorted(found.items()):
            d = by_num[n]
            entries.append({
                'deposit_number': n,
                'axn': d.get('axn'),
                'title': d.get('title'),
                'record_url': f"https://www.alexanarch.org/s/records/{n}/",
                'method': method,
                'evidence': ev,
                'primary': (n == best),
                'doi_status': dep_doi_status.get(n),
            })
            stats[method] += 1
        links[slug] = {
            'query': e.get('q'),
            'date': e.get('date'),
            'section': e.get('s'),
            'match_type': e.get('mt'),
            'deposits': entries,
        }

    # How many captures land on works whose DOI was severed? This is the join
    # that makes tombstone-vs-live competition measurable as a rate rather
    # than case by case.
    severance = {'captures_on_severed_works': 0, 'captures_on_unsevered_works': 0,
                 'captures_with_no_doi_record': 0, 'status_counts': {}}
    for v in links.values():
        prim = next((x for x in v['deposits'] if x['primary']), None)
        ds = (prim or {}).get('doi_status')
        if not ds:
            severance['captures_with_no_doi_record'] += 1
            continue
        sts = ds.get('statuses') or []
        for s in sts:
            severance['status_counts'][s] = severance['status_counts'].get(s, 0) + 1
        if any('410' in str(s) or 'GONE' in str(s).upper() or 'SEVER' in str(s).upper()
               for s in sts):
            severance['captures_on_severed_works'] += 1
        else:
            severance['captures_on_unsevered_works'] += 1

    total = len(caps.get('entries', []))
    payload = {
        '$schema': 'https://www.alexanarch.org/data/capture-deposit-links.schema.json',
        'name': 'Capture \u2194 Deposit Link Map',
        'description': ('Edges between EA-WG-CAPTURES-01 (the AI Overview / AI Mode '
                        'Capture Registry, authored at machinemediation.org) and the '
                        'Alexanarch deposit corpus. Produced by '
                        'scripts/resolve_capture_links.py. Each edge records the '
                        'resolution method so any confidence tier can be discarded. '
                        'An edge asserts that the capture entry references, or its query '
                        'matches, the deposit \u2014 not that the deposit is the capture\'s '
                        'sole subject; exactly one edge per capture is marked primary, '
                        'ranked by evidence of aboutness rather than by identifier '
                        'hardness (a DOI can be cited in passing). '
                        'Deposit-number mentions are deliberately excluded as '
                        'unsafe. Unresolved captures are enumerated rather than '
                        'silently dropped.'),
        'generated_by': 'scripts/resolve_capture_links.py',
        'generated_at': datetime.datetime.now(datetime.timezone.utc)
                        .isoformat(timespec='seconds').replace('+00:00', 'Z'),
        'captures_source': {
            'file': CAPTURES,
            'version': caps.get('version'),
            'date': caps.get('date'),
            'total_captures': caps.get('total_captures'),
            'canonical_home': 'https://www.machinemediation.org/data/registry.json',
            'sha256': hashlib.sha256(open(CAPTURES, 'rb').read()).hexdigest(),
        },
        'totals': {
            'captures': total,
            'captures_linked': len(links),
            'captures_unresolved': len(unresolved),
            'link_rate': round(len(links) / total, 4) if total else 0,
            'edges': sum(len(v['deposits']) for v in links.values()),
        },
        'method_counts': stats,
        'severance_rollup': severance,
        'links': links,
        'unresolved': unresolved,
    }
    return payload


def main():
    # `global` must precede every read of the name in this scope. A withdrawal
    # guard added on 2026-08-12 was inserted ABOVE it and read CAPTURES.exists(),
    # which made the whole module a SyntaxError — so the resolver had not run
    # since. Retired 2026-08-13 on reseating: data/EA-WG-CAPTURES-01.json is live
    # again, generated from the rebuild, with analyst prose and machine text held
    # in separate fields.
    global CAPTURES
    ap = argparse.ArgumentParser()
    ap.add_argument('--captures', default=None)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if a.captures:
        CAPTURES = a.captures
    p = build()
    t, m = p['totals'], p['method_counts']
    print(f"captures={t['captures']}  linked={t['captures_linked']} "
          f"({100*t['link_rate']:.0f}%)  edges={t['edges']}  "
          f"unresolved={t['captures_unresolved']}")
    for k, v in m.items():
        print(f"   {k:14s} {v}")
    if a.dry_run:
        print('[dry-run] no write')
        return
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(p, fh, indent=2, ensure_ascii=False)
    print(f"[ok] wrote {OUT}")


if __name__ == '__main__':
    main()
