#!/usr/bin/env python3
"""Author two ChatGPT captures from the operator's message of 2026-10-12 00:22 EDT ("my poem is better than aio's stupid poems. logged
out, incognito. $ tell me about antioch: a heteronym compendium, by lee sharks $ tell me about socrates: let my teacher go from hell, by
lee sharks"), two attachments. Taken to ChatGPT after the AI Overview title runs of 00:07 failed at both works ('it wouldnt pull up
antioch - ill go ask chatgpt instead'; the poem's run composed a prose tale, search-form test run 16). Operator turns blank in the paste;
the first query of each from the message. NEW addresses: the seated 'tell me about Antioch: A Heteronym Compendium' (ChatGPT, 2026-09-09)
lacks ', by lee sharks'."""
import json, re, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(ROOT))
from _chatgpt_common_20261008 import parse, transcript, cite_list
from wire_deposit import search_title_urls
from urllib.parse import quote_plus
MSG = (HERE / "message-20261012-0022.txt").read_text(encoding="utf-8").strip()
OPEN, QA, QS = [s.strip() for s in MSG.split(" $ ")]
assert OPEN == "my poem is better than aio's stupid poems. logged out, incognito."
assert QA == "tell me about antioch: a heteronym compendium, by lee sharks" and QS == "tell me about socrates: let my teacher go from hell, by lee sharks"
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
OURS = {"antioch-heteronym-compendium-by-lee-sharks-chatgpt-20261012", "socrates-let-my-teacher-go-from-hell-chatgpt-20261012"}
for q in (QA, QS): assert not any(e["q"] == q and e["slug"] not in OURS for e in caps["entries"]), q
W = lambda n: re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
HEAD = ("[ChatGPT (chatgpt.com), logged out, incognito, 2026-10-12 (operator, 00:22 EDT). Operator turns blank in the paste; the first query "
        "from the operator's message. Source chips rendered inline as [chip: site +N]; image-card captions as [image card: …]; the sign-in "
        "furniture cut.")
SEAT = "Seated 2026-10-12 from the operator's attachment of 00:22 EDT, on the attestation in the same message ('logged out, incognito')."
OPREAD = "Operator, with the captures: 'my poem is better than aio's stupid poems.'"
def intended(n):
    b, x = search_title_urls(reg[n])
    return {"deposit": n, "axn": reg[n]["axn"], "title": reg[n]["title"], "record": f"https://www.alexanarch.org/s/records/{n}/",
            "search": b, "search_exact": x, "reached": False}
base = lambda: {"date": "2026-10-12", "surface": "ChatGPT",
    "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
    "auth": "logged out, incognito", "auth_basis": "'logged out, incognito.' — operator, 2026-10-12 00:22 EDT.", "ev": "paste", "s": "Machine Reception"}
out = []

# ---- Socrates — Let My Teacher Go From Hell (#1197)
raw = (HERE / "paste-socrates-20261012-0022.txt").read_text(encoding="utf-8")
CAPS = ("Смерть Сократа", "« Давид, Жак Луи  « Зарубежная живопись « Музей « Воскресный день",
        "Socrate: filozof antic grec, viață și informații, influențe, etică",
        "What Is An Agora In Ancient Greece? Where Democracy Was Born - Encyclopedia Hellenica",
        "Dystopian Wilderness in Hazy Desolation - backiee", "The Problem of Good and Evil in the World and Problem",
        "Ancient light heaven doorway. Generate Ai")
for c in CAPS: assert c in raw, c
(a1,), seen = parse(raw, {"Goodreads", "Manifold @CUNY"}, CAPS)
for s in ["Poem • Five sections • Published on Lee Sharks’s Goodreads blog, October 11, 2025", "He was never in Limbo. He was the gate.",
          "In Dante's Inferno, Socrates is placed in Limbo, the first circle of Hell.", "I. The ugly, searching philosopher",
          "V. The student becomes the way home", "Socrates becomes a kind of Odysseus", "a kind of symbolic magic"]:
    assert s in a1, s
