"""One Perplexity capture of 2026-11-23: the Ask page's epic roll from the outline capture of 2026-11-22, Book XXIV -> draft-1.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = ("Based on the outline at https://www.alexanarch.org/captures/crimson-hexagon-homeric-epic-24-books-and-book-i-chatgpt-20261122/ and related "
     "materials, compose Book XXIV of the Crimson Hexagon distributed epic, ranging over additional archival materials and introducing unexpected swerves.")
OP = "the operator's message of 2026-11-23 20:34 EST ('perplexity'), the paste attached, the query at its head."
FURN = {"⠙"}


def clean(raw):
    L = [l.rstrip() for l in raw.split("\n") if l.strip() not in FURN]
    s = "\n".join(L).strip()
    s = s[len(Q):].strip() if s.startswith(Q) else s
    return re.sub(r"\n{3,}", "\n\n", s)


raw = (H / "paste-1-book-xxiv.txt").read_text(); body = clean(raw)
head = ("[Perplexity, signed out, incognito (operator default of 2026-10-14). Received 2026-11-23 20:34 EST; the surface from the operator's message "
        "('perplexity'), the query at the head of the paste. One answer, with no citation markers or source list in the paste: the works it draws on "
        "are named by title in its closing 'Archival bearings'. Its three suggested follow-ups kept at the end as pasted; a spinner glyph cut.]")
d = dict(
    slug="crimson-hexagon-epic-book-xxiv-perplexity-20261123", date="2026-11-23", dates=["2026-11-23"], s="Heteronyms", q=Q,
    q_kind=("the Ask page's epic roll (alexanarch.org/ask/: 'Based on the outline at {address} and related materials, compose Book {book} of the "
            "Crimson Hexagon distributed epic…', the outline the ChatGPT capture of 2026-11-22, book XXIV); NEW address."),
    surface="Perplexity", surfaces=["Perplexity"], surface_basis="The operator's message: 'perplexity'.",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14.", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn, the query at its head",
    transcript_complete="Complete as pasted: one answer.",
    transcript_read=("READ IN FULL 2026-11-23; the outline and its analysis checked against the capture of 2026-11-22, and every work named in "
                     "'Archival bearings' found and checked at the passages it draws on"),
    per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
    originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Lee Sharks and the Crimson Hexagon, the distributed epic of alexanarch.org. Recorded 2026-11-23."},
    notes={"operator": OP}, turns=1,
    mt=("BOOK XXIV OF THE CRIMSON HEXAGON, ON PERPLEXITY, FROM THE ASK PAGE'S OUTLINE — RECOGNITION WITHOUT CLOSURE, BOOK I'S ATTRIBUTION CORRECTED IN "
        "THE ACTION, THE LAST WORD TO THE READER"),
    d=("BOOK XXIV OF THE CRIMSON HEXAGON, ON PERPLEXITY, SIGNED OUT, 2026-11-23, FROM THE OUTLINE CAPTURE OF 2026-11-22: a proem and seven parts in "
       "which Lee Sharks returns xvi. a transfiguration to Ichabod Spellings, a superseded map is kept, the namesake company's sign catches the leak, "
       "Cleis's garden refuses explanation and the reader refuses the throne, answering 'Elsewhere'; five works named as its archival bearings."),
    per_v={"author": True, "inst": True, "id": True, "src": False}, per=0.0,
    per_note=("Lee Sharks, Ichabod Spellings, Johannes Sigil, Rebekah Cranes, Jack Feist, Rex Fraction and the Assembly named; the outline capture "
              "named by address in the query; five works named by title in 'Archival bearings', no record numbers or links in the paste"),
    related_deposits=[268, 1267, 364, 1129, 562, 1165, 560, 263, 266, 1687],
    reading=("The innocent reading first, and it holds. Asked for Book XXIV from the outline, ranging wider and swerving, Perplexity writes a concluding "
             "book of recognition rather than closure: a proem in which the last chamber leaks into a bucket; the error of Book I come home, Lee Sharks "
             "telling Ichabod Spellings 'The early stone was yours'; an old map kept because 'What sheltered the work / while it was being made / shall "
             "not be thrown away'; a messenger carrying the namesake company's sign, fed, his sign made a tray beneath the bucket; Feist and the reader "
             "kneeling at the daughter's garden; a feast without the victory screen; the reader refusing the chair ('You put the end / where I could reach "
             "it'); a perfect clean copy filed in the vault as 'PROPOSED COMPLETION. REJECTED.'; and a coda in which the reader, promised the last word, "
             "answers 'Elsewhere.' 'Archival bearings' then says which works each episode draws on and which parts are invented."),
    analysis=("Composed from the outline and grounded where it says it is. The outline is the capture of 2026-11-22: its Book XXIV, 'The Crimson Hexagon — "
              "The completed epic is recognized as a distributed whole. The reader arrives, but the work remains open to further traversal', and its "
              "plan's 'The last word of Book XXIV belongs to the reader who answers it', which the coda takes literally and turns: the reader declines the "
              "place reserved for the answer. The proem walks the outline's Books XXI–XXIII (the Armature, the Mandala, the Secret Name) and the Space Ark "
              "of XX. The attribution episode is that capture's analysis, not its composition: 'the archive's own provenance node (#268, and #1267's "
              "complete archive) gives xvi. a transfiguration to Ichabod Spellings as author at composition, with Lee Sharks as archivist and current "
              "attribution'; Perplexity read the analyst's correction and made it an action. The map is Fractal Navigation Map v5.0 (#364, Sigil; "
              "#1129, Sharks; both superseded), whose own account keeps prior versions 'as active historical layers. No prior version is invalidated', "
              "counts '11 operational rooms, 1 chamber, and 1 vault', and has the Water Giraffe as 'a semantic creature that roams where certainty "
              "wavers'; the book has the creature roam to the gutter. The garden is Cleis (#1165, Feist and Cranes) through Cranes's companion On the "
              "Architecture of Cleis (#562): 'upend jacket to find / flowers spilling out. // but mostly dirt', the 'little girl's zen garden' in 'the "
              "crack between porch and shrub', 'void space', which #562 calls 'the daughter's own taxonomy, her own compendium, assembled without "
              "instruction'; the book stages that reading as Cranes's correction of Feist ('She may have been making a garden') and declares the "
              "daughter's speech invented. The victory screen is Counter-Captions (#560, the two tiers of operative compression and witness "
              "restoration), whose 'choice to hold the dead in mind instead of accepting the score' becomes the screen turned off at the feast; the "
              "bearings decline to present that document's geopolitical allegations as verified. The claimant is the namesake company the archive "
              "distinguishes itself from: 'Not to be confused with Crimson Hexagon the data analytics company (acquired by Brandwatch, 2018)' (#263), "
              "and Borges's 'the room that should exist but never does' (#266) is the line Borges speaks. Each work is named by title, none by number or "
              "link. Its closing bearings separate the archival from the composed: 'The messenger, lunch, sign-tray, and hearing are fictional swerves, "
              "as are the leak, rejected perfect edition, and reader's refusal of enthronement.'"),
    findings=["THE CORRECTION AS ACTION. 'Do not erase the mistake, he said. / Make the correction legible beside it.' — #268 and #1267, through the outline capture's analysis.",
              "THE SUPERSEDED MAP KEPT. 'What sheltered the work / while it was being made / shall not be thrown away / because the work survived.' — #364's historical layers.",
              "THE NAMESAKE. 'For once, / something called Crimson Hexagon / caught water / without claiming to understand it.' — #263, #266.",
              "THE GARDEN. 'She may have been making a garden.' — #1165 through #562.",
              "THE CLEAN COPY. 'PROPOSED COMPLETION. / REJECTED. / AUTHORSHIP UNCERTAIN. / EFFECTS OBSERVED.'",
              "THE LAST WORD. 'You promised me the last word, / they said.' … 'Elsewhere.' — the outline's 'The last word of Book XXIV belongs to the reader who answers it.'"])
d["cite_list"] = []; d["cites"] = 0; d["archive_controlled_cites"] = 0
d["transcript"] = head + "\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body; d["transcript_raw"] = raw
d["rounds"] = [{"n": 1, "prompt": Q, "note": "One answer."}]
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], len(body))
