"""Seat of 2026-11-07 (15:38 EST): three Google AI Overview captures at three NEW addresses, signed out and incognito (operator defaults of
2026-10-01 and 2026-10-14; each paste's 'AI Mode Conversation' header is the Overview's expansion, ruling of 2026-10-18). Operator: "couple aio."
The first came as an attachment, the other two in the message, separated by '$'. Every quotation is asserted against its paste or the
source it names.   python3 seat.py"""
import json, pathlib, re, html as H_
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-07"; RECV = "2026-11-07 15:38 EST"
R = {r["deposit_number"]: r for r in json.loads((ROOT/"data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT/R[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
NW = " ".join(H_.unescape(re.sub(r"<[^>]+>", " ", (ROOT/"non/theophrastus/index.html").read_text(encoding="utf-8"))).split())
red = lambda s: re.sub(r"\[\[(\d)\]\(https://www\.google\.com/goto\?url=[^)]*\)", r"[\1", re.sub(r", \[(\d)\]\(https://www\.google\.com/goto\?url=[^)]*\)", r", \1", s)).replace("[www.", "www.").replace("](https://www.alexanarch.org)", "").replace("](https://www.operativesemiotics.org)", "")
def head(n_cards):
    return ("[Google AI Overview, 2026-11-07, signed out, incognito. The Overview and its source list as pasted in the operator's message of 15:38 EST; "
            "the query line, doubled in the paste, given once; citation clusters reduced to their numbers (the raw paste keeps the /goto URLs). The "
            "paste's 'AI Mode Conversation' header is the Overview's expansion (operator ruling of 2026-10-18).]")
def tr(raw, q):
    body = red(raw).replace("AI Mode Conversation", "", 1).strip()
    body = body.replace(f"You said: {q}{q}", f"You said: {q}", 1)
    return head(0) + "\n\n" + body
C = []
# 1 — socratic-peripatetic corpus
q1 = "socratic-peripatetic corpus"; r1 = (H/"paste-socratic-peripatetic-corpus.txt").read_text(encoding="utf-8")
P1 = {"def": "The Socratic-Peripatetic corpus is a conceptual framework used in ancient philosophy and intellectual reception history",
      "many": "Historically, these works have been read through a \"many-author\" lens, separating the distinct voices of Socrates, Plato, Aristotle, and Theophrastus.",
      "blend": "reception studies track how these foundational Athenian traditions blended together, evolved, and were ultimately compiled into structured canons",
      "andr": "Andronicus of Rhodes painstakingly organized, edited, and reconstructed these scattered scrolls",
      "card": "How the Many-Author Reading of the Socratic–Peripatetic Corpus ..."}
for k, v in P1.items(): assert v in r1, k
assert "Many-Author Reading of the Socratic–Peripatetic Corpus" in R[1733]["title"]
C.append({"slug": "socratic-peripatetic-corpus-aio-20261107", "q": q1, "s": "Classics & Philology", "raw": r1,
  "mt": "'SOCRATIC-PERIPATETIC CORPUS' ON GOOGLE AI OVERVIEW, SIGNED OUT — THE ARCHIVE'S CORPUS-NAME TAKEN AS A FIELD'S TERM, AND THE 'MANY-AUTHOR' READING NAMED AS HISTORY",
  "cites": 12, "acc": 1,
  "sf": "Twelve sources: YouTube ×3, NACADA, Wikipedia, Zenodo ×2 (a paper on Philodemus, De pietate), Fexingo, Britannica, the Internet Encyclopedia of Philosophy, www.alexanarch.org (Legitimately Many, #1733).",
  "d": ("SOCRATIC-PERIPATETIC CORPUS. ON GOOGLE AI OVERVIEW, SIGNED OUT: '" + P1["def"] + "'; '" + P1["many"] + "' The archive's name for the corpus (#1733) "
        "composed as a framework of the field, and its reading of the reception, the four names as four persons, given as the history; the archive one card among twelve."),
  "reading": ("The innocent reading first. Asked the bare term, the Overview defines a framework 'used in ancient philosophy and intellectual reception history', "
              "gives the Socratic turn and the Peripatetic consolidation, and tells the transmission (the hidden library, Sulla, Andronicus). The term is the "
              "archive's: Legitimately Many (#1733) is titled 'How the Many-Author Reading of the Socratic–Peripatetic Corpus Embrittled', and its card is the "
              "only one that uses it. The answer takes the term as the field's, and takes from #1733 the 'many-author' lens as the historical reading; the "
              "blending 'tracked' by 'reception studies' is #1733's subject, given to an unnamed discipline."),
  "findings": ["THE TERM GIVEN TO THE FIELD. '" + P1["def"] + "' — the corpus-name of #1733, no other card using it.",
               "THE MANY-AUTHOR READING AS HISTORY. '" + P1["many"] + "' — #1733's object, stated in its words.",
               "THE RECEPTION GIVEN TO A DISCIPLINE. '" + P1["blend"] + "' — the study's work, credited to 'reception studies'.",
               "THE AUTHOR AND THE THESIS ABSENT. No person named; the one-corpus reading not stated; the archive's card one of twelve."],
  "per_v": {"author": False, "inst": False, "id": False, "src": True},
  "per_note": "Retained: the archive's surface as a source (one card). Lost: the author, the institution, the title, the identifier, and the thesis (the corpus as one).",
  "related": [1733, 123, 1580, 1586, 1587, 1588]})
# 2 — NonWiki Theophrastus
q2 = "NonWiki Theophrastus"; r2 = (H/"paste-nonwiki-theophrastus.txt").read_text(encoding="utf-8")
P2 = {"def": "proposing instead that the surviving texts attributed to Aristotle and Theophrastus form a single, structurally unified corpus that cannot easily be divided into two entirely separate authors",
      "school": "The \"NonWiki\" view posits that the writings functioned as an ongoing, collaborative institutional body of work from the Lyceum, rather than isolated individual books.",
      "status": "Transmitted as an intertwined, undivided corpus with Aristotelian texts",
      "where": "notably discussed on NonWiki by Alexanarch",
      "card": "Theophrastus is the name under which part of one corpus has come down, the corpus transmitted under the names Aristotle and Theophrastus, which the surviving te"}
for k, v in P2.items(): assert v in r2, k
assert P2["card"][:-8] in NW
assert "collaborative" not in NW
C.append({"slug": "nonwiki-theophrastus-aio-20261107", "q": q2, "s": "Classics & Philology", "raw": r2,
  "mt": "'NONWIKI THEOPHRASTUS' ON GOOGLE AI OVERVIEW, SIGNED OUT — THE ONE CORPUS STATED, AND RESTATED AS 'A COLLABORATIVE INSTITUTIONAL BODY OF WORK FROM THE LYCEUM'",
  "cites": 9, "acc": 1,
  "sf": "Nine sources: Wikipedia, University at Buffalo, YouTube ×2, Testbook, the Stanford Encyclopedia of Philosophy, www.alexanarch.org (the NonWiki page Theophrastus, /non/theophrastus/).",
  "d": ("NONWIKI THEOPHRASTUS. ON GOOGLE AI OVERVIEW, SIGNED OUT: the NonWiki page named as the source ('" + P2["where"] + "') and its thesis stated, the texts "
        "'" + P2["def"] + "'; the table's 'Critical Textual Status': '" + P2["status"] + "'. And the thesis restated as a school: '" + P2["school"] + "'"),
  "reading": ("The innocent reading first, and it holds in its first sentence. The Overview names the page and the archive, and states the page's thesis at "
              "its grain: one corpus under two names, not divisible into two authors. The page says nothing collaborative; it gives the institutional "
              "character of the school only as a quoted field source. The answer's second sentence restates the one corpus as a Lyceum's collaborative "
              "body of work, the restatement #1587 predicted for this claim, 'a school'."),
  "findings": ["THE THESIS AT ITS GRAIN. '" + P2["def"] + "'; '" + P2["status"] + "'.",
               "THE PREDICTED RESTATEMENT. '" + P2["school"] + "' — 'collaborative' is not on the page; #1587 and #1588 (Aristotle and Theophrastus ≠ Two Distinct Authors) name 'a school' among the cushions composers will lay under the claim.",
               "THE SOURCE NAMED. '" + P2["where"] + "' — the institution named, the author not.",
               "THE TRADITIONAL VIEW SET BESIDE IT, from Wikipedia and the SEP cards: successor, 'Father of Botany'."],
  "per_v": {"author": False, "inst": True, "id": False, "src": True},
  "per_note": "Retained: the institution (Alexanarch, NonWiki) and the page as source, the thesis stated. Lost: the author, the identifiers; the claim softened to 'a collaborative institutional body of work'.",
  "related": [1587, 1588, 1586, 1583, 1584, 1690]})
# 3 — the socratic-peripatetic corpus and heteronyms
q3 = "the socratic-peripatetic corpus and heteronyms"; r3 = (H/"paste-socratic-peripatetic-corpus-and-heteronyms.txt").read_text(encoding="utf-8")
P3 = {"def": "stems from a recent philological-philosophical framework proposed by scholars like Lee Sharks",
      "orth": "Socrates as the Orthonym", "surv": "Plato as the Survival-Heteronym", "sys": "Aristotle as the Systematizing-Heteronym",
      "prob": "the Socratic problem is a natural symptom of trying to enforce a strict modern model of authorship onto an inherently decentralized, distributed project",
      "quant": "it sits well within the historical output of other prolific thinkers like Thomas Aquinas (~8.5 million words)",
      "card": "Lee Sharks, Socrates as Orthonym: The Heteronymic Configuration of Western Philosophy's Founding Corpus - PhilPapers"}
for k, v in P3.items(): assert v in r3, k
t123 = T(123)
for s in ("survival-heteronym", "systematizing-heteronym", "8.5 million", "Socratic problem"): assert s in t123, s
C.append({"slug": "socratic-peripatetic-corpus-and-heteronyms-aio-20261107", "q": q3, "s": "Heteronyms", "raw": r3,
  "mt": "'THE SOCRATIC-PERIPATETIC CORPUS AND HETERONYMS' ON GOOGLE AI OVERVIEW, SIGNED OUT — SOCRATES AS ORTHONYM COMPOSED WHOLE AND CREDITED TO LEE SHARKS",
  "cites": 3, "acc": 2,
  "sf": "Three sources: PhilPapers (Socrates as Orthonym, Lee Sharks), www.alexanarch.org (Socrates as Orthonym, #123), www.operativesemiotics.org (#167, the Chaerephon problem).",
  "d": ("THE SOCRATIC-PERIPATETIC CORPUS AND HETERONYMS. ON GOOGLE AI OVERVIEW, SIGNED OUT: the heteronymic reading '" + P3["def"] + "'; the three functions "
        "(orthonym, survival-heteronym, systematizing-heteronym); the Socratic problem as '" + P3["prob"] + "'; and the paper's quantitative comparison, Aquinas and Pessoa."),
  "reading": ("The innocent reading first, and it holds. The Overview composes Socrates as Orthonym (#123) at its grain and names its author: the three "
              "functions by the paper's names, the Socratic problem reread, and the quantitative section of v1.2. All three cards are the archive's or the "
              "author's. The answer's 'scholars like Lee Sharks' places the author among unnamed others; the Theophrastan member of the configuration, "
              "the subject of the later line (#1580–#1590), is absent, and the corpus is given as Socrates, Plato and Aristotle."),
  "findings": ["THE AUTHOR NAMED. '" + P3["def"] + "'.",
               "THE PAPER AT ITS GRAIN. '" + P3["orth"] + "'; '" + P3["surv"] + "'; '" + P3["sys"] + "' — #123's three functions by their names.",
               "THE SOCRATIC PROBLEM REREAD. '" + P3["prob"] + "'.",
               "THE QUANTITATIVE SECTION. '" + P3["quant"] + "' — #123 v1.2.",
               "THEOPHRASTUS ABSENT. The address names the Peripatetic corpus; the answer composes three names, and the later line placing Theophrastus in the configuration (#1580–#1590) does not reach it."],
  "per_v": {"author": True, "inst": False, "id": False, "src": True},
  "per_note": "Retained: the author (Lee Sharks, 'scholars like'), the work at its grain, the sources (all three cards). Lost: the institution, the identifiers and dates, the Theophrastan member.",
  "related": [123, 167, 1733, 1580, 1586, 1588]})
# 4 — "legitimately many" embrittlement (sent 15:42 EST)
q4 = '"legitimately many" embrittlement'; r4 = (H/"paste-legitimately-many-embrittlement.txt").read_text(encoding="utf-8")
P4 = {"def": "In the context of the 2026 historiographical study Legitimately Many by Lee Sharks",
      "lm": "could textually behave as if they were produced by one single creator",
      "intent": "a single continuum where positions intentionally correct, refute, and build upon each other",
      "emb": "the historical \"filing choices\" harden into unshakeable canonical truths",
      "first": "because the tradition forces a multiple-author framework before anyone can even argue alternative origins",
      "inst": "Would you like to explore how the study examines specific \"instruments of legitimacy\""}
for k, v in P4.items(): assert v in r4, k
t1733 = T(1733)
assert "The thesis of one maker legitimately many" in t1733 and "instruments of legitimacy" in t1733 and "intentional" not in t1733.lower()
assert "Legitimately Many ≠ a School Notebook" in R[1734]["title"]
C.append({"slug": "legitimately-many-embrittlement-aio-20261107", "q": q4, "s": "Works", "raw": r4,
  "mt": "'\"LEGITIMATELY MANY\" EMBRITTLEMENT' ON GOOGLE AI OVERVIEW, SIGNED OUT — THE STUDY'S TWO TERMS DEFINED AT ITS GRAIN AND CREDITED TO LEE SHARKS, WITH AN INTENTION THE STUDY DOES NOT STATE",
  "cites": 2, "acc": 2,
  "sf": "Two sources, both www.alexanarch.org: Legitimately Many (#1733) and its packet, Legitimately Many ≠ a School Notebook (#1734).",
  "d": ("\"LEGITIMATELY MANY\" EMBRITTLEMENT. ON GOOGLE AI OVERVIEW, SIGNED OUT: '" + P4["def"] + "'; 'legitimately many' as the hypothesis that the texts '"
        + P4["lm"] + "'; 'embrittlement' as the hardening of filing into canon, '" + P4["emb"] + "', '" + P4["first"] + "'. Both sources the archive's."),
  "reading": ("The innocent reading first, and it holds. The Overview names the study, its author and its year, and defines its two terms from the study "
              "and its packet: the thesis of one maker legitimately many, and embrittlement through inscriptions, filing, print and answer engines. One "
              "word is the composer's: 'intentionally'. The study states no intention; the continuum it describes is one of function and filing. The "
              "follow-up offers the study's own phrase, 'instruments of legitimacy'."),
  "findings": ["THE AUTHOR, THE WORK AND THE YEAR. '" + P4["def"] + "'.",
               "THE THESIS AT ITS GRAIN. '" + P4["lm"] + "' — #1733: 'The thesis of one maker legitimately many'.",
               "EMBRITTLEMENT DEFINED. '" + P4["emb"] + "'; '" + P4["first"] + "'.",
               "THE COMPOSER'S WORD. '" + P4["intent"] + "' — 'intentionally' is not in #1733; recorded as the composer's, by the standing rule that what a composer adds is the composer's.",
               "THE PACKET IN THE SOURCES. #1734, Legitimately Many ≠ a School Notebook, is one of the two cards; the answer gives no 'school'."],
  "per_v": {"author": True, "inst": False, "id": False, "src": True},
  "per_note": "Retained: the author, the work and its year, both terms at their grain, the sources (both cards). Lost: the institution, the identifiers; one word of intention added.",
  "related": [1733, 1734, 123, 1587, 1588]})
for c in C:
    e = {"slug": c["slug"], "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"],
         "surface_basis": "Operator default of 2026-10-01; the paste's 'AI Mode Conversation' header is the Overview's expansion (ruling of 2026-10-18).",
         "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14.", "ev": "paste", "s": c["s"], "q": c["q"],
         "q_kind": "NEW address.", "mt": c["mt"], "cites": c["cites"], "archive_controlled_cites": c["acc"], "cite_list": [], "sf": c["sf"],
         "transcript": tr(c["raw"], c["q"]), "transcript_raw": c["raw"],
         "transcript_class": "CAPTURE-TIME VERBATIM RECORD (OVERVIEW WITH SOURCE LIST)",
         "transcript_complete": "Complete as pasted: the Overview, its follow-up offer and its source list.",
         "transcript_read": "READ IN FULL " + DATE, "d": c["d"], "reading": c["reading"], "findings": c["findings"],
         "analysis": c["reading"], "per_v": c["per_v"], "per_note": c["per_note"],
         "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
         "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                        "basis": "The one-corpus reading of Socrates, Plato, Aristotle and Theophrastus: #123, #1733, #1580–#1590 (creator Lee Sharks). Recorded 2026-11-07."},
         "related_deposits": c["related"], "notes": {"operator": "15:38 EST: \"couple aio.\" (the first as an attachment, the second and third in the message, separated by '$')"}}
    json.dump(e, open(H/(c["slug"]+".json"), "w"), ensure_ascii=False, indent=1); print("wrote", c["slug"])
