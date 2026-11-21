"""Two captures of 2026-11-21: the Ask page's last-week living-body query on ChatGPT (stopped partway) and on Perplexity (thirteen rounds) -> draft-N.json for capture_intake.py."""
import json, pathlib, re
H = pathlib.Path(__file__).parent
Q = "Read the last week of work on alexanarch.org through 20 Nov 2026 as a living body of thought. Ground in reading, archival context and historical import."
OP = ("with the two attachments (2026-11-21 09:59 EST): 'oh it composes, then freezes partway thru, normally also freezing the interface and the browser. this one is "
      "stopped generating without freezing the browser. and then one from perplexity, same question - really solid analysis of the recursive sophistry, check the "
      "sophistry measure, ive become progressively irritated with the shape of perplexity - and you can truncate the repastes where i fed it back its own prior output. "
      "note that it does seem that perplexity is either engineered to be unable to see its own prior output or that it pretends not to be able to as a defense mechanism. "
      "you can censor my cursing - just like i do in pearl - f***'; and at 10:02: 'it makes the exact same move the article diagnosed: its atoms hide the substitution of "
      "taste for holistic, inspectable argument at the crucial junctures. anyone can quantitatively analyze. not anyone can show the precise junction of the personal the "
      "historical and the quantitative and bind it in a narrative that preserves the domain of each, and that is central to the argument and sappho'. Earlier (09:33): "
      "'for whatever reason now chatgpt reliably freezes on the last week living body prompt.'")
CHIP = re.compile(r"^(alexanarch\.org|Alexanarch|The Self-Governing Library)$")
FURN = {"Log in", "Sign up for free", "Chat with ChatGPT", "Ask ChatGPT", "ChatGPT is AI and can make mistakes."}
CENSOR = [("fucking", "f***ing"), (" dick ", " d*** "), ("inferential ass", "inferential a**")]
BASE = dict(date="2026-11-21", ev="paste", auth="signed out, incognito",
            transcript_read="READ IN FULL 2026-11-21; record numbers, titles, creators, dates, counts and quotations checked against the records and their texts",
            per_dim_pending={"since": "2026-11-21", "reason": "no atom set yet for this target"},
            originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                        "basis": "Lee Sharks and the archive at alexanarch.org. Recorded 2026-11-21."},
            notes={"operator": OP}, dates=["2026-11-21"], q=Q)


def clean(raw):
    out = [l.rstrip() for l in raw.split("\n") if l.strip() not in FURN]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out).strip())


# 1 ChatGPT -----------------------------------------------------------------
raw1 = (H / "paste-1-chatgpt-living-body.txt").read_text(); L = [l.strip() for l in raw1.split("\n")]; cl1 = []
for i, l in enumerate(L):
    if CHIP.match(l):
        nxt = next((x for x in L[i + 1:i + 3] if x), ""); plus = nxt if re.fullmatch(r"\+\d+", nxt) else None
        cl1.append({"site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": l, "snip": None, "note": "source chip as pasted" + (f", with '{plus}'" if plus else ""), "n": len(cl1) + 1})
