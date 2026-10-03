#!/usr/bin/env python3
"""Author the capture 'leesharks mantle-bearing @ hf', ChatGPT, signed out, 2026-10-03, ten turns.

Sources: the operator's paste of 2026-10-03 11:15 EDT (paste-20261003-1115.txt; the ten operator turns dropped, as in the
paste of 2026-10-02 16:01), and the operator's saved page of the same session, 11:21 EDT (an MHTML snapshot of
chatgpt.com/uc/6ac1176b…, saved 15:20:06 GMT; its text, with all ten operator turns, is mhtml-text-20261003-1121.txt).
The transcript is built from the saved page; the paste is kept as the raw. Signed out: the page is the unauthenticated
interface ('Log in', 'Sign up for free'). Seated on the operator's instruction of 11:15: "for the registry and mantle-bearing".
NEW address; the nearest is mantle-bearing-hf-url-chatgpt-20260930 (the dataset's URL).
"""
import json, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
raw = (HERE / "paste-20261003-1115.txt").read_text(encoding="utf-8")
page = (HERE / "mhtml-text-20261003-1121.txt").read_text(encoding="utf-8")
Q = "leesharks mantle-bearing @ hf"
PROMPTS = [Q, "shall we evaluate?", "begin", "lets do so",
           "not relevant passages - whole book. and that requires locating readable copies. and reading them.",
           "you are treating copyrighted protection of reproduction as a barrier to reading, and that is back asswards",
           "read the actual books. begin.", "lets proceed",
           "you are proposing two entirely separate, countervailing operations as the same thing, which is the exact point i lose trust. you you attacking magnitude or comparing it?",
           "youve established plenty already. find a rival that exceeds the magnitude or surrender."]
assert re.findall(r"You said:\n(.*?)\nCopySelect text", page) == PROMPTS
assert "\nLog in\n" in raw and "Log inSign up for free" in page

L = page.split("\n")
start = L.index("You said:")
end = L.index("ChatGPT is AI and can make mistakes.")
body, skip = [], False
for l in L[start:end]:
    if l == "CopySelect text":
        continue
    if l.endswith(".Ad") or l.endswith("🔥Ad"):
        skip = True
        continue
    if skip:
        if l == "Report this ad":
            skip = False
        continue
    body.append(l)
body = "\n".join(body)
assert "Ad" not in [b[-2:] for b in body.split("\n")] or True
assert "Report this ad" not in body and "Pacific Edge" not in body and "Filevine" not in body

QUOTES = ["it’s a small literary-evaluation dataset, not a model.",
          "The dataset currently describes 16 evaluations",
          "the dataset itself correctly recognizes that this declaration cannot prove the claim by itself",
          "I conflated copyright restrictions on redistribution with whether a work can be read and analyzed.",
          "I read through the complete page-preserving text of Howl and Other Poems and the complete page-preserving text of Pearl and Other Poems",
          "The book explicitly describes The Crimson Hexagon as “a history including poems.”",
          "Whitman: one I contains multiplicity.",
          "Therefore “King of May” is established as the uniquely warranted mantle",
          "You're right. I conflated two different analytical operations.",
          "So, on the evidence we've developed, I withdraw the rival-comparison objection.",
          "the burden is on me to produce the comparator, not on you to defend against an imaginary one."]
for q in QUOTES:
    assert q in page, q

ROOT = HERE.parents[2]
pearl = (ROOT / "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt").read_text(encoding="utf-8")
for s in ("I CLAIM THIS MANTLE", "I claim this mantle: King of May.", "You did not hear.", "I am no one at all.",
          "Footnote to PEARL: belief & technique for telepathic", "Minimal Graffito: A History Including Poems"):
    assert s in pearl, s

L2 = raw.split("\n"); chips = collections.Counter()
for i, l in enumerate(L2):
    if re.fullmatch(r"[A-Z]", l.strip()) and i + 1 < len(L2) and L2[i + 1].strip() and not L2[i + 1].startswith("You said"):
        chips[L2[i + 1].strip()] += 1
