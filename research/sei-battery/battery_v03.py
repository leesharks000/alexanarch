#!/usr/bin/env python3
"""SEI Inversion Battery v0.3 — six registered tests clearing the v0.2 ledger.

PRE-REGISTRATION. This header is the registration. It is fixed BEFORE any v0.3
run. Every mismatch between this header and what executes is recorded in
results-v0.3.json under 'deviations', per the correction-ledger discipline
established in deposit #1455 (EA-SEI-BATTERY-01 v2.0).

Predecessors: #1449 (v0.1, single seed) -> #1455 (v0.2, multi-seed + ledger).
v0.2 left four ledger items open (D2, D3, D4, D5, D6) and produced two results
that demand new tests (T5, T6 below). v0.3 addresses all of them.

DELIBERATELY NOT IN v0.3, and why:
  * No GPU pass. It raises scale; scale is not what is contested. Every open
    objection concerns ESTIMAND VALIDITY, not sample size. A clean CPU-scale
    v0.3 is worth more than a delayed larger v0.2.
  * No panel expansion. Four pairs measured well beats eight measured hastily.
    Panel breadth belongs to ACRB (deposit #1454), not here.

ORDER OF EXECUTION (cheap and decisive first; T1 is last because it is the
most expensive and the least likely to change the reading of the others):
  T3 -> T5 -> T6 -> T4 -> T2 -> T1

────────────────────────────────────────────────────────────────────────────
T3  HIERARCHICAL UNCERTAINTY AND A REAL CALIBRATION TAIL      [clears D6]
────────────────────────────────────────────────────────────────────────────
Defect: the alpha = 1e-3 threshold in v0.2 was set by roughly 20 calibration
events, and intervals bootstrapped 5 seed-level scalars only.

Procedure: calibration split raised to 200,000 events per class for the LHCO
pairs (the background pool holds ~1e6, so this is free); T1 pools drawn from
val.h5 AND test.h5 to reach 200,000 per class. Uncertainty by HIERARCHICAL
bootstrap: resample seeds with replacement, and within each resampled seed
resample evaluation events with replacement; 2,000 outer x 1 inner draw.
Report 95 percent percentile intervals so labelled.

Registered prediction: qualitative conclusions (T1 inversion; L1/L2
direction-dependence; quiet control) are unchanged. Fourth-decimal
differences at alpha = 1e-3 do NOT survive; any claim resting on them is
withdrawn.

────────────────────────────────────────────────────────────────────────────
T5  SCORE-FUNCTION ABLATION ON A SINGLE TRAINED MODEL              [new]
────────────────────────────────────────────────────────────────────────────
Motivation: in v0.2 the VAE alone escaped the T1 inversion (0.535/0.739 vs the
AE 0.838/0.243) while carrying the largest T1 asymmetry. The VAE differs from
the AE in BOTH architecture and readout, so v0.2 cannot say which produced the
difference. Everything the program says about 'architecture changes the
orientation of the blind spot' depends on the answer.

Procedure: train ONE VAE per (pair, direction, seed) and read three scores off
the SAME trained weights: (a) reconstruction error of the decoded mean; (b)
latent norm sum mu_i^2 (the deployed AXOL1TL-class score); (c) full negative
ELBO. Calibrate each score independently on own held-out background; report
AUC both directions, M_A, D_A at both alphas.

REGISTERED PREDICTION (stated before running, so a miss is a result):
reconstruction error read from the VAE will INVERT on T1 in the manner of the
AE (AUC Q on P below 0.5); the latent-norm score read from the same weights
will NOT. If that holds, orientation is a property of the SCORE FUNCTION, not
the model, and the program's sentence must be restated as 'the readout changes
the orientation of the blind spot'.

────────────────────────────────────────────────────────────────────────────
T6  DISTILLATION, DONE PROPERLY, IN THREE PARTS          [clears D3, D4]
────────────────────────────────────────────────────────────────────────────
Defects: v0.2 measured rank survival on the withheld class though the header
said background, and quantized weights only while calling it 8-bit fixed point.

Procedure, all three parts:
  T6a  rank survival on BACKGROUND and on the WITHHELD CLASS, both reported,
       so the registered comparison finally exists;
  T6b  survival as a function of alpha over {1e-1, 1e-2, 1e-3}, because 36-47
       percent at a single operating point says nothing about the point a
       trigger actually runs at;
  T6c  TEACHER-STUDENT MISS OVERLAP: the RII quantities (q_T, q_S, q_TS,
       Delta_miss, phi) between a model and its own distilled student. This is
       the direct measurement of blind-spot inheritance that ACRB names as a
       first-class deployment question.
Quantization is reported as WEIGHT-ONLY and labelled as such; no claim of
FPGA-equivalent fixed-point arithmetic is made anywhere.

Registered prediction: survival degrades monotonically as alpha tightens, and
teacher-student phi is high (> 0.5) — the student inherits the teacher's blind
spot even where it loses the teacher's ranking.

────────────────────────────────────────────────────────────────────────────
T4  FULL REPRESENTATIONAL INDEPENDENCE INDEX                   [clears D5]
────────────────────────────────────────────────────────────────────────────
Defect: v0.2's RII was a seed-0, alpha = 1e-2 pilot.

Procedure: miss masks retained for every seed and every alpha; report q_A,
q_B, q_AB, Delta_miss AND phi with intervals over seeds, for every
architecture pair, both alphas. phi is the reportable statistic; raw
Delta_miss is compressed when miss rates approach 1 and is reported only
alongside it.

Registered prediction: the v0.2 spread is stable — same-family pairs (AE with
its energy-normalized variant) near-maximally coincident, AE with the
latent-norm score near-independent. If phi proves seed-unstable, no redundancy
claim can be made from this battery at all.

────────────────────────────────────────────────────────────────────────────
T2  POOLED COMPLEXITY AXIS AND A DISTANCE-MATCHED PANEL        [clears D2]
────────────────────────────────────────────────────────────────────────────
Defect: v0.2 fitted complexity per class without common standardization, and
all three LHCO classes returned identical compressed lengths — the axis had no
resolution, so LCBH was inconclusive.

Procedure: ONE scaler and ONE PCA basis fitted on the POOLED representation
across the classes being compared; participation ratio and compressed length
computed in that common basis with ONE quantization map. Then a
DISTANCE-MATCHED panel: pairs selected to hold representational separation
(measured as symmetrized KL between class score distributions under a common
reference model, and as Wasserstein-1 in the pooled PCA basis) approximately
constant while complexity DIRECTION differs. Without that matching the phrase
'at equal representational separation' in the LCBH statement is unearned and
the hypothesis is not being tested.

Registered outcome conditions: LCBH is SUPPORTED if, at matched separation,
classes below the training class on the pooled axis are assimilated more than
classes above it, consistently in sign across pairs and seeds. It is
FALSIFIED if the sign is consistent in the opposite direction. It remains
INCONCLUSIVE if the sign varies by pair — which is what v0.2 found and is a
live possibility.

────────────────────────────────────────────────────────────────────────────
T1  FAITHFUL NAE / WNAE                                        [clears D1]
────────────────────────────────────────────────────────────────────────────
Defect: the v0.2 'NAE' drew negatives by Gaussian perturbation of the
minibatch with a hinge energy ratio. The published normalized autoencoder
(Dillon et al., SciPost Phys. Core 6 (2023) 074) samples negatives from the
MODEL distribution by Langevin/MCMC. The registered remedy prediction is
therefore still untested; the v0.2 row is frozen and relabelled
pNAE-surrogate, never overwritten.

Procedure: NAE trained with a Langevin negative sampler — K steps, step size
eta, noise sigma_L, buffer of past negatives — with the energy defined as
reconstruction error, per the published construction. WNAE variant if the
Wasserstein form fits the compute budget; otherwise registered as not run.

DECLARED COMPUTE CONSEQUENCE, stated in advance: a K-step chain costs roughly
K times an AE step. At K = 20 a cell runs ~15 minutes on one core against ~50
seconds for an AE. This arm therefore runs at THREE seeds, not five, and the
reduction is declared here rather than discovered later. If the chain must be
shortened to K = 10 to fit, the chain length is recorded as a limitation and
the run is labelled a short-chain approximation.

Registered prediction: NAE shows the smallest |D_A| of the tested families on
the LHCO pairs and does NOT invert on T1. This is the same prediction v0.2
registered and could not test.

────────────────────────────────────────────────────────────────────────────
UNCHANGED FROM v0.2 (so the comparison remains a comparison)
────────────────────────────────────────────────────────────────────────────
Pairs, representations, architectures AE/VAE/GMM, training sizes, threshold
procedure, alphas, and the estimand definitions. M_A (mean assimilation
burden) and signed D_A accompany every IAI, per D7: a low asymmetry at a
severe operating point can mean symmetric FAILURE rather than symmetry, and
IAI is never reported alone.

INTERPRETATION LIMITS (carried forward unchanged)
  * Demonstration-scale surrogates, not deployed systems. Nothing measures
    AXOL1TL, CICADA, or GELATO.
  * No quantity here upper- or lower-bounds any open-world Ontological
    Assimilation Rate (the no-bounds discipline of #931 section 3.2).
  * Compute bound: single-thread CPU, one core, 3 GB.
"""
import os, sys, json, time, zlib
import numpy as np, h5py, hdf5plugin
import torch, torch.nn as nn

