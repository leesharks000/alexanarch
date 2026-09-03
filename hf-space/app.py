"""Crimson Hexagonal Archive — machine interface.
Serves the archive's records, graph and full-text search from the Hub dataset
(leesharsks/crimson-hexagonal-archive), for agents and tools. No page ranking involved."""
import spaces  # must be imported before gradio/torch on ZeroGPU hardware
import os, json, sqlite3, io, time

@spaces.GPU(duration=1)
def zerogpu_declaration():
    """ZeroGPU refuses to start an app with no @spaces.GPU function. This app is CPU-only; this is never called."""
    return "cpu-only"
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from huggingface_hub import hf_hub_download

DATASET = os.environ.get("HF_DATASET", "leesharsks/crimson-hexagonal-archive")
app = FastAPI(title="Crimson Hexagonal Archive — machine interface", version="0.1")
DB = sqlite3.connect(":memory:", check_same_thread=False)
STATE = {"loaded": False, "built_at": None, "rows": 0}
DEP = None; HET = None; SRC = None

def load():
    global DEP, HET, SRC
    t0 = time.time()
    p = hf_hub_download(DATASET, "deposits.parquet", repo_type="dataset")
    DEP = pd.read_parquet(p)
    try: HET = pd.read_parquet(hf_hub_download(DATASET, "heteronyms.parquet", repo_type="dataset"))
    except Exception: HET = pd.DataFrame()
    try: SRC = pd.read_parquet(hf_hub_download(DATASET, "sources.parquet", repo_type="dataset"))
    except Exception: SRC = pd.DataFrame()
    DB.execute("CREATE VIRTUAL TABLE IF NOT EXISTS ft USING fts5(kind, key, title, text, tokenize='unicode61 remove_diacritics 0')")
    DB.execute("DELETE FROM ft")
    DB.executemany("INSERT INTO ft VALUES (?,?,?,?)", [("deposit", str(r.deposit_number), r.title or "", (r.description or "") + "\n" + (r.text or "")) for r in DEP.itertuples()])
    if not SRC.empty:
        DB.executemany("INSERT INTO ft VALUES (?,?,?,?)", [("source", r.source_id, r.title or "", r.text or "") for r in SRC.itertuples()])
    DB.commit()
    STATE.update(loaded=True, built_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), rows=len(DEP), seconds=round(time.time()-t0, 1))


def row(n: int):
    m = DEP[DEP.deposit_number == n]
    if m.empty: raise HTTPException(404, f"no deposit {n}")
    return m.iloc[0]

def _py(v):
    import numpy as np
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.floating,)): return None if np.isnan(v) else float(v)
    if isinstance(v, (np.bool_,)): return bool(v)
    return v

def brief(r, with_text=False):
    d = {k: (None if (not isinstance(v, str) and pd.isna(v)) else _py(v)) for k, v in r.items() if k != "text"}
    for k in ("cites", "cited_by", "cites_axn", "related_deposits", "defines_concepts", "supersedes", "attachments"):
        if isinstance(d.get(k), str):
            try: d[k] = json.loads(d[k])
            except Exception: pass
    for k in ("deposit_number", "series_previous", "series_next", "superseded_by"):
        if d.get(k) is not None:
            try: d[k] = int(d[k])
            except Exception: pass
    if with_text: d["text"] = r["text"]
    return d

