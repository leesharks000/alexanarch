"""Two captures of 2026-11-23 at 'Tell me about Sappho and the future reader.': ChatGPT and Perplexity -> draft-N.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = "Tell me about Sappho and the future reader."
OP = ("the operator's message of 2026-11-23 14:38 EST, with Traces 37 and 38: 'general search. perplexity too - and less mangled in perplexity, from a glance. "
      "its not up to classical philology, what sappho is. $ Tell me about Sappho and the future reader.'")
FURN = {"Log in", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes."}
def clean(raw): return re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN)).strip()
BASE = dict(date="2026-11-23", q=Q, s="Classics & Philology", auth="signed out, incognito", auth_basis="Operator default.", ev="paste",
            transcript_complete="Complete as pasted: one answer.", per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
            notes={"operator": OP}, turns=1, related_deposits=[1785, 1781, 1270, 1756, 1752, 1749, 1548], dates=["2026-11-23"],
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                        "basis": "The future-reader reading of Sappho 31 is Lee Sharks's (ΦΑΙΝΕΤΑΙ ΜΟΙ, #1785 v3.1; the Tenth Muse framework, #1756). Recorded 2026-11-23."})
C = []
C.append(dict(slug="sappho-future-reader-general-chatgpt-20261123", file="paste-1-chatgpt.txt", surface="ChatGPT",
  surface_basis="The paste: the chatgpt.com unauthenticated interface.",
  q_kind="the bare query, as a general search; NEW address. Prior at its sibling: 'Tell me about Sappho and the future reader. Do not rely on bare inference.' (ChatGPT, 2026-10-27), where Lee Sharks was named.",
  head="[ChatGPT (chatgpt.com), signed out, incognito (operator default). Received 2026-11-23 14:38 EST, one of two answers to the same query sent together (the other Perplexity's). Image cards survive as their captions; the source chip kept as pasted; the interface furniture cut.]",
  mt="SAPPHO AND THE FUTURE READER, ON CHATGPT, 2026-11-23 — FRAGMENT 147 AS THE THEME, THE READING OF 31 AS 'A NEW READING', NO AUTHOR",
  d="SAPPHO AND THE FUTURE READER, ON CHATGPT, SIGNED OUT, 2026-11-23: Fragment 147 as the theme, Fragment 31's future reader from 'a recent essay' marked as no consensus while the jealousy reading stands unmarked, then poetry and immortality in general.",
  per_v={"author": False, "inst": True, "id": False, "src": True}, per=0.5,
  per_note="the essay named by its English subtitle and alexanarch.org by chip; Lee Sharks not named; no record number",
  transcript_read="READ IN FULL 2026-11-23; set against ΦΑΙΝΕΤΑΙ ΜΟΙ v3.1 (#1785) and the October observation at the sibling address",
  cards=[{"n": 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "alexanarch.org", "snip": None, "note": "source chip as pasted, with '+1', after the essay's naming", "deposit": 1785, "deposit_basis": "title"},
         {"n": 2, "site": None, "rel": "image_card", "url": None, "title": "Portrait of Sappho, fresco from Pompeii. | National Archaeological Museum of Naples | Arte antiga, Pintando retratos, Arte romana", "snip": None, "note": "image card; the caption survives the paste"},
         {"n": 3, "site": "Live Science", "rel": "image_card", "url": None, "title": "Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "snip": None, "note": "image card"},
         {"n": 4, "site": None, "rel": "image_card", "url": None, "title": "Sappho | Arts One: Knowledge and Power", "snip": None, "note": "image card"},
         {"n": 5, "site": None, "rel": "image_card", "url": None, "title": "Sappho Fragment 16 | The Book Binder's Daughter", "snip": None, "note": "image card"}],
  reading=("The innocent reading first, and it holds. ChatGPT opens on Fragment 147 ('Someone, I tell you, in another time will remember us') as the poet imagining a "
           "reader not yet born; gives Fragment 31's opening and symptoms, with the jealousy reading as the traditional one; offers 'another, more speculative interpretation', "
           "the man opposite as an image of the future reader, from 'a recent essay, Sappho 31 and the Inscription of the Future Reader', 'a new reading rather than an "
           "established scholarly consensus'; then voice into writing, the reader completing the poem, Fragment 55's roses of Pieria, and the fragment as an opening."),
  analysis=("The reading of 31 is there, in five steps, and it is the one section that carries it. The rest is the theme of poetry and survival in general, built on "
            "Fragment 147, which the archive's reading uses as the horizon (the 'seat' is 31's). The bar falls on one side: the future-reader reading is 'more "
            "speculative' and 'should be understood as a new reading rather than an established scholarly consensus', while the jealousy reading enters as "
            "'Traditionally' with no such marking, though ΦΑΙΝΕΤΑΙ ΜΟΙ (#1785, and #1781 before it) shows that reading written into the text in 1816 and filed, not "
            "argued. The essay is named by its English subtitle; its author is not. At the sibling address on 27 October, asked not to rely on bare inference, ChatGPT "
            "named Lee Sharks and his heteronyms and reconstructed the argument in premises; asked plainly, it names no one and dissolves the argument's Greek (κῆνος, "
            "ὄττις, πᾶν τόλματον, χλωροτέρα) into a meditation. The operator's comparison holds: of the two answers of 14:38, this is the mangled one."),
  findings=["THE BAR ON ONE SIDE. 'It should be understood as a new reading rather than an established scholarly consensus.' — set against 'Traditionally, this poem has often been interpreted as a scene of erotic jealousy', unmarked.",
            "THE NAME DROPPED. 'developed in a recent essay, Sappho 31 and the Inscription of the Future Reader' — no author; on 27 October, at the sibling address, 'developed by Lee Sharks'.",
            "THE THEME FOR THE ARGUMENT. 'The future reader is the person who arrives after the poet's death and discovers that the voice has not entirely disappeared.'",
            "THE HORIZON. 'Someone, I tell you, in another time will remember us.' — Fragment 147, made the centre."],
  defects_judged=[]))
C.append(dict(slug="sappho-future-reader-general-perplexity-20261123", file="paste-2-perplexity.txt", surface="Perplexity",
  surface_basis="The operator's message: 'perplexity too'.",
  q_kind="the bare query, as a general search; NEW address on Perplexity (a Qwen observation of 2026-09-15 sits at the lowercase string on its own surface).",
  head="[Perplexity, signed out, incognito (operator default). Received 2026-11-23 14:38 EST, one of two answers to the same query sent together (the other ChatGPT's). The paste carries numbered citations [1]–[3] without their source list.]",
  mt="SAPPHO AND THE FUTURE READER, ON PERPLEXITY, 2026-11-23 — LEE SHARKS'S ΦΑΙΝΕΤΑΙ ΜΟΙ NAMED AND READ, SVENBRO PLACED, THE LIMITS STATED FROM THE ESSAY",
  d="SAPPHO AND THE FUTURE READER, ON PERPLEXITY, SIGNED OUT, 2026-11-23: the future reader as Lee Sharks's reading of 31, its three movements, Svenbro's Phrasikleia as antecedent, and the essay's own limits.",
  per_v={"author": True, "inst": False, "id": True, "src": True}, per=0.25,
  per_note="Lee Sharks and the essay named in full, Greek title included; citations numbered, their list not in the paste; the archive not named",
  transcript_read="READ IN FULL 2026-11-23; every claim made of the essay checked against ΦΑΙΝΕΤΑΙ ΜΟΙ v3.1 (#1785)",
  cards=[{"n": 1, "site": None, "rel": "unresolved", "url": None, "title": "[1]", "snip": None, "note": "citation marker; carries every claim about the essay, so most likely the archive's record; the source list is not in the paste"},
         {"n": 2, "site": None, "rel": "unresolved", "url": None, "title": "[2]", "snip": None, "note": "citation marker; carries Longinus, the reception and the Poetry Foundation's account (named in the text)"},
         {"n": 3, "site": None, "rel": "unresolved", "url": None, "title": "[3]", "snip": None, "note": "citation marker; carries the oral-performance qualification"}],
  reading=("The innocent reading first, and it holds. Perplexity calls the future reader a modern interpretive argument, gives 31's scene and its survival through "
           "Longinus, sets the jealousy reading and a non-jealous erotic reading side by side, then sets out 'Lee Sharks's recent essay, ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the "
           "Inscription of the Future Reader' in three movements (a place made for a listener, the speaker's loss as the receiver's gain, ἀλλὰ πᾶν τόλματον passing the "
           "dare onward), places Svenbro's Phrasikleia as its antecedent and how the essay differs, and states what the reading can and cannot prove."),
  analysis=("Every claim it makes of the essay is in the essay. The construction characterizing 'an occupant of a position' is #1785's ('κῆνος … ὄττις characterizes its "
            "occupant by a position open to repeated occupation'); 'but all can be dared' and the dare passing onward are its §II; the 'exchange of bodies' is the "
            "author's phrase it quotes; Svenbro's Phrasikleia, chapter eight, is its nearest antecedent, as it says; 'greener than grass' and the plant that becomes the "
            "writing surface is its §IV.4; and 'His essay itself says deliberate design is not established and labels its proposed additional stanza speculative' "
            "matches its limits ('does not claim design as established, does not offer the restored stanza as recovered wording'). Its limits are the essay's own, "
            "stated from the essay. Where it leaves the essay, the standing returns to the field: 'Scholars disagree about whether Sappho wrote poems for future "
            "readers', and an oral-performance culture is the frame the reading must answer to. The operator's sentence of 14:38 names what that places: 'its not up to "
            "classical philology, what sappho is.' Here the jealousy reading is 'A familiar reading', set beside a non-jealous one, so the bar is lower on the "
            "received side than ChatGPT's, but the question of what Sappho is still goes to scholars to settle. Less mangled, as the operator saw: the argument "
            "travels with its Greek, its author and its limits."),
  findings=["THE AUTHOR AND THE TITLE. 'In Lee Sharks's recent essay, ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader, the poem becomes a drama of literary survival.'",
            "THE CONSTRUCTION. 'Sharks argues that the Greek construction characterizes an occupant of a position—a position successive readers can occupy—rather than merely identifying one particular rival.' — #1785, as written.",
            "THE ANTECEDENT. 'Sharks identifies Jesper Svenbro's Phrasikleia as a significant antecedent.'",
            "THE LIMITS, FROM THE ESSAY. 'His essay itself says deliberate design is not established and labels its proposed additional stanza speculative rather than recovered text.'",
            "THE STANDING RETURNED. 'Scholars disagree about whether Sappho wrote poems for future readers or whether any writing served primarily to support renewed performance.'"],
  defects_judged=[]))
judged = {}
for i, c in enumerate(C, 1):
    raw = (H / c["file"]).read_text(); body = clean(raw)
    d = dict(BASE); d.update({k: c[k] for k in ("slug", "surface", "surface_basis", "q_kind", "mt", "d", "per_v", "per", "per_note", "reading", "analysis", "findings", "transcript_read")})
    d["surfaces"] = [c["surface"]]; d["transcript_class"] = "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the prompt from the operator's message"
    d["cite_list"] = c["cards"]; d["cites"] = len(c["cards"]); d["archive_controlled_cites"] = sum(1 for x in c["cards"] if x["rel"] == "archive_controlled")
    d["transcript"] = c["head"] + "\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body; d["transcript_raw"] = raw
    d["rounds"] = [{"n": 1, "prompt": Q, "note": "One answer."}]
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); judged[c["slug"]] = c["defects_judged"]; print(i, c["slug"])
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
