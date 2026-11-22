"""PLAN-HM7 'Descriptive, no rule': the 2 kHz strips of G1667 and their controls, each IF, S against R.
Per window and IF: centre channel over the strip's median, averaged over seconds; z of (S mean - R mean) against the
window's own controls."""
import json, numpy as np, hm7
W = hm7.windows(); out = {}
for sname, S in hm7.SESSIONS.items():
    sel = [i for i, w in enumerate(W) if w[3] in hm7.G1667]
    names = [W[i][0] for i in sel]
    def stat(stem):
        f = np.load(f"hm7_{sname}_{stem.split('_')[2]}.npz"); B = f["B"]          # [nsel, nsec, nif, 21]
        r = B[:, :, :, 10] / np.median(B, axis=3); return r.mean(1)             # [nsel, nif]
    on = np.mean([stat(p[0]) for p in S["pairs"]], 0); off = np.mean([stat(p[1]) for p in S["pairs"]], 0)
    d = on - off; res = {}
    for c in hm7.G1667:
        ci = names.index(c); ctl = [k for k, n in enumerate(names) if W[sel[k]][3] == c and n != c]
        mu, sd = d[ctl].mean(0), d[ctl].std(0, ddof=1)
        res[c] = {f"IF{p}": dict(S_minus_R=round(float(d[ci, p]), 5), z_vs_controls=round(float((d[ci, p] - mu[p]) / sd[p]), 2)) for p in range(d.shape[1])}
    out[sname] = res
json.dump(out, open("hm7_describe_2khz.json", "w"), indent=1)
for s, r in out.items():
    print(s); [print(" ", c, {k: v["z_vs_controls"] for k, v in x.items()}) for c, x in r.items()]
