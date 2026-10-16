#!/usr/bin/env python3
"""reconvert_active_20261015.py — the published characters back into nine active records restored in July.

Ruling (Lee Sharks, 2026-10-15): "the ten active. and lets keep proceeding thru. the focus is on active,
non-duplicate records in general."

data/repair-maps/typographic-loss-2026-10-15.json maps the records whose body was recovered from a blog post with
html2text at its default, which replaces entity-encoded characters with ASCII stand-ins (· -> *, — -> --, curly
quotes straight, → -> ->). Ten are ACTIVE. Nine are re-converted here; #1168 ("Untitled") is not, because its seated
body is a different work (the DOI Registry v7.0 post) and stays on the wrong-body hold list.

Exact, not heuristic: for each record the July conversion is regenerated (same post, html2text default) and must
occur verbatim in the seated file; only that span is replaced, by the conversion with characters kept (unicode_snob)
and html2text's markdown escapes dropped where the post has none. Frontmatter, the Description / Methodology /
Falsification / Recovery-note apparatus are untouched. A record whose July conversion is not found verbatim is held.
New hash, glyph and AXN in the same hex and family; the change is recorded (text_reconverted, record_modification).

    python3 scripts/reconvert_active_20261015.py [--dry-run] [--superseded]

--superseded (2026-10-15, "lets fix all of that"): the same exact-span method on the records of the map that are not
ACTIVE (superseded editions and duplicate witnesses are indexable and read; the characters they lost are the same
loss). A record whose July conversion is no longer in the file verbatim (re-seated since) is held, as above.
"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from restore_from_blog import fetch, extract_post
from restore_wrong_bodies import to_md, unescape
import html2text
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-15'
RULING = 'Lee Sharks, 2026-10-15: "the ten active. and lets keep proceeding thru. the focus is on active, non-duplicate records in general"'
SKIP = {1168: 'seated body is a different work (DOI Registry v7.0); wrong-body hold'}
H0 = html2text.HTML2Text(); H0.body_width = 0          # the July conversion, regenerated to locate it


def main():
    dry = '--dry-run' in sys.argv
    m = json.load(open(ROOT / 'data/repair-maps/typographic-loss-2026-10-15.json'))
    reg = json.load(open(ROOT / 'data/registry.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    done, held = [], []
    for r in m['records']:
        n = r['deposit']
        if (r['status'] != 'ACTIVE') != ('--superseded' in sys.argv):
            continue
        if n in SKIP:
            held.append({'n': n, 'why': SKIP[n]}); continue
        if D[n].get('text_reconverted'):
            continue
        d = D[n]; tp = ROOT / d['full_text_path'].lstrip('/'); t = tp.read_text(encoding='utf-8')
        _, body = extract_post(fetch(r['source']).decode('utf-8', 'replace'))
        old = H0.handle(body or '').strip()
        if t.count(old) != 1:
            held.append({'n': n, 'why': f'July conversion found {t.count(old)}x, not once'}); continue
        new_md = unescape(to_md(body or ''), body or '').strip()
        new = t.replace(old, new_md, 1)
        done.append({'n': n, 'chars_before': len(t), 'chars_after': len(new)})
        if dry:
            continue
        tp.write_text(new, encoding='utf-8')
        h = hashlib.sha256(new.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
        rec = {'on': ON, 'source': r['source'], 'hash_before': d['hash'], 'axn_before': d['axn'], 'ruled_by': RULING,
               'why': ('the work segment, converted in July with html2text at its default (ASCII stand-ins for '
                       'entity-encoded characters), converted again with the characters kept; apparatus untouched')}
        d['text_reconverted'] = rec
        d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
        d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
        d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
        if isinstance(d.get('body_status'), dict):
            d['body_status']['residual_chars'] = len(new)
        rm.touch(d, 'body_status', 'work text converted again with the published characters kept (· — “ ” → etc.)',
                 was={'axn': rec['axn_before']}, now={'axn': d['axn']}, when=ON)
    if not dry and done:
        (ROOT / 'data/registry.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    print('reconverted', len(done), done); print('held', len(held)); print('held', held)


if __name__ == '__main__':
    main()
