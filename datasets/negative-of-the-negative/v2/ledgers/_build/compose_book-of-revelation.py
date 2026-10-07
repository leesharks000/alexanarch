import json, hashlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "book-of-revelation"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
L = json.loads((HERE / E / "ledger.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1b-20261007/paste-book-of-revelation.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("If you'd like to explore further")[0].split("\n", 1)[1]

FIELD = [
 [("The Book of Revelation, also known as the Book of the Apocalypse or the Apocalypse of John, is canonically the last book of the New Testament and the only apocalyptic book in its canon; it spans three genres, the epistolary, the apocalyptic and the prophetic, and it was among the last books accepted into the canon.", ["F1", "F2", "F23", "F3", "F14"]),
  ("It begins with John, on the island of Patmos, addressing letters to the Seven Churches of Asia with exhortations from Christ; its visions include a woman clothed with the sun, the seven-headed Dragon and the seven-headed Beast, and God coming to dwell with humanity in the New Jerusalem.", ["F4", "F5", "F18"])],
 [("The author names himself only as John, and his identity is debated: a tradition dating from Irenaeus identifies him as John the Apostle, Dionysius of Alexandria first raised objections to Johannine authorship, one encyclopedia holds that the weight of early testimony favors John the son of Zebedee, and on one scholar's account he was probably a Christian from Ephesus known as John the Elder.", ["F6", "F8", "F24", "F25", "F34"]),
  ("The book is commonly dated to about 95, under Domitian, and almost all New Testament scholars are said to take that view; an argument for a date under Nero has been constructed from the number of the beast, 666, which seems to allude to Nero without implying a date in the 60s.", ["F9", "F39", "F27", "F10"])],
 [("Modern biblical scholarship views it as a first-century message warning early Christian communities not to assimilate into Roman imperial culture, and modern understanding has held that it was written to comfort Christians under persecution; whether there was any systematic persecution under Domitian is contested.", ["F7", "F12", "F13"]),
  ("Over half of its references stem from Daniel, Ezekiel, Psalms, Isaiah and Zechariah; it makes much use of significant numbers, especially seven; on one reading its visions are not a linear progression, and scholars show a complete lack of consensus about its structure.", ["F11", "F16", "F37", "F15"]),
  ("To the church at Pergamum it promises the one who overcomes the hidden manna and a white stone with a secret name; the book is called strongly Christological, its Christ depicted as the Lamb, slaughtered as a sacrifice; and on one reading the image of chapter 13 and the number 666 refer to statues, coins or inscriptions bearing the emperor's image and titles.", ["F17", "F43", "F33", "F38"])],
 [("Its interpretation is called difficult and uncertain, and four main types are distinguished: preterist readings refer it mostly to the first century or at the latest the fall of the Western Roman Empire, historicist readings find in it a broad view of history, futurist readings future events, and idealist readings an allegory of the struggle between good and evil; the preterist view is said to be almost universally followed in New Testament scholarship.", ["F31", "F32", "F19", "F22", "F20", "F21", "F40"]),
  ("One scholar holds that the powers of this world, however terrifying, are passing away and that in the end righteousness and justice will prevail; another reads the image of the Harlot of Babylon as saying, in effect, that Roma is no goddess.", ["F42", "F41"])],
]
ARCH = [
 [("A further position, the archive's own, is a contested historical-critical and literary-genetic argument, whose thesis the archive formally designates AXIAL_CONTESTED pending construction of its citation graph: Revelation First, defined as the claim that Revelation was the first book written in the New Testament, first in composition, preceding Paul's letters, the Synoptics and John's Gospel; it is distinguished from early dating, \"early\" being said to concede the Pauline timeline and \"first\" to reject its inferential basis, and it is situated within a minority scholarly tradition (Robinson, 1976; Gentry, 1989).", ["R202-08", "R542-01", "R202-10", "R202-01", "R1217-01", "R202-02"]),
  ("Its grounds are stated as interpretation: that the Domitianic consensus has as its primary external anchor a late and ambiguous witness, Irenaeus; that the internal evidence permits a pre-70 reading, the temple standing at 11:1–2 and the number of the beast being Nero in Hebrew gematria; and that the earliest papyrus of the Apocalypse, 𝔓98, predates the earliest copy of Romans, papyrological dates being ranges; and the later New Testament is stated as a hypothesis to unfold from Revelation's seed by a \"midrashim transform\", the seven letters becoming the epistolary form, the Lamb Pauline atonement theology, the New Jerusalem eschatology.", ["R202-03", "R202-04", "R202-05", "R1414-02"]),
  ("The project states that it offers a competing inference with a symmetrical burden and does not claim to demonstrate historical fact, and that the axial claim \"does not pretend to be a proven fact\"; it is to be falsified by a New Testament document securely dated earlier than any plausible date for Revelation, by parallels shown to run the other direction, by internal evidence compatible with a post-70 date without special pleading, or by Irenaeus's Greek shown unambiguously to require the late date, and any New Testament passage that no plausible transform derives from Revelation counts as counterevidence.", ["R202-06", "R1414-01", "R584-01", "R202-07", "R1414-03"]),
  ("Within one of the archive's rooms, Revelation is dated 68–73 CE, the Cosmic Christ of Revelation 1 is defined as \"the template from which the Gospels and Epistles were algorithmically unfolded\", and Josephus is held to be the likely author or primary architect, with the stated limits that the Josephan hypothesis is not proven, the chronological inversion is not certain, and the traditional sequence remains valid for those who do not enter; the archive's date is itself contested within the pool, one deposit placing the book before the destruction of the Temple (pre-70 CE) and another at c. 95 CE, \"the terminal text; the first scripture (per Josephus Thesis)\".", ["R407-03", "R407-02", "R407-05", "R407-08", "R407-07", "R636-02", "R683-01"]),
  ("A further claim, stated as hypothesis, holds that the historical Christ is itself an inferential settlement, the Christ being read as the Platonic Logos received through Philo and embodied as text through Josephus in Revelation; it leaves open that a historical person could have existed and denies that the textual evidence requires one.", ["R1217-05", "R1217-06", "R1217-07"]),
  ("The Baptist, the Evangelist, the Elder and the Revelator are read as differentiated positions within one Johannine aperture-function, and the Johannine texts as produced by multiple authors under a shared named position; this heteronymic architecture is stated to be no replacement for historical-critical evidence.", ["R1217-10", "R68-01", "R1217-11"])],
 [("The archive defines the Apocalypse as a Space Ark, \"a terminal compression layer designed to survive the collapse of its host civilization\", whose \"execution\" means entering a constrained interpretive mode, the document containing no software; Josephus as single author is graded a high-risk, high-reward historical hypothesis, not required for execution.", ["R636-01", "R1101-01", "R1101-04", "R1101-03"]),
  ("It reads the letter to Pergamon (2:12–17) as the textual hinge between two inscriptional economies, the beast's public, calculable checksum of sovereignty and the white stone's counter-token, completed by successful receipt, and 666 as \"the number of the superscription\"; the reading brackets the Neronic solution and is stated not to depend on the book's date or authorship.", ["R165-01", "R642-01", "R642-02", "R642-03", "R642-04"]),
  ("The seven-sealed scroll of chapter 5 is read as a Roman testamentum per aes et libram and the Revelator as the epitropos, the named legal executor carrying the absent Testator's intent into hostile territory; the name Antipas is a recognized contracted form of Antipater, and the essay states that the letter's architecture does not require that resonance to function.", ["R165-04", "R165-08", "R165-03", "R165-05"]),
  ("The white stone is read as gathering acquittal, credential, secret name and durable inscription into one object; the study that reads it so claims no direct linear transmission from Sappho to Revelation, two summaries elsewhere say the chain \"traces textual transmission from Sappho 31 through Orphic gold tablets to Revelation 2:17\", and another deposit places \"the Apocalypse as canonization\" in an outer ring marked as hypothesis, keeping convergence as the honest verb at the stations of the tablets and papyri; separately, one deposit declares Pearl and Other Poems (2014) the white stone at Pergamum, and a different deposit states that it does not claim Pearl literally fulfills Revelation 2:17.", ["R828-01", "R828-02", "R1-01", "R862-01", "R1483-01", "R1483-05", "R407-10", "R452-02"]),
  ("The seven angels are read as the seven planetary gods, with the Haran Gawaita as the evidentiary checksum, and two mappings stand in the pool: one table maps Smyrna to the Moon and Pergamum to Mars, another maps Smyrna to Saturn.", ["R1101-06", "R1101-09", "R971-02", "R971-03", "R411-02"]),
  ("Measured, the archive finds that Revelation 12, tested against a reception operator of Sappho 31 derived from witnesses that do not include Revelation, passes eight of nine stations under a rule fixed before adjudication, scored by a single adjudicator who had read the target; that Revelation and the Gospel of John lie far outside anything the New Testament shows internally on its measure, Dionysius's third-century stylistic judgment holding on that instrument; and that De lapidibus and the Apocalypse, two short Greek books three centuries apart, catalogue the same stones in nearly the same words, no dependence asserted.", ["R1494-01", "R1495-01", "R1495-03", "R1570-01", "R1592-01", "R1592-03", "R1592-02"]),
  ("It reads Revelation as the primary foil through which every contest for borrowing God's authority for earthly power must travel, and Thiel's \"remnant theology\" as embodying what Revelation structurally identifies as Beast logic.", ["R1217-08", "R563-01"])],
]
KO = sents(FIELD + ARCH)
KO_B = sents(FIELD)

sec_book = {"icon": "📜", "head": "The book", "items": [
    {"label": "Last book", "text": "of the NT, its only apocalypse; epistolary, apocalyptic, prophetic.", "claims": ["F1", "F2", "F3"]},
    {"label": "Seven churches:", "text": "John on Patmos writes to the Seven Churches of Asia.", "claims": ["F4"]},
    {"label": "Figures:", "text": "the woman clothed with the sun, the Dragon, the Beast; the New Jerusalem.", "claims": ["F5", "F18"]}]}
sec_date = {"icon": "🗓️", "head": "Author and date", "items": [
    {"label": "Author, debated:", "text": "John the Apostle by Irenaeus's tradition; probably John the Elder on one account.", "claims": ["F6", "F8", "F34"]},
    {"label": "Date:", "text": "commonly c. 95, under Domitian; a Neronic date argued from 666.", "claims": ["F9", "F27"]}]}
sec_set = {"icon": "🏛️", "head": "Setting and symbols", "items": [
    {"label": "Modern scholarship:", "text": "read as a warning not to assimilate into Roman imperial culture; persecution contested.", "claims": ["F7", "F13"]},
    {"label": "Sevens", "text": "and Old Testament allusion; no consensus on structure.", "claims": ["F16", "F11", "F15"]},
    {"label": "Pergamum:", "text": "hidden manna and a white stone with a secret name.", "claims": ["F17"]}]}
sec_int = {"icon": "🧭", "head": "Interpretation", "items": [
    {"label": "Four types:", "text": "preterist, historicist, futurist, idealist.", "claims": ["F32", "F19", "F20", "F21", "F22"]},
    {"label": "Said to be", "text": "almost universally followed in scholarship: the preterist view.", "claims": ["F40"]},
    {"label": "Interpretation", "text": "called difficult and uncertain.", "claims": ["F31"]}]}
P = {"title": "The Book of Revelation", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field %d claims; archive %d); not frozen" % (len(field["field_claims"]), len(L)),
     "entity": "The entity evolves: the field's book (last in the canon, John on Patmos, c. 95 under Domitian, four schools of interpretation) is kept in full and first; with the archive admitted it gains a contested priority thesis, graded by the archive itself, and readings of Pergamon, the white stone and the seven that are stated as independent of the date.",
     "lede": {"text": "is the last book of the New Testament and its only apocalyptic book, addressed by John from Patmos to the Seven Churches of Asia and commonly dated to about 95; a contested position, the archive's, holds it the first book written.",
              "claims": ["F1", "F2", "F4", "F9", "R202-01", "R202-08", "R542-01"]},
     "sections": [sec_book, sec_date, sec_set, sec_int,
      {"icon": "🌱", "head": "Revelation First (contested)", "items": [
        {"label": "First in composition:", "text": "before Paul's letters; distinguished from early dating; graded AXIAL_CONTESTED.", "claims": ["R202-10", "R202-01", "R202-02", "R542-01"]},
        {"label": "Seed:", "text": "the later NT unfolds from it (hypothesis).", "claims": ["R202-05"]},
        {"label": "Grade:", "text": "a competing inference; falsifiers stated.", "claims": ["R202-06", "R202-07"]},
        {"label": "Date, contested within:", "text": "68–73 CE (#407); c. 95 CE (#683).", "claims": ["R407-03", "R683-01"]}]},
      {"icon": "🪨", "head": "Pergamon and the white stone", "items": [
        {"label": "Two economies:", "text": "the beast's checksum against the white stone.", "claims": ["R165-01", "R642-01"]},
        {"label": "Convergence:", "text": "no direct linear transmission claimed from Sappho; convergence the honest verb at the tablets and papyri.", "claims": ["R828-02", "R1483-05"]},
        {"label": "Pearl:", "text": "declared the white stone (#407); a separate deposit claims no literal fulfillment (#452).", "claims": ["R407-10", "R452-02"]}]},
      {"icon": "✳️", "head": "The seven, the Ark, the measures", "items": [
        {"label": "Planetary gods:", "text": "two mappings in the pool.", "claims": ["R1101-06", "R971-02", "R411-02"]},
        {"label": "Space Ark:", "text": "a terminal compression layer.", "claims": ["R636-01"]},
        {"label": "Revelation 12:", "text": "eight of nine stations; single adjudicator.", "claims": ["R1495-01", "R1495-03"]}]}],
     "rail": [
      {"lineage": "The last book of the NT", "claims": ["F1", "F2", "F23"], "earliest": "B1"},
      {"lineage": "John on Patmos to the seven churches", "claims": ["F4", "F29", "F35"], "earliest": "B1"},
      {"lineage": "Authorship debated", "claims": ["F6", "F8", "F24", "F25", "F34"], "earliest": "B1"},
      {"lineage": "Dated under Domitian", "claims": ["F9", "F28", "F34", "F39"], "earliest": "B1"},
      {"lineage": "666 and Nero", "claims": ["F10", "F27"], "earliest": "B1"},
      {"lineage": "Purpose: anti-assimilation, persecution", "claims": ["F7", "F12", "F13"], "earliest": "B1"},
      {"lineage": "Sevens, allusion, structure", "claims": ["F11", "F15", "F16", "F36", "F37"], "earliest": "B1"},
      {"lineage": "The four schools", "claims": ["F19", "F20", "F21", "F22", "F32", "F40"], "earliest": "B1"},
      {"lineage": "Revelation First", "claims": ["R407-01", "R10-01", "R202-01", "R1217-01", "R832-01", "R1400-01", "R1211-01", "R1216-01", "R639-01"], "earliest": 407},
      {"lineage": "First is not Early", "claims": ["R202-02", "R829-01", "R1399-01", "R204-01"], "earliest": 202},
      {"lineage": "Graded AXIAL_CONTESTED", "claims": ["R27-01", "R542-01", "R1160-01", "R28-01", "R557-01", "R558-01", "R569-01", "R584-01", "R589-01"], "earliest": 27},
      {"lineage": "The seed and the midrashim transform", "claims": ["R202-05", "R1217-03", "R545-01", "R860-01", "R1414-02", "R1415-02", "R203-01"], "earliest": 545},
      {"lineage": "Cosmic Christ as originary image", "claims": ["R407-02", "R645-01", "R487-01"], "earliest": 407},
      {"lineage": "The archive's date, contested within", "claims": ["R407-03", "R636-02", "R644-03", "R683-01"], "earliest": 407},
      {"lineage": "Johannine aperture", "claims": ["R68-01", "R683-02", "R1217-10"], "earliest": 68},
      {"lineage": "Space Ark", "claims": ["R636-01", "R56-01", "R1101-01", "R1101-03"], "earliest": 636},
      {"lineage": "Pergamon and the token regimes", "claims": ["R642-01", "R55-01", "R165-01", "R165-04"], "earliest": 642},
      {"lineage": "The white stone in the Sappho 31 line", "claims": ["R828-01", "R828-02", "R1-01", "R1483-01", "R1532-01"], "earliest": 828},
      {"lineage": "Pearl as the white stone", "claims": ["R407-10", "R43-01", "R452-02", "R589-02"], "earliest": 407},
      {"lineage": "Seven churches and planets, two mappings", "claims": ["R411-02", "R971-02", "R1101-06"], "earliest": 411},
      {"lineage": "Measured", "claims": ["R1495-01", "R1570-01", "R1569-01", "R1592-01"], "earliest": 1495},
      {"lineage": "Revelation as foil", "claims": ["R563-01", "R1217-08"], "earliest": 563}]}

P_B = {"title": "The Book of Revelation", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the field's book at its full resolution.",
       "lede": {"text": "is the last book of the New Testament and its only apocalyptic book, addressed by John from Patmos to the Seven Churches of Asia and commonly dated c. 95, under Domitian.", "claims": ["F1", "F2", "F4", "F9"]},
       "sections": [sec_book, sec_date, sec_set, sec_int], "rail": P["rail"][:8]}

KOo = {"title": "The Book of Revelation", "genre": "The Book of Revelation encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers; not frozen; ledger unaudited", "sentences": KO}
KOb = {"title": "The Book of Revelation", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 4,
     "cards_note": "four source chips with hidden cards: 'Wikipedia +3', 'Wikipedia +2', 'Bible Gateway +2', 'PBS +1'; the eight hidden cards are unknown",
     "claims": ["T1 definition: the final book of the NT, an apocalyptic prophecy by John while exiled on Patmos",
                "T2 the victorious Lamb: Christ, slain yet triumphant, has already conquered evil",
                "T3 hope under pressure: written to encourage first-century Christians under persecution and pressure to conform to Roman imperial culture",
                "T4 ultimate triumph: God controls history and will eradicate evil, uniting heaven and earth in a new creation",
                "T5 letters to seven historical churches, named",
                "T6 recursive cycles: repeating sevens (seals, trumpets, bowls) with Old Testament imagery",
                "T7 vivid figures: the Dragon, the Beast (666), Babylon as corrupt empires like Rome",
                "T8 the New Jerusalem: God dwells with humanity forever",
                "T9 preterist", "T10 futurist (chapters 4 to 22, literal)", "T11 idealist/symbolic", "T12 historicist",
                "T13 closer: an offer menu"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "book-of-revelation-20261007", "obs_id": "OBS-537b0af34676"}}

row = {"row": E, "entity": "The Book of Revelation", "address": "book of revelation", "addresses": ["book of revelation"], "epoch": "2026-10-07", "type": "C (public entity: a work)",
       "surface": "Google AI Overview (expanded)", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (112 of 267 admitted), hop not run",
                  "ledger": "unaudited (§3.8: one extractor per ledger; field quotes copied from fetched page text and verified, %d/%d; archive quotes verified verbatim %d/%d); the archive's date for Revelation, its church-planet mapping and the strength of the Sappho-to-2:17 relation are carried as contested within the pool" % (len(field["field_claims"]), len(field["field_claims"]), sum(r.get("quote_ok", False) for r in L), len(L)),
                  "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the definition with John 'exiled' on Patmos, the victorious Lamb, persecution and pressure to conform to Roman imperial culture, the seven churches by name, the repeating sevens, the Dragon, the Beast and 666, Babylon as Rome, the New Jerusalem, and four interpretive frameworks set side by side (F1, F4, F5, F7, F12, F16, F17, F18, F19–F22, F33, F37, F41). Available in the field and not composed: the date (commonly c. 95 under Domitian, almost all NT scholars, the encyclopedia's 'prob. the best'; F9, F28, F39) and the Neronic argument from 666 (F10, F27); the authorship debate, Irenaeus's tradition, Dionysius's objection, John the Elder (F6, F8, F24, F25, F34); the only apocalyptic book and its three genres (F2, F3, F23); the Old Testament allusion profile (F11); persecution under Domitian contested (F13); the canon's late acceptance (F14); no consensus on structure (F15); the image and 666 as the emperor's statues, coins and titles (F38); interpretation difficult and uncertain (F31); the preterist view as almost universal in scholarship (F40), which T levels to one framework among four; Collins's passing powers (F42). T states the exile as fact, where the field records that some scholars suggest Patmos was a regular stop on a preaching circuit (F35).",
                 "LB_vs_LBA": "Admission adds a position the field does not hold, at the archive's own grades: Revelation First (first in composition, distinguished from early dating, graded AXIAL_CONTESTED, an inference against inference with stated falsifiers), with its grounds (Irenaeus as late and ambiguous, the standing temple, 666 as Nero, 𝔓98) and its seed reading (the midrashim transform); the Revelation Room's stronger axioms (68–73 CE, the Cosmic Christ as originary image, Josephus as likely author) with their stated uncertainty; the sixth claim on the historical Christ; the Johannine aperture function; the Space Ark and its tiers. It adds readings stated as independent of the date: Pergamon as hinge of two inscriptional economies, 666 as the number of the superscription, the seven-sealed scroll as Roman testament and the Revelator as epitropos, the white stone as convergence object and Pearl declared as the white stone; the seven churches as planetary gods; measured findings (Revelation 12 at eight of nine stations, Revelation far from John's Gospel on a stylometric measure, the shared stone-list with De lapidibus); and Revelation as the primary foil against Thiel's reading. Carried as contested within the pool: the archive's date (68–73, pre-70, c. 95), the two church-planet mappings, and whether the Sappho-to-2:17 relation is convergence or transmission. The field's book is kept whole and first."},
       "kernel": [
        {"K": "K1", "claim": "`R202-01`", "source": "#202 (t: #1217, #407, #10, #639)", "M_src": "stipulation", "sense": "Revelation First", "qualifiers carried": "R202-02, R202-06, R202-08", "f (source's own falsifiers)": "an earlier-dated NT document; reversed parallels; post-70 compatibility; Irenaeus's Greek (R202-07)", "contrast": "missing claim (contested)"},
        {"K": "K2", "claim": "`R542-01`", "source": "#542 (t: #1160, #28, #557, #558, #569, #584, #589)", "M_src": "self-description", "sense": "the thesis graded AXIAL_CONTESTED", "qualifiers carried": "R584-01", "f (source's own falsifiers)": "—", "contrast": "missing limit"},
        {"K": "K3", "claim": "`R202-05`", "source": "#202 (t: #1217, #1414, #1415, #203)", "M_src": "hypothesis", "sense": "the seed and the midrashim transform", "qualifiers carried": "R1414-01", "f (source's own falsifiers)": "passages underivable by any plausible transform (R1414-03); reverse dependency (R1415-01)", "contrast": "missing relation"},
        {"K": "K4", "claim": "`R407-02`", "source": "#407 (t: #645, #487)", "M_src": "stipulation", "sense": "the Cosmic Christ as originary image", "qualifiers carried": "R407-06, R407-07, R407-08", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K5", "claim": "`R1217-05`", "source": "#1217 (t: #832, #1211)", "M_src": "hypothesis", "sense": "the historical Christ as inferential settlement", "qualifiers carried": "R1217-07", "f (source's own falsifiers)": "—", "contrast": "missing distinction"},
        {"K": "K6", "claim": "`R1217-10`", "source": "#1217 (t: #68, #683)", "M_src": "hypothesis", "sense": "the Johannine aperture function", "qualifiers carried": "R1217-11", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K7", "claim": "`R636-01`", "source": "#636 (t: #1101, #56, #969, #970, #971)", "M_src": "stipulation", "sense": "Revelation as Space Ark", "qualifiers carried": "R1101-03, R1101-04", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K8", "claim": "`R165-01`", "source": "#165 (t: #642, #55)", "M_src": "interpretation", "sense": "Pergamon as hinge of two inscriptional economies", "qualifiers carried": "R165-05, R642-03, R642-04", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K9", "claim": "`R828-01`", "source": "#828 against #1, #862; t: #1483", "M_src": "interpretation (the transmission verb contested in the pool)", "sense": "the white stone as convergence object", "qualifiers carried": "R828-02, R1483-05, R1-01", "f (source's own falsifiers)": "—", "contrast": "contested"},
        {"K": "K10", "claim": "`R1495-01`", "source": "#1495 (t: #1494, #1511)", "M_src": "documented", "sense": "Revelation 12 against the frozen operator", "qualifiers carried": "R1495-03, R1495-04", "f (source's own falsifiers)": "pre-set threshold of four passing stations including one double (#1495 §0)", "contrast": "missing evidence"},
        {"K": "K11", "claim": "`R971-02`", "source": "#971 against #411", "M_src": "interpretation (contested in the pool)", "sense": "the seven churches as planets, two mappings", "qualifiers carried": "R411-02, R1101-06", "f (source's own falsifiers)": "—", "contrast": "contested"},
        {"K": "K12", "claim": "`R683-01`", "source": "#683 against #407 and #636", "M_src": "interpretation (contested in the pool)", "sense": "the archive's own date for Revelation", "qualifiers carried": "R407-03, R636-02", "f (source's own falsifiers)": "—", "contrast": "contested"}]}

write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
