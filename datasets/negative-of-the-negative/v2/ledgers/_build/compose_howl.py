import json, hashlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "howl"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1-20261007/paste-ginsberg-howl-aio.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("If you'd like, I can:")[0]

KO = sents([
 [("\"Howl\", also titled \"Howl for Carl Solomon\", is a poem by Allen Ginsberg, begun in the autumn of 1954 and published in 1956 as the title poem of Howl and Other Poems.", ["F1", "F2", "F3"]),
  ("Closely associated with the Beat Generation, it was controversial at first and kept for years out of the academic canon, and it has come to be regarded as a great work of twentieth-century American literature.", ["F23", "F22"])],
 [("Ginsberg first performed Part I on 7 October 1955 at the Six Gallery, 311 Fillmore Street, San Francisco, a reading at which he was the one unknown poet among six.", ["F4", "F5", "F25", "F26"]),
  ("City Lights published the book on 1 October 1956 as number four of its Pocket Poets series, introduced by William Carlos Williams.", ["F6", "H1656-13"])],
 [("The poem runs to 112 paragraph-like lines in three parts, with a footnote, and is dedicated to Carl Solomon; the \"Rockland\" of its third part was in fact the Columbia Presbyterian Psychological Institute.", ["F10", "F7", "F8"]),
  ("Ginsberg called Part I a lament for the Lamb in America and Part III an affirmation of the Lamb, addressed to Solomon; Part II, in his words, \"names the monster of mental consciousness that preys on the Lamb\", and is about the state of industrial civilization, characterized in the poem as Moloch, on lines built from that fixed base.", ["F11", "F9", "F12", "F13"]),
  ("Ginsberg described each line as ideally a single breath unit; he began in the stepped triadic form he had taken from Williams, and his own long line, based on breath and organized by a fixed base, emerged in the middle of the typing, its catalogue adapting Walt Whitman's long line.", ["F14", "F15", "F16"])],
 [("On 25 March 1957 customs officers seized 520 copies as obscene; the bookstore manager Shig Murao and the publisher Lawrence Ferlinghetti were then arrested, and the American Civil Liberties Union took the defence.", ["F17", "F18", "F19", "F28"]),
  ("On 3 October 1957 Judge Clayton W. Horn ruled the poem not obscene, finding it of \"redeeming social importance\".", ["F20", "F21"]),
  ("A piece by Eberhart helped call national attention to the poem, and the book became one of the most renowned of the century, translated into more than twenty languages.", ["F24", "F29"])],
 [("Howl and Other Poems has also been read as Whitman's democratic multiplicity carried as ecstatic movement through lived social space, at the scale of the book, in a line of the prophetic first person that begins with Whitman.", ["H1656-06", "H1656-03", "H152-01"]),
  ("On that reading its ecstasy is a standing outside any fixed place of the self: across the three parts, the footnote and the poems that follow, the speaking position keeps changing place and scale, and the voice acts, witnessing, indicting and joining itself to the one addressed.", ["H1656-08", "H1656-07", "H1656-09"]),
  ("Read as an effective act, an aesthetic object with ontological consequence, it works as an incantation; read aloud, it becomes a participatory rite in which \"the breath is the altar\".", ["H153-02", "H153-01", "H153-03", "H153-04"]),
  ("Its catalogue form has been read as carrying the cost of bearing inside the litany, and its Moloch as an archon, in a stipulated chain of inheritance that places \"Howl\" at the prophetic voice in American English.", ["H572-01", "H683-02", "H683-01", "H1362-01"])],
 [("Howl and Other Poems is also read as an arranged book: Williams's introduction, a dedication to Kerouac, Burroughs and Cassady with the books each wrote, the address to Solomon, the long poem in parts with its footnote, and the shorter poems after it, among them \"A Supermarket in California\", where Whitman is the figure.", ["H1656-12", "H1656-13", "H1656-21"]),
  ("Williams's introduction (\"Hold back the edges of your gowns, Ladies, we are going through hell\") is read as the established master vouching for the insurgent voice.", ["H682-03", "H69-06", "H682-04"])],
 [("Pearl and Other Poems is read as reproducing that structure with deliberate precision, title long poem against title long poem and introduction against introduction, and its introduction, by a heteronym of its own author, as making the vouching recursive; an \"Elegy for 'Howl'\", in a section \"for Allen Ginsberg\", answers with the line \"The best minds of my generation expired while little more than seeds.\"", ["H69-01", "H682-02", "H69-02", "H69-04", "H69-07", "H1636-01", "H1636-02"]),
  ("The title King of May, conferred on Ginsberg by the election of Prague students in May 1965, has been specified as a mantle founded in Howl and Other Poems, and read as recognized because the work bears it; on that reading the book's magnitude cannot derive from Ginsberg's later standing, since the book is what made that standing possible.", ["H1656-02", "H333-04", "H1652-01", "H1651-02", "H1655-01", "H1656-10"]),
  ("Williams and Ginsberg form a directly attested contact pair, announced by the master's introduction, which an authorship programme names as its sharpest test not yet run.", ["H1569-01", "H1569-02", "H1575-01"])],
 [("These readings state their limits: the singularity of the book is held as a literary claim open to reading, the founding work cannot be read blind, and the book is in copyright, with no open text as a whole, which blocks the corpus tests proposed for it.", ["H1656-05", "H1656-23", "H1656-25", "H1570-02"]),
  ("The claim of succession through Ginsberg is stated as falsifiable, and as the claim of a writer no one has heard of.", ["H950-01", "H950-05"])],
])
KO_B = sents([
 [KO[0]["text"] and (KO[0]["text"], KO[0]["claims"]), (KO[1]["text"], KO[1]["claims"])],
 [(KO[2]["text"], KO[2]["claims"]), ("City Lights published the book on 1 October 1956 as number four of its Pocket Poets series.", ["F6"])],
 [(KO[4]["text"], KO[4]["claims"]), (KO[5]["text"], KO[5]["claims"]), (KO[6]["text"], KO[6]["claims"])],
 [(KO[7]["text"], KO[7]["claims"]), (KO[8]["text"], KO[8]["claims"]), (KO[9]["text"], KO[9]["claims"])],
])

