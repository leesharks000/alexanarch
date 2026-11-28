#!/usr/bin/env python3
"""Put EA-CORPORA-44 on the TLL shelf: the cards for 43/01–43/04 (build_originals_shelf.py), the spines after 42/10 and
the index entries after the last, the count set to the seats on the shelf (the form of tll42.py).
    python3 rebuild/corpora/ea-corpora-44/tll43.py /path/to/traininglayerliterature-org [seats-dir]
seats-dir defaults to data/corpora; a staging folder renders a preview before seating (no AXNs yet)."""
import pathlib, re, sys, html
ROOT = pathlib.Path(__file__).resolve().parents[3]; TLL = pathlib.Path(sys.argv[1])
SEATDIR = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data/corpora"
sys.path.insert(0, str(ROOT / "scripts")); import build_originals_shelf as B
B.SEATS = SEATDIR
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from names44 import SEATS as SP
for n, (name, _, _) in enumerate(SP, 1):
    sys.argv = ["build_originals_shelf.py", "--tll", str(TLL), "--corpus", name, "--card-no", f"EA-CORPORA-44/{n:02d}"]
    B.main()
p = TLL / "originals/index.html"; s = p.read_text()
assert f'href="#c-{SP[0][0]}"' not in s, "44 already on the index"
last = list(re.finditer(r'<a class="sp" href="#c-[^"]+"><span class="ser">43/04</span>[^<]*</a>', s))[-1]
spines = "".join(f'<a class="sp" href="#c-{name}"><span class="ser">44/{n:02d}</span>{html.escape(lab)}</a>' for n, (name, lab, _) in enumerate(SP, 1))
s = s[:last.end()] + spines + s[last.end():]
cards = "\n".join(B.ocard(name, SEATDIR / name, title) for name, _, title in SP)
i = s.rfind("</div></div>", 0, s.rfind("</html>")) + len("</div></div>")
s = s[:i] + "\n" + cards + s[i:]
shelf = sum(1 for d in (TLL / "originals").iterdir() if d.is_dir())
s = re.sub(r"\d+ corpora seated", f"{shelf} corpora seated", s, count=1)
p.write_text(s); print("index: spines and entries; count", shelf)
