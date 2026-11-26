#!/usr/bin/env python3
"""v1.5 of EA-HK-REVFIRST-01 (2026-11-26), applied to the built v1.4 kernel in place. At the author's word:
  12:03  "it should not have withdrawn it. it is not evidence of priority but it *is* evidence that pauline priority is inferential rather than grounded in material witness."
  12:03  "its just about what kind of evidence it is"
  12:04  "its not evidence of priority but its also not not evidence of priority"
  12:05  "its a relevant datum in any case"
  12:18  "yes, lets correct the hologram, and while we're at it we might as well update and expand it - how much you wanna bet at the very least has come after and should be represented in the hologram."
Three things, in this order: (A) every record node, claim and move re-bound to the record's current AXN and hash (three records had a References list added in place
on 2026-11-23); (B) the papyri claim of #202 recoded from withdrawn to held, bounded by #1735 §II.3, with the sentences of #202 Claim 3 and #1735 §II.3 entered as claims;
(C) a new stratum for the records deposited after the first kernel (#1759, #1760, #1762, #1765, #1810, #1811), each with anchor claims quoted verbatim. The argument
moves of the new records are not written on this pass and are declared owed (the precedent is v1.2, whose moves came at v1.3).
The v1.4 builder's scratch inputs are not needed: this script reads and writes the kernel files.
    python3 v15_patch.py <alexanarch root> <kernel dir>"""
