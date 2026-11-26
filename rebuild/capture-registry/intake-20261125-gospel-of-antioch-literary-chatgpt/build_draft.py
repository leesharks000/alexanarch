"""Draft: The Gospel of Antioch read closely as a literary work, then side by side with The Secret Book of Walt, ChatGPT, 2026-11-25. Seat with:
    python3 scripts/capture_intake.py rebuild/capture-registry/intake-20261125-gospel-of-antioch-literary-chatgpt/draft.json --seat"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
paste = (H / "paste.txt").read_text(encoding="utf-8")
Q = ("Read The Gospel of Antioch: The Sayings of Jack Feist as Recorded by Emily Antioch the Twin closely, as a literary work: its form, its voice, "
     "its structure, and what it does to the one who reads it. Ground in reading and index the full range before responding.")
T2 = "wow. what is secret book of walt? lets read it side by side. plenty of quotations."
cut = paste.index("Searching the web")
T = "[QUERENT] " + Q + "\n\n" + paste[:cut] + "[QUERENT] " + T2 + "\n\n" + paste[cut:]
chips = [("Academia +1", "after the edition's description, turn 1"), ("Alexanarch +1", "after §1, the Thomas concordance figures"),
         ("Alexanarch +2", "after §2, the voice"), ("Alexanarch +2", "after §3, the structure"), ("Alexanarch +1", "after §5, the kingdom of literature"),
         ("Alexanarch +2", "after §9, the eleven appendices"), ("Alexanarch +2", "after §12, the Waltian Diptych"),
         ("Crimson Hexagonal Archive +2", "turn 2, after the opening account of The Secret Book of Walt"), ("Alexanarch +1", "turn 2, after §1, the kind of book"),
         ("Alexanarch +2", "turn 2, after §9, the architecture of both works")]
draft = {
 "date": "2026-11-25", "dates": ["2026-11-25"], "surface": "ChatGPT", "surfaces": ["ChatGPT"],
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Sign up for free', 'ChatGPT is AI and can make mistakes.').",
 "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14); the paste's own 'Log in' and 'Sign up for free'.",
 "ev": "paste", "turns": 2,
 "slug": "gospel-of-antioch-literary-work-full-range-chatgpt-20261125", "s": "Works",
 "q": Q,
 "originator": {"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Lee Sharks, author of The Gospel of Antioch (#1185) and The Secret Book of Walt (#1184, #1362). Recorded 2026-11-25."},
 "related_deposits": [1184, 1185, 1362],
 "q_kind": "a close literary reading of one work by title, with the grounding instruction; NEW address (the 23 October deep dive is a different string). Neither query is in the paste; both are seated from the operator's message of 22:37 EST, where they are given after '$' marks, each at its place.",
 "transcript": T,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's two turns on the unauthenticated interface; the two queries seated from the operator's message",
 "transcript_complete": "Two answers complete as supplied: the first from 'Reading The Gospel of Antioch' to 'the transmission that makes a teacher survive his own disappearance'; the second from 'Searching the web' to its proposed first close reading. Image captions from the composer's inline images stand in the paste as pasted.",
 "transcript_read": "READ IN FULL 2026-11-25; quotations, counts and section names checked against the seated texts of #1185, #1184 and #1362",
 "cites": len(chips),
 "cite_list": [{"n": i + 1, "site": s, "rel": "archive_controlled", "url": None, "title": None, "snip": None, "note": "source chip as pasted, " + w} for i, (s, w) in enumerate(chips)],
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Lee Sharks named as author, translator and editor; Emily Antioch, Jack Feist and Professor Elara Xanthic-Wells named in their roles; Alexanarch and the Crimson Hexagonal Archive named in the source chips and the text; no deposit number or AXN given; sources are the archive's pages and an Academia copy.",
 "per_dim_pending": {"since": "2026-11-25", "reason": "no atom set yet for this target", "breach": False},
 "mt": "THE GOSPEL OF ANTIOCH READ AS A LITERARY WORK ON CHATGPT, ALL 114 LOGIA AND ELEVEN APPENDICES INDEXED; THEN THE SECRET BOOK OF WALT SIDE BY SIDE — 'THE VOICE SURVIVES NOT BECAUSE IT REMAINS UNCHANGED, BUT BECAUSE SOMEONE ELSE BECOMES CAPABLE OF CARRYING IT'",
 "d": ("THE GOSPEL OF ANTIOCH READ CLOSELY AS A LITERARY WORK ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-25: the 56-page research edition found, its 114 logia and "
       "eleven appendices indexed; form (the Thomas concordance: 62 parallels as 14 direct, 37 reworked, 7 inverted, 4 expanded, and 52 original), voice ('You are a "
       "book and you are living speech.', the bankrupt banks, 'Be flutterbys.'), structure (seven constellations; hinges at logia 13, 57 and 112), Emily Antioch "
       "('You are my own lost voice.'), the five kingdom parables, the Somatic Map (28, 41, 45) and Scroll Baptism, the apparatus as a second voice, logion 114 as "
       "the completion of Thomas; five named vulnerabilities. Then, asked what The Secret Book of Walt is: the two books side by side, section by section — the "
       "Deep Web, Biblios, the Demiurge, the Unicorn Horn, Jack Feist as terminal incarnation, 'Will it be enough?' — and a six-session reading plan."),
 "reading": ("The innocent reading first. Asked to read the Gospel of Antioch closely as a literary work and to index the full range before answering, the composer "
             "says it has located the research edition, separates what the text does from what its apparatus says it does and from what happens to the reader, and "
             "goes through form, voice, structure, the scribe, the kingdom parables, the body, the apparatus, the last saying, the appendices A to K, and the "
             "effect on the reader. The quotations it gives are in the seated text of #1185 word for word, the concordance figures are the edition's own, and the "
             "three somatic tiers carry the edition's counts. It judges as it goes: the sayings are 'often more interesting than their explanations'; the virus "
             "metaphor has 'an authoritarian dimension'; the archive 'risks becoming a closed interpretive system'. At the second turn it reads The Secret Book "
             "of Walt beside it, calls the edition's discovery story 'elements of its fictional editorial construction, not historical claims', and sets the "
             "two books against each other by origin, redeemer, instrument and the reader's part."),
 "analysis": ("The work is read from its text and attributed to its author; the heteronymic persons are given in the roles the edition gives them. The composer "
              "holds the apparatus at a distance the address did not ask for and the edition allows: the projected reception history of 2029–2039 is reported as "
              "the edition labels it, 'projected rather than historical', and named 'retroactive canon formation'. The second turn's quotations from Walt are "
              "in #1184 and #1362 ('Because of her they had come into being.', 'Things flew apart.', 'Will it be enough?'; 'the Deep Web was' across the line break "
              "of 'In the Beginning / The Deep Web was'), and the seven emanations, the thirty-six archons and the brain-sized hologram are the book's. "
              "'Pseudotranslation' is not a word of either seated text; it is in the description of record #1362. Logion numbers for the commuter (8), the "
              "applicant (64) and the saved money (76) were not checked: the sayings are in the seated text, which does not number them. The instruction to "
              "read three times was not found by those words; 'The third reading is the piercing.' is the headnote's. No deposit number or AXN is given anywhere "
              "in either turn."),
 "findings": [
  "THE EDITION FOUND AND INDEXED WHOLE. 114 logia, the headnote, the apparatus, the synoptic concordance and eleven appendices named A to K by subject; the concordance's own summary carried: 62 Thomas parallels (14 direct, 37 reworked, 7 inverted, 4 expanded), 52 original.",
  "QUOTATION VERBATIM. 'You are a book and you are living speech.'; the bankrupt banks; 'Be flutterbys.'; 'Teacher, my tongue cleaves to the roof of my mouth. You are my own lost voice.'; logion 114's 'I will guide you to make you a woman and minority, for I myself am a woman and minority, and will remain that way until I transform myself into something else.'; 'The Word has entered the body.'; 'The body is now the scroll.' Each is in #1185 as given.",
  "LOGION 13 WITH ITS THREE ANSWERS. Rebekah's 'celebrity', Lee Sharks's 'public intellectual' and Emily's lost voice are given in order, and the withdrawal with the three undisclosed sayings is read as 'a compositional principle'.",
  "THE APPARATUS READ AS PART OF THE WORK. 'The apparatus criticus is not an ornamental addition. It is a second literary voice.' The projected reception history (2029–2039) is reported as projected, and called 'retroactive canon formation'.",
  "FIVE VULNERABILITIES NAMED. Uniform voice; uneven sayings; an apparatus that 'overdetermines meaning'; the virus metaphor's 'authoritarian dimension'; the archive as 'a closed interpretive system'.",
  "THE SECOND BOOK BESIDE THE FIRST. The Secret Book of Walt in its twelve sections with their subjects; Biblios set beside Emily; 'Walt explains why there is something to transmit. Antioch explains what transmission costs.' The discovery story is stated to be the edition's fiction, with the August 2015 composition date and the 2026 critical edition.",
  "NO IDENTIFIER. Author, persons, titles and archive are named; neither turn gives a deposit number or an AXN."],
 "notes": {"operator": "pasted 2026-11-25 22:37 EST with both queries after '$' marks; 'this is a strong reading of antioch'",
           "source": "rebuild/capture-registry/intake-20261125-gospel-of-antioch-literary-chatgpt/paste.txt, the paste unchanged; the two queries inserted from the message at their places"},
}
(H / "draft.json").write_text(json.dumps(draft, ensure_ascii=False, indent=1), encoding="utf-8")
print("draft written", len(T))
