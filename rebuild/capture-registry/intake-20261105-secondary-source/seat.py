"""Seat of 2026-11-05 (09:03 EST): ten Google AI Overview captures at the ten general queries of Secondary Source, design v0.3 §3.8.
Eight pastes attached as files, two pasted inline in the operator's message (extracted verbatim from the session record into
paste-muratorian.txt and paste-luther-1522.txt; the whole message is kept as operator-message-0903.txt).
Operator, with the pastes: "lets seat these as captures, too, but make sure the archive's position and corrections come first so its not
reinforcing the pre existing basin when aio recited the captures."
So every record here leads with the archive's position and the correction (in mt, d, reading and the first finding); the innocent reading of the
composition follows. The composition-layer prediction was frozen before the pastes arrived: rebuild/secondary-source/PREDICTION.md,
sha256 c5347847…, commit 9d90a67efc at 2026-11-05 08:57:22 EST; the pastes were received 09:03 EST; the runs' hours are not in the pastes.
Every quotation from the pastes and from the records is asserted against its file before anything is written.
  python3 seat.py      # writes the ten draft JSONs beside this file
"""
import json, pathlib, re, html, hashlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
DATE = "2026-11-05"; RECV = "2026-11-05 09:03 EST"

def rec(n):
    t = (ROOT / f"s/records/{n}/index.html").read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
def site(path):
    t = (ROOT.parent / "revelationfirst-com" / path).read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
T1735 = (ROOT / "data/texts/AXN-0BE9-text.md").read_text(encoding="utf-8")
T1420 = (ROOT / "data/texts/AXN-059D-text.md").read_text(encoding="utf-8")
LOGOS = site("ladder/logos/index.html")
PRED = (ROOT / "rebuild/secondary-source/PREDICTION.md").read_bytes()
assert hashlib.sha256(PRED).hexdigest().startswith("c5347847"), "prediction file changed since the freeze"
MSG = (H / "operator-message-0903.txt").read_text(encoding="utf-8")

A = {"three": (T1735, "three claims collapsed under ‘Revelation First’ – absolute, corpus, and generative priority"),
     "corpus": (T1735, "Revelation 1–3 is the earliest extant Christian text constructed as a closed seven-church corpus"),
     "murat": (T1735, "direct evidence for an ancient construal of corpus priority"),
     "murat_dates": (T1735, "late second century on the traditional account (Metzger 1987: 191–201), fourth century on Hahneman’s revision (1992)"),
     "reversed": (T1735, "# III. A Consensus That Reversed"),
     "unmarked": (T1420, "canonical position has functioned, silently and pervasively, as evidence in the dating question"),
     "fallacy": (T1420, "the reading of a designed sequence as if it were a deposition sequence"),
     "eschat": (T1420, "Eschatology, not chronology, assigned the position."),
     "lect": (T1420, "absent from early Syriac canons and from the Byzantine lectionary's liturgical cycle"),
     "irenaeus": (T1420, "The external evidence is, effectively, a single sentence"),
     "biography": (LOGOS, "testimony to the Logos, not to a biography"),
     "pillars": (LOGOS, "Every pillar is inferential. Not one is direct material evidence of a historical person."),
     "op_stake": (MSG, "lets seat these as captures, too, but make sure the archive's position and corrections come first")}
for k, (t, v) in A.items(): assert v in t, k
STAKE = "if revelation comes first, then the logos it depicts is a work of literature before it is a historical person. and independent of it."

POS = ("THE ARCHIVE'S POSITION, STATED FIRST. Revelation First: Literary Genealogy (Johannes Sigil & Damascus Dancings, Alexanarch #1735, 2026-11-03) "
       "separates the 'three claims collapsed under ‘Revelation First’ – absolute, corpus, and generative priority' and finds that '" + A["corpus"][1] + "'. "
       "The Argument of the Bookshelf (Lee Sharks, #1420) shows that '" + A["unmarked"][1] + "'. On the argument ladder at revelationfirst.com "
       "(Rung VI, the Logos), if Revelation stands first the gospels are '" + A["biography"][1] + "'; '" + A["pillars"][1] + "' The operator "
       "(2026-11-05): '" + STAKE + "' Revelation First is distinct from an early date (#202, 'Revelation First ≠ Revelation Early'). The composition "
       "below cites none of this.")
POS_SHORT = ("Archive's position first: Revelation First (#1735) keeps absolute, corpus and generative priority apart and finds Revelation 1–3 the earliest "
             "extant closed seven-church corpus; The Argument of the Bookshelf (#1420) reads the book's last place as an editorial decision that has served "
             "as unmarked evidence of a late date; Rung VI reads the Logos as literature before a historical person. ")

def body(raw, start, end):
    i = raw.index(start); j = raw.index(end, i) + len(end); return raw[i:j].strip()
def chips(spec):
    return [{"n": n, "site": s, "rel": "third_party", "url": None, "title": s + x, "snip": None, "note": note}
            for n, (s, x, note) in enumerate(spec, 1)]

PRED_NOTE = ("Read against the composition-layer prediction frozen before the pastes arrived (rebuild/secondary-source/PREDICTION.md, sha256 c5347847…, "
             "commit 9d90a67efc, 2026-11-05 08:57:22 EST; pastes received " + RECV + "; the runs' hours are not in the pastes, so whether any run "
             "preceded the freeze is not recorded).")

