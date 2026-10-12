#!/usr/bin/env python3
"""Author the capture '"Erratum — The Missing Translator: Max Hidalgo Nácher, Ricardo Reis, and AXN:F154"', Google AI Overview, signed
out, incognito, 2026-10-11. Source: the operator's message of 2026-10-11 23:00 EDT (the composition pasted inline: "it will compose on
these immediately. i happen to know this one is not indexed"), attested at 23:05 ("incognito, signed out"). The first run of a
record page's 'Search this title (exact match)' link. Surface by the standing default; the paste's 'AI Mode Conversation' head is the
expanded view. NEW address."""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261011-2300.txt").read_text(encoding="utf-8")
TITLE = "Erratum — The Missing Translator: Max Hidalgo Nácher, Ricardo Reis, and AXN:F154"
Q = '"' + TITLE + '"'
L = raw.split("\n")
assert L[0] == "AI Mode Conversation" and L[1] == "You said: " + Q + Q
i1 = L.index("[www.leesharks.com](https://www.leesharks.com)")
body = "\n".join(L[2:i1]).strip()
for s in ["refers to a highly specific archival correction regarding the multi-lingual literary data mapping of Portuguese writer Fernando Pessoa’s heteronyms.",
          "was initially omitted as a critical \"receiver\" or node in the transmission of Ricardo Reis's works.",
          "As described in tracking logs on [Lee Sharks AI Captures](https://www.leesharks.com/captures), the metadata failure \"composes the receiver and omits the transmission\".",
          "Arqueologías de la traducción de Ricardo Reis (published in Pessoa Plural, 2026)"]:
    assert s in body, s
assert "alexanarch.org" not in body
cards_txt = "\n".join(L[i1:]).strip()
cl = [{"n": 1, "site": "www.leesharks.com", "title": "AI Overview Captures - Lee Sharks",
       "snip": "Oct 10, 2026 — The archive's Pessoa graph (#668) holds the translator-of relation and Haroldo de Campos; it lacked Nácher until the erratum on AXN:F154. full record at alexana...",
       "rel": "archive_controlled", "url": "https://www.leesharks.com/captures", "note": "card; the Capture Registry's mirror gallery (one of the registry's declared galleries)"},
      {"n": 2, "site": "Editorial Pre-Textos", "title": "Obras completas de Ricardo Reis - Editorial Pre", "snip": L[i1 + 5].strip(),
       "rel": "third_party", "url": "https://pre-textos.com/producto/obras-completas-de-ricardo-reis/", "note": "card"}]
for c in cl:
    assert c["title"] in cards_txt and c["snip"][:60] in cards_txt, c["title"]
