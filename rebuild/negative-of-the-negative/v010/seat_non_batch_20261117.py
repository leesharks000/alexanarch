#!/usr/bin/env python3
"""Seat the /non batch of 2026-11-17 at the operator's words: "and we need /non articles for ancient philosophy, classical philology,
etc - its been awhile since a batch and weve covered significant ground. lets assess what loci are needed." and "adopted... we'll stick
to just those four for now, need to get back to 3i atlas".

Three new rows (classical-philology, ancient-philosophy, longinus-on-the-sublime), composed under BRIEF-NEW-ROW-*.md, are already in
their folders; this script moves each row's configuration to panel/configs/<row>.json (the row's ledger.config re-pointed before its
AXN is minted) and appends its panel entry, built from the row. The revision of sappho-31, composed under BRIEF-REVISE-ROW-SAPPHO-31.md
and staged at revise-sappho31-20261117/, is seated as seat_crj_revision_20261114.py seated the CRJ revision: every replaced file kept
under v2/history/sappho-31/<date>-<sha12>/, the staged files copied, the second reading merged into reading.json, the panel entry's
stage and homonym fields updated. scripts/non_axn.py mints the three and versions sappho-31; the dataset is released and pages rebuilt.
    python3 rebuild/negative-of-the-negative/v010/seat_non_batch_20261117.py [--no-build]"""
import json, hashlib, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; V2R = "datasets/negative-of-the-negative/v2"; V2 = ROOT / V2R; DATE = "2026-11-17"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
rj = lambda p: json.loads(p.read_text(encoding="utf-8"))
SRC = ("operator, 2026-11-17: 'and we need /non articles for ancient philosophy, classical philology, etc - its been awhile since a batch and "
       "weve covered significant ground. lets assess what loci are needed.'; 'adopted... we'll stick to just those four for now, need to get back to 3i atlas'")
NEW = {"classical-philology": ("Classical Philology (journal)", "BRIEF-NEW-ROW-CLASSICAL-PHILOLOGY.md"),
       "ancient-philosophy": ("Ancient Philosophy (journal)", "BRIEF-NEW-ROW-ANCIENT-PHILOSOPHY.md"),
       "longinus-on-the-sublime": ("[Longinus], On the Sublime (Περὶ ὕψους, De sublimitate)", "BRIEF-NEW-ROW-LONGINUS.md")}
EXTRA = {"longinus-on-the-sublime": ("; four points of the capture record that the field ledger shows wrong are reported, not fixed (the "
         "'Universal Resonance' credit to Wikipedia; 'over 50' for 'about 50'; the YouTube card's title; fr. 31 at 10.2–3, not 10.1–3; "
         "The Nature of Writing attached to the YouTube card)")}
pp = V2 / "panel/panel.json"; praw = pp.read_text(encoding="utf-8"); P = json.loads(praw); have = {e["entity"] for e in P["entities"]}