torch.set_num_threads(1)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
os.makedirs(OUT, exist_ok=True)
RES = os.path.join(OUT, 'results-v0.3.json')
ALPHAS = [1e-2, 1e-3]
SEEDS = [0, 1, 2, 3, 4]
CAL = 200000          # T3: real calibration tail
NTR, NEV = 60000, 20000

sys.path.insert(0, HERE)
from battery import load_top, load_lhco, AE, VAE, make_mlp
from battery_v02 import train_net, fit_system, system_score, auc


def load_state():
    return json.load(open(RES)) if os.path.exists(RES) else {
        'battery': 'EA-SEI-BATTERY-01 v0.3', 'date': '2026-08-12',
        'predecessor': '#1455 AXN:05E0.EMPIRICAL',
        'seeds': SEEDS, 'alphas': ALPHAS, 'calibration_per_class': CAL,
        'tests': {}, 'deviations': []}


def save(R):
    json.dump(R, open(RES, 'w'), indent=1)


def split(X, ntr, ncal, nev, seed):
    r = np.random.default_rng(1000 + seed)
    i = r.permutation(len(X))
    ncal = min(ncal, max(0, len(X) - ntr - nev))
    return X[i[:ntr]], X[i[ntr:ntr + ncal]], X[i[ntr + ncal:ntr + ncal + nev]]


