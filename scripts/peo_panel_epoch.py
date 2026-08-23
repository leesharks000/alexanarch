#!/usr/bin/env python3
"""PEO fixed-panel epoch. Re-query every panel DOI; 404 = erased.

A cohort count measures net change and hides erasure behind minting.
A panel measures erasure directly. Run monthly:  python3 scripts/peo_panel_epoch.py
"""
import json,urllib.request,urllib.parse,time,os,glob
from datetime import date
UA={'User-Agent':'alexanarch-peo/1.0 (contact: archive@alexanarch.org)'}
DIR=os.path.join(os.path.dirname(__file__),'..','datasets','erasure','datacite','panel')
base=json.load(open(sorted(glob.glob(os.path.join(DIR,'*.json')))[0]))
res={'epoch':date.today().isoformat(),'panel_drawn':base['epoch'],'alive':{}, 'erased':{}, 'indeterminate':{}}
for y,dois in base['panel'].items():
    a=e=i=0; gone=[]
    for d in dois:
        u="https://api.datacite.org/dois/"+urllib.parse.quote(d,safe='')
        try:
            urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=45); a+=1
        except urllib.error.HTTPError as ex:
            if ex.code==404: e+=1; gone.append(d)
            else: i+=1
        except Exception: i+=1
        time.sleep(0.25)
    res['alive'][y]=a; res['erased'][y]=e; res['indeterminate'][y]=i
    if gone: res.setdefault('erased_dois',{})[y]=gone
    print(f"  {y}: alive {a} · erased {e} · indeterminate {i}")
tot=sum(res['alive'].values())+sum(res['erased'].values())+sum(res['indeterminate'].values())
res['erasure_rate_within_panel']=round(sum(res['erased'].values())/max(1,tot),5)
json.dump(res,open(os.path.join(DIR,f"result-{res['epoch']}.json"),'w'),indent=1)
print(f"\nerased {sum(res['erased'].values())} of {tot} — within-panel rate {res['erasure_rate_within_panel']:.3%}")
