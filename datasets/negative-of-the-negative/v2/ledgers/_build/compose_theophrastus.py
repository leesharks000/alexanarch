import json, hashlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "theophrastus"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1-20261007/paste-theopheastus-ai-mode.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("Would you like to explore")[0]

KO = sents([
 [("Theophrastus (c. 371 – c. 287 BCE) was an ancient Greek philosopher and naturalist, a native of Eresos on Lesbos, and Aristotle's colleague and successor as head of the Lyceum, the Peripatetic school.", ["F1", "F2", "F23", "F24"]),
  ("Born Tyrtamus, he is said to have been renamed by Aristotle for the grace, or the godlike quality, of his speech.", ["F3", "F4", "F25", "F50"])],
 [("Aristotle left him his library and named him successor; under his headship of some thirty-five years the school acquired a more institutionalized character, and his own will, preserved by Diogenes Laertius, left its garden, house and colonnades to be held in common and the books, Aristotle's manuscripts among them, to Neleus.", ["F6", "F26", "F7", "F27", "T1581-02"]),
  ("Diogenes lists some 227 titles, more than 232,000 lines, across the whole field of knowledge; of well over two hundred treatises less than a tenth survives, and the corrupt state of what does lends plausibility to the story of the books languishing in a cellar at Scepsis.", ["F8", "F28", "F29", "F9", "F10"])],
 [("The surviving works include the Enquiry into Plants, which classifies plants by generation, locality and size, and On the Causes of Plants, the pair described as a counterpart to Aristotle's zoology; after Linnaeus some have called him the father of botany.", ["F11", "F13", "F62", "F56", "F12"]),
  ("The Characters, thirty sketches of negative Athenian types, are the first recorded systematic character writing; in logic he is credited with introducing prosleptic syllogisms and with discussing hypothetical ones alongside Eudemus; and On the Senses, long read only as a doxographic source, is now recognized as an independent work.", ["F14", "F42", "F15", "F32", "F33", "F39", "F40"]),
  ("His short Metaphysics raises difficulties for universal teleology and for the unmoved mover, developing problems beyond experience more than solving them.", ["F17", "F37", "F38", "F22", "F21"])],
 [("How far he followed or departed from Aristotle can be determined only in part: he is read as neither a footnoting disciple nor a radical innovator, and many of his views have to be reconstructed from later writers such as Alexander of Aphrodisias and Simplicius.", ["F19", "F30", "F31", "F20"])],
 [("A body of work set against that received picture holds that the surviving corpora under the names Aristotle and Theophrastus do not support treating the names as two distinct authors; the number of makers is left open, open because uncounted, and calendar and membership are not claimed.", ["T1587-01", "T1588-01", "T1587-02", "T1588-03"]),
  ("On that reading the received biography is a set of relations supplied by receiving texts, and \"Theophrastus\" is read as a position within the corpus, the first draft of the Aristotle-position, \"first\" naming the order of method.", ["T1585-03", "T1585-04", "T1585-01", "T1585-02"]),
  ("Against the received reading of the Metaphysics as a pupil's questions put from outside to Aristotle's Λ, its sixth and seventh sections are read as a hinge written from inside Λ, with no marker at the hinge of a second person taking up a first person's work; at one locus the fragment names Λ 8's object, the number of the spheres, and refuses by name the method Λ has used.", ["T1583-01", "T1583-02", "T1583-06", "T1602-01"]),
  ("A directed measure of rare-term uptake ranks the edge from the fragment to Λ first of 1,482; the two passages are read as standing in ordered dependency at eight locations, and the sequence alone is held unable to decide which was written first.", ["T1605-01", "T1605-03", "T1601-02"]),
  ("Twelve titles stand letter for letter in both catalogues, one entry assigns a work to \"Aristotelian or Theophrastan\", and five of Aristotle's lost early dialogues have Theophrastan twins.", ["T1581-03", "T1581-04", "T1590-01"]),
  ("Theophrastus is also read as void as an independent control for Aristotle: he fails the rule that a control be attested independently of style, doctrine or succession, the two corpora share one transmission channel, and all four kinds of witness to the division between Plato and Aristotle are read as passing through him.", ["T1565-03", "T1571-01", "T1570-04", "T1594-01"]),
  ("The first principal axis of stylistic variation across the two corpora is read as a world/apparatus axis, ahead of any author axis; supervised attribution recovers the names above chance (0.798, against 0.860 for the operation), an earlier claim that they sit at chance was withdrawn, and no such separation is taken to license an inference to distinct makers.", ["T1586-03", "T1593-01", "T1593-03", "T1593-02"]),
  ("The Characters are read as an operation, a registry of thirty vices on a single column, legible before any question of persons.", ["T1584-02", "T1584-03"]),
  ("The strongest form, one self-dividing maker, with Plato the dialogue position, Theophrastus the first draft and Aristotle the treatise position and legal identity, is stated as a hypothesis.", ["T1658-02"])],
 [("These readings state what would weaken or decide them: a grammatical sign at the hinge, or an extant Theophrastan work answering the fragment's questions, would falsify the hinge; an independent witness to the partition from outside the Peripatos would weaken the witness reading; Isḥāq's Arabic, read at five loci, would decide among the competing readings of the fragment; and any epigraphic or papyrological item for Theophrastus is listed as still open.", ["T1583-09", "T1583-10", "T1594-05", "T1597-04", "T1658-09"]),
  ("What they show concerns what Theophrastus's attestation rests on, and leaves open whether he was a person; they are held as provisional, with no independent uptake.", ["T1658-08", "T1611-03"])],
])
KO_B = sents([[(s["text"], s["claims"]) for s in KO[:2]], [(s["text"], s["claims"]) for s in KO[2:4]],
              [(s["text"], s["claims"]) for s in KO[4:7]], [(s["text"], s["claims"]) for s in KO[7:8]]])
