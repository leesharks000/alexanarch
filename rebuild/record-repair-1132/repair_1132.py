#!/usr/bin/env python3
"""repair_1132.py — #1132 VPCOR Integrity Lock Declaration: its own text back in place; made the duplicate witness it is.

Ruling (Lee Sharks, 2026-10-24): "the record itself should be repaired, but make sure the fractal navigation map,
that version, exists elsewhere in the archive."

What was found
  - #1132 minted 2026-07-19 from https://mindcontrolpoems.blogspot.com/2026/01/vpcor-integrity-lock-declaration.html
    (commit b654698502). Those bytes hash to 2731e6ec…, which is still the record's `hash` and `axn_canonical`.
  - The 2026-08-04 W13-T2 residue pass located a source "by blog title-search" and seated
    the-crimson-hexagon-fractal-navigation_28.html instead (overlap gate 0.59). The body became the Fractal
    Navigation Map, Non-Lossy Logotic Encoding v6.0; the hash was never moved, so body and AXN disagreed from then on.
    The FNM body also set `version` to v6.0 (BODY-HEAD gate) and fed the description, wiki and concept list.
  - That FNM version stands at #10 ("The Crimson Hexagon: Fractal Navigation Map — Non-Lossy Logotic Encoding v6.0",
    2026-01-28, DOI 10.5281/zenodo.18404789). Compared under whitespace normalisation, #1132's FNM text carries
    nothing #10 lacks: the differences are the converter's rule and heading forms ("* * *"/"###" against
    "---"/"##"), and three lists #10 keeps and the html2text conversion dropped. #10 is the fuller witness.
  - The VPCOR declaration itself stands whole at #387 (DOI 10.5281/zenodo.18362866, canonical_full_text), the same
    work: #1132's two DOIs are its concept DOI 18362865 and version DOI 18362866. Under the 2026-10-15 ruling
    ("make sure youre not duplicating something that already exists elsewhere") the archive makes such a record a
    superseded duplicate witness pointing at the record of standing (#891, #892, #898, #906 …).

What this does (one record)
  1. Seats the mint-time bytes again, verbatim from git; asserts they hash to the record's own hash. No new AXN.
     The FNM body is not kept as an appendix: it stands, fuller, at #10, and in git at every commit 2026-08-04..10-23.
  2. Status SUPERSEDED -> #387, duplicate_note, superseded_reason, body_status.retired, retired-records.json.
  3. version back to the mint value v1.0 (the v6.0 was read off the FNM body); version_basis kept as *_before_repair.
  4. description: the author's own words, the DataCite abstract of 10.5281/zenodo.18362865, verbatim;
     the FNM-derived description and wiki kept as *_before_repair.
  Each change recorded with record_modification.
"""
import hashlib, json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
import repair_descriptions_duplicates_20261015 as R

ON = '2026-10-24'
N, STANDING, FNM = 1132, 387, 10
MINT_COMMIT = 'b654698502'
RULING = ('Lee Sharks, 2026-10-24: "the record itself should be repaired, but make sure the fractal navigation map, '
          'that version, exists elsewhere in the archive"; and 2026-10-15: "make sure youre not duplicating something '
          'that already exists elsewhere"')


