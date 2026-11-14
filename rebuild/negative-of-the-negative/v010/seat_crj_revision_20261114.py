#!/usr/bin/env python3
"""Seat the revision in place of the /non row classical-receptions-journal (2026-11-14), at the operator's words: 16:38 EST "at this point
qe need to revise the crj /non article so that these can cross link each other"; 17:29 "lets do so"; 17:58 "sure. lets proceed" (on the two
edits the session proposed to the composer's knowledge object). Composed under BRIEF-REVISE-ROW-CRJ.md; staged at revise-crj-20261114/.

As scripts/land_non_row.py does for a landing: every file the revision replaces is first kept, as it stood, under
v2/history/<row>/<date>-<sha12 of the replaced row>/, so the entity page lists the earlier row; then the row, its ledgers, its traversal
candidates and its configuration are copied; reading.json gains the verdicts for #1769 and #1766; the panel entry's first address becomes
the first-round input; scripts/non_axn.py versions AXN:0C66 with this revision as its reason; the /non dataset is released and the pages rebuilt.
    python3 rebuild/negative-of-the-negative/v010/seat_crj_revision_20261114.py [--no-build]"""
import json, hashlib, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; V2R = "datasets/negative-of-the-negative/v2"; V2 = ROOT / V2R
ST = pathlib.Path(__file__).parent / "revise-crj-20261114"; K = "classical-receptions-journal"; DATE = "2026-11-14"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
cur = V2 / "rows" / f"{K}.json"; old = sha(cur)
new_row = json.loads((ST / "row.json").read_text(encoding="utf-8"))
assert new_row["composition"]["revision_20261114"]["prior_row_sha256"] == old, "the live row is not the row the revision was composed on"
REASON = ("revised in place 2026-11-14 under rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-CRJ.md, to cite the Daffodils hologram (#1769) "
          "and be cited by it (operator, 16:38 and 17:29 EST; the two edits ruled 17:58): the first-round address; the editor named as the accountable "
          "party; #1769 and #1766 admitted by reading; the fourteen cards of 14 November and five new field sources; the received definition and the "
          "archive's question; the record at the journal's, the field's and the editor's addresses on 14 November")
PAIRS = [(ST / "row.json", f"{V2R}/rows/{K}.json"), (ST / "field.json", f"{V2R}/ledgers/{K}/field.json"),
         (ST / "ledger-archive.json", f"{V2R}/ledgers/{K}/ledger-archive.json"),
         (ST / "config-classical-receptions-journal.json", f"{V2R}/panel/configs/{K}.json")]
PAIRS += [(ST / "traversal" / n, f"{V2R}/traversal/{K}/{n}") for n in ("candidates-D.jsonl", "candidates-R.jsonl", "candidates-O.jsonl", "candidates-H.jsonl", "summary.json")]
RD = V2 / "traversal" / K / "reading.json"
# 1. keep what is replaced
H = V2 / "history" / K / f"{DATE}-{old[:12]}"
assert not H.exists(), f"{H} exists: already seated"
for _, dst in PAIRS + [(None, f"{V2R}/traversal/{K}/reading.json")]:
    p = ROOT / dst
    if p.exists():
        q = H / dst[len(V2R) + 1:]; q.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, q)
# 2. the revision's files
for src, dst in PAIRS:
    (ROOT / dst).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, ROOT / dst)
# 3. reading.json: #1769 and #1766 admitted by reading, with their claims as the archive ledger holds them
R = json.loads(RD.read_text(encoding="utf-8")); LA = json.loads((ST / "ledger-archive.json").read_text(encoding="utf-8"))
ids = lambda pre: [c["id"] for c in LA if c["id"].startswith(pre)]
R["verdicts"].append({"dep": 1769, "strata": ["D", "R", "O"], "reason": ("Daffodils (#1769, v1.1), the archive's audit of the journal, read whole: the census and "
    "coding (§2.4, §2.6), the decision and the control (§6.2, §6.4.3.2), the captures of 14 November (§6.5, §6.5.1), the editor's article against the criteria "
    "K1–K5 (§7.11.6), the received definition and what is contested (§1.6); the kernel's rival and ontology parsed for K1 and K2"), "claims": ids("D1769"), "cands": []})
R["verdicts"].append({"dep": 1766, "strata": ["D"], "reason": "Critique of Pure Inference (#1766) §6.1.3, the one new candidate of the 14 November rerun: reads the decision as a paralogism of review",
    "claims": ids("D1766"), "cands": []})
R["pass"] = R["pass"] + "; 2026-11-14: D/R/O rerun with the revised address, #1769 and #1766 admitted by reading; hop candidates #4, #32, #165, #189, #280 and #1767 not admitted (they say nothing of the journal)"
R["reader"] = R["reader"] + "; Claude (Opus 5.5), subagent, 2026-11-14"
c = R["counts"]; c["deposits_admitted"] = len(R["verdicts"])
c["deposit_claims"] = sum(1 for x in LA if not x["id"].startswith("CAP-")); c["CAP_claims"] = sum(1 for x in LA if x["id"].startswith("CAP-"))
summ = json.loads((ST / "traversal/summary.json").read_text(encoding="utf-8")).get("counts") or {}
for k2 in ("D_candidates", "D_deposits", "R_candidates", "O_candidates", "O_deposits", "H_candidates"):
    if k2 in summ: c[k2] = summ[k2]
if isinstance(R.get("records"), dict): R["records"]["CAP"] = c["CAP_claims"]
RD.write_text(json.dumps(R, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
# 4. the panel entry: the first-round address; the prior string kept in its note
pp = V2 / "panel/panel.json"; praw = pp.read_text(encoding="utf-8"); P = json.loads(praw)
e = next(x for x in P["entities"] if x["entity"] == K)
a0 = e["addresses"][0]; prior = a0["address"]
if prior != new_row["address"]:
    a0["address"] = new_row["address"]
    a0["note"] = a0["note"] + f"; the address is the first-round input (operator, 2026-11-14: 'a second round input is not an address'); prior string '{prior}'"
e["stage"] = e["stage"] + "; " + REASON
pp.write_text(json.dumps(P, ensure_ascii=False, indent=1 if praw.startswith("{\n \"") else 2) + "\n", encoding="utf-8")
print("kept at", H.relative_to(ROOT), "| row", old[:12], "->", sha(cur)[:12], "| verdicts", len(R["verdicts"]))
# 5. the AXN version, the release, the pages
run = lambda *a: subprocess.run([sys.executable, *a], cwd=ROOT, check=True)
run("scripts/non_axn.py", "--date", DATE, "--reason", REASON)
run("scripts/release_axn.py", "--apply", "--only", "negative-of-the-negative")
if "--no-build" not in sys.argv:
    for s in ("scripts/build_non.py", "scripts/build_central_registry.py", "scripts/generate_axn_resolver.py", "scripts/sync_sigil.py"): run(s)
