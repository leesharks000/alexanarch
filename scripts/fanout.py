#!/usr/bin/env python3
"""fanout.py — autonomous propagation of new deposits to external surfaces.

Doctrine: homes are content-addressed and boring; visibility surfaces are
disposable antennae. Every surface is gated on its credential and skips dark
when unset, so surfaces light up one key at a time with no code change.
State in data/fanout-state.json (per-surface high-water mark, seeded at 1037:
fan-out covers deposits minted from 2026-07-04 onward; earlier corpus reaches
surfaces via repo-level archiving, which covers everything).
"""
import json, os, sys, time, urllib.request, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT/'data/fanout-state.json'
SEED = 1037
SITE = "https://www.alexanarch.org"
REPOS = ["https://github.com/leesharks000/alexanarch",
         "https://github.com/leesharks000/machinemediation-org",
         "https://github.com/leesharks000/the-mandala-oracle"]

def http(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read()[:20000]
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:20000]
    except Exception as e:
        return 0, str(e).encode()[:400]

def load():
    reg = json.load(open(ROOT/'data/registry.json'))
    st = json.load(open(STATE)) if STATE.exists() else {}
    return reg, st

def new_for(st, reg, surface):
    hi = st.get(surface, SEED)
    return [e for e in reg['deposits'] if e['deposit_number'] > hi]

def urls_of(e):
    n, hx = e['deposit_number'], e['hex']
    return [f"{SITE}/s/records/{n}/", f"{SITE}/s/axn/{hx}/"]

def s_swh(st, reg):
    for origin in REPOS:
        code, _ = http(f"https://archive.softwareheritage.org/api/1/origin/save/git/url/{origin}/",
                       data=b"", method="POST")
        print(f"  swh {origin.split('/')[-1]}: {code}")
    st['swh_last_run'] = time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime())

def s_indexnow(st, reg):
    key = os.environ.get('INDEXNOW_KEY','')
    if not key: print("  indexnow: dark (INDEXNOW_KEY unset)"); return
    new = new_for(st, reg, 'indexnow')
    if not new: print("  indexnow: nothing new"); return
    urls = [u for e in new for u in urls_of(e)]
    body = json.dumps({"host":"www.alexanarch.org","key":key,
                       "keyLocation":f"{SITE}/{key}.txt","urlList":urls}).encode()
    code,_ = http("https://api.indexnow.org/indexnow", data=body,
                  headers={"Content-Type":"application/json; charset=utf-8"})
    print(f"  indexnow: {code} ({len(urls)} urls)")
    if code in (200,202): st['indexnow'] = max(e['deposit_number'] for e in new)

def s_wayback(st, reg):
    acc, sec = os.environ.get('IA_ACCESS',''), os.environ.get('IA_SECRET','')
    new = new_for(st, reg, 'wayback')
    if not new: print("  wayback: nothing new"); return
    hdr = {"Accept":"application/json"}
    if acc: hdr["Authorization"] = f"LOW {acc}:{sec}"
    ok = True
    for e in new:
        for u in urls_of(e):
            code,_ = http("https://web.archive.org/save",
                          data=urllib.parse.urlencode({"url":u}).encode(), headers=hdr)
            print(f"  wayback {u.split('/s/')[1]}: {code}")
            ok = ok and code in (200,302)
            time.sleep(4)
    if ok and acc: st['wayback'] = max(e['deposit_number'] for e in new)
    elif not acc: print("  wayback: best-effort only (IA_ACCESS unset; state not advanced)")

def s_ia_items(st, reg):
    acc, sec = os.environ.get('IA_ACCESS',''), os.environ.get('IA_SECRET','')
    if not acc: print("  ia-items: dark (IA_ACCESS unset)"); return
    new = new_for(st, reg, 'ia_items')
    if not new: print("  ia-items: nothing new"); return
    for e in new:
        hx = e['hex']; p = ROOT/f"data/texts/AXN-{hx}-text.md"
        if not p.exists(): continue
        ident = f"alexanarch-axn-{hx.lower()}"
        hdr = {"Authorization": f"LOW {acc}:{sec}",
               "x-archive-meta-title": e.get('title','')[:250],
               "x-archive-meta-creator": e.get('creator','Lee Sharks'),
               "x-archive-meta-licenseurl": "https://creativecommons.org/licenses/by/4.0/",
               "x-archive-meta-mediatype": "texts",
               "x-archive-meta-external-identifier": e['axn'],
               "x-archive-meta-subject": "alexanarch;AXN;independent scholarship",
               "x-archive-auto-make-bucket": "1"}
        code,_ = http(f"https://s3.us.archive.org/{ident}/AXN-{hx}-text.md",
                      data=p.read_bytes(), headers=hdr, method="PUT")
        print(f"  ia-item {ident}: {code}")
        time.sleep(2)
    st['ia_items'] = max(e['deposit_number'] for e in new)

def s_gh_releases(st, reg):
    tok = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN','')
    if not tok: print("  gh-releases: dark (no token)"); return
    new = new_for(st, reg, 'gh_releases')
    if not new: print("  gh-releases: nothing new"); return
    for e in new:
        hx, n = e['hex'], e['deposit_number']
        body = json.dumps({"tag_name": f"axn-{hx}", "name": e['axn'],
          "body": f"Deposit #{n}: {e.get('title','')}\n\nsha256 {e.get('hash','')}\nrecord: {SITE}/s/records/{n}/"}).encode()
        code, resp = http("https://api.github.com/repos/leesharks000/alexanarch/releases",
                          data=body, headers={"Authorization": f"Bearer {tok}",
                          "Accept":"application/vnd.github+json"})
        rid = json.loads(resp).get('id') if code == 201 else None
        if rid:
            p = ROOT/f"data/texts/AXN-{hx}-text.md"
            http(f"https://uploads.github.com/repos/leesharks000/alexanarch/releases/{rid}/assets?name=AXN-{hx}-text.md",
                 data=p.read_bytes(), headers={"Authorization": f"Bearer {tok}",
                 "Content-Type":"text/markdown"})
        print(f"  gh-release axn-{hx}: {code}")
    st['gh_releases'] = max(e['deposit_number'] for e in new)

def s_stub(name, env):
    def run(st, reg):
        if not os.environ.get(env): print(f"  {name}: dark ({env} unset)"); return
        print(f"  {name}: key present but adapter not yet implemented — flag to MANUS")
    return run

SURFACES = [("swh", s_swh), ("indexnow", s_indexnow), ("wayback", s_wayback),
            ("ia_items", s_ia_items), ("gh_releases", s_gh_releases),
            ("devto", s_stub("devto","DEVTO_API_KEY")), ("hashnode", s_stub("hashnode","HASHNODE_TOKEN")),
            ("bluesky", s_stub("bluesky","BSKY_APP_PASSWORD")), ("mastodon", s_stub("mastodon","MASTODON_TOKEN")),
            ("blogger", s_stub("blogger","BLOGGER_TOKEN"))]

def main():
    reg, st = load()
    print(f"fanout: registry at {len(reg['deposits'])} deposits")
    for name, fn in SURFACES:
        try: fn(st, reg)
        except Exception as ex: print(f"  {name}: ERROR {ex}")
    json.dump(st, open(STATE,'w'), indent=1)
    print("state written")

if __name__ == "__main__":
    main()
