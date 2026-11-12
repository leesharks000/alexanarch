"""Assert every double-quoted Greek string in The Josephus Thesis against the seated corpora (Josephus #1499, Nestle 1904, Swete,
Strabo, Diogenes Laertius, Aristotle, Philo). Ellipses split a quotation into parts, each asserted. Prints misses.   python3 quotecheck_jt.py <paper.md>"""
import re, sys, glob, pathlib, unicodedata
ROOT = pathlib.Path(__file__).resolve().parents[2]
def norm(s):
    s = unicodedata.normalize("NFC", s).replace("’", "ʼ").replace("'", "ʼ").replace("ʹ","ʼ")
    s = re.sub(r"[·.,;:!?\"“”«»()\[\]]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()
files = []
for pat in ["data/corpora/josephus/text/*.txt", "data/corpora/gnt-nestle1904/text/*.txt", "data/corpora/lxx-swete/text/*.txt", "data/corpora/strabo/**/*",
            "data/corpora/diogenes-laertius/**/*", "data/corpora/aristotle/**/*", "data/corpora/philo/**/*"]:
    files += [f for f in glob.glob(str(ROOT / pat), recursive=True) if pathlib.Path(f).is_file()]
blob = []
for f in files:
    try: t = open(f, encoding="utf-8").read()
    except Exception: continue
    t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"\b(BJ|AJ|CA|Vita) [\d?]+\.\d+\b", " ", t); t = re.sub(r"^\S+ \d+:\d+\t", " ", t, flags=re.M)
    blob.append(norm(t))
B = " ".join(blob)
paper = open(sys.argv[1], encoding="utf-8").read()
qs = re.findall(r"\"([Ͱ-Ͽἀ-῿][^\"\n]{0,400})\"", paper)  # a quotation opens on Greek; spans between two English quotes are not quotations
ok = miss = 0
for q in qs:
    parts = [p for p in re.split(r"…|\.\.\.", q) if re.search(r"[Ͱ-Ͽἀ-῿]", p)]
    for p in parts:
        n = norm(p)
        if n in B: ok += 1
        else: miss += 1; print("MISS:", p[:120])
print(ok, "ok,", miss, "miss")
