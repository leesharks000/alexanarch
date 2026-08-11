#!/usr/bin/env python3
"""SEI Inversion Battery v0.1 — demonstration-scale Protocol I
(06.SEI.OAR_PROTOCOL v0.3 §4.1.1, executed on public datasets).

PRE-REGISTRATION (fixed before any training; this header is the registration):

Pairs (P, Q):
  T1  (QCD jets, top jets)          — Kasieczka et al. top-tagging reference
                                       dataset (10.5281/zenodo.2603256);
                                       constituents of val.h5 (train pool),
                                       test.h5 (evaluation pool).
  L1  (QCD dijet, W'->XY 2-prong)   — LHCO2020 R&D (10.5281/zenodo.6466204),
  L2  (QCD dijet, Z->XY  3-prong)     high-level feature files.
  L3  (2-prong signal, 3-prong signal)

Representations:
  Top-tagging: leading 40 constituents by pT; per-jet features
     (pT_i / sum pT, eta_i - eta_jetaxis(pT-weighted), dphi_i wrapped),
     flattened to 120 dims, zero-padded.
  LHCO: 7 standard AD features: mjj, min(mj1,mj2), |mj1-mj2|,
     tau21 of each jet, tau32 of each jet.

Architectures (score families mirroring the deployed taxonomy):
  AE   — dense reconstruction autoencoder (in-96-48-8-48-96-in), score = MSE.
         (reconstruction-loss family; CICADA-teacher-class)
  VAE  — same encoder shape, latent d_z = 8, deployed score = sum_i mu_i^2.
         (encoder-side latent-prior family; AXOL1TL-class, incl. d_z = 8)
  GMM  — 20-component full-covariance Gaussian mixture, score = -log p.
         (density family; comparison literature, not a deployed L1 system)

Procedure per (pair, architecture):
  train s_P on P-train and s_Q on Q-train (identical hyperparameters,
  identical seeds); per-system standardization fit on own training
  distribution (the scaler is part of the pipeline and is conditioned like
  everything else); thresholds tau_P, tau_Q calibrated separately on each
  system's own HELD-OUT background to accepted-background rates
  alpha in {1e-2, 1e-3}; measure directional cross-acceptance
     A(P->Q) = P_{X~Q}[ s_P(X) <= tau_P ]   (assimilation of Q by P-system)
     A(Q->P) = P_{X~P}[ s_Q(X) <= tau_Q ]
  IAI(alpha) = | A(P->Q) - A(Q->P) |.
  AUCs both directions reported for orientation only.

Sample sizes: 60k train / 20k threshold-calibration / 20k evaluation per
class where available (3-prong signal: 50k/20k/20k within its 100k).

Interpretation limits (registered in advance, per the protocol):
  - These are demonstration-scale surrogates of the deployed systems, not
    the deployed systems. Nothing here measures AXOL1TL/CICADA/GELATO.
  - IAI and cross-acceptance quantify direction-dependence of the score
    families on these pairs at these operating points. They neither
    upper- nor lower-bound any open-world OAR.
  - Seeds fixed (0); single-seed results; variance unquantified at v0.1.
"""
import os, json, time, math
import numpy as np, h5py, hdf5plugin

RNG = np.random.default_rng(0)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(OUT, exist_ok=True)
ALPHAS = [1e-2, 1e-3]

# ---------------- data loading ----------------

def load_top(split, n_per_class):
    """Return dict class->features (n,120) from top-tagging file."""
    f = h5py.File(os.path.join(DATA, split), 'r')
    t = f['table/table']
    # stream in chunks; collect until n_per_class of each label
    want = {0: [], 1: []}
    CH = 20000
    for i in range(0, t.shape[0], CH):
        rows = t[i:i+CH]
        y = rows['values_block_1'][:, 1]
        x = rows['values_block_0'][:, :800].astype(np.float32)
        for lab in (0, 1):
            need = n_per_class - sum(len(a) for a in want[lab])
            if need > 0:
                sel = x[y == lab][:need]
                if len(sel):
                    want[lab].append(sel)
        if all(sum(len(a) for a in want[l]) >= n_per_class for l in (0, 1)):
            break
    f.close()
    out = {}
    for lab in (0, 1):
        raw = np.concatenate(want[lab])[:n_per_class]
        out[lab] = top_features(raw)
    return out


