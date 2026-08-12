#!/usr/bin/env python3
"""SEI Inversion Battery v0.2 — multi-seed Protocol I with CIs, a fourth score
family, a measured complexity axis, and deployment-transformation tests.

PRE-REGISTRATION (fixed before any v0.2 training; this header is the
registration; deviations are recorded in results-v0.2.json under 'deviations').

WHAT v0.2 ADDS TO v0.1 (#1449 · AXN:05DA.EMPIRICAL.🛤️🌠🗿🖊️🧭🪞)
  R1  Multi-seed: S = 5 seeds {0,1,2,3,4} per (pair, architecture, direction).
      Reported as mean and 95% bootstrap CI (10,000 resamples over seeds and
      evaluation sets, percentile method). The v0.1 point values become the
      seed-0 members of these distributions.
  R2  Fourth score family: NAE — a normalized autoencoder trained with an
      energy-based normalization term, the symmetric-by-design remedy of
      Dillon et al. (SciPost Phys. Core 6 (2023) 74). Registered prediction:
      if the remedy works, NAE shows the smallest |IAI| of the four families.
  R3  LCBH axis: representation complexity measured, not assumed. For each
      class we compute C = (participation ratio of the PCA spectrum fitted on
      the pooled representation) and Ĉ = mean per-event zlib-compressed length
      of the quantized feature vector. Classes are ordered by measured C; the
      LCBH prediction is that a P-trained system assimilates a Q with C_Q <
      C_P more than a Q with C_Q > C_P at equal representational separation.
  R4  Distillation rank-survival (CICADA-class): the AE teacher's scores are
      distilled into a small student (in-32-16-1 regression on teacher score),
      then the student is quantized to 8-bit fixed point. We report Spearman
      rank correlation teacher-vs-student and teacher-vs-quantized student on
      background, and — the estimand that matters — the fraction of the
      teacher's top-α anomalous set that survives into the student's top-α set
      (rank survival at the operating point), and the same after quantization.
  R5  Battery retention map: the battery is itself a selection pipeline, so its
      own per-stage retention is recorded (events entering, surviving each
      preprocessing stage, entering evaluation) per the isomorphism discipline
      of #932 §7.4.
  R6  RII: for each pair and α, miss-overlap between architectures on the
      withheld class — q_A, q_B, q_AB, Δ_miss = q_AB − q_A·q_B, per #1450.

UNCHANGED FROM v0.1 (so the comparison is a comparison)
  Pairs, representations, split sizes, threshold procedure, α ∈ {1e-2, 1e-3},
  the AE/VAE/GMM definitions, and the estimand definitions.

DECLARED COMPUTE BOUND (MANUS decision, 2026-08-11: ship CPU-scale with the
bound declared rather than wait for GPU): all training is single-thread CPU,
1 core, 3 GB RAM. Consequences, registered in advance: network sizes and epoch
counts are those of v0.1 (no scaling up), the GMM on the 120-dim constituent
representation runs diagonal covariance (as in v0.1), and the panel is the
v0.1 panel plus NAE rather than an expanded pair set. v0.2 therefore
quantifies VARIANCE and tests the REMEDY at v0.1 scale; it does not raise
scale. A GPU pass remains a separate, later run.

INTERPRETATION LIMITS (carried forward unchanged from v0.1)
  - Demonstration-scale surrogates, not deployed systems. Nothing here
    measures AXOL1TL, CICADA, or GELATO.
  - IAI and cross-acceptance quantify direction-dependence on these pairs at
    these operating points. They neither upper- nor lower-bound any open-world
    Ontological Assimilation Rate (the no-bounds discipline of #931 §3.2).
  - Rank survival measures the distillation transformation only; it says
    nothing about the teacher's own correctness.
"""
import os, json, time, sys, zlib
import numpy as np, h5py, hdf5plugin
import torch, torch.nn as nn

torch.set_num_threads(1)
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
OUT = os.path.join(HERE, 'results')
os.makedirs(OUT, exist_ok=True)
ALPHAS = [1e-2, 1e-3]
SEEDS = [0, 1, 2, 3, 4]
RETENTION = {}   # R5

