"""Diagnostic after PLAN-P3W-C's failed validation (not frozen, synthetic only): does the circular shift's seam bias the null under steady tones?
Compares, on the five_mixed control, the circular shift (as frozen) with a shift without wraparound (each bin's sequence read from its own offset, no seam)."""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p3w as P, p3wc as C
rng = np.random.default_rng(4242); out = {}
t = np.arange(P.NS)
for name, fr in (("five_mixed", list(zip((60, 140, 230, 330, 420), (0.11, 0.37, 0.52, 0.68, 0.90)))), ("five_same", [(b, 0.37) for b in (60, 140, 230, 330, 420)])):
  for rep in range(3):
    zx = P.noise(rng) + C.steady_tones(rng, fr, 0.3); zy = P.noise(rng)
    PX, px = P.phasors(zx); PY, py = P.phasors(zy); M = P.masks(px, py); S = len(PX); LM = 512; Sp = S - LM
    r = {}
    for mode in ("circular", "no_wrap"):
        if mode == "circular":
            R = P.stats(PX, PY); sur = [P.stats(C.shift(PX, rng), C.shift(PY, rng)) for _ in range(P.NSUR)]
        else:
            R = P.stats(PX[:Sp], PY[:Sp]); sur = []
            for _ in range(P.NSUR):
                Lx = rng.integers(0, LM + 1, PX.shape[1]); Ly = rng.integers(0, LM + 1, PY.shape[1]); ii = np.arange(Sp)[:, None]
                sur.append(P.stats(PX[ii + Lx[None, :], np.arange(PX.shape[1])], PY[ii + Ly[None, :], np.arange(PY.shape[1])]))
        r[mode] = {f: (1 + sum(float(q[f][M[f]].max()) >= float(R[f][M[f]].max()) for q in sur)) / (P.NSUR + 1) for f in ("X+", "X-", "Y+", "Y-")}
    out[f"{name}-{rep}"] = r; print(name, rep, r, flush=True)
json.dump(out, open(os.path.join(HERE, "diagC.json"), "w"), indent=1)