def hier_ci(per_seed_scores, stat, B=2000, seed=0):
    """T3: hierarchical bootstrap — resample seeds, then events within seed."""
    r = np.random.default_rng(seed)
    S = len(per_seed_scores)
    draws = []
    for _ in range(B):
        si = r.integers(0, S, S)
        vals = []
        for k in si:
            a, b = per_seed_scores[k]
            ia = r.integers(0, len(a), len(a))
            ib = r.integers(0, len(b), len(b))
            vals.append(stat(a[ia], b[ib]))
        draws.append(np.mean(vals))
    return [round(float(np.percentile(draws, 2.5)), 4),
            round(float(np.percentile(draws, 97.5)), 4)]


def phi(qA, qB, qAB):
    den = (qA * (1 - qA) * qB * (1 - qB)) ** 0.5
    return round((qAB - qA * qB) / den, 4) if den > 0 else None


# ── T5: three scores off one trained VAE ────────────────────────────────────
def vae_scores(m, mu, sd, X):
    Z = torch.tensor((X - mu) / sd)
    with torch.no_grad():
        h = torch.relu(m.body(Z)); mu_z, lv = m.mu(h), m.lv(h)
        rec = ((m.dec(mu_z) - Z) ** 2).mean(1).numpy()          # (a) reconstruction of the mean
        lat = (mu_z ** 2).sum(1).numpy()                         # (b) latent norm, deployed score
        kl = (-0.5 * (1 + lv - mu_z ** 2 - lv.exp()).sum(1)).numpy()
        elbo = rec * Z.shape[1] + kl                             # (c) negative ELBO
    return {'recon': rec, 'latent': lat, 'nelbo': elbo}



