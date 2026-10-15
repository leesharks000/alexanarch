#!/usr/bin/env python3
"""repair_conversion_spans_20261015.py — conversion damage repaired in place, span by span, in active records.

Rulings (Lee Sharks, 2026-10-15): repair "broken, missing, and mislabelled files"; "the focus is on active,
non-duplicate records"; repair standard "the text as he published it"; the batch plan ("lets proceed").

The texts seated at the 2026-06-20 intake and later recoveries carry conversion damage the reading sweep noted on
188 active records (data/repair-maps/triage-2026-10-15.json, in:conversion). For most of them no input bytes are
retained (data/axn-derivation-ledger.json: unverified_input_not_retained), so they cannot be converted again;
the damage is repaired where it sits. Three kinds, each exact:

  EMPTY BULLETS   a list marker alone on its line, its text after one to three blank lines ("- \\n\\n\\n**Precision…**"):
                  the marker is joined to its text. Not applied inside code fences, nor when the next text line is
                  itself a list item or heading.
  DOUBLED TITLE   the same heading line twice within three lines: the second is dropped.
  EDGE PIPES      a pipe table written without edge pipes (html2text's form: "a | b" over "---|---"): the record
                  renderer draws a table only from lines that begin with "|", so these showed as raw text. Each
                  block around a separator line of 3+-dash cells gets its edge pipes.
  FLAT TABLES     a table written one cell per line. The table is taken from the published post (data/blog-index
                  source, fetched): its cells, in order, must equal a run of the seated text's non-blank lines
                  exactly (whitespace and ** ignored), and only once; that run is replaced by the post's table
                  converted with characters kept. A table not matched exactly is left as it is.

Records: ACTIVE and not superseded. All fixes for a record are applied in one pass so it gets one new hash and AXN
(same hex and family); conversion_spans_repaired records the counts, the hash and AXN before; record_modification
records the change. Front page untouched (deposit order unchanged).

    python3 scripts/repair_conversion_spans_20261015.py --dry-run | --apply [--records 8,23,...]
"""
import hashlib, html, json, pathlib, re, sys
from html.parser import HTMLParser
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-15'
RULING = ('Lee Sharks, 2026-10-15: repair "broken, missing, and mislabelled files"; "the focus is on active, '
          'non-duplicate records"; "lets proceed"')
FENCE = re.compile(r'^\s*(```|~~~)')
MARK = re.compile(r'^([ \t]*)([-*+]|\d+\.)[ \t]*$')
ITEM = re.compile(r'^[ \t]*([-*+]|\d+\.)\s|^[ \t]*#')
HEAD = re.compile(r'^#{1,6}\s+\S')


def fix_empty_bullets(lines):
    out, i, n, fence = [], 0, 0, False
    while i < len(lines):
        l = lines[i]
        if FENCE.match(l):
            fence = not fence
        m = MARK.match(l) if not fence else None
        if m:
            j = i + 1
            while j < len(lines) and j - i <= 4 and not lines[j].strip():
                j += 1
            if 1 < j - i <= 4 and j < len(lines) and lines[j].strip() and not ITEM.match(lines[j]) and not FENCE.match(lines[j]):
                out.append(f'{m.group(1)}{m.group(2)} {lines[j].strip()}'); n += 1; i = j + 1; continue
        out.append(l); i += 1
    return out, n


SEP = re.compile(r'^\s*:?-{3,}:?(\s*\|\s*:?-{3,}:?)+\s*\|?\s*$')


def fix_edge_pipes(lines):
    out = list(lines); n = 0; fence = False; fences = []
    for l in lines:
        if FENCE.match(l):
            fence = not fence
        fences.append(fence)
    for i, l in enumerate(lines):
        if fences[i] or not SEP.match(l) or l.lstrip().startswith('|'):
            continue
        a = i - 1
        while a >= 0 and '|' in lines[a] and lines[a].strip() and not lines[a].lstrip().startswith('|'):
            a -= 1
        b = i + 1
        while b < len(lines) and '|' in lines[b] and lines[b].strip() and not lines[b].lstrip().startswith('|'):
            b += 1
        if a + 1 > i - 1:
            continue                      # no header row: not a table
        for k in range(a + 1, b):
            x = out[k].strip()
            out[k] = '| ' + x.rstrip('|').strip() + ' |'
        n += 1
    return out, n


def fix_doubled_headings(lines):
    out, n, fence = [], 0, False
    for l in lines:
        if FENCE.match(l):
            fence = not fence
        if not fence and HEAD.match(l):
            prev = [x for x in out[-3:] if x.strip()]
            if prev and prev[-1].strip() == l.strip():
                n += 1; continue
        out.append(l)
    return out, n


class _Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables = []; self.depth = 0; self.cell = None; self.raw = []; self.start = None
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.depth += 1
            if self.depth == 1:
                self.tables.append({'cells': [], 'pos': self.getpos()})
        elif tag in ('td', 'th') and self.depth == 1:
            self.cell = []
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.depth == 1 and self.cell is not None:
            self.tables[-1]['cells'].append(' '.join(''.join(self.cell).split())); self.cell = None
        elif tag == 'table':
            self.depth -= 1
    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


