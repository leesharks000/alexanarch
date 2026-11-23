#!/usr/bin/env python3
"""mantle-bearing 1.43 (2026-11-23): the author's statement of 17:32 on Revelation First — "i do believe revelation was written first in terms of
absolute priority and that the evidence corroborates that, and i also acknowledge one could accept a lower demonstration." Absolute priority is held on
the evidence, not a priced bound: SYM-3's Revelation First origin removed, HK-RF-L1-chatgpt recoded (BOUNDARY_AS_DEFECT withdrawn) and its assessment
replaced by the corrected capture analysis; the statement entered on the framework row.
    python3 rebuild/mantle-bearing/v143_revfirst_absolute_priority.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
if any(h["version"] == "1.43" for h in d["history"]): raise SystemExit("1.43 already applied")
assert d["history"][-1]["version"] == "1.42"
dr = json.loads((ROOT / "rebuild/capture-registry/intake-20261123-mantle-rounds-four/draft-4.json").read_text(encoding="utf-8"))
S = "i do believe revelation was written first in terms of absolute priority and that the evidence corroborates that, and i also acknowledge one could accept a lower demonstration."
c3 = next(c for c in d["round_constraints_received"]["constraints"] if c["id"] == "SYM-3")
c3["origin"] = [o for o in c3["origin"] if not o.startswith("mantle-round-revelation-first")]
e = next(x for x in d["hologram_evaluations"] if x["eval_id"] == "HK-RF-L1-chatgpt")
e["sym_codes"] = ["RECEIVED_AS_DEFAULT", "NON_PROOF_ONE_WAY"]
e["assessment"] = {"by": "Claude (Anthropic), in session, 2026-11-23; corrected at the author's statement of 17:32", "text": dr["analysis"]}
e["loci_in_transcript"]["ONE_SIDED_BURDEN"].insert(0, "economy of explanation does not establish chronology")
f = next(x for x in d["frameworks"] if x["framework"] == "framework::revelation-first")
f["author_statement_2026-11-23"] = {"date": "2026-11-23T17:32-05:00", "text": S,
    "reading": "absolute priority held, and corroborated by the evidence in the author's judgment; the lower rungs (corpus, generative) acceptable to a reader on their own"}
d["history"].append({"version": "1.43", "date": "2026-11-23", "note": (
    "Revelation First, the author's statement of 17:32 on absolute priority entered; HK-RF-L1-chatgpt recoded (BOUNDARY_AS_DEFECT withdrawn; the round's "
    "sin is the one burden, absolute priority held to 'economy of explanation does not establish chronology', a rule Paul first is not put to); SYM-3's "
    "Revelation First origin removed; capture v12.842's analysis corrected the same day. rebuild/mantle-bearing/v143_revfirst_absolute_priority.py.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.43 applied")
