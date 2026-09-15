#!/usr/bin/env python3
"""panel_intake.py — seat one observation on the flattening panel from a pasted transcript.

    python3 scripts/panel_intake.py draft.json [--seat]

draft.json: {"item_id","form","surface","date","auth","transcript","sources_presented":[...],
             "capture_ids":[...], "coder", "blind": bool}
The script does NOT decide what the composition reached. It shows the item's distinction inventory with
markers, reports which markers occur in the transcript as a hint, and asks for the coding — distinctions
reached, resolved_to, false_distinction — which is entered by the coder (blind coding means the coder does
not see the item's conflation_target or prior observations; pass --blind to hide them). The transcript is
what gets seated to the Capture Registry; the panel stores the coding and the registry ids.
"""
import json, sys, argparse, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; SRC=ROOT/'datasets'/'flattening-panel'
ap=argparse.ArgumentParser(); ap.add_argument('draft'); ap.add_argument('--seat',action='store_true'); ap.add_argument('--blind',action='store_true'); a=ap.parse_args()
P=json.load(open(SRC/'panel.json')); d=json.load(open(a.draft)); items={i['item_id']:i for i in P['items']}
it=items[d['item_id']]; t=d.get('transcript','').lower()
print(f"item {it['item_id']} ({it['stratum']}) key='{it['key_string']}' form={d['form']}")
if not a.blind: print(f"  conflation_target: {it.get('conflation_target')}; prior observations: {sum(1 for o in P['observations'] if o['item_id']==it['item_id'])}")
for dist in it['distinctions']:
    hits=[m for m in dist.get('markers',[]) if m.lower() in t]
    print(f"  [{dist['id']}] {dist['label']}  markers hit: {hits or '—'}")
if not a.seat:
    print("dry run — supply 'coding' in the draft: distinctions_reached, resolved_to, false_distinction; then --seat"); sys.exit(0)
req=['distinctions_reached','resolved_to','false_distinction']
if not all(k in d for k in req): print('coding incomplete; refusing to seat'); sys.exit(1)
obs={"obs_id":f"O-{it['item_id'][2:]}-{d['form'].upper()}-{d['date'].replace('-','')}","item_id":it['item_id'],"form":d['form'],"surface":d['surface'],"date":d['date'],"auth":d.get('auth','undetermined'),
     "distinctions_reached":d['distinctions_reached'],"resolved_to":d['resolved_to'],"false_distinction":d['false_distinction'],"sources_presented":d.get('sources_presented',[]),
     "coding":{"coder":d.get('coder','operator'),"blind":bool(d.get('blind',a.blind)),"note":d.get('note','')},"capture_ids":d.get('capture_ids',[]),"write_back_seen":d.get('write_back_seen')}
if any(o['obs_id']==obs['obs_id'] for o in P['observations']): obs['obs_id']+='-b'
P['observations'].append(obs); json.dump(P,open(SRC/'panel.json','w'),ensure_ascii=False,indent=1); print('seated',obs['obs_id'])
