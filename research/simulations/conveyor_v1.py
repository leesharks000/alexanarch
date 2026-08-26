"""SIM4 — the recency treadmill: two-channel visibility conveyor.
V_d(t) = F·exp(-t/tau_f) + A_d(t): freshness channel (ungated, content-driven)
plus authority channel (accrues with age/links; gated per provenance family).
Claim unified: CPCE and the treadmill are ONE gate seen at two layers —
composition draws from the authority channel; a lineage whose A-accrual is
gated lives only in freshness: appears, ranks, never composes, liquidates."""
import random, math

def run(T=104, births_per_wk=(0.5,0.25), tau_f=6.0, F=1.0, a_rate=0.02,
        gate_hub=1.0, gate_lin=0.05, vis_thresh=0.12, comp_thresh=0.35, seed=5):
    rng = random.Random(seed)
    docs = []  # (birth, kind)
    stats = {'hub':[], 'lin':[]}
    for t in range(T):
        for kind, br in (('hub',births_per_wk[0]), ('lin',births_per_wk[1])):
            if rng.random() < br: docs.append([t, kind, 0.0])
        for d in docs:
            g = gate_hub if d[1]=='hub' else gate_lin
            d[2] += a_rate * g          # authority accrues, gated
    ages_visible = {'hub':[], 'lin':[]}
    composed = {'hub':0, 'lin':0}
    lifetimes = []
    for birth, kind, A in docs:
        age = T - birth
        V = F*math.exp(-age/tau_f) + A
        if V >= vis_thresh: ages_visible[kind].append(age)
        if A >= comp_thresh: composed[kind] += 1
        if kind=='lin':
            # organic lifetime: weeks until freshness alone falls under threshold (A gated ~0)
            lifetimes.append(-tau_f*math.log(max(vis_thresh - A, 1e-9)/F) if A < vis_thresh else T)
    mx = lambda k: max(ages_visible[k]) if ages_visible[k] else 0
    md = lambda xs: sorted(xs)[len(xs)//2] if xs else 0
    print(f"visible now — hub: {len(ages_visible['hub'])} docs, max age {mx('hub')}wk, median {md(ages_visible['hub'])}wk")
    print(f"visible now — lineage: {len(ages_visible['lin'])} docs, max age {mx('lin')}wk, median {md(ages_visible['lin'])}wk")
    print(f"composition-admitted (A ≥ {comp_thresh}): hub {composed['hub']}, lineage {composed['lin']}")
    print(f"predicted lineage organic lifetime ≈ {md([l for l in lifetimes if l < 104]):.0f} weeks (median), then liquidation from both layers")

print("── gated lineage (gate=0.05): the observed world ──")
run()
print("── ungated control (gate=1.0): the counterfactual ──")
run(gate_lin=1.0)