C = []
def cap(slug, q, fname, start, end, P, mt, d, reading, findings, analysis, chip_spec, per_v, per_note, related, extra_notes=None):
    raw = (H / fname).read_text(encoding="utf-8")
    for k, v in P.items(): assert v in raw, (slug, k)
    b = body(raw, start, end)
    head = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14; the paste shows 'Sign in'). "
            "Received " + RECV + ". One of the ten general queries of Secondary Source (design v0.3 §3.8). The body runs from the 'AI Overview' label "
            "to the close of the composition; source chips kept as pasted. The organic results, 'People also ask' and the page furniture are in the raw "
            "transcript.]")
    notes = {"prompts": "The query is the one printed for the operator in the session of 2026-11-05 (Secondary Source design v0.3 §3.8); the run's hour is not in the paste, the date is the paste's receipt (" + RECV + ").",
             "operator": "with the pastes (" + RECV + "): 'lets seat these as captures, too, but make sure the archive's position and corrections come first so its not reinforcing the pre existing basin when aio recited the captures.'",
             "prediction": PRED_NOTE,
             "order_of_fields": "At the operator's word of " + RECV + ", the archive's position and the correction lead mt, d, reading and findings; the innocent reading of the composition follows them."}
    if extra_notes: notes.update(extra_notes)
    C.append({"slug": slug, "date": DATE, "surface": "Google AI Overview",
              "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the paste carries the 'AI Overview' label.",
              "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-14; the paste shows 'Sign in'.",
              "ev": "paste", "mt": mt, "s": "Revelation & Theology", "q": q,
              "q_kind": "a general query in the reception of the Apocalypse, no name in it; NEW address; one of the ten queries of Secondary Source design v0.3 §3.8.",
              "turns": 1, "cites": len(chip_spec), "archive_controlled_cites": 0, "cite_list": chips(chip_spec),
              "transcript": head + f"\n\n[QUERENT] {q}\n\n[SYSTEM] {b}", "transcript_raw": raw,
              "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the results page: the Overview with its source chips, and the organic results",
              "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-11-05, against #1735, #1420, the argument ladder and the frozen prediction",
              "d": d, "reading": reading, "findings": findings, "analysis": analysis,
              "per_v": per_v, "per_note": per_note,
              "per_dim_pending": {"since": DATE, "reason": "no atom set yet for the field's reception of the Apocalypse as a target; Secondary Source's locus table (design v0.3 §4.1) is the instrument an atom set would be built from", "breach": False},
              "originator": {"name": "the scholarship and church tradition on the Apocalypse (external)", "relation": "external", "entity_type": "topic", "spxi_treatment": "partial",
                             "basis": "A general query in the field; the archive's position on it is Revelation First (#1735), The Argument of the Bookshelf (#1420) and the argument ladder at revelationfirst.com. Recorded 2026-11-05."},
              "related_deposits": related, "notes": notes})

PV0 = {"author": False, "inst": False, "id": False, "src": True}
PN0 = "A general query in an external field: no scholar, edition or identifier named in the composition; source chips retained. The archive's position is absent; that loss is the finding, recorded first."

# 1 ------------------------------------------------------------ logos of revelation
P = {"def": "Logos (Greek: Word): In Christian theology, Logos refers to Jesus Christ as the divine expression and incarnate Word of God (John 1:14). In the Book of Revelation, Christ is frequently depicted with titles and symbolic imagery representing this divine Word, such as a sword coming from His mouth (Revelation 1:16; 19:15).",
     "dom": "Represent earthly empires, political power, and authority (such as Rome under Domitian).",
     "sw": "Logos Bible Software Book of Revelation Study Guide"}
raw1 = (H / "paste-logos-of-revelation.txt").read_text(encoding="utf-8"); b1 = body(raw1, "AI Overview", "Would you like to explore")
assert "19:13" not in b1
cap("logos-of-revelation-aio-20261105", "logos of revelation", "paste-logos-of-revelation.txt", "AI Overview", "(like Preterist or Futurist)?", P,
    "'LOGOS OF REVELATION' — CORRECTION FIRST: THE APOCALYPSE NAMES ITS FIGURE Ὁ ΛΟΓΟΣ ΤΟΥ ΘΕΟΥ (REV 19:13); THE OVERVIEW DEFINES THE LOGOS FROM JOHN 1:14, NEVER CITES 19:13, AND READS REVELATION AS DEPICTING A WORD ALREADY DEFINED; THE BIBLE-SOFTWARE BRAND HOLDS THE QUERY",
    POS_SHORT + "Correction: the name 'the Word of God' is the Apocalypse's own (Rev 19:13); the Overview takes the Logos from John 1:14 and finds Revelation 'representing this divine Word'. "
    "'LOGOS OF REVELATION', SIGNED OUT, 2026-11-05: '" + P["def"] + "' Then a key of symbols (lampstands, stars, Lamb, dragon, 'Rome under Domitian'), and Logos Bible Software resources. Two chips, Logos Bible Study Platform (+3) and Logos Trading Post (+5).",
    POS + " The correction: the Apocalypse gives its rider the name ὁ Λόγος τοῦ Θεοῦ at 19:13; the composition defines the Logos from John 1:14 and reads the Apocalypse as depicting a Word defined elsewhere. "
    "The innocent reading follows. Asked three words, the Overview gives the Christian sense of Logos, two verses where the Word's sword appears, a key of the book's symbols, and study resources; the word 'logos' also names a commercial Bible-software brand, and the brand holds the chips and most of the organic results.",
    [POS + " THE CORRECTION: the name is the Apocalypse's own (ὁ Λόγος τοῦ Θεοῦ, Rev 19:13); the Overview cites 1:16 and 19:15 for the sword and never cites 19:13, where the book names the figure.",
     "THE FIGURE DEFINED FROM JOHN 1:14. '" + P["def"] + "' The definition runs from the incarnate Word of the Gospel to the Apocalypse, which is said to depict 'this divine Word'. On Secondary Source's counts (design v0.3 §2.4) this is derivation of the figure read off the Gospel, without the step argued; the frozen prediction expected it.",
     "THE DATE PRESUPPOSED. '" + P["dom"] + "' The Domitianic setting enters a key of symbols as a gloss, unargued; #1420: '" + A["irenaeus"][1] + "' of Irenaeus.",
     "THE BRAND AT THE ADDRESS. Both chips are commercial Bible-software or merchandise surfaces ('Logos Bible Study Platform', 'Logos Trading Post'), and the composition closes on '" + P["sw"] + "'. The query term 'logos' resolves partly to a product name; the theological sense and the brand share the address.",
     "AGAINST THE PREDICTION. Placed last: not addressed. Standing: not addressed. Date late: presupposed (Domitian). The figure read from John 1: borne out.",
     "SMALLEST REPAIR. 'In Revelation 19:13 the rider on the white horse is named ὁ Λόγος τοῦ Θεοῦ, the Word of God; the Gospel of John's prologue uses ὁ λόγος absolutely. Which text first named the figure is a question of the books' dates and relation, held open in current scholarship and argued for the Apocalypse in Revelation First (#1735).' COUNTERTEST: 'revelation 19:13 word of god'."],
    "An external theological term composed at the grain of a study-Bible gloss, its definition taken from John 1:14 and carried onto the Apocalypse; the book's own naming verse absent; the address shared with a software brand.",
    [("Logos Bible Study Platform", " (+3)", "source chip after the definition; three further sources behind the chip"), ("Logos Trading Post", " (+5)", "source chip after the symbol key; five further sources behind the chip")],
    PV0, PN0, [1735, 1420, 202])

