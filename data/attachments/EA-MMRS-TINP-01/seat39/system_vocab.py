"""Analysis from the seat (2026-11-16): the vocabulary of 'system' beside the vocabulary of standing.
(1) In the construction texts (39/02–39/09, with Tennemann and Schleiermacher from 32/09 and 32/07, Jaeger from 31/10): 'system' and
'standing' terms per 100,000 tokens. (2) In AGPh by period: 'system' terms within 40 tokens of a Plato/Aristotle name, per 1,000
mentions, beside the standing terms. Running heads dropped (heads.py). OCR as served (Brucker's long s is read as f: fyftem is counted)."""
import re,json,pathlib,bisect,sys
sys.path.insert(0,str(pathlib.Path(__file__).parent)); from heads import body
C=pathlib.Path("/home/claude/alexanarch/data/corpora")
SYS=re.compile(r"(s[yi]st[eè]m|fyftem|syftem|fystem)")   # anywhere in the token: the OCR joins words ("politischesSystem")
STAND=re.compile(r"^(echtheit\w*|unecht\w*|athetes\w*|athetier\w*|abfassungszeit\w*|chronolog\w*|zeitfolge\w*|reihenfolge\w*|untergeschoben\w*|authenti\w*|spurious\w*|genuine\w*|apokryph\w*|apocryph\w*|unterschieb\w*|suppositi\w*|spuri\w*|genuin\w*|unächt\w*|ächtheit\w*|aechtheit\w*|unaecht\w*)$")
PA=re.compile(r"^(plat[oa]n?\w*|aristot\w*|aristoteles\w*|sokrat\w*|socrat\w*)$")
tok=re.compile(r"[A-Za-zÄÖÜäöüßſéèàâêîôûç]+")
def toks(p): return [w.lower().replace("ſ","s") for w in tok.findall(body(p.read_text(errors="replace")))]
print("construction texts: per 100,000 tokens")
for seat,f in [("brucker-historia-critica-1742","brucker-hcp-1742-i"),("brucker-historia-critica-iv-1743","brucker-hcp-4-1"),
               ("tennemann-platonische-philosophie","tennemann-system-1792-i.ocr"),("schleiermacher-platons-werke-1804",None),
               ("hermann-geschichte-system-1839","hermann-1839"),("ueberweg-echtheit-zeitfolge-1861","ueberweg-1861"),
               ("zeller-philosophie-griechen-1865","zeller-pdg-1865"),("grote-plato-1865","grote-plato-1865"),
               ("schaarschmidt-sammlung-1866","schaarschmidt-sammlung-1866.ocr"),("lutoslawski-plato-logic-1897",None),
               ("jaeger-aristoteles",None)]:
    d=C/seat/"text"; ps=[d/f"{f}.txt"] if f else sorted(d.glob("*.txt"))
    T=[w for p in ps for w in toks(p)]; n=len(T)
    s=sum(1 for w in T if SYS.search(w)); t=sum(1 for w in T if STAND.match(w))
    print(f"  {seat:40}{n:>9,} tokens  system {1e5*s/n:6.1f}  standing {1e5*t/n:6.1f}")
