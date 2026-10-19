#!/usr/bin/env python3
"""Apply one v0.9 composition (rebuild/negative-of-the-negative/v09/<row>.json) to its /non row, under EA-NEGONT-02 v0.9 (#1690).

    python3 rebuild/negative-of-the-negative/apply_v09.py <row> [--check-only]

Writes, in datasets/negative-of-the-negative/v2/rows/<row>.json: objects.KO (the expansion), objects.P (the compression, its
rail reordered by the plan), objects.L_BA (the KO as running text), row.ontology (the case, E_A, E_F, ρ, the translation table),
row.measure (§4.10, computed; §5.10, the opening-run check, recorded and never blocking), row.spec and row.status.procedure.
The v0.7 objects are kept under row.superseded["v0.7"]; T, the field arm (P_B, KO_B, L_B), the ledgers, the delta and the kernel
are not changed. Run twice, it rewrites the v0.9 objects from the composition and leaves superseded["v0.7"] as first kept.

Checks run first, and a failure stops the apply (these are integrity checks of the composition's own claims, not laws on the
entity): every cited id exists in a ledger; every field claim appears in exactly one translation row; the rail order names every
v0.7 lineage once; every quote in case.loci is present in the defining paper it cites."""
import json, re, sys, difflib, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
ROW = sys.argv[1]; CHECK = "--check-only" in sys.argv
SPEC = "EA-NEGONT-02 v0.9, #1690"
RP = ROOT / f"datasets/negative-of-the-negative/v2/rows/{ROW}.json"
PP = ROOT / "datasets/negative-of-the-negative/v2/panel/panel.json"
C = json.loads((ROOT / f"rebuild/negative-of-the-negative/v09/{ROW}.json").read_text(encoding="utf-8"))
row = json.loads(RP.read_text(encoding="utf-8")); o = row["objects"]
field = json.loads((ROOT / row["ledger"]["field"]).read_text(encoding="utf-8"))["field_claims"]
arch = {c["id"]: c for c in json.loads((ROOT / row["ledger"]["archive"]).read_text(encoding="utf-8"))}
reg = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
v07 = (row.get("superseded") or {}).get("v0.7") or {"KO": o["KO"], "P": o["P"], "L_BA": o["L_BA"], "type": row["type"], "spec": row["spec"],
        "note": "Composed under v0.7 (#1665): the archive admitted on equal terms into the field's entity, the field's composition first. Kept as the record of what v0.9 replaces."}
fail = []
def ids_of(xs): return [x for x in xs]
cited = set()
for s in C["KO"]["sentences"]: cited |= set(s["claims"])
cited |= set(C["P"]["lede"]["claims"])
for sec in C["P"]["sections"]:
    for it in sec["items"]: cited |= set(it["claims"])
for t in C["translation"]: cited |= set(t["field_claims"]) | set(t["archive_claims"])
for k in ("E_A", "E_F", "rho"): cited |= set(C[k].get("claims", []))
for q in C["P"].get("open", []): cited |= set(q.get("rests_on", []))
bad = sorted(x for x in cited if x not in field and x not in arch)
if bad: fail.append(f"ids not in either ledger: {bad}")
seen = {}
for t in C["translation"]:
    for f in t["field_claims"]: seen[f] = seen.get(f, 0) + 1
miss = [f for f in field if f not in seen]; dup = [f for f, n in seen.items() if n > 1]
if miss: fail.append(f"field claims not in the translation: {miss}")
if dup: fail.append(f"field claims in more than one translation row: {dup}")
import collections
old_names = [l["lineage"] for l in v07["P"]["rail"]]
ro = C["rail_order"]
if collections.Counter(ro) != collections.Counter(old_names):
    fail.append(f"rail order differs from the v0.7 lineages: missing {sorted(set(old_names) - set(ro))}, unknown {sorted(set(ro) - set(old_names))}")
ws = lambda s: re.sub(r"\s+", " ", s).strip()
for L in C["case"].get("loci", []):
    d = reg.get(L["dep"]); f = d and ROOT / f"data/texts/AXN-{d['hex']}-text.md"
    if not f or not f.exists(): fail.append(f"case locus #{L['dep']}: no text file"); continue
    q = ws(L["quote"]).strip('"“”'); t = ws(f.read_text(encoding="utf-8"))
    if q not in t and q.replace("’", "'") not in t.replace("’", "'"): fail.append(f"case locus #{L['dep']} quote not in text: {q[:80]}")
words = lambda s: len(re.findall(r"[A-Za-z0-9'’-]+", s))
pw = words(C["P"]["lede"]["text"]) + sum(words(it["label"]) + words(it["text"]) for sec in C["P"]["sections"] for it in sec["items"])
if pw > 350: fail.append(f"compression body {pw} words > 350")
print(f"{ROW}: case {C['case']['value']}, ρ = {C['rho']['value']}; KO {len(C['KO']['sentences'])} sentences; P body {pw} words; "
      f"field {len(field)} carried; archive cited {len([x for x in cited if x in arch])} of {len(arch)}")
_k = ["F" if all(c in field for c in x["claims"]) else ("A" if all(c in arch for c in x["claims"]) else "M") for x in C["KO"]["sentences"]]
print("  KO by claim type:", "".join(_k))
if fail:
    print("FAIL:\n  " + "\n  ".join(fail)); sys.exit(1)
if CHECK: sys.exit(0)

KO_B = [s["text"] for s in o["KO_B"]["sentences"]]
def survive(A):
    out = []
    for b in KO_B:
        r = max((difflib.SequenceMatcher(None, a, b).ratio(), i + 1) for i, a in enumerate(A))
        out.append(r[1] if r[0] >= 0.95 else None)
    return out
