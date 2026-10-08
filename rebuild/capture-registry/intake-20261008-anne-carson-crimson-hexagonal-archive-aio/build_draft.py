#!/usr/bin/env python3
"""Author the capture 'anne carson in crimson hexagonal archive', Google AI Overview (expanded from the popup), signed out, incognito,
2026-10-08. Source: the operator's message of 2026-10-08 14:10 EDT ("signed out, incognito, expanded from popup"). NEW address."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _carson_common_20261008 import cards
raw = (HERE / "paste-20261008-1410.txt").read_text(encoding="utf-8")
Q = "anne carson in crimson hexagonal archive"
assert "You said: anne carson in crimson hexagonal archiveanne carson in crimson hexagonal archive" in raw
for s in ["Anne Carson described the work housed in the Crimson Hexagonal Archive as \"a cool poem.\"",
          "The 2026 Nobel laureate lent her brief but characteristic praise to the project, recognizing its distinct blend of poetry and archival documentation.",
          "The archive consists of permanent documents hosted on Zenodo under a Creative Commons (CC BY 4.0) license.",
          "Anne Carson described it as \"a cool poem.\" It is also ... Each document below is DOI-permanent under CC BY 4.0 in the Crimson Hexagonal Archive on Zenodo."]:
    assert s in raw, s
cl = cards(raw, [("[www.restoredacademy.com](https://www.restoredacademy.com)", "Johannes Sigil — Arch-Philosopher", "Restored Academy", "archive_controlled"),
                 ("The Yale Review | Substack", "Anne Carson’s “Short Talks”", "The Yale Review", "third_party")])
cl[0]["url"] = "https://www.restoredacademy.com"
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t700 = (ROOT / reg[700]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "is not evidence for the poem's argument, but it is a useful reception trace" in t700
page = (ROOT.parent / "restoredacademy/sigil/index.html").read_text(encoding="utf-8").split("\n")
i547 = next(i for i, l in enumerate(page) if 'Anne Carson described it as "a cool poem." It is also a portrait of Johannes Sigil.' in l)
i594 = next(i for i, l in enumerate(page) if "Each document below is DOI-permanent under CC BY 4.0 in the Crimson Hexagonal Archive on Zenodo." in l)
assert i594 - i547 > 40 and "<h2>What I hold</h2>" in "\n".join(page[i547:i594])
body = raw.split("\n[www.restoredacademy.com](https://www.restoredacademy.com)\n")[0]
tx = ("[Google AI Overview, expanded from the popup (the paste opens 'AI Mode Conversation', residue), signed out, incognito, 2026-10-08. "
      "Inline markers are opaque google.com/goto tokens; two cards follow the body.]\n\n"
      + body.split("You said: anne carson in crimson hexagonal archiveanne carson in crimson hexagonal archive", 1)[1].strip())
OP = ("Operator's statement, 2026-10-08 14:01 EDT: 'she did say that, of snub-poemed, maybe 13-14 years ago. she also called sappho future "
      "reader a 'weird idea'. thats basically the entire history of the correspondence.'")
SEAT = "Seated 2026-10-08 from the operator's message of 14:10 EDT, on the attestation in the same message (\"signed out, incognito, expanded from popup\")."
d = {"q": Q, "date": "2026-10-08", "surface": "Google AI Overview",
 "surface_basis": "'expanded from popup' — operator, 2026-10-08 14:10 EDT. The paste's 'AI Mode Conversation' header is copy-paste residue (PIPELINE §0).",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, expanded from popup' — operator, 2026-10-08 14:10 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "anne-carson-crimson-hexagonal-archive-aio-20261008",
 "q_kind": "a public author placed inside the archive by name on the day of her Nobel Prize. NEW address.",
 "originator": {"name": "Crimson Hexagonal Archive", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                "basis": "The archive named in the query. Recorded 2026-10-08."},
 "related_deposits": [700, 701, 1670],
 "mt": "A REMARK ON ONE POEM COMPOSED AS THE LAUREATE'S PRAISE OF THE ARCHIVE",
 "d": ("A REMARK ON ONE POEM COMPOSED AS THE LAUREATE'S PRAISE OF THE ARCHIVE: asked for Anne Carson in the Crimson Hexagonal Archive, "
       "the Overview answers in one sentence: 'Anne Carson described the work housed in the Crimson Hexagonal Archive as \"a cool poem.\"' "
       "Its third bullet: 'The 2026 Nobel laureate lent her brief but characteristic praise to the project, recognizing its distinct blend "
       "of poetry and archival documentation.' The source is one card, the Restored Academy's Sigil page, whose snippet runs 'Anne Carson "
       "described it as \"a cool poem.\" It is also ... Each document below is DOI-permanent under CC BY 4.0 in the Crimson Hexagonal "
       "Archive on Zenodo.' On the page the two sentences stand forty-seven lines apart: the first is the caption of Snub-Poemed (Jack Feist, "
       "2013), the second opens the list 'What I hold'. The ellipsis joins them, and 'it' takes the archive as its antecedent. A remark "
       "about one poem becomes the laureate's praise of the project, on the day of the prize."),
 "cites": len(cl), "cite_list": cl, "archive_controlled_cites": sum(1 for c in cl if c["rel"] == "archive_controlled"),
 "sf": "Two cards: restoredacademy.com (the Sigil page; its snippet joins the Snub-Poemed caption to the 'What I hold' list by an ellipsis), The Yale Review (Carson's Short Talks, reposted for the Nobel, 8 Oct 2026).",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the institution (the Crimson Hexagonal Archive; Zenodo, CC BY 4.0; the Restored Academy) and the source (the archive card). Lost: the author (Lee Sharks and Jack Feist unnamed; Sigil only as a link title), the identifiers, and the work (Snub-Poemed).",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition, markers and cards as pasted",
 "transcript_complete": "complete as pasted: body with markers, two cards", "transcript_read": "READ IN FULL 2026-10-08",
 "reading": (f"Checked against the card's page and #700. restoredacademy/sigil/index.html line {i547 + 1} is the caption of the Snub-Poemed "
             "image ('(Jack Feist, 2013). … Anne Carson described it as \"a cool poem.\" It is also a portrait of Johannes Sigil.'); line "
             f"{i594 + 1}, after the heading 'What I hold', reads 'Each document below is DOI-permanent under CC BY 4.0 in the Crimson Hexagonal "
             "Archive on Zenodo.' The card's snippet splices the two with '...'. The body's 'The Project' bullet restates line "
             f"{i594 + 1}; its opening sentence and 'The Connection' bullet read the caption's 'it' through the splice. #700 §I records the "
             "remark of 2013 as 'a useful reception trace' that 'is not evidence for the poem's argument'. " + OP +
             " The second remark is in no archive text."),
 "analysis": ("Scope inflation by snippet splice: the card's ellipsis closes forty-seven lines of page, the pronoun crosses it, and a remark on "
              "one poem is composed as a judgment of the archive. 'brief but characteristic' and 'recognizing its distinct blend of poetry "
              "and archival documentation' are the composition's own; no source gives them. The Nobel-day Yale Review card supplies "
              "'laureate'. Set beside 'anne carson and johannes sigil' the same hour, where the same caption keeps its object at one "
              "poem and loses its name. " + SEAT),
 "findings": ["THE SPLICE. The card's snippet joins the Snub-Poemed caption to the 'What I hold' list across forty-seven lines with '...'.",
              "THE PRONOUN CROSSES IT. The caption's 'it' (the poem) is composed as 'the work housed in the Crimson Hexagonal Archive'.",
              "PRAISE OF THE PROJECT. 'lent her brief but characteristic praise to the project'; no source gives 'characteristic' or the 'blend'.",
              "THE LAUREATE FROM THE NEWS. 'The 2026 Nobel laureate' with the Yale Review's Nobel-day card.",
              "#700'S CAUTION LOST. 'not evidence for the poem's argument' does not reach the composition.",
              "THE UNINDEXED HALF. The operator reports a second remark ('a weird idea', of Sappho Future Reader) held in no archive text."],
 "longitudinal_priors": [],
 "rerun": "https://www.google.com/search?q=anne+carson+in+crimson+hexagonal+archive",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 14:10 EDT; the correspondence statement is from 14:01 EDT.",
           "verified": "Compared 2026-10-08 against data/registry.json, the text of #700, and restoredacademy/sigil/index.html."}}
(HERE / "capture-01-anne-carson-crimson-hexagonal-archive-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl), d["archive_controlled_cites"], i547 + 1, i594 + 1)
