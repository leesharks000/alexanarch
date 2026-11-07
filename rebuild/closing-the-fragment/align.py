#!/usr/bin/env python3
"""Closing the Fragment v7, §5.3: the line alignment of the January 2026 output, reproduced from the archive's own records and seats.
For each of the fifteen output lines (as transcribed in #337, §1.1) the longest run of consecutive words it shares with each witness of the
reference set: Wharton's literal version (EA-CORPORA-36/14), the January Cranes text (as quoted in #337, §1.2), Carman 1904 (36/13),
O'Hara 1910 and Stacpoole 1920 (36/15). A longest run records a correspondence; the route from witness to output is an inference (§5.3).
    python3 rebuild/closing-the-fragment/align.py"""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]; C = ROOT / "data/corpora"
D = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t337 = (ROOT / D[337]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
i = t337.index("That man seems to me a god"); j = t337.index("But I must dare all.", i) + len("But I must dare all.")
OUT = [l for l in t337[i:j].splitlines() if l.strip()]
k = t337.index("He is an equal to the gods, that man"); m = t337.index("since even a poor man…", k) + len("since even a poor man…")
W = {"Wharton": None, "Cranes, January": t337[k:m]}
wh = (C / "wharton-sappho-1908/text/wharton-1908.txt").read_text(encoding="utf-8"); a = wh.index("That man seems to me peer of gods")
W["Wharton"] = wh[a:wh.index("so poor_ ...", a) + 12]
oh = (C / "renderings-1910-1920/text/ohara-1910.txt").read_text(encoding="utf-8"); a = oh.index("Peer of Gods to me is the man"); W["O'Hara 1910"] = oh[a:oh.index("Image of Kypris", a) + 15]
st = (C / "renderings-1910-1920/text/stacpoole-1920.txt").read_text(encoding="utf-8"); a = st.index("That man, whoever he may be,"); W["Stacpoole 1920"] = st[a:st.index("(To thee I come)", a) + 16]
ca = (C / "carman-sappho-1904/text/carman-1907.txt").read_text(encoding="utf-8"); a = ca.index("Peer of the gods he seems,\nWho in thy presence"); W["Carman 1904"] = ca[a:ca.index("And the sea’s secret.", a) + 21]
tok = lambda s: re.findall(r"[a-z']+", s.lower().replace("’", "'"))
def run(x, y):
    x, y, best = tok(x), tok(y), 0
    for p in range(len(x)):
        for q in range(len(y)):
            n = 0
            while p + n < len(x) and q + n < len(y) and x[p + n] == y[q + n]: n += 1
            best = max(best, n)
    return best
assert len(OUT) == 15
print("| output line | " + " | ".join(W) + " |"); print("|---" * (len(W) + 1) + "|")
for l in OUT:
    print(f"| {l} | " + " | ".join(str(run(l, v)) for v in W.values()) + " |")
