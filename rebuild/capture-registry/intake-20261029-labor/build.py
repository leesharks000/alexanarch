"""Build the fifteen capture records of 2026-10-29 (the Labor Vector meta-aggregator's entities, by their common names, on Google's
AI Overview) from the operator's paste, recovered verbatim (segments.json, from parse.py), with the authored readings in
authored.py and the dimensional PER read at intake (per/out-L1..L3.json, per/BRIEF.md; dimensional PER is standard at intake,
operator 2026-10-29). The readers' record quotes and spans are verified, and the scores computed, by scripts/per_backlog.py's
functions; their new atom sets are merged into data/per-atom-sets.json as TGT-lv-<slug>.
  python3 build.py [--check]"""
import json, pathlib, re, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(H)); sys.path.insert(0, str(ROOT / "scripts"))
from authored import A
import per_backlog as PB
PB.BD = H / "per"; PB.GROUPS = ["L1", "L2", "L3"]
C = json.load(open(H / "census-20261029-labor.json"))  # the Labor Vector census as landed on laborvector.org, 2026-10-29 (bf90841)
CENSUS = {r["slug"]: r for r in C["rows"]}
S = json.load(open(H / "segments.json"))["segments"]
TYPE = {"rating programme": "dataset", "searchable inventory": "dataset", "database": "dataset", "report series": "dataset", "benchmark": "dataset",
        "index of occupational exposure": "dataset", "global policy tracker": "dataset", "working paper and dashboard": "dataset", "interactive tool": "dataset",
        "paper": "work", "workstream and resource library": "institution", "non-profit organisation": "institution", "resource hub": "site",
        "worker-run organizing and advocacy project": "institution", "participatory research initiative": "institution"}
HOMONYM = {"Microsoft Working with AI": "Microsoft's own AI products and workforce", "Canaries in the Coal Mine": "the idiom", "Negotiating Tech": "salary negotiation"}


def slugq(q): return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")


def chipkind(k):
    for full, lab in [("global, radically participatory research initiative", "participatory research initiative")]:
        if k.startswith(full): return lab
    h = re.split(r":| \(|, | with | published | built ", k, maxsplit=1)[0].strip()
    return h.replace("working paper and monthly-updated dashboard", "working paper and dashboard")


sets, by, groups = PB.load()
new, bad, cnt = PB.verify(by, groups)
print(f"per-dim verify: {cnt['quotes']} record quotes · {cnt['spans']} spans · {len(new)} new atom sets · {len(bad)} miss(es)")
for b in bad[:40]: print("  ✗", b)
rows = {r["entry"]: r for r in PB.score(by, new, groups)}
if bad:
    sys.exit("not built: per-dim misses")

for s in S:
    q = s["q"]; au = A[q]; ent = au["ent"]; row = CENSUS[ent]
    rec = f"https://www.laborvector.org/aggregators/{ent}/"
    slug = slugq(q) + "-aio-20261029"
    head = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), 2026-10-29. The paste is the Overview expanded "
            "(the 'AI Mode Conversation' view, with the source cards that follow the answer); the 'You said' line carries the query twice, run together, and is given once here. "
            "Inline links are Google redirect URLs, kept as pasted." + (" Supplied as an attached file." if s["source"] == "attachment" else "") + "]")
    cl = [{"n": i + 1, "site": c["site"], "rel": "third_party", "url": None, "title": c["title"], "snip": c.get("snip"),
           "note": ("video, " + c["duration"]) if c.get("duration") else None} for i, c in enumerate(s["cards"])]
    body = s["text"]
    t = head + "\n\n[QUERENT] " + q + "\n\n[SYSTEM] " + body
    r = rows[slug]
    pd = PB.pd_of(r)
    pd["read"]["brief"] = "rebuild/capture-registry/intake-20261029-labor/per/BRIEF.md"
    pd["read"]["by"] = f"intake reader {r['group']}, spans and record quotes checked verbatim by scripts/per_backlog.py"
    e = {"slug": slug, "date": "2026-10-29", "surface": "Google AI Overview",
         "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18).",
         "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14.",
         "ev": "paste", "match": "BROAD MATCH", "match_note": None, "mt": au["mt"], "s": "Machine Reception", "q": q,
         "q_kind": (f"the common name of an entity of the Labor Vector meta-aggregator ({row['name']}; record {rec}, compiled 2026-10-29), supplied for capture and run by the operator the same day, "
                    "to supply the composition layer's account of the entity for its record and its /non row. "
                    + (f"The name is also {HOMONYM[q]}, and the composition gives that sense. " if q in HOMONYM else "")
                    + "A baseline: the record landed on laborvector.org the same day (commit bf90841) and no card cites it. NEW address."),
         "turns": 1, "cites": len(cl), "archive_controlled_cites": 0, "cite_list": cl,
         "transcript": t, "transcript_raw": body,
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the Overview expanded, with its source cards",
         "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-29",
         "d": au["d"], "reading": au["reading"], "findings": au["findings"], "analysis": au["analysis"],
         "per_v": au["per_v"], "per_note": au["per_note"], "per_dim": pd,
         "originator": {"name": row["operator"], "relation": "external", "entity_type": TYPE.get(chipkind(row["kind"]), "dataset"), "spxi_treatment": "partial",
                        "basis": f"Not the archive's: {row['name']}; its operator, as the record gives it: {row['operator']}. Formalized by the Labor Vector meta-aggregator record of 2026-10-29 ({rec}), editor Lee Sharks; the record's fields carry verbatim quotes from the entity's own pages, saved with sha256."},
         "related_deposits": [],
         "notes": {"prompts": ("One query. Sent by the operator on 2026-10-29 with fourteen others, one per entity of the Labor Vector meta-aggregator, from the common names supplied for capture; "
                               "twelve pasted in one message with '$' between them and three attached as files. Saved verbatim from the session transcript the moment it arrived "
                               "(rebuild/capture-registry/intake-20261029-labor/).")}}
    if "--check" not in sys.argv:
        json.dump(e, open(H / (slug + ".json"), "w"), ensure_ascii=False, indent=1)
    print(slug, len(cl), r["gate"], r["reached"], r["scores"])

if "--check" not in sys.argv:
    have = {x["id"] for x in sets["entities"]}
    added = 0
    for sid, (g, s) in new.items():
        if sid in have: continue
        sets["entities"].append({"id": sid, "name": s["name"], "template": s["template"], "type_basis": s.get("type_basis"), "records": s.get("records"),
                                 "atoms": s["atoms"], "required": [x["atom"] for x in s["atoms"] if x.get("applicability") == "required"],
                                 "inversion_guidance": s.get("inversion_guidance"), "notes": s.get("notes"), "external": True,
                                 "state": f"intake pass (rubric v1.1) 2026-10-29, reader {g}", "state_d": f"intake pass (rubric v1.1) 2026-10-29, reader {g}"}); added += 1
    sets["count"] = len(sets["entities"]); sets["with_atom_set"] = sum(1 for x in sets["entities"] if x.get("atoms"))
    sets.setdefault("intake_pass", []).append({"date": "2026-10-29", "brief": "rebuild/capture-registry/intake-20261029-labor/per/BRIEF.md", "new_sets": sorted(new),
                                               "checked_by": "scripts/per_backlog.py (record quotes and spans verbatim)"})
    PB.PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("atom sets added", added)
