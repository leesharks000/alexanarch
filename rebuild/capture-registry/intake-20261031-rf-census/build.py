"""Build the ten capture records of 2026-10-31 (the Revelation First meta-aggregator's entities, by their common names, on Google's
AI Overview) from the operator's paste, recovered verbatim (segments.json, from parse.py), with the authored readings in authored.py
and the dimensional PER read at intake (per/out-R1.json and out-R2.json, per/BRIEF.md). The readers' record quotes and spans are
verified, and the scores computed, by scripts/per_backlog.py's functions; their new atom sets are merged into data/per-atom-sets.json
as rf-<slug>. Every single-quoted passage in the authored readings is checked against the paste or the census's saved sources.
  python3 build.py [--check]"""
import json, pathlib, re, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
sys.path.insert(0, str(H)); sys.path.insert(0, str(ROOT / "scripts"))
from authored import A
import per_backlog as PB
DATE = "2026-10-31"
PB.BD = H / "per"; PB.GROUPS = ["R1", "R2"]
CENSUS_PATH = pathlib.Path("/home/claude/fleet/revelationfirst-com/data/rf-census/census.json")
C = json.load(open(CENSUS_PATH))  # the Revelation First census as built 2026-10-30 (revelationfirst-com de6cd74)
CENSUS = {r["slug"]: r for r in C["rows"]}
SRC = "\n".join(p.read_text(encoding="utf-8") for p in (CENSUS_PATH.parent / "sources").glob("*.txt"))
S = json.load(open(H / "segments.json"))["segments"]
TYPE = {"csntm": "institution", "oxyrhynchus-online": "dataset", "bodmer-lab": "site", "dss-digital-library": "dataset",
        "early-christian-writings": "site", "enoch-dss-dating": "work", "ithaca": "protocol", "aeneas": "protocol",
        "vesuvius-challenge": "institution", "ai-and-faith": "institution"}
HOMONYM = {"Bodmer Lab": "two laboratories of the same name (a cardiovascular laboratory and a teaching laboratory), set out beside it",
           "Early Christian Writings": "a Penguin Classics book, Early Christian Writings: The Apostolic Fathers",
           "AI and Faith": "the topic at large, with the organisation as one bullet"}


def slugq(q): return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")


def norm(s):
    s = re.sub(r" ?\[\[\d+\]\([^)]*\)(, \[\d+\]\([^)]*\))*\]", "", s)   # the inline citation clusters
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)                              # markdown links, text kept
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip()


# the authored readings quote only what the paste or the saved sources say
QT = re.compile(r"(?<![A-Za-z])'([^']{10,}?)'(?=[\s,.;:)]|$)")
qmiss = []
TX = {s["q"]: norm(s["text"]) for s in S}
for q, au in A.items():
    for fld in ["d", "findings", "analysis"]:
        for t in (au[fld] if isinstance(au[fld], list) else [au[fld]]):
            for m in QT.finditer(t):
                frag = norm(m.group(1)).rstrip(".")
                if frag.upper() == frag or frag == "AI Mode Conversation": continue   # the record's own labels and the paste header
                if frag.endswith("..."): frag = frag[:-3]
                parts = [p.strip() for p in frag.split("…")]
                if not all(p in TX[q] or p in norm(SRC) or p in norm(json.dumps(CENSUS[au["ent"]], ensure_ascii=False)) for p in parts if p):
                    qmiss.append((q, fld, m.group(1)[:90]))
print(f"authored quotes: {len(qmiss)} miss(es)")
for x in qmiss: print("  ✗", x)

sets, by, groups = PB.load()
new, bad, cnt = PB.verify(by, groups)
print(f"per-dim verify: {cnt['quotes']} record quotes · {cnt['spans']} spans · {len(new)} new atom sets · {len(bad)} miss(es)")
for b in bad[:40]: print("  ✗", b)
if bad or qmiss:
    sys.exit("not built")
rows = {r["entry"]: r for r in PB.score(by, new, groups)}