import json, sys, pathlib, re, hashlib, subprocess, yaml
ROOT, KD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
norm = lambda s: re.sub(r"\s+", " ", s.replace("*", "").replace("’", "'").replace("‘", "'"))
BUILT = "2026-11-26"
dump_yaml = lambda p, o: (KD / p).write_text(yaml.safe_dump(o, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
lines = lambda p: [json.loads(l) for l in (KD / p).read_text(encoding="utf-8").splitlines() if l.strip()]
write_lines = lambda p, rows: (KD / p).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
K = yaml.safe_load((KD / "00-kernel.yaml").read_text(encoding="utf-8")); assert str(K["version"]) == "1.4", K["version"]
G = json.loads((KD / "02-graph.jsonld").read_text(encoding="utf-8")); C = lines("03-claims.jsonl"); E = lines("05-temporal.jsonl")
A = [json.loads(l) for l in (KD / "04-arguments.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
T9 = yaml.safe_load((KD / "09-tests.yaml").read_text(encoding="utf-8"))
nodes = {x["@id"]: x for x in G["@graph"]}; CL = {c["id"]: c for c in C}
text = lambda n: (ROOT / REG[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
src = lambda n: norm(text(n)) + " " + norm(REG[n].get("description") or "")
git = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout

# ---------------------------------------------------------------- (A) re-bind to current hashes
refreshed = []
for x in G["@graph"]:
    if x.get("@type") != "Record": continue
    r = REG[x["deposit"]]
    if x["axn"] != r["axn"] or x["sha256"] != r["hash"]:
        refreshed.append({"record": x["@id"], "deposit": x["deposit"], "axn_before": x["axn"], "axn": r["axn"], "sha256_before": x["sha256"], "sha256": r["hash"],
                          "change": "; ".join(f"{m.get('date')}: {m.get('reason')}" for m in (r.get("modifications") or []) if (m.get("date") or "") > "2026-11-11")})
        x.update({"axn": r["axn"], "sha256": r["hash"], "version": r.get("version"), "title": r["title"], "status": r.get("status")})
stale_n = {f["deposit"] for f in refreshed}
for c in C:
    t = c["target"]
    if t["record"].startswith("rec:") and int(t["record"][4:]) in stale_n:
        n = int(t["record"][4:]); assert norm(t["exact"]) in src(n), ("quotation no longer in record", c["id"])
        t["axn"], t["record_sha256"] = REG[n]["axn"], REG[n]["hash"]
moves_rebound = 0
for a in A:
    n = int(a["record"][4:])
    if n in stale_n:
        assert a["exact"] in text(n), ("move no longer verbatim", a["@id"])
        a["axn"], a["record_sha256"] = REG[n]["axn"], REG[n]["hash"]; moves_rebound += 1
for f in refreshed:
    E.append({"timeline": "historical", "date": "2026-11-23", "event": "modified_in_place", "object": f["record"], "axn_before": f["axn_before"], "axn": f["axn"],
              "note": "standard References list added in place; version unchanged; every claim and move of the record re-asserted verbatim against the new text at v1.5"})

# ---------------------------------------------------------------- claims: helper with git-established introduction
_FIRST = {}
def introduced(n, quote):
    r = REG[n]; p = r["full_text_path"].lstrip("/")
    if p not in _FIRST:
        log = git("log", "--diff-filter=A", "--format=%h %ad", "--date=short", "--", p).strip().splitlines()
        _FIRST[p] = (log[-1].split()[:2] + [git("show", f"{log[-1].split()[0]}:{p}")]) if log else None
    log = _FIRST[p]
    base = {"record_date": r["date"]}
    if log:
        h, d, first = log; base.update({"first_seating": d, "first_seating_commit": h})
        if norm(quote) in norm(first):
            return {"date": d, "basis": "present at the record's first seating in this repository", "first_text_sha256": hashlib.sha256(first.encode("utf-8")).hexdigest(), **base,
                    **({"note": "the record is dated earlier than its first seating here; presence before the first seating is not attested by this repository"} if r["date"] < d else {})}
    return {"date": None, "basis": "present in the current version; introduction date unresolved", **base,
            "current_version_since": (r.get("reissue_history") or [{}])[-1].get("date") or r.get("date_modified") or r["date"]}
NEWC = []
def claim(cid, n, quote, kind, state, body, notes=None, role="standing", bodies=None):
    assert cid not in CL, cid
    t, d = norm(text(n)), norm(REG[n].get("description") or ""); q = norm(quote)
    assert q in t or q in d, ("quotation not in record", cid, quote[:70])
    c = {"id": cid, "claim_kind": kind, "role": role, "target": {"record": f"rec:{n}", "axn": REG[n]["axn"], "record_sha256": REG[n]["hash"], "exact": quote, "located_in": "text" if q in t else "description"},
         "state": state, "body": body, "introduced": introduced(n, quote), "bodies": bodies or {body: "principal"}}
    if notes: c["notes"] = notes
    C.append(c); CL[cid] = c; NEWC.append(cid)
    G["@graph"].append({"@id": f"claim:{cid}", "@type": "Claim", "target": f"rec:{n}", "bodies": c["bodies"]})
    E.append({"timeline": "epistemic", "date": c["introduced"]["date"], "event": "introduced", "object": f"claim:{cid}", "basis": c["introduced"]["basis"], "role": role})
A_ = lambda a="asserted", **k: {"assertion": a, **k}

# ---------------------------------------------------------------- (B) the papyri: held, bounded; the kind of evidence
RULINGS_B = [{"at": "2026-11-26 12:03", "text": "it should not have withdrawn it. it is not evidence of priority but it *is* evidence that pauline priority is inferential rather than grounded in material witness."},
             {"at": "2026-11-26 12:03", "text": "its just about what kind of evidence it is"},
             {"at": "2026-11-26 12:04", "text": "its not evidence of priority but its also not not evidence of priority"},
             {"at": "2026-11-26 12:05", "text": "its a relevant datum in any case"}]
WARRANT_B = ("the papyrological inversion held, its strength bounded by kind of evidence: not evidence of priority, and not not evidence of priority; evidence that Pauline "
             "priority is inferential rather than grounded in material witness; a relevant datum in any case (the author, 2026-11-26). 'The physical record cannot rescue "
             "absolute priority, but it also cannot close the bounded questions' (#1735 §II.3). Coded 'rebuts' and 'withdrawn' in v1.0–v1.4; corrected at v1.5 on the author's ruling")
p = CL["rf-202-papyri"]; before_state = dict(p["state"]); assert before_state["assertion"] == "withdrawn"
p["state"] = {"assertion": "held", "bounded_by": "claim:rf-1735-physical", "bound": "kind of evidence", "rung": "I",
              "ruling": "the author, 2026-11-26 12:03: not evidence of priority; evidence that Pauline priority is inferential rather than grounded in material witness"}
p["role"] = "standing"
p["notes"] = ("Coded withdrawn (retained as a historical object) in v1.0–v1.4, on a reading of #1735 §II.3 as a withdrawal. #202 Claim 3 does not offer the papyri as proof of "
              "priority: 'The asymmetry is not between two sets of facts.' The author ruled the coding wrong on 2026-11-26; the claim is held and its strength bounded.")
e_old = [e for e in G["edges"] if e["target"] == "claim:rf-202-papyri" and e["relation"] == "rebuts"]; assert len(e_old) == 1
e_old[0].update({"relation": "bounds", "licensed_dimension": "strength", "warrant": WARRANT_B, "provenance": "the author's ruling, 2026-11-26 12:03–12:05; map v1.5"})
for e in E:
    if e.get("object") == "claim:rf-202-papyri" and e["event"] == "withdrawn":
        e.update({"event": "bounded", "note": "recorded as 'withdrawn' in v1.0–v1.4; recoded at v1.5 on the author's ruling of 2026-11-26"})
    if e.get("object") == "claim:rf-202-papyri" and e["event"] == "introduced": e["role"] = "standing"
E.append({"timeline": "epistemic", "date": "2026-11-26", "event": "bounded", "object": "claim:rf-202-papyri", "by": "claim:rf-1735-physical",
          "basis": "the author's ruling, 12:03–12:05: held; not evidence of priority, and not not evidence of priority; evidence that Pauline priority is inferential rather than grounded in material witness"})
corr_before = K["corrections"]; K["corrections"] = []
K["corrections_history"] = [{"original": "claim:rf-202-papyri", "correction": "claim:rf-1735-physical", "relation": "rebuts", "in_versions": "v1.0–v1.4",
                             "status": "recoded at v1.5 as a bound (see bounds); the author, 2026-11-26: 'it should not have withdrawn it'"}]
claim("rf-202-inferential", 202, "Pauline priority is inferential, not direct material fact.", "generality", A_(rung="II"), "D")
claim("rf-202-asymmetry", 202, "It is between the confidence with which Pauline chronological priority is asserted and the actual evidentiary basis for that confidence.", "generality", A_(rung="II"), "D",
      notes="The sentence before it: 'The asymmetry is not between two sets of facts.' This is what the papyri are evidence of in #202.")
claim("rf-202-unsettle", 202, "material attestation must be allowed to unsettle inherited priority", "interpretation", A_(rung="II"), "D")
claim("rf-1735-masquerade", 1735, "manuscript survival must not masquerade as a date of composition", "generality", A_(rung="I"), "D")
claim("rf-1735-chain-each-side", 1735, "the correct symmetry is not to flatten all inference into equivalence but to identify the chain on each side", "generality", A_(rung="II"), "D")
claim("rf-1735-neutral", 1735, "The material finding is therefore neutral", "interpretation", A_(rung="I", scope="composition dates"), "D",
      notes="Neutral as to dates of composition (§II.3: 'These objects establish circulation, not composition'). The author, 2026-11-26: the papyri are 'a relevant datum in any case', "
            "evidence that Pauline priority is inferential rather than grounded in material witness. The sentence is scoped here and is not edited in #1735.")

# ---------------------------------------------------------------- (C) the stratum after the first kernel
SID = "S00-after-the-first-kernel"; SLABEL = "After the first kernel: the Josephus thesis told and its texts seated, the names crossed, the recovery valued, the name defended (11–26 November)"
NEW = {1810: ("R", ["D", "C", "G"], ["chronology"]), 1811: ("R", [], ["chronology"]), 1765: ("H", ["R"], ["heteronymy"]),
       1762: ("H", ["C"], ["heteronymy"]), 1760: ("H", [], ["heteronymy"]), 1759: ("H", ["R"], ["heteronymy"])}
have = {x["deposit"] for x in G["@graph"] if x.get("@type") == "Record"}; assert not (set(NEW) & have), set(NEW) & have
for x in G["@graph"]:
    if x.get("@type") == "Stratum": x["order_from_latest"] += 1
G["@graph"].append({"@id": f"stratum:{SID}", "@type": "Stratum", "label": SLABEL, "order_from_latest": 1})
for n, (b, sec, cls) in NEW.items():
    r = REG[n]
    G["@graph"].append({"@id": f"rec:{n}", "@type": "Record", "deposit": n, "axn": r["axn"], "url": f"https://www.alexanarch.org/s/records/{n}/", "title": r["title"], "date": r["date"],
                        "status": r.get("status"), "version": r.get("version"), "sha256": r["hash"], "creator": r.get("creator") or r.get("authors"), "body": b, "body_secondary": sec,
                        "stratum": SID, "clusters": cls})
    for tgt in (f"body:{b}", f"stratum:{SID}"):
        G["edges"].append({"source": f"rec:{n}", "relation": "belongs_to", "target": tgt, "family": "structural", "licensed_dimension": None, "warrant": "map", "provenance": "map v1.5"})
    E.append({"timeline": "historical", "date": r["date"], "event": "deposited", "object": f"rec:{n}", "axn": r["axn"]})
    for h in r.get("reissue_history") or []:
        E.append({"timeline": "historical", "date": h["date"], "event": "reissued_in_place", "object": f"rec:{n}", "from": h["from_version"], "to": h["to_version"], "axn_before": h["axn_before_reissue"]})
    for c in cls: K["topology"]["clusters"][c].append(n)
K["topology"]["strata_from_latest"].insert(0, {"id": SID, "label": SLABEL, "records": list(NEW)})

BOUND_J = {"assertion": "held", "bounded_by": "claim:rf-1217-josephus-available", "advancement": "suspended (the author, 2026-11-09 09:52)", "rung": "V"}
# #1810 How Much You Wanna Bet? (SEVP-VAL-003 v1.1)
claim("rf-1810-not-demonstrate", 1810, "The dossier does not demonstrate the thesis.", "generality", A_(), "R")
claim("rf-1810-conditional", 1810, "The dossier is conditional throughout, and each claim carries the status #1735 gives it.", "generality", A_(), "R")
claim("rf-1810-early-insufficient", 1810, "an early date is insufficient for priority", "generality", A_(rung="I"), "D", bodies={"D": "principal"})
claim("rf-1810-load", 1810, "It is the least number of panel items that must be re-grounded for the target distinction δ to be admitted.", "instrument",
      {"specification": "specified", "validation": "run"}, "R", notes="The transition load Θ, on a declared panel; computed on Panel CHA (§6.2). Its unit is the panel item.")
claim("rf-1810-no-valuation", 1810, "It issues no valid monetary valuation.", "generality", A_(), "R")
claim("rf-1810-invalid-figure", 1810, "a deliberately invalid monetary commensuration, preserved as an artifact; not an estimate of the recovery's value", "observation", A_(), "R",
      notes="The figure is $7.2 × 10²⁶, audited to failure on eight counts (§9a). Wherever the figure travels, its invalidity travels with it.")
claim("rf-1810-excludes-v-vi", 1810, "Rungs V and VI of the ladder (the Josephus thesis; the permanent incarnation).", "generality", A_(rung="V", excluded_from_object=True), "R",
      notes="Listed under §2.3 Excluded: they 'fall without disturbing I–IV' (#1755, INV-3) and would need their own dossier.")
# #1811 Revelation First ≠ The First Revelation (EA-MPAI-REVFIRST-02 v1.1)
claim("rf-1811-two-names", 1811, "Revelation First predicates priority of a book. The First Revelation selects an event by its ordinal position.", "generality", A_(), "R")
claim("rf-1811-erasure", 1811, "A composition keeps every lexical element of a name and destroys the relation between them.", "observation", A_(operation="directional propositional erasure"), "R")
claim("rf-1811-liquidation", 1811, "The removal of a proposition's standing through rearrangement of its surviving constituents.", "observation", A_(operation="positional liquidation"), "R")
claim("rf-1811-homology", 1811, "The operation performed on the name is the operation the thesis describes for the book.", "interpretation", A_(), "R")
claim("rf-1811-homology-limit", 1811, "The homology is therefore between the composition and the thesis's claim.", "generality", A_(), "R")
# #1759 The Josephus Thesis: The Custody of the Name (Sparrow Wells)
claim("rf-1759-levels", 1759, "its evidentiary levels (demonstrated, attested, held) are carried in the notes", "generality", A_(rung="V"), "H")
claim("rf-1759-one-intelligence", 1759, "author-functions of one literary intelligence under capture, speaking as many because the one could not speak as himself", "interpretation", dict(BOUND_J), "H",
      notes="A narrative; the reading 'the narrative takes'. Held at rung V under the bound of #1217, its advancement suspended by the author.")
claim("rf-1759-unresolved", 1759, "The tension cannot be resolved, and the narrative does not try to resolve it.", "generality", A_(rung="V"), "H")
# #1760 the thirty-seventh seating
claim("rf-1760-text-layer", 1760, "The text layer the negative search of EA-CORPORA-01/12 (#1510) could not find, held for The Josephus Thesis (#1759).", "observation", A_(rung="V"), "H")
# #1762 The Crossing of Names
claim("rf-1762-operation", 1762, "the organized crossing of names helps bind the literary field itself", "interpretation", A_(), "H", bodies={"H": "principal"})
claim("rf-1762-inventories", 1762, "Alternative identity maps become inventories of proposed crossings, to be tested at the level of their constituent relations.", "generality", A_(rung="V"), "H")
# #1765 The Word That Became Text v2.3
claim("rf-1765-standing", 1765, "The paper begins from that standing and does not re-derive it.", "generality", A_(rung="V"), "H",
      notes="The standing: Revelation First holds the Josephus thesis as an available reading that 'carries no first burden of proof' (#1217), and the Slavonic as 'a carrier under test, not a settled witness' (#1755, rung V).")
claim("rf-1765-census", 1765, "of sixty-six catalogued additions, 32 are better explained by Josephus's account of an earlier version and 2 by the translator's", "observation", A_(rung="V"), "H",
      notes="The census of the whole Slavonic Jewish War (Part I, §II-B, Appendix IV): 25 undecided, 7 features of translation; of the fifty-one with no Christian subject, none goes to the translator.")

# ---------------------------------------------------------------- kernel: version, bounds, statements, the fold-in record
K["version"] = "1.5"; K["built"] = BUILT
K["bounds"].append({"held": "claim:rf-202-papyri", "bounded_by": "claim:rf-1735-physical", "relation": "bounds", "warrant": WARRANT_B})
K["author_statements"].append({"date": "2026-11-26T12:03-05:00", "where": "in session, on a Google AI Overview of the thesis that carried the papyri table and a capture record that called it withdrawn",
    "text": " / ".join(r["text"] for r in RULINGS_B),
    "status": "the author's position on the papyri (rung I and II): held; not evidence of priority, and not not evidence of priority; evidence that Pauline priority is inferential rather than grounded in material witness"})
K["compression_survival_summary"] = K["compression_survival_summary"].rstrip() + (
    " The papyri (𝔓52, 𝔓98, 𝔓46; #202 Claim 3) are held and bounded by #1735 §II.3: they do not date composition and are not offered as proof of priority; they are evidence that Pauline "
    "priority is inferential rather than grounded in material witness. Since the first kernel the Josephus thesis has been told as a narrative with its evidentiary levels in the notes (#1759), "
    "its Slavonic text layer seated and scored (#1760, #1765), names read as operations across the field (#1762), the recovery valued from both ends with no valid monetary figure (#1810), "
    "and the thesis's name kept apart from the First Revelation, whose reordering of the two words repeats on the name what the thesis holds was done to the book (#1811).")
AL = K["argument_layer"]; AL["records_without_moves"] = sorted(NEW)
AL["owed_v15"] = ("the six records of stratum " + SID + " enter with anchor claims and without argument moves; their moves are owed, each record to be read in full and compressed into verbatim moves "
                  "as at v1.3. The 3,051 moves of the forty-nine earlier records stand, " + str(moves_rebound) + " of them re-bound to their records' current hashes.")
K["fold_in_v15"] = {
 "date": BUILT,
 "rulings": RULINGS_B + [{"at": "2026-11-26 12:18", "text": "yes, lets correct the hologram, and while we're at it we might as well update and expand it - how much you wanna bet at the very least has come after and should be represented in the hologram."}],
 "correction": {"claim": "claim:rf-202-papyri", "state_before": before_state, "state": p["state"], "edge_before": {"relation": "rebuts", "licensed_dimension": "establishment"},
                "edge": {"relation": "bounds", "licensed_dimension": "strength"}, "corrections_before": corr_before,
                "found_by": "a capture of 2026-11-26 (revelation-first-thesis-all-aspects-aio-20261126) whose first seating followed this kernel's coding and called the papyri table 'a withdrawn argument carried as live'",
                "claims_added": ["claim:rf-202-inferential", "claim:rf-202-asymmetry", "claim:rf-202-unsettle", "claim:rf-1735-masquerade", "claim:rf-1735-chain-each-side", "claim:rf-1735-neutral"]},
 "rebound": refreshed, "moves_rebound": moves_rebound,
 "stratum": {"id": SID, "label": SLABEL},
 "records": [{"record": f"rec:{n}", "deposit": n, "version": REG[n]["version"], "axn": REG[n]["axn"], "sha256": REG[n]["hash"], "body": NEW[n][0], "body_secondary": NEW[n][1]} for n in NEW],
 "claims_added": [f"claim:{c}" for c in NEWC],
 "not_joined": "#1765 is the Josephus station of the Historical Logos (#1757) and is not added to this kernel's joins on this pass; #1757 and #1756 are not versioned",
 "not_folded": "records of the same weeks that bear on the framework from outside it and are left as related work: #1795 (Why I Believe in Hell), #1798 (Either Forgery or Fact), #1802 (Who Benefits from Bad Inference?)",
 "moves": "none written at v1.5; owed for " + ", ".join(f"#{n}" for n in sorted(NEW)),
 "method": "applied to the built v1.4 kernel by operator/v15_patch.py; the v1.4 builder was not re-run"}
T9["structural"].append("T22 (v1.5) records without moves are declared in argument_layer.records_without_moves")

# ---------------------------------------------------------------- write, integrity
E.sort(key=lambda e: (0 if e["timeline"] == "epistemic" else 1) if False else 0)   # order kept as built; new events appended
dump_yaml("00-kernel.yaml", K)
(KD / "02-graph.jsonld").write_text(json.dumps(G, ensure_ascii=False, indent=1), encoding="utf-8")
write_lines("03-claims.jsonl", C); write_lines("05-temporal.jsonl", E)
(KD / "04-arguments.jsonl").write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a in A), encoding="utf-8")
dump_yaml("09-tests.yaml", T9)
I = yaml.safe_load((KD / "11-integrity.yaml").read_text(encoding="utf-8"))
files = sorted(q.name for q in KD.iterdir() if q.is_file() and q.name not in ("11-integrity.yaml", "10-verification.json"))
I.update({"built": BUILT, "registry_sha256": hashlib.sha256((ROOT / "data/registry.json").read_bytes()).hexdigest(),
          "captures_sha256": hashlib.sha256((ROOT / "data/EA-WG-CAPTURES-01.json").read_bytes()).hexdigest(),
          "files": {f: hashlib.sha256((KD / f).read_bytes()).hexdigest() for f in files}})
dump_yaml("11-integrity.yaml", I)
print(f"v1.5: {sum(1 for x in G['@graph'] if x.get('@type')=='Record')} records, {len(C)} claims ({len(NEWC)} new), {len(G['edges'])} edges, {len(E)} events; "
      f"rebound {len(refreshed)} records and {moves_rebound} moves; unresolved introductions among new: {[c for c in NEWC if CL[c]['introduced']['date'] is None]}")
