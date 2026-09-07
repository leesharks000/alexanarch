#!/usr/bin/env python3
"""
operation_axis.py — the reference implementation of the instrument described in
"Measuring the Operation, Not the Name" (Sharks 2026).

Four procedures, one feature model:

  profile(tokens)            function-word / trigram / ending profiles on blocks
  axis(corpus)               unsupervised: PC1 and k-means over blocks; no labels
  attribute(train, test)     supervised: leave-one-TEXT-out nearest centroid
  project(train, held_out)   train on one set, score another it never saw

Nothing here is specific to Greek, to philosophy, or to the archive. The
instrument takes tokenized texts and returns numbers. What the numbers mean is
decided by the controls (see the paper, §5), not by this file.

Public domain / CC0. Reproduce, break, report.
"""
import re, unicodedata
from collections import Counter
import numpy as np

# ---------------------------------------------------------------- tokenization

GREEK = r'[\u0370-\u03FF\u1F00-\u1FFF]+'
LATIN = r"[A-Za-zÄÖÜäöüßÀ-ÿ]+"

# Elision and movable-nu are EDITORIAL conventions, not authorial ones: editions
# differ, and the difference can correlate with the partition you are testing.
# Normalize them or your first axis may be your editors'. (Paper §4.2.)
GREEK_ELISION = {
    'δ':'δε','αλλ':'αλλα','ουδ':'ουδε','μηδ':'μηδε','τ':'τε','γ':'γε',
    'καθ':'κατα','κατ':'κατα','μετ':'μετα','μεθ':'μετα','επ':'επι','εφ':'επι',
    'υπ':'υπο','υφ':'υπο','απ':'απο','αφ':'απο','παρ':'παρα','δι':'δια',
    'ανθ':'αντι','αντ':'αντι','ουκ':'ου','ουχ':'ου','ουχι':'ου',
    'εστιν':'εστι','εισιν':'εισι','ταυτ':'ταυτα','ταυθ':'ταυτα',
    'τουτ':'τουτο','τουθ':'τουτο','ωστ':'ωστε','ετ':'ετι','οτ':'οτι',
    'μ':'με','σ':'σε',
}

def strip_accents(w):
    return ''.join(c for c in unicodedata.normalize('NFD', w.lower())
                   if unicodedata.category(c) != 'Mn')

def tokenize(text, script='greek', normalize_elision=True):
    pat = GREEK if script == 'greek' else LATIN
    ws = re.findall(pat, text)
    if script == 'greek':
        ws = [strip_accents(w).replace('ς', 'σ') for w in ws]
        if normalize_elision:
            ws = [GREEK_ELISION.get(w, w) for w in ws]
    else:
        ws = [w.lower() for w in ws]
    return ws

