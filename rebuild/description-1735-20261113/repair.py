"""Metadata correction of 2026-11-13: #1735's description opened with three sentences copied verbatim from the paper's abstract, so the
record page printed them twice (check_rendered_record RENDERED-004). At the author's word ("lets fix the doubled description") the three
sentences are restated as description; the rest, which is the record's own, is kept. Erratum entered.
    python3 rebuild/description-1735-20261113/repair.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
OLD = ("New Testament chronology dates its documents; this article tests one of them as an ancestor. It proposes a literary-genealogical test for "
       "the priority question: a literature proposed as earliest should exhibit recoverable ancestry, its load-bearing forms derivable from "
       "independently attested antecedents, while the forms that follow it may show transformations of it. On that test the received sequence is "
       "anomalous: it begins with the literature whose immediate Christian ancestry must be reconstructed, as the field's own category 'pre-Pauline' "
       "concedes, and ends with the literature whose ancestry can be read.")
NEW = ("Johannes Sigil and Damascus Dancings test one document of the New Testament's chronology as the ancestor of the rest. Their test for the "
       "priority question is literary-genealogical: the literature put forward as earliest should show recoverable ancestry, its load-bearing forms "
       "derivable from antecedents attested independently, and what comes after it may show transformations of it. By that test the received "
       "sequence is anomalous. It starts with the literature whose Christian ancestry has to be reconstructed, as the field's own category "
       "'pre-Pauline' concedes, and ends with the literature whose ancestry can be read.")
reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
d = next(x for x in reg["deposits"] if x["deposit_number"] == 1735)
assert d["description"].startswith(OLD), d["description"][:120]
was = d["description"]; d["description"] = NEW + was[len(OLD):]
d.setdefault("errata", []).append({"date": "2026-11-13", "kind": "metadata correction", "locus": "registry field description",
    "was": OLD, "now": NEW,
    "reason": "The description's first three sentences repeated the abstract word for word, so the record page printed them twice. They are restated as description; the rest of the description is unchanged, and the deposited text is untouched.",
    "raised_by": "Lee Sharks (2026-11-13)", "status": "corrected in the metadata"})
(ROOT / "data/registry.json").write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
rp = ROOT / "data/records/1735.json"; r = json.loads(rp.read_text(encoding="utf-8")); r["description"] = d["description"]
rp.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok")
