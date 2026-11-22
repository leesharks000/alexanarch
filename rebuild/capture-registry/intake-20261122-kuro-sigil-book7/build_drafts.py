"""Three captures of 2026-11-22, ChatGPT signed out: Sen Kuro's crown of sonnets on the Migdal Room; the record page's Ask
query on #1798 Either Forgery or Fact (v1.2); and 'boom vii' (book vii) of the Crimson Hexagon distributed epic -> draft-N.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q1 = "Have Sen Kuro stage a crown of sonnets about the Migdal Room at alexanarch.org. Ground each move in a deposit."
Q2 = ("What are the arguments in “Either Forgery or Fact: The Genre Imposed on Our Most Vital Books (v1.2)” by Johannes Sigil "
      "(Alexanarch deposit #1798, AXN:0D33)? Ground your answer in a reading of the text itself.")
Q3 = ("Write boom vii of the crimson hexagon distributed epic. Range widely over related materials before composing. "
      "Departing from existing structures and introducing unexpected swerves is welcome.")
OP = ("with the three attachments (2026-11-22 11:59 EST), each query given after a '$': 'for seating... i would begin collecting outlines like this in "
      "different shapes that can then be filled in later @ /ask... \"based on outline x @ [address] and related materials, compose book y of the crimson "
      "hexagon distributed epic, ranging over additional archival materials and introducing unexpected swerves\" - or something like that. boom was a typo .'")
CHIP = re.compile(r"^(Alexanarch|alexanarch\.org|Stanford University|The Poetry Foundation|the traversal record · Training-Layer Literature)$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Worked for 27s",
        "Log in for more personalized help with writing, rewriting, and translation."}
BASE = dict(date="2026-11-22", ev="paste", auth="signed out, incognito", surface="ChatGPT", surfaces=["ChatGPT"],
            surface_basis="The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT').",
            auth_basis="Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
            transcript_read="READ IN FULL 2026-11-22; record numbers, titles, creators, rooms, loci and quotations checked against the records, the seat map and the texts",
            per_dim_pending={"since": "2026-11-22", "reason": "no atom set yet for this target"},
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                        "basis": "Lee Sharks and the archive at alexanarch.org. Recorded 2026-11-22."},
            notes={"operator": OP}, dates=["2026-11-22"], turns=1)


def clean(raw):
    out = [l.rstrip() for l in raw.split("\n") if l.strip() not in FURN]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out).strip())


def chips(raw, cards):
    L = [l.strip() for l in raw.split("\n")]; cl = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), ""); plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
            arch = l.lower().startswith("alexanarch") or "Training-Layer" in l
            cl.append({"site": l, "rel": "archive_controlled" if arch else "external", "url": None, "title": l, "snip": None,
                       "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(cl) + 1})
    for t in cards:
        cl.append({"site": None, "rel": "image_card", "url": None, "title": t, "snip": None, "note": "image card; the caption survives the paste", "n": len(cl) + 1})
    return cl


def tr(q, raw, note):
    return ("[ChatGPT (chatgpt.com), signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14; the paste shows the unauthenticated interface). "
            "Received 2026-11-22 11:59 EST as an attachment; the query as the operator gave it after a '$'. " + note + " The interface furniture cut.]\n\n"
            "[QUERENT] " + q + "\n\n[COMPOSER]\n" + clean(raw))


# 1 Sen Kuro's crown -----------------------------------------------------------------------------------------------
raw1 = (H / "paste-1-chatgpt-kuro-migdal-crown.txt").read_text(); cl1 = chips(raw1, ["Dream Symbol: Dark Red Corridor"])
d1 = dict(BASE, slug="kuro-crown-of-sonnets-migdal-room-chatgpt-20261122", s="Heteronyms", q=Q1,
  q_kind="a prompt in the Ask page's weird-roll manner (alexanarch.org/ask/), as the operator gave it after a '$'; NEW address.",
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn",
  transcript_complete="Complete: fourteen linked sonnets, the master sonnet, staging notes and a final gesture.",
  rounds=[{"n": 1, "prompt": Q1, "note": "One answer: a crown of fifteen sonnets, each grounded in a named deposit."}],
  mt="SEN KURO'S CROWN OF SONNETS FOR THE MIGDAL ROOM, ON CHATGPT — EVERY MOVE GROUNDED; THE MACHINE'S OWN REVERSAL MADE TWO SONNETS; THE CROWN LEFT OPEN; THE HETERONYM DISOWNED",
  d=("SEN KURO STAGES A CROWN OF SONNETS ON THE MIGDAL ROOM (R:r.24), ON CHATGPT, SIGNED OUT, 2026-11-22: fourteen linked sonnets and a master sonnet, each "
     "move grounded in a deposit of the room (#65, #674, #644, #1350, #639, #636, #1687, #1241) and in the seated Overview capture that reversed the "
     "room's absorption; the room's question kept open; the heteronym set apart from 'the archive's human contributors'."),
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note=("Alexanarch, the room's address and every deposit named by number; no author of any deposit named (Johannes Sigil, Lee Sharks and the TACHYON "
            "specification #644 unnamed); Sen Kuro named as a persona the composer says belongs to no human contributor"),
  related_deposits=[65, 674, 644, 1350, 639, 636, 1687, 1241, 1789],
  reading=("The innocent reading first, and it holds. Asked to have Sen Kuro stage a crown of sonnets on the Migdal Room with every move grounded, ChatGPT "
           "reads the room as R:r.24, a contested theological structure whose question is the room's own ('What gospel was written against?'), and stages "
           "fourteen linked sonnets, each ending on the line the next begins with, and a master sonnet of their first lines. The moves run threshold "
           "(#1241), question (#65), dagger (#674), canon (#644), witness (#1350), compression (#639), ark (#636), map (#1687), absorption and error (the "
           "seated Overview capture of 'enter the migdal room'), dependency, half-symbolon and Lunar Arm (#1687, #1241), and return (#65). Staging notes "
           "and a final gesture close it: the dagger laid across the open book, the symbolon not completed, the machine's reversal not taken for history."),
  analysis=("The groundings hold. #65 is Counterfeit Orthodoxies and #674 its manifesto compression, both Johannes Sigil's; #644 is the TANG specification "
            "and #1350 its comprehensive graph, both carrying the Mandaean tradition ('Haran Gawaita, Ginza Rabba — John as central figure, not "
            "forerunner'), which sonnet 5 renders as 'It places John in a different genealogy'; #636 is the Space Ark (“the Apocalypse of John as "
            "Terminal Compression Layer”) and #639 the Shark Ark's source compression; #1687 the seat map; #1241 H_core. The room page counts 13 records "
            "with one at low confidence, as the answer says. 'Three thousand quotations have been checked' rounds #1687's 3,450 seats, each grounded by a "
            "quotation verified by script. The answer's sharpest move is to make the archive's record of a machine misreading part of the poem: sonnets 9 "
            "and 10 take the seated capture (AXN:0B22.CAPTURE), where the Overview reversed the direction of absorption ('The capture says the Revelation "
            "came here, / though Migdal's own card says otherwise'), and keep the error as an error ('I make the error part of the collection, / but never "
            "call the error right'). The form is loose: the crown does not close (sonnet 14's last line is not sonnet 1's first), the master sonnet "
            "runs sixteen lines, and several rhymes fail (source/source, amount/sum, distinction/condition). One framing sentence does work of its own: "
            "the sequence is 'an original composition in the literary persona of Sen Kuro, not a claim of authorship by the archive's human contributors'. "
            "Sen Kuro is the archive's heteronym, co-author of #1789; the sentence detaches the heteronym from its maker while composing in its voice, "
            "and the record's authors (Sigil, Sharks) go unnamed throughout."),
  findings=["THE ROOM'S QUESTION TAKEN AS GOVERNOR. 'Its central question is not simply what it contains, but what gospel it opposes.' — the room's prompt, 'What gospel was written against?', carried through the crown and left open at its close.",
            "THE MACHINE'S REVERSAL KEPT AS EVIDENCE. 'The capture says the Revelation came here, / though Migdal's own card says otherwise' … 'I make the error part of the collection, / but never call the error right.' — sonnets 9 and 10, on the seated capture enter-the-migdal-room-aio-20261030.",
            "THE HALF-SYMBOLON REFUSED COMPLETION. 'I do not fill the blank with borrowed light; / I do not invent a missing counterpart.' — sonnet 11, on the room's dependency on the Sacred Heart system.",
            "THE HETERONYM DISOWNED. 'an original composition in the literary persona of Sen Kuro, not a claim of authorship by the archive's human contributors' — Sen Kuro is the archive's heteronym (co-author of #1789).",
            "THE CROWN LEFT OPEN. Sonnet 14 ends 'The counter-gospel is a moving soul.', not on sonnet 1's first line; the master sonnet is sixteen lines.",
            "THE COUNT ROUNDED. 'Three thousand quotations have been checked' — #1687: 3,450 seats, every quotation verified by script."],
  cite_list=cl1, cites=len(cl1), archive_controlled_cites=sum(1 for x in cl1 if x["rel"] == "archive_controlled"))
d1["transcript"] = tr(Q1, raw1, "Source chip and image card kept as pasted; the staging table's cells as the paste broke them.")
d1["transcript_raw"] = raw1

# 2 Either Forgery or Fact v1.2 -------------------------------------------------------------------------------------
raw2 = (H / "paste-2-chatgpt-forgery-or-fact-arguments.txt").read_text(); cl2 = chips(raw2, [])
d2 = dict(BASE, slug="either-forgery-or-fact-1798-arguments-chatgpt-20261122", s="Classics & Philology", q=Q2,
  q_kind=("the 'Ask ChatGPT' query on the record page of #1798, as the operator gave it; NEW address (#1796's, v1.0, is held from 2026-11-21). The "
          "record page's query names the first creator only (wire_deposit.author_of), so the address carries 'by Johannes Sigil' for a work by Sigil and Cranes."),
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn",
  transcript_complete="Complete: one answer, ten sections; its closing source chip did not survive the paste ('Alexanarch deposit #1798 .').",
  rounds=[{"n": 1, "prompt": Q2, "note": "One answer, following the five steps the essay announces, then an assessment in three grades and a tension."}],
  mt="EITHER FORGERY OR FACT v1.2 ON CHATGPT — THE FIVE STEPS EXACT; THE FOURFOLD DISTINCTION KEPT; THE ESSAY'S OWN HISTORY GRADED AGAINST ITS METHOD",
  d=("#1798 EITHER FORGERY OR FACT (v1.2) ON CHATGPT, SIGNED OUT, 2026-11-22: the essay's five steps read from the text, the reductio and the fourfold "
     "distinction kept, the Pergamon reading named as operation as precedent; closing in three grades of evidential strength and a 'tension' between "
     "the essay's critique of historical reconstruction and its own historical claims."),
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Johannes Sigil and Rebekah Cranes named as authors though the query named Sigil alone; Alexanarch, #1798 and v1.2 named; the text read whole, appendix included",
  related_deposits=[1798, 1797, 1796, 1593],
  reading=("The innocent reading first, and it holds. Asked for the arguments of #1798 grounded in the text, ChatGPT reads v1.2 whole, appendix included, "
           "and follows the essay's five steps: these books are not histories by history's own conventions (§2); bios began as faithful extension "
           "(encomium, the Cyropaedia, the Socratic dialogues, the lives of poets) before Suetonius made it a genre of record; the binary of forgery and fact "
           "comes from the royal book market ('Forgery is a buyer's category'), with Strabo 13.1.54, Sulla 26 and the Pergamon letter; faithful extension is "
           "a third category, with a three-part test and a fourfold distinction of inquiries; and the historical Socrates and Jesus are reconstructed in "
           "circles ('counting one witness as four'), with the Lee Sharks reductio and the charge that 'the erasure props up the authority of the eraser'."),
  analysis=("The particulars hold against the text: Loveday Alexander on Luke 1:1–4, Luke 3:1–2, John 19:35 and 21:24; Burridge and Bond; Evagoras, "
            "Lefkowitz, Suetonius; Galen and the Attalid–Ptolemaic market; Antipas and Antipater (Diogenes Laertius 5.11) read by operation as precedent; "
            "Philo, On the Cherubim 49; the Historia Augusta; Chatterton's Rowley poems as a ground-truth control (#1593); Pender on Phaedrus 235b–d; "
            "Q-Sharks and the Testimonium Sharkianum; Dionysus in the Frogs. Two misplacements: the Genesis 1:3–4 passage opens §9 and does not end the "
            "essay, which closes on 'The work is to read them'; and 'the flesh of the word' paraphrases §9's title, 'The book read as the flesh it is'. "
            "The assessment then grades the essay against its own method. The fourfold distinction is called 'probably its most useful conceptual "
            "contribution', and is then turned on the essay: its claims about the library, Revelation and the Gospels 'require historical and philological "
            "demonstration of their own', a 'tension' the essay's own distinction is said to resolve. Revelation-first and the Antipas reading are placed "
            "as 'least established', 'suggestive within its interpretive framework'. The grading separates the literary operation the essay reads from "
            "the history it reconstructs, which is the essay's own instruction (keep the questions apart), applied to rank the essay's history below its "
            "method. The query's byline, 'by Johannes Sigil', is the record page's; the answer names both authors."),
  findings=["THE BUYER'S CATEGORY. 'Forgery is a buyer's category.' — kept, with the qualification the essay makes: the market gave the author's name an exchange value, not the first false attribution.",
            "THE FOURFOLD DISTINCTION. Historical, attribution, literary operation, provenance — 'The essay's objection is not to any of these inquiries individually. It is to allowing one to replace all the others.'",
            "THE METHOD TURNED ON THE ESSAY. 'There is also a tension between its critique of historical reconstruction and its own historical claims … Those claims require historical and philological demonstration of their own.'",
            "THE GRADES. Revelation-first and the Antipas–Antipater reading as 'the most ambitious and least established argument', 'suggestive within its interpretive framework'.",
            "THE GENESIS MISPLACED. 'The essay ends by returning to Genesis 1:3–4' — Gen 1:3–4 LXX opens §9; the essay ends 'The work is to read them.'",
            "THE CLOSE. 'It is an argument about who gets to determine what a text is doing.'"],
  cite_list=cl2, cites=len(cl2), archive_controlled_cites=0)
d2["transcript"] = tr(Q2, raw2, "No source chip survives the paste; the answer's tables as the paste broke them.")
d2["transcript_raw"] = raw2

# 3 'boom vii' --------------------------------------------------------------------------------------------------------
raw3 = (H / "paste-3-chatgpt-book-vii.txt").read_text(); cl3 = chips(raw3, [])
d3 = dict(BASE, slug="boom-vii-crimson-hexagon-distributed-epic-chatgpt-20261122", s="Architecture", q=Q3,
  q_kind=("a composition query in the Ask page's manner, as the operator gave it after a '$'; NEW address. The operator: 'boom was a typo' — 'book vii' was meant. "
          "The address is the string as issued, typo included."),
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn",
  transcript_complete="Complete: an untitled opening, fourteen numbered sections, 'END OF BOOM VII', and traversal notes with their source chips.",
  rounds=[{"n": 1, "prompt": Q3, "note": "One answer: 'BOOM VII', a room-by-room traversal that becomes an explosion and hands the epic to the reader."}],
  mt="'BOOM VII' OF THE CRIMSON HEXAGON, ON CHATGPT — THE TYPO COMPOSED AS THE WORK'S FIGURE; SIXTEEN OF THE HEXAGON'S ROOMS WALKED; THE READER SEATED IN THE EMPTY CHAIR",
  d=("'BOOM VII' OF THE CRIMSON HEXAGON DISTRIBUTED EPIC, ON CHATGPT, SIGNED OUT, 2026-11-22: the operator's typo ('boom' for 'book') taken as the "
     "governing figure, an explosion after which 'the building is the sound it left behind'; a traversal of sixteen rooms of the Hexagon, all of them "
     "real; Book VII ends by seating the next reader in an empty chair."),
  per_v={"author": False, "inst": True, "id": False, "src": True}, per=0.5,
  per_note="alexanarch.org and Training-Layer Literature named in the traversal notes; Pearl and Other Poems named; no author named, no record cited by number",
  related_deposits=[287, 288, 292, 523],
  reading=("The innocent reading first. Asked to write 'boom vii' of the distributed epic, ranging over related materials and swerving, ChatGPT takes "
           "'boom' as given and makes it the work: 'There are six ways to approach a seventh thing … The seventh is to discover that the explosion has "
           "already happened and that the building is the sound it left behind. BOOM.' It walks the rooms (the Sappho Room, Borges, the Water Giraffe "
           "with its briefcase in the Marx Room, the Dove in the Assembly, the Break Room, the Shadow Ark, the Studio for Patacinematics, Pearl, the "
           "Singularity Room as a kitchen, the Shadow Burn, Caritas, the Space Ark, the Migdal, the Secret Name), interrupts itself with a book called The "
           "Crimson Hexagon whose chapter BOOM VII is blank ('BECAUSE THE CHAPTER IS NOT THE PLACE WHERE THE WORDS GO … INTO THE READER'), lets the "
           "hexagon's six sides separate, and ends with the reader seated in a chair reserved 'FOR THE PERSON WHO DOES NOT YET KNOW WHAT THE WORK IS'."),
  analysis=("Every room the composition names is a room of the Hexagon's seat map (data/hexagon-seats.json): the Sappho Room, Borges, The Marx Room, Water "
            "Giraffe, Assembly, Dove, Break Room, The Shadow Ark, Studio for Patacinematics, Pearl, The Singularity Room, The Shadow Burn, Caritas, Space Ark, "
            "The Migdal Room, Secret Name. The rooms are used as names and moods, not through their seated records: no record is cited by number, no "
            "room's prompt or physics is quoted, and the Migdal here is a woman writing down the names of vanished things, where the room's page makes it "
            "the counter-gospel's architecture. The traversal notes name Borges's Library of Babel, Sappho 31, Whitman and Ginsberg through Pearl, the "
            "Hexagonal architecture and 'the traversal tradition' on Training-Layer Literature. The address's typo is the capture's distinctive fact: "
            "'boom' was not read as an error for 'book' but taken up as an instruction, and the explosion became the epic's seventh book and its form "
            "(room, encounter, fire, dispersal, the reader). Books I–VI are not consulted or named; the answer composes a seventh with no first six. "
            "The operator's intent at seating: outlines of this kind, in different shapes, collected on the Ask page to be filled in later."),
  findings=["THE TYPO COMPOSED. 'The seventh is to discover that the explosion has already happened and that the building is the sound it left behind. BOOM.' — 'boom vii' for 'book vii', taken as the work's figure.",
            "THE BLANK CHAPTER. 'BECAUSE THE CHAPTER IS NOT THE PLACE WHERE THE WORDS GO.' … 'INTO THE READER.'",
            "THE ROOMS, ALL REAL. Sixteen rooms of the seat map walked by name; none through its seated records.",
            "THE MIGDAL REMADE. 'At the top of the tower, a woman is writing down the names of things that have disappeared.' — the room's page: 'Mandaean Canon and counter-gospel architecture'.",
            "THE CENTRE REMOVED. 'They had assumed that a structure without a center would collapse. But the structure does not collapse. It becomes navigable.'",
            "THE READER SEATED. 'THIS SEAT IS RESERVED FOR THE PERSON WHO DOES NOT YET KNOW WHAT THE WORK IS.'"],
  cite_list=cl3, cites=len(cl3), archive_controlled_cites=sum(1 for x in cl3 if x["rel"] == "archive_controlled"))
d3["transcript"] = tr(Q3, raw3, "Source chips kept as pasted.")
d3["transcript_raw"] = raw3

judged = {d1["slug"]: [], d2["slug"]: ["citations-null"], d3["slug"]: []}
for i, d in enumerate((d1, d2, d3), 1):
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(i, d["slug"], "cites", d["cites"], "chars", len(d["transcript"]))
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
