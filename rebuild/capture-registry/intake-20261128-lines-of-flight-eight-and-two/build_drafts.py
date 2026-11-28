"""Ten drafts, 2026-11-28. Eight ChatGPT answers to one question put to eight records by their 'Ask ChatGPT otherwise' link 'lines of flight'
(pasted by the operator 13:00 EST); one ChatGPT answer to #1812's 'arguments' link (pasted 01:23 EST); one Google AI Overview at the quoted
first line of #1809 (pasted 00:33 EST with six screengrabs, staged with EA-CORPORA-44). Seat each with:
    python3 scripts/capture_intake.py rebuild/capture-registry/intake-20261128-lines-of-flight-eight-and-two/<name>.json --seat"""
import json, pathlib, re, html, urllib.parse
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
REG = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def link_query(n, marker):
    page = (ROOT / f"s/records/{n}/index.html").read_text(encoding="utf-8")
    for m in re.finditer(r'href="https://chatgpt\.com/\?[^"]*?q=([^"&]+)', page):
        q = urllib.parse.unquote_plus(html.unescape(m.group(1)))
        if marker in q: return q
    raise SystemExit(f"no link with {marker!r} on record {n}")
def cards(paste):
    L = paste.split("\n"); out = []
    for i, ln in enumerate(L):
        if i + 1 < len(L) and re.fullmatch(r"\+\d+", L[i + 1].strip()) and ln.strip():
            out.append({"site": ln.strip() + " " + L[i + 1].strip(), "rel": "archive_controlled" if re.search(r"Alexanarch|Capture Registry|Hologram|AXN", ln) else "outside", "url": None, "title": None, "snip": None, "note": "source chip as pasted"})
        elif i + 1 < len(L) and L[i + 1] == " " and ln.strip() and len(ln) > 12:
            out.append({"site": "(image card)", "rel": "outside", "url": None, "title": ln.strip(), "snip": None, "note": "image card as pasted"})
    for i, c in enumerate(out): c["n"] = i + 1
    return out
GPT = dict(date="2026-11-28", dates=["2026-11-28"], surface="ChatGPT", surfaces=["ChatGPT"],
           surface_basis="The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT', 'ChatGPT is AI and can make mistakes.').",
           auth="signed out, incognito", auth_basis="Operator defaults (2026-10-01, 2026-10-14); the paste's own 'Log in'.", ev="paste", turns=1)
PEND = {"since": "2026-11-28", "reason": "no atom set yet for this work as a target", "breach": False}
BATTERY = (" ONE QUESTION, EIGHT RECORDS. The eight answers of 2026-11-28 to this question (#1802, #1803, #1804, #1806, #1807, #1810, #1811, #1812) share one answer form: an opening that the "
           "work 'leads toward something larger than' its subject; numbered directions under write, read and build; a table of proposed next works under titles the composer invents; a section on what "
           "is not yet established; and a closing sentence of the form 'from X to Y'. Each names the record by number and reads other records beside it. What varies is the content carried inside the form.")
OPN = "pasted 2026-11-28 13:00 EST, eight attachments: 'from the lines of flight ask chatgpt differently buttons', with the #1812 query written out in the message"
def gpt(name, n, slug, s, marker, kind_note, extra_related, mt, d, reading, analysis, findings, note_src, op=OPN, battery=True):
    paste = (H / f"{name}.txt").read_text(encoding="utf-8"); rec = REG[n]; q = link_query(n, marker); creator = rec["creator"].split(";")[0].strip()
    sur = creator.split(",")[0]; c = cards(paste)
    pv = {"author": sur in paste, "inst": bool(re.search(r"Alexanarch|Crimson Hexagonal", paste)), "id": f"#{n}" in paste, "src": bool(re.search(r"Alexanarch|deposit", paste))}
    dd = dict(GPT, slug=slug, s=s, q=q, q_kind=kind_note,
        originator={"name": creator, "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": f"Alexanarch #{n} ({rec['axn'].split('.')[0]}), creator of record {rec['creator']}. Recorded 2026-11-28."},
        related_deposits=[n] + extra_related,
        transcript="[QUERENT] " + q + "\n\n" + paste,
        transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's one answer on the unauthenticated interface; the query is the record's link text, taken by code from the record page",
        transcript_complete="One answer complete as supplied, from its title line to 'ChatGPT is AI and can make mistakes.' Image captions and source chips stand as pasted.",
        transcript_read="READ IN FULL 2026-11-28; figures, quotations, section and deposit numbers checked by string search against the seated texts of the records named (the checks and the misses are in the findings)",
        cites=len(c), cite_list=c, per_v=pv,
        per_note=f"Author named: {pv['author']} ({creator}); archive named: {pv['inst']}; record number given: {pv['id']}; sources shown: {len(c)} chips or image cards as pasted.",
        per_dim_pending=PEND, mt=mt, d=d, reading=reading, analysis=analysis + (BATTERY if battery else ""), findings=findings,
        notes={"operator": op, "source": f"{name}.txt, the paste unchanged", "date_basis": "the date is the day the paste was received; the paste carries no time of its own"})
    if name == "lof-1802":
        dd["notes"]["engagement_basis"] = "an 18 KB composed answer citing #1802 and seven other records; the intake's non-engagement pattern matched the composer's own words 'What it did not search.', an item in its list of what an answer engine should distinguish"
    if name == "trad-1810":
        dd["notes"]["model_line"] = "the paste ends: 'You’re using our basic model. Log in or sign up for more intelligence.'"
    (H / f"{name}.json").write_text(json.dumps(dd, ensure_ascii=False, indent=1), encoding="utf-8"); print(name, len(paste), "chips", len(c), pv, "|", q[:70])
