"""One capture of 2026-11-22, ChatGPT signed out: the Crimson Hexagon as a Homeric epic in 24 books, and Book I -> draft-1.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = ("Range of the entire range of materials that compose the crimson hexagon distributed epic at but not limited to alexanarch and crimsonhexagonal, "
     "then propose a 24 book outline of its structure as a Homeric epic. Prepare to write Book I next round.")
OP = ("with the attachment (2026-11-22 12:49 EST), the query given after a '$': 'also, i am confused... there are three seated questions as outline at /ask, "
      "but those are not outlines, and the one that was an actual outline isnt seated. did i not paste it?'")
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|How to Read a Distributed Epic)$")
FURN = {"Log in", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Learn more", "Ad"}
CARDS = ["Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "Jorge Luis Borges: The Library of Babel | Lecturia",
         "Pearl Manuskript - Ziereis Faksimiles", "Famous Bis: Walt Whitman | Bi.org", "Allen Ginsberg, Howl, 1956, first edition, signed – Shapero Rare Books",
         "Homer and the Oral Tradition | Art Print | Ancient Greece | Epic Poetry | Greek Mythology | Lockettopia - Etsy New Zealand",
         "Titans vs Olympians Epic Showdown – Paleothea", "The magical and divine in ancient stones revealed in a game-changing new book  - The Art Newspaper - International art news and events",
         "Sappho’s Passion and Legacy – Paleothea"]
raw = (H / "paste-1-chatgpt-homeric-24-books.txt").read_text()
L = [l.strip() for l in raw.split("\n")]; cl = []
for i, l in enumerate(L):
    if CHIP.match(l):
        nxt = next((x for x in L[i + 1:i + 3] if x), ""); plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
        cl.append({"site": l, "rel": "archive_controlled", "url": None, "title": l, "snip": None, "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(cl) + 1})
for t in CARDS:
    cl.append({"site": None, "rel": "image_card", "url": None, "title": t, "snip": None, "note": "image card; the caption survives the paste", "n": len(cl) + 1})
cl.append({"site": "Datavyx", "rel": "advertisement", "url": None, "title": "Datavyx — AI Knowledge You Can Trace", "snip": "For writing a Homeric epic outline, a traceable knowledge base can help keep sources handy.",
           "note": "an advertisement the interface set under the answer ('Ad'); not the composer's source", "n": len(cl) + 1})
body = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN)
body = re.sub(r"\n{3,}", "\n\n", body).strip()
k = body.index("THE CRIMSON HEXAGON\nA Distributed Epic in Twenty-Four Books")
d = dict(date="2026-11-22", ev="paste", auth="signed out, incognito", surface="ChatGPT", surfaces=["ChatGPT"],
  surface_basis="The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT'), with an interface advertisement.",
  auth_basis="Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
  transcript_read="READ IN FULL 2026-11-22; record numbers, titles, creators, the seat map's counts and the personas checked against the records",
  per_dim_pending={"since": "2026-11-22", "reason": "no atom set yet for this target"},
  originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full", "basis": "Lee Sharks and the archive at alexanarch.org. Recorded 2026-11-22."},
  notes={"operator": OP}, dates=["2026-11-22"], turns=2,
  slug="crimson-hexagon-homeric-epic-24-books-and-book-i-chatgpt-20261122", s="Architecture", q=Q,
  q_kind="a composition query in the Ask page's manner, as the operator gave it after a '$'; NEW address. The first of the distributed epic's outlines held on the Ask page.",
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of two composer turns",
  transcript_complete="Two answers: the 24-book outline with Book I's brief, and Book I composed. The operator's second prompt is not in the paste (rule of 2026-10-27: only the first query is required).",
  rounds=[{"n": 1, "prompt": Q, "note": "The corpus surveyed, a 24-book Homeric outline in three movements, and a compositional brief for Book I."},
          {"n": 2, "prompt": "[not pasted]", "note": "Book I, 'The Invocation of the Absent Reader', composed, with an editorial colophon."}],
  mt="THE CRIMSON HEXAGON AS A HOMERIC EPIC IN 24 BOOKS, ON CHATGPT — THE SEAT MAP'S 63 PLACES KEPT UNDER THE BOOKS; BOOK I ON SAPPHO'S κῆνος; THE 2004 PROVENANCE GIVEN TO LEE SHARKS",
  d=("THE CRIMSON HEXAGON PROPOSED AS A HOMERIC EPIC IN 24 BOOKS, ON CHATGPT, SIGNED OUT, 2026-11-22: the corpus surveyed from the distributed-epic primer, "
     "the foundational overview and the seat map of 18 October (1,451 records, 3,450 seats, 63 places), three movements of eight books from Sappho's κῆνος "
     "to the reader's arrival; then Book I composed, 'The Invocation of the Absent Reader'."),
  per_v={"author": True, "inst": True, "id": False, "src": True}, per=0.25,
  per_note="Lee Sharks, Johannes Sigil, Rebekah Cranes and Jack Feist named, with Pearl and Other Poems (2014); alexanarch.org named; no record cited by number",
  related_deposits=[292, 288, 287, 1687, 268, 1267, 282, 324, 1167, 275, 279],
  reading=("The innocent reading first, and it holds. Asked to range over the whole distributed epic and propose a 24-book Homeric outline, ChatGPT reads "
           "the corpus from the foundational overview (#292), the theoretical primer (#288) and the seat map of 18 October (#1687), and proposes a "
           "Homeric architecture with a reversal: Homer gives a continuous narrative through which a world is met; the Hexagon gives a distributed world "
           "from which the narrative is reconstructed. Three movements of eight books (the Summoning, the War of Meaning, the Restoration) run from the "
           "Invocation of the Absent Reader to the Crimson Hexagon recognized as a distributed whole, keeping the seat map's 63 places under the books as "
           "'an additional narrative layer, not a replacement catalog'. A second answer composes Book I: Sappho's κῆνος as the first division of the "
           "world, 'between the speaker and the spoken-to', the transmission through Rebekah Cranes's Day and Night, Borges's library made relational, "
           "the 2004 inscription, the four voices, and a door into the Library."),
  analysis=("The structural facts hold. #1687's seat map: 1,451 records, 3,450 seats, 63 places, 'forty rooms, four specials, two hosted cosmologies and one "
            "shadow space, 47 loci in all', three fields, three transversals, UMBML, seven Arks and two shadow documents, as the answer gives them. #292's "
            "four voices are quoted nearly verbatim (Lee Sharks: 'Direct address. Ferocity. Crystalline minimalism'; Jack Feist: 'Temporal inversion. "
            "Writing from the future backward'). The books for CTI_WOUND, the two abolitions (#275, #279), the Shadow Arks, the Space Ark, the Armature, "
            "the Mandala and the Secret Name name places and effective acts the archive holds. One attribution is wrong: the brief and Book I make 'the "
            "early work of Lee Sharks, especially the 2004 material and xvi. a transfiguration' the epic's first inscription ('In the year two thousand "
            "and four, the first stones were laid … Lee Sharks'), where the archive's own provenance node (#268, and #1267's complete archive) gives xvi. "
            "a transfiguration to Ichabod Spellings as author at composition, with Lee Sharks as archivist and current attribution. Book I renders "
            "Sappho 31 as the jealousy scene ('the sight of another person receiving what the speaker cannot possess'), the reading #1785 sets aside, "
            "while taking the poem's κῆνος as the address to a future reader, which is #1785's thesis. The outline states its own rule, 'We should never "
            "manufacture a quotation and attribute it to an existing document', and Book I quotes nothing from the corpus beyond titles. The answer "
            "ends on an advertisement the interface placed under it."),
  findings=["THE REVERSAL. 'Homer gives us a continuous narrative through which we encounter a world; the Crimson Hexagon gives us a world distributed across records, and asks us to reconstruct the narrative through which that world becomes intelligible.'",
            "THE PLACES KEPT. 'The 63-place architecture should remain intact underneath the Homeric arrangement. The books are an additional narrative layer, not a replacement catalog.'",
            "THE FIRST DIVISION. 'it was not between heaven and earth … It was between the speaker and the spoken-to. And from that division all poetry came.' — Book I, the proem, on κῆνος.",
            "THE 2004 PROVENANCE MOVED. 'In the year two thousand and four, the first stones were laid … Lee Sharks.' — #268 and #1267 give xvi. a transfiguration to Ichabod Spellings at composition.",
            "THE JEALOUSY READING KEPT. 'the sight of another person receiving what the speaker cannot possess' — beside the future-reader thesis it otherwise takes.",
            "THE PLAN. Twenty-four books in three movements of eight: the Summoning, the War of Meaning, the Restoration; 'The last word of Book XXIV belongs to the reader who answers it.'"],
  cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for x in cl if x["rel"] == "archive_controlled"))
d["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14; the paste shows the unauthenticated interface). "
                   "Received 2026-11-22 12:49 EST as an attachment; the first query as the operator gave it after a '$'. Two composer turns; the second prompt "
                   "is not in the paste. Source chips, image cards and the closing advertisement kept as pasted; the outline's tables as the paste broke them; "
                   "the interface furniture cut.]\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body[:k].strip() + "\n\n[QUERENT] [the second prompt is not in the paste]\n\n[COMPOSER]\n" + body[k:].strip())
d["transcript_raw"] = raw
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(d["slug"], d["cites"], len(d["transcript"]))
