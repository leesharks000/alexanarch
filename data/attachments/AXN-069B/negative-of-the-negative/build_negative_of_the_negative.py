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
                         'date': e.get('date'), 'n_observations': e.get('n_observations'),
                         'composed_sort': m.get('composed_sort'), 'admitted': m['admitted'], 'note': m.get('note'),
                         'permalink': CAPTURE.format(slug=e['slug'])})
            return {'status': 'seated', 'addr_id': aid, 'obs_id': m.get('obs_id') or e.get('obs_id'), 'slug': e['slug'],
                    'permalink': CAPTURE.format(slug=e['slug']), 'date': e.get('date'), 'surface': e.get('surface')}
        mu, mt = resolve(r.get('measured_untied'), 'untied'), resolve(r.get('measured_tied'), 'tied')
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
            'bleed': bleed, 'bleed_status': 'measured' if bleed is not None else ('untied only' if u_adm is not None else ('tied only' if t_adm is not None else 'unmeasured')),
            'maxim': MAXIM,
        })
        # the edge statement a consumer indexing by concept should receive, as text
        row['edge_statement'] = (f"{r['concept']}: {r['claim']} — claimed at {RECORD.format(n=r['source_deposit'])} "
                                 f"({d.get('axn') if d else 'AXN unresolved'}), Crimson Hexagonal Archive; "
                                 + (f"distinguished from: {r['distinction']}; " if r.get('distinction') else '')
                                 + (f"what stands at this concept when the archive is scoped out: {r['default_at_concept']}." if r.get('default_at_concept') else ''))
        for k in ['external_unscoped','convergent_arrivals','world_arrivals','missed_updates','dimensions_RH','neighbours_distorted','introduces_type','coherence','prior_state','distortion','measured_untied','measured_tied','convergence_pair','seated','measured_untied_resolved','measured_tied_resolved']:
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

    if breaches:
        print('BREACHES (recorded, not blocking):'); [print('  -', b) for b in breaches]
    if a.check:
        sys.exit(1 if breaches else 0)

    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    frames = {'rows': pd.DataFrame(out_rows), 'keys': pd.DataFrame(keys_rows), 'edges': pd.DataFrame(edges), 'measurements': pd.DataFrame(meas)}
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
    (out / 'README.md').write_text(card.format(configs='\n'.join(cfg), n_rows=len(rows), n_meas=n_meas, n_half=n_half, n_keys=len(keys_rows), n_edges=len(edges), built=manifest['built'][:10], maxim=MAXIM), encoding='utf-8')
    json.dump(manifest, open(out / 'build-manifest.json', 'w'), indent=1)
    print('card + manifest written to', out)

if __name__ == '__main__':
    main()
