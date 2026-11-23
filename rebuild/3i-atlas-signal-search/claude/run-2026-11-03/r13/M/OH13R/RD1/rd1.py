"""PLAN-RD1: read the start of each scan at the thirteen's coordinates, on the hypothesis that it is signal.  python3 rd1.py"""
import json, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from common import *
RD = os.path.dirname(os.path.abspath(__file__))   # amendment 1: common's HERE overwrote this module's

START = np.arange(0, 17); BODY = np.arange(51, NF); WIN = windows(); NW = len(WIN)
CANDS = [i for i, w in enumerate(WIN) if w[1] == "cand"]; CTRL = [i for i, w in enumerate(WIN) if w[1] == "ctrl"]
REF = [i for i, w in enumerate(WIN) if w[1] == "ref"]
OUT = {"windows": [w[0] for w in WIN], "kind": [w[1] for w in WIN]}


def lz76(s):
    """Lempel-Ziv (1976) complexity of a symbol sequence, normalized by n/log_k(n)."""
    s = list(s); n = len(s); k = max(2, len(set(s)))
    i, c, l = 0, 1, 1; kk = 1; kmax = 1
    if n < 2: return 0.0
    while True:
        if s[i + kk - 1] == s[l + kk - 1]:
            kk += 1
            if l + kk > n: c += 1; break
        else:
            kmax = max(kk, kmax); i += 1
            if i == l:
                c += 1; l += kmax
                if l + 1 > n: break
                i = 0; kk = 1; kmax = 1
            else: kk = 1
    return c * np.log(n) / np.log(k) / n


