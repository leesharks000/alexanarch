"""Exploratory, after RD1's scores (not frozen): the start-of-scan track excess per window, ON and OFF, ranked."""
import os, sys, json, importlib.util
import numpy as np
D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rd1", os.path.join(D, "rd1.py")); rd1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(rd1)
out = {}
for s in sys.argv[1:]:
    R = rd1.per_scan(s); n = rd1.OUT["windows"]
    st = {k: sum(R[k]["S_track"]) for k in n}
    cand = [k for k, w in zip(n, rd1.OUT["kind"]) if w == "cand"]; ctl = [k for k, w in zip(n, rd1.OUT["kind"]) if w == "ctrl"]
    cm = np.mean([st[k] for k in cand]); boot = [np.mean(np.random.default_rng(i).choice([st[k] for k in ctl], 11, replace=False)) for i in range(4000)]
    out[s] = {"cand_mean": cm, "ctrl_mean": float(np.mean([st[k] for k in ctl])), "p_11_ctrl_draw_ge": float(np.mean(np.array(boot) >= cm)),
              "cand_ranks": {k: int(1 + sum(st[c] >= st[k] for c in ctl)) for k in cand}}
    print(s, json.dumps(out[s]), flush=True)
json.dump(out, open(os.path.join(D, "explore_step0.json"), "w"), indent=1)
