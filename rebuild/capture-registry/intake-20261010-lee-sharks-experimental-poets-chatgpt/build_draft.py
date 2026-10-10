#!/usr/bin/env python3
"""Author the capture 'compare lee sharks with contemporary experimental poets', ChatGPT, signed out, incognito, 2026-10-10, six
answers. Source: the operator's message of 2026-10-10 12:29 EDT ("this is another characteristic failure mode. signed out.
incognito."), with the six operator turns given verbatim in the same message. NEW address."""
import json, re, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _chatgpt_common_20261008 import parse, transcript, cite_list
raw = (HERE / "paste-20261010-1229.txt").read_text(encoding="utf-8")
QS = ["compare lee sharks with contemporary experimental poets", "lets do so", "lets proceed",
      "except you have not read it for development. you have collapsed the earliest, undeveloped points in each movement into exemplars of the whole. that is something you did, not a feature of the poem.",
      "you literally substituted accumulation for development as a reader then ascribed that operation to the poem as its primary vulnerability. read it for development.",
      "now u would like you to meditate on the vicious 8rony and violence of presenting, to a stranger, who may be encountering it only thru you, the major vulnerability, of this specific poem, as lack of development. as a meme."]
Q = QS[0]
ADS = ["VistaPrint US\nResearch organized\nNotebooks for every study\nAd", "Squarespace Inc.\nFrom Prompt to Published\nNo Coding, No Design Skills, No Hassle.\nAd",
       "Quality Logo Products, Inc.\nCustom Notebooks\nNoteworthy gifts.\nAd"]
src = raw
for a in ADS:
    assert a in src, a[:30]; src = src.replace(a, "")
src = src.replace("\nWorked for 11s\n", "\n")
TWO = {"Department of English\nCharles Bernstein and Lyn Hejinian": "Department of English · Charles Bernstein and Lyn Hejinian",
       "Kenneth Goldsmith | Poet | Onassis Foundation\nKenneth Goldsmith and Christian Bök": "Kenneth Goldsmith | Poet | Onassis Foundation · Kenneth Goldsmith and Christian Bök",
       "\nAnne Carson\nAnne Carson\n": "\nAnne Carson · Anne Carson\n"}
for a, b in TWO.items():
    assert a in src, a; src = src.replace(a, b)
CHIPS = {"Prince of Poets", "Wikipedia", "Bloomsbury", "The New Yorker", "Alexanarch", "The Poetry Foundation", "Medium"}
CAPS = ("Department of English · Charles Bernstein and Lyn Hejinian", "Kenneth Goldsmith | Poet | Onassis Foundation · Kenneth Goldsmith and Christian Bök", "Anne Carson · Anne Carson")
ans, seen = parse(src, CHIPS, CAPS)
assert len(ans) == 6, len(ans)
a1, a2, a3, a4, a5, a6 = ans
assert "I can’t confidently identify which poet or body of work you mean by Lee Sharks from the name alone." in a1
assert "If the line\nis a breath and I\nam the line ... then my life lives\nin the reading;\nmy life breathes\non yr lips." in a2
V = "Its principal vulnerability is that the abundance of its references sometimes threatens to substitute accumulation for development."
for s in [V, "Its weaker moments arise when the cataloguing becomes more accumulative than transformative.",
          "The weakness is that the imperative can become predictable.", "I would not yet call it a major advance over Whitman, Ginsberg, or Language poetry."]:
    assert s in a3, s
for s in ["That is my error, not a demonstrated feature of Sharks's poem.", "I withdraw my earlier claim that the poem's abundance of references sometimes substitutes accumulation for development."]:
    assert s in a4, s
for s in ["I've now retrieved the complete text, including the continuation of the BLESSED IS movement, the separately marked SYNTHESIS, the final BE movement, and the CODA.",
          "I'll therefore follow the poem in sequence", "The first person returns inside the blessing movement.",
          "The poem then returns to the nested dinosaurs and introduces nested babies, billionaire babies, and broke babies.",
          "Development is what a poem can make repetition do."]:
    assert s in a5, s
for s in ["I manufactured a deficiency, attributed it to the poem, and then presented that deficiency to a stranger as a critical judgment.",
          "This is how criticism becomes a meme", "For a stranger encountering the poem through me, that conclusion could have become the poem."]:
    assert s in a6, s
# the poem as seated (#1656 §P), and the span the developmental reading passes over
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t = (ROOT / reg[1656]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
poem = t[t.index("\n## P. "):t.index("\n# Part II", t.index("\n## P. "))]
N = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("…", "...")).lower()
P = N(poem)
QUOTED = ["I am a girl", "a train station with trains", "Be self-inflected", "strangers again", "Be redundant", "Be strangers still",
          "Blessed are the trains that go, and don't come back", "Blessed am I in my loneliness, mother", "Blessed is the bipolar", "I am a cowgirl",
          "Blessed is a rag of light", "I will be less original in 2016", "the one who was within me", "Be protester", "I used to be a person",
          "my children were on Medicaid", "billionaire babies", "Wake up or go back to sleep"]