def table_html(body):
    """each top-level <table>…</table> of the post, as raw html, in order"""
    out, i = [], 0
    low = body.lower()
    while True:
        a = low.find('<table', i)
        if a < 0:
            return out
        depth, j = 0, a
        while True:
            o = low.find('<table', j + 1); c = low.find('</table>', j + 1)
            if c < 0:
                return out
            if 0 <= o < c:
                depth += 1; j = o
            else:
                if depth == 0:
                    out.append(body[a:c + 8]); i = c + 8; break
                depth -= 1; j = c


def norm(s):
    return ' '.join(html.unescape(re.sub(r'[*_`]+', '', s)).split())


def fix_flat_tables(lines, post_body, to_md):
    if not post_body:
        return lines, 0
    p = _Tables(); p.feed(post_body)
    raws = table_html(post_body)
    n = 0
    for k, tb in enumerate(p.tables):
        cells = [norm(c) for c in tb['cells'] if norm(c)]
        if len(cells) < 4 or k >= len(raws):
            continue
        nb = [(i, norm(l)) for i, l in enumerate(lines) if norm(l)]
        vals = [v for _, v in nb]
        hits = [s for s in range(len(vals) - len(cells) + 1) if vals[s:s + len(cells)] == cells]
        if len(hits) != 1:
            continue
        s = hits[0]; a, b = nb[s][0], nb[s + len(cells) - 1][0]
        from restore_wrong_bodies import unescape   # converter escapes dropped unless the post carries them
        md = unescape(to_md(raws[k]), raws[k]).strip('\n')
        if '|' not in md:
            continue
        rows, _ = fix_edge_pipes(md.split('\n'))
        lines = lines[:a] + rows + lines[b + 1:]
        n += 1
    return lines, n


def main():
    apply = '--apply' in sys.argv
    only = None
    if '--records' in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index('--records') + 1].split(',')}
    sp = pathlib.Path('/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/repair/convscan.json')
    posts = {o['deposit']: o['post'] for o in json.load(open(sp)) if o.get('post') and o['post_in_text'] >= 0.8} if sp.exists() else {}
    from restore_from_blog import fetch, extract_post
    from restore_wrong_bodies import to_md
    reg = json.load(open(ROOT / 'data/registry.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    report = []
    for n, d in sorted(D.items()):
        if d.get('status') != 'ACTIVE' or d.get('superseded_by_deposit_number') or not d.get('full_text_path'):
            continue
        if only and n not in only:
            continue
        tp = ROOT / d['full_text_path'].lstrip('/')
        if not tp.exists():
            continue
        t = tp.read_text(encoding='utf-8'); lines = t.split('\n')
        lines, nb = fix_empty_bullets(lines)
        lines, nh = fix_doubled_headings(lines)
        lines, ne = fix_edge_pipes(lines)
        nt = 0
        if n in posts:
            try:
                _, body = extract_post(fetch(posts[n]).decode('utf-8', 'replace'))
                lines, nt = fix_flat_tables(lines, body, to_md)
            except Exception:
                pass
        new = '\n'.join(lines)
        if new == t:
            continue
        report.append({'n': n, 'empty_bullets': nb, 'doubled_headings': nh, 'edge_pipe_tables': ne, 'tables': nt})
        if not apply:
            continue
        tp.write_text(new, encoding='utf-8')
        h = hashlib.sha256(new.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
        rec = {'on': ON, 'empty_bullets_joined': nb, 'doubled_headings_dropped': nh, 'edge_pipe_tables': ne, 'flat_tables_rebuilt': nt,
               'table_source': posts.get(n) if nt else None, 'hash_before': d.get('hash'), 'axn_before': d.get('axn'),
               'ruled_by': RULING}
        d['conversion_spans_repaired'] = rec
        d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
        d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
        d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
        if isinstance(d.get('body_status'), dict):
            d['body_status']['residual_chars'] = len(new)
        rm.touch(d, 'body_status', f'conversion damage repaired in place: {nb} empty bullets joined, {nh} doubled '
                 f'headings dropped, {ne} tables given edge pipes, {nt} flattened tables rebuilt from the published post',
                 was={'axn': rec['axn_before']}, now={'axn': d['axn']}, when=ON)
    if apply and report:
        json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
        json.dump({'generated': ON, 'ruling': RULING, 'records': report},
                  open(ROOT / 'data/repair-maps/conversion-spans-2026-10-15.json', 'w'), ensure_ascii=False, indent=1)
    tot = {k: sum(r[k] for r in report) for k in ('empty_bullets', 'doubled_headings', 'edge_pipe_tables', 'tables')}
    print(len(report), 'records', tot)
    print(report[:12])


if __name__ == '__main__':
    main()
