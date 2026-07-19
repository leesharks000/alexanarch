#!/usr/bin/env python3
"""
match_semi_candidates.py — record potential blog matches for semi-restored works.

For every queue entry with restored.semi == true: score the full sitemap
inventory by slug-token overlap, merge in the known citing posts, fetch the
top candidates, and record graded evidence — WITHOUT minting anything:

  potential_blog_matches: [
    {url, slug_score, head_containment, body_containment, doi_in_post,
     fetch: ok|error, verdict}
  ]

Verdicts: 'strong' (body head matches at sub-gate level >=0.5, or the post
mentions the work's own DOI with body containment >=0.5), 'partial'
(any nonzero body signal), 'slug_only' (no fetch or no body signal).
The mint gate itself (>=0.75 head containment) already ran during the deep
pass; anything at gate level found here is flagged 'REVIEW: gate-level' for
a human look, since the deep pass should have caught it.

USAGE: python3 scripts/match_semi_candidates.py [--limit N] [--fetch-top N]
Progress: entries gain the field on write (idempotent; re-run skips entries
that already carry potential_blog_matches unless --refresh).
"""
import argparse, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / 'datasets' / 'doi-work-identity' / 'restoration-queue.json'
STOP = {'the','a','an','of','and','or','in','on','for','to','as','with','by','from','at',
        'crimson','hexagon','archive','is','not'}

def norm(t):
    t = re.sub(r'\[SUPERSEDED[^\]]*\]', '', t or '')
    return ' '.join(re.sub(r'[^0-9a-z ]', '', t.lower().replace('\u00a0',' ')).split())

def contain(a, b):
    sa, sb = set(a.split()) - STOP, set(b.split())
    return len(sa & sb) / max(1, len(sa)) if sa else 0.0

_CACHE = {}
def fetch(url):
    if url in _CACHE: return _CACHE[url]
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'alexanarch-matcher/1.0'})
        raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','replace')
    except Exception as ex:
        _CACHE[url] = None
        return None
    b = re.search(r"<div class='post-body entry-content[^']*'[^>]*>(.*?)<div class='post-footer'>", raw, re.S) \
        or re.search(r'<div class="post-body entry-content[^"]*"[^>]*>(.*?)<div class="post-footer">', raw, re.S)
    body = re.sub(r'<[^>]+>', ' ', b.group(1)) if b else ''
    _CACHE[url] = body
    return body

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=1000)
    ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--fetch-top', type=int, default=2)
    ap.add_argument('--refresh', action='store_true')
    args = ap.parse_args()
    inv = []
    for u in open(ROOT/'datasets'/'doi-work-identity'/'blog-post-inventory.txt'):
        u = u.strip()
        if not u: continue
        slug = u.rsplit('/',1)[-1].replace('.html','')
        inv.append((u, set(t for t in slug.split('-') if t and t not in STOP)))
    q = json.load(open(QUEUE))
    targets = [e for cls in ('restorable','metadata_only') for e in q[cls]
               if (e.get('restored') or {}).get('semi')]
    done = 0
    verdicts = {'strong':0,'partial':0,'slug_only':0,'none':0,'REVIEW: gate-level':0}
    for e in targets[args.offset:]:
        if done >= args.limit: break
        if e.get('potential_blog_matches') is not None and not args.refresh: continue
        tt = norm(e['title'])
        tset = set(tt.split()) - STOP
        scored = []
        for u, stoks in inv:
            ov = len(tset & stoks)
            if ov >= 1: scored.append((ov, u))
        scored.sort(reverse=True)
        pool = [u for _, u in scored[:6]]
        for u in e.get('candidate_blog_urls') or []:
            if u and u not in pool: pool.append(u)
        slugsc = dict((u, s) for s, u in scored)
        matches = []
        for i, u in enumerate(pool):
            rec = {'url': u, 'slug_score': slugsc.get(u, 0)}
            if i < args.fetch_top:
                body = fetch(u)
                if body is None:
                    rec['fetch'] = 'error'
                else:
                    rec['fetch'] = 'ok'
                    nb = norm(body)
                    rec['head_containment'] = round(contain(tt, nb[:800]), 2)
                    rec['body_containment'] = round(contain(tt, nb), 2)
                    rec['doi_in_post'] = any(d.rsplit('.',1)[1] in body for d in e['dois'])
            hc = rec.get('head_containment', 0)
            bc = rec.get('body_containment', 0)
            if hc >= 0.75:
                rec['verdict'] = 'REVIEW: gate-level'
            elif hc >= 0.5 or (rec.get('doi_in_post') and bc >= 0.5):
                rec['verdict'] = 'strong'
            elif bc >= 0.3:
                rec['verdict'] = 'partial'
            elif rec.get('slug_score', 0) >= 2:
                rec['verdict'] = 'slug_only'
            else:
                rec['verdict'] = 'none'
            matches.append(rec)
        order = {'REVIEW: gate-level':0,'strong':1,'partial':2,'slug_only':3,'none':4}
        matches.sort(key=lambda r: (order[r['verdict']], -r.get('slug_score',0)))
        e['potential_blog_matches'] = matches[:6]
        best = matches[0]['verdict'] if matches else 'none'
        verdicts[best] = verdicts.get(best, 0) + 1
        done += 1
        if done % 10 == 0:
            json.dump(q, open(QUEUE,'w'), ensure_ascii=False, indent=1)
    json.dump(q, open(QUEUE,'w'), ensure_ascii=False, indent=1)
    print(f'matched {done} entries | best-verdict distribution: {verdicts}')

if __name__ == '__main__':
    main()
