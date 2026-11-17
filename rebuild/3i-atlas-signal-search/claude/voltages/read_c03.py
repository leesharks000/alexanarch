"""read_c03.py — reading C03's band as a voltage signal.
For each scan: dechirp the baseband by the comet drift (track from ../oh13), so a comet-frame carrier sits at 0 Hz.
1. Coherence: FFT of the whole 300 s (3.3 mHz resolution) per polarization; the power within ±2.5 Hz of 0 against
   the same statistic at control offsets ±20..±300 Hz; and the peak bin's z. A coherent carrier would rise above the
   incoherent 0.70 Hz result by up to sqrt(300 s x 0.7 Hz) ~ 14x in amplitude SNR; a 5 Hz-wide process would not.
2. X-Y cross-correlation at 0 Hz: a signal common to both polarizations correlates them; noise does not.
3. Audio: the ±25 Hz band around the track, shifted to 600 Hz and resampled to 8 kHz, one WAV per scan, both pols summed
   incoherently into stereo (left X, right Y); and a control band at +100 Hz.
Writes out/read_c03.json and out/c03_scanSCAN.wav, out/ctrl_scanSCAN.wav."""
import numpy as np, json, pathlib, wave
from scipy.signal import resample_poly
H = pathlib.Path(__file__).resolve().parent
TR = {s["scan"]: s for s in {c["id"]: c for c in json.load(open(H.parent / "oh13/oh13_candidates.json"))["candidates"]}["C03"]["scans"]}
ROLE = {"0013": "ON", "0015": "ON", "0017": "ON", "0014": "OFF", "0016": "OFF", "0018": "OFF"}; res = {}
def wav(path, L, R, rate=8000):
    m = max(np.abs(L).max(), np.abs(R).max()) + 1e-9
    d = np.stack([L / m, R / m], 1); d = (d * 0.9 * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(rate); w.writeframes(d.tobytes())
for s in ROLE:
    f = H / f"out/bb_C03_scan{s}.npz"
    if not f.exists(): continue
    z = np.load(f); x, y, fs = z["x"].astype(np.complex128), z["y"].astype(np.complex128), float(z["fs"]); n = len(x); t = np.arange(n) / fs
    tr = TR[s]; ts, ns = tr["tsamp_s"], tr["n_steps"]; rate = (tr["f_topo_last_Hz"] - tr["f_topo_first_Hz"]) / (ts * (ns - 1))
    fmid = (tr["f_topo_first_Hz"] + tr["f_topo_last_Hz"]) / 2; tm = t.mean()
    # mixed at fmid; remove the drift: track f(t) = fmid + rate*(t - tm) relative to mixer
    ph = np.exp(-1j * 2 * np.pi * (0.5 * rate * (t - tm) ** 2)); xd, yd = x * ph, y * ph
    out = {"role": ROLE[s], "rate_Hz_s": round(rate, 4)}
    for p, v in (("X", xd), ("Y", yd)):
        S = np.abs(np.fft.fftshift(np.fft.fft(v - v.mean()))) ** 2; fr = np.fft.fftshift(np.fft.fftfreq(n, 1 / fs)); dfq = fr[1] - fr[0]
        win = lambda c: S[np.abs(fr - c) <= 2.5].sum()
        ctr = [c for c in np.arange(-300, 300.1, 5) if abs(c) >= 20]
        cv = np.array([win(c) for c in ctr]); zc = (win(0) - np.median(cv)) / (1.4826 * np.median(np.abs(cv - np.median(cv))))
        loc = np.abs(fr) <= 2.5; pk = S[loc].max() / np.median(S[np.abs(fr) < 300])
        pks = [S[np.abs(fr - c) <= 2.5].max() / np.median(S[np.abs(fr) < 300]) for c in ctr]
        out[p] = {"z_band_pm2.5Hz": round(float(zc), 2), "peak_over_median_in_band": round(float(pk), 1),
                  "frac_controls_peak_ge": round(float(np.mean(np.array(pks) >= pk)), 3), "df_mHz": round(dfq * 1e3, 3)}
    # X-Y coherence near 0 Hz vs controls
    Xf = np.fft.fftshift(np.fft.fft(xd)); Yf = np.fft.fftshift(np.fft.fft(yd)); fr = np.fft.fftshift(np.fft.fftfreq(n, 1 / fs))
    def coh(c):
        m = np.abs(fr - c) <= 2.5; return np.abs((Xf[m] * Yf[m].conj()).sum()) / np.sqrt((np.abs(Xf[m]) ** 2).sum() * (np.abs(Yf[m]) ** 2).sum())
    ctr = [c for c in np.arange(-300, 300.1, 5) if abs(c) >= 20]; cv = np.array([coh(c) for c in ctr])
    out["XY_coherence"] = {"at_track": round(float(coh(0)), 4), "controls_median": round(float(np.median(cv)), 4), "frac_controls_ge": round(float(np.mean(cv >= coh(0))), 3)}
    # audio: band ±25 Hz, shift to 600 Hz, 8 kHz
    def band(v, c):
        V = np.fft.fft(v * np.exp(-2j * np.pi * c * t)); fq = np.fft.fftfreq(n, 1 / fs); V[np.abs(fq) > 25] = 0; return np.fft.ifft(V)
    up = lambda v: resample_poly(v, 8000 * 4, int(round(fs * 4)))
    for lab, c in (("c03", 0.0), ("ctrl", 100.0)):
        bx, by = up(band(xd, c)), up(band(yd, c)); ta = np.arange(len(bx)) / 8000
        car = np.exp(2j * np.pi * 600 * ta); wav(H / f"out/{lab}_scan{s}.wav", (bx * car).real, (by * car).real)
    res[s] = out; print(s, out)
json.dump(res, open(H / "out/read_c03.json", "w"), indent=1)
