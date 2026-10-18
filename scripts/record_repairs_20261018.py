#!/usr/bin/env python3
"""record_repairs_20261018.py — three record repairs found while reading the archive for the prediction index.

Ruling (Lee Sharks, 2026-10-18, 00:52): "y thats mislabelled. search alexanarch and blog for 3.0 ... theres also an
issue where each of the hexagonal license specs points to each other as superseded ... check what else is in the
archive ... probably change title"; and on the repairs proposed from that search (01:18): "adopted for all". Repair
scope (2026-10-15): broken, missing and mislabelled files and citations; a record's blog text is the post of the
record's own date; nothing seated twice. Follows restore_wrong_bodies.py: the previous body retained as an appendix
(non-destruction), new hash and glyph, AXN recomposed in the same hex and family, a remediation note per record.

1. #1358 "Hexagonal Contributor License v3.0 — Rhys Owens — Lunar Arm — Full Unified License" (DOI 19673630). Its
   seated body is the essay "Rhys Owens — The Lunar Arm of New Human" (blog, 2025-10-13), not the licence. The v3.0
   text is in neither the archive nor the blog; the one witness is its row in the knowledge-graph post of 2026-04-25.
   The record becomes metadata-only (the licence's identity and that witness), the essay retained as appendix. The
   essay, seated nowhere as its own record (only as appendices of #1356 and #1358), is minted as its own deposit by
   the issue body written beside this script (data/issue-bodies/LUNAR-ARM-ESSAY-2025-issue.md).
2. The Hexagonal Licensing Protocol: #66 is titled v1.0 but holds the v2.0 text (the blog post was overpasted with
   v2.0; v1.0's text is recovered nowhere); #1181 and #1182 hold the same v2.0 text from that one post; #1181 and
   #1182 both name #66 as their successor, and #1182 names #66 and #1181 as earlier versions collapsed under it. Now:
   #66 is the v1.0 record, its text marked not recovered, the v2.0 text retained as appendix, superseded by the v2.0
   head #1182; #1182 is the v2.0 head (ACTIVE); #1181 is a second deposit of the same v2.0 text, superseded by #1182
   as a duplicate, not an earlier version.
3. #1251 "Crimson Hexagon / NH-OS DOI Registry: Complete Document Archive — … 91 DOI-Anchored Documents (January
   2026)" (DOI 18284689). The work its title and DOI name — the post of 2026-01-17, 18:13 — is seated in full at #323
   (91 documents, DOI 18284689); the 94-document state of the same day is #320. Seating it again here would duplicate
   #323, so #1251 stays a duplicate mint, its successor corrected from #31 (the v7.0 registry, the body seated here on
   2026-07-19) to #323. Its title stays: it is the title of the post.
USAGE  python3.12 scripts/record_repairs_20261018.py [--dry-run]
"""
import datetime, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

TODAY = '2026-10-18'
RULING = ('Lee Sharks, 2026-10-18: "y thats mislabelled. search alexanarch and blog for 3.0 ... theres also an issue where '
          'each of the hexagonal license specs points to each other as superseded ... check what else is in the archive"; '
          'the repairs proposed from that search: "adopted for all".')
KG = 'https://mindcontrolpoems.blogspot.com/2026/04/crimson-hexagonal-archive-knowledge.html'
KG_ROW = 'license-rhys | DOCUMENT | license | Rhys Owens Hex License v3.0 | 10.5281/zenodo.19673630 | Lunar Arm | active'
ESSAY = 'https://mindcontrolpoems.blogspot.com/2025/10/rhys-owens-lunar-arm-of-new-human.html'
PROTO = 'https://mindcontrolpoems.blogspot.com/2026/04/hexagonal-licensing-protocol.html'


