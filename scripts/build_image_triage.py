#!/usr/bin/env python3
"""build_image_triage.py — a clickable surface for classifying the blog's images.

The task is to separate machine-generated images and visual schemas from everything
else — photographs, scans, handwriting, screengrabs, analog artifacts. Only 77 of
1,970 images carry alt text, so this cannot be inferred from metadata: it has to be
seen. This builds the seeing surface.

DESIGN NOTES

Marking is inverted deliberately. The majority of the corpus is generated, so the
default state is "generated" and a click marks the exception. Marking 200 images is
an afternoon; marking 1,970 is not.

Three states, not two: unreviewed, generated, and NOT generated. An image nobody has
looked at must not be indistinguishable from one judged generated — the same
distinction the archive draws between an attested absence and a default.

Selections persist in localStorage and export as JSON. The export is the artifact;
localStorage is a convenience that can be lost.

    python3 scripts/build_image_triage.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
IDX = json.loads((ROOT / "data" / "blog-image-index.json").read_text())
ROWS = IDX["images"]

# Trim to what the surface needs; 1,970 rows of full metadata would bloat the file.
SLIM = [{
    "i": n,
    "s": r["src"],
    "f": r["full"],
    "a": r["alt"] or r["title_attr"],
    "p": r["post_url"],
    "t": r["post_title"],
    "d": r["post_date"],
    "o": r["ordinal"],
    "c": r["caption_hint"],
} for n, r in enumerate(ROWS)]

HTML = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blog Image Triage — %(count)d images</title>
<style>
:root{--bg:#0c0e12;--panel:#12141a;--fg:#d8d4cc;--dim:#8a8478;--accent:#c8a868;
--mark:#5aa882;--gen:#3a3f4a;--rule:rgba(168,144,96,.18);
--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
header{position:sticky;top:0;z-index:10;background:var(--panel);border-bottom:1px solid var(--rule);
padding:12px 18px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
h1{font-size:.82rem;font-family:var(--mono);text-transform:uppercase;letter-spacing:.13em;
color:var(--accent);font-weight:500;white-space:nowrap}
.stat{font-family:var(--mono);font-size:.76rem;color:var(--dim);white-space:nowrap}
.stat b{color:var(--fg)}
button,select,input{font:inherit;font-size:.8rem;background:var(--bg);color:var(--fg);
border:1px solid var(--rule);border-radius:5px;padding:5px 10px;cursor:pointer}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);color:#0c0e12;border-color:var(--accent);font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;padding:18px}
.card{background:var(--panel);border:2px solid transparent;border-radius:7px;overflow:hidden;
cursor:pointer;transition:border-color .12s;position:relative}
.card:hover{border-color:var(--dim)}
.card.gen{opacity:.42}
.card.notgen{border-color:var(--mark);opacity:1}
.card.notgen::after{content:'NOT GENERATED';position:absolute;top:6px;right:6px;
background:var(--mark);color:#08130d;font-family:var(--mono);font-size:.6rem;font-weight:700;
padding:2px 6px;border-radius:3px;letter-spacing:.06em}
.card.unseen{border-color:var(--accent);border-style:dashed}
.thumb{width:100%%;height:170px;object-fit:contain;background:#000;display:block}
.meta{padding:8px 10px}
.ttl{font-size:.78rem;line-height:1.35;max-height:2.7em;overflow:hidden;color:var(--fg)}
.sub{font-family:var(--mono);font-size:.64rem;color:var(--dim);margin-top:4px;
display:flex;justify-content:space-between;gap:6px}
.sub a{color:var(--dim);text-decoration:none;border-bottom:1px dotted var(--rule)}
.sub a:hover{color:var(--accent)}
.empty{padding:60px 18px;text-align:center;color:var(--dim)}
kbd{font-family:var(--mono);font-size:.7rem;background:var(--bg);border:1px solid var(--rule);
border-radius:3px;padding:1px 5px}
.help{padding:0 18px 12px;color:var(--dim);font-size:.8rem;max-width:74ch}
</style></head><body>

<header>
<h1>Image Triage</h1>
<span class="stat"><b id="nNot">0</b> not generated</span>
<span class="stat"><b id="nGen">0</b> generated</span>
<span class="stat"><b id="nUnseen">%(count)d</b> unreviewed</span>
<select id="filter">
  <option value="all">all images</option>
  <option value="unseen">unreviewed only</option>
  <option value="notgen">marked NOT generated</option>
  <option value="gen">marked generated</option>
</select>
<select id="year"><option value="">every year</option></select>
<input id="q" placeholder="search post title" style="min-width:170px">
<button id="markPage">mark all shown as generated</button>
<button class="primary" id="exp">export JSON</button>
<button id="imp">import</button>
<input type="file" id="file" accept="application/json" style="display:none">
</header>

<p class="help">Click an image to mark it <b>NOT generated</b> — a photograph, scan,
handwriting, screengrab, or any analog artifact. Click again to mark it
<b>generated</b>. A third click returns it to unreviewed. Dashed gold border means
nobody has looked at it yet; that is a different state from <i>generated</i> and is
kept distinct on purpose. Work persists in this browser, but <b>the export is the
record</b> — save it.</p>

<div class="grid" id="grid"></div>

<script>
const DATA = %(data)s;
const KEY = 'blog-image-triage-v1';
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e) { state = {}; }

const grid = document.getElementById('grid');
const elFilter = document.getElementById('filter');
const elYear = document.getElementById('year');
const elQ = document.getElementById('q');

const years = [...new Set(DATA.map(d => d.d.slice(0,4)))].sort();
years.forEach(y => { const o = document.createElement('option'); o.value = y; o.textContent = y; elYear.appendChild(o); });

function counts(){
  let n=0,g=0;
  for (const k in state){ if(state[k]==='notgen') n++; else if(state[k]==='gen') g++; }
  document.getElementById('nNot').textContent = n;
  document.getElementById('nGen').textContent = g;
  document.getElementById('nUnseen').textContent = DATA.length - n - g;
}

function save(){ try{ localStorage.setItem(KEY, JSON.stringify(state)); }catch(e){} counts(); }

function cls(i){ return state[i] || 'unseen'; }

function visible(){
  const f = elFilter.value, y = elYear.value, q = elQ.value.trim().toLowerCase();
  return DATA.filter(d => {
    if (y && !d.d.startsWith(y)) return false;
    if (q && !(d.t||'').toLowerCase().includes(q)) return false;
    const c = cls(d.i);
    if (f === 'unseen') return c === 'unseen';
    if (f === 'notgen') return c === 'notgen';
    if (f === 'gen')    return c === 'gen';
    return true;
  });
}

function render(){
  const rows = visible();
  if (!rows.length){ grid.innerHTML = '<p class="empty">No images match.</p>'; return; }
  grid.innerHTML = rows.map(d => {
    const c = cls(d.i);
    const alt = (d.a || '').replace(/"/g,'&quot;');
    const t = (d.t || '(untitled)').replace(/</g,'&lt;');
    return `<div class="card ${c}" data-i="${d.i}">
      <img class="thumb" loading="lazy" src="${d.s}" alt="${alt}">
      <div class="meta">
        <div class="ttl" title="${t.replace(/"/g,'&quot;')}">${t}</div>
        <div class="sub"><span>${d.d}${d.o>1?' · img '+d.o:''}</span>
        <a href="${d.p}" target="_blank" rel="noopener">post ↗</a></div>
      </div></div>`;
  }).join('');
}

grid.addEventListener('click', e => {
  if (e.target.closest('a')) return;
  const card = e.target.closest('.card');
  if (!card) return;
  const i = card.dataset.i;
  const cur = state[i] || 'unseen';
  state[i] = cur === 'unseen' ? 'notgen' : cur === 'notgen' ? 'gen' : undefined;
  if (state[i] === undefined) delete state[i];
  card.className = 'card ' + cls(i);
  save();
});

document.getElementById('markPage').addEventListener('click', () => {
  const rows = visible();
  if (!confirm(`Mark ${rows.length} shown image(s) as generated?`)) return;
  rows.forEach(d => { state[d.i] = 'gen'; });
  save(); render();
});

document.getElementById('exp').addEventListener('click', () => {
  const out = { exported: new Date().toISOString(), total: DATA.length,
    not_generated: [], generated: [] };
  DATA.forEach(d => {
    const c = state[d.i];
    if (c === 'notgen' || c === 'gen') {
      (c === 'notgen' ? out.not_generated : out.generated).push({
        src: d.s, full: d.f, post_url: d.p, post_title: d.t,
        post_date: d.d, ordinal: d.o, alt: d.a });
    }
  });
  out.unreviewed = DATA.length - out.not_generated.length - out.generated.length;
  const b = new Blob([JSON.stringify(out, null, 1)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(b);
  a.download = 'blog-image-classification.json';
  a.click();
});

document.getElementById('imp').addEventListener('click', () => document.getElementById('file').click());
document.getElementById('file').addEventListener('change', ev => {
  const f = ev.target.files[0]; if (!f) return;
  const r = new FileReader();
  r.onload = () => {
    try {
      const j = JSON.parse(r.result);
      const bySrc = {}; DATA.forEach(d => { bySrc[d.s + '|' + d.p] = d.i; });
      (j.not_generated||[]).forEach(x => { const i = bySrc[x.src+'|'+x.post_url]; if(i!==undefined) state[i]='notgen'; });
      (j.generated||[]).forEach(x => { const i = bySrc[x.src+'|'+x.post_url]; if(i!==undefined) state[i]='gen'; });
      save(); render();
    } catch(e){ alert('Could not read that file.'); }
  };
  r.readAsText(f);
});

[elFilter, elYear].forEach(el => el.addEventListener('change', render));
elQ.addEventListener('input', render);
counts(); render();
</script>
</body></html>
"""

out = HTML % {"count": len(SLIM), "data": json.dumps(SLIM, ensure_ascii=False, separators=(",", ":"))}
p = pathlib.Path("/mnt/user-data/outputs/blog-image-triage.html")
p.write_text(out, encoding="utf-8")
print(f"{p} · {len(out):,} bytes · {len(SLIM):,} images")
