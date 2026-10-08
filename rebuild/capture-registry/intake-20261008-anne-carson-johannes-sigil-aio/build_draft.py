#!/usr/bin/env python3
"""Author the capture 'anne carson and johannes sigil', Google AI Overview (expanded from the popup), signed out, incognito, 2026-10-08.
Source: the operator's message of 2026-10-08 14:10 EDT ("signed out, incognito, expanded from popup"). NEW address."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _carson_common_20261008 import cards
raw = (HERE / "paste-20261008-1410.txt").read_text(encoding="utf-8")
Q = "anne carson and johannes sigil"
assert "You said: anne carson and johannes sigilanne carson and johannes sigil" in raw
for s in ["Anne Carson described a text associated with the persona as \"a cool poem,\" which also functions as a conceptual portrait of Johannes Sigil",
          "an algorithmic/fictive heteronym and scholar linked to the \"Crimson Hexagonal Archive\" and the \"New Human Operating System\" (NH-OS)",
          "Anne Carson appears as a referenced critical voice or interlocutor regarding Sigil's poetic-philosophical portraits and sigillographic texts",
          "Anne Carson described it as \"a cool poem.\" It is also a portrait of Johannes Sigil. DOI: 10.5281/zenodo.19825730."]:
    assert s in raw, s
cl = cards(raw, [("[www.restoredacademy.com](https://www.restoredacademy.com)", "Johannes Sigil — Arch-Philosopher", "Restored Academy", "archive_controlled"),
                 ("Academia.edu", "Johannes Sigil - Independent Scholar", "Academia.edu", "authored_surface"),
                 ("Academia.edu", "(PDF) THE EPIC WITHOUT HERO", "Academia.edu", "authored_surface"),
                 ("Medium·Johannes Sigil", "MAGIC AS SYMBOLIC ENGINEERING", "Medium", "authored_surface"),
                 ("Medium", "The Fourth Mode: New Human", "Medium", "authored_surface")])
cl[0]["url"] = "https://www.restoredacademy.com"
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
t700 = T(700)
assert "Her response — \"a cool poem\" — is not evidence for the poem's argument, but it is a useful reception trace" in t700
assert "received \"Snub-Poemed\" in 2013" in t700 and reg[701]["title"] == '"Snub-Poemed"'
page = (ROOT.parent / "restoredacademy/sigil/index.html").read_text(encoding="utf-8")
assert "(Jack Feist, 2013). Concrete poem in which scattered letters compose the</span> face of Socrates. The poem <em>is</em> the philosopher. Anne Carson described it as \"a cool poem.\" It is also a portrait of Johannes Sigil." in page
assert "10.5281/zenodo.19825730" in page
body = raw.split("\n[www.restoredacademy.com](https://www.restoredacademy.com)\n")[0]
tx = ("[Google AI Overview, expanded from the popup (the paste opens 'AI Mode Conversation', residue), signed out, incognito, 2026-10-08. "
      "Inline markers are opaque google.com/goto tokens; five cards follow the body.]\n\n"
      + body.split("You said: anne carson and johannes sigilanne carson and johannes sigil", 1)[1].strip())
OP = ("Operator's statement, 2026-10-08 14:01 EDT: 'she did say that, of snub-poemed, maybe 13-14 years ago. she also called sappho future "
      "reader a 'weird idea'. thats basically the entire history of the correspondence.'")
SEAT = "Seated 2026-10-08 from the operator's message of 14:10 EDT, on the attestation in the same message (\"signed out, incognito, expanded from popup\")."
d = {"q": Q, "date": "2026-10-08", "surface": "Google AI Overview",
 "surface_basis": "'expanded from popup' — operator, 2026-10-08 14:10 EDT. The paste's 'AI Mode Conversation' header is copy-paste residue (PIPELINE §0).",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito, expanded from popup' — operator, 2026-10-08 14:10 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "anne-carson-johannes-sigil-aio-20261008",
 "q_kind": "a public author joined to a heteronym of the archive on the day of her Nobel Prize. NEW address.",
 "originator": {"name": "Johannes Sigil", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Johannes Sigil is a heteronym of Lee Sharks (the Dodecad, D.02). Recorded 2026-10-08."},
 "related_deposits": [700, 701, 42, 1271, 532, 301, 1670],
 "mt": "ONE REMARK ON ONE POEM, THE POEM'S NAME DROPPED",
 "d": ("ONE REMARK ON ONE POEM, THE POEM'S NAME DROPPED: asked for Anne Carson and Johannes Sigil on the day of her Nobel, the Overview "
       "opens on the one Carson sentence the archive's surfaces carry. The Restored Academy's Sigil page captions Snub-Poemed (Jack Feist, "
       "2013): 'Anne Carson described it as \"a cool poem.\" It is also a portrait of Johannes Sigil.' The composition keeps the quotation "
       "and the portrait and drops the poem's name: Carson 'described a text associated with the persona as \"a cool poem\"'. A second "
       "bullet makes her 'a referenced critical voice or interlocutor regarding Sigil's poetic-philosophical portraits and sigillographic "
       "texts', a plural built on the one remark. #700 records the remark as 'a useful reception trace', with the caution that it 'is not "
       "evidence for the poem's argument'; the caution does not reach the composition. All five cards are the archive's or its authored surfaces."),
 "cites": len(cl), "cite_list": cl, "archive_controlled_cites": sum(1 for c in cl if c["rel"] == "archive_controlled"),
 "sf": "Five cards: restoredacademy.com (the Sigil page, with the Carson caption and the DOI 10.5281/zenodo.19825730), Academia.edu ×2 (Sigil's profile; The Epic Without Hero, #1271), Medium ×2 (Magic as Symbolic Engineering, #532; The Fourth Mode, #301). No third-party card.",
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author (Johannes Sigil, 'associated with writer Lee Sharks'), the institution (the Crimson Hexagonal Archive; NH-OS), the sources (five archive and authored cards). Lost: the identifiers (the DOI only in a card snippet) and the work's name (Snub-Poemed).",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition, markers and cards as pasted",
 "transcript_complete": "complete as pasted: body with markers, five cards", "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the deposits and the card's page. restoredacademy.com/sigil/ (repo, line 547) captions the Snub-Poemed image: "
             "'(Jack Feist, 2013). Concrete poem in which scattered letters compose the face of Socrates. The poem is the philosopher. Anne "
             "Carson described it as \"a cool poem.\" It is also a portrait of Johannes Sigil.', then the DOI 10.5281/zenodo.19825730, one of "
             "the two poems #700 compiles (#701 is Snub-Poemed). #700 §I: 'Anne Carson … received \"Snub-Poemed\" in 2013. Her response — "
             "\"a cool poem\" — is not evidence for the poem's argument, but it is a useful reception trace'. The card snippet keeps the "
             "caption's last two sentences and the DOI and loses the poem's name, and the composition follows the snippet. No archive text "
             "makes Carson an interlocutor on Sigil's 'portraits' or 'sigillographic texts'. " + OP + " The second remark is in no archive text."),
 "analysis": ("The Nobel makes any sentence with Carson's name salient, and the archive holds one such sentence on its surfaces: a caption. "
              "The composition reads it at the grain of the snippet, which cuts the caption below the poem's name, so the remark attaches "
              "to 'a text associated with the persona' and then, in the plural, to Sigil's portraits. The deflating remark the operator "
              "reports is unindexed, and the composer cannot compose with it. Set beside 'anne carson in crimson hexagonal archive' the "
              "same hour, where the same caption becomes praise of the project. " + SEAT),
 "findings": ["THE ONE SENTENCE. The only Carson-attributed sentence on the archive's surfaces opens the composition on the day of the Nobel.",
              "THE POEM'S NAME DROPPED. The snippet cuts the caption below 'Snub-Poemed'; the remark attaches to 'a text associated with the persona'.",
              "ONE REMARK MADE PLURAL. Carson as 'a referenced critical voice or interlocutor' on Sigil's 'portraits' and 'sigillographic texts'.",
              "#700'S CAUTION LOST. 'not evidence for the poem's argument' does not reach the composition.",
              "THE UNINDEXED HALF. The operator reports a second remark ('a weird idea', of Sappho Future Reader) held in no archive text.",
              "FIVE OF FIVE CARDS THE ARCHIVE'S OR ITS AUTHORED SURFACES."],
 "longitudinal_priors": [],
 "rerun": "https://www.google.com/search?q=anne+carson+and+johannes+sigil",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 14:10 EDT; the correspondence statement is from 14:01 EDT.",
           "verified": "Compared 2026-10-08 against data/registry.json, the text of #700, #701's record, and restoredacademy/sigil/index.html."}}
(HERE / "capture-01-anne-carson-johannes-sigil-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl), d["archive_controlled_cites"])
