#!/usr/bin/env python3
"""Verifier of EA-HK-DAFFODILS-01 (after verify_fw.py, #1753 T1–T17 as they apply). Laws record; they do not prevent: results are written
to 10-verification.json and nothing is blocked.   python3 verify_daffodils.py <alexanarch root> <kernel dir>"""
import json, sys, pathlib, re, hashlib, yaml
ROOT, KD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
OFFLINE = not (ROOT / "data/registry.json").exists()   # pass "offline" (or any path without the archive) to verify from the package alone
if OFFLINE:
    X = json.loads((KD.parent / "operator/registry-extract.json").read_text(encoding="utf-8"))["records"]
    REG = {int(n): {"axn": r["axn"], "hash": r["hash"], "description": r.get("description"), "full_text_path": f"sources/current/{n}.md"} for n, r in X.items()}
    ROOT = KD.parent
else:
    REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
L = lambda f: [json.loads(l) for l in (KD / f).read_text(encoding="utf-8").splitlines() if l.strip()]
Y = lambda f: yaml.safe_load((KD / f).read_text(encoding="utf-8"))
K, O, Q, T9, I = Y("00-kernel.yaml"), Y("01-ontology.yaml"), Y("06-questions.yaml")["questions"], Y("09-tests.yaml"), Y("11-integrity.yaml")
G = json.loads((KD / "02-graph.jsonld").read_text(encoding="utf-8")); C = L("03-claims.jsonl"); CL = {c["id"]: c for c in C}
norm = lambda s: re.sub(r"\s+", " ", s.replace("*", "").replace("’", "'").replace("‘", "'"))
nodes = {x["@id"]: x for x in G["@graph"]}; res = {}
def T(n, ok, d): res[n] = {"pass": bool(ok), "detail": d}
surf_path = {}
OP = KD.parent / "operator"; SD = KD.parent / "surfaces"
for x in G["@graph"]:
    if x.get("@type") == "SurfaceRecord": surf_path[x["@id"]] = x
bad = [x["@id"] for x in G["@graph"] if x.get("@type") == "Record" and (x["axn"] != REG[x["deposit"]]["axn"] or x["sha256"] != REG[x["deposit"]]["hash"])]
stale = [k for k, v in I["surfaces"].items() if (SD / f"{k.split(':')[1]}.txt").exists() and hashlib.sha256((SD / f"{k.split(':')[1]}.txt").read_bytes()).hexdigest() != v]
T("T1 records resolve", not bad and not stale, f"{sum(1 for x in G['@graph'] if x.get('@type')=='Record')} records, {len(I['surfaces'])} surfaces; stale: {bad + stale}")
MAP = KD.parent / K["map"]["file"]; mapok = hashlib.sha256(MAP.read_bytes()).hexdigest() == K["map"]["sha256"]
def src(rec):
    if rec.startswith("rec:"):
        r = REG[int(rec[4:])]; return norm((ROOT / r["full_text_path"].lstrip("/")).read_text(encoding="utf-8", errors="ignore")) + " " + norm(r.get("description") or "")
    if rec == "map:daffodils": return norm(MAP.read_text(encoding="utf-8"))
    return norm((SD / f"{rec.split(':')[1]}.txt").read_text(encoding="utf-8"))
unb = [c["id"] for c in C if c["target"].get("exact") and norm(c["target"]["exact"]) not in src(c["target"]["record"])]
T("T2 quotations bind", not unb and mapok, f"{len(C)} claims; unbound: {unb}; map hash matches: {mapok}")
pol = O["relation_policy"]; ev = [e for e in G["edges"] if e["family"] == "evidentiary"]
off = [e for e in ev if e["relation"] not in pol or e["licensed_dimension"] != pol[e["relation"]]]
T("T3 relations in policy", not off, f"{len(ev)} evidentiary edges; off-policy: {off}")
T("T4 introductions marked", all(c["introduced"].get("basis") for c in C), f"unresolved and marked: {[c['id'] for c in C if c['introduced'].get('date') is None]}")
ids = set(nodes) | {f"claim:{c['id']}" for c in C}
und = sorted({e[k] for e in G["edges"] for k in ("source", "target") if e[k] not in ids})
T("T14 endpoints declared", not und, f"undeclared: {und}")
need = ("question", "posed_in", "body", "bears_on", "how_to_ask", "machine_investigation", "advances_if", "retreats_if", "unchanged_if", "consequence")
qbad = [q["id"] for q in Q if any(not q.get(k) and q.get(k) != [] for k in need) or any(m not in ids for x in q["consequence"] for m in x["moves"]) or any(b not in ids for b in q["bears_on"])
        or any(not x.get("effect") for x in q["consequence"])]
