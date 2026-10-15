#!/usr/bin/env python3
"""repair_reading_tools.py — read-only helpers for the 2026-10-15 repair readers.

  python3.12 scripts/repair_reading_tools.py post <url>            the live post, converted (characters kept), with line numbers
  python3.12 scripts/repair_reading_tools.py find "<passage>"      every record whose seated text (or second store) contains it
  python3.12 scripts/repair_reading_tools.py posts "<title words>" blog posts whose title contains the words (date, url)
Nothing is written.
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
norm = lambda s: ' '.join(re.sub(r'[*_`#>|\\]+', ' ', s).split()).lower()
cmd, arg = sys.argv[1], sys.argv[2]
if cmd == 'post':
    from restore_from_blog import fetch, extract_post
    from restore_wrong_bodies import to_md, unescape
    t, b = extract_post(fetch(arg).decode('utf-8', 'replace'))
    md = unescape(to_md(b or ''), b or '')
    for i, l in enumerate(md.split('\n'), 1):
        print(f'{i:5d}\t{l}')
elif cmd == 'find':
    q = norm(arg)
    for d in json.load(open(ROOT / 'data/registry.json'))['deposits']:
        for p in (d.get('full_text_path') or '', f"/data/deposits/AXN-{d.get('hex')}.md"):
            f = ROOT / p.lstrip('/')
            if p and f.exists() and q in norm(f.read_text(encoding='utf-8', errors='replace')):
                print(d['deposit_number'], d.get('status'), p, d['title'][:90])
elif cmd == 'posts':
    w = arg.lower().split()
    for p in json.load(open(ROOT / 'data/blog-index.json'))['posts']:
        if all(x in p['title'].lower() for x in w):
            print(p['published'][:10], p['chars'], p['url'], '|', p['title'][:90])
