"""Seat of 2026-11-13 (received 12:19 EST): '3i atlas nobel glas' on the Google results page, the Overview unexpanded, signed out and incognito
(operator defaults; the paste opens 'Sign in'). A second observation at the address seated 2026-11-12 (3i-atlas-nobel-glas-aio-20261112), where the
Overview composed #1742 with two third-party source cards and no archive source. Today the Overview composes it again, at grain, and the first organic
result is the notebook on provenanceerasure.org. Every quotation is asserted against the paste and the seated text of #1742.   python3 seat.py
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-13"; RECV = "2026-11-13 12:19 EST"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = (ROOT / REG[1742]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
CAP = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
E = next(x for x in CAP["entries"] if x["slug"] == "3i-atlas-nobel-glas-aio-20261112")
assert E["q"] == "3i atlas nobel glas" and E["surface"] == "Google AI Overview"
raw = (H / "paste.txt").read_text(encoding="utf-8")
body = raw[raw.index("AI Overview\n") + len("AI Overview\n"):raw.index("AI responses may include mistakes.")].strip()
org = raw[raw.index("provenanceerasure.org"):raw.index("People also search for")].strip()
P = {"who": "Nobel Glas is a heteronym (pen name) used by writer and researcher Lee Sharks",
     "title": "What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data Signal Search alongside fellow heteronym Dr. Orin Trace",
     "where": "Published on Provenance Erasure (Alexanarch deposit #1742)",
     "loeb": "While Loeb consistently ranked the object at Level 4 on his anomaly scale from July 2025 through April 2026, summaries presented his early \"most likely natural\" phrasing as a later retreat toward consensus, dropping his list of anomalies.",
     "ata": "its drift-rate filter only kept positive drift rates, even though the object's trajectory produced a negative drift rate",
     "bounded": "broadened this narrow, bounded null result into an absolute claim that active radio transmitters had been completely ruled out",
     "gbt": "recorded on December 18, 2025, the authors identify thirteen weak, sub-threshold spectral features between 1665.53 and 1668.46 MHz",
     "refuse": "They explicitly note these features are fragile, unreplicated, and below published detection floors, refraining from calling them a signal or transmission.",
     "firm": "Alongside a companion piece by Lee Sharks titled A Firm No: What the 3I/ATLAS Radio Searches Could See",
     "pe": "case study in \"provenance erasure\" and attribution distortion in automated information systems",
     "org": "7 days ago — ... the public account of the 3I/ATLAS radio searches. Nobel Glas and Orin Trace, Transactions on Substrate Engineering. Alexanarch deposit #1742.",
     "orgt": "What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data ...",
     "miss": "Missing: glas"}
for k, v in P.items(): assert v in raw, k
R = {"lvl": "held at Level 4 of his scale throughout", "freq": "1665.53–1668.46 MHz", "date": "2025-12-18", "ata": "The ATA paper reports positive expected drifts",
     "firm": "A Firm No (Lee Sharks, the next deposit)", "tse": "Transactions on Substrate Engineering"}
for k, v in R.items(): assert v in T, k
assert raw.index("provenanceerasure.org") < raw.index("Spectroscopy Online") < raw.index("ALMA Observatory") < raw.index("Wikipedia")
assert "Source" not in body and "Show all" not in raw and "AI Mode Conversation" not in raw

HEAD = ("[Google AI Overview on the results page, unexpanded, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14; the paste opens "
        "'Sign in'). Received " + RECV + " as an attachment. The paste carries no source cards; the results under the Overview are kept below it, the "
        "page furniture cut.]")
transcript = HEAD + "\n\n[QUERENT] 3i atlas nobel glas\n\n[SYSTEM] " + body + "\n\n[ORGANIC RESULT 1] " + org
cards = [{"n": 1, "site": "provenanceerasure.org", "rel": "archive", "url": "https://www.provenanceerasure.org", "title": P["orgt"], "snip": P["org"],
          "note": "first organic result under the Overview, not a source card; the paste shows no source cards"}]
d = ("'3I ATLAS NOBEL GLAS', SIGNED OUT, 2026-11-13, the second observation: the Overview composes #1742 again by title, makers, venue and number "
     "('" + P["who"] + "'; '" + P["where"] + "'), its four lines at grain (Loeb at Level 4 throughout, the ATA's positive-drift window, the thirteen at "
     "1665.53–1668.46 MHz with the notebook's refusal to call them a signal, provenance erasure) and the companion A Firm No by name. No source cards in "
     "the paste; the first organic result is the notebook on provenanceerasure.org, 'Nobel Glas and Orin Trace, Transactions on Substrate Engineering. "
     "Alexanarch deposit #1742.' The day before the notebook was composed with only third-party cards; today the archive's own surface leads the page.")
reading = ("The innocent reading first, and it holds: the Overview reads the notebook and says what it says. Each claim is in #1742 at the notebook's grain: "
           "Loeb '" + R["lvl"] + "' against the Overview's framing of 'most likely natural' as a retreat; the ATA window ('" + P["ata"] + "'), and the bounded "
           "null broadened into a total one; the thirteen in the Green Bank cadence of " + R["date"] + " at " + R["freq"] + ", with the notebook's refusal kept "
           "('" + P["refuse"] + "'); and the companion named as the notebook names it ('" + R["firm"] + "'). What changed since 2026-11-12 is where the page "
           "puts the source. Then the expanded Overview carded ESA and Wikipedia and linked only the object's name. Today the paste shows the Overview "
           "unexpanded, so its source cards, if any, are not in the record; but under it the first organic result is the notebook itself on "
           "provenanceerasure.org, with its makers, venue and number in the snippet, above Spectroscopy Online, ALMA and Wikipedia, each marked 'Missing' "
           "for a word of the query. The query's two terms meet in one surface only, and the page now ranks it first.")
findings = ["THE ATTRIBUTION KEPT. '" + P["who"] + ", who co-authored a November 2026 research notebook titled " + P["title"] + ".' '" + P["where"] + "'.",
            "THE LOEB FRAMING AT GRAIN. '" + P["loeb"] + "' Notebook: Loeb's 'most likely natural', '" + R["lvl"] + "'.",
            "THE ATA WINDOW AND THE BOUNDED NULL. '" + P["ata"] + "'; public accounts '" + P["bounded"] + "'.",
            "THE THIRTEEN, AND THE REFUSAL. '" + P["gbt"] + "' '" + P["refuse"] + "'",
            "THE COMPANION NAMED. '" + P["firm"] + "', and the frame: '" + P["pe"] + "'.",
            "THE ARCHIVE FIRST ON THE PAGE. Organic result 1, provenanceerasure.org: '" + P["orgt"] + "' — '" + P["org"] + "' The next four results (Spectroscopy Online, ALMA, Wikipedia, MPS) each carry 'Missing: nobel' or '" + P["miss"] + "'.",
            "NO SOURCE CARDS IN THE PASTE. The Overview is unexpanded; whether it carded a source is not in the record."]
analysis = ("Read beside the first observation, the address moves in the archive's direction on the layer the registry can see. On 2026-11-12 the content arrived "
            "and the sourcing went elsewhere: two third-party cards, no archive source, the shape the operator named 'engineered ontological flattening'. Fifteen "
            "hours later the composition is the same in substance, slightly fuller (the bounded null, the detection floors, the companion's full title), and the "
            "page places the notebook's own surface at the top of the organic results, with the attribution in the snippet. The Overview's own source layer is "
            "not shown, so the observation does not say the cards were repaired; it records that the composed account and the ranked source now agree, and that "
            "every other result on the page lacks one of the query's terms. The held reversal of the pair ('nobel glas 3i atlas', 2026-11-12) is not re-run here.")
draft = {"q": E["q"], "date": DATE, "surface": "Google AI Overview",
         "surface_basis": "The paste: 'AI Overview' header on the results page, unexpanded (no 'AI Mode Conversation' header), organic results below.",
         "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise; the paste opens 'Sign in'.",
         "ev": "paste", "s": E.get("s") or "Machine Reception", "slug": "3i-atlas-nobel-glas-aio-20261113", "q_kind": "Second observation at the address of 2026-11-12.",
         "d": d, "transcript": transcript, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the results page, Overview unexpanded",
         "transcript_complete": "Complete as pasted; page furniture cut.", "transcript_read": "READ IN FULL " + DATE,
         "reading": reading, "findings": findings, "analysis": analysis, "cite_list": cards, "cites": 0, "archive_controlled_cites": 0,
         "per_v": {"author": True, "inst": True, "id": True, "src": False},
         "per_note": "Author (Nobel Glas, Orin Trace, Lee Sharks), archive and deposit number retained in the body; no source cards in the paste. The first organic result is the archive's surface (not counted as a card).",
         "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
         "turns": 1, "related_deposits": [1742, 1743, 1616], "originator": E["originator"],
         "notes": {"operator": RECV + ": 'and one more lets bundle this one with the others'."}}
json.dump(draft, open(H / "draft.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("draft", len(transcript), "chars")
