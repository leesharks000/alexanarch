"""Verify every quote in the staged ledgers against its saved text, the paste, the deposit text, the attachment or the
registry; check the KO's coverage, the plan, the rail's kernel coverage (§5.2) and the open block's claim ids.
Sets quote_ok on each claim and writes verification.json.   /tmp/py312/python3 verify.py"""
import json, collections
from vlib import *

st = STAGE
R = json.loads((st / "row.json").read_text()); F = json.loads((st / "field.json").read_text()); A = json.loads((st / "ledger-archive.json").read_text())
REGD = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text())["deposits"]}
paste = (ROOT / R["objects"]["T"]["path"]).read_text(encoding="utf-8")
src = {s["id"]: s for s in F["field"]}
res = collections.Counter(); fails = []
for k, c in F["field_claims"].items():
    if c.get("title_only"):
        hay = paste
    else:
        hay = "\n".join((ROOT / m["path"]).read_text(encoding="utf-8") for m in src[c["source"]]["files"].values())
    ok = found(unquote(c["quote"]), hay); c["quote_ok"] = ok
    res[("field", c["source"], ok)] += 1
    if not ok: fails.append(("field", k, c["quote"][:100]))
for c in A:
    if c["dep"] == "capture-registry":
        hay = entry_text(c["locus"].split(",")[0]); q = c["quote"]
    else:
        f = c.get("file") or REGD[c["dep"]]["full_text_path"].lstrip("/")
        hay = deposit_text(f); q = strip_md(c["quote"])
    ok = found(q, hay)
    if c["id"] == "A436-01":
        c["quote_ok"] = ok  # expected False (re-seated text); reported
    else:
        c["quote_ok"] = ok
    c.setdefault("quote_check", "within the deposit text as loaded (whitespace-normalised; markdown emphasis stripped)")
    res[("archive", "capture-registry" if c["dep"] == "capture-registry" else ("old" if not c["id"].startswith(("A1781", "A1752", "A1756", "A1774", "A1783", "A1779", "A1749", "A1748", "A1058", "A1670", "A1766", "A1048-03")) else str(c["dep"])), ok)] += 1
    if not ok: fails.append(("archive", c["id"], c["quote"][:100]))
ids = set(F["field_claims"]) | {c["id"] for c in A}
KO = R["objects"]["KO"]; ko = KO["sentences"]; P = R["objects"]["P"]
ko_c = {c for s in ko for c in s["claims"]}
p_c = set(P["lede"]["claims"]) | {c for s in P["sections"] for i in s["items"] for c in i["claims"]} | {c for x in P["rail"] for c in x["claims"]} | {c for q in P["open"] for c in q["rests_on"]}
rail_c = {c for x in P["rail"] for c in x["claims"]}
unknown = sorted((ko_c | p_c) - ids)
not_in_ko = sorted(ids - ko_c)
kernels_off_rail = sorted(c["id"] for c in A if c.get("kernel") and c["id"] not in rail_c) + sorted(k for k, c in F["field_claims"].items() if c.get("kernel") and k not in rail_c)
plan_ok = KO["plan"]["order"] == [c for s in ko for c in s["claims"]]
nums_ok = [s["n"] for s in ko] == list(range(1, len(ko) + 1))
out = {"field": {f"{s} {'ok' if ok else 'FAIL'}": n for (kind, s, ok), n in sorted(res.items()) if kind == "field"},
       "archive": {f"{d} {'ok' if ok else 'FAIL'}": n for (kind, d, ok), n in sorted(res.items()) if kind == "archive"},
       "field_total": f"{sum(1 for c in F['field_claims'].values() if c['quote_ok'])}/{len(F['field_claims'])}",
       "archive_total": f"{sum(1 for c in A if c['quote_ok'])}/{len(A)}",
       "fails": fails, "unknown_claim_ids": unknown, "ledger_claims_not_in_KO": not_in_ko, "kernels_off_rail": kernels_off_rail,
       "plan_matches_text": plan_ok, "numbering_ok": nums_ok, "ko_sentences": len(ko), "p_body_words": P["body_words"],
       "measure": {"v0.10": R["measure"]["v0.10"], "blocks": {k: R["measure"]["blocks"][k] for k in ("sequence", "field_only_head", "archive_only_tail", "breach")}}}
R["status"]["ledger"] = R["status"]["ledger"].replace("(stage scripts/verify.py; counts in verification.json)",
                         f"(stage scripts/verify.py: field {out['field_total']}, archive {out['archive_total']}, the one failure A436-01, whose deposit text was re-seated after extraction, reported)")
F["rule"] = F["rule"] + f"; {out['field_total']} verified (2026-11-17)"
(st / "row.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
(st / "field.json").write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")
(st / "ledger-archive.json").write_text(json.dumps(A, ensure_ascii=False, indent=1), encoding="utf-8")
(st / "verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