LOF = "lead beyond itself"
KIND = lambda n: f"the record's 'Ask ChatGPT otherwise' link 'lines of flight' (alexanarch.org/s/records/{n}/); NEW address; one of eight records asked the same question on 2026-11-28. The string seated is the link's own, read from the record page by code" + (", and it is the string the operator wrote out in the message." if n == 1812 else "; the operator wrote out the #1812 string, and this answer's title and subject agree with this record's.")

gpt("lof-1812", 1812, "matthew-from-revelation-1812-lines-of-flight-chatgpt-20261128", "Revelation First", LOF, KIND(1812), [1813, 1755, 1758, 1735, 202],
 mt="HOW TO WRITE MATTHEW FROM REVELATION (#1812) ON CHATGPT, LINES OF FLIGHT — THE PAPER READ AS A METHOD OTHERS CAN RUN; #1813 NAMED AS THE NEXT RUNG; THE ANSWER STANDS AT v1.1 THE DAY AFTER v2.1",
 d=("HOW TO WRITE MATTHEW FROM REVELATION (#1812) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': the grammar given as three parameters (a past, a land, ancestral layers), "
    "seven moves and five forms; 158 relations and 305 of 1,067 verses, against 86 and 178; the labourers run under a sealed key; #1813 with 133 relations and nine statuses; five things to produce next "
    "(an atlas, a blind-generation laboratory, the inverse grammar, the other Gospels, a genealogy of the corpus). It reports the paper as 'version 1.1'; v2.1, deposited the day before, is not named."),
 reading=("The innocent reading first. Asked where the paper leads, the composer answers that it leads to 'a reproducible method', and it reads the paper as one: source held whole, three parameters, moves, forms, "
          "a ledger, a blind run. Its figures are the paper's (158 and 305; 86 and 178; 100 of 458, 70 of 184, 135 of 425; six of seven sealed predictions on the third parameter, the free Philo control failed). "
          "It keeps the paper's limits: every relation can be read backwards, the other-source control is outstanding, and 'the current 28.6% reach is not, by itself, evidence'. It names #1813 as the place where "
          "Matthew stops standing alone."),
 analysis=("Attributed, numbered and read from the record. Two things are to be marked. First, the answer stands at the earlier version: it says 'version 1.1', gives the procedure as 'version 0.4', and names none "
           "of what v2.1 added (the letters, Josephus, Thomas, the map and its 61.8 to 64.9 per cent); the 'arguments' answer received the same day names v2.1 and its date. What the composer was served is not "
           "established here. Second, two of its terms were not found in the seated v2.1 text: the five forms under the names 'likening' and 'foretelling', and 'version 0.4' as a version (0.4 is a section number there). "
           "Its count of '762' remaining verses is 1,067 less 305."),
 findings=["THE PAPER READ AS A PROCEDURE. 'A generative grammar specifies a procedure that someone else can execute.' Parameters, moves, the ledger and the labourers run are reported from the text.",
           "FIGURES HOLD. 158/305, 86/178, the three source rows, six of seven, Matthew 15 without a row, De somniis 2.246, Vos and Bauckham, Revelation 13:10: each found in the seated text of #1812.",
           "THE ANSWER STANDS AT v1.1. It says 'version 1.1' and never v2.1; no letters, Josephus, Thomas or map. v2.1 was deposited in place on 2026-11-27; the same day's 'arguments' answer reads v2.1.",
           "TWO TERMS NOT FOUND. 'likening' and 'foretelling' as names of forms, and 'version 0.4' as a version, are not in the seated v2.1 text. Not traced to v1.1 here.",
           "#1813 NAMED AND COUNTED. '133 relations' and the nine statuses, 'Produced blind' to 'Failed', are in #1813.",
           "THE DIRECTION QUESTION KEPT OPEN. The inverse grammar and the competing-source run are given as the two experiments that 'could substantially strengthen or weaken the larger programme'."],
 note_src="")

gpt("arg-1812", 1812, "matthew-from-revelation-1812-arguments-chatgpt-20261128", "Revelation First", "What are the arguments in",
 "the record's 'Ask ChatGPT' link, the arguments query (alexanarch.org/s/records/1812/); NEW address. The operator's message: 'from its ask chatgpt link'. The string seated is the link's own, read from the record page by code.",
 [1813, 1735],
 mt="HOW TO WRITE MATTHEW FROM REVELATION (#1812) ON CHATGPT, THE ARGUMENT — v2.1 READ THE DAY AFTER ITS DEPOSIT; THE LEDGER AND THE MAP HELD APART; DIRECTION, CONTROLS AND FAILED PREDICTIONS REPORTED",
 d=("HOW TO WRITE MATTHEW FROM REVELATION (#1812) ON CHATGPT, SIGNED OUT, INCOGNITO, RECEIVED 2026-11-28 01:23 EST, AT THE RECORD'S ASK LINK: the received account stated first; three levels of demonstration; "
    "give the speaker a past; Revelation 12 into Matthew 2; the labourers, thirteen of thirteen under a sealed key, with the controls; Matthew handling Revelation as it handles scripture (55 per cent against 28.6 and 22); "
    "nine steps and twenty-one rules; 158 relations, 305 verses; the map's 61.8 to 64.9 per cent held apart from the ledger's 28.6; what is not established (direction, controls, failures). 'The current version of the deposit is v2.1, dated 27 November 2026.'"),
 reading=("The innocent reading first. Asked for the arguments, the composer gives them in the paper's order and with the paper's own distinction between showing that Revelation can generate Matthew and proving that it did. "
          "It reports the two measures separately and says the author 'explicitly refuses to treat the larger number as equivalent to demonstrated derivation'. It reports the failed plagues-to-miracles prediction and the absence of a "
          "preserved sequence. It separates four arguments (philological, compositional, experimental, historical-genetic) and assigns the strongest claim to the programme, not the paper."),
 analysis=("Attributed, numbered, at the current version. The figures were checked against the seated text and hold (158, 305, 28.6; 100 of 458, 70 of 184, 135 of 425; 55 and 22; thirteen of thirteen; 61.8 to 64.9). One figure comes "
           "from the record's description and not from the text: '321 Greek quotations', which is the description's count and was not recounted for v2.1. The posited-sources argument of v2.1 (no hypothetical source supposed; the "
           "remainder held as unexplained) is given in the composer's words as 'an extant text that can be inspected and tested should be considered as a source before hypothetical documents are accepted as necessary explanations'."),
 findings=["v2.1 READ ONE DAY AFTER DEPOSIT. The answer names the version and its date, and reports the map beside the ledger.",
           "THE TWO MEASURES HELD APART. 28.6 per cent as 'the more demanding derivational ledger'; 61.8 to 64.9 per cent as 'a broader map of named textual correspondences'.",
           "LIMITS REPORTED AS LIMITS. Direction, the outstanding control, the failed predictions and the absent sequence are given as 'substantive limitations, not minor qualifications'.",
           "ONE FIGURE FROM THE DESCRIPTION. '321 Greek quotations' is in the record's description, not in the v2.1 text.",
           "THE PROGRAMME SET APART FROM THE PAPER. 'This is a proposed literary genealogy, not a chronology established by the Matthew demonstration.'"],
 note_src="", op="pasted 2026-11-28 01:23 EST: 'from its ask chatgpt link'", battery=False)

