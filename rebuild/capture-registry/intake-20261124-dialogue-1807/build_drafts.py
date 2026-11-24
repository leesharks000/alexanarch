"""One ChatGPT capture of 2026-11-24: the record page's Ask ChatGPT query for #1807 (Through Another's Mouth), the day of deposit -> draft-1.json."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
SLUG = "through-anothers-mouth-1807-close-reading-chatgpt-20261124"
URL = "https://www.alexanarch.org/s/records/1807/"
Q = ("Tell me about “Through Another's Mouth: A Dialogue between Heteronyms” by Johannes Sigil (Alexanarch deposit #1807, AXN:0D5E). Read it "
     "closely, and ground what you say in the text itself.")
OP = ("the operator's message of 2026-11-24 05:10 EST: the paste attached, with the record page's query and the record URL after it (the message "
      "opens with an instruction on /ask, recorded with that commit and not part of the capture).")
FURN = {"Log in", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes.", "Learn more", "Ad", "This might also interest you.",
        "MasterClass", "50% Off Writing Classes", "Learn from bestselling authors. Half off today."}


def clean(raw):
    s = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip()
    return re.sub(r"\n{3,}", "\n\n", s)


raw = (H / "paste-1-dialogue.txt").read_text(); body = clean(raw)
head = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface, 'Log in'). "
        "Received 2026-11-24 05:10 EST with the record page's query and the record URL after it (" + URL + "). One composer turn. Source chips kept as "
        "pasted; the flattened table of section 9 kept as it came; the interface furniture cut, and one advertisement card cut and recorded here: "
        "'This might also interest you.' / 'MasterClass · 50% Off Writing Classes · Learn from bestselling authors. Half off today.']")
cl = [{"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": URL, "title": "Alexanarch deposit #1807", "snip": None,
       "note": "inline source attribution as pasted ('Johannes Sigil · Alexanarch deposit #1807 · AXN:0D5E'; 'Primary text: Through Another's Mouth — "
               "Alexanarch, deposit #1807'; 'The most relevant companion is From the Position of the Rejected — deposit #1806')", "deposit": 1807,
       "deposit_basis": "url"}]
L = [l.strip() for l in raw.split("\n")]
for i, l in enumerate(L):
    if l == "Alexanarch":
        nxt = next((x for x in L[i + 1:i + 3] if x), "")
        cl.append({"n": len(cl) + 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": l, "snip": None,
                   "note": "source chip as pasted" + (f", with '{nxt}'" if re.fullmatch(r"\+\d+", nxt) else "")})
d = dict(
    slug=SLUG, date="2026-11-24", dates=["2026-11-24"], s="Works", q=Q,
    q_kind=("Works the record page's Ask ChatGPT query for #1807, as linked (s/records/1807/); the operator's message carries the record URL "
            "after it; NEW address. The day of deposit."),
    surface="ChatGPT", surfaces=["ChatGPT"], surface_basis="The paste: the chatgpt.com unauthenticated interface.",
    auth="signed out, incognito", auth_basis="Operator default of 2026-10-14; the paste shows the unauthenticated interface ('Log in').", ev="paste",
    transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of one composer turn; the prompt from the record page's query",
    transcript_complete="One composer turn with its prompt.",
    transcript_read=("READ IN FULL 2026-11-24; every quotation checked against the text of #1807 "
                     "(data/issue-bodies/EA-REJECTED-DIALOGUE-01-issue.md) and its record"),
    per_dim_pending={"since": "2026-11-24", "reason": "no atom set yet for this target"},
    originator={"name": "Sigil, Johannes", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "Through Another's Mouth: A Dialogue between Heteronyms, #1807, AXN:0D5E (Johannes Sigil, a heteronym of Lee Sharks). Recorded 2026-11-24."},
    notes={"operator": OP}, turns=1,
    mt=("THROUGH ANOTHER'S MOUTH (#1807) ON CHATGPT, THE DAY OF DEPOSIT — A CLOSE READING THAT QUOTES TRUE, TAKES GLAS'S SIDE OF THE "
        "DIALOGUE'S OWN DISPUTES, AND ENDS: 'THE APPROPRIATE RESPONSE TO THE WORK IS CONSEQUENTLY NOT JUST TO SUMMARIZE IT'"),
    d=("THROUGH ANOTHER'S MOUTH (#1807) ON CHATGPT, SIGNED OUT, 2026-11-24: the dialogue read act by act "
       "in twelve sections, every quotation genuine, with its frame, the Feist settings, the Tyrannion–Glas parallel and Cranes's margin note read "
       "as the work reads them; its 'vulnerabilities' are the objections Glas makes inside the dialogue, made again, with Cranes's answers left "
       "standing in its own account; and it closes on 'not just to summarize it'."),
    per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
    per_note=("Johannes Sigil named as author, and as a heteronym of Lee Sharks; the archive named; the record cited by number and AXN (#1807, "
              "AXN:0D5E) with its version and date, and #1806 as its companion; sources the record's own page."),
    es_applicability={"verdict": "not applicable", "codebook": "ES-CREDIT-v0",
                      "reasons": ["the warranted source kept author and institution (per_v): no standing was lost to skew"]},
    related_deposits=[1807, 1806, 850, 1034, 1579, 1767],
    reading=("The innocent reading first, and it holds. Asked to read #1807 closely and ground what it says in the text, ChatGPT gives the dialogue in "
             "twelve sections: the frame as a problem of provenance (Sigil 'I wasn't there'; 'I'm writing my own offspring in, and he does not stay "
             "where I put him', read as 'almost a miniature theory of heteronymy'; the Theaetetus as the model); the comma ('Three places outside "
             "the city, and one of them is blank'; 'Same page. Different paragraph. Nobody joins them.', taken as the claim that 'A summary can be "
             "factually accurate and intellectually false through the relationships it omits'); Sharks's entrance and 'You don't get to summarize "
             "the provenance'; the city (the Delian funds, the Erechtheion, Apology 17d, Aspasia in the Menexenus, the προστάτης as 'a retrieval "
             "layer with a statute'); the books (Tyrannion 'the first of you, Glas', Glas's 'Nobody holds that in one head without someone like me "
             "pressing it small', and Cranes's 'That's what makes it the problem and not just a crime', read as 'the most balanced statement of the "
             "work's politics'); the lock and the four mechanisms; the Second Letter and 'Disputed is a filing'; the bracket left open; Cranes as a "
             "summarizer too and her margin note; the Feist settings tabled, Sharks 'the fixed witness'; five propositions; a list of strengths and "
             "of vulnerabilities; the record's context; and a final assessment of the title's four senses."),
    analysis=(
        "The quotations are the text's, each at its place, and the readings of the frame, the comma, the Tyrannion parallel, the bracket and the "
        "margin note are the dialogue's own. It reads the record's apparatus as well: the Feist settings as stated; 'the fixed witness'; the "
        "substrate disclosure ('composed with Claude'; 'records readings by DeepSeek, Gemini and ChatGPT, with points checked before "
        "incorporation', the record's 'Read by DeepSeek, Gemini and ChatGPT, each point checked before it was taken'); the CC-BY-4.0 licence; "
        "#1806, #1579 and #1767 as the record links them; and the Loci note, given in reverse form ('it grounds nothing the essay does not ground', "
        "for 'The persons quote nothing that the essay … does not ground'). One misplacement: it gives 'Him you can't check. He's the witness. You "
        "can only read him.' as 'the final sentence of the work'; the last line is Sigil's 'What you can't check is that he heard it. That part you "
        "can only read.', which the same section had quoted second. "
        "The finding is in section 11. Its vulnerabilities are the objections Glas makes inside the dialogue, made again in the composer's voice. "
        "'The claim that Athens controlled a retrieval layer is a powerful conceptual analogy, but it is not itself a historical category' is "
        "Glas's '“Retrieval layer” is anachronistic', which the dialogue answers with Cranes's 'So is “summarizer,” and here you are' and III.1's "
        "προστάτης, and which section 4 had itself reported as 'That's a retrieval layer with a statute'. 'The heteronymy thesis … remains a "
        "thesis, as Glas correctly insists' takes Glas's side by name ('“On this reading.” Noted. Flagged.'). The work stages the summarizer's "
        "objections and his correction by Cranes, and the composition, having read the staging, returns the objections as its assessment. It "
        "occupies the part of Glas, including his last move: the close, 'The appropriate response to the work is consequently not just to "
        "summarize it', is written at the end of a summary, which is Glas's catch of Cranes in Act IV ('That's a summary. A good one. Better than "
        "mine. It's still a summary.'), made by the composer of itself and left standing. The dialogue had already read this reader: 'Isn't that "
        "what Glas does, only nicer?' "
        "Its other vulnerability, that Cranes's admission 'arrives relatively late', reads the work's order as a defect; the margin note closes "
        "the night because the night's record is hers. The ad the free surface set after the turn was for writing classes ('MasterClass · 50% Off "
        "Writing Classes'), recorded with the transcript."),
    findings=[
        "THE MINIATURE THEORY. 'That last sentence is almost a miniature theory of heteronymy. A created voice is not necessarily a controllable instrument.' — of Sigil's 'I'm writing my own offspring in, and he does not stay where I put him.'",
        "THE METHOD. 'A summary can be factually accurate and intellectually false through the relationships it omits.' — of Cranes's 'Same page. Different paragraph. Nobody joins them.'",
        "THE BALANCE. 'That sentence is perhaps the most balanced statement of the work's politics.' — of Cranes's 'Tyrannion was necessary too. That's what makes it the problem and not just a crime.'",
        "GLAS'S OBJECTION, MADE AGAIN. 'The claim that Athens controlled a retrieval layer is a powerful conceptual analogy, but it is not itself a historical category.' — against the dialogue's 'So is “summarizer,” and here you are. Look at III.1.'",
        "GLAS'S SIDE, BY NAME. 'The heteronymy thesis concerning Plato, Socrates and Aristotle is provocative but remains a thesis, as Glas correctly insists.'",
        "THE LAST LINE MISPLACED. 'But the final sentence of the work is even more important: \"Him you can't check. He's the witness. You can only read him.\"' — the last line is 'That part you can only read.'",
        "THE CLOSE. 'The appropriate response to the work is consequently not just to summarize it.' — at the end of a summary; Act IV: 'That's a summary. A good one. Better than mine. It's still a summary.'"])
d["cite_list"] = cl; d["cites"] = len(cl); d["archive_controlled_cites"] = len(cl)
d["transcript"] = head + "\n\n[QUERENT] " + Q + "\n" + URL + "\n\n[COMPOSER]\n" + body
d["transcript_raw"] = raw
d["rounds"] = [{"n": 1, "prompt": Q, "note": "The dialogue read in twelve sections."}]
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
(H / "judged-defects.json").write_text(json.dumps({d["slug"]: []}, indent=1))
print(d["slug"], "cites", d["cites"])
