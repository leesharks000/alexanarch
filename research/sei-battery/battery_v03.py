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
    save(R)
    print('elapsed %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'T5')