# 1. the three new rows
for k, (name, brief) in NEW.items():
    rp = V2 / "rows" / f"{k}.json"; R = rj(rp)
    cfg_old = ROOT / R["ledger"]["config"]; cfg_new = V2 / "panel/configs" / f"{k}.json"
    if cfg_old != cfg_new:
        shutil.move(cfg_old, cfg_new); R["ledger"]["config"] = f"{V2R}/panel/configs/{k}.json"
        rp.write_text(json.dumps(R, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if k in have:
        continue
    O = R["ontology"]; ef = O["E_F"]
    P["entities"].append({
        "entity": k, "name": name, "type": R["type"], "source": SRC,
        "stage": (f"composed {DATE} under EA-NEGONT-02 v0.10, #1726, by one composer under rebuild/negative-of-the-negative/v010/{brief}; "
                  + R["status"]["procedure"] + EXTRA.get(k, "") + ". Draft, not frozen; " + R["status"]["ledger"] + "; checked by the session"),
        "addresses": [{"address": a["address"], "note": "; ".join(x for x in (
            f"T: {R['surface']}, signed out, incognito, {DATE} ({a.get('axn', '').split('.')[0]}, {a.get('slug')})", a.get("address_note")) if x)}
            for a in R["addresses"]],
        "homonym_names": R["homonyms"]["names"], "homonym_basis": R["homonyms"]["basis"],
        "ontology": {"composition": O["composition"], "E_F": ef.get("definition", ef.get("type")) if isinstance(ef, dict) else ef,
                     "rho": O["rho"]["value"] if isinstance(O["rho"], dict) else O["rho"]}})

# 2. the sappho-31 revision
K = "sappho-31"; ST = pathlib.Path(__file__).parent / "revise-sappho31-20261117"
cur = V2 / "rows" / f"{K}.json"; old = sha(cur); new_row = rj(ST / "row.json")
if old != sha(ST / "row.json"):
    assert new_row["composition"]["revision_20261117"]["prior_row_sha256"] == old, "the live row is not the row the revision was composed on"
    PAIRS = [(ST / "row.json", f"{V2R}/rows/{K}.json"), (ST / "field.json", f"{V2R}/ledgers/{K}/field.json"),
             (ST / "ledger-archive.json", f"{V2R}/ledgers/{K}/ledger-archive.json"), (ST / "config-sappho-31.json", f"{V2R}/panel/configs/{K}.json")]
    PAIRS += [(ST / "traversal" / n, f"{V2R}/traversal/{K}/{n}") for n in ("candidates-D.jsonl", "candidates-R.jsonl", "candidates-O.jsonl", "summary.json")]
    H = V2 / "history" / K / f"{DATE}-{old[:12]}"; assert not H.exists(), f"{H} exists: already seated"
    for _, dst in PAIRS + [(None, f"{V2R}/traversal/{K}/reading.json")]:
        p = ROOT / dst
        if p.exists():
            q = H / dst[len(V2R) + 1:]; q.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, q)
    for src, dst in PAIRS:
        (ROOT / dst).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, ROOT / dst)
    RD = V2 / "traversal" / K / "reading.json"; R = rj(RD); R2 = rj(ST / "traversal/reading-20261117.json")
    by = {v["dep"]: v for v in R["verdicts"]}
    for a in R2["admitted"]:
        if a["dep"] in by:
            v = by[a["dep"]]; v["claims"] = sorted(set(v.get("claims") or []) | set(a.get("claims") or []))
            v["reason"] = v["reason"] + f"; {DATE}: {a['reason']}"
        else:
            R["verdicts"].append({"dep": a["dep"], "strata": a.get("strata", []), "reason": f"{DATE}: {a['reason']}", "claims": a.get("claims", []), "cands": []})
    R["second_reading_20261117"] = R2
    R["pass"] = R["pass"] + f"; {R2['pass']}: D/R/O rerun with the row's config unchanged, {len(R2['admitted'])} deposits admitted by reading, 16 captures admitted"
    R["reader"] = R["reader"] + "; " + R2["reader"]
    R["counts"]["admitted"] = len(R["verdicts"])
    RD.write_text(json.dumps(R, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    e = next(x for x in P["entities"] if x["entity"] == K)
    e["stage"] = e["stage"] + (f"; revised in place {DATE} under EA-NEGONT-02 v0.10, #1726 (BRIEF-REVISE-ROW-SAPPHO-31.md; #1781, #1752, #1756, #1774, "
                               "#1783 and sixteen captures admitted; draft, not frozen; ledgers unaudited)")
    e.setdefault("homonym_names", []); e.setdefault("homonym_basis", new_row["homonyms"]["basis"])
    print("kept at", H.relative_to(ROOT), "| row", old[:12], "->", sha(cur)[:12], "| verdicts", len(R["verdicts"]))

P["changes"].append({"date": DATE, "change": "three entries added and composed (classical-philology, ancient-philosophy, longinus-on-the-sublime); sappho-31 revised in place", "reason": SRC})
pp.write_text(json.dumps(P, ensure_ascii=False, indent=1 if praw.startswith("{\n \"") else 2) + "\n", encoding="utf-8")

run = lambda *a: subprocess.run([sys.executable, *a], cwd=ROOT, check=True)
run("scripts/non_axn.py", "--date", DATE, "--reason", "revised in place " + DATE + " under BRIEF-REVISE-ROW-SAPPHO-31.md: #1781, #1752, #1756, #1774, #1783 and sixteen captures admitted; cross-linked with /non/classical-philology/ and the combined audit")
run("scripts/release_axn.py", "--apply", "--only", "negative-of-the-negative")
if "--no-build" not in sys.argv:
    for s in ("scripts/build_non.py", "scripts/build_central_registry.py", "scripts/generate_axn_resolver.py", "scripts/sync_sigil.py"): run(s)
