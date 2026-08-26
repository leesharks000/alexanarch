"""CPCE refit v1.1 — fitted to the 26 Aug 2026 Google captures (Detroit IP, signed-out).
Observed: q1 'operative semiotics'  — lineage at organic ranks (4,7,8) of ~18; overview cites 3 non-lineage sources, opens 'Operative (or operational)'.
          q2 'operational semiotics' — lineage at organic ranks (6,8,9,15) of ~20 (two snippets explicitly disambiguating); overview cites ~4 non-lineage sources.
Question A: odds of C=0 on both under a fair rank-weighted composer.
Question B: how strong must a lineage-specific authority gate be to make C=0 likely? (hypothesis-2 quantified)"""
import random

def p_c0_both(k1=3, k2=4, n1=18, n2=20, ranks1=(4,7,8), ranks2=(6,8,9,15), w_exp=1.0, gate=1.0, runs=40000, seed=7):
    rng = random.Random(seed)
    def draw(n, k, lineage, gate):
        w = [((1.0/(r+1))**w_exp) * (gate if (r+1) in lineage else 1.0) for r in range(n)]
        pool = list(range(n)); picks = set()
        for _ in range(k):
            tot = sum(w[i] for i in pool); x, acc = rng.random()*tot, 0.0
            for i in pool:
                acc += w[i]
                if acc >= x: picks.add(i+1); pool.remove(i); break
        return len(picks & set(lineage)) == 0
    return sum(draw(n1,k1,ranks1,gate) and draw(n2,k2,ranks2,gate) for _ in range(runs))/runs

print("A. Fair composer (gate=1), sensitivity over rank-weight exponent:")
for w in (0.0, 0.5, 1.0, 1.5):
    p = p_c0_both(w_exp=w)
    print(f"   w={w}: P(C=0 both) = {p:.4f}  → {1/p:,.0f}:1 against chance")
print("B. Gate-strength required to make the observation unremarkable (P≥0.5), at w=1.0:")
for g in (1.0, 0.5, 0.25, 0.1, 0.05, 0.02):
    p = p_c0_both(gate=g)
    flag = ' ← crosses 0.5' if p >= 0.5 else ''
    print(f"   gate={g}: P = {p:.3f}{flag}")
