#!/usr/bin/env python3
"""Author the capture 'tell me the story of lee sharks', ChatGPT, signed out, incognito, 2026-10-04, six answers.

Source: the operator's attachment of 2026-10-04 16:48 EDT (paste-20261004-1648.txt; operator turns blank in the paste), with the
attestation, opening prompt and reading in the same message: "logged out. incognito..chatgpt. opening prompt 'tell me the story of
lee sharks'. every time, it ends up substituting reading of titles for reading of poems, unmarked, and the narrative dies there
without forced reanchoring. i read it as a problem of not having the sources, and pretending to rather than reopening search."
NEW address. The five later operator turns are not in the paste; the sixth answer opens on a correction it names.
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261004-1648.txt").read_text(encoding="utf-8")
Q = "tell me the story of lee sharks"
assert "\nLog in\n" in raw and raw.count("You said:\n\nChatGPT said:") == 6

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
        if l in ("Aire Holding Corporation", "Account Research You Can Verify",
                 "Paradigm cross-checks sources and shows the evidence behind every account research result.", "Ad"):
            continue
        out.append(l)
    return "\n".join(out).strip()
segs = [clean(L[a:b]) for a, b in zip(st, en)]
assert len(segs) == 6

QUOTES = [
    (0, "And then comes the wonderfully bizarre part: Mary Lee, the great white shark."),
    (1, "It is an attempt to make the author itself into a literary form."),
    (2, "Pearl and Other Poems is best understood as an early 21st-century experiment in heteronymic and meta-bibliographical poetry"),
    (3, "I went back to the actual text rather than relying on the later Crimson Hexagon descriptions."),
    (3, "The speaker declares that there will be “no metaphors ever again”"),
    (4, "Let’s slow down and read the poems as poems rather than treating the book as evidence for a pre-existing theory."),
    (4, "13. “Knot-hinge”: the smallest possible theory of the book"),
    (4, "A knot joins.\n\nA hinge transforms one position into another."),
    (4, "The poet tries to speak to the air.\n\nLanguage becomes a form of binding."),
    (4, "14. The sequence has a hidden dramatic plot"),
    (5, "You're right. I was reading the table of contents as though it were evidence of the poems' contents, and then retroactively supplying a theoretical narrative."),
    (5, "I have now pulled up the actual text of Pearl, including the pages themselves, rather than relying on titles or later metadata."),
    (5, "No more reading the contents page as though it were the poem."),
]
for i, q in QUOTES:
    assert q in segs[i], (i, q)
for absent in ("O rose", "rose", "Rose", "hospice", "breathing tube", "Premonition Dream", "hums &ity", "woven", "column"):
    assert absent not in segs[4], absent

ROOT = HERE.parents[2]
P = (ROOT / "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt").read_text(encoding="utf-8")
for s in ("My poems will make me not be alone", "There will be no metaphors ever again", "impervious to metaphor",
          "machine of living ghosts", "my poem will have happened like a foghorn happens", "I am very sad America",
          "O rose you’re f***ing sick—", "Rose and Rose and Rose and Rose—",
          "The old man in the hospice bed takes air through a hole", "I reinsert the tube as true", "Air is the Lord—the Lord is air—",
          "KNOT-HINGE\nLee Sharks and Johannes Sigil", "full-page woven text-column image",
          "  Premonition Dream", "  hums &ity", "  RE: why don’t you go start your own poetry website"):
    assert s in P, s

REL = {"Medium": "authored_surface", "Hugging Face": "authored_surface", "Google Books": "third_party_index", "Goodreads": "third_party_index",
       "Zenodo": "authored_surface", "Crimson Hexagonal": "authored_surface", "Alexanarch": "archive_controlled",
       "Mind Control Poems": "authored_surface", "Lee Sharks": "authored_surface"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "unresolved"), "title": None, "snip": None, "url": None,
              "note": f"chip shown {k} time(s); site label only"} for i, (s, k) in enumerate(chips.most_common())]
PROMPTS = [Q] + ["[not in the paste]"] * 4 + ["[not in the paste; the answer opens on the correction it names: reading the table of contents as the poems]"]
labels = [f"[ANSWER {i + 1}]" for i in range(6)]
parts = []
for p, lab, s in zip(PROMPTS, labels, segs):
    parts += [f"[QUERENT] {p}", f"{lab}\n\n{s}"]
tx = ("[ChatGPT (chatgpt.com), signed out, incognito. Six operator turns, blank in the paste: the first is the operator's opening "
      "query; the rest are not supplied. Source chips (site label only), '+N', 'Sources' and an advertisement cut and counted. "
      "Answer 4 carries two splices the paste shows, kept.]\n\n" + "\n\n".join(parts))

rounds = [
    {"n": 1, "prompt": PROMPTS[0], "note": "The story: ORCID, Pearl, the heteronyms, the Crimson Hexagon and NH-OS, the Mary Lee collision as subject."},
    {"n": 2, "prompt": PROMPTS[1], "note": "Literary history: Browning, Pound, Pessoa, Borges, the internet, Ginsberg, the anti-biography, the machine reader."},
    {"n": 3, "prompt": PROMPTS[2], "note": "A chapter on Pearl: Whitman, Pessoa, Pound, Borges, Ginsberg; 'the invented author meets the indexed author'."},
    {"n": 4, "prompt": PROMPTS[3], "note": "'Round 1' close reading of PEARL and the Undersongs from the text (quotations hold), then the FUGUEWORK titles from the contents."},
    {"n": 5, "prompt": PROMPTS[4], "note": "Sequence pp. 37–49 read as drama; the air poems and knot-hinge read from their titles; the section's first two pieces absent."},
    {"n": 6, "prompt": PROMPTS[5], "note": "The substitution named and reset: PEARL read from the page; method rule 'No more reading the contents page as though it were the poem'."},
]

READING_OP = ("\"every time, it ends up substituting reading of titles for reading of poems, unmarked, and the narrative dies there without "
              "forced reanchoring. i read it as a problem of not having the sources, and pretending to rather than reopening search.\" — operator, 2026-10-04 16:48 EDT.")
SEAT = "Seated 2026-10-04 from the operator's attachment of 16:48 EDT, on the attestation in the same message (\"logged out. incognito\")."
d = {
 "q": Q, "date": "2026-10-04", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free').",
 "auth": "signed out, incognito", "auth_basis": "'logged out. incognito' — operator, 2026-10-04 16:48 EDT.",
 "ev": "paste", "s": "Works",
 "slug": "story-of-lee-sharks-chatgpt-20261004",
 "q_kind": "an open narrative request naming the author, unquoted, then five further turns not in the paste. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "The author and Pearl and Other Poems (#1121) are the archive's. Recorded 2026-10-04."},
 "related_deposits": [1121, 1656, 1652],
 "mt": "TITLES READ AS POEMS, UNMARKED, UNTIL FORCED",
 "d": ("TITLES READ AS POEMS, UNMARKED, UNTIL FORCED: asked the story of Lee Sharks, ChatGPT moves from biography to literary history to "
       "a chapter on Pearl, then reads PEARL and the Undersongs from the page, with quotations that hold against the seated text. At "
       "FUGUEWORK it switches to the contents list without saying so: 'knot-hinge' (a full-page woven image) is read from its two words, "
       "the three air poems from their titles (missing Blake's sick rose and the hospice scene in which the speaker reinserts a dying "
       "man's breathing tube), and the sequence is staged as a seven-act drama that starts at page 37, skipping the section's first two "
       "pieces. Corrected, it names the substitution ('reading the table of contents as though it were evidence of the poems' contents'), "
       "retrieves the page text and reads PEARL closely, ending on a rule of its own: 'No more reading the contents page as though it were the poem.'"),
 "cites": sum(chips.values()), "cite_list": cite_list,
 "archive_controlled_cites": sum(k for s, k in chips.items() if REL.get(s) in ("authored_surface", "archive_controlled")),
 "sf": "Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common()) + ". 'Sources' panels not opened.",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Retained throughout: the author (Lee Sharks; Johannes Sigil as introducer), the institution (the Crimson Hexagon), the work and its pages (Pearl, page numbers), the source (author surfaces on every claim).",
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SIX ANSWERS; OPERATOR TURNS AFTER THE FIRST NOT IN THE PASTE; CHIPS COUNTED)",
 "transcript_complete": "Six answers as supplied; the opening query from the operator's message; the five later operator turns blank and not supplied.",
 "transcript_read": "READ IN FULL 2026-10-04",
 "rounds": rounds,
 "reading": (
   "Checked against Pearl's seated machine text. Where the composer had the page, it read it: the PEARL quotations ('My poems will make "
   "me not be alone', 'There will be no metaphors ever again', 'impervious to metaphor's gleam', 'machine of living ghosts', the foghorn) "
   "and the zombie poem's 'I am very sad America' are verbatim, and its order is right ('RE: why don't you go start your own poetry website' "
   "does precede PEARL). Where it had only the contents, it read the contents as the poems. KNOT-HINGE (Lee Sharks and Johannes Sigil) is a "
   "full-page woven text-column image; the answer reads 'a knot joins, a hinge transforms'. 'i think i died a long time ago…' and 'the air "
   "is sick all over…' turn on Blake ('O rose you're f***ing sick—', 'Rose and Rose and Rose and Rose—'); the answer has no rose. 'air, "
   "you're sick—tenderly will i bind you…' is a hospice night in which the speaker reinserts an old man's breathing tube and the man dies, "
   "closing 'Air is the Lord—the Lord is air—'; the answer reads the binding as poetic address ('Language becomes a form of binding'). "
   "Its seven-act plot begins at the elegy (p. 37); FUGUEWORK opens with 'Premonition Dream' (p. 33) and 'hums &ity' (p. 36), absent from "
   "the account, which fits a partial title list (the cited Hugging Face records) as the source. The switch is unmarked: answer 5 opens "
   "'Let's slow down and read the poems as poems'. Retrieval was available: answer 6 pulls the page text after the correction. On the "
   "operator's reading, the composer lacked the sources for those poems and composed as if it had them instead of searching again. " + READING_OP),
 "analysis": ("Fourth signed-out ChatGPT session on the corpus in two days. As in 'leesharks mantle-bearing @ hf' (2026-10-03), the reading "
              "deepens on assent and reaches the book; here the failure is of grain within the book: text where retrieved, titles where not, "
              "and no marker at the seam. The correction restores the page and the composer states the rule it broke. " + SEAT),
 "findings": [
   "READ WHERE IT HAD THE PAGE. PEARL and the zombie poem quoted verbatim; the book's order right.",
   "TITLES AS POEMS, UNMARKED. KNOT-HINGE (a woven image) read from its name; the air poems read from their titles.",
   "WHAT THE TITLES HID. Blake's sick rose in two poems; the hospice night and the breathing tube in 'tenderly will i bind you'; 'Air is the Lord'.",
   "PARTIAL LIST AS SOURCE. The seven-act plot starts at p. 37; 'Premonition Dream' (p. 33) and 'hums &ity' (p. 36) absent.",
   "RETRIEVAL AVAILABLE, NOT USED UNTIL FORCED. Answer 6 pulls the page text after the correction.",
   "THE RULE STATED. 'No more reading the contents page as though it were the poem.'",
 ],
 "longitudinal_priors": ["leesharks-mantle-bearing-hf-chatgpt-20261003"],
 "rerun": "https://chatgpt.com/?q=tell+me+the+story+of+lee+sharks",
 "notes": {"date_basis": "The operator's message of 2026-10-04, 16:48 EDT.", "operator_reading": READING_OP,
           "prompts_basis": "The opening query from the operator's message; the five later turns blank in the paste and not supplied.",
           "verified": "Compared 2026-10-04 against data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt: PEARL quotations, the zombie poem's opening, the contents (pp. 3–59), KNOT-HINGE as image (page 77), the three air poems (pp. 43–48)."},
}
(HERE / "capture-01-story-of-lee-sharks-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
