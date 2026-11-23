// N3I-OPTICAL-SHAPE, reproducible Node.js 20+ script; no third-party dependencies.
// Source: public 3I-ATLAS/discovery-paper CSV, not redistributed.
const source="https://raw.githubusercontent.com/3I-ATLAS/discovery-paper/main/src/data/3I-Reflectivity_JN_edit.csv";
const raw=await (await fetch(source)).text();
if(!raw.includes("3I Refl")) throw new Error("Unexpected source schema");
const a=raw.trim().replace(/^\uFEFF/,"").split(/\r?\n/).slice(1).map(s=>s.split(",").map(Number));
if(a.length!==1603||a.some(v=>v.length!==2||!v.every(Number.isFinite)))throw new Error("Source changed; inspect provenance");
const cuts=[];for(let i=1;i<a.length;i++)if(a[i][0]-a[i-1][0]>.001)cuts.push(i);
if(cuts.length!==1||cuts[0]!==507)throw new Error("Segment gap changed");
const groups=[a.slice(0,507),a.slice(507)];
const median=x=>{const v=[...x].sort((a,b)=>a-b);return v[Math.floor(v.length/2)]};
function prep(g,k){const v=g.map(q=>q[1]);const r=v.map((x,i)=>x-median(v.slice(Math.max(0,i-k),Math.min(v.length,i+k+1))));const trimmed=r.slice(k,-k),m=median(trimmed),mad=1.4826*median(trimmed.map(x=>Math.abs(x-m)))||1;return trimmed.map(x=>Math.max(-4,Math.min(4,(x-m)/mad)))}
function ac(x,l){const n=x.length-l;let a=0,b=0;for(let i=0;i<n;i++){a+=x[i];b+=x[i+l]}a/=n;b/=n;let num=0,s1=0,s2=0;for(let i=0;i<n;i++){const t=x[i]-a,u=x[i+l]-b;num+=t*u;s1+=t*t;s2+=u*u}return num/Math.sqrt(s1*s2)}
function best(x){let o={lag:0,r:-Infinity};for(let lag=8;lag<=120;lag++){const r=ac(x,lag);if(r>o.r)o={lag,r}}return o}
let seed=20261120;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
function shuffle(x,B){const blocks=[];for(let i=0;i<x.length;i+=B)blocks.push(x.slice(i,i+B));for(let i=blocks.length-1;i>0;i--){const j=Math.floor(rand()*(i+1));[blocks[i],blocks[j]]=[blocks[j],blocks[i]]}return blocks.flat()}
const results=[];
for(const k of [15,30,60]){
 const xs=groups.map(g=>prep(g,k));
 const observed=xs.map(best);
 const nulls=Array.from({length:249},()=>xs.map(x=>best(shuffle(x,16)).r));
 const max=Math.max(...observed.map(o=>o.r));
 const maxNull=nulls.map(a=>Math.max(...a));
 results.push({halfWidthBins:k,halfWidthNm:k*0.3,segments:observed.map((o,j)=>({name:j?"red":"blue",lagBins:o.lag,lagNm:o.lag*0.3,r:o.r,p:(1+nulls.filter(v=>v[j]>=o.r).length)/250})),familyMax:max,p:(1+maxNull.filter(v=>v>=max).length)/250,nullMedian:median(maxNull)})
}
process.stdout.write(JSON.stringify({source,measurementCount:a.length,gap:{lastBlueNm:a[506][0]*1000,firstRedNm:a[507][0]*1000},nullMethod:"249 permutations of 16-bin contiguous blocks, separate segments; maximum across 8-120 lag bins and two arms",limitations:["single spectrum","block null not physical instrument model","three smoothing sizes explored without joint correction"],results},null,2)+"\n");
