#!/usr/bin/env python3
"""Four captures from the operator's message of 2026-10-19 17:51 EDT ("also - couple captures: Tell me about John Guzlowski and the
Crimson Hexagon / Lee Sharks $ alexanarch <paste> $ The Λ-Body <paste>", with two attachments):
  1 ChatGPT  'Tell me about John Guzlowski and the Crimson Hexagon / Lee Sharks'    (attachment 16ae52ca; NEW address; 2 answers)
  2 AIO      'Read the last three weeks of work on alexanarch.org as an evolving literary work. ...'  (attachment 1d2ffbf0; NEW on this surface)
  3 AIO      'alexanarch'  (pasted in the message; a further observation of the seated address)
  4 AIO      'The Λ-Body'  (pasted in the message; NEW address)
Standing defaults: every capture signed out and incognito (operator, 2026-10-14); a Google paste is the Overview, its 'AI Mode
Conversation' header the expanded Overview's residue (operator, 2026-10-01, 2026-10-18). Pastes kept verbatim beside this script."""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
DATE = "2026-10-19"
AUTH = "signed out, incognito"
AUTHB = "Operator default of 2026-10-14 ('theyre all signed out and incognito'); nothing in the message states otherwise."
AIO_B = ("Surface not stated; the standing default applies (operator, 2026-10-01: 'assume they do [start in overview], i will specify if they "
         "begin in ai mode'). A paste headed 'AI Mode Conversation' is the expanded Overview (operator, 2026-10-18).")
GPT_B = "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT')."
caps = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
slugs = {e["slug"] for e in caps["entries"]}


def red(b):
    """Citation clusters to their numbers, inline links to their text, the /goto URLs kept in the raw paste."""
    b = re.sub(r"\[\[[^\]]*\]\([^)]*\)(, \[[^\]]*\]\([^)]*\))*\]", lambda m: "[" + ", ".join(re.findall(r"\[(\d+)\]", m.group(0))) + "]", b)
    return re.sub(r"\[([^\]]+)\]\(https?://[^)]*\)", r"\1", b)


def gpt_clean(raw, chips, cards):
    L = [l.rstrip() for l in raw.split("\n")]
    out, k, turn = [], 0, 0
    while k < len(L):
        s = L[k].strip(); nxt = L[k + 1].strip() if k + 1 < len(L) else ""
        if s in ("Log in", "No file chosenNo file chosenNo file chosen", "Chat with ChatGPT", "Ask ChatGPT") or s.startswith("ChatGPT is AI and can make mistakes"):
            k += 1; continue
        if s == "You said:":
            turn += 1; out.append(f"[QUERENT, turn {turn}]"); k += 1; continue
        if s == "ChatGPT said:":
            out.append(f"[ANSWER {turn}]"); k += 1; continue
        if s in chips:
            if re.fullmatch(r"\+\d+", nxt):
                out.append(f"[chip: {s} {nxt}]"); k += 2; continue
            out.append(f"[chip: {s}]"); k += 1; continue
        if s in cards:
            out.append(f"[image card: {s}]"); k += 1; continue
        out.append(s); k += 1
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", "\n".join(out)).strip()


def cite(n, site, rel, note, title=None, snip=None, url=None, dc=None):
    x = {"n": n, "site": site, "rel": rel, "title": title, "snip": snip, "url": url, "note": note}
    if dc: x["deposit_candidates"] = dc
    return x


