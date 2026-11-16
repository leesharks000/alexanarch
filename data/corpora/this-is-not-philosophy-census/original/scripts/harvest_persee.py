"""Harvest article-level Dublin Core records of a Persée series by OAI-PMH, 2026-11-15. Writes <series>.jsonl (title, date, id, creators, type)."""
import sys,urllib.request,urllib.parse,re,json,time,html
series=sys.argv[1]; out=open(f"{series}.jsonl","w"); base="https://oai.persee.fr/oai"
q={"verb":"ListRecords","metadataPrefix":"oai_dc","set":f"persee:serie-{series}:doc"}; n=0
while True:
    for t in range(5):
        try: x=urllib.request.urlopen(base+"?"+urllib.parse.urlencode(q),timeout=120).read().decode("utf-8"); break
        except Exception as e: time.sleep(10)
    for rec in re.findall(r"<record>(.*?)</record>",x,re.S):
        g=lambda tag: [html.unescape(v).strip() for v in re.findall(rf"<dc:{tag}>(.*?)</dc:{tag}>",rec,re.S)]
        ids=[i for i in g("identifier") if i.startswith("https://www.persee.fr/doc/")]
        out.write(json.dumps({"title":(g("title") or [""])[0],"date":(g("date") or [""])[0],"id":(ids or [""])[0],"creator":g("creator"),"type":g("type")},ensure_ascii=False)+"\n"); n+=1
    tok=re.search(r"<resumptionToken[^>]*>([^<]+)</resumptionToken>",x)
    if not tok: break
    q={"verb":"ListRecords","resumptionToken":tok.group(1)}
    if n%2000<100: print(series,n,flush=True)
print(series,"done",n)