sents = [s["text"] for s in C["KO"]["sentences"]]
s9 = survive(sents); s7 = survive([s["text"] for s in v07["KO"]["sentences"]])
present = [p for p in s9 if p is not None]
# §4.1 by claim type, not similarity: the longest field-only run at the head and archive-only run at the tail (recorded, never blocking)
kind = ["F" if all(c in field for c in s["claims"]) else ("A" if all(c in arch for c in s["claims"]) else "M") for s in C["KO"]["sentences"]]
lead = next((i for i, k in enumerate(kind) if k != "F"), len(kind)); tail = next((i for i, k in enumerate(reversed(kind)) if k != "A"), len(kind))
blocks = {"rule": "v0.9 §4.1 (equal-terms and mixed cases): the KO does not open with the field as a block or close with the archive as one; sentences typed by the ledgers of the claims they cite (F field-only, A archive-only, M both)",
          "sequence": "".join(kind), "field_only_head": lead, "archive_only_tail": tail,
          "breach": bool(C["case"]["value"] != "witness" and (lead >= 3 or tail >= 3))}
opening = bool(present) and present == list(range(1, len(present) + 1))
measure = {"rule": "v0.9 §4.10: KO_B sentences surviving in the KO at similarity ≥ 0.95, with positions",
           "v0.9": {"surviving": len(present), "of": len(KO_B), "positions": s9},
           "v0.7": {"surviving": sum(p is not None for p in s7), "of": len(KO_B), "positions": s7},
           "opening_run": {"rule": "v0.9 §5.10 (equal-terms case): the field-only KO's sentences as the KO's opening run in their own order",
                           "breach": bool(opening and C["case"]["value"] != "witness")},
           "blocks": blocks}
if "superseded" not in row: row["superseded"] = {}
row["superseded"].setdefault("v0.7", v07)
o["KO"] = {"title": C["KO"]["title"],
           "genre": f"knowledge object, {C['case']['value']} case, under EA-NEGONT-02 v0.9 (#1690)" + (": composed in the archive's ontology, every field claim carried and translated" if C["case"]["value"] == "witness" else ": the archive's sources and the field's admitted on equal terms, ontology included, in one claim space"),
           "status": f"composed {C['composed']} under v0.9 on the operator's ruling ('lets craft those /non entries'); not frozen; ledger unaudited",
           "sentences": C["KO"]["sentences"], "field_claims": v07["KO"].get("field_claims"), "field_sources": v07["KO"].get("field_sources")}
P = {"title": C["P"]["title"],
     "genre": "the compression: AIO's interaction grammar (lede, headed clusters, bolded labels, card rail), composed from the v0.9 plan; it faces on the card, with AIO's transcript a record within it",
     "status": f"composed {C['composed']} from the v0.9 knowledge object; not frozen",
     "lede": C["P"]["lede"], "sections": C["P"]["sections"], "open": C["P"].get("open", []),
     "rail": (lambda q: [dict(q[n].pop(0)) for n in ro])({n: [l for l in v07["P"]["rail"] if l["lineage"] == n] for n in set(old_names)}),
     "entity": (f"Composed under v0.9, {C['case']['value']} case (ρ = {C['rho']['value']}): KO_B sentences surviving {measure['v0.9']['surviving']} of {len(KO_B)} "
                f"(v0.7: {measure['v0.7']['surviving']} of {len(KO_B)}); every field claim carried.")}
o["P"] = P
o["L_BA"] = {"words": sum(words(t) for t in sents), "text": " ".join(sents), "rail": [],
             "note": "L(B ∪ A) in the equal-terms case, L_A(B ∪ A) in the witness case (v0.9 §0.4), realized as the knowledge object (objects.KO); its rail is the compression's, by lineage."}
row["spec"] = SPEC
row["status"]["procedure"] = (f"{SPEC}: {C['case']['value']} case, ρ = {C['rho']['value']}, read from the defining papers ({', '.join('#%d' % n for n in C['E_A']['defining_papers'])}); "
                              "composed from the entity's ledgers as selected under v0.7 (D/R/O); the composer read the ledgers, never the transcript")
row["ontology"] = {"composition": C["case"]["value"], "case": C["case"], "E_F": C["E_F"], "E_A": C["E_A"], "rho": C["rho"],
                   "translation": C["translation"],
                   "receiving_texts": ("receiving texts located where the archive seats them" if C["case"]["value"] == "witness"
                                       else "equal-terms case: every field claim composed as received, beside the archive claims it stands with")}
row["measure"] = measure
row["composition_v09"] = {"source": f"rebuild/negative-of-the-negative/v09/{ROW}.json", "composer": C.get("composer"),
                          "defining_papers_read": C.get("defining_papers_read"), "cuts": C.get("cuts", []), "notes": C.get("notes", "")}
RP.write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
raw = PP.read_text(encoding="utf-8"); nl = raw.endswith("\n"); panel = json.loads(raw)
en = next((e for e in panel["entities"] if e["entity"] == row.get("entity", ROW)), None)
if en is not None:
    en["ontology"] = {"composition": C["case"]["value"], "E_A": C["E_A"]["definition"][:160], "E_F": C["E_F"]["type"], "rho": C["rho"]["value"]}
    en["stage"] = f"recomposed {C['composed']} under {SPEC}, {C['case']['value']} case (draft, not frozen; ledgers unaudited)"
    PP.write_text(json.dumps(panel, ensure_ascii=False, indent=1) + ("\n" if nl else ""), encoding="utf-8")
print("applied:", ROW, "measure", measure["v0.9"], "v0.7", measure["v0.7"]["surviving"], "opening-run breach", measure["opening_run"]["breach"])
