#!/usr/bin/env python3
"""PEO global cohort epoch — one call per publication-year cohort, diffed against the prior epoch.

  python3 scripts/peo_cohort_epoch.py            # run a new epoch and diff
  python3 scripts/peo_cohort_epoch.py --diff-only

A cohort count should be monotonically non-decreasing. Any DECREASE is an erasure
event. Cheap by design: 37 public API calls, no auth, reproducible by anyone.
"""
import json,urllib.request,urllib.parse,time,os,sys,glob
from datetime import date
UA={'User-Agent':'alexanarch-peo/1.0 (contact: archive@alexanarch.org)'}
DIR=os.path.join(os.path.dirname(__file__),'..','datasets','erasure','datacite','cohorts')
def count(year):
    u="https://api.datacite.org/dois?"+urllib.parse.urlencode({'page[size]':0,'query':f'publicationYear:{year}'})
    for a in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))['meta']['total']
        except Exception:
            if a==3: raise
            time.sleep(4*(a+1))
def epochs():
    return sorted(glob.glob(os.path.join(DIR,'*.json')))
def diff():
    e=epochs()
    if len(e)<2: print("only one epoch — nothing to diff. The baseline's value is that a second epoch can exist."); return
    a,b=json.load(open(e[-2])),json.load(open(e[-1]))
    print(f"{a['epoch']} → {b['epoch']}\n")
    drops=[]
    for y in sorted(b['cohorts']):
        o,n=a['cohorts'].get(y),b['cohorts'][y]
        if o is None or n is None: continue
        d=n-o
        if d<0: drops.append((y,o,n,d))
        print(f"  {y}  {o:>13,} → {n:>13,}  {d:+,}" + ("   ← DECREASE" if d<0 else ""))
    print()
    if drops:
        print(f"EROSION EVENTS: {len(drops)} cohorts decreased, {sum(-d for _,_,_,d in drops):,} DOIs left the index.")
        print("Before claiming erasure: check whether an adjacent cohort grew by a similar amount, which")
        print("would indicate re-dating rather than removal. That check is NOT automated.")
    else:
        print("No cohort decreased. No erasure detected at cohort granularity this epoch.")
if '--diff-only' in sys.argv: diff(); raise SystemExit
today=date.today().isoformat()
prev=epochs()
c={str(y):count(y) for y in range(1990,2027)}
for y in c: time.sleep(0.3)
tot=sum(v for v in c.values() if v)
glob_total=json.load(urllib.request.urlopen(urllib.request.Request(
  "https://api.datacite.org/dois?page%5Bsize%5D=1",headers=UA),timeout=60))['meta']['total']
out={"epoch":today,"source":"https://api.datacite.org/dois?query=publicationYear:<Y>&page[size]=0",
 "global_total_indexed":glob_total,"cohort_sum":tot,"unaccounted":glob_total-tot,
 "cohorts":c,"prior_epoch":os.path.basename(prev[-1]) if prev else None}
json.dump(out,open(os.path.join(DIR,f'{today}.json'),'w'),ensure_ascii=False,indent=1)
print(f"epoch {today} written | {tot:,} covered | global {glob_total:,}\n")
diff()
