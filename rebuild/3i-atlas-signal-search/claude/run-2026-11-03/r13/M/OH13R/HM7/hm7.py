"""PLAN-HM7: the thirteen at Parkes. Tracked 2 Hz power on each candidate's comet-frame track, three sessions,
against matched controls and the reference pointing. `python3 hm7.py extract SESSION` then `python3 hm7.py score`."""
import json, os, re, ssl, struct, sys, urllib.request
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "../../../../..")
C = 299792.458e3
CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE"))
BASE = "https://bldata.berkeley.edu/ATLAS/"
HALF = 1250          # +-2.5 kHz at 2 Hz per channel
EXC = 30             # +-60 Hz kept out of the reference around any window centre
OFFS = [3.2e3, -3.2e3, 6.4e3, -6.4e3, 9.6e3, -9.6e3, 12.8e3, -12.8e3, 16.0e3, -16.0e3, 19.2e3, -19.2e3]
SEED = 20261122
G1667 = ["C08", "C09", "C10", "C11"]

SESSIONS = {
    "20250731": dict(dir="PKS_Jul_31_2025", fmt="fil", eph="horizons-parkes-20250731.txt",
        pairs=[("guppi_60887_50760_6690867462_3IATLAS_S_0001", "guppi_60887_51102_6690868766_3IATLAS_R_0001"),
               ("guppi_60887_51442_6690870063_3IATLAS_S_0001", "guppi_60887_51782_6690871360_3IATLAS_R_0001"),
               ("guppi_60887_52123_6690872661_3IATLAS_S_0001", "guppi_60887_52472_6690873992_3IATLAS_R_0001")], extra=[]),
    "20250912": dict(dir="PKS_Sep_12_2025", fmt="h5", eph="horizons-parkes-20250912.txt",
        pairs=[("guppi_60930_18846_6704918083_3IATLAS_S_0001", "guppi_60930_19193_6704919406_3IATLAS_R_0001"),
               ("guppi_60930_19543_6704920742_3IATLAS_S_0001", "guppi_60930_19893_6704922077_3IATLAS_R_0001"),
               ("guppi_60930_20244_6704923416_3IATLAS_S_0001", "guppi_60930_20594_6704924751_3IATLAS_R_0001")],
        extra=["guppi_60930_17701_6704913715_3IATLAS_S_0001", "guppi_60930_18085_6704915180_3IATLAS_S_0001",
               "guppi_60930_18796_6704917892_3IATLAS_S_0001"]),
    "20251005": dict(dir="PKS_Oct_05_2025", fmt="h5", eph="horizons-parkes-20251005.txt",
        pairs=[("guppi_60953_19456_6712500976_3IATLAS_S_0001", "guppi_60953_19802_6712502296_3IATLAS_R_0001"),
               ("guppi_60953_20143_6712503597_3IATLAS_S_0001", "guppi_60953_20494_6712504936_3IATLAS_R_0001"),
               ("guppi_60953_20841_6712506259_3IATLAS_S_0001", "guppi_60953_21183_6712507564_3IATLAS_R_0001")], extra=[]),
}


def cands():
    d = json.load(open(os.path.join(ROOT, "oh13/oh13_candidates.json")))
    return {c["id"]: c["f_rest_Hz"] for c in d["candidates"]}


def windows():
    """[(name, kind, f_rest, parent)]: C01 folded into C02 (50 Hz apart); six controls per candidate, first six offsets
    in OFFS whose centre is more than 100 Hz from every candidate and every control already taken."""
    F = cands(); cs = [k for k in sorted(F) if k != "C01"]
    out = [(k, "cand", F[k], k) for k in cs]; taken = [F[k] for k in sorted(F)]
    for k in cs:
        n = 0
        for o in OFFS:
            if n == 6: break
            f = F[k] + o
            if any(abs(f - t) < 100 for t in taken): continue
            out.append((f"{k}{'+' if o > 0 else '-'}{abs(o) / 1e3:.1f}k", "ctrl", f, k)); taken.append(f); n += 1
        assert n == 6, k
    return out