for s in S:
    q = s["q"]; au = A[q]; ent = au["ent"]; row = CENSUS[ent]
    rec = f"https://www.revelationfirst.com/aggregators/{ent}/"
    slug = slugq(q) + "-aio-20261031"
    head = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), received 2026-10-31 00:04 EDT. The paste is the Overview expanded "
            "(the 'AI Mode Conversation' view, with the source cards that follow the answer)"
            + ("; the 'You said' line carries the query twice, run together, and is given once here" if s["header"] else
               "; this paste alone has no 'AI Mode Conversation' header and no 'You said' line, and its query is its first line, given once here")
            + ". Inline links are Google redirect URLs, kept as pasted." + (" Supplied as an attached file." if s["source"] == "attachment" else "") + "]")
    cl = [{"n": i + 1, "site": c["site"], "rel": "third_party", "url": None, "title": c["title"], "snip": c.get("snip"),
           "note": ("video, " + c["duration"]) if c.get("duration") else None} for i, c in enumerate(s["cards"])]
    body = s["text"]
    t = head + "\n\n[QUERENT] " + q + "\n\n[SYSTEM] " + body
    r = rows[slug]
    pd = PB.pd_of(r, on=DATE)
    pd["read"]["brief"] = "rebuild/capture-registry/intake-20261031-rf-census/per/BRIEF.md"
    pd["read"]["by"] = f"intake reader {r['group']}, spans and record quotes checked verbatim by scripts/per_backlog.py"
    e = {"slug": slug, "date": DATE, "surface": "Google AI Overview",
         "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18).",
         "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14.",
         "ev": "paste", "match": "BROAD MATCH", "match_note": None, "mt": au["mt"], "s": "Machine Reception", "q": q,
         "q_kind": (f"the common name of an entity of the Revelation First meta-aggregator, 'the field' ({row['name']}; record {rec}, compiled 2026-10-30), supplied for capture by the archive and run by the operator, "
                    "to supply the composition layer's account of the entity for its record. "
                    + (f"The name is also {HOMONYM[q]}, and the composition gives that. " if q in HOMONYM else "")
                    + ("The operator added the disambiguator to a name that is bare a homonym. " if q in ("Ithaca DeepMind", "Aeneas DeepMind", "Enoch AI dating Dead Sea Scrolls") else "")
                    + "A baseline: the record was built on revelationfirst.com the day before and no card cites it. NEW address."),
         "turns": 1, "cites": len(cl), "archive_controlled_cites": 0, "cite_list": cl,
         "transcript": t, "transcript_raw": body,
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the Overview expanded, with its source cards" if cl else "CAPTURE-TIME VERBATIM RECORD — paste of the Overview expanded; no card rail in the paste",
         "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-31",
         "d": au["d"], "reading": au["reading"], "findings": au["findings"], "analysis": au["analysis"],
         "per_v": au["per_v"], "per_note": au["per_note"], "per_dim": pd,
         "originator": {"name": row["operator"], "relation": "external", "entity_type": TYPE[ent], "spxi_treatment": "partial",
                        "basis": f"Not the archive's: {row['name']}; its operator, as the record gives it: {row['operator']}. Formalized by the Revelation First meta-aggregator record of 2026-10-30 ({rec}), editor Lee Sharks; the record's fields carry verbatim quotes from the entity's own pages, saved with sha256."},
         "related_deposits": [],
         "notes": {"prompts": ("One query. Sent by the operator on 2026-10-31 (00:04 EDT) with nine others, one per entity of the Revelation First meta-aggregator, from the addresses the archive supplied for capture on 2026-10-30; "
                               "eight pasted in one message with '$' between them and two attached as files (the Vesuvius Challenge attached twice, the copies byte-identical). Saved verbatim from the session transcript "
                               "(rebuild/capture-registry/intake-20261031-rf-census/).")}}
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
                                 "state": f"intake pass (rubric v1.1) {DATE}, reader {g}", "state_d": f"intake pass (rubric v1.1) {DATE}, reader {g}"}); added += 1
    sets["count"] = len(sets["entities"]); sets["with_atom_set"] = sum(1 for x in sets["entities"] if x.get("atoms"))
    sets.setdefault("intake_pass", []).append({"date": DATE, "brief": "rebuild/capture-registry/intake-20261031-rf-census/per/BRIEF.md", "new_sets": sorted(new),
                                               "checked_by": "scripts/per_backlog.py (record quotes and spans verbatim)"})
    PB.PS.write_text(json.dumps(sets, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("atom sets added", added)
