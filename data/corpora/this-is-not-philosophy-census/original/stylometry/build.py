import json,re,glob
def clean(a): a=re.sub(r"<[^>]+>"," ",a or ""); a=re.sub(r"\s+"," ",a).strip(); return re.sub(r"^(Abstract|ABSTRACT)[:.]?\s*","",a)
rows=[]
for f in glob.glob("../reach5/in-*.jsonl"):
    for l in open(f):
        r=json.loads(l)
        if r["id"].startswith("ap-"): continue
        rows.append({"id":r["id"],"j":r["id"].rsplit("-",1)[0],"field":"ancient","year":r["year"],"text":clean(r["abstract"])})
for w in json.load(open("../census.json"))["works"]:
    a=clean(w.get("abstract"))
    if len(a)>200 and w["year"]: rows.append({"id":f"ap-{w['n']}","j":"ap","field":"ancient","year":w["year"],"text":a})
for f in glob.glob("../cont/reachc/in-*.jsonl"):
    for l in open(f):
        r=json.loads(l); rows.append({"id":r["id"],"j":r["id"].rsplit("-",1)[0],"field":"continental","year":r["year"],"text":r["abstract"]})
for r in json.load(open("../cont/reachc/cal.json")): rows.append({"id":r["id"],"j":r["id"].rsplit("-",1)[0],"field":"continental","year":r["year"],"text":r["abstract"]})
# English only, for comparability of the language dimension
EN=set("the of and to in that is a this as for be by with which it on are not".split())
def en(t):
    w=re.findall(r"[a-z]+",t.lower()); return len(w)>40 and sum(x in EN for x in w)/len(w)>0.22
rows=[r for r in rows if en(r["text"])]
json.dump(rows,open("corpus.json","w"),ensure_ascii=False)
import collections
print(len(rows)); print(collections.Counter((r["field"],r["year"]//5*5) for r in rows if r["year"]>=2000))
