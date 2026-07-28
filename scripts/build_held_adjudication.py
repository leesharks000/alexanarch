#!/usr/bin/env python3
"""build_held_adjudication.py — turn the held list into readable adjudication material.

For each held record: title, date, content_type, dead DOI(s), what the capture
body currently holds (first line), and every candidate URL with its post title,
a body-head snippet, and gate scores (contain on full title / on title core).
Mechanical read-hints where derivable: digest-only candidate sets, version-token
mismatches, no-blog-presence. Snippets pass the legal-name hygiene mask before
they are written anywhere. Disk-cached (/tmp/adj-cache.json); resumable.
Outputs: data/restoration-held-adjudication-2026-07-28.md (+ .json).
"""
import json, re, sys, time, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from restore_from_blog import norm, fetch, extract_post, contain, slug_candidates, load_inventory
from restore_in_place import to_md, LEGAL_RX, build_targets

CACHE_P = Path('/tmp/adj-cache.json')
CACHE = json.load(open(CACHE_P)) if CACHE_P.exists() else {}
OUT_MD = ROOT / 'data' / 'restoration-held-adjudication-2026-07-28.md'
OUT_JS = ROOT / 'data' / 'restoration-held-adjudication-2026-07-28.json'

VER_RX = re.compile(r'\bv(\d+(?:\.\d+)*)\b', re.I)


def head_of(url):
    if url in CACHE:
        return CACHE[url]
    try:
        htmlb = fetch(url).decode('utf-8', 'replace')
        time.sleep(0.7)
    except Exception as e:
        CACHE[url] = {'err': str(e)[:60]}
        return CACHE[url]
    pt, body = extract_post(htmlb)
    if not body:
        CACHE[url] = {'post_title': pt[:110], 'no_body': True}
        return CACHE[url]
    md = to_md(body).strip()
    snip = re.sub(r'\s+', ' ', re.sub(r'!\[[^\]]*\]\([^)]*\)', '[img]', md))[:180]
    if LEGAL_RX.search(snip) or LEGAL_RX.search(pt or ''):
        snip = '[snippet withheld: hygiene mask]'
        pt = '[masked]'
    CACHE[url] = {'post_title': (pt or '')[:110], 'snip': snip, 'md_norm_head': norm(md[:1200])[:800]}
    return CACHE[url]