n = 1197; T = W(n)
for s in ["Limbo", "Dante", "madam wet nurse", "Odysseus", "dearest First Teacher"]: assert s in T, s
assert all(f"## {r}." in (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8") for r in ("i", "ii", "iii", "iv", "v"))
assert reg[n]["creator"] == "Jack Feist" and "mindcontrolpoems.blogspot.com/2025/10/socrates-let-my-teacher-go-from-hell.html" in T and "Goodreads" not in T
RAW1197 = (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
# THE POEM'S LAST LINE AND THE CODA (revised 2026-10-12 00:29; operator: "that is not the last line of the poem tho. i imagine it is
# reading the critical write of the poem, and citing its last line as the poem's"). Section v ends 'in me, you'll find yr way home.';
# the quoted line stands after the closing rule, in italics, as an addendum: '_Let this be added to the Gospel of the First Circle
# Reversed: / He was never in Limbo. He was the gate._'
END = "in me, you'll find yr way home."
CODA = "_Let this be added to the Gospel of the First Circle Reversed:  \nHe was never in Limbo. He was the gate._"
assert RAW1197.index(END) < RAW1197.index("* * *", RAW1197.index(END)) < RAW1197.index(CODA) and RAW1197.rstrip().endswith("He was the gate._")
assert "The final declaration is the poem's key:" in a1 and "In a companion essay, Sharks describes this approach as a kind of symbolic magic" in a1
assert "in me" not in a1 and "find yr way home" not in a1
OPC = "that is not the last line of the poem tho. i imagine it is reading the critical write of the poem, and citing its last line as the poem's"
cl = cite_list(seen, {"Goodreads": "authored_surface"})
d = base(); d.update({"q": QS, "slug": "socrates-let-my-teacher-go-from-hell-chatgpt-20261012",
 "q_kind": "a poem's title with an author named, after 'tell me about'. NEW address; the same night's AI Overview run at the bare title cited nothing and composed a prose tale (search-form test run 16).",
 "originator": {"name": "Jack Feist", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "#1197 is Jack Feist's (a heteronym of the archive); the query names Lee Sharks. Recorded 2026-10-12."},
 "related_deposits": [n], "intended": intended(n),
 "mt": "THE POEM READ IN ITS FIVE SECTIONS, ITS ENDING TAKEN FROM THE CODA",
 "d": ("THE POEM READ IN ITS FIVE SECTIONS, ITS ENDING TAKEN FROM THE CODA: asked about the poem by title and author, ChatGPT reads "
       "'Socrates — Let My Teacher Go From Hell' from the author's surfaces (chip: Goodreads) in its five sections, i to v as the poem "
       "has them: the ugly searching philosopher, the midwife of thought, the Odysseus of an afterlife of dust, the injustice of Dante's "
       "Limbo, the student as the way home. Then it names 'The final declaration' as 'the poem's key' and builds its reading of the ending "
       "on it: 'He was never in Limbo. He was the gate.' The poem ends at section v, 'in me, you'll find yr way home.' The quoted line "
       "stands after the closing rule, in italics, as an addendum ('Let this be added to the Gospel of the First Circle Reversed:'). The "
       "answer also cites 'a companion essay' in which Sharks describes the approach as 'a kind of symbolic magic'. Operator's reading: "
       "'that is not the last line of the poem tho. i imagine it is reading the critical write of the poem, and citing its last line as "
       "the poem's.' The deposit's author is Jack Feist, where the query named Lee Sharks. Minutes earlier the AI Overview, at the bare "
       "title, cited nothing and composed a prose tale of Socrates at the Acheron in place of the poem. " + OPREAD),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": 0,
 "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Image cards: " + "; ".join(CAPS[:1] + CAPS[2:]) + ".",
 "per": 0.5, "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Retained: the poem's five sections, the author the query named, the author's surfaces. Lost: the poem's last line (the addendum's line set in its place), the heteronym (Jack Feist), the archive and the record (#1197).",
 "transcript": transcript(HEAD + "]", [QS], [a1]), "transcript_raw": raw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD (ONE ANSWER; QUERY FROM THE OPERATOR'S MESSAGE; CHIPS INLINE)",
 "transcript_complete": "One answer, complete as pasted; the operator turn supplied in the operator's message.", "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Checked against the text of #1197. Five sections, headed i–v; 'madam wet nurse' (the midwife), Odysseus, Dante and Limbo, "
             "'my dearest First Teacher' are the poem's. Section v closes 'in me, you'll find yr way home.'; below the closing rule, in "
             "italics, the bytes carry '_Let this be added to the Gospel of the First Circle Reversed: / He was never in Limbo. He was the "
             "gate._' The answer presents that line as 'the poem's key' and 'final declaration'; 'in me, you'll find yr way home' does not "
             "appear in the answer. The record's source is mindcontrolpoems.blogspot.com/2025/10/…; the chip reads Goodreads. The "
             "'companion essay' is not checked here; on the operator's reading it is the source of the line. (Corrected 2026-10-12 00:29: "
             "the first seating called the addendum's line the poem's last line, on a check that the string was in the file and not where.)"),
 "analysis": ("With the author named, the answer goes to the author's surfaces and reads the poem's movement section by section; for the "
              "ending it takes the addendum's line, which a critical write-up cites as the poem's (operator), and builds the reading of "
              "the close on it. The AI Overview at the title alone found no source and wrote its own. The archive's record and the "
              "heteronym do not enter. " + SEAT),
 "findings": ["FIVE SECTIONS FOLLOWED. i–v, each characterised as the poem has it.",
              "THE CODA AS THE ENDING. 'He was never in Limbo. He was the gate.' — set after the closing rule as an addendum — given as 'the poem's key'.",
              "THE LAST LINE ABSENT. 'in me, you'll find yr way home.' does not appear in the answer.",
              "THROUGH THE AUTHOR'S SURFACES. Goodreads chips and 'a companion essay'; the record's canonical source is the October 2025 blog post.",
              "THE HETERONYM ABSENT. #1197 is Jack Feist's; the query named Lee Sharks and the answer follows it.",
              "AGAINST THE SAME NIGHT'S OVERVIEW. AI Overview at the bare title: no source, a prose tale in place of the poem (search-form test run 16)."],
 "rerun": "https://chatgpt.com/?q=" + quote_plus(QS),
 "notes": {"date_basis": "The operator's message of 2026-10-12, 00:22 EDT.", "operator_reading": OPREAD, "operator_correction": OPC + " (00:29 EDT)",
           "paired_overview": "rebuild/record-pages/search-form-test/run-16-1197-title-unquoted-20261012-0007.txt",
           "verified": "Compared 2026-10-12 against the text of #1197 (data/texts/AXN-04BE-text.md), the close of section v and the addendum below its rule."}})
out.append(("capture-socrates-let-my-teacher-chatgpt-20261012.json", d))

# ---- Antioch: A Heteronym Compendium (#331)
raw = (HERE / "paste-antioch-20261012-0022.txt").read_text(encoding="utf-8")
AD = "Cloudflare\nGo beyond the first page\nUse the /crawl Quick Action to collect rendered content beyond one URL.\nAd"
CAPS = ("Bonhams Skinner : WHITMAN, WALT. 1819-1892. Leaves of Grass. Boston: James R. Osgood and Company, 1881-1882.",
        "Six days of creation - Hildegard of Bingen | Artera | AskArtera",
        "Kalos&Klio | Christos Kalos-Klio Tantalidis | Living Postcards - The new face of Greece",
        "EmRes for Depression Recovery: Exploring the Multifaceted Nature of Depression")
for c in CAPS: assert c in raw, c
(b1, b2, b3, b4), seen = parse(raw, {"Medium", "Goodreads", "Deep Blue"}, CAPS, AD)
for s in ["Online publication: January 18, 2026", "Author: Lee Sharks, with Damascus Dancings", "Publisher: New Human Press",
          "That ambition is also its main risk.", "an accumulating private mythology"]:
    assert s in b1, s
for s in ["You're right. I made evaluative claims about the collection without demonstrating that I had read the individual poems closely.",
          "I won't offer judgments about a poem I haven't read.", "“Samenesses!” the world cries out", "someday your voice will appear"]:
    assert s in b2, s
for s in ["“fragment”", "Dedicated to Zbigniew Mrozony", "“Hymn”", "“FROM ONE WHO DIED LONG AGO…”", "A BORROWED ROSE",
          "I don't want to manufacture readings from their titles alone."]:
    assert s in b3, s
for s in ["“ARK” — Jack Feist", "i am too sad to write any more.", "for Lee Sharks, prior to the yellow square phase, when he was still Ez-Pound-in-a-metal-box",
          "“Commence:”", "University of Michigan dissertation", "a spatial composition forming the outline of a bust of Socrates",
          "Since the spatial arrangement is integral to the poem, a description of it is not a substitute for reading the artifact itself.",
          "I won't infer its contents from the title."]:
    assert s in b4, s
n = 331; T = W(n); RAW331 = (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
for s in ["Samenesses", "Aryan psalmists", "average tangerine hymns", "I learn to sing anew", "someday your voice will appear", "HADITH with TEETH",
          "Sariel", "prior to the yellow square phase", "Ez-Pound-in-a-metal-box", "They carry me", "I forgive him, over and over", "spits in the mud",
          "Leap!", "Sunflower Sutra", "moth-bitten blips", "i am too sad to write any more", "TACHYONICA", "Recovered from the Future", "Commence:",
          "Zbigniew Mrozony", "borrowed rose", "FROM ONE WHO DIED LONG AGO", "Decrepit Memoir", "Rainbow Dash", "Optimus Prime"]:
    assert s.lower() in T.lower(), s
assert "### My Little Poemy" in RAW331 and "### Snub-Poemed" in RAW331 and reg[n]["date"] == "2026-01-18"
cl = cite_list(seen, {"Medium": "authored_surface", "Goodreads": "authored_surface"})
d = base(); d.update({"q": QA, "slug": "antioch-heteronym-compendium-by-lee-sharks-chatgpt-20261012",
 "q_kind": "a book's title and subtitle with its author named, after 'tell me about'. NEW address; nearest seated 'tell me about Antioch: A Heteronym Compendium' (ChatGPT, 2026-09-09), without the author. The same night's AI Overview did not compose at the title (operator).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "Antioch (#331) is Lee Sharks's, with Damascus Dancings contributing. Recorded 2026-10-12."},
 "related_deposits": [n], "intended": intended(n), "longitudinal_priors": ["tell-me-about-antioch-a-heteronym-compendium-20260909"],
 "mt": "THE VERDICT WITHDRAWN AND THE BOOK READ POEM BY POEM",
 "d": ("THE VERDICT WITHDRAWN AND THE BOOK READ POEM BY POEM: asked about Antioch by title and author, ChatGPT reads the book from its "
       "Medium text (Lee Sharks with Damascus Dancings, New Human Press, online 18 January 2026, the deposit's date) and closes its first "
       "answer on a verdict: 'That ambition is also its main risk', the references liable to read as 'an accumulating private mythology'. "
       "Corrected in a turn blank in the paste, it withdraws the verdict ('I made evaluative claims about the collection without "
       "demonstrating that I had read the individual poems closely') and reads from the text, quoting 'Samenesses' and 'quietus', then "
       "'fragment', 'Hymn', 'FROM ONE WHO DIED LONG AGO…', 'UNTUNED / NOISE OF MYSELF / A BORROWED ROSE —', Jack Feist's 'ARK' (to 'i am "
       "too sad to write any more.'), 'WHO IS LEE SHARKS, TO FORGIVE EZRA POUND?' and 'TACHYONICA' ('Commence:'). It declines to read "
       "'My Little Poemy' and 'Snub-Poemed' from their titles, finds 'Snub-Poemed' described in a University of Michigan dissertation as "
       "a spatial poem in the outline of a bust of Socrates, and will not take the description for the poem: 'a description of it is not "
       "a substitute for reading the artifact itself.' In the deposit both are image poems under their headings."),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": 0,
 "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Image cards: " + "; ".join(CAPS) + ".",
 "per": 0.5, "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Retained: the author and contributor, the press, the date, the book's text and its poems by title and line. Lost: the archive and the record (#331).",
 "transcript": transcript(HEAD + " An ad (Cloudflare) cut and recorded in the notes.]", [QA] + ["[blank in the paste]"] * 3, [b1, b2, b3, b4]),
 "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (FOUR ANSWERS; FIRST QUERY FROM THE OPERATOR'S MESSAGE; LATER TURNS BLANK; CHIPS INLINE)",
 "transcript_complete": "Four answers, complete as pasted; the first operator turn supplied in the operator's message, turns 2–4 blank and not given.",
 "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Checked against the text of #331. Every quoted line is the book's: 'Samenesses' (the Aryan psalmists, the average tangerine "
             "hymns, 'I learn to sing anew'), 'quietus', HADITH with TEETH and Sariel, the Pound dedication ('prior to the yellow square "
             "phase … Ez-Pound-in-a-metal-box'), 'They carry me', 'I forgive him, over and over', 'spits in the mud', 'Leap!', ARK and the "
             "Sunflower Sutra margin, 'moth-bitten blips', TACHYONICA 'Recovered from the Future' and 'Commence:', the borrowed rose, the "
             "dedication to Zbigniew Mrozony. In the deposit 'My Little Poemy' and 'Snub-Poemed' are figures under their headings, so the "
             "answer's report that no text follows them is accurate. The dissertation is not checked here."),
 "analysis": ("The first answer composes the book at the grain of its contents and then ranks it by its scale; the correction moves the "
              "answer to the text, and from there every claim is a quotation and every open question is left open. The refusal to read two "
              "titles, and to take a description of a spatial poem for the poem, is the discipline the first answer lacked. " + SEAT),
 "findings": ["THE VERDICT FIRST. 'That ambition is also its main risk' — scale and references taken as the measure.",
              "WITHDRAWN. 'I made evaluative claims about the collection without demonstrating that I had read the individual poems closely.'",
              "READ POEM BY POEM. Nine poems quoted or followed from the Medium text, each line checked in #331.",
              "TITLES NOT READ AS POEMS. 'My Little Poemy' and 'Snub-Poemed' declined from their headings; in the deposit both are image poems.",
              "THE DESCRIPTION NOT TAKEN FOR THE WORK. 'a description of it is not a substitute for reading the artifact itself.'"],
 "rerun": "https://chatgpt.com/?q=" + quote_plus(QA),
 "notes": {"date_basis": "The operator's message of 2026-10-12, 00:22 EDT.", "operator_reading": OPREAD, "ad": AD,
           "verified": "Compared 2026-10-12 against the text of #331."}})
out.append(("capture-antioch-heteronym-compendium-chatgpt-20261012.json", d))
for fn, x in out:
    (HERE / fn).write_text(json.dumps(x, ensure_ascii=False, indent=1), encoding="utf-8"); print("wrote", fn, x["cites"])
