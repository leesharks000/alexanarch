import json, urllib.request, urllib.parse, hashlib, time
B="https://api.crossref.org/journals/0740-2007/works"; cur="*"; items=[]
while True:
    u=B+"?"+urllib.parse.urlencode({"rows":1000,"cursor":cur,"mailto":""})
    u=B+"?rows=1000&cursor="+urllib.parse.quote(cur)
    d=json.load(urllib.request.urlopen(u,timeout=120))["message"]
    items+=d["items"]; cur=d.get("next-cursor")
    if not d["items"] or len(items)>=d["total-results"]: break
raw=json.dumps(items,ensure_ascii=False).encode()
open("raw.json","wb").write(raw)
W=[]
for i,w in enumerate(items):
    y=(w.get("issued",{}).get("date-parts") or [[None]])[0][0]
    refs=w.get("reference") or []
    W.append({"n":i,"doi":w["DOI"],"year":y,"type":w.get("type"),"title":" ".join(w.get("title") or []),
      "authors":[(" ".join(x for x in [a.get("given"),a.get("family")] if x)) for a in w.get("author",[])],
      "has_abstract":bool(w.get("abstract")),"abstract":w.get("abstract"),"vol":w.get("volume"),"issue":w.get("issue"),"page":w.get("page"),
      "n_refs":len(refs),"refs_to_ap":sum(1 for r in refs if "ancientphil" in (r.get("DOI") or "").lower() or "Ancient Philosophy" in (r.get("journal-title") or "")),
      "refs":[{"doi":r.get("DOI"),"jt":r.get("journal-title"),"au":r.get("author"),"y":r.get("year"),"u":r.get("unstructured","")[:300]} for r in refs],
      "cited_by":w.get("is-referenced-by-count",0),"license":[l.get("URL") for l in w.get("license",[])]})
json.dump({"source":B,"read":time.strftime("%Y-%m-%d"),"raw_sha256":hashlib.sha256(raw).hexdigest(),"works":W},open("census.json","w"),ensure_ascii=False)
print(len(W))
