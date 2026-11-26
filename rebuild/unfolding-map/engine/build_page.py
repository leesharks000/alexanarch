#!/usr/bin/env python3
"""Builds the demonstration page from derivations.json and runs.json: the same derivations, run again in the page by a port of the engine,
so that a reader can switch an operator off and watch the target fail.   python3 build_page.py"""
import json, re, pathlib, html
H = pathlib.Path(__file__).parent; DS = json.loads((H / "derivations.json").read_text(encoding="utf-8")); RUN = json.loads((H / "runs.json").read_text(encoding="utf-8"))
R = {r["id"]: r for r in RUN["runs"]}
WB = "(?:(?<![α-ω])(?=[α-ω])|(?<=[α-ω])(?![α-ω]))"
js_rx = lambda rx: rx.replace(r"\b", WB).replace(r"\w", "[α-ω]")
data = []
for d in DS["derivations"]:
    r = R[d["id"]]
    data.append({"id": d["id"], "title": d["title"], "family": d["family"], "note": d.get("note"), "records": d.get("records", []),
                 "members": [{**m, "rx": js_rx(m["rx"])} for m in d["members"]],
                 "steps": [{**s, **({"marker": js_rx(s["marker"])} if "marker" in s else {}), **({"negation": js_rx(s["negation"])} if "negation" in s else {})} for s in d["steps"]],
                 "seed": {"loc": d["seed"], "text": r["seed"]["text"]}, "target": {"loc": d["target"], "text": r["target"]["text"]},
                 "controls": [{"loc": c["loc"], "label": c["label"], "text": c["text"]} for c in r["controls"]], "search": r["search"], "py": {"score": r["target"]["score"], "controls": [c["score"] for c in r["controls"]]}})