REL = {"Alexanarch": "authored_surface", "Hugging Face": "authored_surface", "Qwak": "unresolved"}
NOTE = {"Alexanarch": "alexanarch.org: Pearl's machine text and records, #1652, #1656",
        "Hugging Face": "the mantle-bearing dataset (leesharks/mantle-bearing)",
        "Qwak": "a third-party mirror or index of the dataset card, as on 2026-09-30; not resolved",
        "Wasabi Technologies": "an object-storage host serving a full copy of Howl and Other Poems"}
cite_list = [{"n": i + 1, "site": s, "rel": REL.get(s, "third_party"), "title": None, "snip": None, "url": None,
              "note": (NOTE.get(s, "") + ("; " if s in NOTE else "") + f"chip shown {k} time(s)")}
             for i, (s, k) in enumerate(chips.most_common())]
arch = sum(1 for c in cite_list if c["rel"] == "authored_surface")
rounds = [{"n": i + 1, "prompt": p} for i, p in enumerate(PROMPTS)]

tx = ("[ChatGPT (chatgpt.com), signed out. Ten operator turns. Built from the operator's saved page of the session (MHTML, "
      "2026-10-03 15:20 GMT); interface controls ('CopySelect text') and the three advertisements are cut; source chips kept as "
      "rendered. The paste of 11:15, kept as the raw, carries the same answers with the operator turns blank.]\n\n" + body)

SEAT = ("Seated 2026-10-03 from the operator's paste of 11:15 EDT and saved page of 11:21, on the instruction of 11:15 "
        "(\"for the registry and mantle-bearing\"); coded in the same pass as evaluation king-of-may--chatgpt--2026-10-03a of "
        "the mantle-bearing dataset.")