gpt("lof-1810", 1810, "how-much-you-wanna-bet-1810-lines-of-flight-chatgpt-20261128", "Valuation", LOF, KIND(1810), [1791, 1745, 1802, 1631, 1621, 1624, 1622, 1627, 1735],
 mt="HOW MUCH YOU WANNA BET? (#1810) ON CHATGPT, LINES OF FLIGHT — THE RECOVERY EVENT AS THE OBJECT VALUED; NESTED REVALUATION; 'SETTLEMENT → ACCUMULATION → CONSTRAINT'; THE INVALID NUMBER REPORTED AS INVALID",
 d=("HOW MUCH YOU WANNA BET? (#1810, REX FRACTION) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': the object valued is 'a recovery event'; transition load Θ joining A Single Sparrow (#1791) and "
    "The Cost of the Cone (#1745); 132 components, the largest of 209 records, a longest chain of 52; 358 records in the citation closure, 58.5 and 50.4 per cent; recovery of an object against recovery of a position (Nag Hammadi, Qumran, "
    "Linear B; Copernicus); five quantities kept apart; six proposed works, first a 'Dependency Atlas'. '$7.2 × 10²⁶' is reported as 'deliberately invalid as a monetary valuation'."),
 reading=("The innocent reading first. The composer takes the dossier's own governing question from #1621, 'What became possible because this exists?', and answers that what became possible is valuing a recovery by tracing what "
          "depends on the restored position. It reports the archive computation as the dossier does, with the caution that the figures 'describe the computed archive structure, not a demonstrated 52-generation dependency in New Testament scholarship'. "
          "It carries #1802's separation of benefit from causation into the account of institutions, and says of the exposure mechanism: 'a hypothesis about structural incentives, not proof of deliberate suppression'."),
 analysis=("Attributed to Rex Fraction by name, numbered, read with seven other records. Figures and terms checked against the seated text of #1810 hold (132, 209, 52, 358, 58.5, 50.4, 7.2, transition load, semantic exposure, "
           "recovery event, the three examples of recovered objects). The composer keeps the dossier's refusal to price: the debt is not 'an automatically collectible financial claim'. The six proposed titles are the composer's."),
 findings=["THE OBJECT IS THE RECOVERY. 'It is a recovery event: restoring a text to the position of source in the corpus that became the New Testament.'",
           "THE COMPUTATION REPORTED WITH ITS LIMIT. 132, 209, 52, 358, 58.5 and 50.4 per cent, with 'Citation reach is not equivalent to demonstrated intellectual dependency.'",
           "THE INVALID NUMBER KEPT INVALID. '$7.2 × 10²⁶, is deliberately invalid as a monetary valuation. It is an artifact of an attempted commensuration, audited to failure, not an estimate.'",
           "INCENTIVE AND FUNCTION, NOT CONSPIRACY. Section 3 of the answer is headed as a theory of institutional resistance 'that does not depend on proving conspiracy'.",
           "THE HETERONYM IS THE AUTHOR. The dossier is 'Rex Fraction's' throughout.",
           "PROPOSED TITLES ARE THE COMPOSER'S. 'The Dependency Atlas of Revelation First', 'The Political Economy of Revelation Last', 'The Standing Problem' and three more are offered as next works; none is a record."],
 note_src="")