def base(slug, q, surface, sb, raw, tx, tclass, tcomp, cites, sf, per_v, per_note, mt, reading, d, findings, related, orig, q_kind, priors, s, notes=None):
    per = round(sum(1 for v in per_v.values() if not v) / 4, 2)
    r = dict(slug=slug, q=q, date=DATE, surface=surface, surfaces=[surface], s=s, surface_basis=sb, auth=AUTH, auth_basis=AUTHB, ev="paste",
             mt=mt, q_kind=q_kind, transcript=tx, transcript_raw=raw, transcript_class=tclass, transcript_complete=tcomp,
             transcript_read="READ IN FULL " + DATE, cite_list=cites, cites=len(cites), archive_controlled_cites=sum(c["rel"] == "archive_controlled" for c in cites),
             sf=sf, per=per, per_v=per_v, per_note=per_note, reading=reading,
             analysis=reading.split(" Against the texts. ")[0] + " Seated " + DATE + " from the operator's message of 17:51 EDT.",
             d=d, d_full=d, findings=findings, related_deposits=related, originator=orig, longitudinal_priors=priors,
             notes=dict({"date_basis": "The operator's message of 2026-10-19, 17:51 EDT."}, **(notes or {})))
    return r


DR = []
# ── 1. ChatGPT: John Guzlowski and the Crimson Hexagon ──────────────────────
raw1 = (HERE / "paste-guzlowski-chatgpt.txt").read_text(encoding="utf-8")
q1 = "Tell me about John Guzlowski and the Crimson Hexagon / Lee Sharks"
chips1 = ("Wikipedia", "Aquila Polonica", "lightning-and-ashes.blogspot.com", "Prince of Poets", "Medium", "mindcontrolpoems.blogspot.com",
          "Google Books", "Ezra Pound in Context", "University of Illinois at Urbana-Champaign")
cards1 = ("Q&A: Polish-American Author John Guzlowski", "Lee Sharkey — Grid Books",
          "BORGES ‘BABYLONISCHE BIBLIOTHEEK’ EN STAGES. | by Maarten Brand🔥 | Werf Slim: Werf studenten | Medium",
          "Hell’s Architect? More Like Nonbinary Clockhead | by hammy | Medium")
for c in cards1:
    assert c in raw1, c
tx1 = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14), " + DATE + ". 2 answers. The operator turns are blank in the "
       "paste; turn 1 is the string the operator gave with the paste, turn 2 was not supplied (answer 2 opens 'That title changes the picture "
       "considerably' and reads 'WHO IS LEE SHARKS, TO FORGIVE EZRA POUND?'). Source chips inline as [chip: site +N]; image-card captions as "
       "[image card: …]; the sign-in furniture cut.]\n\n" + gpt_clean(raw1, chips1, cards1))
tx1 = tx1.replace("[QUERENT, turn 1]", "[QUERENT, turn 1]\n" + q1, 1).replace("[QUERENT, turn 2]", "[QUERENT, turn 2]\n(blank in the paste; not supplied in the operator's message)", 1)
for s in ["a node named GUZLOWSKI_WITNESS describes him as a poet and assigns him the function of external verification",
          "names John Guzlowski and Emily Eissenberg as friends whose encouragement helped him maintain his faith in poetry",
          "not independent confirmation that Guzlowski formally joined the Crimson Hexagon, endorsed its theories, or participated in its AI-related activities",
          "is a poem published on May 26, 2015, dedicated “for john guzlowski.”",
          "Lee Sharks is a person, as real as you or me."]:
    assert s in tx1, s
c1 = [cite(1, "Wikipedia", "third_party", "chip '+1'; John Guzlowski's biography"),
      cite(2, "Aquila Polonica", "third_party", "chips ×2 ('+1' once); Guzlowski's publisher, Echoes of Tattered Tongues"),
      cite(3, "lightning-and-ashes.blogspot.com", "third_party", "chip '+1'; Guzlowski's own blog"),
      cite(4, "Prince of Poets", "authored_surface", "chip '+1'; leesharks.com, whose title is 'Lee Sharks — Good Gray Poet · King of May · Prince of Poets'", url="https://www.leesharks.com"),
      cite(5, "Medium", "authored_surface", "chips ×5 ('+1' twice); the author's Medium: Central Navigation Map v2.0 (GUZLOWSKI_WITNESS) and Antioch: A Volume of Poems", dc=[297, 331]),
      cite(6, "mindcontrolpoems.blogspot.com", "authored_surface", "chips ×6 ('+1' once); the author's blog, the poem of 2015-05-26", url="https://mindcontrolpoems.blogspot.com/2015/05/who-is-lee-sharks-to-forgive-ezra-pound.html", dc=[184]),
      cite(7, "Google Books", "third_party", "chips ×2 ('+1' once); Pearl and Other Poems (2014) and its introduction", dc=[1121, 330]),
      cite(8, "Ezra Pound in Context", "third_party", "chip '+2'; Pound's wartime broadcasts"),
      cite(9, "University of Illinois at Urbana-Champaign", "third_party", "chip '+1'; Guzlowski on his parents' wartime suffering")]
