"""EA-SEI-RCS-SIM-01 v2 — density-detector co-evolution.
Tests the Sharks hypothesis: (1) what counts as 'human' narrows — natural drafts find it
harder to score 100% human; (2) transient tailsification of measured prose (performed
burstiness) while (3) latent 'thought' dims homogenize undetected; (4) archival human
text is retroactively reclassified as the human class-density tightens."""
import numpy as np
rng = np.random.default_rng(20260824)
D_OBS, D_LAT = 12, 12; D = 24; K = 4
N_AUTH, N_AI, N_HUM = 400, 400, 250
T = 16
TH_PASS, TH_TGT = 0.90, 0.97
DOC_N = 0.35; A_BUDGET, H_BUDGET = 2.5, 5.0
LAM = 0.15; EVADE = 0.75
AI0 = np.zeros(D); AI0[0:4] = -1.6   # gen-0 AI: low burstiness/perplexity family
AI_STD0 = 0.40; ETA_AI = 0.35        # AI generator drifts toward certified corpus

def fit(hum, ai):
    mh, ma = hum.mean(0), ai.mean(0)
    vh = hum.var(0) + 1e-3; va = ai.var(0) + 1e-3
    d = (mh - ma)**2 / (vh + va) + 0.5*(vh/va + va/vh - 2)   # symm. separability
    feats = np.argsort(d[:D_OBS])[::-1][:K]
    return {"f": feats, "mh": mh[feats], "vh": vh[feats], "ma": ma[feats], "va": va[feats]}

def ph(det, X):
    xf = X[:, det["f"]]
    lh = -0.5*(((xf-det["mh"])**2)/det["vh"] + np.log(det["vh"])).sum(1)
    la = -0.5*(((xf-det["ma"])**2)/det["va"] + np.log(det["va"])).sum(1)
    return 1/(1+np.exp(-np.clip(lh-la, -60, 60)))

def optimize(det, X, budget, tgt):
    X = X.copy(); used = np.zeros(len(X)); st = 0.12
    for _ in range(int(budget/st)+1):
        p = ph(det, X); need = (p < tgt) & (used < budget)
        if not need.any(): break
        xf = X[np.ix_(np.where(need)[0], det["f"])]
        g = -(xf-det["mh"])/det["vh"] + (xf-det["ma"])/det["va"]   # grad log(pH/pA)
        g /= (np.linalg.norm(g, axis=1, keepdims=True) + 1e-12)
        X[np.ix_(np.where(need)[0], det["f"])] = xf + st*g
        used[need] += st
    return X, ph(det, X), used

def run(regime, seed=7):
    r = np.random.default_rng(seed)
    sty = r.normal(0, 1, (N_AUTH, D))
    arch = r.normal(0, 1, (2000, D)) + r.normal(0, DOC_N, (2000, D))
    tail = r.normal(0, 1, (1000, D))*2.2 + r.normal(0, DOC_N, (1000, D))
    mu_ai = AI0.copy(); sd_ai = np.full(D, AI_STD0)
    det = fit(arch, r.normal(0,1,(2000,D))*sd_ai + mu_ai)
    f0 = set(det["f"].tolist())
    M = {k: [] for k in "nat_pass effort burst_mean obsvar_meas latvar_sty latvar_acc fp_arch tail_pass feat_ov withheld humpass".split()}
    for t in range(T):
        drafts = sty + r.normal(0, DOC_N, (N_AUTH, D))
        M["nat_pass"].append(float((ph(det, drafts) >= TH_PASS).mean()))
        if regime == "full":
            rev, p, used = optimize(det, drafts, A_BUDGET, TH_TGT)
            ok = p >= TH_PASS
            acc = rev[ok]; M["effort"].append(float(used[ok].mean() if ok.any() else A_BUDGET))
            M["withheld"].append(float(1-ok.mean()))
        else:
            acc = drafts; M["effort"].append(0.0); M["withheld"].append(0.0)
        ai_raw = r.normal(0,1,(N_AI,D))*sd_ai + mu_ai
        hopt, hp, _ = optimize(det, r.normal(0,1,(N_HUM,D))*sd_ai + mu_ai, H_BUDGET, TH_TGT)
        hok = hp >= TH_PASS; M["humpass"].append(float(hok.mean()))
        ev = r.random(hok.sum()) < EVADE
        presumed = np.vstack([acc, hopt[hok][ev]]) if (regime=="full" and ev.any()) else acc
        if regime == "full":
            ex = presumed[r.integers(0, len(presumed), N_AUTH)]
            sty = (1-LAM)*sty + LAM*ex
        M["burst_mean"].append(float(presumed[:, 0:4].mean()))
        M["obsvar_meas"].append(float(presumed[:, det["f"]].var(0).mean()))
        M["latvar_sty"].append(float(sty[:, D_OBS:].var(0).mean()))
        M["latvar_acc"].append(float(presumed[:, D_OBS:].var(0).mean()))
        M["fp_arch"].append(float((ph(det, arch) < 0.5).mean()))
        M["tail_pass"].append(float((ph(det, tail) >= TH_PASS).mean()))
        M["feat_ov"].append(len(f0 & set(det["f"].tolist()))/K)
        if regime in ("full", "advisory"):
            mu_ai = mu_ai + ETA_AI*(presumed.mean(0) - mu_ai)          # AI trains on certified text
            sd_ai = np.sqrt(sd_ai**2 + ETA_AI*(presumed.var(0) - sd_ai**2).clip(-.5,.5))
            caught = hopt[hok][~ev]
            ai_pool = np.vstack([ai_raw, caught]) if len(caught) else ai_raw
            det = fit(presumed, ai_pool)
    return M

res = {n: run(n) for n in ["full", "advisory", "no_regime"]}
import json
np.save("sim2_results.npy", res, allow_pickle=True)
for n, M in res.items():
    print(f"=== {n} ===")
    for k in ["nat_pass","effort","burst_mean","obsvar_meas","latvar_sty","fp_arch","tail_pass","feat_ov","withheld","humpass"]:
        v = M[k]; print(f"{k:12s} " + " ".join(f"{x:6.3f}" for x in v[::2]))
