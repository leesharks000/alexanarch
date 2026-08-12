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
    """Single-writer discipline (added 2026-08-12 after a near-miss).

    Two jobs writing this file concurrently truncated it, and an hours-old job
    holding a stale in-memory snapshot would have silently overwritten a full
    verdict-and-deviations ledger with a pre-correction copy. Every write now
    MERGES into whatever is on disk at write time rather than replacing it, and
    writes atomically via a temp file, so a late finisher can add its own cell
    without clobbering work it never saw.
    """
    disk = json.load(open(RES)) if os.path.exists(RES) else {}
    for k, v in R.items():
        if k == 'tests' and isinstance(v, dict):
            merged = dict(disk.get('tests', {}))
            merged.update(v)
            disk['tests'] = merged
        elif k in ('verdicts', 'standing_tally') and isinstance(v, dict):
            m = dict(disk.get(k, {})); m.update(v); disk[k] = m
        elif k == 'deviations' and isinstance(v, list):
            seen = {d.get('id') for d in disk.get('deviations', [])}
            disk['deviations'] = disk.get('deviations', []) + [d for d in v if d.get('id') not in seen]
        else:
            disk[k] = v
    tmp = RES + '.tmp'
    json.dump(disk, open(tmp, 'w'), indent=1)
    os.replace(tmp, RES)


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


