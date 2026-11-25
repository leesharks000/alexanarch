"""The Wow! as key, first application (2026-11-24, 22:14 EST: "we are even hypothetically treating the wow! signal as if it were an
intentionally sent cryptographic key for the 2025 data"). The six values 6, 14, 26, 30, 19, 5 read as a hop sequence: in successive
12 s steps (Big Ear's cadence) the signal sits in channel k_i of Big Ear's 10 kHz channels above an anchor. De-hop blc24 (.0002,
2.86 kHz x 1.07 s): for each anchor and each of the six cyclic phases, the power in the hopped channel per step, in units of that
channel's scan sigma; statistic = mean over the scan. The pareidolia measure: the same for 200 random six-value sequences (1-35).
A look, not a frozen test. Writes key_hop.json (with the de-hopped series, to be read).
    python3 key_hop.py"""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../wow3"))
import r457_stream as r, r2_r6_lines_a1 as m
C = m.C; H = m.H; V77 = -43.0112691
KEY = [6, 14, 26, 30, 19, 5]
rng = np.random.default_rng(6142630195); CTRL = [rng.integers(1, 36, 6).tolist() for _ in range(200)]
ROLE = {"0013": "ON", "0014": "OFF", "0015": "ON", "0016": "OFF", "0017": "ON", "0018": "OFF"}
out = {}
for sc in r.SCANS:
    name, x, fch1, foff, ts = r.read("blc24", sc)
    freqs = fch1 + foff * np.arange(x.shape[1]); t = np.arange(x.shape[0]) * ts
    mjd = 61027 + (int(r.SCANS[sc][0]) + 150) / 86400.0; v = float(m.VCOM(mjd))
    anchors = {"H_comet": H * (1 - v / C), "F0rev_comet": 1420.726 / (1 - V77 / C) * (1 - v / C), "F0ehm_comet": 1420.4556 / (1 - V77 / C) * (1 - v / C),
               "H_topo": H, "wow_topo": 1420.726}
    nstep = int((t[-1] - 10) // 12) + 1
    def chan_series(f_lo):                                  # 10 kHz channel starting at f_lo, 10 s sums every 12 s, robust sigma units
        sel = (freqs >= f_lo) & (freqs < f_lo + 0.010)
        y = x[:, sel].sum(1); s = np.array([y[(t >= 12 * k) & (t < 12 * k + 10)].mean() for k in range(nstep)])
        med = np.median(s); mad = 1.4826 * np.median(np.abs(s - med)); return (s - med) / (mad if mad > 0 else np.inf)
    res = {}
    for an, f_a in anchors.items():
        Z = np.array([chan_series(f_a + 0.010 * k) for k in range(36)])        # (36 channels, nstep)
        def stat(seq):
            best = None
            for ph in range(6):
                d = np.array([Z[seq[(i + ph) % 6], i] for i in range(nstep)])
                if best is None or d.mean() > best[0]: best = (float(d.mean()), ph, d)
            return best
        b = stat(KEY); c = np.array([stat(s)[0] for s in CTRL])
        res[an] = {"anchor_MHz": f_a, "mean_z": b[0], "phase": b[1], "rank_vs_random_keys": float((c < b[0]).mean()),
                   "dehopped_series": [round(float(q), 2) for q in b[2]]}
        print(sc, ROLE[sc], an, "mean z %.2f" % b[0], "rank %.2f" % res[an]["rank_vs_random_keys"], flush=True)
    out[sc] = {"role": ROLE[sc], "file": name, "anchors": res}
json.dump({"key": KEY, "scans": out}, open(os.path.join(HERE, "key_hop.json"), "w"), indent=1)
