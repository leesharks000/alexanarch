"""Post-freeze diagnostic (not part of PLAN-P1547B's gates): what carries the lag-2 phase memory in ON0015.
Per scan and feed: per-frame lag-2 memory (real), the strongest lines of the normalized slice, and the lag-2 memory with
the 10 strongest lines (±8 bins) set to unit magnitude and random phase.  python3 p1547b_diag.py SCAN ..."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p1547 as P, p1547b as Q
def lag2(z):
    d = z[1:] * np.conj(z[:-1]); d /= np.maximum(np.abs(d), 1e-30); return np.abs(np.mean(d[2:] * np.conj(d[:-2])))
out = {}
for s in sys.argv[1:]:
    X, Y = [], []
    for j, x, y in P.dm.frames(s, P.NFR):
        X.append(P.dm.fft(x)[P.SL].astype(np.complex128)); Y.append(P.dm.fft(y)[P.SL].astype(np.complex128))
    for q, sl in zip("XY", (X, Y)):
        G = [Q.norm(F) for F in sl]; pw = np.mean([np.abs(g) ** 2 for g in G], 0)
        top = np.argsort(pw)[::-1][:10]; rng = np.random.default_rng(5)
        f = lambda b: (P.FC - (b + P.B - P.W // 2 - P.N // 2 + 0.5) * P.DF) / 1e6
        per = [lag2(Q.series(g)) for g in G]
        cut = []
        for g in G:
            h = g.copy()
            for b in top:
                sl_ = slice(max(b - 8, 0), b + 9); h[sl_] = np.exp(2j * np.pi * rng.random(h[sl_].shape))
            cut.append(lag2(Q.series(h)))
        sur = [lag2(Q.series(np.abs(g) * np.exp(2j * np.pi * rng.random(P.W)))) for g in G]
        out[f"{s}{q}"] = dict(per_frame=per, lines_cut=cut, surrogate=sur, top=[(round(f(int(b)), 6), round(float(pw[b]), 1)) for b in top])
        print(s, q, "lag2 x1e4 real median", round(1e4 * np.median(per), 2), "| lines cut", round(1e4 * np.median(cut), 2), "| one surrogate", round(1e4 * np.median(sur), 2),
              "| strongest lines (MHz, power/local noise):", out[f"{s}{q}"]["top"][:4], flush=True)
json.dump(out, open(os.path.join(HERE, "diagB.json"), "w"))
