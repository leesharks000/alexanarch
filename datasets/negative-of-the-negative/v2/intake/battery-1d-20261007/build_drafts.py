#!/usr/bin/env python3
"""Author the /non drafts for battery 1d, run by the operator 2026-10-07 (message of 14:43 EDT):
'literary heteronym', 'machine learning classifiers particle accelerators' — "signed out incognito".
Surface not specified: recorded as the AI Overview by the standing default (operator, 2026-10-01: "it started in
overview, as they all do now - assume they do, i will specify if they begin in ai mode"); the 'AI Mode Conversation'
headers are the expanded Overview's residue. Archive absent at both.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
AUTH = "signed out, incognito"
AUTH_BASIS = "'signed out incognito' — operator, 2026-10-07 14:43 EDT."
SURF_BASIS = "Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they begin in ai mode'). The 'AI Mode Conversation' header is the expanded Overview's residue."
SEAT = "Seated 2026-10-07 from the operator's message of 14:43 EDT (battery 1d)."

def cards(spec):
    return [dict(n=i + 1, site=s, title=t, snip=sn, rel="third_party", url=None, note=no) for i, (s, t, sn, no) in enumerate(spec)]

drafts = []
raw = (HERE / "paste-literary-heteronym.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: literary heteronymliterary heteronym")
spec = [("Wikipedia", "Heteronym (literature) - Wikipedia", "The literary concept of the heteronym refers to one or more imaginary character(s) created by a writer to write in different styles. Heteronyms differ from pen ...", None),
        ("Poetry Society of America", "Fernando Pessoa & His Heteronyms", None, None),
        ("Bright Night 2025", "W.B. Yeats and the Introduction of Heteronym into the Western Literary Canon | Studi irlandesi. A Journal of Irish Studies", None, "site label as shown on the card"),
        ("Art and Popular Culture", "Heteronym (literature)", None, "dated Apr 11, 2008 on the card"),
        ("Art and Soul Group", "The work and the heteronyms", None, None),
        ("Literary Hub", "The Heteronymous Identities of Fernando Pessoa - Literary Hub", None, None),
        ("ThoughtCo", "Heteronyms: Definition and Examples", None, "dated May 15, 2025 on the card"),
        ("Poetry International", "Pessoa’s Heteronyms", None, None)]
for s, t, sn, _ in spec:
    assert t in raw, t
    assert sn is None or sn in raw, sn
drafts.append(("literary-heteronym-aio", {"q": "literary heteronym", "entity": "literary-heteronym", "cites": 8, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body with inline citation markers, offer menu, and the source strip of 8 cards (snippets kept in the transcript)",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[5] resolving to google.com/goto; one entity link (Fernando Pessoa); source strip of 8 cards (8 pages)."}))

raw = (HERE / "paste-ml-classifiers-particle-accelerators.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: machine learning classifiers particle acceleratorsmachine learning classifiers particle accelerators")
spec = [("jacow.org", "Machine Learning for Anomaly Detection and Classification in Particle Accelerators", None, None),
        ("ScienceDirect.com", "Predicting particle accelerator failures using binary classifiers", None, None),
        ("arXiv.org", "Classifier-pruned Bayesian optimization for particle accelerator tuning - arXiv", None, None),
        ("Jefferson Lab", "Machine Learning System Improves Accelerator Diagnostics - Jefferson Lab", None, None),
        ("Los Alamos National Laboratory (.gov)", "AI algorithms used to tune particle accelerators | LANL", None, None),
        ("Oak Ridge National Laboratory (ORNL) (.gov)", "A machine learning approach for particle accelerator errant beam prediction ...", None, None),
        ("YouTube·Greg Bronevetsky", "Machine Learning in High Energy Physics", None, "video, 52m")]
for s, t, sn, _ in spec:
    assert t in raw, t
drafts.append(("ml-classifiers-particle-accelerators-aio", {"q": "machine learning classifiers particle accelerators", "entity": "ml-classifiers-particle-accelerators", "cites": 7, "cite_list": cards(spec), "transcript": raw,
  "transcript_complete": "complete as pasted: body with inline citation markers, offer questions, and the source strip of 7 cards (snippets kept in the transcript)",
  "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[3] resolving to google.com/goto; no entity links; source strip of 7 cards (6 pages, 1 YouTube video)."}))

for name, d in drafts:
    d.update({"date": "2026-10-07", "surface": "Google AI Overview", "surface_basis": SURF_BASIS, "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste",
              "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and sources as pasted", "transcript_read": "READ IN FULL 2026-10-07",
              "notes": {"seated_from": f"paste-{name.rsplit('-', 1)[0]}.txt, the operator's message of 2026-10-07 14:43 EDT", "seat": SEAT}})
    (HERE / f"draft-{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, d["cites"], "cards")
