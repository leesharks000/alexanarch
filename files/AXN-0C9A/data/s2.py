import json,urllib.request,time,sys
W=json.load(open('census.json'))['works']
URL="https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,externalIds,year"
out={}
def call(dois):
  req=urllib.request.Request(URL,data=json.dumps({"ids":["DOI:"+d for d in dois]}).encode(),headers={"Content-Type":"application/json"})
  for k in range(8):
    try: return json.loads(urllib.request.urlopen(req,timeout=60).read())
    except urllib.error.HTTPError as e:
      if e.code==400: return 'bad'
      time.sleep(4*(k+1))
    except Exception: time.sleep(5)
  return None
def run(dois):
  r=call(dois)
  if r=='bad':
    if len(dois)==1: out[dois[0]]={'_error':'400'}; return
    h=len(dois)//2; run(dois[:h]); run(dois[h:]); return
  if r is None:
    for d in dois: out[d]={'_error':'429'}
    return
  for d,x in zip(dois,r): out[d]=x
  time.sleep(2.5)
D=[w['doi'] for w in W]
for i in range(0,len(D),50): run(D[i:i+50]); print(i,len(out),flush=True)
json.dump({"source":"api.semanticscholar.org/graph/v1/paper/batch","read":"2026-11-14","results":out},open('raw/s2-crj-20261114.json','w'),indent=1)
print('done',len(out),sum(1 for v in out.values() if v and '_error' not in v))
