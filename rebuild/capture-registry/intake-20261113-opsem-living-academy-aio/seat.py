"""Seat of 2026-11-13 (received 13:45 EST): two Google AI Overviews, signed out and incognito (each page shows 'Sign in'), both NEW addresses, each
with screenshots of the same page (13:43-13:44 EST).
  1. "operative semiotics predictions"   (paste; screenshots 1-2)
  2. "alexanarch living academy"         (paste; screenshots 1-6)
The pastes carry no source cards (operator, 13:07: select-all now takes the organic results), and the screenshots stop before the cards. Every quotation
is asserted against the paste and against the record or surface it composes from.   python3 seat.py
"""
import json, pathlib, re, html
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-13"; RECV = "2026-11-13 13:45 EST"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n): return (ROOT / REG[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
def flat(p): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", pathlib.Path(p).read_text(encoding="utf-8"))))
OPS = "/home/claude/fleet/operative-semiotics"
SB = "The paste: 'AI Overview' header on the results page, the Overview expanded inline (operator, 2026-11-13 13:07 EST); the screenshots show it."
AB = "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise; the page shows 'Sign in'."
PEND = {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False}
def body(raw): return raw[raw.index("AI Overview\n") + len("AI Overview\n"):raw.index("Ask anything")].strip()
def card(site, rel, title, note, **kw): return dict({"site": site, "rel": rel, "url": None, "title": title, "snip": None, "note": note}, **kw)
drafts = []
def entry(slug, q, raw, tr, imgs, mt, d, reading, findings, analysis, per_v, per_note, origin, rel, cards, notes):
    for p in imgs: assert (ROOT / p).exists(), p
    for i, c in enumerate(cards): c["n"] = i + 1
    assert analysis != reading
    return {"slug": slug, "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"], "surface_basis": SB, "auth": "signed out, incognito",
            "auth_basis": AB, "ev": "paste + frame", "s": "Machine Reception", "q": q, "q_kind": "NEW address.", "turns": 1, "mt": mt,
            "cites": len(cards), "archive_controlled_cites": sum(1 for c in cards if c["rel"] in ("archive", "archive_controlled")), "cite_list": cards,
            "imgs": imgs, "img_urls": ["https://www.alexanarch.org/" + p for p in imgs],
            "transcript": tr, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the results page, Overview expanded inline, with screenshots",
            "transcript_complete": "Complete as pasted; the source cards are in neither the paste nor the screenshots.", "transcript_read": f"READ IN FULL {DATE}",
            "d": d, "reading": reading, "findings": findings, "analysis": analysis, "per_v": per_v, "per_note": per_note, "per_dim_pending": PEND,
            "originator": origin, "related_deposits": rel, "notes": notes}
def head(imgs, extra): return ("[Google AI Overview on the results page, expanded inline, signed out and incognito (the page shows 'Sign in'). Received " + RECV
       + " as an attachment, with screenshots of the same page: " + ", ".join(imgs) + ". " + extra + " The source cards are in neither the paste nor the screenshots.]")

# ------------------------------------------------------------- 1. operative semiotics predictions
q1 = "operative semiotics predictions"
raw = (H / "paste-opsem.txt").read_text(encoding="utf-8"); b = body(raw)
IM1 = [f"data/captures-images/operative-semiotics-predictions-aio-20261113-{i}.png" for i in (1, 2)]
P = {"open": "Operative Semiotics treats signs not as static objects of interpretation, but as interventions and operational tools that transform substrates, knowledge graphs, and AI/retrieval layers.",
     "prog": "Its research program features pre-registered predictions, quantitative metrics, and testable protocols outlined in the Operative Semiotics Archive.",
     "sim": "AI-Text Detector Co-Evolution (Simulation EA-SEI-RCS-SIM-01):",
     "num": "simulating a baseline shift from ~0.9% to 43% by generation 4 and ~100% by generation 8",
     "pv": "Certified corpora produced under detector screening are predicted to show measured surface-novelty statistics (such as burstiness and perplexity variance) at or above matched historical baselines within a few enforcement years.",
     "flat": "Models predicting that tail-distinction loss on evaluation panels compounds from the demand side (as users stop querying what the layer cannot answer, contracting the query and evaluation distributions).",
     "head": "Ontological Flattening & Retract DYNAMICS:", "per": "A quantitative metric tracking authorial dissolution and identity governance",
     "index": "Explore the full methodology and test protocols via the Operative Semiotics Open Research Index.",
     "o1": "Predictions & Builds - Operative Semiotics", "sigil": "Johannes Sigil writes under the sign of operative semiotics. Lee Sharks provides the Semantic Economy framework."}