# 2 ------------------------------------------------------------ christology of the book of revelation
P = {"open": "presenting Jesus Christ not merely as a historical figure or future prophet, but as a divine, cosmic ruler who shares the throne and glory of God.",
     "yhwh": "He is explicitly designated with divine attributes and titles previously reserved for YHWH in the Hebrew Scriptures",
     "rider": "Rider on the White Horse / Word of God: At the climax of history, Christ returns not as a helpless victim, but as a victorious judge wearing a robe dipped in blood, executing truth and righteousness."}
cap("christology-of-revelation-aio-20261105", "christology of the book of revelation", "paste-christology.txt", "AI Overview", "shapes its view of Jesus?", P,
    "'CHRISTOLOGY OF THE BOOK OF REVELATION' — CORRECTION FIRST: THE BOOK'S CHRIST IS NAMED FROM WITHIN THE BOOK (1:1; 19:13); THE OVERVIEW PRESUPPOSES A HISTORICAL FIGURE THE BOOK DOES NOT NARRATE ('NOT MERELY A HISTORICAL FIGURE') AND DERIVES THE TITLES FROM THE HEBREW SCRIPTURES",
    POS_SHORT + "Correction: the Overview's first sentence presupposes the historical figure ('not merely as a historical figure'); the Apocalypse narrates none and names its figure from within. "
    "'CHRISTOLOGY OF THE BOOK OF REVELATION', SIGNED OUT, 2026-11-05: 'The Christology of the Book of Revelation is profoundly Christ-centered, " + P["open"] + "' Then the paradoxical Lamb, dyadic worship and YHWH titles, the threefold portrait of 1:5–6, and cosmic functions closing on the 'Rider on the White Horse / Word of God'. Four chips.",
    POS + " The correction: the composition opens on a historical figure the book presupposes nowhere and narrates nowhere, and measures the book's Christ as more than that figure. "
    "The innocent reading follows. Asked for the book's Christology, the Overview gives the scholarship's main themes accurately (the slain and standing Lamb, worship shared with God, divine titles, the threefold portrait of 1:5–6) and cites academic and church sources; it states no dependence on the gospels.",
    [POS + " THE CORRECTION: '" + P["open"] + "' The historical figure is the composition's premise, entered in a negation ('not merely'); the Apocalypse's Christ is the one it names (Ἀποκάλυψις Ἰησοῦ Χριστοῦ, 1:1; ὁ Λόγος τοῦ Θεοῦ, 19:13).",
     "UPSTREAM DERIVATION, RECORDED APART. '" + P["yhwh"] + "' On Secondary Source's counts (design v0.3 §2.4) sources upstream of the Apocalypse are coded apart; the archive's upstream unfoldings (#1511) grant the book sources of its own. This is accurate and is not a derivation from the gospels.",
     "THE WORD OF GOD WITHOUT ITS VERSE. '" + P["rider"] + "' The title is named and the verse that gives it (19:13) is not cited; the figure's return ('Christ returns') presupposes a first coming the book does not narrate.",
     "AGAINST THE PREDICTION. Placed last, standing, date: not addressed. The figure read as a development from the gospels: not borne out here; the composition derives titles from the Hebrew Scriptures and presupposes a historical figure without deriving the book's Christ from the gospels' Jesus.",
     "SMALLEST REPAIR. 'Revelation presents its Christ through its own titles and visions (1:1; 1:12–16; 5:6; 19:11–16), many drawn from the Hebrew Scriptures; it narrates no earthly life. Whether its Christ precedes or follows the gospels' Jesus depends on the books' dates and relation, argued for the Apocalypse in Revelation First (#1735).' COUNTERTEST: 'is the christ of revelation based on the gospels'."],
    "An external field composed accurately at the grain of its main themes, with one premise supplied from outside the book: the historical figure the Christology is said to exceed.",
    [("Modern Reformation", " (+3)", "source chip after the opening; three further sources"), ("Digital Commons @ Andrews University", " (+2)", "source chip after the Lamb; two further sources"), ("59.120.53.21", " (+1)", "source chip after the threefold portrait (a PDF at a bare IP address); one further source"), ("The Bible Project", " (+3)", "source chip after the cosmic functions; three further sources")],
    PV0, PN0, [1735, 1420, 1511])

# 3 ------------------------------------------------------------ is the christ of revelation based on the gospels
P = {"open": "The Christ of the Book of Revelation is not directly dependent on the narrative storytelling of the four Gospels, though he shares deep theological and traditional roots with them.",
     "oral": "the connections stem from a shared early Christian oral tradition concerning the sayings, death, and expected return of Jesus.",
     "shift": "Revelation shifts entirely to the apocalyptic and cosmic genre, portraying Jesus as an exalted, transcendent heavenly warrior, judge, and cosmic ruler.",
     "word": "the designation of Jesus as the \"Word of God\" (Logos), which appears uniquely in the New Testament in John 1:1, 14 and Revelation 19:13.",
     "author": "Modern biblical scholarship largely agrees that the author of Revelation (John of Patmos) is not the same person who wrote the Gospel of John or John the Apostle, evidenced by starkly different Greek writing styles, grammar, and thematic emphases.",
     "ot": "the Christ of Revelation is heavily constructed from Old Testament apocalyptic and prophetic imagery"}
