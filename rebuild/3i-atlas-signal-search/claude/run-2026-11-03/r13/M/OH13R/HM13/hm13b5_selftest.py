"""PLAN-HM13-B3B5 B5: the amended self-test for N1625's shape score.  python3 hm13b5_selftest.py [nproc] -> b5_selftest.json"""
import json, os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../../N1625"))
import numpy as np, n1625a as A
def trial(args):
    kind, amp, seed = args; rng = np.random.default_rng(seed); n = A.noise(rng); s = None
    if kind == "motif": m, s = A.motif(rng, amp); z = n + m
    elif kind == "tone": z = n + amp * np.exp(2j * np.pi * 0.1234 * np.arange(A.NS))
    else:
        b = rng.integers(0, A.BL, A.NS // A.BL); t = np.arange(A.BL)
        z = n + amp * np.concatenate([np.exp(2j * np.pi * (bb - A.BL // 2) * t / A.BL) for bb in b])
    r = A.test(z, 199, seed + 7); r.update(kind=kind, amp=amp, seed=seed, injected_shift=s); return r
if __name__ == "__main__":
    jobs = [("tone", 1.0, 9100 + k) for k in range(20)] + [("hop", 1.0, 9200 + k) for k in range(20)] + [("motif", 1.0, 1200 + k) for k in range(5)]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 1) as p: res = p.map(trial, jobs)
    c = {k: sum(r["p"] <= 0.05 for r in res if r["kind"] == k) for k in ("tone", "hop", "motif")}
    ok = c["tone"] <= 3 and c["hop"] <= 3 and c["motif"] >= 4
    json.dump({"plan": "PLAN-HM13-B3B5.md", "counts": c, "accepted": ok, "trials": res}, open(os.path.join(HERE, "b5_selftest.json"), "w"), indent=1)
    print(c, "ACCEPTED" if ok else "NOT ACCEPTED")