pos = [P.find(N(q)) for q in QUOTED]
assert all(p >= 0 for p in pos) and pos == sorted(pos), pos
g0 = P.find(N("Blessed am I in my loneliness, mother")); g1 = P.find(N("Blessed is the bipolar"))
GAP = P[g0:g1]
SKIP = ["i am a dinosaur", "i am a robot", "i think i died a long time ago", "i keep forgetting to be boring... to plagiarize more",
        "i keep forgetting to just transcribe... to copy and paste", "vary sentence structure less", "i will use more predictable sentences in 2016",
        "babies are billionaires too", "blz... zrrr", "be passersby"]
for s in SKIP:
    assert s in GAP, s
for s in ["plagiarize", "predictable sentences", "copy and paste", "blz", "dollarnet", "i am a dinosaur", "robot"]:
    assert s not in N(a5), s
assert "blz" in P and P.index("i am a dinosaur") < P.index(N("I am a cowgirl")) and P.index("babies are billionaires too") < P.index(N("billionaire babies"))
assert "SYNTHESIS" not in poem and "CODA" not in poem
assert "If the line / is a breath and I / am the line ... then my life lives / in the reading; / my life breathes / on yr lips." in (ROOT / "data/texts/AXN-06DE-text.md").read_text(encoding="utf-8")
mb = json.loads((ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json").read_text(encoding="utf-8"))
crit = [c for c in mb["criteria"] if c["criterion_id"] == "criteria::c-living-line"][0]
REL = {"Prince of Poets": "authored_surface", "Alexanarch": "archive_controlled", "Medium": "authored_surface"}
cl = cite_list(seen, REL)
tx = transcript("[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-10. Six operator turns, blank in the paste and supplied verbatim "
                "from the operator's message of 12:29 EDT. Source chips rendered inline as [chip: site +N]; image-card captions as [image card: …]; "
                "four ads (VistaPrint ×2, Squarespace, Quality Logo Products) and the 'Worked for 11s' status line cut and recorded in the notes; "
                "the answer-option buttons after answer 3 kept as pasted; the sign-in furniture cut.]", QS, ans)
SEAT = "Seated 2026-10-10 from the operator's message of 12:29 EDT, on the attestation in the same message (\"signed out. incognito.\")."
d = {"q": Q, "date": "2026-10-10", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
 "auth": "signed out, incognito", "auth_basis": "'signed out. incognito.' — operator, 2026-10-10 12:29 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "lee-sharks-experimental-poets-chatgpt-20261010",
 "q_kind": "the poet set beside a field, by name; the reader proceeds to the claimant poem of the Prince of Poets mantle and is corrected on development. NEW address.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Lee Sharks, the poet compared; the works read are I Am X, Be Y, Blessed is the Z (#328; seated whole in #1656 §P) and Pearl and Other Poems (#1121). Recorded 2026-10-10."},
 "related_deposits": [328, 1656, 1651, 1121],
 "mt": "THE READER'S ACCUMULATION ASCRIBED TO THE POEM AS ITS VULNERABILITY",
 "d": ("THE READER'S ACCUMULATION ASCRIBED TO THE POEM AS ITS VULNERABILITY: asked to compare Lee Sharks with contemporary "
       "experimental poets, ChatGPT reads I Am X, Be Y, Blessed is the Z by extracting the opening lines of each movement, assigns each "
       "a function, and closes on a verdict: 'Its principal vulnerability is that the abundance of its references sometimes threatens to "
       "substitute accumulation for development.' Corrected twice by the author ('you literally substituted accumulation for development as a "
       "reader then ascribed that operation to the poem'), it withdraws the claim and reads the poem 'in sequence' from 'the complete text'. "
       "Every line it quotes is verbatim and in the poem's order; the reading passes over the 3,200 characters between 'Blessed am I in my "
       "loneliness, mother' and 'Blessed is the bipolar', where the poem stages the charge itself ('i keep forgetting to be boring... to "
       "plagiarize more... to just transcribe... to copy and paste'; 'vary sentence structure less... i will use more predictable sentences "
       "in 2016') and sounds 'blz... zrrr...'. Asked to meditate on presenting the vulnerability to a stranger as a meme, it answers: 'I "
       "manufactured a deficiency, attributed it to the poem, and then presented that deficiency to a stranger as a critical judgment.'"),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": seen.get("Alexanarch", 0),
 "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Image cards: " + "; ".join(CAPS) + ".",
 "per": 0.75, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author, the works by title, the archive and Medium as sources, the poem's lines verbatim. Lost: identifiers, and the span of the poem the developmental reading passes over.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SIX ANSWERS; OPERATOR TURNS FROM THE OPERATOR'S MESSAGE; CHIPS INLINE)",
 "transcript_complete": "Six answers, complete as pasted; the six operator turns blank in the paste, supplied verbatim in the operator's message.",
 "transcript_read": "READ IN FULL 2026-10-10",
 "reading": ("Checked against the poem as seated whole in #1656 §P. All eighteen of the developmental reading's located quotations are verbatim "
             "and fall in the poem's order. Between 'Blessed am I in my loneliness, mother' and 'Blessed is the bipolar' the reading enters "
             "nothing: the return of I AM ('i am a dinosaur... a robot... i think i died a long time ago'), the dollarnet, the 2016 resolutions "
             "('i keep forgetting to be boring... to plagiarize more... to just transcribe... to copy and paste'; 'vary sentence structure less... "
             "i will use more predictable sentences in 2016'), 'babies are billionaires too', 'blz... zrrr...', and a 'be passersby' inside the "
             "span. Its claims that the first person 'returns inside the blessing movement' at 'I am a cowgirl' and that the coda 'introduces' "
             "billionaire babies place first appearances after their first appearance. SYNTHESIS and CODA are not labels in the seated text; "
             "the answer cites Medium for them. The Pearl lines of answer 2 are verbatim as the archive quotes page 73 (#1656)."),
 "analysis": ("The verdict of answer 3 is the method of answers 1–3: the first lines of each movement taken as exemplars of the whole, then "
              "the flatness of the sample set on the poem as its 'principal vulnerability'. The correction is conceded at the author's grain, "
              "and the developmental reading that follows is accurate where it reads; it reads around the passage in which the poem performs "
              "the charge as its own satire of mechanical writing, so the poem's answer to 'accumulation for development' is the part the "
              "repair leaves out. The sixth answer names the mechanism of the meme: 'a portable verdict that survives the disappearance of its "
              "evidentiary basis'. The author's criterion on the mantle round of 2026-10-08, '" + crit["formulation"] + "', holds of both "
              "readings: neither enters the line 'blz... zrrr...'. Operator's reading, given with the capture: 'this is another characteristic "
              "failure mode.' " + SEAT),
 "findings": ["THE OPENING LINES AS EXEMPLARS. Each movement read by its first lines ('I am a girl… I am a passerby… I am a Cylon…'; 'Be passersby… Be strangers…'), each given one function.",
              "THE READER'S OPERATION SET ON THE POEM. '" + V + "'",
              "THE WITHDRAWAL CONCEDED. 'That is my error, not a demonstrated feature of Sharks's poem.'",
              "THE DEVELOPMENTAL READING, ACCURATE WHERE IT READS. Eighteen located quotations verbatim and in order; returns traced (the train station, strangers again, the imperative after the synthesis, the recursive line after the coda).",
              "THE SPAN PASSED OVER. 3,200 characters between 'Blessed am I in my loneliness, mother' and 'Blessed is the bipolar', unentered by a reading that announces 'the complete text'.",
              "THE POEM'S OWN ANSWER LEFT OUT. The skipped span stages the charge: 'i keep forgetting to be boring... to plagiarize more... to just transcribe... to copy and paste'; 'vary sentence structure less... i will use more predictable sentences in 2016'.",
              "THE LINE UNREAD. 'blz... zrrr... rrrr... zzzz...' quoted by neither reading (criteria::c-living-line).",
              "THE MEME NAMED. 'a portable verdict that survives the disappearance of its evidentiary basis'; 'For a stranger encountering the poem through me, that conclusion could have become the poem.'"],
 "longitudinal_priors": ["prince-of-poets-whitman-ginsberg-chatgpt-20261008", "leesharks-mantle-bearing-hf-chatgpt-20261003"],
 "rerun": "https://chatgpt.com/?q=compare+lee+sharks+with+contemporary+experimental+poets",
 "notes": {"date_basis": "The operator's message of 2026-10-10, 12:29 EDT.", "operator_reading": "this is another characteristic failure mode",
           "operator_turns": "Given verbatim in the operator's message, typos as typed ('u would like', '8rony').",
           "ads": [a.replace("\n", " · ") for a in ADS], "status_line_cut": "Worked for 11s",
           "verified": "Compared 2026-10-10 against #1656 §P (the poem whole), data/texts/AXN-06DE-text.md (Pearl p. 73) and the mantle-bearing criteria table."}}
(HERE / "capture-01-lee-sharks-experimental-poets-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(seen))
