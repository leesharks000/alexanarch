#!/usr/bin/env python3
"""find_flat_table_copies.py — second copies of flattened tables, found in the published blog posts.

Ruling (Lee Sharks, 2026-10-19): "kets develop a method of restoring by eye, then find second copies, then see if the
method would faithfully restore what the second copy confirms"; "lets restore those tables. note that its possible the
blog itself contains flattened tables - they were simple pastes".

A seated record holds a FLAT TABLE when a table was written one cell per line, rows apart by two or more blank lines.
A blog post's <table> is a SECOND COPY of it when the post table's non-empty cells, read row by row, equal a run of the
seated text's non-blank lines exactly (whitespace, *, _, ` and backslashes ignored).

Because the posts were simple pastes, a post can itself be damaged: a table pasted flat is no <table> at all and is never
a copy; a "|" inside a cell splits it into extra columns; a pasted table can carry rows that are not the table's. So a
copy is taken only when it agrees with the seated text's own structure, independently read, and is reported otherwise:
  RECTANGULAR  every row of the copy has the same number of cells;
  ROWS AGREE   each copy row's non-empty cells are exactly one seated block (the lines between two-blank separators):
               the copy gives the columns, the seated text gives the rows, and both must say the same thing;
  ONE LINE     no copy cell holds a line break (a cell spanning several seated lines is left flat);
  ONE COPY     where several posts confirm a span, they must agree on its structure.
Where a span is confirmed by a longer and a shorter copy from the same first line, the longer is taken.

Writes data/repair-maps/flat-table-copies-2026-10-19.json: per span, the record, its lines, the post, and the structure
(for each row, which cells are empty); the cells themselves are never taken from the post.

    python3 scripts/find_flat_table_copies.py --posts <feed dump.json>
The feed dump is a list of {url, published, html} from the blog's JSON feed (feeds/posts/default?alt=json).
"""
import json, re, sys, pathlib, collections
from html.parser import HTMLParser
ROOT = pathlib.Path(__file__).resolve().parents[1]
ON = '2026-10-19'
norm = lambda s: re.sub(r'[\s*_\\`]', '', s)


class Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables, self.stack, self.cell, self.row = [], [], None, None
    def handle_starttag(self, tag, a):
        if tag == 'table': self.stack.append([])
        elif tag == 'tr' and self.stack: self.row = []
        elif tag in ('td', 'th') and self.row is not None: self.cell = []
        elif tag == 'br' and self.cell is not None: self.cell.append('\n')
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(re.sub(r'[ \t\xa0]+', ' ', ''.join(self.cell)).strip()); self.cell = None
        elif tag == 'tr' and self.row is not None:
            if self.stack: self.stack[-1].append(self.row)
            self.row = None
        elif tag == 'table' and self.stack:
            self.tables.append(self.stack.pop())
    def handle_data(self, d):
        if self.cell is not None: self.cell.append(d)


def seated_blocks(L, a, b):
    """The seated span's rows as the seated text gives them: runs of non-blank lines between >= 2 blank lines."""
    out, cur, blanks = [], [], 0
    for i in range(a, b):
        if not L[i].strip():
            blanks += 1; continue
        if cur and blanks >= 2:
            out.append(cur); cur = []
        elif cur and blanks == 1:
            return None                         # a single blank inside a row: the seated structure is not clean
        cur.append(i); blanks = 0
    if cur: out.append(cur)
    return out


def main():
    posts = json.load(open(sys.argv[sys.argv.index('--posts') + 1]))
    reg = {d['deposit_number']: d for d in json.load(open(ROOT / 'data/registry.json'))['deposits']}
    active = {n: d for n, d in reg.items() if d.get('status') == 'ACTIVE' and not d.get('superseded_by_deposit_number') and d.get('full_text_path')}
    texts, index = {}, collections.defaultdict(list)
    for n, d in active.items():
        p = ROOT / d['full_text_path'].lstrip('/')
        if not p.exists(): continue
        L = p.read_text(encoding='utf-8').split('\n'); texts[n] = (d['full_text_path'].lstrip('/'), L)
        fence = False
        for i, l in enumerate(L):
            if re.match(r'^\s*(```|~~~)', l): fence = not fence
            if l.strip() and not fence and not l.strip().startswith('|'): index[norm(l)].append((n, i))
    found = collections.defaultdict(list)       # (n, first line) -> [candidate]
    nt = 0
    for post in posts:
        if '<table' not in post.get('html', ''): continue
        t = Tables(); t.feed(post['html'])
        for rows in t.tables:
            rows = [r for r in rows if r]
            if len(rows) < 2 or max(map(len, rows)) < 2: continue
            nt += 1
            seq = [norm(c) for r in rows for c in r if norm(c)]
            if len(seq) < 4: continue
            for n, i in index.get(seq[0], []):
                p, L = texts[n]; k, j = 0, i
                while j < len(L) and k < len(seq):
                    if L[j].strip():
                        if norm(L[j]) != seq[k]: break
                        k += 1
                    j += 1
                if k == len(seq):
                    found[(n, i)].append({'url': post['url'], 'end': j, 'rows': rows})
    spans, report = [], collections.Counter(); left = []
    for (n, i), cs in sorted(found.items()):
        top = max(c['end'] for c in cs); cs = [c for c in cs if c['end'] == top]   # the longer copy from this first line
        p, L = texts[n]
        shapes = {json.dumps([[bool(norm(x)) for x in r] for r in c['rows']]) for c in cs}
        c = cs[0]; why = None
        if len(shapes) > 1: why = 'copies disagree on the structure'
        elif any('\n' in x for r in c['rows'] for x in r): why = 'a copy cell holds a line break'
        elif len({len(r) for r in c['rows']}) > 1: why = 'the copy is not rectangular (a "|" inside a cell, or a row that is not the table\'s)'
        else:
            blocks = seated_blocks(L, i, c['end'])
            if blocks is None: why = 'a single blank line inside a seated row'
            elif [len(b) for b in blocks] != [sum(bool(norm(x)) for x in r) for r in c['rows']]:
                why = 'the copy\'s rows and the seated rows disagree'
        if why:
            report[why] += 1; left.append({'n': n, 'line': i + 1, 'url': c['url'], 'why': why}); continue
        report['taken'] += 1
        spans.append({'n': n, 'path': p, 'first': i, 'last': c['end'] - 1, 'copy': c['url'],
                      'structure': [[bool(norm(x)) for x in r] for r in c['rows']], 'copies': len(cs)})
    # spans must not overlap one another
    spans.sort(key=lambda s: (s['n'], s['first'])); keep = []
    for s in spans:
        if keep and keep[-1]['n'] == s['n'] and s['first'] <= keep[-1]['last']:
            report['taken'] -= 1; report['overlaps a span already taken'] += 1
            left.append({'n': s['n'], 'line': s['first'] + 1, 'url': s['copy'], 'why': 'overlaps a span already taken'}); continue
        keep.append(s)
    out = {'generated': ON, 'post_tables_read': nt, 'counts': dict(report), 'records': len({s['n'] for s in keep}),
           'spans': keep, 'left_flat': left}
    (ROOT / 'data/repair-maps').mkdir(exist_ok=True)
    json.dump(out, open(ROOT / f'data/repair-maps/flat-table-copies-{ON}.json', 'w'), ensure_ascii=False, indent=1)
    print({k: v for k, v in out.items() if k not in ('spans', 'left_flat')})


if __name__ == '__main__':
    main()