sys.path.insert(0, HERE)
from battery import load_top, load_lhco, top_features, lhco_features, AE, VAE, make_mlp


# ---------------- R2: NAE (normalized autoencoder) ----------------
class NAE(nn.Module):
    """Autoencoder trained with an energy-normalization term. The AE's energy is
    the reconstruction error; the normalization penalizes low energy on
    negative samples drawn by perturbing the data, which is the mechanism by
    which NAE is intended to remove the complexity bias of a plain AE."""
    def __init__(self, d):
        super().__init__()
        self.enc = make_mlp([d, 96, 48, 8])
        self.dec = make_mlp([8, 48, 96, d])
    def energy(self, x):
        return ((self.dec(self.enc(x)) - x) ** 2).mean(1)


def train_nae(model, X, epochs=12, sigma=0.3, lam=1.0, seed=0):
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    X = torch.tensor(X)
    n = len(X)
    for ep in range(epochs):
        perm = torch.randperm(n, generator=g)
        for i in range(0, n, 512):
            xb = X[perm[i:i + 512]]
            neg = xb + sigma * torch.randn(xb.shape, generator=g)
            opt.zero_grad()
            e_pos = model.energy(xb).mean()
            e_neg = model.energy(neg).mean()
            # positive energy down, negative energy up (bounded), = normalization
            loss = e_pos + lam * torch.relu(1.0 - e_neg / (e_pos.detach() + 1e-8))
            loss.backward()
            opt.step()
    return model


# ---------------- systems ----------------
def train_net(model, X, epochs=12, beta=0.5, seed=0):
    g = torch.Generator().manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    X = torch.tensor(X); n = len(X)
    for ep in range(epochs):
        perm = torch.randperm(n, generator=g)
        for i in range(0, n, 512):
            xb = X[perm[i:i + 512]]
            opt.zero_grad()
            if isinstance(model, VAE):
                xh, mu, lv = model(xb)
                rec = ((xh - xb) ** 2).mean()
                kl = (-0.5 * (1 + lv - mu ** 2 - lv.exp()).mean())
                loss = rec + beta * kl
            else:
                loss = ((model(xb) - xb) ** 2).mean()
            loss.backward(); opt.step()
    return model


def fit_system(arch, Xtr, seed):
    torch.manual_seed(seed)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    Z = (Xtr - mu) / sd
    d = Z.shape[1]
    if arch == 'AE':
        m = train_net(AE(d), Z, seed=seed)
    elif arch == 'VAE':
        m = train_net(VAE(d), Z, seed=seed)
    elif arch == 'NAE':
        m = train_nae(NAE(d), Z, seed=seed)
    elif arch == 'GMM':
        from sklearn.mixture import GaussianMixture
        cov = 'diag' if d > 20 else 'full'
        m = GaussianMixture(20, covariance_type=cov, random_state=seed,
                            reg_covar=1e-4, max_iter=100).fit(Z)
    return {'arch': arch, 'm': m, 'mu': mu, 'sd': sd}


def system_score(sysd, X):
    Z = torch.tensor((X - sysd['mu']) / sysd['sd'])
    a, m = sysd['arch'], sysd['m']
    with torch.no_grad():
        if a == 'AE':
            return ((m(Z) - Z) ** 2).mean(1).numpy()
        if a == 'NAE':
            return m.energy(Z).numpy()
        if a == 'VAE':
            h = torch.relu(m.body(Z)); return (m.mu(h) ** 2).sum(1).numpy()
    return -m.score_samples(Z.numpy())


# ---------------- R3: measured complexity ----------------
def complexity(X):
    """Two registered measures. PR = participation ratio of the PCA spectrum
    (effective dimensionality); ZL = mean zlib length of the 8-bit quantized
    feature vector (algorithmic proxy). Both computed on a fixed 5k subsample."""
    Z = X[:5000]
    Zc = Z - Z.mean(0)
    ev = np.linalg.svd(Zc, compute_uv=False) ** 2
    ev = ev / ev.sum()
    pr = float(1.0 / (ev ** 2).sum())
    lo, hi = np.percentile(Z, 1, axis=0), np.percentile(Z, 99, axis=0)
    q = np.clip(np.round((Z - lo) / (hi - lo + 1e-9) * 255), 0, 255).astype(np.uint8)
    zl = float(np.mean([len(zlib.compress(r.tobytes(), 6)) for r in q[:1000]]))
    return {'participation_ratio': round(pr, 3), 'zlib_len': round(zl, 2)}


