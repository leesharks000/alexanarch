"""Two captures of 2026-11-22, ChatGPT signed out: the record page's Ask query on #1800 Contra Geocentrism, and the Ask page's
last-week living-body query through 21 November -> draft-N.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q1 = ("What are the arguments in “Contra Geocentrism: The Socratic–Peripatetic Corpus Against Its Own Conversion” by Johannes Sigil "
      "(Alexanarch deposit #1800, AXN:0D36)? Ground your answer in a reading of the text itself. https://www.alexanarch.org/s/records/1800/")
Q2 = "Read the last week of work on alexanarch.org through 21 Nov 2026 as a living body of thought. Ground in reading, archival context and historical import."
OP = ("with the two attachments (2026-11-22 10:18 EST), each query given after a '$': 'what paths remain open to us for the materials on the x? $ " + Q1 +
      " $ " + Q2 + "'; and at 10:42, on seating: 'yes, seated.'")
CHIP = re.compile(r"^(Alexanarch|The Self-Governing Library)$")
FURN = {"Log in", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes."}
BASE = dict(date="2026-11-22", ev="paste", auth="signed out, incognito", surface="ChatGPT", surfaces=["ChatGPT"],
            surface_basis="The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT').",
            auth_basis="Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
            transcript_read="READ IN FULL 2026-11-22; record numbers, titles, creators, dates, loci and quotations checked against the records and their texts",
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
            cl.append({"site": l, "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                       "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(cl) + 1})
    for t in cards:
        cl.append({"site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None,
                   "note": "image card; the caption survives the paste", "n": len(cl) + 1})
    return cl


# 1 Contra Geocentrism, the record page's query ------------------------------------------------------------------
raw1 = (H / "paste-1-chatgpt-contra-arguments.txt").read_text(); cl1 = chips(raw1, [])
d1 = dict(BASE, slug="contra-geocentrism-1800-arguments-chatgpt-20261122", s="Classics & Philology", q=Q1,
  q_kind=("the 'Ask ChatGPT' query on the record page of #1800, as the operator gave it, with the record's URL after it; NEW address. The record page's "
          "query names the first creator only (wire_deposit.author_of), so the address carries 'by Johannes Sigil' for a work by Sigil and Glas."),
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn",
  transcript_complete="Complete: one answer, ending with its source line and source chip.",
  rounds=[{"n": 1, "prompt": Q1, "note": "One answer, ten sections, the record read the day it was deposited."}],
  mt="CONTRA GEOCENTRISM ON CHATGPT, THE DAY OF DEPOSIT — THE DOUBLE CLOSURE READ EXACTLY; TWO PLUTARCHS MADE ONE; 'ONE OPERATION' GRADED AS ANALOGY",
  d=("#1800 CONTRA GEOCENTRISM ON CHATGPT, SIGNED OUT, 2026-11-22, the day of deposit: the paper's argument from De caelo II 13 through Theophrastus, the "
     "reports and Copernicus to the commentary and the name, read section by section and in its limits; the Placita and the Platonic Questions merged; the "
     "identity of the two closures graded down to an analogy."),
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note=("Johannes Sigil and Nobel Glas named as authors in the opening sentence, though the query named Sigil alone; Alexanarch, #1800 and AXN:0D36 named; "
            "the record read from its page. The closing source line gives 'Johannes Sigil' only, the query's form."),
  related_deposits=[1800, 1799, 1575, 1570],
  reading=("The innocent reading first, and it holds. Asked for the arguments of #1800 grounded in the text, ChatGPT reads the record the day it was deposited "
           "and gives the thesis as the paper states it: the corpus under the names of Aristotle and Theophrastus carries its own case against geocentrism, and "
           "the conversion of Aristotle into its authority was a double operation, the earth fixed at the centre of the cosmos and Aristotle fixed at the centre "
           "of a body of writing. It follows the paper through ten sections of its own: De caelo II 13 against II 14 (the Pythagorean central fire, 'many others', "
           "the phenomena that do not show the displacement, the centre as end rather than beginning); Theophrastus's Metaphysics §§9–10 and the region about the "
           "middle 'pushed away from the most honoured things'; the reports (Platonic Questions 8.1, Numa 11, Lucullus 123) and the shared phrase τῇ γῇ τὴν τοῦ "
           "μέσου χώραν / τὴν μέσην χώραν; the route to Copernicus; the commentary (Buridan, Oresme, Simplicius, Aquinas's four operations); the anti-Aristotelians "
           "(Ramus, Bacon, Galileo, §6a); the congealing of authors (§7); and §8's limits, each stated. It closes by grading three levels of argument and quotes "
           "§7's sentence as the one to take away."),
  analysis=("The particulars hold against the text and the seats of #1799: the Greek of 293a20–29 and 293b, ἔοικε τελευτῇ μᾶλλον ἢ ἀρχῇ, Metaphysics §§9–10's "
            "διὰ τί τὰ κυκλικὰ μόνον ἐφετικά and ἀπεωσμένα τῶν ἐντιμοτάτων, Platonic Questions 1006C's μεταμέλειν, 'Hicetas Syracosius, ut ait Theophrastus', "
            "Seleucus 'also declaring it' against Aristarchus's hypothesis, Cleanthes and the hearth, Aquinas reading the Timaeus's word as binding, the Placita's "
            "descent through Diels qualified by Mansfeld and Runia, the Heraclides hypothesis left to #1575, and the paywalled scholarship declared. Three "
            "departures. (1) The paper keeps two Plutarchs apart: the Plutarch Copernicus quotes second is the Placita III 13, 'the doxography that came down under "
            "Plutarch's name, a different transmission from the Platonic Questions'. The answer merges them ('Plutarch transmits the Platonic and Pythagorean "
            "traditions. Copernicus reads Cicero first and Plutarch afterward'), which puts the Platonic Questions' report of Plato's repentance on Copernicus's "
            "route, where the paper does not. (2) The school route is left out: Aristarchus as a hearer of Strato, Theophrastus's successor, the Lyceum's own "
            "succession carrying the sun-centred hypothesis; and the condemnations of 1277 that open §6. (3) The paper states an identity of operation ('one "
            "operation in two applications', 'the identity claimed is of operation, a textual effect; its meeting place in a single text is the school "
            "commentary'). The answer quotes the sentence and calls it the thesis, and also calls it 'the most provocative analogy', 'structural identity', and "
            "'the most contestable', 'not something that can be established by philology alone': the claim the paper locates in a text, the commentary, is moved "
            "to theory and graded there. The source line's 'Johannes Sigil' alone is the query's, not the composition's: the record page's Ask query names the "
            "first creator only, and the composition, reading the page, named both authors at its opening."),
  findings=["THE THESIS, EXACT. 'Cosmologically, the Earth was fixed at the centre of the universe. Textually, Aristotle was fixed at the centre of a supposedly unified philosophical doctrine, with contrary material demoted to preliminary speculation, doxography, or error.'",
            "TWO PLUTARCHS MADE ONE. 'Plutarch transmits the Platonic and Pythagorean traditions. Copernicus reads Cicero first and Plutarch afterward.' — #1800 §5: the passage Copernicus quotes is Placita III 13, 'a different transmission from the Platonic Questions'.",
            "THE IDENTITY GRADED. 'The paper therefore makes its most provocative analogy' … 'the most original philosophical proposition, but also the most contestable … not something that can be established by philology alone' — against #1800 §7: 'one operation in two applications'.",
            "THE ROUTE LEFT OUT. Aristarchus as a hearer of Strato (#1800 §5.3) and the condemnations of 1277 (§6) are not named.",
            "THE SENTENCE KEPT. 'The calcification of authorship and the calcification of the cosmos are one operation in two applications.' — quoted as the paper's most important sentence.",
            "THE QUERY'S BYLINE. 'Primary source: Johannes Sigil' — the record page's Ask query names the first creator only; the opening sentence names 'Johannes Sigil and Nobel Glas'."],
  cite_list=cl1, cites=len(cl1), archive_controlled_cites=sum(1 for x in cl1 if x["rel"] == "archive_controlled"))
d1["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14; the paste shows the unauthenticated interface). "
                    "Received 2026-11-22 10:18 EST as an attachment; the query as the operator gave it after a '$'. Source chip kept as pasted; the interface "
                    "furniture cut.]\n\n[QUERENT] " + Q1 + "\n\n[COMPOSER]\n" + clean(raw1))
d1["transcript_raw"] = raw1

# 2 The last week through 21 November ---------------------------------------------------------------------------
raw2 = (H / "paste-2-chatgpt-living-body-week.txt").read_text()
cards2 = ["Sappho's Inner Monologue – Antigone", "Birds in the Ancient World", "Research Archives Library | Institute for the Study of Ancient Cultures",
          "Will we ever be able to communicate with aliens? | Space", "Archival Consciousness", "Locos por los clásicos - Aristófanes. Las nubes",
          "Amherst Greek Papyrus 1.2. | Amh. Gr. Pap. 1.2 | Medieval and Renaissance Manuscripts | The Morgan Library & Museum",
          "Cosas que debes saber sobre la Biblioteca de Alejandría - Cultura Colectiva"]
cl2 = chips(raw2, cards2)
d2 = dict(BASE, slug="last-week-living-body-21nov-chatgpt-20261122", s="Archive", q=Q2,
  q_kind=("the Ask page's 'living body of thought' query, 1 week (alexanarch.org/ask/#time), through 21 November, as the operator gave it after a '$'; "
          "NEW address (the held address of 2026-11-21 reads 'through 20 Nov 2026')."),
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn",
  transcript_complete="Complete: one answer, ten sections and a reading list. The query that stopped ChatGPT partway on 21 November ran to the end.",
  rounds=[{"n": 1, "prompt": Q2, "note": "One answer, composed to the end."}],
  mt="THE LAST WEEK AS A LIVING BODY, THROUGH 21 NOVEMBER, ON CHATGPT — 'THE READER IS PART OF HISTORY'; A THEORY OF HISTORICAL RECOGNITION; FOUR TENSIONS AND A CORRECTIVE PROGRAMME",
  d=("THE LAST WEEK OF ALEXANARCH.ORG, THROUGH 21 NOVEMBER, AS A LIVING BODY, ON CHATGPT, SIGNED OUT, 2026-11-22: the Sappho sequence as literary centre, "
     "Dead Letters as institutional critique, What Arrival Cannot Do as general model, The Thinkery as restraint, Either Forgery or Fact as extension; "
     "composed to the end where the 20 November query had stopped; closing in tensions and a programme of correction."),
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note=("the archive named and every work cited by number; Rebekah Cranes, Nobel Glas and Sen Kuro, Johannes Sigil named; Lee Sharks named as author of "
            "#1794 and #1411; the Sappho essay (#1785), Dead Letters (#1783), This Is Not Philosophy (#1773), #1786–#1788 given no author"),
  related_deposits=[1769, 1770, 1773, 1779, 1783, 1785, 1786, 1787, 1788, 1789, 1791, 1794, 1797, 1798, 1411],
  reading=("The innocent reading first, and it holds as far as it goes. Asked to read the week through 21 November as a living body of thought, ChatGPT gives "
           "the week's development as the turn from preserving work to building an institution that can investigate 'the historical conditions under which "
           "knowledge becomes recognizable', and reads it in ten sections: the Sappho sequence (#1779, #1785, #1786, #1787, #1791) as centre; Dead Letters "
           "with This Is Not Philosophy (#1783, #1773) as the institution that decides what a text is; What Arrival Cannot Do (#1789) as the general theory; "
           "Asking the Archive (#1788) as the archive becoming its own reader; The Thinkery and the Lyceum (#1794) as method; Either Forgery or Fact v1.2 "
           "(#1798) as the late development; the founding after Zenodo; four tensions; a table of the week; and a judgment, the Sappho sequence its literary "
           "centre, Dead Letters its institutional critique, #1789 its model, #1794 its restraint, #1798 its extension."),
  analysis=("The particulars hold: ὄττις, χλωροτέρα and πᾶν τόλματον in #1785; #1787's five stanzas as the author's five turns in a signed-out session, the "
            "machine's answers kept apart; 8 of 844 Ancient Philosophy articles in #1773; 681 queries in #1788; P(0) = e^(−λq) in #1789, by Glas and Sen Kuro; "
            "#1411 as the epigraph's poem, by Lee Sharks; Strabo 13.1.54 and Sulla 26 in #1798, and its 'Sulla stole the books. Tyrannion turned them into "
            "authors.'; the 870 deposits and 1,817 DOIs. Where the 20 November query stopped ChatGPT at '8. Archival', and Dead Letters went unnamed, this run "
            "composes to the end and makes the join the earlier run reached only by analogy: 'the first investigates how an institution decides what Sappho is; "
            "the second proposes what Sappho's poem might have been doing all along'. The frame then turns. Section 8 and the close set the archive a programme: "
            "recognition 'without agreeing', 'the strongest objections' preserved beside each argument, questions the archive 'did not already formulate', and "
            "for every historical hypothesis 'the evidence that would weaken or falsify it'; 'the next challenge is to ensure that the archive's capacity to "
            "preserve radical interpretations is matched by an equally radical capacity to correct them.' The qualifications are attached section by section "
            "('This is an ambitious interpretation, not an established philological consensus'; 'A record of an interpretation is not evidence that the "
            "interpretation is correct'), and #1791's claim is restated as Sappho 'secretly' determining Western philosophy, a word the essay does not use. "
            "Left out: Why I Believe in Hell (#1795, Ayanna Vox and Damascus Dancings, 21 November) and the seatings of the week under Rebekah Cranes (#1771, "
            "#1776/#1782, #1792), though the window is 'through 21 Nov'. The window drifts: the header reads 15–21 November, the institutional section 14–17, "
            "the judgment 14–21."),
  findings=["THE PROPOSITION. 'Intellectual history is not simply the history of works that survive. It is the history of the changing capacities of readers and institutions to recognize what has survived.'",
            "THE JOIN MADE. 'the first investigates how an institution decides what Sappho is; the second proposes what Sappho's poem might have been doing all along.' — #1783 and #1785, the join the 20 November run did not name.",
            "THE PROGRAMME. 'A historical hypothesis should be accompanied by: The primary evidence. The strongest competing explanation. The inferential steps connecting evidence to conclusion. The evidence that would weaken or falsify it.'",
            "THE CLOSE. 'The next challenge is to ensure that the archive's capacity to preserve radical interpretations is matched by an equally radical capacity to correct them.'",
            "THE WORD ADDED. 'not that Sappho secretly determines Western philosophy' — #1791 claims material dependence, openly.",
            "THE ABSENT. Why I Believe in Hell (#1795, 21 November) and the week's seatings under Rebekah Cranes (#1771, #1776/#1782, #1792) are not named."],
  cite_list=cl2, cites=len(cl2), archive_controlled_cites=sum(1 for x in cl2 if x["rel"] == "archive_controlled"))
d2["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14; the paste shows the unauthenticated interface). "
                    "Received 2026-11-22 10:18 EST as an attachment; the query as the operator gave it after a '$'. Source chips and image cards kept as pasted; "
                    "the rendered formula's glyphs kept as the paste broke them; the interface furniture cut.]\n\n[QUERENT] " + Q2 + "\n\n[COMPOSER]\n" + clean(raw2))
d2["transcript_raw"] = raw2

judged = {d1["slug"]: ["distinction-collapse"], d2["slug"]: []}
for i, d in enumerate((d1, d2), 1):
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(i, d["slug"], "cites", d["cites"], "chars", len(d["transcript"]))
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
