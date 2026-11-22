"""PLAN-HM13 B1 reading: each recovered nomination, off-source test, ON recurrence.  python3 hm13b1_read.py -> hm13b1.json"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(HERE, "../..")
C = 299792.458; DF = 2.7939677238464355   # km/s; Hz per bin (dm.DF)
CH = [30, 32, 37, 39, 43, 45, 46, 49, 51, 55]; WANT = {30: 1, 32: 3, 37: 1, 39: 1, 43: 2, 45: 3, 46: 2, 49: 6, 51: 2, 55: 4}
ON, OFF = ["0013", "0015", "0017"], ["0014", "0016", "0018"]
log = open(os.path.join(HERE, "hm13b1.log")).read()
out = {"plan": "PLAN-HM13.md", "channels": {}}
for cc in CH:
    c = f"{cc:02d}"; vf = os.path.join(HERE, "volt", f"cc{c}.json")
    if not os.path.exists(vf): out["channels"][f"cc{c}"] = {"error": "no volt file"}; continue
    V = json.load(open(vf)); A = json.load(open(os.path.join(M, "M4", f"cc{c}.json")))[f"cc{c}"]
    v0 = json.load(open(os.path.join(HERE, "v0", f"cc{c}.json"))); FC = V["fc"]
    g1 = f"G1 cc{c} PASS" in log; g2 = len(V["nominations"]) == WANT[cc]
    hits = {h["id"]: h for h in V["hits"]}; rows = []
    for n in V["nominations"]:
        h = hits[n["hit"]]; s = h["scan"]
        offd = min(abs(t["mhz_topo"] - n["mhz_topo"]) * 1e6 for o in OFF for t in A[o]["top"])
        rec = {s}
        for s2 in ON:
            if s2 == s: continue
            p2 = h["bin"] + FC * (v0[s2] - v0[s]) / C / DF
            if any(abs(x["bin"] - p2) <= 2 for x in V["hits"] if x["scan"] == s2): rec.add(s2)
        st = "closed (off-source)" if offd <= 50 else ("lead, recurring" if len(rec) >= 2 else "lead, single-scan")
        rows.append({"hit": n["hit"], "scan": s, "feed": n["feed"], "mhz_topo": round(n["mhz_topo"], 6), "z": n["z"], "why": n["why"], "k4": round(n["k4"], 3),
                     "nearest_off_top_hz": round(offd, 1), "on_scans": sorted(rec), "standing": st})
    out["channels"][f"cc{c}"] = {"fc_mhz": FC / 1e6 if FC > 1e5 else FC, "G1": g1, "G2": g2, "n": len(V["nominations"]), "want": WANT[cc], "nominations": rows}
json.dump(out, open(os.path.join(HERE, "hm13b1.json"), "w"), indent=1)
for k, v in out["channels"].items():
    print(k, {x: v.get(x) for x in ("G1", "G2", "n", "want")}, [r["standing"] for r in v.get("nominations", [])])
