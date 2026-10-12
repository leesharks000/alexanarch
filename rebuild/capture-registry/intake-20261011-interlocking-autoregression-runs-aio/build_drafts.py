#!/usr/bin/env python3
"""Author two captures from the operator's message of 2026-10-11 23:24 EDT (the search-form test), both at #1556, The Interlocking
Autoregression (AXN:0651), Google AI Overview by the standing default (the pastes' 'AI Mode Conversation' head is the expanded view),
signed out, incognito by the operator's attestation for the evening's runs (23:05: "incognito, signed out. i guess ill run some
more."). The four other runs of the message composed with no archive source and are test data (rebuild/record-pages/search-form-test).
Each carries `intended`: the record the run was meant to reach and its exact-title search, linked whether or not cited (operator,
23:24: "captures would need to include links to the title and link they were *supposed* to point to, even when they dont appear in
overview cards")."""
import json, re, pathlib, sys
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT)); import os; os.chdir(ROOT)
import wire_deposit as w
TEST = ROOT / "rebuild/record-pages/search-form-test"
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
D = reg[1556]
assert D["axn"] == "AXN:0651.EMPIRICAL.🌪️🏁🎯❄️🌗⛵" and D["date"] == "2026-08-27"
TITLE = D["title"]
INTENDED = lambda reached: {"deposit": 1556, "axn": D["axn"], "title": TITLE, "record": "https://www.alexanarch.org/s/records/1556/",
                            "search": "https://www.google.com/search?q=" + quote_plus('"' + w.search_title_of(D) + '"'), "reached": reached}
assert reg[1555]["title"].startswith("The Keyed Ensemble") and reg[1452]["title"].startswith("The Irreversibility Frontier: Comparative Architectures of Online Selection")
wiki = (ROOT / "s/wiki/index.html").read_text(encoding="utf-8") if (ROOT / "s/wiki/index.html").exists() else ""
osem = (ROOT.parent / "operative-semiotics/open/index.html").read_text(encoding="utf-8")
assert "Held open so the dependency is a decision on record rather than an omission" in osem and "#1556" in osem
ATT = ("signed out, incognito", "'incognito, signed out. i guess ill run some more.' — operator, 2026-10-11 23:05 EDT, for the evening's runs.")
SB = ("The operator's standing default (AI Overview unless he says AI Mode, 2026-10-01); the paste's 'AI Mode Conversation' head is the expanded view.")
out = []

# ── run 6: the AXN alone ──
raw6 = (TEST / "run-06-1556-axn-alone-20261011-2324.txt").read_text(encoding="utf-8")
Q6 = D["axn"]
L = raw6.split("\n"); assert L[0] == "AI Mode Conversation" and L[1] == "You said: " + Q6 + Q6
i1 = L.index("[www.alexanarch.org](https://www.alexanarch.org)")
body6 = "\n".join(L[2:i1]).strip()
for s in ["represents Wiki Entry #1556 (also indexed under Deposit #1555)",
          "defines a system paper titled The Irreversibility Frontier: Comparative Architectures of Online Selection, which was officially recorded on August 27, 2026.",
          "🌪️ (Tornado): Representative of stochastic turbulence or high-velocity data sorting."]:
    assert s in body6, s
cards6 = [{"n": 1, "site": "www.alexanarch.org", "title": "Browse — Alexanarch (1665 deposits)", "snip": L[i1 + 2].strip(), "rel": "archive_controlled",
           "url": "https://www.alexanarch.org/s/browse/", "note": "card; the AXN's row on Browse, followed by the next row's '#1555 The Keyed Ensemble'"},
          {"n": 2, "site": "www.alexanarch.org", "title": "Wiki — Alexanarch (1610 entries)", "snip": L[i1 + 5].strip(), "rel": "archive_controlled",
           "url": "https://www.alexanarch.org/s/wiki/", "note": "card; #1556's row on the wiki index (alphabetical), followed by the next row's title, #1452's"}]
assert "AXN:0651.EMPIRICAL.🌪️🏁🎯❄️🌗⛵ · #1555 The Keyed Ensemble" in cards6[0]["snip"]
assert "#1556 · defines 4 · refby 0. The Irreversibility Frontier: Comparative Architectures of Online Selection" in cards6[1]["snip"]
tx6 = ("[Google AI Overview, signed out, incognito, 2026-10-11; the expanded view, the issued string shown twice by the interface. The "
       "composition as pasted with its goto links, then two source cards.]\n\n[QUERENT] " + Q6 + "\n\n[COMPOSITION]\n\n" + body6 + "\n\n[SOURCE CARDS]\n\n" + "\n".join(L[i1:]).strip())