def reseat(d, text):
    """write the new canonical text and recompute hash, glyph and AXN in the same hex and family"""
    tp = (d.get('full_text_path') or f"/data/texts/AXN-{d['hex']}-text.md").lstrip('/')
    old_axn, old_hash = d.get('axn'), d.get('hash')
    (ROOT / tp).write_text(text, encoding='utf-8')
    h = hashlib.sha256(text.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
    d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
    d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
    d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
    d['date_modified'] = TODAY
    return {'axn_old': old_axn, 'axn_new': d['axn'], 'hash_old': old_hash, 'hash_new': h}


def body_of(d):
    tp = (d.get('full_text_path') or '').lstrip('/')
    return (ROOT / tp).read_text(errors='replace').strip()


def note(d, kind, text):
    log = d.get('record_modifications') if isinstance(d.get('record_modifications'), list) else []
    log.append({'date': TODAY, 'field': kind, 'note': text, 'ruled_by': RULING})
    d['record_modifications'] = log
    d['remediation_note'] = f'{TODAY} RECORD REPAIR ({kind}): {text}'


def main():
    dry = '--dry-run' in sys.argv
    reg = json.load(open(ROOT / 'data/registry.json')); byn = {d['deposit_number']: d for d in reg['deposits']}
    out = []
    # 1. #1358
    d = byn[1358]; old = body_of(d)
    text = (f"# {d['title']}\n\n**{d.get('creator')}** · record repaired {TODAY}\n\n"
            f"**AXN:** AXN:{d['hex']} — Alexanarch deposit #1358 (self-reference in root form by pre-hash necessity)\n"
            f"**Restoration status:** METADATA ONLY — the text of this licence (v3.0, the full unified licence for Rhys Owens, "
            f"Lunar Arm) is not recovered: it is in neither the archive nor the blog. The body seated here on 2026-07-19 was "
            f"another work, the essay \"Rhys Owens — The Lunar Arm of New Human\" (blog, 2025-10-13), retained below as an "
            f"appendix; the essay is now its own record.\n**DOI(s):** 10.5281/zenodo.19673630 (severed)\n\n---\n\n"
            f"## What is known of the licence\n\n"
            f"- Title as deposited: {d['title']}; deposited 2026-04-25 under DOI 10.5281/zenodo.19673630, severed at Zenodo 2026-06-19.\n"
            f"- Its one surviving witness is its row in the archive's knowledge graph, published the same day ({KG}, 2026-04-25 12:15):\n\n"
            f"  > {KG_ROW}\n\n"
            f"- Its predecessors in the series are seated: v1.0 (creative writing → New Human 2) at #1356.\n\n"
            f"---\n\n## Appendix — another work seated here on 2026-07-19, superseded {TODAY} (retained per non-destruction)\n\n" + old + "\n")
    r = reseat(d, text) if not dry else {}
    d['canonical_text_status'] = 'metadata_only'
    prev = d.get('body_status') if isinstance(d.get('body_status'), dict) else {}
    d['body_status'] = {'class': 'metadata_capture', 'lacuna': True, 'recovery_status': 'NOT_RECOVERED-' + TODAY.replace('-', ''),
                        'residual_chars': len(text), 'audited_at': datetime.datetime.now(datetime.UTC).isoformat(),
                        'audit_version': 'record_repairs_20261018', 'class_before_repair': prev.get('class')}
    d['version'] = 'v3.0'
    d['related_deposits'] = [{'deposit': 1356, 'relation': 'series: v1.0 of the Rhys Owens contributor licence'}]
    note(d, 'mislabelled body', 'the seated body was another work (the Lunar Arm essay, blog 2025-10-13); the licence text is '
         'not recovered; the record is metadata-only with its knowledge-graph witness; the essay retained as appendix and minted as its own record.')
    out.append({'n': 1358, 'repair': 'metadata-only; essay retained as appendix', **r})
    # 2. the protocol chain
    d = byn[66]; old = body_of(d)
    text = (f"# {d['title']}\n\n**{d.get('creator')}** · record repaired {TODAY}\n\n"
            f"**AXN:** AXN:{d['hex']} — Alexanarch deposit #66 (self-reference in root form by pre-hash necessity)\n"
            f"**Restoration status:** v1.0 TEXT NOT RECOVERED — the blog post of this protocol ({PROTO}) was overwritten in place "
            f"with v2.0, and the v1.0 text survives nowhere in the archive or on the blog. The v2.0 text seated here is retained "
            f"below as an appendix; v2.0 stands as its own record, #1182.\n"
            f"**DOI(s):** {', '.join(d.get('zenodo_dois') or [])}\n\n---\n\n"
            f"## What is known of v1.0\n\n- Deposited 2026-04-19 as \"Hexagonal Licensing Protocol v1.0 — Comprehensive Specification "
            f"for Distributed Contributor Infrastructure\".\n- Its successor is v2.0 (\"Three Critical Innovations\"), #1182; a second "
            f"deposit of the same v2.0 text is #1181.\n\n---\n\n## Appendix — v2.0 text seated here, superseded {TODAY} "
            f"(retained per non-destruction)\n\n" + old + "\n")
    r = reseat(d, text) if not dry else {}
    vb = d.get('version_basis') if isinstance(d.get('version_basis'), dict) else {}
    d['version_basis_before_repair'] = vb
    d['version'] = 'v1.0'
    d['version_basis'] = {'ruling': RULING, 'title_version': 'v1.0', 'observed_body_version': 'v2.0 (appendix)', 'audit_date': TODAY,
                          'directive': 'v1.0 record; v1.0 text not recovered; v2.0 is #1182'}
    d['canonical_text_status'] = 'metadata_only'
    d['body_status'] = {'class': 'metadata_capture', 'lacuna': True, 'recovery_status': 'NOT_RECOVERED-' + TODAY.replace('-', ''),
                        'residual_chars': len(text), 'audited_at': datetime.datetime.now(datetime.UTC).isoformat(),
                        'audit_version': 'record_repairs_20261018', 'class_before_repair': 'full'}
    d['status'] = 'SUPERSEDED'; d['superseded_by_deposit_number'] = 1182
    d['superseded_reason'] = 'Earlier version: v1.0 of the Hexagonal Licensing Protocol, superseded by v2.0 (#1182). Its own text is not recovered.'
    note(d, 'mislabelled body / supersession chain', 'titled v1.0 but held the v2.0 text; v1.0 text not recovered; v2.0 retained as appendix; superseded by the v2.0 head #1182.')
    out.append({'n': 66, 'repair': 'v1.0 metadata; v2.0 retained as appendix; superseded by #1182', **r})
    d = byn[1182]
    d['supersession_before_repair'] = {k: d.pop(k, None) for k in ('superseded_by_deposit_number', 'superseded_reason', 'duplicate_note')}
    d['status'] = 'ACTIVE'
    d['related_deposits'] = [{'deposit': 66, 'relation': 'series: v1.0 (text not recovered), superseded by this record'},
                             {'deposit': 1181, 'relation': 'duplicate: a second deposit of this v2.0 text, from the same blog post'}]
    d['date_modified'] = TODAY
    note(d, 'supersession chain', 'the v2.0 head of the Hexagonal Licensing Protocol: ACTIVE; it no longer names #66 (v1.0) as its successor; #1181 is a duplicate deposit of the same text, not an earlier version.')
    out.append({'n': 1182, 'repair': 'v2.0 head, ACTIVE'})
    d = byn[1181]
    d['supersession_before_repair'] = {k: d.get(k) for k in ('superseded_by_deposit_number', 'superseded_reason')}
    d['superseded_by_deposit_number'] = 1182
    d['superseded_reason'] = ('Duplicate deposit of the same work: the v2.0 text of the Hexagonal Licensing Protocol, from the same blog post as #1182, '
                              'which is the record of standing. CORRECTED 2026-10-18: the successor was recorded as #66, whose title is v1.0.')
    d['related_deposits'] = [{'deposit': 1182, 'relation': 'duplicate of: the v2.0 head'}]
    d['date_modified'] = TODAY
    note(d, 'supersession chain', 'successor corrected from #66 (v1.0) to #1182 (the v2.0 head); a duplicate deposit, not an earlier version.')
    out.append({'n': 1181, 'repair': 'duplicate of #1182'})
    # 3. #1251 — the work it names is #323; the family's current edition is #31 (one hop: check_supersession_terminal)
    d = byn[1251]
    d['supersession_before_repair'] = {k: d.get(k) for k in ('superseded_reason', 'duplicate_note')}
    d['duplicate_of_deposit_number'] = 323
    d['superseded_reason'] = ('Duplicate witness: the work this record names — the DOI Registry post of 2026-01-17, 18:13 (91 documents, DOI '
                              '10.5281/zenodo.18284689) — is seated in full at #323, its own record; the registry\'s current edition is #31 (v7.0, March 2026), '
                              'to which every edition points in one hop. CORRECTED 2026-10-18: the reason named #31 as the same work, because the body '
                              'seated here on 2026-07-19 was the v7.0 post; the containment measure matched that body.')
    d['duplicate_note'] = ('DUPLICATE MINT (2026-07-19 restoration): the work this record names — title and DOI 10.5281/zenodo.18284689 — is seated at #323. '
                           'The body seated here is the March 2026 v7.0 registry (held at #31 and #1171), kept as found; seating the January post here would duplicate #323.')
    d['date_modified'] = TODAY
    note(d, 'supersession / citation', 'the duplicate is of #323, the record of the post its title and DOI name (successor stays #31, the current edition); not re-seated (it would duplicate #323).')
    out.append({'n': 1251, 'repair': 'duplicate of #323; successor #31 kept (one hop)'})
    # the retirement layer (data/retired-records.json; body_status.retired) follows the supersession above
    rr = json.load(open(ROOT / 'data/retired-records.json'))
    b2 = byn[1182]; was = (b2.get('body_status') or {}).pop('retired', None)
    if was:
        b2['retirement_reversed'] = {'retired': was, 'reversed_on': TODAY, 'ruled_by': RULING,
                                     'why': 'retired 2026-08-10 as a duplicate witness of #66; #66 is titled v1.0 and its text is not recovered, so #1182, the v2.0 text, is the head of the family.'}
        rr['reversed']['1182'] = {'was': rr['records'].pop('1182', None), 'on': TODAY, 'ruled_by': RULING}
    b1 = byn[1181]; rt = (b1.get('body_status') or {}).get('retired')
    if rt:
        rt['corrected_20261018'] = {'was_resolves_to': rt.get('resolves_to')}; rt['resolves_to'] = 1182
    if '1181' in rr['records']:
        rr['records']['1181'].update({'resolves_to': 1182, 'title': byn[1182]['title'], 'axn': byn[1182].get('axn'),
                                      'corrected_20261018': {'was_resolves_to': 66}})
    b6 = byn[66]
    b6['body_status']['retired'] = {'class': 'superseded', 'resolves_to': 1182, 'declared': TODAY,
                                    'note': 'Superseded, not a stub: indexable (ruling 2026-10-15). The page carries a banner before the body naming the current version to cite, and an axn:retired marker; its canonical is its own URL.',
                                    'indexable': True}
    rr['records']['66'] = {'class': 'superseded', 'resolves_to': 1182, 'title': byn[1182]['title'], 'axn': byn[1182].get('axn'), 'declared': TODAY}
    rr['count'] = len(rr['records'])
    if not dry:
        reg['last_updated'] = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
        json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
        json.dump(rr, open(ROOT / 'data/retired-records.json', 'w'), ensure_ascii=False, indent=2)
        json.dump({'run_at': datetime.datetime.now(datetime.UTC).isoformat(), 'ruling': RULING, 'repairs': out},
                  open(ROOT / 'data/record-repairs-2026-10-18.json', 'w'), ensure_ascii=False, indent=1)
    for x in out:
        print(x)


if __name__ == '__main__':
    main()
