#!/usr/bin/env python3
"""Author the /non drafts for battery 1c, run by the operator 2026-10-07 (message of 12:12 EDT):
'the singularity', 'political economy' — "same conditions" as battery 1b: signed out, incognito, expanded from
the AIO popup. The 'AI Mode Conversation' headers are the expanded Overview's residue. Archive absent at both.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
AUTH = "signed out, incognito"
AUTH_BASIS = "'couple more, same conditions' — operator, 2026-10-07 12:12 EDT, referring to battery 1b's 'all incognito, signed out, expanded from aio popup' (11:49)."
SURF_BASIS = "'same conditions' (expanded from the AIO popup) — operator, 2026-10-07 12:12 EDT; the 'AI Mode Conversation' header is the expanded Overview's residue."
SEAT = "Seated 2026-10-07 from the operator's message of 12:12 EDT (battery 1c)."

def cards(spec):
    return [dict(n=i + 1, site=s, title=t, snip=sn, rel="third_party", url=None, note=no) for i, (s, t, sn, no) in enumerate(spec)]

drafts = []
raw = (HERE / "paste-the-singularity.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: the singularitythe singularity")
spec = [("Wikipedia", "Technological singularity - Wikipedia", "\"The Singularity\" redirects here. For other uses, see Singularity. The technological singularity, often simply called the singularity, is a hypothetical event i...", None),
        ("Third Way", "What is the Artificial Intelligence Singularity?", None, None),
        ("IBM", "What is the Technological Singularity? | IBM", None, None),
        ("Daniel Miessler", "What the Singularity Actually Means | Daniel Miessler", None, None),
        ("Wikipedia", "The Singularity Is Near", None, None),
        ("Forbes", "What Is The Singularity And Are We There Yet?", None, None),
        ("www.singularity.com", "The Singularity is Near » Homepage", None, None),
        ("The Hill", "What is the AI singularity? Some experts say it’s closer than ever", None, None),
        ("Britannica", "Singularity | Benefits, Challenges & Implications - Britannica", None, None),
        ("Reddit", "Would anyone mind explaining to me like I'm 5 what the singularity is?", None, None),
        ("YouTube·Absolutely Agentic", "The Singularity is Coming", None, "video, 19:19")]
for s, t, sn, _ in spec:
    assert t in raw, t
drafts.append(("the-singularity-aio", {"q": "the singularity", "entity": "the-singularity", "cites": 11, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body with inline citation markers and the source strip of 11 cards (snippets kept in the transcript)",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[5] resolving to google.com/goto; one entity link (The Singularity is Near); source strip of 11 cards (9 pages, 1 Reddit thread, 1 YouTube video)."}))

raw = (HERE / "paste-political-economy.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: political economypolitical economy")
spec = [("Wikipedia", "Political economy", None, None),
        ("Harvard University", "Political Economy – Department of Government", None, None),
        ("Britannica", "Political economy | Definition, History, Types, Examples, & Facts - Britannica", None, None),
        ("Investopedia", "Understanding Political Economy: History and Real-World Impacts", None, None),
        ("Universidad Europea", "Political economy meaning | UE Blog", None, None),
        ("EBSCO", "Political economy | Economics | Research Starters | EBSCOhost", None, None),
        ("YouTube·The Left Library", "An Introduction to Political Economy", None, "video, 2m"),
        ("YouTube·Noah Zerbe", "Foundations of Global Political Economy", None, "video, 2m")]
for s, t, sn, _ in spec:
    assert t in raw, t
drafts.append(("political-economy-aio", {"q": "political economy", "entity": "political-economy", "cites": 8, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body with inline citation markers, offer menu, source strip of 8 cards (snippets kept in the transcript), disclaimer",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[5] resolving to google.com/goto; one entity link (Adam Smith); source strip of 8 cards (6 pages, 2 YouTube videos)."}))

for name, d in drafts:
    d.update({"date": "2026-10-07", "surface": "Google AI Overview", "surface_basis": SURF_BASIS, "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste",
              "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-07",
              "notes": {"seated_from": f"paste-{name.rsplit('-', 1)[0]}.txt, the operator's message of 2026-10-07 12:12 EDT", "seat": SEAT}})
    (HERE / f"draft-{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, d["cites"], "cards")
