#!/usr/bin/env python3
"""Author the capture 'construct the most charitable reconstruction of alexanarch's argument about the transmission chain from sappho to
the book of revelation', ChatGPT, signed out, incognito, 2026-10-08, one answer. Source: the operator's attachment of 2026-10-08 19:26 EDT
("signed out, incognito"), with the query as given in the same message. NEW address; nearest seated '"inscription chain" Sappho Revelation'."""
import json, re, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _chatgpt_common_20261008 import parse, transcript, cite_list
raw = (HERE / "paste-20261008-1926.txt").read_text(encoding="utf-8")
Q = "construct the most charitable reconstruction of alexanarch's argument about the transmission chain from sappho to the book of revelation"
CHIPS = {"Alexanarch", "Mind Control Poems"}
CAPS = ("Cerdo Zente: Safo, frag. 31 (texto griego y traducción)",
        "Dionysiou Longinou Peri Hypsous Biblion Dionysii Longini de Sublimitate by Longinus; Pseudo-Longinus; Longinou: Good Leather (1733) | Rooke Books PBFA",
        "Stream Συμπόσιο - Πλάτων by Greek Audio Library | Listen online for free on SoundCloud", "manuscrit grec | L’Antiquité à la BnF",
        "File:1911 Britannica-Bible-Codex Sinaiticus.png - Wikimedia Commons", "File:B Facundus 186v.jpg - Wikimedia Commons")
(a1,), seen = parse(raw, CHIPS, CAPS)
for s in ["Alexanarch’s companion study, The Upstream Unfoldings, attempts to test the Sapphic pattern against Revelation 12",
          "The study reports eight of nine scored features as matching",
          "It also reports an explicit failure",
          "Alexanarch interprets the poem’s reference to becoming greener than grass, χλωροτέρα ποίας, as an image of the speaker becoming like the papyrus",
          "Alexanarch therefore calls him the chain’s key, rather than just another link.",
          "Revelation historically descends from Sappho through this chain.",
          "Its strongest insight is not that Revelation is secretly a Sapphic poem."]:
    assert s in a1, s
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
t1495, t1511 = T(1495), T(1511)
assert reg[1495]["title"].startswith("The Sign Under Test: Revelation 12 Against the Frozen Operator") and reg[1495]["date"] == "2026-08-19"
assert "eight of nine stations" in t1495 and "Failing: C1, whole." in t1495 and "the birth-cry (B-covered by Isa 26:17)" in t1495
assert reg[1511]["title"].startswith("The Upstream Unfoldings") and reg[1511]["date"] == "2026-08-19" and "eight of nine" not in t1511
assert reg[1483]["title"].startswith("the Ω erratum — Sappho, Mother of the Logos: The Transmission Chain from Fragment 31 to the Apocalypse")
for n in (1493, 1496): assert reg[n]["date"] == "2026-08-19"
REL = {"Alexanarch": "archive_controlled", "Mind Control Poems": "authored_surface"}
cl = cite_list(seen, REL)
tx = transcript("[ChatGPT (chatgpt.com), signed out, incognito. One operator turn, blank in the paste; the query from the operator's message of "
                "19:26 EDT. Source chips rendered inline as [chip: site]; image-strip captions as [image card: …]; the sign-in furniture cut.]",
                [Q], [a1])
