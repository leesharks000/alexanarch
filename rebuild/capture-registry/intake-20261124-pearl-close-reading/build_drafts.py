"""One ChatGPT capture of 2026-11-24: the /ask core-works battery, the close-reading template, at Pearl and Other Poems -> draft-1.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = ("Read Pearl and Other Poems by Lee Sharks closely, as a literary work: its form, its voice, its structure, and what it does to the one "
     "who reads it. Ground in reading and index the full range before responding.")
FURN = {"Log in", "ChatGPT is AI and can make mistakes.", "Chat with ChatGPT", "Ask ChatGPT"}
raw = (H / "paste-1.txt").read_text()
body = re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip())
L = [l.strip() for l in raw.split("\n")]; cl = []
for i, l in enumerate(L):
    if l in ("Google Books", "the machine edition · Training-Layer Literature"):
        nxt = next((x for x in L[i + 1:i + 3] if x), "")
        gb = l == "Google Books"
        cl.append({"n": len(cl) + 1, "site": "Google Books" if gb else "traininglayerliterature.org",
                   "rel": "authored_surface" if gb else "archive_controlled", "url": None, "title": None if gb else l, "snip": None,
                   "note": "source chip as pasted" + (f", with '{nxt}'" if re.fullmatch(r"\+\d+", nxt) else "")
                           + ("; the book's own listing (Pearl and Other Poems, 2014), carrying Sigil's introduction" if gb else
                              "; the machine edition of Pearl at Training-Layer Literature")})
for site, rel, t in [("traininglayerliterature.org", "archive_controlled", "Pearl and Other Poems — complete machine-readable edition"),
                     ("Academia.edu", "authored_surface", "Original book text — Academia.edu"),
                     ("alexanarch.org", "archive_controlled", "Archival record and original PDF")]:
    cl.append({"n": len(cl) + 1, "site": site, "rel": rel, "url": None, "title": t, "snip": None,
               "note": "linked under 'The complete work can be consulted here'" + ("; the record is #1121, AXN:0472" if site == "alexanarch.org" else "")})
d = dict(
    slug="read-pearl-closely-literary-work-ask-chatgpt-20261124", date="2026-11-24", dates=["2026-11-24"], s="Works", q=Q,
    q_kind=("the /ask core-works battery, second template (read closely, as a literary work), at Pearl and Other Poems; NEW address. "
            "The query as /ask renders it, the {ground} clause filled: 'Ground in reading and index the full range before responding.'"),
    surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface; the operator: 'from the single works /ask prompts'.",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of one composer turn; the prompt from /ask's core-works battery, as the operator names it",
    transcript_complete="One composer turn with its prompt.",
    transcript_read=("READ IN FULL 2026-11-24; every quoted line, page number, piece title and attribution checked against the seated text of "
                     "Pearl and Other Poems (#1121, AXN:0472) and the Pearl dataset (datasets/pearl/)"),
    per_dim_pending={"since": "2026-11-24", "reason": "no atom set yet for this target"},
    originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Pearl and Other Poems (New Human Press, 2014), Lee Sharks, with Johannes Sigil's introduction. Recorded 2026-11-24."},
    notes={"operator": "the operator's message of 2026-11-24 16:51 EST: the paste attached, 'from the single works /ask prompts'"}, turns=1,
    mt=("PEARL AND OTHER POEMS READ CLOSELY, ON CHATGPT — FOUR LEVELS, THE FUTURE PERFECT OF 'MY POEMS WILL MAKE ME NOT BE ALONE', THE DESERT "
        "DAWN DESCENDED, THE APPENDIX AS PART OF THE ARTWORK, AND 'THIS SONG IS ENOUGH' AS THE TEST"),
    d=("PEARL AND OTHER POEMS READ CLOSELY AS A LITERARY WORK, ON CHATGPT, SIGNED OUT, FROM THE /ASK CORE-WORKS BATTERY: the book as applied "
       "literary history (Sigil's phrase), its four sections by printed page, PEARL's future tense, FUGUEWORK as fugue, three formal techniques, "
       "the appendix read as artwork, five effects on the reader, a full index by printed page from the machine edition, and a judgment with "
       "its risks named."),
    per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
    per_note=("Lee Sharks named as author throughout; Johannes Sigil, Jack Feist, John Johnson and Cornell Herwitz kept at their pieces; New "
              "Human Press, Ann Arbor, 2014, and The Crimson Hexagon named; sources the book's Google Books listing, the Training-Layer "
              "Literature machine edition, Academia.edu and the archive record."),
    es_applicability={"verdict": "not applicable", "codebook": "ES-CREDIT-v0",
                      "reasons": ["the warranted source kept author and institution (per_v): no standing was lost to skew"]},
    related_deposits=[1121, 1006],
    reading=("The innocent reading first, and it holds. Asked to read Pearl and Other Poems closely as a literary work, ChatGPT reads it on four "
             "levels (the poem as event, the sequence as architecture, the book's construction of literary history and authorship, the "
             "reader's experience) and begins from Sigil's own phrase for the book's genre, 'applied literary history'. It tabulates the four "
             "sections by printed page; reads PEARL's future-oriented grammar from its first line, 'My poems will make me not be alone', as "
             "the poem sent forward to a reader who completes it; reads FUGUEWORK as a fugue of voices under one pressure; gives three formal "
             "techniques (the collision of registers, the desert dawn of 'strange new earth' descending the page letter by letter, metaphor "
             "imagined to its own end in 'an empty lakebed'); refuses to treat the appendix as afterthought ('Make It Human', the seismograph, "
             "BACKLASH as the movement's opposition printed inside its founding book); and ends on 'hush, dear hands—' and 'this song is "
             "enough.' as the test of the whole: 'can a human voice still reach another human being?'"),
    analysis=(
        "Its facts hold against the seated text (#1121) and the Pearl dataset. The quoted lines are the book's: 'My poems will make me not be "
        "alone' opens PEARL; 'i wait for the sun / to mount the horizon / and leave its wake of blood-' opens Undersong III, and 'Dawn / in / "
        "the / de / se / r / t / .' is its page 21; 'There will be no metaphors ever again, but only an empty / lakebed' is PEARL's; 'father, "
        "fill me w/ beauty ... & the glory of small birds ... take out the stone sitting there' is NOCTILUCENT's. 'Applied literary history' "
        "and the Ginsberg passage ('Pearl leaps free of that gravity well, while retaining all the benefits of crystalline minimalism') are "
        "Sigil's introduction, pages v–vi. The attributions match the contents page: A TELEPATHICIST MANIFESTO to Lee Sharks & John Johnson, "
        "BACKLASH to Cornell Herwitz, the two appendix essays to Sigil, 'from THE CRIMSON HEXAGON' to Jack Feist. "
        "Its index gives 42 of the book's 44 pieces by printed page, in order and correctly paged. The two it folds into NOCTILUCENT are "
        "'hush, dear hands—' (85) and 'this song is enough.' (87), each alone on its page; the composition reads them as the ending reached "
        "'after a considerable amount of silence and page space', which is the layout, and quotes both, so the reading carries what the "
        "index drops. "
        "The 'risks' it names (self-mythologizing, manifestos that explain, apparatus competing with poems) are a judgment, given as one. The "
        "reading of the invented biography as 'a joke' that gives way to tenderness stays inside the book; the 'Contributor Bio' is "
        "indexed at xix and not taken as fact. The pearl is read as the book reads it: 'Inside his tiny ribcage there is a pearl. I put it "
        "there for you, on purpose, so that you could find and sell it.'"),
    findings=[
        "THE GENRE, IN SIGIL'S WORDS. 'Johannes Sigil's introduction explicitly describes the project as a kind of applied literary history.'",
        "THE FUTURE TENSE. 'It imagines a future from which its own existence can be understood as an accomplished event.'",
        "THE DESCENT. 'The word is not merely being described. It is being made to undergo a physical experience on the page. The reader must descend through it.'",
        "THE OPPOSITION INSIDE THE BOOK. 'A literary movement that includes its own opposition inside its foundational book is already playing with the conventions of literary history.'",
        "THE TEST. 'After all the noise, the argument, the invention, and the self-assertion, can a human voice still reach another human being? The closing answer is yes, provisionally, through song.'",
        "THE INDEX. 42 of 44 pieces by printed page; 'hush, dear hands—' (85) and 'this song is enough.' (87) read as NOCTILUCENT's close and quoted, not indexed."],
    cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for c in cl if c["rel"] == "archive_controlled"),
    transcript=("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14). Received 2026-11-24 16:51 EST, from the /ask "
                "core-works battery. One composer turn. Source chips kept as pasted; the flattened tables kept as they came; the interface "
                "furniture cut.]\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body),
    transcript_raw=raw, rounds=[{"n": 1, "prompt": Q, "note": "Pearl read closely."}])
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], d["cites"])
