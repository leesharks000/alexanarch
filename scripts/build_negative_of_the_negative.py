#!/usr/bin/env python3
"""Build the negative-of-the-negative dataset.

Source of truth: datasets/negative-of-the-negative/rows.json, authored, validated
against schema.json (additionalProperties false). The builder joins provenance
from data/registry.json by deposit number and measurements from
data/EA-WG-CAPTURES-01.json by address/observation id, computes `bleed`, and
emits four parquet configs plus the dataset card. Nothing is authored here.

    python3 scripts/build_negative_of_the_negative.py [--out hf-non] [--check]

Configs: rows (one row per severed edge, keyed by concept) · keys (every string
that should resolve to a row: concept, alt_keys, adjacent_addresses, scoped
form) · edges (concept → deposit, typed) · measurements (one row per capture
referenced, joined to the registry, with the permalink).
"""
import argparse, hashlib, json, sys, datetime, pathlib
import pandas as pd
try:
    import jsonschema
except ImportError:
    jsonschema = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'datasets' / 'negative-of-the-negative'
MAXIM = "all things are now lawful to you in jack feist"
RECORD = "https://www.alexanarch.org/s/records/{n}/"
CAPTURE = "https://www.alexanarch.org/captures/#{slug}"

def load(p):
    return json.load(open(p, encoding='utf-8'))

# ── v2: the /non work (EA-NEGONT-02, #1665), added 2026-10-08 on the operator's ruling ("publish now with the labels").
# Read-only joins of files already in the repo; nothing is authored here. Every row carries its entry's status
# label: these are working objects, draft and not frozen, with unaudited ledgers unless the row's status says otherwise.
V2 = SRC / 'v2'
NON = "https://www.alexanarch.org/non/{e}/"

def _status_label(st):
    if not isinstance(st, dict):
        return 'draft, not frozen; ledger unaudited'
    frozen = 'frozen' if st.get('frozen') else 'not frozen'
    led = st.get('ledger') or 'unaudited'
    return f"draft, {frozen}; ledger {led.split(' (')[0]}"