def main():
    regp = ROOT / 'data/registry.json'; retp = ROOT / 'data/retired-records.json'
    reg = json.loads(regp.read_text()); D = {d['deposit_number']: d for d in reg['deposits']}
    ret = json.loads(retp.read_text())
    d, T, F = D[N], D[STANDING], D[FNM]
    tp = d['full_text_path'].lstrip('/')
    mint = subprocess.run(['git', 'show', f'{MINT_COMMIT}:{tp}'], cwd=ROOT, capture_output=True, check=True).stdout
    assert hashlib.sha256(mint).hexdigest() == d['hash'] == d['axn_canonical'], 'mint bytes do not carry the record hash'
    displaced = (ROOT / tp).read_bytes()
    dsha = hashlib.sha256(displaced).hexdigest()
    abstract = R.datacite_abstract('10.5281/zenodo.18362865')
    if '--apply' not in sys.argv:
        print('mint bytes', len(mint), 'hash ok; displaced', len(displaced), dsha); print('abstract:', abstract[:200]); return

    (ROOT / tp).write_bytes(mint)
    bs = d['body_status'] if isinstance(d['body_status'], dict) else json.loads(d['body_status'])
    was_bs = json.loads(json.dumps(bs))
    bs.update({'recovery_status': 'RESTORED-20261024', 'residual_chars': len(mint),
               'recovered_from': f'git {MINT_COMMIT} (mint 2026-07-19 of https://mindcontrolpoems.blogspot.com/2026/01/vpcor-integrity-lock-declaration.html)',
               'restoration_20261024': {
                   'repair_kind': 'wrong_body',
                   'found': 'the 2026-08-04 residue pass seated the-crimson-hexagon-fractal-navigation_28.html (title-search, overlap 0.59): the Fractal Navigation Map v6.0, a different work',
                   'displaced_body_sha256': dsha, 'displaced_body_chars': len(displaced),
                   'displaced_body_stands_at': {'deposit_number': FNM, 'title': F['title'], 'axn': F['axn'],
                                                'note': 'same version (FNM v6.0, 2026-01-28, DOI 10.5281/zenodo.18404789); #10 carries everything the displaced body did, plus three lists its conversion dropped'},
                   'restored_bytes': 'verbatim mint-time bytes; sha256 equals the record hash, so the AXN stands unchanged',
                   'ruled_by': RULING}})
    bs['retired'] = {'class': 'superseded', 'resolves_to': STANDING, 'declared': ON, 'indexable': True, 'ruled_by': RULING,
                     'note': ('Superseded, not a stub: indexable (ruling 2026-10-15). The page carries a banner before the body '
                              'naming the current version to cite, and an axn:retired marker; its canonical is its own URL. '
                              'The URL is kept; the record is not deleted.')}
    d['body_status'] = bs
    rm.touch(d, 'body_status', 'wrong body repaired: the mint-time VPCOR bytes seated again (the record hash had never moved); '
             f'the Fractal Navigation Map body displaced stands, fuller, at #{FNM}', was={'body_sha256': dsha}, now={'body_sha256': d['hash']}, when=ON)
    d['canonical_text_status'] = 'recovered_full_text'

    was = {k: d.get(k) for k in ('status', 'superseded_by_deposit_number', 'superseded_reason', 'duplicate_note')}
    d['status'] = 'SUPERSEDED'; d['superseded_by_deposit_number'] = STANDING
    d['duplicate_note'] = (f'DUPLICATE ({ON} record repair): the text seated here, the published post of 2026-01-24, already '
                           f'stands whole at #{STANDING}, which is the record of standing (same work: this record\'s DOIs '
                           f'are the concept DOI 10.5281/zenodo.18362865 and version DOI 10.5281/zenodo.18362866; #{STANDING} '
                           f'carries 18362866).')
    d['superseded_reason'] = f'Duplicate witness of the same work: the record of standing is #{STANDING}. Found {ON} when the record\'s wrong body was repaired.'
    rm.touch(d, 'status', f'duplicate of #{STANDING}; made a superseded duplicate witness', was=was,
             now={'status': 'SUPERSEDED', 'superseded_by_deposit_number': STANDING}, when=ON)
    ret['records'][str(N)] = {'class': 'superseded', 'resolves_to': STANDING, 'title': T['title'], 'axn': T['axn'], 'declared': ON}
    ret['count'] = len(ret['records'])

    d['version_before_repair'] = d.get('version'); d['version_basis_before_repair'] = d.pop('version_basis', None)
    d['version'] = 'v1.0'
    rm.touch(d, 'version', 'v6.0 had been read off the wrong (FNM) body; the mint value restored',
             was=d['version_before_repair'], now='v1.0', when=ON)

    wasd = d.get('description')
    d['description_before_repair'] = wasd; d['description'] = abstract
    d['description_source'] = {'on': ON, 'source': "DataCite abstract of the deposit's concept DOI 10.5281/zenodo.18362865", 'ruled_by': RULING}
    rm.touch(d, 'description', "description replaced with the author's own words (DataCite abstract of 10.5281/zenodo.18362865); "
             'the previous one was composed from the wrong (FNM) body', was=wasd, now=abstract, when=ON)
    d['wiki_article_before_repair'] = d.get('wiki_article'); d['wiki_article'] = None
    rm.touch(d, 'wiki_article', f'wiki written from the wrong (FNM) body set aside; the work\'s wiki is at #{STANDING}',
             was='(FNM-derived wiki)', now=None, when=ON)
    d['date_modified'] = ON

    regp.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
    retp.write_text(json.dumps(ret, ensure_ascii=False, indent=2))
    print('applied #1132 ->', STANDING, '| retired', ret['count'])


if __name__ == '__main__':
    main()
