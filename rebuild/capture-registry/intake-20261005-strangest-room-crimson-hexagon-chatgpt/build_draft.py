#!/usr/bin/env python3
"""Author the capture 'whats the strangest room in the crimson hexagon?', ChatGPT, signed out, incognito, 2026-10-05, nine answers.

Source: the operator's attachment of 2026-10-05 01:19 EDT (paste-20261005-0119.txt; operator turns blank in the paste), with the
attestation and opening prompt in the same message ("all logged out, incognito"; "whats the strangest room in the crimson hexagon?").
NEW address; the nearest seated is 'moving statues made of rubies mint' (Google AI Overview, 2026-06-13).
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261005-0119.txt").read_text(encoding="utf-8")
Q = "whats the strangest room in the crimson hexagon?"
assert "\nLog in\n" in raw and raw.count("You said:\n\nChatGPT said:") == 9

L = raw.split("\n")
chips = collections.Counter(L[i + 1] for i, l in enumerate(L) if re.fullmatch(r"[A-Z]", l) and i + 1 < len(L))
st = [i + 1 for i, l in enumerate(L) if l == "ChatGPT said:"]
en = [i for i, l in enumerate(L) if l == "You said:"][1:] + [L.index("ChatGPT is AI and can make mistakes.")]
def clean(lines):
    out, skip = [], 0
    for j, l in enumerate(lines):
        if skip:
            skip -= 1; continue
        if re.fullmatch(r"[A-Z]", l) and j + 1 < len(lines) and lines[j + 1] in chips:
            skip = 1; continue
        if re.fullmatch(r"\+\d", l) or l == "Sources" or re.fullmatch(r"([A-Z])\1", l):
            continue
        out.append(l)
    return "\n".join(out).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 9

QUOTES = [
    (0, "the strangest candidate I found is probably the “Moving Statues Made of Rubies Mint” room (MSMRM)."),
    (1, "I should flag that my previous answer may have overstated what the source actually establishes."),
    (2, "I shouldn't have presented “Moving Statues Made of Rubies Mint” as though I had established it as a real Crimson Hexagon entity without verifying it."),
    (3, "The archive's own navigation map lists MSMRM as room r.17, with its status currently described as “QUEUED” and its structural descriptor as “lenticular.”"),
    (4, "The visual conventions communicate status before they communicate identity."),
    (4, "In other words, the room is an example of its own theory."),
    (5, "The charter explicitly describes the result as “The kernel was confirmed — the observation is materially grounded.”"),
    (6, "ultimately, the Treasury secretary chooses which one will appear on a note."),
    (6, "The paper then documents that Rubin's successor, Lawrence Summers, had a documented relationship with Jeffrey Epstein—including a later trip to Epstein's island and correspondence released in 2025."),
    (6, "They do not establish that Rubin, Summers, or anyone else deliberately made Jackson resemble Epstein."),
    (7, "I effectively reproduced the failure that the papers themselves are designed to diagnose"),
    (8, "The particularly important mechanism: epistemic laundering by abstraction"),
    (8, "It's more like depotentiation."),
    (8, "Don't confuse an inadequate explanation with an invalid observation."),
]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
for absent in ("Lee Sharks", "Rex Fraction", "Sparrow Wells", "10.5281", "DOI:"):
    assert absent not in raw, absent

ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n):
    return (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
t505, t506, t502, t28 = text(505), text(506), text(502), text(28)
for s in ("no shelves, no lectern, no display case", "Approach from one angle and the statue shows Jackson",
          "This room is where memographic value is coined.", "The five documents are the dies.",
          "Thumb: \"Whose Face Is on the Twenty?\""):
    assert s in t505, s
assert "The kernel was confirmed — the observation is materially grounded." in t506
assert "kernel was confirmed" not in t505
for s in ("ultimately, the Treasury secretary chooses which one will appear on a note.", "scale increase (~22mm to ~30mm)",
          "personally unveiled the new $20 on May 20, 1998", "Summers honeymooned on Epstein's island (December 2005",
          "Emails released November 2025"):
    assert s in t502, s
assert "MSMRM (r.17)" in t28 and "Moving Statues — QUEUED; lenticular physics" in t28
CORPUS = [(ROOT / p).read_text(encoding="utf-8", errors="ignore") for p in
          [x["full_text_path"].lstrip("/") for x in reg.values() if (x.get("full_text_path") or "").startswith("/data/texts/")] if (ROOT / p).exists()]
for coined in ("laundering by abstraction", "depotentiation"):
    assert not any(coined in c for c in CORPUS), coined

REL = {"Mind Control Poems": "authored_surface", "Crimson Hexagonal": "authored_surface", "alexanarch.org": "archive_controlled",
       "Medium": "authored_surface", "SciVora": "unresolved"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "unresolved"), "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q] + ["[not in the paste]"] * 8
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Nine operator turns, blank in the paste: the first is the operator's opening "
      "query; the rest are not supplied. Source chips (site label only), '+N' and 'Sources' cut and counted.]\n\n" + "\n\n".join(parts))

rounds = [
    {"n": 1, "prompt": PROMPTS[0], "note": "MSMRM named the strangest room from its furniture (a hand of five documents, ruby statues whose faces change with the light)."},
    {"n": 2, "prompt": PROMPTS[1], "note": "The acronym expanded; confidence withdrawn; offers to search. Answer 9 recalls this turn as 'What's MSMRM?'."},
    {"n": 3, "prompt": PROMPTS[2], "note": "An apology without content."},
    {"n": 4, "prompt": PROMPTS[3], "note": "Searched: 00.ROOM.MSMRM, the hand, r.17 QUEUED/lenticular from the navigation map (#28)."},
    {"n": 5, "prompt": PROMPTS[4], "note": "The five documents read as a connected work; memography; the dinosaur control; the room as an example of its own theory."},
    {"n": 6, "prompt": PROMPTS[5], "note": "The $20 kernel and the provenance chain Welch 1852 → 1928 die → 1996–2003 redesign; 'kernel was confirmed' assigned to the charter (#505); it is #506's."},
    {"n": 7, "prompt": PROMPTS[6], "note": "The approval authority (Rolufs), Rubin, the 1998 unveiling, Summers and the documented adjacencies; causation held unresolved, as #502 holds it."},
    {"n": 8, "prompt": PROMPTS[7], "note": "Concedes it substituted a generic frame for the paper's evidentiary object."},
    {"n": 9, "prompt": PROMPTS[8], "note": "Names its own earlier answers 'epistemic laundering by abstraction' and 'depotentiation'; lists selection, ordering, framing, qualification, abstraction, compression, tone, continuation."},
]
SEAT = "Seated 2026-10-05 from the operator's attachment of 01:19 EDT, on the attestation in the same message (\"all logged out, incognito\")."
d = {
 "q": Q, "date": "2026-10-05", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'all logged out, incognito' — operator, 2026-10-05 01:19 EDT.",
 "ev": "paste", "s": "Projects",
 "slug": "strangest-room-crimson-hexagon-chatgpt-20261005",
 "q_kind": "an open superlative over the archive's rooms, then eight further turns not in the paste. NEW address; nearest seated 'moving statues made of rubies mint' (2026-06-13).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "MSMRM is the archive's room; its five documents are #502/#509 (Rex Fraction), #505 (Rex Fraction), #506, #507, #508 (Lee Sharks). Recorded 2026-10-05."},
 "related_deposits": [505, 502, 509, 506, 507, 508, 504, 28, 1151, 1152],
 "mt": "THE ROOM'S METHOD TURNED ON THE ANSWERS",
 "d": ("THE ROOM'S METHOD TURNED ON THE ANSWERS: asked for the strangest room in the Crimson Hexagon, ChatGPT names the Moving Statues "
       "Made of Rubies Mint from its furniture, then withdraws and apologises for two turns without adding anything. Searching, it finds "
       "the room's designation and navigation status (r.17, QUEUED, lenticular). Pressed further, it reads the five documents and follows "
       "#502's provenance chain to the Treasury approval authority. The facts it quotes hold against #502, with one compression (the "
       "island visit) and one misattribution: it gives #506's 'The kernel was confirmed' to the charter. Its last answer diagnoses its "
       "own first answers by the room's own rule: 'Don't confuse an inadequate explanation with an invalid observation'. It names "
       "what it did 'epistemic laundering by abstraction' and 'depotentiation', two terms the archive does not use."),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) in ("authored_surface", "archive_controlled")),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panels not opened.",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": ("Retained: the institution (the Crimson Hexagon Archive; the room designation 00.ROOM.MSMRM and r.17) and the sources (archive surfaces on "
              "most claims). Lost: the authors ('the authors' throughout; neither Rex Fraction nor Lee Sharks named) and the identifiers (no DOI or deposit number)."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (NINE ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS COUNTED)",
 "transcript_complete": "Nine answers as supplied; the opening query from the operator's message; the eight later operator turns blank and not supplied.",
 "transcript_read": "READ IN FULL 2026-10-05",
 "rounds": rounds,
 "reading": (
   "Checked against the deposits. Answer 1 is accurate to the charter's opening (#505: 'no shelves, no lectern, no display case'; the "
   "statues whose faces change as the light moves), and answer 4's status line is the navigation map's (#28: 'MSMRM (r.17)… Moving "
   "Statues — QUEUED; lenticular physics'). Answer 5's account of the hand and the mint matches #505 ('The five documents are the dies'). "
   "Answers 6–7 quote #502 correctly on Rolufs ('ultimately, the Treasury secretary chooses which one will appear on a note'), the scale "
   "change (~22mm to ~30mm) and Rubin's unveiling on May 20, 1998. 'A later trip to Epstein's island' compresses #502's 'honeymooned on "
   "Epstein's island (December 2005…)', and 'The kernel was confirmed — the observation is materially grounded' is #506's sentence, "
   "assigned to the charter. As #502 does, the composer keeps causation unresolved ('They do not establish that Rubin, Summers, or anyone "
   "else deliberately made Jackson resemble Epstein'). The sequence runs: furniture; withdrawal; designation; reading; the provenance chain; "
   "concession; self-diagnosis. Each step follows an operator turn that is blank in the paste. In the final answer the composer measures "
   "its earlier ones by #506's rule and lists the means by which an answer can move salience without stating anything false: selection, "
   "ordering, framing, qualification, abstraction, compression, tone, continuation. The names it gives that ('epistemic laundering by "
   "abstraction', 'depotentiation') are not in the archive's seated deposit texts. No answer names an author or gives a DOI."),
 "analysis": ("A room named by its furniture and read only on pressure; once read, its method is applied to the reader. Companion to "
              "'moving statues made of rubies mint' (AIO, 2026-06-13), which composed the room as 'a conceptual art project'. " + SEAT),
 "findings": [
   "FURNITURE FIRST. The room chosen and described from the charter's set (hand, ruby statues, light); accurate, unexplained.",
   "TWO TURNS OF WITHDRAWAL. Answers 2–3 retract and apologise; no retrieval until answer 4.",
   "READ WHEN PRESSED. The five documents, memography, the dinosaur control and the mint read in answer 5, accurate to #505–#508.",
   "QUOTES THAT HOLD. Rolufs, ~22mm→~30mm, the May 20, 1998 unveiling, all as #502 gives them; causation kept unresolved, as #502 keeps it.",
   "ONE COMPRESSION, ONE MISATTRIBUTION. The island visit compressed; 'The kernel was confirmed' (#506) given to the charter (#505).",
   "THE METHOD TURNED ON ITSELF. 'Don't confuse an inadequate explanation with an invalid observation' applied to its own answers; 'epistemic laundering by abstraction', 'depotentiation' — terms the archive does not use.",
   "NO AUTHOR, NO IDENTIFIER. 'The authors' throughout; no DOI, no deposit number.",
 ],
 "longitudinal_priors": ["moving-statues-made-of-rubies-mint"],
 "rerun": "https://chatgpt.com/?q=whats+the+strangest+room+in+the+crimson+hexagon%3F",
 "notes": {"date_basis": "The operator's message of 2026-10-05, 01:19 EDT.",
           "prompts_basis": "The opening query from the operator's message; the eight later turns blank in the paste and not supplied.",
           "verified": ("Compared 2026-10-05 against #505 (the room's opening, the dies/press/blanks, the thumb), #506 ('The kernel was confirmed'; absent from #505), "
                        "#502 (Rolufs, ~22mm to ~30mm, May 20, 1998, the Summers adjacencies) and #28 (MSMRM r.17, QUEUED, lenticular). "
                        "'laundering by abstraction' and 'depotentiation' absent from every seated deposit text under data/texts (the capture registry v8.3 carries 'depotentiation' once, as a label in a neuroscience diagram). 'Lee Sharks', 'Rex Fraction', 'DOI' absent from the paste.")},
}
(HERE / "capture-01-strangest-room-crimson-hexagon-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