# ---------------- R4: distillation rank survival ----------------
def distill(teacher_sys, Xtr, Xev, alpha, seed):
    torch.manual_seed(seed)
    Ztr = torch.tensor((Xtr - teacher_sys['mu']) / teacher_sys['sd'])
    y = torch.tensor(system_score(teacher_sys, Xtr)).float().unsqueeze(1)
    ym, ys = y.mean(), y.std() + 1e-8
    student = nn.Sequential(nn.Linear(Ztr.shape[1], 32), nn.ReLU(),
                            nn.Linear(32, 16), nn.ReLU(), nn.Linear(16, 1))
    opt = torch.optim.Adam(student.parameters(), lr=1e-3)
    g = torch.Generator().manual_seed(seed)
    for ep in range(15):
        perm = torch.randperm(len(Ztr), generator=g)
        for i in range(0, len(Ztr), 512):
            idx = perm[i:i + 512]
            opt.zero_grad()
            loss = ((student(Ztr[idx]) - (y[idx] - ym) / ys) ** 2).mean()
            loss.backward(); opt.step()
    Zev = torch.tensor((Xev - teacher_sys['mu']) / teacher_sys['sd'])
    with torch.no_grad():
        s_t = system_score(teacher_sys, Xev)
        s_s = student(Zev).squeeze(1).numpy()
        # 8-bit fixed-point quantization of weights (CICADA-class deployment step)
        qstudent = nn.Sequential(*[nn.Linear(l.in_features, l.out_features) if isinstance(l, nn.Linear) else nn.ReLU()
                                   for l in student])
        with torch.no_grad():
            for lq, l in zip(qstudent, student):
                if isinstance(l, nn.Linear):
                    for p_, q_ in ((l.weight, lq.weight), (l.bias, lq.bias)):
                        scale = p_.abs().max() / 127.0
                        q_.copy_(torch.round(p_ / scale) * scale)
        s_q = qstudent(Zev).squeeze(1).numpy()
    from scipy.stats import spearmanr
    k = max(1, int(round(alpha * len(s_t))))
    top = lambda s: set(np.argsort(-s)[:k].tolist())
    T, S, Q = top(s_t), top(s_s), top(s_q)
    return {'spearman_student': round(float(spearmanr(s_t, s_s).statistic), 4),
            'spearman_quantized': round(float(spearmanr(s_t, s_q).statistic), 4),
            'rank_survival_student': round(len(T & S) / k, 4),
            'rank_survival_quantized': round(len(T & Q) / k, 4), 'k': k}


# ---------------- estimands ----------------
def split3(X, ntr, ncal, nev, seed):
    r = np.random.default_rng(1000 + seed)
    idx = r.permutation(len(X))
    return X[idx[:ntr]], X[idx[ntr:ntr + ncal]], X[idx[ntr + ncal:ntr + ncal + nev]]


def auc(neg, pos):
    s = np.concatenate([neg, pos]); y = np.concatenate([np.zeros(len(neg)), np.ones(len(pos))])
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    n1, n0 = y.sum(), len(y) - y.sum()
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def boot_ci(vals, B=10000, seed=0):
    v = np.asarray(vals, float)
    if len(v) < 2: return [round(float(v[0]), 4)] * 2
    r = np.random.default_rng(seed)
    m = r.choice(v, size=(B, len(v)), replace=True).mean(1)
    return [round(float(np.percentile(m, 2.5)), 4), round(float(np.percentile(m, 97.5)), 4)]


