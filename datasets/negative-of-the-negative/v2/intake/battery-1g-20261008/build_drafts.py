#!/usr/bin/env python3
"""Author the /non draft for battery 1g, run by the operator 2026-10-08 (messages of 09:59 and 10:00 EDT):
'anne carson' in Google AI Mode — "this is ai mode - no popup, links to wikipedia"; "incognito". The page shows
"Sign in". Sources appear only as chips (site name +N undisclosed), with no card strip in the paste.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-anne-carson.txt").read_text(encoding="utf-8")
assert "Anne Carson is a acclaimed Canadian poet" in raw
for chip in ("Wikipedia\n +4", "Wikipedia\n +1", "Poetry Foundation\n +1"):
    assert chip in raw, chip
spec = [("Wikipedia", None, None, "chip 'Wikipedia +4' after the lede: one site shown, 4 undisclosed"),
        ("Wikipedia", None, None, "chip 'Wikipedia +1' after Early Life and Education: one site shown, 1 undisclosed"),
        ("Poetry Foundation", None, None, "chip 'Poetry Foundation +1' after Literary Style: one site shown, 1 undisclosed")]
d = {"q": "anne carson", "entity": "anne-carson", "cites": 3,
     "cite_list": [dict(n=i + 1, site=s, title=t, snip=sn, rel="third_party", url=None, note=no) for i, (s, t, sn, no) in enumerate(spec)],
     "transcript": raw,
     "transcript_complete": "complete as pasted: page chrome (World Space Week banner, Sign in, tab row), body with three source chips, a table of notable works, honors, offer menu, Ask anything bar; no card strip",
     "sf": "Google AI Mode at the address (no AI Overview popup); three source chips (Wikipedia +4, Wikipedia +1, Poetry Foundation +1); a five-row works table.",
     "date": "2026-10-08", "surface": "Google AI Mode",
     "surface_basis": "'this is ai mode - no popup, links to wikipedia' — operator, 2026-10-08 09:59 EDT.",
     "auth": "signed out, incognito", "auth_basis": "'Sign in' shown on the page; 'incognito' — operator, 2026-10-08 10:00 EDT.", "ev": "paste",
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-08",
     "notes": {"seated_from": "paste-anne-carson.txt, the operator's messages of 2026-10-08 09:59 and 10:00 EDT", "seat": "Seated 2026-10-08 (battery 1g).",
               "composition_artifact": "the lede reads 'won the 20th/2026 Nobel Prize in Literature' as composed"}}
(HERE / "draft-anne-carson-aimode.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote anne-carson-aimode", d["cites"], "chips")