def ephem(name):
    t = open(os.path.join(HERE, name)).read()
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in t.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    E = np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
    return lambda mjd: np.interp(mjd, E[:, 0], E[:, 1]) * 1e3      # m/s, range-rate from the Parkes site


def get(url, a=None, b=None, tries=6):
    for i in range(tries):
        try:
            q = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"} if a is not None else {})
            return urllib.request.urlopen(q, context=CTX, timeout=300).read()
        except Exception as e:
            if i == tries - 1: raise
            import time; time.sleep(5 * (i + 1))


def fil_header(url):
    b = get(url, 0, 4095); i = 0; h = {}
    ints = {"nchans", "nifs", "nbits", "telescope_id", "machine_id", "data_type", "nbeams", "ibeam", "barycentric", "pulsarcentric"}
    def s():
        nonlocal i; n = struct.unpack("<i", b[i:i + 4])[0]; i += 4; v = b[i:i + n].decode(); i += n; return v
    assert s() == "HEADER_START"
    while True:
        k = s()
        if k == "HEADER_END": break
        if k in ("source_name", "rawdatafile"): h[k] = s()
        elif k in ints: h[k] = struct.unpack("<i", b[i:i + 4])[0]; i += 4
        else: h[k] = struct.unpack("<d", b[i:i + 8])[0]; i += 8
    h["hdrlen"] = i; return h


class Product:
    """Row access to a 2 Hz (.0000) or 2 kHz (.0002) product: rows(k, a, b) -> float32 [nifs, b-a]."""
    def __init__(self, url, fmt):
        self.url, self.fmt = url, fmt
        if fmt == "h5":
            import fsspec, h5py, hdf5plugin  # noqa: F401
            self.fh = fsspec.open(url, "rb", block_size=2 ** 22).open(); self.h = h5py.File(self.fh, "r"); d = self.h["data"]
            a = d.attrs; self.d = d
            self.fch1, self.foff, self.nch, self.ts, self.t0, self.nifs = (float(a["fch1"]), float(a["foff"]), int(a["nchans"]),
                                                                       float(a["tsamp"]), float(a["tstart"]), int(a["nifs"]))
            self.nint = d.shape[0]
        else:
            h = fil_header(url); self.h = h
            self.fch1, self.foff, self.nch, self.ts, self.t0, self.nifs = h["fch1"], h["foff"], h["nchans"], h["tsamp"], h["tstart"], h["nifs"]
            size = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), context=CTX, timeout=120).headers["Content-Length"])
            self.nint = (size - h["hdrlen"]) // (self.nch * self.nifs * 4)

    def chan(self, f):                       # channel index of frequency f (Hz), fch1 the centre of channel 0
        return (self.fch1 * 1e6 - f) / (-self.foff * 1e6)

    def tmid(self, k): return self.t0 + (k + 0.5) * self.ts / 86400.0

    def rows(self, k, a, b):
        if self.fmt == "h5": return np.asarray(self.d[k, :, a:b], np.float32)
        out = np.empty((self.nifs, b - a), np.float32)
        for p in range(self.nifs):
            o = self.h["hdrlen"] + ((k * self.nifs + p) * self.nch + a) * 4
            out[p] = np.frombuffer(get(self.url, o, o + (b - a) * 4 - 1), "<f4")
        return out


