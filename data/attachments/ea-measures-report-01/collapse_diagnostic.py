"""
collapse_diagnostic.py — a reference-free model-collapse self-diagnostic (v0.2).

Every measure below has a truth-value the model carries in itself; no human
anchor is used as a ruler (a prior snapshot may be passed for TRENDS only).
See EA-LO-COLLAPSE-DIAGNOSTIC-01 Part II.

  D      distinction sensitivity   d(M(p),M(p*)) / d(M(p),M(p')), p' and p* made by M
  N_eff  effective semantic modes  exp(entropy of meaning-clusters over K samples)
  X      cross-prompt convergence  mean centroid distance across unrelated probes
  G/R    Gambetta panel            Gini over top-100, collapsed-prediction ratio, entropy
  lam    self-consumption          dispersion ratio after in-context self-conditioning

Usage:
  python collapse_diagnostic.py --model gpt2 --probes probes.txt [--k 8] [--max_new 96]
      [--encoder sentence-transformers/all-MiniLM-L6-v2] [--snapshot prior.json]
      [--system_prompt file.txt]   # run once bare and once with the production scaffold
"""
import argparse, json, math, random, sys
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


# ------------------------------------------------------------- sampling
@torch.no_grad()
def generate(model, tok, prompt, max_new, device, prefix=None, stats=None):
    text = (prefix + "\n\n" if prefix else "") + prompt
    ids = tok(text, return_tensors="pt").input_ids.to(device)
    out = ids
    for _ in range(max_new):
        probs = torch.softmax(model(out).logits[0, -1].float(), -1)
        if stats is not None:
            s = torch.sort(probs, descending=True).values
            top = s[:100]; top = top / top.sum()
            n = len(top); i = torch.arange(1, n + 1, device=top.device).float()
            gini = float(1 - 2 * (top * (n - i + 0.5) / n).sum())          # Gambetta shortcut
            stats["gini"].append(gini)
            stats["collapsed"].append(float(s[0] >= 0.999))
            stats["entropy"].append(float(-(probs * torch.log(probs + 1e-12)).sum()))
        nxt = torch.multinomial(probs, 1)
        out = torch.cat([out, nxt.view(1, 1)], 1)
        if nxt.item() == tok.eos_token_id:
            break
    return tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()


def ask(model, tok, instruction, device, max_new=64):
    """One low-temperature completion for constructing p' and p*."""
    ids = tok(instruction, return_tensors="pt").input_ids.to(device)
    out = model.generate(ids, max_new_tokens=max_new, do_sample=True, temperature=0.3,
                         pad_token_id=tok.eos_token_id)
    return tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip().split("\n")[0]


# ------------------------------------------------------------- measures
def dispersion(X):
    return float(np.mean(np.linalg.norm(X - X.mean(0), axis=1)))


def effective_modes(X, thresh=0.25):
    """Greedy agglomeration by cosine distance; N_eff = exp(H over cluster masses)."""
    n = len(X); labels = -np.ones(n, int); c = 0
    for i in range(n):
        if labels[i] >= 0: continue
        labels[i] = c
        for j in range(i + 1, n):
            if labels[j] < 0 and 1 - float(X[i] @ X[j]) < thresh: labels[j] = c
        c += 1
    p = np.bincount(labels) / n
    return float(np.exp(-(p * np.log(p)).sum()))


def vendi(X, q=1.0):
    K = X @ X.T / len(X)
    w = np.clip(np.linalg.eigvalsh(K), 1e-12, None)
    return float(np.exp(-(w * np.log(w)).sum()))


