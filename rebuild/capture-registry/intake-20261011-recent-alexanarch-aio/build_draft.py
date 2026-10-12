#!/usr/bin/env python3
"""Author the capture 'recent alexanarch', Google AI Overview, signed out, incognito, 2026-10-11. Source: the operator's attachment of
2026-10-11 22:13 EDT ("signed out, incognito - it prioritize the captures so strongly:"). Surface by the standing default (AI Overview
unless the operator says AI Mode); the paste's head, 'AI Mode Conversation', is the expanded conversation view. NEW address."""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261011-2213.txt").read_text(encoding="utf-8")
Q = "recent alexanarch"
L = raw.split("\n")
assert L[1].strip() == "AI Mode Conversation" and L[4].strip() == "You said: recent alexanarchrecent alexanarch"
i0 = 6; i1 = [i for i, l in enumerate(L) if l.strip() == "www.alexanarch.org"][0]
body = "\n".join(l.strip() for l in L[i0:i1]).strip()
for s in ["founded by digital archivist and researcher Lee Sharks on June 19, 2026",
          "moving past 1,665 total text and research deposits (up from roughly 1,500 in mid-September)",
          "#1660 \"The Seed in the Narrowing Cone\" (October 2, 2026)", "#1659 \"Glyphic Checksum\" (October 1, 2026)",
          "\"Alexanarch:Theophrastus\" (Late 2026): A controversial text-critical thesis published by Lee Sharks",
          "a Capture Registry to record how major LLMs read and interpret its files",
          "In October 2026, algorithmic financial analysis of the venture infrastructure behind Lee Sharks' intellectual property",
          "placed its estimated asset valuation at $1 million to $5 million as an investable meaning-preservation system."]:
    assert s in body, s
end = [i for i, l in enumerate(L) if l.startswith("AI responses may include mistakes")][0]
C = [l.strip() for l in L[i1:end]]
assert len(C) % 3 == 0, len(C)
cards = []
for n, k in enumerate(range(0, len(C), 3), 1):
    site, title, snip = C[k], C[k + 1], C[k + 2]
    cards.append({"n": n, "site": site, "title": title, "snip": snip, "url": "https://www.alexanarch.org" if site == "www.alexanarch.org" else None,
                  "rel": "archive_controlled" if site == "www.alexanarch.org" else "authored_surface" if site == "GitHub" else "third_party", "note": "card"})
assert len(cards) == 11
CAP = {"ChatGPT, 2026-09-27 — Capture Registry (EA-WG- ...": "a capture record (ChatGPT, 2026-09-27)",
       "the last month or so of deposits to alexanarch.org as an evolving system of ...": "last-month-deposits-alexanarch-living-thought-chatgpt-20260927",
       "please estimate the valuation of \"lee sharks\" as emerging meaning ...": "please-estimate-the-valuation-of-lee-sharks-20260910",
       "alexanarch:theophrastus — Google AI Overview, 2026-10": "alexanarch-theophrastus-aio-20261001",
       "\"epic without hero\" — Google AI Overview, 2026-08-13": "epic-without-hero-20260813",
       "glyphic checksum — Google AI Overview, 2026-10-01": "glyphic-checksum-aio-20261001"}
for c in cards:
    if c["title"] in CAP: c["note"] = "card; a Capture Registry record: " + CAP[c["title"]]
ncap = sum(1 for c in cards if c["title"] in CAP)
assert ncap == 6
caps = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
for v in list(CAP.values())[1:]:
    assert v in caps, v
assert caps["alexanarch-theophrastus-aio-20261001"]["q"] == "alexanarch:theophrastus"
PX = json.dumps(caps["please-estimate-the-valuation-of-lee-sharks-20260910-02ef91"], ensure_ascii=False)
assert "worth roughly $1–5 million as an investable venture asset" in PX and "SPXI, MPAI, Holographic Kernel, and UKTP" in PX
assert caps["please-estimate-the-valuation-of-lee-sharks-20260910-02ef91"]["date"] == "2026-09-10" and caps["please-estimate-the-valuation-of-lee-sharks-20260910-02ef91"]["surface"] == "Perplexity"
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert reg[1659]["date"] == "2026-10-01" and reg[1659]["title"].startswith("GLYPHIC CHECKSUM")
assert reg[1660]["date"] == "2026-10-02" and max(reg) >= 1675
assert not any((x.get("title") or "").lower().startswith("alexanarch:theophrastus") for x in reg.values())
tx = ("[Google AI Overview, signed out, incognito, 2026-10-11 (operator); the paste is the expanded conversation view, headed 'AI Mode "
      "Conversation', the issued string shown twice by the interface. The composition as pasted; eleven source cards follow, as data.]\n\n"
      "[QUERENT] " + Q + "\n\n[COMPOSITION]\n\n" + body + "\n\n[SOURCE CARDS]\n\n" + "\n".join(f"{c['n']}. {c['site']} — {c['title']} — {c['snip']}" for c in cards))