nt1 = sum(1 for r in RUN["runs"] if r["search"]["new_testament"]["passing"] == 1); lx0 = sum(1 for r in RUN["runs"] if r["search"]["septuagint"]["passing"] == 0)
ntv = RUN["runs"][0]["search"]["new_testament"]["verses_searched"]; lxv = RUN["runs"][0]["search"]["septuagint"]["verses_searched"]
PAGE = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Midrashim Transform Bench</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Gentium+Book+Plus:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>
/* layout: one column of derivation cards; each card reads top to bottom as seed, operators, emission, target, controls, search */
:root{--bg:#eef0f3;--card:#fbfcfd;--ink:#1b2230;--mute:#5a6475;--line:#cfd5de;--accent:#2b3f8f;--ok:#1f6f4a;--bad:#a23b2a;--warn:#8a6412;
 --m0:#cfe0ff;--m1:#ffe2b8;--m2:#d5f0d2;--m3:#f6d3e6;--m4:#e3dcff;--m5:#fff0a8;--m6:#cdeef0;--drop:#e7e9ee;
 --greek:"Gentium Book Plus","Gentium Plus","Noto Serif",Georgia,serif;--body:"Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#12161d;--card:#1a2029;--ink:#e6eaf1;--mute:#9aa5b6;--line:#2f3846;--accent:#9db2ff;--ok:#6fcf9b;--bad:#f08a78;--warn:#e2bd62;
 --m0:#27407a;--m1:#6b4a17;--m2:#24553a;--m3:#6a2f52;--m4:#40357e;--m5:#5e5413;--m6:#1d5559;--drop:#2a313d}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#12161d;--card:#1a2029;--ink:#e6eaf1;--mute:#9aa5b6;--line:#2f3846;--accent:#9db2ff;--ok:#6fcf9b;--bad:#f08a78;--warn:#e2bd62;
 --m0:#27407a;--m1:#6b4a17;--m2:#24553a;--m3:#6a2f52;--m4:#40357e;--m5:#5e5413;--m6:#1d5559;--drop:#2a313d}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 var(--body)}
main{max-width:860px;margin:0 auto;padding:20px 16px 64px;display:flex;flex-direction:column;gap:18px}
h1{font:700 1.7rem/1.15 var(--greek);margin:8px 0 0;text-wrap:balance}h2{font:700 1.15rem/1.25 var(--body);margin:0;text-wrap:balance}
p{margin:0;max-width:66ch}.lede{color:var(--mute)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.fact{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px}.fact b{display:block;font:700 1.5rem/1.1 var(--body);font-variant-numeric:tabular-nums}.fact span{color:var(--mute);font-size:.86rem}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.bar button{font:600 .9rem var(--body);padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.bar button[aria-pressed="true"]{background:var(--accent);color:var(--bg);border-color:var(--accent)}
button:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:12px}
.head{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;justify-content:space-between}
.id{font:600 .82rem var(--body);color:var(--mute);letter-spacing:.02em}
.pill{font:700 .8rem var(--body);padding:3px 9px;border-radius:999px;border:1px solid currentColor;white-space:nowrap}.pass{color:var(--ok)}.fail{color:var(--bad)}.tie{color:var(--warn)}
.lab{font:700 .72rem var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.gk{font:1.12rem/1.6 var(--greek);overflow-wrap:anywhere}.gk small{font:.8rem var(--body);color:var(--mute)}
mark{color:inherit;border-radius:3px;padding:0 2px}.absent{background:var(--drop);text-decoration:line-through;color:var(--mute)}
ol.steps{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}
ol.steps li{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;align-items:start;border-left:3px solid var(--line);padding-left:10px}
ol.steps li.off{opacity:.45}ol.steps input{margin-top:5px;width:18px;height:18px}
.op{font:700 .92rem var(--body);color:var(--accent)}.does{color:var(--mute);font-size:.9rem}
.chips{display:flex;flex-wrap:wrap;gap:5px;grid-column:2}.chip{font:.9rem var(--greek);padding:1px 7px;border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:.92rem}td,th{padding:4px 6px;border-top:1px solid var(--line);text-align:left;vertical-align:top}td.n{font-variant-numeric:tabular-nums;white-space:nowrap;text-align:right}
details{border-top:1px solid var(--line);padding-top:8px}summary{cursor:pointer;font-weight:600}
.note{color:var(--mute);font-size:.92rem}.search{font-size:.92rem}
footer{color:var(--mute);font-size:.88rem;display:flex;flex-direction:column;gap:8px}
@media (prefers-reduced-motion:no-preference){ol.steps li{transition:opacity .15s}}
</style></head><body><main>
<header><div class="lab">Revelation First · working demonstration · 26 November 2026</div>
<h1>The midrashim transform, run</h1></header>
<p>Each card takes a sentence of the Apocalypse (or of Philo, upstream of it), applies a short list of named operators, and gets a prediction: which words the later text keeps, in what order, which it drops, what it puts in their place. The prediction is then checked against the Greek of the later text, against rival sources, and against every verse of the New Testament and the Septuagint.</p>
<p class="lede">Untick an operator and the card runs again without it. The derivations were written with their targets in view, so a pass shows that the change can be stated in these operators; the controls and the search show how few other verses fit the same statement.</p>
<section class="facts" id="facts"></section>
<nav class="bar" id="fams" aria-label="Families"></nav>
<div id="cards" style="display:flex;flex-direction:column;gap:18px"></div>
<footer><p>Texts: Nestle 1904, Swete's Septuagint and Cohn–Wendland's Philo as seated in the Crimson Hexagonal Archive (alexanarch.org). A member is matched with accents and case removed. The search counts come from the engine's run over the seats and do not change when an operator is switched off.</p>
<p>Frozen __DATE__ · derivations sha256 __SHA__</p></footer>
</main>
<script>
const DATA=__DATA__, OPS=__OPS__, NTV=__NTV__, LXV=__LXV__;
function normMap(s){let out="",map=[];for(let i=0;i<s.length;i++){const d=s[i].normalize("NFD");let b="";for(const c of d){const l=c.toLowerCase().replace("ς","σ");if(l>="α"&&l<="ω")b+=l;}
  if(b){for(const c of b){out+=c;map.push(i);}}else{out+=" ";map.push(i);}}return {n:out,map};}
const rx=(p,f)=>new RegExp(p,f||"");
function emit(d,on){const M=Object.fromEntries(d.members.map(m=>[m.id,m]));const ns=normMap(d.seed.text).n;
  let state=d.members.filter(m=>m.in_seed!==false).map(m=>m.id);const at=k=>{const m=rx(M[k].rx).exec(ns);return m?m.index:1e6};state.sort((a,b)=>at(a)-at(b));
  let dropped=[],marker=null,neg=[],trace=[state.slice()];
  d.steps.forEach((st,i)=>{if(on[i]){const op=st.op;
    if(op==="PARTITION"){dropped=dropped.concat(state.filter(k=>!st.keep.includes(k)));state=state.filter(k=>st.keep.includes(k));}
    else if(op==="REORDER"){const o=st.order.filter(k=>state.includes(k));state=o.concat(state.filter(k=>!o.includes(k)));}
    else if(["SUBSTITUTE","SUBSTITUTE-OBJECT","TRANSFER-ATTRIBUTE","REVERSE-DOER","STATION","HIDE"].includes(op)){const j=state.indexOf(st.old);if(j>=0){state[j]=st.new;dropped.push(st.old);}}
    else if(op==="CITE-AS-SCRIPTURE")marker=st.marker;else if(op==="UNDO")neg.push(st.negation);}
    trace.push(state.slice());});
  return {M,state,dropped,marker,neg,trace};}
function score(e,text){const {n}=normMap(text);const has=k=>rx(e.M[k].rx).test(n);const present=e.state.filter(has);let at=0,ord=true;
  for(const k of e.state){const r=rx(e.M[k].rx,"g");r.lastIndex=at;const m=r.exec(n);if(!m){ord=false;break;}at=m.index+1;}
  const c=[["kept members present",present.length,e.state.length]];if(e.state.length>1)c.push(["in the emitted order",ord?1:0,1]);
  if(e.dropped.length)c.push(["dropped members absent",e.dropped.filter(k=>!has(k)).length,e.dropped.length]);
  if(e.marker)c.push(["marker present",rx(e.marker).test(n)?1:0,1]);if(e.neg.length)c.push(["the seed's ‘no more’ absent",e.neg.filter(r=>!rx(r).test(n)).length,e.neg.length]);
  const got=c.reduce((a,x)=>a+x[1],0),of=c.reduce((a,x)=>a+x[2],0);return {checks:c,score:got/of,pass:got===of};}
const esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function hl(text,e,ids,d){const {n,map}=normMap(text);let spans=[];ids.forEach(k=>{const m=rx(e.M[k].rx).exec(n);if(m&&m[0].length){spans.push([map[m.index],map[m.index+m[0].length-1]+1,d.members.findIndex(x=>x.id===k)%7,e.M[k].gloss]);}});
  spans.sort((a,b)=>a[0]-b[0]);let out="",p=0;for(const [a,b,c,g] of spans){if(a<p)continue;out+=esc(text.slice(p,a))+`<mark style="background:var(--m${c})" title="${esc(g)}">`+esc(text.slice(a,b))+"</mark>";p=b;}return out+esc(text.slice(p));}
const chip=(e,d,k,off)=>`<span class="chip ${off?"absent":""}" ${off?"":`style="background:var(--m${d.members.findIndex(x=>x.id===k)%7})"`} title="${esc(e.M[k].gloss)}">${esc(e.M[k].greek)}</span>`;
const nice=l=>l.replace(/^gnt:/,"").replace(/^lxx:/,"LXX ").replace(/^philo:/,"Philo, ").replace(/_/g," ").replace(/#2$/," (book II)");
const state={};
function card(d){const on=state[d.id]||(state[d.id]=d.steps.map(()=>true));const e=emit(d,on);const t=score(e,d.target.text);const cs=d.controls.map(c=>({...c,...score(e,c.text)}));
  const all=on.every(x=>x);const tie=t.pass&&cs.some(c=>c.pass);const verdict=!t.pass?["fail","target does not fit"]:tie?["tie","fits; a control fits too"]:["pass","fits; no control fits"];
  const seedIds=d.members.filter(m=>m.in_seed!==false).map(m=>m.id);const s=d.search;
  return `<article class="card" id="c-${d.id.replace(/[^a-z0-9]+/gi,"-")}"><div class="head"><div><div class="id">${esc(d.family)} · ${esc(d.id)}</div><h2>${esc(d.title)}</h2></div><span class="pill ${verdict[0]}">${verdict[1]} · ${t.score.toFixed(2)}</span></div>
  <div><div class="lab">Seed · ${esc(nice(d.seed.loc))}</div><div class="gk">${hl(d.seed.text,e,seedIds,d)}</div></div>
  <div><div class="lab">Operators</div><ol class="steps">${d.steps.map((st,i)=>`<li class="${on[i]?"":"off"}"><input type="checkbox" id="s-${d.id}-${i}" data-d="${esc(d.id)}" data-i="${i}" ${on[i]?"checked":""} aria-label="apply ${st.op}"><label for="s-${d.id}-${i}"><span class="op">${st.op}</span> <span class="does">${esc(OPS[st.op])}</span></label><div class="chips">${e.trace[i+1].map(k=>chip(e,d,k)).join("")}</div></li>`).join("")}</ol></div>
  <div><div class="lab">Emission</div><div class="chips">${e.state.map(k=>chip(e,d,k)).join("")}${e.dropped.map(k=>chip(e,d,k,true)).join("")}${e.marker?'<span class="chip" style="border:1px dashed var(--line)">+ marked as written</span>':""}${e.neg.length?'<span class="chip" style="border:1px dashed var(--line)">− οὐ μὴ … ἔτι</span>':""}</div></div>
  <div><div class="lab">Target · ${esc(nice(d.target.loc))}</div><div class="gk">${hl(d.target.text,e,e.state.concat(e.dropped),d)}</div>
  <table><tbody>${t.checks.map(c=>`<tr><td>${c[0]}</td><td class="n ${c[1]===c[2]?"pass":"fail"}">${c[1]} of ${c[2]}</td></tr>`).join("")}</tbody></table></div>
  ${cs.length?`<details ${cs.some(c=>c.pass)?"open":""}><summary>Controls: ${cs.map(c=>`${esc(c.label)} ${c.score.toFixed(2)}`).join(" · ")}</summary>${cs.map(c=>`<div style="margin-top:8px"><div class="lab">${esc(c.label)} · ${esc(nice(c.loc))} · <span class="${c.pass?"tie":""}">${c.score.toFixed(2)}</span></div><div class="gk">${hl(c.text,e,e.state.concat(e.dropped),d)}</div></div>`).join("")}</details>`:""}
  <div class="search"><span class="lab">Search, all operators on</span><br>New Testament: <b>${s.new_testament.passing}</b> of ${s.new_testament.verses_searched.toLocaleString()} verses fit (${s.new_testament.refs.slice(0,4).map(esc).join(", ")||"none"}). Septuagint: <b>${s.septuagint.passing}</b> of ${s.septuagint.verses_searched.toLocaleString()}${s.septuagint.refs.length?" ("+s.septuagint.refs.slice(0,3).map(esc).join(", ")+")":""}.</div>
  ${d.note?`<p class="note">${esc(d.note)}</p>`:""}${d.records.length?`<p class="note">Records: ${d.records.map(n=>`<a href="https://www.alexanarch.org/s/records/${n}/">#${n}</a>`).join(", ")}</p>`:""}</article>`;}
let fam="All";const fams=["All",...new Set(DATA.map(d=>d.family))];
function draw(){document.getElementById("fams").innerHTML=fams.map(f=>`<button aria-pressed="${f===fam}" data-f="${esc(f)}">${esc(f)}</button>`).join("");
  document.getElementById("cards").innerHTML=DATA.filter(d=>fam==="All"||d.family===fam).map(card).join("");}
document.getElementById("facts").innerHTML=[[DATA.length,"derivations, run against the seated Greek"],[__NT1__,"whose emission fits exactly one verse of the New Testament"],[__LX0__,"whose emission fits no verse of the Septuagint"],[Object.keys(OPS).length,"operators, declared before the run"]].map(x=>`<div class="fact"><b>${x[0]}</b><span>${x[1]}</span></div>`).join("");
document.addEventListener("click",ev=>{const b=ev.target.closest("button[data-f]");if(b){fam=b.dataset.f;draw();}});
document.addEventListener("change",ev=>{const i=ev.target.closest("input[data-d]");if(i){state[i.dataset.d][+i.dataset.i]=i.checked;const d=DATA.find(x=>x.id===i.dataset.d);const el=document.getElementById("c-"+d.id.replace(/[^a-z0-9]+/gi,"-"));el.outerHTML=card(d);}});
draw();
</script></body></html>'''
out = (PAGE.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__OPS__", json.dumps(RUN["operators"], ensure_ascii=False)).replace("__NTV__", str(ntv)).replace("__LXV__", str(lxv))
       .replace("__NT1__", str(nt1)).replace("__LX0__", str(lx0)).replace("__DATE__", DS["frozen"]["date"]).replace("__SHA__", DS["frozen"]["sha256_of_derivations"][:16] + "…"))
(H / "index.html").write_text(out, encoding="utf-8"); print(len(out), nt1, lx0)