KO_B[2]["text"] = "Aristotle left him his library and named him successor; under his headship of some thirty-five years the school acquired a more institutionalized character, and his will, preserved by Diogenes Laertius, left its garden, house and colonnades to the school and the books, Aristotle's manuscripts among them, to Neleus."
KO_B[2]["claims"] = ["F6", "F26", "F7", "F27"]

sec_received = {"icon": "👤", "head": "The received person", "items": [
    {"label": "Born Tyrtamus,", "text": "Eresos, c. 371; reputedly renamed by Aristotle for his speech.", "claims": ["F24", "F3", "F25"]},
    {"label": "Successor:", "text": "Aristotle's library and the school; some 35 years as head.", "claims": ["F6", "F26"]},
    {"label": "The will:", "text": "garden and buildings to the school; the books to Neleus.", "claims": ["F7", "F27"]}]}
sec_works = {"icon": "📚", "head": "The works", "items": [
    {"label": "227 titles listed;", "text": "a small fraction survives.", "claims": ["F8", "F52", "F9"]},
    {"label": "Plants:", "text": "Enquiry and Causes, the counterpart to Aristotle's zoology; 'father of botany'.", "claims": ["F11", "F62", "F12"]},
    {"label": "Characters, logic, senses:", "text": "thirty types; prosleptic syllogisms credited to him; On the Senses an independent work.", "claims": ["F14", "F32", "F40"]},
    {"label": "Metaphysics:", "text": "difficulties for teleology and the unmoved mover.", "claims": ["F37", "F38", "F22"]}]}
sec_far = {"icon": "⚖️", "head": "How far from Aristotle", "items": [
    {"label": "Only partly determinable:", "text": "neither footnote nor radical innovator; much known through Alexander and Simplicius.", "claims": ["F19", "F30", "F20"]}]}