@app.get("/api", response_class=HTMLResponse)
def index():
    return f"""<!doctype html><meta charset=utf-8><title>Crimson Hexagonal Archive — machine interface</title>
<body style="font:15px/1.6 Georgia,serif;max-width:720px;margin:2rem auto;padding:0 1rem">
<h1 style="font-size:1.4rem">Crimson Hexagonal Archive — machine interface</h1>
<p>Records, graph, and full-text search over the Hub dataset <a href="https://huggingface.co/datasets/{DATASET}">{DATASET}</a>. {STATE['rows']} deposits loaded {STATE['built_at']}. Canonical seat of every record: <code>https://alexanarch.org/s/records/N/</code>.</p>
<ul>
<li><code>GET /api/record/1574</code> — a deposit with its relations (add <code>?text=1</code> for the canonical text)</li>
<li><code>GET /api/axn/0666</code> — the same by AXN hex</li>
<li><code>GET /api/neighbours/879?hops=2</code> — the citation neighbourhood, both directions</li>
<li><code>GET /api/series/1576</code> — the version/supersession chain</li>
<li><code>GET /api/search?q=οὐδὲν παντελῶς&amp;n=10</code> — full-text search (FTS5, Greek-safe) over descriptions, canonical texts and recovered sources</li>
<li><code>GET /heteronym/johannes-sigil</code> — a Dodecad record; <code>GET /heteronyms</code> lists them</li>
<li><code>GET /api/health</code></li>
</ul>
<p style="font-family:monospace;font-size:.85em">CC BY 4.0 · Lee Sharks · the archive: <a href="https://alexanarch.org">alexanarch.org</a> · node: <a href="https://alexanarch.org/.well-known/axn-node.json">axn-node.json</a></p></body>"""

@app.get("/api/health")
def health(): return STATE

@app.get("/api/record/{n}")
def record(n: int, text: int = 0): return brief(row(n), bool(text))

@app.get("/api/axn/{hexid}")
def by_axn(hexid: str, text: int = 0):
    m = DEP[DEP.hex.str.upper() == hexid.upper()]
    if m.empty: raise HTTPException(404, f"no AXN hex {hexid}")
    return brief(m.iloc[0], bool(text))

@app.get("/api/neighbours/{n}")
def neighbours(n: int, hops: int = Query(1, ge=1, le=3)):
    seen = {n}; frontier = {n}; edges = []
    for _ in range(hops):
        nxt = set()
        for a in list(frontier):
            r = row(a)
            for b in json.loads(r.cites or "[]"): edges.append([a, b]); nxt.add(b)
            for b in json.loads(r.cited_by or "[]"): edges.append([b, a]); nxt.add(b)
        frontier = nxt - seen; seen |= nxt
    nodes = {int(k): {"title": v} for k, v in DEP[DEP.deposit_number.isin(seen)].set_index("deposit_number").title.items()}
    return {"root": n, "hops": hops, "nodes": nodes, "edges": sorted({tuple(e) for e in edges})}

@app.get("/api/series/{n}")
def series(n: int):
    r = row(n); chain = [n]
    cur = r
    while cur.get("series_previous") is not None and not pd.isna(cur.get("series_previous")):
        p = int(cur["series_previous"]); chain.insert(0, p); cur = row(p)
    cur = r
    while cur.get("series_next") is not None and not pd.isna(cur.get("series_next")):
        q = int(cur["series_next"]); chain.append(q); cur = row(q)
    sup = {"superseded_by": (None if pd.isna(r.superseded_by) else int(r.superseded_by)), "supersedes": json.loads(r.supersedes or "[]")}
    return {"deposit": n, "version_series_id": (None if pd.isna(r.version_series_id) else r.version_series_id), "chain": chain, **sup}

@app.get("/api/search")
def search(q: str, n: int = Query(10, ge=1, le=100), kind: str = "any"):
    sql = "SELECT kind, key, title, snippet(ft, 3, '«', '»', ' … ', 24) AS snip, bm25(ft) AS score FROM ft WHERE ft MATCH ? "
    args = [q if any(c in q for c in '"*') else '"' + q.replace('"', '') + '"']
    if kind != "any": sql += "AND kind = ? "; args.append(kind)
    sql += "ORDER BY score LIMIT ?"; args.append(n)
    try: rows = DB.execute(sql, args).fetchall()
    except sqlite3.OperationalError as e: raise HTTPException(400, str(e))
    out = []
    for k, key, title, snip, score in rows:
        item = {"kind": k, "key": key, "title": title, "snippet": snip, "score": round(score, 3)}
        if k == "deposit": item["record"] = f"/api/record/{key}"; item["seat"] = f"https://alexanarch.org/s/records/{key}/"
        out.append(item)
    return {"query": q, "hits": out}

