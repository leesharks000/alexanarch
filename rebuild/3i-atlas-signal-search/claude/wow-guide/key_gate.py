"""The Wow! as key, second application (2026-11-24, 22:48 EST: "lets do the time gate reading"). The six values 6, 14, 26, 30, 19, 5
sum to 100. Read as durations in a unit u, repeating with period 100 u:
  G1, gates: on 6, off 14, on 26, off 30, on 19, off 5 (or the reverse sign); per channel, the correlation of its time series with
      the zero-mean gate pattern, in sigma, largest over every start phase, either sign.
  G2, symbol lengths: six successive symbols lasting 6, 14, 26, 30, 19, 5; per channel, the variance of its time series carried by
      the six segment levels (chi-square, 5 degrees), largest over every start phase.
Units: 0.72 s (the key spans the Wow's 72 s), 1 s, 1.2 s (a tenth of Big Ear's 12 s step), and scan/100 (the key spans the scan).
Data: blc24 .0002 (2.86 kHz x 1.07 s, 65,536 channels), scans 0013-0018. Each time row divided by its band median, each channel
standardised over time (median, MAD). Pareidolia measure: the same for random keys, six parts >= 1 summing to 100 (same period,
other boundaries). A look, not a frozen test.    python3 key_gate.py [n_random]"""
import json, os, sys, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../wow3"))
import r457_stream as r, r2_r6_lines_a1 as m
C = m.C; H = m.H; V77 = -43.0112691; KEY = [6, 14, 26, 30, 19, 5]; NR = int(sys.argv[1]) if len(sys.argv) > 1 else 100
rng = np.random.default_rng(61426301905)
def comp():
    c = np.sort(rng.choice(np.arange(1, 100), 5, replace=False)); return np.diff(np.concatenate([[0], c, [100]])).tolist()
CTRL = [comp() for _ in range(NR)]
ROLE = {"0013": "ON", "0014": "OFF", "0015": "ON", "0016": "OFF", "0017": "ON", "0018": "OFF"}
UNITS = {"0.72s": 0.72, "1s": 1.0, "1.2s": 1.2, "scan/100": None}

def seg_index(key, u, t, ph):
    """Which of the six segments each sample centre falls in, the pattern starting ph seconds before t=0, period 100 u."""
    pos = ((t + ph) / u) % 100.0; return np.searchsorted(np.cumsum(key), pos, side="right").clip(0, 5)

def scores(Z, key, u, t, ts):
    """Z (nt, nch) standardised. Returns per-channel G1 and G2, each the largest over start phases one sample apart."""
    nt = Z.shape[0]; nph = int(np.ceil(100 * u / ts)); G1 = np.zeros(Z.shape[1], np.float32); G2 = np.zeros(Z.shape[1], np.float32)
    T1 = np.empty((nph, nt), np.float32); T2 = np.zeros((nph, 6, nt), np.float32)
    for p in range(nph):
        s = seg_index(key, u, t, p * ts); g = np.where(s % 2 == 0, 1.0, -1.0); g = g - g.mean(); T1[p] = g / np.sqrt((g ** 2).sum())
        for k in range(6):
            w = (s == k).astype(np.float32); n = w.sum()
            if n: T2[p, k] = w / np.sqrt(n)
    G1 = np.abs(T1 @ Z).max(0)
    for p in range(nph):                                    # between-segment sum of squares: sum_k (segment sum)^2 / n_k (channel means are ~0)
        G2 = np.maximum(G2, ((T2[p] @ Z) ** 2).sum(0))
    return G1, G2

