#!/usr/bin/env python3
"""Author the capture 'money alexanarch', Google AI Overview, signed out, incognito, 2026-10-12. Source: the operator's message of 01:02
EDT ("aio is perfectly capable of decent summarization. it is prevented from doing so:" with the composition pasted inline), attested
at 01:03 ("signed out and incognito"). Surface by the standing default; the paste's 'AI Mode Conversation' head is the expanded view.
NEW address."""
import json, re, pathlib
from urllib.parse import quote_plus
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261012-0102.txt").read_text(encoding="utf-8")
Q = "money alexanarch"
L = raw.split("\n")
assert L[0] == "AI Mode Conversation" and L[1] == "You said: " + Q + Q
i1 = raw.index("[www.alexanarch.org](https://www.alexanarch.org)\ndebt/creditor inversion")
body = raw[raw.index(L[1]) + len(L[1]):i1].strip(); ct = raw[i1:]
for s in ["the true \"creditor\" of economic value is not a banking institution, but rather the underlying archive of shared meaning itself",
          "papers like Substrate Sovereignty analyze money as a semantic inscription", "technical protocols (such as `EA-MSAL-01`)", "\"semantic remainders\""]:
    assert s in body, s
spec = [("www.alexanarch.org", "debt/creditor inversion — Google AI Overview, 2026-08", "Aug 14, 2026 — **ADDRESS:** `debt/creditor inversion` (unquoted) **AI OVERVIEW:** The **debt/creditor inversion** is a foundational axiom in the conceptual framework of the \"S...",
         "https://www.alexanarch.org/captures/debt-creditor-inversion-20260814/", "archive_controlled", "card; a Capture Registry record: debt-creditor-inversion-20260814"),
        ("www.alexanarch.org", "Browse — Alexanarch (1665 deposits)", "Oct 5, 2026 — recently deposited AXN:06AE.EMPIRICAL.🔼◇🪝⏫◀️🌾 #1619 Monetary Substrate Audit Ledger: Protocol for Auditing Monetary Inscription, Settlement, and Semantic Rem...",
         "https://www.alexanarch.org/s/browse/", "archive_controlled", "card; the AXN printed before #1619 is #1620's (AXN:06AE), from the row above"),
        ("www.alexanarch.org", "lee sharks money form — Google AI Overview, 2026-09-21 - Alexanarch", "Sep 21, 2026 — The composition states the debt/creditor inversion accurately -- all money is debt, debt presupposes meaning, meaning as creditor -- and offers ...",
         "https://www.alexanarch.org/captures/lee-sharks-money-form-aio-20260921/", "archive_controlled", "card; a Capture Registry record: lee-sharks-money-form-aio-20260921"),
        ("www.alexanarch.org", "Alexanarch", "Alexanarch Alexanarch is a sovereign digital archive. It holds works across all substrates — poetry, essays, criticism, correspondence, datasets, novels, disser...",
         "https://www.alexanarch.org", "archive_controlled", "card; the home page")]
cl = []
for n, (site, title, snip, url, rel, note) in enumerate(spec, 1):
    assert title in ct and snip[:60] in ct, title
    cl.append({"n": n, "site": site, "title": title, "snip": snip, "url": url, "rel": rel, "note": note})
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert not any(e["q"] == Q for e in caps["entries"])
S = {e["slug"] for e in caps["entries"]}
assert {"debt-creditor-inversion-20260814", "lee-sharks-money-form-aio-20260921"} <= S
assert reg[1619]["axn"].startswith("AXN:06AC") and reg[1620]["axn"].startswith("AXN:06AE.EMPIRICAL") and "EA-MSAL-01" in reg[1619]["title"]
assert reg[1617]["title"].startswith("Substrate Sovereignty: Money, the Semantic Commodity Form, and the Meaning Layer")
assert reg[531]["creator"] == "Rex Fraction" and "monetary debt is ontologically downstream from semantic capital" in reg[531]["description"]
assert "Lee Sharks" not in body and "Rex Fraction" not in body
inline = len(re.findall(r"\[\d\]\(https://", body))
OPR = "aio is perfectly capable of decent summarization. it is prevented from doing so"
tx = ("[Google AI Overview, signed out, incognito, 2026-10-12 (operator, 01:03 EDT); the expanded conversation view, headed 'AI Mode "
      "Conversation', the issued string shown twice by the interface. The composition as pasted with its inline links, then four source cards.]\n\n"
      "[QUERENT] " + Q + "\n\n[COMPOSITION]\n\n" + body + "\n\n[SOURCE CARDS]\n\n" + "\n".join(f"{c['n']}. {c['site']} — {c['title']} — {c['snip']}" for c in cl))