P = {"title": "Theophrastus", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field 62 claims; archive 150); not frozen",
     "entity": "The entity evolves: the received person (successor, botanist, a lost library) is kept in full and first; with the archive admitted, the name also becomes a position in a corpus whose division by name is contested, every archive line carrying its grade and its falsifier.",
     "lede": {"text": "was Aristotle's colleague and successor at the Lyceum, a philosopher and naturalist of whose writings less than a tenth survives; on a reading proposed against the received one, the two names do not mark two distinct authors, and the number of makers is open.",
              "claims": ["F23", "F8", "F29", "T1587-01", "T1587-02"]},
     "sections": [sec_received, sec_works, sec_far,
      {"icon": "🔁", "head": "One corpus, two names (proposed)", "items": [
        {"label": "Not two distinct authors:", "text": "the corpora do not support treating the names as two author-variables; maker count open.", "claims": ["T1587-01", "T1588-01", "T1587-02"]},
        {"label": "The hinge, read:", "text": "the fragment's sections 6–7 continue Λ from inside; no second-person marker.", "claims": ["T1583-02", "T1583-06", "T1602-01"]},
        {"label": "Ranked first:", "text": "fragment → Λ, first of 1,482 directed edges; the sequence cannot decide which came first.", "claims": ["T1605-01", "T1601-02"]},
        {"label": "Catalogues:", "text": "twelve shared titles; 'Aristotelian or Theophrastan'; five ghost twins.", "claims": ["T1581-03", "T1581-04", "T1590-01"]}]},
      {"icon": "🧪", "head": "Measured", "items": [
        {"label": "Axis, read:", "text": "world against apparatus, ahead of author.", "claims": ["T1586-03"]},
        {"label": "Names recovered:", "text": "0.798 against 0.860; 'at chance' withdrawn; no inference to makers.", "claims": ["T1593-01", "T1593-03", "T1593-02"]}]},
      {"icon": "🔍", "head": "The witness", "items": [
        {"label": "Read as void as a control:", "text": "no attestation independent of style, doctrine or succession; the witnesses to the Plato/Aristotle split pass through him.", "claims": ["T1565-03", "T1571-01", "T1594-01"]},
        {"label": "Strongest form, a hypothesis:", "text": "one self-dividing maker.", "claims": ["T1658-02"]}]},
      {"icon": "⚠️", "head": "Falsifiers and limits", "items": [
        {"label": "Would weaken or decide it:", "text": "a second-voice sign at the hinge; an independent witness; Isḥāq's Arabic at five loci.", "claims": ["T1583-09", "T1594-05", "T1597-04"]},
        {"label": "Provisional:", "text": "no independent uptake; whether he was a person left open.", "claims": ["T1611-03", "T1658-08"]}]}],
     "rail": [
      {"lineage": "The person and the renaming", "claims": ["F1", "F2", "F3", "F4", "F23", "F24", "F25", "F49", "F50", "F59"], "earliest": "B1"},
      {"lineage": "Succession and the will", "claims": ["F6", "F7", "F26", "F27", "F53", "F60", "T1581-02"], "earliest": "B1"},
      {"lineage": "The catalogue and its loss", "claims": ["F8", "F9", "F28", "F29", "F52", "F57", "F61"], "earliest": "B1"},
      {"lineage": "The Scepsis story", "claims": ["F10"], "earliest": "B1"},
      {"lineage": "Botany", "claims": ["F11", "F12", "F13", "F41", "F55", "F56", "F58", "F62"], "earliest": "B1"},
      {"lineage": "The Characters", "claims": ["F14", "F15", "F42", "F47", "F54"], "earliest": "B1"},
      {"lineage": "Logic", "claims": ["F16", "F32", "F33", "F34", "F35"], "earliest": "B1"},
      {"lineage": "Metaphysics and teleology", "claims": ["F17", "F21", "F22", "F36", "F37", "F38"], "earliest": "B1"},
      {"lineage": "The senses and doxography", "claims": ["F18", "F39", "F40", "F43", "F44", "F48"], "earliest": "B1"},
      {"lineage": "How far from Aristotle", "claims": ["F19", "F20", "F30", "F31", "F51"], "earliest": "B1"},
      {"lineage": "Not two distinct authors; maker count open", "claims": ["T1587-01", "T1588-01", "T1587-02", "T1588-03", "T1587-05"], "earliest": 1587},
      {"lineage": "The received reading stated, its relations reversed", "claims": ["T1583-01", "T1585-03", "T1585-04"], "earliest": 1583},
      {"lineage": "The first draft of the Aristotle-position", "claims": ["T1585-01", "T1585-02"], "earliest": 1585},
      {"lineage": "The hinge", "claims": ["T1583-02", "T1583-06", "T1602-01", "T1605-01", "T1605-03"], "earliest": 1583},
      {"lineage": "Direction unresolved", "claims": ["T1601-02", "T1605-08"], "earliest": 1601},
      {"lineage": "The catalogues: shared titles and ghost twins", "claims": ["T1581-03", "T1581-04", "T1590-01"], "earliest": 1581},
      {"lineage": "Void as a control; the witness inside", "claims": ["T1565-03", "T1570-03", "T1571-01", "T1570-04", "T1594-01"], "earliest": 1565},
      {"lineage": "The axis and the recovered names", "claims": ["T1586-03", "T1593-01", "T1593-03", "T1593-02"], "earliest": 1586},
      {"lineage": "The Characters as an operation", "claims": ["T1584-02", "T1584-03"], "earliest": 1584},
      {"lineage": "One self-dividing maker (hypothesis)", "claims": ["T1658-02"], "earliest": 1658},
      {"lineage": "Falsifiers and limits", "claims": ["T1583-09", "T1583-10", "T1594-05", "T1597-04", "T1658-09", "T1658-08", "T1611-03"], "earliest": 1583}]}

