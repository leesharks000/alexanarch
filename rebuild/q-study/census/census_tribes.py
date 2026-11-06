#!/usr/bin/env python3
"""Run PLAN-tribes.md exactly."""
import unicodedata, re, json, pathlib, hashlib
P = pathlib.Path(__file__).parent; ROOT = P.parents[2]; C = ROOT / "data/corpora"
plan = hashlib.sha256((P / "PLAN-tribes.md").read_bytes()).hexdigest()
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(ch for ch in s if not unicodedata.combining(ch)).replace("ς", "σ")
    return re.sub(r"[^\w\s]|\d|_", " ", s).split()
K = lambda w: w.startswith(("κοψ", "κοπτ", "κεκοπ", "εκοψ"))
F = lambda w: w.startswith("φυλ") and not w.startswith(("φυλακ", "φυλασσ", "φυλαξ", "φυλαττ"))
N = lambda w: w.startswith("νεφελ")
def ok(ws): return any(map(K, ws)) and any(map(F, ws)) and any(map(N, ws))
hits = []
def run(label, path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    versed = sum(1 for l in lines[:200] if "\t" in l) > 50
    if versed:
        vs = [(l.split("\t", 1)[0], l.split("\t", 1)[1]) for l in lines if "\t" in l]
        last = -9
        for i in range(len(vs)):
            win = vs[i:i+3]; ws = norm(" ".join(t for _, t in win))
            if ok(ws) and i - last >= 3: hits.append({"corpus": label, "file": path.name, "ref": win[0][0] + "–" + win[-1][0], "text": " ".join(t for _, t in win)}); last = i
    else:
        toks = []; pos = []
        for n, l in enumerate(lines):
            for w in norm(l): toks.append(w); pos.append(n + 1)
        raw = None; last = -999
        for i in range(0, max(1, len(toks) - 59), 20):
            ws = toks[i:i+60]
            if ok(ws) and i - last >= 60:
                a, b = pos[i], pos[min(i + 59, len(pos) - 1)]
                hits.append({"corpus": label, "file": path.name, "ref": f"lines {a}–{b}", "text": " ".join(lines[a-1:b])[:900]}); last = i
for label, d in [("LXX", "lxx-swete/text"), ("NT", "gnt-nestle1904/text"), ("Josephus", "josephus/text"), ("Philo", "philo/text"), ("Pseudepigrapha", "second-temple-pseudepigrapha/text"), ("Justin", "justin-dialogus/text"), ("Irenaeus", "irenaeus-adversus-haereses/text"), ("Eusebius", "eusebius-historia-ecclesiastica/text")]:
    for f in sorted((C / d).glob("*")):
        if f.is_file(): run(label, f)
(P / "RESULTS-tribes.json").write_text(json.dumps({"plan_sha256": plan, "hits": hits}, ensure_ascii=False, indent=1), encoding="utf-8")
print(plan[:12], len(hits), "hits")
for h in hits: print("-", h["corpus"], h["file"], h["ref"], "|", h["text"][:400])