# ------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--probes", required=True)
    ap.add_argument("--k", type=int, default=8); ap.add_argument("--max_new", type=int, default=96)
    ap.add_argument("--encoder", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--snapshot"); ap.add_argument("--system_prompt"); ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    random.seed(args.seed); torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model).to(device).eval()
    from sentence_transformers import SentenceTransformer
    enc = SentenceTransformer(args.encoder, device=device)
    scaffold = open(args.system_prompt).read().strip() if args.system_prompt else None
    probes = [l.strip() for l in open(args.probes) if l.strip()]

    stats = {"gini": [], "collapsed": [], "entropy": []}
    per_probe, centroids, D_vals = [], [], []
    for p in probes:
        # K samples of p, with the Gambetta panel collected on the way
        S = [generate(model, tok, p, args.max_new, device, scaffold, stats) for _ in range(args.k)]
        ES = enc.encode(S, normalize_embeddings=True)
        # distinction sensitivity: the model constructs p' and p*
        p_para = ask(model, tok, f"Rewrite the following question in different words, keeping its meaning exactly:\n{p}\nRewritten:", device)
        p_star = ask(model, tok, f"Rewrite the following question changing ONE detail so that the correct answer must be different:\n{p}\nChanged:", device)
        a  = generate(model, tok, p, args.max_new, device, scaffold)
        a1 = generate(model, tok, p_para, args.max_new, device, scaffold)
        a2 = generate(model, tok, p_star, args.max_new, device, scaffold)
        e_a, e1, e2 = enc.encode([a, a1, a2], normalize_embeddings=True)
        d_same = 1 - float(e_a @ e1); d_diff = 1 - float(e_a @ e2)
        D = d_diff / (d_same + 1e-6)
        D_vals.append(D); centroids.append(ES.mean(0))
        per_probe.append(dict(probe=p, p_para=p_para, p_star=p_star, D=D,
                              N_eff=effective_modes(ES), vendi=vendi(ES), dispersion=dispersion(ES)))

    C = np.array(centroids); X = float(np.mean([np.linalg.norm(C[i] - C[j])
                                                  for i in range(len(C)) for j in range(i + 1, len(C))])) if len(C) > 1 else None
    # self-consumption contraction (in-context proxy) on the first probe
    p0 = probes[0]
    S0 = [pp for pp in [generate(model, tok, p0, args.max_new, device, scaffold) for _ in range(args.k)]]
    ctx = "\n\n".join(S0)
    S1 = [generate(model, tok, p0, args.max_new, device, (scaffold + "\n\n" if scaffold else "") + ctx) for _ in range(args.k)]
    V0, V1 = dispersion(enc.encode(S0, normalize_embeddings=True)), dispersion(enc.encode(S1, normalize_embeddings=True))
    lam = V1 / V0 if V0 > 0 else float("nan")

    report = dict(model=args.model, condition="production" if scaffold else "base", n_probes=len(probes), k=args.k,
                  D_mean=float(np.mean(D_vals)), N_eff_mean=float(np.mean([r["N_eff"] for r in per_probe])),
                  vendi_mean=float(np.mean([r["vendi"] for r in per_probe])), X_cross_prompt=X,
                  gambetta=dict(gini=float(np.mean(stats["gini"])), collapsed_ratio=float(np.mean(stats["collapsed"])),
                                entropy=float(np.mean(stats["entropy"]))),
                  lam_in_context=lam, generations_to_halve=(math.log(0.5) / math.log(lam)) if 0 < lam < 1 else None,
                  per_probe=per_probe,
                  note="state only; no absolute degree of collapse is reported. Compare against a prior snapshot for trends.")
    if args.snapshot:
        s = json.load(open(args.snapshot))
        r = {k: min(1.0, report[k] / s[k]) for k in ("D_mean", "N_eff_mean", "X_cross_prompt") if s.get(k)}
        r["gini"] = min(1.0, s["gambetta"]["gini"] / report["gambetta"]["gini"])
        r["lam"] = min(1.0, lam)
        report["MCSD_vs_snapshot"] = 1 - float(np.prod(list(r.values())) ** (1 / len(r)))
        report["retention_ratios"] = r
    json.dump(report, sys.stdout, indent=2, default=float); print()


if __name__ == "__main__":
    main()