P_B = {"title": "Theophrastus", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the received person at the field's full resolution.",
       "lede": {"text": "was Aristotle's colleague and successor at the Lyceum, a philosopher and naturalist of whose writings less than a tenth survives; how far he departed from Aristotle can be determined only in part.", "claims": ["F23", "F8", "F29", "F19"]},
       "sections": [sec_received, sec_works, sec_far], "rail": P["rail"][:10]}

KOo = {"title": "Theophrastus", "genre": "Theophrastus encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers on the operator's instruction ('lets go ahead and write the entries for the others'); not frozen; ledger unaudited",
       "sentences": KO}
KOb = {"title": "Theophrastus", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 9,
     "claims": ["T1 definition: philosopher, naturalist, successor to Aristotle as head of the Peripatetic school (the Lyceum)",
                "T2 originally Tyrtamus; the nickname 'he of godlike speech' given by Aristotle", "T3 'over 200 treatises'; 'Father of Botany'",
                "T4 'less than 10%' survives", "T5 Enquiry into Plants: 'nine-volume', 'over 500 plant varieties'", "T6 On the Causes of Plants: 'six-volume'",
                "T7 the Characters: 30 sketches, with named types", "T8 minor treatises: On Fire, On Stones, On Odours, Weather Signs; 'earliest documented weather forecasters'",
                "T9 empirical botany: classification by growth form", "T10 logic: hypothetical and modal syllogisms, with Eudemus",
                "T11 metaphysics: challenged Aristotle's 'rigid teleology'", "T12 closer: an offer menu"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "theopheastus-20261007", "obs_id": "OBS-9ff360597434"},
     "null_overview": {"slug": "theophrastus-20261007", "obs_id": "OBS-bdcbf02de4c9",
                       "note": "At the person's own address no Overview is composed: the knowledge panel projects one Wikipedia sentence (F2), with unsourced quick facts (Parents: Melantas; Full name: Tyrtamus)."}}