def top_features(raw):
    """(n,800) E,px,py,pz x200 -> leading-40 (pTfrac, deta, dphi) = (n,120)."""
    n = raw.shape[0]
    v = raw.reshape(n, 200, 4)
    E, px, py, pz = v[..., 0], v[..., 1], v[..., 2], v[..., 3]
    pt = np.hypot(px, py)
    # protect zeros
    p = np.sqrt(px**2 + py**2 + pz**2)
    eta = np.zeros_like(pt); phi = np.zeros_like(pt)
    m = pt > 0
    eta[m] = np.arctanh(np.clip(pz[m] / np.maximum(p[m], 1e-8), -0.9999999, 0.9999999))
    phi[m] = np.arctan2(py[m], px[m])
    order = np.argsort(-pt, axis=1)[:, :40]
    idx = np.arange(n)[:, None]
    pt40, eta40, phi40 = pt[idx, order], eta[idx, order], phi[idx, order]
    sumpt = pt40.sum(1, keepdims=True) + 1e-8
    w = pt40 / sumpt
    etax = (w * eta40).sum(1, keepdims=True)
    # pT-weighted circular mean for phi axis
    cs = (w * np.cos(phi40)).sum(1, keepdims=True)
    sn = (w * np.sin(phi40)).sum(1, keepdims=True)
    phix = np.arctan2(sn, cs)
    dphi = np.mod(phi40 - phix + np.pi, 2 * np.pi) - np.pi
    deta = eta40 - etax
    mask = pt40 > 0
    feats = np.stack([w * mask, deta * mask, dphi * mask], axis=2)  # (n,40,3)
    return feats.reshape(n, 120).astype(np.float32)


def load_lhco():
    """Return dict: 'bkg','sig2','sig3' -> (n,7) engineered features."""
    f = h5py.File(os.path.join(DATA, 'lhco_features.h5'), 'r')
    X = f['df/block0_values'][:]
    f.close()
    lab = X[:, 14]
    feats = lhco_features(X[:, :14])
    g = h5py.File(os.path.join(DATA, 'lhco_3prong_features.h5'), 'r')
    X3 = g['df/block0_values'][:].astype(np.float64)
    g.close()
    return {'bkg': feats[lab == 0], 'sig2': feats[lab == 1],
            'sig3': lhco_features(X3)}


def lhco_features(X):
    px1, py1, pz1, mj1 = X[:, 0], X[:, 1], X[:, 2], X[:, 3]
    t11, t21, t31 = X[:, 4], X[:, 5], X[:, 6]
    px2, py2, pz2, mj2 = X[:, 7], X[:, 8], X[:, 9], X[:, 10]
    t12, t22, t32 = X[:, 11], X[:, 12], X[:, 13]
    E1 = np.sqrt(px1**2 + py1**2 + pz1**2 + np.maximum(mj1, 0)**2)
    E2 = np.sqrt(px2**2 + py2**2 + pz2**2 + np.maximum(mj2, 0)**2)
    mjj2 = (E1 + E2)**2 - (px1 + px2)**2 - (py1 + py2)**2 - (pz1 + pz2)**2
    mjj = np.sqrt(np.maximum(mjj2, 0))
    tau21a = t21 / np.maximum(t11, 1e-8)
    tau32a = t31 / np.maximum(t21, 1e-8)
    tau21b = t22 / np.maximum(t12, 1e-8)
    tau32b = t32 / np.maximum(t22, 1e-8)
    mmin = np.minimum(mj1, mj2)
    mdiff = np.abs(mj1 - mj2)
    F = np.stack([mjj, mmin, mdiff, tau21a, tau21b, tau32a, tau32b], 1)
    return F.astype(np.float32)

# ---------------- models ----------------
import torch, torch.nn as nn
torch.manual_seed(0)
torch.set_num_threads(1)


def make_mlp(dims):
    layers = []
    for a, b in zip(dims[:-1], dims[1:]):
        layers += [nn.Linear(a, b), nn.ReLU()]
    return nn.Sequential(*layers[:-1])


