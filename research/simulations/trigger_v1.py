"""SIM5 — the Stabilization Trigger Hypothesis (composition-triggered liquidation)
vs the passive gate. Reactive model: sub-threshold lineage visibility tolerated;
crossing composition admission fires enforcement with prob p_det/wk, zeroing BOTH
layers (doc-scoped or lineage-scoped). Discriminators: transient-composition rate,
decay shape (cliff vs slope), cross-layer time-locking, collateral decline."""
import random, math

def world(model='trigger', scope='doc', T=104, tau_f=6.0, F=1.0, a_rate=0.02,
          comp_thresh=0.30, p_det=0.5, births=0.25, seed=9):
    rng = random.Random(seed)
    docs = []   # [birth, A, alive, composed_ever, comp_week, kill_week]
    events = []
    for t in range(T):
        if rng.random() < births: docs.append([t, 0.0, True, False, None, None])
        for d in docs:
            if not d[2]: continue
            d[1] += a_rate                       # ungated accrual: content earns
            age = t - d[0]
            V = F*math.exp(-age/tau_f) + d[1]
            if V >= comp_thresh and d[1] >= comp_thresh*0.6:
                if not d[3]: d[3], d[4] = True, t # composition debut
                if model=='trigger' and rng.random() < p_det:
                    if scope=='doc':
                        d[2], d[5] = False, t
                    else:
                        for e in docs:
                            if e[2]: e[2], e[5] = False, t
                    events.append(t)
            if model=='passive':
                d[3] = False                      # never composes; gate on channel
    n = len(docs)
    comp_transients = sum(1 for d in docs if d[3])
    lags = [d[5]-d[4] for d in docs if d[4] is not None and d[5] is not None]
    lifetimes = [ (d[5]-d[0]) if d[5] else None for d in docs]
    killed = [l for l in lifetimes if l]
    med = lambda xs: sorted(xs)[len(xs)//2] if xs else None
    return dict(n=n, transients=comp_transients,
                med_lag=med(lags), med_kill_age=med(killed),
                alive=sum(d[2] for d in docs), events=len(events))

for label, kw in (("TRIGGER doc-scoped", dict(model='trigger', scope='doc')),
                  ("TRIGGER lineage-scoped", dict(model='trigger', scope='lineage')),
                  ("PASSIVE gate", dict(model='passive'))):
    r = world(**kw)
    print(f"{label:22s} docs={r['n']:2d} transient-compositions={r['transients']:2d} "
          f"median comp→kill lag={r['med_lag']}wk kill-age={r['med_kill_age']}wk alive={r['alive']:2d} events={r['events']}")
print()
print("DISCRIMINATORS: trigger world shows (1) nonzero transient compositions — the June Sappho")
print("composition is evidence FOR trigger, impossible under pure passive gate; (2) cliff decay")
print("time-locked to debut (lag ~0-2wk) vs smooth freshness slope; (3) lineage-scoped variant:")
print("one debut kills siblings — collateral decline is the entity-level signature.")
print("SAMPLING DESIGN: weekly battery baseline; on any composition debut, daily capture ±14d")
print("of BOTH layers, both addresses — the tripwire protocol: we control supply, so a designated")
print("tripwire doc's debut gives the trigger test at n=1 with event-locked resolution.")
