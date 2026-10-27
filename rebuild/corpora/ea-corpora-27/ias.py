import json,sys,urllib.request,urllib.parse
def s(q,rows=12):
    u='https://archive.org/advancedsearch.php?'+urllib.parse.urlencode({'q':q,'fl[]':['identifier','title','date','year','publisher','mediatype','contributor','collection'],'rows':rows,'output':'json'},doseq=True)
    return json.load(urllib.request.urlopen(u,timeout=60))['response']['docs']
for q in sys.argv[1:]:
    print('##',q)
    for d in s(q):
        print(' ',d.get('identifier'),'|',str(d.get('title'))[:80],'|',d.get('date') or d.get('year'),'|',str(d.get('publisher'))[:50],'|',str(d.get('contributor'))[:40])