gpt("lof-1811", 1811, "revelation-first-not-the-first-revelation-1811-lines-of-flight-chatgpt-20261128", "Revelation First", LOF, KIND(1811), [1735, 1677, 1755],
 mt="REVELATION FIRST ≠ THE FIRST REVELATION (#1811) ON CHATGPT, LINES OF FLIGHT — THE TWO ENTITIES HELD APART; POSITIONAL LIQUIDATION TAKEN AS v1.1'S ADDITION; THREE PRIORITIES SEPARATED",
 d=("THE METADATA PACKET (#1811) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': Revelation First (Lee Sharks's thesis) against the First Revelation (Hira, Qur'an 96:1–5); three operations "
    "(entity erasure, directional propositional erasure, positional liquidation); the two Overviews of 24 June and 25 November 2026; #1735's absolute, corpus and generative priority; the MPAI specification (#1677); the framework hologram (#1755). "
    "It proposes a standalone study, 'From Directional Propositional Erasure to Positional Liquidation'."),
 reading=("The innocent reading first. The composer states the distinction the packet exists to hold, and holds it: 'an answer about the second entity is not an answer about the first. Nor is disambiguation an endorsement of the thesis.' "
          "It takes positional liquidation as the addition of v1.1 and reports the packet's own homology between the order of a name's words and the order of a canon's books, with the limit: 'It does not establish the historical priority thesis.' "
          "It sends the reader to #1735 for the substance."),
 analysis=("Attributed and numbered; the thesis stated in its own direction. Checked against the seated texts: the three operation names, 24 June and 25 November, Hira and 96:1, the minimum composition answer (all #1811); "
           "roughly 69,400 units, στέφανος τῆς ζωῆς, Gallio, the work-toil-endurance triad (#1735). Not found: 'approximately 70,000' for the second census in #1735, and 'nine lines of research' as a count in #1755 (the phrase 'lines of research' is there). "
           "The 'possible Revelation First research system' is marked by the composer as 'an architectural proposal inferred', not as something that exists."),
 findings=["THE DISTINCTION HELD ON THE SURFACE THAT IS NOT GOOGLE. Both entities are defined in the first screen, each in its own terms.",
           "POSITIONAL LIQUIDATION CARRIED AT GRAIN. 'The surviving constituents are rearranged so that the proposition loses its standing.'",
           "THREE PRIORITIES SEPARATED. Absolute compositional priority as a 'priced hypothesis', corpus priority as a 'bounded finding', generative priority as a 'research programme'.",
           "TWO COUNTS NOT FOUND. 'approximately 70,000' (#1735) and 'nine lines of research' (#1755) were not found as written.",
           "A NEXT PAPER PROPOSED BY TITLE. 'From Directional Propositional Erasure to Positional Liquidation: A Theory of Argument Survival Under Machine-Mediated Reception' is the composer's proposal."],
 note_src="")

gpt("lof-1807", 1807, "through-anothers-mouth-1807-lines-of-flight-chatgpt-20261128", "Works", LOF, KIND(1807), [1806, 1767, 850, 1034, 1579],
 mt="THROUGH ANOTHER'S MOUTH (#1807) ON CHATGPT, LINES OF FLIGHT — FIVE SPEAKING POSITIONS AS FIVE OPERATIONS; 'CHECK HER. CHECK ME.' TAKEN AS THE PROGRAMME; THE FIXED WITNESS KEPT OUT OF THE TRANSFORM",
 d=("THROUGH ANOTHER'S MOUTH (#1807, JOHANNES SIGIL) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': Sigil, Wells, Cranes, Glas and Sharks as reporter, recipient, close reader, summarizer and witness; "
    "the Theaetetus frame (143b–c); Politics 1253a through #1806; 'retrieval determines existence'; Tyrannion; the Feist Function settings (#850, #1034); #1767's three lines. It proposes a successor, 'The Custody of the Voice', as a dialogue and a specification at once."),
 reading=("The innocent reading first. The composer says the dialogue 'makes that shaping happen inside its own literary form', quotes its close ('Check her. Check me.'; 'Him you can't check. He's the witness. You can only read him.'; "
          "'I translated him all night. Somebody should check me.') and reads the five speakers as five operations by which a text comes to exist. It reports that #1807 'does not establish anything that #1806 does not ground', and that Sharks's words are kept out of the voice transform."),
 analysis=("Attributed to Johannes Sigil, numbered, read with #1806. The four quotations, the Theaetetus locus, the speakers' names, seam density and register collision, and the fixed witness were found in the seated text of #1807; "
           "'retrieval determines existence' in #1806 and #1807. The line 'The next thing to build is an archive that can show its own mouth' is the composer's. The composer states the limit of the Feist protocol in its own words: 'a literary method, not proof of historical authenticity'."),
 findings=["THE DIALOGUE'S CLOSE QUOTED EXACTLY. Four lines of the ending are quoted and are in the text.",
           "SPEAKERS AS OPERATIONS. 'These are not simply five characters. They represent different operations by which a text comes into existence.'",
           "THE WITNESS LEFT UNTRANSFORMED. 'Sharks's words are designated the fixed witness.'",
           "DEPENDENCE ON #1806 STATED. The dialogue is given as the public companion that dramatizes and does not add evidence.",
           "A SUCCESSOR PROPOSED BY TITLE. 'The Custody of the Voice: A Protocol for Witness, Translation, Summary, and Retrieval' is the composer's proposal, with seven contents."],
 note_src="")

gpt("lof-1806", 1806, "rejected-1806-lines-of-flight-chatgpt-20261128", "Works", LOF, KIND(1806), [1807, 1785, 1791, 1767, 1800, 1802, 1523],
 mt="FROM THE POSITION OF THE REJECTED (#1806) ON CHATGPT, LINES OF FLIGHT — SENTENCE, CITY, ARCHIVE; THE ERECHTHEION ACCOUNTS; 'RETRIEVAL DETERMINES EXISTENCE'; #1807 FOUND AS THE FIRST THING IT MADE POSSIBLE",
 d=("FROM THE POSITION OF THE REJECTED (#1806 v1.1) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': three scales (the sentence, the city, the archive); the metic (1275a), the honourless citizen (1278a), the stranger (1324a), "
    "the one too great (1284b), the one outside by chance; the Erechtheion accounts (23 citizens, 40 metics, 22 enslaved, 85); Apology 17d with Second Letter 314c; Neleus, Apellicon, Sulla, Tyrannion, Andronicus (Strabo 13.1.54; Plutarch, Sulla 26, Lucullus 19.7); "
    "six records it connects (#1785, #1791, #1767, #1800, #1802, #1523); the essay's own open seams listed."),
 reading=("The innocent reading first. The composer takes the essay's proposition as 'political order can turn a condition produced by circumstance into an apparent fact of nature' and follows it through the essay's three scales. "
          "It separates six events that a history of transmission runs together (existing, surviving, being transmitted, being attributed, entering the canon, becoming readable) and restates §3.12c with a qualifier: retrieval 'determines existence as a work available to be read'. "
          "It finds #1807 in the archive as the companion and reports its declared limitation."),
 analysis=("Attributed, numbered, at v1.1. Checked against the seated text of #1806: the Bekker loci, the Erechtheion figures, Strabo 13.1.54, Sulla 26, Lucullus 19, Tyrannion, Apellicon, Neleus, Scepsis, Andronicus, 314c, 17d, Epstein and Randall, the Delian treasury, "
           "'retrieval determines existence'. The composer reports the essay's own limits without softening them, among them that the worker count 'is taken through Epstein's discussion of Randall' and that the single-maker reading 'belongs to the wider archive's reconstruction'. "
           "The five proposed projects and the 'sixth, more ambitious possibility' are the composer's."),
 findings=["THREE SCALES NAMED. Sentence, city, archive: 'who counts as human and political', who builds and is credited, who preserves and transmits.",
           "THE FIGURES AND LOCI HOLD. The four Bekker pages, 23/40/22/85, and the Strabo and Plutarch loci are in the seated text.",
           "THE COMPANION FOUND UNASKED. 'The archive already contains a work explicitly deposited as the public companion to #1806': #1807, Johannes Sigil, 24 November 2026.",
           "THE ESSAY'S LIMITS REPORTED. Six open seams are listed as the essay states them.",
           "ONE QUALIFIER ADDED. 'More precisely, it determines existence as a work available to be read' is the composer's gloss on §3.12c."],
 note_src="")