for k, v in P.items(): assert v in raw, k
assert "Sharks" not in b and "Sigil" not in b and "Crimson" not in b and "Alexanarch" not in b
T1540 = text(1540); OPEN = flat(OPS + "/open/index.html"); FLAT = flat(OPS + "/papers/flattening/index.html")
S = {"num": "rises from 0.9% under the generation-zero detector to 43% by generation 4 and saturates at approximately 100% from generation 8 onward",
     "file": "certified-center-sim-EA-SEI-RCS-SIM-01.py", "pre": "running successive versions of the leading commercial detectors against a fixed pre-2022 human corpus"}
for k, v in S.items(): assert v in T1540, k
O = {"pv": "Certified corpora produced under detector screening will show measured surface-novelty statistics (burstiness, perplexity variance) at or above matched historical baselines within a few enforcement years — the performed-variance transient.",
     "pre": "Experimental predictions — pre-registered", "count": "46 registered, 44 live"}
for k, v in O.items(): assert v in OPEN, k
F = "And it compounds from the demand side: people stop asking what the layer cannot answer, so the query distribution contracts, so the evaluation set contracts, so the target narrows again."
assert F in FLAT
tr1 = head(IM1, "The body's links: 'pre-registered predictions' (highlighted), 'Operative Semiotics Archive' and 'Operative Semiotics Open Research Index', and a link chip "
           "after each of five paragraphs (screenshots 1-2), marked [link chip].") + "\n\n[QUERENT] " + q1 + "\n\n[SYSTEM] " + b \
      + "\n\n[ORGANIC RESULTS] " + raw[raw.index("operativesemiotics.org\nhttps"):raw.index("Videos\nAn Introduction")].strip()
reading1 = ("The innocent reading first, in full: asked for the discipline's predictions, the Overview defines operative semiotics and lists four of its "
            "registered predictions and measures, as a fair summary of a research program would. Each is the archive's, at grain. The detector co-evolution "
            "carries the simulation's file name and its three numbers ('" + P["num"] + "'; #1540: '" + S["num"] + "', the attached '" + S["file"] + "'). The "
            "performed-variance transient is the /open/ dashboard's prediction nearly word for word ('" + O["pv"] + "'). The flattening line is the flattening "
            "paper's demand-side clause ('" + F + "'). The program is described as the dashboard describes itself, pre-registered. No person is named in the "
            "Overview: not Lee Sharks, not Johannes Sigil, not the archive. Its links go to the discipline's own surfaces, 'Operative Semiotics Archive' and "
            "'Operative Semiotics Open Research Index', and the first three organic results are operativesemiotics.org twice and the discipline's GitHub "
            "repository; the author's name reaches the page only in a crimsonhexagonal.org snippet sixth.")
f1 = ["THE DISCIPLINE, UNSIGNED. '" + P["open"] + "' '" + P["prog"] + "'",
      "THE SIMULATION BY ITS FILE NAME AND NUMBERS. '" + P["sim"] + "' … '" + P["num"] + "'. #1540: '" + S["num"] + "'; '" + S["file"] + "'.",
      "THE DASHBOARD'S PREDICTION. '" + P["pv"] + "' /open/: '" + O["pv"] + "'",
      "THE FLATTENING PAPER'S CLAUSE, UNDER A GARBLED HEAD. '" + P["head"] + "' '" + P["flat"] + "' Paper: '" + F + "'",
      "PER. '" + P["per"] + " …'.",
      "LINKS TO THE DISCIPLINE'S SURFACES. 'Operative Semiotics Archive'; '" + P["index"] + "' Organic 1: '" + P["o1"] + "'. The author appears sixth, in a crimsonhexagonal.org snippet: '" + P["sigil"] + "'"]
analysis1 = ("The basin is uncontested: operative semiotics as a discipline with registered predictions exists only in the archive's surfaces, and the composition "
             "has no other source to assign it to. In that basin unattributed fine-grain composition places the work rather than taking it, and the page bears "
             "this out: every link and the first three results lead to the discipline's own sites. The Overview attributes to the discipline, not its author, so "
             "the discipline's name now carries the work by itself, which is what an operative sign is built to do. The one loss is resolution in a heading: "
             "'Ontological Flattening & Retract DYNAMICS' fuses two items of the dashboard into one.")
