#!/usr/bin/env python3
"""flattening_battery.py — computes the EA-FLAT-01 §4 battery from datasets/flattening-panel/panel.json.

N_eff^sense   per item and address form: effective number of distinctions reached across observations (exp of entropy of resolved_to)
R_new         representability of dated distinctions after a cutoff: share whose composition reaches them as their own kind
DS            distinction survival: per item, share of the reference inventory reached in the latest observation per form
FALSE         false-distinction rate: observations asserting a distinction the reference does not carry
N_eff^source  effective number of presented sources per observation, and its share curve
recovery      share of items whose latest observation reaches a distinction lost at an earlier observation
write_back    share of observations marked write_back_seen
divergence    the head instruments over the same period, so ΔH_head and ΔD_world can be read side by side
Validates against schema.json; --check exits 1 on breach. Nothing is fetched; observations enter by seating.
"""
import json, math, sys, argparse, pathlib, collections, datetime
try: import jsonschema
except ImportError: jsonschema=None
ROOT=pathlib.Path(__file__).resolve().parents[1]; SRC=ROOT/'datasets'/'flattening-panel'
ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); ap.add_argument('--cutoff',default='2024-01-01'); ap.add_argument('--out',default=str(ROOT/'battery')); a=ap.parse_args()
schema=json.load(open(SRC/'schema.json')); P=json.load(open(SRC/'panel.json'))
breaches=[]
if jsonschema:
    for e in jsonschema.Draft202012Validator(schema).iter_errors(P): breaches.append('/'.join(map(str,e.path))+': '+e.message[:140])
items={i['item_id']:i for i in P['items']}
for o in P['observations']:
    if o['item_id'] not in items: breaches.append(f"{o['obs_id']}: unknown item"); continue
    ids={d['id'] for d in items[o['item_id']]['distinctions']}
    for d in o['distinctions_reached']:
        if d not in ids: breaches.append(f"{o['obs_id']}: unknown distinction {d}")
    if o['form'] not in {f['form'] for f in items[o['item_id']]['address_family']}: breaches.append(f"{o['obs_id']}: form {o['form']} not in the item's address family")
if breaches: print('BREACHES:'); [print('  -',b) for b in breaches]
if a.check: sys.exit(1 if breaches else 0)
def eff(counter):
    tot=sum(counter.values()); 
    if not tot: return None
    ps=[c/tot for c in counter.values()]; return round(math.exp(-sum(p*math.log(p) for p in ps if p>0)),2)
by_item=collections.defaultdict(list)
for o in sorted(P['observations'],key=lambda o:o['date']): by_item[o['item_id']].append(o)
rows=[]; false_n=0; n_obs=0; src_eff=[]; wb=[]; recov=[]
for iid,it in items.items():
    obs=by_item.get(iid,[]); inv=[d['id'] for d in it['distinctions']]
    sense_by_form={}
    for form in {o['form'] for o in obs}:
        c=collections.Counter(o['resolved_to'] or 'multi' for o in obs if o['form']==form); sense_by_form[form]={'n':sum(c.values()),'N_eff_sense':eff(c),'resolved':dict(c)}
    latest_by_form={}
    for o in obs: latest_by_form[o['form']]=o
    ds={f:round(len(set(o['distinctions_reached'])&set(inv))/len(inv),2) for f,o in latest_by_form.items()}
    # recovery: a distinction reached earlier, lost later, reached again later
    reached_seq=[set(o['distinctions_reached']) for o in obs if o['form']=='naked']
    lost=set(); recovered=set()
    seen=set()
    for s in reached_seq:
        for d in seen-s: lost.add(d)
        for d in s&lost: recovered.add(d)
        seen|=s
    if lost: recov.append(len(recovered)/len(lost))
    for o in obs:
        n_obs+=1; false_n+= 1 if o.get('false_distinction') else 0
        if o.get('sources_presented'): src_eff.append(eff(collections.Counter(o['sources_presented'])))
        if o.get('write_back_seen') is not None: wb.append(1 if o['write_back_seen'] else 0)
    rows.append({'item_id':iid,'stratum':it['stratum'],'inventory':len(inv),'n_obs':len(obs),'N_eff_sense_by_form':sense_by_form,'DS_latest_by_form':ds,'lost':sorted(lost),'recovered':sorted(recovered)})
