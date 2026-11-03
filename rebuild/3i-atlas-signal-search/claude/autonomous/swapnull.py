"""Beam-swap asymmetry in the comet frame against false frames: for the true comet path and 40 false range-accelerations (0.03-1 Hz/s at
1.42 GHz, seed 11), count persistent clusters with ON as target (ON >= 2.5 x3, OFF < 2 x3) and with the beams swapped, and ON-singles against
OFF-singles (z >= 6 in exactly one scan, the other beam < 2 x3). Reuses autonomous.py's functions without its frame loop.
    python3 swapnull.py"""
import json, numpy as np
src = open("autonomous.py").read().split("rng = np.random.default_rng(7)")[0]
exec(compile(src, "autonomous.py", "exec"))
vf = FRAMES["comet (uncompensated)"]
rng = np.random.default_rng(11)
offs = [0.0] + list(rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * C / 1.42e9)
rows = []
for i, dv in enumerate(offs):
    A, _ = align({s: tracked(s, vf, dv) for s in ON + OFF})
    r = {"dv": float(dv), "on": clusters(persistent(A, ON, OFF)), "swap": clusters(persistent(A, OFF, ON)),
         "on_singles": clusters(singles(A, ON, OFF)), "off_singles": clusters(singles(A, OFF, ON))}
    rows.append(r); print(i, r, flush=True)
json.dump(rows, open("raw/OH_swapnull.json", "w"), indent=1)
