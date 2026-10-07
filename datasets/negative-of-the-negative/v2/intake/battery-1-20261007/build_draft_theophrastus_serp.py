#!/usr/bin/env python3
"""Author the /non draft for 'theophrastus' (the person's address), 2026-10-07, attachment of 09:24 EDT.

At 09:21 the operator explained why the Theophrastus run went to AI Mode: "there isnt an aio popup for the
named individual itself, per se - there is a Wikipedia snippet and it links to wikipedia." This is that results
page: no Overview is composed; the knowledge panel projects a Wikipedia extract. Under spec §2.2 a null
composition is a transcript; it is seated as the address's Overview observation, with the extract as what
stands in the composition's place. The organic layer is recorded in sf, outside the field.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-theophrastus-serp.txt").read_text(encoding="utf-8")
L = raw.split("\n")
assert L[0] == "Sign in" and L[2] == "theophrastus" and "AI Overview" not in raw
EXTRACT = ("Theophrastus was an ancient Greek philosopher and naturalist. A native of Eresos in Lesbos, he was Aristotle's close "
           "colleague and successor as head of the Lyceum, the Peripatetic school of philosophy in Athens.")
assert EXTRACT in raw and L[L.index(EXTRACT + " ") + 1] == "Wikipedia"
for f in ("Parents: Melantas", "Full name: Tyrtamus", "Theophrastus Bombastus Von Hohenheim (Paracelsus)"):
    assert f in raw, f
d = {
 "q": "theophrastus", "date": "2026-10-07", "surface": "Google AI Overview",
 "surface_basis": ("The Overview surface at a named individual: no Overview is composed (operator, 2026-10-07 09:21: 'there isnt an aio "
                   "popup for the named individual itself, per se - there is a Wikipedia snippet and it links to wikipedia'). Seated as a "
                   "null composition (spec §2.2), from the results page the operator attached at 09:24."),
 "auth": "not attested",
 "auth_basis": "The attachment of 09:24 carries no statement; the page shows 'Sign in'. The 09:21 attestation ('signed out, incognito') was given for battery 1's three runs.",
 "ev": "paste", "entity": "theophrastus", "transcript": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — results page with no Overview: knowledge panel, organic layer, footer",
 "transcript_complete": "complete as attached: tab row, knowledge panel (images, born/died, the Wikipedia extract, quick facts), People also ask, organic results to the footer",
 "transcript_read": "READ IN FULL 2026-10-07", "cites": 1,
 "cite_list": [{"n": 1, "site": "Wikipedia", "title": None, "snip": EXTRACT, "rel": "third_party", "url": None,
                "note": "the knowledge panel's 'Overview' extract and its one source label; no composition"}],
 "sf": ("Google Search, signed-out page ('Sign in'), dark theme on; AI Mode tab listed, not selected; no AI Overview. Knowledge panel: "
        "'Theophrastus · Philosopher', 15 images, Born Eresos / Died Athens, the Wikipedia extract under 'Overview', Quick facts "
        "(Parents: Melantas; Full name: Tyrtamus), People also ask (four questions, one 'What was Theophrastus' real name?'). Organic: "
        "Wikipedia, SEP (Ierodiakonou 2016), Books strip, University at Buffalo, Britannica, Loeb, three YouTube videos, Herbal Academy, "
        "Classical Liberal Arts Academy, NIH/PMC on Theophrastus Bombastus von Hohenheim (Paracelsus), California Academy of Sciences. "
        "Location line 'Brightmoor, Detroit, MI - Based on your past activity'."),
 "notes": {"seated_from": "paste-theophrastus-serp.txt, the operator's attachment of 2026-10-07 09:24 EDT",
           "pair": "the AI Mode composition for the same person is theopheastus-20261007 (issued misspelled, 09:08)",
           "facts_unsourced": "the quick facts (Parents: Melantas; Full name: Tyrtamus) carry no source on the panel",
           "name_collision": "the organic layer includes a second person carrying the name: Theophrastus Bombastus von Hohenheim (Paracelsus)",
           "seat": "Seated 2026-10-07 from the operator's attachment of 09:24 EDT."},
}
(HERE / "draft-theophrastus-serp.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote theophrastus null-Overview draft")
