import json,sys,urllib.request
for i in sys.argv[1:]:
    try: m=json.load(urllib.request.urlopen(f'https://archive.org/metadata/{i}',timeout=60))
    except Exception as e: print(i,'ERR',e); continue
    md=m.get('metadata',{});fs=m.get('files',[])
    pdf=[(f['name'],round(int(f.get('size',0))/1e6,1),f.get('private')) for f in fs if f['name'].endswith('.pdf')]
    dj=[f['name'] for f in fs if f['name'].endswith('_djvu.txt')]
    print(i,'| restricted:',md.get('access-restricted-item'),'| title:',str(md.get('title'))[:60],'| date:',md.get('date'),'| pub:',str(md.get('publisher'))[:40],'| contrib:',str(md.get('contributor'))[:30],'| pdf',pdf[:2],'| djvu',len(dj),'| rights:',str(md.get('rights') or md.get('possible-copyright-status'))[:40])