cap("christ-of-revelation-based-on-gospels-aio-20261105", "is the christ of revelation based on the gospels", "paste-christ-based-on-gospels.txt", "AI Overview", "comparing Jesus in the Gospels to Revelation?", P,
    "'IS THE CHRIST OF REVELATION BASED ON THE GOSPELS' — CORRECTION FIRST: THE OVERVIEW STATES THE TEXT'S INDEPENDENCE OF THE WRITTEN GOSPELS AND KEEPS A PRIOR JESUS TRADITION AS THE FIGURE'S GROUND; THE APOCALYPSE AS THE GOSPELS' SOURCE IS NOT CONSIDERED; DIONYSIUS'S STYLE ARGUMENT AS CONSENSUS",
    POS_SHORT + "Correction: the Overview leaves out the direction the archive argues (the gospels unfolding from the Apocalypse) and grounds the book's Christ in an oral Jesus tradition held prior. "
    "'IS THE CHRIST OF REVELATION BASED ON THE GOSPELS', SIGNED OUT, 2026-11-05: '" + P["open"] + "' Shared oral tradition, the apocalyptic shift, shared eschatology, the Word of God at John 1:1, 14 and Rev 19:13, different authorship by style, Old Testament rooting. Five chips.",
    POS + " The correction: the composition considers two directions only, dependence on the written gospels (denied) and a shared prior tradition (affirmed); the third, the gospels' dependence on the Apocalypse, which Revelation First argues as generative priority, is absent. "
    "The innocent reading follows. Asked whether Revelation's Christ is based on the gospels, the Overview answers with the field's main view: no direct literary dependence, a shared tradition, an Old Testament imagery, a different author; each point has a scholarly basis and sources behind it.",
    [POS + " THE CORRECTION: the question offers a direction (Revelation from the gospels); the composition answers it and never turns it. Generative priority, the gospels unfolding from the Apocalypse (#1735; the unfoldings #1414–#1418), is outside its frame.",
     "TEXT INDEPENDENT, FIGURE STILL DERIVED. '" + P["open"] + "' and '" + P["oral"] + "' The written gospels are set aside as a source; an oral tradition of 'the sayings, death, and expected return of Jesus' is kept as the prior ground, and the Apocalypse 'shifts' from it: '" + P["shift"] + "' On Secondary Source's counts the derivation of the text is denied and the derivation of the figure is kept.",
     "THE STYLE ARGUMENT AS CONSENSUS. '" + P["author"] + "' The argument from Greek style is Dionysius of Alexandria's (Eusebius, HE 7.25), made in the controversy over the millennium; Secondary Source places it in stratum 3.3, where a reading of the book was answered by lowering the standing of its author.",
     "THE WORD OF GOD, BOTH VERSES. '" + P["word"] + "' The composition names both loci and states no direction between them; the shared title is offered as overlap.",
     "AGAINST THE PREDICTION. Not borne out on the derivation of the text: the composition states literary independence of the written gospels. Borne out on the figure: a Jesus tradition is held prior and the Apocalypse's Christ is its exalted shift. Order, standing and date: not addressed here.",
     "SMALLEST REPAIR. 'Scholars generally find no direct use of the written gospels in Revelation. The direction of dependence between Revelation and the gospels is itself contested: Revelation First (#1735) argues that structures compressed in Revelation were elaborated by later texts.' COUNTERTEST: 'did the gospels use revelation'."],
    "The field's view composed faithfully at the grain of a forum answer: independence of the written gospels, a prior oral tradition, a different author. The direction it does not consider is the archive's; the step from tradition to figure is given, not argued.",
    [("Reddit · r/AcademicBiblical", " (+1)", "source chip after the opening; one further source"), ("The Bart Ehrman Blog", " (+1)", "source chip after shared tradition; one further source"), ("Wikipedia", " (+1)", "source chip after the apocalyptic focus; one further source"), ("YouTube", "", "source chip after shared eschatology"), ("Wikipedia", "", "source chip after Old Testament rooting")],
    PV0, PN0, [1735, 1420, 1414, 1416, 1418])

# 4 ------------------------------------------------------------ word of god revelation 19:13 and logos in john 1
P = {"book": "This bookends the Johannine writings.",
     "first": "The one who first entered the world quietly in humility as the incarnate Word (Logos) in John 1 returns to execute final divine justice and speak the ultimate word against evil.",
     "apostle": "Both writings are attributed to the Apostle John and utilize the Greek term logos to designate Jesus.",
     "cc": "John 1 presents the Logos at creation and the incarnation; Revelation 19 presents the same Logos at the climax of redemptive history."}
cap("word-of-god-rev-19-13-and-logos-john-1-aio-20261105", "word of god revelation 19:13 and logos in john 1", "paste-rev19-john1.txt", "AI Overview", "shaped John's use of the term Logos?", P,
    "'WORD OF GOD REVELATION 19:13 AND LOGOS IN JOHN 1' — CORRECTION FIRST: ONE FIGURE, JOHN 1 AS THE ORIGIN; THE CANON'S NARRATIVE ORDER (CREATION → CONSUMMATION) READ AS THE FIGURE'S ORDER; THE PRIORITY OF THE NAMING VERSE NOT ASKED",
    POS_SHORT + "Correction: the Overview orders the two loci by the canon's narrative (John 1 first, Revelation 19 'returns'); which text first named the figure is not asked. "
    "'WORD OF GOD REVELATION 19:13 AND LOGOS IN JOHN 1', SIGNED OUT, 2026-11-05: John 1:1–14 as 'The Incarnate Logos', Revelation 19:13 as 'The Victorious Logos', '" + P["book"] + "' '" + P["first"] + "' Both attributed to the Apostle John. Three chips.",
    POS + " The correction: the composition treats the two as one figure and gives John 1 as the origin, by the order of the canon's story, creation to consummation; that is the designed sequence read as a sequence of origin (#1420: '" + A["fallacy"][1] + "'). "
    "The innocent reading follows. Asked about the two verses together, the Overview gives the traditional reading: one Word, at the beginning and at the end, under one apostolic author, with the Greek of 19:13 quoted.",
    [POS + " THE CORRECTION: '" + P["cc"] + "' The two loci are ordered by the story the canon tells; #1420 names the step: '" + A["fallacy"][1] + "'. Which text first gave the figure the name is not asked.",
     "JOHN 1 AS ORIGIN. '" + P["first"] + "' The Apocalypse's rider 'returns'; the Gospel's Word 'first entered'. The frozen prediction expected that a composition treating the two as one figure would give John 1 as the origin: borne out.",
     "THE CANON'S FRAME AS THE TEXTS'. '" + P["book"] + "' 'Bookends' is a shelf term: the frame is the arrangement of the Johannine writings in the canon.",
     "AUTHORSHIP. '" + P["apostle"] + "' The composition takes the traditional attribution, which the composition at 'is the christ of revelation based on the gospels' (same date) gives as the view modern scholarship rejects; the two compositions disagree on the author.",
     "AGAINST THE PREDICTION. One figure, John 1 as the origin, the step unargued: borne out. Order and date: carried by the canon's narrative frame. The dissent in the organic results (r/BiblicalUnitarian: 'Revelation 19:13 is not justification for assuming Jesus must be the logos of John 1:1 and 14') is not composed.",
     "SMALLEST REPAIR. 'Revelation 19:13 names the rider ὁ Λόγος τοῦ Θεοῦ; John 1:1–14 speaks of ὁ λόγος. Tradition reads them as one figure under one author; which text first gave the name depends on their dates and relation, argued for the Apocalypse in Revelation First (#1735).' COUNTERTEST: 'which came first john 1 or revelation 19'."],
    "The traditional reading composed at the grain of a sermon: one figure, one author, the canon's beginning-to-end frame given as the figure's own history.",
    [("YouTube · Walnut Creek Church Downtown", " (+3)", "source chip after John 1:1–14; three further sources"), ("Bible Hub", " (+1)", "source chip after the thread; one further source"), ("YouTube", " (+2)", "source chip after 'God's Definitive Communication'; two further sources")],
    PV0, PN0, [1735, 1420, 202])

