#!/usr/bin/env python3
"""Author the /non draft for battery 1f, run by the operator 2026-10-08 (message of 08:34 EDT):
'google ai overview' — "signed out incognito" (as typed: "sifned out incognito"). Surface by the standing AIO default;
the 'AI Mode Conversation' header is the expanded Overview's residue. The surface queried for itself.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-google-ai-overview.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: google ai overviewgoogle ai overview")
spec = [("search.google", "Google AI Overviews - Search anything, effortlessly", None, "Google's own product page"),
        ("Wikipedia", "AI Overviews - Wikipedia", None, None),
        ("Google Help", "Find information in faster & easier ways with AI Overviews in Google ...", None, "Google's own help page; one inline marker resolves to support.google.com/websearch/answer/14901683 directly, without google.com/goto"),
        ("Botify", "What Are Google AI Overviews and How Do They Work? - Botify", None, None),
        ("Semrush", "AI Overviews: What Are They & How to Optimize for Them - Semrush", None, None),
        ("TechRepublic", "What Is Google’s AI Overviews?", None, None),
        ("Digital Marketing Institute", "Google AI Overviews: What Do They Mean for Search?", None, None),
        ("Quora", "What is Google AI Overview and how does it affect website traffic?", None, None),
        ("Coalition Technologies", "What Are Google AI Overviews? Everything You Need To Know", None, None)]
for s, t, sn, _ in spec: assert t in raw, t
d = {"q": "google ai overview", "entity": "google-ai-overviews", "cites": 9,
     "cite_list": [dict(n=i + 1, site=s, title=t, snip=sn, rel=("first_party" if s in ("search.google", "Google Help") else "third_party"), url=None, note=no) for i, (s, t, sn, no) in enumerate(spec)],
     "transcript": raw,
     "transcript_complete": "complete as pasted: body with inline citation markers, offer line, and the source strip of 9 cards (snippets kept in the transcript)",
     "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[3], all resolving to google.com/goto except one that resolves directly to support.google.com; one entity link (Wikipedia); source strip of 9 cards, 2 of them Google's own pages.",
     "date": "2026-10-08", "surface": "Google AI Overview",
     "surface_basis": "Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they begin in ai mode'). The 'AI Mode Conversation' header is the expanded Overview's residue.",
     "auth": "signed out, incognito", "auth_basis": "'sifned out incognito' [sic] — operator, 2026-10-08 08:34 EDT.", "ev": "paste",
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-08",
     "notes": {"seated_from": "paste-google-ai-overview.txt, the operator's message of 2026-10-08 08:34 EDT", "seat": "Seated 2026-10-08 from the operator's message of 08:34 EDT (battery 1f).",
               "self_reference": "The composition layer answering for itself: the surface under observation composed its own entry, citing its owner's two pages first."}}
(HERE / "draft-google-ai-overview-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote google-ai-overview-aio", d["cites"], "cards")
