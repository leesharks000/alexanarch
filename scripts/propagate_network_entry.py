#!/usr/bin/env python3
"""propagate_network_entry.py - add a domain to every fleet site's network bloc.

WHY THIS EXISTS
data/fleet-domains.json is the declared source of the fleet, and every site carries
its own hand-typed copy of the network list in its footer. Adding axnidentifiers.org
to the source and to alexanarch's bloc changed alexanarch and nothing else; an audit
found EIGHTEEN sites serving a stale list, none of which could report that it was
stale, because nothing compares a footer to the source.

This is the same failure as the capture links: a value stored once and copied by
hand into eighteen places. The copies are not wrong when written; they rot in place.

This script edits each site's repository through the GitHub contents API, inserting
the entry in the Archive group ahead of persistentidentifiers.org, per MANUS's
ruling that identifier infrastructure leads the Archive group rather than sitting
mid-list under Framework Sites.

Usage:
    python3 scripts/propagate_network_entry.py --dry-run
    python3 scripts/propagate_network_entry.py --apply
"""
import argparse, base64, json, re, subprocess, sys, urllib.request

ENTRY_DOMAIN = "axnidentifiers.org"
ANCHOR_DOMAIN = "persistentidentifiers.org"

REPOS = {
    "leesharks.com": "leesharks.com",
    "godkinggoogle.com": "godkinggoogle",
    "laborvector.org": "laborvector",
    "restoredacademy.org": "restoredacademy",
    "surfacemap.org": "surface-map",
    "vpcor.org": "vpcor-org",
    "traininglayerliterature.org": "traininglayerliterature-org",
    "semanticphysics.org": "semanticphysics-site",
    "watergiraffe.org": "watergiraffe-org",
    "revelationfirst.com": "revelationfirst-com",
    "spxi.dev": "spxi-dev",
    "chatgptpsychosis.org": "chatgptpsychosis-site",
    "metadatapacket.dev": "metadatapacket-dev",
}


def token():
    u = subprocess.run(["git", "remote", "get-url", "origin"],
                       capture_output=True, text=True).stdout
    return u.split("x-access-token:")[1].split("@")[0]


def api(url, pat, data=None, method=None):
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {pat}",
                                          "Accept": "application/vnd.github+json",
                                          "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=45))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    pat = token()
    done = skipped = failed = 0

    for domain, repo in REPOS.items():
        try:
            f = api(f"https://api.github.com/repos/leesharks000/{repo}/contents/index.html", pat)
            html = base64.b64decode(f["content"]).decode("utf-8", "replace")
        except Exception as e:
            print(f"  {domain:<30} could not read index.html ({e})", file=sys.stderr)
            failed += 1
            continue

        if ENTRY_DOMAIN in html:
            print(f"  {domain:<30} already present")
            skipped += 1
            continue

        m = re.search(r'<div><a href="https://' + re.escape(ANCHOR_DOMAIN) +
                      r'"[^>]*>[^<]*</a></div>', html)
        if not m:
            m = re.search(r'<li><a href="https://' + re.escape(ANCHOR_DOMAIN) +
                          r'/?"[^>]*>[^<]*</a></li>', html)
        if not m:
            print(f"  {domain:<30} no anchor found; markup differs, left alone")
            skipped += 1
            continue

        anchor = m.group(0)
        if anchor.startswith("<li>"):
            entry = f'<li><a href="https://{ENTRY_DOMAIN}/" rel="noopener">{ENTRY_DOMAIN}</a></li>'
        else:
            entry = f'<div><a href="https://{ENTRY_DOMAIN}">{ENTRY_DOMAIN}</a></div>'
        new = html.replace(anchor, entry + "\n" + anchor, 1)

        if not a.apply:
            print(f"  {domain:<30} WOULD ADD (anchor: {anchor[:44]}...)")
            done += 1
            continue

        payload = {
            "message": (f"Add {ENTRY_DOMAIN} to the network bloc. The fleet list is "
                        f"hand-copied into every site, so adding the domain to "
                        f"data/fleet-domains.json and to alexanarch's own footer left "
                        f"eighteen sites serving a stale list with nothing able to report "
                        f"it. Seated first in the Archive group per MANUS: identifier "
                        f"infrastructure leads, so a reader meets it before the rest."),
            "content": base64.b64encode(new.encode()).decode(),
            "sha": f["sha"],
        }
        try:
            r = api(f"https://api.github.com/repos/leesharks000/{repo}/contents/index.html",
                    pat, data=json.dumps(payload).encode(), method="PUT")
            print(f"  {domain:<30} added · {r['commit']['sha'][:8]}")
            done += 1
        except Exception as e:
            print(f"  {domain:<30} write failed ({e})", file=sys.stderr)
            failed += 1

    print(f"\n{'applied' if a.apply else 'dry run'}: {done} changed · "
          f"{skipped} skipped · {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
