#!/usr/bin/env python3
"""Put EA-CORPORA-42 (#1799) on the TLL shelf: the cards for 42/01–42/10 (build_originals_shelf.py),
the spines after 41/14 and the index entries after the last, the count set to the seats on the shelf (the form of tll41.py).
    python3 rebuild/corpora/ea-corpora-42/tll42.py /path/to/traininglayerliterature-org"""
import pathlib, re, subprocess, sys, html
ROOT = pathlib.Path(__file__).resolve().parents[3]; TLL = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "scripts")); import build_originals_shelf as B
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from names42 import SEATS as SP
for n, (name, _, _) in enumerate(SP, 1):
    subprocess.run([sys.executable, str(ROOT / "scripts/build_originals_shelf.py"), "--tll", str(TLL), "--corpus", name, "--card-no", f"EA-CORPORA-42/{n:02d}"], check=True)
p = TLL / "originals/index.html"; s = p.read_text()
assert 'href="#c-plutarch-platonic-questions-de-facie-numa"' not in s, "42 already on the index"
last = list(re.finditer(r'<a class="sp" href="#c-[^"]+"><span class="ser">41/14</span>[^<]*</a>', s))[-1]
spines = "".join(f'<a class="sp" href="#c-{name}"><span class="ser">42/{n:02d}</span>{html.escape(lab)}</a>' for n, (name, lab, _) in enumerate(SP, 1))
s = s[:last.end()] + spines + s[last.end():]
cards = "\n".join(B.ocard(name, ROOT / "data/corpora" / name, title) for name, _, title in SP)
i = s.rfind("</div></div>", 0, s.rfind("</html>")) + len("</div></div>")
s = s[:i] + "\n" + cards + s[i:]
shelf = sum(1 for d in (TLL / "originals").iterdir() if d.is_dir())
s = re.sub(r"\d+ corpora seated", f"{shelf} corpora seated", s, count=1)
p.write_text(s); print("index: 10 spines, 10 entries; count", shelf)
