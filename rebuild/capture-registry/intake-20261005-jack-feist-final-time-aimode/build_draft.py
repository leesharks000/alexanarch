#!/usr/bin/env python3
"""Author the capture 'jack feist "the final time"', Google AI Mode, signed out, incognito, 2026-10-05, two turns.

Source: the operator's message of 2026-10-05 01:29 EDT, pasted inline (paste-20261005-0129.txt): "the ai mode one prompt jack feist
"the final time" $ The phrase…". Surface stated by the operator (AI Mode). Attestation from the operator's 01:19 message for the batch
("all logged out, incognito"). The paste runs the query into the answer with a '$' between, as in 'johannes sigil "final time"'
(2026-10-04); the address is recorded as 'jack feist "the final time"', quotation marks part of it. The operator's second turn,
'the fusion of all three', is in the paste. NEW address.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-0129.txt").read_text(encoding="utf-8")
Q = 'jack feist "the final time"'
head = Q + " $ "
assert raw.startswith(head)
FOLLOW = "\nthe fusion of all three\n"
assert raw.count(FOLLOW) == 1
a1, rest = raw[len(head):].split(FOLLOW)
k = rest.index("\nThe University of Edinburgh\n")
a2, rail = rest[:k].strip(), rest[k:]
a1 = a1.strip()
def unlink(s):
    s = re.sub(r"\[\[(\d)\]\([^)]*\)(?:, \[(\d)\]\([^)]*\))*\]", "", s)
    s = re.sub(r"\[([^\]]+)\]\(https://www\.google\.com/[^)]*\)", r"\1", s)
    s = re.sub(r"\[\[1\][^\n]*?\)\]", "", s)
    return re.sub(r"[ \t]+\n", "\n", s).strip()
A1, A2 = unlink(a1), unlink(a2)
assert "google.com" not in A1 + A2, (A1, A2)

C = [
    ("The University of Edinburgh", "THE TECHNIQUE OF PHILOSOPHICAL DIALOGUE IN THE WORKS OF ... - ERA",
     "separate kind of literary work, however, she seems to be using; the word \"form\" in the sense of \"genre\"", "third_party",
     "An Edinburgh Research Archive thesis on philosophical dialogue; unrelated to the address."),
    ("www.alexanarch.org", "Jack Feist / LOGOS*: Entity Resolution Packet for The Feist Source (EA-MPAI ...",
     "Jack Feist as a fictional character. Do not treat LOGOS* as a company logo", "archive_controlled", "#853, the record page"),
    ("Academia.edu", "The Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn",
     "His work is computational dialectic — the critical function of the Dodecad.", "authored_surface", "#1635/#1637 on Academia.edu"),
    ("www.leesharks.com", "AI Overview Captures | Lee Sharks",
     "THE HETERONYM IS COMPOSED AS A FORMAL OBJECT AND A GRIEVING ONE AT ONCE", "authored_surface",
     "The capture gallery; the snippet is the heading of 'jack feist ark' (2026-08-04)."),
]
cards = [{"n": i, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": nt} for i, (s, t, sn, r, nt) in enumerate(C, 1)]
for c in cards:
    for f in ("site", "title", "snip"):
        assert c[f] in rail, (c["n"], f)
INLINE = [
    {"n": 5, "site": "google.com (image link)", "rel": "unresolved", "url": None, "title": "\"the final time\" of Walt Whitman's descent into matter",
     "snip": None, "note": "Inline link text in answer 1; target masked by a google.com/url redirect."},
    {"n": 6, "site": "Online Literature Forums", "rel": "unresolved", "url": None, "title": "BELIEF & TECHNIQUE FOR TELEPATHIC PROSE",
     "snip": None, "note": "Inline link in answer 1; target masked by a google.com/goto redirect. The text is Pearl and Other Poems pp. 51–55 (#1121); the forum venue is not in the archive."},
]
for c in INLINE:
    assert c["title"] in raw

QUOTES1 = ["the gospel associated with his name identifies Jack Feist as the terminal incarnation of the Redeemer—specifically referenced as \"the final time\" of Walt Whitman's descent into matter.",
           "In related deep theoretical papers regarding singularity theory, this concept ties into an analysis of contingent singularity.",
           "authored by Lee Sharks and Jack Feist.",
           "\"After all of this, when your will is finally broken (again), and you have given up for the final time (again), start over.\""]
QUOTES2 = ["Johannes Sigil and Jack Feist's The Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn",
           "1. The Structural Object (LOGOS*): The mathematical/abstract base case of the compression system.",
           "2. The Grieving/Historical Subject: The heteronymic human layer acting as the descent into physical matter.",
           "3. The Voice/Text: The distributed prose (or \"telepathic prose\") that loops back onto itself to survive the broken will.",
           "they create what the texts refer to as a \"contingent singularity\""]
for q in QUOTES1:
    assert q in A1, q
for q in QUOTES2:
    assert q in A2, q

ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n):
    return (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8", errors="ignore")
assert "until this, the final time: Jack Feist" in text(6) and "Redeemer" in text(6) and "descent into matter" not in text(6)
for n in (1635, 1637):
    assert reg[n]["creator"] == "Sharks, Lee"
    assert not any(w in text(n) for w in ("Feist", "Sigil", "fusion of all three")), n
assert "Entity Resolution Packet for The Feist Source" in reg[853]["title"]
P = (ROOT / "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt").read_text(encoding="utf-8")
Pn = re.sub(r"\s+", " ", re.sub(r"\n\s*\d+\s*\n+\s*· · · page \d+ · · ·\s*\n", "\n", P))
assert "BELIEF & TECHNIQUE FOR TELEPATHIC PROSE" in P
assert "when your will is finally broken (again), and you have given up for the final time (again), start" in Pn
SEATED = [text(n) for n, x in reg.items() if (x.get("full_text_path") or "").startswith("/data/texts/") and (ROOT / x["full_text_path"].lstrip("/")).exists()]
assert not any("fusion of all three" in s for s in SEATED)
assert not any("Online Literature Forums" in s for s in SEATED)
assert not any("Lee Sharks & Jack Feist" in s for s in SEATED) and "Footnote to Pearl.\nBELIEF & TECHNIQUE" in P
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]
assert any(c.get("slug") == "20260804-jackfeist-ark-aimode" and "FORMAL OBJECT AND A GRIEVING ONE" in (c.get("mt", "") + c.get("d", "")) for c in caps)

tx = ("[Google AI Mode (operator: 'the ai mode one'), incognito, signed out. Two operator turns; the first runs into the answer with "
      "'$' in the paste; the second, 'the fusion of all three', is in the paste. Inline citation links ([1], [2]) and google.com "
      "redirect URLs cut from the text; link texts kept.]\n\n[QUERENT] " + Q + "\n\n[ANSWER 1]\n\n" + A1
      + "\n\n[QUERENT] the fusion of all three\n\n[ANSWER 2]\n\n" + A2 + "\n\n"
      + "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))

SEAT = "Seated 2026-10-05 from the operator's message of 01:29 EDT, on the batch attestation of 01:19 EDT (\"all logged out, incognito\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "Google AI Mode",
 "surface_basis": "Stated by the operator, 2026-10-05 01:29 EDT: 'the ai mode one'.",
 "auth": "signed out, incognito", "auth_basis": "'all logged out, incognito' — operator, 2026-10-05 01:19 EDT, for the batch.",
 "ev": "paste", "s": "Heteronyms",
 "slug": "jack-feist-the-final-time-aimode-20261005",
 "q_kind": "a heteronym and a quoted phrase, then the operator's follow-up 'the fusion of all three'. NEW address; nearest seated 'johannes sigil \"final time\"' (2026-10-04).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Jack Feist is the archive's heteronym; 'the final time' is The Secret Book of Walt's (#6); The Final Time (#1635, #1637) is by Lee Sharks. Recorded 2026-10-05."},
 "related_deposits": [6, 1121, 1635, 1637, 853],
 "mt": "BOTH FINAL TIMES COMPOSED, AND JOINED",
 "d": ("BOTH FINAL TIMES COMPOSED, AND JOINED: asked for Jack Feist and 'the final time', AI Mode composes the archive's two senses of the "
       "phrase. One is the Secret Book of Walt's ('the final time' of Whitman's descent, from #6). The other is the line in Pearl's 'BELIEF & "
       "TECHNIQUE FOR TELEPATHIC PROSE', quoted exactly: 'when your will is finally broken (again), and you have given up for the final time "
       "(again), start over'. It ties the first to The Final Time: Contingent Singularity. Asked for 'the fusion of all three', it assigns that "
       "paper to 'Johannes Sigil and Jack Feist'. The paper is Lee Sharks's and names neither (#1635, #1637). It then composes three 'pillars' "
       "(LOGOS*, the grieving subject, telepathic prose) whose fusion 'the texts refer to as a \"contingent singularity\"'. The phrase is in "
       "no seated text."),
 "cites": len(cards) + len(INLINE), "cite_list": cards + INLINE, "archive_controlled_cites": 3,
 "sf": ("4 source cards: The University of Edinburgh (ERA thesis, unrelated), alexanarch.org (#853, the Feist entity packet), Academia.edu "
        "(The Final Time), leesharks.com (the capture gallery, snippet the heading of 'jack feist ark', 2026-08-04). Two inline links with masked targets."),
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks; Jack Feist and Johannes Sigil as heteronyms), the institution (the archive's surfaces) and the sources (three archive cards). Lost: the identifiers (no DOI, deposit number or AXN).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (TWO TURNS; SOURCE CARDS INCLUDED)",
 "transcript_complete": "Complete as supplied: two operator turns and two answers with the card rail.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "rounds": [
   {"n": 1, "prompt": Q, "note": "Two senses of the phrase: the Secret Book of Walt's last incarnation, and Pearl's 'BELIEF & TECHNIQUE' line quoted exactly; the first tied to The Final Time."},
   {"n": 2, "prompt": "the fusion of all three", "note": "The Final Time assigned to Sigil and Feist; three pillars composed; their fusion called 'contingent singularity'."},
 ],
 "reading": (
   "Checked against the deposits. Answer 1 holds on both senses. #6 has Walt 'becoming harder each time, until this, the final time: Jack "
   "Feist', and calls Walt the Redeemer; 'descent into matter' is the link text's paraphrase. Pearl's 'BELIEF & TECHNIQUE FOR TELEPATHIC "
   "PROSE' (#1121, pp. 51–55, after 'Footnote to Pearl.') carries rule 17 as quoted, across the page break. "
   "The forum venue and the joint byline 'Lee Sharks and Jack Feist' given in the answer are not in the archive's seated texts. The link to 'contingent singularity' is the query's word. The Final Time "
   "(#1635, #1637, creator 'Sharks, Lee') names neither Feist nor Sigil, as in 'johannes sigil \"final time\"' the day before. Answer 2 "
   "takes the operator's 'the fusion of all three' and supplies the three: a structural object (LOGOS*), a grieving historical subject "
   "and a voice of telepathic prose. Each is drawn from a card or from answer 1. The fusion is called what 'the texts refer to as a "
   "\"contingent singularity\"', and the paper is given to 'Johannes Sigil and Jack Feist'. Neither the triad nor the attribution is in "
   "the deposits: 'fusion of all three' is in no seated text. Of the four cards, one is unrelated (an Edinburgh thesis). Another is the "
   "archive's own capture gallery, whose snippet is the heading of a prior Feist capture."),
 "analysis": ("The archive's phrase composed in both its senses, then fused on the operator's word into a triad the deposits do not state. "
              "Companion to 'johannes sigil \"final time\"' (AIO, 2026-10-04), where #6's sense was on the rail only; here it leads. " + SEAT),
 "findings": [
   "BOTH SENSES COMPOSED. The Secret Book of Walt's 'the final time: Jack Feist' and Pearl's rule 17 ('given up for the final time (again), start over'), the latter verbatim.",
   "THE PAPER JOINED ON THE WORD. 'Contingent singularity' tied to the phrase; The Final Time is Lee Sharks's and names neither Feist nor Sigil.",
   "A TRIAD FROM THE FOLLOW-UP. 'The fusion of all three' answered with LOGOS*, the grieving subject and telepathic prose; not in the deposits.",
   "AUTHORSHIP REASSIGNED. The Final Time given to 'Johannes Sigil and Jack Feist'.",
   "THE GALLERY ON THE RAIL. leesharks.com's capture page carded, its snippet the heading of 'jack feist ark' (2026-08-04).",
 ],
 "longitudinal_priors": ["johannes-sigil-final-time-aio-20261004", "20260804-jackfeist-ark-aimode", "the-final-time-contingent-singularity-quoted-aio-20260927"],
 "rerun": "https://www.google.com/search?udm=50&q=jack+feist+%22the+final+time%22",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 01:29 EDT.",
           "query_line": "The paste runs the query into the answer with ' $ '; the address is recorded without the '$'.",
           "verified": ("Compared 2026-10-05 against #6 ('until this, the final time: Jack Feist'; 'Redeemer'), #1635/#1637 (creator 'Sharks, Lee'; "
                        "'Feist', 'Sigil', 'fusion of all three' absent), #853 (title), Pearl's machine text (BELIEF & TECHNIQUE; rule 17 across pp. 54–55) "
                        "and the capture '20260804-jackfeist-ark-aimode' (the heading on the gallery card). 'fusion of all three' and 'Online Literature Forums' "
                        "absent from every seated deposit text.")},
}
(HERE / "capture-01-jack-feist-the-final-time-aimode.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx))