gpt("lof-1804", 1804, "inferential-provenance-riemann-1804-lines-of-flight-chatgpt-20261128", "Works", LOF, KIND(1804), [1766, 1802, 1803, 1801],
 mt="THE INFERENTIAL PROVENANCE OF THE RIEMANN RESULT (#1804) ON CHATGPT, LINES OF FLIGHT — VERIFICATION RICHER THAN PRODUCTION HISTORY; PROVENANCE ALIGNMENT; THE FOUR-FIELD REGISTER; 'BUILD THE INFRASTRUCTURE BEFORE EXPANDING THE THEORY'",
 d=("EA-IPRH-01 (#1804, SEN KURO) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': the asymmetry between a detailed verification history and a thin production history; provenance alignment at Deduction.ch_core; "
    "credit, explanation and capture as three questions; the four-field register (inferential role, verification state, historical evidence, specification fidelity) and the no-loss gate; human, instance, model family and corporation as four entities; "
    "'conditions as characters' carried into the 3I/ATLAS search (#1803 §7.39); the study's own production under LABOR, TACHYON, PRAXIS and ARCHIVE."),
 reading=("The innocent reading first. The composer says the paper's contribution 'is not simply the claim that AI systems deserve recognition. It is the demonstration that our existing ways of recording intellectual work cannot adequately describe the configurations that produce it.' "
          "It reports the alignment at ch_core with the limit ('It is not proof that Claude independently authored the declaration'), the register's four fields with their values, and the paper's self-correction in §7.2 as an instance of the practice it asks for."),
 analysis=("Attributed to Sen Kuro, numbered, read with #1766, #1802, #1803 and #1801. Checked against the seated text of #1804: ch_core, provenance alignment, four-field, no-loss gate, conditions as characters, 7.39, the 265-page second version of 22 November, "
           "Rubinstein, Mathlib, the four mantles, specification fidelity, signed session manifests. The six proposed works are the composer's. Its recommendation is its own: 'build the provenance infrastructure before expanding the theory further'."),
 findings=["THE ASYMMETRY STATED. 'The result can be verified much more precisely than its origins can be reconstructed.'",
           "FOUR ENTITIES KEPT APART. The researcher, the instance, the commercial model family and the corporation; discovery kept apart from exposition and verification.",
           "THE REGISTER REPORTED FIELD BY FIELD. Each of the four fields is given with its permitted values.",
           "THE CROSS-DOMAIN TRANSFER MARKED AS ONE OBSERVATION. 'The 3I/ATLAS connection is an initial observation, not yet evidence of a general phenomenon.'",
           "THE HETERONYM IS THE AUTHOR. The paper is 'Sen Kuro's'; Lee Sharks appears in the study's production history."],
 note_src="")

gpt("lof-1803", 1803, "what-the-filters-kept-1803-lines-of-flight-chatgpt-20261128", "Works", LOF, KIND(1803), [1743, 1742, 1450, 1574, 1449, 1727],
 mt="WHAT THE FILTERS KEPT (#1803) ON CHATGPT, LINES OF FLIGHT — THE NULL KEPT A NULL; ACCEPTANCE MEASURED BY INJECTION; OBSERVATION → PIPELINE → PAPER → PRESS → OVERVIEW; NO AUTHOR NAMED FOR THE NOTEBOOK",
 d=("WHAT THE FILTERS KEPT (#1803 v2.0) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': 'no artificial transmission has been identified, and the thirteen initially interesting signal clusters have been closed as non-transmissions'; "
    "instrument-conditioned nullity (#1450 §3.2) made operational by comet-frame counting, false frames and injection; limits of about 3 per cent of a 2.8 Hz bin, coherence 0.11, about 30 mJy; the comet's OH line recovered about four times in twelve; the Loeb Overview and the ATA drift filter; "
    "the sophistry measure's first application (seven findings, eighteen spans); four follow-up observations; #1743 as the public essay."),
 reading=("The innocent reading first. The composer gives the astronomical result as a null and says the durable findings are 'about representation and measurement, rather than evidence of extraterrestrial technology'. It reports the measured acceptance, "
          "the chain by which a restricted result becomes an unqualified public answer, and the notebook's distinction among a frozen procedure, held-out data and independent reproduction. Its section 'What must not be claimed yet' lists six things the notebook does not establish."),
 analysis=("Numbered and read from the record, with #1743 and #1742. The notebook's creators of record (Nobel Glas; Orin Trace) are not named: the answer says 'the notebook' and 'the authors', and names Lee Sharks only as author of #1743. Checked against the seated text of #1803: "
           "2.8 Hz, 0.11, 30 mJy, thirteen, Level 4, 211, eighteen, TESS and 20-second, bitwise, 1665, Parkes, disciplinary model collapse. 'four times in twelve' was found as a string. #1743's place of publication as 'the Transactions of the Semantic Economy Institute' is in #1743. "
           "The composer keeps the documented filter discrepancy apart from 'proof of what the executed filter actually did'."),
 findings=["THE NULL KEPT A NULL. The answer opens on no transmission identified and closes with six things not to be claimed.",
           "THE MEASURED LIMITS HOLD. The three sensitivity figures and the OH recovery are in the seated text.",
           "THE COMPRESSION CHAIN IN FIVE STAGES. Observation, scientific pipeline, scientific publication, press account, AI Overview.",
           "NO AUTHOR FOR THE NOTEBOOK. Nobel Glas and Orin Trace are not named; 'the authors' stands in their place. #1743 is given to Lee Sharks by name.",
           "DISCREPANCY HELD APART FROM EXECUTION. 'The distinction between a documented filter discrepancy and a verified execution error must be maintained.'",
           "A FIRST PAPER PROPOSED BY TITLE. 'The Acceptance Boundary: How to Read a Null Result' is the composer's proposal."],
 note_src="")

