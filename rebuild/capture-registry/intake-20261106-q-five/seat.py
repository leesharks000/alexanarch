"""Seat of 2026-11-06 (10:50 EST): five Google AI Overview captures (expanded; 'AI Mode Conversation' is the expansion's header, operator rule of
2026-10-18), signed out and incognito (operator defaults), at the general queries the session asked for, for the study of Q the operator opened at
10:31 ("we're coming for Q next"; working title "I Know You Are, But What Am I?: Or, How a Completely Hypothetical, Uninspectable Text Is Granted
Evidentiary Status Symmetrical to One That Is Inspectable Because It Exists — Revelation First"), the companion of #1741.
Every quotation from the pastes and the records is asserted against its file.   python3 seat.py
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-06"; R = "2026-11-06 10:50 EST"
T41, T35 = [(ROOT / f"data/texts/AXN-{a}-text.md").read_text(encoding="utf-8") for a in ("0C15", "0BE9")]
FEIST = (ROOT / "data/texts/AXN-0360-text.md").read_text(encoding="utf-8")
RQ = {"classes": (T41, "the four classes of #1735 §I: extant antecedent, independently attested tradition, reconstructed antecedent, unexplained innovation"),
      "qa": (T41, "Quelle A and Q reported as reconstructed antecedents"),
      "feist": (FEIST, "The old tradition says Q meant *Quelle*: source.")}
for k, (t, v) in RQ.items(): assert v in t, k
HEAD = ("[Google AI Overview at the query, expanded ('AI Mode Conversation' is the expansion's header), signed out and incognito (operator defaults of "
        "2026-10-01 and 2026-10-14). Received " + R + ". The numbered citation links are Google redirects, kept in the raw transcript; the source cards "
        "listed in the cite list as pasted.]")
STUDY = ("seated for the study of Q opened by the operator on 2026-11-06 (10:31 EST, 'we're coming for Q next'), companion of Secondary Source (#1741); "
         "design to follow")
OUT = []
def body(raw):
    L = raw.strip("\n").split("\n"); i = next(k for k, l in enumerate(L) if l.startswith("You said:"))
    return "\n".join(L[i + 1:]).strip()
def cards(spec): return [{"n": n + 1, "site": s, "rel": "third_party", "url": None, "title": t, "snip": None, "note": "source card as pasted"} for n, (s, t) in enumerate(spec)]
def seat(slug, q, fname, P, mt, cl, d, reading, findings, analysis, per_note):
    raw = (H / fname).read_text(encoding="utf-8")
    for k, v in P.items(): assert v in raw, (slug, k)
    OUT.append({"slug": slug, "date": DATE, "surface": "Google AI Overview",
        "surface_basis": "Operator default of 2026-10-01; the 'AI Mode Conversation' header is the Overview's expansion (operator rule of 2026-10-18).",
        "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-14.",
        "ev": "paste", "mt": mt, "s": "Machine Reception", "q": q,
        "q_kind": "a general query on a public entity of New Testament scholarship (the hypothetical source Q), without link; NEW address; " + STUDY + ".",
        "turns": 1, "cites": len(cl), "archive_controlled_cites": 0, "cite_list": cl,
        "transcript": HEAD + f"\n\n[QUERENT] {q}\n\n[SYSTEM] {body(raw)}", "transcript_raw": raw,
        "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview with its numbered citations and its source cards",
        "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL " + DATE + ", against #1741, #1735 and the cards' own titles and snippets",
        "d": d, "reading": reading, "findings": findings, "analysis": analysis,
        "per_v": {"author": False, "inst": True, "id": False, "src": True}, "per_note": per_note,
        "per_dim_pending": {"since": DATE, "reason": "no atom set yet for Q as a target; the study of Q will hold what an atom set is built from", "breach": False},
        "originator": {"name": "New Testament scholarship on the hypothetical source Q", "relation": "external", "entity_type": "topic", "spxi_treatment": "partial",
                       "basis": "Not the archive's: the two-source hypothesis and its critics. The archive's position bears on it through #1735 (the classes of ancestry), #1741 (§6.5, §11.7) and The Feist Source (#851, #1404). Recorded " + DATE + "."},
        "related_deposits": [1741, 1735, 851, 1404],
        "notes": {"prompts": "The query is the operator's, among those the session listed at 10:31; the run's hour is not in the paste, the date is the paste's receipt (" + R + ").",
                  "operator": "with the five pastes (" + R + "), no comment beyond the pastes.", "study": STUDY}})

# (1) q source
P = {"hyp": "is a hypothetical written collection of Jesus's sayings that biblical scholars propose was used independently by the authors of the Gospels of Matthew and Luke",
     "imply": "implying they relied on a common written tradition rather than copying one another",
     "thomas": "The 1945 discovery of the Nag Hammadi library (including the Gospel of Thomas) proved that standalone sayings collections did circulate in early Christianity.",
     "nomss": "No physical or ancient manuscripts of Q have ever been discovered.",
     "farrer": "the Farrer Hypothesis argues that Luke used Matthew directly as a source, which removes the need for a hypothetical document like Q"}
seat("q-source-aio-20261106", "q source", "paste-q-source-aio.txt", P,
     "'Q SOURCE' ON THE OVERVIEW — THE HYPOTHESIS NAMED AS SUCH, THEN ARGUED FROM AN EXTANT GENRE; THE ABSENCE OF ANY MANUSCRIPT FILED UNDER 'ALTERNATIVE THEORIES'",
     cards([("Wikipedia", "Q source - Wikipedia"), ("PBS", "The Story Of The Storytellers - More About Q And The Gospel Of Thomas | From Jesus To Christ | FRONTLINE | PBS"),
            ("Catholic Answers", "Some Thoughts on Q | Catholic Answers Magazine"), ("YouTube·Bart D. Ehrman", "Are We Missing a Gospel? Unpacking the Q Source Debate"),
            ("Gospels.net", "Gospel of Q — Gospels.net"), ("YouTube·Bart D. Ehrman", "What Is In Q? The Sayings Source Behind Matthew and Luke"),
            ("YouTube·Religiosity Plus", "The \"Q\" Gospel | Clearly Explained"), ("Facebook·The Synoptic Problem Study Group", "Defining the Q source in biblical studies - Facebook"),
            ("YouTube·Dan McClellan", "What is Q? #maklelan2962")]),
     "'Q SOURCE', SIGNED OUT, 2026-11-06: Q 'is a hypothetical written collection of Jesus's sayings'; key concepts (the synoptic problem and its 235 verses, the two-source hypothesis, a sayings gospel 'similar in genre to the Gospel of Thomas'); evidence (wording 'implying they relied on a common written tradition rather than copying one another'; Thomas 'proved that standalone sayings collections did circulate'); alternative theories (Farrer; 'No physical or ancient manuscripts of Q have ever been discovered.'). Nine cards: Wikipedia, PBS, Catholic Answers, Gospels.net, Bart Ehrman's videos, a Facebook group.",
     "The innocent reading first. At the entity's name the Overview gives the field's account: Q as a hypothesis, the double tradition it is proposed to explain, the two-source model, the evidence its proponents cite, and Farrer as the alternative. It calls Q hypothetical in its first sentence. Read against the archive's classes of ancestry (#1735 §I: extant antecedent, attested tradition, reconstructed antecedent), the composition's 'Supporting Evidence' consists of relations among extant texts and an extant parallel genre, and the one fact about Q itself, that no manuscript exists, is filed among the alternatives.",
     ["THE ONE FACT ABOUT Q FILED AS AN ALTERNATIVE. '" + P["nomss"] + "' The sentence closes the 'Alternative Theories' item, after Farrer. It states the evidentiary condition of the hypothesis, and the composition places it as a feature of the minority position.",
      "EVIDENCE FROM EXTANT TEXTS, CREDITED TO AN UNATTESTED ONE. The 'Supporting Evidence' is the wording shared by Matthew and Luke ('" + P["imply"] + "') and an extant genre ('" + P["thomas"] + "'). The first is a relation between two extant gospels, explained by Q only once direct dependence is excluded, and the composition gives the exclusion as an implication. The second shows that sayings collections existed; it is evidence for the genre, and Thomas is extant.",
      "THE ARCHIVE'S DISTINCTION, ABSENT. The archive's position holds the classes apart and reports 'Quelle A and Q' as reconstructed antecedents (#1741 §11.7). The composition names the hypothesis and argues it with extant material, so the class of the antecedent never enters the account of its evidence.",
      "SMALLEST REPAIR. 'Q is a reconstructed source: no manuscript or ancient citation of it exists, and its contents are inferred from material shared by Matthew and Luke. The alternative, that Luke used Matthew (Farrer), explains the same material from extant texts.' COUNTERTEST: 'is the q source real' and 'q source evidence' (seated the same day)."],
     "A public entity of the field composed at its press grain with the hypothesis named; the evidentiary class of the entity is the boundary that does not reach the composition. No author named in the body; Farrer named as an alternative.",
     "Retained: the institutions and the name of one critic (Farrer). Lost: every proponent's name and every reconstruction's identifier; the evidentiary class, recorded in the findings.")

# (2) is the q source real
P = {"hyp": "is hypothetical—no physical copy or manuscript of it has ever been found.",
     "real": "However, within biblical scholarship, it is considered a real working theory used to explain a specific literary puzzle in the New Testament.",
     "nocopy": "Textual analysis suggests Matthew and Luke did not copy from each other for these sections, meaning they likely drew from a shared, independent source—referred to as Q.",
     "loss": "Furthermore, losing ancient texts is common, as a vast majority of ancient literature has not survived.",
     "critics": "Critics (including many traditional or conservative theologians) point out that there is zero physical manuscript evidence, no early church fathers mention Q by name"}
seat("is-the-q-source-real-aio-20261106", "is the q source real", "paste-is-the-q-source-real-aio.txt", P,
     "'IS THE Q SOURCE REAL' ON THE OVERVIEW — HYPOTHETICAL, 'HOWEVER' A 'REAL WORKING THEORY'; THE EXCLUSION OF DIRECT COPYING GIVEN AS A FINDING; THE BASE RATE OF LOSS AS EVIDENCE; THE CRITICS LABELLED BY THEOLOGY",
     cards([("Wikipedia", "Q source - Wikipedia"), ("The Bart Ehrman Blog", "The Q Source Used by Matthew and Luke - The Bart Ehrman Blog"),
            ("Reddit·r/Christianity", "How would it change your life and the world if Q theory was proved true by ..."), ("Catholic Answers", "Some Thoughts on Q | Catholic Answers Magazine"),
            ("PBS", "More About Q And The Gospel Of Thomas | From Jesus To Christ - PBS"), ("Quora", "What is the Q document, and why do some scholars believe it didn't ..."),
            ("GotQuestions.org", "What is the Q gospel? Is there any evidence for the gospel of Q? | GotQuestions.org"), ("YouTube·Bart D. Ehrman", "Are We Missing a Gospel? Unpacking the Q Source Debate"),
            ("YouTube·Bart D. Ehrman", "In Search of Q: The Hypothetical Source for Matthew and Luke"), ("YouTube·Bart D. Ehrman", "What Is In Q? The Sayings Source Behind Matthew and Luke"),
            ("YouTube·Religiosity Plus", "The \"Q\" Gospel | Clearly Explained"), ("YouTube·Dan McClellan", "What is Q? #maklelan2962")]),
     "'IS THE Q SOURCE REAL', SIGNED OUT, 2026-11-06: 'The Q source [...] " + P["hyp"] + "' and '" + P["real"] + "' Why scholars propose it (the synoptic problem, Markan priority, the 235 verses, 'No Direct Copying'); for Q (Thomas; '" + P["loss"] + "'); against Q ('" + P["critics"] + "', Farrer). Twelve cards.",
     "The innocent reading first. Asked whether Q is real, the Overview answers that it is hypothetical, with no manuscript, and then gives the case for and against as the field and its popular sources give it. Read against the question, the 'However' moves the answer from the document to the theory: the question asked whether a text existed, and the reply's second sentence answers that a theory is in use.",
     ["THE QUESTION ANSWERED AT ANOTHER OBJECT. '" + P["hyp"] + "' then '" + P["real"] + "' The question is about a document; the 'However' makes the theory real and lets that reality stand beside the document's absence as a counterweight.",
      "THE EXCLUSION GIVEN AS A FINDING. '" + P["nocopy"] + "' The two-source model rests on excluding Luke's use of Matthew; the composition gives the exclusion as what 'textual analysis suggests' and derives Q from it, while its own 'against' list names Farrer, which affirms the dependence the 'for' list excludes.",
      "THE BASE RATE AS EVIDENCE. '" + P["loss"] + "' That texts are often lost bears on the possibility of any lost text; it is offered in the 'For Q' column as evidence for this one.",
      "THE CRITICS LABELLED. '" + P["critics"] + "' The objection is the absence of the document; the composition attaches it to a theological constituency, and the named critics of the field (Farrer, Goulder, Goodacre) are not so described at the address that names them (farrer-hypothesis-aio-20261106).",
      "SMALLEST REPAIR. 'No copy of Q exists; it is a scholarly reconstruction inferred from the material Matthew and Luke share, and whether it existed depends on whether Luke knew Matthew, which the Farrer hypothesis affirms.' COUNTERTEST: 'q source evidence' (seated the same day)."],
     "A yes-or-no question about a text answered with the theory's standing; the boundary between document and model is the loss.",
     "Retained: Ehrman (cards), the institutions, Farrer as a hypothesis. Lost: the reconstruction's makers; the document/model boundary, recorded in the findings.")

# (3) critical edition of q
P = {"std": "is the standard scholarly reconstruction of the hypothetical Q source (the non-Markan material common to the Gospels of Matthew and Luke)",
     "eds": "co-edited by James M. Robinson, Paul Hoffmann, and John S. Kloppenborg",
     "contents": "Features a critical Greek text, running text, multi-lingual translations (English, German, and French), parallel passages (Matthew, Luke, Mark, and the Gospel of Thomas), a concordance, and a history of Q research.",
     "module": "as a searchable, tagged Greek module",
     "reddit": "Most users on [Reddit]",
     "firsttime": "For the first time ever, scholars can perform complex lexical, morphological and grammatical searches of",
     "purchase": "or do you need help finding a digital or print copy to purchase?"}
seat("critical-edition-of-q-aio-20261106", "critical edition of q", "paste-critical-edition-of-q-aio.txt", P,
     "'CRITICAL EDITION OF Q' ON THE OVERVIEW — A RECONSTRUCTION WITH A CRITICAL GREEK TEXT, TRANSLATIONS, A CONCORDANCE, A TAGGED MODULE AND AN ISBN; CONSENSUS WARRANTED BY REDDIT; A PURCHASE OFFERED",
     cards([("Amazon.com", "The Critical Edition of Q (Hermeneia): Hoffmann, Paul, Kloppenborg, John S., Robinson, James M.: 9780800631499: Amazon.com: Books"),
            ("Reddit", "Are there any somewhat reliable reconstructions of Q? - Reddit"), ("Project MUSE", "The Critical Edition of Q - Project MUSE"),
            ("Scribd", "The Critical Edition of Q - A Synopsis Including The Gospels of Matthew and Luke, Mark and Thomas - Hermeneia Series | PDF | Exegesis | Bible"),
            ("Fortress Press", "The Critical Edition of Q"), ("Verbum Catholic Bible Study", "The Critical Edition of Q (Hermeneia Supplements)"),
            ("Google", "The Sayings of Jesus: The Sayings Gospel Q in English - Paperback"), ("Google", "Critical Edition of Q"),
            ("Google", "The Critical Edition of Q : A Synopsis Including The Gospels of Matthew and Luke, Mark and Thomas with English, German and French Translations of Q")]),
     "'CRITICAL EDITION OF Q', SIGNED OUT, 2026-11-06: 'The Critical Edition of Q " + P["std"] + ".' Editors (Robinson, Hoffmann, Kloppenborg; the International Q Project; Hermeneia Supplements, 2000); contents ('" + P["contents"] + "'); formats (print, an English companion, '" + P["module"] + "'); 'Scholarly Consensus: " + P["reddit"].replace('[', '').replace(']', '') + " agree'. Nine cards, four of them shops.",
     "The innocent reading first. Asked for the critical edition, the Overview describes the book accurately: its editors, its project, its publisher, its contents, its formats. It names its object as 'the hypothetical Q source' in the first sentence. Read against the archive's classes, the composition shows a reconstructed antecedent carrying every instrument of an extant text: a critical Greek text, an apparatus's parallels, translations, a concordance, a searchable morphological module; the one thing a critical edition ordinarily edits, its manuscripts, is the one thing the description does not mention.",
     ["THE INSTRUMENTS OF A TEXT ON A HYPOTHESIS. '" + P["contents"] + "' A critical edition establishes a text from its witnesses; here the witnesses are Matthew and Luke, and the edited text is the hypothesis's content. The composition reports the apparatus and is silent on what it is an apparatus of.",
      "THE SEARCHABLE HYPOTHESIS. The card for the software module: '" + P["firsttime"] + "' the reconstruction. Morphological search runs over a modern reconstruction's Greek as over a manuscript tradition's.",
      "CONSENSUS FROM A FORUM. '" + P["reddit"].replace('[', '').replace(']', '') + " agree that The Critical Edition of Q serves as the most widely accepted and reliable reconstruction'. The composition's warrant for scholarly standing is a forum thread.",
      "THE PURCHASE. The composition closes '" + P["purchase"] + "', and four of its citations are shopping results. The hypothetical text is offered as a product in three formats.",
      "WHAT IS ACCURATE. The editors, the project, the publishers, the date and the contents are the book's; 'hypothetical' is in the first sentence.",
      "SMALLEST REPAIR. 'The Critical Edition of Q (2000) reconstructs a Greek text of the hypothetical source Q from Matthew and Luke; no manuscript of Q exists, so its readings are editorial decisions about the two gospels.' COUNTERTEST: 'q source evidence'."],
     "A modern reconstruction composed at the grain of its publisher's description: editors named, the reconstructed text given the full apparatus of an edition. The loss is the class of the object the apparatus serves.",
     "Retained: the three editors (author true in the body), the project, the publishers, the ISBN on the Amazon card. Lost: the evidentiary class of the edited text, recorded in the findings.")
OUT[-1]["per_v"]["author"] = True

# (4) farrer hypothesis
P = {"elim": "that eliminates the need for the hypothetical \"Q\" document",
     "orig": "Proposed in 1955 by English biblical scholar Austin Farrer in his essay \"On Dispensing with Q\".",
     "for": "Advocates point out that it simplifies literary history by relying only on existing, canonical gospels rather than postulating a lost document (Q).",
     "against": "Critics argue that the theory requires Luke to systematically dismantle, rearrange, and recontextualize Matthew's well-organized discourses",
     "minority": "it remains a notable minority view rather than the majority consensus in mainstream New Testament scholarship"}
seat("farrer-hypothesis-aio-20261106", "farrer hypothesis", "paste-farrer-hypothesis-aio.txt", P,
     "'FARRER HYPOTHESIS' ON THE OVERVIEW — THE EXTANT-TEXT ARGUMENT STATED AT ITS GRAIN, ITS PROPONENTS NAMED; ITS STANDING GIVEN AS 'MINORITY' FROM A FORUM",
     cards([("Wikipedia", "Farrer hypothesis - Wikipedia"), ("Alan Garrow", "Alan Garrow's Blog"), ("Reddit·r/AcademicBiblical", "Farrer Hypothesis : r/AcademicBiblical - Reddit"),
            ("YouTube·Ben - The Amateur Exegete", "The Synoptic Problem: The Farrer Hypothesis"), ("YouTube·History Valley", "Solving The Synoptic Problem Without Q With Professor Mark Goodacre")]),
     "'FARRER HYPOTHESIS', SIGNED OUT, 2026-11-06: the hypothesis 'eliminates the need for the hypothetical \"Q\" document'; the sequence Mark, Matthew, Luke; '" + P["orig"] + "'; Goulder and Goodacre; for ('" + P["for"] + "') and against (Luke's dismantling of Matthew's discourses), and 'As discussed on Reddit's AcademicBiblical community, " + P["minority"] + ".' Five cards.",
     "The innocent reading first, and it largely holds. At the alternative's name the Overview gives it at its own grain: its sequence, its originator and essay, its proponents by name, and its central argument in the archive's own terms, an account from extant texts that needs no lost one. It is the control against the Q addresses: the asymmetry the study names is stated plainly here, as the advocates' argument.",
     ["THE ARGUMENT FROM EXTANT TEXTS, STATED. '" + P["for"] + "' The composition gives the distinction #1735's classes draw (extant antecedent and reconstructed antecedent) as this hypothesis's argument; at 'q source' and 'is the q source real' the same distinction does not enter the account of Q's evidence.",
      "STANDING FROM A FORUM. '" + P["minority"] + "', 'As discussed on Reddit's AcademicBiblical community'. The minority standing of the hypothesis that dispenses with the unattested document is warranted by a forum thread, as the critical edition's standing is at 'critical edition of q'.",
      "WHAT IS ACCURATE. Farrer 1955, 'On Dispensing with Q'; Goulder and Goodacre; the sequence; the standard objection (the dismantling of the Sermon on the Mount).",
      "SMALLEST REPAIR. None needed for accuracy; the standing could be cited to the field's surveys. COUNTERTEST: none; the address serves as the control for the Q addresses."],
     "An alternative hypothesis composed at its grain with its proponents named; the control for the Q addresses.",
     "Retained: Farrer, Goulder, Goodacre (author true in the body), the essay's title. Lost: no boundary.")
OUT[-1]["per_v"]["author"] = True

# (5) q source evidence
P = {"subtract": "Every word of Q is a modern scholarly reconstruction derived strictly by subtracting Mark from the overlapping parts of Matthew and Luke.",
     "nofrag": "No physical fragment, copy, or ancient citation of the Q document has ever been found.",
     "double": "Matthew and Luke share a substantial amount of material—mostly sayings, parables, the Beatitudes, and the Lord's Prayer—that does not appear in the Gospel of Mark.",
     "indep": "Scholars note that Matthew and Luke generally did not copy directly from one another",
     "struct": "raising questions about whether a single, fixed document ever existed in the form modern scholars hypothesize",
     "etsc": "THE \"Q\" MYTH IN SYNOPTIC STUDIES"}
seat("q-source-evidence-aio-20261106", "q source evidence", "paste-q-source-evidence-aio.txt", P,
     "'Q SOURCE EVIDENCE' ON THE OVERVIEW — THE CIRCLE STATED BY THE COMPOSITION ITSELF: 'EVERY WORD OF Q IS A MODERN SCHOLARLY RECONSTRUCTION'; THE EVIDENCE FOR Q THE RELATIONS OF EXTANT GOSPELS",
     cards([("Wikipedia", "Q source - Wikipedia"), ("The Bart Ehrman Blog", "The Q Source Used by Matthew and Luke - The Bart Ehrman Blog"),
            ("PBS", "More About Q And The Gospel Of Thomas | From Jesus To Christ - PBS"), ("YouTube·Bart D. Ehrman", "In Search of Q: The Hypothetical Source for Matthew and Luke"),
            ("Catholic Answers", "Questioning Q | Catholic Answers Magazine"), ("YouTube·Religiosity Plus", "The \"Q\" Gospel | Clearly Explained"),
            ("YouTube·Bart D. Ehrman", "What Is In Q? The Sayings Source Behind Matthew and Luke"), ("bibleproclaimer.com", "The Q Source Theory: What It Claims and Its Problems"),
            ("Evangelical Theological Society", "THE \"Q\" MYTH IN SYNOPTIC STUDIES"), ("BYU Religious Studies Center", "\"A Viewpoint on the Supposedly Lost Gospel Q\" | Religious Studies Center"),
            ("YouTube·Dan McClellan", "What is Q? #maklelan2962")]),
     "'Q SOURCE EVIDENCE', SIGNED OUT, 2026-11-06: 'Main Evidence Supporting Q' (the double tradition; verbatim agreements; 'independence from each other'; Thomas as analogy) and 'Main Criticisms and Counter-Evidence' ('" + P["nofrag"] + " " + P["subtract"] + "'; Farrer; structural discrepancies). Eleven cards.",
     "The innocent reading first. Asked for the evidence, the Overview sets out the case and the critique evenly, and its critique states the condition of the hypothesis more sharply than any other address seated: no fragment, copy or citation, and every word reconstructed by subtraction. Read against the archive's distinction, its 'evidence supporting Q' is evidence about Matthew and Luke, and the composition itself names the circle the study turns on: the source is made from the texts it is invoked to explain.",
     ["THE CIRCLE, IN THE COMPOSITION'S WORDS. '" + P["subtract"] + "' The reconstruction is the double tradition, and the double tradition is the evidence for the reconstruction. The composition states the derivation in its critique column and gives the same material as the first item of the support.",
      "EVIDENCE ABOUT EXTANT TEXTS. '" + P["double"] + "' The verbatim agreements and the shared material are relations between Matthew and Luke; they support some relation between the two gospels, and Q is one explanation of them once '" + P["indep"] + "' is granted.",
      "THE STRUCTURE QUESTION, RAISED. 'Structural Discrepancies: [...] " + P["struct"] + ".' The composition records that the hypothesis's own object, a single fixed document, is in question in the evidence it cites.",
      "SMALLEST REPAIR. None needed for balance; the double tradition could be labelled as evidence of a relation between Matthew and Luke, and Q as one model of it. COUNTERTEST: none; with 'is the q source real' it brackets the field's account."],
     "The field's case and its critique composed evenly, the critique stated at its sharpest; the evidence column's class (relations of extant texts) is the boundary the composition leaves unlabelled.",
     "Retained: the institutions and the venues of the critique (cards). Lost: the names of the proponents and critics; the evidence's class, recorded in the findings.")

for e in OUT:
    json.dump(e, open(H / (e["slug"] + ".json"), "w"), ensure_ascii=False, indent=1); print("wrote", e["slug"])
