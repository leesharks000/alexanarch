import json, hashlib, sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "literary-heteronym"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
ledger = json.loads((HERE / E / "ledger.json").read_text(encoding="utf-8"))
reading = json.loads((HERE / E / "reading.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1d-20261007/paste-literary-heteronym.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("literary heteronymliterary heteronym", 1)[1].split("\nWikipedia\nHeteronym (literature)")[0]
body = re.sub(r"\(https?://[^)]*\)", "", re.sub(r"\[\[.*?\]\]", "", body))  # composition text without citation markup
body = re.sub(r"\[(\d+)\]", "", body)

FIELD_PARAS = [
 [("In literature, one of the term's several senses beside its grammatical and linguistic ones, the concept of the heteronym refers to one or more imaginary characters created by a writer to write in different styles, such as the fictitious authors Fernando Pessoa invented, who \"wrote\" parts of his work.", ["F48", "F1", "F35"]),
  ("Heteronyms differ from pen names, or pseudonyms, in that pseudonyms are just false names while heteronyms are characters with their own supposed physiques, biographies and writing styles; one study adds that they can hold views in sharp contrast to those of the author who created them, and George Steiner, calling pseudonymous writing not rare, with Kierkegaard a celebrated instance, finds \"heteronyms\", as Pessoa called and defined them, \"something different and exceedingly strange\".", ["F2", "F32", "F33", "F24", "F11", "F55"]),
  ("Pessoa drew the line himself: his figures being too radically different from him to be considered simple pseudonyms, Pessoa called them \"heteronyms\", Richard Zenith writes, and in a \"Bibliographical Summary\" published in 1928 Pessoa explained that \"Pseudonymous works are by the author in his own person, except in the name he signs; heteronymous works are by the author outside his own person\"; a statement the Poetry Society of America quotes has a heteronymic work \"by an author writing outside his own personality\".", ["F38", "F54", "F39", "F16"])],
 [("Heteronyms were named and developed by Pessoa in the early twentieth century, the writer credited with introducing the concept into literature, and on Wikipedia's account they were thoroughly explored by Kierkegaard in the nineteenth, who had more than a dozen with distinct biographies and personalities.", ["F3", "F25", "F13"]),
  ("Pessoa described his literary enterprise as \"a drama divided into people instead of into acts\"; the process began in his childhood and made literary history in 1914 with the creation of Alberto Caeiro, Álvaro de Campos and Ricardo Reis, his three chief heteronyms, of whom Caeiro was considered the Master of the other two and of Pessoa himself.", ["F49", "F50", "F40", "F6", "F51"]),
  ("Counts differ: at least 70 heteronyms by the latest count of Pessoa's editor Teresa Rita Lopes, about 75 names in one study, more than seventy personae in another account, and, on Zenith's reckoning, if the childhood riddlers and humorists are included, more than one hundred fictitious authors in whose name Pessoa wrote or at least planned to write, about thirty of whom signed a significant work, with only three full-fledged heteronyms, a word Zenith says he will use \"rather loosely\", authorized by Pessoa's example.", ["F4", "F28", "F18", "F45", "F46", "F54"]),
  ("Beside them Pessoa called Bernardo Soares and the Baron of Teive semi-heteronyms, semi-autobiographical characters who write in prose, \"a mere mutilation\" of the Pessoa personality, and one account makes Soares the closest identity to a pseudonym; there is, lastly, an orthonym, Fernando Pessoa, the namesake of the author, which one account glosses as Pessoa \"himself\".", ["F7", "F10", "F21", "F8", "F36"]),
  ("Some of the heteronyms know each other; they criticise and translate each other's works, collaborate on projects and dialogue in what Pessoa calls \"drama in people\", and in Steiner's description Pessoa conceived for each voice an idiom, a biography and \"subtle interrelations and reciprocities of awareness\"; they sometimes intervened in Pessoa's social life, a jealous Campos writing letters to the girl in Pessoa's only attested romance.", ["F5", "F20", "F9", "F12", "F55", "F34"])],
 [("Readings of the practice differ: Gaspar Simões is reported to have judged the heteronyms a kind of subterfuge, or a gimmick, symptomatic of the author's inability or unwillingness to concentrate his entire self in writing; Zenith holds that Pessoa staked his very identity on the system and that no writer can rival his configured ensemble; the account the Poetry Society excerpts holds that the conceit did not spring from a desire to fool anyone.", ["F44", "F47", "F43", "F54", "F19"]),
  ("Precedents are argued: one study holds that strong heteronymic qualities can be discerned in W. B. Yeats, in works some of which came about twenty years before Pessoa began his career, finds three fictional names in Yeats's collected poems, Red Hanrahan, Owen Aherne and Michael Robartes, and concludes that Yeats either originated the concept without naming it or paved the way for its introduction into Western literature, finding it feasible to think that Yeats's works could have been a source of inspiration even if Pessoa did not borrow from him; Zenith finds \"some faint parallels\", Yeats's Robartes and Owen Hearne and Antonio Machado's Juan de Mairena and Abel Martín.", ["F26", "F29", "F31", "F30", "F41", "F42", "F54"])],
]

ARCHIVE_PARAS = [
 [("A further position, the archive's typology of Pessoa's system, states the distinction as definition: a pseudonym is defined as a name substitution in which the writing remains that of the biographical person, a heteronym in Pessoa's sense as an independent authorial figure whose writing emerges from a constructed position, and the orthonym as the author's own name as literary voice, apart from the biographical person; Teresa Rita Lopes and later critics are reported to have extended the typology with the proto-heteronym and the para-heteronym, and a strict heteronym test of five criteria is specified.", ["N667-01", "N667-03", "N667-04", "N667-05", "N667-07"]),
  ("The typology claims adequacy to the practices it was developed to describe, disclaims cultural universality, and states that classical literatures, certain non-European traditions and oral traditions may require adjustments it has not yet made; within it Kierkegaard's pseudonymous authors are read as mapping predominantly to the heteronym in the extended sense, Machado's Mairena and Martín are held heteronymic in substantially Pessoan sense, Borges's Menard is held typologically distinct, a diegetic character, and Yeats's Robartes and Hearne are placed in a zone between heteronym and literary character.", ["N667-13", "N667-14", "N667-08", "N667-09", "N667-10", "N667-11"]),
  ("Another archive paper holds Pessoa's practice the canonical case of a describable theoretical practice, a practice with a history, Pessoa its most richly theorized instance though neither its origin nor its termination, and Kierkegaard as having operated heteronymically in substantively Pessoa's sense half a century earlier and without the term; on origins the archive is divided, one deposit calling Pessoa the poet \"who invented the form\" and another holding that he \"did not invent heteronymic practice. He formalized it.\"", ["N666-01", "N666-02", "N666-04", "N1127-02", "N96-01"]),
  ("One essay defines the meta-heteronym as a heteronymic system whose personae produce, beyond literary works, the institutional apparatus under which those works become legible, reads Orpheu (1915) as such an institution, holds that Pessoa can be read as the first modern meta-heteronym, and states as its central thesis \"heteronymy is a technology, not a pathology\", describing its reading as typological and disclaiming that Pessoa \"anticipated\" digital infrastructure; another deposit holds the meta-heteronym to be \"an inscription that generates heteronyms\".", ["N682-01", "N682-03", "N682-08", "N682-04", "N682-07", "N666-07"])],
 [("Several archive deposits define the heteronym as a function: heteronyms as \"authorial functions\", a heteronym as \"a structure-function\" validated by performance, and, in a further pair of definitions, a pseudonym as changing the label attached to an authorial function and a heteronym as changing its organization.", ["N348-01", "N348-02", "N79-01", "N940-02"]),
  ("The archive is divided on what the heteronym is: one essay states that \"A heteronym is a person\", while a registry says of the archive's own heteronyms that they \"are not separate persons; they are differentiated positions\" through which their bearer's labour is articulated, and a further paper reports as its parent paper's central premise that a heteronym must \"survive as a person\", with biography, style and plausible independence, or be a transparent pseudonym; on the mask, one deposit holds heteronyms to be \"not pseudonyms, masks, or personas\", while another holds that \"A single heteronym is a mask; a system of heteronyms is an authorial architecture\" and a third that \"The heteronym is a mask\".", ["N96-02", "N90-02", "N136-01", "N348-01", "N666-03", "N852-01"]),
  ("An ethics paper defines heteronymy as the ethical practice of sustaining a distinct named authorial function without falsely reducing it to a civil identity or falsely presenting it as an independent civil person, holds the function attributable through the civil bearer without being reducible to that bearer, and states its limits: heteronymy \"is not ethical by its existence\", and the false multiplication of one voice into apparent independent corroboration is stated to be fabrication.", ["N940-01", "N940-04", "N940-05", "N940-06"]),
  ("The orthonym is contested within the archive: it is defined as the author's own name as literary voice, as the authorial position bearing a project's founding operative gesture, which on Pessoa's corpus is \"arguably Caeiro\" under the functional definition and Pessoa-himself under Pessoa's usage, a corpus seat recording both readings and settling neither, and as \"the regulatory fiction that stabilizes a heteronymic system\", with Socrates as the central mask through which Plato's authorship is distributed.", ["N667-03", "N123-08", "N1561-01", "N1561-02", "N859-01", "N859-02"])],
 [("A paper on the Socratic corpus states as hypothesis that the founding corpus of Western philosophy can be read as a single distributed authorial project, defines the heteronym analytically as a stable authorial position functionally required by an operation the project performs, distinguishes pseudepigrapha by concealment, and limits its claim to the reading becoming thinkable, disclaiming that Pessoa-style heteronymy existed as a named or institutionalized practice in classical Athens; a further deposit, without reference to concealment, lists an \"Inherited\" named position, in which a disciple writes under a teacher's name, the Pauline school among its cases, separately from the \"Heteronymic\" position, a created name functioning independently.", ["N123-01", "N123-02", "N123-05", "N123-12", "N123-09", "N68-02", "N68-04"]),
  ("A further paper states a No-Floor Theorem, that under the premise that documentary separateness is constructed by a heteronymic configuration the method has no internal criterion for halting attribution of adjacent named figures, sets a firewall, \"Biographical identity requires evidence. Functional identity requires pattern.\", and does not assert that the founding corpus was written by one hidden person; on maker-count the archive is divided, another paper proposing as hypothesis \"one self-dividing maker\" as the production model with which the Platonic, Theophrastan and Aristotelian corpus is consistent, \"nothing in it\" requiring another maker.", ["N136-02", "N136-04", "N136-06", "N1658-02", "N1658-03"]),
  ("The archive seats Browning, Pound and Pessoa as \"one practice at three stages\", Pound read as the middle term where the mask becomes a position the poet inhabits, and takes Pessoa, whose letter of 13 January 1935 attributes the heteronyms, as the positive control for instruments claiming to detect designed differentiation, Kierkegaard's printed acknowledgements of 1846 and 1851 making his grouping documented in the same way.", ["N1560-04", "N1560-01", "N1560-02", "N1560-03", "N1562-01"]),
  ("On these corpora a measure finds that pooling Pessoa's three heteronyms recovers the orthonym inside the same-author band while individually the voices do not look like Pessoa, a size confound among its stated limits; that every term by which Caeiro is known is absent from Caeiro's own text, supplied by Mora, Campos and Reis, a capture the register then records as not distinctive of heteronymy; and that relation-type, heteronymic construction included, is not recoverable from lexical distribution; from these results the register reads a heteronymic configuration as able to instantiate a master–student relation, Pessoa being \"the existence proof\".", ["N1570-01", "N1570-02", "N1570-03", "N1570-04", "N1572-04", "N1570-05"])],
]

KO = sents(FIELD_PARAS + ARCHIVE_PARAS)
KO_B = sents(FIELD_PARAS)

sec_def = {"icon": "🧭", "head": "Definition", "items": [
    {"label": "Pseudonym:", "text": "just a false name; heteronyms have physiques, biographies, styles.", "claims": ["F2", "F33"]},
    {"label": "Pessoa, 1928 (per Zenith):", "text": "heteronymous works are \"by the author outside his own person\".", "claims": ["F39", "F54"]},
    {"label": "Orthonym:", "text": "Fernando Pessoa, the namesake of the author.", "claims": ["F8"]}]}
sec_sys = {"icon": "📜", "head": "Pessoa's system", "items": [
    {"label": "Drama in people:", "text": "Caeiro, Campos and Reis created in 1914; Caeiro their Master.", "claims": ["F9", "F49", "F50", "F51"]},
    {"label": "Counts:", "text": "at least 70 (Lopes); about 75; over a hundred written or planned, three full-fledged (Zenith).", "claims": ["F4", "F28", "F45", "F54"]},
    {"label": "Interplay:", "text": "mutual criticism and translation; sometimes intervening in Pessoa's life.", "claims": ["F5", "F20", "F34"]}]}
sec_prec = {"icon": "⚖️", "head": "Precedents, readings", "items": [
    {"label": "Kierkegaard:", "text": "more than a dozen heteronyms, per Wikipedia.", "claims": ["F3", "F13"]},
    {"label": "Yeats, argued:", "text": "either originated the concept unnamed or paved the way, one study concludes.", "claims": ["F26", "F31", "F30"]},
    {"label": "Readings:", "text": "a gimmick (Gaspar Simões, reported); identity staked on it (Zenith).", "claims": ["F44", "F47", "F54"]}]}
P = {"title": "Literary heteronym", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field %d claims; archive %d); not frozen" % (len(field["field_claims"]), len(ledger)),
     "entity": "The entity evolves: the field's heteronym (an imaginary character with its own biography and style, set against the pseudonym, Pessoa's coinage, counted variously, with Yeats and Kierkegaard as argued precedents) is kept in full and first; with the archive admitted it gains a defined typology with stated limits, a theory of the heteronym as function that the archive contests within itself (person or position, mask or operation, three orthonyms), an ethics with its own limits, an extension to antiquity stated as hypothesis and bounded by a No-Floor Theorem, and measured findings on Pessoa and Kierkegaard as calibration corpora.",
     "lede": {"text": "is an imaginary character a writer creates to write in a different style, with its own supposed physique, biography and style; a pseudonym is just a false name. Archive deposits further define it as an authorial function, one as a person.",
              "claims": ["F1", "F2", "N348-02", "N79-01", "N96-02"]},
     "sections": [sec_def, sec_sys, sec_prec,
      {"icon": "🗂️", "head": "Typology and ethics (archive)", "items": [
        {"label": "Defined:", "text": "a heteronym, in Pessoa's sense, as an independent authorial figure whose writing emerges from a constructed position.", "claims": ["N667-01"]},
        {"label": "Bounded:", "text": "adequacy claimed, universality disclaimed.", "claims": ["N667-13", "N667-14"]},
        {"label": "Origin, contested within:", "text": "Pessoa \"invented the form\" (#1127); \"He formalized it\" (#96).", "claims": ["N1127-02", "N96-01"]},
        {"label": "Ethical practice:", "text": "defined as a named function neither falsely reduced to a civil identity nor falsely presented as an independent civil person.", "claims": ["N940-01"]},
        {"label": "Meta-heteronym, two accounts:", "text": "personae producing their apparatus of legibility, defined (#682); an inscription generating heteronyms, held (#666).", "claims": ["N682-01", "N666-07"]}]},
      {"icon": "🔁", "head": "Function, contested within", "items": [
        {"label": "Defined as function:", "text": "a structure-function validated by performance.", "claims": ["N79-01"]},
        {"label": "Person or position:", "text": "\"A heteronym is a person\" (#96); the archive's own heteronyms \"differentiated positions\" (#90).", "claims": ["N96-02", "N90-02"]},
        {"label": "Orthonym, defined three ways:", "text": "literary voice (#667); founding-gesture position, arguably Caeiro (#123, #1561); regulatory fiction (#859).", "claims": ["N667-03", "N123-08", "N1561-01", "N859-01"]}]},
      {"icon": "🏛️", "head": "Antiquity", "items": [
        {"label": "Hypothesis:", "text": "philosophy's founding corpus as one distributed project, claimed thinkable.", "claims": ["N123-01", "N123-12"]},
        {"label": "Pseudepigrapha:", "text": "set apart by concealment (#123); an inherited position listed apart from the heteronymic (#68).", "claims": ["N123-05", "N68-02", "N68-04"]},
        {"label": "No floor:", "text": "a halting criterion held absent; one hidden person unasserted (#136); a self-dividing maker hypothesized, contested (#1658).", "claims": ["N136-02", "N136-06", "N1658-02"]}]},
      {"icon": "📏", "head": "Measured", "items": [
        {"label": "Pooling:", "text": "a measure finds Pessoa's pooled heteronyms recover the orthonym; size confound stated.", "claims": ["N1570-01", "N1570-02"]},
        {"label": "Capture:", "text": "Caeiro's known terms found absent from Caeiro; capture found not distinctive.", "claims": ["N1570-03", "N1570-04"]},
        {"label": "Relation-type:", "text": "found not recoverable from lexical distribution.", "claims": ["N1572-04"]}]}],
     "rail": []}

# rail: one entry per lineage, in order of first appearance; field lineages first; archive earliest from the reading's lineages
fc = field["field_claims"]
rl = {l["lineage"]: l for l in reading["lineages"]}
order = []
for k, v in fc.items():
    if v["lineage"] not in [o[0] for o in order]:
        order.append((v["lineage"], "F"))
for c in ledger:
    if c["lineage"] not in [o[0] for o in order]:
        order.append((c["lineage"], "N"))
for lin, kind in order:
    if kind == "F":
        cl = [k for k, v in fc.items() if v["lineage"] == lin]
        P["rail"].append({"lineage": lin, "claims": cl, "earliest": fc[cl[0]]["source"]})
    else:
        cl = [c["id"] for c in ledger if c["lineage"] == lin]
        P["rail"].append({"lineage": lin, "claims": cl, "earliest": rl[lin]["earliest"], "instances": rl[lin]["instances"]})
nF = sum(1 for _, k in order if k == "F")

P_B = {"title": "Literary heteronym", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the field's heteronym at its full resolution.",
       "lede": {"text": "is an imaginary character a writer creates to write in a different style, with its own supposed physique, biography and writing style; a pseudonym is just a false name. Pessoa named and developed it.", "claims": ["F1", "F2", "F3"]},
       "sections": [sec_def, sec_sys, sec_prec], "rail": P["rail"][:nF]}

KOo = {"title": "Literary heteronym", "genre": "Literary heteronym encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers on the operator's instruction; not frozen; ledger unaudited",
       "sentences": KO}
KOb = {"title": "Literary heteronym", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 8,
     "words_note": "words of the composition before the card list, citation link markup removed",
     "claims": ["T1 definition: a fully developed fictional character created by an author to write under a distinct identity, with biography, physical appearance, philosophy and writing style",
                "T2 pseudonyms (pen names): simply a false name used by an author who continues to write as themselves",
                "T3 heteronyms: independent personae operating outside the author's own personality, sometimes critiquing or translating each other's work",
                "T4 the creator writing as themselves is the 'orthonym'",
                "T5 Pessoa coined the term and invented dozens of heteronyms: Caeiro (pastoral, anti-philosophical, the 'master'), Reis (neoclassical, formal, pagan worldview), Campos (exuberant modernist engineer and futurist poet)",
                "T6 Kierkegaard used numerous pseudonymous/heteronymous authors (Johannes de Silentio, Anti-Climacus) to present conflicting philosophical viewpoints"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "literary-heteronym-20261007", "obs_id": "OBS-cd659e41d9ec"}}

row = {"row": E, "entity": E, "address": "literary heteronym", "addresses": ["literary heteronym"], "epoch": "2026-10-07", "type": "C (public entity)",
       "surface": "Google AI Overview (expanded)", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (%d of %d admitted, %d as lineage instances), hop not run" % (reading["counts"]["admitted"], reading["counts"]["candidate_deposits"], reading["counts"]["lineage_instances"]),
                  "ledger": "unaudited (§3.8: one extractor per ledger; field excerpts by WebFetch and page text, archive quotes verified verbatim %d/%d); the archive's statements are carried as contested within the pool where they disagree (person or position #96/#90; mask #666, #852/#123, #482; the orthonym #667/#123, #1561/#859; origin #1127/#96; the non-human case #794/#940; maker-count #136/#1658; the meta-heteronym #666/#682)" % (sum(1 for c in ledger if c.get("quote_ok")), len(ledger)), "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the definition (F1, F32, F35) with T's 'physical appearance' and 'philosophy' as the field's physiques and world views (F2, F24); the pseudonym as a false name (F2, F33); the heteronym 'outside the author's own personality' (F16, F39); mutual critique and translation (F5, F20); the orthonym (F8, F36); Pessoa's coinage (T: 'coined the term'; the field: 'named and developed', 'credited with the development, naming and introduction', F3, F25); Caeiro, Reis and Campos with Caeiro the master (F6, F37, F50, F51); Kierkegaard (F3, F13). Available in the field and not composed: Yeats as argued precedent or originator (F26, F29, F30, F31) and Zenith's 'faint parallels' with Machado (F41, F42); the counts and their disagreement (F4, F18, F28, F45) and Zenith's loose usage (F46); the semi-heteronyms (F7, F10, F21); 1914 and the 'drama in people' (F9, F40, F49, F50); the heteronyms' interventions in Pessoa's life (F34, F53); Steiner's reading (F11, F12); the readings of the practice (F44, F47, F19, F43, F23); the term's other senses (F48); performers (F14). T's Reis 'pagan worldview' and its naming of Johannes de Silentio and Anti-Climacus are not in the field ledger's quotes.",
                 "LB_vs_LBA": "Admission adds a position the field does not hold: a typology defined with operational tests and Lopes's extensions, its stated limits (adequacy, no cultural universality, classical and oral literatures not yet accommodated) and its placements of Kierkegaard, Machado, Borges and Yeats; the heteronym defined as a function (structure-function, label against organization) and the archive's own contests over whether that function is a person or a position, a mask or an operation, and which voice is the orthonym (literary voice, founding gesture and 'arguably Caeiro', regulatory fiction); heteronymy defined as an ethical practice with conditions and with its limits stated; the meta-heteronym, defined twice; the extension to antiquity stated as hypothesis, with pseudepigrapha contested, a No-Floor Theorem and a firewall bounding it, and a later naming of one self-dividing maker; and measured findings on Pessoa and Kierkegaard as calibration corpora (pooling, capture not distinctive, relation-type not recoverable). The field's Yeats precedent is met by the archive's placement of Yeats's figures between heteronym and literary character. The field's heteronym is kept whole and first; with the archive it gains these at stated grades."},
       "kernel": [
        {"K": "K1", "claim": "`N667-01`", "source": "#667 (t: #666, #668)", "M_src": "stipulation", "sense": "heteronym against pseudonym, defined", "qualifiers carried": "N667-13, N667-14", "f (source's own falsifiers)": "—", "contrast": "missing distinction"},
        {"K": "K2", "claim": "`N79-01`", "source": "#79 (t: #348, #940, #123)", "M_src": "stipulation", "sense": "the heteronym as function", "qualifiers carried": "N348-02, N940-02, N123-02", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K3", "claim": "`N96-02`", "source": "#96 against #90", "M_src": "stipulation (contested in the pool)", "sense": "person or position", "qualifiers carried": "N90-02, N136-01, N96-05", "f (source's own falsifiers)": "—", "contrast": "contested"},
        {"K": "K4", "claim": "`N123-08`", "source": "#123 against #667 and #859 (t: #1561)", "M_src": "stipulation (contested in the pool)", "sense": "the orthonym", "qualifiers carried": "N667-03, N859-01, N1561-01, N1561-02", "f (source's own falsifiers)": "—", "contrast": "contested"},
        {"K": "K5", "claim": "`N940-01`", "source": "#940", "M_src": "stipulation", "sense": "heteronymy as ethical practice", "qualifiers carried": "N940-05, N940-06, N940-13", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K6", "claim": "`N682-01`", "source": "#682 against #666 (t: #69)", "M_src": "stipulation", "sense": "the meta-heteronym", "qualifiers carried": "N682-07, N666-07", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K7", "claim": "`N666-01`", "source": "#666 (t: #96, #1127)", "M_src": "interpretation", "sense": "a practice with a history", "qualifiers carried": "N666-02, N96-01, N1127-02", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K8", "claim": "`N123-01`", "source": "#123 (t: #203, #68)", "M_src": "hypothesis", "sense": "heteronymy in antiquity", "qualifiers carried": "N123-12, N123-09, N123-05, N68-02", "f (source's own falsifiers)": "— (#203's falsifier (b), N203-02, for the NT application)", "contrast": "missing relation"},
        {"K": "K9", "claim": "`N136-02`", "source": "#136 against #1658 (t: #1261, #1585)", "M_src": "interpretation", "sense": "no floor", "qualifiers carried": "N136-04, N136-06, N1658-02", "f (source's own falsifiers)": "—", "contrast": "missing limit"},
        {"K": "K10", "claim": "`N1570-01`", "source": "#1570 (t: #1560)", "M_src": "documented", "sense": "Pessoa as calibration", "qualifiers carried": "N1570-02, N1560-03", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K11", "claim": "`N1570-05`", "source": "#1570 (t: #1572, #1575)", "M_src": "interpretation", "sense": "position structure and maker-count", "qualifiers carried": "N1570-06, N1572-04, N1570-04", "f (source's own falsifiers)": "—", "contrast": "missing relation"}]}

pb = words(P["lede"]["text"]) + sum(words(it["label"]) + words(it["text"]) for s in P["sections"] for it in s["items"])
print("P body words (lede + labels + texts):", pb, "| with heads:", pb + sum(words(s["head"]) for s in P["sections"]))
assert pb <= 350, pb
write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
