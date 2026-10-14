import json, sys, pathlib
sys.path.insert(0, "/home/claude/alexanarch/scripts")
from non_intake import ids
H = pathlib.Path(__file__).resolve().parent
c = json.loads((H / "capture-draft.json").read_text(encoding="utf-8"))
addr, obs = ids(c["q"], c["date"], c["surface"])
raw = (H.parent / "paste-what-is-spxi-protocol-20261013.txt").read_text(encoding="utf-8")
d = {"q": c["q"], "entity": "spxi", "cites": 10, "cite_list": c["cite_list"], "transcript": raw,
     "transcript_complete": "complete as pasted: body with inline citation markers, the closing question, and the source strip of 10 cards (snippets kept in the transcript)",
     "sf": c["sf"], "date": c["date"], "surface": c["surface"], "surface_basis": c["surface_basis"],
     "auth": c["auth"], "auth_basis": c["auth_basis"], "ev": "paste",
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-13",
     "capture_ref": {"slug": "what-is-spxi-protocol-aio-20261002", "obs_id": obs},
     "notes": {"seated_from": "paste-what-is-spxi-protocol.txt (battery-spxi-20261013), the operator's message of 2026-10-13 22:26 EDT; auth 23:16 EDT",
               "seat": "Seated 2026-10-13 in both registers; T of the /non spxi row."}}
(H / "register-draft.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(addr, obs)
