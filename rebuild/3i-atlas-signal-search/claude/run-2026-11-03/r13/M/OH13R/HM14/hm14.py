"""PLAN-HM14: the Parkes pattern (HM7) against 380 false drifts.  python3 hm14.py"""
import os, sys, json, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); H7 = os.path.join(HERE, "..", "HM7")
spec = importlib.util.spec_from_file_location("hm7", os.path.join(H7, "hm7.py")); hm7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(hm7)
W = hm7.windows(); names = [w[0] for w in W]; HALF = hm7.HALF; EXC = hm7.EXC
SC = json.load(open(os.path.join(H7, "hm7_score.json")))
rng = np.random.default_rng(20261123); DD = np.concatenate([[0.0], rng.uniform(0.02, 0.20, 380) * rng.choice([-1, 1], 380)])

def z(A, co, R):
    Rw = A / np.median(A, axis=1, keepdims=True); s = Rw.sum(0); S = s[:-2] + s[1:-1] + s[2:]
    c = len(S) // 2; j = np.arange(len(S)) - c
    ok = (np.abs(j) >= EXC) & (np.abs(j) <= R)
    for o in co: ok &= np.abs(j - o) > EXC
    ref = S[ok]; m = np.median(ref); mad = 1.4826 * np.median(np.abs(ref - m)); return (S[c] - m) / mad

out = {"dd": DD.tolist(), "sessions": {}}
gate_ok = True
for sname, S in hm7.SESSIONS.items():
    stems = [x for p in S["pairs"] for x in p]
    F = {st: {k: v for k, v in np.load(os.path.join(H7, f"hm7_{sname}_{st.split('_')[2]}.npz")).items()} for st in stems}   # amendment 1: arrays read once, not re-decompressed per access
    tmid = {st: float(F[st]["t0"]) + (np.arange(F[st]["A"].shape[1]) + 0.5) * float(F[st]["ts"]) / 86400.0 for st in stems}
    tref = np.mean([tmid[st].mean() for st in stems]); foff = abs(float(F[stems[0]]["foff"])) * 1e6
    cand = [i for i, w in enumerate(W) if w[1] == "cand" and not SC["sessions"][sname]["candidates"][w[0]]["flags"]]
    co = {}
    for st in stems:
        IC = F[st]["IC"]; co[st] = [[float(np.median(IC[u] - IC[w])) for u in range(len(W)) if u != w and abs(np.median(IC[u] - IC[w])) <= HALF] for w in range(len(W))]
    # gate: comet, HM7's own range
    Dg = {}
    for i in cand:
        zs = [z(F[st]["A"][i], co[st][i], HALF - 1) for st in stems]
        Dg[names[i]] = np.mean(zs[0::2]) - np.mean(zs[1::2])
    diffs = {n: round(abs(Dg[n] - SC["sessions"][sname]["candidates"][n]["D"]), 4) for n in Dg}
    ok = all(v <= 1e-3 for v in diffs.values()); gate_ok &= ok
    out["sessions"][sname] = {"gate": {"ok": ok, "absdiff": diffs}}
    if not ok: continue
    R2 = 999; fam = []; c09 = []; HW = 1000
    for d in DD:
        Ds = []
        for i in cand:
            zs = []
            for st in stems:
                A = F[st]["A"][i]; sh = np.rint(d * (tmid[st] - tref) * 86400.0 / foff).astype(int)
                Ap = np.stack([A[k, HALF + sh[k] - HW: HALF + sh[k] + HW + 1] for k in range(A.shape[0])])
                zs.append(z(Ap, [o for o in co[st][i] if abs(o) <= HW], R2))
            Ds.append(np.mean(zs[0::2]) - np.mean(zs[1::2]))
        fam.append(float(np.mean(Ds))); c09.append(float(Ds[[names[i] for i in cand].index("C09")]) if "C09" in [names[i] for i in cand] else None)
    fam = np.array(fam); c = np.array(c09, dtype=float)
    out["sessions"][sname].update({"family": fam.tolist(), "C09": c.tolist(),
        "family_rank": int(1 + (fam[1:] >= fam[0]).sum()), "C09_rank": int(1 + (c[1:] >= c[0]).sum()),
        "family_false_mean": float(fam[1:].mean()), "family_false_sd": float(fam[1:].std()), "n_cand": len(cand)})
    print(sname, "gate", ok, "family", round(fam[0], 3), "rank", out["sessions"][sname]["family_rank"], "C09 rank", out["sessions"][sname]["C09_rank"], flush=True)
if gate_ok:
    ss = list(out["sessions"])
    Zf = np.mean([(np.array(out["sessions"][s]["family"]) - out["sessions"][s]["family_false_mean"]) / out["sessions"][s]["family_false_sd"] for s in ss], axis=0)
    Zc = np.mean([(np.array(out["sessions"][s]["C09"]) - np.mean(out["sessions"][s]["C09"][1:])) / np.std(out["sessions"][s]["C09"][1:]) for s in ss], axis=0)
    rf = int(1 + (Zf[1:] >= Zf[0]).sum()); rc = int(1 + (Zc[1:] >= Zc[0]).sum())
    top = sum(out["sessions"][s]["family_rank"] <= 19 for s in ss); topc = sum(out["sessions"][s]["C09_rank"] <= 19 for s in ss)
    out["combined"] = {"family_rank": rf, "C09_rank": rc, "sessions_top5_family": top, "sessions_top5_C09": topc,
                       "family_survives": bool(top >= 2 and rf <= 4), "C09_survives": bool(topc >= 2 and rc <= 4)}
    print(json.dumps(out["combined"]))
json.dump(out, open(os.path.join(HERE, "hm14.json"), "w"), default=float)   # amendment 2, after run 2: the write failed on a float32