def build_v2(deps, breaches):
    T = {k: [] for k in ('non_entities', 'non_observations', 'non_compositions', 'non_field_claims',
                         'non_archive_claims', 'non_readings', 'non_kernel')}
    panel = load(V2 / 'panel' / 'panel.json')
    register = load(V2 / 'register.json')
    reg_entries = next(v for k, v in register.items() if isinstance(v, list) and v and isinstance(v[0], dict) and 'addr_id' in v[0])
    rowfiles = {f.stem: load(f) for f in sorted((V2 / 'rows').glob('*.json'))}
    labels = {}
    for ent in panel['entities']:
        e = ent['entity']; row = rowfiles.get(e)
        labels[e] = _status_label(row.get('status')) if row else 'no entry composed'
        T['non_entities'].append({'entity': e, 'name': ent.get('name'), 'type': ent.get('type'), 'type_basis': ent.get('type_basis'),
            'source': ent.get('source'), 'stage': ent.get('stage'), 'addresses': json.dumps(ent.get('addresses', []), ensure_ascii=False),
            'has_entry': row is not None, 'status_label': labels[e], 'frozen': bool(row and (row.get('status') or {}).get('frozen')),
            'page_url': NON.format(e=e) if (ROOT / 'non' / e / 'index.html').exists() else None,
            'json_url': NON.format(e=e) + 'entity.json' if (ROOT / 'non' / e / 'entity.json').exists() else None})
    for o in reg_entries:
        e = o.get('entity')
        if e not in labels:
            breaches.append(f"v2 register {o.get('slug')}: entity {e} not on the panel")
        T['non_observations'].append({'slug': o['slug'], 'addr_id': o['addr_id'], 'obs_id': o['obs_id'], 'query': o['q'], 'entity': e,
            'date': o['date'], 'surface': o['surface'], 'surface_basis': o.get('surface_basis'), 'auth': o.get('auth'), 'auth_basis': o.get('auth_basis'),
            'cites': o.get('cites'), 'cite_list': json.dumps(o.get('cite_list'), ensure_ascii=False), 'archive_present': o.get('archive_present'),
            'transcript': o.get('transcript'), 'transcript_sha256': o.get('transcript_sha256'), 'transcript_complete': o.get('transcript_complete'),
            'source_form': o.get('sf'), 'page_url': (NON.format(e=e) + '#reg-' + o['slug']) if e else None})
    for e, row in rowfiles.items():
        lab = labels.get(e) or _status_label(row.get('status'))
        O = row.get('objects', {})
        for obj, arm in (('KO', 'B ∪ A'), ('KO_B', 'B'), ('P', 'B ∪ A'), ('P_B', 'B')):
            x = O.get(obj)
            if not x: continue
            if obj.startswith('KO'):
                for s_ in (x.get('sentences') if isinstance(x, dict) else x) or []:
                    T['non_compositions'].append({'entity': e, 'object': obj, 'arm': arm, 'unit': 'sentence', 'position': s_.get('n'),
                        'section': None, 'label': None, 'text': s_.get('text'), 'claims': json.dumps(s_.get('claims', [])), 'status_label': lab})
            else:
                L = x.get('lede') or {}
                T['non_compositions'].append({'entity': e, 'object': obj, 'arm': arm, 'unit': 'lede', 'position': 0, 'section': None, 'label': None,
                    'text': L.get('text') if isinstance(L, dict) else L, 'claims': json.dumps(L.get('claims', []) if isinstance(L, dict) else []), 'status_label': lab})
                i = 0
                for sec in x.get('sections', []):
                    for it in sec.get('items', []):
                        i += 1
                        T['non_compositions'].append({'entity': e, 'object': obj, 'arm': arm, 'unit': 'item', 'position': i, 'section': sec.get('head'),
                            'label': it.get('label'), 'text': it.get('text'), 'claims': json.dumps(it.get('claims', [])), 'status_label': lab})
        for k in row.get('kernel') or []:
            T['non_kernel'].append({'entity': e, 'K': k.get('K'), 'claim': k.get('claim'), 'source': k.get('source'), 'modality': k.get('M_src'),
                'sense': k.get('sense'), 'qualifiers': k.get('qualifiers carried'), 'falsifiers': k.get('f (source\'s own falsifiers)'), 'contrast': k.get('contrast'), 'status_label': lab})
        led = V2 / 'ledgers' / e
        if (led / 'field.json').exists():
            F = load(led / 'field.json'); src = {s_['id']: s_ for s_ in F.get('field', [])}
            for cid, c in F.get('field_claims', {}).items():
                card = src.get(c.get('source'), {})
                T['non_field_claims'].append({'entity': e, 'claim_id': cid, 'source': c.get('source'), 'card': card.get('card'), 'url': card.get('url'),
                    'locus': c.get('locus'), 'quote': c.get('quote'), 'claim': c.get('claim'), 'modality': c.get('modality'),
                    'kernel': c.get('kernel'), 'lineage': c.get('lineage'), 'status_label': lab})
        if (led / 'ledger-archive.json').exists():
            for c in load(led / 'ledger-archive.json'):
                n = c.get('dep'); d = deps.get(n)
                if d is None:
                    breaches.append(f"v2 {e}: archive claim {c.get('id')} cites deposit {n} not in registry")
                T['non_archive_claims'].append({'entity': e, 'claim_id': c.get('id'), 'deposit': n, 'axn': d.get('axn') if d else None,
                    'record_url': RECORD.format(n=n), 'title': c.get('title') or (d.get('title') if d else None), 'locus': c.get('locus'),
                    'quote': c.get('quote'), 'claim': c.get('claim'), 'kind': c.get('kind'), 'modality': c.get('modality'),
                    'strata': json.dumps(c.get('strata')) if isinstance(c.get('strata'), (list, dict)) else c.get('strata'),
                    'kernel': c.get('kernel'), 'lineage': c.get('lineage'), 'quote_verified': c.get('quote_ok'), 'status_label': lab})
        rd = V2 / 'traversal' / e / 'reading.json'
        if rd.exists():
            R = load(rd)
            for v in R.get('verdicts', []):
                x_ = v.get('dep')
                for n in (x_ if isinstance(x_, list) else [x_]):
                    T['non_readings'].append({'entity': e, 'deposit': n, 'record_url': RECORD.format(n=n) if n is not None else None,
                        'verdict': 'admitted', 'strata': json.dumps(v.get('strata')) if isinstance(v.get('strata'), (list, dict)) else v.get('strata'),
                        'n_candidates': len(v.get('cands') or []), 'reason': v.get('reason'), 'status_label': lab})
            for v in R.get('not_admitted', []):
                x_ = v.get('deps') if v.get('deps') is not None else v.get('dep')
                deps_ = x_ if isinstance(x_, list) else ([x_] if x_ is not None else [])
                for n in deps_:
                    T['non_readings'].append({'entity': e, 'deposit': n, 'record_url': RECORD.format(n=n), 'verdict': 'not admitted',
                        'strata': None, 'n_candidates': len(v.get('cands') or []), 'reason': v.get('reason') or v.get('group'), 'status_label': lab})
    return T

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(ROOT / 'hf-non'))
    ap.add_argument('--registry', default=str(ROOT / 'data' / 'registry.json'))
    ap.add_argument('--captures', default=str(ROOT / 'data' / 'EA-WG-CAPTURES-01.json'))
    ap.add_argument('--check', action='store_true', help='validate only; exit 1 on any breach')
    a = ap.parse_args()

    schema = load(SRC / 'schema.json')
    rows = load(SRC / 'rows.json')
    breaches = []
    if jsonschema is None:
        breaches.append('jsonschema not installed; schema not enforced')
    else:
        v = jsonschema.Draft202012Validator(schema)
        for r in rows:
            for e in v.iter_errors(r):
                breaches.append(f"{r.get('key','?')}: {e.message}")
    keys = [r['key'] for r in rows]
    if len(keys) != len(set(keys)):
        breaches.append('duplicate keys')

    reg = load(a.registry)
    deps = {d['deposit_number']: d for d in reg['deposits']}
    caps = load(a.captures)
    by_addr, by_obs = {}, {}
    for e in caps['entries']:
        by_addr.setdefault(e.get('addr_id'), e)
        by_obs.setdefault(e.get('obs_id'), e)
        for o in (e.get('observations') or []):
            if isinstance(o, dict) and o.get('obs_id'):
                by_obs.setdefault(o['obs_id'], e)

    out_rows, keys_rows, edges, meas = [], [], [], []
    for r in rows:
        d = deps.get(r['source_deposit'])
        if d is None:
            breaches.append(f"{r['key']}: deposit {r['source_deposit']} not in registry")
        for n in r.get('companion_deposits', []):
            if n not in deps:
                breaches.append(f"{r['key']}: companion deposit {n} not in registry")
        # measurements: ids must resolve unless marked PENDING-
        def resolve(m, arm):
            if not m: return None
            aid = m['addr_id']
            if aid.startswith('PENDING-'):
                return {'status': 'pending seating', 'addr_id': aid}
            e = by_addr.get(aid)
            if e is None:
                breaches.append(f"{r['key']}: {arm} addr_id {aid} not in the Capture Registry")
                return {'status': 'unresolved', 'addr_id': aid}
            meas.append({'row_key': r['key'], 'arm': arm, 'addr_id': aid, 'obs_id': m.get('obs_id') or e.get('obs_id'),
                         'slug': e['slug'], 'query': e.get('q'), 'surface': e.get('surface'), 'auth': e.get('auth'),
                         'date': m.get('date') or e.get('date'), 'n_observations': e.get('n_observations'),
                         'composed_sort': m.get('composed_sort'), 'admitted': m['admitted'], 'attributed': m.get('attributed'), 'treatment': None, 'note': m.get('note'),
                         'permalink': CAPTURE.format(slug=e['slug'])})
            return {'status': 'seated', 'addr_id': aid, 'obs_id': m.get('obs_id') or e.get('obs_id'), 'slug': e['slug'],
                    'permalink': CAPTURE.format(slug=e['slug']), 'date': e.get('date'), 'surface': e.get('surface')}
        mu, mt = resolve(r.get('measured_untied'), 'untied'), resolve(r.get('measured_tied'), 'tied')
        # the longitudinal record (2026-09-28): later observations, of either arm or of a control address
        latest = {}
        for o in r.get('observations', []):
            e = by_addr.get(o['addr_id'])
            if e is None:
                breaches.append(f"{r['key']}: observation addr_id {o['addr_id']} not in the Capture Registry"); continue
            if o.get('obs_id') and o['obs_id'] not in by_obs:
                breaches.append(f"{r['key']}: observation obs_id {o['obs_id']} not in the Capture Registry")
            meas.append({'row_key': r['key'], 'arm': o['arm'], 'addr_id': o['addr_id'], 'obs_id': o.get('obs_id'),
                         'slug': e['slug'], 'query': e.get('q'), 'surface': e.get('surface'), 'auth': e.get('auth'),
                         'date': o['date'], 'n_observations': e.get('n_observations'),
                         'composed_sort': o.get('composed_sort'), 'admitted': o['admitted'], 'attributed': o.get('attributed'),
                         'treatment': o.get('treatment'), 'note': o.get('note'),
                         'permalink': CAPTURE.format(slug=e['slug'])})
            if o['arm'] != 'control' and (o['arm'] not in latest or o['date'] >= latest[o['arm']]['date']):
                latest[o['arm']] = {'date': o['date'], 'composed_sort': o.get('composed_sort'), 'admitted': o['admitted'], 'attributed': o.get('attributed'), 'addr_id': o['addr_id'], 'obs_id': o.get('obs_id')}
        u_adm = r['measured_untied']['admitted'] if r.get('measured_untied') else None
        t_adm = r['measured_tied']['admitted'] if r.get('measured_tied') else None
        bleed = None
        if u_adm is not None and t_adm is not None:
            bleed = (1.0 if u_adm else 0.0) / (1.0 if t_adm else 0.0) if t_adm else None
        for p in r.get('neighbours_distorted', []):
            if not p['addr_id'].startswith('PENDING-') and p['addr_id'] not in by_addr:
                breaches.append(f"{r['key']}: neighbour addr_id {p['addr_id']} not in the Capture Registry")
        ps = r.get('prior_state')
        if ps and ps.get('addr_id') and ps['addr_id'] not in by_addr:
            breaches.append(f"{r['key']}: prior_state addr_id not in the Capture Registry")

        row = dict(r)
        row.update({
            'axn': d.get('axn') if d else None, 'title': d.get('title') if d else None,
            'record_url': RECORD.format(n=r['source_deposit']), 'record_status': d.get('status') if d else None,
            'companion_record_urls': [RECORD.format(n=n) for n in r.get('companion_deposits', [])],
            'measured_untied_resolved': mu, 'measured_tied_resolved': mt,
            'latest_untied': latest.get('untied'), 'latest_tied': latest.get('tied'),
            'bleed': bleed, 'bleed_status': 'measured' if bleed is not None else ('untied only' if u_adm is not None else ('tied only' if t_adm is not None else 'unmeasured')),
            'maxim': MAXIM,
        })
        # the edge statement a consumer indexing by concept should receive, as text
        row['edge_statement'] = (f"{r['concept']}: {r['claim']} — claimed at {RECORD.format(n=r['source_deposit'])} "
                                 f"({d.get('axn') if d else 'AXN unresolved'}), Crimson Hexagonal Archive; "
                                 + (f"distinguished from: {r['distinction']}; " if r.get('distinction') else '')
                                 + (f"what stands at this concept when the archive is scoped out: {r['default_at_concept']}." if r.get('default_at_concept') else ''))
        for k in ['external_unscoped','convergent_arrivals','world_arrivals','missed_updates','dimensions_RH','neighbours_distorted','introduces_type','coherence','prior_state','distortion','measured_untied','measured_tied','convergence_pair','seated','measured_untied_resolved','measured_tied_resolved','observations','transition','latest_untied','latest_tied']:
            row[k] = json.dumps(row.get(k), ensure_ascii=False) if row.get(k) is not None else None
        out_rows.append(row)
        # keys
        allkeys = [r['concept']] + r.get('alt_keys', []) + r.get('adjacent_addresses', [])
        if r.get('scoped_form'): allkeys.append(r['scoped_form'])
        for k in allkeys:
            keys_rows.append({'key_string': k, 'row_key': r['key'], 'kind': 'concept' if k == r['concept'] else ('adjacent_address' if k in r.get('adjacent_addresses', []) else ('scoped_form' if k == r.get('scoped_form') else 'alt_key')), 'concept_type': r['concept_type'], 'record_url': RECORD.format(n=r['source_deposit'])})
        # edges
        edges.append({'subject': r['concept'], 'predicate': 'claimed_by', 'object_deposit': r['source_deposit'], 'object_axn': d.get('axn') if d else None, 'object_url': RECORD.format(n=r['source_deposit']), 'row_key': r['key'], 'locus': r['defining_text_locus']})
        for n in r.get('companion_deposits', []):
            edges.append({'subject': r['concept'], 'predicate': 'developed_by', 'object_deposit': n, 'object_axn': deps[n].get('axn') if n in deps else None, 'object_url': RECORD.format(n=n), 'row_key': r['key'], 'locus': None})
        for dim in r.get('dimensions_RH', []):
            edges.append({'subject': r['concept'], 'predicate': 'dimension_supplied_by', 'object_deposit': dim['deposit'], 'object_axn': deps[dim['deposit']].get('axn') if dim['deposit'] in deps else None, 'object_url': RECORD.format(n=dim['deposit']), 'row_key': r['key'], 'locus': dim['dimension']})
        if r.get('distinction'):
            edges.append({'subject': r['concept'], 'predicate': 'distinguished_from', 'object_deposit': None, 'object_axn': None, 'object_url': None, 'row_key': r['key'], 'locus': r['distinction']})

    v2 = build_v2(deps, breaches)
    if breaches:
        print('BREACHES (recorded, not blocking):'); [print('  -', b) for b in breaches]
    if a.check:
        sys.exit(1 if breaches else 0)

    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    frames = {'rows': pd.DataFrame(out_rows), 'keys': pd.DataFrame(keys_rows), 'edges': pd.DataFrame(edges), 'measurements': pd.DataFrame(meas)}
    frames.update({k: pd.DataFrame(v) for k, v in v2.items()})
    cfg, manifest = [], {'built': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_rows_sha256': hashlib.sha256(open(SRC/'rows.json','rb').read()).hexdigest(), 'schema_sha256': hashlib.sha256(open(SRC/'schema.json','rb').read()).hexdigest(), 'registry_total': len(deps), 'captures_total': len(caps['entries']), 'breaches': breaches, 'configs': {}}
    for name, df in frames.items():
        for c in df.columns:
            if df[c].map(lambda x: isinstance(x, (list, dict))).any():
                df[c] = df[c].map(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)
        df.to_parquet(out / f'{name}.parquet', index=False, engine='pyarrow')
        cfg.append(f"- config_name: {name}\n  data_files: {name}.parquet")
        manifest['configs'][name] = len(df)
        print(f"  {name}: {len(df)} rows")
    n_meas = sum(1 for r in rows if r.get('measured_untied') and r.get('measured_tied'))
    n_half = sum(1 for r in rows if bool(r.get('measured_untied')) != bool(r.get('measured_tied')))
    card = (out.parent / 'datasets' / 'negative-of-the-negative' / 'CARD.md').read_text(encoding='utf-8') if (out.parent / 'datasets' / 'negative-of-the-negative' / 'CARD.md').exists() else (SRC / 'CARD.md').read_text(encoding='utf-8')
    (out / 'README.md').write_text(card.format(configs='\n'.join(cfg), n_rows=len(rows), n_meas=n_meas, n_half=n_half, n_keys=len(keys_rows), n_edges=len(edges), built=manifest['built'][:10], maxim=MAXIM, n_non_entities=len(v2['non_entities']), n_non_entries=sum(1 for r in v2['non_entities'] if r['has_entry']), n_non_obs=len(v2['non_observations']), n_non_units=len(v2['non_compositions']), n_non_field=len(v2['non_field_claims']), n_non_archive=len(v2['non_archive_claims'])), encoding='utf-8')
    json.dump(manifest, open(out / 'build-manifest.json', 'w'), indent=1)
    print('card + manifest written to', out)

if __name__ == '__main__':
    main()
