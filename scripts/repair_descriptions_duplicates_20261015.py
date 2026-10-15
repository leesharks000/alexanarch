#!/usr/bin/env python3
"""repair_descriptions_duplicates_20261015.py — descriptions written from wrong bodies; duplicates made legible.

Rulings (Lee Sharks, 2026-10-15): repair "broken, missing, and mislabelled files / and citations"; repair standard
"the text as he published it"; and, of today's restorations, "make sure youre not duplicating something that
already exists elsewhere".

A. DUPLICATES. A duplication check of every restoration made today (each recovered post's 8-word shingles against
   every seated text) found seven records whose newly seated text already stands, whole, at an earlier record:
     #891 -> #368 (1.00)  #892 -> #467 (1.00)  #898 -> #572 (1.00)  #906 -> #15 (1.00)  #1023 -> #199 (1.00)
     #1252 -> #404 (0.93, the Charter)   #1277 -> #403 (0.94, Damascus Dancings; already carried a DUPLICATE MINT
     note while ACTIVE)
   #891–#906 were minted 2026-06-23 for Zenodo DOIs whose works were already deposited (#891's 18342107 is the
   concept DOI of #368's 18342108). They are made what the archive makes every duplicate mint (#1138, #1181,
   #1278): SUPERSEDED, a duplicate witness pointing at the record of standing, the page carrying the cite-instead
   banner (indexable, canonical self, ruling 2026-10-15). Their bodies keep the published text seated today.

B. DESCRIPTIONS. Each replacement is the author's own words, verbatim, never composed:
   the deposit's own DataCite abstract (#891, #1023, #1025); the Zenodo metadata of the triptych (#406), which
   describes each document in turn (Document A -> #402, B -> #1277, C -> #1252); or the work's own opening —
   #892 its Abstract, #898 its Executable Kernel, #906 its Preface, #325 the schema's opening lines, #1264 the
   packet's header lines, #1170 the poem itself (also its DataCite abstract). The replaced description is kept
   (description_before_repair) and the change recorded with record_modification.

    python3 scripts/repair_descriptions_duplicates_20261015.py --apply
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm

ON = '2026-10-15'
RULING = ('Lee Sharks, 2026-10-15: "make sure youre not duplicating something that already exists elsewhere"; '
          'repair standard "the text as he published it"')
DUP = {891: (368, 1.00), 892: (467, 1.00), 898: (572, 1.00), 906: (15, 1.00), 1023: (199, 1.00),
       1252: (404, 0.93), 1277: (403, 0.94)}


def body(D, n):
    t = (ROOT / D[n]['full_text_path'].lstrip('/')).read_text(encoding='utf-8')
    return t[t.find('\n\n---\n\n') + 7:].split('\n## Appendix —')[0]


def plain(s):
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'[*_#`]+', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def para_after(text, marker, n=1):
    i = text.find(marker); assert i >= 0, marker
    rest = text[i + len(marker):].strip('\n *')
    paras = [p for p in re.split(r'\n\s*\n', rest) if plain(p)]
    return plain(' '.join(paras[:n]))


def datacite_abstract(doi):
    j = json.load(open(ROOT / 'data/datacite-full-backup.json'))
    found = []
    def walk(o):
        if isinstance(o, dict):
            a = o.get('attributes') if isinstance(o.get('attributes'), dict) else o
            if str(a.get('doi') or o.get('id') or '').lower() == doi and a.get('descriptions'):
                found.extend(x['description'] for x in a['descriptions'] if x.get('descriptionType') == 'Abstract')
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(j)
    return plain(re.sub(r'<[^>]+>', ' ', found[0]))


def descriptions(D):
    t406 = (ROOT / D[406]['full_text_path'].lstrip('/')).read_text(encoding='utf-8')
    doc = lambda k: plain(re.search(r'\*\*' + k + r'.*?\*\*.*?\n(.*?)\n\s*\n', t406, re.S).group(1))
    out = {
        891: (datacite_abstract('10.5281/zenodo.18342107'), 'DataCite abstract of the deposit\'s DOI 10.5281/zenodo.18342107'),
        1023: (datacite_abstract('10.5281/zenodo.20675199'), 'DataCite abstract of the deposit\'s DOI 10.5281/zenodo.20675199'),
        1025: (datacite_abstract('10.5281/zenodo.20691466'), 'DataCite abstract of the deposit\'s DOI 10.5281/zenodo.20691466'),
        402: (doc('Document A: Epistle to the Human Diaspora'), 'the triptych\'s Zenodo metadata (#406), Document A'),
        1277: (doc('Document B: Damascus Dancings: Heteronym Provenance'), 'the triptych\'s Zenodo metadata (#406), Document B'),
        1252: (doc('Document C: Charter: Commission of the Immanent Turning'), 'the triptych\'s Zenodo metadata (#406), Document C'),
        892: (para_after(body(D, 892), 'Abstract'), 'the work\'s own Abstract, first paragraph'),
        898: (para_after(body(D, 898), 'EXECUTABLE KERNEL'), 'the work\'s own Executable Kernel, first paragraph'),
        906: (para_after(body(D, 906), '## PREFACE'), 'the work\'s own Preface, first paragraph'),
        325: (para_after(body(D, 325), '## Canonical Visual Schema Specification', 2), 'the schema\'s own opening lines'),
        1264: ('Metadata Packet for AI Indexing — The Meaning Economy Is Now Possible: Provenance Documentation. '
               + para_after(body(D, 1264), 'Provenance Documentation', 1), 'the packet\'s own header lines'),
        1170: (plain(body(D, 1170).split('\n---\n')[0]), 'the poem itself (verbatim also the DataCite abstract of 10.5281/zenodo.18512288)'),
    }
    return out


def main():
    regp = ROOT / 'data/registry.json'; retp = ROOT / 'data/retired-records.json'
    reg = json.loads(regp.read_text()); D = {d['deposit_number']: d for d in reg['deposits']}
    ret = json.loads(retp.read_text())
    desc = descriptions(D)
    for n, (s, src) in desc.items():
        print(f'#{n} [{src}] {s[:160]}')
    if '--apply' not in sys.argv:
        return
    for n, (t, c) in DUP.items():
        d = D[n]; T = D[t]
        assert d['status'] == 'ACTIVE' and T['status'] == 'ACTIVE' and not T.get('superseded_by_deposit_number')
        was = {k: d.get(k) for k in ('status', 'superseded_by_deposit_number', 'superseded_reason', 'duplicate_note')}
        d['status'] = 'SUPERSEDED'; d['superseded_by_deposit_number'] = t
        if was['duplicate_note']:
            d['duplicate_note_before_repair'] = was['duplicate_note']
        d['duplicate_note'] = (f'DUPLICATE ({ON} duplication check; containment {c:.2f}): the text seated here today, the '
                               f'published post, already stands whole at #{t}, which is the record of standing.')
        d['superseded_reason'] = (f'Duplicate witness of the same work: the record of standing is #{t}. Found {ON} when '
                                  'every restoration of the day was checked against every seated text.')
        d.setdefault('body_status', {})['retired'] = {
            'class': 'superseded', 'resolves_to': t, 'declared': ON, 'indexable': True, 'ruled_by': RULING,
            'note': ('Superseded, not a stub: indexable (ruling 2026-10-15). The page carries a banner before the body '
                     'naming the current version to cite, and an axn:retired marker; its canonical is its own URL. '
                     'The URL is kept; the record is not deleted.')}
        rm.touch(d, 'status', f'duplicate of #{t} (containment {c:.2f}); made a superseded duplicate witness',
                 was=was, now={'status': 'SUPERSEDED', 'superseded_by_deposit_number': t}, when=ON)
        ret['records'][str(n)] = {'class': 'superseded', 'resolves_to': t, 'title': T['title'], 'axn': T['axn'],
                                  'declared': ON}
    for n, (s, src) in desc.items():
        d = D[n]; was = d.get('description')
        d['description_before_repair'] = was
        d['description'] = s
        d['description_source'] = {'on': ON, 'source': src, 'ruled_by': RULING}
        rm.touch(d, 'description', f'description replaced with the author\'s own words ({src}); the previous one '
                 'was written from a wrong body or described the record\'s pre-restoration state', was=was, now=s, when=ON)
    ret['count'] = len(ret['records'])
    regp.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    retp.write_text(json.dumps(ret, ensure_ascii=False, indent=2))
    print('applied: duplicates', list(DUP), '| descriptions', list(desc), '| retired', ret['count'])


if __name__ == '__main__':
    main()
