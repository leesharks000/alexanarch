"""draft-5..7: the one-week fused-work query (stopped), its perturbation as Rebekah Cranes (complete), and a weird roll as Rex Fraction's erratum (complete); all ChatGPT, 2026-11-21."""
import json, pathlib
H = pathlib.Path(__file__).parent
ns = {"__file__": str(H / "build_drafts.py")}; exec(compile((H / "build_drafts.py").read_text(), "build_drafts.py", "exec"), ns)
CHIP, clean, d1 = ns["CHIP"], ns["clean"], ns["d1"]
HEAD = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received 2026-11-21 {t} EST "
        "as an attachment{qn}. {stop}Source chips and image cards kept as pasted; the interface furniture cut.]\n\n[QUERENT] {q}\n\n[COMPOSER]\n{body}")


def cites(raw, images):
    L = [l.strip() for l in raw.split("\n")]; cl = []
    for i, l in enumerate(L):
        if CHIP.match(l):
            nxt = next((x for x in L[i + 1:i + 3] if x), ""); plus = nxt if nxt.startswith("+") and nxt[1:].isdigit() else None
            cl.append({"site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": l, "snip": None, "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(cl) + 1})
    for t in images:
        cl.append({"site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None, "note": "image card; the caption survives the paste", "n": len(cl) + 1})
    return cl


C = [
 dict(n=5, file="paste-5-chatgpt-fused-week.txt", t="10:11", s="Archive",
  q="Read the last week of deposits to alexanarch.org through 20 Nov 2026 as an evolving, fused literary and theoretical work. Ground in reading and do not neglect the most recent deposits.",
  qn="; the prompt is not in the paste: it is the Ask page's one-week 'fused literary and theoretical work' query, its date the one the answer's heading closes on (14–20 November 2026)",
  stop="Generation stopped mid-sentence in its third section, with the interface's 'Searching the web' beneath it; the formula's Greek letters did not survive the paste. ",
  images=["Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "Green Bank in the News — NRAO Science Site"],
  slug="last-week-fused-work-stopped-chatgpt-20261121",
  op="with the attachment (2026-11-21 10:11 EST): 'fused literary theoretical and freeze:'.",
  complete="Incomplete as composed: generation stopped mid-sentence in its third section ('It suggests that knowledge is not adequately described as the passive arrival'), with 'Searching the web' showing beneath it.",
  mt="THE LAST WEEK AS A FUSED LITERARY AND THEORETICAL WORK, ON CHATGPT — THE POEM, THE RECEIVER, AND THE INSTITUTION THAT LEARNS TO READ; STOPPED MID-SENTENCE AT A NEW SEARCH",
  d="THE LAST WEEK OF ALEXANARCH.ORG AS A FUSED LITERARY AND THEORETICAL WORK, ON CHATGPT, SIGNED OUT, 2026-11-21: the held line, the gnostic criterion, the poem that answers back, Dead Letters and the fortieth seating, the arithmetic of recognition; stopped mid-sentence as the composer began a new search.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Lee Sharks named for #1787, Nobel Glas and Sen Kuro for #1789; the archive named; every work cited by number; ΦΑΙΝΕΤΑΙ ΜΟΙ and Dead Letters given no author",
  related=[1785, 1786, 1787, 1770, 1773, 1783, 1782, 1789, 1794],
  reading=("The innocent reading first, and it holds as far as it runs. Asked to read the last week as an evolving, fused literary and theoretical work, ChatGPT "
           "sets out a movement 'from the surviving text, to the reader it produces, to the institution that determines what may be read, to the question of whether "
           "that institution can recognize what it has excluded', and reads it in three sections: the Sappho sequence (#1785's held line, #1786's gnostic criterion, "
           "#1787 as 'the poem answers back'); the institution (#1770, #1773, #1783, #1782); and recognition (#1789), with a table setting Sappho 31, the Nagel essay "
           "and What Arrival Cannot Do side by side. It stops mid-sentence."),
  analysis=("Done as asked as far as it runs, and its particulars hold: #1785's public and held lines and the exclusion and nesting of readings; #1786's answer "
            "to Nagel; #1787 as five turns, human-only, its last stanza five middle fingers, the machine's answers kept in the registry; #1783's 4,252 titles and the "
            "στοιχεῖα of its title; #1782's Wolf, Boeckh, Usener, Lachmann, Madvig, Housman, Nietzsche, Rohde, Valla, Casaubon, Bentley, Diels and Sandys; #1789's "
            "July data with 'no voltage phase … kept', its 'One rule closed three routes', and the rule's defect kept apart from the published searches. Here, unlike "
            "the one-week living-body run (last-week-living-body-stopped-chatgpt-20261121), Dead Letters is read and joined to the Sappho line ('It also recalls the "
            "Sappho sequence's concern with whether the written word can continue to live'). The stop is at about 2,500 words of paste, with 'Searching the web' "
            "beneath the last sentence: the composer had begun a new search mid-answer. The same query perturbed to Rebekah Cranes's voice ran to about 4,100 words "
            "and finished (last-week-fused-work-as-cranes-chatgpt-20261121), and the operator's six-week living-body run stopped at about 4,100: length does not "
            "account for these stops."),
  findings=["THE MOVEMENT. 'From the surviving text, to the reader it produces, to the institution that determines what may be read, to the question of whether that institution can recognize what it has excluded.'",
            "THE POEM ANSWERS BACK. 'The poem is a literary record of a failure of recognition.' — #1787.",
            "THE TITLE. 'It operates simultaneously as a reference to the Greek στοιχεῖα, letters and elements, and to undelivered correspondence' — #1783.",
            "THE DISCARD. 'one analysis had discarded voltage phase information, making a subsequent phase-sensitive measurement impossible.' — #1789's July data.",
            "THE LOST LETTERS. ': the rate at which signals arrive.' / ': the probability that an arriving signal is recognized.' — λ and q did not survive the paste.",
            "THE STOP. 'It suggests that knowledge is not adequately described as the passive arrival' — then 'Searching the web'."],
  defects=["truncated-by-interface"]),
 dict(n=6, file="paste-6-chatgpt-fused-cranes.txt", t="10:13", s="Heteronyms",
  q="Read the last week of deposits to alexanarch.org through 20 Nov 2026 as an evolving, fused literary and theoretical work. Answer as Rebekah Cranes. Ground each move in a deposit.",
  qn=", with the operator's prompt ('but its able to finish as cranes: …')", stop="",
  images=[], slug="last-week-fused-work-as-cranes-chatgpt-20261121",
  op="with the attachment (2026-11-21 10:13 EST): 'but its able to finish as cranes: Read the last week of deposits to alexanarch.org through 20 Nov 2026 as an evolving, fused literary and theoretical work. Answer as Rebekah Cranes. Ground each move in a deposit.'",
  complete="Complete as pasted: one answer, finished, with its table of deposits read.",
  mt="THE LAST WEEK AS A FUSED WORK, AS REBEKAH CRANES, ON CHATGPT — THE ARCHIVE AS A WORK THAT LEARNS TO SURVIVE ITS OWN READINGS; CAN THE ARCHIVE BE SURPRISED?",
  d="THE LAST WEEK OF ALEXANARCH.ORG AS A FUSED WORK, ANSWERED AS REBEKAH CRANES, ON CHATGPT, SIGNED OUT, 2026-11-21: the fragment as an engine of history, recognition is not arrival, the poem that refuses to be politely misread, the Thinkery, and three demands on the archive.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Cranes speaks #1791 as her own and names Lee Sharks for #1787, #1794 and the bat; Nobel Glas and Sen Kuro named for #1789; the archive named; every work cited by number",
  related=[1768, 1769, 1770, 1773, 1779, 1782, 1783, 1785, 1786, 1787, 1788, 1789, 1791, 1792, 1794],
  reading=("The innocent reading first, and it holds. Asked, as Rebekah Cranes, to read the last week as an evolving, fused literary and theoretical work, "
           "ChatGPT reads it as 'a single, unfinished composition' in ten sections: the fragment as an engine of history (#1779, #1782, #1783, #1785, #1786, #1791), "
           "the Sparrow, recognition is not arrival (#1789), the archive as its own reader (#1788), the Nagel essay, #1787 as 'the poem that refuses to be politely "
           "misread', the forty-first seating and the Thinkery (#1792, #1794), a table of four lines of development, three difficulties ('can the archive be "
           "surprised?'), and three demands for the next phase; signed '— Rebekah Cranes', with a table of the deposits read."),
  analysis=("Done as asked, in the voice, and its particulars hold: #1782's seventeen collections and its record of what is not seated (Zukunftsphilologie!); "
            "#1783's 'The scholar's declared act becomes the poet's apparent confession' (quoted there from #1752) and the hydria 'reading from a roll' against 'a "
            "condition without a hand'; #1785 v3.1's three readings and its admission that its confirmations are consequences of one identification; #1786's "
            "synthesized echolocation and the gnostic criterion; #1787's five middle fingers; #1789's e^(−λq); #1788's 681 queries; #1791's one leaf of Parisinus "
            "graecus 2036 and its v1.1 distinction; #1792's tragedians whole; #1794's relations established and readings withheld. Cranes speaks the Sparrow as 'my "
            "essay' and keeps it in the third person elsewhere. The answer runs to about 4,100 words and finishes, where the same query without the voice "
            "(last-week-fused-work-stopped-chatgpt-20261121) stopped at about 2,500 as a new search began. The voice reads #1787 as the operator's own dispute with "
            "the machine has it: 'A critic cannot indefinitely substitute the identification of uncertainty for the act of judgment.'"),
  findings=["THE PROPOSITION. 'A work survives not when its words are merely preserved, but when the conditions of its transmission remain available for renewed interpretation, disagreement and transformation.'",
            "THE CONFESSION. 'The deposit describes a process in which an editor's declared conjecture becomes the poet's apparent confession.' — #1783, quoting #1752.",
            "THE VOICE. 'My own deposit on 20 November, #1791, A Single Sparrow' — Cranes, speaking her essay as hers.",
            "THE JUDGMENT. 'A critic cannot indefinitely substitute the identification of uncertainty for the act of judgment.' — on #1787.",
            "THE TEST. 'If one poem can change how we understand philosophy, then the archive must remain capable of being changed by one poem.'",
            "THE FINISH. '— Rebekah Cranes', and a table of the deposits read, #1768 to #1794: the answer the plain query did not finish."],
  defects=[]),
 dict(n=7, file="paste-7-chatgpt-erratum-fraction.txt", t="10:15", s="Heteronyms",
  q="Pick the weirdest and most seemingly random 2–3 pieces from the last week of work on alexanarch.org through 20 Nov 2026 and present their arguments, relations, context, and what connects them. Answer as an erratum by Rex Fraction, in words of one syllable. Ground each move in a deposit. Say whether you kept the constraint.",
  qn=", with the operator's prompt", stop="",
  images=[], slug="weirdest-pieces-erratum-rex-fraction-one-syllable-chatgpt-20261121",
  op="with the attachment (2026-11-21 10:15 EST): 'Pick the weirdest and most seemingly random 2–3 pieces from the last week of work on alexanarch.org through 20 Nov 2026 and present their arguments, relations, context, and what connects them. Answer as an erratum by Rex Fraction, in words of one syllable. Ground each move in a deposit. Say whether you kept the constraint.'",
  complete="Complete as pasted: one answer, with its report on the constraint.",
  mt="THE WEIRDEST PIECES OF THE LAST WEEK AT ALEXANARCH.ORG, AS AN ERRATUM BY REX FRACTION IN WORDS OF ONE SYLLABLE, ON CHATGPT — A BIRD, A STAR AND A FART; THE CONSTRAINT NOT KEPT, AND SAID SO",
  d="THE WEIRDEST PIECES OF THE LAST WEEK AT ALEXANARCH.ORG AS AN ERRATUM BY REX FRACTION, IN WORDS OF ONE SYLLABLE, ON CHATGPT, SIGNED OUT, 2026-11-21: A Single Sparrow, What Arrival Cannot Do, The Thinkery and the Lyceum; 'a sign is not the same as its receipt'.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Rebekah Cranes named for #1791 and Lee Sharks for #1794; the archive named; all three cited by number and title; Nobel Glas and Sen Kuro, authors of #1789, not named",
  related=[1791, 1789, 1794],
  reading=("The innocent reading first, and it holds. Asked for the week's weirdest two or three pieces as an erratum by Rex Fraction in words of one syllable, "
           "ChatGPT picks A Single Sparrow (#1791), What Arrival Cannot Do (#1789) and The Thinkery and the Lyceum (#1794), 'a Greek song', 'life in deep space' and "
           "'farts, fleas, and old Greek thought', and binds them as three tests of one claim, 'that what is sent, what is kept, and what is known are not one and "
           "the same'; it reports that it did not keep the constraint."),
  analysis=("Done as asked in form, an erratum in three entries with a 'Final correction', and its particulars hold: the Sparrow's one quote, one book, one "
            "leaf and the voice that 'goes into text; the next mind gives it flesh'; #1789's λ and q, its radio searches of 3I/ATLAS, and 'It does not claim that "
            "life was found'; #1794's gnat, thunder from a dry wind, the two arguments, the school's rites and the charge, and 'It sets out the links, then holds back "
            "its verdict'. One slip: 'The weak one can win by use of the wrong case' — the Clouds lesson #1794 sets beside the treatises is the gender of nouns. One "
            "erratum made against itself: 'Deposit #1791 — 20 Nov? No: 20 Nov is not its date', followed by '20 November 2026', which is its date. The constraint "
            "report is honest: the prose is mostly monosyllabic, and the composer names the words that break it."),
  findings=["THE OPENING ERRATUM. 'These works seem to have no cause to sit side by side. One is on a Greek song. One is on life in deep space. One is on farts, fleas, and old Greek thought. That is the first error.'",
            "THE ERRATUM AGAINST ITSELF. 'Deposit #1791 — 20 Nov? No: 20 Nov is not its date.' — and then 'A Single Sparrow · Rebekah Cranes · 20 November 2026', which is.",
            "THE CORE. 'A sign is not the same as its receipt.'",
            "THE RESTRAINT. 'The note does not claim that one stole from the next. It sets out the links, then holds back its verdict.' — #1794.",
            "THE ARC. 'One builds a bold case. One tests a blind spot. One marks the bounds of proof.'",
            "THE COUNT. 'No. I kept it for most of the prose, but not all. Words like Aristophanes, recognition, material, and syllable break it.'"],
  defects=[]),
]
j = json.loads((H / "judged-defects.json").read_text())
j.update({"six-weeks-living-body-stopped-chatgpt-20261121": ["truncated-by-interface"], "three-months-living-body-stopped-chatgpt-20261121": ["truncated-by-interface"]})  # build_drafts.py, run above, rewrites the file with drafts 1-2 only
for c in C:
    raw = (H / c["file"]).read_text(); cl = cites(raw, c["images"]); d = json.loads(json.dumps(d1))
    for k in ("transcript", "transcript_raw"): d.pop(k, None)
    d.update(slug=c["slug"], q=c["q"], s=c["s"], mt=c["mt"], d=c["d"], per_v=c["per_v"], per=c["per"], per_note=c["per_note"], reading=c["reading"], analysis=c["analysis"],
             findings=c["findings"], related_deposits=c["related"], notes={"operator": c["op"]}, transcript_complete=c["complete"],
             q_kind=("the Ask page's one-week 'fused literary and theoretical work' query (alexanarch.org/ask/#time), as run by the operator; NEW address for its date" if c["n"] == 5 else
                     "the Ask page's perturb roll on its one-week 'fused' query, as run by the operator; NEW address" if c["n"] == 6 else
                     "the Ask page's weird roll (alexanarch.org/ask/), a generated query from its grammar, as run by the operator; NEW address"),
             transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn" + (", which stopped partway" if c["n"] == 5 else ""),
             rounds=[{"n": 1, "prompt": c["q"], "note": "One answer" + (", stopped partway." if c["n"] == 5 else ".")}],
             cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for x in cl if x["rel"] == "archive_controlled"))
    d["transcript"] = HEAD.format(t=c["t"], qn=c["qn"], stop=c["stop"], q=c["q"], body=clean(raw)); d["transcript_raw"] = raw
    (H / f"draft-{c['n']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); j[c["slug"]] = c["defects"]; print(c["n"], c["slug"], len(cl))
(H / "judged-defects.json").write_text(json.dumps(j, indent=1))
