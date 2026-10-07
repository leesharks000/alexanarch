import json, hashlib, sys, pathlib, collections
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "sappho-31"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
reading = json.loads((HERE / E / "reading.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1b-20261007/paste-sappho-31.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("If you'd like")[0].split("sappho 31sappho 31", 1)[1]

KO = sents([
 # the field's poem, in full and first
 [("Sappho 31 is a lyric poem by the Archaic Greek poet Sappho of the island of Lesbos, also known as phainetai moi, 'It seems to me', after the opening words of its first line, and as the Ode to Anactoria, a title based on a conjecture that its subject is Anactoria.", ["F1", "F2", "F3"]),
  ("It is one of Sappho's most famous poems, describing her love for a young woman; Emmet Robbins calls it probably the single most famous poem to come down from Antiquity, and it has been the subject of more scholarly commentary than any other of her works.", ["F4", "F23", "F24"])],
 [("It is preserved by quotation in the treatise On the Sublime, attributed to Longinus and dated to the first century AD by one account, to the first or third century by another, and quoted there for the intensity of its emotion; four Sapphic stanzas in the Aeolic dialect are well preserved, followed by part of one more line, and as preserved it seems to be missing the ending; Longinus leaves off one line into the fifth stanza, which begins 'Still, all must be endured, since even a poor…'.", ["F5", "F30", "F40", "F27", "F8", "F9", "F6", "F34"]),
  ("Armand D'Angour argues that the phrase ἀλλὰ πὰν τόλματον means 'all must be dared', against the 'endured' of some translations, and a reconstruction of his suggests the original may have had up to 8 stanzas; translators treat the fragmentary final stanza differently.", ["F20", "F7", "F41"])],
 [("The poem centres on three characters, a man and a woman, both otherwise unidentified, and the speaker; the grammar of the original Greek makes the gender of each figure clear, and on one anthology's account the speaker, a woman watching another woman talking to a man, turns to her own intense contradictory bodily emotions of jealousy and desire, with “tongue,” “fire,” “seeing/eyes,” “hearing/ears,” “sweat,” and “trembling” as grammatical subjects in the sentence that straddles the third and fourth stanzas; Longinus places its excellence in the selection of the most striking symptoms and their combination into a single whole.", ["F10", "F38", "F39", "F44", "F31"])],
 [("Its context has been the subject of much scholarly debate, the 'central controversy' in Thomas McEvilley's phrase: Wilamowitz suggested a wedding song with the man as bridegroom, while scholars since the second half of the twentieth century have tended to follow Denys Page in dismissing the argument, and the poem has no explicit mention of a marriage.", ["F11", "F12", "F13", "F48"]),
  ("That the poem is about Sappho's jealousy has been proposed since the eighteenth century and remains a popular interpretation, a major theory put forward by many critics; many critics deny it, Anne Carson arguing that Sappho is amazed at the man's composure, Joan DeJean that the jealousy reading plays down the poem's homoeroticism, and others reading the man as a 'contrast figure' or, with John Winkler, an introductory set-up to be dismissed.", ["F16", "F45", "F17", "F18", "F19", "F14", "F15"]),
  ("George Devereux suggested in 1970 that Sappho is describing a seizure, its symptoms the same as those of an anxiety attack, Gallavotti that the text was corrupted by the disappearance of the sound [w]; scholars have spent much time on the man in the first stanza and on whether the symptoms are of eros or envy, a multivalence the translation's note counts part of the poem's appeal.", ["F22", "F21", "F32", "F33"])],
 [("Catullus adapted it as his 51st poem, putting Lesbia into the role of the beloved, in a free translation that goes a different way in its final stanza; Theocritus and Apollonius of Rhodes adapted it, Plato draws on it in the Phaedrus, and in the nineteenth century it began to be seen as an exemplar of Romantic lyric.", ["F25", "F35", "F42", "F26", "F28", "F29"])],
 # the archive, at its grades
 [("A further reading, proposed in the archive, holds that the distal demonstrative κῆνος points to a future reader who will sit face-to-face with the inscribed text; on that reading the somatic catalogue describes voice becoming text, the χλωρός simile figures the speaker's transformation into papyrus substrate, and the fragment is proposed as the foundational text of lyric self-archiving.", ["A1270-01", "A1270-02", "A1270-03"]),
  ("A scroll dated 9 November 2025 puts as hypothesis that the reader becomes the 'that man' of fragment 31, and another paper argues that lyric address functions as a temporal projection mechanism whose future readers complete the circuit of transmission.", ["A991-01", "A991-02", "A134-01"]),
  ("The archive's own research notes name Svenbro's reading of 1988, in which, per O'Donnell's summary, the 'you' is the poem itself and the man the reader, as the major antecedent for a future reader inside the fragment, and list among what was not found in the literature swept, pending a further sweep, κῆνος as a deictic transmission mechanism.", ["A1548-01", "A1548-02", "A1548-04"]),
  ("The archive is divided on how this reading stands to jealousy: one statement holds the jealousy reading 'not wrong but incomplete', another holds the two readings mutually exclusive at the level of what κῆνος refers to.", ["A1270-05", "A1054-01"])],
 [("On the poem's ending the archive corrects itself in sequence: a reconstructed 'fourth stanza' ending γράμμασι μολπὰν, stated as hypothesis, is corrected: the reconstructed stanza is the fifth; its warrant is then held interpretive and the line is proposed, as a speculation, to be a hanging line whose logic of completion is inscribed in it; later papers report that the sole witness, Parisinus graecus 2036, writes the poem as continuous prose, so every printed boundary is editorial.", ["A281-01", "A1270-08", "A201-01", "A201-03", "A1051-01", "A1051-02", "A1474-01", "A1484-04"]),
  ("A dialect count finds seventeen Aeolic markers in seventy-four words and none in the six disputed words, stated as not significant in isolation (P = 0.209); one paper holds those words to be the quoting author's as material and Sappho's as form, another places the break in Longinus's citation; the last transmitted form, τολματόν, is a verbal adjective that cannot govern a nominative agent, and the configuration at the edge is argued to be the object itself, a design reading its paper states as a choice.", ["A1474-02", "A1484-06", "A1052-03", "A1484-05", "A1476-01", "A1476-02"]),
  ("A continuity record of the sequence states that six documents used the archive's instruments on the hanging line and returned, each time, the reading the instruments were built to produce, and that the seventh reversed it.", ["A1482-01"])],
 [("The treatise On the Sublime is held to contain a theory of transmissional inscription, which its paper states as a fact about the text, and at the only point where the treatise addresses its reader immediately after a quotation without naming him, the quotation is Sappho 31.", ["F30", "A1458-01", "A1458-03"]),
  ("Catullus is held to be κῆνος, the anticipated reader arrived; the archive is divided on his fourth stanza, read in its errata as a structurally precise operator inversion of Sappho's fifth and in a later note as a fourth stanza about idleness that has no Greek counterpart, while a measure aligns Sappho 31 and Catullus 51 at C = 0.688, slot by slot, and Catullus is not Sappho.", ["A1270-09", "A1484-07", "A1049-02", "A1601-01", "A1572-01"])],
 [("A survey maps the ancient reception as a braided field, with Catullus as the control case and the program's own transforms kept as program-specific hypotheses.", ["A1532-05", "A1532-02", "A1532-06"]),
  ("A claim tiered in three rings of descending evidentiary hardness holds the Logos to be a technology with an extant founding document in Sappho 31; Augustine's Confessions 10.27 is read as an organ-by-organ transformation of the poem and two loci of canonical Josephus as realizing its apparatus, a note on inscription with Revelation 2:17 as its convergence point does not claim a direct linear transmission, a pre-registered verdict holds that Revelation 12's redaction of its biblical materials realizes the apparatus of the poem's ancient reception at eight of nine stations, and a program mapping Sappho 31 onto Philo names the failure mode that would destroy it as unfalsifiable pan-Sapphism.", ["A1484-01", "A1484-02", "A496-01", "A496-02", "A1477-01", "A1493-01", "A828-01", "A828-02", "A1495-01", "A1486-01", "A1486-02"]),
  ("Within the archive Sappho of Lesbos is established as the originary node of the Crimson Hexagon by structural identity, and Fragment 31 is the source of its operator σ_S :: Body → Text, through which all queries regarding the fragment are to resolve, and its 'root directory'; and a further deposit holds that Fragment 147 says a future receiver will exist and 31 builds the receiver's seat, attributes the seat and the joining to Lee Sharks, and states that τινα does not mean 'reader'.", ["A283-01", "A38-01", "A299-01", "A306-01", "A1645-01", "A1645-02"])],
])
KO_B = sents([[(s["text"], s["claims"]) for s in KO[:2]], [(s["text"], s["claims"]) for s in KO[2:4]], [(KO[4]["text"], KO[4]["claims"])],
              [(s["text"], s["claims"]) for s in KO[5:8]], [(KO[8]["text"], KO[8]["claims"])]])

sec_poem = {"icon": "📜", "head": "The poem", "items": [
    {"label": "Sappho of Lesbos,", "text": "Archaic lyric; also phainetai moi, and the Ode to Anactoria (a conjecture).", "claims": ["F1", "F2", "F3"]},
    {"label": "Famous:", "text": "her love for a young woman; more commentary than any other of her works.", "claims": ["F4", "F24"]},
    {"label": "Three figures:", "text": "a man, a woman, the speaker; the Greek marks each one's gender.", "claims": ["F10", "F38"]}]}
sec_text = {"icon": "🗞️", "head": "The text", "items": [
    {"label": "Preserved", "text": "by quotation in On the Sublime, attributed to Longinus.", "claims": ["F5", "F30", "F27"]},
    {"label": "Four stanzas", "text": "and part of a line, Sapphic stanzas, Aeolic; the ending seems missing.", "claims": ["F6", "F8", "F9", "F40"]},
    {"label": "The last line:", "text": "'endured' or 'dared' (D'Angour); translators differ.", "claims": ["F34", "F20", "F41"]}]}
sec_read = {"icon": "⚖️", "head": "Readings", "items": [
    {"label": "Context debated:", "text": "a wedding song (Wilamowitz), an argument scholars have tended to follow Page in dismissing.", "claims": ["F11", "F12", "F13"]},
    {"label": "Jealousy,", "text": "proposed since the eighteenth century; denied by many (Carson: amazement; DeJean).", "claims": ["F16", "F17", "F18", "F19"]},
    {"label": "That man:", "text": "a contrast figure; a set-up to be dismissed (Winkler).", "claims": ["F14", "F15"]},
    {"label": "Symptoms:", "text": "a seizure with the symptoms of an anxiety attack (Devereux, 1970).", "claims": ["F22"]}]}
sec_rec = {"icon": "🔁", "head": "Reception", "items": [
    {"label": "Catullus 51:", "text": "Lesbia in the beloved's role; a different final stanza.", "claims": ["F25", "F35", "F42"]},
    {"label": "Greek reception:", "text": "Theocritus, Apollonius; Plato's Phaedrus.", "claims": ["F26", "F28"]},
    {"label": "Romantic lyric", "text": "from the nineteenth century.", "claims": ["F29"]}]}
P_sections = [sec_poem, sec_text, sec_read, sec_rec,
 {"icon": "👁️", "head": "The future reader (proposed)", "items": [
    {"label": "κῆνος", "text": "as the future reader facing the inscribed text; χλωρός as papyrus.", "claims": ["A1270-01", "A1270-02"]},
    {"label": "Lyric self-archiving;", "text": "address as temporal projection.", "claims": ["A1270-03", "A134-01"]},
    {"label": "Antecedent:", "text": "Svenbro (1988), by allegory.", "claims": ["A1548-01", "A1548-04"]},
    {"label": "Relation to jealousy, contested within:", "text": "incomplete (#1270); exclusive (#1054).", "claims": ["A1270-05", "A1054-01"]}]},
 {"icon": "✂️", "head": "The ending, corrected in sequence", "items": [
    {"label": "Reconstructed", "text": "'fourth stanza' ending γράμμασι μολπὰν (hypothesis), corrected to the fifth.", "claims": ["A281-01", "A1270-08", "A201-03"]},
    {"label": "Dialect step:", "text": "17 markers in 74 words, 0 in 6; not significant alone.", "claims": ["A1474-02"]},
    {"label": "τολματόν:", "text": "an act with no doer; the edge argued to be the object, a stated choice.", "claims": ["A1484-05", "A1476-01", "A1476-02"]},
    {"label": "Instruments:", "text": "six returned the reading they were built for; the seventh reversed it.", "claims": ["A1482-01"]}]},
 {"icon": "🧭", "head": "Longinus, Catullus, the Logos (graded)", "items": [
    {"label": "Longinus:", "text": "held to contain a theory of transmissional inscription; the only address right after a quotation that names no one follows fr. 31.", "claims": ["A1458-01", "A1458-03"]},
    {"label": "Catullus held to be κῆνος;", "text": "his fourth stanza contested within.", "claims": ["A1484-07", "A1049-02", "A1601-01"]},
    {"label": "Founding document:", "text": "the Logos as a technology, Sappho 31 its extant founding document, tiered in three rings; Revelation 2:17 a convergence point, direct linear transmission unclaimed.", "claims": ["A1484-01", "A1484-02", "A828-01", "A828-02"]},
    {"label": "Limit named:", "text": "unfalsifiable pan-Sapphism.", "claims": ["A1486-02"]}]}]

# rail: field lineages (earliest = first card carrying it), then archive lineages from the reading
fc = field["field_claims"]
fl = collections.OrderedDict()
for k, v in fc.items():
    fl.setdefault(v["lineage"], []).append(k)
names = {"s31-identity": "The poem identified", "s31-names": "Its names", "s31-subject-love": "Love for a young woman; same-sex desire",
         "s31-preserved-by-longinus": "Preserved in On the Sublime", "s31-incomplete": "Incomplete: four stanzas and a line", "s31-metre": "Sapphic stanzas",
         "s31-dialect": "Aeolic", "s31-scene": "The three figures", "s31-context-debated": "The context debated", "s31-wedding-song": "Wedding song, dismissed",
         "s31-that-man": "That man", "s31-jealousy": "Jealousy: proposed and denied", "s31-final-line": "The final line: endured or dared",
         "s31-opening-text": "The opening's text", "s31-symptoms": "The symptoms", "s31-fame": "Fame", "s31-catullus-51": "Catullus 51",
         "s31-ancient-adaptation": "Ancient adaptations", "s31-modern-reception": "Romantic lyric", "s31-longinus-concourse": "Longinus's verdict",
         "s31-multivalence": "Multivalence", "s31-date": "Date", "s31-greek-reading": "Read in Greek"}
rail_B = [{"lineage": names[k], "claims": v, "earliest": fc[v[0]]["source"]} for k, v in fl.items()]
lin_claims = collections.defaultdict(list)
L = json.loads((HERE / E / "ledger.json").read_text(encoding="utf-8"))
for c in L: lin_claims[c["lineage"]].append(c["id"])
rail_A = [{"lineage": x["lineage"] + (" (contested within)" if x["lineage"] in ("Jealousy and the future reader: compatible or exclusive", "Where the poem ends", "Catullus 51 as transform", "The reconstructed final stanza") else ""),
           "claims": lin_claims[x["lineage"]], "earliest": x["earliest"]} for x in reading["lineages"]]

P = {"title": "Sappho 31", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field %d claims; archive %d); not frozen" % (len(fc), len(L)),
     "entity": "The entity evolves: the field's poem (a fragment preserved by Longinus, its man, its symptoms, the jealousy reading proposed and denied, Catullus) is kept in full and first; with the archive admitted it gains a proposed reading of κῆνos as the future reader, an ending re-examined in a self-correcting sequence with its measures and their limits, and a widest claim tiered by evidentiary grade.".replace("κῆνos", "κῆνος"),
     "lede": {"text": "is a lyric poem by Sappho of Lesbos, preserved by quotation in On the Sublime, in which a speaker watches a man sitting with a woman and, in one anthology's reading, turns to her own bodily emotions; a further reading, proposed, holds κῆνος to be the future reader.",
              "claims": ["F1", "F5", "F40", "F38", "A1270-01"]},
     "sections": P_sections, "rail": rail_B + rail_A}
P_B = {"title": "Sappho 31", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the field's poem at its full resolution.",
       "lede": {"text": "is a lyric poem by Sappho of Lesbos, preserved by quotation in On the Sublime, in which a speaker watches a man sitting with a woman and, in one anthology's reading, turns to her own bodily emotions; long read as jealousy, a reading many critics deny.",
                "claims": ["F1", "F5", "F40", "F38", "F39", "F16", "F17"]},
       "sections": P_sections[:4], "rail": rail_B}

KOo = {"title": "Sappho 31", "genre": "Sappho 31 encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers on the operator's instruction; not frozen; ledger unaudited", "sentences": KO}
KOb = {"title": "Sappho 31", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 6,
     "claims": ["T1 definition: a famous ancient Greek lyric poem describing the physical and emotional symptoms of falling in love and jealousy",
                "T2 author Sappho of Lesbos, Archaic period, around the 6th century BCE",
                "T3 alternative names: phainetai moi ('It seems to me') or the Ode to Anactoria",
                "T4 preservation: survives mostly intact because a later ancient critic quoted it in On the Sublime",
                "T5 scene: the speaker watches a man sitting close to a beloved woman, listening to her talk and laugh",
                "T6 reaction: jealousy, desire, physical shock",
                "T7 symptoms: racing heart, silent tongue, ringing ears, cold sweat, feeling close to death",
                "T8 closer: an offer menu (a full translation, or Catullus's adaptation)"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "sappho-31-20261007", "obs_id": "OBS-040b5a4ccafb"}}

row = {"row": E, "entity": E, "address": "sappho 31", "addresses": ["Sappho 31", "sappho 31"], "epoch": "2026-10-07", "type": "C (public entity: a work)",
       "surface": "Google AI Overview (expanded)", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (%d of %d admitted, %d lineage instances grouped), hop not run" % (reading["counts"]["admitted"], reading["counts"]["candidate_deposits"], reading["counts"]["lineage_instances"]),
                  "ledger": "unaudited (§3.8: one extractor per ledger; field excerpts by HTTP fetch of the cards' pages, archive quotes verified verbatim %d/%d); the archive's disagreements with itself (jealousy compatible or exclusive; where the poem ends; Catullus's fourth stanza; the reconstruction's wording) are carried as contested within the pool" % (sum(c["quote_ok"] for c in L), len(L)), "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the identity, the two alternative names, the date, preservation in On the Sublime, the scene, a reaction of jealousy and desire, and the symptoms (F1, F2, F3, F4, F5, F10, F16, F37, F39, F45). Available in the field and not composed: that the Ode to Anactoria rests on a conjecture (F3, T gives it as a name without the hedge); that the poem is incomplete, four stanzas and part of a line, its ending missing (F6, F34, F40; T says it 'survives mostly intact'); the final line and the endured/dared dispute (F20, F41); the debate over the context and the wedding-song argument dismissed after Page (F11–F13, F48); the denial of the jealousy reading by many critics, with Carson's amazement and DeJean's homoeroticism (F17–F19), and the man as contrast figure (F14, F15); Devereux and Gallavotti (F21, F22); the speaker's gender fixed by the Greek and the poem as same-sex desire (F38, F43; T gives a 'beloved woman' and no gender for the speaker); Longinus's verdict on the combination of symptoms (F31); the metre and dialect (F8, F9); the reception beyond an offer of Catullus (F25, F26, F28, F29, F35, F42). On date the field itself differs: the Archaic period (F1) and 'the fifth century B.C.' (F36) against T's 'around the 6th century BCE'; On the Sublime is first-century (F5), first- or third-century (F30), or Roman Imperial–era (F40). T composes the jealousy reading as the poem's description and omits its contest.",
                 "LB_vs_LBA": "Admission adds a reading the field does not hold: κῆνος as the future reader facing the inscribed text, the catalogue as voice becoming text and χλωρός as papyrus, fr. 31 as the foundational text of lyric self-archiving and lyric address as temporal projection, dated in the archive from 9 November 2025, with its antecedent (Svenbro 1988) named and its claim narrowed to the deictic mechanism; and, carried as contested, the archive's disagreement on whether that reading is compatible with jealousy. It adds a re-examination of the ending the field leaves as a fragment missing its ending: the reconstruction stated as hypothesis and renumbered, the hanging-line speculation, continuous prose in the sole witness, the dialect step with its significance stated, τολματόν as an act with no doer, and the record that six instruments returned the reading they were built to produce. It adds Longinus read as a theory of transmissional inscription with a measured unnamed address, Catullus as κῆνος with the archive divided on his fourth stanza, the C = 0.688 calibration, a braided reception field, and the widest claim (the Logos with a founding document in Sappho 31) tiered by grade, with its non-claims (no linear transmission to Revelation; pan-Sapphism named as failure mode). The field's poem is kept whole and first."},
       "kernel": [
        {"K": "K1", "claim": "`A1270-01`", "source": "#1270 (t: #991, #134, #313, #1645)", "M_src": "interpretation", "sense": "κῆνος as the future reader", "qualifiers carried": "A1270-06, A1548-01", "f (source's own falsifiers)": "future evidence may confirm, modify, or refute the reconstruction (A1270-08)", "contrast": "missing referent"},
        {"K": "K2", "claim": "`A134-01`", "source": "#134", "M_src": "stipulation", "sense": "lyric address as temporal projection", "qualifiers carried": "A134-05", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K3", "claim": "`A1270-03`", "source": "#1270 (t: #283, #1645)", "M_src": "stipulation", "sense": "lyric self-archiving", "qualifiers carried": "A1548-04", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K4", "claim": "`A1054-01`", "source": "#1054 against #1270", "M_src": "interpretation (contested in the pool)", "sense": "jealousy and the future reader", "qualifiers carried": "A1270-05, A1054-03", "f (source's own falsifiers)": "—", "contrast": "contested"},
        {"K": "K5", "claim": "`A1270-02`", "source": "#1270 (t: #1484, #313)", "M_src": "interpretation", "sense": "χλωρός as papyrus substrate", "qualifiers carried": "A1484-03", "f (source's own falsifiers)": "the papyrus identification, falsifiable against the lexical record (A1484-03)", "contrast": "missing reading"},
        {"K": "K6", "claim": "`A1474-01`", "source": "#1474 (t: #1484, #1052, #1485)", "M_src": "documented", "sense": "continuous prose in the sole witness", "qualifiers carried": "A1052-01, A1485-02", "f (source's own falsifiers)": "—", "contrast": "missing evidence"},
        {"K": "K7", "claim": "`A1474-02`", "source": "#1474 (t: #1484)", "M_src": "documented", "sense": "the dialect step", "qualifiers carried": "A1484-09", "f (source's own falsifiers)": "significance conceded: 0.209, not significant alone", "contrast": "missing measurement"},
        {"K": "K8", "claim": "`A1484-05`", "source": "#1484 (t: #1475, #1478, #1052)", "M_src": "documented", "sense": "τολματόν: an act with no doer", "qualifiers carried": "A1476-02, A1482-01", "f (source's own falsifiers)": "—", "contrast": "missing grammar"},
        {"K": "K9", "claim": "`A1458-03`", "source": "#1458 (t: #1476, #1484)", "M_src": "documented", "sense": "the unnamed address after the quotation", "qualifiers carried": "A1458-08", "f (source's own falsifiers)": "—", "contrast": "missing evidence"},
        {"K": "K10", "claim": "`A1049-02`", "source": "#1049 against #1601; #576", "M_src": "interpretation (contested in the pool)", "sense": "Catullus's fourth stanza", "qualifiers carried": "A1572-01, A1601-01", "f (source's own falsifiers)": "—", "contrast": "contested"},
        {"K": "K11", "claim": "`A1484-01`", "source": "#1484 (t: #897, #828, #1532)", "M_src": "interpretation", "sense": "Sappho, mother of the Logos", "qualifiers carried": "A1484-02, A828-02, A1532-06, A1486-02", "f (source's own falsifiers)": "outer ring marked as hypothesis (A1484-02)", "contrast": "missing relation"},
        {"K": "K12", "claim": "`A1645-01`", "source": "#1645 (t: #1646)", "M_src": "interpretation", "sense": "fr. 147's horizon, fr. 31's seat", "qualifiers carried": "A1645-02, A1645-03", "f (source's own falsifiers)": "—", "contrast": "missing distinction"}]}

write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
