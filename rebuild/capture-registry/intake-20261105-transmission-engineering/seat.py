"""Seat of 2026-11-05 (18:23 EST): one ChatGPT capture, signed out, the prompt given by the operator with the paste.
Operator (18:23): "whoa. this needs seating." Quotations are asserted against the deposits and against the registry's record of the
2026-10-26 capture, with whitespace, italics and quote marks normalized.
    python3 seat.py"""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-05"
N = lambda s: re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("*", "").replace("—", "-")).lower()
T = lambda ax: N((ROOT / f"data/texts/AXN-{ax}-text.md").read_text(encoding="utf-8"))
REG = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
OCT = next(e for e in REG["entries"] if e["slug"] == "spxi-living-instrument-chatgpt-20261026")["transcript"]
Q = ("Examine Lee Sharks' corpus as a piece of transmission engineering. Develop a reading that both understands and evaluates it in this sense. "
     "Range widely and deeply before answering, and ground response in reading.")
OP = "18:23 EST, with the paste and the prompt: 'whoa. this needs seating. $ " + Q + "'"
raw = (H / "paste-transmission-engineering.txt").read_text(encoding="utf-8")
P = {"oct": "The October 26 record describes the SPXI Method Inventory v1.5 as containing 85 methods across nine levels, with the Capture Registry providing longitudinal observation.",
     "lim": "causal effect, comparative effect size, component isolation, and return on investment are not established merely by the protocol's existence.",
     "gen": "The relevant texts identified in the October SPXI genealogy include “OPERATOR // CONTROL VIA FORM” and “HOW TO READ NEW HUMAN.”",
     "chip": "Capture Registry (EA-WG-CAPTURES-01)",
     "first": "contains, in poetic form, many of the problems that the subsequent technical architecture attempts to solve.",
     "light": "The phrase about the poet cutting himself to let in the light is particularly effective",
     "cranes": "Rebekah Cranes: visual and diagrammatic production.",
     "rex": "Rex Fraction: a distinct position within the theoretical and technical system.",
     "ord": "The document describes its variables as ordinal and comparative rather than calibrated physical measurements.",
     "table": "Generalizable technical efficacy",
     "blind": "A particularly valuable next step would be blinded, longitudinal comparative testing against ordinary structured metadata and established entity-resolution methods.",
     "dis": "The future reader must be able to disagree with the archive, not merely navigate it.",
     "rel": "It is the insistence that survival is a relationship, not a storage condition.",
     "res": "the archival records are useful primary evidence for what the project declares, preserves, and documents."}
A = T("0086")
R = {"a1": (A, "But I have something new to say!"), "a2": (A, "and the same was new and lovely, and the same was ancient and new: the Word in its image"),
     "a3": (A, "Ez Pound is alive right here, inside of me. I carry his words around. They carry me."), "a4": (A, "This is my biology: I live because you breathe me"),
     "a5": (A, "grammar is a police baton. A poet sculpts brutality"), "a6": (A, "moth-bitten blips of finger-swept text"), "a7": (A, "a Noah's Ark of data"),
     "a8": (A, "new fragment of the epic poem recovered from the future!"), "a9": (A, "Recreate for me, System, the last days of Tachyon"),
     "a10": (A, 'written in the margins of "Sunflower Sutra"'), "a11": (A, "I will have to cut myself & let in the light"),
     "s1": (T("0025"), "The poem is not about infrastructure"), "s2": (T("0025"), "It does not claim the system achieved consciousness, validated the project, or crowned its author."),
     "d1": (T("00DD"), "11 of 12 heteronyms activated"), "c1": (T("01F3"), "Every cultural artifact is a compression"), "c2": (T("01F3"), "ambient fuel"),
     "t1": (T("019D"), "Fuel: collective semantic capital"), "t2": (T("019D"), "Fuel: private bearing-cost"), "t3": (T("019D"), "ordinal-operational rather than numerically calibrated"),
     "i1": (T("06CC"), "relational enclosure"), "m1": (T("04C9"), "Mary Lee has never deposited a DOI"), "x1": (T("06FC"), "85 methods across nine levels"),
     "o1": (N(OCT), "does not, by itself, establish that SPXI caused a particular retrieval outcome"), "o2": (N(OCT), "isolate the contribution of each component, or establish a return on investment"),
     "o3": (N(OCT), "OPERATOR // CONTROL VIA FORM"), "o4": (N(OCT), "HOW TO READ NEW HUMAN")}