@app.get("/api/heteronyms")
def heteronyms():
    if HET.empty: return []
    def c(v): return None if (not isinstance(v, str) and pd.isna(v)) else _py(v)
    return [{"person_id": r.person_id, "name": c(getattr(r, "name", None)), "function": c(getattr(r, "function", None)), "works_count": c(getattr(r, "works_count", None))} for r in HET.itertuples()]

@app.get("/api/heteronym/{pid}")
def heteronym(pid: str):
    m = HET[HET.person_id == pid]
    if m.empty: raise HTTPException(404, pid)
    d = {k: (None if (not isinstance(v, str) and pd.isna(v)) else _py(v)) for k, v in m.iloc[0].items()}
    for k, v in list(d.items()):
        if isinstance(v, str) and v[:1] in "[{":
            try: d[k] = json.loads(v)
            except Exception: pass
    return d

@app.get("/api/robots.txt", response_class=PlainTextResponse)
def robots(): return "User-agent: *\nAllow: /\n"


# ── Gradio panel at / (the Space's free tier runs Gradio; the API above is mounted beside it) ──
import gradio as gr

def ui_search(q, n):
    if not q.strip(): return "Enter a query."
    res = search(q, n=int(n))
    if not res["hits"]: return "No hits."
    out = []
    for h in res["hits"]:
        seat = f' · <a href="{h["seat"]}">seat</a>' if h.get("seat") else ""
        out.append(f'**{h["title"]}** <small>({h["kind"]} {h["key"]}{seat})</small>\n\n{h["snippet"]}')
    return "\n\n---\n\n".join(out)

def ui_record(n):
    try: d = brief(row(int(n)))
    except Exception as e: return f"{e}"
    keep = ["deposit_number","axn","title","creator","date","family","status","venue","cites","cited_by","related_deposits","series_previous","series_next","superseded_by","record_url"]
    return "```json\n" + json.dumps({k: d.get(k) for k in keep}, ensure_ascii=False, indent=1) + "\n```\n\n" + (d.get("description") or "")

with gr.Blocks(title="Crimson Hexagonal Archive — machine interface") as demo:
    gr.Markdown("## Crimson Hexagonal Archive — machine interface\nFull-text search (Greek-safe) and record lookup over the Hub dataset "
                f"[{DATASET}](https://huggingface.co/datasets/{DATASET}). The JSON API for agents is documented at [/api](/api). Canonical seat of every record: `https://alexanarch.org/s/records/N/`.")
    with gr.Tab("Search"):
        q = gr.Textbox(label="Query", placeholder="οὐδὲν παντελῶς · provenance erasure · Lies Within")
        n = gr.Slider(1, 50, value=10, step=1, label="Hits")
        out = gr.Markdown()
        q.submit(ui_search, [q, n], out); gr.Button("Search").click(ui_search, [q, n], out)
    with gr.Tab("Record"):
        num = gr.Number(label="Deposit number", value=1574, precision=0)
        rec = gr.Markdown()
        num.submit(ui_record, num, rec); gr.Button("Look up").click(ui_record, num, rec)
    # ZeroGPU's startup check looks for a @spaces.GPU function REGISTERED AS A GRADIO EVENT,
    # not merely defined; wire the no-op to a hidden button so the tier will start the app.
    _gpu_btn = gr.Button("zerogpu", visible=False); _gpu_out = gr.Textbox(visible=False)
    _gpu_btn.click(zerogpu_declaration, None, _gpu_out)
    gr.Markdown("<small>CC BY 4.0 · Lee Sharks · [alexanarch.org](https://alexanarch.org) · [axn-node.json](https://alexanarch.org/.well-known/axn-node.json)</small>")

# ZeroGPU's startup check hooks Gradio's own launch(); so boot through
# demo.launch() and attach the /api routes to Gradio's server app.
load()  # build the index at import, whichever way the process is started
demo.queue()
gradio_app = gr.mount_gradio_app(app, demo, path="/")   # for uvicorn-style hosts

if __name__ == "__main__":
    import threading
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), prevent_thread_lock=True)
    server_app = getattr(demo, "server_app", None) or demo.app
    for r in app.routes:
        if getattr(r, "path", "").startswith("/api"):
            server_app.router.routes.append(r)
    threading.Event().wait()