# ── T6: distillation, three parts (clears D3, D4) ───────────────────────────
def distill_full(teacher, Xtr, Xbkg_ev, Xwith_ev, seed):
    """Train a student on teacher scores, weight-quantize it, and measure:
    T6a survival on BACKGROUND and on the WITHHELD class;
    T6b survival as a function of alpha;
    T6c teacher-student miss overlap (RII between a model and its own student).
    Quantization is WEIGHT-ONLY and labelled as such — no fixed-point claim."""
    from scipy.stats import spearmanr
    torch.manual_seed(seed)
    mu, sd = teacher['mu'], teacher['sd']
    Ztr = torch.tensor((Xtr - mu) / sd)
    y = torch.tensor(system_score(teacher, Xtr)).float().unsqueeze(1)
    ym, ys = y.mean(), y.std() + 1e-8
    student = nn.Sequential(nn.Linear(Ztr.shape[1], 32), nn.ReLU(),
                            nn.Linear(32, 16), nn.ReLU(), nn.Linear(16, 1))
    opt = torch.optim.Adam(student.parameters(), lr=1e-3)
    g = torch.Generator().manual_seed(seed)
    for _ in range(15):
        perm = torch.randperm(len(Ztr), generator=g)
        for i in range(0, len(Ztr), 512):
            idx = perm[i:i + 512]
            opt.zero_grad()
            ((student(Ztr[idx]) - (y[idx] - ym) / ys) ** 2).mean().backward()
            opt.step()
    qstudent = nn.Sequential(*[nn.Linear(l.in_features, l.out_features)
                               if isinstance(l, nn.Linear) else nn.ReLU() for l in student])
    with torch.no_grad():
        for lq, l in zip(qstudent, student):
            if isinstance(l, nn.Linear):
                for p_, q_ in ((l.weight, lq.weight), (l.bias, lq.bias)):
                    sc = p_.abs().max() / 127.0
                    q_.copy_(torch.round(p_ / sc) * sc)

    def scores(X):
        Z = torch.tensor((X - mu) / sd)
        with torch.no_grad():
            return (system_score(teacher, X),
                    student(Z).squeeze(1).numpy(),
                    qstudent(Z).squeeze(1).numpy())

    out = {'quantization': 'WEIGHT-ONLY 8-bit-spaced rounding; activations and arithmetic remain float. Not an FPGA fixed-point equivalent.'}
    for label, Xev in (('background', Xbkg_ev), ('withheld_class', Xwith_ev)):
        s_t, s_s, s_q = scores(Xev)
        row = {'spearman_student': round(float(spearmanr(s_t, s_s).statistic), 4),
               'spearman_quantized': round(float(spearmanr(s_t, s_q).statistic), 4)}
        for a in (1e-1, 1e-2, 1e-3):                      # T6b
            k = max(1, int(round(a * len(s_t))))
            top = lambda v: set(np.argsort(-v)[:k].tolist())
            T, S, Q = top(s_t), top(s_s), top(s_q)
            row['survival@%g' % a] = round(len(T & S) / k, 4)
            row['survival_quantized@%g' % a] = round(len(T & Q) / k, 4)
            row['k@%g' % a] = k
        out[label] = row
    # T6c: teacher-student miss overlap on the withheld class, thresholds on background
    s_t_b, s_s_b, _ = scores(Xbkg_ev)
    s_t_w, s_s_w, _ = scores(Xwith_ev)
    for a in ALPHAS:
        tT = np.quantile(s_t_b, 1 - a); tS = np.quantile(s_s_b, 1 - a)
        mT = s_t_w <= tT; mS = s_s_w <= tS
        qT, qS, qTS = float(mT.mean()), float(mS.mean()), float((mT & mS).mean())
        out['miss_overlap@%g' % a] = {'q_teacher': round(qT, 4), 'q_student': round(qS, 4),
                                      'q_both': round(qTS, 4),
                                      'delta_miss': round(qTS - qT * qS, 4), 'phi': phi(qT, qS, qTS)}
    return out


