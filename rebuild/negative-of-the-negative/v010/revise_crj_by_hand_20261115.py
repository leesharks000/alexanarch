#!/usr/bin/env python3
"""Revise by hand the /non row classical-receptions-journal (2026-11-15), at the operator's words: 14:38 "i would revise it to speak of a previous article by the
author"; "i dont necessarily dispute the decision"; "i dispute the field"; 14:43 "on this one we can simply revise by hand. that is the normal rule for how /non is
supposed to work but its not meant to exclude the capacity for editorial discernment".

The row's knowledge object refers to the author's previous article in the journal unnamed (sentence 15, the 'Its pages' item, the note on the article, the lineage
'the archive's author in its pages'); its ledger quotes #1769 and the capture finding as they now read; one sentence and one claim (D1770-01, #1770 §0.1) state that
the archive contests the field and not the decision. The field's own claim of the register (F57, Crossref) and the field object's sentence on it are unchanged.
As seat_crj_revision_20261114.py does: every replaced file is kept under v2/history/<row>/<date>-<sha12>/; scripts/non_axn.py versions AXN:0C66; the /non
dataset is released and the pages rebuilt.
    python3 rebuild/negative-of-the-negative/v010/revise_crj_by_hand_20261115.py"""
import json, hashlib, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; V2R = "datasets/negative-of-the-negative/v2"; V2 = ROOT / V2R; K = "classical-receptions-journal"; DATE = "2026-11-15"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
RP = V2 / "rows" / f"{K}.json"; LP = V2 / "ledgers" / K / "ledger-archive.json"; old = sha(RP)
REASON = ("revised by hand in place 2026-11-15 (operator, 14:43: 'on this one we can simply revise by hand'): the author's previous article in the journal referred to "
          "unnamed (operator, 14:38); the archive contests the field and not the decision (operator, 14:38), carried from #1770 §0.1")
H = V2 / "history" / K / f"{DATE}-{old[:12]}"; assert not H.exists(), H
for p in (RP, LP):
    q = H / p.relative_to(V2); q.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, q)
r = json.loads(RP.read_text(encoding="utf-8")); L = json.loads(LP.read_text(encoding="utf-8"))
T1770 = (ROOT / "data/texts/AXN-0C9C-text.md").read_text(encoding="utf-8"); T1769 = (ROOT / "data/texts/AXN-0C9A-text.md").read_text(encoding="utf-8")
Q1770 = "The article does not contest the decision on the manuscript; it contests the field the decision administers."
assert Q1770 in T1770
REG = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
# 1. the knowledge object
KO = r["objects"]["KO"]["sentences"]
s15 = next(s for s in KO if s["n"] == 15); assert "Metatexts" in s15["text"]
s15["text"] = "Among the register's works is a previous article by the archive's author."; s15["claims"] = ["D1769-36"]
s61 = next(s for s in KO if s["n"] == 61)
s61["text"] = s61["text"].rstrip() + " The archive does not contest the decision; it contests the field the decision administers."; s61["claims"] = s61["claims"] + ["D1770-01"]
it = r["objects"]["P"]["sections"][1]["items"][2]; assert it["label"] == "The archive's author:"
it["text"] = "a previous article in the journal; no recorded citation."; it["claims"] = ["D1769-36", "D1769-37", "D1750-06"]
n6 = next(i for i, n in enumerate(r["notes"]) if n.startswith("The archive's author's earlier article in the journal"))
r["notes"][n6] = ("The archive's author's previous article in the journal is referred to unnamed, as #1769 and #1770 refer to it (operator, 2026-11-15, 14:38: 'i would revise "
                  "it to speak of a previous article by the author'). The field's own record of the register (F57) is unchanged.")
tr = next(t for t in r["ontology"]["translation"] if t.get("lineage") == "the archive's author in its pages")
tr["field_claims"] = ["F30"]; tr["received"] = tr["received"][:tr["received"].index("; F57")]
tr["archive_claims"] = ["D1769-36", "D1750-06"]; tr["translation"] = "untranslated: composed as received beside D1769-36, D1750-06"
for k in ("composition", "composition_v09"):
    if k in r and "source" in r[k]: r[k]["source"] = r[k]["source"].replace("the Metatexts article", "the author's previous article in the journal")
r["composition"]["revision_20261115"] = {"by": "hand", "operator": "2026-11-15, 14:38 and 14:43", "prior_row_sha256": old, "reason": REASON}
# 2. the archive ledger
def claim(i): return next(c for c in L if c["id"] == i)
c = claim("D1769-36"); c["claim"] = "the author's previous article: no Crossref citation; none of the 16,818 references points to it"
c["quote"] = "Crossref records no citation of it, and none of the journal's 16,818 references points to it."
c = claim("D1769-37"); c["claim"] = "the author's previous article: 0 citations in Crossref and Semantic Scholar"; c["quote"] = "Its count is 0 in both indexes."
for i in ("D1769-36", "D1769-37"):
    c = claim(i); assert c["quote"] in T1769, i
c = claim("CAP-3-06"); c["claim"] = "THE AUTHOR'S PREVIOUS ARTICLE IN THE JOURNAL DROPPED"
c["quote"] = ("THE AUTHOR'S PREVIOUS ARTICLE IN THE JOURNAL DROPPED. The entry records the author's previous article in the journal and the two years its review took. "
              "The composition has none of it, and builds its provenance-inversion sequence on 'An independent researcher develops a theoretical framework.'")
if not any(x["id"] == "D1770-01" for x in L):
    d = REG[1770]
    L.append({"id": "D1770-01", "dep": 1770, "axn": d["axn"], "claim": "the archive contests the field the decision administers, not the decision", "kind": "interpretation",
              "modality": "interpretation", "strata": ["D"], "locus": "§0.1", "quote": Q1770, "kernel": False, "const": False, "lineage": "the archive's question",
              "date": DATE, "title": d["title"], "creator": "Sharks, Lee", "file": "data/texts/AXN-0C9C-text.md", "quote_ok": True,
              "quote_check": "within the deposit text as loaded (whitespace-normalised; markdown emphasis stripped)"})
for x in ("Metatexts", "clu016", "byline withheld"):
    for nm, o in (("row KO/P/notes", [r["objects"]["KO"], r["objects"]["P"], r["notes"]]), ("ledger", [c for c in L if c["id"].startswith(("D1769", "CAP-3", "D1770"))])):
        assert x not in json.dumps(o, ensure_ascii=False), (nm, x)
indent = 1 if RP.read_text(encoding="utf-8").startswith("{\n \"") else 2
RP.write_text(json.dumps(r, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
LP.write_text(json.dumps(L, ensure_ascii=False, indent=1 if LP.read_text(encoding="utf-8").startswith("[\n {") else 2) + "\n", encoding="utf-8")
print("kept at", H.relative_to(ROOT), "| row", old[:12], "->", sha(RP)[:12])
run = lambda *a: subprocess.run([sys.executable, *a], cwd=ROOT, check=True)
run("scripts/non_axn.py", "--date", DATE, "--reason", REASON)
run("scripts/release_axn.py", "--apply", "--only", "negative-of-the-negative")
for s in ("scripts/build_non.py", "scripts/build_central_registry.py", "scripts/generate_axn_resolver.py", "scripts/sync_sigil.py"): run(s)