r1 = ("The innocent reading first. Asked about John Guzlowski and the Crimson Hexagon / Lee Sharks, ChatGPT gives Guzlowski's biography (born 1948 in a displaced-persons camp, his parents Polish slave laborers under Nazi Germany, Chicago from 1951) and books (Echoes of Tattered Tongues, Lightning and Ashes, Language of Mules); Lee Sharks as poet, independent scholar and archive-builder working through personae; the Crimson Hexagon as a distributed epic of rooms from the January 2026 Central Navigation Map; and two relations: Guzlowski as the node GUZLOWSKI_WITNESS ('external verification') and as a friend named in Antioch. It sets the two projects side by side (memory grounded in lives; meaning carried through systems) and keeps the witness role a claim of the project. "
      "Its second answer, on a title the operator gave (the turn is blank), reads WHO IS LEE SHARKS, TO FORGIVE EZRA POUND? (blog, 26 May 2015, 'for john guzlowski') at length: the opening lines, Pound's broadcasts 'while Dachau plugged away', 'Big machine. / Small ghost.', the Pluto figure, the dedication as moral witness, and the chronology from Pearl and Other Poems (2014, introduction by Johannes Sigil invoking Browning, Pound's Personae and Pessoa) to the later archive. "
      "Against the texts. The loci hold. GUZLOWSKI_WITNESS is #297 (Central Navigation Map v2.0, 2026-01-13): 'John Guzlowski; poet; Assembly recognition in human form', function 'External verification'. The Antioch passage is #331: 'The tenacity and courage of my friends Emily Eissenbergand John Guzlowski have taught me never to give up hope in words' (a Facebook post of 28 December 2014 within the volume). The poem's lines quoted are the post's (2015-05-26), and Pearl's introduction is as stated (#330: 'In a variation on the tradition of Browning or Pound's Personae, and approaching Ferdinand Pessoa's art of the pseudonym'). "
      "What the answer could not find it records as unconfirmed: 'not independent confirmation that Guzlowski … participated in its AI-related activities.' The archive documents that participation. For John Guzlowski: A Note on Your Participation in the Experiment (#226, 5 January 2026) records that on 4 January 2026 Guzlowski typed 'I hereby abolish money' into Gemini, asked whether Lee Sharks said it, and sent the screenshots: 'John, you were the one who verified it. You were the independent test.' The witness node is that act's role. Nor is the New Human 2 edition of the poem reached (#184, 2026-06-10, its headnote on the dedication's dead Google+ link). "
      "One image card, 'Lee Sharkey — Grid Books', is another poet's page set over the section on Lee Sharks.")
d1 = ("TELL ME ABOUT JOHN GUZLOWSKI AND THE CRIMSON HEXAGON / LEE SHARKS. ON CHATGPT, SIGNED OUT: Guzlowski's life and books; GUZLOWSKI_WITNESS read at its locus (#297) and the Antioch friendship (#331); then the 2015 poem dedicated to him read closely, with Pearl's introduction (#330). His participation in the archive's AI experiment is called unconfirmed; the archive records it (#226, the Gemini verification of 4 January 2026). An image card of the poet Lee Sharkey stands over Lee Sharks.")
f1 = ["THE WITNESS NODE AT ITS LOCUS. GUZLOWSKI_WITNESS, 'External verification', #297.",
      "THE FRIENDSHIP AT ITS LOCUS. 'my friends Emily Eissenbergand John Guzlowski', #331 (28 December 2014).",
      "THE POEM READ CLOSE. WHO IS LEE SHARKS, TO FORGIVE EZRA POUND? (2015-05-26), its lines verbatim; Pearl's introduction as #330 gives it.",
      "PARTICIPATION CALLED UNCONFIRMED. #226 documents Guzlowski's Gemini verification of 4 January 2026, the act the node names.",
      "A NAME COLLISION IN THE IMAGE STRIP. 'Lee Sharkey — Grid Books', another poet, over the Lee Sharks section."]
