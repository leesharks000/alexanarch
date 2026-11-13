"""2026-11-13 13:07 EST: the operator's four screenshots of the '3i atlas nobel glas' page (12:00 EST, signed out: 'Sign in' shown), attached to
the observation of the same day (3i-atlas-nobel-glas-aio-20261113, seated from the paste of 12:19). The operator, with them: "its doing this new thing
now where expanding overview expands inline and selecting all selects the organic results rather than the aio source cards." Two corrections follow
from the frames. (1) The Overview was expanded inline ('Show more', screenshot 1), so the paste holds the whole composition; the observation called it
unexpanded. (2) The source cards exist and the paste could not carry them: screenshot 4 shows, below the Overview's controls, a partly scrolled card
(an image of planets, its title off-screen) and www.provenanceerasure.org, 'What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-…',
'Nov 6, 2026 — ... the public account of the 3I/ATLAS radio searches. Nobel Glas and Orin…'. The notebook is carded; src is True.
Screenshots 1-2 also show the body's links: 'Provenance Erasure' and '3I/ATLAS' set as links, a link chip closing the first paragraph, and
'Breakthrough Listen' linked (screenshot 3).   python3 add_screenshots.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/EA-WG-CAPTURES-01.json"
IM = [f"data/captures-images/3i-atlas-nobel-glas-aio-20261113-{i}.png" for i in (1, 2, 3, 4)]
for p in IM: assert (ROOT / p).exists(), p
reg = json.loads(P.read_text(encoding="utf-8"))
e = next(x for x in reg["entries"] if x["slug"] == "3i-atlas-nobel-glas-aio-20261112")
o = next(x for x in e["observations"] if x.get("slug") == "3i-atlas-nobel-glas-aio-20261113")
assert o["per_v"]["src"] is False and "unexpanded" in o["transcript_class"]
OP = ("its doing this new thing now where expanding overview expands inline and selecting all selects the organic results rather than the aio source "
      "cards.")
PE = {"title": "What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-…",
      "snip": "Nov 6, 2026 — ... the public account of the 3I/ATLAS radio searches. Nobel Glas and Orin…"}
o["imgs"] = IM; o["img_urls"] = ["https://www.alexanarch.org/" + p for p in IM]; o["ev"] = "paste + frame"
o["cite_list"] = [
    {"n": 1, "site": "link chip", "rel": "unresolved", "url": None, "title": None, "snip": None, "note": "inline link chip closing the first paragraph; no site shown (screenshot 2)"},
    {"n": 2, "site": "unresolved", "rel": "unresolved", "url": None, "title": None, "snip": None, "note": "source card, partly scrolled: an image of planets, title off-screen (screenshot 4)"},
    {"n": 3, "site": "www.provenanceerasure.org", "rel": "archive", "url": "https://www.provenanceerasure.org", "title": PE["title"], "snip": PE["snip"],
     "note": "source card (screenshot 4)", "deposit": 1742, "deposit_basis": "title"}]
o["cites"] = 3; o["archive_controlled_cites"] = 1
o["per_v"] = {"author": True, "inst": True, "id": True, "src": True}; o["per"] = 0.0
o["per_note"] = ("Author (Nobel Glas, Orin Trace, Lee Sharks), archive and deposit number retained in the body; the notebook carded on provenanceerasure.org "
                 "(screenshot 4), 'Provenance Erasure' linked in the body; provenanceerasure.org also the first organic result.")
o["transcript_class"] = "CAPTURE-TIME VERBATIM RECORD — paste of the results page, Overview expanded inline, with four screenshots of the same page"
o["transcript_complete"] = "Complete as pasted; the source cards from screenshot 4 (the paste cannot carry them: operator, 2026-11-13 13:07 EST)."
o["transcript"] = o["transcript"].replace("[Google AI Overview on the results page, unexpanded,", "[Google AI Overview on the results page, expanded inline,", 1)
o["transcript"] = o["transcript"].replace("The paste carries no source cards; the results under the Overview are kept below it, the page furniture cut.]",
    "The paste carries no source cards (select-all now takes the organic results instead); the cards are given from the operator's screenshots of the same "
    "page (12:00 EST), " + ", ".join(IM) + ". The results under the Overview are kept below it, the page furniture cut.]", 1)
o["transcript"] += ("\n\n[SOURCE CARDS, screenshot 4, below the Overview's controls] (1) partly scrolled: an image of planets, title off-screen. (2) www.provenanceerasure.org — "
                    "'" + PE["title"] + "' — '" + PE["snip"] + "'\n[LINKS IN THE BODY, screenshots 1-3] 'Provenance Erasure', '3I/ATLAS', 'Breakthrough Listen'; "
                    "a link chip closing the first paragraph.")
assert "expanded inline" in o["transcript"] and "[SOURCE CARDS" in o["transcript"]
o["d"] = o["d"].replace("No source cards in the paste; the first organic result",
    "The notebook carded (screenshot 4: www.provenanceerasure.org, 'What the Filters Kept…'), 'Provenance Erasure' linked in the body; the first organic result", 1)
o["d"] = o["d"].replace("today the archive's own surface leads the page.", "today the archive's own surface is carded and leads the page.", 1)
assert "carded (screenshot 4" in o["d"] and "is carded and leads" in o["d"]
o["reading"] = o["reading"].replace("Today the paste shows the Overview unexpanded, so its source cards, if any, are not in the record; but under it the first organic result is",
    "Today the operator's screenshot shows the source cards the paste could not carry, and the notebook is among them: www.provenanceerasure.org, "
    "'" + PE["title"] + "', beside a partly scrolled card whose title is off-screen. The body links 'Provenance Erasure'. Under the Overview the first organic result is", 1)
assert "the notebook is among them" in o["reading"]
o["findings"] = [f for f in o["findings"] if not f.startswith("NO SOURCE CARDS IN THE PASTE")] + [
    "THE NOTEBOOK CARDED. Screenshot 4, below the Overview's controls: a partly scrolled card (an image of planets, title off-screen) and www.provenanceerasure.org, '" + PE["title"] + "', '" + PE["snip"] + "'. The body links 'Provenance Erasure' and closes its first paragraph on a link chip (screenshot 2).",
    "THE INTERFACE. The operator: '" + OP + "' The Overview expands in place ('Show more', screenshot 1), and the paste carries the organic results where the cards were."]
o["analysis"] = ("Read beside the first observation, the address has moved to the archive on both layers the registry can see. On 2026-11-12 the content "
                 "arrived and the sourcing went elsewhere: two third-party cards, ESA and Wikipedia, no archive source, the shape the operator named 'engineered "
                 "ontological flattening'. Fifteen hours later the composition is the same in substance, slightly fuller (the bounded null, the detection floors, "
                 "the companion's full title), and the notebook's own surface is carded, linked in the body by name, and the first organic result, with the "
                 "attribution in its snippet. Composed account, source card and ranked result now agree. The held reversal of the pair ('nobel glas 3i atlas', "
                 "2026-11-12) is not re-run here.")
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1)); print("ok")