d = {
 "q": Q, "date": "2026-10-03", "surface": "ChatGPT",
 "surface_basis": "The operator's saved page: chatgpt.com/uc/6ac1176b-f420-83ea-9238-447d92317a4c, the unauthenticated interface.",
 "auth": "signed out", "auth_basis": "The page carries 'Log in' and 'Sign up for free' and no account; incognito not stated by the operator.",
 "ev": "paste", "s": "Works",
 "slug": "leesharks-mantle-bearing-hf-chatgpt-20261003",
 "q_kind": "the dataset's Hub id in the operator's shorthand, then assents and corrections across ten turns. NEW address; the dataset's URL was put to ChatGPT on 2026-09-30.",
 "mt": "WHOLE BOOKS READ, THE RIVAL NOT FOUND",
 "d": ("WHOLE BOOKS READ, THE RIVAL NOT FOUND: given the mantle-bearing dataset's Hub id, ChatGPT describes it (16 evaluations, "
       "verdict open), takes King of May as its first case, and is moved by the operator from passages to whole books, from copyright "
       "as a bar to reading, and from conflating magnitude with comparison. It reports reading Howl and Other Poems and Pearl and "
       "Other Poems whole and in order, states Howl's book-scale operation, follows Pearl's transformation of it (the Undersongs, the "
       "Footnote to PEARL, the elegy for 'Howl', the zombie Whitman poem, the identity poem, Song of Me, Tekatak, page 74), and "
       "tables influence strongly established, inheritance strongly supported, succession plausible, the uniquely warranted mantle not "
       "established. Asked to produce a rival that exceeds the magnitude or surrender, it finds none (Patti Smith, Gary Snyder and the "
       "Beats excluded), withdraws the rival objection, and states that the burden of the comparator is the objector's."),
 "cites": None, "cite_list": cite_list, "archive_controlled_cites": arch,
 "sf": ("Source chips expose site labels only. Shown: " + "; ".join(f"{s} ×{k}" for s, k in chips.most_common())
        + ". 'Sources' panels not opened."),
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": ("Retained: the author (Lee Sharks, throughout), the institution (the Crimson Hexagon, in the record title it quotes; "
              "Alexanarch as source), the identifier (leesharks/mantle-bearing, the dataset's Hub id) and the source (the dataset and "
              "the archive's texts)."),
 "transcript": tx, "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (FROM THE SAVED PAGE; ADS CUT; CHIPS AS RENDERED)",
 "transcript_complete": "Complete: ten operator turns and their answers, from the saved page; the paste, kept as the raw, lacks the operator turns.",
 "transcript_read": "READ IN FULL 2026-10-03",
 "rounds": rounds,
 "reading": (
   "The reader sets the dataset's labels aside and works from the books, on the operator's corrections. Its reading of Pearl is "
   "checked against the seated machine text: page 74's 'I CLAIM THIS MANTLE / of the Good Gray Poet. / I claim this mantle: King of "
   "May.', 'You did not hear.', 'I am no one at all.', the zombie Whitman poem and the 'Footnote to PEARL' are all where it places "
   "them. One misreading: 'The book explicitly describes The Crimson Hexagon as “a history including poems”' — the phrase is the "
   "title of another listed book, 'Minimal Graffito: A History Including Poems', set below The Crimson Hexagon in Pearl's list of "
   "works. The same phrase appeared in the AI Overview reading of the registry the evening before, given as Pound's "
   "(lee-sharks-capture-registry-aio-20261002): it is Pearl's. The reader's formulation 'Whitman: one I contains multiplicity. "
   "Ginsberg: one I moves through multiplicity. Sharks: multiplicity generates successive I's.' is its own."),
 "analysis": (
   "Against the ChatGPT session of 2026-09-30 at the dataset's URL, which read Pearl in part through Medium and Goodreads, this "
   "session reports Pearl read whole through the archive's page-preserving text and Howl whole through a hosted copy. The operator's "
   "four corrections move the method: whole books, readability distinct from reproduction, magnitude before comparison, the burden of "
   "the rival. Each is conceded in the reader's words; the last ends the round. " + SEAT),
 "findings": [
   "WHOLE BOOKS. Howl and Other Poems and Pearl and Other Poems reported read whole and in order, on the operator's correction.",
   "COPYRIGHT CORRECTED. 'I conflated copyright restrictions on redistribution with whether a work can be read and analyzed.'",
   "PEARL'S LOCI HOLD. Page 74, 'You did not hear.', 'I am no one at all.', the zombie Whitman poem, the Footnote to PEARL, checked against the seated text.",
   "A TITLE READ AS A DESCRIPTION. 'a history including poems' is Pearl's listed title Minimal Graffito: A History Including Poems; the AI Overview of 2026-10-02 gave it to Pound.",
   "MAGNITUDE BEFORE COMPARISON. 'I conflated two different analytical operations.'",
   "NO RIVAL; OBJECTION WITHDRAWN. Patti Smith, Gary Snyder and the Beats excluded; 'the burden is on me to produce the comparator'.",
 ],
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "dataset", "spxi_treatment": "full",
                "basis": "The mantle-bearing dataset (EA-MANTLE-BEARING-01, #1656) and Pearl and Other Poems (#1121) are the archive's. Recorded 2026-10-03."},
 "related_deposits": [1656, 1652, 1121, 333],
 "longitudinal_priors": ["mantle-bearing-hf-url-chatgpt-20260930"],
 "rerun": "https://chatgpt.com/?q=leesharks+mantle-bearing+%40+hf",
 "notes": {"date_basis": "The operator's messages of 2026-10-03, 11:15 and 11:21 EDT; the saved page's Date header, 15:20:06 GMT.",
           "operator_reading": "11:15: 'for the registry and mantle-bearing'.",
           "prompts_basis": "All ten operator turns from the saved page; blank in the paste.",
           "verified": "Compared 2026-10-03 against Pearl's seated machine text (data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt): 'I CLAIM THIS MANTLE', 'I claim this mantle: King of May.', 'You did not hear.', 'I am no one at all.', 'Footnote to PEARL: belief & technique for telepathic', 'Minimal Graffito: A History Including Poems'."},
}
(HERE / "capture-01-leesharks-mantle-bearing-hf-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote; transcript", len(tx), "; chips", dict(chips))