def strip_tei(xml, drop_speakers=True):
    """TEI → plain text. Drops the apparatus, which is the editor's, and
    optionally speaker labels, which are the copyist's."""
    x = re.sub(r'<teiHeader.*?</teiHeader>', '', xml, flags=re.S)
    x = re.sub(r'<(note|app|rdg|bibl)[^>]*>.*?</\1>', '', x, flags=re.S)
    if drop_speakers:
        x = re.sub(r'<(speaker|label)[^>]*>.*?</\1>', '', x, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', x)

# -------------------------------------------------------------- feature models

def f_function_words(ws, maxlen=5):
    """Short words. In Greek maxlen=5 captures the particles and articles; in
    German and English use 6. This is the classic authorship feature."""
    return [w for w in ws if len(w) <= maxlen]

def f_trigrams(ws):
    out = []
    for w in ws:
        s = '_' + w + '_'
        out += [s[i:i+3] for i in range(len(s) - 2)]
    return out

def f_endings(ws):
    return ([w[-2:] for w in ws if len(w) >= 3] +
            ['3:' + w[-3:] for w in ws if len(w) >= 4])

FAMILIES = {'function_words': (f_function_words, 120),
            'trigrams':       (f_trigrams, 400),
            'endings':        (f_endings, 300)}

# ------------------------------------------------------------------- profiling

def blocks(corpus, feature, topk, size=1000, vocab=None):
    """corpus: {name: [tokens]}. Returns (X, labels, vocab).
    Features are relative frequencies within each block; X is z-scored across
    blocks. Blocks, not whole texts: a text is not one observation."""
    if vocab is None:
        cnt = Counter()
        for ws in corpus.values():
            cnt.update(feature(ws))
        vocab = [k for k, _ in cnt.most_common(topk)]
    idx = {k: i for i, k in enumerate(vocab)}
    X, L = [], []
    for name, ws in corpus.items():
        for i in range(0, len(ws) - size + 1, size):
            c = Counter(feature(ws[i:i+size])); tot = sum(c.values())
            if tot < size // 20:
                continue
            v = np.zeros(len(vocab))
            for k, n in c.items():
                if k in idx:
                    v[idx[k]] = n / tot
            X.append(v); L.append(name)
    X = np.array(X)
    return X, np.array(L), vocab

def zscore(X):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    return (X - mu) / sd, mu, sd

# ------------------------------------------------------------------ procedures

def axis(corpus, family='function_words', size=1000, anchor=None):
    """UNSUPERVISED. Returns the first principal axis over blocks, per-text
    means, and the k=2 clustering. No labels are used anywhere. `anchor` names a
    text that should score negative, fixing the sign so runs are comparable."""
    feature, topk = FAMILIES[family]
    X, L, vocab = blocks(corpus, feature, topk, size)
    Z, _, _ = zscore(X)
    U, S, Vt = np.linalg.svd(Z - Z.mean(0), full_matrices=False)
    pc = (Z - Z.mean(0)) @ Vt[0]
    if anchor is not None and pc[L == anchor].mean() > 0:
        pc = -pc
    means = {t: float(pc[L == t].mean()) for t in dict.fromkeys(L)}
    return {'pc1': pc, 'labels': L, 'per_text': means,
            'variance_explained': float(S[0]**2 / (S**2).sum()),
            'loadings': dict(sorted(zip(vocab, Vt[0]), key=lambda kv: -abs(kv[1]))[:25]),
            'clusters': kmeans2(Z)}

def kmeans2(Z, restarts=20, iters=100, seed=0):
    rng = np.random.default_rng(seed); best = None
    for _ in range(restarts):
        C = Z[rng.choice(len(Z), 2, replace=False)]
        for _ in range(iters):
            a = ((Z[:, None, :] - C[None])**2).sum(2).argmin(1)
            C2 = np.array([Z[a == j].mean(0) if (a == j).any() else C[j] for j in range(2)])
            if np.allclose(C2, C): break
            C = C2
        inertia = ((Z - C[a])**2).sum()
        if best is None or inertia < best[0]: best = (inertia, a)
    return best[1]

def attribute(corpus, group_of, family='function_words', size=1000, fold_vocab=True):
    """SUPERVISED, with the fold sealed. Leave-one-TEXT-out nearest centroid, and
    — this is the repair of v0.2, which fitted both on the whole corpus —
    VOCABULARY AND SCALING ARE FITTED INSIDE EACH FOLD. Returns balanced accuracy,
    class recalls and the confusion matrix, because a bare accuracy hides which
    class is being missed, and block- and text-weighted accuracy, because long
    texts otherwise dominate.

    fold_vocab=False falls back to a corpus-wide vocabulary. That is legitimate
    ONLY inside a permutation comparison, where every labeling sees the identical
    feature space and the selection is label-independent; it is not held-out
    vocabulary selection, and any table produced with it must say so."""
    feature, topk = FAMILIES[family]
    B = {k: [v[i:i+size] for i in range(0, len(v) - size + 1, size)] for k, v in corpus.items()}
    B = {k: v for k, v in B.items() if v}
    fixed = None
    if not fold_vocab:
        cnt = Counter()
        for k in B:
            for b in B[k]: cnt.update(feature(b))
        fixed = [w for w, _ in cnt.most_common(topk)]
    per = {}; conf = Counter()
    for t in B:
        tr = [k for k in B if k != t]
        groups = {group_of(k) for k in tr}
        if len(groups) < 2: continue
        if fixed is None:
            cnt = Counter()
            for k in tr:
                for b in B[k]: cnt.update(feature(b))
            vocab = [w for w, _ in cnt.most_common(topk)]
        else:
            vocab = fixed
        Xtr = np.vstack([_vecs(B[k], feature, vocab) for k in tr])
        Ltr = np.concatenate([[k] * len(B[k]) for k in tr])
        mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
        Ztr = (Xtr - mu) / sd
        G = np.array([group_of(k) for k in Ltr])
        cent = {g: Ztr[G == g].mean(0) for g in groups}
        Zte = (_vecs(B[t], feature, vocab) - mu) / sd
        pred = [min(cent, key=lambda g: np.linalg.norm(z - cent[g])) for z in Zte]
        truth = group_of(t); per[t] = float(np.mean([p == truth for p in pred]))
        for p in pred: conf[(truth, p)] += 1
    gs = sorted({group_of(t) for t in per})
    rec = {g: conf[(g, g)] / max(1, sum(conf[(g, h)] for h in gs)) for g in gs}
    tot = sum(conf.values())
    return {'balanced': float(np.mean(list(rec.values()))),
            'block_accuracy': sum(conf[(g, g)] for g in gs) / max(1, tot),
            'text_accuracy': float(np.mean(list(per.values()))) if per else 0.0,
            'recalls': rec, 'confusion': {f'{a}->{b}': c for (a, b), c in conf.items()},
            'per_text': per, 'n_blocks': tot,
            'majority_baseline': max(Counter([group_of(t) for t in per]).values()) / max(1, len(per)),
            'fold_vocab': fold_vocab}


def _vecs(bs, feature, vocab):
    idx = {w: i for i, w in enumerate(vocab)}
    out = []
    for b in bs:
        c = Counter(feature(b)); tot = sum(c.values()); v = np.zeros(len(vocab))
        for w, n in c.items():
            if w in idx: v[idx[w]] = n / tot
        out.append(v)
    return np.array(out)


def permutation_null(corpus, group_of, family='function_words', size=1000, n=150, seed=0):
    """Text-level label permutation preserving class counts — the comparator that
    makes an accuracy figure mean something. Uses fold_vocab=False by design:
    every labeling must see the identical feature space, and frequency-based
    selection uses no labels."""
    rng = np.random.default_rng(seed)
    texts = list(corpus); labs = [group_of(t) for t in texts]
    out = []
    for _ in range(n):
        m = dict(zip(texts, rng.permutation(labs)))
        out.append(attribute(corpus, lambda k: m[k], family, size, fold_vocab=False)['balanced'])
    return np.array(out)


def compare_partitions(corpus, a_of, b_of, family='function_words', size=1000, n=150, seed=0):
    """Two partitions of ONE corpus, and a null for the DIFFERENCE — separate
    nulls for each do not test whether the gap between them is reliable."""
    A = attribute(corpus, a_of, family, size, fold_vocab=False)['balanced']
    Bv = attribute(corpus, b_of, family, size, fold_vocab=False)['balanced']
    rng = np.random.default_rng(seed); texts = list(corpus)
    labs = [b_of(t) for t in texts]; diffs = []
    for _ in range(n):
        m = dict(zip(texts, rng.permutation(labs)))
        diffs.append(attribute(corpus, lambda k: m[k], family, size, fold_vocab=False)['balanced'] - A)
    diffs = np.array(diffs)
    return {'a': A, 'b': Bv, 'difference': Bv - A, 'null_mean': float(diffs.mean()),
            'p_difference': float((diffs >= (Bv - A)).mean())}


def matched_removal(corpus, group_of, removed, family='function_words', size=1000, n=120, seed=0):
    """Before attributing a drop to what you removed, remove something else the
    same shape. Draws removals with the same per-class counts and reports where
    the real removal falls among them."""
    import itertools
    feature, topk = FAMILIES[family]
    real = attribute({k: v for k, v in corpus.items() if k not in removed}, group_of,
                     family, size, fold_vocab=False)['balanced']
    byg = {}
    for k in corpus: byg.setdefault(group_of(k), []).append(k)
    counts = Counter(group_of(k) for k in removed)
    pools = [list(itertools.combinations(byg[g], c)) for g, c in counts.items()]
    rng = np.random.default_rng(seed); vals = []
    for _ in range(n):
        pick = tuple(x for p in pools for x in p[rng.integers(len(p))])
        if set(pick) == set(removed): continue
        vals.append(attribute({k: v for k, v in corpus.items() if k not in pick}, group_of,
                              family, size, fold_vocab=False)['balanced'])
    vals = np.array(vals)
    return {'real': real, 'matched_mean': float(vals.mean()), 'matched_sd': float(vals.std()),
            'fraction_at_or_below_real': float((vals <= real).mean()), 'n': len(vals)}

def project(train, group_of, held_out, family='function_words', size=1000):
    """Train centroids on one corpus; score texts it never saw. Vocabulary,
    standardization and centroids all come from `train`. This is the only
    procedure that can test a hypothesis rather than describe a corpus."""
    feature, topk = FAMILIES[family]
    X, L, vocab = blocks(train, feature, topk, size)
    Z, mu, sd = zscore(X)
    G = np.array([group_of(l) for l in L])
    cent = {g: Z[G == g].mean(0) for g in set(G)}
    if len(cent) != 2:
        raise ValueError('project() expects exactly two training groups')
    a, b = sorted(cent)
    Y, LY, _ = blocks(held_out, feature, topk, size, vocab=vocab)
    Zy = (Y - mu) / sd
    out = {}
    for t in dict.fromkeys(LY):
        z = Zy[LY == t]
        lean = np.linalg.norm(z - cent[b], axis=1) - np.linalg.norm(z - cent[a], axis=1)
        out[t] = {'n_blocks': int(len(z)), 'mean_lean': float(lean.mean()),
                  f'pct_nearer_{a}': float((lean > 0).mean())}
    return {'toward': a, 'away': b, 'texts': out}

def localize(text_tokens, train, group_of, family='function_words',
             window=1000, step=250):
    """Where inside one text does the lean move? Rolling windows on a fixed
    axis. Use it to find seams; do not use it to find single sentences."""
    feature, topk = FAMILIES[family]
    X, L, vocab = blocks(train, feature, topk, window)
    Z, mu, sd = zscore(X)
    G = np.array([group_of(l) for l in L]); cent = {g: Z[G == g].mean(0) for g in set(G)}
    a, b = sorted(cent)
    idx = {k: i for i, k in enumerate(vocab)}
    out = []
    for i in range(0, len(text_tokens) - window + 1, step):
        c = Counter(feature(text_tokens[i:i+window])); tot = sum(c.values())
        v = np.zeros(len(vocab))
        for k, n in c.items():
            if k in idx: v[idx[k]] = n / tot
        z = (v - mu) / sd
        out.append((i, float(np.linalg.norm(z - cent[b]) - np.linalg.norm(z - cent[a]))))
    return out

# ------------------------------------------------------------------- reporting

def report(corpus, group_of, anchor=None, families=('function_words','trigrams','endings')):
    """The minimum report the protocol requires: every family, the unsupervised
    axis, the supervised accuracy against its own baseline, and the agreement
    between the axis and the labels. Publish all three families or none."""
    rows = []
    for fam in families:
        A = axis(corpus, fam, anchor=anchor)
        S = attribute(corpus, group_of, fam)
        gs = sorted({group_of(t) for t in corpus})
        agree = None
        if len(gs) == 2:
            neg = [t for t in A['per_text'] if A['per_text'][t] < 0]
            agree = max(
                sum(1 for t in A['per_text'] if (t in neg) == (group_of(t) == gs[0])),
                sum(1 for t in A['per_text'] if (t in neg) == (group_of(t) == gs[1])),
            ) / len(A['per_text'])
        rows.append({'family': fam, 'pc1_variance': A['variance_explained'],
                     'axis_agrees_with_labels': agree,
                     'attribution_accuracy': S['accuracy'], 'baseline': S['baseline']})
    return rows

if __name__ == '__main__':
    print(__doc__)
    print('Import it. The controls of §5 are not optional:')
    print('  1. a bounded single-author corpus  → expect closed neighbours, high self-attribution')
    print('  2. distinct authors, one genre     → expect the instrument to recover the names')
    print('  3. a documented case               → project a known attribution and check it')
    print('  4. then, and only then, the corpus you are asking about')
