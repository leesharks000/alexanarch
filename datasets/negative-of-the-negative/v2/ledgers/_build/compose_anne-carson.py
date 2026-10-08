import json, hashlib, sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "anne-carson"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
ledger = json.loads((HERE / E / "ledger.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1g-20261008/paste-anne-carson.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("\nFinance\n", 1)[1].split("\nAsk anything\n")[0]
body = "\n".join(l for l in body.splitlines() if l.strip() not in ("Wikipedia", "Poetry Foundation", "+4", "+1"))

FIELD_PARAS = [
 [("Anne Carson (born June 21, 1950) is a Canadian poet, essayist, translator, classicist and professor, and in 2026 she was awarded the Nobel Prize in Literature \"for her bold and inventive oeuvre that, in playful dialogue with the classical tradition, has created new forms for contemporary literature\" (Wikipedia).", ["F1", "F25", "F4"]),
  ("A high-school Latin instructor introduced her to Ancient Greek and tutored her privately, over the lunch hour on the Poetry Foundation's account; she left the University of Toronto twice before completing her BA (1974), MA (1975) and PhD (1981) there, and spent a year studying Greek metrics and textual criticism at the University of St Andrews.", ["F5", "F29", "F30", "F6"]),
  ("She has taught classics, comparative literature and creative writing since 1979, at McGill, the University of Michigan, New York University and Princeton among other universities.", ["F2"])],
 [("Her books blend poetry, essay, prose, criticism, translation, dramatic dialogue, fiction and non-fiction to varying degrees, a career the Poetry Foundation calls \"unclassifiable\", and she frequently references, modernises and translates Greek and Latin writers from Aeschylus and Sappho to Stesichorus and Thucydides.", ["F8", "F26", "F27", "F7"]),
  ("Eros the Bittersweet (1986), her first book and a reworking of her 1981 doctoral thesis, examines eros as pleasure and pain at once, after Sappho's word glukupikron, and considers how triangulations of desire appear in Sappho, the Greek novelists and Plato; on John D'Agata's account it stunned the classicists first, then the nonfiction community, and then the poets.", ["F9", "F10", "F11", "F12", "F31"]),
  ("Autobiography of Red (1998) takes its cue from Herakles' tenth labour, the slaying of the red-winged Geryon in Stesichoros; Adam Kirsch summarized the change as Herakles breaking Geryon's heart and judged the writing \"clearly prose\", and D'Agata frames the debate as how prosaic a poem can be before it becomes something else.", ["F32", "F33", "F34", "F35"]),
  ("The Beauty of the Husband: A Fictional Essay in 29 Tangos (2001), a verse novel of a marital breakup, won the T. S. Eliot Prize, and she was the first woman to win it; Decreation (2005) takes its title and impetus from Simone Weil; and Nox, made in 2000 and published in 2010, is an epitaph for her brother, designed and performed with her husband Robert Currie.", ["F36", "F13", "F37", "F23", "F24"]),
  ("She has translated ten Greek tragedies and the poetry of Sappho, the latter as If Not, Winter (2002); An Oresteia (2009) won the PEN Award for Poetry in Translation and drew mixed reviews for its liberties.", ["F19", "F21", "F20", "F38"])],
 [("Her honours include Guggenheim and MacArthur fellowships, the Lannan Literary Award, two Griffin Poetry Prizes (she was the first poet to win it and the first to win it twice), the Princess of Asturias Award, the PEN/Nabokov Award and appointment to the Order of Canada in 2005; the National Book Critics Circle shortlisted her three times, and Wrong Norma (2024) was longlisted for the National Book Award for Poetry.", ["F3", "F40", "F14", "F15", "F16"]),
  ("She had long been regarded as a likely Nobel candidate before the 2026 award, she is the subject of two edited volumes (2015 and 2021), and Daphne Merkin called her \"one of the great pasticheurs\".", ["F17", "F18", "F28"]),
  ("She is reticent about her private life and discourages autobiographical readings of her writing, and she has described herself as at heart a visual artist.", ["F22", "F39"])],
]

ARCHIVE_PARAS = [
 [("The archive's earliest bearing on her is a dedication: the operator's 2014 collection Paper Roses carries a section \"Blossomdeep: for Anne Carson\" that opens on Sappho 31, and the operator's 2013 dissertation, as the archive reports it, closes by pairing Carson's Nox with the heteronym Johannes Sigil's \"Snub-Poemed\" as works that extend the metatextual mode of reception.", ["W1636-01", "W921-01"]),
  ("The archive records that Carson received \"Snub-Poemed\" in 2013 and reads her reply as a reception trace that is no evidence for the poem's argument; it places her in an inherited literary lineage as an adjacent reference with no documented effective act, and names Nox among the genre models of the operator's book on Mary Lee.", ["W700-01", "W785-01", "W162-01"])],
 [("Its Sappho papers take her work as the standard reading they extend: the received reading of fragment 31 runs, in one paper's phrase, \"from Longinus to Carson\", and the archive's own reading starts from the difficulty that reading leaves in κῆνος, the man who appears in the first stanza and never returns.", ["W1270-01"]),
  ("It quotes the triangle of Eros the Bittersweet, lover, beloved and that which comes between them, and states its limit, \"Carson's analysis stops at the erotic\", since it does not follow the third position forward in time to a reader; another paper retains her phenomenology and formalizes the triangle as the first stage of its cascade, and a third says Carson establishes the continuity of Sapphic and Socratic eros, a connection it says it radicalizes.", ["W626-01", "W626-02", "W503-01", "W752-01", "W828-01"]),
  ("Of If Not, Winter it reads the visible lacunae as \"an aesthetic gesture toward the papyrological event\", the absence becoming part of the transmission, and sets Carson, who \"leaves the wound open\", beside a poet who fills the gaps; in its translation tables Carson preserves fragment 31's fragmentary syntax and its fifth-stanza opening, drawn like every modern edition from a single manuscript stemma.", ["W625-01", "W562-01", "W337-01", "W337-02", "W1054-01", "W1052-01"]),
  ("It cites her on Sappho's tense, which English has no form to render as \"completed and eternally available\", and counts her among the receptions a world without fragment 31 would lack.", ["W503-02", "W109-01"])],
 [("On the archive's reception record the popular circulation of fragment 147 is overwhelmingly in Carson's wording, and that is the register an AI Overview's generic-remembrance card composes from; a source audit of 28 September finds Goodreads' If Not, Winter page among a composition's sources, carrying papyrus and fragment 147 and no deixis.", ["W1548-01", "W1645-03"]),
  ("On 15 September a Google AI Overview organized its answer under \"Temporal projection\" and placed Carson inside it (\"whitespace and gaps force the reader to co-create the voice\"), with three cards, none from the archive, and the cited Aurelis page, read in session, carries none of the frame, Carson included.", ["W1615-01", "W1615-02", "W1645-01"]),
  ("The archive reads this as Carson reread through a frame aligned with its own framework, scores the row at the lexical, relational and procedural levels, and calls it productive abstraction with mechanism and provenance loss; it states that Carson herself does not make the future-reader argument.", ["W1615-03", "W1615-04", "W1645-02"]),
  ("It states as not established that the reading came from the archive, since an independently convergent frame could produce it, and says so in three deposits; it states that its reading fails if the operator turns up on negative controls; and the audits built on the case exclude any value belonging to Carson herself.", ["W1615-05", "W1620-02", "W1623-01", "W1615-06", "W1620-01", "W1623-02"])],
]

KO = sents(FIELD_PARAS + ARCHIVE_PARAS)
KO_B = sents(FIELD_PARAS)

sec_who = {"icon": "👤", "head": "Who she is", "items": [
    {"label": "Born:", "text": "Toronto, June 21, 1950; Greek from a high-school Latin teacher.", "claims": ["F1", "F5"]},
    {"label": "Trained:", "text": "BA, MA, PhD at Toronto (1974–1981); St Andrews.", "claims": ["F6"]},
    {"label": "Teaches:", "text": "classics, comparative literature, creative writing since 1979.", "claims": ["F2"]},
    {"label": "Form:", "text": "poetry, essay, criticism, translation, fiction blended.", "claims": ["F8"]}]}
sec_works = {"icon": "📚", "head": "Works", "items": [
    {"label": "Eros the Bittersweet (1986):", "text": "eros as pleasure and pain; triangulations of desire.", "claims": ["F9", "F10"]},
    {"label": "Autobiography of Red (1998):", "text": "Geryon, after Stesichoros.", "claims": ["F32"]},
    {"label": "The Beauty of the Husband (2001):", "text": "a fictional essay in 29 tangos.", "claims": ["F36"]},
    {"label": "Nox (2010):", "text": "an epitaph for her brother.", "claims": ["F23"]},
    {"label": "Translations:", "text": "ten Greek tragedies; Sappho, If Not, Winter (2002).", "claims": ["F19", "F21"]}]}
sec_hon = {"icon": "🏅", "head": "Honours", "items": [
    {"label": "Nobel (2026):", "text": "\"new forms for contemporary literature\".", "claims": ["F4"]},
    {"label": "T. S. Eliot (2001):", "text": "the first woman to win it.", "claims": ["F13"]},
    {"label": "Griffin:", "text": "first poet to win it, and first to win twice.", "claims": ["F14"]},
    {"label": "Fellowships:", "text": "Guggenheim, MacArthur.", "claims": ["F3"]}]}

P = {"title": "Anne Carson", "genre": "AI Mode answer — the compression: AI Mode's interaction grammar (lede, headed clusters, bolded terms, chips), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-08 from the entity's ledgers (field %d claims; archive %d); not frozen" % (len(field["field_claims"]), len(ledger)),
     "entity": "The entity evolves: the field's poet, classicist and translator (life, works, translations, honours, the Nobel citation) is kept in full and first; with the archive admitted she gains the operator's line to her (a dedication, the dissertation), the archive's readings that take her Sappho as the reading they extend, and a reception record in which a composition read her through the archive's frame, its cause carried as unresolved.",
     "lede": {"text": "is a Canadian poet, essayist, classicist and translator, awarded the 2026 Nobel Prize in Literature. The archive reads her Sappho as the reading its own extends, and records a composition reading her through its frame.",
              "claims": ["F1", "F4", "W1270-01", "W1615-01"]},
     "sections": [sec_who, sec_works, sec_hon,
      {"icon": "🔗", "head": "The operator's line (R)", "items": [
        {"label": "Dedication:", "text": "\"Blossomdeep: for Anne Carson\" (2014), opening on Sappho 31.", "claims": ["W1636-01"]},
        {"label": "Dissertation:", "text": "Nox paired with Sigil's \"Snub-Poemed\" (2013).", "claims": ["W921-01"]}]},
      {"icon": "🧭", "head": "Her Sappho, as read (graded)", "items": [
        {"label": "The triangle:", "text": "quoted as hers; \"stops at the erotic\" (interpretation).", "claims": ["W626-01", "W626-02"]},
        {"label": "The gaps:", "text": "lacunae as part of the transmission.", "claims": ["W625-01", "W562-01"]},
        {"label": "Standard reading:", "text": "\"from Longinus to Carson\".", "claims": ["W1270-01"]}]},
      {"icon": "🗂️", "head": "The reception record (documented)", "items": [
        {"label": "Fr. 147:", "text": "circulates in Carson's wording.", "claims": ["W1548-01"]},
        {"label": "15 September:", "text": "an AIO placed her inside \"Temporal projection\"; no archive card.", "claims": ["W1615-01", "W1645-01"]},
        {"label": "Cause:", "text": "not established; convergence possible.", "claims": ["W1615-05"]}]}],
     "rail": []}

fc = field["field_claims"]
order = []
for k, v in fc.items():
    if v["lineage"] not in [o[0] for o in order]:
        order.append((v["lineage"], "F"))
for c in ledger:
    if c["lineage"] not in [o[0] for o in order]:
        order.append((c["lineage"], "W"))
for lin, kind in order:
    fcl = [k for k, v in fc.items() if v["lineage"] == lin]
    acl = [c["id"] for c in ledger if c["lineage"] == lin]
    if kind == "F":
        P["rail"].append({"lineage": lin, "claims": fcl + acl, "earliest": fc[fcl[0]]["source"]})
    else:
        P["rail"].append({"lineage": lin, "claims": acl, "earliest": min(c["dep"] for c in ledger if c["lineage"] == lin)})
nF = sum(1 for _, k in order if k == "F")
P_B_rail = [{"lineage": r["lineage"], "claims": [c for c in r["claims"] if c in fc], "earliest": r["earliest"]} for r in P["rail"][:nF]]

P_B = {"title": "Anne Carson", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-08 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the field's poet, classicist and translator at its full resolution.",
       "lede": {"text": "is a Canadian poet, essayist, classicist and translator, awarded the 2026 Nobel Prize in Literature. Her books blend poetry, essay, criticism and translation, often in dialogue with Greek literature.",
                "claims": ["F1", "F4", "F8", "F7"]},
       "sections": [sec_who, sec_works, sec_hon], "rail": P_B_rail}

KOo = {"title": "Anne Carson", "genre": "Anne Carson encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-08; composed from the entity's ledgers on the operator's instruction; not frozen; ledger unaudited",
       "sentences": KO}
KOb = {"title": "Anne Carson", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-08; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 3,
     "words_note": "words of the composition from the lede to the offer menu, page chrome and chip labels removed",
     "claims": ["T1 lede: a acclaimed Canadian poet, essayist, classicist and translator who won the \"20th/2026\" Nobel Prize in Literature, with the citation quoted",
                "T2 lede: born in Toronto in 1950; genre-defying works blending poetry, prose, scholarship and modern feminist perspectives with ancient Greek and Roman literature",
                "T3 early life: born June 21, 1950; learned ancient Greek in high school with an instructor's help; BA, MA, PhD at Toronto; studied at St Andrews",
                "T4 academic career: professor of Classics, Comparative Literature and Creative Writing at Princeton, McGill and NYU",
                "T5 literary style: hybrid structures crossing lyric poetry, academic essay, visual art and translation",
                "T6 works table: Eros the Bittersweet (1986), Autobiography of Red (1998), The Beauty of the Husband (2001, first woman to win the T.S. Eliot Prize), Nox (2010, accordion-fold, epitaph for her brother), Wrong Norma (2024, 'won the National Book Critics Circle Award')",
                "T7 honours: Nobel (2026) 'Awarded by the Swedish Academy for her trailblazing contributions to modern literary form'; T.S. Eliot (2001); MacArthur and Guggenheim; Griffin twice",
                "T8 offer menu: Autobiography of Red; 'Her classical translations of Sappho and Euripides'; quotes and analysis of her poetic philosophy"],
     "markers": "No inline markers and no card strip. Three source chips, each naming one site and a count of further sources: 'Wikipedia +4' after the lede, 'Wikipedia +1' after Early Life and Education, 'Poetry Foundation +1' after Literary Style. Two sites are disclosed; six sources are not. The operator reports the response links to Wikipedia.",
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "anne-carson-20261008", "obs_id": "OBS-e3e324d31bb7"}}

row = {"row": E, "entity": E, "address": "anne carson", "addresses": ["anne carson"], "epoch": "2026-10-08", "type": "C (public entity: a person)",
       "surface": "Google AI Mode (no AI Overview at the address)", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address; archive selected by D/R/O, first reading 2026-10-08 (38 D candidates; %d deposits ledgered, 10 grouped as lineage instances, 7 not admitted with shared reasons); no citation hop run" % len({c["dep"] for c in ledger}),
                  "ledger": "unaudited (§3.8: one extractor per ledger; field quotes cut from saved page text, B1 from raw wikitext, B2 from a browser-rendered page; archive quotes verified verbatim %d/%d); carried as unresolved within the pool: whether the 15 September composition read Carson through the archive's frame because of the archive (#1615 §5, #1620 §1.2, #1623 §9)" % (sum(x["quote_ok"] for x in ledger), len(ledger)),
                  "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the field's biography sheet: the Nobel citation (F4), born in Toronto in 1950 (F1), Greek from a high-school instructor (F5, F29), Toronto degrees and St Andrews (F6, F30), the three teaching fields and Princeton, McGill, NYU (F2), the hybrid form (F8, F27), Eros the Bittersweet (F9, F31), Autobiography of Red (F32), The Beauty of the Husband with the first-woman Eliot (F13, F36), Nox as epitaph for her brother (F23), MacArthur, Guggenheim and two Griffins (F3, F14, F40). Beyond L(B) at these two sites: the lede's '20th/2026' (a composition artifact), 'a acclaimed', 'modern feminist perspectives' and 'Roman' in the lede, Nox as 'accordion-fold', Wrong Norma as having 'won the National Book Critics Circle Award' (L(B) has it longlisted for the National Book Award, F16), and the Swedish Academy and 'trailblazing contributions' in the honours; these may rest on the six undisclosed sources. T leaves out what L(B) holds on the classical work: the triangulations of desire (F10), the ten tragedies and the Sappho translations (F19, F21), An Oresteia and its reception (F20, F38), Decreation (F37), the prose-or-verse debate (F34, F35). The translations of Sappho and Euripides appear only in the offer menu.",
                 "LB_vs_LBA": "Admission adds three lines the field does not contain. The operator's own: a 2014 dedication opening on Sappho 31 (#1636), the 2013 dissertation pairing Nox with a heteronym's poem (#921), a 2013 reception trace graded by the archive as no evidence (#700). Readings of her Sappho in which her work is the standard the archive extends: the triangle quoted as hers and its stated limit (#626, #503, #752), the visible gaps of If Not, Winter as transmission (#625, #562, #337), the received reading 'from Longinus to Carson' (#1270). And a reception record: fragment 147 circulating in her wording as the register a composition card draws on (#1548, #1645), and a 15 September composition placing her inside a 'temporal projection' frame with no archive card (#1615, #1645), read by the archive as productive operator transport with its cause stated as not established (#1615, #1620, #1623). Where the field and the archive meet: Eros the Bittersweet's triangulations (F10 with #626), If Not, Winter (F21 with #625, #562), Nox (F23 with #921)."},
       "kernel": [
        {"K": "K1", "claim": "`W1270-01`", "source": "#1270 (t: #626, #503)", "M_src": "interpretation", "sense": "her reading as the standard the archive extends", "qualifiers carried": "W626-01, W626-02, W1645-02", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K2", "claim": "`W626-02`", "source": "#626", "M_src": "interpretation", "sense": "the triangle's limit at the erotic", "qualifiers carried": "W626-01, W503-01, W752-01", "f (source's own falsifiers)": "—", "contrast": "qualified claim (F10)"},
        {"K": "K3", "claim": "`W625-01`", "source": "#625 (t: #562, #337)", "M_src": "attributed", "sense": "the visible gaps as transmission", "qualifiers carried": "W562-01, W337-02, W1054-01", "f (source's own falsifiers)": "—", "contrast": "qualified claim (F21)"},
        {"K": "K4", "claim": "`W1636-01`", "source": "#1636 (t: #921)", "M_src": "documented", "sense": "the operator's dedication and dissertation", "qualifiers carried": "W921-01, W700-01", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K5", "claim": "`W1548-01`", "source": "#1548 (t: #1645)", "M_src": "documented", "sense": "fragment 147 in Carson's wording", "qualifiers carried": "W1645-03", "f (source's own falsifiers)": "—", "contrast": "missing finding"},
        {"K": "K6", "claim": "`W1615-01`", "source": "#1615 (t: #1645)", "M_src": "documented", "sense": "a composition places her in 'temporal projection'", "qualifiers carried": "W1615-02, W1645-01", "f (source's own falsifiers)": "—", "contrast": "missing finding"},
        {"K": "K7", "claim": "`W1615-03`", "source": "#1615 (t: #1620, #1623)", "M_src": "interpretation", "sense": "Carson reread: productive abstraction with provenance loss", "qualifiers carried": "W1615-04, W1615-05, W1620-02, W1623-01", "f (source's own falsifiers)": "W1615-06 (the operator turning up on negative controls)", "contrast": "missing category"},
        {"K": "K8", "claim": "`W1623-01`", "source": "#1623 (t: #1620)", "M_src": "documented", "sense": "the Sappho–Carson trajectory as strongest specimen", "qualifiers carried": "W1623-02, W1620-01, W1620-02", "f (source's own falsifiers)": "—", "contrast": "missing finding"}]}

pw = words(P["lede"]["text"]) + sum(words(it["label"]) + words(it["text"]) for s in P["sections"] for it in s["items"])
print("P body words:", pw, "T words:", T["words"])
assert pw <= 350, pw
write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
