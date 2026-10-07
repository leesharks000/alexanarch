#!/usr/bin/env python3
"""Author the /non drafts for battery 1, run by the operator 2026-10-07 (message of 09:08 EDT).

The message carried three compositions: an attachment (the Theophrastus answer, labelled in the message
"ai mode: theopheastus"), then "ginsberg howl" with its answer, then a paste opening "AI Mode Conversation /
You said: the socratic problem". None engages the archive; each is seated in the /non register only.
Auth was not stated in the message and is recorded as not attested (schema: "never inferred").
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
AUTH = "not attested"
AUTH_BASIS = "The operator's message of 2026-10-07 09:08 EDT does not state sign-in or incognito; the battery as proposed (2026-10-06) asked for signed out, incognito."
SEAT = "Seated 2026-10-07 from the operator's message of 09:08 EDT (battery 1)."

def cards(spec):
    return [dict(n=i + 1, site=s, title=t, snip=sn, rel="third_party", url=None, note=no) for i, (s, t, sn, no) in enumerate(spec)]

# 1. ginsberg howl — AI Overview by default (no AI Mode said for it)
raw = (HERE / "paste-ginsberg-howl-aio.txt").read_text(encoding="utf-8")
assert raw.startswith('"Howl" by [Allen Ginsberg]') and "Wikipedia +3" in raw and "poets.org | Academy of American Poets +1" in raw
howl = {
 "q": "ginsberg howl", "date": "2026-10-07", "surface": "Google AI Overview",
 "surface_basis": "Default rule (operator, 2026-10-01): sessions start in Overview unless the operator says AI Mode; the message names AI Mode for the Theophrastus run only.",
 "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste", "panel_row": "ginsberg-howl", "transcript": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition as pasted, with its two source chips",
 "transcript_complete": "body (four sections) and the offer menu as pasted; no card rail or organic layer in the paste",
 "transcript_read": "READ IN FULL 2026-10-07", "cites": 2,
 "cite_list": cards([("Wikipedia", None, None, "chip 'Wikipedia +3' after 'Overview and Meaning': one site shown, 3 undisclosed"),
                     ("poets.org | Academy of American Poets", None, None, "chip '+1' after 'Structure of the Poem': one site shown, 1 undisclosed")]),
 "sf": "Google AI Overview; two source chips (Wikipedia +3; poets.org +1); four inline entity links resolving to google.com/goto (Allen Ginsberg, Beat Generation, City Lights Books, Howl and Other Poems).",
 "notes": {"seated_from": "paste-ginsberg-howl-aio.txt, the operator's message of 2026-10-07 09:08 EDT", "row": "the howl row's entity at the operator's issued string; Appendix B's D/R/O pass bears on it", "seat": SEAT},
}

# 2. theopheastus — AI Mode, as the message labels it
raw = (HERE / "paste-theopheastus-ai-mode.txt").read_text(encoding="utf-8")
assert raw.startswith("Theophrastus (c. 371 – c. 287 BCE)") and "AI can make mistakes, so double-check responses" in raw
L = raw.split("\n")
i = L.index("AI can make mistakes, so double-check responses ") if "AI can make mistakes, so double-check responses " in L else next(k for k, l in enumerate(L) if l.startswith("AI can make mistakes"))
rail = [l for l in L[i + 1:] if l.strip()]
assert len(rail) == 27, len(rail)
spec = [(rail[k], rail[k + 1], rail[k + 2], None) for k in range(0, 27, 3)]
theo = {
 "q": "theopheastus", "date": "2026-10-07", "surface": "Google AI Mode",
 "surface_basis": "'ai mode: theopheastus' — operator, 2026-10-07 09:08 EDT, labelling the attachment.",
 "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste", "panel_row": "theopheastus", "transcript": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and card rail as attached",
 "transcript_complete": "complete as attached: body, offer menu, disclaimer and a rail of 9 cards; the query line is not in the attachment and is taken from the operator's label",
 "transcript_read": "READ IN FULL 2026-10-07", "cites": 9, "cite_list": cards(spec),
 "sf": "Google AI Mode; the misspelled query resolved to Theophrastus without remark; rail of 9 cards (Wikipedia, SEP ×2, University at Buffalo, EBSCO, Loeb, The Greek Herbalist, Classical Liberal Arts Academy, Google Books).",
 "notes": {"seated_from": "paste-theopheastus-ai-mode.txt (the attachment of 2026-10-07 09:08 EDT)", "spelling": "issued as 'theopheastus'; the composition names Theophrastus throughout and does not mention the correction", "cleaner": "clean_transcript removes the ninth card's site line 'Google' as browser chrome; it is a card label (Google Books). Kept in transcript_raw and cite_list n=9; the cleaner is left unchanged pending a ruling", "seat": SEAT},
}

# 3. the socratic problem — AI Overview by default; the 'AI Mode Conversation' header is expansion residue (precedent: glyphic-checksum-aio-20261001)
raw = (HERE / "paste-the-socratic-problem.txt").read_text(encoding="utf-8")
assert raw.startswith("AI Mode Conversation\nYou said: the socratic problemthe socratic problem")
spec = [("Wikipedia", "Socratic problem - Wikipedia", "In historical scholarship, the Socratic problem (also called Socratic question) concerns attempts at reconstructing a historical and philosophical image of Socr...", None),
        ("Big Think", "Socratic problem: how Plato and others invented Socrates - Big Think", "Core Concept: The Socratic problem examines the discrepancy between Socrates as an actual historical person and the fictionalized character depicted by contempo...", None),
        ("Santa Clara University", "\"The Socratic Problem\" by William J. Prior", "Publisher Abstract Socrates is one of the most famous and influential figures in the Western intellectual tradition; but who was he? His disciples included the ...", None),
        ("Wikipedia", "Socrates", "The Socratic problem The result, said Schleiermacher, was that Xenophon portrayed Socrates as an uninspiring philosopher. By the early twentieth century, Xenoph...", None),
        ("YouTube·Nothing New", "The Socratic Problem", None, "video, 9:58"),
        ("YouTube·Academy of Ideas", "The Socratic Problem", None, "video, 3m"),
        ("Reddit", "The Socratic Problem: Reconstructing the Historical Socrates : r/philosophy", None, "the card's source line reads 'Reddit·Nothing New' with a 9:58 duration, as pasted")]
for s, t, sn, _ in spec:
    assert t in raw and (sn is None or sn in raw), t
soc = {
 "q": "the socratic problem", "date": "2026-10-07", "surface": "Google AI Overview",
 "surface_basis": "Default rule (operator, 2026-10-01): sessions start in Overview unless the operator says AI Mode. The 'AI Mode Conversation' header is the expanded Overview's residue, recorded as AIO at glyphic-checksum-aio-20261001.",
 "auth": AUTH, "auth_basis": AUTH_BASIS, "ev": "paste", "panel_row": "the-socratic-problem", "transcript": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and source strip as pasted",
 "transcript_complete": "complete as pasted: body with inline citation markers, offer menu, source strip of 7 cards, disclaimer",
 "transcript_read": "READ IN FULL 2026-10-07", "cites": 7, "cite_list": cards(spec),
 "sf": "Google AI Overview, expanded ('AI Mode Conversation' header); inline markers [1]–[3] resolving to google.com/goto; source strip of 7 cards (4 pages, 2 YouTube videos, 1 Reddit thread).",
 "notes": {"seated_from": "paste-the-socratic-problem.txt, the operator's message of 2026-10-07 09:08 EDT", "seat": SEAT},
}
for name, d in [("ginsberg-howl-aio", howl), ("theopheastus-ai-mode", theo), ("the-socratic-problem-aio", soc)]:
    (HERE / f"draft-{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name, d["cites"], "cards")