P = {"title": "Howl", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field 32 claims; archive 126); not frozen",
     "entity": "The entity evolves: AIO's entity (a Beat protest poem, its trial and its canon) becomes, with the archive admitted, also an operation, Whitman's multiplicity carried as ecstatic movement, and a book that founds a line still claimed; every archive line keeps its grade (read as, specified, stated limit).",
     "lede": {"text": "is Allen Ginsberg's poem of 1954–55, published in 1956 as the title poem of Howl and Other Poems: associated with the Beat Generation, cleared in an obscenity case, and, on readings proposed and still open, the book that carried Whitman's multiplicity into ecstatic movement and founded a line.",
              "claims": ["F1", "F2", "F23", "F20", "H1656-06", "H1656-11"]},
     "sections": [
      {"icon": "🎙️", "head": "Made and heard", "items": [
        {"label": "Written", "text": "from autumn 1954.", "claims": ["F3", "F1"]},
        {"label": "First read:", "text": "Six Gallery, San Francisco, 7 October 1955; Ginsberg the one unknown of six.", "claims": ["F5", "F4", "F25", "F26"]},
        {"label": "Published:", "text": "City Lights, Pocket Poets 4, 1 October 1956; introduced by Williams.", "claims": ["F6", "H1656-13"]}]},
      {"icon": "🧱", "head": "Form", "items": [
        {"label": "Three parts and a footnote,", "text": "112 lines; by Ginsberg's gloss, the Lamb lamented, its monster named, the Lamb affirmed to Solomon in \"Rockland\"; Moloch the base of Part II.", "claims": ["F10", "F11", "F12", "F13", "F9", "F8"]},
        {"label": "The breath line:", "text": "ideally one breath a line (Ginsberg); begun in Williams's triadic form, the long breath line emerging mid-typing; the catalogue adapted from Whitman.", "claims": ["F14", "F15", "F16"]},
        {"label": "Read as an arranged book:", "text": "introduction, dedication, address, the poem in parts, shorter poems after.", "claims": ["H1656-12", "H1656-13", "H1656-21"]}]},
      {"icon": "⚖️", "head": "The trial", "items": [
        {"label": "Seized and charged,", "text": "1957: 520 copies; Murao and Ferlinghetti arrested; the ACLU defends.", "claims": ["F17", "F18", "F19", "F28"]},
        {"label": "Not obscene:", "text": "Judge Horn, 3 October 1957: \"redeeming social importance\".", "claims": ["F20", "F21"]}]},
      {"icon": "🔥", "head": "The operation (read)", "items": [
        {"label": "Read as:", "text": "Whitman's multiplicity carried as ecstatic movement; ecstasy a standing outside any fixed place of the self.", "claims": ["H1656-06", "H1656-08", "H1656-07", "H1656-03"]},
        {"label": "Read as an effective act:", "text": "an incantation; read aloud, a rite.", "claims": ["H153-01", "H153-02", "H153-04"]},
        {"label": "Moloch read as archon,", "text": "in a stipulated chain of the prophetic voice.", "claims": ["H683-02", "H683-01", "H1362-01"]}]},
      {"icon": "🌱", "head": "Carried forward", "items": [
        {"label": "Read as reproduced:", "text": "Pearl and Other Poems sets its structure, element by element, against Howl's.", "claims": ["H69-01", "H682-02", "H69-07"]},
        {"label": "\"An Elegy for 'Howl'\":", "text": "\"The best minds of my generation expired while little more than seeds.\"", "claims": ["H1636-02", "H1636-01"]},
        {"label": "King of May:", "text": "a title Prague conferred in 1965, specified as a mantle the book founds.", "claims": ["H1656-02", "H1652-01", "H1651-02", "H1656-10"]},
        {"label": "Canon:", "text": "excluded for years, now one of the century's most renowned books; 20+ languages.", "claims": ["F22", "F29", "F24"]}]},
      {"icon": "⚠️", "head": "Stated limits", "items": [
        {"label": "", "text": "Its singularity a literary claim; it cannot be read blind; in copyright, no open text as a whole.", "claims": ["H1656-05", "H1656-23", "H1656-25", "H1570-02"]}]}],
     "rail": [
      {"lineage": "The poem defined and published", "claims": ["F1", "F2", "F3", "F6"], "earliest": "B1"},
      {"lineage": "The Six Gallery reading", "claims": ["F4", "F5", "F25", "F26"], "earliest": "B1"},
      {"lineage": "Three parts and a footnote, by Ginsberg's gloss", "claims": ["F10", "F11", "F12", "F13", "F9", "F7", "F8"], "earliest": "B1"},
      {"lineage": "The breath line, from Williams and Whitman", "claims": ["F14", "F15", "F16", "F31", "F30"], "earliest": "B1"},
      {"lineage": "Seizure, trial and ruling", "claims": ["F17", "F18", "F19", "F20", "F21", "F27", "F28"], "earliest": "B1"},
      {"lineage": "Reception and canon", "claims": ["F22", "F24", "F29", "F23", "F32"], "earliest": "B1"},
      {"lineage": "Whitman's multiplicity as ecstatic movement", "claims": ["H1656-06", "H1656-03", "H1656-07", "H1656-08", "H1656-09", "H152-01"], "earliest": 152},
      {"lineage": "The effective act: incantation", "claims": ["H153-01", "H153-02", "H153-03", "H153-04"], "earliest": 153},
      {"lineage": "Catalogue form and Moloch as archon", "claims": ["H572-01", "H683-01", "H683-02", "H1362-01"], "earliest": 572},
      {"lineage": "The arranged book and its seated society", "claims": ["H1656-12", "H1656-13", "H1656-21", "H682-03", "H69-06"], "earliest": 69},
      {"lineage": "Pearl reproduces Howl's structure", "claims": ["H69-01", "H69-02", "H69-04", "H682-02", "H682-04", "H69-07"], "earliest": 69},
      {"lineage": "\"An Elegy for 'Howl'\"", "claims": ["H1636-01", "H1636-02"], "earliest": 1636},
      {"lineage": "King of May founded in Howl", "claims": ["H1656-02", "H333-04", "H1652-01", "H1651-02", "H1655-01", "H1656-10", "H1656-11"], "earliest": 1651},
      {"lineage": "Williams → Ginsberg, the contact pair", "claims": ["H1569-01", "H1569-02", "H1575-01"], "earliest": 1569},
      {"lineage": "The readings' own limits", "claims": ["H1656-05", "H1656-23", "H1656-25", "H1570-02", "H950-01", "H950-05"], "earliest": 950}]}

