#!/usr/bin/env python3
"""reprobe_live.py — OPTIONAL live integration probe. Emits a dated
observation report; NEVER mutates the fixture's expected results.

Live re-probing consumes external services (doi.org, api.datacite.org,
alexanarch.org). Requests are serialized with delays and retried past 503.
Respect the providers' rate limits. The committed cases.json is the
deterministic artifact — conformance testing does not require this script.

Routing is by identifier_kind:
  doi / doi_shaped_string -> HEAD https://doi.org/<id>
  archive_record          -> HEAD <id>
  declared_path / state_change_claim -> skipped (repository-evidence cases)
Divergence cases additionally GET the DataCite record and parse
attributes.state with a UTC timestamp.

The verified_erased_registration class is reported as an observed
DISTRIBUTION against its recorded state, not pass/fail: the ~even 404/410
split is the finding the class exists to preserve.

License: MIT.
"""
import json, time, datetime, argparse, collections, urllib.request, urllib.error
from pathlib import Path

FIX = Path(__file__).resolve().parent
EXPECT = {'verified_tombstone': {'410'}, 'verified_registered': {'200'}, 'fragment_candidate': {'404'}}

def head(url, tries=3):
    code = None
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'alexanarch-fixture/2.1'}, method='HEAD'), timeout=20)
            code = str(r.status); break
        except urllib.error.HTTPError as e:
            code = str(e.code)
            if code != '503': break
            time.sleep(2.5)
        except Exception:
            code = None
    time.sleep(0.4)
    return code

def dc_get(doi):
    try:
        r = urllib.request.urlopen(urllib.request.Request(f'https://api.datacite.org/dois/{doi}',
            headers={'User-Agent': 'alexanarch-fixture/2.1', 'Accept': 'application/vnd.api+json'}), timeout=25)
        b = json.loads(r.read().decode('utf-8', 'replace'))
        return {'http': str(r.status), 'state': ((b.get('data') or {}).get('attributes') or {}).get('state'),
                'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    except urllib.error.HTTPError as e:
        return {'http': str(e.code), 'state': None,
                'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    except Exception:
        return {'http': None, 'state': None, 'retrieved_utc': None}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', help='write full observation report here')
    a = ap.parse_args()
    c = json.load(open(FIX / 'cases.json'))
    report = {'fixture_version': c['version'],
              'run_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'observations': []}
    dist = collections.defaultdict(collections.Counter)
    agree = disagree = skipped = 0
    for x in c['cases']:
        kind = x['identifier_kind']
        if kind in ('declared_path', 'state_change_claim'):
            skipped += 1; continue
        url = f"https://doi.org/{x['identifier']}" if kind in ('doi', 'doi_shaped_string') else x['identifier']
        code = head(url)
        obs = {'identifier': x['identifier'], 'case_class': x['case_class'], 'observed': code}
        iv = (x.get('recorded') or {}).get('identifier_validity')
        if iv == 'verified_erased_registration':
            dist[iv][code] += 1
        elif iv in EXPECT and code:
            if code in EXPECT[iv]: agree += 1
            else: disagree += 1; obs['disagreement'] = f"recorded {iv}, observed {code}"
        if x['case_class'] == 'registry_resolution_divergence':
            obs['datacite'] = dc_get(x['identifier'])
        report['observations'].append(obs)
    report['summary'] = {'agree': agree, 'disagree': disagree, 'skipped_local': skipped,
                         'erased_class_distribution': {k: dict(v) for k, v in dist.items()}}
    print(json.dumps(report['summary'], indent=1))
    if a.json:
        json.dump(report, open(a.json, 'w'), indent=1)
        print("report ->", a.json)

if __name__ == '__main__':
    main()