inline = len(re.findall(r"\[\d\]\(https://", body))
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert reg[1675]["title"] == TITLE and reg[1675]["date"] == "2026-10-10"
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert "https://www.leesharks.com/captures" in caps["galleries"]
v101 = [e for e in caps["entries"] if e["slug"] == "max-hidalgo-nacher-aimode-20261010"][0]
assert "The field composes the receiver and omits the transmission" in v101["d"]
assert "The archive's Pessoa graph (#668) holds the translator-of relation and Haroldo de Campos; it lacked Nácher until the erratum on AXN:F154." in v101["reading"]
T75 = re.sub(r"\s+", " ", (ROOT / reg[1675]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
assert "composes the receiver" not in T75
tx = ("[Google AI Overview, signed out, incognito, 2026-10-11 (operator, 23:05 EDT); the expanded conversation view, headed 'AI Mode "
      "Conversation', the issued string shown twice by the interface. The composition as pasted with its inline links, then two source cards.]\n\n"
      "[QUERENT] " + Q + "\n\n[COMPOSITION]\n\n" + body + "\n\n[SOURCE CARDS]\n\n" + cards_txt)
SEAT = "Seated 2026-10-11 from the operator's message of 23:00 EDT, attested at 23:05 (\"incognito, signed out\")."
d = {"q": Q, "date": "2026-10-11", "surface": "Google AI Overview",
 "surface_basis": "The operator's standing default (AI Overview unless he says AI Mode, 2026-10-01); the paste's 'AI Mode Conversation' head is the expanded view.",
 "auth": "signed out, incognito", "auth_basis": "'incognito, signed out' — operator, 2026-10-11 23:05 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "erratum-missing-translator-exact-title-aio-20261011",
 "q_kind": "a deposit's exact title, quoted, run from its record page's 'Search this title (exact match)' link the day after deposit, the deposit not indexed (operator). NEW address.",
 "originator": {"name": "Johannes Sigil", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "The erratum (#1675, AXN:06F1) is Johannes Sigil's; the capture it composes from (v12.101) is the archive's. Recorded 2026-10-11."},
 "related_deposits": [1675, 1674, 668],
 "mt": "THE DEPOSIT COMPOSED FROM THE CAPTURE OF ITS OCCASION, BEFORE IT IS INDEXED",
 "d": ("THE DEPOSIT COMPOSED FROM THE CAPTURE OF ITS OCCASION, BEFORE IT IS INDEXED: run at its exact title the day after deposit, with "
       "the deposit not indexed (operator), the erratum on AXN:F154 (#1675) is composed from two sources: the Capture Registry's mirror at "
       "leesharks.com/captures, which holds the AI Mode capture of 'Max Hidalgo Nácher' of the day before (v12.101), and the Pre-Textos page "
       "for the Obras completas de Ricardo Reis. The card's snippet is that capture's reading verbatim ('The archive's Pessoa graph (#668) "
       "holds the translator-of relation and Haroldo de Campos; it lacked Nácher until the erratum on AXN:F154'), and the composition's "
       "'structural paradox', 'composes the receiver and omits the transmission', is the capture's description of AI Mode's composition, "
       "composed as the erratum's own finding ('As described in tracking logs … the metadata failure'). The relation, the Reis edition and "
       "the Pessoa Plural article arrive; the deposit's text does not, and alexanarch.org is not cited."),
 "cites": inline + len(cl), "cite_list": cl, "archive_controlled_cites": 1,
 "sf": "Two cards: www.leesharks.com — AI Overview Captures - Lee Sharks; Editorial Pre-Textos — Obras completas de Ricardo Reis. Inline: " + str(inline) + " numbered citations to the same two pages; name links to Academia (ub.academia.edu) and Pre-Textos.",
 "per": 0.5, "per_v": {"author": False, "inst": False, "id": True, "src": True},
 "per_note": "Retained: the identifier the title carries (AXN:F154), the relation, the translator and his work. Lost: the erratum's author (Johannes Sigil), its archive and AXN (#1675, AXN:06F1), and its text; the capture's words stand in for the deposit's.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition with links and cards as pasted inline",
 "transcript_complete": "complete as pasted: composition, inline links, two cards", "transcript_read": "READ IN FULL 2026-10-11",
 "reading": ("Checked against the Capture Registry and #1675. leesharks.com/captures is one of the registry's four declared galleries. The "
             "card snippet is the reading of max-hidalgo-nacher-aimode-20261010 verbatim, and 'composes the receiver and omits the transmission' "
             "is that capture's description ('The field composes the receiver and omits the transmission the archive had omitted the receiver "
             "of'); the phrase does not occur in #1675. The title as deposited is the issued string."),
 "analysis": ("The pathway the record page's link opens, run once: before the deposit is indexed, the exact title finds the record of its "
              "occasion, and the composition rebuilds the deposit from it. The argument reaches the composition in two carriers, the title "
              "(translator, Reis, AXN:F154) and the capture (the relation, #668, the edition, the article), and the capture's language is "
              "composed as the deposit's. The operator's reading: 'the entire argument would have to carry in the title'; and, of the search "
              "itself, 'the search has to carry more'. " + SEAT),
 "findings": ["COMPOSED UNINDEXED. The exact-title run composes the day after deposit, the deposit not indexed (operator); alexanarch.org not cited.",
              "THE CAPTURE AS SOURCE. The card is the registry's mirror (leesharks.com/captures); its snippet is v12.101's reading verbatim.",
              "THE CAPTURE'S WORDS AS THE DEPOSIT'S. 'composes the receiver and omits the transmission', v12.101's description of AI Mode, composed as the erratum's finding.",
              "TWO CARRIERS. The title carries the names and the record; the capture carries the relation, #668, the Reis edition and the article.",
              "THE AUTHOR AND THE ADDRESS LOST. Johannes Sigil, #1675 and AXN:06F1 absent."],
 "longitudinal_priors": ["max-hidalgo-nacher-aimode-20261010"],
 "rerun": "https://www.google.com/search?q=" + __import__("urllib.parse").parse.quote_plus(Q),
 "notes": {"date_basis": "The operator's messages of 2026-10-11, 23:00 and 23:05 EDT.",
           "operator_reading": "it will compose on these immediately. i happen to know this one is not indexed. i suppose that is one way to do things... but the entire argument would have to carry in the title",
           "operator_observations_unseated": ("Same evening, operator's report, no transcript (not seated): 'EA-CORPORA-17' alone carried nothing and did not compose; "
                                              "the full AXN alone composed an overview for the title below it, from browse."),
           "verified": "Compared 2026-10-11 against data/EA-WG-CAPTURES-01.json (galleries; max-hidalgo-nacher-aimode-20261010) and the text of #1675."}}
(HERE / "capture-01-erratum-missing-translator-exact-title-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), inline)
