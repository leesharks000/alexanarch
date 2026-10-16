#!/usr/bin/env python3
"""repair_from_readings_20261015.py — the repairs the six repair readings support (data/repair-maps/readings/RP01–RP06).

Rulings (Lee Sharks, 2026-10-15): repair "broken, missing, and mislabelled files / and citations"; focus on active,
non-duplicate records; "never duplicate"; readers "long as they have provenance". Each reading is verified
(RP0x.verified.json: quotes verbatim at their lines, read coverage, transcript audit of lines actually returned).
Only verdicts with a single reading are applied; every needs_ruling is left and listed on the ruling sheet.

TITLES (registry title; the deposit's own heading governs):
  #155 the subtitle alone -> main title + subtitle      #696 stray "# " from joined heading lines
  #698 "Adversarial AI Discourse" -> "…Agent Architecture" (the text's own title field; "Discourse" occurs nowhere)
  #884 the §0 heading "0. Status declaration" welded on   #1002 the capture heading " Description (as recorded by DataCite)" welded on
  #1420 the title of a different essay -> the deposit's own heading (line 36)
CONTENT TYPES: #121 Scholarly essay (genre note) · #341 Episode declaration · #344 Metadata packet · #745 Work plan
DUPLICATES (superseded duplicate witnesses of the standing record, the archive's form for every duplicate):
  #972 -> #57 · #995 -> #97 · #1343 -> #800 · #1348 -> #52 · #1366 -> #714 · #1368 -> #599 · #1370 -> #105
ATTACHMENTS ("a referenced attachment must be a clickable link from the body", 2026-09-12):
  #1488 the 18 listed workplan files, bare paths -> links · #1573 collapse_diagnostic.py linked · #1097 the atlas
  (data/specs/AXN-DATAFLOW-MAP-v0.2.md) and its v0.1 predecessor linked · #1568 the paper PDF (the record's own
  sidecar names it) linked · #379 the schema image restored as an image (the post embeds it; the conversion kept an
  empty link) · #1362 BOOK_OF_LIFE.md and FOOTNOTES.md, named by the record as companions, copied from the
  secret-book-of-walt repository (commit 6cdad74) into data/attachments/ea-sbw-01/ and linked.
ARCHIVE-MADE TRUNCATIONS:
  licence cells of the generated seat tables (#1559, #1560, #1562) cut at 46 characters -> the seat's own
  data/corpora/<seat>/source.json licence string, only where the cut cell is a prefix of it;
  registry keyword lists cut mid-word (#1323 from the Zenodo pre-termination XML export, #1338 and #1342 from the
  DataCite backup of the record's own DOI).
A record whose text changes gets a new hash and AXN (same hex and family); every change is recorded.
"""
import hashlib, json, pathlib, re, shutil, sys, tarfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-15'
RULING = ('Lee Sharks, 2026-10-15: repair "broken, missing, and mislabelled files / and citations"; readers "long as '
          'they have provenance" — data/repair-maps/readings/')
READ = {}
for b in ('RP01', 'RP02', 'RP03', 'RP04', 'RP05', 'RP06'):
    for e in json.load(open(ROOT / f'data/repair-maps/readings/{b}.json'))['deposits']:
        READ[e['deposit']] = (b, e)
TITLES = {155: None, 696: None, 698: None, 884: None, 1002: None, 1420: None}       # value from the reading
CTYPES = {121: 'Scholarly essay (genre note)', 341: 'Episode declaration', 344: 'Metadata packet', 745: 'Work plan'}
DUPS = {972: 57, 995: 97, 1343: 800, 1348: 52, 1366: 714, 1368: 599, 1370: 105}


