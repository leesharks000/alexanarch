"""Locate each Plato/Aristotle article of AGPh 1888–1924 (census codes, group Plato or Aristotle; numbered duplicates once)
in the seated text of its volume, and take its opening: the 170 words after the byline. A title is matched by a run of
4–8 of its folded words; among the matches, a table-of-contents line (roman-numeral entries or leader dots within the next
40 words) and a running head (no byline) are refused; the match taken is the first followed within 15 words by a byline
(Von, with the OCR's misreadings Yon, Voii, Vou, \\oii; Par, By, Di, Del; Dargestellt von); a match followed by a page-number list or a heading of the volume's back matter is refused. Not located: the article's title is not found with a byline (OCR damage, or a Jahresbericht entry)."""
import json,re,pathlib,unicodedata,bisect
SV=pathlib.Path(__file__).resolve().parent.parent
T=pathlib.Path("/home/claude/alexanarch/data/corpora/agph-archiv-1888-1923/text")
C=json.load(open(SV/"codes-agph.json")); W={w['doi']:w for w in json.load(open(SV/"census-agph.json"))["works"]}
def fw(x): return re.sub(r"[^a-zäöüßéèàçâêîôû0-9]+","",unicodedata.normalize("NFC",x.lower().replace("ſ","s")))
vfile={}
for p in T.glob("archivfrgeschi*steiuoft.txt"):
    m=re.match(r"archivfrgeschi(\d+)steiuoft",p.name)
    if m: vfile[int(m.group(1))]=p
for v in (33,34,35,36): vfile[v]=T/"archivfrgeschi33a36steiuoft.txt"
BYL=re.compile(r"^([VY\\\\][oö0][nuil]{1,2}|VON|Par|PAR|By|BY|Di|Del|Dargestellt)\.?$")
BY=re.compile(r"^(von|par|by|di|del|dr|prof|professor)$")
TOC=re.compile(r"^[ivxl]+$")
PASS=0
cache={}; out=[]; seen=set()
for c in C:
    if not (c['year'] and c['year']<=1924 and c['group'] in ('Plato','Aristotle')): continue
    w=W[c['doi']]; v=int(w['vol']) if str(w.get('vol') or '').isdigit() else None
    t=re.sub(r"^[IVXLC]+\.\s*","",c['title']).strip(); key=(v,t.lower())
    if key in seen: continue
    seen.add(key)
    rec={"doi":c['doi'],"year":c['year'],"vol":v,"title":t,"group":c['group'],"opening":None}
    if v in vfile:
        if v not in cache:
            words=vfile[v].read_text(errors="replace").split(); f=[fw(x) for x in words]
            idx=[i for i,x in enumerate(f) if x]; F=[f[i] for i in idx]; cache[v]=(words,idx,F)
        words,idx,F=cache[v]
        tw=[x for x in (fw(y) for y in t.split()) if x]
        hit=None; fallback=None
        for L in range(min(len(tw),8),3,-1):
            for s0 in range(len(tw)-L+1):
                pat=tw[s0:s0+L]
                for j in range(len(F)-L):
                    if F[j]!=pat[0] or F[j:j+L]!=pat: continue
                    nxt=F[j+L:j+L+40]; raw=" ".join(words[idx[j+L]:idx[min(j+L+40,len(idx)-1)]])
                    if sum(1 for x in nxt if TOC.match(x))>=2 or "...." in raw or ". . ." in raw: continue
                    if re.search(r"\d{2,3}\s+[IVX]+\.|Rezensionen|Zeitschriftenschau|Inhalt", raw): continue
                    by=[k for k in range(15) if j+L+k+1<len(idx) and BYL.match(words[idx[j+L+k]])]
                    if not by:
                        if PASS==2 and j>len(F)*0.03 and (fallback is None): fallback=(j,j+L)
                        continue
                    hit=(j,j+L+by[0]); break
                if hit: break
            if hit: break
        if not hit and fallback: hit=fallback; rec["located_by"]="title without byline (second pass)"
        if hit:
            st=idx[hit[1]]; rec["opening"]=" ".join(words[st:st+190]); rec["at_word"]=st
            rec.setdefault("located_by","title and byline")
    out.append(rec)
json.dump(out,open("early/openings.json","w"),ensure_ascii=False,indent=1)
print(len(out),"articles;",sum(1 for r in out if r["opening"]),"located")
