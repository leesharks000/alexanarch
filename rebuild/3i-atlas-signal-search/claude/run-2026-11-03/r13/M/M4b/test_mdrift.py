import numpy as np, mdrift as M
rng = np.random.default_rng(1); n, N = 47, 1 << 16
R = rng.normal(0, 1, (n, N)).astype(np.float32)
cases = [(5000, 0.0), (12000, 20.0), (20000, -35.0), (30000, 150.0), (40000, -600.0), (50000, 900.0)]  # start bin, total drift in bins over NR-1 rows
for b0, dt in cases:
    for r in range(n):
        R[r, int(round(b0 + dt * r / (M.NR - 1))) % N] += 3.0 if len(__import__('sys').argv)>1 else 1.2
o = M.search(R)
for b0, dt in cases:
    for L in M.LEVELS:
        e = o[L]; c = b0 // L; w = slice(max(c - 2, 0), c + 3)
        i = np.argmax(e["maxz"][w].astype(float)) + w.start
        print(f"inj b0={b0} drift={dt:+} L={L}: z={float(e['maxz'][i]):.1f} at cell {i} (exp {c}) d={e['drift'][i]} (exp {dt / L:+.1f})")
print("noise max z per level:", {L: float(o[L]['maxz'].astype(float).max()) for L in M.LEVELS}, "n>=6:", {L: len(o[L]['idx']) for L in M.LEVELS})
