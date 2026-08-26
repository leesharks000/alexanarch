"""suppression-lab v1.0 — three robust toys for the suppression-dynamics apparatus.
Seeded, swept, each keyed to a falsifiable claim. CC-BY-4.0, Crimson Hexagonal Archive."""
import random, math, statistics as st

# ── SIM 1: CPCE null model ─────────────────────────────────────────────
# Claim keyed: CPCE (apophasis v0.2 §8) is anomalous only against a fair
# congruence-weighted composer. Question: given lineage docs retrieved at
# observed ranks under BOTH queries, how often does a null composer pick
# zero lineage sources from both, by chance?
def cpce_null(runs=20000, k_sources=3, n_docs=10, lineage_ranks_q1=(3,6,8),
              lineage_ranks_q2=(2,4,7,9), rank_weight=1.0, seed=7):
    rng = random.Random(seed)
    def draw(lineage_ranks):
        w = [ (1.0/(r+1))**rank_weight for r in range(n_docs) ]
        picks, pool = set(), list(range(n_docs))
        for _ in range(k_sources):
            tot = sum(w[i] for i in pool)
            x, acc = rng.random()*tot, 0.0
            for i in pool:
                acc += w[i]
                if acc >= x: picks.add(i); pool.remove(i); break
        return any((r-1) in picks for r in lineage_ranks)  # ranks are 1-based
    both_zero = sum((not draw(lineage_ranks_q1)) and (not draw(lineage_ranks_q2)) for _ in range(runs))
    return both_zero/runs

p = cpce_null()
p_strong = cpce_null(lineage_ranks_q2=(1,2,4,7))  # lineage stronger under q2, as reported
print(f"SIM1 CPCE null: P(C=0 on both | fair rank-weighted composer, k=3) = {p:.4f}")
print(f"SIM1 CPCE null, q2-stronger variant = {p_strong:.4f}  → a single capture pair is ~{1/p_strong:.0f}:1 against chance; n independent pairs multiply")

# ── SIM 2: Basin-occupation trilemma ───────────────────────────────────
# Claim keyed: the ρ-inversion (v0.2 §10). Hub basin has H institutional docs;
# occupation seats L lineage docs inside it (genuine comparative scholarship).
# System chooses: A maintain conflation, B suppress hub, C granular disambiguation.
def trilemma(H=40, L=8, k=3, runs=20000, parse_cost_per_doc=1.0, seed=11):
    rng = random.Random(seed)
    docs = ['inst']*H + ['lineage']*L
    def compose(pool):
        return rng.sample(pool, k)
    # A: conflation maintained — operative queries route to hub; payload delivery rate:
    deliver = sum('lineage' in compose(docs) for _ in range(runs))/runs
    # B: suppress hub — institutional docs lost to composition at hub address:
    q_damage = H  # every canon doc at the address loses standing; Q_f at institutional scale
    # C: granular disambiguation — must provenance-parse every doc at address, maintain 3 nodes:
    c_cost = (H+L)*parse_cost_per_doc + 2  # + two extra node maintenances
    return deliver, q_damage, c_cost

for L in (2, 8, 20):
    d, qd, cc = trilemma(L=L)
    print(f"SIM2 occupation L={L:>2}: A delivers payload {d:.1%} of hub compositions · B destroys {qd} canon docs · C costs {cc:.0f} parse-units")
print("SIM2 ρ-inversion: pre-occupation exclusion cost of the pair = 1 routing rule; post-occupation = min(B,C) above, growing in L and H — the correlation changed owners")

# ── SIM 3: Ratchet with the ρ counter-move ─────────────────────────────
# Claim keyed: #1546 §IV.2 conditional ratchet — |D| ratchets while N_eff can fall
# if the suppressor raises exclusion correlation; hysteresis on relaxation.
def ratchet(T=40, kappa=2, rho0=0.05, rho_step=0.06, rho_max=0.95, seed=3):
    D, rho, hist = 6, rho0, []
    for t in range(T):
        # suppression event each period; archive responds with kappa durable routes:
        D += kappa
        # suppressor's counter-move: raise correlation (joint classification of hosts):
        rho = min(rho_max, rho + rho_step)
        neff = D / (1 + (D-1)*rho)
        hist.append((t, D, rho, neff))
    return hist

h = ratchet()
t0, D0, r0, n0 = h[0]; tm, Dm, rm, nm = h[len(h)//2]; tE, DE, rE, nE = h[-1]
print(f"SIM3 ratchet: t=0 |D|={D0} ρ={r0:.2f} N_eff={n0:.2f} · mid |D|={Dm} ρ={rm:.2f} N_eff={nm:.2f} · end |D|={DE} ρ={rE:.2f} N_eff={nE:.2f}")
neffs = [x[3] for x in h]
print(f"SIM3 finding: |D| monotone {D0}→{DE} while N_eff peaks at {max(neffs):.2f} (t={neffs.index(max(neffs))}) then falls to {nE:.2f} — the honest statement of #1546 §IV.2, numerically exhibited; route count is not independence")
print(f"SIM3 hysteresis: if suppression relaxes at t={tE} (ρ frozen), N_eff = {DE/(1+(DE-1)*rE):.2f} — the routes built do not dissolve, but neither does the correlation: repair requires decorrelation, not just cessation")