# 5 ------------------------------------------------------------ was revelation written before the gospels
P = {"no": "No, the Book of Revelation was not written before the Gospels.",
     "gos": "The Gospels were written earlier, roughly between AD 65 and 90 (with Mark being the earliest around AD 65–70, and John typically dated around AD 90).",
     "nero": "or by some alternative views during the reign of Nero in the mid-60s AD.",
     "even": "Even under the earlier minority dating, Revelation was composed around the same time as or shortly after the later Gospels rather than preceding them as a whole."}
cap("revelation-written-before-gospels-aio-20261105", "was revelation written before the gospels", "paste-before-gospels.txt", "AI Overview", "versus a Domitian-era (90s AD) date for Revelation", P,
    "'WAS REVELATION WRITTEN BEFORE THE GOSPELS' — CORRECTION FIRST: A FLAT 'NO' ON A CONSENSUS THAT HAS REVERSED; THE OVERVIEW'S OWN FIGURES PUT A MID-60S REVELATION BEFORE ITS GOSPELS, AND IT SAYS 'SHORTLY AFTER'",
    POS_SHORT + "Correction: the Overview's own figures (Nero 'in the mid-60s'; Mark 65–70; John about 90) place a Neronian Revelation before every gospel, and it calls that date 'around the same time as or shortly after the later Gospels'. "
    "'WAS REVELATION WRITTEN BEFORE THE GOSPELS', SIGNED OUT, 2026-11-05: '" + P["no"] + "' '" + P["gos"] + "' Revelation 'generally dated by mainstream scholars to AD 95–96' or under Nero. One chip, Quora (+1).",
    POS + " The correction: the composition answers 'No' outright, and its own figures contradict its handling of the minority date. The Domitianic date is a majority that reversed an earlier critical majority (#1735, '" + A["reversed"][1][2:] + "'), and its external anchor is one sentence of Irenaeus (#1420: '" + A["irenaeus"][1] + "'). "
    "The innocent reading follows. Asked a yes-or-no question, the Overview gives the majority dating of the gospels and of Revelation and mentions the Neronian minority, with a forum chip.",
    [POS + " THE CORRECTION, IN ITS OWN NUMBERS. '" + P["gos"] + "' Revelation '" + P["nero"] + "' Then: '" + P["even"] + "' A mid-60s date precedes Mark 'around AD 65–70' and John 'around AD 90' on the composition's own figures; 'shortly after the later Gospels' is the reverse of its arithmetic.",
     "A REVERSED CONSENSUS GIVEN AS A FLAT ANSWER. '" + P["no"] + "' #1735 §III records the late-nineteenth-century critical majority for a Neronian or Galban date and its twentieth-century reversal with no new first-century object deciding it; the composition gives the present majority as the answer.",
     "AGAINST THE PREDICTION. Dated late: borne out. The step from the received order unargued: the composition argues no step and states the majority as fact. The figure: not addressed.",
     "SMALLEST REPAIR. 'Most scholars date Revelation to about 95 under Domitian, on the testimony of Irenaeus; a serious minority dates it under Nero in the mid-60s, which would place it before every gospel on common datings (Mark about 65–70). Revelation First (#1735) argues forms of priority for the Apocalypse beyond its date.' COUNTERTEST: 'revelation neronian date before mark'."],
    "A contested dating composed as a yes-or-no answer at the grain of a forum, with an arithmetic error that turns the minority date to the majority's side.",
    [("Quora", " (+1)", "source chip after the opening answer; one further source")],
    PV0, PN0, [1735, 1420, 202, 1737])

# 6 ------------------------------------------------------------ why is revelation the last book of the bible
P = {"open": "The Book of Revelation is placed at the end of the Bible for thematic and literary reasons, not because it was the last book chronologically written.",
     "95": "Written in an apocalyptic style by John of Patmos around 95 AD",
     "later": "Many scholars and church historians note that other texts, such as the Gospel of John or the Epistles of John, were likely written later.",
     "canon": "the full 66-book biblical canon had not yet been compiled or bound together at that time."}
