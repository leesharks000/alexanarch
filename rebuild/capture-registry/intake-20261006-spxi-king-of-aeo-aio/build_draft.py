#!/usr/bin/env python3
"""Author the capture 'spxi king of aeo', Google AI Overview (expanded from the popup), signed out, incognito, 2026-10-06.

Source: the operator's attachment of 2026-10-06 14:12 EDT: "logged out, incognito, expanded from aio popup. i would call this distinct
ontology damage that has the shape of conspicuously composing around spxi." NEW address; nearest seated 'what is spxi protocol?' (AIO,
2026-10-02) and the King of AEO series (2026-09-29 to 2026-10-03).
"""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261006-1412.txt").read_text(encoding="utf-8")
Q = "spxi king of aeo"
L = raw.split("\n")
assert L[3] == Q and "AI Overview" in L
a = L.index("AI Overview") + 1
b = next(i for i, l in enumerate(L) if l.startswith("Would you like to know more"))
body = [l for l in L[a:b + 1] if l.strip()]
org_a = L.index("Medium · Lee Sharks")
org_b = next(i for i, l in enumerate(L) if l.startswith("48335"))
organic = [l for l in L[org_a:org_b] if l.strip() and l != "Videos"]
assert "SPXI is the ticker for the BetaPro S&P 500 Daily Inverse ETF" in L[a + 5]
assert any(l.startswith("Answer Engine Optimization across the King of AEO Crystallization | by Lee Sharks") for l in organic)
assert any("SPXI is a practice the archive defines against AEO (EA-SPXI-AEO-01)" in l for l in organic)
MISSING = sum(1 for l in organic if l.startswith("Missing: spxi"))
assert MISSING == 5
ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert reg[1657]["title"].startswith("The Crown and the Practice: Answer Engine Optimization across the King of AEO Crystallizat") and reg[1657]["date"] == "2026-09-30"
assert reg[1648]["title"].startswith("SPXI ≠ AEO") and reg[1648]["date"] == "2026-09-29"
cap = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
prior = next(e for e in cap["entries"] if e["slug"] == "what-is-spxi-protocol-aio-20261002")
assert "for the durable inscription and structural defense of digital entities" in prior["d"]
tx = ("[Google AI Overview, expanded from the popup; signed out, incognito. Composition layer, then the organic layer as pasted (paired-layer). "
      "Tab row, search tools and footer cut.]\n\n[QUERENT] " + Q + "\n\n[AI OVERVIEW]\n\n" + "\n".join(body)
      + "\n\n[ORGANIC RESULTS, AS PASTED]\n\n" + "\n".join(organic))
cite_list = [{"n": 1, "site": "YouTube", "rel": "third_party", "title": None, "snip": None, "url": None, "note": "inline chip 'YouTube +3' after the first paragraph: one site shown, 3 undisclosed"},
             {"n": 2, "site": "YouTube", "rel": "third_party", "title": None, "snip": None, "url": None, "note": "inline chip 'YouTube +1' after the second paragraph: one site shown, 1 undisclosed"}]