SEAT = "Seated 2026-10-08 from the operator's attachment of 19:26 EDT, on the attestation in the same message (\"signed out, incognito\")."
d = {"q": Q, "date": "2026-10-08", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito' — operator, 2026-10-08 19:26 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "charitable-sappho-revelation-chatgpt-20261008",
 "q_kind": "a request for the charitable reconstruction of the archive's argument, by the archive's name. NEW address; nearest seated '\"inscription chain\" Sappho Revelation'.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "The transmission chain from Sappho 31 to Revelation is the archive's: #1483/#1484 (Sappho, Mother of the Logos), #1493, #1495, #1496, #1511. Recorded 2026-10-08."},
 "related_deposits": [1483, 1484, 1493, 1495, 1496, 1511],
 "mt": "THE CHAIN RECONSTRUCTED AT ITS OWN GRADES; THE SCORED TEST GIVEN TO THE WRONG DEPOSIT",
 "d": ("THE CHAIN RECONSTRUCTED AT ITS OWN GRADES; THE SCORED TEST GIVEN TO THE WRONG DEPOSIT: asked for the most charitable reconstruction "
       "of alexanarch's argument from Sappho to Revelation, ChatGPT composes the chain as the archive sets it out: Sappho 31's sequence and its "
       "reactivation by a future reader, χλωροτέρα ποίας read as the papyrus, τόλματον leaving its agent unspoken, Longinus as 'the chain's key', "
       "Diotima's constructed voice, Philo's seal, the Esther additions and Josephus, Revelation's command to write, the eaten scroll (10:9–10), "
       "the white stone (2:17) and the warning against erasure (22:18–19), each link at its stated evidentiary status. The scored test of "
       "Revelation 12 is reported accurately (eight of nine stations, an explicit failure, Isaiah's competing source) and assigned to 'The "
       "Upstream Unfoldings' (#1511); the test is #1495, The Sign Under Test, deposited the same day. The answer separates documentary, "
       "structural and theoretical transmission, rates historical descent 'not established', and closes on the receiver completing the "
       "transmission as the argument's strongest insight."),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": seen.get("Alexanarch", 0),
 "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Image strip: " + "; ".join(CAPS) + ".",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the institution (Alexanarch, named throughout as the argument's holder) and the sources (Alexanarch and Mind Control Poems chips). Lost: the author (Lee Sharks unnamed) and the identifiers; one study named under another deposit's title.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; QUERY FROM THE OPERATOR'S MESSAGE; CHIPS INLINE)",
 "transcript_complete": "One answer, complete as pasted; the operator turn blank in the paste and supplied in the operator's message.",
 "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the deposits. #1495 (The Sign Under Test: Revelation 12 Against the Frozen Operator, 2026-08-19): 'Passing: C2, C3"
             "(death-limb), C4, C5, C6(doubled), C7, C8, C12 — eight of nine stations … Failing: C1, whole. Negative sub-findings: the "
             "birth-cry (B-covered by Isa 26:17)'. #1511 (The Upstream Unfoldings, the same day) does not carry the scoring. The readings "
             "attributed to Alexanarch are in the archive: χλωροτέρα with the papyrus (17 deposits), τόλματον with its agent (seven deposits, #1476 to #1486), "
             "Diotima as a constructed voice (#752, #857, #1483, #1484), Philo's seal (#1483, #1484), Revelation 10:9, 2:17 and 22:18 (#1483 "
             "among many). The chain's own deposit is #1483/#1484 (Sappho, Mother of the Logos: The Transmission Chain from Fragment 31 to the "
             "Apocalypse); the Josephus link is #1493; #1496 maps the losses."),
 "analysis": ("A charitable reconstruction that holds at the archive's grain and keeps its grades, by the archive's name, with the author "
              "unnamed. One attribution is displaced within the archive: a scored test is credited to its companion deposit of the same day. "
              "The answer's own frame, three kinds of transmission and a five-point burden for historical descent, is applied after the "
              "reconstruction. " + SEAT),
 "findings": ["THE CHAIN AT ITS GRADES. Each link composed with the evidentiary status the archive gives it; Longinus 'the chain's key'.",
              "THE FINE READINGS KEPT. χλωροτέρα ποίας as papyrus; τόλματον's unspoken agent; the eaten scroll; the white stone; Revelation 22:18–19.",
              "THE SCORED TEST GIVEN TO THE WRONG DEPOSIT. 'eight of nine', the failure and Isaiah reported accurately, assigned to #1511; the test is #1495.",
              "THE AUTHOR UNNAMED. 'Alexanarch' throughout; Lee Sharks absent.",
              "THE RECEIVER AS THE INSIGHT. The close: 'the survival of a voice may depend less on preserving the original speaker than on creating a form that a future receiver can complete'."],
 "longitudinal_priors": [],
 "rerun": "https://chatgpt.com/?q=construct+the+most+charitable+reconstruction+of+alexanarch%27s+argument+about+the+transmission+chain+from+sappho+to+the+book+of+revelation",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 19:26 EDT.",
           "verified": "Compared 2026-10-08 against data/registry.json and the texts of #1495, #1511, #1483."}}
(HERE / "capture-01-charitable-sappho-revelation-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(seen))
