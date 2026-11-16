import json,urllib.request,hashlib,time,pathlib
B=pathlib.Path('books')
items={"wolf-prolegomena-1795":"prolegomenaadho00wolfgoog","wolf-darstellung-1807-ed1833":"10254672bsb","boeckh-encyklopaedie-1877":"encyklopdieund00bcuoft",
"usener-philologie-geschichtswissenschaft-1882":"bub_gb_jJYtAQAAMAAJ","bentley-phalaris-1699":"dissertationupon00bent","valla-donatio-schwahn-1928":"defalsocreditaetementitateubner",
"casaubon-exercitationes-1614":"bub_gb_D23scf3zIVcC","lachmann-lucretius-commentarius-1850":"bub_gb_ihWGVasklRMC","madvig-adversaria-i-1871":"adversariacritic01madv",
"madvig-adversaria-ii-1873":"adversariacriti02madv","housman-manilius-ii-1912":"astronomiconrece02maniuoft","rohde-afterphilologie-1872":"bub_gb__o4uAAAAYAAJ",
"diels-doxographi-graeci-1879":"doxographigraec00dielgoog","sandys-history-classical-scholarship-i-1903":"cu31924021596824"}
log={}
for k,i in items.items():
    m=json.load(urllib.request.urlopen(f"https://archive.org/metadata/{i}",timeout=60))
    f=[x['name'] for x in m['files'] if x['name'].endswith('_djvu.txt')][0]
    u=f"https://archive.org/download/{i}/{urllib.request.quote(f)}"
    for t in range(3):
        try: data=urllib.request.urlopen(u,timeout=300).read(); break
        except Exception as e: time.sleep(5)
    (B/f"{k}.txt").write_bytes(data)
    md=m['metadata']; log[k]={"identifier":i,"file":f,"url":u,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"title":md.get('title'),"date":md.get('date'),"creator":md.get('creator'),"language":md.get('language'),"fetched":time.strftime('%Y-%m-%d')}
    print(k,len(data))
json.dump(log,open('books-log.json','w'),ensure_ascii=False,indent=1)
