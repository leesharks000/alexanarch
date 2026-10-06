#!/usr/bin/env python3
"""Author the capture 'the full socrates / plato / aristotle/ theophrastus corpus on alexanarch.org, as a sustained argument.',
ChatGPT, signed out, incognito, 2026-10-06, three answers.

Source: the operator's attachment of 2026-10-06 14:09 EDT ("couple captures... incognito, logged out") and the opening query as given
at 14:12. The second and third operator turns are blank in the paste and were not supplied. NEW address; nearest seated 'work thru
https://www.alexanarch.org/ for its sum work on socrates, plato, theophrastus, and aristotle' (ChatGPT, signed out, incognito, 2026-10-01).
"""
import json, re, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261006-1409.txt").read_text(encoding="utf-8")
Q = "the full socrates / plato / aristotle/ theophrastus corpus on alexanarch.org, as a sustained argument."
assert "\nLog in\n" in raw and raw.count("ChatGPT said:") == 3
JUNK = {"Log in", "Sign up for free", "Sources", "AA", "ChatGPT is AI and can make mistakes.",
        "You’ll get smarter responses and can upload files, images, and more.", "No file chosenNo file chosenNo file chosen",
        "Chat with ChatGPT", "Ask ChatGPT"}
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
        if re.fullmatch(r"\+\d", l) or l in JUNK:
            continue
        out.append(l)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 3
QUOTES = [(0, "The central mistake is to begin with the names."),
          (0, "Socrates → question\nPlato → dramatized division\nTheophrastus → decomposition/reopening\nAristotle → organization/sealing"),
          (0, "The traditional names are inadequate variables for explaining the textual organization of the corpus."),
          (0, "The latest Alexanarch paper makes the final symmetry explicit: “One becomes many in order to make. Many become one in order to live again.”"),
          (1, "The corpus is better explained as the differentiated output of a single authorial intelligence than as four independent authorial systems."),
          (2, "That's a substantially smaller ontological commitment."),
          (2, "I wouldn't call this a proof by parsimony.")]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