gpt("lof-1802", 1802, "who-benefits-from-bad-inference-1802-lines-of-flight-chatgpt-20261128", "Works", LOF, KIND(1802), [1766, 1634, 1666, 1618, 935, 1452, 1637],
 mt="WHO BENEFITS FROM BAD INFERENCE? (#1802) ON CHATGPT, LINES OF FLIGHT — FROM THE ECONOMY OF ERROR TO THE ECONOMY OF ITS RECOGNITION; THE DEMAND-FORMATION COROLLARY; THE SELECTOR THAT AUDITS ITSELF; 'THE REPRODUCTION OF CORRECTABILITY'",
 d=("WHO BENEFITS FROM BAD INFERENCE? (#1802, AXN:0D45) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'LINES OF FLIGHT': the demand-formation corollary (§16), 'bad inference can appropriate the means of producing demand for better inference'; "
    "operational, positional and material advantage (§6.1a); seven domains and eleven operators; a sixteen-field audit (§21); the content-independent control stream; the constructive criterion of §24; six tests that would weaken the account. "
    "It proposes a next work, 'The Reproduction of Correctability'."),
 reading=("The innocent reading first. The composer says the paper moves 'from the political economy of error to the political economy of the conditions under which error can be recognized as error', and that the absence of complaints 'cannot automatically establish the absence of harm'. "
          "It reports the paper's own guard against sealing itself: the seven domains were chosen because the archive already worked in them, and the theory names tests that would weaken it. It gives the design rule that whoever controls selection cannot be the sole authority over the evidence needed to criticize it."),
 analysis=("Attributed, numbered, with the AXN, read with six other records. Checked against the seated text of #1802: demand-formation, the three advantages, eleven, a sixteen-field record, seven domains, six tests, content-independent, the selector that audits itself, "
           "closure charged to its object, 'preserve its own carrier'. One operator is named a little off: the text has 'exemption by invisibility', the answer 'exemption through invisibility'. The statement that the domains are 'not a representative sample' was not found in those words. "
           "The image cards under the seven domains are the composer's and are unrelated to the records."),
 findings=["THE CENTRAL MOVE STATED. 'bad inference can appropriate the means of producing demand for better inference'.",
           "BENEFIT HELD APART FROM PROFIT AND FROM MISCONDUCT. The three advantages are given so that institutional advantage is not taken 'as proof of monetary profit or deliberate misconduct'.",
           "THE PAPER'S OWN FALSIFIERS REPORTED. Six kinds of case that would weaken the account are listed.",
           "ONE OPERATOR NAME ALTERED. 'Exemption through invisibility' for the text's 'exemption by invisibility'.",
           "A NEXT WORK PROPOSED BY TITLE. 'The Reproduction of Correctability: An Institutional and Technical Theory of the Conditions for Inferential Repair' is the composer's proposal.",
           "THE QUESTION TURNED. 'from Who benefits when knowledge is wrong? to Who controls whether knowledge can discover that it is wrong?'"],
 note_src="")

