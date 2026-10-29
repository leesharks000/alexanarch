"""Build the fourteen capture records of 2026-10-29 (the provenance meta-aggregator's entities, by name, on Google's AI Overview)
from the operator's paste, recovered verbatim (segments.json, from parse.py), with the authored readings in authored.py."""
import json, pathlib, re, sys
H = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(H))
from authored import A
C = json.load(open(H / "census-20261029-provenance.json"))  # the provenance census as landed on provenanceerasure.org, 2026-10-29 (8a9f153)
CENSUS = {r["slug"]: r for r in C["rows"]}
TYPE = {"benchmark": "dataset", "database": "dataset", "monitor": "dataset", "registry": "dataset", "test series": "work", "tracing tool": "service",
        "algorithm and API": "service", "documentation wiki": "work", "repository (retired)": "service"}
S = json.load(open(H / "segments.json"))["segments"]
CHIPS = ["Wikipedia +3", "Fastly +1", "wikiHow +2", "wikiHow +1"]
def slugq(q): return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")
for s in S:
    q = s["q"]; au = A[q]; ent = au["ent"]; row = CENSUS[ent]
    rec = f"https://www.provenanceerasure.org/aggregators/{ent}/"
    body = s["text"]
    if s["expanded"]:
        head = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), 2026-10-29. The paste is the Overview expanded "
                "(the 'AI Mode Conversation' view, with the source cards that follow the answer); the 'You said' line carries the query twice, run together, and is given once here. "
                "Inline links are Google redirect URLs, kept as pasted.]")
        cl = [{"n": i + 1, "site": c["site"], "rel": "third_party", "url": None, "title": c["title"], "snip": c.get("snip"),
               "note": ("video, " + c["duration"]) if c.get("duration") else None} for i, c in enumerate(s["cards"])]
    else:
        head = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), 2026-10-29. The paste is the Overview as shown, "
                "unexpanded: the query once, the source chips inline with their counts ('Wikipedia +3'), no card rail. The operator's note with it: '" + s["operator_note"] + "'.]")
        cl = [{"n": i + 1, "site": c.split(" +")[0], "rel": "third_party", "url": None, "title": None, "snip": None, "note": "source chip as shown: '" + c + "'"} for i, c in enumerate(CHIPS)]
        assert all(c in body for c in CHIPS)
    t = head + "\n\n[QUERENT] " + q + "\n\n[SYSTEM] " + body
    e = {"slug": slugq(q) + "-aio-20261029", "date": "2026-10-29", "surface": "Google AI Overview",
         "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18).",
         "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14.",
         "ev": "paste", "match": "BROAD MATCH", "match_note": None, "mt": au["mt"], "s": "Machine Reception", "q": q,
         "q_kind": (f"the name of an entity of the provenance meta-aggregator ({row['name']}; record {rec}, compiled 2026-10-29), the bare entity string supplied at the operator's request "
                    "('strings on the bare entity, no follow questions') and run by him the same day, to supply the composition layer's account of the entity for its record and its /non row. "
                    "A baseline: the record landed on provenanceerasure.org the same day (commit 8a9f153) and no card cites it. NEW address."),
         "turns": 1, "cites": len(cl), "archive_controlled_cites": 0, "cite_list": cl,
         "transcript": t, "transcript_raw": body,
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the Overview" + (" expanded, with its source cards" if s["expanded"] else " as shown, with its source chips"),
         "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-29",
         "d": au["d"], "reading": au["reading"], "findings": au["findings"], "analysis": au["analysis"],
         "per_v": au["per_v"], "per_note": au["per_note"],
         "originator": {"name": row["operator"], "relation": "external", "entity_type": TYPE.get(row["kind"], "dataset"), "spxi_treatment": "partial",
                        "basis": f"Not the archive's: {row['name']}, run by {row['operator']}. Formalized by the provenance meta-aggregator record of 2026-10-29 ({rec}), editor Lee Sharks; the record's fields carry verbatim quotes from the entity's own pages, saved with sha256. Recorded 2026-10-29."},
         "related_deposits": [],
         "notes": {"prompts": "One query. Sent by the operator on 2026-10-29 with thirteen others, one per entity of the provenance meta-aggregator, from the strings supplied at his request ('shoot me those search strings. strings on the bare entity, no follow questions'); pasted in one message separated by '$'. The paste was lost to a context compaction of this session and re-pasted by the operator the same day; the second paste is the one seated."
                   + (" Seated with the operator's note on the substitution." if s["operator_note"] else "")}}
    json.dump(e, open(H / (e["slug"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print(e["slug"], len(cl))