def main(offset=0, limit=0):
    reg = json.load(open(ROOT / 'data' / 'registry.json'))
    dri = json.load(open(ROOT / 'data' / 'doi-resolution-index.json'))
    rep = json.load(open(ROOT / 'data' / 'restoration-inplace-2026-07-28.json'))
    inv = load_inventory()
    targets = {t[0]['deposit_number']: t for t in build_targets(reg, dri)}
    byn = {d['deposit_number']: d for d in reg['deposits']}
    doimap = {}
    for m in dri['mappings']:
        t = norm(m.get('title', ''))
        if t:
            doimap.setdefault(t, []).append(m.get('dead_doi'))

    held = rep['held']
    if limit:
        held = held[offset:offset + limit]
    records = json.load(open(OUT_JS))['records'] if OUT_JS.exists() else {}

    for h in held:
        n = h['n']
        if str(n) in records:
            continue
        d = byn[n]
        tt = norm(d.get('title', ''))
        entry = {'n': n, 'title': d.get('title'), 'date': d.get('date'),
                 'content_type': d.get('content_type'), 'reason': h['reason'],
                 'dead_dois': doimap.get(tt, []),
                 'capture_first_line': '', 'candidates': [], 'hint': ''}
        tp = (d.get('full_text_path') or '').lstrip('/')
        if tp and (ROOT / tp).exists():
            first = (ROOT / tp).read_text(errors='replace').strip().split('\n', 1)[0]
            entry['capture_first_line'] = first[:160]
        if h['reason'] == 'non_blog_source':
            entry['hint'] = f"non-blog source; lane {h.get('lane')} — {h.get('detail')}"
            entry['candidates'] = [{'url': h.get('detail'), 'note': 'alt source (not fetched by blog extractor)'}]
        else:
            tgt = targets.get(n)
            urls = list(tgt[1]) if tgt else []
            for c in slug_candidates(d.get('title', ''), inv, k=10, min_ov=2):
                u = c[0] if isinstance(c, (list, tuple)) else c
                if u not in urls:
                    urls.append(u)
            digesty, vers_mismatch = 0, None
            tver = VER_RX.search(d.get('title', ''))
            for u in urls[:4]:
                info = head_of(u)
                cand = {'url': u}
                if 'err' in info:
                    cand['fetch'] = info['err']
                elif info.get('no_body'):
                    cand['post_title'] = info.get('post_title', '')
                    cand['note'] = 'no Blogger post body at URL'
                else:
                    cand['post_title'] = info['post_title']
                    cand['head'] = info['snip']
                    cand['contain_full'] = round(contain(tt, info['md_norm_head']), 2)
                    core = re.split(r'\s+\u2014\s+|\s*\(', d.get('title', ''), 1)[0]
                    cand['contain_core'] = round(contain(norm(core), info['md_norm_head']), 2)
                    if 'doi registry' in info['md_norm_head'][:120] or 'registry v7' in info['md_norm_head'][:120]:
                        digesty += 1
                    pver = VER_RX.search(info.get('post_title', '') + ' ' + info['snip'])
                    if tver and pver and tver.group(1) != pver.group(1) and cand['contain_core'] >= 0.5:
                        vers_mismatch = f"deposit v{tver.group(1)} vs candidate v{pver.group(1)} at {u.rsplit('/',1)[-1][:40]}"
            if vers_mismatch:
                entry['hint'] = f"VERSION MISMATCH — {vers_mismatch}; ruling needed (restore earlier version as chain-head, or hold)"
            elif digesty == len(urls[:4]) and urls:
                entry['hint'] = 'all candidates are registry-digest posts — the work itself may never have been blogged'
            elif not urls:
                entry['hint'] = 'no candidates at all: not in blog inventory and no mapped URL'
            entry['candidates'] = [c for c in ([] if h['reason'] == 'non_blog_source' else [])] or entry['candidates']
            entry['candidates'] = []
            for u in urls[:4]:
                info = head_of(u)
                cand = {'url': u}
                if 'err' in info:
                    cand['fetch_error'] = info['err']
                elif info.get('no_body'):
                    cand['post_title'] = info.get('post_title', ''); cand['note'] = 'no post body'
                else:
                    cand.update({'post_title': info['post_title'], 'head': info['snip'],
                                 'contain_full': round(contain(tt, info['md_norm_head']), 2),
                                 'contain_core': round(contain(norm(re.split(r'\s+\u2014\s+|\s*\(', d.get('title',''),1)[0]), info['md_norm_head']), 2)})
                entry['candidates'].append(cand)
        records[str(n)] = entry
        json.dump(CACHE, open(CACHE_P, 'w'))
        json.dump({'records': records}, open(OUT_JS, 'w'), ensure_ascii=False, indent=1)
        print(f"done #{n} ({len(records)}/{len(rep['held'])})")

    # markdown render
    lines = [f"# Held-Record Adjudication Material — {len(records)} of {len(rep['held'])} held (2026-07-28)",
             "", "Per record: what the archive holds, what was tried, what was actually at each URL, and a mechanical hint where one is derivable. Rulings are yours; nothing here writes anything.", ""]
    for n in sorted(int(k) for k in records):
        e = records[str(n)]
        lines.append(f"## #{n} — {e['title']}")
        lines.append(f"*{e['date']} · {str(e['content_type'])[:60]} · reason: {e['reason']}*  ")
        if e['dead_dois']:
            lines.append(f"Dead DOI(s): {', '.join(str(x) for x in e['dead_dois'][:3])}  ")
        if e['capture_first_line']:
            lines.append(f"Capture body opens: `{e['capture_first_line']}`  ")
        if e['hint']:
            lines.append(f"**Hint:** {e['hint']}  ")
        for c in e['candidates']:
            if 'fetch_error' in c:
                lines.append(f"- {c['url']} — fetch failed: {c['fetch_error']}")
            elif c.get('note'):
                lines.append(f"- {c['url']} — {c['note']}")
            else:
                lines.append(f"- **{c.get('post_title','')}** — scores full={c.get('contain_full')} core={c.get('contain_core')}  \n  `{c.get('head','')}`  \n  {c['url']}")
        lines.append("")
    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')
    print(f"markdown: {OUT_MD.relative_to(ROOT)} | json: {OUT_JS.relative_to(ROOT)}")


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    main(a.offset, a.limit)
