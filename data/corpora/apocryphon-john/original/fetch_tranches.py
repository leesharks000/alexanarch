#!/usr/bin/env python3
"""Tranches 2-3: fetch Codex III and IV Apocryphon plates from CCDL IIIF.
Usage: fetch_tranches.py III|IV. Uses three-witness-plate-map.json. Pace >=6s; use full/max."""
import json, urllib.request, os, time, sys, hashlib
UA={'User-Agent':'alexanarch-corpora-seating/1.0 (contact: archive@alexanarch.org)'}
cod=sys.argv[1]; rng={'III':range(1,41),'IV':range(1,50)}[cod]
apoc=json.load(open(os.path.join(os.path.dirname(__file__),'three-witness-plate-map.json')))
sel={}
for e in sorted(apoc[cod], key=lambda x:int(x['pointer'])):
    for p in e['pages']:
        if p in rng:
            if p not in sel: sel[p]=e
            elif len(e['pages'])==1 and len(sel[p]['pages'])>1: sel[p]=e
d=f"codex-{cod}"; os.makedirs(d, exist_ok=True); pins=[]
for p in sorted(sel):
    ptr=sel[p]['pointer']; dest=f"{d}/{cod}_p{p:03d}_ptr{ptr}.jpg"
    if not os.path.exists(dest):
        data=urllib.request.urlopen(urllib.request.Request(
            f"https://ccdl.claremont.edu/iiif/2/nha:{ptr}/full/max/0/default.jpg",headers=UA),timeout=180).read()
        open(dest,'wb').write(data); time.sleep(6)
    pins.append({"page":p,"pointer":ptr,"title":sel[p]['title'],
        "sha256":hashlib.sha256(open(dest,'rb').read()).hexdigest(),"size":os.path.getsize(dest)})
json.dump(pins, open(f"{d}/plate-pins.json","w"), indent=1)
print(cod, len(pins), "plates")
