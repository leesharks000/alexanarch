#!/usr/bin/env python3
"""Author the capture 'anne carson and rebekah cranes', Google AI Overview (expanded from the popup), signed out, incognito, 2026-10-08.
Source: the operator's attachment of 2026-10-08 13:52 EDT ("signed out, incognito, expanded from popup"). NEW address; nearest seated
'rebekah cranes sappho reconstruction' (2026-06-14)."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _carson_common_20261008 import cards
raw = (HERE / "paste-20261008-1352.txt").read_text(encoding="utf-8")
Q = "anne carson and rebekah cranes"
assert "You said: anne carson and rebekah cranes" in raw
for s in ["Anne Carson and Rebekah Cranes (often stylized as Rebekah Cranes) are prominent figures in contemporary experimental literature",
          "Their names frequently cross paths in the sphere of \"operative philology,\"",
          "Rebekah Cranes is an avant-garde translator, poet, and critic",
          "She is the author of On the Architecture of Cleis (2026)",
          "that author is spelled Rebekah Crane)", "awarded the 2026 Nobel Prize in Literature"]:
    assert s in raw, s
cl = cards(raw, [("Wikipedia", "Anne Carson - Wikipedia", "Wikipedia", "third_party"),
                 ("Poetry Foundation", "Anne Carson | The Poetry Foundation", "Poetry Foundation", "third_party"),
                 ("Spokane Public Radio", "A Conversation with Rebekah Crane", "Spokane Public Radio", "third_party"),
                 ("www.alexanarch.org", "ON THE ARCHITECTURE OF CLEIS", "Alexanarch", "archive_controlled"),
                 ("Sweden Herald", "Anne Carson Is a Unique Writer", "Sweden Herald", "third_party"),
                 ("www.alexanarch.org", "APZPZ C: ΦΑΙΝΕΤΑΙ ΜΟΙ", "Alexanarch", "archive_controlled"),
                 ("The Yale Review | Substack", "Anne Carson's “Short Talks”", "The Yale Review", "third_party"),
                 ("Britannica", "Anne Carson | 2026 Nobel Prize", "Britannica", "third_party"),
                 ("KDRV NewsWatch 12", "Anne Carson, the genre", "KDRV", "third_party"),
                 ("Goodreads", "Rebekah Crane (Author of The Upside of Falling Down)", "Goodreads", "third_party"),
                 ("Medium·Johannes Sigil", "The Fourth Mode: New Human", "Medium", "authored_surface")])
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "Rebekah Cranes" in T(562)[:300] and reg[562]["date"] == "2026-03-14" and "Carson's is scholarly." in T(562)
assert reg[436]["title"].startswith("APZPZ C: ΦΑΙΝΕΤΑΙ ΜΟΙ") and reg[436]["date"] == "2026-02-02"
assert "She is not Rebekah Crane, the young-adult novelist" in T(1645) and "An authorial identity of Lee Sharks dating to 2004 (HET-CRANES-001)" in T(1645)
body = raw.split("\nWikipedia\nAnne Carson - Wikipedia")[0]
tx = ("[Google AI Overview, expanded from the popup (the paste opens 'AI Mode Conversation', residue), signed out, incognito, 2026-10-08. "
      "No inline markers in the paste; eleven cards follow the body.]\n\n" + body.split("You said: anne carson and rebekah cranesanne carson and rebekah cranes", 1)[1].strip())
SEAT = "Seated 2026-10-08 from the operator's attachment of 13:52 EDT, on the attestation in the same message (\"signed out, incognito, expanded from popup\")."
d = {"q": Q, "date": "2026-10-08", "surface": "Google AI Overview",
 "surface_basis": "'expanded from popup' — operator, 2026-10-08 13:52 EDT. The paste's 'AI Mode Conversation' header is copy-paste residue (PIPELINE §0).",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, expanded from popup' — operator, 2026-10-08 13:52 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "anne-carson-rebekah-cranes-aio-20261008",
 "q_kind": "a public author joined to a heteronym on the day of the author's Nobel Prize. NEW address; nearest seated 'rebekah cranes sappho reconstruction' (2026-06-14).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Rebekah Cranes is an authorial identity of Lee Sharks (HET-CRANES-001, #1645 §11). Recorded 2026-10-08."},
 "related_deposits": [562, 436, 1645, 1270, 1604, 1670],
 "mt": "THE HETERONYM SEATED BESIDE THE LAUREATE AS A PEER",
 "d": ("THE HETERONYM SEATED BESIDE THE LAUREATE AS A PEER: on the day of the Nobel, asked for Anne Carson and Rebekah Cranes, the "
       "Overview composes the two as 'prominent figures in contemporary experimental literature' whose 'names frequently cross paths in "
       "the sphere of \"operative philology\"', and gives Cranes a section of her own as 'an avant-garde translator, poet, and critic', "
       "author of On the Architecture of Cleis (#562) and of a reconstructed Sappho 31 (#436). It disambiguates her from the novelist "
       "Rebekah Crane, as #1645 does. It does not say that Cranes is a heteronym of Lee Sharks, and Lee Sharks is not named. The relation "
       "it asserts between the two names has one basis in the archive: #562's single sentence setting Carson's If Not, Winter beside Feist's Cleis."),
 "cites": len(cl), "cite_list": cl, "archive_controlled_cites": sum(1 for c in cl if c["rel"] == "archive_controlled"),
 "sf": "Eleven cards: Wikipedia, Poetry Foundation, Spokane Public Radio (Rebekah Crane), Alexanarch (#562), Sweden Herald, Alexanarch (#436), The Yale Review, Britannica, KDRV, Goodreads (Rebekah Crane), Medium (Johannes Sigil).",
 "per": 0.5, "per_v": {"author": False, "inst": False, "id": True, "src": True},
 "per_note": "Retained: the heteronym's works by title and date (On the Architecture of Cleis, the Sappho 31 reconstruction; an identifier in the #562 card, DOI 10.5281/zenodo.19025556) and the sources (two archive cards). Lost: the author (Lee Sharks, behind the heteronym) and the institution (neither the archive nor the Institute for Diagrammatic Poetics is named in the body).",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and cards as pasted",
 "transcript_complete": "complete as pasted: body and eleven cards", "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the deposits. #562 (2026-03-14) is Rebekah Cranes's companion to Cleis; its one Carson passage ends 'Carson's is "
             "scholarly.' #436 (2026-02-02) is APZPZ C, Sappho 31 with a reconstructed fourth stanza, translation by Rebekah Cranes. #1645 §11: "
             "'An authorial identity of Lee Sharks dating to 2004 (HET-CRANES-001)… She is not Rebekah Crane, the young-adult novelist'. The "
             "'witness voice' and the I Ching are not located in a seated Cranes text; the card beside them is Johannes Sigil's 'The Fourth "
             "Mode' (Medium, 2025-12-17). The composition's 'performance artist on the page' for Carson carries no card here."),
 "analysis": ("A heteronym composed as a person beside a laureate on the day of the award, with the disambiguation the archive supplied kept "
              "and the heteronymy itself dropped. Set beside 'anne carson sappho' (/non battery 1h), where the same day's composition names no archive work. " + SEAT),
 "findings": ["THE HETERONYM AS A PEER. Cranes composed as an avant-garde translator beside Carson; 'their names frequently cross paths'.",
              "THE HETERONYMY DROPPED. Lee Sharks unnamed; Cranes's status as an authorial identity (#1645) absent.",
              "THE DISAMBIGUATION KEPT. Rebekah Crane, the YA novelist, kept apart, as #1645 does.",
              "THE WORKS KEPT. #562 and #436 by title and date.",
              "THE RELATION FROM ONE SENTENCE. The one archive basis for the pair is #562's Carson/Feist sentence."],
 "longitudinal_priors": ["rebekah-cranes-sappho-reconstruction-20260614"],
 "rerun": "https://www.google.com/search?q=anne+carson+and+rebekah+cranes",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 13:52 EDT.", "verified": "Compared 2026-10-08 against data/registry.json and the texts of #562, #436 and #1645."}}
(HERE / "capture-01-anne-carson-rebekah-cranes-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl))
