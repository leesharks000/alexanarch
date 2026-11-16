import json,urllib.request,hashlib,time,pathlib,os
os.environ.setdefault('SSL_CERT_FILE','/root/.ccr/ca-bundle.crt')
D=json.load(open('cp-jstor-items.json')); out=pathlib.Path('cp'); log={}
if os.path.exists('cp-log.json'): log=json.load(open('cp-log.json'))
for n,d in enumerate(D):
    i=d['identifier']
    if i in log: continue
    j=i.split('-',1)[1]; u=f"https://archive.org/download/{i}/{j}_djvu.txt"
    data=None
    for t in range(3):
        try: data=urllib.request.urlopen(u,timeout=120).read(); break
        except Exception as e: err=str(e); time.sleep(3)
    if data is None: log[i]={"error":err,"url":u}; continue
    (out/f"{i}.txt").write_bytes(data)
    log[i]={"url":u,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"title":d.get('title'),"date":d.get('date')}
    if n%50==0: json.dump(log,open('cp-log.json','w'),ensure_ascii=False); print(n,flush=True)
    time.sleep(0.3)
json.dump(log,open('cp-log.json','w'),ensure_ascii=False); print('done',len(log),sum(1 for v in log.values() if 'error' in v))
