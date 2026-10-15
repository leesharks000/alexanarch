#!/usr/bin/env python3
"""repair_links_20261015.py — broken links in active records: placeholder record links and chat-URL contents links.

Ruling (Lee Sharks, 2026-10-15): repair "broken, missing, and mislabelled files / and citations"; focus on active,
non-duplicate records; "lets proceed".

1. /s/records/0/. The archive's link tooling wrote https://(www.)alexanarch.org/s/records/0/ where it could not
   resolve a target (#985, #986, #1012, #1359). An occurrence is repointed only when its own element names the
   target: the anchor text, or the label of the same data object. Designations resolve uniquely in the registry:
     EA-RBT-01 / The Writable Retrieval Basin -> #695    EA-HK-01 -> #76    EA-SPXI-WEB-01 / SPXI for Websites -> #72
     The Network Is the Poem -> #1191    "Holographic Kernel" (the theory, #1012) -> #76 (EA-HK-01, its specification)
   #1359 is the holographickernel.org landing page source; its bare sameAs is EA-HK-01 -> #76. Every other bare
   occurrence (sameAs / anchoredBy lists in #985 and #986 naming nothing) is left as it is and listed.
2. CONTENTS LINKS. Tables of contents in #317, #339, #354 link each section to https://claude.ai/chat/<id>#<anchor>
   (the session the text was drafted in), which resolves for no reader. Each becomes the in-page #<anchor>.
   NOT changed: figure images pointing at claude.ai/chat/<file> (#502, #507, #509) — the published posts carry the
   same links, and which uncaptioned Blogger image is which figure is not determinable from the post.

New hash, glyph and AXN per changed record (same hex and family); links_repaired records what changed.

    python3 scripts/repair_links_20261015.py --dry-run | --apply
"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-15'
RULING = 'Lee Sharks, 2026-10-15: repair "broken, missing, and mislabelled files / and citations"; "lets proceed"'
TARGETS = [(re.compile(r'EA-RBT-01|Writable Retrieval Basin', re.I), 695), (re.compile(r'EA-HK-01|Holographic Kernel', re.I), 76),
           (re.compile(r'EA-SPXI-WEB-01|SPXI for Websites', re.I), 72), (re.compile(r'The Network Is the Poem', re.I), 1191)]
R0 = re.compile(r'(https://(?:www\.)?alexanarch\.org)/s/records/0/')
CHAT = re.compile(r'\]\(https://claude\.ai/chat/[0-9a-f-]{36}(#[^)\s]+)\)')


def target_for(s, m):
    """the target named by this occurrence's own element: anchor text after it, or a label on its line"""
    after = re.match(r'[^>]*>([^<]{3,160})<', s[m.end():m.end() + 400])
    line = s[s.rfind('\n', 0, m.start()) + 1: s.find('\n', m.end())]
    for txt in ([after.group(1)] if after else []) + [line]:
        hits = {t for rx, t in TARGETS if rx.search(txt)}
        if len(hits) == 1:
            return hits.pop()
    return None


def main():
    apply = '--apply' in sys.argv
    reg = json.load(open(ROOT / 'data/registry.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    report = {}
    for n in (985, 986, 1012, 1359, 317, 339, 354):
        d = D[n]; tp = ROOT / d['full_text_path'].lstrip('/'); t = tp.read_text(encoding='utf-8')
        done, left = [], 0
        out, pos = [], 0
        for m in R0.finditer(t):
            tg = target_for(t, m)
            if tg is None and n == 1359 and 'sameAs' in t[max(0, m.start() - 40):m.start()]:
                tg = 76
            out.append(t[pos:m.start()])
            if tg:
                out.append(f'{m.group(1)}/s/records/{tg}/'); done.append(tg)
            else:
                out.append(m.group(0)); left += 1
            pos = m.end()
        out.append(t[pos:]); new = ''.join(out)
        new, nchat = CHAT.subn(r'](\1)', new)
        if new == t:
            continue
        report[n] = {'records0_repointed': done, 'records0_left_bare': left, 'contents_links_made_in_page': nchat}
        if not apply:
            continue
        tp.write_text(new, encoding='utf-8')
        h = hashlib.sha256(new.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
        rec = dict(report[n], on=ON, hash_before=d.get('hash'), axn_before=d.get('axn'), ruled_by=RULING)
        d['links_repaired'] = rec
        d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
        d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
        d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
        rm.touch(d, 'body_status', f'broken links repaired: {len(done)} placeholder record links repointed, '
                 f'{nchat} contents links made in-page', was={'axn': rec['axn_before']}, now={'axn': d['axn']}, when=ON)
    if apply and report:
        json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
    print(json.dumps(report))


if __name__ == '__main__':
    main()