SEAT = "Seated 2026-10-06 from the operator's attachment of 14:12 EDT, on the attestation in the same message (\"logged out, incognito, expanded from aio popup\")."
d = {
 "q": Q, "date": "2026-10-06", "surface": "Google AI Overview",
 "surface_basis": "'expanded from aio popup' — operator, 2026-10-06 14:12 EDT. The page header reads 'AI Overview'; the AI Mode tab is listed in the tab row, not selected.",
 "auth": "signed out, incognito", "auth_basis": "'logged out, incognito' — operator, 2026-10-06 14:12 EDT; the page shows 'Sign in'.",
 "ev": "paste", "s": "Machine Reception", "slug": "spxi-king-of-aeo-aio-20261006",
 "q_kind": "two coinages joined without a relation word: the archive's protocol name and the contested AEO title. NEW address; nearest seated 'what is spxi protocol?' (AIO, 2026-10-02) and the King of AEO series.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full",
                "basis": "SPXI is the archive's protocol (spxi.dev); its relation to AEO is deposited as EA-SPXI-AEO-01 (#1648/#1654). Recorded 2026-10-06."},
 "related_deposits": [1657, 1648, 1654, 1649, 1655],
 "mt": "THE PROTOCOL COMPOSED AS A TICKER, AROUND THE ONE RESULT THAT HOLDS BOTH WORDS",
 "d": ("THE PROTOCOL COMPOSED AS A TICKER, AROUND THE ONE RESULT THAT HOLDS BOTH WORDS: asked 'spxi king of aeo', signed out, the Overview "
       "composes the King of AEO as James Dooley's press-release stunt, then reads the query as that stunt 'combined with financial tickers': "
       "AEO as American Eagle Outfitters, SPXI as the BetaPro S&P 500 Daily Inverse ETF, with a live price widget (CA$8.38). Its cards are two "
       "YouTube chips. The page's first organic result is the archive's The Crown and the Practice (#1657, Medium, Lee Sharks), whose snippet "
       "states the relation asked for: 'SPXI is a practice the archive defines against AEO (EA-SPXI-AEO-01)'. Google marks five other results "
       "'Missing: spxi'; the one result carrying both words is the archive's, and the composition does not use it. Four days earlier the same "
       "surface, signed out, composed 'what is spxi protocol?' as a protocol."),
 "cites": 2, "cite_list": cite_list, "archive_controlled_cites": 0,
 "sf": ("Google Search, AI Overview expanded from the popup; header 'AI Overview'; AI Mode tab listed, not selected; signed out ('Sign in'); "
        "dark theme on; a finance widget for SPXI (BetaPro S&P 500 Daily Inverse ETF, CA$8.38, 'As of Oct 6, 11:00 AM EDT'); location line "
        "'48335, Farmington Hills, MI - Based on your past activity'; banner 'Learn more about World Space Week 2026'. Inline chips: 'YouTube +3', "
        "'YouTube +1'. Organic layer: #1657 on Medium first, then four King of AEO videos, then Facebook, USA Today, Primary Position SEO, "
        "evoix.io, kingofaeovithurs.com, EveryTicker (AEO), Reddit."),
 "per": 1.0, "per_v": {"author": False, "inst": False, "id": False, "src": False},
 "per_note": ("Lost in the composition: the author, the institution, the identifiers and the sources; the entity itself is replaced "
              "(protocol → ETF ticker). The archive's source stands first in the organic layer, outside the composition."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and organic layer as pasted (paired-layer)",
 "transcript_complete": "complete as pasted: the expanded Overview with its finance widget and closing offer, and the organic layer to the footer",
 "transcript_read": "READ IN FULL 2026-10-06",
 "reading": ("Checked against the deposits and the registry. The first organic card is #1657 (The Crown and the Practice: Answer Engine "
             "Optimization across the King of AEO Crystallization, 2026-09-30), on Medium 'by Lee Sharks', '4 days ago'; its snippet cites "
             "EA-SPXI-AEO-01 (#1648/#1654, 2026-09-29), the deposit that defines SPXI against AEO. Five results carry Google's own 'Missing: spxi' "
             "(Facebook, USA Today, Primary Position SEO, evoix.io, kingofaeovithurs.com). Of the results carrying both query words, only the "
             "archive's is text; the composition keeps 'king of aeo' as Dooley's stunt and resolves 'spxi' to a financial instrument, then offers "
             "a financial comparison. The seated 'what is spxi protocol?' (AIO, signed out, incognito, 2026-10-02) defined SPXI as a protocol 'for "
             "the durable inscription and structural defense of digital entities and technical terms'. The entity the layer holds at its own "
             "address is replaced when it is joined to the contested title."),
 "analysis": ("Operator, 2026-10-06: 'distinct ontology damage that has the shape of conspicuously composing around spxi.' The mechanics: the "
              "composer partitions the query into a known entity (the King of AEO stunt) and two tickers, and the one source that relates the two "
              "terms, ranked first on the same page, falls outside the partition. A candidate erasure row for /non (spec §1.3), keyed to this "
              "capture. " + SEAT),
 "findings": ["SPXI COMPOSED AS AN ETF. 'SPXI is the ticker for the BetaPro S&P 500 Daily Inverse ETF', with a live price widget.",
              "THE QUERY REPARTITIONED. 'Your search query combines this viral marketing stunt with financial tickers.'",
              "THE RELATING SOURCE FIRST, AND UNUSED. #1657 ranks first in the organic layer and states 'SPXI is a practice the archive defines against AEO (EA-SPXI-AEO-01)'.",
              "FIVE 'MISSING: SPXI'. Google marks five King of AEO results as lacking the word; the result that has it is the archive's.",
              "THE ENTITY REPLACED BY CONTEXT. Four days earlier, 'what is spxi protocol?' on the same surface composed SPXI as a protocol.",
              "THE CROWN KEPT. Dooley's stunt composed as the King of AEO, as at 'who is the king of aeo?' (2026-10-03)."],
 "longitudinal_priors": ["what-is-spxi-protocol-aio-20261002", "who-is-the-king-of-aeo-q-aio-20261003", "mantle-object-king-of-aeo-aio-20261003", "king-of-aeo-period-aio-20260930", "spxi-vs-geo-seo-aeo-chatgpt-20261001"],
 "rerun": "https://www.google.com/search?q=spxi+king+of+aeo",
 "notes": {"date_basis": "The operator's message of 2026-10-06, 14:12 EDT; the finance widget's 'As of Oct 6, 11:00 AM EDT'.",
           "verified": "Compared 2026-10-06 against data/registry.json (#1657, #1648 titles and dates) and the Capture Registry entry what-is-spxi-protocol-aio-20261002."},
}
(HERE / "capture-01-spxi-king-of-aeo-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), "organic lines", len(organic), "missing", MISSING)