def extract(sname):
    S = SESSIONS[sname]; v = ephem(S["eph"]); W = windows(); FR = np.array([w[2] for w in W])
    stems = [x for p in S["pairs"] for x in p] + S["extra"]
    for stem in stems:
        out = os.path.join(HERE, f"hm7_{sname}_{stem.split('_')[2]}.npz")
        if os.path.exists(out): continue
        url = BASE + S["dir"] + "/blc07/" + stem + (".0000.h5" if S["fmt"] == "h5" else ".0000.fil")
        P = Product(url, S["fmt"]); nk = P.nint
        A = np.zeros((len(W), nk, 2 * HALF + 1), np.float32); IC = np.zeros((len(W), nk))
        for k in range(nk):
            r = 1 - v(P.tmid(k)) / C; ic = P.chan(FR * r); IC[:, k] = ic; ii = np.rint(ic).astype(int)
            a, b = ii.min() - HALF - 2, ii.max() + HALF + 3
            row = P.rows(k, a, b)[0]
            for w in range(len(W)):
                A[w, k] = row[ii[w] - HALF - a: ii[w] + HALF + 1 - a]
        # descriptive 2 kHz strips, every IF, for G1667 and their controls
        url2 = BASE + S["dir"] + "/blc07/" + stem + (".0002.h5" if S["fmt"] == "h5" else ".0002.fil")
        sel = [i for i, w in enumerate(W) if w[3] in G1667]
        try:
            Q = Product(url2, S["fmt"]); nq = Q.nint
            B = np.zeros((len(sel), nq, Q.nifs, 21), np.float32)
            for k in range(nq):
                r = 1 - v(Q.tmid(k)) / C; jj = np.rint(Q.chan(FR[sel] * r)).astype(int); a, b = jj.min() - 11, jj.max() + 12
                row = Q.rows(k, a, b)
                for n, j in enumerate(jj): B[n, k] = row[:, j - 10 - a: j + 11 - a]
            q2 = dict(B=B, q_nifs=Q.nifs, q_t0=Q.t0, q_ts=Q.ts)
        except Exception as e:
            q2 = dict(B=np.zeros(0), q_err=str(e)[:300])
        np.savez_compressed(out, A=A, IC=IC, t0=P.t0, ts=P.ts, fch1=P.fch1, foff=P.foff, names=np.array([w[0] for w in W]), **q2)
        print(sname, stem, nk, "done", flush=True)


def zscore(A, centre_offsets):
    """A [nk, 2H+1] one window, rows flattened by their median; S(j) = sum over k and j-1..j+1; Z of S(0) against S(j),
    |j| >= EXC, |j| <= HALF-1, and |j - c| > EXC for every other window centre c in the band."""
    R = A / np.median(A, axis=1, keepdims=True)
    s = R.sum(0); S = s[:-2] + s[1:-1] + s[2:]; j = np.arange(-HALF + 1, HALF)
    ok = np.abs(j) >= EXC
    for c in centre_offsets: ok &= np.abs(j - c) > EXC
    ref = S[ok]; med = np.median(ref); mad = 1.4826 * np.median(np.abs(ref - med))
    return (S[HALF - 1] - med) / mad