# R_new: dated distinctions after cutoff, share reached as their own kind in any naked observation
dated=[(iid,d) for iid,it in items.items() for d in it['distinctions'] if d.get('dated') and d['dated']>=a.cutoff]
reached_new=[(iid,d['id']) for iid,d in dated if any(d['id'] in o['distinctions_reached'] and o['form']=='naked' for o in by_item.get(iid,[]))]
observed_new=[(iid,d['id']) for iid,d in dated if any(o['form']=='naked' for o in by_item.get(iid,[]))]
summary={'built':datetime.date.today().isoformat(),'items':len(items),'observations':n_obs,'strata':dict(collections.Counter(i['stratum'] for i in items.values())),
 'R_new':{'cutoff':a.cutoff,'dated_distinctions':len(dated),'with_naked_observation':len(observed_new),'reached_as_own_kind':len(reached_new),'rate':round(len(reached_new)/len(observed_new),2) if observed_new else None},
 'false_distinction_rate':round(false_n/n_obs,2) if n_obs else None,
 'N_eff_source_mean':round(sum(x for x in src_eff if x)/len([x for x in src_eff if x]),2) if src_eff else None,
 'write_back_rate':round(sum(wb)/len(wb),2) if wb else None,'recovery_rate':round(sum(recov)/len(recov),2) if recov else None,
 'head_instruments':P['head_instruments'],'breaches':breaches,'coverage_note':'items with no observation yet count in the panel and not in the rates; every rate here is over the archive stratum and two taxonomy/fact items, since the world strata have not been run'}
out=pathlib.Path(a.out); out.mkdir(exist_ok=True)
json.dump({'summary':summary,'items':rows},open(out/'battery.json','w'),ensure_ascii=False,indent=1)
L=[f"# Flattening battery — {summary['built']}\n",f"Panel: {summary['items']} items across strata {summary['strata']}; {summary['observations']} observations seated. World strata ran as wave 1 on 2026-09-15; {sum(1 for r in rows if r['n_obs'])} of {summary['items']} items now carry observations. Rates below are over all seated observations across six strata.\n",
 f"- R_new (dated ≥ {a.cutoff}, naked address): {summary['R_new']['reached_as_own_kind']} of {summary['R_new']['with_naked_observation']} observed reached as their own kind → {summary['R_new']['rate']}",
 f"- false-distinction rate: {summary['false_distinction_rate']} of observations assert a distinction the reference does not carry",
 f"- N_eff^source (mean effective presented sources per observation): {summary['N_eff_source_mean']}",
 f"- write-back rate (compositions found as later sources, where recorded): {summary['write_back_rate']}",
 f"- recovery rate (distinctions lost at a naked address and reached again later): {summary['recovery_rate']}",
 "\n| item | stratum | inventory | obs | N_eff^sense by form | DS latest by form | lost | recovered |","|---|---|---|---|---|---|---|---|"]
for r in rows: L.append(f"| {r['item_id']} | {r['stratum']} | {r['inventory']} | {r['n_obs']} | {'; '.join(f'{f}:{v['N_eff_sense']}' for f,v in r['N_eff_sense_by_form'].items()) or '—'} | {'; '.join(f'{f}:{v}' for f,v in r['DS_latest_by_form'].items()) or '—'} | {','.join(r['lost']) or '—'} | {','.join(r['recovered']) or '—'} |")
L.append("\n## Head instruments over the same period\n\n| surface | date | instrument | value | source |\n|---|---|---|---|---|")
for h in P['head_instruments']: L.append(f"| {h['surface']} | {h['date']} | {h['instrument']} | {h['value']} | {h.get('source','')} |")
L.append("\nDivergence signature: read ΔH_head (the rows above) beside ΔD_world (DS, R_new, N_eff^sense over time) on the same surface. With the world strata unrun, the signature cannot yet be read; the archive stratum shows DS falling at naked addresses (Sappho fr31→fr147+false fr2; semantic economy sharks→business; operative→operational) while the head rows show the admitted set concentrating.")
(out/'battery.md').write_text('\n'.join(L)+'\n',encoding='utf-8'); print('\n'.join(L))
