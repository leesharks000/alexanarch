#!/usr/bin/env python3
"""Verify a framework holographic kernel against the archive (v0.2).

Runs the structural tests T1–T16 of 09-tests.yaml, executes the relation policy over the claim graph (T12) and a historical reconstruction at
stated dates (T13), and scores back-projection v0.1 (structural presence, after EA-HK-INFRA-01 #74) on two declared input scopes:
scope A, 00-kernel.yaml + 01-ontology.yaml (the kernel's own compression test); scope B, A + 02-graph.jsonld (topology at record and claim grain).
Results are written as data to 10-verification.json; nothing is blocked.

What this verifier does not check, stated so the distinction stays explicit: whether a reading is right; whether a relation's warrant is sufficient;
reconstructive validity by a reader (back-projection v1.0, 09b); anything in a record beyond the quotations the kernel binds.
   python3 verify_hk.py <alexanarch root> <kernel dir>"""
import json, pathlib, sys, re, yaml, hashlib, subprocess, itertools
ROOT, K = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
HERE = pathlib.Path(__file__).resolve().parent
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
CAP = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
FIRST = json.loads((HERE / "first-seating.json").read_text())
kernel = yaml.safe_load((K / "00-kernel.yaml").read_text()); onto = yaml.safe_load((K / "01-ontology.yaml").read_text())
graph = json.loads((K / "02-graph.jsonld").read_text()); claims = [json.loads(l) for l in (K / "03-claims.jsonl").read_text().splitlines() if l]
questions = yaml.safe_load((K / "06-questions.yaml").read_text())["questions"]
events = [json.loads(l) for l in (K / "05-temporal.jsonl").read_text().splitlines() if l]
G = {n["@id"]: n for n in graph["@graph"]}; E = graph["edges"]; POLICY = onto["relation_policy"]; CL = {c["id"]: c for c in claims}
norm = lambda s: re.sub(r"\s+", " ", (s or "").replace("*", "").replace("’", "'").replace("‘", "'"))
num = lambda ref: int(ref.split(":")[1])
def text(n):
    p = REG[n].get("full_text_path"); f = ROOT / p.lstrip("/") if p else None
    return f.read_text(encoding="utf-8", errors="ignore") if f and f.exists() else ""