out = {"key": KEY, "n_random": NR, "scans": {}}; P = os.path.join(HERE, "key_gate.json")
if os.path.exists(P): out = json.load(open(P))                    # resume: scans already written are kept (the run was stopped once at 30 min)
for sc in r.SCANS:
    if sc in out["scans"]: continue
    t0 = time.time(); name, x, fch1, foff, ts = r.read("blc24", sc)
    x = x / np.median(x, 1, keepdims=True); med = np.median(x, 0); mad = 1.4826 * np.median(np.abs(x - med), 0); mad[mad == 0] = np.inf
    Z = ((x - med) / mad).astype(np.float32); Z = np.clip(Z, -8, 8); Z -= Z.mean(0); Z /= Z.std(0) + 1e-9; del x
    nt = Z.shape[0]; t = (np.arange(nt) + 0.5) * ts; freqs = fch1 + foff * np.arange(Z.shape[1])
    mjd = 61027 + (int(r.SCANS[sc][0]) + 150) / 86400.0; v = float(m.VCOM(mjd))
    anch = {"H_comet": H * (1 - v / C), "F0rev_comet": 1420.726 / (1 - V77 / C) * (1 - v / C), "F0ehm_comet": 1420.4556 / (1 - V77 / C) * (1 - v / C), "H_topo": H, "wow_topo": 1420.726}
    ai = {k: int(round((f - fch1) / foff)) for k, f in anch.items()}
    S = {"role": ROLE[sc], "file": name, "nt": nt, "tsamp": ts, "units": {}}
    for un, u in UNITS.items():
        u = u or nt * ts / 100.0; g1, g2 = scores(Z, KEY, u, t, ts)
        U = {"u_s": u, "G1": {"max": float(g1.max()), "p9999": float(np.quantile(g1, 0.9999)), "n_ge6": int((g1 >= 6).sum()), "top5": [(float(freqs[i]), float(g1[i])) for i in np.argsort(g1)[-5:][::-1]]},
             "G2": {"max": float(g2.max()), "p9999": float(np.quantile(g2, 0.9999)), "n_ge45": int((g2 >= 45).sum()), "top5": [(float(freqs[i]), float(g2[i])) for i in np.argsort(g2)[-5:][::-1]]},
             "anchors": {k: {"G1": float(g1[i - 1:i + 2].max()), "G2": float(g2[i - 1:i + 2].max()), "G1_pct": float((g1 < g1[i - 1:i + 2].max()).mean()), "G2_pct": float((g2 < g2[i - 1:i + 2].max()).mean())} for k, i in ai.items()}}
        c1 = []; c2 = []; cn1 = []; cn2 = []; ca = {k: [] for k in ai}
        for ck in CTRL:
            a, b = scores(Z, ck, u, t, ts); c1.append(float(np.quantile(a, 0.9999))); c2.append(float(np.quantile(b, 0.9999))); cn1.append(int((a >= 6).sum())); cn2.append(int((b >= 45).sum()))
            for k, i in ai.items(): ca[k].append((float(a[i - 1:i + 2].max()), float(b[i - 1:i + 2].max())))
        U["rank"] = {"G1_p9999": float((np.array(c1) < U["G1"]["p9999"]).mean()), "G2_p9999": float((np.array(c2) < U["G2"]["p9999"]).mean()),
                     "G1_n_ge6": float((np.array(cn1) < U["G1"]["n_ge6"]).mean()), "G2_n_ge45": float((np.array(cn2) < U["G2"]["n_ge45"]).mean()),
                     "ctrl_G1_n_ge6_median": float(np.median(cn1)), "ctrl_G2_n_ge45_median": float(np.median(cn2)),
                     "anchors": {k: {"G1": float((np.array([q[0] for q in ca[k]]) < U["anchors"][k]["G1"]).mean()), "G2": float((np.array([q[1] for q in ca[k]]) < U["anchors"][k]["G2"]).mean())} for k in ai}}
        S["units"][un] = U
        print(sc, ROLE[sc], un, "G1 n>=6 %d (ctrl med %.0f, rank %.2f) p9999 rank %.2f | G2 n>=45 %d (ctrl med %.0f, rank %.2f) p9999 rank %.2f | %.0fs" % (
            U["G1"]["n_ge6"], U["rank"]["ctrl_G1_n_ge6_median"], U["rank"]["G1_n_ge6"], U["rank"]["G1_p9999"], U["G2"]["n_ge45"], U["rank"]["ctrl_G2_n_ge45_median"], U["rank"]["G2_n_ge45"], U["rank"]["G2_p9999"], time.time() - t0), flush=True)
    out["scans"][sc] = S; json.dump(out, open(os.path.join(HERE, "key_gate.json"), "w"), indent=1)
