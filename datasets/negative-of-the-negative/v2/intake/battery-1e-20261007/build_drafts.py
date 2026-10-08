#!/usr/bin/env python3
"""Author the /non drafts for battery 1e, run by the operator 2026-10-07 (message of 19:41 EDT):
'the civil war', 'the causes of the german roke in wwii' — "signed out. incognito." Surface by the standing AIO
default; 'AI Mode Conversation' headers are the expanded Overview's residue. 'roke' = 'role' (operator's answer).
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
AUTH = "signed out, incognito"
AUTH_BASIS = "'signed out. incognito.' — operator, 2026-10-07 19:41 EDT."
SURF_BASIS = "Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they begin in ai mode'). The 'AI Mode Conversation' header is the expanded Overview's residue."
SEAT = "Seated 2026-10-07 from the operator's message of 19:41 EDT (battery 1e)."
def cards(spec):
    return [dict(n=i + 1, site=s, title=t, snip=sn, rel="third_party", url=None, note=no) for i, (s, t, sn, no) in enumerate(spec)]
drafts = []
raw = (HERE / "paste-the-civil-war.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: the civil warthe civil war")
spec = [("Wikipedia", "American Civil War - Wikipedia", None, None),
        ("History.com", "American Civil War: Causes, Dates & Battles | HISTORY", None, None),
        ("Britannica", "American Civil War | History, Summary, Dates, Causes, Map ... - Britannica", None, None),
        ("Gilder Lehrman Institute of American History |", "The American Civil War | Gilder Lehrman Institute of American History", None, "site label as shown on the card"),
        ("American Battlefield Trust", "A Brief Overview of the American Civil War | American Battlefield Trust", None, None),
        ("YouTube·Mapper Maniac", "Why did the American civil war happen?", None, "video, 1:00")]
for s, t, sn, _ in spec: assert t in raw, t
drafts.append(("the-civil-war-aio", {"q": "the civil war", "entity": "american-civil-war", "cites": 6, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body with inline citation markers and the source strip of 6 cards (snippets kept in the transcript), disclaimer",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[3] resolving to google.com/goto; entity links (American Civil War, Emancipation Proclamation); source strip of 6 cards (5 pages, 1 YouTube video)."}))
raw = (HERE / "paste-the-causes-of-the-german-roke-in-wwii.txt").read_text(encoding="utf-8")
assert "You said: the causes of the german roke in wwiithe causes of the german roke in wwii" in raw
spec = [("The National WWII Museum | New Orleans", "How Did Adolf Hitler Happen? | The National WWII Museum | New Orleans", None, None),
        ("The Holocaust Explained", "Causes of the Second World War – The Holocaust Explained: Designed for schools", None, None),
        ("History Hit", "5 Major Causes of World War Two in Europe | History Hit", None, "dated Jan 17, 2023 on the card"),
        ("The Holocaust Explained", "Why did Germany lose? – The Holocaust Explained: Designed for schools", None, None),
        ("History.com", "World War II: Causes, Timeline, Key Battles, Facts & Legacy | HISTORY", None, None),
        ("United States Holocaust Memorial Museum", "World War II and the Holocaust, 1939–1945", None, None),
        ("YouTube·HistoryExtra", "Why did Germany lose WW2? Expert explains the road to the Allies' win", None, "video, 3m"),
        ("The Guardian", "Why Hitler's grand plan during the second world war collapsed | Second world war | The Guardian", None, None),
        ("www.richardjevans.com", "Why Did Germany Lose the Second World War? | Richard J Evans", None, None),
        ("Facebook·German Embassy Port of Spain", "The causes for World War II lie in the ideology of National Socialism. Under ...", None, "video, 2:06"),
        ("Facebook·German Embassy Beirut", "Germany was responsible for the outbreak of World War II", None, "video, 1m")]
for s, t, sn, _ in spec: assert t in raw, t
drafts.append(("the-causes-of-the-german-roke-in-wwii-aio", {"q": "the causes of the german roke in wwii", "entity": "germany-role-wwii", "cites": 11, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body in two halves (causes of the war; causes of Germany's defeat), offer line, source strip of 11 cards (snippets kept in the transcript), disclaimer; no inline citation markers in the paste",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); the composition glosses the typo ('defeat (\"roke\")'); no inline markers or entity links in the paste; source strip of 11 cards (8 pages, 1 YouTube video, 2 Facebook videos)."}))
for name, d in drafts:
    d.update({"date": "2026-10-07", "surface": "Google AI Overview", "surface_basis": SURF_BASIS, "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste",
              "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-07",
              "notes": {"seated_from": f"paste-{name.rsplit('-', 1)[0]}.txt, the operator's message of 2026-10-07 19:41 EDT", "seat": SEAT}})
    (HERE / f"draft-{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, d["cites"], "cards")
