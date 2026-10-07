import json, hashlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "the-socratic-problem"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1-20261007/paste-the-socratic-problem.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("If you'd like to explore further")[0].split("the socratic problemthe socratic problem", 1)[1]

KO = sents([
 [("The Socratic problem is the difficulty of reconstructing a historical and philosophical image of Socrates from sources that vary and contradict one another.", ["F1", "F26", "F35"]),
  ("Socrates wrote nothing and is known mainly through posthumous accounts; the four important sources are Plato and Xenophon, his disciples, Aristotle, born fifteen years after his death and informed at second hand, and the comic playwright Aristophanes, his contemporary, with fragments from other Socratics such as Aeschines and Antisthenes.", ["F2", "F34", "F3", "F4", "F29", "F14", "F5"])],
 [("The earliest source is Aristophanes' Clouds of 423 BC, whose Socrates may amalgamate several philosophers; Xenophon's Socrates is more practical, and is described as duller than Plato's, and the two disciples contradict each other, for instance on whether Socrates took payment for teaching.", ["F28", "F24", "F25", "F36", "F10"]),
  ("Socrates is the principal speaker in all of Plato's dialogues but the Laws, some of which depict events before Plato's birth; it is widely believed that few if any are verbatim accounts; a common view holds that they move from Socratic toward Platonic doctrine, and stylometry groups them as early, middle and late.", ["F22", "F23", "F7", "F8", "F9"]),
  ("Aristotle reports that Socrates did not hold the forms to be separate, a testimony often taken as free of the disciples' bias.", ["F15", "F40"])],
 [("Schleiermacher's essay of 1815 shaped the modern question, treating the Apology and the Crito as purely Socratic, and by the early twentieth century Xenophon had been largely set aside.", ["F11", "F12", "F38"]),
  ("Positions range from the argument that much can be known of Socrates' life, character, interests and method, while knowledge does not extend to his doctrines, if he had any, to the view that the problem cannot be solved: that his era did not separate fact from fiction, that the Socratic dialogue is a non-historical genre, and, with de Vogel, that the \"real\" Socrates we do not have, only the possible ones.", ["F31", "F32", "F16", "F18", "F17", "F20", "F41"])],
 [("A further position reclassifies the problem without solving it: the difficulty becomes the symptom of an authorial configuration that a biographical model of authorship cannot represent.", ["S123-02", "S1576-01", "S1575-01"]),
  ("In that configuration Socrates is defined as the orthonym, the position that bears the founding gesture of willing death for the logos and does not write, and Plato as the survival-position, writing a made character and withdrawing from it; biographical identity is held to require evidence, functional identity a pattern.", ["S123-01", "S1585-01", "S136-08", "S1576-02"]),
  ("Read so, Plato's Second Letter at 314c describes an edition, the revamping and inhabiting of a received character, whose base is a circulating figure surviving as Aristophanes' Socrates-the-sophist; the corpus's relation to the historical Socrates is held to lie beyond any text's reach.", ["S1579-01", "S1579-03"]),
  ("On the same reading there is no Socrates to recover apart from the family of renderings and the negative space they imply, and Aristotle's Sophistical Refutations 34 is read as having already dissolved Socrates as a predecessor from whom part of the inquiry was received.", ["S168-02", "S1603-01"]),
  ("The reading is also measured: in Aristotle, Socrates never appears in snub contexts (0 of 144) against his placeholder twin Callias (5 of 35), a distribution the innocent reading, that his snub is biographical and so avoided, is stated to explain fully; in Plato he is the most loosely specified of seven speaking positions, under a falsifier fixed in advance, with the limit that a dramatist would produce the same gradient.", ["S1570-01", "S1571-02", "S1571-01", "S1570-02", "S1575-05"]),
  ("Its strongest thesis, that one hand wrote Plato and Socrates, and probably Xenophon and Aristophanes, was tested on how confined Socrates' attestation is to these texts; Protagoras proved more confined still (99.8 against 99.5 per cent), and the confinement was found unremarkable within its class, produced by being a subject of philosophical dialogue.", ["S1569-01", "S1569-05", "S1572-01", "S1572-02"]),
  ("The Clouds' Socrates is held to be a literary relation at a named seam, outside the corpus relations of the configuration; the comic layer is read as carrying the accusation-profile and none of the questioning method; and Xenophon is held apart as a candidate, with the test across the Plato/Xenophon seam specified.", ["S1594-03", "S1569-12", "S1585-03", "S1658-01"])],
 [("Within this position the man's status is unsettled: one formulation keeps the historical Socrates real, his historical function the founding gesture; another, under the orthonymic reading, denies that he is a historical figure imperfectly accessed through later authors; later work declines any thesis about who the historical Socrates was.", ["S123-09", "S167-02", "S1579-04", "S203-01"]),
  ("It states its limits: it makes the configuration thinkable and does not prove it, it claims no identity of persons, and it leaves the authenticity of the Second Letter undecided.", ["S123-16", "S123-05", "S136-03", "S1579-05"])],
])
KO_B = sents([[(s["text"], s["claims"]) for s in KO[:2]], [(s["text"], s["claims"]) for s in KO[2:5]], [(s["text"], s["claims"]) for s in KO[5:7]]])

