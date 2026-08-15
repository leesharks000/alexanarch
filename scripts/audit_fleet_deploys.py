#!/usr/bin/env python3
"""Fleet deploy audit: is production behind main, and did the webhook fire?

WHY THIS EXISTS. On 2026-08-15 the operator noticed a heteronym on a live page
who had been relocated weeks earlier. The repo was correct; the DEPLOYMENT was
five commits stale. A fleet-wide check then found SIX live sites serving builds
that predated their own fixes -- grid repointing, favicons, page faults already
committed and never served -- and nothing anywhere reported it. The webhooks
were alive; individual pushes had simply dropped, silently, and the only
detector in the system was someone looking at a page.

A fleet that deploys on push has no way to notice when a push does not deploy.
This is that way. Run it after any batch of fleet commits.

Vercel registers a GitHub Deployment for every build it makes, so GitHub itself
knows the last commit that deployed. Comparing that against the branch head
detects both failure modes in one pass:
  BEHIND  — commits landed on main and produced no deployment (webhook drop)
  NEVER   — repo has no deployments at all (never linked, or link removed)
"""
import json, subprocess, sys, urllib.request, urllib.error

TOKEN = open('/home/claude/.secrets/gh').read().strip()
OWNER = 'leesharks000'

def api(path):
    req = urllib.request.Request(f'https://api.github.com{path}',
                                 headers={'Authorization': f'token {TOKEN}',
                                          'Accept': 'application/vnd.github+json'})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {'_error': e.code}
    except Exception as e:
        return {'_error': str(e)[:40]}

repos = []
page = 1
while page <= 2:
    d = api(f'/user/repos?per_page=100&page={page}&affiliation=owner')
    if not isinstance(d, list) or not d: break
    repos += [r['name'] for r in d if not r.get('archived')]
    page += 1

rows = []
for name in sorted(repos):
    br = api(f'/repos/{OWNER}/{name}/branches/main')
    if '_error' in br:
        br = api(f'/repos/{OWNER}/{name}/branches/master')
    head = br.get('commit', {}).get('sha', '')[:7] if 'commit' in br else None
    if not head:
        continue
    deps = api(f'/repos/{OWNER}/{name}/deployments?per_page=5')
    if not isinstance(deps, list):
        rows.append((name, head, None, 'API-ERR', 0)); continue
    if not deps:
        rows.append((name, head, None, 'NEVER', 0)); continue
    dsha = deps[0].get('sha', '')[:7]
    if dsha == head:
        rows.append((name, head, dsha, 'CURRENT', 0))
    else:
        cmp_ = api(f'/repos/{OWNER}/{name}/compare/{dsha}...{head}')
        behind = cmp_.get('ahead_by', '?') if isinstance(cmp_, dict) else '?'
        rows.append((name, head, dsha, 'BEHIND', behind))

print(f"{'repo':<32}{'head':<9}{'deployed':<10}{'status':<9}{'behind':>7}")
print('-'*70)
for n, h, d, s, b in rows:
    mark = '  ' if s == 'CURRENT' else '! '
    print(f"{mark}{n:<30}{h:<9}{(d or '-'):<10}{s:<9}{(b if b else ''):>7}")
bad = [r for r in rows if r[3] != 'CURRENT']
print(f"\n{len(rows)} repos checked · {len(rows)-len(bad)} current · {len(bad)} need attention")