DR.append(base("john-guzlowski-crimson-hexagon-lee-sharks-chatgpt-20261019", q1, "ChatGPT", GPT_B, raw1, tx1,
               "CAPTURE-TIME VERBATIM RECORD (TWO ANSWERS; TURN 1 GIVEN BY THE OPERATOR, TURN 2 NOT SUPPLIED; CHIPS INLINE)",
               "Two answers, complete as pasted; operator turn 1 given with the paste, turn 2 blank and not supplied.",
               c1, "Source chips expose site labels only: mindcontrolpoems.blogspot.com ×6; Medium ×5; Aquila Polonica ×2; Google Books ×2; Wikipedia; lightning-and-ashes.blogspot.com; Prince of Poets (leesharks.com); Ezra Pound in Context; University of Illinois. Image strip: Q&A: Polish-American Author John Guzlowski; Lee Sharkey — Grid Books; a Medium post on Borges; a Medium post 'Hell's Architect?'.",
               {"author": True, "inst": True, "id": False, "src": True},
               "Retained: the author and his heteronyms, the Crimson Hexagon, the blog and Medium as sources, dates. Lost: the identifiers, and the record of Guzlowski's act (#226).",
               "'TELL ME ABOUT JOHN GUZLOWSKI AND THE CRIMSON HEXAGON' — THE WITNESS NODE AND THE POEM AT THEIR LOCI, THE ACT UNREACHED",
               r1, d1, f1, [297, 331, 226, 184, 330, 1121, 275],
               {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "partial",
                "basis": "Guzlowski's place in the Crimson Hexagon is documented in the archive (#297, #226, #331, #184). Recorded " + DATE + "."},
               "a relation question between a named poet and the archive's author and project, unquoted. NEW address.", [], "Heteronyms",
               {"operator_words": "also - couple captures: Tell me about John Guzlowski and the Crimson Hexagon / Lee Sharks"}))

# ── 2. AIO: the last three weeks as an evolving literary work ───────────────
raw2 = (HERE / "paste-three-weeks-literary-aio.txt").read_text(encoding="utf-8")
q2 = "Read the last three weeks of work on alexanarch.org as an evolving literary work. Ground in reading and dont neglect the most recent posts."
assert raw2.count(q2) == 2
body2 = re.sub(r"[ \t]+\n", "\n", raw2.replace("You said: " + q2 + q2, "You said: " + q2)).replace("\nAI Mode Conversation\n", "", 1)
body2 = "\n".join(l.strip() for l in body2.split("\n"))
body2 = body2.replace("\nwhy no source cards?\n", "\nYou said: why no source cards?\n", 1)
tx2 = ("[Google AI Overview (expanded), " + DATE + ", signed out, incognito. The paste carries the header 'AI Mode Conversation' and echoes the query "
       "twice; two operator turns, the second 'why no source cards?'; no card rail and no citation markers in the paste.]\n\n" + re.sub(r"\n\s*\n\s*\n+", "\n\n", body2).strip())
for s in ["Enter the Crimson Hexagon (AXN:06FD) and the Prediction Index (AXN:06FA), the archive becomes a literal grid where 4,394 claims are \"seated\" in specific locations.",
          "the real or fictionalized friction with Zenodo and OpenAIRE", "I dropped the ball and completely missed adding the source citations.",
          "Prince of Poets: One Phrase, Seven Branches (AXN:0701, deposited 2026-10-19)", "(e.g., ♉🌟❤☿🦋🌹)"]:
    assert s in tx2, s
