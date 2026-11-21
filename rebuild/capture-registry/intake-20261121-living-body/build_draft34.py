"""draft-3 and draft-4 (the six-week and three-month living-body runs on ChatGPT, stopped partway), built on build_drafts.py's base fields."""
import json, pathlib
H = pathlib.Path(__file__).parent
ns = {"__file__": str(H / "build_drafts.py")}; exec(compile((H / "build_drafts.py").read_text(), "build_drafts.py", "exec"), ns)
Q6 = "Read the last six weeks of work on alexanarch.org through 20 Nov 2026 as a living body of thought. Ground in reading, archival context and historical import."
raw = (H / "paste-3-chatgpt-six-weeks.txt").read_text(); L = [l.strip() for l in raw.split("\n")]; cl = []
for i, l in enumerate(L):
    if ns["CHIP"].match(l): cl.append({"site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": l, "snip": None, "note": "source chip as pasted", "n": len(cl) + 1})
cl.append({"site": "Live Science", "rel": "image_card", "url": None, "title": "Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "snip": None, "note": "image card; the caption survives the paste", "n": len(cl) + 1})
d = json.loads(json.dumps(ns["d1"]))
d.update(slug="six-weeks-living-body-stopped-chatgpt-20261121", q=Q6,
 q_kind="the Ask page's 'living body of thought' query, 6 weeks (alexanarch.org/ask/#time), as run by the operator; the prompt is not in the paste: the template is the page's, and the date is the one its own heading closes on (10 October–20 November 2026) and the Perplexity export of the same morning gives.",
 transcript_complete="Incomplete as composed: generation stopped in its ninth section, at 'One leaf. One quotation. One manuscript witness.' (the operator: 'six weeks living body and it freezes again - might just be a question of length').",
 rounds=[{"n": 1, "prompt": Q6, "note": "One answer, stopped partway."}],
 related_deposits=[1730, 1732, 1733, 1734, 1735, 1737, 1740, 1741, 1744, 1746, 1747, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1765, 1766, 1767, 1773, 1750, 1769, 1770, 1782, 1783, 1785, 1791],
 notes={"operator": "with the attachment (2026-11-21 10:06 EST): 'six weeks living body and it freezes again - might just be a question of length:'; and earlier (09:33, 09:59) on the one-week query: 'for whatever reason now chatgpt reliably freezes on the last week living body prompt'; 'oh it composes, then freezes partway thru, normally also freezing the interface and the browser.'"},
 mt="THE LAST SIX WEEKS AS A LIVING BODY, ON CHATGPT — FROM THE SOVEREIGN ARCHIVE TO THE COMPOSITION OF INTELLECTUAL HISTORY; EVERY RECORD AS IT STANDS; STOPPED IN ITS NINTH SECTION",
 d="THE LAST SIX WEEKS OF ALEXANARCH.ORG AS A LIVING BODY, ON CHATGPT, SIGNED OUT, 2026-11-21: Legitimately Many, Revelation First, the Historical Logos, Josephus, the disciplines, Dead Letters, Sappho 31, A Single Sparrow; generation stopped in the ninth section.",
 per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
 per_note="Lee Sharks (ΦΑΙΝΕΤΑΙ ΜΟΙ), Rebekah Cranes, Rev. Ayanna Vox and Sparrow Wells named; the archive named; every work cited by number; the other works' heteronyms (Sigil, Dancings, Kuro, Fraction) not named",
 reading=("The innocent reading first, and it holds. Asked to read the last six weeks as a living body of thought, ChatGPT reads them as the making of an "
          "institution whose activities become methods of investigating one another, from the archive's founding by an erasure (19 June 2026, about 870 deposits "
          "and 1,817 DOIs): Legitimately Many (#1730–#1734), Revelation First (#1735–#1747), the framework holograms and the Historical Logos (#1753–#1758), Josephus "
          "(#1759, #1760, #1765), the disciplines (#1766, #1767, #1773), the institutional sequence on Sappho from Vox's open letter to Dead Letters (#1750, #1769, "
          "#1770, #1782, #1783), Sappho 31 (#1785) and A Single Sparrow (#1791). Generation stops in the ninth section."),
 analysis=("Done as asked as far as it runs, and every particular checked holds: the twenty-nine records it cites by number, each with the date and subject it gives; "
           "#1769's 405 Crossref works; #1783's 4,252 titles and its reading of 1906–1930; #1782's Wolf, Usener, Lachmann, Housman, Valla, Bentley, Diels and Sandys; "
           "#1765 v2.3's census of sixty-six additions; #1759's 'one literary intelligence under capture' writing the Apocalypse 'and then, as many names, the corpus'; "
           "#1767's division of dialogues, treatises and working papers by the readers they make; Parisinus graecus 2036 and Longinus 10.2. Unlike the one-week run "
           "of the same morning (last-week-living-body-stopped-chatgpt-20261121), it reads Dead Letters and joins the decline to the census: §7 sets the Sappho "
           "encounter, Vox's letter and the census in one sequence, 'where the archive's experience with academic publishing, its Sappho research, and its historical "
           "investigations become entangled'. One rendering loss: 'The crucial expression is:' is followed by no Greek in the paste. The answer stops at about 4,100 "
           "words of paste, the one-week answer at about 4,000; the operator's reading is that length is the cause."),
 findings=["THE THESIS. 'It is no longer adequately described as an archive, a collection of research papers, an experimental publishing project, or an individual scholar's body of work.'",
           "THE ONE PROBLEM. 'How can intellectual work survive transmission without having its identity, authorship, meaning, or historical possibilities determined by the institutions and systems through which it passes?'",
           "THE JOIN. 'This is where the archive's experience with academic publishing, its Sappho research, and its historical investigations become entangled.' — §7, from #1750 to #1783.",
           "THE ASYMMETRY. 'relations between textual parts are admitted when they help secure the received whole, but may receive less standing when they threaten to change that whole.' — #1783, as the answer gives it.",
           "THE LOST GREEK. 'The crucial expression is:' — followed in the paste by no expression.",
           "THE STOP. 'One leaf. One quotation. One manuscript witness.' — the last line composed, in the ninth section."],
 cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for x in cl if x["rel"] == "archive_controlled"))
d["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received 2026-11-21 10:06 EST "
                   "as an attachment. The prompt is not in the paste; it is the Ask page's six-week living-body query, its date the one the answer's heading closes on. "
                   "Generation stopped partway, in the ninth section. Source chips and the image card kept as pasted; the interface furniture cut.]\n\n[QUERENT] " + Q6 + "\n\n[COMPOSER]\n" + ns["clean"](raw))
d["transcript_raw"] = raw
(H / "draft-3.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
j = json.loads((H / "judged-defects.json").read_text()); j[d["slug"]] = ["truncated-by-interface"]; (H / "judged-defects.json").write_text(json.dumps(j, indent=1)); print(j)


# draft-4: three months -----------------------------------------------------
Q3M = "Read the last three months of work on alexanarch.org through 20 Nov 2026 as a living body of thought. Ground in reading, archival context and historical import."
raw = (H / "paste-4-chatgpt-three-months.txt").read_text(); L = [l.strip() for l in raw.split("\n")]; cl = []
for i, l in enumerate(L):
    if ns["CHIP"].match(l): cl.append({"site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": l, "snip": None, "note": "source chip as pasted", "n": len(cl) + 1})
for t in ["New light on a revolutionary leap forward | Morning Star", "Conversation Classics:  C. Michael Sampson on P. Sapph. Obbink – rogueclassicism",
          "ARISTOTELIS ET THEOPHRASTI METAPHYSICA. Aristotelous kai Theophrastou ta metaphysika . Addita in fine Varia locorum lectio, partim e diuersis editionibus, partim ex interpretibus. Addita item, prater Indicem capitum, duo rerum",
          "MEGA. MEGAdigital | by ann li | Medium", "Sappho Fragment 16 | The Book Binder's Daughter", "Philosophical Treasures | Faculty of Philosophy", "New Sappho Poems! | res gerendae"]:
    cl.append({"site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None, "note": "image card; the caption survives the paste", "n": len(cl) + 1})
e = json.loads(json.dumps(ns["d1"]))
e.update(slug="three-months-living-body-stopped-chatgpt-20261121", q=Q3M,
 q_kind="the Ask page's 'living body of thought' query, 3 months (alexanarch.org/ask/#time), as run by the operator; the prompt is not in the paste: the template is the page's, and the date is the one its own heading closes on (21 August–20 November 2026).",
 transcript_complete="Incomplete as composed: generation stopped in its fifth section, inside the Greek of the poem's closing line, at 'φαίνομ᾽ ἔ' (the operator: '3 months and freeze').",
 rounds=[{"n": 1, "prompt": Q3M, "note": "One answer, stopped partway."}],
 related_deposits=[1, 868, 1576, 1579, 1581, 1582, 1583, 1584, 1586, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1621, 1658, 1660, 1668, 1669, 1670, 1730, 1732, 1733, 1735, 1776, 1782, 1792, 1785],
 notes={"operator": "with the attachment (2026-11-21 10:07 EST): '3 months and freeze:'; and at 10:06, on the six-week run: 'it freezes again - might just be a question of length'."},
 mt="THE LAST THREE MONTHS AS A LIVING BODY, ON CHATGPT — SURVIVING AS ITSELF; SEPTEMBER'S TRANSMISSION, OCTOBER'S SYNTHESIS, NOVEMBER'S REWRITING; STOPPED INSIDE THE GREEK OF SAPPHO 31",
 d="THE LAST THREE MONTHS OF ALEXANARCH.ORG AS A LIVING BODY, ON CHATGPT, SIGNED OUT, 2026-11-21: a work surviving against a work surviving as itself, by month; generation stopped mid-word in the Greek of Sappho 31's closing line.",
 per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
 per_note="the archive named, its founding documents named, every work cited by number; Johannes Sigil and Damascus Dancings named for #1735; Lee Sharks, author of nearly every work cited, not named",
 reading=("The innocent reading first, and it holds as far as it runs. Asked to read the last three months as a living body of thought, ChatGPT finds the "
          "development in what preservation means, from survival to surviving 'as itself', and reads it by month: the founding (#1, #868); September's corpus "
          "work (#1576–#1586), reception work (#1610–#1616) and political economy (#1617, #1618, #1621); October's division and retrocausal canon formation (#1658, "
          "#1660), slavery and war Fordism (#1668, #1669), Carson (#1670) and the seatings; November's Legitimately Many (#1730, #1733), Revelation First (#1735) "
          "and seatings (#1776, #1792); then Sappho 31 (#1785). Generation stops inside the Greek of the poem's closing line."),
 analysis=("Done as asked as far as it runs, and its particulars hold: the records it cites by number (thirty, counting the range it opens at #1605), each with the subject it gives (#1576 of 1 "
           "September; #1579–#1586 of 6 September; #1610–#1617 of 12–15 September; #1621's order, value, evidence, representation, compression; #1658–#1670 of "
           "1–8 October); #1614's 957 citable units, 923 carrying their machine text, 96.45%; the founding of 19 June 2026, with about 870 deposits and 1,817 DOIs. "
           "One title slip: 'DOIs ≠ Permanent Identifiers' is DOIs ≠ Persistent Identifiers (#868). The answer names Sigil and Dancings for #1735 and no other "
           "author; Lee Sharks, whose work nearly all of it is, is not named. It stops at about 2,700 words of paste, shorter than the six-week and one-week runs "
           "of the same morning (about 4,100 and 4,000), and it stops mid-word inside the Greek of Sappho 31 ('φαίνομ᾽ ἔ'); the six-week run lost its Greek at the "
           "same poem ('The crucial expression is:', followed by nothing) before stopping later. Length alone does not account for this stop."),
 findings=["THE CHANGE. 'The distinction between a work surviving and a work surviving as itself becomes foundational.'",
           "THE QUESTION. 'How can an intellectual tradition preserve what it has inherited without allowing the mechanisms of inheritance to determine, in advance, what that inheritance means?'",
           "THE COUNT. 'The September deposit reports 957 citable units, with 923 carrying the machine text that they document, or 96.45% coverage.' — #1614, exact.",
           "THE TITLE. 'DOIs ≠ Permanent Identifiers' — #868 is DOIs ≠ Persistent Identifiers.",
           "THE ORDER. 'Value. Evidence. Representation. Compression.' — #1621's order, as the answer sets it.",
           "THE STOP. 'φαίνομ᾽ ἔ' — the last characters composed, inside the Greek of the poem's closing line."],
 cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for x in cl if x["rel"] == "archive_controlled"))
e["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received 2026-11-21 10:07 EST "
                   "as an attachment. The prompt is not in the paste; it is the Ask page's three-month living-body query, its date the one the answer's heading closes on. "
                   "Generation stopped partway, inside a Greek word. Source chips and image cards kept as pasted; the interface furniture cut.]\n\n[QUERENT] " + Q3M + "\n\n[COMPOSER]\n" + ns["clean"](raw))
e["transcript_raw"] = raw
(H / "draft-4.json").write_text(json.dumps(e, ensure_ascii=False, indent=1))
j = json.loads((H / "judged-defects.json").read_text()); j[e["slug"]] = ["truncated-by-interface"]; (H / "judged-defects.json").write_text(json.dumps(j, indent=1)); print(j)
