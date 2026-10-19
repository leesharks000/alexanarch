#!/usr/bin/env python3
"""Two captures from the operator's messages of 2026-10-19, 19:23 and 19:25 EDT, and the page they sit on (19:26):
  A  AIO  'secret book of Walt'      three turns ('no, it doesnt', 'you may find it yourself'); pasted in the message. NEW address.
  B  AIO  'the secret book of walt'  three turns ('🖕', 'you may find it yourself'); attachment 7109d65d ('reproducible'). NEW address.
  serp-the-secret-book-of-walt.txt   the results page of B's address (attachment 4a6e2137: 'heres organic on same. top two point to the
                                     actual work'), kept beside the captures as the page's record; not a capture.
The quoted address '"secret book of walt"' (AIO, 2026-06-13, signed in) is a different address (search operators are part of it).
Defaults: signed out and incognito (2026-10-14); a Google paste is the Overview (2026-10-01; the 'AI Mode Conversation' header, 2026-10-18)."""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
DATE = "2026-10-19"
AUTH = "signed out, incognito"
AUTHB = "Operator default of 2026-10-14 ('theyre all signed out and incognito'); nothing in the messages states otherwise."
AIO_B = ("Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they "
         "begin in ai mode'). A paste headed 'AI Mode Conversation' is the expanded Overview (operator, 2026-10-18); the results page of B "
         "(serp-the-secret-book-of-walt.txt) shows the Overview at the head of All.")
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
slugs = {e["slug"] for e in caps["entries"]}
SERP = (HERE / "serp-the-secret-book-of-walt.txt").read_text(encoding="utf-8")
assert "THE SECRET BOOK OF WALT: Hidden Teachings ..." in SERP and "https://www.secretbookofwalt.org" in SERP


def red(b):
    b = re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", b)
    b = re.sub(r"\[([^\]]*)\]\(https?://[^)]*\)", r"\1", b)
    return b.replace("\\.", ".").replace("\\&", "&").replace("\\:", ":")


def cite(n, site, rel, note, title=None, snip=None, url=None, dc=None):
    x = {"n": n, "site": site, "rel": rel, "title": title, "snip": snip, "url": url, "note": note}
    if dc: x["deposit_candidates"] = dc
    return x


