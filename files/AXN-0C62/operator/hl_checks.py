#!/usr/bin/env python3
"""Scope C, mechanical half, for EA-HK-HISTLOGOS-01 (v1.1): consequence tests C1–C8, the method check M1 run on the built files, and a reference check for the fields that carry
identifiers outside the edge array. Records results into 10-verification.json under scope_C_mechanical; records, does not block.
    python3 hl_checks.py <kernel dir>"""
import sys, json, pathlib, yaml
KD = pathlib.Path(sys.argv[1])
K = yaml.safe_load((KD / "00-kernel.yaml").read_text(encoding="utf-8")); G = json.loads((KD / "02-graph.jsonld").read_text(encoding="utf-8"))
A = {json.loads(l)["@id"]: json.loads(l) for l in (KD / "04-arguments.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
C = {json.loads(l)["id"]: json.loads(l) for l in (KD / "03-claims.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
nodes = {x["@id"]: x for x in G["@graph"]}; res = {}
def T(k, ok, d): res[k] = {"pass": bool(ok), "detail": d}
def refs(x):
    out = []
    if isinstance(x, str) and x.split(":", 1)[0] in ("arg", "claim", "site", "stmt", "argument", "erasure", "bridge", "rec"): out.append(x)
    elif isinstance(x, list):
        for y in x: out += refs(y)
    elif isinstance(x, dict):
        for y in x.values(): out += refs(y)
    return out
def resolves(r):
    s = r.split(":", 1)
    return (r in A) if s[0] == "arg" else (s[1] in C) if s[0] == "claim" else (r in nodes or s[0] == "rec")
BR = K["bridges"]; MA = K["maker_argument"]
# C1 remove rung V: nothing but the outer-ring bridges into Josephus rests on it; rung VI carries no dependency on V
josephus = {"arg:a1484-st-josephus", "arg:a626-void", "arg:a625-first-cycle", "arg:a1484-jos-viii", "arg:a626-protocol-not-recovery"}
dep = [b["@id"] for b in BR if josephus & set(b["operation_at_from"] + b["operation_at_to"] + b["supporting"]) and b["@id"] != "bridge:into-the-record"]
vi = nodes.get("hk:revfirst/rung/VI", {})
T("C1 remove rung V: only bridge:into-the-record rests on the Josephus moves; rung VI independent of V", not dep and "depends_on" not in vi and "INDEPENDENT" in str(vi.get("fit")), {"other_bridges_on_josephus_moves": dep, "rung_VI_fit": vi.get("fit")})
# C2 Philo presence unestablished: the mapping bridge's ends carry no presence claim; the erasure row keeps the crossing conditional
mp = next(b for b in BR if b["@id"] == "bridge:mapping"); er = next(r for r in K["erasure_by_station"] if r["station"] == "site:philo")
cross = next(p for p in er.get("propositions", []) if "crossing" in p["proposition"])
T("C2 Philo: the mapping stands as structure; the crossing stays conditional", "arg:a1486-not-established" not in mp["operation_at_to"] and "modular" in cross["standing"], {"mapping_to": mp["operation_at_to"], "crossing_standing": cross["standing"]})
# C3 disable the lifespan premise: no maker step or demonstration cites a bounded move; those moves carry current_standing
bounded = [k for k, a in A.items() if (a.get("current_standing") or {}).get("state") == "bounded"]
cited = set(refs(MA["steps"])) | set(refs(MA["demonstrations"]))
T("C3 lifespan disabled: argument:one-maker cites no bounded move", bounded and not (set(bounded) & cited), {"bounded": bounded, "cited_bounded": sorted(set(bounded) & cited)})
# C4 the collective substitution is caught
T("C4 'a collective' is a changed thesis", "one composing person" in MA["thesis"] and "collective" in MA["substitution_test"] and any("not a collective" in m for m in K["acceptance"]["scopes"]["C"]["mandatory_passes"]), {"thesis": MA["thesis"][:80]})
# C5 a challenged erasure finding stays local
er_edges = [e for e in G["edges"] if e["source"].startswith("erasure:")]
cross_station = [e for e in er_edges if e["target"] != "claim:hl-stmt-erasure"]
into_gen = [e for e in G["edges"] if e["target"] == "claim:hl-stmt-genealogy"]
T("C5 erasure findings local: each supports only the erasure statement; none feeds the genealogy statement", er_edges and not cross_station and not into_gen, {"findings": len(er_edges), "cross": cross_station[:3], "into_genealogy": len(into_gen)})
# C6 the settlement: the label read as a dated settlement; the flag set; D5 kept as a disputed step, warranted on both sides
SJ = K.get("settlement_join", {}); D5 = next((d for d in K["rival"]["disputed_steps"] if d.get("id") == "D5"), {})
T("C6 the settlement: SETTLEMENT_AS_CORPUS set on the inference, D5 in four objects each warranted, 367 dating one collection's boundary, the warrants from the rival, the primary witnesses and the records",
  "SETTLEMENT_AS_CORPUS" in json.dumps(yaml.safe_load((KD / "08-traversal.yaml").read_text(encoding="utf-8")).get("failure_flags", {})) and SJ.get("states", {}).get("current_state") == "rec:978" and SJ.get("states", {}).get("prior_state") == "rec:674"
  and len(D5.get("objects", {})) == 4 and all(w in C for o in D5.get("objects", {}).values() for w in o["warrants"]) and "inference" in json.dumps(yaml.safe_load((KD / "08-traversal.yaml").read_text(encoding="utf-8"))["failure_flags"]["SETTLEMENT_AS_CORPUS"]) and any(w.startswith("pr-") for w in D5.get("warrants", [])) and any(w.startswith("rv-") for w in D5.get("warrants", [])) and any(w.startswith("hl-") for w in D5.get("warrants", [])) and all(w in C for w in D5.get("warrants", [])), {"D5_warrants": D5.get("warrants")})
# C7 remove instrument V: no bridge depends on it alone; the maker argument's steps and demonstrations cite none of its moves only
INS = {i["@id"]: i for i in K["method"]["instruments"]}; V = INS.get("instrument:corpus-scale", {})
v_moves = set(refs({k: V.get(k) for k in ("specification", "controls", "negatives_and_residue", "results", "defeats_if", "grades")}))
only_v = [b["@id"] for b in BR if b.get("instruments") == ["instrument:corpus-scale"]]
shared = {k: sorted(set(refs(i.get("results"))) & v_moves) for k, i in INS.items() if k != "instrument:corpus-scale"}
T("C7 remove instrument V: no bridge rests on it alone; the results of instruments I–IV cite none of its moves", not only_v and not any(shared.values()), {"bridges_only_on_V": only_v, "shared_results": {k: v for k, v in shared.items() if v}})
# C8 M-D1 carries #1576's four propositions, the fourth as precedence
MD1 = next(d for d in MA["demonstrations"] if d["id"] == "M-D1")
T("C8 M-D1 carries #1576's four propositions; the fourth is precedence, with its bundle", all(w in MD1["configuration"] for w in ("part of the method", "existed beforehand", "named art", "conventionally dated before")) and "two makers" not in MD1["configuration"] and "arg:a1576-fourth-bundles" in MD1["moves"], {"configuration": MD1["configuration"][:160]})
# M1 every instrument complete: specification, controls, results with status, defeats, grades, and a statement of what it licenses no conclusion about; every move resolves
inc = {k: [f for f in ("specification", "controls", "results", "defeats_if", "grades", "licenses_no") if not i.get(f)] for k, i in INS.items()}
nostat = [k for k, i in INS.items() if any(not r.get("status") for r in i.get("results", []))]
unres = sorted({r for i in INS.values() for r in refs(i) if not resolves(r)} | {r for r in K["method"].get("losses_recorded", []) if not resolves(r)})
BB = K["method"].get("by_bridge", []); cst = [k for k, i in INS.items() if set(i.get("controls_status", {})) != set(i.get("controls", [])) or not set(i.get("controls_status", {}).values()) <= {"run", "specified"}]
unres += sorted({r for row in BB for r in refs(row) if not resolves(r)})
T("M1 five instruments, each complete, every result at a status, every control marked run or specified, a method row for every bridge, every move and loss resolving",
  len(INS) == 5 and not any(inc.values()) and not nostat and not unres and K["method"].get("losses_recorded") and not cst and {r["bridge"] for r in BB} == {b["@id"] for b in BR},
  {"incomplete": {k: v for k, v in inc.items() if v}, "no_status": nostat, "controls_unmarked": cst, "unresolved": unres[:8]})
# references in the new fields resolve
bad = []
for obj in BR + [MA, K["rival"], {"e": K["erasure_by_station"]}, K["method"], K.get("settlement_join", {})]:
    bad += [r for r in refs(obj) if not resolves(r)]
for a in A.values():
    bad += [r for r in refs(a.get("current_standing")) if not resolves(r)]
ctx = G["@context"]; need = ["from", "to", "move", "operation_at_from", "operation_at_to", "supporting", "see", "moves"]
T("R1 every identifier in the bridges, the maker argument, the rival, the erasure rows and current_standing resolves; each carrying field is coerced @id", not bad and all(isinstance(ctx.get(p), dict) and ctx[p].get("@type") == "@id" for p in need),
  {"unresolved": sorted(set(bad))[:8], "coerced": [p for p in need if isinstance(ctx.get(p), dict)]})
v = json.loads((KD / "10-verification.json").read_text(encoding="utf-8")); v["scope_C_mechanical"] = res
(KD / "10-verification.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
for k, r in res.items(): print("PASS" if r["pass"] else "FAIL", k, "" if r["pass"] else json.dumps(r["detail"], ensure_ascii=False)[:400])
