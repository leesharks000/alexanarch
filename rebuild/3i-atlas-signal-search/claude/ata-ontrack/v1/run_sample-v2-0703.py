#!/usr/bin/env python3
"""Run ontrack.py over the planned units (PLAN.json), ON beam, prefetching the next unit while the current one is searched.
Writes results/<sub>-<chunk>.json, ledger.jsonl (one line per decoded array, with hashes) and stacks/<sub>-<chunk>.npz
(the comet-track and reversed-track stacks T, float16). Resumable: a unit with a result file is skipped."""
import json, os, sys, time, threading, queue, numpy as np
import ontrack as o
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = json.load(open(os.path.join(HERE, "PLAN.json")))
os.makedirs(os.path.join(HERE, "results"), exist_ok=True); os.makedirs(os.path.join(HERE, "stacks"), exist_ok=True)
units = [(u["sub"], u["chunk"], u.get("why", "random")) for u in PLAN["units"]]
todo = [u for u in units if not os.path.exists(os.path.join(HERE, "results", f"{u[0]}-{u[1]}.json"))]
q = queue.Queue(maxsize=1)


def reader():
    import concurrent.futures as cf
    for sub, c, why in todo:
        try:
            with cf.ThreadPoolExecutor(2) as ex:
                fut = {sc: ex.submit(o.read, sc, sub, 0, c) for sc in o.SCAN_IDS}
                raw = {sc: fut[sc].result() for sc in o.SCAN_IDS}
            q.put((sub, c, why, raw, None))
        except Exception as e:
            q.put((sub, c, why, None, repr(e)))
    q.put(None)


threading.Thread(target=reader, daemon=True).start()
n = 0
while True:
    item = q.get()
    if item is None:
        break
    sub, c, why, raw, err = item
    if err:
        print(f"ERROR {sub} {c}: {err}", flush=True); continue
    t0 = time.time(); f0 = o.FCH1[sub] + c * 0.5e6
    Z = {sc: o.normalize(x.astype(np.float64))[0] for sc, (x, _) in raw.items()}
    with open(os.path.join(HERE, "ledger.jsonl"), "a") as L:
        for sc, (_, r) in raw.items():
            L.write(json.dumps(dict(r, scan=sc, sub=sub, beam=0)) + "\n")
    del raw
    res = o.search(Z, f0)
    summ = {"sub": sub, "chunk": c, "why": why, "beam": 0, "f0_hz": f0, "proc_s": None, "rv0_mps": o.RV0, "tracks": {}}
    def pk_rec(T, S, p, f0, extra=None):
        sl = S[:, max(0, p - 1):p + 2].max(axis=1)
        r = {"j": p, "g_hz": f0 + p * o.FOFF, "T": float(T[p]), "S": [round(float(v), 3) for v in sl],
             "n_scans_ge3": int((sl >= 3).sum()), "n_pos": int((S[:, p] > 0).sum()), "max_S": float(sl.max())}
        if extra: r.update(extra)
        return r
    for k, (T, Traw, S, valid, Tres, dbest, Thalf) in res.items():
        summ["tracks"][str(k)] = {"n_valid": int(valid.sum()),
            "max_T": float(T.max()), "max_Traw": float(Traw.max()), "max_Tres": float(Tres.max()), "max_Thalf": float(Thalf.max()),
            "peaks": [pk_rec(T, S, p, f0, {"Traw": float(Traw[p])}) for p in o.peaks(T)],
            "peaks_res": [pk_rec(Tres, S, p, f0, {"d_hz_per_s": float(dbest[p])}) for p in o.peaks(Tres)],
            "peaks_half": [pk_rec(Thalf, S, p, f0) for p in o.peaks(Thalf)]}
    np.savez_compressed(os.path.join(HERE, "stacks", f"{sub}-{c}.npz"), T_comet=res[1.0][0].astype(np.float16), Tres_comet=res[1.0][4].astype(np.float16),
                        dbest_comet=res[1.0][5].astype(np.float16), Thalf_comet=res[1.0][6].astype(np.float16), T_rev=res[-1.0][0].astype(np.float16))
    summ["proc_s"] = round(time.time() - t0, 1)
    json.dump(summ, open(os.path.join(HERE, "results", f"{sub}-{c}.json"), "w"))
    n += 1
    tr = summ["tracks"]
    cm = lambda f: round(max(v[f] for k, v in tr.items() if k not in ("1.0", "0.0")), 2)
    print(time.strftime("%H:%M:%S"), n, len(todo), sub, c, why, "| T comet/ctrl", round(tr["1.0"]["max_T"], 2), cm("max_T"),
          "| Tres", round(tr["1.0"]["max_Tres"], 2), cm("max_Tres"), "| Thalf", round(tr["1.0"]["max_Thalf"], 2), cm("max_Thalf"),
          "| fixed", round(tr["0.0"]["max_T"], 2), flush=True)
print("done", n, flush=True)