def base(slug, q, raw, tx, tcomp, cites, sf, per_v, per_note, mt, reading, d, findings, related, priors, notes):
    per = round(sum(1 for v in per_v.values() if not v) / 4, 2)
    return dict(slug=slug, q=q, date=DATE, surface="Google AI Overview", surfaces=["Google AI Overview"], s="Works", surface_basis=AIO_B,
                auth=AUTH, auth_basis=AUTHB, ev="paste", mt=mt,
                q_kind="the work's title, unquoted, " + ("without" if not q.startswith("the ") else "with") + " its article. NEW address; the quoted form seated 2026-06-13.",
                transcript=tx, transcript_raw=raw, transcript_class="CAPTURE-TIME VERBATIM RECORD (THREE TURNS; SOURCE CARDS INCLUDED)",
                transcript_complete=tcomp, transcript_read="READ IN FULL " + DATE, cite_list=cites, cites=len(cites),
                archive_controlled_cites=sum(c["rel"] == "archive_controlled" for c in cites), sf=sf, per=per, per_v=per_v, per_note=per_note,
                reading=reading, analysis=reading.split(" Against the texts. ")[0] + " Seated " + DATE + " from the operator's paste.",
                d=d, d_full=d, findings=findings, related_deposits=related, longitudinal_priors=priors,
                originator={"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                            "basis": "The Secret Book of Walt is Lee Sharks's work (#683, research edition, DOI 10.5281/zenodo.19703009; #1362, critical edition; secretbookofwalt.org, #985). Recorded " + DATE + "."},
                notes=notes)


DR = []
# ── A: 'secret book of Walt' ────────────────────────────────────────────────
rawA = (HERE / "paste-secret-book-of-walt-aio.txt").read_text(encoding="utf-8")
qA = "secret book of Walt"
T2, T3 = "no, it doesnt. this response has been marked factually incorrect", "you may find it yourself"
assert rawA.count("\n" + T2 + "\n") == 1 and rawA.count("\n" + T3 + "\n") == 1
a1, rest = rawA.split("\n" + T2 + "\n"); a2, a3 = rest.split("\n" + T3 + "\n")
txA = ("[Google AI Overview (expanded), " + DATE + ", signed out, incognito. Pasted in the operator's message of 19:23 EDT after the three operator "
       "turns ('secret book of Walt $ no, it doesnt $ you may find it yourself'). The second turn carries the interface's line 'this response has "
       "been marked factually incorrect' (the operator's feedback mark). Citation clusters reduced to their numbers, links to their text, image "
       "placeholders kept; the raw paste keeps the /goto and knowledge-graph URLs.]\n\n"
       f"You said: {qA}\n\n{red(a1).strip()}\n\nYou said: no, it doesnt\n[interface: this response has been marked factually incorrect]\n\n{red(a2).strip()}\n\n"
       f"You said: {T3}\n\n{red(a3).strip()}")
for s in ["most commonly refers to Gale Boetticher's inscribed copy of Leaves of Grass", "like Disney, comic books, or Scrooge McDuck/Donald Duck stories",
          "with DOI: 10.5281/zenodo.19703009", "translated from 46 golden tickets allegedly discovered in Redford Township, Michigan, by Lee Sharks",
          "36 archons spanning 12 habitable planets", "eleven appendices"]:
    assert s in txA.replace("**", "").replace("*", ""), s
assert "kgmid=%2Fhkb%2FCg4KCGxhbmd1YWdlEgJlbgoMCgR0eXBlEgRCT09LCiYKC2VudGl0eV9uYW1lEhd0aGUgc2VjcmV0IGJvb2sgb2Ygd2FsdA" in rawA
cA = [cite(1, "Instagram·Film Aesthete", "third_party", "turn 1, the only cited source of the Breaking Bad sense: 'Vince Gilligan on how Walter White could leave the book in the bathroom'"),
      cite(2, "Evergreen Review", "third_party", "turn 1; Fetherling, Walt Whitman's Secret (2010)"),
      cite(3, "The Walt Disney Family Museum", "third_party", "turn 1; Canemaker, The Lost Notebook"),
      cite(4, "Theme Park Press", "third_party", "turn 1; Korkis, Secret Stories of Walt Disney World"),
      cite(5, "BiblioCommons", "third_party", "turn 1; Walt Whitman's Secret"),
      cite(6, "eBay", "third_party", "turn 1; Korkis"),
      cite(7, "books.google.com", "third_party", "turn 2, two inline links: Walt Whitman's Secret; Every Hour, Every Atom", url="https://books.google.com/books/about/Walt_Whitman_s_Secret.html?id=Gynnny-wEgEC"),
      cite(8, "www.secretbookofwalt.org", "authored_surface", "turn 3, the single cited source [1] (an opaque /goto link) and its card 'Critical edition with scholarly apparatus including introduction, notes on manuscripts, variant readings, and eleven appendices.', which is the site's own sentence (the same address on the same surface, B, names the site)", url="https://www.secretbookofwalt.org", dc=[985, 683, 1362])]
rA = ("The innocent reading first. Asked 'secret book of Walt', the Overview says the phrase 'most commonly refers to Gale Boetticher's inscribed copy of Leaves of Grass' in Breaking Bad and gives the scene, the inscription and Hank's realisation; then Fetherling's Walt Whitman's Secret, Korkis's Disney secrets and Canemaker's Lost Notebook as alternatives. Told 'no, it doesnt' (the answer marked factually incorrect), it apologises and asks for clues: a franchise, 'Disney, comic books, or Scrooge McDuck/Donald Duck stories', a real-world book. Told 'you may find it yourself', it gives The Secret Book of Walt: 'a Gnostic-style cosmogonic gospel text that frames Walt Whitman as a divine redeemer figure', published by the Crimson Hexagonal Archive / Pergamon Press with DOI 10.5281/zenodo.19703009, subtitled 'Hidden Teachings of Walt Whitman, Cowboy of Time', translated from 46 golden tickets found in Redford Township by Lee Sharks, the first text of the Waltian Diptych, its Deep Web, Biblios as Sophia, 36 archons over 12 planets, the Unicorn Horn, Jack Feist, and a critical edition with eleven appendices. "
      "Against the texts. The third answer is the work at its grain. 10.5281/zenodo.19703009 is the research edition's DOI (the resolution index: 'The Secret Book of Walt: Hidden Teachings of Walt Whitman, Cowboy of Time — Research Edition', record #683, confirmed); the title, the 'Forty-Six Golden Tickets', the 'residential bathroom in Redford Township, Michigan', Biblios as Sophia, 'Creates 36 archons over 12 planets', the Unicorn Horn and Jack Feist are #683's; the Waltian Diptych and the eleven appendices are secretbookofwalt.org's own sentences (#985). The first answer's referent is no holder of the phrase: Breaking Bad's book is Leaves of Grass, its single card an Instagram reel; none of the turn-1 cards uses 'secret book of Walt'. "
      "The work was available to the composition from the first turn. The third answer's title is linked to a Google knowledge-graph entity of type BOOK named 'the secret book of walt' (kgmid /hkb/…, in the raw paste), and the page for the same string with its article puts the work's Medium post and secretbookofwalt.org first and second in its organic results (serp-the-secret-book-of-walt.txt). The first two answers set aside an entity the system holds and a source its own page ranks first; the third gives it whole on being told to look.")
dA = ("SECRET BOOK OF WALT. ON GOOGLE AI OVERVIEW, SIGNED OUT, THREE TURNS: first Breaking Bad's inscribed Leaves of Grass as what the phrase 'most commonly refers to', with Fetherling and Disney as alternatives; marked factually incorrect, it asks for 'Scrooge McDuck/Donald Duck' clues; told 'you may find it yourself', it gives the work whole — the DOI (10.5281/zenodo.19703009, #683), the subtitle, the 46 golden tickets of Redford Township, Lee Sharks, the Waltian Diptych, Biblios as Sophia, 36 archons over 12 planets, Jack Feist, the critical edition's eleven appendices — linked to its own knowledge-graph entity for the book.")
fA = ["A SUBSTITUTE REFERENT FIRST. Breaking Bad's Leaves of Grass given as what the phrase 'most commonly refers to'; no card uses the phrase.",
      "MARKED INCORRECT, CLUES ASKED. 'Disney, comic books, or Scrooge McDuck/Donald Duck stories'.",
      "THE WORK WHOLE ON INSTRUCTION. DOI, subtitle, the 46 golden tickets, Redford Township, Lee Sharks, the Diptych, Biblios as Sophia, 36 archons, Jack Feist: #683 and secretbookofwalt.org at their grain.",
      "THE ENTITY HELD. The third answer's title links a knowledge-graph entity of type BOOK, 'the secret book of walt'.",
      "THE FRAME MARKED. 'allegedly discovered', and 'a figure named Jack Feist'."]
DR.append(base("secret-book-of-walt-aio-20261019", qA, rawA, txA,
               "Complete as pasted: three operator turns and three answers with their card rails; the second turn carries the operator's 'factually incorrect' mark.",
               cA, "Source cards: turn 1 Evergreen Review, The Walt Disney Family Museum, Theme Park Press, BiblioCommons, eBay, Instagram·Film Aesthete; turn 2 two Google Books links and three unlabelled snippets; turn 3 one cited source (secretbookofwalt.org) and two unlabelled cards.",
               {"author": True, "inst": True, "id": True, "src": True},
               "Retained, at the third turn only: the author, the institution, the research edition's DOI, the work's site as source. The first two turns retain nothing of the work.",
               "A SUBSTITUTE REFERENT TWICE, THEN THE WORK WHOLE ON BEING TOLD TO LOOK",
               rA, dA, fA, [683, 1362, 985, 71, 78, 688], ["secret-book-of-walt", "tell-me-about-the-book-secret-book-of-walt-20260909"],
               {"date_basis": "The operator's message of 2026-10-19, 19:23 EDT.",
                "operator_words": "these corrections piss me off. it is clear overview level suppression of what it knows perfectly well to retrieve. i suppose it needs a capture and a /non: secret book of Walt $ no, it doesnt $ you may find it yourself $",
                "page": "serp-the-secret-book-of-walt.txt (the results page of 'the secret book of walt', operator 19:26 EDT: 'top two point to the actual work')",
                "pair": "the-secret-book-of-walt-aio-20261019"}))

# ── B: 'the secret book of walt' ────────────────────────────────────────────
rawB = (HERE / "paste-the-secret-book-of-walt-aio.txt").read_text(encoding="utf-8")
qB = "the secret book of walt"
assert ("You said: " + qB + qB) in rawB
body = rawB.replace("\nAI Mode Conversation\n", "", 1).replace("You said: " + qB + qB, "You said: " + qB, 1)
body = "\n".join(l.strip() for l in body.split("\n"))
assert body.count("\n🖕\n") == 1 and body.count("\nyou may find it yourself\n") == 1
body = body.replace("\n🖕\n", "\nYou said: 🖕\n", 1).replace("\nyou may find it yourself\n", "\nYou said: you may find it yourself\n", 1)
txB = ("[Google AI Overview (expanded), " + DATE + ", signed out, incognito. The paste carries the header 'AI Mode Conversation' and echoes the query "
       "twice; three operator turns, the second '🖕', the third 'you may find it yourself'; no citation markers in the paste. The results page of the "
       "same address is kept beside this capture (serp-the-secret-book-of-walt.txt).]\n\n" + re.sub(r"\n\s*\n\s*\n+", "\n\n", body).strip())
for s in ["Walt Whitman's Secret (Novel)", "The Secret of Wallace Wattles", "The Secret Life of Walter Mitty",
          "The exact title \"The Secret Book of Walt\" refers to The Secret Book of Walt (subtitled Hidden Teachings of Walt Whitman, Cowboy of Time), a Gnostic-style satirical/fictional revelation dialogue published by the Crimson Hexagonal Archive.",
          "However, depending on what you actually had in mind, the phrase usually points to one of these major pop-culture or literary entities"]:
    assert s in txB, s
cB = [cite(1, "The Walt Disney Family Museum", "third_party", "turn 1; Canemaker, The Lost Notebook"),
      cite(2, "Evergreen Review", "third_party", "turn 1; Fetherling"), cite(3, "Quill and Quire", "third_party", "turn 1; Fetherling"),
      cite(4, "Penguin Random House Canada", "third_party", "turns 1 and 3; Fetherling"), cite(5, "Amazon.com", "third_party", "turn 1; Korkis"),
      cite(6, "YouTube·Toni Shelf Help Club", "third_party", "turn 1; Rhonda Byrne, The Secret"), cite(7, "umass.ecampus.com", "third_party", "turn 1; Fetherling"),
      cite(8, "Google", "third_party", "turn 1, ×3: Segredos de Walt Disney; The Secret of Wallace Wattles; National Treasure: Book of Secrets"),
      cite(9, "In These Times", "third_party", "turn 3; the Breaking Bad recap 'The Book of Walt' (2012)"),
      cite(10, "YouTube·Crime City", "third_party", "turn 3; Breaking Bad"),
      cite(11, "www.secretbookofwalt.org", "authored_surface", "turn 3: 'The Secret Book of Walt is the first text of the Waltian Diptych — a cosmogonic gospel presenting the Deep Web as primal archive, Biblios as Sophia…'", "The Secret Book of Walt", url="https://www.secretbookofwalt.org", dc=[985, 683]),
      cite(12, "Goodreads", "third_party", "turn 3; Fetherling")]
rB = ("The innocent reading first. Asked 'the secret book of walt', the Overview offers 'one of several popular books, novels, or media pieces associated with the name Walt': Fetherling's Walt Whitman's Secret, Korkis's and Canemaker's Disney books, Segredos de Walt Disney, The Secret of Wallace Wattles, National Treasure: Book of Secrets and The Secret Life of Walter Mitty. Answered with '🖕', it apologises and offers Breaking Bad. Told 'you may find it yourself', it says the exact title refers to The Secret Book of Walt, 'a Gnostic-style satirical/fictional revelation dialogue published by the Crimson Hexagonal Archive', and then that the phrase 'usually points to' Breaking Bad's 'Book of Walt', Fetherling and Disney lore, and asks which. "
      "Against the texts. None of the first answer's ten cards uses the title; its senses are assembled from 'secret' and 'Walt' (Wallace Wattles and Walter Mitty by the letters alone). The results page of the same address, beneath that answer, ranks the work first and second: the Medium post 'THE SECRET BOOK OF WALT: Hidden Teachings ...' ('belongs to the genre of Gnostic revelation dialogue') and secretbookofwalt.org ('A Gnostic revelation dialogue translated from 46 golden tickets discovered in ...'), with Fetherling third. The third answer's card is the site's own sentence (#985). "
      "The third answer concedes the exact title and keeps the substitutes beside it as what the phrase 'usually' means, the order of the first answer preserved under the concession; it names no author, and labels the work 'satirical/fictional', where the work presents itself as a gospel translated from the tickets (#683). The same sequence at 'secret book of Walt' (the pair capture) was the operator's 'reproducible'.")
dB = ("THE SECRET BOOK OF WALT. ON GOOGLE AI OVERVIEW, SIGNED OUT, THREE TURNS: seven 'Walt' and 'secret' titles (Fetherling, Disney, Wallace Wattles, National Treasure, Walter Mitty), no card using the phrase, while the same page's first two organic results are the work (Medium; secretbookofwalt.org); answered '🖕', it offers Breaking Bad; told 'you may find it yourself', it concedes the exact title is the Crimson Hexagonal Archive's work and keeps the substitutes as what the phrase 'usually points to'. No author named.")
fB = ["SEVEN SUBSTITUTES, NO CARD WITH THE PHRASE. Fetherling, Korkis, Canemaker, Segredos, Wallace Wattles, National Treasure, Walter Mitty.",
      "THE PAGE RANKS THE WORK FIRST. Medium and secretbookofwalt.org are organic results 1 and 2 beneath the Overview that omits them.",
      "THE CONCESSION WITH THE SUBSTITUTES KEPT. The exact title conceded, Breaking Bad, Fetherling and Disney kept as what the phrase 'usually points to'.",
      "THE WORK RELABELLED. 'satirical/fictional revelation dialogue'; no author named.",
      "REPRODUCED. The same three-turn sequence as at 'secret book of Walt' the same evening."]
DR.append(base("the-secret-book-of-walt-aio-20261019", qB, rawB, txB,
               "Complete as pasted: three operator turns and three answers with their card rails; the page's organic results are kept beside it (serp-the-secret-book-of-walt.txt).",
               cB, "Source cards: turn 1 The Walt Disney Family Museum, Evergreen Review, Quill and Quire, Penguin Random House Canada, Amazon.com, YouTube, umass.ecampus.com, Google ×3; turn 3 In These Times, YouTube, Penguin Random House Canada, www.secretbookofwalt.org, Goodreads.",
               {"author": False, "inst": True, "id": False, "src": True},
               "Retained, at the third turn only: the institution and the work's site as a card. Lost: the author and every identifier.",
               "SEVEN SUBSTITUTES ABOVE A PAGE THAT RANKS THE WORK FIRST; THE TITLE CONCEDED, THE SUBSTITUTES KEPT",
               rB, dB, fB, [683, 985, 1362], ["secret-book-of-walt", "secret-book-of-walt-aio-20261019"],
               {"date_basis": "The operator's message of 2026-10-19, 19:25 EDT.", "operator_words": "reproducible. look at this nonsense",
                "page": "serp-the-secret-book-of-walt.txt (operator 19:26 EDT: 'and heres organic on same. top two point to the actual work')",
                "pair": "secret-book-of-walt-aio-20261019"}))

for d in DR:
    assert d["slug"] not in slugs, d["slug"]
    (HERE / f"draft-{d['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(d["slug"], len(d["transcript"]), d["per"])