drafts.append(entry("operative-semiotics-predictions-aio-20261113", q1, raw, tr1, IM1,
    "'OPERATIVE SEMIOTICS PREDICTIONS' ON AI OVERVIEW, SIGNED OUT — FOUR REGISTERED PREDICTIONS AT GRAIN, UNSIGNED, LINKED TO THE DISCIPLINE'S OWN SURFACES",
    "'OPERATIVE SEMIOTICS PREDICTIONS', SIGNED OUT, 2026-11-13: the discipline defined and four of its measures given at grain — the detector co-evolution simulation by file name and numbers (#1540: 0.9%, 43% by generation 4, ~100% from generation 8), the performed-variance transient in the /open/ dashboard's words, the flattening paper's demand-side clause, PER — with no person named; links to the 'Operative Semiotics Archive' and the 'Open Research Index'; operativesemiotics.org first and second organic.",
    reading1, f1, analysis1, {"author": False, "inst": True, "id": True, "src": True},
    "No person named; the discipline's archive and index named and linked (operativesemiotics.org), the simulation's identifier EA-SEI-RCS-SIM-01 given; source cards not shown.",
    {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full", "basis": "Operative semiotics (operativesemiotics.org; /open/ predictions; #1540), Crimson Hexagonal Archive. Recorded " + DATE + "."},
    [1540, 1616],
    [card("operativesemiotics.org", "authored_surface", "Operative Semiotics Archive", "body link (screenshot 1); target by name"),
     card("link chip", "unresolved", None, "after the opening paragraph (screenshot 1)"),
     card("link chip", "unresolved", None, "after the detector co-evolution item (screenshots 1-2)"),
     card("link chip", "unresolved", None, "after the performed-variance item (screenshot 2)"),
     card("link chip", "unresolved", None, "after the flattening item (screenshot 2)"),
     card("link chip", "unresolved", None, "after the PER item (screenshot 2)"),
     card("operativesemiotics.org", "authored_surface", "Operative Semiotics Open Research Index", "body link (screenshot 2); target by name, the /open/ index")],
    {"operator": RECV + ": 'and two captures.'"}))

# ------------------------------------------------------------- 2. alexanarch living academy
q2 = "alexanarch living academy"
raw = (H / "paste-living-academy.txt").read_text(encoding="utf-8"); b = body(raw)
IM2 = [f"data/captures-images/alexanarch-living-academy-aio-20261113-{i}.png" for i in range(1, 7)]
L = {"open": "The Living Academy is a conceptual \"mantle\" (a specified title and evaluation framework) constituted on October 13, 2026, within Alexanarch, a self-governing digital library founded by Lee Sharks on June 19, 2026.",
     "fn": "operates across 17 distinct technical and scholarly functions—plus their integration as an 18th—on a single deposit registry using content-derived AXN identifiers",
     "mpai": "documented in Metadata Packet EA-MPAI-ALEXANARCH-01", "pair": "It is paired with a sister mantle, the Arch-Philosopher",
     "rest": "the Restored Academy (an internal heteronymic institution attributed to Johannes Sigil)",
     "four": "four distinct dimensions (which are never averaged into a single score)", "lc": "governed by criteria LC-01 through LC-12",
     "eight": "a program is examined across eight modes", "spec": "the packet explicitly notes that the title is specified, not determined",
     "rivals": "rival research programs (such as AI Now, Data & Society, or AlgorithmWatch)",
     "gov": "Because Alexanarch was founded in mid-2026 and is operated by a single individual, its external peer review, outside reproduction, and long-term institutional adoption remain unestablished.",
     "o1": "Concepts in this composition. Living Academy (Lee Sharks, #1680): A mantle constituted by the Crimson Hexagonal Archive (2026-10-13)"}
for k, v in L.items(): assert v in raw, k
T78 = text(1678); T80 = text(1680)
R = {"fd": "founded by Lee Sharks on 2026-06-19", "seventeen": "Alexanarch is one library with seventeen functions on one deposit registry and identifier spine",
     "rest": "the Restored Academy, Johannes Sigil's heteronym institution", "spec": "Specified, not determined; paired with the Arch-Philosopher",
     "one": "Founded 2026-06-19; one operator; no external peer review of deposits."}
for k, v in R.items(): assert v in T80, k
assert "| historical_depth |" in T80 and "| historical_depth |" not in T78
assert "LC-16" in T80 and "LC-13" not in T78 and "Extent, longitudinality, historical depth, critical quality and integration are reported separately" in T80
assert REG[1678]["status"] == "SUPERSEDED" and REG[1680]["status"] == "ACTIVE"
tr2 = head(IM2, "The body's links: 'Alexanarch' (twice) and 'Metadata Packet EA-MPAI-ALEXANARCH-01', and link chips after the opening paragraph and the first two "
           "entities (screenshots 1-3), marked [link chip].") + "\n\n[QUERENT] " + q2 + "\n\n[SYSTEM] " + b \
      + "\n\n[ORGANIC RESULTS] " + raw[raw.index("alexanarch.org\nhttps"):raw.index("crimsonhexagonal.org\nhttps")].strip()
reading2 = ("The innocent reading first, in full: asked for the Living Academy by the library's name, the Overview reads the mantle object and reports it, with "
            "its own caveats, as a careful summary would. Its facts are the record's: the date of constitution, the library 'founded by Lee Sharks on 2026-06-19', "
            "the seventeen functions and their joins as the eighteenth ('" + R["seventeen"] + "'), the pairing with the Arch-Philosopher, the Restored Academy as "
            "'" + R["rest"] + "', the eight modes, 'specified, not determined'. Its caveats are the record's own disclosures re-filed ('" + R["one"] + "' becomes '"
            + L["gov"] + "'). Its frame is not the current record's. The Overview gives '" + L["four"] + "' and '" + L["lc"] + "': the four dimensions and twelve "
            "criteria of v0.4, #1678, now superseded. #1680, v0.5, the active record, reports five dimensions, adding historical depth, and runs its criteria to "
            "LC-16. The first organic result is the archive's capture page citing #1680 by number.")
f2 = ["THE OBJECT BY ITS RECORD'S FACTS. '" + L["open"] + "' #1680: '" + R["fd"] + "'.",
      "THE FUNCTIONS. '" + L["fn"] + "' #1680: '" + R["seventeen"] + "'.",
      "THE DISTINCTIONS. '" + L["pair"] + "'; '" + L["rest"] + "'. #1680: '" + R["spec"] + "'; '" + R["rest"] + "'.",
      "THE SUPERSEDED FRAME. '" + L["four"] + "'; '" + L["lc"] + "'. #1678 (v0.4, SUPERSEDED): four dimensions, LC-01–LC-12. #1680 (v0.5, ACTIVE): extent, longitudinality, historical depth, critical quality, integration; criteria to LC-16.",
      "THE RECORD'S DISCLOSURES AS CAVEATS. '" + L["spec"] + "'; '" + L["gov"] + "' #1680: '" + R["one"] + "' Rivals named as comparators: '" + L["rivals"] + "'.",
      "SOURCES. Body links 'Alexanarch' (twice) and '" + L["mpai"] + "'; link chips (screenshots 1-3); no cards shown. Organic 1, alexanarch.org: '" + L["o1"] + " …'."]
analysis2 = ("Attributed, institutional and at grain, with one displacement in time. The Overview reads the mantle object as v0.4 had it, so the dimension v0.5 "
             "added, historical depth, and the four criteria after LC-12 are absent from what a reader is told the framework is; the version notice that "
             "supersedes #1678 has not reached the composition. The record's own limits arrive intact and are presented as the composer's caveats, which is "
             "accurate in substance: the library's disclosure that it has one operator and no external review is carried as the reason its status is "
             "unestablished. Compare the ChatGPT capture of 2026-10-14 at 'what is the living academy mantle object?', which read #1680 and reported five "
             "dimensions apart.")
drafts.append(entry("alexanarch-living-academy-aio-20261113", q2, raw, tr2, IM2,
    "'ALEXANARCH LIVING ACADEMY' ON AI OVERVIEW, SIGNED OUT — THE MANTLE OBJECT AT GRAIN AND ATTRIBUTED, IN THE FRAME OF ITS SUPERSEDED VERSION (#1678): FOUR DIMENSIONS, LC-01–LC-12",
    "'ALEXANARCH LIVING ACADEMY', SIGNED OUT, 2026-11-13: the Living Academy composed from the mantle object by date, library, founder ('founded by Lee Sharks on June 19, 2026'), seventeen functions and their joins, the Arch-Philosopher, the Restored Academy, eight modes and 'specified, not determined'; the dimensions and criteria of v0.4 (#1678, superseded: four, LC-01–LC-12) where the active v0.5 (#1680) has five and LC-16; the record's own disclosures re-filed as caveats; alexanarch.org first organic.",
    reading2, f2, analysis2, {"author": True, "inst": True, "id": True, "src": True},
    "Lee Sharks, Alexanarch and the Crimson Hexagonal Archive named; EA-MPAI-ALEXANARCH-01 named and linked; 'Alexanarch' linked; source cards not shown.",
    {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": "The Living Academy (#1680, superseding #1678), Crimson Hexagonal Archive. Recorded " + DATE + "."},
    [1680, 1678, 1679, 1656],
    [card("link chip", "unresolved", None, "after the opening paragraph (screenshots 1-2)"),
     card("alexanarch.org", "archive", "Alexanarch", "body link in the opening paragraph and again under Core Entities (screenshot 2); target by name"),
     card("link chip", "unresolved", None, "after the Alexanarch entity (screenshot 2)"),
     card("link chip", "unresolved", None, "after the Semantic Economy entity (screenshots 2-3)"),
     card("metadatapacket.dev", "authored_surface", "Metadata Packet EA-MPAI-ALEXANARCH-01", "body link (screenshot 3); target by name", deposit_candidates=[1680, 1678])],
    {"operator": RECV + ": 'and two captures.'"}))

for e in drafts:
    json.dump(e, open(H / f"draft-{e['slug']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(e["slug"], e["cites"], "cites;", len(e["transcript"]), "chars")
