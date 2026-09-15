#!/usr/bin/env python3
"""Build the argument-as-dataset: a paper cluster translated out of prose into five tables.
Validates rows.json against schema.json; checks referential integrity (every relation endpoint,
every tests_claims entry, every result_evidence entry exists); computes per-claim support
topology (what supports it, at which epistemic level, what is missing); emits parquet + card.
No confidence scores anywhere. --check exits 1 on breach.
"""
import json,sys,argparse,pathlib,datetime,collections
import pandas as pd
try: import jsonschema
except ImportError: jsonschema=None
ROOT=pathlib.Path(__file__).resolve().parents[1]; SRC=ROOT/'datasets'/'argument-as-dataset'
MAXIM="all things are now lawful to you in jack feist"
ap=argparse.ArgumentParser(); ap.add_argument('--out',default=str(ROOT/'hf-aad')); ap.add_argument('--check',action='store_true'); a=ap.parse_args()
schema=json.load(open(SRC/'schema.json')); rows=json.load(open(SRC/'rows.json'))
breaches=[]
if jsonschema:
    for e in jsonschema.Draft202012Validator(schema).iter_errors(rows): breaches.append(f"schema: {'/'.join(map(str,e.path))}: {e.message[:160]}")
ids={}
for tbl,key in [('claims','claim_id'),('evidence','evidence_id'),('tests','test_id'),('terms','term_id')]:
    for r in rows[tbl]:
        if r[key] in ids: breaches.append(f"duplicate id {r[key]}")
        ids[r[key]]=tbl
for r in rows['relations']:
    for k in ('subject_id','object_id'):
        if r[k] not in ids: breaches.append(f"relation endpoint missing: {r[k]}")
for t in rows['tests']:
    for c in t['tests_claims']:
        if c not in ids: breaches.append(f"test {t['test_id']} names missing claim {c}")
    for e in t.get('result_evidence',[]):
        if e not in ids: breaches.append(f"test {t['test_id']} names missing evidence {e}")
for c in rows['claims']:
    if c.get('superseded_by') and c['superseded_by'] not in ids: breaches.append(f"claim {c['claim_id']} superseded_by missing")
# support topology per claim
level_of={c['claim_id']:c['epistemic_status'] for c in rows['claims']}; level_of.update({e['evidence_id']:('gap' if e['evidence_type']=='measurement_gap' else e.get('status','')) for e in rows['evidence']})
inbound=collections.defaultdict(list)
for r in rows['relations']: inbound[r['object_id']].append((r['subject_id'],r['relation']))
tested=collections.defaultdict(list)
for t in rows['tests']:
    for c in t['tests_claims']: tested[c].append((t['test_id'],t['status']))
topo=[]
for c in rows['claims']:
    sup=inbound.get(c['claim_id'],[])
    topo.append({'claim_id':c['claim_id'],'epistemic_status':c['epistemic_status'],'n_inbound':len(sup),
     'supported_by_measured':sorted(s for s,r in sup if r=='supports' and level_of.get(s) in ('measured','measured_internal')),
     'supported_by_external':sorted(s for s,r in sup if r=='supports' and level_of.get(s) in ('reported_by_others','measured_external','literature_claim')),
     'derived_under_model':sorted(s for s,r in sup if r in ('entails_under_model','formalizes')),
     'contradicted_by':sorted(s for s,r in sup if r=='contradicts'),'qualified_by':sorted(s for s,r in sup if r in ('qualifies','constrains')),
     'gaps':sorted(s for s,r in sup if r=='measures_gap_of'),'tests':tested.get(c['claim_id'],[]),'superseded_by':c.get('superseded_by')})
    if c['epistemic_status'] in ('measured_internal','measured_external') and not any(r=='supports' for _,r in sup) and c['claim_class']!='self_application': breaches.append(f"{c['claim_id']} is marked measured but has no supporting evidence relation")
if breaches: print('BREACHES:'); [print('  -',b) for b in breaches]
if a.check: sys.exit(1 if breaches else 0)
out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=True)
def J(df):
    for col in df.columns:
        if df[col].map(lambda x:isinstance(x,(list,dict))).any(): df[col]=df[col].map(lambda x: json.dumps(x,ensure_ascii=False) if isinstance(x,(list,dict)) else x)
        if col=='value': df[col]=df[col].map(lambda x: None if x is None else str(x))  # mixed numeric/string values kept as text; the number survives as text
    return df
frames={'claims':J(pd.DataFrame(rows['claims'])),'evidence':J(pd.DataFrame(rows['evidence'])),'relations':J(pd.DataFrame(rows['relations'])),'tests':J(pd.DataFrame(rows['tests'])),'terms':J(pd.DataFrame(rows['terms'])),'support_topology':J(pd.DataFrame(topo))}
cfg=[]
for n,df in frames.items():
    df['maxim']=MAXIM; df.to_parquet(out/f'{n}.parquet',index=False); cfg.append(f"- config_name: {n}\n  data_files: {n}.parquet"); print(f"  {n}: {len(df)} rows")
counts={n:len(df) for n,df in frames.items()}
card=(SRC/'CARD.md').read_text(encoding='utf-8').format(configs='\n'.join(cfg),maxim=MAXIM,built=datetime.date.today().isoformat(),**{f'n_{k}':v for k,v in counts.items()})
(out/'README.md').write_text(card,encoding='utf-8')
json.dump({'built':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':counts,'breaches':breaches},open(out/'build-manifest.json','w'),indent=1)
print('card + manifest written to',out)
