#!/usr/bin/env python3
"""blog_to_markdown.py — faithful Blogger post -> markdown.

WHY (MANUS, 2026-08-04, on #1225): an earlier restoration pass wrote blog HTML
into deposit bodies WITHOUT decoding entities and WITHOUT preserving block
structure. Result: `&#8212;` `&#8594;` `&nbsp;` left raw in the archive's own
canonical text, and whole essays collapsed into single run-on paragraphs (one
record holds a 125,213-character "paragraph"). The source HTML had the
structure all along — #1225's post carries 79 <p> and 12 <h2>.

Rules:
  · entities decoded exactly once (html.unescape), then NBSP -> real space
  · <h1..h4> -> markdown headings; <p>/<div> -> paragraph breaks
  · <br> -> hard line break (verse and address blocks keep their lineation)
  · <li> -> list items; <blockquote> -> quote; <table> preserved as pipe rows
  · <pre>/<code> fenced, never reflowed
  · leading whitespace preserved on lines that carry it (prosody)
"""
import html as H
import re
import subprocess
import sys


def fetch(url):
    r = subprocess.run(['curl', '-s', '-L', '--max-time', '30', url],
                       capture_output=True, text=True)
    return r.stdout


def post_body(page):
    m = re.search(r"<div class=['\"]post-body[^'\"]*['\"][^>]*>(.*?)<div class=['\"]post-footer",
                  page, re.S)
    return m.group(1) if m else ''


def convert(body):
    t = body
    t = re.sub(r'(?is)<script.*?</script>', '', t)
    t = re.sub(r'(?is)<style.*?</style>', '', t)
    # code first, so nothing else touches it
    t = re.sub(r'(?is)<pre[^>]*>(.*?)</pre>', lambda m: '\n\n```\n' + re.sub(r'<[^>]+>', '', m.group(1)) + '\n```\n\n', t)
    # tables -> pipe rows
    def _table(m):
        rows = re.findall(r'(?is)<tr[^>]*>(.*?)</tr>', m.group(1))
        out = []
        for r in rows:
            cells = [re.sub(r'<[^>]+>', '', c).strip()
                     for c in re.findall(r'(?is)<t[dh][^>]*>(.*?)</t[dh]>', r)]
            if cells:
                out.append('| ' + ' | '.join(cells) + ' |')
        if out and len(out) > 1:
            out.insert(1, '|' + '---|' * len(re.findall(r'\|', out[0])[:-1]))
        return '\n\n' + '\n'.join(out) + '\n\n'
    t = re.sub(r'(?is)<table[^>]*>(.*?)</table>', _table, t)
    for lvl in (1, 2, 3, 4):
        t = re.sub(rf'(?is)<h{lvl}[^>]*>(.*?)</h{lvl}>',
                   lambda m, l=lvl: '\n\n' + '#' * (l + 1) + ' ' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n\n', t)
    t = re.sub(r'(?is)<blockquote[^>]*>(.*?)</blockquote>',
               lambda m: '\n\n> ' + re.sub(r'<[^>]+>', '', m.group(1)).strip().replace('\n', '\n> ') + '\n\n', t)
    t = re.sub(r'(?is)<li[^>]*>(.*?)</li>',
               lambda m: '\n- ' + re.sub(r'<[^>]+>', '', m.group(1)).strip(), t)
    t = re.sub(r'(?i)</?(b|strong)>', '**', t)
    t = re.sub(r'(?i)</?(i|em)>', '*', t)
    t = re.sub(r'(?i)<br\s*/?>', '\n', t)
    t = re.sub(r'(?i)</(p|div)>', '\n\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = H.unescape(t)                    # ENTITIES DECODED — exactly once
    t = t.replace('\xa0', ' ')           # NBSP -> real space, after decoding
    lines = [l.rstrip() for l in t.split('\n')]
    out, blank = [], 0
    for l in lines:
        if not l.strip():
            blank += 1
            if blank <= 2:
                out.append('')
        else:
            blank = 0
            out.append(l)
    return re.sub(r'\n{4,}', '\n\n\n', '\n'.join(out)).strip() + '\n'


if __name__ == '__main__':
    md = convert(post_body(fetch(sys.argv[1])))
    if len(sys.argv) > 2:
        open(sys.argv[2], 'w', encoding='utf-8').write(md)
        print(f'wrote {sys.argv[2]} ({len(md):,} chars)')
    else:
        sys.stdout.write(md)