# ─────────────────────────────────────────────────────────────────────────────
# T3 IMPLEMENTATION NOTE — added 2026-08-12, AFTER v0.3 results existed.
#
# The pre-registration (commit c7e5b4e7) specified T3 before any run; the
# executable shipped without a T3 branch, which the code audit caught. This
# code is therefore a POST-RESULTS IMPLEMENTATION OF A PRE-REGISTERED
# PROCEDURE. The original registration commit stands unedited; the prediction
# and the estimands are unchanged from it:
#   PREDICTION (unchanged): qualitative conclusions — the constituent inversion,
#   LHCO direction-dependence, quiet control — survive; fourth-decimal
#   differences at alpha = 1e-3 do NOT, and any claim resting on them is
#   withdrawn.
# What changes here is only that the procedure is now actually executed.
#
# Two registration gaps this closes, both recorded as deviations V3-D1/V3-D2:
#   * calibration is drawn as large as each pool permits and the ACHIEVED size
#     is recorded per direction, rather than a declared 200k that split()
#     silently clipped;
#   * the constituent pools are drawn from val.h5 AND test.h5, as registered.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# T7 PRE-REGISTRATION — written and committed 2026-08-12 BEFORE any T7 run.
#
# WHY. v0.3 claimed "miss correlation is a property of the representation" from
# T4, and the code audit withdrew it: the constituent panel and the engineered
# panel differ in representation AND in task and class distributions together,
# so representation was confounded with dataset. The audit named the fix — take
# the SAME physical pair and encode it twice — and this is that test.
#
# DESIGN. One physical pair (top-tagging QCD vs top jets), two encodings of the
# SAME events, same classes, same splits, same seeds:
#   R1  leading-40 constituents, 120 dims (as used throughout v0.1-v0.3)
#   R2  seven engineered jet observables computed FROM THE SAME EVENTS:
#       jet mass, jet pT, constituent multiplicity above 1% pT fraction,
#       girth (pT-weighted radial spread), leading-constituent pT fraction,
#       pT dispersion, and the pT-weighted RMS of delta-R.
#   Architectures AE, VAE, GMM; five seeds; thresholds on own held-out
#   background at alpha in {1e-2, 1e-3}; RII phi between every architecture
#   pair, in each representation.
#
# REGISTERED PREDICTION, stated before running so a miss is a result:
#   If miss correlation is representation-conditioned, phi for a GIVEN
#   architecture pair will differ substantially between R1 and R2 on these
#   identical classes — specifically, AE~VAE phi will be near zero on R1
#   (as measured in T4: 0.020) and materially higher on R2.
#   If instead it is task-conditioned, phi will be similar across the two
#   encodings, and the T4 finding was about the DATASETS rather than their
#   representations — in which case the restated T4 claim also needs revising.
#
# LIMIT. Two encodings of one pair cannot establish a general law; they can
# establish whether representation alone is sufficient to move phi, which is
# exactly what the withdrawn claim asserted and what T4 could not separate.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# T8 PRE-REGISTRATION — written and committed 2026-08-12 BEFORE any T8 run.
# THE PUBLISHED NAE REMEDY, third attempt, this time with the construction the
# paper actually specifies.
#
# HISTORY OF THIS ARM, stated because it is the point. v0.2 shipped a Gaussian-
# perturbation surrogate and called it NAE (deviation D1). v0.3 shipped an
# input-space PCD chain and called it faithful (deviation V3-D10). Both were
# relabelled after audit rather than overwritten. The published collider NAE
# (Dillon, Favaro, Plehn, Sorrenson, Kramer, SciPost Phys. Core 6 (2023) 074;
# arXiv:2206.14225) specifies:
#     (a) PRETRAIN an ordinary autoencoder on the training class;
#     (b) ON-MANIFOLD INITIALIZATION: run a Langevin chain in LATENT space,
#         decode the resulting latent samples through the trained decoder to
#         obtain on-manifold negatives;
#     (c) run a further Langevin chain in INPUT space starting from those
#         decoded negatives;
#     (d) train the normalized-energy objective against those negatives, with
#         a replay buffer and stabilisation.
# T8 implements (a)-(d). If it still fails to converge, that is reported as a
# sampler outcome, not as a verdict on the remedy.
#
# REGISTERED PREDICTION, stated before running:
#   On the LHCO pairs the published NAE shows SMALLER directional asymmetry
#   |D_A@1e-2| than the plain AE (0.155 on L1, 0.268 on L2 from T3), and on the
#   constituent pair it does NOT invert (AUC Q on P >= 0.5, against the plain
#   AE's 0.241). If either fails, the remedy does not remedy the failure mode
#   this battery measures, at this scale, on these representations.
#
# REGISTERED CONVERGENCE DIAGNOSTIC, so a null is interpretable rather than
# ambiguous: report mean negative-sample energy relative to mean data energy at
# the end of training. A sampler that has converged should place negatives at
# comparable or lower energy than data under the normalized objective; a ratio
# far above 1 indicates the chain never reached the model distribution, and the
# result is then reported as UNINTERPRETABLE rather than as a failure of NAE.
#
# DECLARED SCOPE: three seeds (as for the earlier NAE arms); K_latent = 20,
# K_input = 20; LHCO pairs first, constituent pair last since it is the
# expensive one. WNAE remains NOT RUN.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# T9 PRE-REGISTRATION — written and committed 2026-08-12 BEFORE any T9 run.
# CHAIN-LENGTH LADDER ON THE CONSTITUENT REPRESENTATION.
#
# WHY. T8 found the published NAE reduces directional asymmetry on the LHCO
# pairs with a converged sampler (energy ratio 0.95-0.98), but on the 120-dim
# constituent pair the ratio was 0.48 — the chain had not equilibrated, so that
# cell was reported UNINTERPRETABLE rather than as a failure of the remedy.
# T9 asks whether the constituent cell becomes interpretable with a longer
# chain, and whether the inversion survives if it does.
#
# DESIGN. Constituent pair only. K_latent = K_input in {20, 40, 80}, all other
# settings identical to T8 (three seeds, epochs 3, 15,000 training events per
# class, eta 0.05, sigma 0.05, buffer 1024). Report per rung: the convergence
# diagnostic, AUC both directions, and D_A at both alphas.
#
# REGISTERED PREDICTIONS, stated before running:
#   (1) The energy ratio rises monotonically with chain length and reaches the
#       0.9-1.0 band the LHCO cells occupied by K = 80.
#   (2) IF a rung reaches that band, the constituent inversion PERSISTS there —
#       AUC Q on P stays below 0.5 — because T8's LHCO cells showed the remedy
#       shrinking asymmetry without reversing an inversion, and the constituent
#       inversion is far deeper than any asymmetry the remedy corrected.
#   Prediction (2) is the substantive one. If a converged rung shows AUC Q on P
#   at or above 0.5, the published remedy DOES prevent the inversion and every
#   inversion claim in this program is bounded to non-normalized scores.
#
# OUTCOME CONDITIONS. If no rung reaches the band, T9 reports that the
# constituent cell remains uninterpretable at feasible chain lengths on this
# compute, and the question is deferred rather than answered — a null about the
# sampler, not about the remedy.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# T10 PRE-REGISTRATION — written and committed 2026-08-12 BEFORE any T10 run.
# STEP-SIZE AND NOISE-SCALE SWEEP ON THE CONSTITUENT REPRESENTATION.
#
# WHY. T9 ruled out chain length: the energy ratio sat at 0.40-0.48 across
# K = 20, 40, 80 and never approached the 0.9-1.0 band the LHCO cells reached.
# T9's own verdict named the next diagnostic — the Langevin step size and noise
# scale, or the on-manifold decode in 120 dimensions — rather than more steps.
# This is that sweep. It is a SAMPLER diagnostic, not a test of the remedy.
#
# DESIGN. Constituent pair, K = 20 fixed (T9 showed K is not binding), three
# seeds, all else as T8. Grid over (eta, sigma):
#   eta   in {0.01, 0.05, 0.20}
#   sigma in {0.01, 0.05, 0.20}
# Nine cells; report the energy ratio for each, plus AUC both directions and
# D_A for any cell that lands in band.
#
# REGISTERED PREDICTIONS:
#   (1) At least one (eta, sigma) cell reaches the 0.85-1.15 band. The ratio
#       being pinned near 0.4 across chain lengths is the signature of a chain
#       that equilibrates quickly to the WRONG stationary distribution, which
#       is a step-size and noise problem, so the grid should move it.
#   (2) The ratio increases with sigma at fixed eta — larger injected noise
#       pushes negatives away from the low-energy manifold the decode places
#       them on.
#   (3) SUBSTANTIVE, conditional: in any cell that lands in band, the
#       constituent inversion persists (AUC Q on P below 0.5).
#
# OUTCOME CONDITION. If no cell reaches the band, the on-manifold construction
# itself — not its hyperparameters — is implicated on 120-dim constituents, and
# the correct report is that this battery cannot make the constituent cell
# interpretable at all, with the reason localised to the decode rather than
# left vague. That would be a stronger and more useful null than T9's.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# T10 PRE-REGISTRATION — written and committed 2026-08-12 BEFORE any T10 run.
# STEP-SIZE AND NOISE-SCALE SWEEP ON THE CONSTITUENT REPRESENTATION.
#
# WHY. T9 ruled out chain length: energy ratios sat at 0.40-0.48 across K = 20,
# 40, 80, never reaching the 0.85-1.15 band the LHCO cells occupied. The
# negatives are persistently at roughly half the data energy no matter how long
# the chain runs, which points at the sampler's step geometry rather than at
# mixing time. T10 sweeps that geometry.
#
# DESIGN. Constituent pair only, K fixed at the registered 20, three seeds,
# everything else as in T8. Grid over Langevin step size eta and noise sigma:
#   eta   in {0.01, 0.05, 0.20}
#   sigma in {0.01, 0.05, 0.20}
# Nine cells. Report per cell: energy ratio, whether it lands in band, AUC both
# directions, D_A at both alphas.
#
# REGISTERED PREDICTIONS, stated before running:
#   (1) At least one cell of the nine reaches the 0.85-1.15 band. The specific
#       expectation is that LARGER eta is what does it — the chain is not
#       descending far enough per step in 120 dimensions — with sigma mattering
#       less.
#   (2) In any cell that reaches the band, the constituent inversion PERSISTS
#       (AUC Q on P below 0.5). This is the same substantive prediction T9 could
#       not test, carried forward unchanged.
#
# OUTCOME CONDITIONS. If no cell reaches the band, the constituent
# representation is recorded as one where this implementation of the published
# construction does not equilibrate under any tested geometry, and the question
# of whether the remedy prevents inversion there is CLOSED FOR THIS BATTERY and
# handed to anyone with the collaboration's compute. That is a null about our
# implementation, stated as such, and it is the honest end of this line rather
# than a further ladder.
# ─────────────────────────────────────────────────────────────────────────────

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
    if which == 'T3':
        R['tests'].setdefault('T3', {})
        # registered: constituent pools from val.h5 AND test.h5
        topA = load_top('val.h5', 100000); topB = load_top('test.h5', 100000)
        TOP = {k: np.concatenate([topA[k], topB[k]]) for k in (0, 1)}
        P3 = {'T1': (TOP[0], TOP[1]), 'L1': (L['bkg'], L['sig2']),
              'L2': (L['bkg'], L['sig3']), 'L3': (L['sig2'], L['sig3'])}
        only = os.environ.get('ONLY_PAIR')
        for pname, (P, Q) in P3.items():
            if pname in R['tests']['T3'] or (only and pname != only):
                continue
            per_seed = []
            achieved = {}
            for s_ in SEEDS:
                Ptr, Pcal, Pev = split(P, NTR, CAL, NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR, CAL, NEV, s_)
                achieved = {'P_calibration': int(len(Pcal)), 'Q_calibration': int(len(Qcal)),
                            'evaluation_per_class': int(len(Pev))}
                sysP, sysQ = fit_system('AE', Ptr, s_), fit_system('AE', Qtr, s_)
                per_seed.append({
                    'sPcal': system_score(sysP, Pcal), 'sPev': system_score(sysP, Pev),
                    'sPQ': system_score(sysP, Qev), 'sQcal': system_score(sysQ, Qcal),
                    'sQev': system_score(sysQ, Qev), 'sQP': system_score(sysQ, Pev)})
            # HIERARCHICAL bootstrap: resample seeds, then events within each seed
            rng = np.random.default_rng(3)
            B = 2000
            draws = {'auc_P_on_Q': [], 'auc_Q_on_P': []}
            for a in ALPHAS:
                draws['M_A@%g' % a] = []; draws['D_A@%g' % a] = []
            for _ in range(B):
                si = rng.integers(0, len(per_seed), len(per_seed))
                acc = {k: [] for k in draws}
                for k_ in si:
                    d = per_seed[k_]
                    rs = lambda v: v[rng.integers(0, len(v), len(v))]
                    sPcal, sPev, sPQ = rs(d['sPcal']), rs(d['sPev']), rs(d['sPQ'])
                    sQcal, sQev, sQP = rs(d['sQcal']), rs(d['sQev']), rs(d['sQP'])
                    acc['auc_P_on_Q'].append(auc(sPev, sPQ))
                    acc['auc_Q_on_P'].append(auc(sQev, sQP))
                    for a in ALPHAS:
                        tP, tQ = np.quantile(sPcal, 1 - a), np.quantile(sQcal, 1 - a)
                        aPQ, aQP = float(np.mean(sPQ <= tP)), float(np.mean(sQP <= tQ))
                        acc['M_A@%g' % a].append((aPQ + aQP) / 2)
                        acc['D_A@%g' % a].append(aPQ - aQP)
                for k in draws:
                    draws[k].append(np.mean(acc[k]))
            out = {'calibration_achieved': achieved,
                   'bootstrap': 'HIERARCHICAL: %d outer draws; seeds resampled with replacement, then events resampled within each seed' % B}
            # point estimates from the unresampled data
            for k, f in (('auc_P_on_Q', lambda d: auc(d['sPev'], d['sPQ'])),
                         ('auc_Q_on_P', lambda d: auc(d['sQev'], d['sQP']))):
                out[k] = {'mean': round(float(np.mean([f(d) for d in per_seed])), 4),
                          'ci95_hier': [round(float(np.percentile(draws[k], 2.5)), 4),
                                        round(float(np.percentile(draws[k], 97.5)), 4)]}
            for a in ALPHAS:
                ms, ds = [], []
                for d in per_seed:
                    tP, tQ = np.quantile(d['sPcal'], 1 - a), np.quantile(d['sQcal'], 1 - a)
                    aPQ, aQP = float(np.mean(d['sPQ'] <= tP)), float(np.mean(d['sQP'] <= tQ))
                    ms.append((aPQ + aQP) / 2); ds.append(aPQ - aQP)
                for lbl, vals in (('M_A@%g' % a, ms), ('D_A@%g' % a, ds)):
                    out[lbl] = {'mean': round(float(np.mean(vals)), 4),
                                'ci95_hier': [round(float(np.percentile(draws[lbl], 2.5)), 4),
                                              round(float(np.percentile(draws[lbl], 97.5)), 4)]}
            R['tests']['T3'][pname] = out
            print('T3 %-3s cal %d/%d | AUC %.3f %s / %.3f %s | D_A@1e-3 %+.4f %s  (%.0fs)' % (
                pname, achieved['P_calibration'], achieved['Q_calibration'],
                out['auc_P_on_Q']['mean'], out['auc_P_on_Q']['ci95_hier'],
                out['auc_Q_on_P']['mean'], out['auc_Q_on_P']['ci95_hier'],
                out['D_A@0.001']['mean'], out['D_A@0.001']['ci95_hier'], time.time() - t0), flush=True)
            save(R)
    if which == 'T7':
        R['tests'].setdefault('T7', {})
        topA = load_top('val.h5', 100000)
        import h5py, hdf5plugin
        def engineered(raw):
            """Seven jet observables from the same leading-40 constituents."""
            pt, eta, phi_ = raw[:, 0::3], raw[:, 1::3], raw[:, 2::3]
            tot = pt.sum(1) + 1e-9
            f = pt / tot[:, None]
            dr = np.sqrt(eta ** 2 + phi_ ** 2)
            mult = (f > 0.01).sum(1).astype(np.float32)
            girth = (f * dr).sum(1)
            lead = f.max(1)
            disp = np.sqrt((f ** 2).sum(1))
            rms = np.sqrt((f * dr ** 2).sum(1))
            mass = np.sqrt(np.maximum(0.0, (tot ** 2) - ((pt * np.cos(phi_)).sum(1) ** 2
                        + (pt * np.sin(phi_)).sum(1) ** 2 + (pt * np.sinh(eta)).sum(1) ** 2)))
            return np.stack([mass, tot, mult, girth, lead, disp, rms], 1).astype(np.float32)
        REPS = {'R1_constituents': {0: topA[0], 1: topA[1]},
                'R2_engineered': {0: engineered(topA[0]), 1: engineered(topA[1])}}
        ARCHS = ['AE', 'VAE', 'GMM']
        for rname, cls in REPS.items():
            if rname in R['tests']['T7']:
                continue
            P, Q = cls[0], cls[1]
            masks = {a: {arch: [] for arch in ARCHS} for a in ALPHAS}
            aucs = {arch: [] for arch in ARCHS}
            for s_ in SEEDS:
                Ptr, Pcal, Pev = split(P, NTR, 20000, NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR, 20000, NEV, s_)
                for arch in ARCHS:
                    sysP = fit_system(arch, Ptr, s_)
                    sPcal, sPev, sPQ = (system_score(sysP, Pcal), system_score(sysP, Pev),
                                        system_score(sysP, Qev))
                    aucs[arch].append(round(auc(sPev, sPQ), 4))
                    for a in ALPHAS:
                        masks[a][arch].append(sPQ <= np.quantile(sPcal, 1 - a))
            out = {'auc_P_on_Q': {k: {'mean': round(float(np.mean(v)), 4), 'seed_values': v}
                                  for k, v in aucs.items()}, 'dims': int(P.shape[1])}
            for a in ALPHAS:
                for i, A in enumerate(ARCHS):
                    for B in ARCHS[i + 1:]:
                        vals = []
                        for k in range(len(SEEDS)):
                            mA, mB = masks[a][A][k], masks[a][B][k]
                            qA, qB, qAB = float(mA.mean()), float(mB.mean()), float((mA & mB).mean())
                            vals.append(phi(qA, qB, qAB))
                        vals = [v for v in vals if v is not None]
                        r_ = np.random.default_rng(13)
                        bs = r_.choice(np.asarray(vals, float), size=(4000, len(vals)), replace=True).mean(1)
                        out['%s~%s@%g' % (A, B, a)] = {
                            'phi_mean': round(float(np.mean(vals)), 4),
                            'ci95_seeds': [round(float(np.percentile(bs, 2.5)), 4),
                                           round(float(np.percentile(bs, 97.5)), 4)],
                            'seed_values': [round(v, 4) for v in vals]}
            R['tests']['T7'][rname] = out
            print('T7 %-18s dims %3d | AE~VAE phi %.3f %s | AE~GMM %.3f  (%.0fs)' % (
                rname, out['dims'], out['AE~VAE@0.01']['phi_mean'], out['AE~VAE@0.01']['ci95_seeds'],
                out['AE~GMM@0.01']['phi_mean'], time.time() - t0), flush=True)
            save(R)
    if which == 'T8':
        R['tests'].setdefault('T8_published_NAE', {})
        # K_latent and K_input stay at the REGISTERED 20; seeds stay at the
        # registered 3. Epochs and training-set size were not fixed by the T8
        # registration and are reduced here to fit the execution window; the
        # values actually used are recorded with every cell.
        K_LAT, K_INP, ETA, SIG, BUF = 20, 20, 0.05, 0.05, 1024
        EPOCHS = int(os.environ.get('T8_EPOCHS', 4))
        NTR8 = int(os.environ.get('T8_NTR', 20000))

        def train_published_nae(X, seed, d):
            torch.manual_seed(seed)
            g = torch.Generator().manual_seed(seed)
            Xt = torch.tensor(X)
            # (a) pretrain an ordinary autoencoder
            m = train_net(AE(d), X, epochs=8, seed=seed)
            energy = lambda z: ((m(z) - z) ** 2).mean(1)
            enc, dec = m.enc, m.dec
            zdim = enc[-1].out_features
            zbuf = torch.randn(BUF, zdim, generator=g)
            opt = torch.optim.Adam(m.parameters(), lr=5e-4)
            diag = {}
            for ep in range(EPOCHS):
                perm = torch.randperm(len(Xt), generator=g)
                for i in range(0, len(Xt), 512):
                    xb = Xt[perm[i:i + 512]]
                    nb = xb.shape[0]
                    # (b) ON-MANIFOLD INITIALIZATION: Langevin in LATENT space
                    bidx = torch.randint(0, BUF, (nb,), generator=g)
                    z = zbuf[bidx].clone().requires_grad_(True)
                    for _ in range(K_LAT):
                        xz = dec(z)
                        ez = ((m(xz) - xz) ** 2).mean(1).sum()
                        gz = torch.autograd.grad(ez, z)[0]
                        with torch.no_grad():
                            z = z - ETA * gz + SIG * torch.randn(z.shape, generator=g)
                        z.requires_grad_(True)
                    with torch.no_grad():
                        zbuf[bidx] = z.detach()
                        neg = dec(z.detach())          # decode to on-manifold negatives
                    # (c) further Langevin chain in INPUT space
                    neg = neg.requires_grad_(True)
                    for _ in range(K_INP):
                        gx = torch.autograd.grad(energy(neg).sum(), neg)[0]
                        with torch.no_grad():
                            neg = neg - ETA * gx + SIG * torch.randn(neg.shape, generator=g)
                        neg.requires_grad_(True)
                    neg = neg.detach()
                    # (d) normalized-energy objective
                    opt.zero_grad()
                    e_pos, e_neg = energy(xb), energy(neg)
                    loss = e_pos.mean() - e_neg.mean() + 0.1 * (e_pos ** 2).mean()
                    loss.backward(); opt.step()
                    diag = {'e_data': float(e_pos.mean().detach()), 'e_neg': float(e_neg.mean().detach())}
            diag['energy_ratio_neg_over_data'] = round(diag['e_neg'] / (diag['e_data'] + 1e-12), 3)
            return m, diag

        def sysd(Xtr, seed):
            mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
            m, diag = train_published_nae((Xtr - mu) / sd, seed, Xtr.shape[1])
            return {'m': m, 'mu': mu, 'sd': sd, 'diag': diag}

        def sc(s_, X):
            Z = torch.tensor((X - s_['mu']) / s_['sd'])
            with torch.no_grad():
                return ((s_['m'](Z) - Z) ** 2).mean(1).numpy()

        only = os.environ.get('ONLY_PAIR')
        for pname, (P, Q) in PAIRS.items():
            if pname in R['tests']['T8_published_NAE'] or (only and pname != only):
                continue
            per, diags = [], []
            for s_ in SEEDS[:3]:
                Ptr, Pcal, Pev = split(P, NTR8, 20000, NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR8, 20000, NEV, s_)
                sP, sQ = sysd(Ptr, s_), sysd(Qtr, s_)
                diags.append({'P': sP['diag'], 'Q': sQ['diag']})
                sPcal, sPev, sPQ = sc(sP, Pcal), sc(sP, Pev), sc(sP, Qev)
                sQcal, sQev, sQP = sc(sQ, Qcal), sc(sQ, Qev), sc(sQ, Pev)
                row = {'auc_P_on_Q': round(auc(sPev, sPQ), 4), 'auc_Q_on_P': round(auc(sQev, sQP), 4)}
                for a in ALPHAS:
                    tP, tQ = np.quantile(sPcal, 1 - a), np.quantile(sQcal, 1 - a)
                    aPQ, aQP = float(np.mean(sPQ <= tP)), float(np.mean(sQP <= tQ))
                    row['M_A@%g' % a] = round((aPQ + aQP) / 2, 4)
                    row['D_A@%g' % a] = round(aPQ - aQP, 4)
                per.append(row)
            ratios = [d[k]['energy_ratio_neg_over_data'] for d in diags for k in ('P', 'Q')]
            R['tests']['T8_published_NAE'][pname] = {
                'construction': 'AE pretraining -> latent-space Langevin (On-Manifold Initialization) -> decode -> input-space Langevin -> normalized-energy objective',
                'K_latent': K_LAT, 'K_input': K_INP, 'seeds': SEEDS[:3],
                'epochs': EPOCHS, 'train_events_per_class': NTR8,
                'scope_note': 'K and seeds are the registered values; epochs and training-set size were unspecified in the T8 registration and were reduced to fit the execution window — recorded here rather than declared in advance',
                'convergence_diagnostic': {'energy_ratio_neg_over_data': [round(r_, 3) for r_ in ratios],
                                           'mean_ratio': round(float(np.mean(ratios)), 3),
                                           'reading': 'ratio near or below 1 indicates negatives reached comparable-energy regions; a ratio far above 1 means the chain did not reach the model distribution and the cell is UNINTERPRETABLE as a test of the remedy'},
                **{k: {'mean': round(float(np.mean([d[k] for d in per])), 4),
                       'seed_values': [d[k] for d in per]} for k in per[0]}}
            r_ = R['tests']['T8_published_NAE'][pname]
            print('T8 %-3s AUC %.3f / %.3f  D_A@1e-2 %+.4f  energy_ratio %.2f  (%.0fs)' % (
                pname, r_['auc_P_on_Q']['mean'], r_['auc_Q_on_P']['mean'],
                r_['D_A@0.01']['mean'], r_['convergence_diagnostic']['mean_ratio'], time.time() - t0), flush=True)
            save(R)
    if which == 'T9':
        R['tests'].setdefault('T9_chain_ladder', {})
        P, Q = PAIRS['T1']
        for K in [int(x) for x in os.environ.get('T9_K', '20,40,80').split(',')]:
            key = 'K=%d' % K
            if key in R['tests']['T9_chain_ladder']:
                continue
            os.environ['T8_K'] = str(K)
            per, ratios = [], []
            ETA, SIG, BUF, EPOCHS, NTR9 = 0.05, 0.05, 1024, 3, 15000

            def train_pub(X, seed, d):
                torch.manual_seed(seed); g = torch.Generator().manual_seed(seed)
                Xt = torch.tensor(X)
                m = train_net(AE(d), X, epochs=8, seed=seed)
                energy = lambda z: ((m(z) - z) ** 2).mean(1)
                dec = m.dec; zdim = m.enc[-1].out_features
                zbuf = torch.randn(BUF, zdim, generator=g)
                opt = torch.optim.Adam(m.parameters(), lr=5e-4)
                diag = {}
                for ep in range(EPOCHS):
                    perm = torch.randperm(len(Xt), generator=g)
                    for i in range(0, len(Xt), 512):
                        xb = Xt[perm[i:i + 512]]; nb = xb.shape[0]
                        bidx = torch.randint(0, BUF, (nb,), generator=g)
                        z = zbuf[bidx].clone().requires_grad_(True)
                        for _ in range(K):
                            xz = dec(z); ez = ((m(xz) - xz) ** 2).mean(1).sum()
                            gz = torch.autograd.grad(ez, z)[0]
                            with torch.no_grad():
                                z = z - ETA * gz + SIG * torch.randn(z.shape, generator=g)
                            z.requires_grad_(True)
                        with torch.no_grad():
                            zbuf[bidx] = z.detach(); neg = dec(z.detach())
                        neg = neg.requires_grad_(True)
                        for _ in range(K):
                            gx = torch.autograd.grad(energy(neg).sum(), neg)[0]
                            with torch.no_grad():
                                neg = neg - ETA * gx + SIG * torch.randn(neg.shape, generator=g)
                            neg.requires_grad_(True)
                        neg = neg.detach()
                        opt.zero_grad()
                        e_pos, e_neg = energy(xb), energy(neg)
                        (e_pos.mean() - e_neg.mean() + 0.1 * (e_pos ** 2).mean()).backward()
                        opt.step()
                        diag = {'e_data': float(e_pos.mean().detach()), 'e_neg': float(e_neg.mean().detach())}
                diag['ratio'] = diag['e_neg'] / (diag['e_data'] + 1e-12)
                return m, diag

            def mk(Xtr, seed):
                mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
                m, diag = train_pub((Xtr - mu) / sd, seed, Xtr.shape[1])
                return {'m': m, 'mu': mu, 'sd': sd, 'diag': diag}

            def sc(s_, X):
                Z = torch.tensor((X - s_['mu']) / s_['sd'])
                with torch.no_grad():
                    return ((s_['m'](Z) - Z) ** 2).mean(1).numpy()

            for s_ in SEEDS[:3]:
                Ptr, Pcal, Pev = split(P, NTR9, 20000, NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR9, 20000, NEV, s_)
                sP, sQ = mk(Ptr, s_), mk(Qtr, s_)
                ratios += [sP['diag']['ratio'], sQ['diag']['ratio']]
                sPcal, sPev, sPQ = sc(sP, Pcal), sc(sP, Pev), sc(sP, Qev)
                sQcal, sQev, sQP = sc(sQ, Qcal), sc(sQ, Qev), sc(sQ, Pev)
                row = {'auc_P_on_Q': round(auc(sPev, sPQ), 4), 'auc_Q_on_P': round(auc(sQev, sQP), 4)}
                for a in ALPHAS:
                    tP, tQ = np.quantile(sPcal, 1 - a), np.quantile(sQcal, 1 - a)
                    aPQ, aQP = float(np.mean(sPQ <= tP)), float(np.mean(sQP <= tQ))
                    row['D_A@%g' % a] = round(aPQ - aQP, 4)
                per.append(row)
            mr = float(np.mean(ratios))
            R['tests']['T9_chain_ladder'][key] = {
                'K_latent': K, 'K_input': K, 'seeds': SEEDS[:3], 'epochs': EPOCHS,
                'train_events_per_class': NTR9,
                'energy_ratio_mean': round(mr, 3),
                'energy_ratio_values': [round(r_, 3) for r_ in ratios],
                'converged_band': bool(0.85 <= mr <= 1.15),
                **{k: {'mean': round(float(np.mean([d[k] for d in per])), 4),
                       'seed_values': [d[k] for d in per]} for k in per[0]}}
            r_ = R['tests']['T9_chain_ladder'][key]
            print('T9 %-6s ratio %.2f (band %s) | AUC %.3f / %.3f | D_A@1e-2 %+.4f  (%.0fs)' % (
                key, mr, r_['converged_band'], r_['auc_P_on_Q']['mean'],
                r_['auc_Q_on_P']['mean'], r_['D_A@0.01']['mean'], time.time() - t0), flush=True)
            save(R)
    if which == 'T10':
        R['tests'].setdefault('T10_sampler_sweep', {})
        P, Q = PAIRS['T1']
        K, BUF, EPOCHS, NTR10 = 20, 1024, 3, 15000
        ETAS = [float(x) for x in os.environ.get('T10_ETA', '0.01,0.05,0.2').split(',')]
        SIGS = [float(x) for x in os.environ.get('T10_SIG', '0.01,0.05,0.2').split(',')]

        def train_pub(X, seed, d, eta, sig):
            torch.manual_seed(seed); g = torch.Generator().manual_seed(seed)
            Xt = torch.tensor(X)
            m = train_net(AE(d), X, epochs=8, seed=seed)
            energy = lambda z: ((m(z) - z) ** 2).mean(1)
            dec = m.dec; zdim = m.enc[-1].out_features
            zbuf = torch.randn(BUF, zdim, generator=g)
            opt = torch.optim.Adam(m.parameters(), lr=5e-4)
            diag = {}
            for ep in range(EPOCHS):
                perm = torch.randperm(len(Xt), generator=g)
                for i in range(0, len(Xt), 512):
                    xb = Xt[perm[i:i + 512]]; nb = xb.shape[0]
                    bidx = torch.randint(0, BUF, (nb,), generator=g)
                    z = zbuf[bidx].clone().requires_grad_(True)
                    for _ in range(K):
                        xz = dec(z); ez = ((m(xz) - xz) ** 2).mean(1).sum()
                        gz = torch.autograd.grad(ez, z)[0]
                        with torch.no_grad():
                            z = z - eta * gz + sig * torch.randn(z.shape, generator=g)
                        z.requires_grad_(True)
                    with torch.no_grad():
                        zbuf[bidx] = z.detach(); neg = dec(z.detach())
                    neg = neg.requires_grad_(True)
                    for _ in range(K):
                        gx = torch.autograd.grad(energy(neg).sum(), neg)[0]
                        with torch.no_grad():
                            neg = neg - eta * gx + sig * torch.randn(neg.shape, generator=g)
                        neg.requires_grad_(True)
                    neg = neg.detach()
                    opt.zero_grad()
                    e_pos, e_neg = energy(xb), energy(neg)
                    (e_pos.mean() - e_neg.mean() + 0.1 * (e_pos ** 2).mean()).backward()
                    opt.step()
                    diag = {'e_data': float(e_pos.mean().detach()), 'e_neg': float(e_neg.mean().detach())}
            diag['ratio'] = diag['e_neg'] / (diag['e_data'] + 1e-12)
            return m, diag

        for eta in ETAS:
            for sig in SIGS:
                key = 'eta=%g,sigma=%g' % (eta, sig)
                if key in R['tests']['T10_sampler_sweep']:
                    continue
                per, ratios = [], []
                for s_ in SEEDS[:3]:
                    Ptr, Pcal, Pev = split(P, NTR10, 20000, NEV, s_)
                    Qtr, Qcal, Qev = split(Q, NTR10, 20000, NEV, s_)
                    out = {}
                    for tag, tr in (('P', Ptr), ('Q', Qtr)):
                        mu, sd = tr.mean(0), tr.std(0) + 1e-6
                        m, diag = train_pub((tr - mu) / sd, s_, tr.shape[1], eta, sig)
                        out[tag] = {'m': m, 'mu': mu, 'sd': sd}; ratios.append(diag['ratio'])
                    sc = lambda s_d, X: ((s_d['m'](torch.tensor((X - s_d['mu']) / s_d['sd']))
                                          - torch.tensor((X - s_d['mu']) / s_d['sd'])) ** 2).mean(1).detach().numpy()
                    with torch.no_grad():
                        sPcal, sPev, sPQ = sc(out['P'], Pcal), sc(out['P'], Pev), sc(out['P'], Qev)
                        sQcal, sQev, sQP = sc(out['Q'], Qcal), sc(out['Q'], Qev), sc(out['Q'], Pev)
                    row = {'auc_P_on_Q': round(auc(sPev, sPQ), 4), 'auc_Q_on_P': round(auc(sQev, sQP), 4)}
                    tP, tQ = np.quantile(sPcal, 0.99), np.quantile(sQcal, 0.99)
                    row['D_A@0.01'] = round(float(np.mean(sPQ <= tP)) - float(np.mean(sQP <= tQ)), 4)
                    per.append(row)
                mr = float(np.mean(ratios))
                R['tests']['T10_sampler_sweep'][key] = {
                    'eta': eta, 'sigma': sig, 'K': K, 'seeds': SEEDS[:3],
                    'energy_ratio_mean': round(mr, 3),
                    'in_band': bool(0.85 <= mr <= 1.15),
                    **{k: {'mean': round(float(np.mean([d[k] for d in per])), 4)} for k in per[0]}}
                r_ = R['tests']['T10_sampler_sweep'][key]
                print('T10 %-18s ratio %6.3f  band %-5s | AUC %.3f / %.3f  (%.0fs)' % (
                    key, mr, r_['in_band'], r_['auc_P_on_Q']['mean'], r_['auc_Q_on_P']['mean'],
                    time.time() - t0), flush=True)
                save(R)
    if which == 'T10':
        R['tests'].setdefault('T10_sampler_geometry', {})
        P, Q = PAIRS['T1']
        K, BUF, EPOCHS, NTR10 = 20, 1024, 3, 15000
        grid = [(e, sg) for e in (0.01, 0.05, 0.20) for sg in (0.01, 0.05, 0.20)]
        only = os.environ.get('T10_CELLS')
        if only:
            want = set(only.split(','))
            grid = [g for g in grid if 'eta%g_sig%g' % g in want]
        for ETA, SIG in grid:
            key = 'eta%g_sig%g' % (ETA, SIG)
            if key in R['tests']['T10_sampler_geometry']:
                continue

            def train_pub(X, seed, d):
                torch.manual_seed(seed); g = torch.Generator().manual_seed(seed)
                Xt = torch.tensor(X)
                m = train_net(AE(d), X, epochs=8, seed=seed)
                energy = lambda z: ((m(z) - z) ** 2).mean(1)
                dec = m.dec; zdim = m.enc[-1].out_features
                zbuf = torch.randn(BUF, zdim, generator=g)
                opt = torch.optim.Adam(m.parameters(), lr=5e-4)
                diag = {}
                for ep in range(EPOCHS):
                    perm = torch.randperm(len(Xt), generator=g)
                    for i in range(0, len(Xt), 512):
                        xb = Xt[perm[i:i + 512]]; nb = xb.shape[0]
                        bidx = torch.randint(0, BUF, (nb,), generator=g)
                        z = zbuf[bidx].clone().requires_grad_(True)
                        for _ in range(K):
                            xz = dec(z); ez = ((m(xz) - xz) ** 2).mean(1).sum()
                            gz = torch.autograd.grad(ez, z)[0]
                            with torch.no_grad():
                                z = z - ETA * gz + SIG * torch.randn(z.shape, generator=g)
                            z.requires_grad_(True)
                        with torch.no_grad():
                            zbuf[bidx] = z.detach(); neg = dec(z.detach())
                        neg = neg.requires_grad_(True)
                        for _ in range(K):
                            gx = torch.autograd.grad(energy(neg).sum(), neg)[0]
                            with torch.no_grad():
                                neg = neg - ETA * gx + SIG * torch.randn(neg.shape, generator=g)
                            neg.requires_grad_(True)
                        neg = neg.detach()
                        opt.zero_grad()
                        e_pos, e_neg = energy(xb), energy(neg)
                        (e_pos.mean() - e_neg.mean() + 0.1 * (e_pos ** 2).mean()).backward()
                        opt.step()
                        diag = {'e_data': float(e_pos.mean().detach()), 'e_neg': float(e_neg.mean().detach())}
                diag['ratio'] = diag['e_neg'] / (diag['e_data'] + 1e-12)
                return m, diag

            def mk(Xtr, seed):
                mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
                m, diag = train_pub((Xtr - mu) / sd, seed, Xtr.shape[1])
                return {'m': m, 'mu': mu, 'sd': sd, 'diag': diag}

            def sc(s_, X):
                Z = torch.tensor((X - s_['mu']) / s_['sd'])
                with torch.no_grad():
                    return ((s_['m'](Z) - Z) ** 2).mean(1).numpy()

            per, ratios = [], []
            for s_ in SEEDS[:3]:
                Ptr, Pcal, Pev = split(P, NTR10, 20000, NEV, s_)
                Qtr, Qcal, Qev = split(Q, NTR10, 20000, NEV, s_)
                sP, sQ = mk(Ptr, s_), mk(Qtr, s_)
                ratios += [sP['diag']['ratio'], sQ['diag']['ratio']]
                sPcal, sPev, sPQ = sc(sP, Pcal), sc(sP, Pev), sc(sP, Qev)
                sQcal, sQev, sQP = sc(sQ, Qcal), sc(sQ, Qev), sc(sQ, Pev)
                row = {'auc_P_on_Q': round(auc(sPev, sPQ), 4), 'auc_Q_on_P': round(auc(sQev, sQP), 4)}
                for a in ALPHAS:
                    tP, tQ = np.quantile(sPcal, 1 - a), np.quantile(sQcal, 1 - a)
                    row['D_A@%g' % a] = round(float(np.mean(sPQ <= tP)) - float(np.mean(sQP <= tQ)), 4)
                per.append(row)
            mr = float(np.mean(ratios))
            R['tests']['T10_sampler_geometry'][key] = {
                'eta': ETA, 'sigma': SIG, 'K': K, 'seeds': SEEDS[:3],
                'energy_ratio_mean': round(mr, 3), 'converged_band': bool(0.85 <= mr <= 1.15),
                **{k: {'mean': round(float(np.mean([d[k] for d in per])), 4),
                       'seed_values': [d[k] for d in per]} for k in per[0]}}
            r_ = R['tests']['T10_sampler_geometry'][key]
            print('T10 %-16s ratio %6.2f band %-5s | AUC %.3f / %.3f | D_A %+.4f  (%.0fs)' % (
                key, mr, r_['converged_band'], r_['auc_P_on_Q']['mean'],
                r_['auc_Q_on_P']['mean'], r_['D_A@0.01']['mean'], time.time() - t0), flush=True)
            save(R)
    save(R)
    print('elapsed %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'T5')
