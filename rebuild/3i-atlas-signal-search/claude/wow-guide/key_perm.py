"""The Wow! as key, third application (2026-11-24, 23:42 EST: "yup, lets run the permutation reading"). The six values 6, 14, 26,
30, 19, 5 ranked by size are 2, 3, 5, 6, 4, 1: an order for six things. Read as a transposition key: the stream was scrambled in
blocks of six and the key puts each block back. Two conventions, both read: S = (2,3,5,6,4,1), take the block's slots in that
order; Sinv = (6,1,2,5,3,4), its inverse.
  P1, in time: blocks of six successive steps of each channel's time series (steps of 1.07 s, 6.4 s, and 11.8 s, Big Ear's step).
  P2, in frequency: blocks of six adjacent channels of each scan's time-mean spectrum.
What a right key would do: make the stream more orderly than it is as recorded. Order is measured as the correlation of each
sample with the next after re-ordering (z = sum of adjacent products / sqrt(pairs), every block alignment, the largest kept).
The pareidolia measure is exhaustive: all 720 orders of six, the recorded order among them.
Data: blc24 .0002 (2.86 kHz x 1.07 s, 65,536 channels), scans 0013-0018; and look1.npz (2.79 Hz x 6.08 s, comet frame, +-6 kHz
around the vessel's two frequencies). A look, not a frozen test.    python3 key_perm.py"""
import json, os, sys, itertools, time, numpy as np
from scipy.ndimage import median_filter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../wow3"))
C = 299792.458; H = 1420.40575177; V77 = -43.0112691
PERMS = np.array(list(itertools.permutations(range(6)))); ID = 0
S = (1, 2, 4, 5, 3, 0); SINV = tuple(int(i) for i in np.argsort(S))
iS = int(np.flatnonzero((PERMS == S).all(1))[0]); iSI = int(np.flatnonzero((PERMS == SINV).all(1))[0])
ROLE = {"0013": "ON", "0014": "OFF", "0015": "ON", "0016": "OFF", "0017": "ON", "0018": "OFF"}

def order_z(Z):
    """Z (n, nch), unit variance along axis 0. Returns (720, nch): adjacent-sample order after each permutation of blocks of six."""
    best = None
    for p in range(6):
        nb = (Z.shape[0] - p) // 6
        if nb < 2: continue
        X = Z[p:p + 6 * nb].reshape(nb, 6, -1); M = np.einsum('bic,bjc->ijc', X, X); N = np.einsum('bic,bjc->ijc', X[:-1], X[1:])
        A = sum(M[PERMS[:, k], PERMS[:, k + 1]] for k in range(5)) + N[PERMS[:, 5], PERMS[:, 0]]
        A = A / np.sqrt(6 * nb - 1); best = A if best is None else np.maximum(best, A)
    return best.astype(np.float32)

def std_t(x):
    med = np.median(x, 0); mad = 1.4826 * np.median(np.abs(x - med), 0); mad[mad == 0] = np.inf
    Z = np.clip((x - med) / mad, -8, 8).astype(np.float32); Z -= Z.mean(0); return Z / (Z.std(0) + 1e-9)

def rank(v, i): return float((v < v[i]).mean())

def summarize(A, label):
    """A (720, nch). Counts of channels made orderly, and of channels lifted above the recorded order, for the key against all orders."""
    n5 = (A >= 5).sum(1); lift = ((A >= 5) & (A - A[ID] >= 3)); nl = lift.sum(1); mean = A.mean(1)
    o = {"n_ge5": {"S": int(n5[iS]), "Sinv": int(n5[iSI]), "recorded": int(n5[ID]), "median_of_720": float(np.median(n5)), "rank_S": rank(n5, iS), "rank_Sinv": rank(n5, iSI)},
         "lifted": {"S": int(nl[iS]), "Sinv": int(nl[iSI]), "median_of_719": float(np.median(np.delete(nl, ID))), "max_of_719": int(np.delete(nl, ID).max()),
                    "rank_S": float((np.delete(nl, ID) < nl[iS]).mean()), "rank_Sinv": float((np.delete(nl, ID) < nl[iSI]).mean())},
         "band_mean": {"S": float(mean[iS]), "Sinv": float(mean[iSI]), "recorded": float(mean[ID]), "rank_S": rank(mean, iS), "rank_Sinv": rank(mean, iSI)}}
    print(label, "n>=5: S %d Sinv %d recorded %d (median %.0f; ranks %.2f %.2f) | lifted: S %d Sinv %d (median %.0f max %d; ranks %.2f %.2f) | band mean ranks %.2f %.2f" % (
        n5[iS], n5[iSI], n5[ID], np.median(n5), o["n_ge5"]["rank_S"], o["n_ge5"]["rank_Sinv"], nl[iS], nl[iSI], o["lifted"]["median_of_719"], o["lifted"]["max_of_719"],
        o["lifted"]["rank_S"], o["lifted"]["rank_Sinv"], o["band_mean"]["rank_S"], o["band_mean"]["rank_Sinv"]), flush=True)
    return o, lift

