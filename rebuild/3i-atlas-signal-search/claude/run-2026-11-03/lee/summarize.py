"""Summary of lee.json under PLAN-lee.md's rule and STOP-lee.md's stopping rule (the runner was stopped at 64 channels before its own summary block).
    python3 summarize.py -> lee.json["summary"], summary.json"""
import json, numpy as np
st = json.load(open("lee.json")); R = st["channels"]
def Ev(v): return (v["T"] - v["mu"]) / max(v["sd"], 0.5)
def flag(v): return v["T"] > v["max"] and (v["T"] - v["swap"]) > v["d_max"]
def summ(S):
    e7 = Ev(S["blc23_cc07"]); Es = np.array([Ev(v) for k, v in S.items() if k != "blc23_cc07"])
    return {"channels": len(S), "E_cc07": round(e7, 3), "p_LEE": sum(Ev(v) >= e7 for v in S.values()) / len(S), "p_LEE_count": f"{sum(Ev(v) >= e7 for v in S.values())}/{len(S)}",
            "N_FLAG": sum(flag(v) for v in S.values()), "chance_N_FLAG": round(len(S) / 41, 2), "E_others_mean": round(float(Es.mean()), 3), "E_others_sd": round(float(Es.std()), 3),
            "E_others_max": round(float(Es.max()), 3), "flagged": [k for k, v in S.items() if flag(v)],
            "top_E": [{"ch": k, "f_mid_MHz": v["f_mid_MHz"], "T": v["T"], "swap": v["swap"], "mu": round(v["mu"], 2), "sd": round(v["sd"], 2), "max": v["max"], "E": round(Ev(v), 2), "flag": flag(v), "source": v["source"]}
                      for k, v in sorted(S.items(), key=lambda kv: -Ev(kv[1]))[:10]]}
ALL = [f"{nd}_cc{cc:02d}" for nd in ("blc22", "blc23", "blc24", "blc25") for cc in range(64)]
out = {"all_64": summ(R), "cc07_plus_seed29": summ({k: v for k, v in R.items() if v["source"] == "lee/run_lee.py"}),
       "not_surveyed": [k for k in ALL if k not in R]}
st["summary"] = out; json.dump(st, open("lee.json", "w"), indent=0); json.dump(out, open("summary.json", "w"), indent=1)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ("top_E",)} if isinstance(v, dict) else len(v) for k, v in out.items()}, indent=1))