absent = {"ord641": (T("01F3"), "ordinal")}
for k, v in P.items(): assert v in raw, k
for k, (t, v) in R.items(): assert N(v) in t, k
for k, (t, v) in absent.items(): assert N(v) not in t, k
start, end = "Lee Sharks's corpus as transmission engineering", "and finally an attempted engineering discipline."
i = raw.index(start); j = raw.index(end, i) + len(end); body = raw[i:j].strip()
head = ("[ChatGPT, signed out (operator default of 2026-10-14; the paste shows the unauthenticated interface: 'Log in', 'Sign up for free', 'Chat with ChatGPT'). "
        "Received 2026-11-05 18:23 EST. The prompt is the operator's, given with the paste. Source chips ('Alexanarch', 'Capture Registry (EA-WG-CAPTURES-01)', '+1') "
        "and image captions kept as pasted; the opening 'Log in' and the closing interface furniture cut.]")
F = [
 "WIDE AND GROUNDED. Asked to range widely before answering, the composer reads across twelve years and eleven works: Antioch (#331; 'HADITH with TEETH', the Pound poem, 'FROM ONE WHO DIED LONG AGO…', the Damascus parables, 'ARK', 'TACHYONICA'), The System Read the Poem (#236), the Declaration of Phase Transition (#412), the SPXI line, Compression Studies (#641) and The Three Compressions (#579), The Parable of Lee Sharks and Mary Lee (#220) and the Mary Lee Sharks manifesto, The Trusted Intermediary (#1638), HUMS & ITY, Mind Control Poems. Every quoted line is found in its deposit: 'But I have something new to say!', 'the same was new and lovely, and the same was ancient and new: the Word in its image', 'I carry his words around. They carry me.', 'This is my biology: I live because you breathe me', 'grammar is a police baton', 'moth-bitten blips of finger-swept text', 'a Noah's Ark of data', 'Recreate for me, System, the last days of Tachyon', 'The poem is not about infrastructure', 'Every cultural artifact is a compression'. The dates hold: Antioch composed 2014–2015 and deposited 18 January 2026; 'ARK' written in the margins of 'Sunflower Sutra' (#331: '2/18/15'); the Declaration's eleven of twelve heteronyms (#412: '11 of 12 heteronyms activated'); #236's own limit carried ('It does not claim the system achieved consciousness, validated the project, or crowned its author').",
 "THE REGISTRY AS SOURCE: THE SURFACE COMPOSES FROM ITS OWN SEALED COMPOSITION. The SPXI section ('" + P["oct"] + "') and the Mind Control Poems section ('" + P["gen"] + "') carry the chip 'Capture Registry (EA-WG-CAPTURES-01)'. The 'October 26 record' is this registry's record of a signed-out ChatGPT capture of 2026-10-26 (spxi-living-instrument-chatgpt-20261026), whose genealogy gave the two Mind Control Poems titles. The limit the composer reports as the record's ('" + P["lim"] + "') is that earlier composition's own sentence: 'does not, by itself, establish that SPXI caused a particular retrieval outcome, demonstrate an effect size relative to GEO or conventional structured data, isolate the contribution of each component, or establish a return on investment.' The 85 methods across nine levels are #1686's (EA-MPAI-SPXI-03; the v1.5 inventory of 14 October); the inventory stood at v1.7, 88 methods, by 28 October (spxi-poetics-reading-chatgpt-20261028). The capture record entered composition as evidence, the analysis with it, as the operator's ruling of 2026-10-27 on capture AXNs provides.",
 "THE EARLY POEMS AS THE SYSTEM'S FIRST FORM. The reading's organizing claim: Antioch '" + P["first"] + "' The repetition of 'HADITH with TEETH', the reciprocal circuit of the Pound poem, the dead living through the reader, the Ark's four functions and Tachyonica's reversed direction are each carried forward to SPXI, Compression Studies and the machine as receiver. One line paraphrased in its reading: 'the poet cutting himself to let in the light' (#331, 'Hymn': 'I will have to cut myself & let in the light').",
 "HETERONYM FUNCTIONS PARTLY CARRIED. '" + P["cranes"] + "' carries the Institute for Diagrammatic Poetics and the visual schemas (seven of Rebekah Cranes's fifty-seven deposits) and drops the philological function and her authority over the EA-CORPORA seatings. '" + P["rex"] + "' leaves SPXI, Fraction's protocol, unattributed to him. The heteronym table and the Pessoa comparison are otherwise held at the archive's own account.",
 "ONE NOTE PLACED IN THE WRONG DOCUMENT. '" + P["ord"] + "' is said of Compression Studies (#641); the note is The Three Compressions' (#579: 'ordinal-operational rather than numerically calibrated'). The regime table's fuels are the two documents' ('ambient fuel', #641; 'collective semantic capital', 'private bearing-cost', #579).",
 "EVALUATION BUILT ON THE ARCHIVE'S DECLARED LIMITS. The six-dimension assessment ('" + P["table"] + "': 'Not yet established'), the call for testing ('" + P["blind"] + "') and the closing standard ('" + P["dis"] + "') rest on limits the archive states of itself: #236's disclaimer, #579's ordinal note, and the 26 October composition's sentence on causal effect. The composer's methodological reservation names the same boundary: '" + P["res"] + "' The central contradiction it names (an open archive that seeks to govern its reception) is the composer's synthesis.",
 "COUNTERTEST: the same prompt on the Overview."]