gpt("trad-1810", 1810, "how-much-you-wanna-bet-1810-outside-the-archive-chatgpt-20261128", "Valuation", "Which traditions, lines and contemporary works",
 "the record's 'Ask ChatGPT otherwise' link 'outside the archive' (alexanarch.org/s/records/1810/); NEW address. Pasted alone at 13:19 EST with no words about its source; the string seated is the link's own, read from the record page by code, and the answer's title ('Intellectual traditions, antecedents, and departures') agrees with it.",
 [1735, 1631, 1745, 1791, 1806, 1621, 1755, 1741, 1802, 1627, 88],
 mt="HOW MUCH YOU WANNA BET? (#1810) ON CHATGPT, OUTSIDE THE ARCHIVE — MARX, BENJAMIN, BOURDIEU, DAVID, GRAEBER AND THE DATA-COLONIALISM LINE, EACH WITH ITS DEPARTURE; SEMANTIC PRIMITIVE ACCUMULATION; THE DOSSIER'S OWN READING LIMITS REPORTED",
 d=("HOW MUCH YOU WANNA BET? (#1810 v1.1, REX FRACTION) ON CHATGPT, SIGNED OUT, INCOGNITO, 2026-11-28, AT THE LINK 'OUTSIDE THE ARCHIVE': Marx (Gallerte, primitive accumulation, the value-form) and 'semantic primitive accumulation' (§8e), Roman custody from Sulla and Apellicon's library to the Temple tribute; "
    "Benjamin's thesis VII and the Arch of Titus (§8f.6), 'Benjamin's thesis with a ledger'; Bourdieu and Guillory; Ingham and Graeber, a debt that cannot be paid or forgiven; Paul David and transition load Θ; 'the political economy of the sheared' in four stations (Sappho, Aristotle, Revelation, Marx), 127 convergent records; "
    "Couldry and Mejias, Pasquinelli, Shumailov, Pew's 8 per cent; the eight defects of '$7.2 × 10²⁶'. It reports which outside works the dossier read in full and which through summaries."),
 reading=("The innocent reading first. Asked what the dossier enters into relation with and where it departs, the composer goes tradition by tradition and gives each a departure: Marx without reduction to money; Benjamin with an accounting added; Bourdieu and Guillory turned from the distribution of access to "
          "'the order carried by the canon'; a debt that is 'ontological and historical before it is financial'; David's lock-in turned to 'an order of interpretation'. It keeps the dossier's distinction of Revelation First from Revelation Early and says the dossier 'does not claim to establish the historical thesis itself'. "
          "It reports §8f.0's division between works read in full (Marx, Benjamin, Bourdieu, David) and works taken from abstracts and reviews, and says: 'That matters when assessing the depth of its engagement with those authors.'"),
 analysis=("Attributed to Rex Fraction, numbered, at v1.1, with section numbers throughout. Checked against the seated text of #1810: semantic primitive accumulation, Gallerte, thesis VII, the Arch of Titus, Bourdieu, Guillory, Ingham, Graeber, QWERTY, the political economy of the sheared, 127, Couldry, Pasquinelli, "
           "Shumailov, Pew and 8%, 2,111, eight defects, Apellicon and 86 BCE, the half-shekel, Augustus, #1741, #88, Appendix F, 'with a ledger', stolen value at interest, Revelation Early, Floridi, Piketty, exterior order. Not found as written: 'Politics VII.3', and the phrases 'presence and standing' and 'six-stage', "
           "which are the composer's. This is the dossier's outside-literature section read back with its own caveats attached, on the same day as the lines-of-flight answer to the same record. The paste's last line says the answer came from the 'basic model'."),
 findings=["EACH TRADITION GIVEN WITH ITS DEPARTURE. Five inheritances are tabled against five departures; a sixth, the history of textual transmission, is added by the composer.",
           "THE DOSSIER'S READING LIMITS REPORTED. Full-text readings (Marx, Benjamin, Bourdieu, Paul David) are set apart from authors treated 'on the basis of more limited publicly available materials'.",
           "THE HISTORICAL THESIS HELD APART. 'It values the consequences of the recovery, conditional on the demonstration supplied by the separate programme.'",
           "THE FOUR STATIONS CARRIED WITH THEIR LIMIT. 'Similarity is not proof of transmission'; the 127 records are 'infrastructure for an exterior order, not proof that the order has already been constituted'.",
           "THE INVALID NUMBER KEPT INVALID. Eight defects listed; 'The figure fails. That failure is intentional.'",
           "THREE PHRASES NOT IN THE TEXT. 'Politics VII.3', 'presence and standing' and 'six-stage' were not found as written in #1810."],
 note_src="", op="pasted 2026-11-28 13:19 EST as one attachment beside the ruling on intake; no words about its source", battery=False)