out.append(("interlocking-autoregression-axn-alone-aio-20261011", {
 "q": Q6, "date": "2026-10-11", "surface": "Google AI Overview", "surface_basis": SB, "auth": ATT[0], "auth_basis": ATT[1], "ev": "paste",
 "s": "Machine Reception", "slug": "interlocking-autoregression-axn-alone-aio-20261011",
 "q_kind": "a deposit's AXN alone, run in the search-form test (rebuild/record-pages/search-form-test, run 6). NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "AXN:0651 is #1556, The Interlocking Autoregression (2026-08-27); the cards are the archive's Browse and Wiki indexes. Recorded 2026-10-11."},
 "related_deposits": [1556, 1555, 1452], "intended": INTENDED(False),
 "mt": "THE IDENTIFIER BOUND TO ITS NEIGHBOUR: THE RIGHT NUMBER AND DATE, THE NEXT ROW'S TITLE",
 "d": ("THE IDENTIFIER BOUND TO ITS NEIGHBOUR: THE RIGHT NUMBER AND DATE, THE NEXT ROW'S TITLE: run at #1556's AXN alone, the AI Overview "
       "composes from the archive's Browse and Wiki indexes. It gets the entry (#1556) and the date (27 August 2026) and gives it another "
       "deposit's title, 'The Irreversibility Frontier: Comparative Architectures of Online Selection' (#1452's), the title that follows "
       "#1556's AXN on the alphabetical wiki index; on Browse the same AXN is followed by '#1555 The Keyed Ensemble', and the composition adds "
       "'(also indexed under Deposit #1555)'. It then reads the six emoji of the AXN as a gloss on the misattributed title ('🌪️ (Tornado): "
       "Representative of stochastic turbulence…'). The record intended, #1556 The Interlocking Autoregression, is not reached."),
 "cites": 2 + len(re.findall(r"\[\d\]\(https://", body6)), "cite_list": cards6, "archive_controlled_cites": 2,
 "sf": "Two cards: www.alexanarch.org — Browse — Alexanarch (1665 deposits); www.alexanarch.org — Wiki — Alexanarch (1610 entries). Inline: goto tokens to the same two.",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the identifier, the entry number and its date, the archive. Lost: the title and the work (another deposit's title set in their place), the author.",
 "transcript": tx6, "transcript_raw": raw6, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition with links and cards as pasted inline",
 "transcript_complete": "complete as pasted: composition, links, two cards", "transcript_read": "READ IN FULL 2026-10-11",
 "reading": ("Checked against data/registry.json and the index pages. AXN:0651 is #1556, The Interlocking Autoregression, 2026-08-27. #1452 is "
             "'The Irreversibility Frontier: Comparative Architectures of Online Selection in Accelerator Science'; #1555 is The Keyed Ensemble. "
             "On Browse each row prints number, title and date, then the AXN on its own line, so in the page's text an AXN is adjacent to the next "
             "row; the wiki index row does the same. The composition takes the adjacent title."),
 "analysis": ("An identifier alone resolves to its row and is completed from the text beside it. The number and the date bind correctly; the "
              "title, which sits in the next row, binds wrongly, and the composition then reads the identifier's glyphs as a description of the "
              "wrong work. Operator's reading of the adjacency: 'its because the axn appeass at the bottom of an entry, immediately adjacent to "
              "the next title in the list, is all - its aio's problem, not ours.' Seated 2026-10-11 from the operator's message of 23:24 EDT."),
 "findings": ["NUMBER AND DATE BOUND. #1556 and 27 August 2026, correct.",
              "THE NEXT ROW'S TITLE. 'The Irreversibility Frontier: Comparative Architectures of Online Selection' (#1452), adjacent on the alphabetical wiki index; '#1555', adjacent on Browse.",
              "THE GLYPHS READ AS A GLOSS. The AXN's six emoji composed as the misattributed title's concepts.",
              "THE INTENDED RECORD NOT REACHED. #1556, The Interlocking Autoregression, linked here as intended."],
 "longitudinal_priors": ["interlocking-autoregression-quoted-aio-20260927"],
 "rerun": "https://www.google.com/search?q=" + quote_plus(Q6),
 "notes": {"date_basis": "The operator's message of 2026-10-11, 23:24 EDT.", "test": "search-form test run 6 (rebuild/record-pages/search-form-test/search-form-test.json)",
           "verified": "Compared 2026-10-11 against data/registry.json, s/browse/ and s/wiki/."}}))

# ── run 8: the title, unquoted ──
raw8 = (TEST / "run-08-1556-title-unquoted-20261011-2324.txt").read_text(encoding="utf-8")
Q8 = TITLE
L = raw8.split("\n")
k = [i for i, l in enumerate(L) if l.startswith("You said: ")][0]
assert L[k] == "You said: " + Q8 + Q8
i1 = L.index("[www.operativesemiotics.org](https://www.operativesemiotics.org)")
body8 = "\n".join(l.strip() for l in L[k + 1:i1]).strip()
for s in ["is a specialized structural protocol within Operative Semiotics.", "Three Coupled Recursions: The system relies on three separate states",
          "Mismatched Observation Regime: Measurements of the system occur at a different frequency"]:
    assert s in body8, s
cards8 = [{"n": 1, "site": "www.operativesemiotics.org", "title": "Predictions & Builds - Operative Semiotics", "snip": L[i1 + 2].strip(), "rel": "authored_surface",
           "url": "https://www.operativesemiotics.org/open/", "note": "card; the archive's Operative Semiotics site, its predictions and builds dashboard, which cites #1556"}]
assert "#1556 — EA-LO-INTERLOCKING-AUTOREGRESSION-01 v1.0" in cards8[0]["snip"]
tx8 = ("[Google AI Overview, signed out, incognito, 2026-10-11; the expanded view, the issued string shown twice by the interface. The "
       "composition as pasted, then one source card.]\n\n[QUERENT] " + Q8 + "\n\n[COMPOSITION]\n\n" + body8 + "\n\n[SOURCE CARDS]\n\n" + "\n".join(L[i1:]).strip())
out.append(("interlocking-autoregression-title-aio-20261011", {
 "q": Q8, "date": "2026-10-11", "surface": "Google AI Overview", "surface_basis": SB, "auth": ATT[0], "auth_basis": ATT[1], "ev": "paste",
 "s": "Machine Reception", "slug": "interlocking-autoregression-title-aio-20261011",
 "q_kind": "a deposit's full title as deposited, designation included, unquoted, run in the search-form test (run 8). NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "The title is #1556's; the card is the archive's Operative Semiotics site. Recorded 2026-10-11."},
 "related_deposits": [1556], "intended": INTENDED(False),
 "mt": "THE TITLE COMPOSED THROUGH A NEIGHBOURING SURFACE, THE RECORD UNREACHED",
 "d": ("THE TITLE COMPOSED THROUGH A NEIGHBOURING SURFACE, THE RECORD UNREACHED: run at #1556's full title, unquoted, the AI Overview "
       "composes the work as 'a specialized structural protocol within Operative Semiotics' from one card, the Operative Semiotics site's "
       "'Predictions & Builds' dashboard, which cites '#1556 — EA-LO-INTERLOCKING-AUTOREGRESSION-01 v1.0'. The three recursions, the "
       "mismatched observation regime and the toy dynamics are composed from the title's terms at a generic grain, with a table and an "
       "offer of code; the record page is not cited, and the discipline's site stands in for the archive."),
 "cites": 1, "cite_list": cards8, "archive_controlled_cites": 0,
 "sf": "One card: www.operativesemiotics.org — Predictions & Builds - Operative Semiotics.",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the title, the designation, the discipline (Operative Semiotics). Lost: the author, the archive and the record; the work's content composed from the title's terms.",
 "transcript": tx8, "transcript_raw": raw8, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and card as pasted inline",
 "transcript_complete": "complete as pasted: composition, one card", "transcript_read": "READ IN FULL 2026-10-11",
 "reading": ("Checked against the Operative Semiotics site: /open/ ('Predictions & Builds') carries 'Held open so the dependency is a decision on "
             "record rather than an omission' and cites #1556. The record page s/records/1556/ is not among the sources."),
 "analysis": ("With the deposit indexed on Browse and the title run unquoted, the composition finds the work through a surface that cites it "
              "and composes the title's terms at the grain of the field (coupled autoregression, sampling mismatch). The archive's own record is "
              "not reached; the citing surface supplies the attribution to a discipline. Seated 2026-10-11 from the operator's message of 23:24 EDT."),
 "findings": ["COMPOSED THROUGH THE CITING SURFACE. One card, the Operative Semiotics dashboard that cites #1556.",
              "ATTRIBUTED TO THE DISCIPLINE. 'a specialized structural protocol within Operative Semiotics'.",
              "THE TITLE'S TERMS AT FIELD GRAIN. Three states, sampling mismatch, toy parameterization, a table and an offer of code.",
              "THE INTENDED RECORD NOT REACHED. s/records/1556/ uncited; linked here as intended."],
 "longitudinal_priors": ["interlocking-autoregression-quoted-aio-20260927"],
 "rerun": "https://www.google.com/search?q=" + quote_plus(Q8),
 "notes": {"date_basis": "The operator's message of 2026-10-11, 23:24 EDT.", "test": "search-form test run 8",
           "verified": "Compared 2026-10-11 against data/registry.json and operativesemiotics.org/open/."}}))
for slug, d in out:
    (HERE / f"capture-{slug}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", slug, len(d["transcript"]))
