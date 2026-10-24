#!/usr/bin/env python3
"""repair_missing_fields_20261024.py — two registry fields missing from live records, restored from what the records hold.

Found 2026-10-24 while seating the records the seat map had not reached (Lee Sharks: "yes, lets assign the seats if
that makes sense"); repair scope as ruled 2026-10-15, "broken, missing, and mislabelled files".

A. `status` absent: #1441, #1442, #1445, #1446, #1447 (entered by hand 2026-08-09/10, no minted_at). Each is a live
   record with its full text; no record supersedes, duplicates or withdraws any of them; their neighbours #1443 and
   #1444 are ACTIVE; and every consumer that counts active records (the HF build, the seat map's own count) already
   treated them as active. #1445's title, "the batch was withdrawn", names a batch the tether records, not the record.
   Set: ACTIVE.
B. `full_text_path` absent: #1050, #1056, #1057, #1058. Each record's text is on disk and hashes exactly to the
   record's own `hash`: the path is set to that file (data/texts/ preferred where both hold the bytes).
C. #1056's description was a stub written while its text was unlinked ("The deposited body is structured data rather
   than prose. A description composed from a reading of the work belongs to the description/wiki review stream."). It
   is replaced by the work's own Description section, first paragraph, verbatim with markup stripped (the 2026-10-15
   convention: the author's own words, never composed); the stub kept as description_before_repair. Applied in the
   same session by an inline step equivalent to describe_1056() below.
Each change recorded with record_modification.
"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm

ON = '2026-10-24'
STATUS = [1441, 1442, 1445, 1446, 1447]
PATHS = [1050, 1056, 1057, 1058]


def main():
    regp = ROOT / 'data/registry.json'
    reg = json.loads(regp.read_text()); D = {d['deposit_number']: d for d in reg['deposits']}
    for n in STATUS:
        d = D[n]; assert 'status' not in d
        d['status'] = 'ACTIVE'
        rm.touch(d, 'status', 'status field absent (entered by hand 2026-08-09/10); a live record with its full text, '
                 'superseded, duplicated and withdrawn by none: ACTIVE', was='(absent)', now='ACTIVE', when=ON)
    for n in PATHS:
        d = D[n]; assert not d.get('full_text_path')
        cands = [f"data/texts/AXN-{d['hex']}-text.md", f'data/deposits/AXN-{n}.md', f"data/deposits/AXN-{d['hex']}.md"]
        hit = next(c for c in cands if (ROOT / c).exists() and hashlib.sha256((ROOT / c).read_bytes()).hexdigest() == d['hash'])
        d['full_text_path'] = '/' + hit
        rm.touch(d, 'full_text_path', "path absent; the record's text found on disk, its sha256 equal to the record hash",
                 was='(absent)', now='/' + hit, when=ON)
        print(n, '->', hit)
    if '--apply' in sys.argv:
        regp.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
        print('applied')


def describe_1056(D):
    import re
    d = D[1056]
    t = (ROOT / d['full_text_path'].lstrip('/')).read_text(encoding='utf-8')
    first = t.split('## Description\n', 1)[1].split('\n## ', 1)[0].strip().split('\n\n')[0].strip()
    plain = re.sub(r'[*_`]+', '', first)
    was = d['description']; d['description_before_repair'] = was; d['description'] = plain
    d['description_source'] = {'on': ON, 'source': "the work's own Description section, first paragraph, verbatim (markup stripped)",
                               'ruled_by': 'Lee Sharks, 2026-10-15: repair standard "the text as he published it"'}
    rm.touch(d, 'description', "stub description replaced with the work's own Description section, first paragraph",
             was=was, now=plain, when=ON)


if __name__ == '__main__':
    main()
