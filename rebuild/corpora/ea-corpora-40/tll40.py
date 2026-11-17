#!/usr/bin/env python3
"""Put EA-CORPORA-40 (v1.0 #1776, v1.1 #1782) on the TLL shelf: the cards for 40/01–40/17 (build_originals_shelf.py),
the spines after 39/13 and the index entries after the last, the count set to the seats on the shelf.
    python3 rebuild/corpora/ea-corpora-40/tll40.py /path/to/traininglayerliterature-org"""
import json, pathlib, re, subprocess, sys, html
ROOT = pathlib.Path(__file__).resolve().parents[3]; TLL = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "scripts")); import build_originals_shelf as B
SP = [("classical-philology-1906-1922", "Classical Philology, the reviews", "Classical Philology I–XVII (1906–1922): the Book Reviews section"),
      ("wolf-prolegomena-1795", "Wolf, Prolegomena", "Wolf — Prolegomena ad Homerum I (1795)"),
      ("wolf-darstellung-altertumswissenschaft-1807", "Wolf, Darstellung", "Wolf — Darstellung der Alterthums-Wissenschaft (1807; ed. 1833)"),
      ("boeckh-encyklopaedie-1877", "Boeckh, Encyklopädie", "Boeckh — Encyklopädie und Methodologie der philologischen Wissenschaften (1877)"),
      ("usener-philologie-geschichtswissenschaft-1882", "Usener, Philologie", "Usener — Philologie und Geschichtswissenschaft (1882)"),
      ("lachmann-lucretius-1850", "Lachmann, Lucretius", "Lachmann — In T. Lucretii Cari De rerum natura libros commentarius (1850)"),
      ("madvig-adversaria-critica-1871-1873", "Madvig, Adversaria", "Madvig — Adversaria critica I–II (1871–1873)"),
      ("housman-manilius-ii-1912", "Housman, Manilius II", "Housman — Manilius, Astronomicon II (1912)"),
      ("nietzsche-philologica-1869-1910", "Nietzsche, philologica", "Nietzsche — the philological writings (1869, 1870; eds. 1896, 1910)"),
      ("rohde-afterphilologie-1872", "Rohde, Afterphilologie", "Rohde — Afterphilologie (1872)"),
      ("valla-donatio-schwahn-1928", "Valla, Donatio", "Valla — De falso credita et ementita Constantini donatione (ed. Schwahn, 1928)"),
      ("casaubon-exercitationes-1614", "Casaubon, Exercitationes", "Casaubon — De rebus sacris et ecclesiasticis exercitationes XVI (1614)"),
      ("bentley-phalaris-1699", "Bentley, Phalaris", "Bentley — A Dissertation upon the Epistles of Phalaris (1699)"),
      ("diels-doxographi-graeci-1879", "Diels, Doxographi", "Diels — Doxographi Graeci (1879)"),
      ("sandys-history-classical-scholarship-1903-1908", "Sandys, History", "Sandys — A History of Classical Scholarship I–III (1903–1908)"),
      ("philology-census-classical-philology", "The census of CP", "The census of Classical Philology, 1906–2026"),
      ("classical-philology-1906-1922-articles", "Classical Philology, the articles", "Classical Philology I–XVII (1906–1922): the articles and notes, with the codes")]
for n, (name, _, _) in enumerate(SP, 1):
    subprocess.run([sys.executable, str(ROOT / "scripts/build_originals_shelf.py"), "--tll", str(TLL), "--corpus", name, "--card-no", f"EA-CORPORA-40/{n:02d}"], check=True)
p = TLL / "originals/index.html"; s = p.read_text()
assert 'href="#c-classical-philology-1906-1922"' not in s, "40 already on the index"
last = list(re.finditer(r'<a class="sp" href="#c-[^"]+"><span class="ser">39/13</span>[^<]*</a>', s))[-1]
spines = "".join(f'<a class="sp" href="#c-{name}"><span class="ser">40/{n:02d}</span>{html.escape(lab)}</a>' for n, (name, lab, _) in enumerate(SP, 1))
s = s[:last.end()] + spines + s[last.end():]
cards = "\n".join(B.ocard(name, ROOT / "data/corpora" / name, title) for name, _, title in SP)
i = s.rfind("</div></div>", 0, s.rfind("</html>")) + len("</div></div>")
s = s[:i] + "\n" + cards + s[i:]
shelf = sum(1 for d in (TLL / "originals").iterdir() if d.is_dir())
s = re.sub(r"\d+ corpora seated", f"{shelf} corpora seated", s, count=1)
p.write_text(s); print("index: 17 spines, 17 entries; count", shelf)
