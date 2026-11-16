import json, urllib.request, urllib.parse, hashlib, time, sys
ISSN=sys.argv[1]; NAME=sys.argv[2]
B=f"https://api.crossref.org/journals/{ISSN}/works"; cur="*"; items=[]
while True:
    u=B+"?rows=1000&select=DOI,title,author,issued,type,volume,issue,page,abstract,is-referenced-by-count,subtitle&cursor="+urllib.parse.quote(cur)
    for t in range(4):
        try: d=json.load(urllib.request.urlopen(u,timeout=180))["message"]; break
        except Exception as e: time.sleep(5)
    items+=d["items"]; cur=d.get("next-cursor")
    print(len(items),d["total-results"],file=sys.stderr)
    if not d["items"] or len(items)>=d["total-results"]: break
raw=json.dumps(items,ensure_ascii=False).encode(); open(f"raw-{NAME}.json","wb").write(raw)
W=[]
for w in items:
    y=(w.get("issued",{}).get("date-parts") or [[None]])[0][0]
    W.append({"doi":w["DOI"],"year":y,"type":w.get("type"),"title":" ".join(w.get("title") or []),"subtitle":" ".join(w.get("subtitle") or []),
      "authors":[" ".join(x for x in [a.get("given"),a.get("family")] if x) for a in w.get("author",[])],
      "abstract":w.get("abstract"),"vol":w.get("volume"),"issue":w.get("issue"),"page":w.get("page"),"cited_by":w.get("is-referenced-by-count",0)})
json.dump({"source":B,"read":time.strftime("%Y-%m-%d"),"raw_sha256":hashlib.sha256(raw).hexdigest(),"works":W},open(f"census-{NAME}.json","w"),ensure_ascii=False)
print(NAME,len(W))