d = {"q": Q, "date": "2026-10-12", "surface": "Google AI Overview",
 "surface_basis": "The operator's standing default (AI Overview unless he says AI Mode, 2026-10-01); the paste's 'AI Mode Conversation' head is the expanded view.",
 "auth": "signed out, incognito", "auth_basis": "'signed out and incognito' — operator, 2026-10-12 01:03 EDT.",
 "ev": "paste", "s": "Semantic Economy", "slug": "money-alexanarch-aio-20261012",
 "q_kind": "a topic word with the archive's name. NEW address; priors at the topic: debt-creditor-inversion-20260814, lee-sharks-money-form-aio-20260921 (both cited as cards).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                "basis": "The Semantic Economy's account of money is the archive's: #531 (Rex Fraction), #1617, #1619 (Lee Sharks). Recorded 2026-10-12."},
 "related_deposits": [531, 1617, 1619, 1620],
 "mt": "THE ARCHIVE'S ACCOUNT OF MONEY SUMMARIZED WELL, FROM THE RECORDS OF ITS EARLIER SUMMARIES",
 "d": ("THE ARCHIVE'S ACCOUNT OF MONEY SUMMARIZED WELL, FROM THE RECORDS OF ITS EARLIER SUMMARIES: at 'money alexanarch' the AI Overview "
       "composes the Semantic Economy's account of money in three tenets, each accurate at the archive's grain: the debt/creditor "
       "inversion (money created as debt, debt resting on shared meaning, 'the underlying archive of shared meaning itself' as creditor; "
       "#531's thesis), the semantic commodity form ('papers like Substrate Sovereignty analyze money as a semantic inscription'; #1617), "
       "and monetary substrate auditing ('EA-MSAL-01', 'semantic remainders'; #1619). All four cards are the archive's, and two of them "
       "are Capture Registry records of earlier compositions at the topic ('debt/creditor inversion', 14 August; 'lee sharks money form', "
       "21 September); the others are the Browse page and the home page. No author is named. The Browse card's AXN is #1620's, printed at "
       "the foot of the row above #1619. Operator's reading: '" + OPR + ".'"),
 "cites": inline + len(cl), "cite_list": cl, "archive_controlled_cites": len(cl),
 "sf": "Four cards, all www.alexanarch.org: two Capture Registry records (debt/creditor inversion, 2026-08-14; lee sharks money form, 2026-09-21), Browse, the home page. Inline: " + str(inline) + " numbered citations; the opening name-link to the archive.",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": True, "src": True},
 "per_note": "Retained: the archive, the three positions at grain, one paper by title (Substrate Sovereignty), one protocol by designation (EA-MSAL-01). Lost: the authors (Rex Fraction, Lee Sharks), the deposit numbers.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition with links and cards as pasted inline",
 "transcript_complete": "complete as pasted: composition, inline links, four cards", "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Checked against the registry and the Capture Registry. #531 (Γ_Asset-040, Rex Fraction) argues 'that monetary debt is "
             "ontologically downstream from semantic capital'; #1617 is 'Substrate Sovereignty: Money, the Semantic Commodity Form, and the "
             "Meaning Layer'; #1619 is the Monetary Substrate Audit Ledger (EA-MSAL-01), for 'Monetary Inscription, Settlement, and Semantic "
             "Remainder'. The sentence 'money writes economic claims, while the semantic economy dictates what those claims actually owe' "
             "is the composition's, not located in #1617. The Browse card's 'AXN:06AE.EMPIRICAL' is #1620's (Monetary Substrate Audit 001); "
             "#1619 is AXN:06AC."),
 "analysis": ("Where the cards carry composed prose, the composition is accurate and dense: the capture records hold the earlier "
              "Overviews' statements of the inversion, and the composition restates them, adds the paper and the protocol from the Browse "
              "row, and keeps the three positions distinct. The same evening's title runs, which reached only listing rows, composed from "
              "the title. Operator's reading, given with the capture: '" + OPR + ".' Seated 2026-10-12 from the operator's message of 01:02 "
              "EDT, attested at 01:03."),
 "findings": ["SUMMARIZED AT GRAIN. The inversion, the semantic commodity form, the audit protocol — each accurate.",
              "FROM THE REGISTRY. Two of four cards are capture records of earlier compositions at the topic.",
              "NAMED BY PAPER AND PROTOCOL. 'Substrate Sovereignty' (#1617) and 'EA-MSAL-01' (#1619).",
              "NO AUTHOR. Rex Fraction (#531) and Lee Sharks (#1617, #1619) absent.",
              "THE NEIGHBOUR'S AXN ON THE CARD. 'AXN:06AE.EMPIRICAL' before #1619 is #1620's."],
 "longitudinal_priors": ["debt-creditor-inversion-20260814", "lee-sharks-money-form-aio-20260921"],
 "rerun": "https://www.google.com/search?q=" + quote_plus(Q),
 "notes": {"date_basis": "The operator's messages of 2026-10-12, 01:02 and 01:03 EDT.", "operator_reading": OPR,
           "verified": "Compared 2026-10-12 against data/registry.json (#531, #1617, #1619, #1620) and data/EA-WG-CAPTURES-01.json."}}
(HERE / "capture-money-alexanarch-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", inline, len(cl))
