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
    summ = {"sub": sub, "chunk": c, "why": why, "beam": 0, "f0_hz": f0, "proc_s": round(time.time() - t0, 1), "rv0_mps": o.RV0, "tracks": {}}
    for k, (T, Traw, S, valid) in res.items():
        pk = o.peaks(T)
        summ["tracks"][str(k)] = {"max_T": float(T.max()), "max_Traw": float(Traw.max()), "n_valid": int(valid.sum()),
            "peaks": [{"j": p, "g_hz": f0 + p * o.FOFF, "T": float(T[p]), "Traw": float(Traw[p]),
                       "S": [round(float(v), 3) for v in S[:, max(0, p - 1):p + 2].max(axis=1)],
                       "n_scans_ge3": int((S[:, max(0, p - 1):p + 2].max(axis=1) >= 3).sum()),
                       "n_pos": int((S[:, p] > 0).sum()), "max_S": float(S[:, max(0, p - 1):p + 2].max())} for p in pk]}
    np.savez_compressed(os.path.join(HERE, "stacks", f"{sub}-{c}.npz"), T_comet=res[1.0][0].astype(np.float16), T_rev=res[-1.0][0].astype(np.float16))
    json.dump(summ, open(os.path.join(HERE, "results", f"{sub}-{c}.json"), "w"))
    n += 1
    tr = summ["tracks"]
    print(time.strftime("%H:%M:%S"), n, len(todo), sub, c, why, "comet", round(tr["1.0"]["max_T"], 2),
          "ctrl", round(max(v["max_T"] for k, v in tr.items() if k not in ("1.0", "0.0")), 2), "fixed", round(tr["0.0"]["max_T"], 2), flush=True)
print("done", n, flush=True)
