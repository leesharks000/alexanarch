"""Verify every quote in the staged ledgers against its saved text, the registry or the deposit text, and the row's coverage.
Sets quote_ok on each claim and writes the counts to verification.json.   python3.12 verify.py"""
import json, yaml, collections
from vlib import *

st = STAGE
R = json.loads((st / "row.json").read_text()); F = json.loads((st / "field.json").read_text()); A = json.loads((st / "ledger-archive.json").read_text())
INT = ROOT / "datasets/negative-of-the-negative/v2/intake/classical-receptions-journal-20261110"
srcfiles = {s["id"]: s.get("files") or {} for s in F["field"]}
paste = (INT / "paste-classical-receptions-journal-aio-five-turns.txt").read_text()


def walk(o):
    if isinstance(o, dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
    elif isinstance(o, str): yield o


def field_hay(c):
    sid = c["source"]
    if c.get("title_only") or c["checked_against"].startswith("the paste"):
        return paste
    if c["checked_against"].startswith("the registry's cite_list"):
        return entry_text("classical-receptions-journal-ai-mediation-aio-20261110-20261114")
    hay = []
    for f, meta in srcfiles[sid].items():
        p = ROOT / meta["path"]
        if p.suffix in (".txt", ".wiki", ".json") and p.exists():
            t = p.read_text(encoding="utf-8")
            if p.suffix == ".json":
                t = "\n".join(walk(json.loads(t))) + "\n" + t
            hay.append(t)
    return "\n".join(hay)


res = collections.Counter(); fails = []
for k, c in F["field_claims"].items():
    ok = found(c["quote"], field_hay(c)); c["quote_ok"] = ok
    res[("field", c["pool"], ok)] += 1
    if not ok: fails.append(("field", k, c["quote"][:100]))
for c in A:
    if c["dep"] == "capture-registry":
        hay = entry_text(c["locus"].split(",")[0])
    elif "kernel" in c["file"]:
        hay = "\n".join(s for f in c["file"].split(" + ") for s in walk(yaml.safe_load((ROOT / f).read_text())))
    else:
        hay = deposit_text(c["file"])
    ok = found(c["quote"], hay); c["quote_ok"] = ok
    res[("archive", str(c["dep"]), ok)] += 1
    if not ok: fails.append(("archive", c["id"], c["quote"][:100]))
R["field_claims"] = F["field_claims"]
# coverage
ids = set(F["field_claims"]) | {c["id"] for c in A}
ko = R["objects"]["KO"]["sentences"]; P = R["objects"]["P"]
ko_c = {c for s in ko for c in s["claims"]}
p_c = {c for c in P["lede"]["claims"]} | {c for s in P["sections"] for i in s["items"] for c in i["claims"]} | {c for x in P["rail"] for c in x["claims"]} | {c for q in P["open"] for c in q["rests_on"]}
unknown = sorted((ko_c | p_c) - ids)
uncovered = sorted(ids - ko_c - p_c)
field_not_in_ko = sorted(set(F["field_claims"]) - ko_c)
plan_ok = R["objects"]["KO"]["plan"]["order"] == [c for s in ko for c in s["claims"]]
corr = [(m["move"], m["ko"]) for m in R["delta"]["correction"]["moves"]]
corr_ok = all(1 <= n <= len(ko) for _, v in corr for n in v)
out = {"field": {f"{pool} {'ok' if ok else 'FAIL'}": n for (kind, pool, ok), n in res.items() if kind == "field"},
       "archive": {f"{dep} {'ok' if ok else 'FAIL'}": n for (kind, dep, ok), n in res.items() if kind == "archive"},
       "field_total": f"{sum(1 for c in F['field_claims'].values() if c['quote_ok'])}/{len(F['field_claims'])}",
       "archive_total": f"{sum(1 for c in A if c['quote_ok'])}/{len(A)}",
       "fails": fails, "unknown_claim_ids": unknown, "claims_in_neither_KO_nor_P": uncovered, "field_claims_not_in_KO": field_not_in_ko,
       "plan_matches_text": plan_ok, "correction_ko_in_range": corr_ok, "ko_sentences": len(ko), "p_body_words": P["body_words"]}
R["status"]["ledger"] = (f"unaudited (§3.8: one extractor per ledger); revised 2026-11-14: field quotes {out['field_total']} verified by script against saved text, the paste or the registry's cards; "
                         f"archive quotes {out['archive_total']} verified against the registry, the deposit texts and #1769's kernel (stage scripts/verify.py)")
F["rule"] = (F["rule"].split("; 57/57")[0] + f"; {out['field_total']} verified by script (revised 2026-11-14; the cards of v12.681 checked against the registry's cite_list)")
(st / "row.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
(st / "field.json").write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")
(st / "ledger-archive.json").write_text(json.dumps(A, ensure_ascii=False, indent=1), encoding="utf-8")
(st / "verification.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