SEAT = "Seated 2026-10-11 from the operator's attachment of 22:13 EDT, on the attestation in the same message (\"signed out, incognito\")."
d = {"q": Q, "date": "2026-10-11", "surface": "Google AI Overview",
 "surface_basis": "The operator's standing default (AI Overview unless he says AI Mode, 2026-10-01); the paste's 'AI Mode Conversation' head is the expanded view.",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito' — operator, 2026-10-11 22:13 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "recent-alexanarch-aio-20261011",
 "q_kind": "the archive's name with a recency word. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Alexanarch is the archive; ten of the eleven cards are its pages. Recorded 2026-10-11."},
 "related_deposits": [1659, 1660],
 "mt": "THE ARCHIVE'S RECENT WORK COMPOSED FROM THE REGISTRY OF ITS RECEPTION",
 "d": ("THE ARCHIVE'S RECENT WORK COMPOSED FROM THE REGISTRY OF ITS RECEPTION: asked for recent alexanarch, the AI Overview cites "
       "eleven cards, ten of them alexanarch.org pages and six of those Capture Registry records (a ChatGPT capture of 2026-09-27, the "
       "last-month reading of the same date, the valuation address, 'alexanarch:theophrastus', '\"epic without hero\"', 'glyphic checksum'). "
       "Two deposits are composed at their dates (#1660, #1659). A capture's address enters as a work: '\"Alexanarch:Theophrastus\" (Late "
       "2026): A controversial text-critical thesis published by Lee Sharks'; the deposits that hold the thesis are not named. A capture's "
       "machine answer enters as an event: Perplexity's estimate at the valuation address on 2026-09-10 ('roughly $1–5 million as an "
       "investable venture asset'; 'SPXI, MPAI, Holographic Kernel, and UKTP') is composed as 'In October 2026, algorithmic financial "
       "analysis … placed its estimated asset valuation at $1 million to $5 million'. The count is the Browse card's '1,665', ten behind "
       "the registry. Operator's reading: 'it prioritize the captures so strongly.'"),
 "cites": len(cards), "cite_list": cards, "archive_controlled_cites": sum(1 for c in cards if c["rel"] == "archive_controlled"),
 "sf": "Eleven cards: " + "; ".join(f"{c['site']} — {c['title']}" for c in cards) + f". Of the ten alexanarch.org cards, {ncap} are Capture Registry records.",
 "per": 0.5, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the founder and founding date, the institution, two deposits by number and date. Lost: the deposits behind the Theophrastus thesis (a capture address set in their place) and the provenance of the valuation (a machine answer at a seated address, re-dated).",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and source cards as pasted",
 "transcript_complete": "complete as pasted: composition, eleven cards", "transcript_read": "READ IN FULL 2026-10-11",
 "reading": ("Checked against data/registry.json and the Capture Registry. #1659 'GLYPHIC CHECKSUM — Transmission · Division · Recollection' "
             "(2026-10-01) and #1660 (2026-10-02) are composed at their dates. No deposit is titled 'Alexanarch:Theophrastus'; the string is the "
             "address of the capture alexanarch-theophrastus-aio-20261001. The valuation figures and the four protocols are Perplexity's answer "
             "in please-estimate-the-valuation-of-lee-sharks-20260910-02ef91 (2026-09-10). The registry stands at 1,675 deposits; the live "
             "Browse page reads '1675 deposits', the card '1665'."),
 "analysis": ("For a recency query the registry is the archive's most recent-looking surface: its record pages carry the query, a date and a "
              "dense reading, and six of ten archive cards are records of compositions. The composition then takes the records' contents "
              "for the archive's: an address becomes a published thesis and a machine estimate becomes a dated analysis of the venture. "
              "The deposits themselves enter only through the Browse and Search cards. Operator's reading, given with the capture: 'it "
              "prioritize the captures so strongly.' " + SEAT),
 "findings": [f"THE REGISTRY FOREGROUNDED. {ncap} of the ten alexanarch.org cards are Capture Registry records.",
              "A CAPTURE ADDRESS COMPOSED AS A WORK. '\"Alexanarch:Theophrastus\" (Late 2026): A controversial text-critical thesis published by Lee Sharks'; no deposit carries that title.",
              "A MACHINE ANSWER COMPOSED AS AN EVENT. Perplexity's estimate of 2026-09-10 composed as 'In October 2026, algorithmic financial analysis … placed its estimated asset valuation at $1 million to $5 million'.",
              "TWO DEPOSITS AT THEIR DATES. #1660 (2 October) and #1659 (1 October).",
              "THE COUNT FROM A STALE CARD. '1,665 total' from the Browse card; the registry holds 1,675."],
 "longitudinal_priors": ["alexanarch-on-model-collapse-aio-20261010"],
 "rerun": "https://www.google.com/search?q=recent+alexanarch",
 "notes": {"date_basis": "The operator's message of 2026-10-11, 22:13 EDT.", "operator_reading": "it prioritize the captures so strongly",
           "verified": "Compared 2026-10-11 against data/registry.json, data/EA-WG-CAPTURES-01.json and s/browse/index.html."}}
(HERE / "capture-01-recent-alexanarch-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cards), ncap)
