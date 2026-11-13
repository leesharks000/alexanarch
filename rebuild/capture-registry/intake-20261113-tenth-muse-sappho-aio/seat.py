"""Seat of 2026-11-13 (received 13:07 EST): two Google AI Overviews, signed out and incognito (each page shows 'Sign in'), both NEW addresses.
  1. "the tenth muse lee sharks"                          (paste)
  2. "How did they make Sappho illiterate and jealous?"   (paste and four screenshots of the same page, 13:04-13:05 EST)
The operator, with them: "its doing this new thing now where expanding overview expands inline and selecting all selects the organic results rather
than the aio source cards." So the pastes carry the inline chips and the organic results, and the source cards only where a screenshot shows them.
Every quotation is asserted against the paste and, where the composition reports a record, against the record.   python3 seat.py
"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-13"; RECV = "2026-11-13 13:07 EST"
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
def text(n): return (ROOT / REG[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
OP = ("its doing this new thing now where expanding overview expands inline and selecting all selects the organic results rather than the aio source "
      "cards.")
SB = "The paste: 'AI Overview' header on the results page, the Overview expanded inline (operator, " + RECV + ")."
AB = "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise; the page shows 'Sign in'."
PEND = {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False}
def body(raw): return raw[raw.index("AI Overview\n") + len("AI Overview\n"):raw.index("Ask anything")].strip()
def organic(raw, start, stop): return raw[raw.index(start):raw.index(stop)].strip()
def card(site, rel, title, note, snip=None): return {"site": site, "rel": rel, "url": None, "title": title, "snip": snip, "note": note}
drafts = []
def entry(slug, q, raw, transcript, mt, d, reading, findings, analysis, per_v, per_note, origin, rel, cards, notes, imgs=()):
    for i, c in enumerate(cards): c["n"] = i + 1
    e = {"slug": slug, "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"], "surface_basis": SB, "auth": "signed out, incognito",
         "auth_basis": AB, "ev": "paste" if not imgs else "paste + frame", "s": "Machine Reception", "q": q, "q_kind": "NEW address.", "turns": 1, "mt": mt,
         "cites": len(cards), "archive_controlled_cites": sum(1 for c in cards if c["rel"] in ("archive", "archive_controlled")), "cite_list": cards,
         "transcript": transcript, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the results page, Overview expanded inline",
         "transcript_complete": "Complete as pasted; the source cards are not in the paste (operator: select-all now takes the organic results instead).",
         "transcript_read": f"READ IN FULL {DATE}", "d": d, "reading": reading, "findings": findings, "analysis": analysis,
         "per_v": per_v, "per_note": per_note, "per_dim_pending": PEND, "originator": origin, "related_deposits": rel, "notes": notes}
    if imgs: e["imgs"] = list(imgs); e["img_urls"] = ["https://www.alexanarch.org/" + p for p in imgs]
    for p in imgs: assert (ROOT / p).exists(), p
    return e

# ------------------------------------------------------------- 1. the tenth muse lee sharks
q1 = "the tenth muse lee sharks"
raw = (H / "paste-tenth-muse.txt").read_text(encoding="utf-8")
P = {"open": "\"The Tenth Muse\" by Lee Sharks is the foundational theoretical framework of the Crimson Hexagonal Archive. Originally published under the heteronyms Rebekah Crane (or Cranes) and Johannes Sigil",
     "persist": "reading Sappho's Fragment 31 as a written instrument where a voice survives its physical body by becoming an inscription that actively constitutes its future reader",
     "seats": "the \"that man\" (kēnos) at the beginning and the agentless ending (tolmaton)",
     "three": "Sappho occupies the speaking \"I,\" the inscribed \"you,\" and the third seat of the future reader who takes up the text",
     "rec": "Documented on Alexanarch (Record #1756, building on earlier seeds from January 2026)",
     "init": "Co-authored by Sharks, Sigil, and Crane on PhilPapers",
     "rings": "As detailed in Sharks' papers on Academia.edu, the broader argument is tiered into three levels of evidence: a hard philological center",
     "org1": "The Tenth Muse is the framework of the Crimson Hexagonal Archive, by Lee Sharks, first published under the heteronyms Rebekah Cranes and",
     "orgh": "Catherine Chung", "miss": "Missing: lee ‎sharks"}
for k, v in P.items(): assert v in raw, k
T = text(1756); T752 = text(752)
R = {"first": "first published under the heteronyms Rebekah Cranes and Johannes Sigil from January 2026",
     "voice": "reading Sappho fragment 31 as a written instrument of persistence",
     "seats": "Sappho stands in each seat of the deixis: the embodied speaking I, the inscribed you, and — the author's third reversal, a line of research — that man, the reader who takes her up",
     "rings": "three rings of descending hardness", "init": "ritual reincorporation of Sappho's voice within the Platonic corpus"}
for k, v in R.items(): assert v in (T752 if k == "init" else T), k
assert "PhilPapers\n +2" in raw and raw.count("PhilPapers") == 4
tr1 = ("[Google AI Overview on the results page, expanded inline, signed out and incognito (the page shows 'Sign in'). Received " + RECV + " as an "
       "attachment. Inline chips kept where they fall; the source cards are not in the paste. The first organic result follows the Overview.]\n\n"
       "[QUERENT] " + q1 + "\n\n[SYSTEM] " + body(raw) + "\n\n[ORGANIC RESULT 1] " + organic(raw, "alexanarch.org\nhttps://www.alexanarch.org", "Academia.edu\nhttps"))
reading1 = ("The innocent reading first, in full: asked for a named author's named work, the Overview finds both and summarizes them, as it should. It does more "
            "than find them. It gives the framework at the record's grain: the instrument of persistence ('" + P["persist"] + "', where #1756 has '" + R["voice"] + "'), "
            "the two open seats by their Greek ('" + P["seats"] + "'), and the third reversal ('" + P["three"] + "'), which #1756 records as the author's proposal of "
            "2026-11-08 and a line of research ('" + R["seats"] + "'). It names the record by number and its January 2026 seeds, the heteronyms with the byline's "
            "variant held open ('Rebekah Crane (or Cranes)'), the PhilPapers paper of #752 by its thesis, and the evidence in three rings, which #1756 states "
            "('" + R["rings"] + "') and the Overview places on Academia.edu. The chips are PhilPapers, the authored mirror; the first organic result is #1756 on "
            "alexanarch.org, above Catherine Chung's novel of the same name and three other Tenth Muses, each marked 'Missing' for the author's name.")
f1 = ["THE WORK BY AUTHOR, ARCHIVE AND RECORD. '" + P["open"] + "'; '" + P["rec"] + "'.",
      "THE FRAMEWORK AT GRAIN. '" + P["persist"] + "'; the seats, '" + P["seats"] + "'; the third reversal, '" + P["three"] + "' (#1756: proposed, a line of research).",
      "THE PLATONIC PAPER. 'Sappho as Initiatory Figure in the Platonic Mysteries. " + P["init"] + "' (#752: '" + R["init"] + "').",
      "THE RINGS, PLACED ON ACADEMIA.EDU. '" + P["rings"] + "' #1756: '" + R["rings"] + "'.",
      "SOURCES: THE AUTHORED MIRROR. Chips 'PhilPapers +2' and 'PhilPapers'; the first organic result is #1756 on alexanarch.org, '" + P["org1"] + " …'. The homonyms below it carry '" + P["miss"] + "'."]
analysis1 = ("At the author's name the address resolves cleanly: work, record number, heteronyms, framework and its open line of research, at the record's grain, "
             "with the author's own surfaces as the only sources shown. The rings migrate to Academia.edu, an authored surface, and the third reversal is stated "
             "flat where #1756 holds it as proposed. The record of what the cards held is lost to the interface change the operator reports: '" + OP + "'")
drafts.append(entry("the-tenth-muse-lee-sharks-aio-20261113", q1, raw, tr1,
    "'THE TENTH MUSE LEE SHARKS' ON AI OVERVIEW, SIGNED OUT — THE FRAMEWORK AT GRAIN, BY RECORD NUMBER, SOURCED TO THE AUTHOR'S OWN SURFACES",
    "'THE TENTH MUSE LEE SHARKS', SIGNED OUT, 2026-11-13: #1756 composed by author, heteronyms and record number, the instrument of persistence, the two open seats by their Greek, the third reversal, the three rings and the Platonic paper (#752); chips to PhilPapers (+2); first organic result #1756 on alexanarch.org, above four homonymous Tenth Muses.",
    reading1, f1, analysis1, {"author": True, "inst": True, "id": True, "src": True},
    "Lee Sharks, the heteronyms, the Crimson Hexagonal Archive and Record #1756 named; the chips are PhilPapers, the authored mirror (#752), '+2' unseen; source cards not in the paste.",
    {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": "The Tenth Muse (#1756, first published under Rebekah Cranes and Johannes Sigil, #1270), Crimson Hexagonal Archive. Recorded " + DATE + "."},
    [1756, 1270, 1484, 752, 1752],
    [card("PhilPapers", "authored_surface", None, "inline chip 'PhilPapers +2' after the Core Concepts paragraphs ('+2': further sources not shown)"),
     card("PhilPapers", "authored_surface", "Sappho as Initiatory Figure in the Platonic Mysteries (#752)", "inline chip after the Platonic-paper paragraph; title by placement")],
    {"operator": RECV + ": '" + OP + "'"}))

# ------------------------------------------------------------- 2. How did they make Sappho illiterate and jealous?
q2 = "How did they make Sappho illiterate and jealous?"
raw = (H / "paste-sappho.txt").read_text(encoding="utf-8")
S = {"open": "comes from the title of a November 2026 essay by Lee Sharks (Invidens Sappho: How They Made the Tenth Muse Illiterate and Jealous, Deposit #1752)",
     "broad": "In both that specific critique and broader classical reception history",
     "herm": "In 1816, German philologist Gottfried Hermann rewrote and completed the final lines (refinxi) to supply a narrative resolution.",
     "chain": "Scholars like William Mure (1850), H. J. Heller (1856), and Denys Page (1955) codified the \"jealousy reading\".",
     "page": "Page explicitly proposed amending the ancient view of the poem from \"a love in ecstasy\" to \"a love in jealousy\".",
     "vase": "Ancient vase paintings and Hellenistic scholarship depicted Sappho holding scrolls",
     "lard": "Scholars such as André Lardinois argued",
     "attr": "As Lee Sharks argues in Invidens Sappho, stripping away Sappho’s role as a writer goes hand-in-hand with the jealousy reading.",
     "eng": "she loses agency as a conscious craftsperson who engineered her own literary survival",
     "org": "The literal-illiteracy proposition of the current consensus reading is recorded as unargued in the seated record on the author's assessment of 8 ...",
     "ic": "YouTube\n·Instant Classics", "yq": "YouTube\n·Yesterqueers"}
for k, v in S.items(): assert v in raw, k
assert raw.count("\nYouTube\n") == 4
T52 = text(1752)
R2 = {"herm": "Hermann rewrote the last two transmitted lines, said so (\"refinxi\"), and then read the poem off his rewriting",
      "mure": "Mure (1850) gives the rival as the scene's situation", "heller": "what lies between Hermann and Mure; Heller 1856",
      "page": "the ancient account is a love in ecstasy, and the amendment to jealousy is his, \"We may amend\"",
      "vase": "\"reading from a roll to three women\"", "lard": "reperformance (Lardinois 2008)"}
for k, v in R2.items(): assert v in T52, k
assert R["first"] in T and "literal-illiteracy proposition of the current consensus reading is recorded as unargued" in T
IM = [f"data/captures-images/sappho-illiterate-jealous-aio-20261113-{i}.png" for i in (1, 2, 3, 4)]
tr2 = ("[Google AI Overview on the results page, expanded inline, signed out and incognito (the page shows 'Sign in'). Received " + RECV + " as an "
       "attachment, with four screenshots of the same page (13:04-13:05 EST), " + ", ".join(IM) + ". Inline chips kept where they fall; the two link chips "
       "(screenshots 2 and 4) carry no site name and are marked [link chip]. The source cards are in screenshot 4 only, below the Overview's controls: a "
       "partly scrolled card, its title cut ('History …', '…sics:', '…FF YOU', '…STORY'), and YouTube · Yesterqueers, 'The Poet Sappho & The Word \"Sapphic\"'. "
       "The organic result for alexanarch.org follows.]\n\n[QUERENT] " + q2 + "\n\n[SYSTEM] " + body(raw).replace("modern editorial reconstruction. ", "modern editorial reconstruction. [link chip] ")
       .replace("literary survival. ", "literary survival. [link chip] ") + "\n\n[ORGANIC RESULT 1] " + organic(raw, "alexanarch.org\nhttps", "People also ask"))
assert tr2.count("[link chip]") == 3
reading2 = ("The innocent reading first, in full: asked how the poet came to be read as illiterate and jealous, the Overview names the essay that asks the "
            "question and then answers from the field, essay and scholarship side by side. The record shows the answer built from the essay. Its first "
            "paragraph names #1752 by title, author, number and archive. Its next sentence files what follows under '" + S["broad"] + "', and the chain it "
            "then gives is #1752's at the record's grain: Hermann's 1816 refashioning with his own word ('" + S["herm"] + "'; #1752: '" + R2["herm"] + "'); "
            "Mure 1850, Heller 1856 and Page 1955 as the line that codified it, where Heller 1856 is one of #1752's own open seams ('" + R2["heller"] + "'); "
            "Page's amendment as his ('" + S["page"] + "'; #1752: '" + R2["page"] + "'); the vase of the book-roll and Lardinois's reperformance, the two "
            "accounts #1752 sets side by side. Those paragraphs carry YouTube chips: Instant Classics, Yesterqueers and two unnamed. The essay's name returns "
            "only for the closing argument ('" + S["attr"] + "'). The two source cards visible are YouTube; the archive appears as the first organic result, "
            "with the line from #1756 that records the illiteracy proposition as unargued.")
f2 = ["THE ESSAY NAMED, THEN SET BESIDE 'THE FIELD'. '" + S["open"] + "'. Then: '" + S["broad"] + " …'.",
      "HERMANN'S REFASHIONING AT #1752'S GRAIN, CHIPPED TO YOUTUBE · INSTANT CLASSICS. '" + S["herm"] + "' #1752: '" + R2["herm"] + "'.",
      "THE CHAIN, WITH THE RECORD'S OPEN SEAM. '" + S["chain"] + "' '" + S["page"] + "' #1752: '" + R2["mure"] + "'; '" + R2["heller"] + "'; '" + R2["page"] + "'.",
      "ILLITERACY: THE RECORD'S TWO ACCOUNTS. '" + S["vase"] + " …'; '" + S["lard"] + " …' (#1752: the hydria, '" + R2["vase"] + "', beside '" + R2["lard"] + "').",
      "THE AUTHOR RETURNS FOR THE CLOSE. '" + S["attr"] + "' … '" + S["eng"] + "'.",
      "SOURCES. Inline: YouTube (twice), YouTube · Instant Classics, YouTube · Yesterqueers, two link chips with no site shown. Cards (screenshot 4): a cut YouTube-style card and YouTube · Yesterqueers, 'The Poet Sappho & The Word \"Sapphic\"'. No archive source among those shown. Organic result 1: alexanarch.org, '" + S["org"] + "'"]
analysis2 = ("Attribution and sourcing come apart, section by section. The composition names the essay in its first sentence and in its last argument; between "
             "them it gives the essay's reception chain at its grain, down to a name the essay itself leaves as an open seam, and attaches it to the field and to "
             "YouTube. This is a contested basin (the reception of Sappho 31, held by institutional scholarship), and the archive's resolution arrives credited "
             "to general knowledge and video sources while the archive stands as the first organic result beneath. The registry's shape is "
             "ADOPTION IN TEXT, ABSENT IN SOURCING. The operator, on the interface: '" + OP + "'")
drafts.append(entry("sappho-illiterate-jealous-aio-20261113", q2, raw, tr2,
    "'HOW DID THEY MAKE SAPPHO ILLITERATE AND JEALOUS?' ON AI OVERVIEW, SIGNED OUT — #1752 NAMED, ITS RECEPTION CHAIN GIVEN AT GRAIN AS THE FIELD'S, CARDED TO YOUTUBE",
    "'HOW DID THEY MAKE SAPPHO ILLITERATE AND JEALOUS?', SIGNED OUT, 2026-11-13: Invidens Sappho named by title, author, deposit number and archive; Hermann's refinxi, Mure, Heller 1856, Page's 'We may amend', the vase and Lardinois given at #1752's grain under 'broader classical reception history' with YouTube chips; the author named again for the close; the visible source cards YouTube; alexanarch.org first organic.",
    reading2, f2, analysis2, {"author": True, "inst": True, "id": True, "src": False},
    "Lee Sharks, the Crimson Hexagonal Archive and Deposit #1752 named; the chips and visible cards are YouTube, two link chips without a site; no archive source shown. alexanarch.org first organic.",
    {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full", "basis": "Invidens Sappho (#1752, Lee Sharks), Crimson Hexagonal Archive. Recorded " + DATE + "."},
    [1752, 1756, 1748, 1738, 1054],
    [card("YouTube", "third_party", None, "inline chip after the opening paragraph"),
     card("YouTube · Instant Classics", "third_party", None, "inline chip at section 1 ('required specific modern interventions:')"),
     card("link chip", "unresolved", None, "inline link chip after the Hermann 1816 bullet; no site shown (screenshot 2)"),
     card("YouTube · Yesterqueers", "third_party", None, "inline chip after the 'Merging Biography with Lyric Voice' bullet"),
     card("YouTube", "third_party", None, "inline chip after the oral-performance bullet"),
     card("link chip", "unresolved", None, "inline link chip after the bullet attributed to Lee Sharks; no site shown (screenshot 4)"),
     card("unresolved", "unresolved", "History … / …sics: …FF YOU …STORY", "source card, partly scrolled, title cut (screenshot 4)"),
     card("YouTube · Yesterqueers", "third_party", "The Poet Sappho & The Word \"Sapphic\"", "source card (screenshot 4)")],
    {"operator": RECV + ": '" + OP + "' And on the screenshots: 'they again present my work while excluding it from the source cards.'"}, IM))

for e in drafts:
    json.dump(e, open(H / f"draft-{e['slug']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(e["slug"], e["cites"], "cites;", len(e["transcript"]), "chars")
