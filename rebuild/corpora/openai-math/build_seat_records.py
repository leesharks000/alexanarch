import re, json, pathlib, hashlib, collections, sys
R = pathlib.Path('repo'); OUT = pathlib.Path('seat'); COMMIT = 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb'
tree = {}
for l in open('SOURCE-TREE.sha256', encoding='utf-8'):
    h, p = l.rstrip('\n').split('  ', 1); tree[p] = h
TOP = ['README.md', 'CONTENTS.md', 'history.md', 'LICENSE', 'overview.pdf', 'overview.tex']
LEANTOP = ['lean/README.md', 'lean/LICENSE', 'lean/formalization.yaml', 'lean/lakefile.lean', 'lean/lake-manifest.json', 'lean/lean-toolchain', 'lean/OAI.lean']
PREF = ['preprints/', 'reasoning_traces/', 'lean/docs/', 'lean/ComparatorChallenges/', 'lean/patches/']
seated = [p for p in tree if p in TOP or p in LEANTOP or any(p.startswith(x) for x in PREF)]
seated.sort()
missing = [p for p in TOP + LEANTOP if p not in tree]
size = sum((R / p).stat().st_size for p in seated)
print(len(seated), 'seated files', round(size / 1e6, 1), 'MB; missing top:', missing)
json.dump(seated, open('seated-paths.json', 'w'))
# manuscripts table from CONTENTS.md
C = (R / 'CONTENTS.md').read_text(encoding='utf-8')
rows, fam = [], None
for l in C.split('\n'):
    m = re.match(r'\*\*(\d{3})\. (.+?)\*\* ?(.*)$', l)
    if m:
        fam = (m.group(1), m.group(2).rstrip('.'), bool(re.search(r'\(\[Lean\]\(lean/docs/\d+\.md\)\)', l)))
        continue
    m = re.match(r'&emsp;\[(.+?)\]\((preprints/.+?\.pdf)\)', l)
    if m and fam:
        path = m.group(2); d = path.split('/')[1]
        dm = re.search(r'-((?:January|February|March|April|May|June|July|August|September|October|November|December)-\d{1,2}-\d{4})$', d)
        rows.append({'family': fam[0], 'family_title': fam[1], 'family_lean_scope_note': fam[2], 'manuscript': re.sub(r'\s+', ' ', m.group(1)).strip(),
                     'date_in_path': dm.group(1) if dm else '', 'pdf': path, 'pdf_in_tree': path in tree})
fams = {r['family'] for r in rows}
H = (R / 'history.md').read_text(encoding='utf-8')
wd = re.findall(r'^- (.+)$', H.split('**Withdrawals**')[1].split('**Fixes**')[0], re.M)
for r in rows: r['withdrawn_2026_10_07'] = any(w.strip() == r['manuscript'] for w in wd)
print(len(rows), 'manuscripts in', len(fams), 'families;', sum(r['family_lean_scope_note'] for r in rows), 'rows in families with a Lean note;',
      sum(r['withdrawn_2026_10_07'] for r in rows), 'withdrawn matched of', len(wd), '; pdf missing from tree:', sum(not r['pdf_in_tree'] for r in rows))
json.dump(rows, open('manuscripts.json', 'w'), ensure_ascii=False)
# ── the table, one row per manuscript directory ──
inmap = {r['pdf'].split('/')[1]: r for r in rows}
assert all(r['pdf_in_tree'] for r in rows), [r for r in rows if not r['pdf_in_tree']]
superseded = {}
for d in sorted(x.name for x in (R / 'preprints').iterdir() if x.is_dir()):
    t = (R / 'preprints' / d / 'README.md').read_text(encoding='utf-8')
    for prev in re.findall(r'\[previous version\]\(\.\./([^/]+)/', t): superseded[prev] = d
table = []
for d in sorted(x.name for x in (R / 'preprints').iterdir() if x.is_dir()):
    t = (R / 'preprints' / d / 'README.md').read_text(encoding='utf-8')
    h1 = re.match(r'# \[(.+?)\]\((.+?)\)', t)
    title = h1.group(1) if h1 else ''
    wd_ = title.startswith('Withdrawal notice: ')
    au = re.search(r'\*\*Author:\*\* (.+?)\s*$', t, re.M) or re.search(r'^(OpenAI)\s*$', t, re.M)
    dt = re.search(r'\*\*Date:\*\* (.+?)\s*$', t, re.M)
    m = inmap.get(d)
    if wd_: status = 'withdrawn 2026-10-06 (notice in place; pre-withdrawal manuscript at adc7f124, seated under original-adc7f124/)'
    elif m: status = 'current (in CONTENTS.md)'
    elif d in superseded: status = 'previous version, superseded by ' + superseded[d]
    else: status = 'not in CONTENTS.md'
    table.append({'directory': d, 'title': title.replace('Withdrawal notice: ', ''), 'author_line': au.group(1) if au else '',
                  'date': dt.group(1) if dt else (re.search(r'Withdrawn on (.+?)\.\*\*', t).group(1) if wd_ else ''),
                  'family': m['family'] if m else '', 'family_title': m['family_title'] if m else '',
                  'family_has_lean_scope_note': (m['family_lean_scope_note'] if m else ''), 'status': status,
                  'pdf': ('preprints/' + d + '/' + h1.group(2)) if h1 else ''})
c = collections.Counter(x['status'].split(' (')[0].split(', superseded')[0] for x in table)
print(len(table), 'directories;', dict(c), '; author lines:', collections.Counter(x['author_line'] for x in table))
json.dump(table, open('table.json', 'w'), ensure_ascii=False)
