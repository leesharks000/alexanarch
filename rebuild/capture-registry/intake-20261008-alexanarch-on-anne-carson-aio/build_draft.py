#!/usr/bin/env python3
"""Author the capture 'alexanarch on anne carson', Google AI Overview (expanded), signed out, incognito, 2026-10-08, the day of
Carson's Nobel. Source: the operator's message of 2026-10-08 11:29 EDT ("captures. logged out. incognito."). The paste opens 'AI Mode
Conversation', which is copy-paste residue and no surface signal (PIPELINE §0); the operator did not say AI Mode, and the standing
default (2026-10-01) records AI Overview. NEW address; nearest seated 'alexanarch sappho' (AIO, 2026-07-31).
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
raw = (HERE / "paste-20261008-1129.txt").read_text(encoding="utf-8")
Q = "alexanarch on anne carson"
assert raw.startswith("AI Mode Conversation\nYou said: alexanarch on anne carson")
body = raw.split("\nThe New York Times\n")[0]
for s in ["examining her structural use of the \"third\" or the gap in classical and contemporary text",
          "her work is evaluated through the lens of unspaced lyric forms, notebook shorthand, archival preservation",
          "treats incompleteness not as a flaw to be fixed, but as the active site where transmission, translation, and textuality take place",
          "her recent 2026 Nobel Prize in Literature win"]:
    assert s in raw, s
cards = [("The New York Times", "New to Anne Carson's Books? Start Here. - The New York Times", "third_party"),
         ("France 24", "Anne Carson: modern takes on Greek classics - France 24", "third_party"),
         ("www.alexanarch.org", "The Slavonic Josephus, the Grammar of Incarnation, and the Doctrine - Alexanarch", "archive_controlled"),
         ("www.alexanarch.org", "The Word That Became Text: The Slavonic Josephus, the Grammar ...", "archive_controlled"),
         ("www.alexanarch.org", "ON THE ARCHITECTURE OF CLEIS Compression, Botanics ...", "archive_controlled"),
         ("Firstpost", "Anne Carson, the Nobel-winning poet who taught Greek for a living", "third_party")]
cite_list = []
for i, (site, title, rel) in enumerate(cards, 1):
    k = raw.find("\n" + title + "\n"); assert k >= 0, title
    snip = raw[k + len(title) + 2:].split("\n", 1)[0]
    cite_list.append({"n": i, "site": "Alexanarch" if rel == "archive_controlled" else site, "title": title, "snip": snip, "rel": rel, "url": "https://www.alexanarch.org" if rel == "archive_controlled" else None, "note": "card"})
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t562 = (ROOT / reg[562]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
t626 = (ROOT / reg[626]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "notebook shorthand" in t562 and "Rebekah Cranes" in t562[:300] and "Where Carson leaves the wound open, Feist sutures it with devotion." in t562
assert "But Carson's analysis stops at the erotic." in t626
assert reg[626]["date"] == "2026-04-05" and reg[1176]["date"] == "2026-04-05" and reg[562]["date"] == "2026-03-14"
tx = ("[Google AI Overview, expanded (the paste opens 'AI Mode Conversation', residue), signed out, incognito, 2026-10-08. Inline markers "
      "are opaque google.com/goto tokens; six cards follow the body.]\n\n" + body.split("\n", 2)[2].strip())
SEAT = "Seated 2026-10-08 from the operator's message of 11:29 EDT, on the attestation in the same message (\"logged out. incognito.\")."
d = {
 "q": Q, "date": "2026-10-08", "surface": "Google AI Overview",
 "surface_basis": "The operator did not say AI Mode; standing default (operator, 2026-10-01): 'it started in overview, as they all do now - assume they do, i will specify if they begin in ai mode'. The paste's 'AI Mode Conversation' header is copy-paste residue (PIPELINE §0).",
 "auth": "signed out, incognito", "auth_basis": "'captures. logged out. incognito.' — operator, 2026-10-08 11:29 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "alexanarch-on-anne-carson-aio-20261008",
 "q_kind": "the archive's domain name joined to a public author on the day of her Nobel Prize. NEW address; nearest seated 'alexanarch sappho' (AIO, 2026-07-31).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                "basis": "alexanarch is the archive; its readings of Carson are deposits #626, #562, #625, #1270, #1615, #1645 and the /non entry anne-carson. Recorded 2026-10-08."},
 "related_deposits": [626, 1176, 562, 625, 1270, 1645, 1615, 1665, 1670],
 "mt": "THE TRIANGLE KEPT AS HERS, THE CLEIS READING GIVEN TO HER",
 "d": ("THE TRIANGLE KEPT AS HERS, THE CLEIS READING GIVEN TO HER: on the day of the Nobel, asked what alexanarch does with Anne Carson, "
       "the Overview composes three moves from three archive cards beside three Nobel-day news cards. The triangle is Carson's, quoted from "
       "#626 ('that which comes between them'), and the gap as the active site of transmission matches #625 and #562. The middle bullet "
       "gives Carson's work an evaluation 'through the lens of unspaced lyric forms, notebook shorthand, archival preservation': the "
       "'notebook shorthand' is #562's account of Jack Feist's Cleis ('a theological claim delivered in notebook shorthand'), a companion "
       "by Rebekah Cranes in which Carson appears once, as the translator who leaves the gap open. The archive's limit on the triangle "
       "(#626, 'Carson's analysis stops at the erotic') does not reach the composition. Author unnamed; Cranes only in a card snippet."),
 "cites": len(cite_list), "cite_list": cite_list, "archive_controlled_cites": 3,
 "sf": "Six cards: The New York Times, France 24 (both dated 8 Oct 2026, the award), Alexanarch ×3 (#626 and its second deposit #1176 under two titles; #562), Firstpost.",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the institution (Alexanarch, 'an independent, self-governing static archive') and the sources (three archive cards). Lost: the author (Lee Sharks unnamed; Rebekah Cranes only in a card snippet) and the identifiers.",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition, markers and cards as pasted",
 "transcript_complete": "complete as pasted: body with markers, the follow-up offer, six cards", "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the deposits. Bullet 1 quotes #626 §II (2026-04-05; second deposit #1176, same day), which the first two archive "
             "cards carry. Bullet 3 matches #625 §4 ('the absence becomes part of the transmission') and #562 ('Where Carson leaves the wound "
             "open'). Bullet 2's 'notebook shorthand' is #562's phrase for Feist's poem '\"death came in / to the world w/ / you\"'; #562 "
             "(2026-03-14) is Rebekah Cranes's companion to Cleis, and its one Carson passage sets her If Not, Winter beside Feist's completions. "
             "'unspaced lyric forms' is in no Carson passage of the archive. The offer at the end ties fragmentation to 'her recent 2026 Nobel "
             "Prize in Literature win', with the NYT and Firstpost Nobel-day cards."),
 "analysis": ("The archive's Carson line composed on the day of the award, from its own deposits, at the archive's address: the readings "
              "it holds survive (the triangle, the gap), its stated limit on Carson does not, and a companion about another poet supplies "
              "a predicate for Carson's work. Set beside #1670 (deposited later the same day; absent from the cards) and the /non entry anne-carson. " + SEAT),
 "findings": ["THE TRIANGLE KEPT AS HERS. #626's quotation of Eros the Bittersweet carried, attributed to Carson.",
              "THE LIMIT DROPPED. #626's 'Carson's analysis stops at the erotic' is absent; the archive's extension is not composed.",
              "ANOTHER POET'S FORM GIVEN TO HER. 'notebook shorthand' is #562's description of Feist's Cleis, composed as the lens on Carson.",
              "ONE DEPOSIT TWICE. #626 and #1176 (the same paper, two deposits) appear as two cards.",
              "THE NOBEL IN THE FRAME. Two of three third-party cards are Nobel-day news; the closing offer ties the reading to the prize."],
 "longitudinal_priors": ["alexanarch-sappho-20260731", "alexanarch-sappho-room-20260726"],
 "rerun": "https://www.google.com/search?q=alexanarch+on+anne+carson",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 11:29 EDT.",
           "verified": "Compared 2026-10-08 against data/registry.json and the texts of #626, #1176, #562 and #625."},
}
(HERE / "capture-01-alexanarch-on-anne-carson-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cite_list))