out = {"S": [i + 1 for i in S], "Sinv": [i + 1 for i in SINV], "coarse": {}, "fine": {}}; P = os.path.join(HERE, "key_perm.json"); LIFT = {}
# ---- fine: look1.npz, comet frame, at the vessel's frequencies (no download)
G = np.load(os.path.join(HERE, "look1.npz"))
for k in G.files:
    Z = G[k].astype(np.float32); Zt = Z - Z.mean(0); Zt /= Zt.std(0) + 1e-9
    o1, _ = summarize(order_z(Zt), "fine P1 " + k)
    line = Z.mean(0); line = (line - line.mean()) / line.std(); A2 = order_z(line[:, None])[:, 0]
    out["fine"][k] = {"role": ROLE[k[-4:]], "P1": o1, "P2": {"S": float(A2[iS]), "Sinv": float(A2[iSI]), "recorded": float(A2[ID]), "max_of_720": float(A2.max()), "rank_S": rank(A2, iS), "rank_Sinv": rank(A2, iSI)}}
    print("fine P2", k, "S %.2f Sinv %.2f recorded %.2f max %.2f ranks %.2f %.2f" % (A2[iS], A2[iSI], A2[ID], A2.max(), rank(A2, iS), rank(A2, iSI)), flush=True)
json.dump(out, open(P, "w"), indent=1)
# ---- coarse: blc24 .0002, the whole node
import r457_stream as r, r2_r6_lines_a1 as m
for sc in r.SCANS:
    t0 = time.time(); name, x, fch1, foff, ts = r.read("blc24", sc); x = x / np.median(x, 1, keepdims=True); freqs = fch1 + foff * np.arange(x.shape[1])
    mjd = 61027 + (int(r.SCANS[sc][0]) + 150) / 86400.0; v = float(m.VCOM(mjd))
    anch = {"H_comet": H * (1 - v / C), "F0rev_comet": 1420.726 / (1 - V77 / C) * (1 - v / C), "F0ehm_comet": 1420.4556 / (1 - V77 / C) * (1 - v / C), "H_topo": H, "wow_topo": 1420.726}
    ai = {k: int(round((f - fch1) / foff)) for k, f in anch.items()}; R = {"role": ROLE[sc], "file": name, "P1": {}}
    for un, nb in (("1.07s", 1), ("6.4s", 6), ("11.8s", 11)):
        n = x.shape[0] // nb * nb; A = order_z(std_t(x[:n].reshape(-1, nb, x.shape[1]).mean(1)))
        o, lift = summarize(A, f"{sc} {ROLE[sc]} P1 {un}")
        o["anchors"] = {k: {"S": float(A[iS, i - 1:i + 2].max()), "Sinv": float(A[iSI, i - 1:i + 2].max()), "recorded": float(A[ID, i - 1:i + 2].max()),
                            "rank_S": rank(A[:, i - 1:i + 2].max(1), iS), "rank_Sinv": rank(A[:, i - 1:i + 2].max(1), iSI)} for k, i in ai.items()}
        for nm, ii in (("S", iS), ("Sinv", iSI)):
            idx = np.flatnonzero(lift[ii]); LIFT[(sc, un, nm)] = idx
            o[f"lifted_{nm}_channels"] = [(round(float(freqs[i]), 4), round(float(A[ii, i]), 1), round(float(A[ID, i]), 1)) for i in idx[np.argsort(A[ii, idx])[::-1][:40]]]
        R["P1"][un] = o; del A, lift
    s = x.mean(0); q = s / median_filter(s, 101, mode="nearest") - 1; z = np.concatenate([r.rsig(q[i:i + 1024]) for i in range(0, len(q), 1024)]); z = np.clip(z, -8, 8); z = (z - z.mean()) / z.std()
    A2 = order_z(z[:, None])[:, 0]; R["P2"] = {"band": {"S": float(A2[iS]), "Sinv": float(A2[iSI]), "recorded": float(A2[ID]), "max_of_720": float(A2.max()), "rank_S": rank(A2, iS), "rank_Sinv": rank(A2, iSI)}, "anchors": {}}
    for k, i in ai.items():
        w = z[i - 300:i + 300]; w = (w - w.mean()) / w.std(); a = order_z(w[:, None])[:, 0]
        R["P2"]["anchors"][k] = {"S": float(a[iS]), "Sinv": float(a[iSI]), "recorded": float(a[ID]), "rank_S": rank(a, iS), "rank_Sinv": rank(a, iSI)}
    print(sc, ROLE[sc], "P2 band: S %.1f Sinv %.1f recorded %.1f max %.1f ranks %.2f %.2f | anchors" % (A2[iS], A2[iSI], A2[ID], A2.max(), rank(A2, iS), rank(A2, iSI)),
          {k: (round(v["rank_S"], 2), round(v["rank_Sinv"], 2)) for k, v in R["P2"]["anchors"].items()}, "%.0fs" % (time.time() - t0), flush=True)
    out["coarse"][sc] = R; json.dump(out, open(P, "w"), indent=1); del x
out["on_only_lifted"] = {}
for un in ("1.07s", "6.4s", "11.8s"):
    for nm in ("S", "Sinv"):
        for on, off in (("0013", "0014"), ("0015", "0016"), ("0017", "0018")):
            a = np.setdiff1d(LIFT[(on, un, nm)], LIFT[(off, un, nm)]); out["on_only_lifted"][f"{un}|{nm}|{on}/{off}"] = [round(float(freqs[i]), 4) for i in a]
        allon = np.intersect1d(np.intersect1d(LIFT[("0013", un, nm)], LIFT[("0015", un, nm)]), LIFT[("0017", un, nm)])
        out["on_only_lifted"][f"{un}|{nm}|in all three ON"] = [round(float(freqs[i]), 4) for i in allon]
        print(un, nm, "lifted in all three ON scans:", len(allon), flush=True)
json.dump(out, open(P, "w"), indent=1)
