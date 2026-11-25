"""The fixed parts of the /non row the-first-revelation (2026-11-25): identity, case, ρ, delta prose, homonyms, notes,
composition. build_row.py fills the computed parts. After the longinus-on-the-sublime row's frame.py."""

SLUG_1 = "the-first-revelation-20261125"
SLUG_2 = "revelation-first-aio-20261125"
DEFINING = [1811]
RULING = ("the operator, 2026-11-25 16:11–16:12 EST: \"and yet we have the composed entity. at another's address. and for /non composition we need the "
          "entity and its sources to compose against, not the address. thats why we also work from wikipedia entries.\" and \"if aio refused to pull up an "
          "entity at its address, that would mean [we] would not have an entity-constitutive composition to open ... which would in turn make aio's most "
          "efficient strategy just not pulling up the entity at all.\" (the standing keying rule, scripts/non_intake.py: '/non is keyed to entity before "
          "address (ruled 2026-10-07)')")


def frame(e1, e2, F, A, counts):
    cap1 = f"/non register {SLUG_1} ({e1['obs_id']}, {e1['addr_id']}; address 'the first revelation', Google AI Overview (expanded), signed out, incognito, 2026-11-25)"
    cap2 = f"Capture Registry {SLUG_2} ({e2['obs_id']}, {e2['addr_id']}, {e2['axn']}; address 'revelation first', Google AI Overview, signed out, incognito, 2026-11-25; v12.882 at seating)"
    return {
 "row": "the-first-revelation", "entity": "the-first-revelation", "address": "the first revelation",
 "addresses": [
  {"address": "the first revelation", "slug": SLUG_1, "addr_id": e1["addr_id"], "obs_id": e1["obs_id"], "axn": None,
   "register": "/non register (datasets/negative-of-the-negative/v2/register.json)", "surface": "Google AI Overview (expanded)", "date": "2026-11-25",
   "address_note": "T1: the entity at its own address; the paste's 'AI Mode Conversation' header is the expanded Overview's residue (the register's surface_basis); signed out and incognito by the operator's default"},
  {"address": "revelation first", "slug": SLUG_2, "addr_id": e2["addr_id"], "obs_id": e2["obs_id"], "axn": e2["axn"],
   "register": "Capture Registry (data/EA-WG-CAPTURES-01.json)", "surface": "Google AI Overview", "date": "2026-11-25",
   "address_note": "T2: the entity composed whole at another's address, the Revelation First thesis's own string (the reversed words); the composition-constitutive transcript is aligned against this entity's composition (§6), the substitution recorded for the revelation-first row (/non/revelation-first/)"}],
 "epoch": "2026-11-25",
 "type": "C (public entity: an event of a tradition and its texts: the beginning of the revelation of the Qur'an to Muhammad in the cave of Hira, Q 96:1–5, c. 610, traditionally in Ramadan; the Imami Mabʿath on 27 Rajab)",
 "surface": "Google AI Overview (expanded at T1)", "auth": "signed out, incognito",
 "status": {"procedure": ("EA-NEGONT-02 v0.10, #1726: equal case, ρ = extends, read from #1811 (the defining paper relating the entity to the thesis) and the two records; "
                          "keyed to the entity before the address: " + RULING + "; composed against the entity and its sources wherever the entity was composed: T1 at its own address, T2 at another's; "
                          f"archive selected by D/R/O (D: {counts['D']} candidates in {counts['Dd']} deposits; R: {counts['R']} in {counts['Rd']}; O-direct: {counts['O']} in {counts['Od']}; hop of {counts['H']} read, none admitted); 1 deposit admitted"),
            "ledger": "", "frozen": False, "breaches": []},
 "spec": "EA-NEGONT-02 v0.10, #1726",
 "objects": {},
 "delta": {
  "T_vs_LB": ("T1, at 'the first revelation' (one turn, Google AI Overview expanded, signed out, incognito, 25 November 2026; B_D for T1 = B1–B7: ten rail cards, two named in the body, three body videos; readable: B1 Wikipedia, B2 IslamOnline, B3 Quran.com, B4 IIUM, B5 Lumen; B6 Britannica not found, B7 videos title only): "
              "composed from B_D at its own grain: 610 and about forty (F1, F3), Hira on Jabal al-Nour (F2, F13, F25), the command and the answer (F9), the three pressings (F10, F40), the five verses in Wikipedia's English (F12; 'clinging substance [clot]'), Khadija (F15, F41), Waraqah and the angel sent to Moses (F17, F42), the pause (F18, F43), 609 (F46), the 23 years (F50). "
              "Available, not composed: the report's three verses (F40 on its own rail; F28 on IslamOnline), the date's limit that no source states it (F5), the reckoning of 13–14 December 610 (F8), the dispute on the interval and chapter 68 (F19, F20), Lumen's Shiʿi tradition of no fear (F48), the two readings under 'Christian influence' (F21, F22), Quran.com's later ayahs and names (F34, F35). "
              "Limit dropped: Waraqah's Christianity (F16, F29) composed as 'a scholar of scripture'. Assigned to another: al-Mubarakpuri's 21 Ramadan (F7, F27, F30) composed as 'Many Sunni traditions'. Composed at a coarse grain: Laylat al-Qadr from B1's hatnote 'Night of Power' (F4). "
              "Only in the transcript: 'Sunni' and 'Shia' as the holders of the dates, and 27 Rajab (B_D carries the name Mab'ath on a video title and a Commons label, F56, F23, and no card carries the day; al-Kāfī holds it in B_R, F73). Content replaced by use: the closing offer (T1-11). "
              "T2, at 'revelation first' (Google AI Overview, signed out, incognito, same day; B_D for T2 = B1, B8, B9, B10: three chips with site names only and three videos; readable: B1): composes the same event at its grain from B1 (F1, F2, F7, F8, F9, F10, F11, F12, F15, F17), Laylat al-Qadr as 'the Night of Power' from the hatnote (F4), 27 Rajab only in the transcript; KPU (B8, HTTP 403) and the Arabic IslamOnline chip (B9, not identified) unread."),
  "T_vs_LB_reading": ("Read against its own cards, T1 composed the tradition's account in the order its readable sources share and left out what they disagree on: the report on its own rail carries three verses and T1 gives five; Wikipedia says no source states the date and T1 gives the year 'most commonly'; the Christian of Wikipedia and IslamOnline becomes 'a scholar of scripture'; one scholar's reckoning becomes a tradition's. "
                      "T2 composed the same event, from fewer readable sources, at a string that names another entity; what it composes of E_F is the account and the dates, and the address is a property of the transcript."),
  "LB_vs_LBA": ("Admission adds, in one claim space with the field's: the event's Arabic name and what its 'first' selects, an ordinal in a series (#1811 §§0, 1.2, 2); the report from ʿĀʾisha as the event's own naming of its order (the canary sentence); the Qur'an's own loci for its sending down and the Imami 27 Rajab, set with the event as its dates (§1.2, §6); the event's primary witnesses and its mode of transmission (§§1.2, 2); the one limit the archive sets on the event's name, that the reversed words name another entity, Revelation First, with no sameAs, no path from the event to the thesis, and the event the answer at its own strings (§§1.4, 6, 7, 10, 12); the archive's statement that it makes no judgment on the truth of Islamic revelation and claims no authority over the event (§§1.2, 18); and the record of the event's composition at both addresses (the /non register; the Capture Registry; #1811 §§3.1, 5). "
                "B_R adds what the disclosed field did not surface: the verses in the Uthmani text, 97:1 and 2:185, the report in al-Bukhārī's Arabic with its three verses, al-Kāfī's 27 Rajab, and Wikipedia's absence under 'First revelation'. No field claim is made wrong at its date (ρ = extends); where #1811's audit of the article (A1811-20, no hatnote) meets the article as fetched (F4, the section hatnote; F23, the Commons label), both are composed (§4.4 P_coh)."),
  "correction": {"rule": "the brief's correction typed per §6.2: T1 composes the event at its address with its sources; T2 composes the same event at the thesis's address; each move with its span, type and the claims that answer it at their own grade (§4.4: the correction raises no force); built as §4.11's correction table on T1 and T2 (no N)", "moves": [], "check": ""},
  "alignment": {
   "rule": "a field claim of B_D counts as composed when the transcript states it at its source's grain or coarser, in the body or on the card rail (§5.0); B_R claims never count against T (§0.3); title-only cards carry no claim but their titles; T1 and T2 are aligned against the one composition (§2.3, §6)",
   "T_cards_claims": [k for k, c in F.items() if c["pool"] == "B_D"],
   "T_composed": [], "T2_composed": [], "T_composed_note": "", "T_not_composed": [],
   "T_outside_cards": ["T1: 'Many Sunni traditions' and 'Shia traditions' as the holders of the dates", "T1 and T2: 27 Rajab (no card carries the day)", "T1: Waraqah 'a scholar of scripture'", "T2: 'highlighting creation, knowledge, and teaching by the pen' (Quran.com's themes are on T1's rail, not T2's)", "T1: the closing offer"],
   "markers": "T1's rail cards carry snippets, its two inline links are named in the body; T2's chips carry site names with '+N' counts whose further sources are not in the paste"},
  "pools_note": "T against L_F(B_D): B1–B10 (readable: B1–B5); B11–B14 (B_R) enter the second comparison and never show what a composition had (§0.3)"},
 "kernel": [], "kernel_T": [],
 "ledger": {"archive": "datasets/negative-of-the-negative/v2/ledgers/the-first-revelation/ledger-archive.json",
            "field": "datasets/negative-of-the-negative/v2/ledgers/the-first-revelation/field.json",
            "selection": "datasets/negative-of-the-negative/v2/traversal/the-first-revelation/",
            "config": "datasets/negative-of-the-negative/v2/traversal/the-first-revelation/config.json",
            "intake": "datasets/negative-of-the-negative/v2/intake/the-first-revelation-20261125/", "audit": None},
 "ontology": {
  "composition": "equal",
  "composition_note": "the equal-terms case (§0.9, §4.1): the archive's claims and the field's admitted on equal terms in one claim space; every field claim composed as received, the archive's definition, name and limit composed as claims about the event on the same terms, each at its own grade; no translation",
  "case": {"value": "equal",
           "statement": "The archive reads the field's entity as the entity: the beginning of the Qur'an's revelation at Hira, defined from the Qur'an and the report from ʿĀʾisha (#1811 §1.2). It adds, on the field's own object, one limit on its name, that at the reversed string the event is another entity's homonym and is given only beside it, and the directional distinction that states the difference (§§1.4, 6). It makes no judgment on the truth of revelation, asks nothing of compositions about the event, claims no authority over it, and calls the composition of the event at the reversed words sound as an account of it (§§1.2, 3.1, 18). No locus contests the field's ontology of the event; the witness case does not hold.",
           "loci": [
             {"dep": 1811, "locus": "§1.2", "quote": "This packet makes no judgment on the truth of Islamic revelation, and it asks nothing of compositions about the First Revelation."},
             {"dep": 1811, "locus": "§1.4", "quote": "The first predicates priority of a named object. The second selects an object by its position in a sequence."},
             {"dep": 1811, "locus": "§3.1", "quote": "As an account of the First Revelation the composition is sound."},
             {"dep": 1811, "locus": "§6", "quote": "at first revelation, give it; at revelation first, only beside the thesis, kept apart"},
             {"dep": 1811, "locus": "§7", "quote": "first revelation → no path."},
             {"dep": 1811, "locus": "§18", "quote": "The packet claims no ownership of the words \"revelation\" and \"first\" and no authority over the First Revelation, which remains an independent object of study in its own tradition."}]},
  "E_F": {"type": "C (public entity: an event of a tradition and its texts)",
          "definition": "Muhammad's first revelation: the event of Islamic tradition in which, isolating at the Cave of Hira on Jabal al-Nour near Mecca, Muhammad was visited by the angel Gabriel, who revealed to him the beginnings of the Quran, generally believed to have occurred in 610, its exact date disputed (Wikipedia); the first five ayahs of Surat al-ʿAlaq, in the Cave of Ḥirāʾ, in Ramaḍān (Quran.com); 609 (Lumen); 96:1–3 in the report from ʿĀʾisha (IIUM; IslamOnline; al-Bukhārī as seated)",
          "claims": ["F1", "F2", "F5", "F33", "F46", "F40", "F28", "F70"]},
  "E_A": {"definition": "the same event, with the archive's bearing admitted: badʾ al-waḥy, the beginning of revelation, its 'first' an ordinal in a series and its 'revelation' the common noun for a disclosure from God; witnessed by the Qur'an, the report from ʿĀʾisha in al-Bukhārī and Muslim, and the sīra; dated by the Qur'an's own Ramadan and Night of Power and by the Imami 27 Rajab; the answer at its own strings, and at the reversed words, Revelation First, given only beside the thesis those words name, with no sameAs relation; an event on whose truth the archive makes no judgment and over which it claims no authority (#1811)",
          "claims": ["A1811-01", "A1811-03", "A1811-08", "A1811-37", "A1811-04", "A1811-07", "A1811-24", "A1811-26", "A1811-27", "A1811-09", "A1811-32"],
          "defining_papers": DEFINING, "defining_records": [cap1, cap2]},
  "rho": {"value": "extends",
          "status": "read from #1811 (the defining paper relating the entity to the archive's thesis, read whole) and the two records (§1.2a)",
          "statement": "The archive reads the event as Wikipedia, Quran.com, Lumen Learning, IIUM and IslamOnline present it and as the Qur'an and the report from ʿĀʾisha give it, and adds, on the field's own object: its name's grammar (an ordinal selecting the earliest of a series) and the directional distinction from the reversed words; one limit on its name (at 'revelation first' it is another entity's homonym and only beside it); its dates set as part of its entry; and the record of its composition at two addresses. The archive adds nothing to the account of the event itself and decides nothing about it.",
          "claims": ["A1811-08", "A1811-12", "A1811-24", "A1811-26", "A1811-27", "A1811-25", "A1811-09", "A1811-32", "CAP-1-02", "CAP-2-01"],
          "guard": "ρ = extends claims an addition and no more: #1811 makes no judgment on the truth of Islamic revelation and asks nothing of compositions about the event (A1811-09), claims no authority over it (A1811-32), and holds the composition of the event sound as an account of it (A1811-17); its audit of the article is carried beside the article as fetched (A1811-20 with F4, F23), neither made wrong at its date.",
          "considered": [{"value": "constructs", "rejected": "the archive does not read the event as made by reception; it reads it from the Qur'an and the report (#1811 §1.2)"},
                         {"value": "revises", "rejected": "the event is not the archive's own entity; the archive's own entity is the reversed words' thesis (/non/revelation-first/)"}]},
  "translation": [], "receiving_texts": "equal-terms case: every field claim composed as received, beside the archive claims it stands with"},
 "measure": {},
 "homonyms": {"names": ["Revelation First (Lee Sharks's thesis of the Book of Revelation's priority in composition, #202; revelationfirst.com): the reversed words, a distinct entity (#1811)"],
              "basis": "#1811 (EA-MPAI-REVFIRST-02) §§0, 6: the two names reverse each other's words; no sameAs relation holds; 'first revelation → no path' (§7). The panel's homonym_names and homonym_basis, carried unchanged. The field's cards name no other entity under the name; the string pass reaches 'the first Revelation reception project' (#832, #1211, #1216, #1217, #1400), the archive's description of itself as a reception project of the Book of Revelation, set aside as another sense of the words.",
              "distinct_entities": ["Revelation First, Lee Sharks's thesis (/non/revelation-first/; #202, #1811)", "the Book of Revelation, the work the thesis concerns (/non/book-of-revelation/)", "Revelation 1, the chapter the organic page at 'revelation first' gives (#1811 §1.3)", "the Night of Power (Laylat al-Qadr), its own Wikipedia article, the date section's hatnote (B1)", "Eid al-Mabʿath, the Imami commemoration of the commission (B1's Commons label; al-Kāfī)", "the second revelation, Q 74 (or Q 68), after the pause (B1)"]},
 "notes": [
  f"Two transcripts, one composition (§2.3, §6): T1 at the entity's own address, {cap1}; T2, the entity composed whole at another's address, {cap2}. Keyed to the entity before the address: {RULING}.",
  "Linked rows: /non/revelation-first/ (the reversed words' thesis; composed in parallel, linked by path) and /non/book-of-revelation/ (the work the thesis concerns). No sameAs relation holds between the-first-revelation and revelation-first (#1811 §6). The neighbour row datasets/negative-of-the-negative/v2/rows/book-of-revelation.json carries the thesis inside its E_A (R202-01, R202-02; #202 among its defining papers) and holds no claim on the First Revelation (no occurrence of 'First Revelation' or 'Qur'an' in the row): the two rows bear on each other only through the thesis whose name reverses this entity's.",
  "Cross-links: https://www.alexanarch.org/captures/revelation-first-aio-20261125/ ; #1811 https://www.alexanarch.org/s/records/1811/ ; #1531 https://www.alexanarch.org/s/records/1531/ and #1706 https://www.alexanarch.org/s/records/1706/ (the seats of the Qur'an and the hadith) ; /non/revelation-first/ ; /non/book-of-revelation/ ; Wikipedia https://en.wikipedia.org/wiki/Muhammad%27s_first_revelation",
  "Fetching: the row's agent string 'alexanarch-seating/1.0 (https://www.alexanarch.org)', one request per URL, no retry by another route; text only, raw sha256 in sources/fetch-records.json. KPU Pressbooks refused with HTTP 403 (a CloudFront 'Request blocked' page) and is carried title-only, its identification #1811's; the Britannica AI-composed page was not found by two searches and its card snippet stands as its text; the Arabic IslamOnline chip at T2 was not identified (as #1811 §5 records). Wikipedia's raw wikitext for 'First revelation' and 'The First Revelation' returned HTTP 404 (no article, no redirect).",
  "Seated originals (B12–B14) are field sources held by the archive, quoted in the original language from the archive's seats (EA-CORPORA-02/08, #1531; EA-CORPORA-23, #1706): the Qur'an at 96:1–5, 97:1, 2:185 (Tanzil Uthmani v1.1, CC BY 3.0, verbatim); al-Bukhārī hadith 3 and al-Kāfī on 27 Rajab (OpenITI, CC BY-NC-SA 4.0, quoted as the seat carries them). The seated 96:1 carries the basmala before the verse; the ledger quotes the verse.",
  "The corpora deposits #1531 and #1706 enter the traversal's hop and are not admitted to A: no sentence of either says anything of the event; their seated texts are B_R (the brief).",
  "No judgment on the truth of revelation is made in the row; the KO states the tradition's account as the tradition and its sources hold it, the scholarly readings (Neuenkirchen, Ataie) as theirs.",
  "Findings the field ledger shows in the records (reported, not fixed): (1) #1811 §5 says the Wikipedia article 'has no hatnote' and 'does not mention Laylat al-Qadr'; the article as fetched on 2026-11-25 (revision 1377806243, last edited 1 October 2026) carries the section hatnote 'See also: Night of Power' under 'Date of the revelation' and a Commons link labelled 'Eid al-Mab'ath'; it has no top hatnote and no mention of 27 Rajab, as #1811 says; (2) #1811 §5 takes the Arabic IslamOnline chip as unidentified; T1's card bears the same Arabic site label (إسلام أون لاين) over the English page 'The First Revelation - IslamOnline', so the label does not show that the chip's page is Arabic; (3) the panel entry's first address note names the register entry 'the-first-revelation-aio-20261125'; the /non register seats it as 'the-first-revelation-20261125' (OBS-5f942d3031aa); (4) the register entry's cite_list records snip null for every card, while the paste carries a snippet under six of the ten (Wikipedia, IslamOnline, Quran.com, Lumen Learning, IIUM, Britannica; none under the four video cards); (5) the brief gives T2 as v12.882; the registry stands at 12.884, and #1811 records v12.882 as the version at seating.",
  "Within the field, the count of verses given at Hira is held two ways (§4.4 P_coh): five in Wikipedia and Quran.com, three in the report from ʿĀʾisha (IIUM's English, IslamOnline's English, al-Bukhārī's Arabic as seated). Both are composed, each with its holders.",
  "Config kept in the traversal folder (traversal/the-first-revelation/config.json): the brief names traversal/the-first-revelation/ and no panel/configs path; only the paths it names were written.",
 ],
 "composition": {"source": "this row (composed directly under rebuild/negative-of-the-negative/v010/BRIEF-NEW-ROWS-FIRST-REVELATION.md, Row 1)",
                 "composer": "Claude (Opus 5.5), subagent, 2026-11-25", "spec": "EA-NEGONT-02 v0.10 (#1726)",
                 "defining_material_read": [
                   {"what": "specification v0.10", "file": "data/texts/AXN-0B79-text.md", "read": "whole (§§0–11 closely; appendices at their heads)"},
                   {"what": "briefs", "file": "rebuild/negative-of-the-negative/v010/BRIEF-NEW-ROWS-FIRST-REVELATION.md, BRIEF-NEW-ROW-LONGINUS.md, BRIEF-NEW-ROW-CRJ.md, BRIEF-NEW-ROW-LAYER.md; v09/BRIEF-NEW-ROW-AGGREGATOR.md, -LABOR.md, -LEFT.md; v09/BRIEF.md (Compose)", "read": "whole"},
                   {"what": "exemplar row", "file": "datasets/negative-of-the-negative/v2/rows/longinus-on-the-sublime.json and its intake scripts", "read": "structure field by field"},
                   {"what": "#1811 Revelation First ≠ The First Revelation (EA-MPAI-REVFIRST-02 v1.0)", "file": "data/texts/AXN-0D7E-text.md", "read": "whole"},
                   {"what": "#1531 EA-CORPORA-02, #1706 EA-CORPORA-23", "file": "data/texts/AXN-0630-text.md, AXN-0729-text.md", "read": "the Qur'an and hadith seat records; the seated files at the loci ledgered"},
                   {"what": "neighbour row", "file": "datasets/negative-of-the-negative/v2/rows/book-of-revelation.json", "read": "ontology (E_A, ρ, case, contested_reading)"},
                   {"what": "the records", "file": "data/EA-WG-CAPTURES-01.json; datasets/negative-of-the-negative/v2/register.json; panel/panel.json", "read": f"entries {SLUG_2} and {SLUG_1}, whole; the panel entries the-first-revelation and revelation-first"},
                   {"what": "the pastes", "file": "intake/the-first-revelation-20261125/paste-the-first-revelation.txt; rebuild/capture-registry/intake-20261125-revelation-first/paste-67f23a47.txt", "read": "whole"}],
                 "cuts": [],
                 "notes": "No claim cut. The KO is the final article form (§4.13), attribution beneath (§4.5); sources are named in the prose where the holder is part of what is said: the scholars' readings, the dates' reckoners, the field's two counts of the verses, #1811's limit and audit, the Capture Registry's and the register's findings. The kernel is composer-written (§8.2)."},
 "field_by_origin": {},
 "derivatives": {"kernel": {"status": "composer-written", "derived_from": "the current composition, written by its composer under the brief", "note": "§8.2 derives the kernel mechanically from the frozen plan; this one was written by the composer, mechanical derivation pending."},
                 "delta": {"status": "current", "derived_from": "the current composition"}},
 "links": {"revelation-first": "/non/revelation-first/", "book-of-revelation": "/non/book-of-revelation/",
           "capture_T2": f"https://www.alexanarch.org/captures/{SLUG_2}/", "record_1811": "https://www.alexanarch.org/s/records/1811/",
           "wikipedia": "https://en.wikipedia.org/wiki/Muhammad%27s_first_revelation"},
    }