sec_sources = {"icon": "📜", "head": "The sources", "items": [
    {"label": "Wrote nothing:", "text": "known mainly through others' accounts.", "claims": ["F2", "F34"]},
    {"label": "Four witnesses:", "text": "Plato and Xenophon (disciples), Aristophanes (contemporary), Aristotle (at second hand).", "claims": ["F3", "F4", "F14", "F29"]},
    {"label": "They disagree:", "text": "the Clouds, 423 BC, perhaps a composite; Xenophon practical; payment for teaching.", "claims": ["F28", "F24", "F25", "F10"]}]}
sec_plato = {"icon": "🧭", "head": "Plato's Socrates", "items": [
    {"label": "Principal speaker", "text": "in every dialogue but the Laws; few if any thought verbatim.", "claims": ["F22", "F7"]},
    {"label": "Developmental view:", "text": "early Socratic, later Platonic; stylometry groups early, middle, late.", "claims": ["F8", "F9"]},
    {"label": "Aristotle's testimony:", "text": "the forms not separate.", "claims": ["F15", "F40"]}]}
sec_pos = {"icon": "⚖️", "head": "Positions", "items": [
    {"label": "Schleiermacher, 1815:", "text": "Apology and Crito purely Socratic; Xenophon later set aside.", "claims": ["F11", "F12", "F38"]},
    {"label": "Reconstruct (Prior):", "text": "life, character, interests, method; knowledge not reaching the doctrines.", "claims": ["F31", "F32"]},
    {"label": "Unsolvable:", "text": "fact and fiction unseparated; a non-historical genre (Kahn); only possible Socrateses (de Vogel).", "claims": ["F16", "F18", "F17", "F20"]}]}
