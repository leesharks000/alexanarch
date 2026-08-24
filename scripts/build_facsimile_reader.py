#!/usr/bin/env python3
"""Build a facsimile reader for a PDF-only deposit.

  python3 scripts/build_facsimile_reader.py --deposit 1539

WHY THIS EXISTS. A deposit whose work IS a document — a handwritten paper, a scan,
a photographed manuscript — has no body text, and every surface downstream assumes
one. The record page showed metadata where the work should be, the PDF route
rendered the metadata rather than the document, and the only way to read the deposit
was to download a file.

The alternative that must NOT be taken: transcribing. A transcription of someone's
handwriting is an editorial act on their work, and it is not the archive's to make.
The facsimile is the primary source. It is shown as deposited — un-OCR'd,
untranscribed, unreflowed.

Renders each page to an image and writes a single-page reader with prev/next,
keyboard navigation and edge taps. Same pattern as the Pearl reader.
"""
import argparse, json, subprocess, shutil, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def build(deposit_number: int, dpi: int = 150, quality: int = 88) -> None:
    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
    entry = next(d for d in reg["deposits"] if d["deposit_number"] == deposit_number)
    atts = entry.get("attachments") or []
    pdfs = [a for a in atts if str(a.get("archive_path", "")).lower().endswith(".pdf")]
    if not pdfs:
        raise SystemExit(f"#{deposit_number}: no archive-held PDF attachment — take custody first")
    att = pdfs[0]
    src = ROOT / str(att["archive_path"]).lstrip("/")
    if not src.exists():
        raise SystemExit(f"missing: {src}")

    out = ROOT / "read" / str(deposit_number)
    pages = out / "pages"
    if pages.exists():
        shutil.rmtree(pages)
    pages.mkdir(parents=True, exist_ok=True)

    subprocess.run(["pdftoppm", "-jpeg", "-r", str(dpi), "-jpegopt", f"quality={quality}",
                    str(src), str(pages / "p")], check=True)
    # pdftoppm zero-pads to the page count; normalise to 3 digits
    for f in sorted(pages.glob("p-*.jpg")):
        n = int(f.stem.split("-")[1])
        f.rename(pages / f"p-{n:03d}.jpg")
    n_pages = len(list(pages.glob("*.jpg")))

    title = entry.get("title", "")
    creator = entry.get("creator", "")
    date = entry.get("date", "")
    axn = entry.get("axn", "")
    fname = att.get("filename", "")
    sha = att.get("sha256", "")
    size = att.get("size", 0)
    e = html.escape

    doc = f"""<!doctype html><html lang="{e(entry.get('language') or 'en')}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — {e(creator)}</title>
<meta name="description" content="{e(title)} by {e(creator)}, {e(date)}. Handwritten primary source, presented as deposited — un-OCR'd and untranscribed. {n_pages} pages.">
<link rel="canonical" href="https://www.alexanarch.org/read/{deposit_number}/">
<style>
:root{{--bg:#14120f;--fg:#e8e2d6;--dim:#8a8378;--line:#2e2a24}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 Georgia,serif}}
header{{padding:1.6rem 1.2rem .8rem;text-align:center;border-bottom:1px solid var(--line)}}
h1{{font-size:1.3rem;margin:0 0 .3rem;font-weight:normal;line-height:1.3}}
.sub{{color:var(--dim);font:12px/1.5 ui-monospace,monospace;letter-spacing:.04em}}
.sub a{{color:#b08d57}}
.stage{{position:relative;max-width:min(94vw,900px);margin:1.4rem auto 0}}
.leaf{{background:#0d0b09;border:1px solid var(--line)}}
.leaf img{{display:block;width:100%;height:auto}}
.tap{{position:absolute;top:0;bottom:0;width:30%;cursor:pointer}}
.tap.l{{left:0}} .tap.r{{right:0}}
.bar{{display:flex;gap:1rem;justify-content:center;align-items:center;padding:1rem;font:12px/1 ui-monospace,monospace}}
button{{background:none;border:1px solid var(--line);color:var(--fg);padding:.55rem .9rem;font:12px/1 ui-monospace,monospace;cursor:pointer;letter-spacing:.05em}}
button:hover{{border-color:#b08d57}}
button:disabled{{opacity:.3;cursor:default}}
.note{{max-width:44rem;margin:0 auto;padding:0 1.2rem 2rem;color:var(--dim);font-size:.9rem;text-align:center}}
.note b{{color:var(--fg);font-weight:normal}}
footer{{border-top:1px solid var(--line);padding:1.2rem;text-align:center;color:var(--dim);font:11px/1.7 ui-monospace,monospace}}
footer a{{color:#b08d57}}
</style></head><body>
<header>
<h1>{e(title)}</h1>
<div class="sub">{e(creator)} · {e(date)} · <a href="/s/records/{deposit_number}/">{e(axn)}</a></div>
</header>
<div class="stage">
  <div class="leaf"><img id="pg" src="/read/{deposit_number}/pages/p-001.jpg" alt="{e(title)}, page 1"></div>
  <div class="tap l" onclick="go(-1)" title="previous page"></div>
  <div class="tap r" onclick="go(1)" title="next page"></div>
</div>
<div class="bar">
  <button id="prev" onclick="go(-1)">&larr; PREV</button>
  <span id="ctr">1 / {n_pages}</span>
  <button id="next" onclick="go(1)">NEXT &rarr;</button>
</div>
<p class="note"><b>Presented as deposited — un-OCR'd, untranscribed, unreflowed.</b>
The document is the work. Tap the page edges or use the arrow keys.</p>
<footer>
<a href="/data/attachments/AXN-{entry['hex']}/{e(fname)}">{e(fname)}</a><br>
{n_pages} pages · {size:,} bytes · SHA-256 {e(sha[:16])}…<br>
held by the archive · <a href="/s/records/{deposit_number}/">record</a> · ∮ = 1
</footer>
<script>
const N={n_pages}; let p=1;
const pad=n=>String(n).padStart(3,'0');
function show(){{
  document.getElementById('pg').src=`/read/{deposit_number}/pages/p-${{pad(p)}}.jpg`;
  document.getElementById('ctr').textContent=`${{p}} / ${{N}}`;
  document.getElementById('prev').disabled=(p<=1);
  document.getElementById('next').disabled=(p>=N);
}}
function go(d){{ const n=p+d; if(n>=1&&n<=N){{p=n;show();}} }}
document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowLeft')go(-1);
  if(e.key==='ArrowRight'||e.key===' ')go(1);
}});
show();
</script>
</body></html>"""
    (out / "index.html").write_text(doc, encoding="utf-8")
    print(f"#{deposit_number}: reader built — {n_pages} pages at /read/{deposit_number}/")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposit", type=int, required=True)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--quality", type=int, default=88)
    build(ap.parse_args().deposit, ap.parse_args().dpi, ap.parse_args().quality)