P_B = {"title": "Howl", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is AIO's entity at the field's full resolution.",
       "lede": {"text": "is Allen Ginsberg's poem of 1954–55, published in 1956 as the title poem of Howl and Other Poems: associated with the Beat Generation, and cleared in an obscenity case.", "claims": ["F1", "F2", "F23", "F20"]},
       "sections": [P["sections"][0] | {"items": P["sections"][0]["items"][:2] + [{"label": "Published:", "text": "City Lights, Pocket Poets 4, 1 October 1956.", "claims": ["F6"]}]},
                    P["sections"][1] | {"items": P["sections"][1]["items"][:2]},
                    P["sections"][2],
                    {"icon": "🌱", "head": "Canon", "items": [P["sections"][4]["items"][3]]}],
       "rail": P["rail"][:6]}

KOo = {"title": "Howl", "genre": "Howl encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers on the operator's instruction ('lets go ahead and write the entries for the others'); not frozen; ledger unaudited",
       "sentences": KO}
KOb = {"title": "Howl", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 2,
     "claims": ["T1 definition: 'a landmark 1955 free-verse poem and the defining literary expression of the Beat Generation'",
                "T2 the opening line quoted", "T3 'a furious protest against the conformity, materialism, and cold capitalism of 1950s America'",
                "T4 'Celebration of Outcasts'", "T5 dedication to Carl Solomon, 'whom Ginsberg met in a psychiatric hospital'",
                "T6 Parts I–III and the Footnote glossed (Moloch 'an ancient Canaanite idol'; 'Holy the bop apocalypse!')",
                "T7 first reading 7 October 1955, Six Gallery", "T8 City Lights, 1956, Howl and Other Poems",
                "T9 1957 arrests of Ferlinghetti and Murao", "T10 'redeeming social importance'; 'a major First Amendment precedent'", "T11 closer: an offer menu (sections, Whitman, the trial)"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "ginsberg-howl-20261007", "obs_id": "OBS-e47ecdda2f64"}}

