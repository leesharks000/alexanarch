#!/usr/bin/env python3
"""
verify.py — re-probe every fixture case and report agreement.

Run this before relying on the fixture. Identifier state drifts: between
2026-07-12 and 2026-07-28, two identifiers recorded as registered had become
tombstoned and one had lost its registration. A fixture that assumes static
state will rot.

The landing host returns 503 intermittently and 403 to some user agents.
Requests retry past 503; results are best-effort rather than authoritative,
and 503/None outcomes are reported separately rather than folded into
disagreement.

Usage: python3 verify.py [--cases cases.json] [--json report.json]
"""
import json, time, argparse, collections, urllib.request, urllib.error

EXPECTED = {
    'verified_tombstone': {'410'},
    'verified_registered': {'200'},
    'verified_erased_registration': {'404', '410'},   # class known unreliable; both observed
    'fragment_candidate': {'404'},
    'syntactically_valid_unverified': set(),          # no expectation asserted
}


def probe(doi, tries=3, pause=3):
    for i in range(tries):
        try:
            req = urllib.request.Request('https://doi.org/' + doi,
                                         headers={'User-Agent': 'curl/8.0 deletion-fixture-verify'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return str(r.status)
        except urllib.error.HTTPError as e:
            if e.code == 503 and i < tries - 1:
                time.sleep(pause); continue
            return str(e.code)
        except Exception:
            if i < tries - 1:
                time.sleep(pause); continue
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cases', default='cases.json')
    ap.add_argument('--json')
    a = ap.parse_args()

    data = json.load(open(a.cases, encoding='utf-8'))
    cases = data['cases']
    print('probing %d cases\n' % len(cases))

    agree = disagree = inconclusive = 0
    byclass = collections.defaultdict(collections.Counter)
    out = []
    for c in cases:
        obs = probe(c['identifier'])
        rec = c['recorded']['identifier_validity']
        exp = EXPECTED.get(rec, set())
        if obs in (None, '503'):
            verdict = 'INCONCLUSIVE'; inconclusive += 1
        elif not exp:
            verdict = 'NO EXPECTATION'
        elif obs in exp:
            verdict = 'agree'; agree += 1
        else:
            verdict = 'DISAGREE'; disagree += 1
        byclass[c['case_class']][obs] += 1
        was = c.get('observed_2026_07_28')
        drift = '' if (was is None or was == obs) else '   DRIFT since 2026-07-28: %s -> %s' % (was, obs)
        if verdict in ('DISAGREE', 'INCONCLUSIVE') or drift:
            print('  [%-14s] %-26s recorded=%-30s observed=%s%s'
                  % (verdict, c['identifier'], rec, obs, drift))
        out.append(dict(c, observed_now=obs, verdict=verdict))

    print('\nagree %d | disagree %d | inconclusive %d' % (agree, disagree, inconclusive))
    print('\nby case class:')
    for k, v in byclass.items():
        print('  %-40s %s' % (k, ', '.join('%s:%d' % (s, n) for s, n in sorted(v.items(), key=lambda x: -x[1]))))
    if disagree:
        print('\nDisagreement is expected in registration_erased, which is documented as unreliable.')
        print('Disagreement elsewhere means state has drifted and the fixture needs re-dating.')
    if a.json:
        json.dump({'probed_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                   'agree': agree, 'disagree': disagree, 'inconclusive': inconclusive,
                   'cases': out}, open(a.json, 'w'), indent=1, ensure_ascii=False)
        print('\n[ok] wrote %s' % a.json)


if __name__ == '__main__':
    main()