P = {"title": "The Socratic problem", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field 42 claims; archive 157); not frozen",
     "entity": "The entity evolves: the field's problem (a real man behind contradictory portraits, perhaps unrecoverable) is kept in full and first; with the archive admitted, the problem gains a further position that reclassifies it as the symptom of an authorial configuration, measured, partly withdrawn, and unsettled within itself on the man.",
     "lede": {"text": "is the difficulty of recovering the historical Socrates, who wrote nothing, from portrayals that contradict one another; a further position, proposed, reclassifies it as the symptom of an authorial configuration with Socrates as its orthonym.",
              "claims": ["F1", "F2", "F35", "S123-02", "S123-01"]},
     "sections": [sec_sources, sec_plato, sec_pos,
      {"icon": "🔁", "head": "Reclassified (proposed)", "items": [
        {"label": "A symptom", "text": "of a configuration the biographical model cannot represent; reclassified, left unsolved.", "claims": ["S123-02", "S1576-01"]},
        {"label": "The orthonym:", "text": "the founding gesture, willing death for the logos; does not write.", "claims": ["S123-01", "S1585-01"]},
        {"label": "An edition:", "text": "Letter II 314c, a received Aristophanic character revamped.", "claims": ["S1579-01", "S1579-03"]},
        {"label": "Only renderings:", "text": "no Socrates apart from them.", "claims": ["S168-02"]}]},
      {"icon": "🧪", "head": "Measured", "items": [
        {"label": "Snub:", "text": "Socrates 0 of 144 in Aristotle, Callias 5 of 35; the innocent reading explains it fully.", "claims": ["S1570-01", "S1570-02"]},
        {"label": "Loosest speaker:", "text": "rank 1 of 7 in Plato, falsifier fixed in advance.", "claims": ["S1571-02", "S1571-01"]},
        {"label": "Not decisive:", "text": "confinement of attestation; Protagoras more confined.", "claims": ["S1569-05", "S1572-01"]}]},
      {"icon": "⚠️", "head": "Unsettled and limited", "items": [
        {"label": "The man's status, contested within:", "text": "kept real (#123); denied as a figure imperfectly accessed (#167); no thesis about persons (#1579).", "claims": ["S123-09", "S167-02", "S1579-04"]},
        {"label": "Limits:", "text": "makes it thinkable, proves nothing; no identity of persons.", "claims": ["S123-16", "S123-05"]}]}],
     "rail": [
      {"lineage": "The problem defined", "claims": ["F1", "F26", "F35"], "earliest": "B1"},
      {"lineage": "Socrates wrote nothing", "claims": ["F2", "F27", "F34"], "earliest": "B1"},
      {"lineage": "The sources", "claims": ["F3", "F4", "F5", "F21", "F14", "F29"], "earliest": "B1"},
      {"lineage": "Aristophanes' Socrates", "claims": ["F28", "F24"], "earliest": "B2"},
      {"lineage": "Xenophon's Socrates", "claims": ["F25", "F36", "F37", "F38", "F10"], "earliest": "B1"},
      {"lineage": "Plato's dialogues", "claims": ["F6", "F7", "F8", "F9", "F22", "F23", "F33"], "earliest": "B1"},
      {"lineage": "Aristotle's testimony", "claims": ["F15", "F40"], "earliest": "B1"},
      {"lineage": "Schleiermacher", "claims": ["F11", "F12", "F13"], "earliest": "B1"},
      {"lineage": "What can be reconstructed", "claims": ["F30", "F31", "F32"], "earliest": "B3"},
      {"lineage": "Unsolvable", "claims": ["F16", "F17", "F18", "F19", "F20", "F39", "F41", "F42"], "earliest": "B1"},
      {"lineage": "The problem as a symptom", "claims": ["S123-02", "S1576-01", "S1575-01", "S1261-01"], "earliest": 123},
      {"lineage": "Socrates as orthonym", "claims": ["S123-01", "S1585-01", "S859-01", "S152-01"], "earliest": 123},
      {"lineage": "Biographical against functional identity", "claims": ["S136-08", "S1576-02", "S123-05", "S136-03"], "earliest": 123},
      {"lineage": "An edition of a received character", "claims": ["S1579-01", "S1579-03", "S1583-01"], "earliest": 1579},
      {"lineage": "No Socrates apart from the renderings", "claims": ["S168-01", "S168-02"], "earliest": 168},
      {"lineage": "Socrates inside the inquiry (SE 34)", "claims": ["S1603-01", "S1574-01", "S1603-05"], "earliest": 1574},
      {"lineage": "Measured: snub and the loosest speaker", "claims": ["S1570-01", "S1570-02", "S1571-01", "S1571-02", "S1575-05"], "earliest": 1570},
      {"lineage": "One hand: tested, withdrawn", "claims": ["S1569-01", "S1569-05", "S1572-01", "S1572-02"], "earliest": 1569},
      {"lineage": "Aristophanes outside; Xenophon held apart", "claims": ["S1594-03", "S1569-12", "S1585-03", "S1658-01"], "earliest": 1569},
      {"lineage": "The man's status, unsettled in the archive", "claims": ["S123-09", "S167-02", "S1579-04", "S203-01"], "earliest": 123},
      {"lineage": "The reading's limits", "claims": ["S123-16", "S1579-05"], "earliest": 123}]}

P_B = {"title": "The Socratic problem", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the field's problem at its full resolution.",
       "lede": {"text": "is the difficulty of recovering the historical Socrates, who wrote nothing, from portrayals by Plato, Xenophon, Aristophanes and Aristotle that contradict one another; some hold it cannot be solved.", "claims": ["F1", "F2", "F4", "F35", "F16"]},
       "sections": [sec_sources, sec_plato, sec_pos], "rail": P["rail"][:10]}

KOo = {"title": "The Socratic problem", "genre": "The Socratic problem encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers on the operator's instruction ('lets go ahead and write the entries for the others'); not frozen; ledger unaudited",
       "sentences": KO}
KOb = {"title": "The Socratic problem", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 7,
     "claims": ["T1 definition: separating the real, historical Socrates from the fictionalized character portrayed by students and contemporaries",
                "T2 no written records", "T3 conflicting accounts", "T4 ancient writers did not write strict biographies",
                "T5 Aristophanes: The Clouds", "T6 Plato: later a mouthpiece for his own theories", "T7 Xenophon: practical; 'uninspiring' to later critics",
                "T8 Aristotle: secondary commentary", "T9 chronological sorting of the dialogues", "T10 the early dialogues closest to the historical style",
                "T11 permanent skepticism", "T12 closer: an offer menu"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "the-socratic-problem-20261007", "obs_id": "OBS-723305818c26"}}

