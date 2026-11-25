"""Context for key_gate at the 1 s unit, where the key's G2 stood above the random keys in the three ON scans. Written after that
was seen; post hoc. Two questions. (1) Is it the order of the six values or only their sizes? Controls here are 60 orderings of
the same six values (not rotations of the key, which the phase search already covers). (2) Where are the channels,
and are they ON only? Per pair, the channels with G2 >= 45 in the ON scan and < 30 in the OFF scan after it, for the key and for
each ordering.    python3 key_gate_perm.py"""
import json, os, sys, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = sys.argv[:1] + ["0"]
exec(open(os.path.join(HERE, "key_gate.py")).read().split("out = {")[0])
def canon(p):
    rots = [tuple(p[i:] + p[:i]) for i in range(6)]; return min(rots)
seen = {canon(list(KEY))}; perms = []
prng = np.random.default_rng(100)
while len(perms) < 60:
    p = prng.permutation(KEY).tolist()
    if canon(p) not in seen: seen.add(canon(p)); perms.append(p)
out = {"key": KEY, "orderings": perms, "scans": {}, "pairs": {}}; G = {}
for sc in r.SCANS:
    name, x, fch1, foff, ts = r.read("blc24", sc)
    x = x / np.median(x, 1, keepdims=True); med = np.median(x, 0); mad = 1.4826 * np.median(np.abs(x - med), 0); mad[mad == 0] = np.inf
    Z = np.clip(((x - med) / mad).astype(np.float32), -8, 8); Z -= Z.mean(0); Z /= Z.std(0) + 1e-9; del x
    t = (np.arange(Z.shape[0]) + 0.5) * ts; freqs = fch1 + foff * np.arange(Z.shape[1])
    G[sc] = [scores(Z, k, 1.0, t, ts) for k in [KEY] + perms]
    q = lambda a: float(np.quantile(a, 0.9999))
    k1, k2 = G[sc][0]; c1 = np.array([q(a) for a, b in G[sc][1:]]); c2 = np.array([q(b) for a, b in G[sc][1:]]); n2 = np.array([(b >= 45).sum() for a, b in G[sc][1:]])
    out["scans"][sc] = {"role": ROLE[sc], "G1_p9999": q(k1), "G1_rank": float((c1 < q(k1)).mean()), "G2_p9999": q(k2), "G2_rank": float((c2 < q(k2)).mean()),
                        "G2_n_ge45": int((k2 >= 45).sum()), "G2_n_rank": float((n2 < (k2 >= 45).sum()).mean()), "ctrl_G2_p9999": [float(c2.min()), float(np.median(c2)), float(c2.max())]}
    print(sc, json.dumps(out["scans"][sc]), flush=True)
    if ROLE[sc] == "OFF":
        on = "%04d" % (int(sc) - 1); cnt = []
        for (a_on, b_on), (a_off, b_off) in zip(G[on], G[sc]): cnt.append(np.flatnonzero((b_on >= 45) & (b_off < 30)))
        idx = cnt[0]; cn = np.array([len(c) for c in cnt[1:]])
        out["pairs"][on + "/" + sc] = {"on_only_key": int(len(idx)), "on_only_orderings_median": float(np.median(cn)), "rank": float((cn < len(idx)).mean()),
                                       "freqs_MHz": [round(float(freqs[i]), 4) for i in idx], "G2_on": [round(float(G[on][0][1][i]), 1) for i in idx]}
        print(on, sc, "ON-only channels, key %d, orderings median %.0f, rank %.2f" % (len(idx), np.median(cn), out["pairs"][on + "/" + sc]["rank"]), flush=True)
        del G[on], G[sc]
    json.dump(out, open(os.path.join(HERE, "key_gate_perm.json"), "w"), indent=1)