def per_scan(s):
    A = load(s); st = json.load(open(os.path.join(HERE, f"win_{s}.json")))["starts"]
    R = {}
    for w in range(NW):
        name, kind, f, _ = WIN[w]
        Z = A[:, w, :, :, 0].astype(np.float32) + 1j * A[:, w, :, :, 1].astype(np.float32)   # (NF, 2, WS)
        P = np.abs(Z) ** 2
        med = np.median(P[BODY], axis=0); med[med <= 0] = np.median(med)
        Pn = P / med
        itrack = track(s, f)[0] - st[w]                                                   # local index per frame
        S_track, S_wide = [], []
        for q in (0, 1):
            tb = np.array([Pn[j, q, max(0, itrack[j] - 1):itrack[j] + 2].mean() for j in START])
            S_track.append(float(tb.mean() - 1)); S_wide.append(float(Pn[START, q, M:M + W].mean() - 1))
        # comet frame: normalize amplitude per topocentric bin by the body, then de-Doppler the start frames
        Zn = Z / np.sqrt(med)
        Phi = phase_track(s, f, nf=len(START))
        D = []
        for q in (0, 1):
            Sel = Zn[START, q, M:M + W]
            D.append(dedop(Sel, Phi))                                                     # (17, W) comet frame
        D = np.stack(D)                                                                   # (2, 17, W)
        c = W // 2
        patch = (np.abs(D[:, :, c - 16:c + 17]) ** 2).sum(0)                              # (17, 33) X+Y
        # R4: band-limited series, track ±1.5 bins
        lzA, lzP, flat = [], [], []
        for q in (0, 1):
            B = np.zeros_like(D[q]); B[:, c - 1:c + 2] = D[q][:, c - 1:c + 2]
            z = np.fft.ifft(np.fft.ifftshift(B, axes=1), axis=1).ravel()                  # 17*W samples
            seg = z[: (len(z) // 128) * 128].reshape(-1, 128).mean(1)
            amp = np.abs(seg); lzA.append(lz76((amp > np.median(amp)).astype(int)))
            dph = np.angle(seg[1:] * np.conj(seg[:-1])); lzP.append(lz76(np.digitize(dph, [-np.pi / 2, 0, np.pi / 2])))
            sp = np.abs(np.fft.fftshift(np.fft.fft(z))) ** 2; mid = len(sp) // 2; band = sp[mid - 26:mid + 27] + 1e-30
            flat.append(float(np.exp(np.log(band).mean()) / band.mean()))
        R[name] = {"S_track": S_track, "S_wide": S_wide, "S_local": float(sum(S_track) - sum(S_wide)),
                   "lzA": float(np.mean(lzA)), "lzP": float(np.mean(lzP)), "flat": float(np.mean(flat)),
                   "patch": patch.astype(np.float32).tolist(),
                   "dyn": [(Pn[0:34, q, max(0, int(itrack[0]) - 32):int(itrack[0]) + 33]).astype(np.float32).round(3).tolist() for q in (0, 1)] if kind != "ctrl" else None}
        print(s, name, round(R[name]["S_local"], 3), flush=True)
    del A
    return R


def main():
    res = {s: per_scan(s) for s in SCANS}
    names = OUT["windows"]; cn = [names[i] for i in CANDS]; ctl = [names[i] for i in CTRL]
    rep = {"R1": {}, "R3": {}, "R4": {}, "step0": {}}
    for s in SCANS:
        rep["step0"][s] = {"cand_S_wide_mean": float(np.mean([sum(res[s][n]["S_wide"]) for n in cn])),
                           "ctrl_S_wide_mean": float(np.mean([sum(res[s][n]["S_wide"]) for n in ctl])),
                           "cand_S_track_mean": float(np.mean([sum(res[s][n]["S_track"]) for n in cn])),
                           "ctrl_S_track_mean": float(np.mean([sum(res[s][n]["S_track"]) for n in ctl]))}
    def Q(n, scans):
        p = [np.array(res[s][n]["patch"]).ravel() for s in scans]
        return float(np.mean([np.corrcoef(p[a], p[b])[0, 1] for a, b in ((0, 1), (0, 2), (1, 2))]))
    for n in cn:
        r1 = {}; r4 = {}
        for s in SCANS:
            v = res[s][n]["S_local"]; cv = [res[s][m]["S_local"] for m in ctl]
            r1[s] = {"S_local": v, "rank": int(1 + sum(x >= v for x in cv)), "of": len(cv) + 1, "confined": bool(v > max(cv))}
            r4[s] = {}
            for k, lower in (("lzA", True), ("lzP", True), ("flat", True)):
                v4 = res[s][n][k]; c4 = [res[s][m][k] for m in ctl]
                r4[s][k] = {"value": v4, "rank_low": int(1 + sum(x <= v4 for x in c4)), "structure": bool(v4 < min(c4))}
        qon = Q(n, ON); qoff = Q(n, OFF); qc = [Q(m, ON) for m in ctl]
        rep["R1"][n] = r1; rep["R4"][n] = r4
        rep["R3"][n] = {"Q_on": qon, "Q_off": qoff, "rank": int(1 + sum(x >= qon for x in qc)), "of": len(qc) + 1,
                        "recurs": bool(qon > max(qc) and qon > qoff)}
    verdict = {}
    for n in cn:
        ok = [s for s in ON if rep["R1"][n][s]["confined"] and any(rep["R4"][n][s][k]["structure"] for k in ("lzA", "lzP", "flat"))]
        verdict[n] = {"scans_confined_and_structured": ok, "recurs": rep["R3"][n]["recurs"], "pass": len(ok) >= 2 and rep["R3"][n]["recurs"]}
    rep["verdict"] = verdict
    json.dump(rep, open(os.path.join(RD, "rd1_report.json"), "w"), indent=1)
    json.dump({s: {n: {k: v for k, v in res[s][n].items() if k in ("dyn",)} for n in cn + [names[i] for i in REF]} for s in SCANS},
              open(os.path.join(RD, "rd1_dyn.json"), "w"))
    print("written rd1_report.json, rd1_dyn.json")


if __name__ == "__main__":
    main()