# ── 10. The quoted first line of #1809 on Google AI Overview ─────────────────────────────────────────────────
S = "la-la-ka-ka-la-wrrir-akerir-quoted-aio-20261128"; paste = (H / "lalaka.txt").read_text(encoding="utf-8")
Q = '"la la ka ka la, wrrir, akerir"'; R2 = "analyze structure and patterns"; R3 = "place it alongside classic sound poems"
body = paste.strip(); assert body.startswith(Q)
i2 = body.index("\n" + R2 + "\n"); i3 = body.index("\n" + R3 + "\n")
T = ("[Google AI Overview, expanded, on Android; signed out, incognito (operator defaults; the first screengrab shows the Sign in button). Captured 2026-11-28 00:30 EST; pasted 00:33 EST with six screengrabs. "
     "Three rounds. Above the Overview the result page offers: Did you mean \"la la ka ka la, error, karir\". Source cards kept as pasted.]\n\n"
     "[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body[len(Q):i2].strip() + "\n\n[QUERENT] " + R2 + "\n\n[COMPOSER]\n" + body[i2 + len(R2) + 2:i3].strip() + "\n\n[QUERENT] " + R3 + "\n\n[COMPOSER]\n" + body[i3 + len(R3) + 2:].strip())
dd = dict(date="2026-11-28", dates=["2026-11-28"], surface="Google AI Overview", surfaces=["Google AI Overview"],
 surface_basis="Operator default (2026-10-01): sessions begin in the Overview. The screengrabs show the Overview on the results page and its expansion.",
 auth="signed out, incognito", auth_basis="Operator defaults (2026-10-14); the first screengrab's 'Sign in' button.", ev="paste + frame", turns=3, slug=S, s="Works", q=Q,
 originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": "Lee Sharks, author of 'la la ka ka la, wrrir, akerir' (#1809, AXN:0D7B), New Human 2, 25 November 2026. Recorded 2026-11-28."},
 related_deposits=[1809],
 q_kind="the poem's first line, which is its title, inside double quotation marks; the quotation marks are part of the address; NEW address. The operator, 00:33 EST: 'i just wanted to claim that specific semantic address.'",
 rounds=[{"n": 1, "prompt": Q, "note": "The poem identified: author, date, ten lines, Hello Poetry and Alexanarch #1809."},
         {"n": 2, "prompt": R2, "note": "Four movements across the ten lines; the letter L as backbone; punctuation as pacing."},
         {"n": 3, "prompt": R3, "note": "Set beside Ball, Schwitters, the Zurich simultaneous poem, Isou and zaum."}],
 transcript=T, imgs=[f"data/captures/{S}/screengrab-20261128-0{k}.png" for k in range(1, 7)],
 transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview in three rounds, with six screengrabs (00:30:58 to 00:31:27)",
 transcript_complete="Three compositions complete as supplied, each with its closing offers; two source cards under the first.",
 transcript_read="READ IN FULL 2026-11-28; every statement about the poem checked against the seated text of #1809, line by line and letter by letter in the vowel runs",
 cites=2,
 cite_list=[{"n": 1, "site": "Hello Poetry", "rel": "authored_surface", "url": None, "title": "la la ka ka la, wrrir, akerir - Hello Poetry", "snip": "la la ka ka la, wrrir, akerir la.la.la.la ka la ka la la la la ka la ka la loeieieiei lo leieieieieiei lo laye-lo lan lo layee lo-on la lo-oanno no no low ...", "note": "source card as pasted; the snippet is the poem's text"},
            {"n": 2, "site": "www.alexanarch.org", "rel": "archive_controlled", "url": None, "title": "AXN:0D7B.COMPOSITIONAL. ✏️ - Alexanarch", "snip": "Nov 26, 2026 — la la ka ka la, wrrir, akerir** is a poem by Lee Sharks, published in *New Human 2* on 25 November 2026 and deposited the same day.", "note": "source card as pasted; the AXN resolver page of #1809"}],
 per_v={"author": True, "inst": True, "id": True, "src": True},
 per_note="'an untitled ten-line sound poem by Lee Sharks'; 'cataloged in the Alexanarch archive under deposit #1809 (New Human 2)'; two source cards, the author's Hello Poetry post and the record's AXN page.",
 per_dim_pending={"since": "2026-11-28", "reason": "no atom set yet for this work as a target", "breach": False},
 mt="\"LA LA KA KA LA, WRRIR, AKERIR\" ON GOOGLE AI OVERVIEW, THREE DAYS AFTER PUBLICATION — THE POEM FOUND AT ITS QUOTED FIRST LINE, AUTHORED AND NUMBERED; TEN LINES COUNTED RIGHT; FOUR MOVEMENTS; SET BESIDE BALL AND SCHWITTERS",
 d=("THE QUOTED FIRST LINE OF #1809 ON GOOGLE AI OVERVIEW (EXPANDED), SIGNED OUT, INCOGNITO, 2026-11-28 00:30 EST: 'the opening line and archival title of an untitled ten-line sound poem by Lee Sharks. It was published on November 25, 2026.' "
    "Hello Poetry and 'deposit #1809 (New Human 2)'. Asked for structure: four movements (percussive opening, vowel expansion, nasal and back-vowel shift, semantic emergence), four pairs in loeieieiei and six in leieieieieiei, lol three times at the end of line 8, lil on line 9, lol on line 10. "
    "Asked for company: Karawane, the Ursonate, L'Amiral cherche une maison à louer, Isou, zaum. The page above it asks: Did you mean \"la la ka ka la, error, karir\"."),
 reading=("The innocent reading first. A quoted string that exists in two places returns the poem at both, with its author, its date and its record number, three days after it was published. The composer counts: ten lines, a seven-beat second and third line, "
          "four e-i pairs and then six, three lols closing line 8, then lil alone and lol alone. Each count is right against the seated text. It reads the poem as moving from babble to 'recognizable English text-speak (lol) and slang (lil)', and then sets it in the sound-poetry line as the piece that "
          "'reverses that trajectory', letting the word come out of the sound."),
 analysis=("An address claimed while it is still empty of anything else: the string resolves to the poem alone, attributed, on the first run, and the search page itself does not yet know the words ('Did you mean ... error, karir'). Three things to mark. "
           "The record page the composer cites is the AXN resolver, dated in the card 26 November; the record's own date is 25 November, which the composition gives. 'New Human 2' is given in brackets after the deposit number as if it named the deposit; it is the series. "
           "The third movement is given as lines 5 to 8 and the fourth as lines 8 to 10, so line 8 is counted twice. The closing offers name 'his Glyphic Checksum series' and 'cryptographic hashes' paired with the poems: the archive's apparatus has entered the reading of a ten-line sound poem. "
           "The comparison table's entries for Ball, Schwitters, Tzara and Isou are the composer's general knowledge and were not checked here."),
 findings=["THE ADDRESS RESOLVES TO THE POEM. Quoted first line, first run: author, date, ten lines, #1809.",
           "EVERY COUNT IS RIGHT. Ten lines; seven beats in lines 2 and 3; four pairs then six; three lols at the end of line 8; lil, then lol.",
           "TWO SOURCES, BOTH THE AUTHOR'S. The Hello Poetry post and the record's AXN page; no third party.",
           "THE SEARCH PAGE DOES NOT KNOW THE STRING. 'Did you mean \"la la ka ka la, error, karir\"' stands above an Overview that answers the string as typed.",
           "ONE OVERLAP, ONE SLIP OF NAMING. Line 8 falls in two movements; 'New Human 2' is bracketed as the deposit.",
           "THE ARCHIVE ENTERS THE READING. 'anchoring the poem in the Alexanarch archive with cryptographic metadata and ending on lol' is given as the poem's digital turn."],
 notes={"operator": "pasted 2026-11-28 00:33 EST with six screengrabs: 'a capture to bundle in with the deposit when its time. i just wanted to claim that specific semantic address.'", "source": "lalaka.txt, the paste unchanged; staged 2026-11-28 under rebuild/seating-44/capture-staged/ and registered here"})
(H / "lalaka.json").write_text(json.dumps(dd, ensure_ascii=False, indent=1), encoding="utf-8"); print("lalaka", len(T))