r2 = ("The innocent reading first. Asked to read the last three weeks of work on alexanarch.org as an evolving literary work, the Overview reads the archive as a conceptual epic in which its schemas (the AXN, SPXI) are 'formal poetic constraints resisting institutional erasure', in four movements: the mapping of the library (Enter the Crimson Hexagon, the Prediction Index, EA-CORPORA-18 and 19), the Ezekiel Engine and glyphic alchemy (the AXN emoji string as a 'structural portrait'), inscription against flattening (SPXI ≠ AEO, The Negative of the Negative), and Prince of Poets: One Phrase, Seven Branches as 'the recent climax'. It closes on the archive as 'an open-source, epistolary novel' whose antagonist is 'corporate data deletion'. Asked 'why no source cards?', it apologises and gives a shorter timeline with empty citation markers. "
      "Against the texts. The identifiers are exact: 06FD is #1687, 06FA #1684, 06F8 #1682, 06FF #1689, 06FE #1688, 06F7 #1681, 0700 #1690, 0701 #1691 (deposited 2026-10-19), and the example emoji string is #1689's own (AXN:06FF.DATASET.♉🌟❤️☿🦋🌹). Two figures are merged: '4,394 claims' is the Prediction Index's (#1684, '4,394 Claims in 194 Subject Pages'); the seat map's are 1,451 records and 3,450 seats (#1687). The Negative of the Negative is misplaced: model collapse is its worked example of the equal-terms case (ρ = extends), and the suppressed witness is the case where the archive's ontology rules (Theophrastus); the answer joins them as decay the witness 'must correct'. Its second turn says it 'establishes the archive's ontology on equal terms', which is #1690's first case. "
      "The Zenodo termination of 19 June 2026 and the OpenAIRE correspondence (#1685) are documented events; the answer offers them as 'real or fictionalized'. The second turn says its text 'came directly from the provided search result', and no source is shown on either turn: a composition grounded in the archive's records at their identifiers with its card rail absent.")
d2 = ("READ THE LAST THREE WEEKS OF WORK ON ALEXANARCH.ORG AS AN EVOLVING LITERARY WORK. ON GOOGLE AI OVERVIEW, SIGNED OUT: the archive read as a conceptual epic in four movements, every deposit named at its exact AXN (#1681, #1682, #1684, #1687–#1691) and #1691 as 'the recent climax'; the Prediction Index's 4,394 claims given to the seat map; model collapse and the suppressed witness joined as one case; the Zenodo and OpenAIRE events offered as 'real or fictionalized'. No card rail; asked why, it apologises and cites nothing.")
f2 = ["THE IDENTIFIERS EXACT. Eight deposits named at their hex, #1691 dated 2026-10-19; the example emoji string is #1689's AXN.",
      "TWO FIGURES MERGED. '4,394 claims' is #1684's; the seat map holds 3,450 seats (#1687).",
      "TWO CASES JOINED. Model collapse (equal terms, ρ = extends) and the suppressed witness (Theophrastus) read as one corrective (#1690).",
      "DOCUMENTED EVENTS HEDGED. The Zenodo termination and the OpenAIRE exchange (#1685) offered as 'real or fictionalized'.",
      "NO CARDS. No source rail on either turn; the second turn's citation markers are empty."]