row = {"row": E, "entity": E, "address": "theopheastus", "addresses": ["theophrastus", "theopheastus"], "epoch": "2026-10-07", "type": "C (public entity: a person)",
       "surface": "Google AI Mode", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (32 of 35 admitted), hop not run",
                  "ledger": "unaudited (§3.8: one extractor per ledger; field excerpts by WebFetch, archive quotes verified verbatim 150/150)", "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T (AI Mode, at 'theopheastus') composes the definition, the succession, the renaming, the count of treatises and the surviving fraction, the botanical works, the Characters, the logic and the teleology critique (F1, F3, F12, F14, F21, F23, F25, F29, F32, F33). Available in the field and not composed: Eresos and Lesbos (F2, F24), Aristotle's library and the naming of the successor (F6), the will and the books to Neleus (F7, F27), the 227 titles and 232,808 lines (F8, F28), the Scepsis story (F10), the partial determinability of his departure from Aristotle (F19), 'neither footnoting disciple nor radical innovator' (F30), reconstruction through Alexander and Simplicius (F20), On the Senses as an independent work and the doxographic line (F40, F43, F48), the unmoved mover abandoned (F38), the definition of possibility against Aristotle (F35). In T and not in the field as fetched: 'nine-volume' and 'over 500 plant varieties' (the field: ten books, nine surviving), 'six-volume', On Fire, On Odours and Weather Signs, 'earliest documented weather forecasters', the named sketches. At 'theophrastus' itself no Overview is composed: one Wikipedia sentence and unsourced quick facts.",
                 "LB_vs_LBA": "Admission adds what the field does not hold: the received reading stated as relations supplied by receiving texts; the claim that the two names are not two distinct authors, with the number of makers left open; the Metaphysics fragment as a hinge written from inside Λ, and its measured dependency on Λ, direction unresolved; the shared titles and ghost twins of the two catalogues; Theophrastus as void as an independent control, the witness inside the thing witnessed; the stylometric axis (world against apparatus) and the names recovered above chance, with a withdrawn claim recorded; the Characters as an operation; the one-maker hypothesis; and the falsifiers and limits, including that nothing is shown about a person. The field's entity, a person with a lost library, is kept whole and first; with the archive it also becomes a name whose division from Aristotle's is contested at stated grades."},
       "kernel": [
        {"K": "K1", "claim": "`T1587-01`", "source": "#1587 (t: #1588)", "M_src": "interpretation", "sense": "two names, not two authors", "qualifiers carried": "T1587-02", "f (source's own falsifiers)": "first axis failing on another feature family or edition; blind labels or held-out prediction at chance (T1587-08)", "contrast": "missing distinction"},
        {"K": "K2", "claim": "`T1587-02`", "source": "#1587 (t: #1588)", "M_src": "self-description", "sense": "maker count open", "qualifiers carried": "T1588-03", "f (source's own falsifiers)": "—", "contrast": "missing limit"},
        {"K": "K3", "claim": "`T1583-02`", "source": "#1583 (t: #1595, #1602, #1605)", "M_src": "interpretation", "sense": "the hinge", "qualifiers carried": "T1583-05", "f (source's own falsifiers)": "a second-voice sign at the hinge; an extant Theophrastan answer (T1583-09, T1583-10)", "contrast": "missing distinction"},
        {"K": "K4", "claim": "`T1605-01`", "source": "#1605", "M_src": "documented", "sense": "measured dependency", "qualifiers carried": "T1605-08", "f (source's own falsifiers)": "Isḥāq's Arabic at five loci (T1597-04)", "contrast": "missing evidence"},
        {"K": "K5", "claim": "`T1581-03`", "source": "#1581 (t: #1590)", "M_src": "documented", "sense": "shared titles", "qualifiers carried": "T1581-01", "f (source's own falsifiers)": "—", "contrast": "missing evidence"},
        {"K": "K6", "claim": "`T1570-03`", "source": "#1570 (t: #1565, #1571)", "M_src": "interpretation", "sense": "void as a control", "qualifiers carried": "T1570-05", "f (source's own falsifiers)": "an attestation independent of style, doctrine or succession (T1571-01)", "contrast": "missing distinction"},
        {"K": "K7", "claim": "`T1594-01`", "source": "#1594", "M_src": "interpretation", "sense": "the witness inside", "qualifiers carried": "T1594-02", "f (source's own falsifiers)": "an independent non-Peripatetic witness to the partition (T1594-05)", "contrast": "missing relation"},
        {"K": "K8", "claim": "`T1593-01`", "source": "#1593 (t: #1594)", "M_src": "documented", "sense": "names recovered", "qualifiers carried": "T1593-02", "f (source's own falsifiers)": "—", "contrast": "missing evidence"},
        {"K": "K9", "claim": "`T1585-01`", "source": "#1585", "M_src": "hypothesis", "sense": "first draft of the Aristotle-position", "qualifiers carried": "T1585-02", "f (source's own falsifiers)": "each seam prediction's received-reading inverse (T1585-08)", "contrast": "missing operation"},
        {"K": "K10", "claim": "`T1584-02`", "source": "#1584", "M_src": "interpretation", "sense": "the Characters as an operation", "qualifiers carried": "T1584-06", "f (source's own falsifiers)": "—", "contrast": "missing operation"},
        {"K": "K11", "claim": "`T1658-08`", "source": "#1658", "M_src": "self-description", "sense": "nothing shown about a person", "qualifiers carried": "T1658-09", "f (source's own falsifiers)": "any epigraphic or papyrological attestation (T1658-09)", "contrast": "missing limit"}]}

write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