qpose = [q["id"] for q in Q if norm(q["posed_in"]["exact"]) not in norm(MAP.read_text(encoding="utf-8"))]
T("T15 questions complete", not qbad and not qpose, f"{len(Q)} questions; incomplete: {qbad}; posed_in unbound: {qpose}")
rows = K["symmetric_ledger"]["rows"]; asym = []
for b, row in rows.items():
    for side in ("daffodils", "received_flagship"):
        cell = row.get(side) or {}
        if not cell.get("text") or not cell.get("warrants"): asym.append(f"{b}:{side} empty")
        for w in cell.get("warrants", []):
            if w not in CL: asym.append(f"{b}:{side}:{w} missing")
    if not row.get("withheld_from_both"): asym.append(f"{b}: nothing withheld stated")
    for side in ("daffodils", "received_flagship"):
        if not any(CL[w]["body"] == b for w in (row.get(side) or {}).get("warrants", []) if w in CL): asym.append(f"{b}:{side} has no warrant of its own body")
own = {b: sum(1 for w in r["daffodils"]["warrants"] + r["received_flagship"]["warrants"] if CL[w]["body"] == b) for b, r in rows.items()}
T("T17 ledger symmetric", not asym and set(rows) == set(O["evidence_bodies"]), f"rows {sorted(rows)}; defects: {asym}; warrants of the row's own body: {own}")
flags = set(O["failure_flags"]); unk = [a["q"] for a in T9["adversarial_queries"] if not any(f in a["fail_if"] for f in flags)]
T("TA adversarial queries name defined flags", not unk, f"{len(T9['adversarial_queries'])} queries; naming no flag: {unk}; flags defined: {len(flags)}")
miss = [s["text"][:60] for s in K["author_statements"] if s["in_map"] and norm(s["text"]) not in norm(MAP.read_text(encoding="utf-8"))]
T("TB author statements verbatim", not miss, f"{len(K['author_statements'])} statements; quoted in the map: {sum(s['in_map'] for s in K['author_statements'])}; mismatched: {miss}")
# T16: the kernel's prose agrees with its lists (after #1753 §6.3)
t16 = []
summ = K["compression_survival_summary"]
for key in ("K1", "K2", "K3", "K4", "K5"):
    if not (K.get("criteria", {}).get(key) or {}).get("asks"): t16.append(f"{key} undefined")
if set("abcdef") - set(K.get("points_of_contact", {})): t16.append("points of contact incomplete")
if K.get("accountable_editor", {}).get("name", "") not in summ: t16.append("editor unnamed in summary")
if "none reopened" in json.dumps(rows["A"]): t16.append("ledger A says none reopened where the summary says almost never")
oc = K.get("object_coding", {}); 
if oc and oc["fixed_point"] + oc["rereading"] + oc["ancient_reception"] + oc["unsettling"] != 185: t16.append("coding classes do not sum to 185")
for n in ("405", "37", "782", "184", "153", "185"):
    if n not in summ: t16.append(f"count {n} missing from summary")
if not all(isinstance(q, dict) and q.get("advances_if") for q in K["lines_of_research"]): t16.append("lines of research without results in scope A")
if len(K.get("four_functions", [])) != 4: t16.append("four functions not enumerated")
T("T16 prose agrees with lists", not t16, f"defects: {t16}")
# back-projection v0.1: structural presence of must_survive in scope A (00 + 01)
A = json.dumps(K, ensure_ascii=False) + json.dumps(O, ensure_ascii=False)
probe = {"the identity and the map's status": ["EA-HK-DAFFODILS-01", "not deposited"], "the six bodies and their rules": ["RA:", "RB:", "RC:", "RD", "RE:", "RF:"],
         "the findings with their counts": ["405", "37", "782", "184"], "the rival at its strength": ["stated_at_strength"], "the symmetric ledger": ["withheld_from_both"],
         "the concession": ["Real defects are conceded"], "the two-relation repair test": ["two-relation"], "K1–K5 with the K2 count": ["five criteria", "two are redirected and four are absent"],
         "the allegation and its control": ["authorship allegation", "2015 article"], "the author statements": ["author_statements"], "the lines of research": ["Q1-repair", "Q8-entry"],
         "the failure flags": ["DISPUTE_REDUCTION", "BURDEN_ONE_WAY", "MOTIVE_SUPPLIED"]}
present = {k: all(p in A for p in v) for k, v in probe.items()}
y = sum(present.values()) / len(present)
T("BP v0.1 structural presence (scope A; string probes, not reconstruction)", y >= 0.85, f"yield {y:.3f}; missing: {[k for k, v in present.items() if not v]}")
out = {"id": K["id"] + "/verification", "mode": "offline, from the package" if OFFLINE else "against the archive clone", "kernel_version": K["version"], "built": K["built"], "results": res, "passed": sum(v["pass"] for v in res.values()), "of": len(res),
       "not_checked": ["whether a reading is right or a warrant sufficient", "back-projection v1.0 (reconstructive validity), which needs readers on 09b",
                       "the six points' selection, which is the map's", "the context of passages read only in quotation"]}
(KD / "10-verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in res.items(): print(("PASS " if v["pass"] else "FAIL ") + k + " — " + v["detail"][:200])