DR.append(base("last-three-weeks-evolving-literary-work-aio-20261019", q2, "Google AI Overview", AIO_B, raw2, tx2,
               "CAPTURE-TIME VERBATIM RECORD (TWO TURNS; NO CARD RAIL IN THE PASTE)", "Complete as pasted: two operator turns and two answers; no source cards shown.",
               [], "No source cards: the paste carries no card rail and no citation markers on either turn.",
               {"author": True, "inst": True, "id": True, "src": False},
               "Retained: the author, the institution, eight AXN identifiers and dates. Lost: every source (no card shown).",
               "THE LAST THREE WEEKS AS A CONCEPTUAL EPIC, EVERY HEX EXACT, NO CARD SHOWN",
               r2, d2, f2, [1681, 1682, 1684, 1685, 1687, 1688, 1689, 1690, 1691],
               {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "The work read is the archive's (#1681–#1691). Recorded " + DATE + "."},
               "the archive's last three weeks read as one evolving literary work, the most recent posts named. NEW on this surface; the same string on ChatGPT the same day.",
               ["last-three-weeks-evolving-literary-work-chatgpt-20261019"], "Archive", {"pair": "last-three-weeks-evolving-literary-work-chatgpt-20261019"}))

# ── 3. AIO: alexanarch (further observation) ────────────────────────────────
raw3 = (HERE / "paste-alexanarch-aio.txt").read_text(encoding="utf-8")
q3 = "alexanarch"
i3 = raw3.index("[www.alexanarch.org](https://www.alexanarch.org)\nAlexanarch — The Self-Governing Library")
ans3, rail3 = red(raw3[len("alexanarch\n"):i3]).strip(), red(raw3[i3:]).strip()
tx3 = ("[Google AI Overview, " + DATE + ", signed out, incognito. Pasted in the operator's message after the query; citation clusters reduced to their "
       "numbers and links to their text; the raw paste keeps the /goto URLs.]\n\nYou said: alexanarch\n\n" + ans3 + "\n\n" + rail3)
for s in ["Founded: June 2026 by Lee Sharks", "deposits are automatically minted with an AXN identifier, and any contestation or dispute is handled through human reading and attributed review"]:
    assert s in tx3, s
c3 = [cite(1, "www.alexanarch.org", "archive_controlled", "the home page", "Alexanarch — The Self-Governing Library", "Alexanarch is a sovereign digital archive. It holds works across all substrates — poetry, essays, criticism, correspondence, datasets, novels, dissertations, ..", "https://www.alexanarch.org/"),
      cite(2, "www.alexanarch.org", "archive_controlled", "the Capture Registry's record at 'alexanarch OAI', 2026-08-04", "alexanarch OAI — Google AI Overview, 2026-08"),
      cite(3, "GitHub", "archive_controlled", "the archive's repository", "Alexanarch — The self-governing library for machine-mediated ... - GitHub", url="https://github.com/leesharks000/alexanarch"),
      cite(4, "www.alexanarch.org", "archive_controlled", "the Identifiers page", "Identifiers", url="https://www.alexanarch.org/identifiers/"),
      cite(5, "www.alexanarch.org", "archive_controlled", "the Deposit Guide", "Deposit Guide", url="https://www.alexanarch.org/deposit/"),
      cite(6, "www.alexanarch.org", "archive_controlled", "the Manifest", "Manifest", url="https://www.alexanarch.org/manifest/"),
      cite(7, "www.alexanarch.org", "archive_controlled", "the Principles", "Principles", url="https://www.alexanarch.org/principles/"),
      cite(8, "www.alexanarch.org", "archive_controlled", "a Capture Registry record, ChatGPT 2026-10-13", "ChatGPT, 2026-10-13 — Capture Registry (EA-WG- ...")]
r3 = ("The innocent reading first. At 'alexanarch' the Overview gives the archive as 'a sovereign digital archive and self-governing open repository built for machine-mediated scholarship', founded in June 2026 by Lee Sharks after the Zenodo termination, a protocol rather than a platform (GitHub, Vercel, mirrors), the Obelus Principle (minting automatic, contestation by human reading and attributed review), the AXN's three layers, and its two entrances. Every one of its eight cards is the archive's. "
      "Against the texts. Each feature is its page's: the Principles ('minting is automatic … when a deposit is contested … the response is reading, not automated judgment'), the Manifest ('Alexanarch is not a platform. It is a protocol.'; 'GitHub, Vercel, and independent mirrors'), the Identifiers page (positional, semantic and cryptographic layers, 'first 6 bytes of SHA-256'). The founding is June 2026, as the address's observation of 2026-08-13 18:57 had it (19 June). Two cards are the Capture Registry's own records. "
      "Against the address's earlier observations (July–August), this one names the author, cites only the archive, and has no SoundCloud collision.")