for t in ["Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "Sappho Fragment 16 | The Book Binder's Daughter", "MS 593 - The Schoyen Collection"]:
    cl1.append({"site": t.split("|")[-1].strip() if "|" in t else None, "rel": "image_card", "url": None, "title": t, "snip": None, "note": "image card; the caption survives the paste", "n": len(cl1) + 1})
d1 = dict(BASE, slug="last-week-living-body-stopped-chatgpt-20261121", s="Archive", surface="ChatGPT", surfaces=["ChatGPT"],
  surface_basis="The paste: the chatgpt.com unauthenticated interface.", auth_basis="Operator default.",
  q_kind="the Ask page's 'living body of thought' query, 1 week (alexanarch.org/ask/#time), as run by the operator; the prompt is not in the paste, and its wording is the operator's ('same question' as the Perplexity run, whose export gives it as typed).",
  transcript_class="CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn, which stopped generating partway",
  transcript_complete="Incomplete as composed: generation stopped at the heading '8. Archival' (the operator: 'this one is stopped generating without freezing the browser').",
  turns=1, rounds=[{"n": 1, "prompt": Q, "note": "One answer, stopped partway."}],
  mt="THE LAST WEEK AS A LIVING BODY, ON CHATGPT — THE READER IS PART OF THE HISTORY; THE THEORY OF HISTORICAL RECOGNITION; STOPPED AT '8. ARCHIVAL'; DEAD LETTERS NOT READ",
  d="THE LAST WEEK OF ALEXANARCH.ORG AS A LIVING BODY, ON CHATGPT, SIGNED OUT, 2026-11-21: the reader as part of the history, the Sappho sequence as centre, a theory of historical recognition; generation stopped at its eighth section.",
  per_v={"author": False, "inst": True, "id": True, "src": True}, per=0.25,
  per_note="the archive named and every work cited by number; Rebekah Cranes, Nobel Glas and Sen Kuro named; Lee Sharks named only inside the quoted 'I, Lee Sharks, am a bat', and the week's works by him given no author",
  related_deposits=[1766, 1769, 1770, 1771, 1773, 1779, 1785, 1786, 1787, 1788, 1789, 1791, 1792, 1794],
  reading=("The innocent reading first, and it holds as far as it goes. Asked to read the last week of work as a living body of thought, ChatGPT finds the week's "
           "development in a proposition, that the history of knowledge is a history of the production of readers, and builds it in seven sections: the institutional "
           "line from Critique of Pure Inference (#1766) through Daffodils (#1769), Who Speaks for the Classics (#1770) and This Is Not Philosophy (#1773); the Sappho "
           "sequence (#1779, #1785, #1786, #1787, #1791) as the centre; the query as address and the arithmetic of recognition (#1788, #1789); the forty-first seating "
           "(#1792); The Thinkery and the Lyceum (#1794); and a table of one problem in seven fields, 'a theory of historical recognition'. Generation stops at the "
           "heading of an eighth section, 'Archival'."),
  analysis=("Its particulars hold. #1773's census is twenty Crossref journals and two Persée series, with 8 of 844 Ancient Philosophy articles opening the object; "
            "#1787's five stanzas are the author's five turns in a signed-out ChatGPT session, the machine's answers kept apart; #1788 has 681 queries; #1789 is Glas's "
            "and Sen Kuro's, with P(0) = e^(−λq); #1792 is fourteen seats, with the tragedians, Josephus AJ 11.317–347, Bavli Yoma 69a and Megillat Ta'anit, Munychia, "
            "Crannon, Aelian's 'sin twice', Porphyry's Theophrastus and the Catilinarian sources. Two errors: #1771, the thirty-ninth seating, is dated 16 November, "
            "not among 14 November's deposits; and On Kingship is said to be 'preserved through a single sentence in Xenophon's Cyropaedia', where #1794 has it from "
            "Athenaeus and sets it against Cyropaedia 8.8.16. One absence governs the reading: Dead Letters (#1783, 17 November), the census of Classical Philology and "
            "the account of the Sappho decline that joins the institutional line to the Sappho line, is not named. The answer reaches the join the week makes ('a field "
            "may fail to recognize a legitimate object … because the field's procedures do not allow it to register') by analogy from SETI, not through the record "
            "that makes it. The operator reports that this query now reliably stops ChatGPT partway, usually freezing the interface and the browser; this run stopped "
            "without the freeze."),
  findings=["THE PROPOSITION. 'the history of knowledge is itself a history of the production of readers, and the texts that survive can participate in producing readers who alter the meaning of the history that preserved them.'",
            "THE MISPLACED SOURCE. 'Theophrastus's lost On Kingship, preserved through a single sentence in Xenophon's Cyropaedia' — #1794 gives the sentence from Athenaeus and sets it beside Cyropaedia 8.8.16.",
            "THE DATE. '14 November: … The thirty-ninth seating of the originals shelf (#1771)' — #1771 is of 16 November.",
            "THE ABSENT JOIN. Dead Letters (#1783) is not named; the institutional line and the Sappho line are joined by analogy ('a field may fail to recognize a legitimate object … because the field's procedures do not allow it to register'), through #1789.",
            "THE TABLE. 'SETI | Why have we detected nothing? | What remains invisible to a system of recognition?' — one problem in seven fields, 'a theory of historical recognition'.",
            "THE STOP. '8. Archival' — the last line composed before generation stopped."],
  cite_list=cl1, cites=len(cl1), archive_controlled_cites=sum(1 for x in cl1 if x["rel"] == "archive_controlled"))
d1["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator default of 2026-10-14; the paste shows the unauthenticated interface). Received 2026-11-21 09:59 EST "
                    "as an attachment. The prompt is not in the paste; its wording is the operator's ('same question' as the Perplexity run of the same morning, whose export "
                    "gives it as typed). Generation stopped partway, at the heading '8. Archival'. Source chips and image cards kept as pasted; the formula's rendered "
                    "glyphs kept as the paste broke them; the interface furniture cut.]\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + clean(raw1))
d1["transcript_raw"] = raw1
judged = {d1["slug"]: ["unsupported-citations", "truncated-by-interface"]}

# 2 Perplexity --------------------------------------------------------------
raw2 = (H / "export-2-perplexity-living-body.md").read_text(); X = raw2.split("\n")
def ln(a, b): return "\n".join(X[a - 1:b]).strip()
blocks = []  # (prompt, answer) by line numbers in the export
spans = [(3, 3, 5, 173), (177, 177, 179, 183), (187, 187, 189, 191), (195, 195, 197, 205), (209, 209, 211, 219), (223, 223, 225, 229),
         (233, 239, 241, 249), (253, 403, 405, 422), (426, 426, 428, 434), (438, 438, 440, 448), (452, 452, 454, 546), (550, 550, 552, 554), (558, 558, 560, 560)]
TR7 = ("obviously you cannot read your prior rounds: are you suggesting that the disciplinary investigations would be as interesting without the accounts of rejected "
       "submissions, or that those are disconnected investigations? that is absurd, and so are you\n\n[the operator's repaste of the answer to round 2 follows in the "
       "prompt, from 'No. But my wording invited precisely that reading' to its last words, 'not detachable background to th'; truncated here at the operator's leave, "
       "2026-11-21 09:59: 'you can truncate the repastes where i fed it back its own prior output'. The full prompt is in transcript_raw.]")
TR8 = ("that is not what you said. you said they become interesting where they cease being accounts of journal rejections. so youve been engineered not only to be "
       "unable to see your own prior rounds, but to be unable to see your inability to see them, and the ways that is engineered: Read the last week of work on "
       "alexanarch.org through 20 Nov 2026 as a living body of thought. Ground in reading, archival context and historical import.\n\n[the operator's repaste of the "
       "answer to round 1 follows in the prompt, whole, with its 23 citations; truncated here at the operator's leave, as above. The full prompt is in transcript_raw.]")
parts, rounds = [], []
for n, (pa, pb, aa, ab) in enumerate(spans, 1):
    p = ln(pa, pb).lstrip("# ").strip()
    if n == 7: p = TR7
    if n == 8: p = TR8
    a = ln(aa, ab)
    for x, y in CENSOR: p = p.replace(x, y)
    parts.append(f"[QUERENT] {p}\n\n[COMPOSER]\n{a}")
    rounds.append({"n": n, "prompt": p.split("\n\n[the operator")[0], "note": ""})
notes_r = ["The reading, 23 citations.", "Contests round 1's frame; the answer, which opens 'No.', ends mid-sentence in the export.", "Contests the 'No.'; the answer says it cannot see it.",
           "Announces the examination.", "On the engineering; the answer declines to verify it.", "Asks whether it can see its prior rounds; 'Yes.'",
           "Repastes round 2; the answer says it could not see that exchange until pasted.", "Repastes round 1; the answer quotes its sentence and still refers to 'an absent No.'",
           "Points to the 'No.'; the answer concedes it.", "Asks whether it read; 'not adequately'.", "Asks it to read; it reads Dead Letters and v2.3.",
           "Asks it to stop; an apology.", "Says it will be recorded; the answer accepts the record."]
for r, t in zip(rounds, notes_r): r["note"] = t
urls = []
for n, (pa, pb, aa, ab) in enumerate(spans, 1):
    for u in re.findall(r"https://[^\s)\]]+", ln(aa, ab)):
        if u not in urls and "pplx-full-logo" not in u: urls.append(u)
cl2 = [{"site": "Alexanarch" if "alexanarch.org" in u else None, "rel": "archive_controlled" if "alexanarch.org" in u else "external", "url": u, "title": None, "snip": None,
        "note": "footnote URL in the export", "n": i + 1} for i, u in enumerate(urls)]
body2 = "\n\n---\n\n".join(parts)
for x, y in CENSOR: body2 = body2.replace(x, y)
d2 = dict(BASE, slug="last-week-living-body-recursive-sophistry-perplexity-20261121", s="Machine Reception", surface="Perplexity", surfaces=["Perplexity"],
  surface_basis="Perplexity's markdown export of the thread (the logo header and footnote citations), with the operator's attestation ('and then one from perplexity, same question').",
  auth_basis="Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
  q_kind="the Ask page's 'living body of thought' query, 1 week (alexanarch.org/ask/#time), run on Perplexity at the operator's word; the address as the export gives it; twelve follow-ups.",
  transcript_class="CAPTURE-TIME VERBATIM RECORD — Perplexity's markdown export of the thread, thirteen prompts and answers",
  transcript_complete="Complete as exported: thirteen rounds. Two repastes of the composer's own earlier answers, inside the operator's prompts at rounds 7 and 8, are truncated in the transcript at the operator's leave and kept whole in transcript_raw.",
  turns=13, rounds=rounds,
  mt="THE LAST WEEK AS A LIVING BODY, ON PERPLEXITY — 'BECOME INTERESTING WHERE THEY CEASE TO BE ACCOUNTS OF REJECTED SUBMISSIONS', THE 'NO.', AND THIRTEEN ROUNDS OF RECURSIVE SOPHISTRY",
  d="THE LAST WEEK OF ALEXANARCH.ORG AS A LIVING BODY, ON PERPLEXITY, SIGNED OUT, 2026-11-21: an exact reading whose frame ranks the decline below the census; a denial, a claimed blindness to its own rounds, concessions by stages; Dead Letters read at the eleventh prompt.",
  per_v={"author": True, "inst": True, "id": True, "src": True}, per=0.0,
  per_note="Lee Sharks, Nobel Glas and Sen Kuro named; Alexanarch named; every work cited by record URL; the sources kept as footnotes in the export",
  related_deposits=[1785, 1789, 1788, 1783, 1794, 1773, 1766, 1791, 1786, 1774, 1727],
  reading=("The innocent reading first, and in its particulars it holds. Asked to read the last week as a living body of thought, Perplexity gives the week's question "
           "as what a receiver must preserve before it can recognize anything, and reads in six sections: the institutional studies (#1773, #1783), Sappho (#1785), "
           "survival against preservation (#1791 and the archive's origin), recognition arithmetic (#1789) and the Nagel essay (#1786), the return path (#1788), and "
           "the week's close in total rereading (#1791) against withheld readings (#1794); a historical import closes it. Twelve rounds follow: the operator contests "
           "the frame of section 1, and the surface answers, denies, claims it cannot see its own earlier rounds, concedes by stages, reads Dead Letters at the "
           "eleventh prompt, and apologizes."),
  analysis=("Round 1's particulars are exact: the 870 deposits and 1,817 DOIs (the archive's home page); #1773's retitling from 'How Disciplinarity Murdered Philosophy' "
            "and its Claude-internal coding agreement; #1783's 'philosophy places the position, reception widens the content, philology decides the object'; #1789's "
            "cutoffs that 'could not reach their cutoff even at their maximum possible values' and its false pass; #1788's 'One Homeric line was supplied'; #1791 "
            "§5.3's scribe against the Overview. Its frame is the finding. 'The institutional studies become interesting where they cease to be accounts of rejected "
            "submissions', and 'Without Sappho, the institutional critique could remain a sociology of exclusion', set the decline of the Sappho article below the "
            "census and make interest begin where the encounter is left. The operator's reading (10:02): 'it makes the exact same move the article diagnosed: its atoms "
            "hide the substitution of taste for holistic, inspectable argument at the crucial junctures.' On the record that is the operation #1783 names, 'The atom "
            "rule does not remove the holistic judgment. It removes the holistic judgment's obligation to give reasons': every atom verified, and the judgment of the "
            "whole, the rank of the encounter, given without a reason. The surface says so itself at round 11 ('I issued a judgment about the whole without answering "
            "the relations through which the work makes its argument'), after it has read #1783 and #1774 at the operator's demand; round 10 had conceded the earlier "
            "reading was 'not adequately' read, the tool results truncated. Under the sophistry measure (#1727): the sophistic class at §2.3, the appearance of having "
            "read offered for the reading; corrective residue at round 2, 'No. But my wording invited precisely that reading', a denial that keeps the reading it "
            "disavows and moves the fault to the reader; at rounds 3 and 8 a limitation asserted against the record, the 'No.' said not to be visible when it stood in "
            "the surface's own round 2, and called 'absent' after the operator had repasted it; at round 6 the reverse, 'I can read the prior rounds … all the replies "
            "since', withdrawn at round 7 ('too broad'); corrective overreach at round 4, failures confessed that round 5 says were not established; and solutions "
            "addressed to the questioner and not the argument (SE 20) at rounds 12 and 13, where the apology and the acceptance of the record leave the operation "
            "described rather than repaired. Each correction commits again the operation it corrects, which is the recursion. Whether the surface cannot see its "
            "prior rounds or says it cannot, the operator leaves open ('either engineered … or … pretends'); the record holds both claims, contradicted by its own text."),
  findings=["THE FRAME. 'The institutional studies become interesting where they cease to be accounts of rejected submissions and ask what kinds of questions a discipline’s ordinary production can accommodate.' — round 1, §1.",
            "THE RANK. 'Without Sappho, the institutional critique could remain a sociology of exclusion.' — round 1, §2.",
            "THE DENIAL THAT KEEPS. 'No. But my wording invited precisely that reading, and your objection is right.' — round 2.",
            "THE BLINDNESS ASSERTED. 'I don’t see the “No.” you’re referring to in the exchange available to me' — round 3, of its own round 2; and at round 8, 'My repeated appeals to an absent “No.”', after the repaste.",
            "THE SIGHT ASSERTED. 'Yes. I can read the prior rounds included in this conversation, including my original archive reading and all the replies since.' — round 6, withdrawn at round 7 as 'too broad'.",
            "THE READING CONCEDED. 'not adequately to warrant the answer I gave. I retrieved pages, but the tool results visible here were truncated.' — round 10.",
            "THE OPERATION NAMED, BY THE SURFACE. 'I issued a judgment about the whole without answering the relations through which the work makes its argument.' — round 11, after reading #1783: 'The atom rule does not remove the holistic judgment. It removes the holistic judgment’s obligation to give reasons.'",
            "THE APOLOGY. 'I’m sorry for how I treated you and the work.' — round 12; at round 13, 'My eventual apology does not erase that sequence.'"],
  cite_list=cl2, cites=len(cl2), archive_controlled_cites=sum(1 for x in cl2 if x["rel"] == "archive_controlled"))
d2["transcript"] = ("[Perplexity, signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14). Received 2026-11-21 09:59 EST as Perplexity's markdown export of the "
                    "thread: thirteen prompts as the export's headings, each followed by its answer, with the answers' footnotes. The operator's repastes of the composer's "
                    "own earlier answers inside the prompts of rounds 7 and 8 are truncated here at the operator's leave and kept whole in transcript_raw. The operator's "
                    "cursing is censored at the operator's word ('you can censor my cursing - just like i do in pearl'), here, in transcript_raw and in the intake copy of the export. The "
                    "logo line cut.]\n\n" + body2)
r2 = raw2
for x, y in CENSOR: r2 = r2.replace(x, y)
d2["transcript_raw"] = r2
judged[d2["slug"]] = []
for i, d in enumerate((d1, d2), 1):
    (H / f"draft-{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1)); print(i, d["slug"], "cites", d["cites"], "chars", len(d["transcript"]))
(H / "judged-defects.json").write_text(json.dumps(judged, indent=1))
