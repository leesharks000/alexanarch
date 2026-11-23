"""PLAN-HM13-B2b: time structure of B2's rule-leads (PLAN-C4850 limit 2).
python3 hm13b2b.py SCAN -> b2b_SCAN.npz  (per-frame power, +-256 bins around each rule-lead of that scan, both polarizations; comet track +-2 bins)
python3 hm13b2b.py read -> b2b.json"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.normpath(os.path.join(HERE, "../.."))
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
cc = 21; FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6; dm.CH = cc; dm.FC = FC
N, C, DF, TBIN = dm.N, dm.C, dm.DF, dm.TBIN; NF = 833; HW = 256; QB = [(0, 208), (208, 416), (416, 624), (624, 833)]; ZON = 12.0
L = json.load(open(os.path.join(HERE, "b2.json")))["summary"]["leads"]
def tobin(f): return int(np.rint(N // 2 + (FC - f) / DF - 0.5))
if sys.argv[1] != "read":
    s = sys.argv[1]; T = [x for x in L if x["scan"] == s]; B0 = np.array([tobin(x["mhz"] * 1e6) for x in T]); off = np.arange(-HW, HW + 1)
    Eph = dm.ephem(); vel = lambda t: np.interp(t, Eph[:, 0], Eph[:, 1]); t0s = 61027 + int(dm.SCANS[s][0]) / 86400.0; v0 = vel(t0s + 0.5 * N * TBIN / 86400.0)
    Wn = np.zeros((NF, len(T), 2, 2 * HW + 1), np.float32); Pc = np.zeros((NF, len(T), 2), np.float32); SH = np.zeros(NF, int); n = 0; T0 = time.time()
    for j, X, Y in dm.frames(s, NF):
        sh = int(np.rint(FC * (vel(t0s + (j + 0.5) * N * TBIN / 86400.0) - v0) / C / DF)); SH[j] = sh
        for q, Z in enumerate((X, Y)):
            F = dm.fft(Z); p = F.real ** 2 + F.imag ** 2
            Wn[j, :, q] = p[B0[:, None] + off]; Pc[j, :, q] = p[B0[:, None] + sh + np.arange(-2, 3)].sum(1)
        n += 1
        if n % 100 == 0: print(s, n, round(time.time() - T0), flush=True)
    assert n == NF, n
    np.savez_compressed(os.path.join(HERE, f"b2b_{s}.npz"), W=Wn, Pc=Pc, SH=SH, B0=B0, mhz=np.array([x["mhz"] for x in T]), nframes=n)
    print(s, "done", n, round(time.time() - T0), flush=True); sys.exit()
Eph = dm.ephem(); out = []
for s in ("0013", "0015", "0017"):
    D = np.load(os.path.join(HERE, f"b2b_{s}.npz")); W = D["W"].astype(np.float32).sum(2); tt = (np.arange(NF) + 0.5) * N * TBIN
    t0s = 61027 + int(dm.SCANS[s][0]) / 86400.0; v = np.interp([t0s, t0s + NF * N * TBIN / 86400.0], Eph[:, 0], Eph[:, 1]); comet_dfdt = -FC * (v[1] - v[0]) / C / (NF * N * TBIN)
    for k, mhz in enumerate(D["mhz"]):
        w = W[:, k]; med = np.median(w, 1); pk = w.max(1) / med; am = w.argmax(1) - HW; on = pk > ZON
        duty = [round(float(on[a:b].mean()), 3) for a, b in QB]
        idx = np.where(on)[0]; drift = None; resid = None
        if len(idx) >= 10:
            c = np.polyfit(tt[idx], am[idx], 1); good = idx[np.abs(am[idx] - np.polyval(c, tt[idx])) <= 16]
            if len(good) >= 10: c = np.polyfit(tt[good], am[good], 1); drift = round(float(-c[0] * DF), 4); resid = int(len(good))
        pcr = D["Pc"][:, k].sum(1) / (5 * med)
        out.append(dict(scan=s, mhz=round(float(mhz), 6), duty_quarters=duty, duty_all=round(float(on.mean()), 3), first_on_s=(round(float(tt[idx[0]]), 1) if len(idx) else None),
                        last_on_s=(round(float(tt[idx[-1]]), 1) if len(idx) else None), measured_drift_hz_per_s=drift, frames_on_fit=resid, comet_drift_hz_per_s=round(float(comet_dfdt), 4),
                        comet_track_median_ratio=round(float(np.median(pcr)), 2), steady=bool(min(duty) >= 0.8), lead=bool(min(duty) >= 0.8)))
json.dump(dict(rule="steady iff on (peak/median > 12 within +-256 bins) in >= 80% of frames of every quarter; a rule-lead is a lead only if steady", events=out,
               summary=dict(n=len(out), steady=sum(x["steady"] for x in out), leads=[x for x in out if x["lead"]])), open(os.path.join(HERE, "b2b.json"), "w"), indent=1)
for x in out: print(x["scan"], x["mhz"], x["duty_quarters"], x["first_on_s"], x["last_on_s"], x["measured_drift_hz_per_s"], x["comet_drift_hz_per_s"], "steady" if x["steady"] else "")
print("steady", sum(x["steady"] for x in out), "of", len(out))
