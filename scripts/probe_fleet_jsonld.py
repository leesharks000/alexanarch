#!/usr/bin/env python3
"""probe_fleet_jsonld.py — weekly guard for the fleet's structured data (2026-09-04).

For every fleet host, fetch the root and up to N pages from its sitemap and check, live:
  - every <script type="application/ld+json"> block parses
  - every Dataset node carries name, description, license, creator
  - Dataset.citation objects are CreativeWork; Dataset.isPartOf is Dataset/DataCatalog
  - no <span data-count=…> inside a JSON block (the 2026-09-04 count-injection fault)
Writes data/probes/fleet-jsonld/YYYY-MM-DD.json. Never mutates anything. Exit 1 if any fault.
"""
import json, re, sys, urllib.request, datetime, pathlib, socket
socket.setdefaulttimeout(20)
ROOT = pathlib.Path(__file__).resolve().parent.parent
HOSTS = ["www.alexanarch.org","www.crimsonhexagonal.org","www.leesharks.com","www.holographickernel.org","www.livingarchitecturelab.org",
 "www.pessoagraph.org","www.secretbookofwalt.org","www.semanticeconomy.org","www.semanticphysics.org","www.spxi.dev","www.surfacemap.org",
 "www.axnidentifiers.org","www.chatgptpsychosis.org","www.laborvector.org","www.lagrangeobservatory.org","www.machinemediation.org",
 "www.maryleelabor.org","www.metadatapacket.dev","www.operativesemiotics.org","www.persistentidentifiers.org","www.provenanceerasure.org",
 "www.restoredacademy.com","www.revelationfirst.com","www.themandalaoracle.com","www.traininglayerliterature.org","www.vpcor.org",
 "www.watergiraffe.org","www.godkinggoogle.com"]
N = 4
UA = "alexanarch-fleet-jsonld-probe/1.0 (+https://www.alexanarch.org/)"

def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=20) as r: return r.read().decode('utf-8','replace')

def check_page(html):
    faults = []
    for b in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        if '<span data-count=' in b: faults.append("count-span inside JSON-LD")
        try: j = json.loads(b)
        except Exception as e: faults.append(f"unparsable JSON-LD: {str(e)[:50]}"); continue
        st = [j]
        while st:
            o = st.pop()
            if isinstance(o, dict):
                t = o.get('@type'); ts = t if isinstance(t, list) else [t]
                if 'Dataset' in ts:
                    miss = [k for k in ('name','description','license','creator') if not o.get(k)]
                    if miss: faults.append(f"Dataset '{str(o.get('name'))[:40]}' missing {miss}")
                    c = o.get('citation')
                    if isinstance(c, dict) and c.get('@type') != 'CreativeWork': faults.append("Dataset.citation not CreativeWork")
                    ip = o.get('isPartOf')
                    if isinstance(ip, dict) and ip.get('@type') not in ('Dataset','DataCatalog'): faults.append("Dataset.isPartOf wrong type")
                st.extend(o.values())
            elif isinstance(o, list): st.extend(o)
    return faults

def main():
    today = datetime.date.today().isoformat(); out = {"date": today, "hosts": {}}; total = 0
    for h in HOSTS:
        urls = [f"https://{h}/"]
        try:
            locs = re.findall(r'<loc>([^<]+)</loc>', get(f"https://{h}/sitemap.xml"))
            urls += [u for u in locs if u.rstrip('/') != f"https://{h}"][:N]
        except Exception as e: out["hosts"][h] = {"error": f"sitemap: {str(e)[:60]}"}
        res = {}
        for u in urls:
            try: f = check_page(get(u))
            except Exception as e: f = [f"fetch: {str(e)[:60]}"]
            if f: res[u] = f; total += len(f)
        out["hosts"][h] = res or "clean"
        print(f"{h:34} {'clean' if not res else str(len(res))+' page(s) with faults'}")
    d = ROOT/'data/probes/fleet-jsonld'; d.mkdir(parents=True, exist_ok=True)
    (d/f"{today}.json").write_text(json.dumps(out, indent=1)); (d/"latest.json").write_text(json.dumps(out, indent=1))
    print("faults:", total); return 1 if total else 0

if __name__ == '__main__': sys.exit(main())