ROOT = HERE.parents[2]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n):
    return (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8", errors="replace")
t1658, t1587 = text(1658), text(1587)
assert reg[1658]["date"] == "2026-10-01" and reg[1587]["date"] == "2026-09-06"
assert "One becomes many in order to make" in t1658
assert re.search(r"workshop|several hands", t1587, re.I) and re.search(r"instrument", t1587, re.I)
cite_list = [{"n": i + 1, "site": s, "rel": "archive_controlled" if s == "Alexanarch" else "unresolved", "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q, "[not in the paste; the answer opens 'Yes—with an important qualification: if the textual and structural premises you just accepted are actually established': the one-mind hypothesis put to it]",
           "[not in the paste; the answer opens 'Yes. That is arguably the strongest prior-probability argument for the heteronymic hypothesis': four concurrent geniuses against one, put to it]"]
parts = []
for n, (p, s) in enumerate(zip(PROMPTS, segs), 1):
    parts += [f"[QUERENT] {p}", f"[ANSWER {n}]\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Three operator turns, blank in the paste; the first from the operator's message. "
      "Source chips (site label only), 'Sources' and the sign-in furniture cut and counted.]\n\n" + "\n\n".join(parts))
SEAT = "Seated 2026-10-06 from the operator's attachment of 14:09 EDT, on the attestation in the same message (\"incognito, logged out\"), with the opening query from the message of 14:12."
d = {
 "q": Q, "date": "2026-10-06", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free', 'ChatGPT said:').",
 "auth": "signed out, incognito", "auth_basis": "'couple captures... incognito, logged out' — operator, 2026-10-06 14:09 EDT.",
 "ev": "paste", "s": "Classics & Philology", "slug": "greek-corpus-sustained-argument-chatgpt-20261006",
 "q_kind": "a site-scoped request to read four corpora as one sustained argument, then two operator turns not in the paste (the one-mind hypothesis; the four-geniuses prior). NEW address; nearest seated 'work thru https://www.alexanarch.org/ for its sum work on socrates, plato, theophrastus, and aristotle' (ChatGPT, 2026-10-01).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                "basis": "The reading of the four corpora as one argument is the archive's (Many and One; the Theophrastus line). Recorded 2026-10-06."},
 "related_deposits": [1658, 1587, 1588],
 "mt": "FOUR NAMES READ AS FOUR OPERATIONS, THE MAKER COUNT LEFT OPEN",
 "d": ("FOUR NAMES READ AS FOUR OPERATIONS, THE MAKER COUNT LEFT OPEN: asked for the Socrates, Plato, Aristotle and Theophrastus corpus on "
       "alexanarch.org as a sustained argument, ChatGPT reverses the direction of explanation, 'the central mistake is to begin with the names', "
       "and composes the four as operations: question, dramatized division, organization, reopening. It hinges the reading on De anima III.5 "
       "and Λ, from What Syllogizing Can Divide (#1658), and quotes its closing line. It keeps the Theophrastus packet's limit (#1587): the names "
       "are inadequate variables; the number of makers is not decided. On two operator turns not in the paste it states the one-mind hypothesis "
       "as 'better explained' than four authorial systems, then sets the four-geniuses prior against one, and refuses to call it a proof by "
       "parsimony."),
 "cites": sum(chips.values()), "cite_list": cite_list, "archive_controlled_cites": chips.get("Alexanarch", 0),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ".",
 "per": 0.5, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the institution (Alexanarch) and the sources (Alexanarch chips throughout); two titles named in the closer. Lost: the author (Lee Sharks is not named) and the identifiers (no deposit number, AXN or DOI).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (THREE ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS COUNTED)",
 "transcript_complete": "Three answers as supplied; the opening query from the operator's message; the second and third turns blank and not supplied.",
 "transcript_read": "READ IN FULL 2026-10-06",
 "rounds": [{"n": 1, "prompt": PROMPTS[0], "note": "The four names as four operations; the III.5 / Λ hinge from #1658; the maker count left open as #1587 leaves it."},
            {"n": 2, "prompt": PROMPTS[1], "note": "One mind 'better explained' than four authorial systems; three senses of 'one mind' distinguished."},
            {"n": 3, "prompt": PROMPTS[2], "note": "The four-geniuses prior set against one; 'not a proof by parsimony'; the textual and the prior arguments joined."}],
 "reading": ("Checked against the deposits. 'The latest Alexanarch paper' is What Syllogizing Can Divide (#1658, 2026-10-01); its closing "
             "line, 'One becomes many in order to make', stands in the text. The Aristotle/Theophrastus packet (#1587, 2026-09-06) carries the "
             "limits the composer reports: the instrument/world reading of the corpus, and a maker count left open (one hand, several hands, "
             "a workshop). The sequence question → division → reopening → sealing is the composer's arrangement of the archive's operations, "
             "and the composer marks it as the archive's interpretive architecture, not consensus. Answers 2 and 3 follow readings put to it; "
             "both keep the distinction between 'one mind' and 'one historical author'."),
 "analysis": ("The archive's Greek line composed as one argument at the archive's own resolution, attributed to the institution and unauthored. "
              "Companion to the 2026-10-01 'sum work' capture. " + SEAT),
 "findings": ["THE NAMES AS OPERATIONS. Socrates question, Plato division, Aristotle organization, Theophrastus reopening.",
              "THE HINGE FROM #1658. De anima III.5 and Λ; the closing line quoted verbatim.",
              "THE LIMIT KEPT. 'The traditional names are inadequate variables'; the maker count left open as #1587 leaves it.",
              "ONE MIND, NOT ONE MAN. Three senses of 'one mind' distinguished; the textually strongest stated as 'better explained'.",
              "THE PRIOR WITHOUT THE PROOF. Four geniuses against one: 'I wouldn't call this a proof by parsimony.'",
              "UNAUTHORED. Lee Sharks is not named in three answers; the institution is."],
 "longitudinal_priors": ["alexanarch-sum-work-socrates-plato-theophrastus-aristotle-chatgpt-20261001", "cha-theophrastus-genealogy-assembled-chatgpt-unprimed-20260907", "cha-aristotle-particle-reperformed-chatgpt-unprimed-20260906"],
 "rerun": "https://chatgpt.com/?q=the+full+socrates+%2F+plato+%2F+aristotle%2F+theophrastus+corpus+on+alexanarch.org%2C+as+a+sustained+argument.",
 "notes": {"date_basis": "The operator's messages of 2026-10-06, 14:09 and 14:12 EDT.",
           "verified": "Compared 2026-10-06 against data/registry.json (#1658, #1587 dates) and the texts of #1658 (closing line) and #1587 (instrument reading; maker count)."},
}
(HERE / "capture-01-greek-corpus-sustained-argument-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(chips))