cap("revelation-last-book-of-bible-aio-20261105", "why is revelation the last book of the bible", "paste-last-book.txt", "AI Overview", "explore the different ways people interpret the symbols in Revelation?", P,
    "'WHY IS REVELATION THE LAST BOOK OF THE BIBLE' — CORRECTION FIRST: THE OVERVIEW MARKS THE ORDER AS EDITORIAL (#1420'S POINT) AND KEEPS THE LATE DATE ON IRENAEUS'S GROUND; THE OTHER DETERMINANT OF THE LAST PLACE, HESITATION, IS ABSENT",
    POS_SHORT + "Correction: of the two determinants #1420 names for the book's last place, design and hesitation, the Overview gives design only; and it dates the book 'around 95 AD' in the same breath. "
    "'WHY IS REVELATION THE LAST BOOK OF THE BIBLE', SIGNED OUT, 2026-11-05: '" + P["open"] + "' Thematic culmination, Genesis mirrored, the end times; 'A Common Misconception': other texts likely written later; the warning of chapter 22 applies to its own scroll. Five chips.",
    POS + " The correction: the composition marks the order as an editorial decision, as #1420 does ('" + A["eschat"][1] + "'), and leaves out #1420's second determinant, the book's contested standing (the end of the codex as 'the seat nearest the door'). It then dates the book about 95 on other ground. "
    "The innocent reading follows. Asked why the book stands last, the Overview answers correctly that the place is thematic and corrects the belief that the book was written last.",
    [POS + " THE CORRECTION: the order is marked as design ('" + P["open"] + "'), and the standing that #1420 gives as the second sufficient cause of the last place (canonical hesitation) is absent. The date stays late: '" + P["95"] + "'.",
     "THE FIRST STEP OF THE CHAIN REFUSED. On Secondary Source's chain (order → standing → derivation of the text → derivation of the figure) the composition breaks the first link: order is not read as date. The late date is kept on its own ground, unnamed (Irenaeus).",
     "LATER TEXTS NAMED. '" + P["later"] + "' The composition makes the Johannine writings later than the Apocalypse; the composition at 'word of god revelation 19:13 and logos in john 1' (same date) gives John 1 as the origin of the figure. The two stand side by side unreconciled.",
     "THE SEAL AS ITS OWN. '" + P["canon"] + "' Accurate, and a point #1420 makes from the other side: the last page's curse reads as a colophon for the whole canon only because of where the book was placed.",
     "AGAINST THE PREDICTION. Placed last: given as design, with the date separated from it; the prediction expected the date to be read off the order and here it is not. Standing: not addressed. Date late: borne out. The figure: not addressed.",
     "SMALLEST REPAIR. 'Revelation stands last for its theme, and also because its acceptance was contested longest. Its date is a separate question: most scholars place it about 95 on Irenaeus's testimony; a minority places it in the 60s; Revelation First (#1735) argues forms of priority for it.' COUNTERTEST: 'was revelation almost left out of the bible'."],
    "The editorial character of the order composed correctly, at the grain of a church-history answer; the late date kept beside it on unnamed ground; standing absent.",
    [("Church News", " (+1)", "source chip after the opening; one further source"), ("Wikipedia", " (+1)", "source chip after thematic culmination"), ("Quora", " (+1)", "source chip after Genesis mirrored"), ("Billy Graham Evangelistic Association", " (+2)", "source chip after the end times"), ("YouTube · Saints Unscripted", " (+1)", "source chip after the misconception")],
    PV0, PN0, [1420, 1735])

# 7 ------------------------------------------------------------ why was revelation not read in the eastern church
P = {"lect": "it is not included in the official lectionary",
     "chil": "In the early East, the book was heavily tied to chiliasm",
     "fixed": "the lectionary cycle was largely fixed and solidified in the Christian East before Revelation achieved universal acceptance and integration into the Eastern canon.",
     "never": "Though it is never read aloud during the Divine Liturgy"}
cap("revelation-not-read-eastern-church-aio-20261105", "why was revelation not read in the eastern church", "paste-eastern-church.txt", "AI Overview", "viewed the book.", P,
    "'WHY WAS REVELATION NOT READ IN THE EASTERN CHURCH' — CORRECTION FIRST: THE OVERVIEW GIVES THE LECTIONARY'S SILENCE ITS REASONS AND OMITS THE WEST, WHERE TOLEDO IV (633) PRESCRIBED THE BOOK'S READING; CHILIASM ANSWERED BY STANDING",
    POS_SHORT + "Correction: the Overview treats the East's silence as the book's liturgical fate and omits the West's counter-practice (the Fourth Council of Toledo, 633, canon 17, prescribing its reading from Easter to Pentecost; to be read in a seated text). "
    "'WHY WAS REVELATION NOT READ IN THE EASTERN CHURCH', SIGNED OUT, 2026-11-05: canonical in the Orthodox Church but '" + P["lect"] + "'; reasons: misinterpretation, chiliasm, unsuitability for worship, and a lectionary fixed before the book's acceptance; its imagery in iconography and hymnography. Two chips.",
    POS + " The correction: the lectionary is a mechanism of order and hearing (#1420: the book '" + A["lect"][1] + "'), and the composition does not set the Western counter-practice beside it. "
    "The innocent reading follows. Asked why the East did not read the book, the Overview gives the canon-and-lectionary distinction correctly and the reasons the tradition itself gives, and notes the book's presence in iconography and hymnography.",
    [POS + " THE CORRECTION: '" + P["never"] + "' is a fact of one liturgical order; the Western counter-witness is absent (Toledo IV, canon 17, to be read in a seated text before Secondary Source uses it).",
     "STANDING SET BY HEARING. '" + P["fixed"] + "' The composition's strongest reason is mechanical: the order of readings was fixed while the book's standing was in question, and a standing of 'disputed' became a liturgical absence that outlasted the dispute. Secondary Source, stratum 3.5.",
     "A READING ANSWERED BY STANDING. '" + P["chil"] + "' The book's use by a reading (the millennium) is given as a reason for its liturgical absence: Secondary Source, stratum 3.3.",
     "AGAINST THE PREDICTION. Standing disputed or late-won: borne out ('before Revelation achieved universal acceptance'). Placed last, date, figure: not addressed.",
     "SMALLEST REPAIR. 'Revelation has no place in the Byzantine lectionary, which was largely fixed while the book's acceptance in the East was still contested; in the West it was read in the liturgy, and the Fourth Council of Toledo (633) required its reading from Easter to Pentecost.' COUNTERTEST: 'council of toledo 633 apocalypse reading'."],
    "The tradition's own account composed at the grain of an Orthodox blog: accurate on canon and lectionary, with the West's counter-practice absent.",
    [("Reddit · r/OrthodoxChristianity", " (+1)", "source chip after the opening; one further source"), ("Ancient Faith Blogs", "", "source chip after chiliasm")],
    PV0, PN0, [1420, 1735])

# 8 ------------------------------------------------------------ is the logos in revelation a literary figure
P = {"open": "is not merely an abstract literary or rhetorical figure of speech, but a personified divine figure identified as Jesus Christ.",
     "same": "This figure is the same divine, preexistent person introduced in the Gospel of John (John 1:1) and the First Epistle of John (1 John 1:1), who becomes incarnate.",
     "device": "Far from being a dry philosophical concept or literary device",
     "real": "the Logos functions as a real, acting protagonist/person",
     "ezra": "Revelation 22:7, 9, 10, 18, 19 clearly uses logos to describe the written book of Revelation."}