row = {"row": E, "entity": E, "address": "the socratic problem", "addresses": ["the socratic problem"], "epoch": "2026-10-07", "type": "C (public entity)",
       "surface": "Google AI Overview", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (48 of 145 admitted), hop not run",
                  "ledger": "unaudited (§3.8: one extractor per ledger; field excerpts by WebFetch, archive quotes verified verbatim 157/157); the archive's statements of the man's status are carried as contested within the pool (#123, #167, #1579)", "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the definition, the absence of writings, the conflicting accounts, the four sources in one line each, the developmental sorting of the dialogues and permanent skepticism (F1, F2, F4, F6, F8, F9, F14, F16, F18, F24, F25, F37). Available in the field and not composed: the fragmentary Socratics (F5), the payment contradiction (F10), Schleiermacher and his Apology and Crito (F11–F13), Aristotle's report on the forms and its independence of the disciples (F15, F40), Kahn's non-historical genre and Apology-only position (F17, F42), De Vogel's 'possible Socrateses' (F20), Prior's division between the knowable life and the unknowable doctrines (F31, F32), the date of the Clouds (F28), the 35 dialogues and the events before Plato's birth (F22, F23), the logoi Sokratikoi's failure even where they overlap (F41), Xenophon's twentieth-century rejection (F38). T's 'fictionalized character' sharpens the field's frame; its 'ancient writers did not try to write strict, modern biographies' matches F18.",
                 "LB_vs_LBA": "Admission adds a position the field does not hold: the problem reclassified as the symptom of an authorial configuration; Socrates defined as the orthonym and Plato as the survival-position, with biographical identity kept apart from functional identity; Letter II 314c as the edition of a received Aristophanic character; no Socrates apart from the renderings; Aristotle's SE 34 as having dissolved Socrates as a predecessor; measurements (the snub examples, the loosest speaking position) with their innocent readings; the one-hand thesis tested and its inference withdrawn; Aristophanes outside the configuration and Xenophon held apart, untested; and, carried as contested, the archive's own disagreement on whether the historical man is real, a position, or beyond any thesis. The field's problem is kept whole and first; with the archive it gains a further answer at stated grades."},
       "kernel": [
        {"K": "K1", "claim": "`S123-02`", "source": "#123 (t: #1575, #1576)", "M_src": "hypothesis", "sense": "the problem as a symptom", "qualifiers carried": "S123-04", "f (source's own falsifiers)": "under scarcity, gaps random with respect to function and resolvable by more evidence (S136-07)", "contrast": "missing distinction"},
        {"K": "K2", "claim": "`S123-01`", "source": "#123 (t: #1585, #859)", "M_src": "stipulation", "sense": "Socrates as orthonym", "qualifiers carried": "S123-05", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K3", "claim": "`S136-08`", "source": "#136 (t: #1576)", "M_src": "stipulation", "sense": "biographical against functional identity", "qualifiers carried": "S136-03", "f (source's own falsifiers)": "—", "contrast": "missing distinction"},
        {"K": "K4", "claim": "`S1579-01`", "source": "#1579 (t: #1583)", "M_src": "interpretation", "sense": "an edition of a received character", "qualifiers carried": "S1579-04, S1579-05", "f (source's own falsifiers)": "—", "contrast": "missing operation"},
        {"K": "K5", "claim": "`S168-02`", "source": "#168", "M_src": "interpretation", "sense": "only renderings", "qualifiers carried": "—", "f (source's own falsifiers)": "—", "contrast": "missing distinction"},
        {"K": "K6", "claim": "`S1603-01`", "source": "#1603 (t: #1574)", "M_src": "interpretation", "sense": "Socrates inside the inquiry", "qualifiers carried": "S1603-05", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K7", "claim": "`S1570-01`", "source": "#1570", "M_src": "documented", "sense": "the snub examples", "qualifiers carried": "S1570-02", "f (source's own falsifiers)": "—", "contrast": "missing evidence"},
        {"K": "K8", "claim": "`S1571-02`", "source": "#1571", "M_src": "documented", "sense": "the loosest speaking position", "qualifiers carried": "S1575-05", "f (source's own falsifiers)": "Socrates not among the loosest positions (S1571-01)", "contrast": "missing evidence"},
        {"K": "K9", "claim": "`S1569-05`", "source": "#1569 (t: #1572)", "M_src": "documented", "sense": "one hand: inference withdrawn", "qualifiers carried": "S1569-03", "f (source's own falsifiers)": "other genre-subjects as confined (S1569-04), met", "contrast": "missing limit"},
        {"K": "K10", "claim": "`S1594-03`", "source": "#1594 (t: #1569, #1585, #1658)", "M_src": "documented", "sense": "Aristophanes outside; Xenophon apart", "qualifiers carried": "S1585-03", "f (source's own falsifiers)": "the Plato/Xenophon seam test, specified (S1585-03)", "contrast": "missing distinction"},
        {"K": "K11", "claim": "`S167-02`", "source": "#167 against #123 and #1579", "M_src": "interpretation (contested in the pool)", "sense": "the man's status unsettled", "qualifiers carried": "S123-09, S1579-04, S203-01", "f (source's own falsifiers)": "—", "contrast": "contested"}]}

write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