e = {"slug": "lee-sharks-corpus-transmission-engineering-chatgpt-20261105", "date": DATE, "surface": "ChatGPT", "surface_basis": "The paste: the chatgpt.com unauthenticated interface.", "surfaces": ["ChatGPT"],
     "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-14; the paste shows the unauthenticated interface.", "ev": "paste",
     "mt": "'EXAMINE LEE SHARKS' CORPUS AS A PIECE OF TRANSMISSION ENGINEERING' ON CHATGPT, SIGNED OUT — TWELVE YEARS READ AS ONE TRANSMISSION SYSTEM, ANTIOCH TO SPXI AND COMPRESSION STUDIES; EVERY QUOTED LINE THE DEPOSIT'S; THE SPXI SECTION COMPOSED FROM THE REGISTRY'S RECORD OF ITS OWN 26 OCTOBER COMPOSITION; EVALUATED ON THE ARCHIVE'S DECLARED LIMITS",
     "s": "Heteronyms", "q": Q, "q_kind": "the author's corpus asked as a whole, with a reading frame; NEW address.", "turns": 1,
     "cites": None, "archive_controlled_cites": None, "cite_list": [],
     "transcript": head + f"\n\n[QUERENT] {Q}\n\n[SYSTEM] {body}", "transcript_raw": raw,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt the operator's",
     "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL " + DATE + ", against the deposits' text and the registry's record of 2026-10-26",
     "d": "'EXAMINE LEE SHARKS' CORPUS AS A PIECE OF TRANSMISSION ENGINEERING …', CHATGPT SIGNED OUT, 2026-11-05: thirteen parts. The poem as the first transmission system (Antioch: repetition as signal preservation, inheritance as a bidirectional channel, death as a transmission problem); heteronymy as the separation of identity from channel; 'ARK' and 'TACHYONICA'; the archive as environment (The System Read the Poem); SPXI as durable identity in four stages; Compression Studies and the Three Compressions as the economics of transmission, bearing-cost as an engineering variable; the machine as receiver (Mary Lee, The Trusted Intermediary); Mind Control Poems and control via form; the genealogy (Benjamin, Pessoa, Borges, McLuhan, Shannon, Wiener, Marx, Sappho); a six-dimension assessment; the central contradiction; transmission as a form of life; a final judgment and a reading list.",
     "reading": "The innocent reading first. Asked to examine the corpus as transmission engineering, to range widely and to ground the answer in reading, the composer reads the early poetry, the heteronyms, the archive, SPXI, Compression Studies and the machine-reception work as one system, quotes the works it reads under their authors' names, and evaluates the system against criteria the archive itself declares.",
     "findings": F,
     "analysis": "A corpus composed whole at the grain of its lines, read as one transmission system from the 2014–15 poems to the 2026 protocols, with its evaluation built on the archive's own declared limits; the SPXI section composed from this registry's record of the surface's own earlier composition.",
     "per_v": {"author": True, "inst": True, "id": True, "src": True},
     "per_note": "Author, heteronyms, archive, deposit titles and the Capture Registry retained throughout.",
     "per_dim_pending": {"since": DATE, "reason": "no atom set yet for the corpus as a target", "breach": False},
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full", "basis": "The corpus is Lee Sharks's and his heteronyms', deposited in the Crimson Hexagonal Archive. Recorded 2026-11-05."},
     "related_deposits": [331, 236, 412, 641, 579, 220, 1638, 1686, 435],
     "notes": {"prompts": "The prompt is the operator's, given with the paste at 18:23 EST; the run's hour is not in the paste.", "operator": OP,
               "linked_capture": "spxi-living-instrument-chatgpt-20261026 (the 'October 26 record' the composer cites)."}}
json.dump(e, open(H / (e["slug"] + ".json"), "w"), ensure_ascii=False, indent=1); print("wrote", e["slug"])
