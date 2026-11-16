"""Parse the seven ChatGPT outputs (signed out, 2026-11-16, pasted by the author) into gen.json: one row per abstract
(journal, n, title, abstract). Two formats: '### n\\. Title' + 'Abstract' + paragraph; 'n. Title' line + paragraph (or 'Abstract. …')."""
import re,json,pathlib
FIELD={"phronesis":"ancient","apeiron":"ancient","ap":"ancient","rip":"continental","phiToday":"continental","nous":"analytic","ppr":"analytic"}
out=[]
for p in sorted(pathlib.Path("raw").glob("*.txt")):
    j=p.stem; L=[l.strip() for l in p.read_text().split("\n")]
    items=[];cur=None
    for l in L:
        m=re.match(r"^(?:###\s*)?(\d{1,2})\\?\.\s+(.+)$",l)
        if m and int(m.group(1))==len(items)+1:
            cur={"n":int(m.group(1)),"title":m.group(2).strip(),"lines":[]}; items.append(cur); continue
        if cur is None or not l or l in("Abstract","**Abstract**"): continue
        if l.startswith("Editorial note") or l.startswith("These twenty") or l.startswith("These are") or l.startswith("ChatGPT is AI"): cur=None; continue
        cur["lines"].append(re.sub(r"^Abstract\.\s*","",l))
    for it in items:
        out.append({"id":f"gen-{j}-{it['n']:02d}","j":j,"field":FIELD[j],"n":it["n"],"title":it["title"],"text":" ".join(it["lines"]).replace("_","")})
json.dump(out,open("gen.json","w"),ensure_ascii=False,indent=1)
import collections; print(collections.Counter(r["j"] for r in out)); print(min(len(r["text"].split()) for r in out), max(len(r["text"].split()) for r in out))
