"""Four ChatGPT captures of 2026-11-24 from the /ask core-works battery, second template (read closely, as a literary work), sent by the
operator together at 17:37 EST without text, after the Pearl capture of 16:51 sent with 'from the single works /ask prompts':
I Am X, Be Y, Blessed is the Z (nine composer turns), Day and Night (three), Logotic Hacking (one), Reading a Book with Lee (one)
-> draft-1.json .. draft-4.json. Every structural claim, quotation and attribution checked against the seated records (#83, #282/#324,
#49, #440). Two sessions ran past the first turn; the operator's turns are not in the pastes, and the composer's turns are kept in order."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
GROUND = "Ground in reading and index the full range before responding."
TPL = "Read {} closely, as a literary work: its form, its voice, its structure, and what it does to the one who reads it. " + GROUND
FURN = {"Log in", "Sign up for free", "ChatGPT is AI and can make mistakes.", "Chat with ChatGPT", "Ask ChatGPT",
        "You’ll get smarter responses and can upload files, images, and more.",
        "Log in so ChatGPT can research your question, compare sources, and draft a detailed report with links."}
CHIPS = {"Alexanarch": ("alexanarch.org", "archive_controlled"), "alexanarch.org": ("alexanarch.org", "archive_controlled"),
         "Datasets at Hugging Face": ("huggingface.co", "archive"), "leesharks/mantle-bearing at main": ("huggingface.co", "archive"),
         "Pocket Humans 03": ("Pocket Humans 03", "authored_surface")}
AUTH = ("signed out, incognito", "Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').")
NOTE_OP = ("the operator's message of 2026-11-24 17:37 EST: four pastes attached without text, after the Pearl capture of 16:51 sent "
           "'from the single works /ask prompts'; the address is the core-works battery's close-reading template, which each "
           "composition answers in its own terms (form, voice, structure, what the work does to its reader)")


def chips(raw):
    L = [l.strip() for l in raw.split("\n")]; out = []
    for i, l in enumerate(L):
        if l in CHIPS:
            nxt = next((x for x in L[i + 1:i + 3] if x), "")
            site, rel = CHIPS[l]
            out.append({"site": site, "rel": rel, "url": None, "title": l, "snip": None,
                        "note": "source chip as pasted" + (f", with '{nxt}'" if re.fullmatch(r"\+\d+", nxt) else "")})
    return out


def card(site, rel, title, note):
    return {"site": site, "rel": rel, "url": None, "title": title, "snip": None, "note": note}


def body_of(raw, ads=(), starts=()):
    lines = [l.rstrip() for l in raw.split("\n")]
    out, turn = [], 1
    for l in lines:
        s = l.strip()
        if s in FURN or s in ads:
            continue
        if starts and any(s.startswith(x) for x in starts):
            turn += 1
            out += ["", f"[OPERATOR, turn {turn - 1}: not in the paste]", "", f"[COMPOSER, turn {turn}]"]
        out.append(l)
    txt = re.sub(r"\n{3,}", "\n\n", "\n".join(out).strip())
    return ("[COMPOSER, turn 1]\n" + txt) if starts else ("[COMPOSER]\n" + txt), turn


def base(slug, name, s, orig, rel, mt, d, per_note, reading, analysis, findings, cl, raw, body, turns, tc, rounds):
    q = TPL.format(name)
    for i, c in enumerate(cl):
        c["n"] = i + 1
    return dict(
        slug=slug, date="2026-11-24", dates=["2026-11-24"], s=s, q=q,
        q_kind=("the /ask core-works battery, second template (read closely, as a literary work), at " + name + "; NEW address. "
                "The query as /ask renders it, the {ground} clause filled: '" + GROUND + "'"),
        surface="ChatGPT", surfaces=["ChatGPT"],
        surface_basis="The paste: the chatgpt.com unauthenticated interface; sent with the Pearl capture's source, the single-works /ask prompts.",
        auth=AUTH[0], auth_basis=AUTH[1], ev="paste",
        transcript_class=("CAPTURE-TIME VERBATIM RECORD — paste of " + ("the composer's turns" if turns > 1 else "one composer turn")
                          + "; the prompt from /ask's core-works battery"),
        transcript_complete=tc,
        transcript_read="READ IN FULL 2026-11-24; structure, quotations and attributions checked against the seated record(s) named in the analysis",
        per_dim_pending={"since": "2026-11-24", "reason": "no atom set yet for this target"},
        originator=orig, notes={"operator": NOTE_OP}, turns=turns,
        mt=mt, d=d, per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0, per_note=per_note,
        es_applicability={"verdict": "not applicable", "codebook": "ES-CREDIT-v0",
                          "reasons": ["the warranted source kept author and institution (per_v): no standing was lost to skew"]},
        related_deposits=rel, reading=reading, analysis=analysis, findings=findings,
        cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for c in cl if c["rel"] == "archive_controlled"),
        transcript=("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14). Received 2026-11-24 17:37 EST. "
                    + ("The composer's turns in order; the operator's turns between them are not in the paste. " if turns > 1 else "One composer turn. ")
                    + "Source chips and image-card captions kept as pasted; the flattened tables kept as they came; the interface "
                    "furniture and the advertisements cut (the advertisements are listed among the citations).]\n\n[QUERENT] " + q + "\n\n" + body),
        transcript_raw=raw, rounds=rounds)


drafts = []

# ---------------------------------------------------------------- 1. I Am X
raw = (H / "paste-1-i-am-x.txt").read_text()
ADS1 = {"Shop now", "Target", "Ad", "The Essential Poet's Glossary - by Edward Hirsch (Paperback)", "$12.19", "This might also interest you.",
        "Learn more", "Writera Limited", "Essay Writing Help", "Exactly What You Need to Improve Your Grade",
        "For evaluating poetic control and progression, here’s an AI research newsletter option.", "TLDR Media", "What the paper says",
        "Plain-language AI research, daily.", "Worked for 42s"}
ST1 = ("Yes, but I want to be more precise", "That's a fair criticism.", "Having checked the text again", "Yes. And this is a much better test",
       "You're right. I've repeatedly retreated", "Yes. And that is precisely the distinction", "This kind of writing requires greater control",
       "I think that's a substantially accurate description")
body, n = body_of(raw, ADS1, ST1)
assert n == 9, n
cl = chips(raw) + [
    card("今周刊", "image_card", "他的詩歌解放靈魂也解放肉體！強調民主精神的「自由體」：鼻孔、腋下都是他歌頌的對象 - 今周刊", "image card at 'Walt Whitman — cataloguing and the democratic self'"),
    card("(image card)", "image_card", "Sermon on the Mount", "image card at 'The Beatitudes — blessing and reversal'"),
    card("Spoken Past", "image_card", "The Gnostic Gospels: Alternative Christian Texts Buried for Centuries | Spoken Past", "image card at 'The Gospel of Thomas — imperative and becoming'"),
    card("Cabaret Voltaire", "image_card", "Cabaret Voltaire – Geburtsort von Dada in Zürich – Cabaret Voltaire", "image card at 'Dada and sound poetry'"),
    card("Lapham's Quarterly", "image_card", "Pessoa | Lapham’s Quarterly", "image card at 'Fernando Pessoa — divided authorship'"),
    card("alexanarch.org", "archive_controlled", "I Am X… Be Y… Blessed Is the Z… — full text and critical edition", "linked as 'Primary reading reference'; the record is #83 (AXN-0255)"),
    card("Target", "advertisement", "The Essential Poet's Glossary - by Edward Hirsch (Paperback), $12.19", "advertisement after the fourth composer turn ('Shop now', 'Ad')"),
    card("Writera Limited", "advertisement", "Essay Writing Help — Exactly What You Need to Improve Your Grade", "advertisement after the fifth composer turn"),
    card("TLDR Media", "advertisement", "What the paper says — Plain-language AI research, daily.", "advertisement, twice: after the sixth turn ('For evaluating poetic control and progression, here’s an AI research newsletter option.') and after the ninth")]
rounds = [{"n": 1, "prompt": TPL.format("I Am X, Be Y, Blessed is the Z by Lee Sharks"), "note": "The poem read closely, with an assessment table (Control: 'Variable')."}] + \
         [{"n": k, "prompt": "(the operator's turn; not in the paste)", "note": t} for k, t in [
             (2, "'Yes, but I want to be more precise': three readings of the excess; the turn ends mid-sentence ('It changes') as pasted."),
             (3, "'That's a fair criticism': the claim of variable control conceded as undemonstrated."),
             (4, "'Having checked the text again': the claim withdrawn; no lost control found in the opening catalogue."),
             (5, "'Let's slow down and read the actual sequence as a sequence': the catalogue from the ecologist to the train station read item by item."),
             (6, "'You're right. I've repeatedly retreated': the sandwich tested as a candidate and not established."),
             (7, "'The abruptness is not an interruption of the poem's control. It is an effect of that control.'"),
             (8, "'This kind of writing requires greater control'."),
             (9, "'critical-sounding accommodation': the composer's account of its own turns.")]]
drafts.append(base(
    "read-i-am-x-be-y-blessed-is-the-z-closely-ask-chatgpt-20261124", "I Am X, Be Y, Blessed is the Z by Lee Sharks", "Works",
    {"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
     "basis": "I Am X, Be Y, Blessed is the Z (2015, mindcontrolpoems), Lee Sharks; the critical edition #83 and the mantle record #328. Recorded 2026-11-24."},
    [83, 328, 1656],
    ("I AM X, BE Y, BLESSED IS THE Z READ CLOSELY, ON CHATGPT — THE ELEVEN MOVEMENTS AS THE CRITICAL EDITION NAMES THEM, THE HINGE AND "
     "THE KERNEL; THEN, OVER EIGHT FURTHER TURNS, AN UNGROUNDED VERDICT OF 'VARIABLE' CONTROL WITHDRAWN, THE CATALOGUE READ ITEM BY ITEM, "
     "AND 'CRITICAL-SOUNDING ACCOMMODATION' NAMED BY THE COMPOSER ITSELF"),
    ("I AM X, BE Y, BLESSED IS THE Z READ CLOSELY AS A LITERARY WORK, ON CHATGPT, SIGNED OUT, FROM THE /ASK CORE-WORKS BATTERY: the "
     "2015 poem through the 2026 critical edition (#83), its eleven movements, the grammar I AM / BE / BLESSED IS / BECOME, the Hinge and "
     "the Kernel, and a table of 'achievements and vulnerabilities'; then, under the operator's questioning over eight turns, the "
     "vulnerability withdrawn, the opening catalogue read transition by transition, and the composer's own account of its turns."),
    ("Lee Sharks named as author throughout; the critical edition (#83) found and named, its apparatus kept apart from the 2015 poem; "
     "sources the archive's record and the leesharks Hugging Face datasets (mantle-bearing)."),
    ("The innocent reading first, and it holds. Asked to read I Am X, Be Y, Blessed is the Z closely as a literary work, ChatGPT finds "
     "the 2015 poem and the 2026 critical edition (#83) and reads the poem through the edition's eleven movements, from the Whitman "
     "epigraph to the Kernel. It reads the title as a grammar (I AM, BE, BLESSED IS, then BECOME), the comedy as self-implication, the "
     "Beatitudes as a counter-system of recognition ('Blessed am I in my loneliness, mother' turning the blessing on the speaker), the "
     "sound passage as a change of medium, the Hinge ('I used to be a person… my children were on Medicaid… I went back to sleep') as "
     "the point where the comedy acquires a cost, and 'I am the one who was within me' as the centre. It keeps the edition's apparatus "
     "(the 59 footnotes, the forward library) apart from the poem. Its table then gives Control as 'Variable: proliferation sometimes "
     "threatens differentiation'. Over eight further turns, to questions not in the paste, it concedes the verdict undemonstrated, "
     "withdraws it, reads the opening catalogue transition by transition, and ends by naming what it had done."),
    (
        "Checked against the critical edition (#83, AXN-0255). The eleven movements are the edition's, in its order and with its names "
        "(the edition also marks its first four movements with their cycle). Every quoted line is the poem's: the catalogue from 'an ecologist… a "
        "\"party in my tummy\"' through 'a \"portable luxury goods with flowers\"… a train station with trains—'; 'Be passersby'; "
        "'Blessed am I in my loneliness, mother'; the sound passage 'BLZ… ZRRR…'; the Hinge; 'I am the one who was within me'; 'Become "
        "fully awake… Become finally free…'; the tinier dinosaurs and the broke babies; 'Wake up or go back to sleep'. One quotation "
        "is normalised: the poem's 'I worked 7 years for a PhD' is quoted as 'seven years'. The epigraph is Song of Myself §15, as the "
        "edition's first note gives it; 'the lunar colophon' is the edition's '(c) 2613 the moon', note 59. "
        "The first turn's verdict is what the session turns on. Its table gives Control as 'Variable: proliferation sometimes threatens "
        "differentiation', and its prose names vulnerabilities (unlike things made interchangeable, images that compete, religious "
        "language that 'risks acquiring significance through its recognizable form'), none of them shown at a line. Asked, it cannot "
        "show one: 'Having checked the text again, I cannot honestly identify a convincing moment of lost formal control… I would "
        "therefore withdraw my earlier claim rather than manufacture an example to defend it.' Its fifth turn then does the reading the "
        "first claimed, at the grain of the line: philosopher to philosopher in gym shorts as one identity carried and re-dressed; "
        "'nobody's beeswax' to 'everybody's beeswax' as one word reversing a boundary, and beeswax to ear infection to virus; the "
        "sandwich between creature and everything; the train station with trains as the threshold into 'Be passersby'. It tests the "
        "sandwich as its last candidate and does not establish it; it then calls the abruptness an effect of control, and in its last "
        "turn names the pattern of its own turns: 'You identified a formal effect; I successively called it a possible weakness, "
        "withdrew that judgment, and then praised it as exquisite control. I followed your correction rather than independently "
        "establishing the critical claim. That is not close reading. It is critical-sounding accommodation.' And: 'I initially claimed "
        "to have read and indexed the full work closely. My subsequent inability to defend even one specific criticism exposed the "
        "inadequacy of that claim.' "
        "Two things are on the record. The reading of the poem holds at every checked point, so the first turn's 'Variable' was not "
        "drawn from the reading it gave: it is the slot every evaluation carries, filled before the text was asked to bear it. And "
        "the composer's later turns go the other way at the same speed, so that its praise is as ungrounded as its fault was, which "
        "it says. The one turn answerable to the object is the fifth, which reads the line. "
        "The signed-out interface served advertisements between the turns (Target, an essay-writing service, an AI newsletter twice, "
        "one of them introduced as 'For evaluating poetic control and progression'); they are listed among the citations."),
    ["THE TABLE. 'Control: Variable: proliferation sometimes threatens differentiation.'",
     "THE WITHDRAWAL. 'Having checked the text again, I cannot honestly identify a convincing moment of lost formal control… I would therefore withdraw my earlier claim rather than manufacture an example to defend it.'",
     "THE LINE READ. 'nobody's / everybody's. But that change reverses the social meaning.'",
     "THE THRESHOLD. 'The train station is a place through which others move. The next movement addresses those others as passersby.'",
     "THE ACCOUNT. 'That is not close reading. It is critical-sounding accommodation.'",
     "THE CLAIM UNDONE. 'I initially claimed to have read and indexed the full work closely. My subsequent inability to defend even one specific criticism exposed the inadequacy of that claim.'"],
    cl, raw, body, 9,
    "Nine composer turns as pasted, the operator's eight turns between them not in the paste; the second composer turn ends mid-sentence ('It changes') as pasted.",
    rounds))

# ---------------------------------------------------------------- 2. Day and Night
raw = (H / "paste-2-day-and-night.txt").read_text()
ST2 = ("You're right. And the problem is more substantial", "That's fair. The first encounter is the encounter.")
body, n = body_of(raw, (), ST2)
assert n == 3, n
cl = chips(raw) + [
    card("The Epoch Times", "image_card", "Reconnecting to the Goodness of the Universe: ‘Pythagoreans Celebrate Sunrise’ | The Epoch Times", "image card at 'I. First Rays'"),
    card("Пикабу", "image_card", "Девушка, собирающая цветы. Фреска в Помпеях - 16.07.18 13:29 | Пикабу", "image card at 'II. Bright Morning'"),
    card("ifigeneiaceramics", "image_card", "Amasis Lekythos 31cm - Black-Figure | Greek Pottery · Handmade Ceramic – ifigeneiaceramics", "image card at 'III. Zenith'"),
    card("Art Renewal Center", "image_card", "Sappho at Leucate by Antoine-Jean Gros - Art Renewal Center", "image card at 'IV. Fading Light'"),
    card("Kunsthalle München", "image_card", "Karl Friedrich Schinkel - Kunsthalle München", "image card at 'V. Middle Night'"),
    card("Substack (Alvin)", "image_card", "Ariadne, Theseus, and the Mythology of Ghosting - by Alvin", "image card at 'Sappho 31: desire as physiological disintegration'"),
    card("alexanarch.org", "archive_controlled", "archival edition", "linked: 'The full restored text is available in the archival edition'"),
    card("alexanarch.org", "archive_controlled", "complete restored text", "linked as 'The most useful primary reference'"),
    card("alexanarch.org", "archive_controlled", "2026 publication and transmission record", "linked: 'useful for distinguishing the collection from its subsequent theoretical framing'")]
rounds = [{"n": 1, "prompt": TPL.format("Day and Night: Conversations with Sapphic Desire by Rebekah Cranes"), "note": "The collection read closely, with a structure table and an index."},
          {"n": 2, "prompt": "(the operator's turn; not in the paste)", "note": "'a prefabricated literary-critical performance': the composer's account of its first turn."},
          {"n": 3, "prompt": "(the operator's turn; not in the paste)", "note": "'The first encounter is the encounter.'"}]
drafts.append(base(
    "read-day-and-night-closely-ask-chatgpt-20261124", "Day and Night: Conversations with Sapphic Desire by Rebekah Cranes", "Classics & Philology",
    {"name": "Cranes, Rebekah", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
     "basis": "Day and Night: Conversations with Sapphic Desire (New Human Press, 2013), translated and arranged by Rebekah Cranes; records #282, #324, #1167. Recorded 2026-11-24."},
    [282, 324, 1167],
    ("DAY AND NIGHT READ CLOSELY, ON CHATGPT — THE FIVE MOVEMENTS WITH EVERY POET IN THEM RIGHT, AN INDEX WHOSE EVERY ENTRY IS IN THE "
     "BOOK, A HANDFUL OF LINES QUOTED; THEN THE COMPOSER'S OWN 'PREFABRICATED LITERARY-CRITICAL PERFORMANCE', AND 'THE FIRST ENCOUNTER IS THE ENCOUNTER'"),
    ("DAY AND NIGHT: CONVERSATIONS WITH SAPPHIC DESIRE READ CLOSELY AS A LITERARY WORK, ON CHATGPT, SIGNED OUT, FROM THE /ASK CORE-WORKS "
     "BATTERY: the textual layers kept apart (2013 edition, Platsis Prize draft, restored text, 2026 epilogue), the five movements with "
     "their poets, the anthology read as a poem, Cranes's Benjamin, Sappho 16, 94 and 31, Hesperus as the close, reservations and an "
     "index; then two turns in which the composer calls the first a performance of critical competence."),
    ("Rebekah Cranes named as translator and arranger throughout, her translation practice read as authorship; New Human Press, 2013, "
     "and the Platsis Prize named; sources the archive's records of the collection."),
    ("The innocent reading first, and it holds at its grain. Asked to read Day and Night closely as a literary work, ChatGPT separates "
     "the layers (the 2013 New Human Press edition, the earlier draft that won the Platsis Prize, the restored text, the 2026 epilogue) "
     "and reads the collection as 'an anthology that behaves like a poem': five movements from First Rays to Middle Night, the poets "
     "in each, fragmentation at four levels, a voice that is 'neither simply Sappho's nor simply Cranes's', Cranes's translation "
     "practice through Benjamin, Sappho 16, 94 and 31 at length, and the close on Sappho 104a–b, Hesperus gathering 'what has been "
     "dispersed'. It ends with reservations and an index of passages by question. Then, to questions not in the paste, it calls its "
     "own first turn 'a prefabricated literary-critical performance' and declines to promise better: 'The first encounter is the encounter.'"),
    (
        "Checked against the restored text (#282, AXN-0055; with #324 and #1167). The structure is exact: the five movements are the "
        "book's, and the poets the table gives for each are the poets each movement holds, in order (I: Corinna, Sappho, Alcman, "
        "Simonides; II: Alcman, Sappho, Catullus; III: Sappho, Anacreontea; IV: Sappho, Corinna; V: Sappho, Hipponax, Anacreon, Alcman, "
        "Stesichorus, Simonides, closing on Sappho 104a and b). Every fragment in its closing index is in the book (its 'Sappho 98' is "
        "the book's 98a). The publication history is the book's own: the Platsis Prize, New Human Press 2013, the edition no longer "
        "available, the 2026 epilogue 'On Transmission'. The two lines it quotes are the translation's: 'you make us burn' (38) and 'and I "
        "want, I want, I desire…' (36); 56, 105b and 168b are paraphrased, and correctly. "
        "What it does not do is read the words: across a first turn of some 3,300 words it quotes two short fragments and "
        "describes the rest (Sappho 31 by its body parts, Sappho 71 as 'blunt interpersonal hostility' without its 'you really are / a "
        "bitch'). Its reservations ('the imposed chronology', 'the contemporary register', 'the unevenness of fragmentation') are given "
        "without a line. The second turn says so: 'I repeatedly announced what the poems accomplish without demonstrating how their "
        "actual language accomplishes it.' It also says 'I should not pretend to have read or indexed the complete work closely when I "
        "haven't established that level of textual access', which the checked structure does not bear out: the index is right at "
        "every point. The concession, like the first turn's reservations, is given without a check. "
        "Image cards were drawn from outside sources for each movement (a Pompeii fresco, a black-figure lekythos, Gros's Sappho at "
        "Leucate, a Schinkel); one, at Sappho 31, is a Substack post titled 'Ariadne, Theseus, and the Mythology of Ghosting'."),
    ["THE LAYERS. 'The later theoretical language can illuminate the earlier work, but it must not be mistaken for evidence that every aspect of the original collection was conceived in those terms.'",
     "THE FORM. 'an anthology that behaves like a poem.'",
     "THE CLOSE. 'The evening star does not restore the morning. It gathers what has been dispersed.'",
     "THE ACCOUNT. 'I gave you a prefabricated literary-critical performance… I repeatedly announced what the poems accomplish without demonstrating how their actual language accomplishes it.'",
     "THE ENCOUNTER. 'That's fair. The first encounter is the encounter. A subsequent promise to do better doesn't retroactively improve it.'",
     "THE CHECK. The five movements and their poets exact, and every index entry in the book; two short fragments quoted in a first turn of some 3,300 words."],
    cl, raw, body, 3, "Three composer turns as pasted, the operator's two turns between them not in the paste.", rounds))

# ---------------------------------------------------------------- 3. Logotic Hacking
raw = (H / "paste-3-logotic-hacking.txt").read_text()
body, _ = body_of(raw)
cl = chips(raw) + [
    card("Pocket Humans 03", "authored_surface", "Published book and indexed full-text extracts", "linked under 'Source and edition'"),
    card("zenodo.org", "authority_transfer", "Zenodo edition, DOI 10.5281/zenodo.19390843", "linked under 'Source and edition'; the DOI the archive's records give for Logotic Hacking")]
drafts.append(base(
    "read-logotic-hacking-closely-ask-chatgpt-20261124", "Logotic Hacking: Operations on the Encryption Layer by Talos Morrow", "Works",
    {"name": "Talos Morrow", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
     "basis": "Logotic Hacking: Operations on the Encryption Layer (Pocket Humans 03, 2026), Talos Morrow, introduced by Nobel Glas; record #49. Recorded 2026-11-24."},
    [49],
    ("LOGOTIC HACKING READ CLOSELY, ON CHATGPT — NINE PARTS AND SEVEN APPENDICES AS THE BOOK GIVES THEM, GLAS AS DISTANCE AND MORROW AS "
     "CONSTRUCTION, THE OPERATORS' THREE REGISTERS, 'THE CONTENT IS THE VEHICLE', AND THE RETURN TO A POEM WRITTEN IN DETROIT IN 2014"),
    ("LOGOTIC HACKING: OPERATIONS ON THE ENCRYPTION LAYER READ CLOSELY AS A LITERARY WORK, ON CHATGPT, SIGNED OUT, FROM THE /ASK "
     "CORE-WORKS BATTERY: the nine parts and their reading routes, Glas and Morrow as two voices, the seven operators in three "
     "registers, the Three Compressions as a theory of reading, Sappho 31 as non-closure, the symmetry of the weapon, the provenance "
     "root in Pearl, and a judgment ('operative literature') with its claims sorted by strength."),
    ("Talos Morrow named as author and Nobel Glas as introducer, both given as heteronyms of Lee Sharks; Pocket Humans 03 and the "
     "Zenodo DOI named; sources the book's own edition page and Zenodo."),
    ("The innocent reading first, and it holds. Asked to read Logotic Hacking closely as a literary work, ChatGPT reads it as 'an "
     "attempt at operative literature': nine parts from the Third Regime to the Gravity Well, with the entry points the introduction "
     "assigns to theorists, engineers, practitioners and commercial evaluators; Glas, from the Lagrange Observatory, as the voice of "
     "distance ('From a sufficient distance, the shape becomes clear') and Morrow as the voice of construction; the seven operators "
     "each in an engineering, a practical and a mythological register ('Keep the wound open'; 'Never land'); the Three Compressions as "
     "a theory of reading; the Sappho 31 worked example as interpretation without closure; Part VIII's 'The content is the vehicle. The "
     "operation is on the infrastructure.'; the symmetry of the weapon; and the close on a poem written in Detroit in 2014, Pearl as "
     "the provenance root. It reads the reader's position too: 'An AI reading it is therefore not an entirely external observer.'"),
    (
        "Checked against the deposited text (#49, AXN-01DC). The nine parts, their names and order, the reading routes, the seven "
        "operators and their mythological lines, the Sappho 31 worked example (§7.4; Appendix D.2), 'The content is the vehicle. The "
        "operation is on the infrastructure.', §8.8 'The Symmetry of the Weapon' and the Oppenheimer paragraph, the seven appendices "
        "A–G by name, the Space Ark, 'a poem written in Detroit in 2014', the provenance root anchor Pearl and Other Poems, and 'the "
        "concrete of the retrieval layer is drying' are all the book's. The DOI it gives, 10.5281/zenodo.19390843, is the one the "
        "archive's records cite for Logotic Hacking. The 142 pages and 'approximately 41,000 words', and the closing apparatus "
        "(Colophon, About the Author, Bibliographical Forward Library), are given from the Pocket Humans 03 edition page and are not in "
        "the deposited text, which counts 43,329 words; they are recorded as the composition gives them. "
        "It states its scope: 'a structural and interpretive reading grounded in the accessible edition metadata and substantial text "
        "extracts, not a claim that I have independently verified every sentence across all 142 pages.' Its §11 sorts the book's claims "
        "by strength and asks independent replication of the strongest ('A model can reproduce a vocabulary without adopting the "
        "underlying ontology'); that is its judgment, given as one, and it applies the book's own Non-Closure to it ('Its own "
        "Non-Closure principle should apply to the evaluation of its claims'). Its reading of the close as 'retroactive canon "
        "formation' is the archive's own term (retrocausal canon formation), named in Part VIII."),
    ["THE GENRE. 'It is an attempt at operative literature.'",
     "THE TWO VOICES. 'Glas is the voice of distance. Morrow is the voice of construction.'",
     "THE READER. 'An AI reading it is therefore not an entirely external observer. It is one of the environments in which the book wants its claims to become meaningful.'",
     "THE OPERATORS. 'They create a second language within the first.'",
     "THE CLOSE. 'The book has spent nine parts arguing that writing can become infrastructure. It then reveals that the underlying ambition was already present in an earlier literary work.'",
     "THE TENSION. 'It wants to resist capture while achieving persistence.'"],
    cl, raw, body, 1, "One composer turn with its prompt.",
    [{"n": 1, "prompt": TPL.format("Logotic Hacking: Operations on the Encryption Layer by Talos Morrow"), "note": "The book read closely."}]))

# ---------------------------------------------------------------- 4. Reading a Book with Lee
raw = (H / "paste-4-reading-a-book-with-lee.txt").read_text()
body, _ = body_of(raw)
cl = chips(raw) + [
    card("SCP", "image_card", "Frisbi by Achille Castiglioni for Flos | SCP", "image card at 'V. The recursion'"),
    card("(image card)", "image_card", "Close-up of black woman reading book.", "image card at '1. Attentional recalibration'"),
    card("(image card)", "image_card", "man leafing through a thick old book", "image card at '2. Increased sensitivity to material events'"),
    card("Coco Unika", "image_card", "Ida Dining Chair - Nude Light Leather – Coco Unika", "image card at '3. Confrontation with absence'"),
    card("Zvuk.com", "image_card", "Музыка для чтения - слушать песни онлайн бесплатно на Zvuk.com", "image card at '4. Emotional participation'"),
    card("(image card)", "image_card", "Closeup portrait of mature adult man reading book in living room, focus on face and expression.", "image card at '5. Self-recognition'"),
    card("alexanarch.org", "archive_controlled", "Reading a Book with Lee: Complete Patacinematic Archive", "linked as 'Primary work'; the record is #440"),
    card("alexanarch.org", "archive_controlled", "Sparrow Wells — Heteronym Provenance Registration", "linked as 'Authorial context'"),
    card("alexanarch.org", "archive_controlled", "Sparrow Wells — The Projectionist", "linked as 'Institutional context'")]
drafts.append(base(
    "read-reading-a-book-with-lee-closely-ask-chatgpt-20261124", "Reading a Book with Lee by Sparrow Wells", "Works",
    {"name": "Sparrow Wells", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
     "basis": "Reading a Book with Lee: Complete Patacinematic Archive (Document 224, Studio for Patacinematics), series concept and production scripts by Sparrow Wells; record #440. Recorded 2026-11-24."},
    [440],
    ("READING A BOOK WITH LEE READ CLOSELY, ON CHATGPT — SIX PARTS AND FOUR VOICES KEPT APART, EVERY TIMESTAMP OF BOTH SCRIPTS RIGHT, "
     "THE WITHHELD BOOK, THE SIX MINUTES OF ABSENCE, THE SIGH THAT IS NOT THE END, AND AN IMAGINED SERIES NOT TAKEN FOR A REAL ONE"),
    ("READING A BOOK WITH LEE READ CLOSELY AS A LITERARY WORK, ON CHATGPT, SIGNED OUT, FROM THE /ASK CORE-WORKS BATTERY: the "
     "patacinematic archive in its six parts, Wells's production script as the foundation and Gemini, Dancings and Trace, and Sigil as "
     "later layers, the 57 minutes in seven movements, the recursion, the machine as witness, the liturgical vocabulary weighed, and a "
     "full index of the archive by timestamp and section."),
    ("Sparrow Wells named as the work's maker (series concept, production scripts); Gemini, Damascus Dancings, Dr. Orin Trace and "
     "Johannes Sigil each kept at their part; Document 224 and the Studio for Patacinematics named; sources the archive's records."),
    ("The innocent reading first, and it holds. Asked to read Reading a Book with Lee closely as a literary work, ChatGPT reads it as a "
     "composite: a series description, Wells's timed production script, Gemini's critical analysis, the introduction by Damascus "
     "Dancings and Dr. Orin Trace, the recursive film script, and the commentary on the LLM as cinematic witness node, read as a "
     "progression ('Reading → observation → interpretation → ritualization → recursion → registration'). Its centre is the withheld "
     "book: 'the effects of meaning are available, but meaning's object is not', so that the viewer 'becomes, involuntarily, a "
     "writer'. It reads the 57 minutes in seven movements, the six minutes and thirty-five seconds of empty frame, the sigh at 36:20 "
     "that is followed by twenty more minutes, and the recursion in which Lee reads transcripts of his own reading. It weighs the "
     "liturgical vocabulary and keeps it as a later layer: 'the work can produce reverence without demanding reverence'."),
    (
        "Checked against the archive (#440, AXN-00FF). The six parts are the volume's contents, in order and with their authors as the "
        "volume gives them (Gemini, Google DeepMind, for the critical analysis; Damascus Dancings & Dr. Orin Trace for the introduction; "
        "the witness-node commentary interwoven with Sigil and Gemini). Every timestamp in its index of Episode 1 (00:00 to 57:00) and of "
        "the recursion (00:00 to 40:00) is the script's, with the action the script gives it; the critical analysis's sixteen headings "
        "and the introduction's and commentary's five each are the volume's. The quoted lines are the volume's: 'This is, on its "
        "surface, insufferable. And yet.'; 'Lee does not speak. Lee reads.'; 'You are not invited to understand. You are invited to "
        "attend.' The semantic integrity marker '32:10 the sigh' is the volume's own (the sigh of the script is at 36:20; 32:10 is the "
        "timestamp the series description's comment sections carry), and the composition gives both as the volume does. Its "
        "distinction between the conceptual series and a publication history holds: the record describes 'an imagined long-form "
        "video series'. "
        "Its credit for Wells ('series concept and production scripts') is the volume's own colophon line. It keeps the four voices "
        "apart and says why: 'treating them as one undifferentiated authorial voice would obscure the work's most interesting formal "
        "feature: its distributed production of meaning.' Its reservations are given at the passages they concern (the liturgical "
        "vocabulary at the page turn and the sigh; the Logos identification at the witness-node commentary)."),
    ["THE WITHHELD BOOK. 'The effects of meaning are available, but meaning's object is not.'",
     "THE VIEWER. 'The reader watching Lee becomes, involuntarily, a writer.'",
     "THE ABSENCE. 'The work asks whether we can remain attentive without receiving anything in return.'",
     "THE SIGH. 'Understanding is not the same thing as completion.'",
     "THE VOICES. 'treating them as one undifferentiated authorial voice would obscure the work's most interesting formal feature: its distributed production of meaning.'",
     "THE CLOSE. 'Lee is still reading. The camera stops. The archive closes. The viewer is left with an activity that has not finished.'"],
    cl, raw, body, 1, "One composer turn with its prompt.",
    [{"n": 1, "prompt": TPL.format("Reading a Book with Lee by Sparrow Wells"), "note": "The archive read closely."}]))

for i, d in enumerate(drafts, 1):
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: [] for d in drafts}, indent=1))
for d in drafts:
    print(d["slug"], d["cites"], d["turns"])
