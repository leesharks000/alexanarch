"""read_c03_nodrift.py — C03's baseband read without removing the comet's drift.
(a) Fixed in the receiver frame at the scan's mid-track frequency (no dechirp): band power ±2.5 Hz, peak bin, X–Y correlation.
(b) Fixed at the receiver-frame coordinate 1665644304.70 Hz (ChatGPT S-band audit), likewise.
(c) Coherent drift scan: rates -0.5..+0.5 Hz/s in 0.002 steps; at each, the strongest 3.3 mHz bin within ±25 Hz of the
    track centre, against the same at control centres ±100, ±150, ±200 Hz.
Writes out/read_c03_nodrift.json."""
import numpy as np, json, pathlib
H = pathlib.Path(__file__).resolve().parent
RX = 1665644304.702512
ROLE = {"0013": "ON", "0015": "ON", "0017": "ON", "0014": "OFF", "0016": "OFF", "0018": "OFF"}; res = {}
def stats(xd, yd, fs, c):
    n = len(xd); fr = np.fft.fftshift(np.fft.fftfreq(n, 1 / fs)); out = {}
    Xf = np.fft.fftshift(np.fft.fft(xd - xd.mean())); Yf = np.fft.fftshift(np.fft.fft(yd - yd.mean()))
    ctr = [k for k in np.arange(c - 300, c + 300.1, 5) if abs(k - c) >= 20 and abs(k) < 340]
    for p, F in (("X", Xf), ("Y", Yf)):
        S = np.abs(F) ** 2; med = np.median(S[np.abs(fr) < 340]); win = lambda k: S[np.abs(fr - k) <= 2.5].sum()
        cv = np.array([win(k) for k in ctr]); zc = (win(c) - np.median(cv)) / (1.4826 * np.median(np.abs(cv - np.median(cv))))
        pk = S[np.abs(fr - c) <= 2.5].max() / med; pks = np.array([S[np.abs(fr - k) <= 2.5].max() / med for k in ctr])
        out[p] = {"z_band": round(float(zc), 2), "peak_over_median": round(float(pk), 1), "frac_controls_peak_ge": round(float((pks >= pk).mean()), 3)}
    def coh(k):
        m = np.abs(fr - k) <= 2.5; return np.abs((Xf[m] * Yf[m].conj()).sum()) / np.sqrt((np.abs(Xf[m]) ** 2).sum() * (np.abs(Yf[m]) ** 2).sum())
    cv = np.array([coh(k) for k in ctr]); out["XY"] = {"at": round(float(coh(c)), 4), "ctrl_median": round(float(np.median(cv)), 4), "frac_ge": round(float((cv >= coh(c)).mean()), 3)}
    return out
for s in ROLE:
    z = np.load(H / f"out/bb_C03_scan{s}.npz"); x, y, fs, F0 = z["x"].astype(np.complex128), z["y"].astype(np.complex128), float(z["fs"]), float(z["F0"])
    n = len(x); t = np.arange(n) / fs; tm = t.mean()
    r = {"role": ROLE[s], "fixed_midtrack": stats(x, y, fs, 0.0), "receiver_fixed_offset_Hz": round(RX - F0, 2), "receiver_fixed": stats(x, y, fs, RX - F0)}
    # coherent drift scan
    rates = np.arange(-0.5, 0.5001, 0.002); fr = np.fft.fftshift(np.fft.fftfreq(n, 1 / fs)); centres = [0.0, -100, 100, -150, 150, -200, 200]
    best = {c: (0, 0, 0) for c in centres}; grid = {c: [] for c in centres}
    for rt in rates:
        ph = np.exp(-1j * np.pi * rt * (t - tm) ** 2)
        S = np.abs(np.fft.fftshift(np.fft.fft(x * ph))) ** 2 + np.abs(np.fft.fftshift(np.fft.fft(y * ph))) ** 2
        med = np.median(S)
        for c in centres:
            m = np.abs(fr - c) <= 25; j = np.argmax(S[m]); v = S[m][j] / med; grid[c].append(v)
            if v > best[c][0]: best[c] = (v, rt, fr[m][j])
    ctrlmax = [best[c][0] for c in centres if c != 0]
    r["drift_scan"] = {"track_best": {"peak_over_median": round(float(best[0][0]), 1), "rate_Hz_s": round(float(best[0][1]), 3), "offset_Hz": round(float(best[0][2]), 3)},
                       "controls_best_peak": [round(float(v), 1) for v in ctrlmax]}
    res[s] = r
    print(s, ROLE[s], "| fixed:", r["fixed_midtrack"], "| rx-fixed(off", r["receiver_fixed_offset_Hz"], "):", r["receiver_fixed"], "| drift scan:", r["drift_scan"])
json.dump(res, open(H / "out/read_c03_nodrift.json", "w"), indent=1)