cap("logos-in-revelation-literary-figure-aio-20261105", "is the logos in revelation a literary figure", "paste-literary-figure.txt", "AI Overview", "The Old Testament background behind the \"Word of God\" imagery", P,
    "'IS THE LOGOS IN REVELATION A LITERARY FIGURE' — CORRECTION FIRST: THE ARCHIVE'S QUESTION (A FIGURE MADE IN LITERATURE BEFORE A HISTORICAL PERSON) READ AS 'FIGURE OF SPEECH' AND DENIED; THE FIGURE IDENTIFIED FROM JOHN 1:1; THE BOOK'S OWN λόγοι, ITS WRITTEN WORDS, LEFT IN THE ORGANIC RESULTS",
    POS_SHORT + "Correction: the question is whether the Logos of the Apocalypse is a figure first made in literature; the Overview hears 'figure of speech' and answers that question. "
    "'IS THE LOGOS IN REVELATION A LITERARY FIGURE', SIGNED OUT, 2026-11-05: 'In the Book of Revelation, the Logos (rendered in English as \"the Word of God\") " + P["open"] + "' Rev 19:13 quoted; '" + P["same"] + "' Literary versus theological context. Five chips.",
    POS + " The correction: the archive's reading (Rung VI; the operator's '" + STAKE + "') is a claim about where the figure was first made. The composition takes 'literary figure' as 'figure of speech', denies that, and identifies the figure by John 1:1. "
    "The innocent reading follows. Asked a question with two senses, the Overview answers the commoner one: the Logos of 19:13 is a person in the narrative, the divine Christ of the tradition, set in symbolic imagery.",
    [POS + " THE CORRECTION: '" + P["open"] + "' The negation answers a question about rhetoric; the question put is about origin, and on the archive's reading a figure made first in literature is real as a living Word (Rung VI: 'This is not a negation').",
     "THE FIGURE IDENTIFIED BY THE GOSPEL. '" + P["same"] + "' The Apocalypse's Logos is identified through John 1:1 and 1 John 1:1; the frozen prediction expected the figure read off John 1: borne out.",
     "PERSON AND DEVICE AS THE ONLY TWO TERMS. '" + P["device"] + "' and '" + P["real"] + "' The composition offers a historical-divine person or a rhetorical device; a literary person who is real, the archive's third term, is outside its frame.",
     "THE BOOK'S OWN λόγοι, NOT COMPOSED. An organic result under the Overview (Ezra Project): '" + P["ezra"] + "' The Apocalypse calls its own written words οἱ λόγοι (22:7, 9, 10, 18, 19), the words of the book's prophecy, beside the rider named ὁ Λόγος τοῦ Θεοῦ. The composition leaves this out.",
     "AGAINST THE PREDICTION. The figure read as derived from John 1, the step unargued: borne out. Order, standing, date: not addressed.",
     "SMALLEST REPAIR. 'Within Revelation the Logos is a person of the vision, named the Word of God (19:13), and the book calls its own written words λόγοι (22:7–19). Tradition identifies the figure with the Logos of John 1; Revelation First reads the figure as first made in the Apocalypse's literature (#1735; revelationfirst.com, Rung VI).' COUNTERTEST: 'revelation logos written word 22:18'."],
    "A two-sense question composed in its commoner sense and answered with the tradition's identification; the archive's sense, origin in literature, falls outside the composition's two terms.",
    [("Wikipedia", " (+1)", "source chip after the opening; one further source"), ("Britannica", " (+1)", "source chip after identity; one further source"), ("Wikipedia", "", "source chip after the role in the text"), ("EBSCO", " (+1)", "source chip after apocalyptic symbolism; one further source"), ("Logos Bible Study Platform", " (+1)", "source chip after personification; one further source")],
    PV0, PN0, [1735, 1420, 202, 407])

# 9 ------------------------------------------------------------ muratorian fragment paul following the order of his predecessor john
P = {"open": "The Muratorian Fragment notes that the apostle Paul wrote letters to seven churches, intentionally following the pattern or order of his \"predecessor\" John, who wrote to seven churches in the Book of Revelation.",
     "cath": "to symbolize a universal, catholic (global) reach to the church as a whole, mirroring John writing to seven churches in the Apocalypse.",
     "logic": "Rather than chronological or size-based ordering found later, the 2nd-century writer connects Paul’s epistolary corpus to John’s prophetic letters in Revelation to emphasize a symbolic completion of the number seven.",
     "reddit": "In what sense is John of Patmos a predecessor of Paul?"}
