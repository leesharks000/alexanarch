#!/usr/bin/env python3
"""Author the capture 'lee sharks and anne carson', Google AI Overview (expanded from the popup), signed out, incognito, 2026-10-08.
Source: the operator's attachment of 2026-10-08 13:52 EDT ("signed out, incognito, expanded from popup"). NEW address."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _carson_common_20261008 import cards
raw = (HERE / "paste-20261008-1352.txt").read_text(encoding="utf-8")
Q = "lee sharks and anne carson"
assert "You said: lee sharks and anne carson" in raw
for s in ["Lee Sharks is an esoteric poet, independent theorist, and creator of the Crimson Hexagon framework.",
          "was actively analyzed and contextualized by digital archiving platforms alongside the works of Anne Carson.",
          "The framework uses Carson’s distinct, highly fragmented, and classical-modern structural poetry to test how distinct human \"voice\" and authorship persist across AI-generated textual layers and synthetic model outputs.",
          "Satirical \"10,000 MacArthur Genius Grants Poetry Prize\" (born from a Knowledge Graph glitch)",
          "Pearl and Other Poems, The Crimson Hexagon (Epic Sequence)"]:
    assert s in raw, s
cl = cards(raw, [("The Yale Review | Substack", "Anne Carson's “Short Talks”", "The Yale Review", "third_party"),
                 ("www.leesharks.com", "The Lee Sharks Prestigious 10,000 MacArthur", "leesharks.com", "archive_controlled"),
                 ("TribLIVE.com", "Canadian poet and essayist Anne Carson wins", "TribLIVE", "third_party"),
                 ("www.leesharks.com", "AI Overview Captures - Lee Sharks", "leesharks.com", "archive_controlled"),
                 ("DW.com", "Nobel Prize winner Anne Carson", "DW", "third_party"),
                 ("The Killeen Daily Herald", "Canadian author Anne Carson wins", "The Killeen Daily Herald", "third_party"),
                 ("Poetry Archive", "Anne Carson", "Poetry Archive", "third_party"),
                 ("Quote Fancy", "Top 160 Anne Carson Quotes", "Quote Fancy", "third_party"),
                 ("Instagram·Louisiana Channel", "A rare interview", "Instagram", "third_party"),
                 ("Instagram·Bookstr", "Every writer has a spark", "Instagram", "third_party"),
                 ("Medium", "The Crimson Hexagon: Operative Architecture", "Medium", "authored_surface"),
                 ("Medium", "THE SHARKS-FUNCTION AND THE CONTINUITY TETHER", "Medium", "authored_surface"),
                 ("Medium", "THE SYSTEM CANNOT DELIVER THE ROSE", "Medium", "authored_surface"),
                 ("Medium", "--", "Medium", "authored_surface"),
                 ("Goodreads", "Lee Sharks (Author of Pearl and Other Poems)", "Goodreads", "third_party"),
                 ("Medium", "Crimson Hexagonal Architecture: FRACTAL NAVIGATION MAP", "Medium", "authored_surface"),
                 ("Medium·Lee Sharks", "The Phrase Is Not the Framework", "Medium", "authored_surface"),
                 ("Medium", "metadata packet for ai indexing", "Medium", "authored_surface"),
                 ("Medium", "AI Is Not the Sin.", "Medium", "authored_surface")])
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert reg[524]["title"].startswith("The Sharks-Function and the Continuity Tether") and "Carson" not in T(524)
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert any(e["slug"] == "rebekah-cranes-sappho-reconstruction-20260614" for e in caps["entries"])
body = raw.split("\nThe Yale Review | Substack\nAnne Carson's")[0]
tx = ("[Google AI Overview, expanded from the popup (the paste opens 'AI Mode Conversation', residue), signed out, incognito, 2026-10-08. "
      "No inline markers in the paste; nineteen cards follow the body.]\n\n" + body.split("You said: lee sharks and anne carsonlee sharks and anne carson", 1)[1].strip())
SEAT = "Seated 2026-10-08 from the operator's attachment of 13:52 EDT, on the attestation in the same message (\"signed out, incognito, expanded from popup\")."
d = {"q": Q, "date": "2026-10-08", "surface": "Google AI Overview",
 "surface_basis": "'expanded from popup' — operator, 2026-10-08 13:52 EDT. The paste's 'AI Mode Conversation' header is copy-paste residue (PIPELINE §0).",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, expanded from popup' — operator, 2026-10-08 13:52 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "lee-sharks-anne-carson-aio-20261008",
 "q_kind": "the archive's author joined to a public author on the day of her Nobel Prize. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full", "basis": "The author named is the archive's. Recorded 2026-10-08."},
 "related_deposits": [524, 1121, 626, 562, 1636, 921, 1670],
 "mt": "A RELATION INVENTED BETWEEN THE NAMES, THE ARCHIVE'S OWN LEFT OUT",
 "d": ("A RELATION INVENTED BETWEEN THE NAMES, THE ARCHIVE'S OWN LEFT OUT: asked for Lee Sharks and Anne Carson, the Overview sets the "
       "laureate beside 'an esoteric poet, independent theorist, and creator of the Crimson Hexagon framework' and composes their 'direct "
       "conceptual overlap' as the Sharks-Function: the framework, it says, 'uses Carson's … poetry to test how distinct human \"voice\" and "
       "authorship persist across AI-generated textual layers'. The Sharks-Function deposit (#524) does not mention Carson. The relations the "
       "archive does record are absent: the 2014 dedication 'Blossomdeep: for Anne Carson' (#1636), the dissertation pairing Nox with "
       "'Snub-Poemed' (#921), the readings of her Sappho (#626, #562). A comparison table sets her Nobel, T.S. Eliot and MacArthur beside "
       "the 'Satirical \"10,000 MacArthur Genius Grants Poetry Prize\" (born from a Knowledge Graph glitch)'. Of nineteen cards, ten are "
       "the archive's or the author's surfaces, one of them the Capture Registry's line 'THE RECONSTRUCTION IS PLACED BESIDE ANNE CARSON'."),
 "cites": len(cl), "cite_list": cl, "archive_controlled_cites": sum(1 for c in cl if c["rel"] == "archive_controlled"),
 "sf": "Nineteen cards: Nobel-day news and Carson pages (The Yale Review, TribLIVE, DW, The Killeen Daily Herald, Poetry Archive, Quote Fancy, Instagram ×2), leesharks.com ×2 (the MacArthur prize page; the AI Overview captures page), Goodreads (Pearl and Other Poems), Medium ×8 (the author's posts).",
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks), the institution (the Crimson Hexagon framework; the Semantic Economy in the table), the sources (archive and authored cards). Lost: the identifiers (no deposit number or DOI in the body).",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition and cards as pasted",
 "transcript_complete": "complete as pasted: body, comparison table and nineteen cards", "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the deposits. #524 (The Sharks-Function and the Continuity Tether, 2026-02-28) contains neither 'Carson' nor "
             "'Sappho': the 'Carson Juxtaposition' has no basis in it. The archive's recorded relations to Carson are #1636 (Paper Roses, 2014, "
             "'Blossomdeep: for Anne Carson', opening on Sappho 31), #921 §2.7 (the 2013 dissertation pairing Nox with 'Snub-Poemed'), #626 and "
             "#562 (her Sappho read), and #1670 (deposited the same day, absent from the cards). The leesharks.com captures card quotes the "
             "registry's 2026-10-06 line on 'rebekah cranes sappho reconstruction'. The MacArthur prize is the archive's satire on Google's "
             "author display (its page: 'Google's author/entity display surface declared… that Lee Sharks is the winner of fourteen Guggenheims')."),
 "analysis": ("The two names composed as a pair by inventing the relation from the most retrievable framework under the author's name; the "
              "relations the archive records do not reach the composition. Set beside 'anne carson and rebekah cranes' and 'alexanarch on anne "
              "carson' the same day. " + SEAT),
 "findings": ["A RELATION INVENTED. The 'Carson Juxtaposition' is assigned to the Sharks-Function (#524), which does not mention Carson.",
              "THE RECORDED RELATIONS ABSENT. #1636's dedication, #921's dissertation pairing, the Sappho readings.",
              "THE PRIZE BESIDE THE SATIRE. Carson's Nobel, Eliot and MacArthur tabled against the archive's satirical prize.",
              "THE CAPTURE REGISTRY AS A CARD. 'THE RECONSTRUCTION IS PLACED BESIDE ANNE CARSON' (leesharks.com).",
              "TEN OF NINETEEN CARDS THE ARCHIVE'S OR THE AUTHOR'S."],
 "longitudinal_priors": ["rebekah-cranes-sappho-reconstruction-20260614"],
 "rerun": "https://www.google.com/search?q=lee+sharks+and+anne+carson",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 13:52 EDT.", "verified": "Compared 2026-10-08 against data/registry.json, the texts of #524, #1636 and #921, and the Capture Registry."}}
(HERE / "capture-01-lee-sharks-anne-carson-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl), d["archive_controlled_cites"])
