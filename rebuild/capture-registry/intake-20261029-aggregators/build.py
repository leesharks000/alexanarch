"""Build the twenty capture records of 2026-10-29 (the MMRS meta-aggregator's entities, by name, on Google's AI Overview) from
the operator's paste, recovered verbatim, with the authored readings in authored.py."""
import json, pathlib, re, sys
H = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(H))
from cards import split_answer, cards
from authored import A, slugq
C = json.load(open(H / "census-20261028.json"))  # the meta-aggregator census as landed on machinemediation.org, 2026-10-28
CENSUS = {r["slug"]: r for r in C["rows"]}
TYPE = {"database": "dataset", "monitor": "dataset", "leaderboard": "dataset", "curated list": "work", "audit series": "work"}
S = json.load(open(H / "segments.json"))
for s in S:
    q = s["q"]; k = slugq(q); au = A[k]; ent = au["ent"]; row = CENSUS[ent]
    ans, rest = split_answer(s["text"]); cl = cards(rest)
    for c in cl:
        if c.get("duration"): c["duration"] = re.match(r"\[?([^\]]+)", c["duration"]).group(1)
    pre = ""
    if s["operator_note_before"]:
        pre = (" Before this composition Google corrected the query to 'presence' and gave an unrelated Overview; the operator chose 'show results for presenc' (his note with the paste: '"
               + s["operator_note_before"].rstrip(":") + "'). The capture is the composition at the issued string after the override.")
    body = "\n".join(l for l in s["text"].split("\n") if not l.strip().startswith("AI responses may include mistakes")).strip()
    t = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), 2026-10-29. The paste is the Overview expanded (the 'AI Mode Conversation' view, with the source cards that follow the answer); the 'You said' line carries the query twice, run together, and is given once here. Inline links are Google redirect URLs, kept as pasted. The closing disclaimer cut." + pre + "]\n\n"
         "[QUERENT] " + q + "\n\n[SYSTEM] " + body)
    rec = f"https://www.machinemediation.org/aggregators/{ent}/"
    e = {"slug": k + "-aio-20261029", "date": "2026-10-29", "surface": "Google AI Overview",
         "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18).",
         "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14.",
         "ev": "paste", "match": "BROAD MATCH", "match_note": None, "mt": au["mt"], "s": "Machine Reception", "q": q,
         "q_kind": (f"the name of an entity of the MMRS meta-aggregator ({row.get('name', ent)}; record {rec}, compiled 2026-10-28), run at the operator's offer on 2026-10-29 to supply the composition layer's account of the entity for its record and its /non row"
                    + ("; one of the record's reception battery queries" if au.get("battery") else "")
                    + ". A baseline: the record landed on machinemediation.org the same night (commit 8997e28) and no card cites it. NEW address."),
         "turns": 1, "cites": len(cl), "archive_controlled_cites": 0,
         "cite_list": [{"n": i + 1, "site": c["site"], "rel": "third_party", "url": None, "title": c["title"], "snip": c.get("snip"),
                        "note": ("video, " + c["duration"]) if c.get("duration") else None} for i, c in enumerate(cl)],
         "transcript": t, "transcript_raw": s["text"],
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview with its source cards",
         "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-29",
         "d": au["d"], "reading": au["reading"], "findings": au["findings"], "analysis": au["analysis"],
         "per_v": au["per_v"], "per_note": au["per_note"],
         "originator": {"name": row.get("operator", ent), "relation": "external", "entity_type": "service" if ent == "codesota" else TYPE.get(row.get("kind"), "dataset"),
                        "spxi_treatment": "partial",
                        "basis": f"Not the archive's: {row.get('name', ent)}, run by {row.get('operator', 'its operator')}. Formalized by the MMRS meta-aggregator record of 2026-10-28 ({rec}), editor Lee Sharks; the record's fields are read from the entity's own pages with source and basis. Recorded 2026-10-29."},
         "related_deposits": [],
         "notes": {"prompts": "One query. Sent by the operator on 2026-10-29 with nineteen others, one per entity of the MMRS meta-aggregator, at his offer to run them: 'ill run captures if you want, just list the semantic addresses'."
                   + (" Seated with the operator's note on the spelling correction." if s["operator_note_before"] else "")}}
    json.dump(e, open(H / (e["slug"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print(e["slug"], len(cl))