def score():
    W = windows(); names = [w[0] for w in W]; FR = np.array([w[2] for w in W]); rng = np.random.default_rng(SEED)
    res = {"windows": [list(w[:2]) + [w[2], w[3]] for w in W], "sessions": {}}
    for sname, S in SESSIONS.items():
        Z = {}; flags = {}; inj = {}
        for stem in [x for p in S["pairs"] for x in p] + S["extra"]:
            f = np.load(os.path.join(HERE, f"hm7_{sname}_{stem.split('_')[2]}.npz")); A = f["A"]; IC = f["IC"]
            fch1, foff = float(f["fch1"]), float(f["foff"])
            z = []
            for w in range(len(W)):
                d = IC - IC[w]; co = [float(np.median(d[u])) for u in range(len(W)) if u != w and abs(np.median(d[u])) <= HALF]
                z.append(zscore(A[w], co))
                # coarse-channel DC: 0.5 MHz coarse channels, centres at fch1 - (n + 1/2) * 0.5 MHz
                fr = fch1 * 1e6 + IC[w] * foff * 1e6; dc = np.abs(((fch1 * 1e6 - fr) / 0.5e6) % 1 - 0.5) * 0.5e6
                if dc.min() < 100: flags.setdefault(names[w], set()).add("dc")
            Z[stem] = z
        ON = [p[0] for p in S["pairs"]]; OFF = [p[1] for p in S["pairs"]]
        zon = np.array([Z[s] for s in ON]); zoff = np.array([Z[s] for s in OFF]); D = zon.mean(0) - zoff.mean(0)
        good = np.array([n not in flags for n in names]); kind = np.array([w[1] for w in W])
        ctrl = (kind == "ctrl") & good
        rows = {}
        for i, w in enumerate(W):
            if w[1] != "cand": continue
            own = [j for j, u in enumerate(W) if u[1] == "ctrl" and u[3] == w[0] and good[j]]
            rows[w[0]] = dict(Z_on=zon[:, i].round(3).tolist(), Z_off=zoff[:, i].round(3).tolist(), D=round(float(D[i]), 3),
                              R1=bool((zon[:, i] >= 2.5).all() and (zoff[:, i] < 2.0).all()),
                              own_controls_D=[round(float(D[j]), 3) for j in own],
                              above_all_own=bool(len(own) > 0 and (D[i] > D[own]).all()),
                              pooled_pct=round(float((D[ctrl] < D[i]).mean() * 100), 1),
                              flags=sorted(flags.get(w[0], [])),
                              extra_Z=[round(float(Z[s][i]), 3) for s in S["extra"]])
        sc = [i for i, w in enumerate(W) if w[1] == "cand" and good[i]]; cpool = np.where(ctrl)[0]
        def fam(idx):
            m = D[idx].mean(); null = np.array([D[rng.choice(cpool, len(idx), replace=False)].mean() for _ in range(10000)])
            return dict(n=len(idx), mean_D=round(float(m), 3), p=round(float((1 + (null >= m).sum()) / 10001), 5))
        g = [i for i in sc if W[i][0] in G1667]
        # injection: a tone on the track, a * sigma_k in one channel per integration, every ON scan, scored candidates
        grid = [0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32]
        det = {}
        for a in grid:
            hits = []
            for s in ON:
                f = np.load(os.path.join(HERE, f"hm7_{sname}_{s.split('_')[2]}.npz")); A = f["A"].copy(); IC = f["IC"]
                for i in sc:
                    R = A[i] / np.median(A[i], axis=1, keepdims=True); sig = 1.4826 * np.median(np.abs(R - 1), axis=1)
                    R[:, HALF] += a * sig
                    d = IC - IC[i]; co = [float(np.median(d[u])) for u in range(len(W)) if u != i and abs(np.median(d[u])) <= HALF]
                    hits.append(zscore(R, co) >= 2.5)
            det[str(a)] = round(float(np.mean(hits)), 3)
        sig_frac = []
        for s in ON:
            A = np.load(os.path.join(HERE, f"hm7_{sname}_{s.split('_')[2]}.npz"))["A"]
            for i in sc:
                R = A[i] / np.median(A[i], axis=1, keepdims=True); sig_frac.append(float(np.median(1.4826 * np.median(np.abs(R - 1), axis=1))))
        res["sessions"][sname] = dict(candidates=rows, family_all=fam(sc), family_G1667=fam(g) if g else None,
                                      injection_detect_fraction=det, sigma_per_channel_over_median=round(float(np.median(sig_frac)), 4),
                                      flagged={k: sorted(v) for k, v in flags.items()})
    reps = {}
    for w in W:
        if w[1] != "cand": continue
        reps[w[0]] = [s for s in SESSIONS if res["sessions"][s]["candidates"][w[0]]["R1"]]
    res["R1_sessions"] = reps; res["replicates"] = {k: len(v) >= 2 for k, v in reps.items()}
    json.dump(res, open(os.path.join(HERE, "hm7_score.json"), "w"), indent=1); print(json.dumps(res["R1_sessions"]))
    for s in SESSIONS: print(s, res["sessions"][s]["family_all"], res["sessions"][s]["family_G1667"], res["sessions"][s]["injection_detect_fraction"])


if __name__ == "__main__":
    extract(sys.argv[2]) if sys.argv[1] == "extract" else score()
