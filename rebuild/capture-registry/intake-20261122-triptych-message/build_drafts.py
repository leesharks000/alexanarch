"""One capture of 2026-11-22, Google AI Overview signed out: a developed reading of Three Poems: A Triptych for C., then the poem as a message -> draft-1.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = "give a developed reading of three poems a triptych for c."
Q2 = "ground in archival context to explain the poem as a message"
raw = (H / "paste-1-aio-triptych-for-c.txt").read_text()
L = raw.split("\n")
# source cards as pasted: a site line, then a title line, then a snippet line
CARDS = [  # (round, site, title, rel, note)
 (1, "Medium", "We of the Garden. Three Poems in Triptych | by Andrea Blythe | ArtMusing", "third_party", "a triptych of poems on Bosch, 2024; not this work"),
 (1, "WordPress.com", "Unfolding the Triptych | A Speculative Poetry Blog - WordPress.com", "third_party", "on the triptych as a form, 2014"),
 (1, "www.crimsonhexagonal.org", "Maybe Space Baby Garden Lanes · 16.ROOM.MSBGL", "archive_controlled", "the room page, with the triptych's framing"),
 (1, "www.crimsonhexagonal.org", "Three Poems: A Triptych for C. — Lee Sharks — New Human 2 ...", "archive_controlled", "the triptych on the room page"),
 (1, "www.alexanarch.org", "I would have loved you — Lee Sharks — New Human 2 — Alexanarch", "archive_controlled", "#750"),
 (1, "www.alexanarch.org", "I would have loved you — Alexanarch", "archive_controlled", "#750"),
 (1, "www.alexanarch.org", "\"This thing destroyed me\" — Alexanarch", "archive_controlled", "#749; its snippet: 'The registry mistakenly uses its opening phrase, “This thing destroyed me,” as the title'"),
 (1, "www.crimsonhexagonal.org", "\"This thing destroyed me\" · AXN:02A3 | Crimson Hexagonal Archive", "archive_controlled", "#749"),
 (1, "www.alexanarch.org", "UNCLASSIFIED — Family (page 1 of 7) — Alexanarch", "archive_controlled", "a family listing page; the card's date (Jan 23, 2026) is not the poem's"),
 (1, "www.alexanarch.org", "The reward of love — Lee Sharks — New Human 2 — Alexanarch", "archive_controlled", "#749"),
 (2, "JHI Blog", "Historical Traces in Archival Poetry - JHI Blog", "third_party", "2021; not this work"),
 (2, "www.crimsonhexagonal.org", "Maybe Space Baby Garden Lanes · 16.ROOM.MSBGL", "archive_controlled", "the room page"),
 (2, "www.crimsonhexagonal.org", "23.ROOM.CATULLUS | Crimson Hexagonal Archive", "archive_controlled", "the Catullus room page"),
 (2, "www.alexanarch.org", "Three Poems: A Triptych for C. — Lee Sharks — New Human 2 ...", "archive_controlled", "#1195"),
 (2, "www.crimsonhexagonal.org", "\"This thing destroyed me\" · AXN:02A3 | Crimson Hexagonal Archive", "archive_controlled", "#749, 'Forms a diptych with 06.NH.SHARKS.01'"),
 (2, "www.crimsonhexagonal.org", "I would have loved you · AXN:02A4 | Crimson Hexagonal Archive", "archive_controlled", "#750"),
 (2, "www.alexanarch.org", "if your heart should ever slowly turn - Alexanarch", "archive_controlled", "#734, dated May 17, 2026"),
 (2, "www.crimsonhexagonal.org", "Three Poems: A Triptych for C. — Lee Sharks — New Human 2 ...", "archive_controlled", "#1195"),
 (2, "www.alexanarch.org", "if your heart should ever slowly turn — Alexanarch", "archive_controlled", "#734")]
for _, site, title, _, _ in CARDS:
    assert title in raw, title
cl = [{"n": i + 1, "site": s, "rel": r, "url": None, "title": t, "snip": None, "note": f"source card, round {rd}, as pasted; {nt}"} for i, (rd, s, t, r, nt) in enumerate(CARDS)]
i2 = raw.index(Q2)
r1 = raw[:i2].split("c.give a developed reading of three poems a triptych for c.", 1)[1].strip()
r2 = raw[i2 + len(Q2):].strip()
d = dict(date="2026-11-22", ev="paste", auth="signed out, incognito", surface="Google AI Overview", surfaces=["Google AI Overview"],
  surface_basis="The operator's default (begun in Overview unless stated); the expansion carries the 'AI Mode Conversation' header.",
  auth_basis="Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
  transcript_read="READ IN FULL 2026-11-22; the four records (#734, #749, #750, #1195), their dates and the triptych's text and framing checked; the two room pages on crimsonhexagonal.org read for 'symbolon' and for Catullus 51",
  per_dim_pending={"since": "2026-11-22", "reason": "no atom set yet for this target"},
  originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full", "basis": "Lee Sharks, author of the four poems. Recorded 2026-11-22."},
  notes={"operator": "the paste as an attachment, without comment (2026-11-22 23:00 EST)"}, dates=["2026-11-22"], turns=2,
  slug="developed-reading-three-poems-triptych-for-c-aio-20261122", s="Works", q=Q,
  q_kind="a work query, lower case, as typed; NEW address. The work's earlier capture (three-poems-triptych-for-c-chatgpt-20261105) is at another address on ChatGPT",
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of two rounds",
  transcript_complete="Two rounds, both prompts and both answers, with their source cards.",
  rounds=[{"n": 1, "prompt": Q, "note": "The triptych read panel by panel (counterfactual past, destructive present, conditional future), largely in the deposit's own framing."},
          {"n": 2, "prompt": Q2, "note": "The triptych read as an archival message to C.: from diptych to triptych, the Catullus room, and the symbolon as a three-stage signalling protocol."}],
  mt="THREE POEMS: A TRIPTYCH FOR C., ON GOOGLE AI OVERVIEW — THE DEPOSIT'S FRAMING CARRIED WHOLE AND THE LINES QUOTED RIGHT; THEN A MESSAGE TO C. BUILT FROM A ROOM PAGE'S SYMBOLON AND A CATULLUS THE ROOM DOES NOT HOLD",
  d=("THREE POEMS: A TRIPTYCH FOR C. (Lee Sharks, New Human 2, #1195, AXN:04BC), ON GOOGLE AI OVERVIEW, SIGNED OUT, 2026-11-22: a developed reading of the triptych "
     "as counterfactual past, destructive present and conditional future, then, grounded in archival context, the poem read as a delayed message to C. through "
     "the diptych's history, the Catullus room and the symbolon."),
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Lee Sharks named as author; New Human 2 and the Crimson Hexagonal Archive named; AXN:04BC, 02A4, 02A3 and 0285 and the hexes 06.NH.SHARKS.01–03 given; sources from alexanarch.org and crimsonhexagonal.org",
  related_deposits=[1195, 750, 749, 734],
  reading=("The innocent reading first, and in its first round it holds closely. Asked for a developed reading of Three Poems: A Triptych for C., the Overview "
           "reads it as the deposit frames it: counterfactual past, destructive present, conditional future; the first panel's anaphora holding love 'in the "
           "subjunctive' under 'conditions … never theirs to set'; the narrowing from 'for the rest of my time' to 'for the rest of the time / I have left'; the "
           "second panel's 'the reward of love' as a bitter genitive in which love is the agent of the destruction; the third's long em-dashed line and the "
           "landing on 'then know / that I have loved you', in the present perfect. Asked next to ground the poem in archival context as a message, it reads the "
           "triptych as a 'time-capsule epistle' to C.: a diptych completed by a third panel, the poem seated in Maybe Space Baby Garden Lanes and the Catullus "
           "room, and the three panels as a signalling protocol on the model of the symbolon, the third 'waiting in the archive like an unopened packet'."),
  analysis=("The text holds. Every line quoted is #1195's: the two endings of the first panel, the second panel's 'This thing destroyed me / beyond all repair; "
            "there are no words for it; there is nothing left to become; there is only a wound-down regime of fewer and fewer returns', and the third panel's "
            "'then know / that I have loved you'. The first round is close to a paraphrase of the deposit's own framing: 'counterfactual past → destructive "
            "present → conditional future', 'the bitter genitive recognition that love itself was the agent of the destruction', 'the conditions … not the "
            "speaker's to set', the six lines, the long enjambed line 'through its em-dashes'. It keeps the right title for the second panel, 'The reward of love', "
            "where #749's registry title is its first line (a card it was shown says so). The second round adds three things the archive does not say. First, the "
            "symbolon: 'One half of a symbolon; it completes in traversal' is the description every room page on crimsonhexagonal.org carries of itself, the page "
            "and its traversal; the Overview moves it onto the poem and its addressee, and builds from it a 'three-stage signalling protocol' to C. Second, Catullus: "
            "the Overview says the Catullus room treats Catullus as a poet who 'orbits' an unattainable original, 'without claiming to replace it'. The room's "
            "documents say the reverse: 'Catullus 51 is not merely a translation of Sappho 31', it is the 'first recorded κῆνος activation', 'not imitation but "
            "instantiation: Catullus IS κῆνος, the future reader the poem anticipated'. By the room's own thesis C. stands where Catullus stands, as the future "
            "reader who receives; the Overview puts the speaker there instead. Third, the first panel 'proving that the failure to love in the present was due to "
            "external conditions … not a lack of will': the framing says the loving was 'displaced into the subjunctive by conditions that were not the speaker's "
            "to set'; 'proving' and 'failure to love' are the Overview's. One archival fact is given both ways: the triptych's framing says the three were 'composed "
            "in sequence over twenty-four hours' and marks the third 'First published in this triptych', while #734, 'if your heart should ever slowly turn', is "
            "dated 17 May, five days before the first two (22 May); the Overview repeats the twenty-four hours and then offers to explain 'how the third poem "
            "(AXN:0285) functions as a standalone piece before being folded into the triptych'. C. is not identified, and the Overview does not try."),
  findings=["THE BITTER GENITIVE. '“the reward of love” operates as a double-edged genitive: it is both the price paid for loving and the realization that love itself was the agent of the speaker’s undoing.'",
            "THE PANELS. 'Left Panel: Mourns the unlived possibility (what would have been). Center Panel: Endures the lived devastation (what is). Right Panel: Offers a transfigured testimony (what may yet be received).'",
            "THE MESSAGE. 'Three Poems: A Triptych for C. is a time-capsule epistle.'",
            "THE SYMBOLON MOVED. 'works in Maybe Space Baby Garden Lanes are described as one half of a symbolon' — the room page's description of itself, carried onto the poem and C.",
            "CATULLUS REVERSED. 'Catullus is treated as a poet who “orbits” an unattainable original' — the room holds that Catullus IS κῆνος, the future reader the poem anticipated.",
            "THE PACKET. 'the poem waits in the archive like an unopened packet. It does not demand an immediate reply'."],
  cite_list=cl, cites=len(cl), archive_controlled_cites=sum(1 for x in cl if x["rel"] == "archive_controlled"))
d["transcript"] = ("[Google AI Overview, expanded (the paste carries the 'AI Mode Conversation' header), signed out, incognito (operator defaults). Received 2026-11-22 "
                   "23:00 EST as an attachment. Two rounds; the first prompt doubled in the paste's 'You said' line, given once here. Source cards kept as pasted.]\n\n"
                   "[QUERENT] " + Q + "\n\n[COMPOSER]\n" + r1 + "\n\n[QUERENT] " + Q2 + "\n\n[COMPOSER]\n" + r2)
d["transcript_raw"] = raw
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(d["slug"], d["cites"], len(d["transcript"]))