def reglyph(d, text):
    h = hashlib.sha256(text.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
    b = {'hash': d.get('hash'), 'axn': d.get('axn')}
    d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
    d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
    d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
    if isinstance(d.get('body_status'), dict):
        d['body_status']['residual_chars'] = len(text)
    return b


def textfix(d, fn, what):
    tp = ROOT / d['full_text_path'].lstrip('/'); t = tp.read_text(encoding='utf-8'); new = fn(t)
    if new == t:
        return False
    tp.write_text(new, encoding='utf-8'); b = reglyph(d, new)
    d.setdefault('readings_repaired', []).append({'on': ON, 'what': what, 'hash_before': b['hash'], 'axn_before': b['axn']})
    rm.touch(d, 'body_status', what, was={'axn': b['axn']}, now={'axn': d['axn']}, when=ON)
    return True


def datacite_subjects(doi):
    j = json.load(open(ROOT / 'data/datacite-full-backup.json')); out = []
    def walk(o):
        if isinstance(o, dict):
            a = o.get('attributes') if isinstance(o.get('attributes'), dict) else o
            if str(a.get('doi') or o.get('id') or '').lower() == doi and a.get('subjects') and not out:
                out.extend(s['subject'] for s in a['subjects'] if s.get('subject'))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(j); return out


def zenodo_xml_subjects(rec):
    with tarfile.open(ROOT / 'data/zenodo-xml-pretermination-2026-06-07.tar.gz') as tf:
        for m in tf.getmembers():
            if m.isfile() and rec in m.name:
                x = tf.extractfile(m).read().decode('utf-8', 'replace')
                return [re.sub(r'<[^>]+>', '', s) for s in re.findall(r'<subject[^>]*>.*?</subject>', x)]
    return []


def complete_keywords(d, full, src):
    kw = list(d.get('keywords') or []); cut = kw[-1] if kw else ''
    i = next((k for k, s in enumerate(full) if s.startswith(cut) and s != cut), None)
    if i is None:
        return False
    new = kw[:-1] + full[i:]
    d['keywords'] = new
    rm.touch(d, 'keywords', f'keyword list was cut mid-word at intake ("{cut}"); completed from {src}', was=kw, now=new, when=ON)
    return True


def main():
    reg = json.load(open(ROOT / 'data/registry.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    ret = json.load(open(ROOT / 'data/retired-records.json')); done = []
    for n in TITLES:
        d = D[n]; v = READ[n][1]['value']; was = d['title']
        if v and v != was:
            d['title_before_repair'] = was; d['title'] = v
            rm.touch(d, 'title', f'registry title corrected to the deposit\'s own heading (reading {READ[n][0]})', was=was, now=v, when=ON)
            done.append(('title', n))
    for n, v in CTYPES.items():
        d = D[n]; was = d.get('content_type')
        d['content_type'] = v
        rm.touch(d, 'content_type', f'content_type did not describe the text (reading {READ[n][0]})', was=was, now=v, when=ON)
        done.append(('content_type', n))
    for n, t in DUPS.items():
        d, T = D[n], D[t]
        assert d['status'] == 'ACTIVE' and T['status'] == 'ACTIVE' and not T.get('superseded_by_deposit_number'), n
        why = READ[n][1]['note'][:240]
        was = {'status': d['status'], 'superseded_by_deposit_number': d.get('superseded_by_deposit_number')}
        d['status'] = 'SUPERSEDED'; d['superseded_by_deposit_number'] = t
        d['duplicate_note'] = f'DUPLICATE ({ON}, reading {READ[n][0]}): the record of standing is #{t}. {why}'
        d['superseded_reason'] = f'Duplicate witness of the same work: the record of standing is #{t}.'
        d.setdefault('body_status', {})['retired'] = {'class': 'superseded', 'resolves_to': t, 'declared': ON, 'indexable': True,
            'ruled_by': RULING, 'note': ('Superseded, not a stub: indexable (ruling 2026-10-15). The page carries a banner '
            'before the body naming the current version to cite, and an axn:retired marker; its canonical is its own URL.')}
        rm.touch(d, 'status', f'duplicate of #{t} (reading {READ[n][0]}); made a superseded duplicate witness',
                 was=was, now={'status': 'SUPERSEDED', 'superseded_by_deposit_number': t}, when=ON)
        ret['records'][str(n)] = {'class': 'superseded', 'resolves_to': t, 'title': T['title'], 'axn': T['axn'], 'declared': ON}
        done.append(('duplicate', n))
    ret['count'] = len(ret['records'])
    # attachments
    A = lambda p: f'[{pathlib.Path(p).name}](/{p})'
    if textfix(D[1488], lambda t: re.sub(r'(?m)^- (data/attachments/operative-semiotics-idp/[^\s]+)$', lambda m: '- ' + A(m.group(1)), t),
               '18 attached workplan files linked from the body (were bare paths)'):
        done.append(('attach', 1488))
    def f1573(t):
        if 'collapse_diagnostic.py](' in t:
            return t
        u = 'https://alexanarch.org/data/attachments/ea-lo-collapse-diagnostic-01/EA-LO-COLLAPSE-DIAGNOSTIC-01.md'
        i = t.rfind(u)                      # the Files list at the end, not the attached-file header
        j = t.find('\n', i)
        return t[:j] + '\n- [collapse_diagnostic.py](/data/attachments/ea-lo-collapse-diagnostic-01/collapse_diagnostic.py) — reference implementation of Part II\'s black-box panel' + t[j:]
    if textfix(D[1573], f1573, 'reference implementation collapse_diagnostic.py linked from the body'):
        done.append(('attach', 1573))
    def f1097(t):
        if 'AXN-DATAFLOW-MAP-v0.2.md](' in t:
            return t
        return t.rstrip('\n') + ('\n\n**Attached:** [AXN Dataflow Atlas v0.2](/data/specs/AXN-DATAFLOW-MAP-v0.2.md) · predecessor '
                                 '[v0.1](/data/specs/archive/AXN-DATAFLOW-MAP-v0.1-superseded-by-v0.2.md)\n')
    if textfix(D[1097], f1097, 'the atlas (data/specs/AXN-DATAFLOW-MAP-v0.2.md) and its predecessor linked from the body'):
        done.append(('attach', 1097))
    def f1568(t):
        u = 'https://www.provenanceerasure.org/rebuttal-as-warrant/EA-MMRS-RAW-01-v1.2.pdf'
        return t if u in t else t.rstrip('\n') + f'\n\n**The full paper:** [EA-MMRS-RAW-01 v1.2 (PDF)]({u})\n'
    if textfix(D[1568], f1568, 'the full paper (PDF named in the record\'s sidecar) linked from the body'):
        done.append(('attach', 1568))
    if textfix(D[379], lambda t: re.sub(r'\*\*\[\]\((https://blogger\.googleusercontent\.com/img/[^)\s]+)\)', r'**[![](\1)](\1)', t, count=1),
               'schema image restored as an image (the post embeds it; the conversion had kept an empty link)'):
        done.append(('attach', 379))
    dst = ROOT / 'data/attachments/ea-sbw-01'; dst.mkdir(parents=True, exist_ok=True)
    for f in ('BOOK_OF_LIFE.md', 'FOOTNOTES.md'):
        shutil.copy2(f'/home/claude/sbw/docs/{f}', dst / f)
    def f1362(t):
        if 'ea-sbw-01/BOOK_OF_LIFE.md' in t:
            return t
        return t.replace('`docs/BOOK_OF_LIFE.md`', '[docs/BOOK_OF_LIFE.md](/data/attachments/ea-sbw-01/BOOK_OF_LIFE.md)', 1) \
                .replace('`docs/FOOTNOTES.md`', '[docs/FOOTNOTES.md](/data/attachments/ea-sbw-01/FOOTNOTES.md)', 1)
    if textfix(D[1362], f1362, 'companion files BOOK_OF_LIFE.md and FOOTNOTES.md (secret-book-of-walt @6cdad74) attached and linked'):
        done.append(('attach', 1362))
    # licence cells
    for n in (1559, 1560, 1562):
        def fl(t):
            lines = t.split('\n')
            for i, l in enumerate(lines):
                m = re.search(r'\|\s*\*\*([a-z0-9_-]+)\*\*\s*\|', l)
                if not m or not l.lstrip().startswith('|'):
                    continue
                sj = ROOT / f'data/corpora/{m.group(1)}/source.json'
                if not sj.exists():
                    continue
                lic = json.load(open(sj)).get('license') or ''
                cells = [c.strip() for c in l.strip().strip('|').split('|')]
                for c in cells:
                    if len(c) >= 30 and lic.startswith(c) and c != lic:
                        lines[i] = l.replace(c, lic, 1)
            return '\n'.join(lines)
        if textfix(D[n], fl, 'seat-table licence cells cut at 46 characters completed from each seat\'s source.json'):
            done.append(('licence', n))
    # keywords
    if complete_keywords(D[1323], zenodo_xml_subjects('18674147'), 'the Zenodo pre-termination XML export (record 18674147)'):
        done.append(('keywords', 1323))
    if complete_keywords(D[1338], datacite_subjects('10.5281/zenodo.18446646'), 'the DataCite backup of 10.5281/zenodo.18446646'):
        done.append(('keywords', 1338))
    if complete_keywords(D[1342], datacite_subjects('10.5281/zenodo.19099748'), 'the DataCite backup of 10.5281/zenodo.19099748'):
        done.append(('keywords', 1342))
    json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
    json.dump(ret, open(ROOT / 'data/retired-records.json', 'w'), ensure_ascii=False, indent=2)
    print(done)


if __name__ == '__main__':
    main()