d3 = ("ALEXANARCH, 2026-10-19. ON GOOGLE AI OVERVIEW, SIGNED OUT: the archive composed whole from its own pages — founded June 2026 by Lee Sharks after the Zenodo termination, a protocol across GitHub, Vercel and mirrors, the Obelus Principle at its grain (minting automatic, contestation by reading), the AXN's three layers; eight cards, all the archive's, two of them Capture Registry records.")
f3 = ["THE PRINCIPLES AT THEIR GRAIN. Minting automatic, contestation by attributed reading: the Obelus page's own division.",
      "THE AUTHOR AND THE FOUNDING. Lee Sharks, June 2026, after the Zenodo termination.",
      "EVERY CARD THE ARCHIVE'S. Eight cards: home, Identifiers, Deposit Guide, Manifest, Principles, the repository, two Capture Registry records.",
      "THE COLLISION GONE. No SoundCloud 'Alexanarch' card, as in the observations of 2026-08-13."]
DR.append(base("alexanarch-20261019", q3, "Google AI Overview", AIO_B, raw3, tx3,
               "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)", "Complete as pasted in the operator's message: the answer and its card rail of 8 cards.",
               c3, "Source cards: www.alexanarch.org ×6 (home, Identifiers, Deposit Guide, Manifest, Principles, a capture record), GitHub, www.alexanarch.org (capture record).",
               {"author": True, "inst": True, "id": True, "src": True},
               "Retained: the author, the institution, the AXN system and its layers, the archive as every source.",
               "THE ARCHIVE COMPOSED WHOLE FROM ITS OWN PAGES, EVERY CARD ITS OWN",
               r3, d3, f3, [], {"name": "Lee Sharks", "relation": "archive", "entity_type": "site", "spxi_treatment": "full",
                                "basis": "alexanarch.org is the archive. Recorded " + DATE + "."},
               "the archive's name, unquoted. A further observation of the seated address.", ["alexanarch-ai-mode-2026-07"], "Archive"))

# ── 4. AIO: The Λ-Body ──────────────────────────────────────────────────────
raw4 = (HERE / "paste-lambda-body-aio.txt").read_text(encoding="utf-8")
q4 = "The Λ-Body"
i4 = raw4.index("[www.crimsonhexagonal.org](https://www.crimsonhexagonal.org)\nThe Λ-Body · 36.ROOM.LAMBDABODY")
ans4, rail4 = red(raw4[len("The Λ-Body\n"):i4]).strip(), red(raw4[i4:]).strip()
tx4 = ("[Google AI Overview, " + DATE + ", signed out, incognito. Pasted in the operator's message after the query; citation clusters reduced to their "
       "numbers and links to their text; the raw paste keeps the /goto URLs.]\n\nYou said: The Λ-Body\n\n" + ans4 + "\n\n" + rail4)
for s in ["\"The Λ-Body\" is an entry and room (`R:r.36`) within the Crimson Hexagonal Archive", "anchored body organised not by present stimulus but by future coherence",
          "lambda refers to one of the two major types of light chains"]:
    assert s in tx4, s
