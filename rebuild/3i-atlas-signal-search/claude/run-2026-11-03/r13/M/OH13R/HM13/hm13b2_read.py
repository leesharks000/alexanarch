"""PLAN-HM13-B2 reading.  python3 hm13b2_read.py -> b2.json   (or: python3 hm13b2_read.py selftest -> b2_selftest.json)"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
N = 1 << 20; TBIN = 3.41333333333333e-07; DF = 1 / TBIN / N; C = 299792.458; W = 1024; cc = 21
FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6
VALID = np.arange(41, 983)                         # tiles inside the central 92% of the channel
SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
def thresh(D): return [float(np.percentile(D["HC"][q][VALID], 99.9)) for q in range(2)]
def flags(D, th): return np.stack([D["HI"][q] > th[q] for q in range(2)])          # (2, 1024)
def tmhz(t): return round((FC - ((t + 0.5) * W - N // 2) * DF) / 1e6, 4)
if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    out = {}
    for tag in sorted(f[3:-4] for f in os.listdir(HERE) if f.startswith("b2_synth_") and f.endswith(".npz")):
        D = dict(np.load(os.path.join(HERE, f"b2_{tag}.npz"))); th = thresh(D); fl = flags(D, th)
        out[tag] = dict(theta=th, injected_tiles_HI=[[round(float(D["HI"][q][t]), 2) for t in (299, 300, 301)] for q in range(2)],
                        injected_flagged=bool(fl[:, 299:302].any()), n_flagged_valid_elsewhere=int(fl[:, VALID].sum() - fl[:, 299:302].sum()),
                        rI_tile300=[[round(float(x), 2) for x in D["rI"][q][300]] for q in range(2)])
    json.dump(out, open(os.path.join(HERE, "b2_selftest.json"), "w"), indent=1); print(json.dumps(out, indent=1)); sys.exit()
D = {s: dict(np.load(os.path.join(HERE, f"b2_{s}.npz"))) for s in SC}; TG = json.load(open(os.path.join(HERE, "targets_hm13b2.json")))["targets"]
TH = {s: thresh(D[s]) for s in SC}; FL = {s: flags(D[s], TH[s]) for s in SC}
out = dict(theta=TH, band={s: dict(n_flagged_X=int(FL[s][0][VALID].sum()), n_flagged_Y=int(FL[s][1][VALID].sum()),
                                   tiles=[dict(tile=int(t), mhz=tmhz(t), HI=[round(float(D[s]["HI"][q][t]), 2) for q in range(2)]) for t in VALID if FL[s][:, t].any()]) for s in SC})
# ON-specificity: each tile flagged in an ON scan, and where else it is flagged
anyon = sorted({int(t) for s in ON for t in VALID if FL[s][:, t].any()})
out["on_tiles"] = [dict(tile=t, mhz=tmhz(t), flagged_in=[s for s in SC if FL[s][:, t].any()]) for t in anyon]
out["summary"] = dict(on_flagged=len(anyon), on_flagged_also_in_an_off=sum(1 for x in out["on_tiles"] if any(s in OFF for s in x["flagged_in"])),
                      on_only=[x for x in out["on_tiles"] if not any(s in OFF for s in x["flagged_in"])])
# per target: the envelope answer in its own scan and the others; location as PLAN-C4850 (fixed bin and comet track)
v0 = {s: float(D[s]["v0"]) for s in SC}
dshift = lambda a, b: int(np.rint(FC * (v0[b] - v0[a]) / C / DF))
def excess(S, b, w=128, h=10):
    if b - w < 0 or b + w > S.shape[-1]: return np.nan
    seg = S[:, b - w:b + w].sum(0); m = np.median(seg); return float((seg[w - h:w + h + 1] - m).clip(0).sum() / m)
rng = np.random.default_rng(1); RB = rng.integers(int(N * .05), int(N * .95), 400)
noise = {s: dict(S=float(np.percentile([excess(D[s]["S"], b) for b in RB], 95)), Sc=float(np.percentile([excess(D[s]["Sc"], b) for b in RB], 95))) for s in SC}
TT = []
for t in TG:
    s0, b = t["scan"], t["bin"]
    env = {s: dict(flag=bool(FL[s][:, t["tiles"]].any()), HI_over_theta=round(max(float(D[s]["HI"][q][x]) / TH[s][q] for q in range(2) for x in t["tiles"]), 3)) for s in SC}
    fx = {s: excess(D[s]["S"], b) for s in SC}; cm = {s: excess(D[s]["Sc"], b + dshift(s0, s)) for s in SC}; on = max(fx[s0], cm[s0])
    quiet = lambda tr, key: all(tr[s] <= max(0.01 * on, noise[s][key]) for s in OFF)
    lead = bool(s0 in ON and quiet(fx, "S") and quiet(cm, "Sc") and on > 2 * noise[s0]["S"])
    TT.append(dict(kind=t["kind"], cls=t["cls"], scan=s0, mhz=round(t["f"] / 1e6, 6), z=t["z"], hz_per_s=t["hz_per_s"], tiles=t["tiles"],
                   carries_11_11_in_own_scan=env[s0]["flag"], envelope=env,
                   location=dict(fixed={s: round(v, 2) for s, v in fx.items()}, comet={s: round(v, 2) for s, v in cm.items()},
                                 off_over_on_fixed=round(max(fx[s] for s in OFF) / fx[s0], 3) if fx[s0] > 0 else None, lead=lead)))
out["targets"] = TT
out["summary"].update(events_E=sum(1 for x in TT if x["kind"] == "E"), E_carrying=sum(1 for x in TT if x["kind"] == "E" and x["carries_11_11_in_own_scan"]),
                      classA=[{k: x[k] for k in ("scan", "mhz", "hz_per_s", "carries_11_11_in_own_scan")} for x in TT if x["cls"] == "A"],
                      Q_carrying=sum(1 for x in TT if x["kind"] == "Q" and x["carries_11_11_in_own_scan"]), leads=[x for x in TT if x["location"]["lead"]])
json.dump(out, open(os.path.join(HERE, "b2.json"), "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out["summary"].items() if k != "on_only"}, indent=1)); print("on_only", len(out["summary"]["on_only"]))
