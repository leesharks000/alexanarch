#!/usr/bin/env python3
"""Structural verifier for a framework holographic kernel built on hkcore (EA-HK-FRAME-01 #1753, tests T1–T17 as they generalize).
Records results; writes 10-verification.json.   python3 verify_fw.py <alexanarch root> <kernel dir> [site root]"""
import json, sys, pathlib, re, hashlib, yaml
ROOT, KD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); SITE = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else None
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
CAP = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
K = yaml.safe_load((KD / "00-kernel.yaml").read_text(encoding="utf-8")); O = yaml.safe_load((KD / "01-ontology.yaml").read_text(encoding="utf-8"))
G = json.loads((KD / "02-graph.jsonld").read_text(encoding="utf-8"))
C = [json.loads(l) for l in (KD / "03-claims.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
E = [json.loads(l) for l in (KD / "05-temporal.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
Q = yaml.safe_load((KD / "06-questions.yaml").read_text(encoding="utf-8"))["questions"]
I = yaml.safe_load((KD / "11-integrity.yaml").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"\s+", " ", s.replace("*", "").replace("’", "'").replace("‘", "'"))
nodes = {x["@id"]: x for x in G["@graph"]}; CL = {c["id"]: c for c in C}; res = {}
def T(name, ok, detail): res[name] = {"pass": bool(ok), "detail": detail}

bad = [x["@id"] for x in G["@graph"] if x.get("@type") == "Record" and (x["axn"] != REG[x["deposit"]]["axn"] or x["sha256"] != REG[x["deposit"]]["hash"])]
badp = []
for k, v in (I.get("surfaces") or {}).items():
    page = nodes.get(k) or {}
    if SITE and page.get("url"):
        p = SITE / page["url"].split(".com/", 1)[1] / "index.html"
        if hashlib.sha256(p.read_bytes()).hexdigest() != v: badp.append(k)
T("T1 records resolve", not bad and not badp, f"{sum(1 for x in G['@graph'] if x.get('@type')=='Record')} records, {len(I.get('surfaces') or {})} surface pages; stale: {bad + badp}")
def src(rec):
    if not rec.startswith("rec:"): return None   # surface pages are checked by quotecheck against the clone; author statements are verbatim provenance
    r = REG[int(rec.split(":")[1])]; f = ROOT / r["full_text_path"].lstrip("/"); return norm(f.read_text(encoding="utf-8", errors="ignore")) + " " + norm(r.get("description") or "")
unb = []
for c in C:
    t = c["target"]
    if t.get("exact") is None: continue
    s = src(t["record"])
    if s is not None and norm(t["exact"]) not in s: unb.append(c["id"])
    if s is not None and t.get("record_sha256") != REG[int(t["record"].split(":")[1])]["hash"]: unb.append(c["id"] + " (hash)")
T("T2 quotations bind", not unb, f"{len(C)} claims; unbound: {unb}")
pol = O["relation_policy"]; off = [e for e in G["edges"] if e["family"] in ("evidentiary",) and (e["relation"] not in pol or e["licensed_dimension"] != pol[e["relation"]])]
T("T3 relations in policy", not off, f"{sum(1 for e in G['edges'] if e['family']=='evidentiary')} evidentiary edges; off-policy: {off}")
unres = [c["id"] for c in C if c["introduced"]["date"] is None]
T("T4 introductions established or marked", all(c["introduced"].get("basis") for c in C), f"unresolved and marked: {unres}")
bodies = K["topology"]["bodies"]; fail = {b: sum(1 for c in C if c["body"] == b and (c["state"].get("assertion") in ("withdrawn", "bears_on_rival") or c["state"].get("validation") == "failed_controls" or c["state"].get("reportability") in ("against", "station_failed"))) for b in bodies}
T("T6 failures per body", all(fail.values()), fail)
by_axis = {}
for e in E:
    if e["event"].endswith("_state"): by_axis.setdefault(e["axis"], []).append(e)
order_ok, det = True, {}
for ax, es in by_axis.items():
    ds = [e["date"] for e in es]; order_ok &= ds == sorted(ds)
    for e in es:
        w = CL[e["warrant"].split(":", 1)[1]]; order_ok &= w["target"]["record"] == e["object"]
    det[ax] = [f"{e['date']} {e['object']} {e['state']}" for e in es]
T("T7 states ordered and bound", order_ok, det)
joins = K["topology"]["joins"]; hl = {e["source"] for e in G["edges"] if e["relation"] == "joins" and "historical-logos" in e["target"]}
miss = [j for j in joins if (j if isinstance(j, str) else f"rec:{j}") not in hl]
T("T8 joins edged to the Historical Logos", not miss, f"{len(joins)} joins; missing: {miss}")
uc = [x["slug"] for x in G["@graph"] if x.get("@type") == "Capture" and x["slug"] not in CAP]
T("T9 captures resolve", not uc, f"{sum(1 for x in G['@graph'] if x.get('@type')=='Capture')} captures; unresolved: {uc}")
rows = K["symmetric_ledger"]["rows"]; rv = next(x for x in G["@graph"] if x.get("@type") == "RivalFramework")
# v1.0: both sides of every row; the claim carries the row's body among its claim-local bodies (principal or ledger role)
mism = [(b, side, w) for b, row in rows.items() for side, cell in row.items() if isinstance(cell, dict) and "warrants" in cell
        for w in cell["warrants"] if w not in CL or b not in (CL[w].get("bodies") or {CL[w]["body"]: "principal"})]
gnode = {x["@id"]: x for x in G["@graph"] if x.get("@type") == "Claim"}
drift = [w for w in CL if gnode.get(f"claim:{w}", {}).get("bodies") not in (None, CL[w].get("bodies"))]
T("T11 every ledger warrant, both sides, carries its row's body claim-locally", not mism and not drift, {"mismatched": mism, "graph_claim_bodies_differ": drift})
ids = set(nodes) | {f"claim:{c['id']}" for c in C}
und = [e for e in G["edges"] if e["source"] not in ids or e["target"] not in ids]
T("T14 endpoints declared", not und, f"{len(G['edges'])} edges; undeclared: {[(e['source'], e['target']) for e in und][:6]}")
qf = [q["id"] for q in Q if not (q.get("advances_if") and q.get("retreats_if") and q.get("unchanged_if") and q.get("posed_in", {}).get("exact"))]
T("T15 lines of research posed and bounded", not qf, f"{len(Q)} questions; failed: {qf}")
fw_keys = [k for k in next(iter(rows.values())) if k != "rule"]
lf = [b for b in bodies if b not in rows or any(k not in rows[b] for k in fw_keys) or any(not rows[b][k].get("warrants") for k in fw_keys)]
T("T17 the symmetric ledger: one question, both frameworks, every body", not lf, {"frameworks": fw_keys, "failed": lf})
dep = K.get("dependency")
if dep:
    # change one rung's standing and propagate along depends_on; the result must equal the ladder's declared consequence for every rung
    R_ = {r["@id"]: r for r in O.get("rungs", [])}
    def falls(x):
        out_, frontier = {x}, [x]
        while frontier:
            y = frontier.pop()
            for k, r in R_.items():
                if y in (r.get("depends_on") or []) and k not in out_: out_.add(k); frontier.append(k)
        return sorted(out_)
    got = {k: falls(k) for k in R_}; exp = {k: sorted(v) for k, v in dep["consequence_of_defeat"].items()}
    T("T18 dependency propagates as the ladder states", got == exp, {"propagated": got, "declared": exp})
try:
    from pyld import jsonld
    X = jsonld.expand(G); flat = X[0] if X else {}
    node_iris = {n["@id"] for n in flat.get("@graph", []) if "@id" in n}
    edges_key = next(k for k in flat if k.endswith("#edges"))
    bad_e = []
    for e in flat[edges_key]:
        for end in ("source", "target"):
            k = next(k for k in e if k.endswith("#" + end))
            v = e[k][0]
            if "@id" not in v or v["@id"] not in node_iris: bad_e.append((end, v))
    T("T19 JSON-LD: every edge endpoint expands to the IRI of a declared node", not bad_e, {"edges": len(flat[edges_key]), "nodes": len(node_iris), "failed": bad_e[:6]})
except ImportError:
    T("T19 JSON-LD: every edge endpoint expands to the IRI of a declared node", False, "pyld not installed")
out = {"kernel": K["id"], "version": K["version"], "structural_tests": res,
       "integrity": {f: hashlib.sha256((KD / f).read_bytes()).hexdigest() == h for f, h in I["files"].items()},
       "not_checked": ["whether a reading is right", "whether a relation's warrant is sufficient", "reconstructive validity by a reader (v1.0)"]}
(KD / "10-verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in res.items(): print(("PASS " if v["pass"] else "FAIL ") + k, "" if v["pass"] else v["detail"])
print("integrity:", all(out["integrity"].values()))