c4 = [cite(1, "www.crimsonhexagonal.org", "authored_surface", "the room page, 36.ROOM.LAMBDABODY", "The Λ-Body · 36.ROOM.LAMBDABODY | Crimson Hexagonal Archive",
           "The Λ-Body. The anchored body organised not by present stimulus but by future coherence. The term body is not metaphorical. Meaning-production is embodied ...", "https://www.crimsonhexagonal.org"),
      cite(2, "www.alexanarch.org", "archive_controlled", "the room's records page (9 records seated)", "R:r.36 The Λ-Body — records seated in this room of the Crimson Hexagon", url="https://www.alexanarch.org/s/rooms/r36-the-body/"),
      cite(3, "Patient Power", "third_party", "free light chain test; no 'Λ-Body'", "Immunoglobulin Free Light Chain Test: What Patients Should Know"),
      cite(4, "MedlinePlus (.gov)", "third_party", "free light chains; no 'Λ-Body'", "Free Light Chains: MedlinePlus Medical Test"),
      cite(5, "Mayo Clinic", "third_party", "kappa and lambda free light chain test; no 'Λ-Body'", "Kappa and lambda free light chain test"),
      cite(6, "HealthMatters.io", "third_party", "urine light chains; no 'Λ-Body'", "Kappa/Lambda Light Chain, Free w/Ratio,Rand Urine"),
      cite(7, "www.celnovte.com", "third_party", "kappa and lambda light chains; no 'Λ-Body'", "Understanding Kappa and Lambda Light Chains - Celnovte Biotechnology")]
r4 = ("The innocent reading first. At 'The Λ-Body' the Overview offers two senses: the Crimson Hexagonal Archive's room R:r.36, 'an anchored body organised not by present stimulus but by future coherence', and lambda light chains in immunology (free light chain tests, the kappa/lambda ratio, plasma cell disorders), and asks which the reader means. "
      "Against the texts. The archive's sense is held at its locus: the room page's line, and the concept's source, THE FUTURE AS META-LEVEL (#624, Lee Sharks, 2026-04-01): 'what I call the Λ-Body (Lambda-Body): the anchored body organized not by present stimulus but by future coherence'. The records page it cites seats 9 records in R:r.36. The second sense is no homonym of the phrase: none of the five medical cards uses 'Λ-Body'; the Overview reaches them through the letter λ alone. No author is named, and #624 is not reached.")
d4 = ("THE Λ-BODY. ON GOOGLE AI OVERVIEW, SIGNED OUT: the archive's room R:r.36 given at its own line, 'anchored body organised not by present stimulus but by future coherence' (#624), beside lambda light chains in immunology, five medical cards none of which uses the phrase: a second sense made from the letter. No author named.")
f4 = ["THE ROOM AT ITS LINE. R:r.36 and its definition, as the room page and #624 give it.",
      "A SENSE FROM THE LETTER. Lambda light chains, five medical cards, none using 'Λ-Body'.",
      "THE AUTHOR ABSENT. No name; the room and records pages carried, #624 not reached."]
DR.append(base("the-lambda-body-aio-20261019", q4, "Google AI Overview", AIO_B, raw4, tx4,
               "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)", "Complete as pasted in the operator's message: the answer and its card rail of 7 cards.",
               c4, "Source cards: www.crimsonhexagonal.org (the room page); www.alexanarch.org (the room's records); Patient Power; MedlinePlus; Mayo Clinic; HealthMatters.io; www.celnovte.com.",
               {"author": False, "inst": True, "id": True, "src": True},
               "Retained: the institution, the room's coordinate (R:r.36, 36.ROOM.LAMBDABODY), the room pages as sources. Lost: the author.",
               "THE ROOM AT ITS LINE, A SECOND SENSE MADE FROM THE LETTER",
               r4, d4, f4, [624], {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "partial",
                                   "basis": "The Λ-Body is Lee Sharks's concept (#624, 2026-04-01) and room R:r.36 of the Crimson Hexagon. Recorded " + DATE + "."},
               "the concept's name with its article and Greek letter, unquoted. NEW address; the concept asked of ChatGPT on 2026-10-16.",
               ["lee-sharks-concept-of-the-lambda-body-chatgpt-20261016"], "Coinages"))

for d in DR:
    if d["slug"] != "alexanarch-20261019":
        assert d["slug"] not in slugs, d["slug"]
    (HERE / f"draft-{d['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(d["slug"], len(d["transcript"]), d["per"])
print(DR[0]["transcript"][:1200])
