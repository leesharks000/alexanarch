#!/usr/bin/env python3
"""build_image_triage.py — grouped, low-resolution, three-state image triage.

CORRECTED BY MANUS, 2026-08-09. Four changes, each of which was wrong before.

1 · THUMBNAILS. Blogger encodes size in the URL path, so /s320/ requests a 320px
    render from the same asset. The first build served originals — some of them
    multi-megabyte — 1,970 at a time, and the page never finished loading. Cards
    now request /s320/ and the click-through keeps the full-size URL.

2 · NO CLICKS MEANS GENERATED. The first build treated an unreviewed image as a
    distinct third state, which is right for an audit and wrong for this task: the
    corpus IS overwhelmingly generated, so the default is a classification rather
    than an absence of one.

3 · THREE STATES ON TWO CLICKS.
      0 — GENERATED. Machine-made; belongs in the schema registry.
      1 — EXCLUDED. Not generated and not wanted: art without rights, screen
          captures, junk. Kept out of the registry entirely.
      2 — OWNED. Not generated, and MANUS holds the rights.
    The distinction between 1 and 2 is not aesthetic. It is whether the archive
    may carry the thing.

4 · DUPLICATES COLLAPSE, POST RUNS SURVIVE. An image used across 105 posts is one
    card and one decision — but the export keeps every post it appeared in, with
    its date range, because the run of posts an image marked is itself a fact about
    the corpus.

    python3 scripts/build_image_triage.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
H = json.loads((ROOT / "data" / "blog-image-hashes.json").read_text())
IDX = json.loads((ROOT / "data" / "blog-image-index.json").read_text())

SIZE = re.compile(r"/(s\d+(?:-c)?|w\d+-h\d+(?:-[a-z-]+)?)/")


def thumb(u, px=320):
    if "blogger.googleusercontent" not in u and "bp.blogspot" not in u:
        return u
    if SIZE.search(u):
        return SIZE.sub(f"/s{px}/", u, count=1)
    return re.sub(r"(/[^/]+)$", rf"/s{px}\1", u, count=1)


groups = {}
for im in H["images"]:
    groups.setdefault(im["group"], []).append(im)

hashed = {im["src"] for im in H["images"]}
gid = (max(groups) + 1) if groups else 0
for r in IDX["images"]:
    if r["src"] not in hashed:
        groups[gid] = [{"src": r["src"], "post_url": r["post_url"],
                        "post_title": r["post_title"], "post_date": r["post_date"],
                        "ordinal": r["ordinal"], "alt": r["alt"], "group": gid}]
        gid += 1

CARDS = []
for g, members in groups.items():
    members = sorted(members, key=lambda m: (m["post_date"], m["ordinal"]))
    lead = members[0]
    dates = [m["post_date"] for m in members]
    CARDS.append({
        "g": g, "s": thumb(lead["src"]), "o": lead["src"], "n": len(members),
        "d0": dates[0], "d1": dates[-1], "t": lead["post_title"],
        "a": lead.get("alt", ""), "u": lead["post_url"],
        "posts": [{"u": m["post_url"], "t": m["post_title"], "d": m["post_date"],
                   "s": m["src"]} for m in members],
    })
CARDS.sort(key=lambda c: (-c["n"], c["d0"]))

HTML = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Image Triage &mdash; %(groups)d groups, %(images)d images</title>
<style>
:root{--bg:#0c0e12;--panel:#12141a;--fg:#d8d4cc;--dim:#8a8478;--accent:#c8a868;
--excl:#b84030;--own:#5aa882;--rule:rgba(168,144,96,.18);
--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
header{position:sticky;top:0;z-index:20;background:var(--panel);border-bottom:1px solid var(--rule);
padding:11px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
h1{font-size:.78rem;font-family:var(--mono);text-transform:uppercase;letter-spacing:.13em;
color:var(--accent);font-weight:500;white-space:nowrap}
.stat{font-family:var(--mono);font-size:.73rem;color:var(--dim);white-space:nowrap}
.stat b{color:var(--fg)}
.sw{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px}
button,select,input{font:inherit;font-size:.79rem;background:var(--bg);color:var(--fg);
border:1px solid var(--rule);border-radius:5px;padding:5px 9px;cursor:pointer}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);color:#0c0e12;border-color:var(--accent);font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(196px,1fr));gap:13px;padding:16px}
.card{background:var(--panel);border:2px solid transparent;border-radius:7px;overflow:hidden;
cursor:pointer;position:relative}
.card:hover{border-color:var(--dim)}
.card.gen{opacity:.5}
.card.excl{border-color:var(--excl);opacity:1}
.card.own{border-color:var(--own);opacity:1}
.tag{position:absolute;top:6px;left:6px;font-family:var(--mono);font-size:.58rem;font-weight:700;
padding:2px 6px;border-radius:3px;letter-spacing:.05em;display:none}
.card.excl .tag.e{display:block;background:var(--excl);color:#fff}
.card.own .tag.o{display:block;background:var(--own);color:#08130d}
.count{position:absolute;top:6px;right:6px;font-family:var(--mono);font-size:.6rem;
background:rgba(0,0,0,.72);color:var(--accent);padding:2px 6px;border-radius:3px}
.thumb{width:100%%;height:160px;object-fit:contain;background:#000;display:block}
.meta{padding:7px 9px}
.ttl{font-size:.75rem;line-height:1.32;max-height:2.7em;overflow:hidden}
.sub{font-family:var(--mono);font-size:.62rem;color:var(--dim);margin-top:4px;
display:flex;justify-content:space-between;gap:6px}
.sub a{color:var(--dim);text-decoration:none}
.sub a:hover{color:var(--accent)}
.help{padding:0 16px 12px;color:var(--dim);font-size:.81rem;max-width:80ch;line-height:1.65}
.help b{color:var(--fg)}
.empty{padding:60px;text-align:center;color:var(--dim)}
</style></head><body>

<header>
<h1>Image Triage</h1>
<span class="stat"><span class="sw" style="background:#3a3f4a"></span><b id="nGen">0</b> generated</span>
<span class="stat"><span class="sw" style="background:var(--excl)"></span><b id="nEx">0</b> excluded</span>
<span class="stat"><span class="sw" style="background:var(--own)"></span><b id="nOwn">0</b> owned</span>
<select id="filter">
  <option value="all">all groups</option>
  <option value="gen">generated (default)</option>
  <option value="excl">excluded</option>
  <option value="own">owned</option>
  <option value="multi">repeated images only</option>
</select>
<select id="year"><option value="">every year</option></select>
<input id="q" placeholder="search post title" style="min-width:160px">
<button class="primary" id="exp">export JSON</button>
<button id="imp">import</button>
<input type="file" id="file" accept="application/json" style="display:none">
</header>

<p class="help">Every image is <b>generated</b> until you say otherwise &mdash; that is
the default and it is a classification, not a gap. <b>One click</b> marks a group
<b>excluded</b>: not generated and not wanted in the schema registry &mdash; art you do
not hold the rights to, screen captures, junk. <b>Two clicks</b> marks it <b>owned</b>:
not generated, and yours. A third click returns it to generated. Repeated images are
<b>one card and one decision</b>; the badge shows how many posts carry it, and the
export keeps every one of them with its date range.</p>

<div class="grid" id="grid"></div>

<script>
const DATA = %(data)s;
const KEY = 'blog-image-triage-v2';
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e) {}

const grid = document.getElementById('grid');
const elF = document.getElementById('filter'), elY = document.getElementById('year'),
      elQ = document.getElementById('q');
const years = [...new Set(DATA.flatMap(c => c.posts.map(p => p.d.slice(0,4))))].sort();
years.forEach(y => { const o=document.createElement('option'); o.value=y; o.textContent=y; elY.appendChild(o); });

function cls(g){ return state[g] || 'gen'; }
function counts(){
  let e=0,o=0,ge=0;
  DATA.forEach(c => { const k=cls(c.g);
    if(k==='excl') e+=c.n; else if(k==='own') o+=c.n; else ge+=c.n; });
  document.getElementById('nEx').textContent=e;
  document.getElementById('nOwn').textContent=o;
  document.getElementById('nGen').textContent=ge;
}
function save(){ try{ localStorage.setItem(KEY, JSON.stringify(state)); }catch(e){} counts(); }

function visible(){
  const f=elF.value, y=elY.value, q=elQ.value.trim().toLowerCase();
  return DATA.filter(c => {
    if (y && !c.posts.some(p=>p.d.startsWith(y))) return false;
    if (q && !c.posts.some(p=>(p.t||'').toLowerCase().includes(q))) return false;
    if (f==='multi') return c.n>1;
    if (f!=='all') return cls(c.g)===f;
    return true;
  });
}

function render(){
  const rows=visible();
  if(!rows.length){ grid.innerHTML='<p class="empty">Nothing matches.</p>'; return; }
  grid.innerHTML = rows.map(c => {
    const t=(c.t||'(untitled)').replace(/</g,'&lt;').replace(/"/g,'&quot;');
    const span = c.d0===c.d1 ? c.d0 : c.d0+' \\u2192 '+c.d1;
    return `<div class="card ${cls(c.g)}" data-g="${c.g}">
      <span class="tag e">EXCLUDED</span><span class="tag o">OWNED</span>
      ${c.n>1?`<span class="count">${c.n} posts</span>`:''}
      <img class="thumb" loading="lazy" decoding="async" src="${c.s}" alt="${(c.a||'').replace(/"/g,'&quot;')}">
      <div class="meta"><div class="ttl" title="${t}">${t}</div>
      <div class="sub"><span>${span}</span><a href="${c.u}" target="_blank" rel="noopener">post \\u2197</a></div>
      </div></div>`;
  }).join('');
}

grid.addEventListener('click', e => {
  if (e.target.closest('a')) return;
  const card=e.target.closest('.card'); if(!card) return;
  const g=card.dataset.g, cur=state[g]||'gen';
  state[g] = cur==='gen' ? 'excl' : cur==='excl' ? 'own' : undefined;
  if(state[g]===undefined) delete state[g];
  card.className='card '+cls(g);
  save();
});

document.getElementById('exp').addEventListener('click', () => {
  const out={ exported:new Date().toISOString(), groups:DATA.length,
    images:DATA.reduce((a,c)=>a+c.n,0), generated:[], excluded:[], owned:[] };
  DATA.forEach(c => {
    const rec={ image:c.o, thumb:c.s, alt:c.a, post_count:c.n,
      first_post:c.d0, last_post:c.d1,
      posts:c.posts.map(p=>({url:p.u,title:p.t,date:p.d,src:p.s})) };
    const k=cls(c.g);
    (k==='excl'?out.excluded:k==='own'?out.owned:out.generated).push(rec);
  });
  const b=new Blob([JSON.stringify(out,null,1)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(b); a.download='blog-image-classification.json'; a.click();
});

document.getElementById('imp').addEventListener('click',()=>document.getElementById('file').click());
document.getElementById('file').addEventListener('change', ev => {
  const f=ev.target.files[0]; if(!f) return;
  const r=new FileReader();
  r.onload=()=>{ try{
    const j=JSON.parse(r.result), by={};
    DATA.forEach(c=>{ by[c.o]=c.g; });
    (j.excluded||[]).forEach(x=>{ const g=by[x.image]; if(g!==undefined) state[g]='excl'; });
    (j.owned||[]).forEach(x=>{ const g=by[x.image]; if(g!==undefined) state[g]='own'; });
    save(); render();
  }catch(e){ alert('Could not read that file.'); } };
  r.readAsText(f);
});

[elF, elY].forEach(el=>el.addEventListener('change', render));
elQ.addEventListener('input', render);
counts(); render();
</script>
</body></html>
"""

out = HTML % {
    "groups": len(CARDS),
    "images": sum(c["n"] for c in CARDS),
    "data": json.dumps(CARDS, ensure_ascii=False, separators=(",", ":")),
}
(ROOT / "triage").mkdir(exist_ok=True)
(ROOT / "triage" / "index.html").write_text(out, encoding="utf-8")
pathlib.Path("/mnt/user-data/outputs/blog-image-triage.html").write_text(out, encoding="utf-8")
print(f"{len(CARDS):,} cards covering {sum(c['n'] for c in CARDS):,} images "
      f"· {len(out):,} bytes")
print(f"repeated-image groups: {sum(1 for c in CARDS if c['n'] > 1)}")
