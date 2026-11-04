"""Frozen full-band comet-frame search, Parkes 2025-07-31 (pks/PLAN-fullband.md, sha256 2337ec83...). Streams each node in overlapped blocks by HTTP
range, keeps nothing but results. python3 pks/fullband.py blc07 [blc06 ...]   -> pks/fb_<node>.json (resumable per block)"""
import sys, json, os, re, struct, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
R = "https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/"
C = 299792.458; BLK = 1 << 20; OV = 600; CORE = OV // 2; ZON, ZOFF = 2.5, 2.0
rng = np.random.default_rng(11); OFFS = list(rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * C / 1.42e9)[:20]

def get(u, a, b, tries=5):
    for t in range(tries):
        try:
            r = urllib.request.Request(u, headers={"Range": f"bytes={a}-{b}"}); return urllib.request.urlopen(r, timeout=180).read()
        except Exception:
            time.sleep(2 + 3 * t)
    raise RuntimeError(f"range failed {u} {a}")

def header(u):
    b = get(u, 0, 2047); i = 0
    def rs(i):
        n = struct.unpack('<i', b[i:i + 4])[0]; return b[i + 4:i + 4 + n].decode('latin1'), i + 4 + n
    _, i = rs(0); h = {}
    while True:
        k, i = rs(i)
        if k == 'HEADER_END': h['hdr_len'] = i; return h
        if k in ('source_name', 'rawdatafile'): v, i = rs(i)
        elif k in ('telescope_id', 'machine_id', 'data_type', 'nchans', 'nbits', 'nifs', 'nbeams', 'ibeam', 'barycentric', 'pulsarcentric'):
            v = struct.unpack('<i', b[i:i + 4])[0]; i += 4
        else: v = struct.unpack('<d', b[i:i + 8])[0]; i += 8
        h[k] = v

def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
         "SITE_COORD": "'148.2635,-32.9984,0.415'", "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'",
         "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])

def run(node):
    out_p = f"pks/fb_{node}.json"
    idx = urllib.request.urlopen(R + node + "/", timeout=60).read().decode()
    files = sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"', idx)))
    assert len(files) == 6, files
    roles = ["S" if "_S_" in f else "R" for f in files]
    H = [header(R + node + "/" + f) for f in files]
    nch, foff, fch1 = H[0]['nchans'], H[0]['foff'] * 1e6, H[0]['fch1'] * 1e6
    E = horizons(min(h['tstart'] for h in H), max(h['tstart'] for h in H) + 0.01)
    t = [h['tstart'] + (np.arange(20) + 0.5) * h['tsamp'] / 86400.0 for h in H]
    T0 = min(h['tstart'] for h in H)
    state = json.load(open(out_p)) if os.path.exists(out_p) else {"node": node, "plan_sha256": "2337ec83e33719c0b1182417a0872bae0d842ed48be4fff3d0036f70d4199d73",
            "files": files, "fch1_MHz": fch1 / 1e6, "foff_Hz": foff, "blocks": {}}
    starts = list(range(0, nch - OV, BLK - OV))
    ex = cf.ThreadPoolExecutor(24)
    for b0 in starts:
        if str(b0) in state["blocks"]: continue
        n = min(BLK, nch - b0)
        def fetch(job):
            i, k = job; h = H[i]; a = h['hdr_len'] + (k * nch + b0) * 4
            return i, k, np.frombuffer(get(R + node + "/" + files[i], a, a + n * 4 - 1), '<f4')
        X = np.zeros((6, 20, n), np.float32)
        for i, k, row in ex.map(fetch, [(i, k) for i in range(6) for k in range(20)]): X[i, k] = row
        Fc = fch1 + foff * (b0 + n / 2)   # block centre, Hz
        Rn = []
        for i in range(6):
            med = np.median(X[i], 0); med[med == 0] = 1
            r = X[i] / med - 1.0; r = r + np.roll(r, 1, 1) + np.roll(r, -1, 1); Rn.append(r)
        def frame(dv):
            zs = []
            for i in range(6):
                v = np.interp(t[i], E[:, 0], E[:, 1]) + dv * (t[i] - T0) * 86400.0
                sh = np.rint(Fc * (v[0] - v) / C / foff).astype(int)
                acc = np.zeros(n)
                for k in range(20): acc += np.roll(Rn[i][k], -sh[k])
                m = np.median(acc); s = 1.4826 * np.median(np.abs(acc - m)); z = (acc - m) / s
                z[:CORE] = -99; z[-CORE:] = -99
                # align to scan 0's rest grid: channel of rest F at this scan's first sample vs scan 0's
                d = int(np.rint(Fc * (v0[0] - v[0]) / C / foff)) if i else 0
                zs.append(np.roll(z, -d) if d else z)
            mf = lambda a: np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
            Z = [mf(z) for z in zs]
            S = [Z[i] for i in range(6) if roles[i] == "S"]; Rr = [Z[i] for i in range(6) if roles[i] == "R"]
            def hits(A, B):
                ok = np.ones(n, bool)
                for z in A: ok &= z >= ZON
                for z in B: ok &= z < ZOFF
                return np.where(ok)[0]
            return hits(S, Rr), hits(Rr, S), Z
        cl = lambda ix: 0 if not len(ix) else 1 + int(np.sum(np.diff(np.sort(ix)) > 5))
        v0 = np.interp(t[0], E[:, 0], E[:, 1])
        p, q, Z = frame(0.0)
        cands = []
        if len(p):
            grp = np.split(np.sort(p), np.where(np.diff(np.sort(p)) > 5)[0] + 1)
            for g in grp:
                j = int(g[np.argmax(np.min([Z[i][g] for i in range(6) if roles[i] == "S"], 0))])
                cands.append({"chan": int(b0 + j), "f_topo0_MHz": round((fch1 + foff * (b0 + j)) / 1e6, 6),
                              "f_rest_MHz": round((fch1 + foff * (b0 + j)) / (1 - v0[0] / C) / 1e6, 6),
                              "z": {f"{roles[i]}{i}": round(float(Z[i][j]), 2) for i in range(6)}})
        false = []
        for dv in OFFS:
            fp, fq, _ = frame(v0[0] * 0 + dv)
            false.append([cl(fp), cl(fq)])
        state["blocks"][str(b0)] = {"f_lo_MHz": round(min(fch1 + foff * b0, fch1 + foff * (b0 + n)) / 1e6, 3), "true": cl(p), "swap": cl(q),
                                    "false": false, "cands": cands}
        json.dump(state, open(out_p + ".tmp", "w")); os.replace(out_p + ".tmp", out_p)
        print(node, b0, state["blocks"][str(b0)]["f_lo_MHz"], "true", cl(p), "swap", cl(q), "false mean %.2f" % np.mean([f[0] for f in false]), flush=True)
    B = state["blocks"].values()
    tot = sum(b["true"] for b in B); sw = sum(b["swap"] for b in B)
    fa = np.array([[sum(b["false"][k][0] for b in B), sum(b["false"][k][1] for b in B)] for k in range(len(OFFS))])
    state["summary"] = {"true": tot, "swap": sw, "false_mean": float(fa[:, 0].mean()), "false_sd": float(fa[:, 0].std()), "false_max": int(fa[:, 0].max()),
                        "false_minus_swap_max": int((fa[:, 0] - fa[:, 1]).max()), "lead": bool(tot > fa[:, 0].max() and (tot - sw) > (fa[:, 0] - fa[:, 1]).max())}
    json.dump(state, open(out_p, "w")); print(node, "SUMMARY", state["summary"], flush=True)

for nd in sys.argv[1:]:
    run(nd)
