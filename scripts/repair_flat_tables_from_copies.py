#!/usr/bin/env python3
"""repair_flat_tables_from_copies.py — flattened tables rebuilt with the structure their second copy confirms.

Ruling (Lee Sharks, 2026-10-19): "lets restore those tables. note that its possible the blog itself contains flattened
tables - they were simple pastes". Repair standard (2026-10-15): "the text as he published it"; focus "active,
non-duplicate records".

Reads data/repair-maps/flat-table-copies-2026-10-19.json (scripts/find_flat_table_copies.py). For each span, the
copy gives only the structure: how many columns, where the rows break, which cells are empty. Every cell's text is the
seated line as it stands, markup included; no text is taken from the post. Checked before writing: the cells read back
from the rebuilt table, empty cells dropped, equal the seated lines removed, in order.

Records: ACTIVE and not superseded. One pass per record, one new hash and AXN (same hex and family), recorded in
flat_tables_repaired with the hash and AXN before, and through record_modification. Deposit order is unchanged.

    python3 scripts/repair_flat_tables_from_copies.py [--apply] [--records 8,23]
"""
import hashlib, json, pathlib, re, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-19'
RULING = ('Lee Sharks, 2026-10-19: "lets restore those tables. note that its possible the blog itself contains flattened '
          'tables - they were simple pastes"; 2026-10-15: "the text as he published it"')
MAP = ROOT / f'data/repair-maps/flat-table-copies-{ON}.json'


def esc(x):
    return x.replace('|', '\\|')


def build(L, s):
    cells = [L[i].strip() for i in range(s['first'], s['last'] + 1) if L[i].strip()]
    it = iter(cells); rows = []
    for shape in s['structure']:
        rows.append([next(it) if full else '' for full in shape])
    assert next(it, None) is None, 'cells left over'
    n = len(rows[0])
    t = ['| ' + ' | '.join(map(esc, rows[0])) + ' |', '|' + '---|' * n] + ['| ' + ' | '.join(map(esc, r)) + ' |' for r in rows[1:]]
    back = [c.strip().replace('\\|', '|') for l in t if not re.match(r'^\|(---\|)+$', l) for c in re.split(r'(?<!\\)\|', l.strip())[1:-1]]
    assert [c for c in back if c] == cells, 'cells changed'
    return t, rows


def main():
    apply = '--apply' in sys.argv
    only = {int(x) for x in sys.argv[sys.argv.index('--records') + 1].split(',')} if '--records' in sys.argv else None
    m = json.load(open(MAP))
    reg = json.load(open(ROOT / 'data/registry.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    by = collections.defaultdict(list)
    for s in m['spans']:
        if not only or s['n'] in only: by[s['n']].append(s)
    rep, tot = [], collections.Counter()
    for n, ss in sorted(by.items()):
        d = D[n]
        if d.get('status') != 'ACTIVE' or d.get('superseded_by_deposit_number'): continue
        p = ROOT / d['full_text_path'].lstrip('/'); L = p.read_text(encoding='utf-8').split('\n')
        done = []
        for s in sorted(ss, key=lambda s: -s['first']):
            t, rows = build(L, s)
            L = L[:s['first']] + t + L[s['last'] + 1:]
            done.append({'line': s['first'] + 1, 'header': rows[0], 'rows': len(rows) - 1, 'columns': len(rows[0]),
                         'empty_cells': sum(not x for r in rows for x in r), 'copy': s['copy']})
        done.reverse(); new = '\n'.join(L)
        tot['records'] += 1; tot['tables'] += len(done); tot['empty_cells_placed'] += sum(x['empty_cells'] for x in done)
        rep.append({'n': n, 'tables': done})
        if not apply: continue
        p.write_text(new, encoding='utf-8')
        h = hashlib.sha256(new.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
        rec = {'on': ON, 'method': 'structure from a second copy (published blog post); cells as seated',
               'tables_rebuilt': len(done), 'tables': done, 'hash_before': d.get('hash'), 'axn_before': d.get('axn'), 'ruled_by': RULING}
        d.setdefault('flat_tables_repaired', []).append(rec)
        d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
        d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
        d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
        if isinstance(d.get('body_status'), dict):
            d['body_status']['residual_chars'] = len(new)
        rm.touch(d, 'body_status', f'{len(done)} flattened table(s) rebuilt with the structure a second copy confirms '
                 '(published blog post); every cell as seated', was={'axn': rec['axn_before']}, now={'axn': d['axn']}, when=ON)
    if apply:
        json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
        json.dump({'generated': ON, 'ruling': RULING, 'source_map': str(MAP.relative_to(ROOT)), 'totals': dict(tot), 'records': rep},
                  open(ROOT / f'data/repair-maps/flat-tables-from-copies-{ON}.json', 'w'), ensure_ascii=False, indent=1)
    print(dict(tot))


if __name__ == '__main__':
    main()
