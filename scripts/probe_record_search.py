#!/usr/bin/env python3
"""probe_record_search.py — the record-visibility cohort probe (WS0 of ASSEMBLY-WORKPLAN-RECORD-VISIBILITY).

For each of twenty records: (1) exact-URL fetch of /s/records/N/ — status, canonical, bytes;
(2) an exact-title web search through a public HTML results page (DuckDuckGo html endpoint,
Bing-backed, which also proxies the index ChatGPT search retrieves from) — the top results,
whether the record's own page appears and at what rank, and which alexanarch or fleet URL
appears if the record itself does not. Writes a dated JSON under data/probes/record-search/
and never mutates any expectation. Stdlib only. Run weekly by workflow; also by hand.
"""
import json, re, sys, time, html, urllib.request, urllib.parse, datetime, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT/'data/probes/record-search'
COHORT = {"pre_june_legacy":[27,311,500,560,761],"mid":[879,1038,1087,1204,1400],
          "recent":[1500,1546,1552,1574,1576],"strong_duplicates":[24,1,1079,1496,1187]}
UA = "Mozilla/5.0 (X11; Linux x86_64) alexanarch-record-probe/1.0 (+https://www.alexanarch.org/)"
OWN = ("alexanarch.org","provenanceerasure.org","machinemediation.org","semanticeconomy.org","operativesemiotics.org",
       "revelationfirst.com","godkinggoogle.com","restoredacademy.com","axnidentifiers.org","leesharks.com","traininglayerliterature.org")

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8','replace'), r.geturl()

def fetch_record(n):
    url = f"https://www.alexanarch.org/s/records/{n}/"
    try:
        st, body, final = get(url)
        can = re.search(r'<link rel="canonical" href="([^"]+)"', body)
        return {"url": url, "status": st, "final_url": final, "bytes": len(body), "canonical": can.group(1) if can else None,
                "self_canonical": bool(can and can.group(1).rstrip('/') == url.rstrip('/'))}
    except Exception as e:
        return {"url": url, "error": str(e)[:200]}

def search_title(title, n):
    """Exact-title search. The public HTML endpoints (DuckDuckGo, Bing) answer automated
    fetches with a challenge page, so the engine is the Brave Search API (BRAVE_API_KEY;
    free tier suffices for 20 queries a week). Without a key the search half is skipped
    and marked, never faked."""
    import os
    q = re.sub(r'\s+', ' ', title.split(' — ')[0].split(' (')[0]).strip()
    key = os.environ.get('BRAVE_API_KEY')
    if not key:
        return {"query": q, "skipped": "no BRAVE_API_KEY; search half not run"}
    url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode({"q": q, "count": 10})
    req = urllib.request.Request(url, headers={"Accept": "application/json", "X-Subscription-Token": key, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: j = json.loads(r.read().decode())
    except Exception as e:
        return {"query": q, "error": str(e)[:200]}
    urls = [x.get('url') for x in (j.get('web') or {}).get('results', [])][:10]
    rec = f"/s/records/{n}/"
    own_rank = next((i+1 for i,u in enumerate(urls) if rec in u), None)
    own_any = [(i+1,u) for i,u in enumerate(urls) if any(d in u for d in OWN)]
    return {"query": q, "engine": "brave", "top": urls, "record_rank": own_rank, "own_surfaces_ranked": own_any, "n_results": len(urls)}

def main():
    reg = {d['deposit_number']: d for d in json.load(open(ROOT/'data/registry.json'))['deposits']}
    today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    out = {"probe": "record-search", "date": today, "engine": "brave-search-api (or skipped)", "cohort": COHORT, "records": {}}
    for group, ns in COHORT.items():
        for n in ns:
            d = reg[n]
            r = {"group": group, "title": d['title'], "status": d.get('status'), "date": d.get('date'),
                 "fetch": fetch_record(n), "search": search_title(d['title'], n)}
            out["records"][str(n)] = r
            s = r["search"]; f = r["fetch"]
            print(f"{n:5} {group:18} fetch={f.get('status')} self_canonical={f.get('self_canonical')} | search: record_rank={s.get('record_rank')} own={len(s.get('own_surfaces_ranked',[]))}/{s.get('n_results')}")
            time.sleep(1.2)
    summ = {"records_probed": 20,
            "record_page_ranked_top10": sum(1 for r in out["records"].values() if r["search"].get("record_rank")),
            "any_own_surface_top10": sum(1 for r in out["records"].values() if r["search"].get("own_surfaces_ranked")),
            "fetch_ok_self_canonical": sum(1 for r in out["records"].values() if r["fetch"].get("self_canonical"))}
    out["summary"] = summ
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f"{today}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    (OUT/"latest.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps(summ))

if __name__ == '__main__': main()