class AE(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.enc = make_mlp([d, 96, 48, 8])
        self.dec = make_mlp([8, 48, 96, d])
    def forward(self, x):
        return self.dec(self.enc(x))


class VAE(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.body = make_mlp([d, 96, 48])
        self.mu = nn.Linear(48, 8)
        self.lv = nn.Linear(48, 8)
        self.dec = make_mlp([8, 48, 96, d])
    def forward(self, x):
        h = torch.relu(self.body(x))
        mu, lv = self.mu(h), self.lv(h)
        z = mu + torch.exp(0.5 * lv) * torch.randn_like(mu)
        return self.dec(z), mu, lv


def train_net(model, X, epochs=12, beta=0.5):
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    X = torch.tensor(X)
    n = len(X)
    for ep in range(epochs):
        perm = torch.randperm(n)
        for i in range(0, n, 512):
            xb = X[perm[i:i+512]]
            opt.zero_grad()
            if isinstance(model, VAE):
                xh, mu, lv = model(xb)
                rec = ((xh - xb)**2).mean()
                kld = (-0.5 * (1 + lv - mu**2 - lv.exp()).sum(1)).mean()
                loss = rec + beta * kld / xb.shape[1]
            else:
                loss = ((model(xb) - xb)**2).mean()
            loss.backward(); opt.step()
    return model


def score(model, kind, X):
    X = torch.tensor(X)
    out = []
    with torch.no_grad():
        for i in range(0, len(X), 4096):
            xb = X[i:i+4096]
            if kind == 'VAE':
                h = torch.relu(model.body(xb))
                mu = model.mu(h)
                out.append((mu**2).sum(1))          # AXOL1TL-class score
            else:
                out.append(((model(xb) - xb)**2).mean(1))  # MSE
    return torch.cat(out).numpy()

from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score


def fit_system(arch, Xtr):
    sc = StandardScaler().fit(Xtr)
    Z = sc.transform(Xtr).astype(np.float32)
    if arch == 'GMM':
        m = GaussianMixture(20, covariance_type='full', random_state=0,
                            reg_covar=1e-4, max_iter=100).fit(Z)
        return ('GMM', sc, m)
    net = AE(Z.shape[1]) if arch == 'AE' else VAE(Z.shape[1])
    train_net(net, Z)
    net.eval()
    return (arch, sc, net)


def system_score(sys_, X):
    arch, sc, m = sys_
    Z = sc.transform(X).astype(np.float32)
    if arch == 'GMM':
        return -m.score_samples(Z)
    return score(m, arch, Z)

# ---------------- battery ----------------

def split3(X, ntr, ncal, nev):
    idx = RNG.permutation(len(X))
    return X[idx[:ntr]], X[idx[ntr:ntr+ncal]], X[idx[ntr+ncal:ntr+ncal+nev]]


def run_pair(name, P, Q, sizes, results):
    (ptr, pcal, pev) = split3(P, *sizes)
    (qtr, qcal, qev) = split3(Q, *sizes)
    for arch in ('AE', 'VAE', 'GMM'):
        t0 = time.time()
        sP = fit_system(arch, ptr)
        sQ = fit_system(arch, qtr)
        # thresholds on own held-out background
        cP = system_score(sP, pcal)
        cQ = system_score(sQ, qcal)
        # eval scores
        sP_on_Q = system_score(sP, qev); sP_on_P = system_score(sP, pev)
        sQ_on_P = system_score(sQ, pev); sQ_on_Q = system_score(sQ, qev)
        aucPQ = roc_auc_score(np.r_[np.zeros(len(pev)), np.ones(len(qev))],
                              np.r_[sP_on_P, sP_on_Q])
        aucQP = roc_auc_score(np.r_[np.zeros(len(qev)), np.ones(len(pev))],
                              np.r_[sQ_on_Q, sQ_on_P])
        row = {'pair': name, 'arch': arch,
               'auc_P_system_vs_Q': round(float(aucPQ), 4),
               'auc_Q_system_vs_P': round(float(aucQP), 4),
               'alphas': {}}
        for a in ALPHAS:
            tauP = float(np.quantile(cP, 1 - a))
            tauQ = float(np.quantile(cQ, 1 - a))
            A_PQ = float((sP_on_Q <= tauP).mean())   # Q assimilated by P-system
            A_QP = float((sQ_on_P <= tauQ).mean())   # P assimilated by Q-system
            row['alphas'][str(a)] = {
                'assim_Q_under_P': round(A_PQ, 4),
                'assim_P_under_Q': round(A_QP, 4),
                'IAI': round(abs(A_PQ - A_QP), 4)}
        row['train_s'] = round(time.time() - t0, 1)
        results.append(row)
        print(json.dumps(row), flush=True)


def main():
    results = []
    print('== loading LHCO ==', flush=True)
    L = load_lhco()
    print({k: v.shape for k, v in L.items()}, flush=True)
    run_pair('L1 qcd-dijet vs 2prong', L['bkg'], L['sig2'], (60000, 20000, 20000), results)
    run_pair('L2 qcd-dijet vs 3prong', L['bkg'], L['sig3'], (50000, 20000, 20000), results)
    run_pair('L3 2prong vs 3prong', L['sig2'], L['sig3'], (50000, 20000, 20000), results)
    json.dump(results, open(os.path.join(OUT, 'results_partial.json'), 'w'), indent=1)
    print('== loading top-tagging ==', flush=True)
    tr = load_top('val.h5', 60000 + 20000)
    ev = load_top('test.h5', 20000)
    # combine: train+cal from val, eval from test — registered split
    P = np.concatenate([tr[0], ev[0]]); Q = np.concatenate([tr[1], ev[1]])
    run_pair('T1 qcd vs top (constituents)', P, Q, (60000, 20000, 20000), results)
    json.dump(results, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)
    print('BATTERY COMPLETE', flush=True)


if __name__ == '__main__':
    main()