def run_cell(P, Q, arch, sizes, seed):
    ntr, ncal, nev = sizes
    Ptr, Pcal, Pev = split3(P, ntr, ncal, nev, seed)
    Qtr, Qcal, Qev = split3(Q, ntr, ncal, nev, seed)
    sysP, sysQ = fit_system(arch, Ptr, seed), fit_system(arch, Qtr, seed)
    sPP, sPQ = system_score(sysP, Pcal), system_score(sysP, Qev)
    sQQ, sQP = system_score(sysQ, Qcal), system_score(sysQ, Pev)
    sPPev = system_score(sysP, Pev)
    out = {'auc_P_on_Q': round(auc(sPPev, sPQ), 4), 'auc_Q_on_P': round(auc(system_score(sysQ, Qev), sQP), 4)}
    miss = {}
    for a in ALPHAS:
        tP, tQ = np.quantile(sPP, 1 - a), np.quantile(sQQ, 1 - a)
        aPQ = float(np.mean(sPQ <= tP)); aQP = float(np.mean(sQP <= tQ))
        out['assim_Q_by_P@%g' % a] = round(aPQ, 4)
        out['assim_P_by_Q@%g' % a] = round(aQP, 4)
        out['IAI@%g' % a] = round(abs(aPQ - aQP), 4)
        miss['%g' % a] = (sPQ <= tP)          # per-event miss mask for RII
    return out, miss, (sysP, Ptr, Qev)


def main(pairs_arg, arch_arg):
    t0 = time.time()
    res_path = os.path.join(OUT, 'results-v0.2.json')
    R = json.load(open(res_path)) if os.path.exists(res_path) else {
        'battery': 'EA-SEI-BATTERY-01 v0.2', 'date': '2026-08-11',
        'seeds': SEEDS, 'alphas': ALPHAS, 'compute': 'CPU 1 core / 3 GB, declared bound',
        'cells': {}, 'complexity': {}, 'distillation': {}, 'rii': {}, 'retention_map': {},
        'deviations': []}
    top = load_top('val.h5', 100000)
    RETENTION['top_loaded'] = {0: int(len(top[0])), 1: int(len(top[1]))}
    L = load_lhco()
    RETENTION['lhco_loaded'] = {k: int(len(v)) for k, v in L.items()}
    PAIRS = {'T1': (top[0], top[1], (60000, 20000, 20000)),
             'L1': (L['bkg'], L['sig2'], (60000, 20000, 20000)),
             'L2': (L['bkg'], L['sig3'], (60000, 20000, 20000)),
             'L3': (L['sig2'], L['sig3'], (50000, 20000, 20000))}
    if not R['complexity']:
        R['complexity'] = {'T1_qcd': complexity(top[0]), 'T1_top': complexity(top[1]),
                           'L_bkg': complexity(L['bkg']), 'L_2prong': complexity(L['sig2']),
                           'L_3prong': complexity(L['sig3'])}
    for pname in pairs_arg.split(','):
        P, Q, sizes = PAIRS[pname]
        for arch in arch_arg.split(','):
            key = '%s|%s' % (pname, arch)
            if key in R['cells']: continue
            per_seed = []
            masks = {}
            for s in SEEDS:
                o, miss, aux = run_cell(P, Q, arch, sizes, s)
                per_seed.append(o)
                if s == 0:
                    masks = {a: m.tolist() for a, m in miss.items()}
                    if arch == 'AE':
                        Ptr = split3(P, *sizes, 0)[0]; Qev = split3(Q, *sizes, 0)[2]
                        R['distillation'][pname] = distill(fit_system('AE', Ptr, 0), Ptr, Qev, 1e-2, 0)
            agg = {}
            for k in per_seed[0]:
                vals = [d[k] for d in per_seed]
                agg[k] = {'mean': round(float(np.mean(vals)), 4), 'ci95': boot_ci(vals),
                          'seed_values': vals}
            R['cells'][key] = agg
            np.save(os.path.join(OUT, 'miss_%s_%s.npy' % (pname, arch)),
                    np.array(masks.get('0.01', []), dtype=bool))
            print('%-10s done  IAI@1e-2 %.3f %s  (%.0fs)' % (
                key, agg['IAI@0.01']['mean'], agg['IAI@0.01']['ci95'], time.time() - t0), flush=True)
            json.dump(R, open(res_path, 'w'), indent=1)
    R['retention_map'].update(RETENTION)
    json.dump(R, open(res_path, 'w'), indent=1)
    print('elapsed %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'T1,L1,L2,L3',
         sys.argv[2] if len(sys.argv) > 2 else 'AE,VAE,GMM,NAE')