def main(which):
    R = load_state()
    t0 = time.time()
    top = load_top('val.h5', 100000); L = load_lhco()
    PAIRS = {'T1': (top[0], top[1]), 'L1': (L['bkg'], L['sig2']),
             'L2': (L['bkg'], L['sig3']), 'L3': (L['sig2'], L['sig3'])}
    if which == 'T5':
        R['tests'].setdefault('T5', {})
        for pname, (P, Q) in PAIRS.items():
            if pname in R['tests']['T5']:
                continue
            per = {k: [] for k in ('recon', 'latent', 'nelbo')}
            for s in SEEDS:
                Ptr, Pcal, Pev = split(P, NTR, CAL, NEV, s)
                Qtr, Qcal, Qev = split(Q, NTR, CAL, NEV, s)
                out = {}
                for tag, (tr, cal, ev, oev) in (('P', (Ptr, Pcal, Pev, Qev)),
                                                ('Q', (Qtr, Qcal, Qev, Pev))):
                    torch.manual_seed(s)
                    mu, sd = tr.mean(0), tr.std(0) + 1e-6
                    m = train_net(VAE(tr.shape[1]), (tr - mu) / sd, seed=s)
                    out[tag] = (m, mu, sd, cal, ev, oev)
                for k in per:
                    mP, muP, sdP, calP, evP, oevP = out['P']
                    mQ, muQ, sdQ, calQ, evQ, oevQ = out['Q']
                    sPcal = vae_scores(mP, muP, sdP, calP)[k]
                    sPev = vae_scores(mP, muP, sdP, evP)[k]
                    sPQ = vae_scores(mP, muP, sdP, oevP)[k]
                    sQcal = vae_scores(mQ, muQ, sdQ, calQ)[k]
                    sQev = vae_scores(mQ, muQ, sdQ, evQ)[k]
                    sQP = vae_scores(mQ, muQ, sdQ, oevQ)[k]
                    row = {'auc_P_on_Q': round(auc(sPev, sPQ), 4),
                           'auc_Q_on_P': round(auc(sQev, sQP), 4)}
                    for a in ALPHAS:
                        tP = np.quantile(sPcal, 1 - a); tQ = np.quantile(sQcal, 1 - a)
                        aPQ = float(np.mean(sPQ <= tP)); aQP = float(np.mean(sQP <= tQ))
                        row['M_A@%g' % a] = round((aPQ + aQP) / 2, 4)
                        row['D_A@%g' % a] = round(aPQ - aQP, 4)
                    per[k].append(row)
            R['tests']['T5'][pname] = {
                k: {kk: {'mean': round(float(np.mean([d[kk] for d in v])), 4),
                         'seed_values': [d[kk] for d in v]} for kk in v[0]}
                for k, v in per.items()}
            print('T5 %-3s recon AUC Q->P %.3f | latent %.3f | nelbo %.3f  (%.0fs)' % (
                pname, R['tests']['T5'][pname]['recon']['auc_Q_on_P']['mean'],
                R['tests']['T5'][pname]['latent']['auc_Q_on_P']['mean'],
                R['tests']['T5'][pname]['nelbo']['auc_Q_on_P']['mean'], time.time() - t0), flush=True)
            save(R)
    if which == 'T6':
        R['tests'].setdefault('T6', {})
        for pname, (P, Q) in PAIRS.items():
            if pname in R['tests']['T6']:
                continue
            per = []
            for s_ in SEEDS:
                Ptr, Pcal, Pev = split(P, NTR, CAL, NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR, CAL, NEV, s_)
                teacher = fit_system('AE', Ptr, s_)
                per.append(distill_full(teacher, Ptr, Pev, Qev, s_))
            agg = {'quantization': per[0]['quantization'], 'seeds': SEEDS,
                   'per_seed': per}
            for sec in ('background', 'withheld_class'):
                agg[sec] = {k: round(float(np.mean([d[sec][k] for d in per])), 4) for k in per[0][sec]}
            for a in ALPHAS:
                key = 'miss_overlap@%g' % a
                agg[key] = {k: round(float(np.mean([d[key][k] for d in per])), 4) for k in per[0][key]}
            R['tests']['T6'][pname] = agg
            b = agg['background']; w = agg['withheld_class']
            print('T6 %-3s bkg surv@1e-2 %.3f | withheld %.3f | phi(T,S)@1e-2 %.3f  (%.0fs)' % (
                pname, b['survival@0.01'], w['survival@0.01'],
                agg['miss_overlap@0.01']['phi'], time.time() - t0), flush=True)
            save(R)
    if which == 'T4':
        # T4: full RII — every seed, both alphas, phi with intervals over seeds.
        R['tests'].setdefault('T4', {})
        ARCHS = ['AE', 'VAE', 'GMM']
        for pname, (P, Q) in PAIRS.items():
            if pname in R['tests']['T4']:
                continue
            masks = {a: {arch: [] for arch in ARCHS} for a in ALPHAS}
            for s_ in SEEDS:
                Ptr, Pcal, Pev = split(P, NTR, CAL, NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR, CAL, NEV, s_)
                for arch in ARCHS:
                    sysP = fit_system(arch, Ptr, s_)
                    sPcal = system_score(sysP, Pcal)
                    sPQ = system_score(sysP, Qev)
                    for a in ALPHAS:
                        t = np.quantile(sPcal, 1 - a)
                        masks[a][arch].append(sPQ <= t)
            out = {}
            for a in ALPHAS:
                for i, A in enumerate(ARCHS):
                    for B in ARCHS[i + 1:]:
                        per = []
                        for k in range(len(SEEDS)):
                            mA, mB = masks[a][A][k], masks[a][B][k]
                            n = min(len(mA), len(mB)); mA, mB = mA[:n], mB[:n]
                            qA, qB, qAB = float(mA.mean()), float(mB.mean()), float((mA & mB).mean())
                            per.append({'q_A': qA, 'q_B': qB, 'q_AB': qAB,
                                        'delta_miss': qAB - qA * qB, 'phi': phi(qA, qB, qAB)})
                        agg = {}
                        for kk in per[0]:
                            vals = [d[kk] for d in per if d[kk] is not None]
                            if not vals:
                                agg[kk] = None; continue
                            r = np.random.default_rng(7)
                            bs = r.choice(np.asarray(vals, float), size=(4000, len(vals)), replace=True).mean(1)
                            agg[kk] = {'mean': round(float(np.mean(vals)), 4),
                                       'ci95_seeds': [round(float(np.percentile(bs, 2.5)), 4),
                                                      round(float(np.percentile(bs, 97.5)), 4)],
                                       'seed_values': [round(v, 4) for v in vals]}
                        out['%s~%s@%g' % (A, B, a)] = agg
            R['tests']['T4'][pname] = out
            k1 = 'AE~VAE@0.01'
            print('T4 %-3s AE~VAE phi %.3f %s | AE~GMM phi %.3f  (%.0fs)' % (
                pname, out[k1]['phi']['mean'], out[k1]['phi']['ci95_seeds'],
                out['AE~GMM@0.01']['phi']['mean'], time.time() - t0), flush=True)
            save(R)
    if which == 'T2':
        # T2: pooled complexity axis + distance-matched panel (clears D2).
        # ONE scaler, ONE PCA basis, ONE quantization map, fitted on the POOLED
        # representation of the classes being compared. Separation measured in
        # that common basis so "at equal representational separation" is earned.
        from scipy.stats import wasserstein_distance
        R['tests'].setdefault('T2', {})
        GROUPS = {'constituents': {'qcd': PAIRS['T1'][0], 'top': PAIRS['T1'][1]},
                  'lhco7': {'bkg': PAIRS['L1'][0], '2prong': PAIRS['L1'][1],
                            '3prong': PAIRS['L2'][1]}}
        for gname, classes in GROUPS.items():
            if gname in R['tests']['T2']:
                continue
            names = list(classes)
            sub = {k: classes[k][:20000] for k in names}
            pooled = np.concatenate([sub[k] for k in names])
            mu, sd = pooled.mean(0), pooled.std(0) + 1e-9          # ONE scaler
            Zp = (pooled - mu) / sd
            Zc = Zp - Zp.mean(0)
            U, S, Vt = np.linalg.svd(Zc, full_matrices=False)      # ONE PCA basis
            lo = np.percentile(Zp, 1, axis=0); hi = np.percentile(Zp, 99, axis=0)  # ONE quant map
            comp = {}
            for k in names:
                Z = (sub[k] - mu) / sd
                proj = (Z - Zp.mean(0)) @ Vt.T                      # common basis
                ev = proj.var(0); ev = ev / ev.sum()
                pr = float(1.0 / (ev ** 2).sum())
                q = np.clip(np.round((Z - lo) / (hi - lo + 1e-9) * 255), 0, 255).astype(np.uint8)
                zl = float(np.mean([len(zlib.compress(r_.tobytes(), 6)) for r_ in q[:1000]]))
                comp[k] = {'participation_ratio_pooled_basis': round(pr, 3),
                           'zlib_len_common_map': round(zl, 2),
                           'mean_pc1': round(float(proj[:, 0].mean()), 4)}
            # separation between every class pair in the common basis
            sep = {}
            for i, a in enumerate(names):
                for b in names[i + 1:]:
                    Za = ((sub[a] - mu) / sd - Zp.mean(0)) @ Vt.T
                    Zb = ((sub[b] - mu) / sd - Zp.mean(0)) @ Vt.T
                    w1 = float(np.mean([wasserstein_distance(Za[:, d], Zb[:, d])
                                        for d in range(min(10, Za.shape[1]))]))
                    sep['%s~%s' % (a, b)] = {
                        'wasserstein1_top10pc': round(w1, 4),
                        'delta_complexity_PR': round(comp[b]['participation_ratio_pooled_basis']
                                                     - comp[a]['participation_ratio_pooled_basis'], 3),
                        'delta_complexity_zlib': round(comp[b]['zlib_len_common_map']
                                                       - comp[a]['zlib_len_common_map'], 2)}
            R['tests']['T2'][gname] = {'complexity': comp, 'separation': sep,
                'axis_resolves': bool(len(set(round(v['zlib_len_common_map'], 1) for v in comp.values())) > 1
                                      or len(set(round(v['participation_ratio_pooled_basis'], 1) for v in comp.values())) > 1)}
            print('T2 %-12s %s | axis resolves: %s  (%.0fs)' % (
                gname, {k: v['participation_ratio_pooled_basis'] for k, v in comp.items()},
                R['tests']['T2'][gname]['axis_resolves'], time.time() - t0), flush=True)
            save(R)
        # distance-matched verdict against the measured directional results
        v02 = json.load(open(os.path.join(OUT, 'results-v0.2.json')))
        verdict = {}
        for pname, (Pn, Qn, grp) in (('T1', ('qcd', 'top', 'constituents')),
                                     ('L1', ('bkg', '2prong', 'lhco7')),
                                     ('L2', ('bkg', '3prong', 'lhco7'))):
            g = R['tests']['T2'][grp]['complexity']
            cP = g[Pn]['participation_ratio_pooled_basis']; cQ = g[Qn]['participation_ratio_pooled_basis']
            c = v02['cells']['%s|AE' % pname]
            aQ = c['assim_Q_by_P@0.01']['mean']; aP = c['assim_P_by_Q@0.01']['mean']
            lower_is_Q = cQ < cP
            lower_assimilated_more = (aQ > aP) if lower_is_Q else (aP > aQ)
            key = '%s~%s' % (Pn, Qn) if '%s~%s' % (Pn, Qn) in R['tests']['T2'][grp]['separation'] else '%s~%s' % (Qn, Pn)
            verdict[pname] = {'C_P': cP, 'C_Q': cQ,
                              'separation_W1': R['tests']['T2'][grp]['separation'][key]['wasserstein1_top10pc'],
                              'assim_Q_by_P': aQ, 'assim_P_by_Q': aP,
                              'LCBH_consistent': bool(lower_assimilated_more)}
        signs = [v['LCBH_consistent'] for v in verdict.values()]
        R['tests']['T2']['lcbh_verdict'] = {
            'per_pair': verdict,
            'outcome': ('SUPPORTED' if all(signs) else 'FALSIFIED' if not any(signs) else 'INCONCLUSIVE'),
            'note': ('Registered outcome conditions: SUPPORTED if lower-complexity classes are assimilated more '
                     'consistently in sign across pairs; FALSIFIED if consistently the opposite; INCONCLUSIVE if the '
                     'sign varies by pair. Separation is NOT matched across these pairs, so this is the pooled-axis '
                     'rerun of the v0.2 comparison, not the distance-matched test — a matched panel requires pairs '
                     'holding W1 approximately constant while complexity direction differs, which this data does not '
                     'contain. The matched panel is therefore registered as NOT RUN.')}
        print('T2 LCBH verdict:', R['tests']['T2']['lcbh_verdict']['outcome'],
              {k: v['LCBH_consistent'] for k, v in verdict.items()})
    if which == 'T1':
        # T1: FAITHFUL NAE — negatives sampled from the MODEL distribution by
        # Langevin MCMC with a replay buffer, per Dillon et al., SciPost Phys.
        # Core 6 (2023) 074. Energy = reconstruction error. Three seeds, declared
        # in the pre-registration; chain length recorded with the result.
        K_STEPS, ETA, SIGMA_L, BUF = 20, 0.05, 0.05, 1024
        R['tests'].setdefault('T1_faithful_NAE', {})

        def train_faithful_nae(X, seed, d):
            torch.manual_seed(seed)
            g = torch.Generator().manual_seed(seed)
            m = AE(d)
            opt = torch.optim.Adam(m.parameters(), lr=1e-3)
            Xt = torch.tensor(X)
            buf = Xt[torch.randperm(len(Xt), generator=g)[:BUF]].clone()
            energy = lambda z: ((m(z) - z) ** 2).mean(1)
            for ep in range(12):
                perm = torch.randperm(len(Xt), generator=g)
                for i in range(0, len(Xt), 512):
                    xb = Xt[perm[i:i + 512]]
                    # negatives from the MODEL distribution: Langevin chain,
                    # 95% initialised from the replay buffer, 5% from noise
                    nb = xb.shape[0]
                    bidx = torch.randint(0, len(buf), (nb,), generator=g)
                    neg = buf[bidx].clone()
                    fresh = torch.rand(nb, generator=g) < 0.05
                    if fresh.any():
                        neg[fresh] = torch.randn((int(fresh.sum()), d), generator=g)
                    neg.requires_grad_(True)
                    for _ in range(K_STEPS):
                        e = energy(neg).sum()
                        gr = torch.autograd.grad(e, neg)[0]
                        with torch.no_grad():
                            neg = neg - ETA * gr + SIGMA_L * torch.randn(neg.shape, generator=g)
                        neg.requires_grad_(True)
                    neg = neg.detach()
                    with torch.no_grad():
                        buf[bidx] = neg
                    opt.zero_grad()
                    # normalized-energy objective: lower energy on data, raise on
                    # model samples (the normalization term of the published NAE)
                    loss = energy(xb).mean() - energy(neg).mean()
                    loss = loss + 0.1 * (energy(xb) ** 2).mean()   # energy regulariser
                    loss.backward(); opt.step()
            return m

        def nae_sys(Xtr, seed):
            mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
            m = train_faithful_nae((Xtr - mu) / sd, seed, Xtr.shape[1])
            return {'arch': 'NAE_faithful', 'm': m, 'mu': mu, 'sd': sd}

        def nae_score(sysd, X):
            Z = torch.tensor((X - sysd['mu']) / sysd['sd'])
            with torch.no_grad():
                return ((sysd['m'](Z) - Z) ** 2).mean(1).numpy()

        only = os.environ.get('ONLY_PAIR')
        for pname, (P, Q) in PAIRS.items():
            if pname in R['tests']['T1_faithful_NAE'] or (only and pname != only):
                continue
            per = []
            for s_ in SEEDS[:3]:
                Ptr, Pcal, Pev = split(P, NTR, min(CAL, 60000), NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR, min(CAL, 60000), NEV, s_)
                sP, sQ = nae_sys(Ptr, s_), nae_sys(Qtr, s_)
                sPcal, sPev, sPQ = nae_score(sP, Pcal), nae_score(sP, Pev), nae_score(sP, Qev)
                sQcal, sQev, sQP = nae_score(sQ, Qcal), nae_score(sQ, Qev), nae_score(sQ, Pev)
                row = {'auc_P_on_Q': round(auc(sPev, sPQ), 4), 'auc_Q_on_P': round(auc(sQev, sQP), 4)}
                for a in ALPHAS:
                    tP, tQ = np.quantile(sPcal, 1 - a), np.quantile(sQcal, 1 - a)
                    aPQ, aQP = float(np.mean(sPQ <= tP)), float(np.mean(sQP <= tQ))
                    row['M_A@%g' % a] = round((aPQ + aQP) / 2, 4)
                    row['D_A@%g' % a] = round(aPQ - aQP, 4)
                    row['IAI@%g' % a] = round(abs(aPQ - aQP), 4)
                per.append(row)
            R['tests']['T1_faithful_NAE'][pname] = {
                'chain': {'K_steps': K_STEPS, 'eta': ETA, 'sigma_langevin': SIGMA_L,
                          'buffer': BUF, 'seeds': SEEDS[:3],
                          'note': 'negatives sampled from the model distribution by Langevin MCMC with a replay buffer; energy = reconstruction error'},
                **{k: {'mean': round(float(np.mean([d[k] for d in per])), 4),
                       'seed_values': [d[k] for d in per]} for k in per[0]}}
            r_ = R['tests']['T1_faithful_NAE'][pname]
            print('T1nae %-3s AUC %.3f / %.3f  D_A@1e-2 %+.4f  (%.0fs)' % (
                pname, r_['auc_P_on_Q']['mean'], r_['auc_Q_on_P']['mean'],
                r_['D_A@0.01']['mean'], time.time() - t0), flush=True)
            save(R)
    save(R)
    print('elapsed %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'T5')