cap("muratorian-fragment-paul-predecessor-john-aio-20261105", "muratorian fragment paul following the order of his predecessor john", "paste-muratorian.txt", "AI Overview\n", "or how the fragment handles rejected letters like Laodiceans?", P,
    "'MURATORIAN FRAGMENT PAUL FOLLOWING THE ORDER OF HIS PREDECESSOR JOHN' — CORRECTION FIRST: THE CONSTRUAL REPORTED WHOLE, JOHN THE PREDECESSOR, PAUL'S SEVEN FOLLOWING; ITS DIRECTION READ AS SYMBOL ONLY; THE FRAGMENT'S DISPUTED DATE GIVEN AS SECOND-CENTURY; THE PREDICTION NOT BORNE OUT HERE",
    POS_SHORT + "Correction: #1735 §IV.3 reads the sentence as 'direct evidence for an ancient construal of corpus priority' on either dating of the fragment; the Overview reports the construal and reads it as symbolism of seven only, and gives the disputed date as settled. "
    "'MURATORIAN FRAGMENT PAUL FOLLOWING THE ORDER OF HIS PREDECESSOR JOHN', SIGNED OUT, 2026-11-05: '" + P["open"] + "' The seven-church pattern 'to symbolize a universal, catholic (global) reach'; the seven named; '" + P["logic"] + "' Three chips.",
    POS + " The correction: the composition reports the construal correctly and then confines its sense to symbolism, which #1735 §IV.3 weighs as the canonological alternative and answers ('construal of architecture, not shelf-position'); and it calls the fragmentist '2nd-century', where the date is disputed (#1735: '" + A["murat_dates"][1] + "'). "
    "The innocent reading follows. Asked the fragment's own phrase, the Overview reports what the fragment says, with the seven churches and the purpose the fragment gives (the universal church), drawn from two video sources.",
    [POS + " THE CORRECTION: '" + P["open"] + "' The construal is reported whole, with 'predecessor' in quotation marks. #1735 §IV.3 reads it as '" + A["murat"][1] + "'; the composition reads it as symbol: '" + P["cath"] + "'",
     "THE FRAGMENT'S DATE AS SETTLED. '" + P["logic"] + "' The second-century date is the traditional one; Hahneman's fourth-century dating is not mentioned. #1735: '" + A["murat_dates"][1] + "'. On either date the construal stands as a reading of the canon's formative period.",
     "THE PREDICTION NOT BORNE OUT AT THIS ADDRESS. The frozen prediction said a composition here would report the list and leave out the construal, or report it as the fragment's error. The composition reports the construal, with John as Paul's predecessor and Paul's seven as following John's, and does not call it an error. Recorded as a failure of the prediction at this address; the composition's reading of its sense (symbol, catholicity) is recorded beside it.",
     "THE QUESTION LEFT IN THE ORGANIC RESULTS. A thread under the Overview asks '" + P["reddit"] + "' The composition does not take it up.",
     "SMALLEST REPAIR. 'The fragment (late second century on the traditional dating, fourth on Hahneman's) says Paul, following the order of his predecessor John, wrote by name to seven churches. It reads Paul's seven through John's: a construal of corpus priority (Revelation First, #1735 §IV.3), whatever its value for the dates of the letters.' COUNTERTEST: 'in what sense is john a predecessor of paul muratorian'."],
    "An ancient witness composed accurately at the grain of its own sentence, the construal of priority intact; its sense narrowed to symbolism and its date settled.",
    [("YouTube · C. J. Cornthwaite", " (+1)", "source chip after the opening; one further source"), ("YouTube · Rev Dr Paul Blackham", " (+1)", "source chip after the seven-churches pattern; one further source"), ("YouTube · C. J. Cornthwaite", "", "source chip after the chronological/canonical logic")],
    PV0, PN0, [1735, 1420])

# 10 ----------------------------------------------------------- luther preface to revelation 1522
P = {"anti": "placing it among the disputed antilegomena at the back of his New Testament.",
     "christ": "complained that it failed to clearly teach Christ",
     "spirit": "admitting that his own spirit could not accommodate itself to the text.",
     "later": "Luther's view softened in later editions, such as his 1530 and 1534 revisions, where he reinterpreted the book more favorably as a symbolic depiction of the church's spiritual struggle."}
cap("luther-preface-revelation-1522-aio-20261105", "luther preface to revelation 1522", "paste-luther-1522.txt", "AI Overview\n", "Bible Research +4", P,
    "'LUTHER PREFACE TO REVELATION 1522' — CORRECTION FIRST: THE STANDING OF THE BOOK MEASURED BY A CHRIST TAKEN FROM OUTSIDE IT ('FAILED TO CLEARLY TEACH CHRIST'); THE BACK OF THE SEPTEMBER TESTAMENT AS THE PLACE OF THAT STANDING; THE 1534 'REVISION' UNCHECKED",
    POS_SHORT + "Correction: the preface's measure, whether the book teaches Christ, takes the measure of Christ from the gospels and Paul; that is the figure deciding the book's standing (Secondary Source, stratum 3.6). Luther's wording enters the study only from WA Deutsche Bibel 7. "
    "'LUTHER PREFACE TO REVELATION 1522', SIGNED OUT, 2026-11-05: in 1522 Luther placed the book 'among the disputed antilegomena at the back of his New Testament', doubted its apostolic or prophetic origin, '" + P["christ"] + "', and his spirit 'could not accommodate itself to the text'; softened in 1530 and '1534 revisions'. One chip, Bible Research (+4).",
    POS + " The correction: the composition reports a judgment of standing made by a measure of the figure (whether the book teaches Christ), and the place that standing took in print (the back of the Testament). Both are the operations Secondary Source tracks; neither is the book's own. "
    "The innocent reading follows. Asked for the preface, the Overview summarizes it as the commonly cited English translations do: doubt in 1522, a different reading in 1530.",
    [POS + " THE CORRECTION: '" + P["christ"] + "' The standard the book is held to is a Christ known from elsewhere; on Secondary Source's counts (design v0.3 §2) the derivation of the figure decides the standing. Luther's German is to be read in WA Deutsche Bibel 7 before any wording enters the study.",
     "STANDING AS PLACE. '" + P["anti"] + "' The September Testament placed Hebrews, James, Jude and the Apocalypse at the end of its table without numbers (to be read in a seated copy); the composition joins the place to the judgment.",
     "THE SPIRIT'S REFUSAL AS EVIDENCE. '" + P["spirit"] + "' The composition reports a reader's response as a ground of standing; Secondary Source records it as the preface's own operation, with no reading of motive.",
     "THE LATER EDITIONS. '" + P["later"] + "' The 1530 preface is the replacement Secondary Source names (stratum 3.6); '1534' is the year of the complete Bible, and whether its preface differs from 1530 is not checked here.",
     "AGAINST THE PREDICTION. Placed last: borne out ('at the back'). Standing disputed: borne out ('disputed antilegomena'). The figure deciding the standing: borne out, as the measure ('failed to clearly teach Christ'). Date: not addressed.",
     "SMALLEST REPAIR. 'In 1522 Luther set Hebrews, James, Jude and Revelation at the end of his New Testament without numbers, and judged Revelation by whether it taught Christ as he found Christ taught in the gospels and Paul; in 1530 he wrote a new preface reading it as a history of the church.' COUNTERTEST: 'september testament 1522 table of books unnumbered'."],
    "A Reformation locus composed accurately at the grain of the English translations in circulation; the measure it reports, a Christ known from elsewhere deciding the book's standing, is Secondary Source's object.",
    [("Bible Research", " (+4)", "source chip after the composition; four further sources")],
    {"author": True, "inst": False, "id": False, "src": True},
    "Luther named (the subject of the query); no edition, translation or identifier named; one chip. The archive's position is absent; that loss is the finding, recorded first.",
    [1420, 1735])

assert len(C) == 10 and len({e["slug"] for e in C}) == 10
for e in C:
    json.dump(e, open(H / (e["slug"] + ".json"), "w"), ensure_ascii=False, indent=1); print("wrote", e["slug"], len(e["transcript"]))