row = {"row": E, "entity": E, "address": "ginsberg howl", "addresses": ["howl", "ginsberg howl"], "epoch": "2026-10-07", "type": "C (public entity)",
       "surface": "Google AI Overview", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-05, hop unread",
                  "ledger": "unaudited (§3.8: one extractor per ledger; field excerpts by WebFetch, archive quotes verified verbatim 126/126)", "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665 (Appendix B, the first traversal of Howl)",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the definition, the Six Gallery reading, the 1956 publication, the parts with Ginsberg's glosses, the dedication, and the trial and ruling (F1, F2, F4–F7, F9, F11, F12, F19–F21, F27). Available in the disclosed field and not composed: the composition date (F3), the 112 lines (F10), the Rockland referent (F8), the fixed base of Part II (F13), the breath unit and the triadic beginning (F14, F15), the Whitman long line (F16, offered only in the closing menu), the customs seizure and the ACLU (F17, F28), Eberhart's review (F24), the canon's early exclusion (F22), the translations (F29). In T and not in the field as fetched (the hidden cards are unread): 'cold capitalism' (T3), the outcasts catalogue (T4), 'met in a psychiatric hospital' (T5), Moloch as 'an ancient Canaanite idol' (T6), 'a major First Amendment precedent' (T10).",
                 "LB_vs_LBA": "Admission adds what the field does not hold: the operation (Whitman's multiplicity carried as ecstatic movement; ecstasy defined; the moving speaking position); the book read as an arranged society, with Williams's introduction as the master's vouching; the poem read as an effective act and its catalogue as bearing-cost; Moloch as archon in a stipulated chain; the afterlife in the archive (Pearl's element-by-element reproduction, the 2014 Elegy, the King of May mantle founded in the book, with standing made to follow the work); the Williams→Ginsberg contact pair as a test; and the readings' own limits (singularity a literary claim, no blind reading, copyright). The field's entity, a poem with its event history and canon, gains an operation and a line, each at its own grade."},
       "kernel": [
        {"K": "K1", "claim": "`H1656-06`", "source": "#1656", "M_src": "interpretation", "sense": "the operation", "qualifiers carried": "H1656-05", "f (source's own falsifiers)": "reading Pearl against Howl, book against book (H1652-04)", "contrast": "missing operation"},
        {"K": "K2", "claim": "`H1656-08`", "source": "#1656", "M_src": "interpretation", "sense": "ecstasy defined", "qualifiers carried": "—", "f (source's own falsifiers)": "none stated", "contrast": "missing distinction"},
        {"K": "K3", "claim": "`H1656-12`", "source": "#1656", "M_src": "documented", "sense": "the arranged book", "qualifiers carried": "H1656-13", "f (source's own falsifiers)": "none stated", "contrast": "missing distinction"},
        {"K": "K4", "claim": "`H153-01`", "source": "#153", "M_src": "interpretation", "sense": "the effective act", "qualifiers carried": "H153-02", "f (source's own falsifiers)": "none stated", "contrast": "missing operation"},
        {"K": "K5", "claim": "`H683-02`", "source": "#683 (t: #1362)", "M_src": "interpretation", "sense": "Moloch as archon", "qualifiers carried": "H683-03", "f (source's own falsifiers)": "none stated", "contrast": "missing relation"},
        {"K": "K6", "claim": "`H69-01`", "source": "#69 (t: #682)", "M_src": "interpretation", "sense": "reproduced structure", "qualifiers carried": "H69-07", "f (source's own falsifiers)": "none stated", "contrast": "missing relation"},
        {"K": "K7", "claim": "`H1636-02`", "source": "#1636", "M_src": "documented", "sense": "the 2014 elegy", "qualifiers carried": "—", "f (source's own falsifiers)": "none stated", "contrast": "missing relation"},
        {"K": "K8", "claim": "`H1652-01`", "source": "#1652 (t: #1651, #1653–#1656)", "M_src": "stipulation", "sense": "the mantle founded", "qualifiers carried": "H1652-04", "f (source's own falsifiers)": "the reader may conclude Pearl does not carry what Howl founded (H1652-04)", "contrast": "missing relation"},
        {"K": "K9", "claim": "`H1656-10`", "source": "#1656", "M_src": "interpretation", "sense": "standing follows the work", "qualifiers carried": "—", "f (source's own falsifiers)": "none stated", "contrast": "missing distinction"},
        {"K": "K10", "claim": "`H1569-02`", "source": "#1569 (t: #1572, #1575)", "M_src": "interpretation", "sense": "the contact pair as a test", "qualifiers carried": "H1569-03", "f (source's own falsifiers)": "one directly attested pair producing unannounced, sequence-kept, transformative interlock (H1572-01)", "contrast": "missing distinction"},
        {"K": "K11", "claim": "`H1656-25`", "source": "#1656 (t: #1570)", "M_src": "documented", "sense": "the copyright limit", "qualifiers carried": "H1570-02", "f (source's own falsifiers)": "—", "contrast": "missing limit"}]}

write_row(E, row, field, HERE / E / "ledger.json")
