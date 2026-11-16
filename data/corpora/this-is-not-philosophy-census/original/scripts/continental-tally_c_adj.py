import json,glob,collections
inp={}
for f in glob.glob("in-c*.jsonl"):
    for l in open(f): r=json.loads(l); inp[r["id"]]=r
for r in json.load(open("cal.json")): inp[r["id"]]=r
CAL={"rip-931":"E","rip-868":"E","rip-836":"C","phiToday-2664":"C","phiToday-3049":"C","rip-1075":"F","rip-909":"E","phiToday-3183":"G","rip-893":"G","phiToday-3152":"F","rip-985":"G","rip-820":"E","rip-50":"E","cpr-822":"C"}
out={k:{"id":k,"code":v,"dir":""} for k,v in CAL.items()}; bad=[]
for f in glob.glob("out-c*.jsonl"):
    for l in open(f):
        if not l.strip(): continue
        r=json.loads(l)
        if r["id"] not in inp or r["quote"] not in inp[r["id"]]["abstract"]: bad.append(r["id"]); continue
        out[r["id"]]=r
ADJ=json.load(open("reachc-adjudicated.json")); out={k:ADJ.get(k,v) for k,v in out.items()}
print("rows",len(out),"of",len(inp),"invalid",bad)
P=lambda y:"2000–09" if y<2010 else "2010–15" if y<2016 else "2016–20" if y<2021 else "2021–26"
def tab(sel,label):
    print(f"\n== {label}\n{'group':9} {'period':8} {'n':>4} "+" ".join(f"{k:>4}" for k in "ABCDEFG")+"  anchored%  inside-one%")
    for j in ["ALL","rip","phiToday","cpr"]:
        cs=collections.defaultdict(collections.Counter)
        for k,v in out.items():
            if v["code"]=="X": continue
            if j!="ALL" and not k.startswith(j+"-"): continue
            cs[P(inp[k]["year"])][v["code"]]+=1
        for p in sorted(cs):
            c=cs[p]; n=sum(c.values())
            if n<15: continue
            print(f"{j:9} {p:8} {n:4} "+" ".join(f"{100*c[x]/n:4.0f}" for x in "ABCDEFG")+f"  {100*(n-c['G'])/n:8.0f}  {100*(c['A']+c['B']+c['C'])/n:9.0f}")
tab(lambda k:True,"continental reach, %")
print("\nD rows:",[(inp[k]["year"],v.get("dir"),inp[k]["title"][:60]) for k,v in out.items() if v["code"]=="D"])
json.dump(out,open("reachc-coded.json","w"),ensure_ascii=False)