def git_show(commit, path):
    r = subprocess.run(["git", "-c", "gc.auto=0", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True)
    return r.stdout.decode("utf-8", "ignore") if r.returncode == 0 else None
R = {}
def test(tid, ok, detail=""): R[tid] = {"pass": bool(ok), "detail": detail}

recs = [n for n in G.values() if n.get("@type") == "Record"]
bad = [r["@id"] for r in recs if r["deposit"] not in REG or REG[r["deposit"]]["axn"] != r["axn"] or REG[r["deposit"]]["hash"] != r["sha256"]]
test("T1 records resolve", not bad, f"{len(recs)} records ({sum(1 for r in recs if r.get('external'))} external); stale: {bad}")

quoted = [c for c in claims if c["target"]["exact"]]
miss = [c["id"] for c in quoted if norm(c["target"]["exact"]) not in norm(text(num(c["target"]["record"])) + " " + (REG[num(c["target"]["record"])].get("description") or ""))]
stale = [c["id"] for c in claims if REG[num(c["target"]["record"])]["hash"] != c["target"]["record_sha256"]]
test("T2 quotations bind", not miss and not stale, f"{len(quoted)} quoted claims, {len(claims) - len(quoted)} unseated originals; unbound: {miss}; hash drift: {stale}")

badrel = [(e["source"], e["relation"]) for e in E if e["family"] in ("evidentiary", "historical") and (e["relation"] not in POLICY or POLICY[e["relation"]] != e["licensed_dimension"])]
test("T3 relations in policy", not badrel, f"{sum(1 for e in E if e['family'] in ('evidentiary', 'historical'))} licensing-family edges; off-policy: {badrel}")

# T4: re-establish each resolved introduction from the first seated version itself (git), and keep the unresolved ones visible
regcache, t4bad, unresolved = {}, [], []
for c in quoted:
    i = c["introduced"]; n = num(c["target"]["record"]); f = FIRST[str(n)]
    if i["date"] is None:
        unresolved.append(c["id"]); continue
    first_text = git_show(f["commit"], f["path"]) or ""
    if f["commit"] not in regcache:
        raw = git_show(f["commit"], "data/registry.json")
        regcache[f["commit"]] = {r["deposit_number"]: r for r in json.loads(raw)["deposits"]} if raw else {}
    first_desc = (regcache[f["commit"]].get(n) or {}).get("description") or ""
    if not (norm(c["target"]["exact"]) in norm(first_text) or norm(c["target"]["exact"]) in norm(first_desc)) or i["date"] != f["date"]:
        t4bad.append(c["id"])
test("T4 introductions established at first seating", not t4bad, f"{len(quoted) - len(unresolved)} established from git; unresolved and marked: {unresolved}; failed: {t4bad}")

absent = [(i["id"], x) for i in kernel["invariants"] for x in i["nodes"] if x not in G]
test("T5 invariants resolve", not absent, f"{len(kernel['invariants'])} invariants; unresolved nodes: {absent}")

byb = {}
for c in claims:
    st = c["state"]; failing = st.get("assertion") == "withdrawn" or st.get("limit") or st.get("reportability") in ("underpowered", "against", "null_both_directions", "unsupervised only")
    byb.setdefault(c["body"], []).append(bool(failing))
test("T6 failures per body", all(any(v) for v in byb.values()), {b: f"{sum(v)} failing or limited of {len(v)}" for b, v in byb.items()})

ms = [e for e in events if e["event"] == "maker_count_state"]
ordered = all(ms[i]["date"] <= ms[i + 1]["date"] for i in range(len(ms) - 1)) and all(REG[num(e["object"])]["date"] == e["date"] for e in ms) and all(e.get("warrant") in G for e in ms)
test("T7 maker-count states ordered, bound and warranted", ordered and len(ms) == 5, [f"{e['date']} {e['object']} {e['state']} (attested from {e.get('attested_from')})" for e in ms])

joins = {}
for e in E:
    if e["relation"] == "joins": joins.setdefault(e["source"], set()).add(e["target"])
test("T8 joins carry both clusters", len(joins) >= 5 and all(v == {"cluster:functional", "cluster:peripatetic"} for v in joins.values()), sorted(joins))

caps = [n for n in G.values() if n.get("@type") == "Capture"]
cbad = [c["slug"] for c in caps if c["slug"] not in CAP or CAP[c["slug"]].get("axn") != c["axn"]]
test("T9 captures resolve", not cbad, f"{len(caps)} captures; unresolved: {cbad}")

summ = kernel["compression_survival_summary"]
need = ["Socrates", "Plato", "Aristotle", "Theophrastus", "interpretive", "stylometric", "manuscript-philological", "reception-historical", "#123", "#1576", "#1588", "#1658", "#1733"]
test("T10 summary carries the architecture", all(x in summ for x in need), [x for x in need if x not in summ])

rv = G.get("fw:many-maker", {}); rvbad = []
for b, st in (rv.get("status") or {}).items():
    for w in st.get("warrants", []):
        if w not in CL or CL[w]["body"] != b: rvbad.append((b, w))
test("T11 rival statuses bound to warrants of their body", set(rv.get("status", {})) == {"I", "S", "M", "R"} and not rvbad and all(st.get("warrants") for st in rv["status"].values()),
     {"bodies": sorted(rv.get("status", {})), "warrants": {b: st.get("warrants") for b, st in rv.get("status", {}).items()}, "mismatched": rvbad})

# T12: execute the policy. A path licenses a transition only if every edge licenses the same dimension in the same direction (#1529 §5.2).
CE = [e for e in E if e["source"].startswith("claim:") and e["target"].startswith("claim:")]
out_ = {}
for e in CE: out_.setdefault(e["source"], []).append(e)
def licensed_paths(src, maxlen=4):
    paths = []
    def walk(node, dim, path):
        for e in out_.get(node, []):
            d = e["licensed_dimension"]
            if d is None: continue
            dims = set(d.split(","))
            nd = dims if dim is None else dim & dims
            if not nd: continue
            p = path + [e]; paths.append((p, nd))
            if len(p) < maxlen: walk(e["target"], nd, p)
    walk(src, None, []); return paths
propagation = {}
for c in claims:
    for p, d in licensed_paths("claim:" + c["id"]):
        propagation.setdefault("claim:" + c["id"], []).append({"to": p[-1]["target"], "dimension": sorted(d), "via": [x["relation"] for x in p]})
r_to_maker = [s for s, ps in propagation.items() if CL[s.split(":", 1)[1]]["body"] == "R" and any(x["to"] == "claim:sy-1658-maker" for x in ps)]
grounds = [s for s, ps in propagation.items() if any(x["to"] == "claim:sy-1658-maker" and "establishment" in x["dimension"] for x in ps)]
mixed = []   # every two-edge path whose dimensions differ must license nothing
for a in CE:
    for b in out_.get(a["target"], []):
        if a["licensed_dimension"] and b["licensed_dimension"] and not set(a["licensed_dimension"].split(",")) & set(b["licensed_dimension"].split(",")):
            if any(x["to"] == b["target"] and len(x["via"]) == 2 for x in propagation.get(a["source"], [])): mixed.append((a["source"], b["target"]))
test("T12 propagation along licensing paths only", not r_to_maker and {"claim:th-1588-uncounted", "claim:th-1583-hinge", "claim:se-1603-provenance"} <= set(grounds) and not mixed,
     {"reception claims reaching the production model": r_to_maker, "establishment grounds of #1658": sorted(grounds), "mixed paths licensing": mixed,
      "licensed propagations": sum(len(v) for v in propagation.values())})

# T13: historical reconstruction
def reconstruct(day):
    state = None
    for e in ms:
        if e["date"] <= day: state = e
    present = [c["id"] for c in claims if c["introduced"]["date"] and c["introduced"]["date"] <= day]
    unres = [c["id"] for c in claims if not (c["introduced"]["date"] and c["introduced"]["date"] <= day) and c["introduced"].get("record_date") and c["introduced"]["record_date"] <= day]
    return {"state": state and (state["state"], state.get("establishment")), "state_record": state and state["object"], "state_attested_from": state and state.get("attested_from"), "present": present, "unresolved_on_date": unres}
expect = {"2026-05-23": ("not_claimed", None), "2026-09-02": ("two_not_established", None), "2026-09-07": ("open_because_uncounted", None),
          "2026-10-02": ("one_self_dividing_maker", "governing_hypothesis"), "2026-11-04": ("one_self_dividing_maker", "governing_hypothesis")}
recon, t13bad = {}, []
for day, st in expect.items():
    r = reconstruct(day); recon[day] = {"state": r["state"], "record": r["state_record"], "attested_from": r["state_attested_from"], "claims_present": len(r["present"]), "unresolved_on_date": len(r["unresolved_on_date"])}
    if r["state"] != st or any(CL[x]["introduced"]["date"] > day for x in r["present"]) or set(r["present"]) & set(r["unresolved_on_date"]): t13bad.append(day)
test("T13 historical reconstruction", not t13bad, {"by_date": recon, "failed": t13bad})

ids = set(G)
dangling = sorted({x for e in E for x in (e["source"], e["target"]) if x not in ids})
test("T14 endpoints declared", not dangling, f"{len(E)} edges; undeclared endpoints: {dangling}")

qbad = []
for qn in questions:
    n = num(qn["posed_in"]["record"])
    ok = norm(qn["posed_in"]["exact"]) in norm(text(n) + " " + (REG[n].get("description") or "")) and qn.get("advances_if") and qn.get("retreats_if") and qn.get("how_to_ask") \
         and qn.get("how_a_machine_investigates") and all(b in G for b in qn["bears_on"]) \
         and all(qn.get("consequence", {}).get(k, {}).get("effect") for k in ("if_advances", "if_retreats")) \
         and all(m in G or m.startswith("extension: ") for k in ("if_advances", "if_retreats") for m in qn["consequence"][k]["moves"])
    if not ok: qbad.append(qn["id"])
test("T15 lines of research posed and bounded", not qbad and len(questions) >= 5, f"{len(questions)} questions; failed: {qbad}")

# T16: what the kernel says in prose, the kernel's lists and the graph hold
import re as _re
words = {"five": 5, "six": 6, "seven": 7, "four": 4}
prose = [kernel["uktp_seed"]["topology"], kernel["litmus"]["topology"]]
joins = topo_k = kernel["topology"]["joins"]; t16bad = []
for p in prose:
    m = _re.search(r"(\w+) joins", p)
    if m and words.get(m.group(1)) != len(joins): t16bad.append(f"says {m.group(1)} joins; the list holds {len(joins)}")
    named = {int(x) for x in _re.findall(r"#(\d+)", p.split("joined at")[1].split("; six")[0])} if "joined at" in p else None
    if named is not None and named != set(joins): t16bad.append(f"names joins {sorted(named)}; the list holds {sorted(joins)}")
grounds_g = {int(e["source"].split("-")[1]) for e in E if e["target"] == "claim:sy-1658-maker" and e["relation"] in ("generalizes", "rebuts", "undercuts")}
for line in kernel["uktp_seed"]["dependencies"] + [kernel["litmus"]["dependency_chain"].split(";")[0]]:
    if "production model (#1658)" in line:
        left = {int(x) for x in _re.findall(r"#(\d+)", line) if x != "1658"}
        if left != grounds_g: t16bad.append(f"names {sorted(left)} as grounds of #1658; the graph holds {sorted(grounds_g)}")
cl = kernel["topology"]["clusters"]; overlap = sorted(set(joins) & (set(cl["functional"]) | set(cl["peripatetic"])))
if overlap: t16bad.append(f"joins also listed as cluster members: {overlap}")
ax = onto["state_axes"]
for st in kernel["topology"]["maker_count_states"]:
    if st.get("maker_count") not in ax["maker_count"] or (st.get("establishment") and st["establishment"] not in ax["establishment"]): t16bad.append(f"state of #{st['record']} outside the ontology's axes")
test("T16 the kernel's prose agrees with its lists and the graph", not t16bad, {"joins": len(joins), "grounds_of_1658": sorted(grounds_g), "failed": t16bad})

# back-projection v0.1, scored on the two declared scopes
pos = onto["positions"]; topo = kernel.get("topology", {})
scopeA = {
 "framework, seed, author": kernel["framework"]["canonical_record"] == "rec:123" and kernel["framework"]["author"] == "Lee Sharks",
 "four positions with the Theophrastan asymmetry": len(pos) == 4 and any(p.get("asymmetry") for p in pos),
 "six strata in order with their records": len(topo.get("strata_from_latest", [])) == 6 and all(s.get("records") for s in topo["strata_from_latest"]),
 "two clusters and the joins": set(topo.get("clusters", {})) == {"functional", "peripatetic"} and len(topo.get("joins", [])) >= 5,
 "four bodies with their rules": len(onto["evidence_bodies"]) == 4 and all(b.get("rule") for b in onto["evidence_bodies"].values()),
 "five maker-count states with dates and records": len(topo.get("maker_count_states", [])) == 5,
 "forbidden operations": len(kernel["uktp_seed"]["constraints"]) >= 5 and bool(kernel["litmus"]["forbidden_operation"]),
 "the dependency chain to the production model": "#1588" in kernel["litmus"]["dependency_chain"] and "#1583" in kernel["litmus"]["dependency_chain"],
 "the corrections as original–correction pairs": len(kernel.get("corrections", [])) >= 5,
 "the rival evaluated, with its summary": bool(kernel.get("rival", {}).get("summary")),
 "the lines of research": len(kernel.get("lines_of_research", [])) >= 5,
}
scopeB = dict(scopeA, **{
 "every record placed in a body and a stratum": all(any(e["source"] == r["@id"] and e["target"].startswith("body:") for e in E) and any(e["source"] == r["@id"] and e["target"].startswith("stratum:") for e in E) for r in recs if not r.get("external")),
 "every relation with its licensed dimension": not badrel,
 "every endpoint declared": not dangling,
 "provenance on every record": all(r.get("axn") and r.get("url") and r.get("sha256") for r in recs),
})
yA, yB = sum(scopeA.values()) / len(scopeA), sum(scopeB.values()) / len(scopeB)
thr = kernel["acceptance"]["back_projection_yield_threshold"]
counts = {"records": sum(1 for r in recs if not r.get("external")), "external_records": sum(1 for r in recs if r.get("external")), "positions": len(pos), "claims": len(claims),
          "withdrawn": sum(1 for c in claims if c["state"].get("assertion") == "withdrawn"), "bearing_on_rival": sum(1 for c in claims if c["state"].get("assertion") == "bears_on_rival"),
          "edges": len(E), "captures": len(caps), "events": len(events), "questions": len(questions), "structural_tests": len(R)}
out = {"kernel": kernel["id"], "version": kernel["version"], "counts": counts, "structural_tests": R, "propagation": propagation,
       "back_projection_v0_1": {"scope_A": {"elements": scopeA, "yield": round(yA, 3)}, "scope_B": {"elements": scopeB, "yield": round(yB, 3)}, "threshold": thr,
                                "note": "structural presence only; reconstructive validity is v1.0, run by a reader on scope A (09b)"},
       "not_checked": ["whether a reading is right", "whether a relation's warrant is sufficient", "reconstructive validity by a reader (v1.0)", "anything in a record beyond the quotations bound"],
       "integrity": {f: hashlib.sha256((K / f).read_bytes()).hexdigest() == h for f, h in yaml.safe_load((K / "11-integrity.yaml").read_text())["files"].items()}}
(K / "10-verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in R.items():
    d = v["detail"]; print(("PASS " if v["pass"] else "FAIL ") + k, "·", d if not isinstance(d, (list, dict)) else json.dumps(d, ensure_ascii=False)[:260])
print(f"back-projection v0.1: scope A {yA:.3f} ({sum(scopeA.values())}/{len(scopeA)}), scope B {yB:.3f} ({sum(scopeB.values())}/{len(scopeB)}); threshold {thr}")
for k, v in scopeB.items():
    if not v: print("  missing:", k)
print("counts:", counts); print("integrity:", "ok" if all(out["integrity"].values()) else out["integrity"])
