#!/usr/bin/env python3
"""repair_flat_tables.py — tables flattened to one cell per line, rebuilt as pipe tables from their own cells.

Rulings (Lee Sharks): 2026-10-15, repair "broken, missing, and mislabelled files", "the text as he published it",
"the focus is on active, non-duplicate records"; 2026-10-19, "lets fix the flattened table, too" (#1651's).

WHAT THE DAMAGE IS. The intake conversion wrote some tables one cell per line: each row a block of n lines, rows
separated by two or more blank lines, so the record page shows a column of words where the table was:

    Figure                                  | Figure | Context | Claim Basis |
    Context                                 |---|---|---|
    Claim Basis              becomes        | **Pierre de Ronsard** (1524-1585) | French Renaissance | Honored by contemporaries |
                                            ...
    **Pierre de Ronsard** (1524-1585)
    French Renaissance
    Honored by contemporaries

The 2026-10-15 pass (repair_conversion_spans_20261015.py) rebuilt flat tables only where the published blog post's
table matched the seated cells exactly. This rebuilds a table from the seated cells themselves: no cell is changed,
added, dropped or reordered; the first block is the header. Exact by construction (checked: the cells read back from
the rebuilt table equal the cells removed, in order).

WHAT IS A FLAT TABLE HERE. A run of >= 3 consecutive blocks, each block n >= 2 single lines (no blank line inside),
blocks separated by >= 2 blank lines, every line <= 140 characters and none a heading, list item, quote, rule, fence
or pipe line; and the first block a header: every cell <= 40 characters, none ending in . , ; or :, and no line in
the run ending in a comma. Verse with stanzas of equal length can take the first shape; the header test is what
separates them, and a run that fails it is reported and left alone.

Records: ACTIVE and not superseded. One pass per record, one new hash and AXN (same hex and family), recorded in
flat_tables_repaired with the hash and AXN before, and through record_modification. Deposit order is unchanged.

    python3 scripts/repair_flat_tables.py --records 1651 [--apply]
    python3 scripts/repair_flat_tables.py --census            # every active record, nothing written
"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-19'
RULING = ('Lee Sharks, 2026-10-15: repair "broken, missing, and mislabelled files", "the text as he published it"; '
          '2026-10-19: "lets fix the flattened table, too"')
BAD = re.compile(r'^(#|[-*+] |\d+\. |\||>|```|~~~|---)')
FENCE = re.compile(r'^\s*(```|~~~)')


def blocks(lines):
    """[(first_line, last_line, [cells])] for each run of non-blank lines; a single blank inside marks the block broken."""
    out, cur, blanks, fence = [], None, 0, False
    for i, l in enumerate(lines):
        if FENCE.match(l):
            fence = not fence
        s = l.strip()
        if not s:
            blanks += 1
            continue
        if cur and (blanks >= 2 or fence):
            out.append(cur); cur = None
        if cur and blanks == 1:
            cur[3] = True
        if cur is None:
            cur = [i, i, [], fence]
        cur[1] = i; cur[2].append(s); blanks = 0
    if cur:
        out.append(cur)
    return [(a, b, c, broken) for a, b, c, broken in out]


def cell_ok(x):
    return len(x) <= 140 and not BAD.match(x)


def find(lines):
    B = blocks(lines); runs, i = [], 0
    while i < len(B):
        j = i
        a, b, c, broken = B[i]
        if not broken and len(c) >= 2 and all(map(cell_ok, c)):
            n = len(c)
            while j + 1 < len(B) and not B[j + 1][3] and len(B[j + 1][2]) == n and all(map(cell_ok, B[j + 1][2])):
                j += 1
            if j - i + 1 >= 3:
                run = B[i:j + 1]
                hdr = run[0][2]
                tablelike = (all(len(x) <= 40 and not x.endswith(('.', ',', ';', ':')) for x in hdr)
                             and not any(x.endswith(',') for r in run for x in r[2]))
                runs.append({'first': run[0][0], 'last': run[-1][1], 'rows': [r[2] for r in run], 'tablelike': tablelike})
        i = j + 1
    return runs


def esc(x):
    return x.replace('|', '\\|')


def to_table(rows):
    n = len(rows[0])
    t = ['| ' + ' | '.join(esc(c) for c in rows[0]) + ' |', '|' + '---|' * n]
    t += ['| ' + ' | '.join(esc(c) for c in r) + ' |' for r in rows[1:]]
    return t


def read_back(table):
    return [[c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', l.strip())[1:-1]] for l in table if not re.match(r'^\|(---\|)+$', l)]


def repair(text):
    lines = text.split('\n')
    runs = [r for r in find(lines) if r['tablelike']]
    for r in reversed(runs):
        tb = to_table(r['rows'])
        assert read_back(tb) == r['rows'], 'cells changed'
        lines = lines[:r['first']] + tb + lines[r['last'] + 1:]
    return '\n'.join(lines), runs


def main():
    reg = json.load(open(ROOT / 'data/registry.json'))
    D = {d['deposit_number']: d for d in reg['deposits']}
    census = '--census' in sys.argv; apply = '--apply' in sys.argv
    only = {int(x) for x in sys.argv[sys.argv.index('--records') + 1].split(',')} if '--records' in sys.argv else None
    tot = {'records': 0, 'tables': 0, 'left_not_tablelike': 0}; rep = []
    for n, d in sorted(D.items()):
        if only and n not in only:
            continue
        if d.get('status') != 'ACTIVE' or d.get('superseded_by_deposit_number') or not d.get('full_text_path'):
            continue
        p = ROOT / d['full_text_path'].lstrip('/')
        if not p.exists():
            continue
        t = p.read_text(encoding='utf-8')
        allr = find(t.split('\n'))
        new, runs = repair(t)
        left = len(allr) - len(runs)
        if not runs and not left:
            continue
        tot['records'] += bool(runs); tot['tables'] += len(runs); tot['left_not_tablelike'] += left
        rep.append({'n': n, 'tables': len(runs), 'left': left, 'headers': [r['rows'][0] for r in runs]})
        if census or not apply or not runs:
            continue
        p.write_text(new, encoding='utf-8')
        h = hashlib.sha256(new.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
        rec = {'on': ON, 'tables_rebuilt': len(runs), 'headers': [r['rows'][0] for r in runs], 'left_not_tablelike': left,
               'hash_before': d.get('hash'), 'axn_before': d.get('axn'), 'ruled_by': RULING}
        d.setdefault('flat_tables_repaired', []).append(rec)
        d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
        d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
        d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
        if isinstance(d.get('body_status'), dict):
            d['body_status']['residual_chars'] = len(new)
        rm.touch(d, 'body_status', f'{len(runs)} flattened table(s) rebuilt from their own cells (one cell per line → pipe table; '
                 'no cell changed)', was={'axn': rec['axn_before']}, now={'axn': d['axn']}, when=ON)
    if apply and not census:
        json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
        (ROOT / 'data/repair-maps').mkdir(exist_ok=True)
        json.dump({'generated': ON, 'ruling': RULING, 'records': rep},
                  open(ROOT / f'data/repair-maps/flat-tables-{ON}.json', 'w'), ensure_ascii=False, indent=1)
    print(tot)
    for r in rep[:20]:
        print(r['n'], r['tables'], 'left', r['left'], r['headers'][:2])


if __name__ == '__main__':
    main()
